"""Test runner — validates parsers against 4 known shops with known answers.

Each test asserts on values we manually verified during the Lange-Hezelstraat pilot.
URLs are pre-supplied so we skip the (less reliable) search-discovery step
and isolate parser correctness.

Run:  python3 test_shops.py
Exit code 0 = all passed, 1 = any failed.
"""

from __future__ import annotations
import sys
from typing import List, Tuple
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from enrich import enrich, print_summary
from fetch import enable_cache


# Known shops with expected outcomes — these come from the Lange Hezelstraat pilot.
# Pre-supplying URLs makes the test deterministic & isolates parser correctness
# from search-engine flakiness.
TESTS: List[dict] = [
    {
        "name": "Kaashandel De Wit",
        "city": "Nijmegen",
        "addr_hint": "Lange Hezelstraat 11",
        "telefoonboek_url": "https://www.telefoonboek.nl/bedrijven/t2317813/nijmegen/kaashandel-de-wit/",
        "oozo_url": None,  # find via search — may legitimately not exist
        "expect": {
            "tel_contains": "024",
            "street_contains": "Hezelstraat",
            # active may be unknown if oozo search misses — that's OK as long as we have tel+adres
            "status_in": ("ready", "needs_review"),
        },
    },
    {
        "name": "Vinylarchief",
        "city": "Nijmegen",
        "addr_hint": "Lange Hezelstraat 68",  # disambiguates from same-name restaurant
        "telefoonboek_url": None,
        "oozo_url": None,
        "expect": {
            # Without explicit URLs, search may return wrong business or nothing.
            # The address-mismatch safeguard should reject the 2021 restaurant.
            "status_in": ("ready", "needs_review", "skip-no-data"),
        },
    },
    {
        "name": "Bruining Dakbedekking",
        "city": "Nijmegen",
        "telefoonboek_url": "https://www.telefoonboek.nl/bedrijven/t4066708/nijmegen/bruining-dakbedekking/",
        "oozo_url": "https://www.oozo.nl/bedrijven/nijmegen/nijmegen-noord/ressen/980955/bruining-dakbedekking",
        "expect": {
            "active": True,
            "kvk": "61049166",
            "founding_year": 2014,
            "status_in": ("ready", "needs_review"),
        },
    },
    {
        "name": "Kapsalon Oud-West",
        "city": "Nijmegen",
        "telefoonboek_url": None,
        "oozo_url": "https://www.oozo.nl/bedrijven/nijmegen/nijmegen-oud-west/wolfskuil/1809481/kapsalon-oud-west",
        "expect": {
            "active": False,
            "kvk": "75985691",
            "founding_year": 2015,
            "status_in": ("skip-inactive",),
        },
    },
]


def assert_eq(label: str, actual, expected) -> bool:
    ok = actual == expected
    icon = "✓" if ok else "✗"
    print(f"     {icon} {label}: expected {expected!r}, got {actual!r}")
    return ok


def assert_contains(label: str, actual: str, substr: str) -> bool:
    ok = substr.lower() in (actual or "").lower()
    icon = "✓" if ok else "✗"
    print(f"     {icon} {label}: expected '{substr}' in '{actual}'")
    return ok


def assert_in(label: str, actual, options) -> bool:
    ok = actual in options
    icon = "✓" if ok else "✗"
    print(f"     {icon} {label}: expected one of {options}, got {actual!r}")
    return ok


def run_test(spec: dict) -> Tuple[bool, str]:
    rec = enrich(
        spec["name"],
        spec["city"],
        addr_hint=spec.get("addr_hint"),
        telefoonboek_url=spec.get("telefoonboek_url"),
        oozo_url=spec.get("oozo_url"),
    )
    print_summary(rec)
    print()
    print("   ── assertions ──")

    expect = spec["expect"]
    passes = []
    if "status_in" in expect:
        passes.append(assert_in("status", rec["status"], expect["status_in"]))
    if "active" in expect:
        actual = rec["data"].get("is_active", {}).get("value")
        passes.append(assert_eq("is_active", actual, expect["active"]))
    if "tel_contains" in expect:
        actual = rec["data"].get("tel", {}).get("value", "")
        passes.append(assert_contains("tel", actual, expect["tel_contains"]))
    if "street_contains" in expect:
        actual = rec["data"].get("street", {}).get("value", "")
        passes.append(assert_contains("street", actual, expect["street_contains"]))
    if "kvk" in expect:
        actual = rec["data"].get("kvk", {}).get("value")
        passes.append(assert_eq("kvk", actual, expect["kvk"]))
    if "founding_year" in expect:
        actual = rec["data"].get("founding_year", {}).get("value")
        passes.append(assert_eq("founding_year", actual, expect["founding_year"]))

    return all(passes), spec["name"]


def main() -> int:
    enable_cache()
    print("=" * 70)
    print(f"Running {len(TESTS)} parser tests on known Nijmegen shops")
    print("=" * 70)

    failed: List[str] = []
    for spec in TESTS:
        print(f"\n┌─ {spec['name']} ──")
        ok, name = run_test(spec)
        if not ok:
            failed.append(name)

    print("\n" + "=" * 70)
    if failed:
        print(f"❌  {len(failed)}/{len(TESTS)} failed: {', '.join(failed)}")
        return 1
    print(f"✅  All {len(TESTS)} tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
