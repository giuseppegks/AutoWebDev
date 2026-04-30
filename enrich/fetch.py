"""Shared HTTP helper — realistic UA, rate-limit, retry, friendly to host servers.

We zijn een gast op andermans server; respect en geduld eerst.
"""

from __future__ import annotations
import time
import random
import urllib.request
import urllib.parse
import urllib.error
import gzip
import io
from typing import Optional, Dict
from pathlib import Path

UA_POOL = [
    # Recent, realistic Mac UAs — we zijn niet stiekem maar ook geen 'Python-urllib/3.11'
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

DEFAULT_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# Per-host minimum interval between requests (seconds)
RATE_LIMIT: Dict[str, float] = {
    "telefoonboek.nl": 2.0,
    "oozo.nl":          2.0,
    "wanderlog.com":    2.0,
    "leuketip.com":     2.0,
    "denijmegengids.nl":2.0,
    "duckduckgo.com":   3.0,   # extra cautious — they rate-limit hard
    "html.duckduckgo.com": 3.0,
    "search.brave.com": 3.0,   # be polite, also rate-limit-prone
    "default":          1.5,
}

_last_hit: Dict[str, float] = {}


class FetchError(Exception):
    pass


def _host_of(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.replace("www.", "")


def _wait_for_host(host: str) -> None:
    """Sleep so we never hit a host more often than RATE_LIMIT allows."""
    interval = RATE_LIMIT.get(host, RATE_LIMIT["default"])
    last = _last_hit.get(host, 0.0)
    elapsed = time.time() - last
    if elapsed < interval:
        time.sleep(interval - elapsed + random.uniform(0.1, 0.4))  # add jitter
    _last_hit[host] = time.time()


def fetch(
    url: str,
    *,
    timeout: int = 15,
    retries: int = 2,
    extra_headers: Optional[Dict[str, str]] = None,
) -> str:
    """GET a URL → return decoded HTML (str). Raises FetchError on failure.

    Respects per-host rate limits, sets realistic UA + Accept headers,
    handles gzip, retries once on 5xx / network errors.
    """
    host = _host_of(url)
    _wait_for_host(host)

    headers = dict(DEFAULT_HEADERS)
    headers["User-Agent"] = random.choice(UA_POOL)
    if extra_headers:
        headers.update(extra_headers)

    last_err: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                # Decompress gzip if applicable
                if resp.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
                # Try utf-8 first, fall back to latin-1 (Dutch sites mostly utf-8)
                for enc in ("utf-8", "latin-1"):
                    try:
                        return raw.decode(enc)
                    except UnicodeDecodeError:
                        continue
                return raw.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise FetchError(f"404 Not Found: {url}")
            if 500 <= e.code < 600 and attempt < retries:
                time.sleep(2 ** attempt)
                last_err = e
                continue
            raise FetchError(f"HTTP {e.code}: {url}")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last_err = e
            if attempt < retries:
                time.sleep(2 ** attempt)
                continue
            raise FetchError(f"Network error fetching {url}: {e}")

    raise FetchError(f"Exhausted retries for {url}: {last_err}")


# ---------------------------------------------------------------------------
# Caching layer (optional, but recommended during development to be kind to hosts)
# ---------------------------------------------------------------------------
_cache_dir: Optional[Path] = None


def enable_cache(directory: str = "~/.cache/autowebdev-enrich") -> None:
    global _cache_dir
    _cache_dir = Path(directory).expanduser()
    _cache_dir.mkdir(parents=True, exist_ok=True)


def _cache_key(url: str) -> Path:
    if _cache_dir is None:
        raise RuntimeError("Cache not enabled; call enable_cache() first.")
    safe = urllib.parse.quote(url, safe="")[:200]
    return _cache_dir / f"{safe}.html"


def fetch_cached(url: str, *, max_age_seconds: int = 3600 * 24, **kwargs) -> str:
    """Like fetch() but serves from disk cache if recent."""
    if _cache_dir is None:
        return fetch(url, **kwargs)

    path = _cache_key(url)
    if path.exists() and (time.time() - path.stat().st_mtime) < max_age_seconds:
        return path.read_text(encoding="utf-8", errors="replace")

    html = fetch(url, **kwargs)
    path.write_text(html, encoding="utf-8")
    return html


# ---------------------------------------------------------------------------
# Convenience wrapper for parsers
# ---------------------------------------------------------------------------
def safe_fetch(url: str, **kwargs) -> Optional[str]:
    """Returns HTML string or None on any error. Logs error to stderr."""
    try:
        return fetch_cached(url, **kwargs) if _cache_dir else fetch(url, **kwargs)
    except FetchError as e:
        import sys
        print(f"  ⚠️  fetch failed: {e}", file=sys.stderr)
        return None


def site_search(query: str, *, site: str, max_results: int = 5) -> list[str]:
    """Search the web for `site:<site> <query>` and return clean target URLs.

    Brave Search is primary (scrape-friendly, fast), DuckDuckGo HTML is fallback.
    Returns deduped, in-domain URLs. Empty list on failure.

    Used by parsers to discover their listing URL when no direct API exists.
    """
    import re
    full_query = f"site:{site} {query}"

    # Try Brave first — most reliable, no captchas at low volume
    brave_url = f"https://search.brave.com/search?q={urllib.parse.quote_plus(full_query)}"
    try:
        html = fetch(brave_url)
        pattern = re.compile(rf'href="(https?://[^"]*{re.escape(site)}[^"]+)"')
        seen = set()
        results = []
        for m in pattern.finditer(html):
            url = m.group(1)
            # Filter: must be within the target site
            if site not in url:
                continue
            if url in seen:
                continue
            seen.add(url)
            results.append(url)
            if len(results) >= max_results:
                break
        if results:
            return results
    except FetchError:
        pass

    # Fallback: DuckDuckGo HTML endpoint
    ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote_plus(full_query)}"
    try:
        html = fetch(ddg_url)
        pattern = re.compile(r'uddg=([^&"]+)')
        seen = set()
        results = []
        for m in pattern.finditer(html):
            target = urllib.parse.unquote(m.group(1))
            if site not in target:
                continue
            if target in seen:
                continue
            seen.add(target)
            results.append(target)
            if len(results) >= max_results:
                break
        return results
    except FetchError:
        return []


# Backwards alias
ddg_site_search = site_search


if __name__ == "__main__":
    # Self-test
    enable_cache()
    print("Testing fetch on telefoonboek...")
    html = fetch_cached("https://www.telefoonboek.nl/")
    print(f"  ok, {len(html):,} chars")
    print("Cache hit?")
    t = time.time()
    html2 = fetch_cached("https://www.telefoonboek.nl/")
    print(f"  cached: {(time.time()-t)*1000:.1f}ms, {len(html2):,} chars")
    print("\nDDG site-search test...")
    urls = ddg_site_search("Kaashandel De Wit Nijmegen", site="telefoonboek.nl", max_results=3)
    for u in urls:
        print(f"  → {u}")
