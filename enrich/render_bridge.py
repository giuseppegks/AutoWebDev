"""render_bridge.py — enriched.json → mockups via template_generator.

Workflow:
    1. Load enriched.json (output of batch_enrich.py)
    2. For each shop with status='ready' or 'needs_review' (and you've reviewed):
       - Auto-fill TARGET fields from enriched data
       - Auto-fill photos from Pexels (per branche)
       - Auto-fill testimonials from wanderlog reviews
       - Leave marketing copy (tagline_h1, lead, about_body) as PLACEHOLDER
         or use the --copy <copy.json> file to provide them
    3. Call template_generator.render_all() to write the mockups

Usage:
    # Auto-render with placeholder copy (raw structure preview)
    python3 render_bridge.py enriched.json --output sites/

    # With Claude/manual copy provided
    python3 render_bridge.py enriched.json --copy copy.json --output sites/

The copy.json format is a dict keyed by shop name (or row_number) with copy
fields:
    {
      "Kaashandel De Wit": {
        "tagline_h1": "Een Klever begrip — ...",
        "lead": "Op de hoek van de Lange Hezelstraat...",
        "about_heading": "Waar smaak begint met een goed gesprek",
        "about_body": "...",
        "services": [
          {"icon": "plate", "title": "Binnen- en buitenlandse kazen", "body": "..."},
          ...
        ]
      }
    }
"""

from __future__ import annotations
import json
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pexels  # noqa: E402

# Path to the building-prospect-mockups skill (template_generator.py)
SKILL_PATH = Path("~/.claude/skills/building-prospect-mockups").expanduser()


def _g(d: Dict[str, Any], key: str, default=None):
    """Safely get value from {value, source_url, confidence} field dict."""
    f = d.get(key)
    if isinstance(f, dict) and "value" in f:
        return f["value"]
    return default


def _wanderlog_to_testimonials(reviews: List[Dict[str, Any]], max_count: int = 4) -> List[Dict[str, Any]]:
    """Convert wanderlog reviews → animated_testimonials format.

    Filter: only 5-star reviews (high signal); cap at max_count.
    """
    high_star = [r for r in reviews if r.get("stars", 0) >= 4]
    out = []
    for r in high_star[:max_count]:
        platform = r.get("source_platform", "Google")
        date = r.get("date", "")
        designation = f"{platform}" + (f" · {date.lower()}" if date else "")
        if r.get("stars"):
            designation = f"{platform} · {r['stars']}/5" + (f" · {date.lower()}" if date else "")
        out.append({
            "name": r["name"],
            "designation": designation,
            "quote": r["quote"],
            "stars": r.get("stars", 5),
        })
    return out


PLACEHOLDER_TAGLINE = "[TAGLINE — Claude vult dit op basis van de feiten hieronder]"
PLACEHOLDER_LEAD    = "[LEAD — 2-3 zinnen intro op basis van branche + reviews + adres]"
PLACEHOLDER_ABOUT_BODY = "[ABOUT BODY — verhaal van het bedrijf, sinds-jaar, lokaal, etc.]"


def build_target(record: Dict[str, Any], *, copy: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Convert one enriched record to a TARGET dict for template_generator.

    Returns None if status disqualifies the record (skip-inactive, skip-no-data).
    """
    status = record.get("status", "")
    if status in ("skip-inactive", "skip-no-data"):
        return None

    inp = record["input"]
    data = record["data"]
    name = inp["name"]
    city = inp.get("city", "")
    branche = inp.get("branche", "")

    # Address — prefer parsed (telefoonboek street), else input addr
    street = _g(data, "street") or inp.get("addr", "")
    postcode = _g(data, "postcode")

    # Lat/lon must come from input (we don't auto-geocode)
    try:
        lat = float(inp.get("lat") or 0)
        lon = float(inp.get("lon") or 0)
    except (TypeError, ValueError):
        lat, lon = 0.0, 0.0

    target: Dict[str, Any] = {
        "name": name,
        "branche": branche,
        "city": city,
        "addr": street,
        "tel": _g(data, "tel") or inp.get("phone_hint", ""),
        "lat": lat, "lon": lon,
        "sources": record.get("sources", []),
    }

    # Optional structured fields
    since = _g(data, "founding_year")
    if since:
        target["since_year"] = since
    kvk = _g(data, "kvk")
    if kvk:
        target["kvk"] = kvk
    category = _g(data, "category")
    if category:
        target["category"] = category

    # WhatsApp from tel (mobile-format only — needs +country)
    tel = target["tel"]
    if tel and tel.lstrip().startswith(("06", "+316")):
        digits = "".join(c for c in tel if c.isdigit())
        if digits.startswith("06"):
            digits = "31" + digits[1:]
        if digits.startswith("316"):
            digits = "31" + digits[2:]
        target["whatsapp"] = digits

    # Email
    if "email" in data:
        target["email"] = _g(data, "email")
    if "email" in inp:
        target.setdefault("email", inp["email"])

    # Rating + testimonials
    rating = _g(data, "rating")
    if rating:
        target["rating"] = rating
    reviews_field = _g(data, "reviews", [])
    if reviews_field:
        testimonials = _wanderlog_to_testimonials(reviews_field)
        if testimonials:
            target["animated_testimonials"] = testimonials
            target["reviews_heading"] = "Klanten waarderen het persoonlijke advies"

    # Photos via Pexels
    if branche:
        photos = pexels.for_branche(branche)
        if photos:
            target.update(pexels.pick_for_template(photos))

    # Marketing copy — from copy-file or PLACEHOLDER
    copy_for_shop = (copy or {}).get(name) or (copy or {}).get(str(inp.get("row_number", "")), {})
    target["tagline_h1"]    = copy_for_shop.get("tagline_h1", PLACEHOLDER_TAGLINE)
    target["lead"]          = copy_for_shop.get("lead", PLACEHOLDER_LEAD)
    target["about_heading"] = copy_for_shop.get("about_heading", "Wat we doen")
    target["about_body"]    = copy_for_shop.get("about_body", PLACEHOLDER_ABOUT_BODY)
    # Optional CTA-strip overrides (sensible defaults in template_generator)
    for k in ("cta_eyebrow", "cta_heading", "cta_body"):
        if k in copy_for_shop:
            target[k] = copy_for_shop[k]
    if "services" in copy_for_shop:
        target["services"] = copy_for_shop["services"]
    else:
        # Skip rendering services if no copy — they need branche-specific words
        target["services"] = [
            {"icon": "smile", "title": "[SERVICE 1]", "body": "[Beschrijving]"},
            {"icon": "smile", "title": "[SERVICE 2]", "body": "[Beschrijving]"},
            {"icon": "smile", "title": "[SERVICE 3]", "body": "[Beschrijving]"},
        ]

    # Hours — convert Dutch day names if present (parser leaves them as-is)
    if "hours" in inp:
        target["hours"] = inp["hours"]

    return target


def render_from_enriched(
    enriched_path: Path,
    *,
    output_dir: str = "sites",
    base_dir: str = ".",
    copy_path: Optional[Path] = None,
    port: int = 8080,
    statuses: tuple = ("ready", "needs_review"),
) -> None:
    """Run the full enriched→render pipeline."""
    payload = json.loads(enriched_path.read_text())
    shops = payload["shops"]
    print(f"📋  Loaded {len(shops)} enriched shops from {enriched_path.name}")

    copy = json.loads(copy_path.read_text()) if copy_path else None
    if copy:
        print(f"📝  Loaded copy for {len(copy)} shops from {copy_path.name}")

    # Filter to renderable
    targets = []
    for r in shops:
        if r["status"] not in statuses:
            print(f"   ⏭  skip {r['input']['name']} ({r['status']})")
            continue
        t = build_target(r, copy=copy)
        if t:
            targets.append(t)

    if not targets:
        print("❌  No targets to render after filtering. Check enriched.json statuses.")
        return

    print(f"\n🎨  Rendering {len(targets)} mockup(s)...")

    # Import the generator from the skill
    sys.path.insert(0, str(SKILL_PATH))
    try:
        from template_generator import render_all  # type: ignore
    except ImportError as e:
        print(f"❌  Cannot import template_generator from {SKILL_PATH}: {e}")
        print(f"     Make sure the building-prospect-mockups skill is installed at that path.")
        sys.exit(1)

    render_all(targets=targets, output_dir=output_dir, base_dir=base_dir, port=port)
    print(f"\n✅  Done. Open http://127.0.0.1:{port}/{output_dir}/<shop-slug>/")


def main():
    ap = argparse.ArgumentParser(description="Render mockups from enriched.json")
    ap.add_argument("enriched", type=Path, help="enriched.json from batch_enrich.py")
    ap.add_argument("--output", default="sites", help="Output dir (default: sites)")
    ap.add_argument("--base-dir", default=".", help="Base dir (default: cwd)")
    ap.add_argument("--copy", type=Path, default=None,
                    help="Optional copy.json with marketing-copy per shop")
    ap.add_argument("--port", type=int, default=8080, help="Port for local URLs in output")
    ap.add_argument("--include-needs-review", action="store_true",
                    help="Also render shops with status=needs_review")
    args = ap.parse_args()

    statuses = ("ready",)
    if args.include_needs_review:
        statuses = ("ready", "needs_review")

    render_from_enriched(
        args.enriched,
        output_dir=args.output,
        base_dir=args.base_dir,
        copy_path=args.copy,
        port=args.port,
        statuses=statuses,
    )


if __name__ == "__main__":
    main()
