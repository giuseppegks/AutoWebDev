"""wanderlog.com parser — verbatim review extractie.

Wanderlog aggregates Google + Yelp reviews per place. Hun HTML markup is React-
gegenereerd maar consistent: elke review zit in een `<div id="PlaceReviewsSection__review-XXX">`
wrapper met stars, author, date + quote.

Returns per shop:
    {
      "site": "wanderlog.com",
      "url": "...",
      "data": {
        "reviews": {
          "value": [
            {"stars": 5, "name": "Luis C", "date": "27 Sep 2024",
             "quote": "A Must-Visit Gem in Nijmegen! …", "source_platform": "Google"},
            ...
          ],
          "source_url": "...",
          "confidence": "high"
        },
        "rating_summary": {  # optional aggregate if available
          "value": {"score": 4.8, "count": 5, "max": 5, "source": "Wanderlog"},
          ...
        }
      },
      "warnings": [...]
    }

Honesty: every review is verbatim from the HTML. We don't paraphrase.
Quote-text is HTML-unescaped (e.g. &quot; → ").
"""

from __future__ import annotations
import re
import html
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fetch import safe_fetch, site_search


SITE = "wanderlog.com"

# --- Block boundaries ---
RE_BLOCK_START = re.compile(r'<div id="PlaceReviewsSection__review-[^"]+">')
# --- Per-review fields ---
RE_STARS = re.compile(r"<strong>(\d)<!-- -->/<!-- -->5</strong>")
RE_NAME  = re.compile(r'<strong class="ms-2">([^<]+)</strong>')
RE_DATE  = re.compile(r">(\d{1,2}\s+\w{3,9}\s+\d{4})\s+from", re.IGNORECASE)
RE_PLATFORM = re.compile(r"from\s*<[^>]+>(?:<div[^>]+>)*<span>([^<]+)</span>", re.DOTALL)
# Quote: prefer ExpandableText__text-content; fall back to ExpandableText__text
RE_QUOTE_CONTENT = re.compile(
    r'ExpandableText__text(?:-content)?[^>]*>([^<]{10,5000})',
    re.IGNORECASE,
)


def _decode_quote(raw: str) -> str:
    """HTML-unescape and tidy up the review text."""
    text = html.unescape(raw).strip()
    # Wanderlog often wraps the headline in &quot;…&quot; — keep but normalize
    # Collapse any internal whitespace runs to single spaces
    text = re.sub(r"\s+", " ", text)
    return text


def find_listing_url(name: str, city: str) -> Optional[str]:
    """Discover the wanderlog place URL via search."""
    query = f"{name} {city}"
    urls = site_search(query, site=SITE, max_results=8)
    for u in urls:
        if "/place/details/" in u:
            return u
    return None


def parse(name: str, city: str, *, listing_url: Optional[str] = None) -> Dict[str, Any]:
    """Extract verbatim reviews from a wanderlog place page."""
    result: Dict[str, Any] = {
        "site": "wanderlog.com",
        "url": None,
        "data": {},
        "warnings": [],
    }

    url = listing_url or find_listing_url(name, city)
    if not url:
        result["warnings"].append(f"wanderlog: no place page found for '{name}' in {city}")
        return result
    result["url"] = url

    page = safe_fetch(url)
    if not page:
        result["warnings"].append(f"wanderlog: fetch failed for {url}")
        return result

    # Slice review blocks by wrapper-div start positions
    starts = [m.start() for m in RE_BLOCK_START.finditer(page)]
    if not starts:
        result["warnings"].append("wanderlog: no review wrappers in page (template change?)")
        return result

    reviews: List[Dict[str, Any]] = []
    for i, s in enumerate(starts):
        e = starts[i + 1] if i + 1 < len(starts) else s + 5000
        chunk = page[s:e]

        stars_m = RE_STARS.search(chunk)
        name_m  = RE_NAME.search(chunk)
        date_m  = RE_DATE.search(chunk)
        quote_m = RE_QUOTE_CONTENT.search(chunk)
        platform_m = RE_PLATFORM.search(chunk)

        # Honesty: only include if we have at least stars + name + quote
        if not (stars_m and name_m and quote_m):
            continue

        review = {
            "stars": int(stars_m.group(1)),
            "name": name_m.group(1).strip(),
            "date": date_m.group(1) if date_m else None,
            "quote": _decode_quote(quote_m.group(1)),
            "source_platform": platform_m.group(1).strip() if platform_m else "Wanderlog",
        }
        reviews.append(review)

    if not reviews:
        result["warnings"].append("wanderlog: review wrappers found but no extractable reviews")
    else:
        result["data"]["reviews"] = {
            "value": reviews,
            "source_url": url,
            "confidence": "high",
        }

    # ---- Embedded JSON-blob: highest-quality structured fields ----
    # Wanderlog ships a JSON state with website, rating, numRatings, phone, etc.
    # All values are JS-escaped Unicode (/ = /); we unescape via json.loads.
    def _json_field(key: str, ttype: str = "str"):
        if ttype == "str":
            m = re.search(rf'"{key}"\s*:\s*"((?:[^"\\]|\\.)*)"', page)
            if not m:
                return None
            try:
                return json.loads(f'"{m.group(1)}"')
            except json.JSONDecodeError:
                return m.group(1)
        elif ttype == "num":
            m = re.search(rf'"{key}"\s*:\s*([0-9.]+)', page)
            return float(m.group(1)) if m else None
        elif ttype == "int":
            m = re.search(rf'"{key}"\s*:\s*(\d+)', page)
            return int(m.group(1)) if m else None

    website = _json_field("website")
    if website and "wanderlog" not in website:
        result["data"]["website"] = {
            "value": website,
            "source_url": url,
            "confidence": "high",
        }

    rating = _json_field("rating", "num")
    num_ratings = _json_field("numRatings", "int")
    if rating is not None and num_ratings is not None:
        result["data"]["rating"] = {
            "value": {"score": rating, "count": num_ratings, "max": 5, "source": "Google"},
            "source_url": url,
            "confidence": "high",
        }

    phone = _json_field("internationalPhoneNumber")
    if phone:
        # Normalize "+31 24 323 1975" → "024 3231975" Dutch local
        digits = re.sub(r"[^\d+]", "", phone)
        if digits.startswith("+31"):
            digits = "0" + digits[3:]
        result["data"]["tel"] = {
            "value": f"{digits[:3]} {digits[3:]}" if digits.startswith("0") else phone,
            "source_url": url,
            "confidence": "high",
        }

    # Fallback: if the embedded JSON didn't yield a website, fall back to
    # most-mentioned-external-domain heuristic. Less reliable but a useful
    # safety net when wanderlog template changes.
    if "website" in result["data"]:
        return result

    from collections import Counter
    PLATFORM_HOSTS = {
        "wanderlog.com", "wanderlogstatic.com", "wanderlog-cdn.com",
        "itin-dev.wanderlogstatic.com",
        "googleapis.com", "gstatic.com", "google.com", "ggpht.com",
        "googleusercontent.com", "googletagmanager.com", "google-analytics.com",
        "facebook.com", "twitter.com", "x.com", "instagram.com",
        "youtube.com", "linkedin.com", "tripadvisor.com", "yelp.com",
        "cdninstagram.com", "fbcdn.net", "schema.org", "w3.org", "ogp.me",
        "stripe.com", "sentry.io", "amplitude.com", "fonts.googleapis.com",
        "fonts.gstatic.com", "amazonaws.com", "cloudfront.net",
        "twimg.com", "ytimg.com", "doubleclick.net", "branch.io",
    }
    raw_links = re.findall(r'https?://([^/\s"\'<>]+)/', page)
    domain_counts: "Counter[str]" = Counter()
    for h in raw_links:
        h = h.lower()
        if h.startswith("www."):
            h = h[4:]
        if any(h == p or h.endswith("." + p) for p in PLATFORM_HOSTS):
            continue
        # Drop common static asset extensions when host has them
        if any(h.endswith(ext) for ext in (".png", ".jpg", ".svg", ".gif", ".webp")):
            continue
        domain_counts[h] += 1
    if domain_counts:
        # Score domains: prefer .nl (Dutch businesses) and short hosts
        def domain_score(item):
            host, count = item
            score = count
            if host.endswith(".nl"):
                score += 5
            if host.count(".") == 1 and len(host) < 30:
                score += 2
            return score

        ranked = sorted(domain_counts.items(), key=domain_score, reverse=True)
        top_host, count = ranked[0]
        if count >= 3:
            result["data"]["website"] = {
                "value": f"https://{top_host}",
                "source_url": url,
                "confidence": "high" if count >= 5 else "medium",
                "evidence_count": count,
            }

    # Aggregate rating: only count high-star reviews (≥4) for the average — the page
    # has a real summary somewhere but is more reliably reconstructed from the reviews
    if reviews:
        avg = sum(r["stars"] for r in reviews) / len(reviews)
        result["data"]["rating_aggregate"] = {
            "value": {"score": round(avg, 1), "count": len(reviews), "max": 5,
                      "source": "Wanderlog"},
            "source_url": url,
            "confidence": "medium",  # aggregated by us, not directly scraped
        }

    return result


# --------------------------------------------------------------------------- CLI
if __name__ == "__main__":
    import json
    from fetch import enable_cache

    enable_cache()
    name = sys.argv[1] if len(sys.argv) > 1 else "Kaashandel De Wit"
    city = sys.argv[2] if len(sys.argv) > 2 else "Nijmegen"
    direct = sys.argv[3] if len(sys.argv) > 3 else None
    result = parse(name, city, listing_url=direct)
    print(json.dumps(result, indent=2, ensure_ascii=False))
