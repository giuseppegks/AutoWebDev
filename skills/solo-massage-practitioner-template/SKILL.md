---
name: Solo-Massage-Practitioner-Template
description: Use when spinning up a website for a solo massage therapist or body-work practitioner — one person, one practice room, holistic/therapeutic positioning rather than commercial spa. Light cream + terracotta + sage palette, 4 pages (home / over / behandelingen / praktijk), with the Cal.com booking-system skill pre-integrated so visitors book online in a branded modal. Distinct from `premium-spa-template` (dark luxury, multi-location, phone-first) and from `massage-shops-template` (Aurora editorial, masseuse roster, request-booking). Triggers on phrases like "solo massage therapist site", "single-practitioner massage website", "build a site like Gerrit Jonker", "holistic body-work practitioner", "light cream massage site", "lichaamsgerichte therapeut site", "intuitieve massage praktijk".
---

# Solo Massage Practitioner Template — Spin-Up Workflow

## When to Use

Pick this template when the client is:

- **One person** delivering the massages themselves (not a team of therapists)
- Working from **one practice room or studio**, often their home or a small rented space
- Positioned as **therapeutic / body-oriented / holistic** rather than as a commercial spa
- Comfortable with **online booking** (Cal.com) — and wants visitors to book without phoning
- Aiming for a **light, calm, professional** aesthetic — not dark luxury

Compare:

| Template | Best for | Look | Booking |
|---|---|---|---|
| `premium-spa-template` | Multi-location Thai/spa with team | Dark wine + gold | Phone-first |
| `massage-shops-template` (Aurora) | Editorial with masseuse roster | Dark + video + photo modals | Request via WhatsApp |
| **`solo-massage-practitioner-template`** | **One therapist, one room, holistic** | **Light cream + terracotta + sage** | **Cal.com online** |

## Reference Build

**`websites/massage-salons/gerrit-jonker-massage`** — solo lichaamsgericht therapeut in Nijmegen-Oost. The canonical example. Read its `DESIGN.md`, `README.md`, and the 4 HTML pages before customizing.

## Architecture (4 pages)

```
<slug>/
├── index.html              # Home — hero, over-teaser, 3 featured massages, kanker-strip, reviews, praktijk-teaser, booking CTA
├── over-ons.html           # "Over <name>" — story, 4 method-cards (intake/aanraking/adem/verbinding), opleidingen-timeline, praktijk-glimpse
├── behandelingen.html      # 6 massage forms + 3-column tariff strip + massage-bij-kanker section + praktisch (6 cards)
├── locaties.html           # Single-location detail + Google Maps embed + bereikbaarheid (fiets/OV/auto)
├── js/booking.js           # ← from skills/booking-system/template
├── api/                    # ← from skills/booking-system/template (Cal.com proxy)
├── package.json            # type: module
├── vercel.json             # cleanUrls + security headers
├── DESIGN.md               # palette + typography + components
├── README.md               # shop-specific setup + verify-before-live checklist
└── images/                 # optional — usually empty, photos load from client WP/CDN
```

## Design System

### Palette (light cream + terracotta + sage)

| Token | Hex | Role |
|---|---|---|
| `bg-deep` | `#FAF6EF` | Page background — warm cream |
| `bg-surface` | `#FFFFFF` | Cards, elevated panels |
| `bg-elevated` | `#F3ECDF` | Hover state, accent panels |
| `border-subtle` | `#DDD0BC` | Soft warm-beige dividers |
| `ink-primary` | `#2A2620` | Body text — warm near-black |
| `ink-muted` | `#6F6557` | Secondary text |
| `ink-faint` | `#A89D8C` | Fine print |
| `gold` (accent) | `#B8654B` | Warm terracotta — CTAs, kickers, italic accents |
| `gold.soft` | `#9C5239` | Hover state |
| `botanical` | `#7A8B6F` | "Op afspraak" indicator + accent of life |

**Voice:** "ik" (solo practitioner) — not "wij". Direct, body-aware, calm. Keywords: aandacht, aanraking, verbinding, lichaam, gevoel, ademhaling.

### Typography

| Use | Font | Notes |
|---|---|---|
| Display H1/H2 | Cormorant Garamond | One italic word per heading as accent (e.g. *werken*) |
| Body | Manrope | 16–18px, line-height 1.6 |
| Kicker | Manrope 600 uppercase | letter-spacing 0.18em |

Logo: pure typographic wordmark (no PNG) — practitioner's full name in Cormorant Garamond italic + tiny initials in a thin terracotta ring.

### Animations

- GSAP + ScrollTrigger fade-up reveals (`.reveal`)
- Clip-path inset image reveals (`.reveal-img`)
- Lenis smooth scroll
- All respect `prefers-reduced-motion`

## Booking Integration (Cal.com)

This template ships with the [booking-system skill](../booking-system/SKILL.md) pre-integrated. See that SKILL.md for the full architecture; the short version:

1. Copy `skills/booking-system/template/{api,js,package.json}` into the new site
2. Edit `js/booking.js` → `SHOP_CONFIG` block at the top (shop name, phone, domain, address, hours, services)
3. Wire CTAs:
   - `data-book` on the nav "Afspraak maken" button (every page)
   - `data-book` on the hero "Plan een afspraak" button (home)
   - `data-book` on the `#boeken` section primary "Boek online" button — keep bel/WhatsApp/mail as secondary fallbacks
   - `data-book` on each sub-page CTA strip
   - `data-book data-service="<key>"` on each massage card's "Boek deze massage" link (pre-selects the service)
   - `data-book data-service="intake"` on the kanker-intake CTA (pre-selects the intake)
4. Client creates a Cal.com account, makes Event Types with slugs matching `SHOP_CONFIG.services` × durations (e.g. `intuitief-60`, `intuitief-90`, …), sets availability to match `SHOP_CONFIG.hours`
5. Deploy with `CALCOM_API_KEY` env var

**Graceful degradation:** if Cal.com isn't yet wired, the modal opens and steps 1–3 work. Step 4 (time) shows "Online boeken nog niet geactiveerd — bel of WhatsApp <phone>." Bel/WhatsApp/email remain available throughout.

## Spin-Up Workflow

### 1. Verify shop facts

Quick `WebFetch` of the client's current site:
- Practitioner full name + tagline
- Full address + postcode
- Phone (E.164 + display format) + WhatsApp same number?
- E-mail
- Opening hours (per weekday)
- KvK number
- Massage types offered + duration/price structure
- Training/certification timeline if going on the over-ons page
- Reviews (extract verbatim, anonymize if needed)
- Photo URLs from their WP CDN

### 2. Duplicate the blueprint

```bash
cp -r websites/massage-salons/gerrit-jonker-massage websites/massage-salons/<slug>
cd websites/massage-salons/<slug>
```

### 3. Customize content (in this order)

1. **`js/booking.js`** — `SHOP_CONFIG` block: shopName, phoneDisplay, phoneE164, domain, addressICS, hours, services, price.
2. **`DESIGN.md`** — usually no palette change needed. Only edit if the practitioner has a distinct brand color that should replace the terracotta accent.
3. **All 4 HTML pages** — search & replace:
   - "Gerrit Jonker Massage" → new practitioner full name
   - "Gerrit Jonker" → name shown in body copy
   - "Gerrit" → first name where used informally
   - "06 542 005 28" → display phone
   - "+31654200528" → E.164 phone in `tel:` and `https://wa.me/` links
   - "gerritjonkermassage@gmail.com" → new email
   - "Cees de Jongstraat 6" → new street address
   - "Nijmegen-Oost" → new city / neighbourhood
   - `https://gerritjonkermassage.nl/wp-content/uploads/...` → new photo URLs
   - Wordmark initials `gj` (in nav + footer) → new initials
4. **`behandelingen.html`** — adapt to the practitioner's actual menu. Default has 6 forms (sport/intuitief/MER/psoas/cranio/stoel) — drop or rename rows that don't apply. Each card has a `data-book data-service="<key>"` button — keys must match `SHOP_CONFIG.services[*].key`.
5. **`over-ons.html`** — opleidingen-timeline rows: year + title + provider. Add/remove as needed.
6. **`locaties.html`** — single-location practical info. Update map embed URL to new address.
7. **`README.md`** — rewrite "Wat de klant moet doen vóór livegang" section with the client's actual slugs.

### 4. Test locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Click every booking CTA. Verify the modal opens, the right service is pre-selected (where applicable), all 4 pages link correctly.

### 5. Deploy

```bash
vercel
vercel env add CALCOM_API_KEY production
vercel --prod
```

Custom domain via Vercel dashboard → Settings → Domains.

## Common Customizations

### Practitioner has fewer than 6 massage types

Remove the unused service entries from `SHOP_CONFIG.services` AND the matching `<article>` cards in `behandelingen.html`. Update the section heading from "Zes vormen" to whatever fits ("Vier vormen", "Drie technieken", etc.).

### Practitioner offers stoelmassage on location (workplace)

Add a marketing bullet on `behandelingen.html` under the stoelmassage card; the booking modal can still work since it's a fixed-30-min event type. Optionally add a separate `stoel-locatie` service if pricing differs.

### Practitioner specializes in oncology / cancer-recovery

Keep the `#kanker` section in `behandelingen.html`. The `intake` service (gratis kennismakingsgesprek) is the entry point — pre-selected by `data-book data-service="intake"`.

If the practitioner is NOT trained in oncologic massage, remove the entire kanker section and the matching menu nav link.

### Practitioner wants a different accent color

Edit the `gold.DEFAULT` value in each HTML page's Tailwind config block (4 files) and in DESIGN.md. The class name `gold` stays — only the hex changes.

| Vibe | Hex |
|---|---|
| Warm terracotta (default) | `#B8654B` |
| Muted sage | `#7A8B6F` (the current botanical token) |
| Dusty rose | `#B86B7A` |
| Warm bronze | `#A87E4F` |
| Forest green | `#5B7A5B` |

Check WCAG: text on `#FAF6EF` cream needs ≥4.5:1 for body, ≥3:1 for large display.

## ⚠️ Verify Before Livegang Checklist

Same as `premium-spa-template` plus:

- [ ] All Cal.com event-type slugs exist and exactly match `SHOP_CONFIG.services` × durations
- [ ] Cal.com availability matches `SHOP_HOURS` exactly (test by booking a slot, then re-loading — should disappear)
- [ ] `CALCOM_API_KEY` is set on Vercel production
- [ ] Test end-to-end on production URL: open modal → service → duration → date → time → details → confirm → check inbox for confirmation email → check Cal.com dashboard for the booking
- [ ] Verify the .ics download has correct date/time/location after booking confirmation
- [ ] Practitioner's actual photos uploaded to `/images/` (or kept on their WP CDN for now)
- [ ] Reviews verified or replaced with anonymized excerpts
- [ ] Phone numbers in `tel:` links AND display copy match exactly
- [ ] Address verified — incl. postcode (the bron-site often only mentions street + city)

## Roadmap

- [ ] FAQ page (extend the "Praktisch" 6-card grid into a full page if needed)
- [ ] Newsletter signup (Mailchimp embedded form)
- [ ] LocalBusiness + MedicalBusiness Schema.org JSON-LD for SEO
- [ ] Multi-language variant (e.g. `/en/` mirror) — only if a clear use case
- [ ] Stripe checkout for cadeaubonnen

---

## Workflow refinements (from real-world batch builds)

When building 5 sites in one batch (May 2026 — Edith Libbers, Massages InBalans, Kanta Massage, B-KwieK, HomeMas — see `websites/massage-salons/`), these patterns emerged. Apply them BEFORE starting a new site.

### 1. Source-palette audit (NOT one-size-fits-all)

The cream + terracotta default works for Gerrit because his identity is holistic-body-therapeutic. For ANY new site, inspect the source-site's actual palette first:

```bash
curl -s -L -A "Mozilla/5.0" "<bron-url>/" -o /tmp/src.html
# Pull CSS hrefs, then fetch each, then count hex colors:
grep -oE '#[0-9a-fA-F]{3,6}' /tmp/style.css | sort | uniq -c | sort -rn | head -15
```

Identify the practitioner's signature non-default colors (the ones that aren't `#fff`, `#000`, browser-default greys, or framework defaults like WordPress blue `#1982d1`, Divi blue `#2ea3f2`, or W3CSS theme colors). Those are the brand.

Then pick a "similar but better" variant — same family, slightly refined for WCAG accessibility on a light-cream background. Tested examples:

| Site | Source signature | Refined palette accent |
|---|---|---|
| Edith Libbers | `#629a93` (muted teal in WP custom) | `#5C8784` jade |
| Massages InBalans | `#a8b691` (soft sage in Divi) + `#103455` (deep navy) | `#6B8A52` deeper sage + navy ink |
| Kanta Massage | `#cbd18f` + `#e3b448` + `#543636` (Simplybook brand colors) | `#A8911E` mustard + `#543636` brown |
| B-KwieK | `#fa9b16` (vibrant orange in Elementor) | `#D77E1F` refined amber |
| HomeMas | `#808040` (olive — old-school WP) | `#7E8B3A` refined olive |

**Why this matters:** The Tailwind class name `gold` stays — only the hex values change. So the markup is reusable across sites; only the palette block in `tailwind.config` + the inline SVG `fill=` / `stroke=` attributes differ.

### 2. Real reviews — Google first, bron-site fallback

The user wants real testimonials, never PLACEHOLDER. Order of preference:
1. **Google Maps reviews** via Places API (paid, but most authentic). For each site, scrape `https://www.google.com/maps/place/<name>/` — note this hits a consent-redirect via WebFetch, so requires the API.
2. **Bron-site recensies/aanbevelingen page** — many WP-based practitioner sites have a `/recensies/`, `/reviews/`, `/aanbevolen/` or similar page with real client quotes. Scrape and reuse verbatim, with a "Recensies overgenomen van [bron]" footer link.
3. **If nothing exists** — REMOVE the reviews section entirely (don't ship PLACEHOLDERs). Also remove the "Reviews" nav link on all pages. Note in README that the client should provide Google reviews when they have them.

### 3. Pexels integration for duplicate photo prevention

Solo-practitioner sites often have only 3–5 real photos. The blueprint has ~13 image slots across 4 pages, so duplication is inevitable without supplementation.

**Photo bank**: `skills/solo-massage-practitioner-template/pexels-photo-bank.json` — curated Pexels CDN URLs (no API key needed for hot-linking) in 6 themes:
- `spa_room` — interior spa shots
- `oil_massage` — oil-on-back, hands-on-shoulders
- `foot_massage` — voetreflex closeups
- `thai_massage` — Thai massage poses (stretches, wooden tools)
- `wellness_interior` — calm interiors, plants, candles
- `massage_general` — fallback variety

**Usage strategy per site:**
1. Audit: `grep -hoE 'src="https?://[^"]+\.(jpg|jpeg|png|webp)"' *.html | sort | uniq -c | sort -rn`
2. Keep real practitioner photos at **identity moments** (hero primary, over-ons intro, locaties primary card)
3. Replace within-page duplicates (same URL appearing 2+ times on one page) with thematic Pexels photos
4. Append `?auto=compress&cs=tinysrgb&w=1200` to Pexels URLs for sized variants

**Don't** replace empty-slot PLACEHOLDERs that say "vragen aan klant" — those are intentionally visible to the client during review.

### 4. Praktijk-teaser layout (6/6 with card on right)

The blueprint's original index.html had:
```html
<div class="grid lg:grid-cols-12 gap-10 lg:gap-16 items-end mb-14">
  <div class="lg:col-span-7">[kicker + heading]</div>
  <div class="lg:col-span-5">[paragraph]</div>
</div>
<a class="...block max-w-3xl mx-auto">[card]</a>   <!-- below, full-width -->
```

Better — 50/50 split with card on the right of the text content:
```html
<div class="grid lg:grid-cols-12 gap-10 lg:gap-16 items-center">
  <div class="lg:col-span-6">[kicker + heading + paragraph]</div>
  <div class="lg:col-span-6"><a class="..." block>[card]</a></div>
</div>
```

This is now the canonical layout in all 6 sites.

### 5. Floating "Boek nu" FAB

Persistent fixed bottom-right call-to-action on every page. Uses the site's accent color automatically (via Tailwind `bg-gold` class). Opens the existing booking modal via the `data-book` mechanism — no extra JS wiring needed.

Snippet to inject just before `</body>` on every page:
```html
<!-- ============ FLOATING BOOK CTA ============ -->
<a data-book href="#boeken" aria-label="Boek nu" class="cta-gold fixed bottom-5 right-5 sm:bottom-6 sm:right-6 z-40 inline-flex items-center gap-2 bg-gold text-white pl-4 pr-5 py-3 sm:pl-5 sm:pr-6 sm:py-3.5 rounded-full font-semibold text-sm tracking-wide shadow-xl hover:bg-gold-soft hover:-translate-y-0.5 transition-all" style="box-shadow: 0 10px 30px -8px rgba(0,0,0,0.25);">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="shrink-0"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
  <span>Boek nu</span>
</a>
```

z-40 keeps it under the booking modal (which is z-100) so it disappears behind the modal overlay automatically. Modal CSS doesn't need changes.

### 6. Reference builds

Five completed sites in `websites/massage-salons/` showcase these patterns:
- `gerrit-jonker-massage` — canonical blueprint (cream + terracotta, oncology specialization)
- `edith-libbers` — soft white + jade teal, NGS sportmasseur
- `massages-inbalans` — cream + deep navy + sage, Peace & Calming signature
- `kanta-massage` — cream + mustard + brown, Thai-style with 7 services
- `b-kwiek` — warm cream + refined amber, thin-content with explicit "vragen aan klant" markers
- `homemas` — olive cream + olive, Chinese Tui Na with pedicure

---

## Cross-cutting patterns

This template uses (or should use, when polishing) the shared patterns documented in [`../_shared-template-patterns.md`](../_shared-template-patterns.md). Skim that file when starting a new build for:

1. **Power-design rules** — ≥40% whitespace, 60-30-10 color, max 4 type sizes, borders-first cards, anti-pattern checklist
2. **Awesome-design-md DESIGN.md format** — 9 mandatory sections (Visual Theme, Color, Typography, Components, Layout, Depth, Do/Dont, Responsive, Agent Prompt Guide)
3. **`.vercel` collision protection** — always `rm -rf .vercel` before first `vercel --prod` in a copied folder
4. **Source-palette workflow** — derive "similar but better" palette from the bron-site CSS instead of reusing the blueprint default
5. **Pexels photo bank** — see `pexels-<niche>-bank.json` next to this SKILL.md, hot-link without API key
6. **Floating "Boek nu" FAB** — snippet for templates with online booking
7. **Reviews fallback chain** — Google Places API → bron-site → manual → remove section (never PLACEHOLDER cards)

See the quick-links table at the bottom of `_shared-template-patterns.md` to find which patterns specifically apply to this template.

