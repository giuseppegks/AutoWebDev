# AutoWebDev

Drie elkaar opvolgende **Claude Code skills** die samen één workflow vormen: van **lokaal bedrijf zonder website vinden** → **pitch-mockup genereren voor cold outreach** → **echte site bouwen** zodra ze klant worden.

Gebouwd voor freelance webdesigners en kleine agencies die buurtwinkels, kappers, café's, restaurants en trade-bedrijven (dakdekkers, fysio's, garages) als doelgroep hebben.

## De 3 skills — als pipeline

```
┌──────────────────────────────────┐
│ 1. finding-businesses-           │  Open data (OSM Overpass + telefoonboek)
│    without-websites              │  → CSV met prospects per stad/branche
└────────────────┬─────────────────┘
                 │ CSV
                 ▼
┌──────────────────────────────────┐
│ enrich/ (auto-enrichment)        │  Wanderlog + Oozo + telefoonboek + Pexels
│                                  │  → CSV → enriched.json → mockups (one cmd)
└────────────────┬─────────────────┘
                 │ enriched JSON
                 ▼
┌──────────────────────────────────┐
│ 2. building-prospect-mockups     │  Verify → activity-check → enrich → render
│                                  │  → 20 branches, Pexels stock, Fraunces
│                                  │  → 1-page pitch-mockups voor cold outreach
└────────────────┬─────────────────┘
                 │ winnende prospect → klant
                 ▼
┌──────────────────────────────────┐
│ 3. building-local-business-      │  Multi-page site met logo + foto's + verhaal
│    website                       │  → fact-audit + verify-before-publish
└──────────────────────────────────┘
```

## Wat zit erin

### 1. `finding-businesses-without-websites/`
**Vrij + zonder API-keys** prospects vinden via OpenStreetMap Overpass API. 14-branche-tabel (café, kapper, restaurant, bakkerij, schoonheidssalon, fysio, garage, …) met OSM-tag mapping. Output: CSV met naam, adres, telefoon (indien bekend), social-media-handles, OSM-id.

Belangrijke caveat ingebouwd: ~50% false-positive rate na alleen OSM-filter, dus skill bevat een verplichte verify-step met Google-search per kandidaat.

**Niet via OSM**: trade-bedrijven (dakdekker, loodgieter, schilder) hebben geen winkelpand om te mappen — skill verwijst voor die branches naar telefoonboek.nl/branche.

### 2. `building-prospect-mockups/`
Pipeline + Python-renderer (`template_generator.py`, ~950 regels) die prospect-data omzet in convincing 1-page mockup-websites. Universal template, alleen branche-specifieke icons + Pexels-zoekwoorden + schema.org type verschillen.

**Features:**
- 5-step pipeline: verify → activity-check (Oozo) → enrich (2 directories) → render → CSV-update
- 20 branches in `BRANCHES`-config (café, kapper, restaurant, bakkerij, slager, schoonheidssalon, bloemist, fysio, tandarts, garage, boekhandel, apotheek, dakdekker, kaashandel, juwelier, platenzaak, wonen, kleding, drankspeciaalzaak)
- Typografie: **Fraunces** (variable serif, opsz 144) + **Inter Tight** (modern body)
- Vaste secties: hero met live "open/gesloten" status, 8-card services-grid, animated testimonials carousel, "hoe werkt het" 3-stappen op donker-navy band, sfeerbeelden 3×2 grid, contact + OSM map, WhatsApp FAB, sticky mobile bottom-bar
- 100% **echte data** — letterlijke review-quotes uit Wanderlog/Google met naam + datum + bron, percentage-based star fills (4.8/5 → 96% goud)
- Pexels stockfoto's met licentie-attributie, alle foto's hotlinkable
- Schema.org JSON-LD per branche (HairSalon, RoofingContractor, JewelryStore, etc.)
- Footer-disclaimer + `<meta name="robots" content="noindex,nofollow">` — zodat pitch-mockups niet ge-indexeerd raken

### `enrich/` (auto-enrichment pipeline)
**Bridge tussen skill #1 en skill #2** — pure-Python, geen API-keys verplicht (Pexels optioneel). Neemt een prospect-CSV en produceert renderable mockups in twee commando's.

**Onderdelen:**
- `parsers/telefoonboek.py` — schema.org microdata: tel, adres, postcode, openingstijden, rating
- `parsers/oozo.py` — verplichte activity-check ("niet langer actief"), KvK, founding-jaar, branchecode
- `parsers/wanderlog.py` — embedded JSON-blob: website + Google rating + verbatim 5★ reviews + tel
- `parsers/verify.py` — search-fallback (Brave + DDG) wanneer Wanderlog leeg is
- `pexels.py` — branche-aware photo-fetcher met disk-cache (200 req/h gratis tier)
- `enrich.py` — orchestrator met source-attribution + address-mismatch safeguard
- `batch_enrich.py` — CSV → enriched.json met status-counts (`ready` / `needs_review` / `skip-inactive` / `skip-no-data` / `has-site`)
- `render_bridge.py` — enriched.json → mockups via `template_generator.render_all()`
- `test_shops.py` — 4 known-answer regression tests (Kaashandel, Vinylarchief, Bruining, Oud-West)

**Workflow:**
```bash
# 1. Skill #1 produceert prospects.csv (name, addr, city, lat, lon, shop_type, branche)
# 2. Auto-enrich → JSON met source-attributed velden
python3 enrich/batch_enrich.py prospects.csv --out enriched.json
# 3. Render mockups (Claude vult marketing-copy in optionele copy.json)
python3 enrich/render_bridge.py enriched.json --copy copy.json --output sites/
```

**Honesty per veld:** elk extracted veld krijgt `{value, source_url, confidence: high|medium|low}` zodat de pipeline weet welke aannames hij doet en welke uit eerste-hand bron komen.

### 3. `building-local-business-website/`
Voor zodra een prospect een **echte klant** is. Werkflow voor 4-page presentational sites — Home / Menu / About / Contact — pure HTML+CSS+JS, geen framework, geen backend, statisch hostbaar (Vercel/Netlify/GitHub Pages).

Honesty principles ingebouwd: fact-audit (✅/⚠️/❌), verify via 2+ bronnen, vague-but-true beats specific-and-fake. Geen verzonnen prijzen, owners, founding years.

## Honesty als design-principe

Alle drie skills delen dezelfde regels:

1. **Geen fabricatie** — geen verzonnen prijzen, namen, founding years, supplier-namen, reviews
2. **Verify via 2+ bronnen** voor verhaal-elementen (founding year, owners, partnerships)
3. **Vague-but-true beats specific-and-fake** — *"Bel voor afspraak"* niet *"vanaf €19"*
4. **Mockup-disclaimer altijd** — pitch-mockups krijgen footer-banner + `noindex` + Pexels-credit
5. **mailto-only by default** — geen Formspree/Supabase/SendGrid silent-add
6. **Stock-photo disclosure** — verbal in pitch, niet visueel op de pagina
7. **Activity-check verplicht** — Oozo/KvK voor je een mockup bouwt voor een mogelijk inactief bedrijf

## Gebruik

### Met Claude Code
1. Clone deze repo of fork hem
2. Symlink `skills/*` in je `~/.claude/skills/` directory:
   ```bash
   ln -s /path/to/AutoWebDev/skills/finding-businesses-without-websites ~/.claude/skills/
   ln -s /path/to/AutoWebDev/skills/building-prospect-mockups ~/.claude/skills/
   ln -s /path/to/AutoWebDev/skills/building-local-business-website ~/.claude/skills/
   ```
3. Start een Claude Code-sessie en zeg bv:
   - *"Vind kappers in Nijmegen zonder website"* → triggert skill #1
   - *"Bouw mockups voor deze prospect-lijst"* → triggert skill #2
   - *"Bouw een site voor café Wanders Kleve"* → triggert skill #3

### Zonder Claude Code
De Python-renderer in `skills/building-prospect-mockups/template_generator.py` is **stand-alone bruikbaar** — `python3 template_generator.py` draait een self-test die een sample-mockup rendert in `./demo-output/`. Importeer `render_all` uit je eigen scripts:

```python
import sys
sys.path.insert(0, "skills/building-prospect-mockups")
from template_generator import render_all, BRANCHES

render_all(
    targets=[{
        "name": "Mijn Lokale Café",
        "branche": "cafe",
        "city": "Nijmegen",
        "addr": "Lange Hezelstraat 1",
        "tel": "024 123 4567",
        "lat": 51.8480, "lon": 5.8590,
        # ... zie TARGET_EXAMPLE in template_generator.py voor volledig contract
    }],
    output_dir="sites",
    port=8080,
)
```

## Tech stack

- **Python 3.10+** voor de renderer (geen externe dependencies behalve `Pillow` voor de optionele logo-fix in skill #3)
- **Pure HTML/CSS/JS** output — geen build step, geen framework
- **Vanilla JS** voor live-status badges, gallery, testimonials carousel, mobile nav
- **OpenStreetMap Overpass API** + **Pexels** + **WebSearch** als data-bronnen (alle gratis, geen API-keys)

## Bijdragen

PRs welkom voor:
- Nieuwe branches in `BRANCHES`-config (extend `template_generator.py` + de tabel in `SKILL.md`)
- Extra SVG-iconen in `ICONS` dict
- Vertalingen (skill is nu NL-first; engels/duits welkom)
- Nieuwe palettes in `PALETTES`

## Licentie

MIT. Zie `LICENSE`. De Pexels-foto's die de generator hotlinkt vallen onder de [Pexels-licentie](https://www.pexels.com/license/).

## Verhaal achter het project

Gebouwd in een handvol sessies met Claude Code, getest op echte velddata in Nijmegen (10 winkels op de Lange Hezelstraat, dakdekkers in regio Nijmegen, café's in Kleve). De false-positive rate van 50% in OSM "no-website" entries is empirisch vastgesteld — daarom de verplichte verify-step. De typografie-keus (Fraunces + Inter Tight) is doorlopen na expliciete afwijzing van Cormorant Garamond ("te bruidstaart-klassiek"). De animated testimonials gebruiken **geen avatar-foto's** omdat we die zelden hebben — een witte review-card met percentage-correcte sterren is honest én visueel even sterk.
