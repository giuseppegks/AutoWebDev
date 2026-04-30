"""batch_enrich.py — CSV → enriched.json voor een hele prospect-lijst.

Usage:
    python3 batch_enrich.py prospects.csv [--out enriched.json] [--branche kapper]

CSV input (minimaal):
    name, addr, city
    "Kaashandel De Wit", "Lange Hezelstraat 11", "Nijmegen"

Optionele kolommen die search-discovery overslaan (snelheid + betrouwbaarheid):
    wanderlog_url, oozo_url, telefoonboek_url, branche

Voor elke rij: run enrich() en consolideer naar één JSON-bestand met:
    {
      "shops": [<enriched-record>, ...],
      "summary": {
        "total": 10,
        "ready": 4,           # full data, ready to render
        "needs_review": 2,    # missing pieces, manual check
        "skip-inactive": 1,   # business no longer operating
        "skip-no-data": 2,    # nothing found — wrong listing or unindexed
        "has-site": 1,        # already has official website
      },
      "generated": "2026-04-30T14:00:00Z"
    }

Honesty: every shop carries source-attribution per field.
Status drives downstream pipeline (skip vs. render).
"""

from __future__ import annotations
import csv
import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from enrich import enrich, print_summary  # noqa: E402
from fetch import enable_cache  # noqa: E402


def process_csv(csv_path: Path, *, default_branche: str = None) -> List[Dict[str, Any]]:
    """Read CSV, run enrich on each row, return list of enriched records."""
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    print(f"📋  Loaded {len(rows)} rows from {csv_path.name}")
    print()

    records: List[Dict[str, Any]] = []
    for i, row in enumerate(rows, 1):
        name = (row.get("name") or "").strip()
        if not name:
            continue
        city = (row.get("city") or "").strip()
        addr_hint = (row.get("addr") or row.get("address") or row.get("street") or "").strip()
        branche = row.get("branche") or default_branche

        print(f"━━━ [{i}/{len(rows)}] {name} ━━━")
        rec = enrich(
            name,
            city,
            addr_hint=addr_hint,
            wanderlog_url=row.get("wanderlog_url") or None,
            telefoonboek_url=row.get("telefoonboek_url") or None,
            oozo_url=row.get("oozo_url") or None,
        )
        # Annotate input-row metadata so downstream knows the source
        rec["input"]["row_number"] = i
        rec["input"]["branche"] = branche
        if "addr" in row:           rec["input"]["addr"] = row["addr"]
        if "phone" in row:          rec["input"]["phone_hint"] = row["phone"]
        if "lat" in row:            rec["input"]["lat"] = row["lat"]
        if "lon" in row:            rec["input"]["lon"] = row["lon"]
        if "shop_type" in row:      rec["input"]["shop_type"] = row["shop_type"]

        print_summary(rec)
        records.append(rec)
        print()

    return records


def summary_counts(records: List[Dict[str, Any]]) -> Dict[str, int]:
    """Aggregate status counts."""
    counts = {"total": len(records)}
    for r in records:
        s = r["status"]
        counts[s] = counts.get(s, 0) + 1
    return counts


def main():
    ap = argparse.ArgumentParser(description="Batch-enrich prospect CSV to JSON")
    ap.add_argument("csv", type=Path, help="Input CSV (must have name + city columns)")
    ap.add_argument("--out", type=Path, default=None,
                    help="Output JSON (defaults to <csv-basename>-enriched.json)")
    ap.add_argument("--branche", default=None,
                    help="Default branche key for all rows lacking a 'branche' column")
    args = ap.parse_args()

    if not args.csv.exists():
        print(f"❌ CSV not found: {args.csv}")
        sys.exit(1)

    out_path = args.out or args.csv.with_suffix("").with_name(
        f"{args.csv.stem}-enriched.json"
    )

    enable_cache()
    records = process_csv(args.csv, default_branche=args.branche)
    counts = summary_counts(records)

    # Write JSON
    payload = {
        "shops": records,
        "summary": counts,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_csv": str(args.csv),
    }
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

    # Final report
    print("=" * 70)
    print(f"✅  Wrote {out_path}")
    print()
    print("📊  Status summary:")
    for status, n in sorted(counts.items()):
        if status == "total":
            continue
        icon = {"ready": "✅", "needs_review": "⚠️", "skip-inactive": "❌",
                "skip-no-data": "❓", "has-site": "🌐"}.get(status, "•")
        print(f"     {icon}  {status:<16} {n}")
    print(f"     ─────────────────  ──")
    print(f"        total            {counts['total']}")


if __name__ == "__main__":
    main()
