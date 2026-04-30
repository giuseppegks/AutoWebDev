"""oozo.nl parser — activity check + KvK + founding date + employee count.

Critical use-case: detect inactive businesses BEFORE we render a mockup
that would embarrass us in a pitch. Oud-West case from Lange Hezelstraat:
"Dit bedrijf is niet langer actief" — must catch this every time.

Returns:
    {
      "site": "oozo.nl",
      "url": "...",
      "data": {
        "is_active": {"value": True/False, "confidence": "high", ...},
        "kvk": {"value": "75985691", ...},
        "founding_date": {"value": "maart 2015", ...},
        "employee_count": {"value": "1 persoon", ...},
        "category": {"value": "Haarverzorging", ...},
      },
      "warnings": [...]
    }
"""

from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import Optional, Dict, Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fetch import safe_fetch, site_search


SITE = "oozo.nl"

# Pre-compiled patterns — kept simple & robust against minor markup churn
RE_INACTIVE  = re.compile(r"niet\s+langer\s+actief", re.IGNORECASE)
RE_ACTIVE    = re.compile(r"\bis\s+actief\b", re.IGNORECASE)
RE_KVK       = re.compile(r"kvk\s*nummer\s*:?\s*(\d{6,9})", re.IGNORECASE)
RE_FOUNDED   = re.compile(r"[Oo]pgericht\s+(?:in\s+)?([\w\s]+\d{4})", re.IGNORECASE)
RE_EMPLOYEES = re.compile(r"(?:was\s+)?(\d+)\s+pers(?:oon|onen)\s+werkzaam", re.IGNORECASE)
RE_CATEGORY  = re.compile(r"branche\s+([\w\s\-]+?)(?:\.|,|<)", re.IGNORECASE)
RE_ADDRESS   = re.compile(r"gevestigd\s+op\s+([^<\.]{5,80})", re.IGNORECASE)


def find_listing_url(name: str, city: str) -> Optional[str]:
    """Use Brave/DDG to discover the oozo listing URL."""
    query = f"{name} {city}"
    urls = site_search(query, site=SITE, max_results=8)
    for u in urls:
        if "/bedrijven/" in u and re.search(r"/\d{4,}/", u):
            return u
    return None


def parse(name: str, city: str, *, listing_url: Optional[str] = None) -> Dict[str, Any]:
    """Parse oozo for a shop. Activity check is the most important field."""
    result: Dict[str, Any] = {
        "site": "oozo.nl",
        "url": None,
        "data": {},
        "warnings": [],
    }

    url = listing_url or find_listing_url(name, city)
    if not url:
        result["warnings"].append(f"oozo: no listing found for '{name}' in {city}")
        return result
    result["url"] = url

    html = safe_fetch(url)
    if not html:
        result["warnings"].append(f"oozo: fetch failed for {url}")
        return result

    def field(key, value, *, confidence="high"):
        if value is not None and value != "":
            result["data"][key] = {
                "value": value,
                "source_url": url,
                "confidence": confidence,
            }

    # ACTIVITY CHECK — top priority. Inactive marker beats active fallback.
    if RE_INACTIVE.search(html):
        field("is_active", False, confidence="high")
        result["warnings"].append("⚠️  INACTIVE business — do NOT generate mockup")
    elif RE_ACTIVE.search(html):
        field("is_active", True, confidence="medium")  # heuristic, not as strong as inactive marker
    else:
        result["warnings"].append("oozo: no clear active/inactive marker found")

    # KvK
    m = RE_KVK.search(html)
    if m:
        field("kvk", m.group(1))

    # Founding date — preserve human format ("maart 2015")
    m = RE_FOUNDED.search(html)
    if m:
        founding = m.group(1).strip()
        field("founding_date", founding)
        # Try to extract just the year as int for since_year usage
        year_match = re.search(r"(\d{4})", founding)
        if year_match:
            field("founding_year", int(year_match.group(1)))

    # Employee count
    m = RE_EMPLOYEES.search(html)
    if m:
        n = int(m.group(1))
        field("employee_count", n)

    # Category / branche (e.g. "Haarverzorging")
    m = RE_CATEGORY.search(html)
    if m:
        field("category", m.group(1).strip())

    # Verbatim address line
    m = RE_ADDRESS.search(html)
    if m:
        field("address_line", m.group(1).strip(), confidence="medium")

    return result


# CLI
if __name__ == "__main__":
    import json
    from fetch import enable_cache

    enable_cache()
    name = sys.argv[1] if len(sys.argv) > 1 else "Kaashandel De Wit"
    city = sys.argv[2] if len(sys.argv) > 2 else "Nijmegen"

    # Allow direct URL via env-var or 3rd arg
    direct = sys.argv[3] if len(sys.argv) > 3 else None
    result = parse(name, city, listing_url=direct)
    print(json.dumps(result, indent=2, ensure_ascii=False))
