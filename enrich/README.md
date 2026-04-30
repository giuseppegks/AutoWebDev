# enrich/

Auto-enrichment pipeline voor `building-prospect-mockups`. Gegeven `naam + stad + addr_hint`, fetcht en parseert publieke directory's tot een gestructureerde dict met **bron-attributie per veld**.

## Status

**Sessie 1 (deze commit) — werkend voor:**
- ✅ `parsers/telefoonboek.py` — naam, tel, adres, postcode, beschrijving (microdata-extractie)
- ✅ `parsers/oozo.py` — **activity-check**, KvK, founding date, employee count, category
- ✅ `enrich.py` orchestrator — combineert beiden, kortsluit op inactief, address-mismatch safeguard
- ✅ `test_shops.py` — 4-shop validation suite (Kaashandel, Vinylarchief, Bruining, Oud-West) — **all passing**

**Volgende sessies:**
- Sessie 2: `parsers/wanderlog.py` (verbatim review-extractie) + `parsers/verify.py` (heeft shop al een echte site?)
- Sessie 3: Pexels API integration + render-bridge naar `template_generator.py`

## Honesty principes

1. **Elk veld carries `{"value", "source_url", "confidence"}`** — geen "magic" defaults, geen verzonnen data
2. **Activity-check first, hard-stop op inactief** — Oud-West-blunder uit pilot moet nooit meer
3. **Address-mismatch safeguard** — als oozo een match vindt op naam maar het adres komt niet overeen met `addr_hint` → data wordt verworpen + warning
4. **Confidence-flags** (`high` / `medium` / `low`): `high` = expliciet veld in markup, `medium` = heuristiek of eerste-match
5. **Status-codes** (`ready` / `needs_review` / `skip-inactive` / `skip-no-data`): voor downstream-filter

## Quick start

```bash
# Setup (eenmalig)
mkdir -p ~/.cache/autowebdev-enrich  # cache voor herhaalde runs

# Test alle 4 known shops
python3 test_shops.py

# Eén shop verrijken
python3 enrich.py "Kaashandel De Wit" "Nijmegen"

# Met JSON output voor scripting
python3 enrich.py "Bruining Dakbedekking" "Nijmegen" --json
```

## Hoe URL-discovery werkt (en waarom het wankel is)

Pure-Python search engines schalen slecht — DDG en Brave rate-limiten / serveren captcha's bij hoge volumes. **De parsers werken 100% met een directe URL** (zoals in `test_shops.py`).

Aanbevolen workflow:
1. **Bouw upstream je CSV met `oozo_url` en `telefoonboek_url` kolommen** waar je ze al weet (uit eerder onderzoek)
2. Voor de rest probeert `enrich.py` Brave (primair) en DDG (fallback). Slaagt of slaagt niet
3. Mislukte URL-discovery levert `status="needs_review"` op — geen verzonnen data, dus veilig

## File structure

```
enrich/
├── README.md
├── fetch.py              # HTTP helper: realistic UA, rate-limit, retry, cache, site_search
├── enrich.py             # Orchestrator: oozo → telefoonboek → consolidated record
├── test_shops.py         # 4-shop validation suite
└── parsers/
    ├── __init__.py
    ├── telefoonboek.py   # microdata-extractie
    └── oozo.py           # activity-check + KvK + founding
```

## Output contract

```json
{
  "input": {"name": "...", "city": "...", "addr_hint": "..."},
  "status": "ready" | "needs_review" | "skip-inactive" | "skip-no-data",
  "data": {
    "tel":           {"value": "024 3231975", "source_url": "...", "confidence": "high"},
    "street":        {"value": "Lange Hezelstraat 11", ...},
    "postcode":      {"value": "6511 CA", ...},
    "is_active":     {"value": true|false, ...},
    "kvk":           {"value": "75985691", ...},
    "founding_year": {"value": 2015, ...},
    "category":      {"value": "Haarverzorging", ...},
    "rating":        {"value": {"score": 9.1, "count": 12, "max": 10, "source": "Telefoonboek.nl"}, ...}
  },
  "sources": ["oozo.nl", "telefoonboek.nl"],
  "warnings": ["Address mismatch — discarding oozo data", "..."]
}
```
