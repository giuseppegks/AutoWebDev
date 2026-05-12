---
name: Nailstudio-Template
description: Use when spinning up a new nailstudio / nail bar / press-on press-on studio website. The template is a light-cream Apple-influenced multi-page build (home + behandelingen + stijlen + studio) with a Pinterest-style masonry of nail-art looks, a split-layout interactive price-menu where the image crossfades on row hover, a clickable category-tabs filter, a sticky mobile "Boek nu" CTA, a live open/closed status badge that reads SHOP_HOURS, a Cal.com booking modal that walks Service → Date → Time → Details, and a Reviews section with placeholder cards + Google reviews link. Pairs Fraunces (display) with Inter (body) on a warm cream canvas (#FAF7F2), rose-gold accent (#B68F62), and a soft blush band (#F4DDD9). Distinct from `massage-shops-template` (Aurora — dark editorial, masseuse profiles), `premium-spa-template` (Royal Thai — dark wine + gold), and `barbershop-template` (single-page Cal.com). Triggers on phrases like "build a nail salon site for [shop]", "spin up a new nailstudio from template", "clone the Global Beautybar for [client]", "nail bar website", "press-on studio site", "premium nail salon site like Paintbox".
---

# Nailstudio Template — Spin-Up Workflow

## Overview

A reusable, deployable **multi-page light-premium** template for nail
salons, nail bars, and press-on studios. The aesthetic target is
"modern luxury editorial" — think **Paintbox NYC** + Apple's light
surface system + Pinterest's masonry pin-grid. Not spa-moody, not
beauty-blogger pastel — quiet, expensive, image-first.

**Reference build:** [websites/beauty-salons/the-global-beautybar/](../../websites/beauty-salons/the-global-beautybar/)
— live at https://the-global-beautybar.vercel.app and
https://github.com/maximetdoucet-glitch/The-Global-Beautybar.

## When to Use

Use this skill (instead of the massage / spa / barbershop variants) when
the shop:

- Sells **nail services** (acryl, BIAB, gellak, manicure, pedicure, nailart)
- Wants an **image-first browsing experience** — Pinterest-style gallery > spa-editorial blocks
- Has **a long structured price list** that benefits from category tabs + a split-layout menu where the image responds to row hover
- Prefers a **light, boutique-shop palette** (cream / white / warm gold / soft blush) over the dark wine/gold spa look
- Operates on **Cal.com** booking (or wants to migrate from Salonized/Treatwell to a branded UI)

Use a different skill when:

- The shop is a **single-page barbershop with one operator** → `barbershop-template`
- The shop is a **traditional massage parlour with masseuse profiles** → `massage-shops-template`
- The shop is a **dark-luxury spa with phone-first booking** → `premium-spa-template`
- The shop has **no published service catalog** → `building-prospect-mockups` first

## Architecture

```
nailstudio/
├── index.html              ← home: hero + Pinterest masonry + blush band +
│                              split-layout price menu + reviews + visit
├── nagels.html             ← full prijslijst — split-layout, ALL services,
│                              same interactive image swap as homepage
├── stijlen.html            ← masonry gallery, category-filtered (Acryl /
│                              BIAB / Manicure / Pedicure / Nailart)
├── over-ons.html           ← editorial split-hero ("Eén paar handen, volle
│                              aandacht") + practical cards. INFORMATIONAL —
│                              no in-page CTAs by design
├── api/
│   ├── _cal.js             ← Bearer auth, cal-api-version pinning
│   ├── event-types.js      ← GET — Cal.com event types
│   ├── slots.js            ← GET — available slots
│   └── bookings.js         ← POST — creates a booking
├── css/style.css           ← single stylesheet (~3 000 lines, design
│                              tokens at :root + override blocks per version)
├── js/main.js              ← all interactivity (SHOP/SHOP_HOURS/SERVICES
│                              config at top, then booking modal, scroll
│                              reveals, live status badge, sticky CTA toggle)
├── package.json
├── vercel.json
└── .env.example
```

## Design system

### Palette — light premium

```css
:root {
  --bg:        #FAF7F2;   /* warm cream canvas */
  --bg-2:      #FFFFFF;   /* white surface */
  --surface:   #FFFFFF;
  --surface-2: #F5F0E6;
  --line:      #E8E0D2;
  --line-soft: #F0EAE0;
  --bone:      #1D1D1F;   /* Apple ink — primary text */
  --bone-dim:  #555150;
  --text:      #2A2A2A;
  --muted:     #86827A;
  --gold:      #B68F62;   /* warm rose-gold accent */
  --gold-2:    #946F42;
  --rose:      #6B1F3B;   /* used only for negative-state dot */
  --blush:     #F4DDD9;   /* soft blush — band callouts + avatars */
  --blush-deep:#D8B5AC;
}
```

60-30-10 split:
- 60% cream + white surfaces
- 30% charcoal text
- 10% rose-gold for CTAs, eyebrows, links, hover accents
- ~1% blush as a warm callout for the band section + review avatars

### Typography

```css
--serif: "Fraunces", "Cormorant Garamond", "EB Garamond", Georgia, serif;
--sans:  "Inter", -apple-system, "Segoe UI", Roboto, system-ui, sans-serif;
```

Google Fonts import:
```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=Inter:wght@300;400;500;600;700" rel="stylesheet">
```

Fraunces handles display + italic accents in `<em>`. Inter handles body
+ eyebrows (uppercase with 0.18–0.24em letter-spacing). Never bold the
serif — use Fraunces 400/500 with italic for emphasis instead.

## Key patterns (don't rebuild — copy and adapt)

### 1. Split-layout interactive price-menu (homepage + /nagels)

Two-column grid: sticky nail-art image left, menu rows right. Image
crossfades on row hover (desktop) and on tab click. The killer feature.

```html
<div class="menu-section__grid">
  <div class="menu-image" id="menu-image">
    <div class="menu-image__layer" data-layer="a" style="background-image:url('...');"></div>
    <div class="menu-image__layer is-out" data-layer="b"></div>
    <span class="menu-image__caption" id="menu-image-caption">Alle behandelingen</span>
  </div>
  <div class="menu-list" data-active="all">
    <!-- groups with data-cat + rows with data-img + data-label -->
  </div>
</div>
```

Each `.menu-list__row` carries `data-img="<pexels-url>"` +
`data-label="Treatment · €XX"`. Each tab carries the same plus
`data-menu-filter="<category>"`.

Inline JS at end of page wires up the crossfade — see the canonical
build's `index.html` near the closing `</body>`. The pattern uses two
absolutely-positioned `.menu-image__layer` divs; one is `.is-out`
(opacity: 0), the other visible. On change, we swap which is `.is-out`.
Forced reflow before fade so the new background-image has had time to
load before the opacity transition starts.

Row hover is gated by `window.matchMedia('(hover: hover)').matches` so
touch devices don't trigger awkward swaps on tap-near-row.

### 2. Pinterest masonry pin-grid (homepage `#looks` + `/stijlen`)

CSS-columns (no JS library) for the masonry. Each pin is a fully-rounded
16px-radius card; on hover a cream-on-blur caption pill appears bottom-left.

```css
.gallery__masonry { column-count: 4; column-gap: 12px; }
@media (max-width: 1100px) { column-count: 3; }
@media (max-width: 760px)  { column-count: 2; column-gap: 8px; }

.gallery__pin {
  position: relative;
  margin: 0 0 12px;
  border-radius: 16px;
  overflow: hidden;
  break-inside: avoid;
}
.gallery__pin .gallery__pin-img {
  aspect-ratio: var(--ratio, 3/4);
  background-size: cover;
  background-position: center;
}
```

Mix aspect ratios per pin via inline `style="--ratio:3/4"`, `1/1`, `4/5`
for visual variety. Click on any pin opens the booking modal with that
service pre-selected (via `data-open-book data-service="<slug>"`).

### 3. Live open/closed status badge (hero)

```html
<span data-shop-status><strong>Ma – Za</strong> · 10:00 – 18:00</span>
```

`main.js` reads `SHOP_HOURS` + current time, sets `data-state="open"`
or `data-state="closed"`, and rewrites the inner HTML to one of:
- `Vandaag open · 10:00 – 18:00` (green dot)
- `Gesloten · vandaag open 10:00` (wine dot)
- `Gesloten · morgen weer open` (wine dot)
- `Gesloten · maandag 12:00` (wine dot, day-of-week aware)

Re-renders every 60 s so a visitor sitting on the page across the
opening hour sees it tick over.

### 4. Mobile sticky "Boek nu" CTA

Floating gold pill bottom-center on ≤880px, appears after
`body.is-scrolled-past-hero` (set by JS when `scrollY > 360`). Hidden
when the booking modal is open (`body:has(.book:not([hidden]))`).
Lives on the conversion-oriented pages (`/index`, `/nagels`,
`/stijlen`) but is **deliberately omitted from `/over-ons`** which is
positioned as purely informational.

### 5. Split-hero (sub-page editorial header)

Used on `/over-ons` for "Eén paar handen, volle aandacht." Two-column
grid: 4/5 nail-art photo left, eyebrow + display headline + lede + stat
strip right. Mobile stacks; image becomes a 4/5 banner above the copy.

### 6. Editorial reviews section

Three review-cards in a grid, italic Fraunces quote with a gold quote-mark
ornament, small blush-colored avatar with the reviewer's initial, "Lees
alle reviews op Google →" link to the shop's Google Maps listing.

**Honesty default:** ships with placeholder reviews (Sanne K., Lisa M.,
Yara H.) marked with a visible blush pill "Voorbeelden — vervang met
echte Google reviews vóór livegang" AND a prominent HTML comment block
above the section. Never invent specific quotes claiming to be real.

### 7. Blush band

Soft pink (`var(--blush)`) full-width band between sections. One
display heading + a short lede + a CTA. Functions as a "breathing
station" between gallery and menu, or before the visit section.

## Spin-Up Workflow

### 1. Verify the shop (5 min — non-negotiable)

WebSearch the shop name + city. Confirm:
- Address, phone, email, Instagram handle
- The shop actually offers **nail services** (not a general beauty bar
  with no nails — common with names like "Beauty Bar" that turn out to
  be lash / facial / massage)
- Opening hours (Google Maps + their existing Salonized/Treatwell page)
- Service catalog with prices (Salonized URL pattern:
  `https://<slug>.salonized.com/services`)

Output a **fact audit** before writing any copy:
- ✅ verified · ⚠️ plausible · ❌ unknown
- Drop all ❌ from the build
- Show the audit to the user before generating content

### 2. Clone the canonical build

```bash
cp -r websites/beauty-salons/the-global-beautybar websites/beauty-salons/<slug>
cd websites/beauty-salons/<slug>
rm -rf .git
git init
```

### 3. Edit the SHOP config in `js/main.js`

Top of the file — only block that should ever change per shop:

```js
const SHOP = {
  name: "...",
  fullName: "...",
  phone: "+31...",
  phoneDisplay: "06 ...",
  whatsapp: "31...",        // wa.me format
  email: "...",
  address: "...",
  timezone: "Europe/Amsterdam",
  language: "nl",
  instagram: "...",
};

const SHOP_HOURS = {
  1: [12, 18], // Monday
  2: [10, 18], // ...
  // closed days are absent
};

const SERVICES = {
  "<slug>": { label: "...", cat: "Acryl", duration: 60, price: 45 },
  // ...
};
```

### 4. Update the 4 HTML pages

The service rows + Pexels image URLs are baked into HTML (not rendered
from `SERVICES` — keeps it SEO-friendly). Per-row changes:

| Where | What to change |
|---|---|
| `index.html` hero | Title, sub, lede |
| `index.html` looks masonry | 16 pins with `data-img` + caption + `data-service` |
| `index.html` menu-list | Teaser ~5 rows per category + link to /nagels#cat |
| `index.html` reviews | Placeholder names + quotes (mark TODO clearly) |
| `index.html` visit | Address, phone, WhatsApp, email, hours table |
| `nagels.html` | Full menu — every service the shop offers |
| `stijlen.html` | Masonry pins per category, `data-category` for filters |
| `over-ons.html` | Split-hero copy, practical cards |

For imagery: pull from Pexels (search "nail art", "manicure", "gel
manicure"). URL format:
```
https://images.pexels.com/photos/<ID>/pexels-photo-<ID>.jpeg?auto=compress&cs=tinysrgb&w=1200
```

Add `<link rel="preconnect" href="https://images.pexels.com" crossorigin>`
to every page's `<head>` for faster paint.

### 5. Cal.com setup

1. Sign up at https://cal.com (free for single user)
2. Set availability matching `SHOP_HOURS` exactly
3. Create an event type for **every** `SERVICES` key — the slug must
   match exactly (`acryl-french-nieuw`, `mani-gellak`, etc.)
4. Generate an API key
5. `vercel env add CALCOM_API_KEY production`

Until the API key is set, the booking modal lands at step 4 with a
friendly "deze behandeling is nog niet aangemaakt" hint.

### 6. Deploy

```bash
git add . && git commit -m "Initial build for <shop>"
gh repo create <slug> --public --source=. --push
npx vercel --prod
```

Add custom domain in Vercel → Settings → Domains.

## Cache-bust discipline

`vercel.json` sets `Cache-Control: public, max-age=31536000, immutable`
on `.jpg/.mp4/.css/.woff2`. **Bump the `?v=N` query strings** on
`style.css` and `main.js` every time you change those files — otherwise
returning visitors keep the stale copy for up to a year:

```bash
# Bump cache-bust across all HTML files in one go
node -e "
const fs = require('fs');
const N = 7; // new version
['index.html','nagels.html','stijlen.html','over-ons.html'].forEach(f => {
  let c = fs.readFileSync(f, 'utf-8');
  c = c.replace(/style\.css\?v=\d+/g, 'style.css?v=' + N);
  c = c.replace(/main\.js\?v=\d+/g, 'main.js?v=' + N);
  fs.writeFileSync(f, c);
});
"
```

## Mobile pass — what's already done

The canonical build ships with a layered breakpoint ladder. Don't
touch the desktop rules in the body of the stylesheet — append
overrides at the end.

| Width | What changes |
|---|---|
| **≤880px** | Nav switches to burger (with `is-open` drawer including the Boek nu CTA); split-layout menu stacks (image → menu); split-hero stacks (image → copy + stats) |
| **≤760px** | Tab bars (`.menu-list__tabs`, `.gallery__filters`) become horizontally scrollable strips with a soft mask-image fade at both edges; hero's top-right badges hidden; masonry → 2 cols; reviews → 1 col |
| **≤600px** | Booking modal full-screen with sticky footer; menu rows stack name → meta → CTA single-column; footer 1-col; subhero padding halved |
| **≤420px** | Hero title bumped down further; masonry gap → 6px |
| **≤380px** | iPhone-SE-class — booking modal service-cards get smaller meta text; menu row price-pill scales down |

**Special mobile patterns to preserve verbatim:**

1. **`100svh` not `100vh`** — iOS Safari's `100vh` jumps when the URL
   bar toggles. The `@supports (height: 100svh) { .hero { min-height: 100svh; } }` block handles this.

2. **iOS auto-zoom defeat** — any `<input>` or `<textarea>` below 16px
   triggers iOS to zoom into the field on focus. The
   `@supports (-webkit-touch-callout: none)` block forces
   `font-size: max(16px, 1rem) !important` on form controls.

3. **44px touch targets** — Fitts's Law. `.nav__burger`, `.book__close`,
   `.menu-list__tab` all have `min-width: 44px; min-height: 44px` on phone.

4. **Themed tap highlight** — `-webkit-tap-highlight-color: rgba(0,0,0,.08)`
   instead of the default electric blue.

## Booking flow

1. Hero CTA / sticky CTA / gallery pin / menu row CTA → modal opens
   (with service pre-selected if launched from a pin or row)
2. Step 1: visitor confirms / picks treatment from the categorized list
3. Step 2: calendar; closed days disabled
4. Step 3: slot grid from `SHOP_HOURS`
5. Step 4: name, phone, email, optional wensen
6. Submit → POST `/api/bookings` to the Cal.com proxy
7. Confirm screen with summary + WhatsApp deep link for changes

If the Cal.com proxy fails (no key, no event type for slug, network
error) the confirmation hint shows a phone CTA + WhatsApp fallback.

## Honesty principles (non-negotiable)

Per `building-local-business-website`:

1. **Never invent specific prices, treatments, hours, or founder names.**
2. **Verify via 2+ sources** for any "since 20XX" or staff-count claims.
3. **Vague-but-true beats specific-and-fake.** "Geen wachtkamer, geen
   geroezemoes" is fine if true. "Sinds 2016" requires a source.
4. **Mark placeholder reviews clearly** — both in HTML comment + a
   visible "voorbeelden — vervang vóór livegang" pill.
5. **No invented owner names.** The Global Beautybar's owner contact
   email contains a name; that's still kept off the public site (marked
   ⚠️ plausible in the fact audit, never published).

## Pitfalls

- **Don't ship placeholder reviews silently.** The visible pill + HTML
  TODO comment is the contract. Always check `grep "Voorbeelden"`
  before the client demo.
- **Cal.com event type slugs MUST match SERVICES keys exactly.** A typo
  ("acryl-french-new" vs "acryl-french-nieuw") = silent failure at submit.
- **Pexels URL hot-linking is fine for demos but unstable for production.**
  Curate a set of self-hosted nail-art photos before final handover
  (see Photo TODOs in the canonical README).
- **`vercel.json` `immutable` cache means a stale CSS bug haunts users
  for a year unless you bump the `?v=N` query.** Bump on every CSS/JS
  edit.
- **Don't add a sticky CTA to `/over-ons` (informational page).**
  Conversion CTAs there violate the page's information-only intent.
- **Don't change palette tokens lightly.** The cream + rose-gold +
  blush trio passes WCAG AA on bone text; ad-hoc swaps usually don't.

## Selling notes

- **Lead with the masonry + interactive menu** in cold-outreach. A live
  image swap on row hover is a strong "wow" moment.
- **Position the live status badge as a trust signal** — "Vandaag open"
  is more reassuring than a static hours table.
- **The reviews section is wired for Google reviews from day one** —
  just swap the 3 placeholders for verbatim quotes and the section
  flips from "voorbeelden" to "echte stem".
- **Premium light palette positions the shop above competitors that
  use Salonized's default theme.** Salonized + Treatwell sites all
  look the same; a branded studio site at the same domain ranks higher
  and converts better.

## Future Improvements (for the next iteration)

- **Real Google Places API integration** for live review pulls — would
  remove the "voorbeelden" pill and auto-update star count
- **Slot availability check** — wire `renderSlots()` to `/api/slots`
  so booked times are visibly disabled instead of all slots showing
- **Multi-language** — NL / EN switcher (Fraunces handles both)
- **Self-hosted nail-art** — replace Pexels with a curated 30-photo
  set delivered as WebP via Vercel's image CDN
- **`<picture>` with `srcset`** for the masonry — currently single
  `?w=900` URL; could serve 600/900/1200 responsive
- **Schema.org `LocalBusiness` + `Review` structured data** for SEO

## Reference live build

- **URL:** https://the-global-beautybar.vercel.app/
- **Repo:** https://github.com/maximetdoucet-glitch/The-Global-Beautybar
- **Local:** [websites/beauty-salons/the-global-beautybar/](../../websites/beauty-salons/the-global-beautybar/)

The canonical build is the source of truth. When in doubt, diff against
that repo before spinning up a new shop.

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

