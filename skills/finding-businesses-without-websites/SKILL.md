---
name: finding-businesses-without-websites
description: Use when the user wants a list of local businesses without a website (café, kapper, restaurant, bakkerij, schoonheidssalon, fysio, garage, etc.) — for cold outreach, web-design lead generation, or local market research in a specific city or region. Triggers on phrases like "bedrijven zonder website", "kappers zonder website in [stad]", "leads voor webdesign", "prospects without a website", "find local businesses for [city]", "lead generation [branche]".
---

# Finding Local Businesses Without Websites

## Overview

Free, no-API-key technique to enumerate local businesses in a city and filter to those missing a `website` tag. Uses **OpenStreetMap Overpass API**. Faster, more accurate, and legally cleaner than scraping KVK / Chamber of Commerce.

**Core principle:** OSM is the right bron. KVK is the wrong bron for this.

## Why NOT KVK / Handelsregister

| KVK Limitation | Reality |
|---|---|
| No `website` field in zoek-results | Niet queryable, ook niet via login |
| Bulk export | Alleen via betaald dataproduct |
| Scrapen op schaal | ToS-overtreding |

KVK registreert geen websites als doorzoekbaar attribuut. Stop hier en ga naar OSM.

## Workflow

### 1. Pick the right OSM tag

| Branche (NL/DE) | OSM tag |
|---|---|
| Café / koffiebar | `amenity=cafe` |
| Restaurant | `amenity=restaurant` |
| Bar / kroeg | `amenity=bar` of `amenity=pub` |
| Kapper / Friseur | `shop=hairdresser` |
| Bakkerij / Bäckerei | `shop=bakery` |
| Slager / Metzger | `shop=butcher` |
| Schoonheidssalon | `shop=beauty` |
| Kledingwinkel | `shop=clothes` |
| Bloemist | `shop=florist` |
| Fysiotherapeut | `healthcare=physiotherapist` |
| Tandarts | `amenity=dentist` |
| Autogarage | `shop=car_repair` |
| Boekhandel | `shop=books` |
| Apotheek | `amenity=pharmacy` |

Onbekende branche? Zoek op [taginfo.openstreetmap.org](https://taginfo.openstreetmap.org/).

### 2. Run the Overpass query

Pas `<TAG>=<VALUE>` en `<CITY>` aan, daarna draai vanaf shell:

```bash
mkdir -p /tmp/biz && cat > /tmp/biz/q.txt <<'EOF'
[out:json][timeout:60];
area["name"="<CITY>"]["boundary"="administrative"]["admin_level"="8"]->.a;
(
  node["<TAG>"="<VALUE>"](area.a);
  way["<TAG>"="<VALUE>"](area.a);
);
out tags center;
EOF

curl -s --data-urlencode "data@/tmp/biz/q.txt" \
  https://overpass-api.de/api/interpreter -o /tmp/biz/raw.json
```

Voor Duitse steden werkt `admin_level=8` (Stadt). Voor sommige NL gemeentes ook `admin_level=8`. Werkt het niet? Probeer 6 of laat `admin_level` weg.

### 3. Filter + export to CSV

```python
import json, csv

d = json.load(open('/tmp/biz/raw.json'))
elements = d.get('elements', [])

without_web = []
for el in elements:
    t = el.get('tags', {}) or {}
    # Check ALL three website-style tags — niet alleen 'website'
    if any(t.get(k) for k in ('website', 'contact:website', 'url')):
        continue
    without_web.append({
        'name': t.get('name') or '(naam onbekend)',
        'addr': f"{t.get('addr:street','')} {t.get('addr:housenumber','')}".strip() or '(adres onbekend)',
        'postcode': t.get('addr:postcode',''),
        'phone': t.get('phone') or t.get('contact:phone') or '',
        'email': t.get('email') or t.get('contact:email') or '',
        'facebook': t.get('contact:facebook') or t.get('facebook') or '',
        'instagram': t.get('contact:instagram') or t.get('instagram') or '',
        'osm_id': f"{el['type']}/{el['id']}",
    })

print(f"Totaal: {len(elements)} | zonder website: {len(without_web)}")
with open('prospects.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(without_web[0].keys()))
    w.writeheader(); w.writerows(sorted(without_web, key=lambda x: x['name'].lower()))
```

### 4. Show top candidates to user

Sorteer eerst entries **mét** telefoonnummer en **mét** adres — dat zijn de directst-bruikbare prospects. Toon top 8–10 in een markdown-tabel.

## Critical Caveats

**Vertel de user altijd deze 4 punten — anders krijg je een verkeerd verwachtingsbeeld:**

1. **OSM is community-maintained.** Een ontbrekend `website`-veld ≠ "geen website". Het kan gewoon niet ingevuld zijn. **Verifieer top-kandidaten met een Google-search** voor je benadert.
2. **Volledigheid wisselt per stad.** Grote NL-steden zijn redelijk compleet; kleinere dorpen kunnen lacunes hebben. Cross-check met Google Maps als de aantallen verdacht laag zijn.
3. **Sommige entries hebben geen naam of adres** — gooi die weg of nodig de user uit ze in OSM zelf aan te vullen.
4. **Check 3 tags**, niet alleen `website`: `website`, `contact:website`, `url`. OSM-mappers gebruiken ze door elkaar.

## Verification step (optional but recommended)

Voor een **A-kwaliteit prospect-lijst**: Google-search elke top-kandidaat met `"<naam>" <stad> site:` en mark elk als:
- ✅ confirmed no website
- ⚠️ has Facebook/Insta-only
- ❌ has website (OSM was outdated)

Dit reduceert de lijst maar elimineert valse positieven.

## Paid alternatives (when OSM is too thin)

| Bron | Wanneer | Cost |
|---|---|---|
| Google Places API (`Place Details`) | OSM-data is te dun voor de regio | ~$17/1.000 detail-calls |
| Yelp Fusion API | US/UK markten | Gratis tier beperkt |
| Apple MapKit JS | Cross-check tegen Apple | Gratis met Apple ID |

Google Places heeft een structureerde `website`-veld en is de meest betrouwbare bron als je geld mag uitgeven.

## Worked example

**Vraag:** "Kappers in Nijmegen zonder website"

```bash
# tag: shop=hairdresser, city: Nijmegen
# resultaat: 75 totaal → 40 zonder website
# CSV met name, addr, postcode, phone, email, fb, ig, osm_id
```

Top-kandidaten (entries met telefoonnummer prioritair tonen):

| # | Naam | Adres | Telefoon |
|---|---|---|---|
| 1 | Kapperij Einstein | Einsteinstraat 153 | +31 24 350 17… |
| 2 | Schaar En Haar | Heyendaalseweg 203 | +31 24 663 99… |
| ... | ... | ... | ... |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Naar KVK gaan om websites te checken | KVK heeft geen website-veld. Gebruik OSM. |
| Alleen `website` tag checken | Check ook `contact:website` én `url` |
| OSM-data 100% vertrouwen | Verifieer top-kandidaten met Google-search |
| Resultaten tonen zonder caveat | Altijd de 4 caveats vertellen |
| Entries zonder naam meeleveren | Filter weg of toon apart als "incomplete OSM" |
| `admin_level=8` werkt niet | Probeer `=6`, of laat het weg en filter op naam |
| Scrapen van KVK voor schaal | ToS-overtreding. Niet doen. |

## Red Flags — STOP and reconsider

- User wil **e-mailadressen** in bulk → OSM heeft die meestal niet; e-mail-discovery is een aparte techniek (en juridisch glad ijs onder GDPR)
- User wil de lijst **publiceren** → check OSM-attributie eis (CC-BY-SA gelijkwaardig)
- Aantal results = 0 → admin_level klopt niet, of stadnaam exact-match faalt (bv. "'s-Hertogenbosch" vs "Den Bosch")
- User vraagt "voor heel Nederland" → splits per gemeente; één Overpass-call op landniveau is traag/timeouts
