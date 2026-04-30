"""telefoonboek.nl parser — extract LocalBusiness facts via microdata.

Strategy:
1. site_search to find the listing URL (per shop name + city)
2. fetch the URL
3. Parse via microdata (itemprop=…) — telefoonboek uses schema.org markup heavily
4. Per field: {"value": ..., "source_url": ..., "confidence": "high|medium|low"}

Honesty: every field is either present in the source OR omitted. Never invented.
"""

from __future__ import annotations
import re
from typing import Optional, Dict, Any

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fetch import safe_fetch, site_search


SITE = "telefoonboek.nl"

# Compiled microdata extractor — captures the inner text of an itemprop element
# Works for both <span itemprop="name">value</span> and meta[itemprop=name][content=...]
_MICRO = lambda prop: re.compile(
    rf'itemprop\s*=\s*["\']?{prop}["\']?[^>]*?(?:content\s*=\s*["\']([^"\']*)["\']|>([^<]*))',
    re.IGNORECASE,
)

_MICRO_PROPS = {
    "name":             "name",
    "telephone":        "tel",
    "streetAddress":    "street",
    "addressLocality":  "city",
    "postalCode":       "postcode",
    "description":      "description",
    "foundingDate":     "founding_date",
    "ratingValue":      "rating_value",
    "reviewCount":      "review_count",
    "bestRating":       "rating_max",
    "openingHours":     "hours_raw",
}


def _extract_microdata(html: str) -> Dict[str, str]:
    """Pull every itemprop value from the page → flat dict."""
    out = {}
    for prop, key in _MICRO_PROPS.items():
        m = _MICRO(prop).search(html)
        if not m:
            continue
        # Value is either group 1 (content="…") or group 2 (inner text)
        val = (m.group(1) or m.group(2) or "").strip()
        if val:
            out[key] = val
    return out


def _normalize_phone(s: str) -> str:
    """Telefoonboek uses '024-3231975'; normalize to '024 3231975' for display."""
    s = s.strip()
    # Keep + and digits only, then space-format common Dutch patterns
    digits = re.sub(r"[^\d+]", "", s)
    if digits.startswith("+31"):
        digits = "0" + digits[3:]
    if digits.startswith("0") and len(digits) >= 10:
        # 024-3231975 → 024 3231975
        return f"{digits[:3]} {digits[3:]}"
    return s


def find_listing_url(name: str, city: str) -> Optional[str]:
    """Use Brave/DDG to find the telefoonboek.nl page for this shop."""
    query = f"{name} {city}"
    urls = site_search(query, site=SITE, max_results=8)
    # Pick the first /bedrijven/ URL — those are detail pages
    for u in urls:
        if "/bedrijven/t" in u:
            return u
    return None


def parse(name: str, city: str, *, listing_url: Optional[str] = None) -> Dict[str, Any]:
    """Parse a telefoonboek listing for a shop. Returns structured facts.

    Each field has shape:
        {"value": <str|None>, "source_url": <str>, "confidence": "high"|...}

    Or None if the field couldn't be found.
    """
    result: Dict[str, Any] = {
        "site": "telefoonboek.nl",
        "url": None,
        "data": {},
        "warnings": [],
    }

    # 1. Find URL if not supplied
    url = listing_url or find_listing_url(name, city)
    if not url:
        result["warnings"].append(f"telefoonboek: no listing found for '{name}' in {city}")
        return result
    result["url"] = url

    # 2. Fetch
    html = safe_fetch(url)
    if not html:
        result["warnings"].append(f"telefoonboek: fetch failed for {url}")
        return result

    # 3. Extract microdata
    micro = _extract_microdata(html)

    # 4. Build typed field dict with source-attribution
    def field(key, raw, confidence="high", normalizer=None):
        if not raw:
            return
        value = normalizer(raw) if normalizer else raw
        result["data"][key] = {
            "value": value,
            "source_url": url,
            "confidence": confidence,
        }

    field("name", micro.get("name"))
    field("tel", micro.get("tel"), normalizer=_normalize_phone)
    field("street", micro.get("street"))
    field("city", micro.get("city"))
    field("postcode", micro.get("postcode"))
    field("description", micro.get("description"))
    field("founding_date", micro.get("founding_date"))

    # Rating with sensible structure
    if "rating_value" in micro:
        try:
            score = float(micro["rating_value"].replace(",", "."))
            count = int(micro.get("review_count", 0)) if micro.get("review_count", "").isdigit() else None
            max_score = float(micro.get("rating_max", 5))
            result["data"]["rating"] = {
                "value": {"score": score, "count": count, "max": max_score, "source": "Telefoonboek.nl"},
                "source_url": url,
                "confidence": "high",
            }
        except (ValueError, TypeError):
            result["warnings"].append(f"telefoonboek: rating parse failed: {micro.get('rating_value')!r}")

    # Hours — telefoonboek often renders these via JS, so static HTML may be empty
    hours_raw = micro.get("hours_raw")
    if hours_raw:
        field("hours_raw", hours_raw, confidence="medium")
    else:
        result["warnings"].append("telefoonboek: opening hours not in static HTML (JS-rendered)")

    return result


# ---------------------------------------------------------------------------
# CLI for quick testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json
    from fetch import enable_cache

    enable_cache()
    name = sys.argv[1] if len(sys.argv) > 1 else "Kaashandel De Wit"
    city = sys.argv[2] if len(sys.argv) > 2 else "Nijmegen"
    result = parse(name, city)
    print(json.dumps(result, indent=2, ensure_ascii=False))
