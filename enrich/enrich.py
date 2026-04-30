"""enrich.py — orchestrator: prospect-row → enriched dict with confidence flags.

Input contract (one shop):
    {"name": "Kaashandel De Wit", "city": "Nijmegen", "addr_hint": "Lange Hezelstraat 11"}
    Plus optional pre-discovered URLs (skip search):
    {"telefoonboek_url": "...", "oozo_url": "..."}

Output contract:
    {
      "input": {...},
      "status": "ready" | "needs_review" | "skip-inactive" | "skip-no-data",
      "data": {                  # consolidated, deduplicated
        "tel": {"value": ..., "source": ..., "confidence": ...},
        "address": {"street": ..., "postcode": ..., "city": ...},
        "kvk": ..., "founding_year": ..., "category": ..., "rating": ...,
        "is_active": ...,
      },
      "sources": ["telefoonboek.nl", "oozo.nl"],
      "warnings": [...],
    }

Order of operations:
1. oozo  → activity check first; if inactive → STOP (skip-inactive)
2. telefoonboek → tel + adres + microdata
3. Future sessions: wanderlog (reviews), verify-step (DDG/Brave), pexels (photos)

Honesty: every field carries a source URL. Missing > invented.
"""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parsers import telefoonboek, oozo, wanderlog, verify  # noqa: E402


def enrich(
    name: str,
    city: str,
    *,
    addr_hint: Optional[str] = None,
    telefoonboek_url: Optional[str] = None,
    oozo_url: Optional[str] = None,
    wanderlog_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Run the parsers and return a consolidated enrichment record."""
    out: Dict[str, Any] = {
        "input": {"name": name, "city": city, "addr_hint": addr_hint},
        "status": "ready",
        "data": {},
        "sources": [],
        "warnings": [],
    }

    # 0. WANDERLOG (when listed) — gold mine: gives website, rating(google), tel,
    #    AND verbatim reviews in one fetch. Run first because it determines verify-status.
    print(f"  → wanderlog: rich data + reviews for {name}…")
    w = wanderlog.parse(name, city, listing_url=wanderlog_url)
    if w["url"]:
        out["sources"].append("wanderlog.com")
    out["warnings"].extend(w["warnings"])
    for k, v in w["data"].items():
        out["data"][k] = v

    # If wanderlog gave us a website, this shop ALREADY has online presence
    # → mark for skip (downstream pipeline can decide pitch-mode: refresh vs. new)
    if "website" in out["data"]:
        out["data"]["has_site"] = {
            "value": True,
            "source_url": out["data"]["website"]["source_url"],
            "confidence": "high",
        }

    # 1. ACTIVITY CHECK FIRST — saves the rest of the work for inactive businesses
    print(f"  → oozo: activity check for {name}…")
    o = oozo.parse(name, city, listing_url=oozo_url)

    # Wrong-business safeguard: when search found a listing, verify the address
    # matches the addr_hint. Different businesses can share names — without this
    # check we'd happily accept a 2021 restaurant as the active version of a
    # vinyl shop. (Lesson from Vinylarchief test.)
    if o["url"] and addr_hint and "address_line" in o["data"]:
        addr_line = o["data"]["address_line"]["value"].lower()
        # Match: at least one substantial word of addr_hint should appear in oozo's address
        hint_words = [w for w in addr_hint.lower().split() if len(w) >= 4 and not w.isdigit()]
        if hint_words and not any(w in addr_line for w in hint_words):
            out["warnings"].append(
                f"oozo: address mismatch — input '{addr_hint}' vs oozo '{addr_line[:60]}'. "
                "Likely wrong business with same name. Discarding oozo data."
            )
            o = {"site": "oozo.nl", "url": None, "data": {}, "warnings": o["warnings"]}

    if o["url"]:
        out["sources"].append("oozo.nl")
    out["warnings"].extend(o["warnings"])

    is_active_field = o["data"].get("is_active")
    if is_active_field and is_active_field["value"] is False:
        out["status"] = "skip-inactive"
        out["data"]["is_active"] = is_active_field
        # Still copy KvK + founding date for record-keeping
        for k in ("kvk", "founding_date", "founding_year"):
            if k in o["data"]:
                out["data"][k] = o["data"][k]
        print(f"  ❌ INACTIVE — skipping rest of pipeline")
        return out

    # Active or unknown — collect everything from oozo
    for k, v in o["data"].items():
        out["data"][k] = v

    # 2. Telefoonboek — tel + microdata
    print(f"  → telefoonboek: facts for {name}…")
    t = telefoonboek.parse(name, city, listing_url=telefoonboek_url)
    if t["url"]:
        out["sources"].append("telefoonboek.nl")
    out["warnings"].extend(t["warnings"])

    # Merge — telefoonboek wins for tel/adres (more reliable than oozo's text-line parse).
    # But don't overwrite wanderlog's tel (Google-sourced, normalized).
    for k, v in t["data"].items():
        if k == "founding_date" and "founding_date" in out["data"]:
            continue
        if k == "tel" and "tel" in out["data"] and out["data"]["tel"]["confidence"] == "high":
            continue  # wanderlog has it from Google
        out["data"][k] = v

    # 3. Optional verify-step (only when no wanderlog → fall back to search)
    if "has_site" not in out["data"]:
        print(f"  → verify: search-fallback for {name}…")
        v_result = verify.parse(name, city)
        if v_result.get("has_site") is not None:
            out["data"]["has_site"] = {
                "value": v_result["has_site"],
                "source_url": v_result.get("url") or "brave-search",
                "confidence": "medium",  # search-derived, less reliable than wanderlog
            }
        out["warnings"].extend(v_result.get("warnings", []))
        if v_result.get("has_site"):
            out["data"]["website"] = {
                "value": v_result["url"],
                "source_url": "brave-search",
                "confidence": "medium",
            }

    # 4. Decide final status
    has_tel = "tel" in out["data"]
    has_address = "street" in out["data"]
    has_active_check = "is_active" in out["data"]
    has_existing_site = out["data"].get("has_site", {}).get("value") is True

    if has_existing_site:
        out["status"] = "has-site"
    elif not (has_tel or has_address):
        out["status"] = "skip-no-data"
        out["warnings"].append("No tel and no address found — likely wrong listing or shop not indexed")
    elif not has_active_check:
        out["status"] = "needs_review"
        out["warnings"].append("No clear activity confirmation — manual check recommended")
    elif not has_tel:
        out["status"] = "needs_review"
        out["warnings"].append("No phone number found")

    return out


# ---------------------------------------------------------------------------
# Pretty-printer for terminal review
# ---------------------------------------------------------------------------
STATUS_ICON = {
    "ready": "✅",
    "needs_review": "⚠️ ",
    "skip-inactive": "❌",
    "skip-no-data": "❓",
    "has-site": "🌐",
}


def print_summary(record: Dict[str, Any]) -> None:
    inp = record["input"]
    icon = STATUS_ICON.get(record["status"], "•")
    print(f"\n{icon}  {inp['name']} ({inp['city']})  →  {record['status']}")
    if record["data"]:
        d = record["data"]
        if "tel" in d:           print(f"     tel:    {d['tel']['value']}")
        if "street" in d:        print(f"     adres:  {d['street']['value']} {d.get('postcode', {}).get('value','')}".rstrip())
        if "founding_year" in d: print(f"     sinds:  {d['founding_year']['value']} ({d.get('founding_date',{}).get('value','')})")
        if "kvk" in d:           print(f"     KvK:    {d['kvk']['value']}")
        if "category" in d:      print(f"     branche:{d['category']['value']}")
        if "is_active" in d:
            active = "actief" if d["is_active"]["value"] else "INACTIEF"
            print(f"     status: {active}")
        if "rating" in d:
            r = d["rating"]["value"]
            print(f"     rating: {r['score']}/{r['max']} op {r['count']} beoordelingen ({r['source']})")
        if "website" in d:
            print(f"     site:   {d['website']['value']}")
        if "reviews" in d:
            n = len(d["reviews"]["value"])
            print(f"     reviews:{n} verbatim quotes (wanderlog)")
    if record["warnings"]:
        for w in record["warnings"]:
            print(f"     ⚠ {w}")
    if record["sources"]:
        print(f"     sources: {' + '.join(record['sources'])}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import json
    from fetch import enable_cache

    enable_cache()
    if len(sys.argv) < 3:
        print("Usage: python3 enrich.py 'Shop Name' 'City' [--json]")
        sys.exit(1)

    name = sys.argv[1]
    city = sys.argv[2]
    rec = enrich(name, city)
    if "--json" in sys.argv:
        print(json.dumps(rec, indent=2, ensure_ascii=False))
    else:
        print_summary(rec)
