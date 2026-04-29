---
name: building-prospect-mockups
description: Use when generating cold-outreach 1-page mockup websites for local businesses (café, kapper, restaurant, bakkerij, salon, garage, fysio, etc.) that don't have a real website yet — to use as a "kijk wat je site kan worden"-pitch. Triggers on phrases like "bouw mockups voor deze prospect-lijst", "pitch website voor [bedrijf]", "outreach mockup", "voorbeeldsite voor cold call", "lead-generation websites genereren".
---

# Building Prospect Mockups for Cold Outreach

## Overview

Pipeline that turns a CSV of prospect businesses (typically from `finding-businesses-without-websites`) into convincing 1-page mockup websites for cold outreach. Each mockup combines **only verified business data** with **stock photos as placeholders** and a **clear footer-only mockup-disclaimer**. Branch-agnostic via a config table.

**Core principle:** verify → activity-check → enrich → render. Skip a step and the pitch backfires.

## When to Use

- You have a prospect list (CSV with name, address, phone, OSM-id) and want pitch material
- Goal is **outreach mockup**, not a finished site
- Local business types: café, kapper, restaurant, bakkerij, schoonheidssalon, fysio, garage, etc.
- Up to ~30-40 mockups per batch (web-search + fetch budget)

**Skip when:**
- Customer has paid for an actual site → use `building-local-business-website` instead
- Just need to find prospects (not build) → use `finding-businesses-without-websites`
- More than ~50 prospects → split into batches; one Overpass / WebSearch storm hits limits

## The 5-Step Pipeline (mandatory order)

```
For each prospect:
  1. VERIFY website?  WebSearch "<name>" "<city>" → if real site found, status=has_website, SKIP
  2. ACTIVITY check   WebFetch oozo.nl listing → if "niet langer actief", status=inactive, SKIP
  3. ENRICH           WebFetch 2 directories → description, services, hours, reviews, sinds-jaar
  4. RENDER           template_generator.py with verified data + Pexels stock photos
  5. CSV              write status + localhost URL per row to results.csv
```

**Skipping #1** ⇒ wasted mockup for someone who already has a site.
**Skipping #2** ⇒ embarrassing pitch for a closed business.
**Skipping #3** ⇒ generic, doesn't impress — looks like a template, not a brand.

Pilot 5 first; **expect ~50% false-positive rate** in the OSM list (real websites that OSM didn't have).

## Per-Branche Config Table

| Branche | OSM tag | Schema.org | Pexels keyword | Palette | Service icons |
|---|---|---|---|---|---|
| Café / koffie | `amenity=cafe` | `CafeOrCoffeeShop` | `cafe interior` | sienna · olive | coffee, cake, plate, smile |
| Kapper / Friseur | `shop=hairdresser` | `HairSalon` | `barbershop` / `hair salon` | navy · graphite | scissors, comb, drop, razor, kid, spray |
| Restaurant | `amenity=restaurant` | `Restaurant` | `restaurant interior` | rose · sienna | knife, plate, glass, smile |
| Bar / kroeg | `amenity=bar` of `amenity=pub` | `BarOrPub` | `cocktail bar` / `pub interior` | graphite · navy | glass, music, smile |
| Bakkerij | `shop=bakery` | `Bakery` | `bakery bread` | sienna · olive | bread, oven, plate |
| Slager | `shop=butcher` | `Store` | `butcher shop` | sienna · graphite | knife, plate |
| Schoonheidssalon | `shop=beauty` | `BeautySalon` | `beauty salon` | rose · sage | drop, flower, spray, smile |
| Bloemist | `shop=florist` | `Florist` | `flower shop` | sage · rose | flower, drop, scissors |
| Fysiotherapeut | `healthcare=physiotherapist` | `MedicalClinic` | `physiotherapy clinic` | sage · navy | heart, hand, smile |
| Tandarts | `amenity=dentist` | `Dentist` | `dental clinic` | navy · sage | tooth, smile, drop |
| Garage | `shop=car_repair` | `AutoRepair` | `auto mechanic shop` | graphite · navy | car, tools, scissors |
| Boekhandel | `shop=books` | `BookStore` | `independent bookstore` | olive · navy | book, smile |
| Apotheek | `amenity=pharmacy` | `Pharmacy` | `pharmacy interior` | navy · sage | drop, plus |
| Dakdekker | `craft=roofer` (use directory ipv OSM!) | `RoofingContractor` | `roofer roof construction` | graphite | tools, drop, knife |
| Kaashandel | `shop=cheese` | `Store` | `cheese shop` | olive | plate, knife, glass |
| Juwelier / sieraden | `shop=jewelry` | `JewelryStore` | `jewelry boutique` | rose | flower, drop, smile |
| Platenzaak / vinyl | `shop=music` | `Store` | `vinyl record store` | graphite | music, smile |
| Wonen / meubels | `shop=furniture` | `FurnitureStore` | `vintage furniture shop` | sienna | plate, smile |
| Kleding / boutique | `shop=clothes` | `ClothingStore` | `clothing boutique interior` | rose | smile |
| Drankspeciaalzaak | `shop=alcohol` | `Store` | `craft beer shop` | sienna | glass, drop |

Add a new branche by extending `BRANCHES` in `template_generator.py`.

**Trade-bedrijven uitzondering**: voor branches zonder etalage (dakdekker, loodgieter, schilder, klusbedrijf, elektricien) is OSM bijna leeg — gebruik **telefoonboek.nl/branche/`<plaats>`/`<branche>`** als prospect-bron in plaats van Overpass.

## Template Structure (universal — same for every branche)

1. **Sticky header** — monogram block + wordmark + nav + tel CTA
2. **Hero** — stock-image bg @ 22% opacity over color gradient, status badge (open/closed via JS), `sinds JAAR` badge, dual CTA (bel + WhatsApp)
3. **Hero-card sidebar** — full week hours with "vandaag" highlighted
4. **Services grid** — 6-8 cards with branche-specific SVG icons
5. **Reviews** — two render modes:
   - **`animated_testimonials`** (preferred) — compact 2-col: links eyebrow + h2 + intro-tekst + rating-pill, rechts witte review-card met sterren-row (echte percentage-fill via `.rs-stars__bg/__fg` overlay), italic quote, naam + bron, ←→ + dots-nav onder de card. Auto-rotate 7s. **Geen avatar-stack** (zou nep zijn zonder echte foto's).
   - `reviews` (fallback) — static 3-card grid
6. **"Hoe werkt het" 3-stappen** — **`section.dark`** (navy bg, witte step-cards met `var(--primary)` titels overridden) — alterneert met de paper-dim `atst` ervoor
7. **About** — verhaal + Pexels stock-foto naast in 4:5 frame
8. **Sfeerbeelden gallery** — 3×2 even grid, no captions, no overlay labels
9. **Contact card + OSM map** — adres, tel, e-mail, openingstijden (vandaag highlighted), maps-link
10. **CTA strip** — laatste call-to-action met telefoonnummer
11. **Footer** — single-line mockup-disclaimer + Pexels credit fine-print
12. **WhatsApp FAB** rechts-onderin (alleen desktop) met puls-ring
13. **Sticky bottom bar** (alleen mobile) met bel + WhatsApp

## Typography (locked — don't substitute)

- **Display:** Fraunces (variable, `opsz 144`, `SOFT 50`, ss01+ss02 features)
- **Body:** Inter Tight (ss01, cv11)
- **Tracking:** h1 `-.035em`, h2 `-.025em` (negative tracking is the modern signal)
- **Italic accents:** Fraunces italic at high opsz only — never use it on body text

This pairing was tested across multiple iterations; reverting to Cormorant Garamond / Inter or all-sans Bricolage gave a worse pitch result. Don't second-guess unless customer specifies.

## Honesty Rules (non-negotiable)

1. **Only verified facts** in user-facing copy — never invent prices, owners, founding year, supplier names
2. **Activity check is mandatory** — Oozo / KvK before generating. Skipping this once embarrassed the pitch (kapsalon-oud-west case)
3. **Footer-only mockup disclaimer** — *"Voorbeeld-mockup · Geen officiële site"*. No visual disclaimers in the body (the pitch is verbal)
4. **`<meta name="robots" content="noindex,nofollow">`** — non-negotiable, don't index pitch sites
5. **Pexels credit** in fine-print legal line (license requirement, but tiny)
6. **mailto only** — never silently add Formspree, Supabase, SendGrid, etc.
7. **Stock-foto disclosure is verbal** — say it on the call, don't plaster the page with `📷 stockfoto` labels
8. **Testimonials = letterlijke citaten** uit publieke bronnen (Wanderlog, Google, Trustpilot) met **naam zoals reviewer hem schreef + datum + bron + score**. Geen paraphrases tenzij expliciet als thema gemarkeerd. Geen verzonnen avatars/foto's.
9. **Stars renderen op echte percentage** — gebruik altijd `.rs-stars` overlay-techniek (`__bg` + `__fg` met `width: {pct}%`), nooit `round(score/2)` shortcuts. 4.8/5 → width 96%. Schaal automatisch detecteren: ≤5 = 5-pts, >5 = 10-pts (override met `rating.max`).

## Reusable code

The full v6 generator lives in `template_generator.py` next to this SKILL.md. Run as:

```python
from template_generator import render_all
render_all(
    targets=[...],         # list of dicts (data contract below)
    output_dir="sites/",
    port=8912,             # for local URLs in CSV
)
```

**Target data contract** (per prospect):

```python
{
  "name": "Bedrijfsnaam",
  "branche": "kapper",                          # key into BRANCHES table
  "city": "Nijmegen",
  "neighborhood": "Wijk · Nijmegen",            # optional
  "addr": "Straatnaam 123",
  "tel": "024 350 1735",
  "whatsapp": "31243501735",                    # optional, enables WA buttons
  "lat": 51.8254, "lon": 5.8439,
  "since_year": 1996,                           # optional, from telefoonboek/oozo
  "facebook": "https://...", "instagram": "https://...",  # optional
  "tagline_h1": "Een begrip in <city> — sinds <year>.",
  "lead": "Eerlijke korte intro op basis van verbatim directorytekst.",
  "quote": {"text": "...", "attr": "haar.expert"},
  "rating": {"score": 4.8, "count": 66, "source": "Google", "max": 5},  # max optional, auto-detect: ≤5=5-pt, >5=10-pt
  "reviews": [{"stars": 5, "text": "...", "author": "Naam · Bron"}, ...],
  "animated_testimonials": [           # preferred over "reviews"; compact carousel
      {"name": "Luis C.", "designation": "Wanderlog · 5/5 · sep 2024",
       "quote": "Letterlijke quote uit publieke review", "stars": 5},
      ...
  ],
  "reviews_intro": "Korte tekst onder h2, links van card",  # optional, default "Verifieerbare citaten ..."
  "hours": [("Maandag", "Gesloten"), ("Dinsdag", "9:00 – 18:00"), ...],
  "services": [{"icon": "scissors", "title": "...", "body": "..."}, ...],
  "tags": ["Knippen", "Kleur", ...],
  "about_heading": "...", "about_body": "...",
  "hero_image": 18173343,                        # Pexels ID
  "about_image": {"id": 19664875},
  "gallery": [{"id": ..., "label": "..."}, x6],
  "sources": ["haar.expert", "telefoonboek.nl"], # for footer attribution
  "palette": "navy",                             # optional, defaults from BRANCHES
}
```

Anything missing in the dict gets graceful fallback (e.g. no reviews → reviews-section omitted).

## Common Mistakes

| Mistake | Fix |
|---|---|
| Generating before WebSearch verify | 50%+ of OSM "no website" entries actually have a site. Verify or waste batch. |
| Skipping Oozo activity-check | Inactive business + polished mockup = embarrassing pitch. Mandatory step. |
| `📷 stockfoto · Pexels` labels in every UI element | Verbal in pitch only. Footer fine-print suffices. |
| Mosaic gallery (`is-large`, `is-tall`) | Looks 2018-templatey. Use 3×2 even grid. |
| Cormorant Garamond / Playfair display | Bridal-cake feel. Use Fraunces — modern editorial. |
| WhatsApp emoji `💬` instead of real logo | Use the official 24×24 logo SVG (in `template_generator.py`) |
| WhatsApp FAB on top of mobile sticky-bar | Hide FAB at `max-width: 680px` — sticky-bar takes over there |
| Hardcoded "vandaag open 9-18" in HTML | Date().getDay() switch + `data-day` rows |
| `<form action="mailto:">` | Skill defaults to `tel:` + `https://wa.me/` only — no form |
| Inventing reviews | Only quote real review bodies with author + bron credit |
| Inventing prices | "Bel voor afspraak / Vraag aan de bar" — never make up prices |
| Avatar-stack met initialen ipv echte foto's | Skip de avatar-stack volledig — gebruik 2-col layout met witte review-card |
| `round(score/2)` voor sterren | Use `.rs-stars__fg style="width:{pct}%"` met percentage |
| Twee `paper-dim` of `paper` secties achter elkaar | Wissel af met `section.dark` — patroon: dark → paper → paper-dim → dark → ... |
| Cards met h3 op dark sectie | Override: `section.dark .step h3, .card h3, .svc h3 {{color: var(--primary)}}` |
| Slugs met `&amp;` of `é` letterlijk | Slugify decodeert HTML-entities + `unicodedata.normalize NFD` strip accents (Bob &amp; Bill → bob-en-bill) |
| Mock telefoonnummers als placeholder (`024 322 6321`) | Beter `tel: ""` + email fallback dan een fake nummer dat de pitch breekt |

## Red Flags — STOP and reconsider

- About to write a price → did you verify? If not, omit
- "Oozo says inactive" but the listing looks recent → fetch a 2nd source (cylex, telefoonboek) before deciding
- WebSearch returned a Facebook page → that's NOT a website; status stays `no_website`, but mark the FB-link in the contact card
- Customer paid for the site → STOP, switch skill: this is for unpaid pitch material only
- Stock photo doesn't fit the branche (e.g. café photo on a fysio mockup) → check `BRANCHES[branche].pexels_keyword` and refresh

## Cross-references

- **`finding-businesses-without-websites`** — upstream skill that produces the prospect CSV consumed here
- **`building-local-business-website`** — downstream skill once a prospect becomes a paying customer
- **`copywriting`** — useful for tagline / lead variations beyond defaults

## Honesty principles (carried from sister skills)

1. Never invent specific facts — verify with 2+ sources before quoting
2. `noindex` always, mockup-disclaimer always, Pexels credit always
3. Vague-but-true beats specific-and-fake — "Bel voor prijslijst" not "vanaf €19"
4. The mockup is a **conversation starter**, not a finished product. Don't oversell, don't underdeliver
