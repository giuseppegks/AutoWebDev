"""verify.py — does this shop already have a real website?

Output:
    {
      "has_site": True|False|None,
      "url": "https://kaashandeldewit.nl"  # if found, else None
      "candidates": [...all classified URLs...],
      "warnings": [...]
    }

Logic:
1. Brave search for `"<name>" <city>` (no site:filter)
2. Filter known-directory domains (telefoonboek, oozo, wanderlog, …)
3. Score remaining URLs: matches name-slug, has business name in path, host length
4. Top scoring URL = official site; if none qualifies → no site

Honesty: we return `has_site=None` if search fails (not False — never assume a
shop has no site just because we couldn't find one).
"""

from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import urllib.parse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fetch import fetch, FetchError


# Domains we KNOW are directories — never the official business site
DIRECTORY_DOMAINS = {
    "telefoonboek.nl", "detelefoongids.nl", "oozo.nl", "wanderlog.com",
    "leuketip.com", "denijmegengids.nl", "cylex.nl", "infobel.com",
    "nicelocal.co.nl", "nicelocal.nl", "yelp.com", "yelp.nl",
    "facebook.com", "instagram.com", "linkedin.com", "twitter.com", "x.com",
    "tiktok.com", "youtube.com", "pinterest.com",
    "google.com", "maps.google.com", "google.nl",
    "tripadvisor.com", "tripadvisor.nl", "foursquare.com",
    "openingstijden.nl", "openingstijden.com", "1kapper.nl",
    "kappers.nl", "kappersalons.nl", "salons.nl", "haar.expert",
    "dakdekkers.net", "dakdekkersgids.nl", "eendakdekker.nl",
    "offertesonline.nl", "werkspot.nl", "trustoo.nl",
    "drimble.nl", "kvk.nl", "openkvk.nl", "companyinfo.nl", "transfirm.nl",
    "shopgids.nl", "huisvoordebinnenstad.nl", "intonijmegen.com",
    "places.nl", "yellowpages.net", "wheree.com", "near-place.com",
    "sardaworld.com", "sardaglobal.com", "kickinoost.nl", "primagum.nl",
    "openalfa.nl", "iens.nl", "thuisbezorgd.nl",
    "findglocal.com", "openingstijden.com", "untappd.com", "brewver.com",
    "bestedakdekkers.nl", "kostendakdekker.nl", "dakdekker-gezocht.nl",
    "dakwerkennijmegen.nl", "evendo.com", "soamaps.com",
    "wonen­innijmegen.blog", "woneninnijmegen.blog", "nijmegenleeft.nl",
    "nijmegenspotted.com", "024nijmegen.nl", "nijmegen-024.nl", "nijmeegsglorie.nl",
    "kavariner.de", "mein-kleve.de", "kleve.de",
    "openingstijden.com", "openingstijden.nl", "open-closed.nl",
    "destreekoptafel.nl", "goodfoodclub.nu", "goudengids.nl",
    "spreaker.com", "blogspot.com", "wordpress.com",
    "nederlandsebiercultuur.nl", "vinylcrafts.nl", "noviomagus.nl",
    "openbare-inspectieresultaten.nvwa.nl", "bedrijvenmonitor.info",
    "verjaardagstaart.com", "ilovenijmegen024",
    "winkelcentrumdukenburg.nl", "huisinhetdorp.nl", "koopzondag-nijmegen.nl",
    "boekingen.org", "booking.page", "hifi.nl", "leuketip.nl", "followfox.nl",
    "winterhart.com",
}


def _slugify(s: str) -> str:
    """Normalize 'Kaashandel De Wit' → 'kaashandeldewit'."""
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def _score(url: str, business_name: str) -> int:
    """Higher = more likely the official site for this business.

    Components:
      +5  business slug appears in domain
      +3  business slug appears in path
      +2  short domain (single .nl/.com, no subdomain)
      -10 known directory
    """
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower().replace("www.", "")
    if any(host == d or host.endswith("." + d) for d in DIRECTORY_DOMAINS):
        return -10

    slug = _slugify(business_name)
    path = (parsed.path or "").lower()
    score = 0

    # First word of business name (most distinctive)
    main_word = re.split(r"\W+", business_name.lower(), maxsplit=1)[0]
    if len(main_word) >= 4 and main_word in host:
        score += 5
    if slug in host.replace(".", "").replace("-", ""):
        score += 5  # full-slug match in domain
    if main_word in path:
        score += 3
    # Short host = more likely to be the business's own domain
    if host.count(".") == 1 and len(host.split(".")[0]) <= 25:
        score += 2
    return score


def parse(name: str, city: str) -> Dict[str, Any]:
    """Search the web for this shop and classify the top results.

    Returns a verification record.
    """
    result: Dict[str, Any] = {
        "site": "verify",
        "has_site": None,
        "url": None,
        "candidates": [],
        "warnings": [],
    }

    query = f'"{name}" {city}'
    brave_url = f"https://search.brave.com/search?q={urllib.parse.quote_plus(query)}"
    try:
        html_text = fetch(brave_url)
    except FetchError as e:
        result["warnings"].append(f"verify: search failed — {e}")
        return result

    # Extract all external href URLs from search-results area
    raw_urls = re.findall(r'href="(https?://[^"]+)"', html_text)
    seen = set()
    candidates = []
    for u in raw_urls:
        # Skip Brave-internal & query-tracker links
        if "brave.com" in u or "search.brave" in u:
            continue
        # Drop the URL fragment + query string for dedup
        clean = u.split("#")[0]
        if clean in seen:
            continue
        seen.add(clean)
        candidates.append(clean)
        if len(candidates) >= 20:
            break

    if not candidates:
        result["warnings"].append("verify: no usable URLs in search results")
        return result

    # Score each candidate
    scored = sorted(
        [(c, _score(c, name)) for c in candidates],
        key=lambda x: x[1],
        reverse=True,
    )
    result["candidates"] = [
        {"url": c, "score": s, "is_directory": s == -10}
        for c, s in scored
    ]

    # Top candidate must score ≥ 5 (i.e. domain or path matches business name)
    if scored and scored[0][1] >= 5:
        result["has_site"] = True
        result["url"] = scored[0][0]
    else:
        # No clear official site found — but only state False if we had enough non-directory candidates
        non_dir_count = sum(1 for _, s in scored if s != -10)
        if non_dir_count >= 3:
            result["has_site"] = False
        else:
            result["warnings"].append(
                "verify: search returned mostly directory URLs — uncertain whether shop has own site"
            )

    return result


# --------------------------------------------------------------------------- CLI
if __name__ == "__main__":
    import json
    from fetch import enable_cache

    enable_cache()
    name = sys.argv[1] if len(sys.argv) > 1 else "Kaashandel De Wit"
    city = sys.argv[2] if len(sys.argv) > 2 else "Nijmegen"
    print(json.dumps(parse(name, city), indent=2, ensure_ascii=False))
