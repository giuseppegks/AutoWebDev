# The Global Beautybar — Nijmegen

Multi-page presentational site for **The Global Beautybar**, a nailstudio
on Zwanenveld 8403 in Nijmegen-Dukenburg. Built by combining three
template skills:

- **massage-shops-template** (Aurora) — 4-page editorial structure, booking modal, hero pattern, scroll reveals
- **booking-system** (Cal.com proxy) — server-side `/api/*` endpoints
- **Royal Thai blueprint** — design tokens (burgundy + warm gold + cream, Cormorant Garamond + Manrope)

Vertical: **nails salon**. Verified via the shop's existing Salonized
listing and Instagram bio ("Nail Tech"). Source of truth for prices,
hours and services: <https://the-global-beautybar.salonized.com/>.

## Stack

- Vanilla HTML + custom-property CSS + ES module JS (no build step)
- Google Fonts: Cormorant Garamond + Manrope
- Cal.com v2 REST API proxied via Vercel serverless functions
- Vercel for hosting (Hobby tier is free for this shape of site)

## Project structure

```
the-global-beautybar/
├── index.html              ← home: hero, about, services teaser, signature styles, sfeer, visit
├── nagels.html             ← full prijslijst (31 services in 5 categorieën)
├── stijlen.html            ← editorial detail rows per category
├── over-ons.html           ← studio + werkwijze + praktisch
├── api/
│   ├── _cal.js             ← Bearer auth, version pinning, response normalization
│   ├── event-types.js      ← GET — lists Cal.com event types
│   ├── slots.js            ← GET — available slots for a day
│   └── bookings.js         ← POST — creates a booking via Cal.com v2
├── css/style.css           ← single stylesheet (design tokens at :root)
├── js/main.js              ← all interactivity in one file (SHOP config at top)
├── images/                 ← TODO: replace placeholder photos (see Photo TODOs below)
├── videos/                 ← unused on this build — kept for future video hero
├── audio/ambient.mp3       ← spa loop for the homepage Sfeer toggle
├── package.json
├── vercel.json
└── .env.example
```

## Local development

```bash
cd the-global-beautybar
npm run dev          # http://localhost:3000  (static only)
# OR
npx vercel dev       # full stack including /api/* proxies
```

Serverless functions (`/api/*`) only run under `vercel dev` or on
Vercel. Plain `npm run dev` serves the static site but the booking
modal will fail at step 4 without a backend.

## Cal.com setup (BEFORE going live)

1. Sign up at <https://cal.com>. Single-user is free.
2. Configure availability: Cal.com → Settings → My Availability.
   **Must match** `SHOP_HOURS` in `js/main.js`:
   - Mon 12:00 – 18:00
   - Tue – Sat 10:00 – 18:00
   - Sun closed
3. For each entry in `SERVICES` (see `js/main.js`), create a Cal.com
   **event type** at <https://cal.com/event-types>. The slug **must
   match exactly**. See the slug list below.
4. Generate an API key at <https://cal.com/settings/developer/api-keys>.
   Set it in Vercel:
   ```bash
   vercel env add CALCOM_API_KEY production
   ```

### Event type slugs to create

| Slug | Length | Price |
|---|---|---|
| `acryl-naturel-nieuw` | 60 min | €45,00 |
| `acryl-naturel-opvullen` | 60 min | €40,00 |
| `acryl-gellak-nieuw` | 60 min | €50,00 |
| `acryl-gellak-opvullen` | 60 min | €45,00 |
| `acryl-babyboom-nieuw` | 60 min | €55,00 |
| `acryl-babyboom-opvullen` | 60 min | €50,00 |
| `acryl-french-nieuw` | 60 min | €55,00 |
| `acryl-french-opvullen` | 60 min | €50,00 |
| `biab-naturel-nieuw` | 60 min | €50,00 |
| `biab-naturel-opvullen` | 60 min | €45,00 |
| `biab-gellak-nieuw` | 60 min | €55,00 |
| `biab-gellak-opvullen` | 60 min | €50,00 |
| `biab-french-nieuw` | 60 min | €60,00 |
| `biab-french-opvullen` | 60 min | €55,00 |
| `mani-knippen` | 15 min | €10,00 |
| `mani-klassiek` | 30 min | €15,00 |
| `mani-gellak` | 30 min | €30,00 |
| `mani-gellak-french` | 45 min | €35,00 |
| `mani-gellak-met-verw` | 45 min | €32,50 |
| `mani-met-gellak` | 45 min | €35,00 |
| `pedi-knippen` | 15 min | €10,00 |
| `pedi-spa` | 30 min | €40,00 |
| `pedi-spa-gellak` | 60 min | €50,00 |
| `pedi-spa-french` | 60 min | €55,00 |
| `pedi-gellak` | 30 min | €30,00 |
| `pedi-gellak-french` | 30 min | €35,00 |
| `pedi-gellak-met-verw` | 30 min | €32,50 |
| `extra-reparatie` | 15 min | €3,00 |
| `extra-nailart` | 15 min | €2,00 |
| `extra-verw-gellak` | 15 min | €10,00 |
| `extra-verw-biab` | 30 min | €15,00 |

## Deploy to Vercel

```bash
cd the-global-beautybar
npx vercel
npx vercel env add CALCOM_API_KEY production
npx vercel --prod
```

Then add the production domain in Vercel → Settings → Domains.

## Photo TODOs (before client handoff)

The current images are placeholders inherited from the Aurora massage
template (moody dark-warm photos that still _function_ visually in this
palette but don't depict the shop). Before going live, replace these —
keep filenames identical so HTML doesn't need touching:

- `images/hero-poster.jpg` — front-of-studio shot or signature nail-art close-up
- `images/suites/egypt.jpg` — Acryl French (Stijl I on /stijlen)
- `images/suites/japanese.jpg` — Acryl Babyboom (Stijl II)
- `images/suites/hamam.jpg` — BIAB French (Stijl III)
- `images/suites/thai.jpg` — Spa Pedicure French (Stijl IV)
- `images/sfeer/01.jpg` – `06.jpg` — six atmosphere shots for the homepage scroller

Then bump `CACHE_BUST` in `js/main.js` (currently `v=1`) and the `?v=`
query strings in HTML — Vercel's immutable cache header would otherwise
keep serving the old files.

## What was adapted from Aurora

Removed (massage-specific):

- Hero video rotator (4 atmospheric clips) → static still hero
- Masseuse roster (Vandaag/Morgen filtered by `weekdays:[]`)
- Masseuse detail modal with photo gallery
- Suite dropdown in booking modal step 1
- Masseuse picker chips in booking modal step 1
- WhatsApp deep-link confirmation flow (booking-request mode)

Kept (transferable):

- Sticky nav with mobile burger menu
- Reveal-on-scroll via IntersectionObserver
- Editorial section pattern (eyebrow + display heading + sub)
- 4-step booking modal scaffold (Service → Date → Time → Details)
- Calendar renderer with horizon + closed days
- Slot grid renderer from `SHOP_HOURS`
- Ambient audio toggle on the homepage
- Sfeer scroller, alternating editorial rows
- Mobile breakpoint ladder (880 / 760 / 600 / 380)
- iOS 16px input-size rule

Added (nails-specific):

- Full menu with prices (table layout on `/nagels`)
- Service-category labels inside booking modal step 1
- Method cards + practical cards on `/over-ons`
- Active-page indicator in nav

## Booking flow

1. User clicks "Boek nu" → modal opens at step 1
2. Step 1: scrolls list of 31 services (grouped by category), picks one
3. Step 2: picks date from calendar (closed days disabled)
4. Step 3: picks time slot from `SHOP_HOURS` grid
5. Step 4: enters name, phone, email, optional wensen
6. Submit → POST `/api/bookings` with Cal.com v2 payload
7. Confirmation screen shows summary + WhatsApp link for changes

If the Cal.com proxy fails (missing event type, network error), the
confirmation hint shows a phone CTA + WhatsApp fallback so the customer
can still reach the shop manually.

## Known gaps (future work)

- Slot availability check: `renderSlots()` currently shows all slots
  from `SHOP_HOURS` without calling `/api/slots`. The proxy is wired
  and ready; upgrading the slot renderer to compare against real Cal.com
  availability is a ~30-line change.
- Multilingual switcher (NL / EN) — copy is NL-only.
- Owner-name not published anywhere on the site; only the contact email
  hints at "Bich Hao Pham" but we treat this as plausible-not-verified.
- Real photography — see Photo TODOs.
- Schema.org `LocalBusiness` structured data for SEO.

## Fact audit (verified May 2026)

- Name: ✅ "The Global Beautybar" (Salonized + IG)
- Vertical: ✅ nails salon — IG bio "Nail Tech"
- Address: ✅ Zwanenveld 8403, 6538 TL Nijmegen
- Phone: ✅ 06 34 56 56 53
- Email: ✅ bichhao_pham@hotmail.com
- Instagram: ✅ @theglobalbeautybar
- Opening hours: ✅ Mon 12–18, Tue–Sat 10–18, Sun closed
- 31 services with prices: ✅ scraped from Salonized services page
- Owner's name: ⚠️ inferred from email — not published, kept off-site
- Founding year, staff count, signature claims: ❌ unknown — omitted

Per `building-local-business-website` skill: vague-but-true beats
specific-and-fake. No invented prices, durations, founder names, or
process claims appear in the HTML.
