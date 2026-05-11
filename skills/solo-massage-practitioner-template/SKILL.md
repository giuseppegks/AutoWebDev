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
