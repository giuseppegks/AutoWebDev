---
name: Massage-Shops-Template
description: Use when spinning up a new massage parlour, spa, or wellness salon website from the proven Aurora multi-page template. The template is dark-editorial (4 pages — home, massages, suites, masseuses) with: full-bleed hero video rotator with per-clip duration caps, custom 4-step booking modal that combines massage + suite dropdown + masseuse photo chips, masseuse detail modal with photo gallery (prev/next + thumbnails) and bio + specialties + availability, today/tomorrow roster on homepage filtered by each masseuse's weekdays, variant card grids for long massage menus, ambient audio toggle with scroll auto-pause, and a CACHE_BUST constant for swapping assets under Vercel's immutable Cache-Control. Triggers on phrases like "build a massage parlour site for [shop]", "spin up a new spa from the Aurora template", "clone Aurora for [client]", "new massage salon site", "wellness website with masseuse profiles", "erotic massage site like Aurora".
---

# Massage Shops Template — Spin-Up Workflow

## Overview

A reusable, deployable **multi-page** template for massage parlours, spas, and wellness salons. Distinct from `barbershop-template` (which is single-page + Cal.com): this template is editorial, four pages, with deeper masseuse profiles and a request-booking flow.

**Reference template:** [github.com/maximetdoucet-glitch/Aurora](https://github.com/maximetdoucet-glitch/Aurora) — the Aurora Massages build is the canonical source.

## When to Use

Use this skill (instead of `barbershop-template`) when the shop has:

- A **roster of named masseuses/therapists** that visitors want to browse by photo + bio
- **Themed suites/rooms** (Egypt / Japanese / Hamam / Thai etc.) the visitor can book by name
- A **long, structured menu** (e.g. 14+ Tantra variants) better shown as a card grid than a list
- **Editorial copy in Dutch** (or another language using the same eyebrow + display pattern)
- A preference for **WhatsApp confirmation** over real-time calendar booking

Use `barbershop-template` instead when the shop is a single-page presentational site driven by a Cal.com calendar with no masseuse profiles or themed rooms.

## Two Booking Variants

The Aurora build ships with the **request-booking** variant. The same UI shell can drive Cal.com if needed:

| Vertical | Booking layer | Notes |
|---|---|---|
| **Therapeutic / wellness** (Chill & Refill, Baipho, Kanta) | Cal.com proxy via `/api/_cal.js` | Same as `barbershop-template` |
| **Erotic / sensual** (Aurora, Massagewereld, Le Fouet) | Request-booking via `/api/booking-request` | WhatsApp deep link + email confirmation. Vercel AUP grey area — be ready to migrate to Hetzner+Caddy if suspended. |

A `BOOKING_MODE` constant in `js/main.js` selects the endpoint. UI flow is identical.

## Architecture (4 pages)

```
aurora-massages/
├── index.html              # Home: hero video + about + services + suites + roster + sfeer + visit
├── massages.html           # Full menu — detail rows + 3-up variant card grids per category
├── suites.html             # Each suite as an editorial detail-row spread
├── masseuses.html          # Team grid + values + clickable detail modal
├── audio/
│   ├── ambient.mp3         # Pixabay/Mixkit royalty-free spa loop
│   └── README.txt
├── css/style.css           # Single stylesheet (editorial dark + accent)
├── js/main.js              # All interactivity in one file (config block at top)
├── images/
│   ├── aurora-source/      # Hero shots per massage type (b2b, tantra, hamam, etc.)
│   ├── masseuses/          # Per-person photos: alex.jpg, alex-2.jpg, …
│   ├── sfeer/              # 6 atmosphere shots for the homepage scroller
│   ├── suites/             # 4 suite room photos
│   └── README.txt
├── videos/
│   ├── hero-1.mp4          # Candle (cap to ~2s)
│   ├── hero-2.mp4          # Grey cover (cap to ~3s)
│   ├── hero-3.mp4          # Massage clip
│   ├── hero-4.mp4          # Massage clip
│   └── README.txt
├── api/
│   └── booking-request.js  # POST handler — sends email + Telegram (server-side)
├── package.json
├── vercel.json             # immutable Cache-Control on .jpg/.mp4 — see CACHE_BUST below
└── .gitignore
```

### Built-in features (don't rebuild — copy and adapt)

1. **Hero video rotator** — `<video data-src="..." data-max-seconds="2">` plays clips in sequence, capping each clip's display time. Set `data-max-seconds` to trim a long clip; omit to play full duration.
2. **Roster section** (homepage) — filters `MASSEUSES_DATA` by today's `Date.getDay()` against each entry's `weekdays:[1,2,4,6]` array and shuffles deterministically by date so the order is stable per day but rotates daily.
3. **Masseuse detail modal** — split-panel: photo gallery (prev/next + thumbnail strip + keyboard nav + counter) on the left, bio + specialty chips + availability days + book CTA on the right.
4. **Booking modal step 1** — three groups: massage cards (required), suite custom dropdown (optional), masseuse photo-chip horizontal scroller (optional, includes "Geen voorkeur" first).
5. **Variant card grids** (massages.html) — for categories with many sub-types (Tantra has 14), use `.variant-grid` 3-up cards rather than a list.
6. **Custom suite dropdown** — div-based (not native `<select>`) so it matches the dark/gold modal aesthetic; opens on click, closes on outside click / ESC / option select.
7. **Ambient audio toggle** — fixed bottom-right "Sfeer" pill with animated wave bars. Off by default (browsers block autoplay-with-sound). Auto-pauses on scroll past ~70% of viewport. Volume 0.45. Persists in localStorage.
8. **CACHE_BUST helper** — `vercel.json` sets `Cache-Control: public, max-age=31536000, immutable` on `.jpg` and `.mp4`. When you replace an asset's contents without changing its URL, browsers serve stale forever. The `cb()` helper in `main.js` appends `?v=N` to every image/video URL — bump `CACHE_BUST` to force re-download. Don't remove the immutable cache — it's good for repeat visits.

## Spin-Up Workflow (per shop)

### 1. Gather content (the slow part — 1–3 hours)

Pull from the client's existing site / Instagram / WhatsApp:

- Logo or brand initial for the monogram
- Hero video clips: candle, ambience, massage detail (no people for adult vertical — legal/discretion)
- Per-masseuse: 1–6 photos, name, 1-line tagline, 1-paragraph bio, list of services they offer, days they typically work
- Per-suite: 1 hero photo, 1-paragraph description, USP
- Atmosphere shots (6) for the homepage sfeer scroller
- Per-massage-type: 1 hero photo + intro paragraphs + list of variants
- Address, phone, WhatsApp, email, opening hours, KVK
- Royalty-free ambient audio (Pixabay → free for commercial use, no attribution)

**Verify against ground truth.** Never invent prices, names, hours, or specialties. For erotic shops also Google `"<name> <city>"` to confirm the vertical before pitching — adult vs therapeutic determines hosting + booking choices.

### 2. Clone the template

```bash
git clone https://github.com/maximetdoucet-glitch/Aurora <shop-slug>
cd <shop-slug>
rm -rf .git
git init
```

### 3. Replace assets

- `images/masseuses/` — per person, primary as `<slug>.jpg` plus optional `<slug>-2.jpg`, `<slug>-3.jpg` …
- `images/suites/` — `egypt.jpg`, `japanese.jpg`, `hamam.jpg`, `thai.jpg` (or rename to the shop's actual room names)
- `images/aurora-source/` — rename folder to `<shop>-source/` and update HTML refs; provides hero shots for each massage type's detail row
- `images/sfeer/` — 6 atmospheric shots
- `videos/hero-1.mp4` … `hero-4.mp4` — atmospheric clips, no people for adult vertical
- `audio/ambient.mp3` — spa loop from Pixabay/Mixkit
- `images/hero-poster.jpg` — first frame of hero-1 so the page doesn't flash black

### 4. Edit the SHOP config block in `js/main.js`

```js
const SHOP = {
  name: "Aurora",
  fullName: "Aurora Massages Nijmegen",
  phone: "+31243502776",
  phoneDisplay: "024 350 2776",
  whatsapp: "31243502776",
  email: "balie@auroramassages.nl",
  address: "Heidebloemstraat 79, 6533 SM Nijmegen",
  timezone: "Europe/Amsterdam",
  language: "nl",
};

const SHOP_HOURS = { 1: [10, 22], 2: [10, 22], ... };  // Sun=0..Sat=6

const SERVICES = { tantra: "Tantra", b2b: "Body 2 Body", ... };

const SUITES = { egypt: "Egypt Suite", ... };

const BOOKING_MODE = "request";  // or "cal" once Cal.com proxy is wired

// IMPORTANT: bump this whenever you replace asset contents at the same URL
const CACHE_BUST = "v=1";
```

### 5. Replace `MASSEUSES_DATA` in `js/main.js`

For each masseuse:

```js
slug: {
  name: "Isabel",
  photos: [
    "images/masseuses/isabel.jpg",
    "images/masseuses/isabel-2.jpg",
  ],
  tagline: "Slank · donkerblond · gevangen ogen",
  bio: "Een slanke verschijning met lange donkerblonde haren …",
  specialties: ["Hot Sensual Tantra", "Lingam Massage", "Body to Body"],
  days: "Maandag · Dinsdag · Donderdag · Zaterdag",  // human-readable
  weekdays: [1, 2, 4, 6],                            // for Vandaag/Morgen filter
},
```

`weekdays` drives the homepage roster — keep it in sync with `days`.

### 6. Edit the four HTML pages

Find-and-replace per page:

| File | What to change |
|---|---|
| `index.html` | hero title + lede, about copy (3 paragraphs), services cards (4), suite rows (4 — alternating editorial), visit address + map iframe, footer |
| `massages.html` | per category: hero detail-row image, intro paragraphs, variant cards (`<article class="variant-card">`) |
| `suites.html` | per suite: hero photo, copy block |
| `masseuses.html` | masseuse grid (one `<button class="masseuse-card" data-masseuse="<slug>">` per person), value cards, notice text |

The `data-masseuse="<slug>"` on cards must match keys in `MASSEUSES_DATA` — that's how the modal hydrates.

### 7. Update `vercel.json` and the favicon / OG image

`vercel.json` already sets `cleanUrls: true`, security headers, and immutable cache for assets. Usually no changes needed.

### 8. Adjust the palette in `css/style.css` `:root`

Aurora uses amber gold for an adult/sensual vertical. For wellness verticals swap the accent:

```css
:root {
  /* keep these — they're vertical-agnostic dark warm neutrals */
  --bg, --bg-2, --surface, --bone, --bone-dim, --text;
  /* swap THIS — the per-shop signature color */
  --gold: #c9842a;     /* sensual amber */
  /* --gold: #5a7d5a;  -- muted forest for wellness */
  /* --gold: #a85a3a;  -- terracotta for therapeutic */
  --gold-2: ...;       /* darker shade of accent */
}
```

Everything cascades — buttons, dropdowns, monogram ring, CTA gradients, audio pill.

### 9. Booking system setup

For **request-booking** (default):
- Create `/api/booking-request.js` Vercel serverless function: parse JSON body, send email via Resend / Postmark, optional Telegram bot ping for instant alert. Fire-and-forget; the WhatsApp deep link is the user-facing confirm path.
- Set env vars in Vercel: `RESEND_API_KEY`, `BOOKING_EMAIL_TO`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.

For **Cal.com**:
- Use the Booking-System skill — port `/api/_cal.js` + `event-types.js` + `slots.js` + `bookings.js` from `barbershop-template`.
- Set `CALCOM_API_KEY` env var.

### 10. Deploy

```bash
git add . && git commit -m "Initial spin-up for <shop>"
gh repo create <shop-slug> --public --source=. --push
npx vercel --prod
```

Add custom domain in Vercel dashboard → Settings → Domains.

## Mobile optimization (built in — don't rebuild)

The template ships with a **layered breakpoint strategy** that keeps desktop intact and progressively refines down. Don't touch existing media queries in the body of the stylesheet — append per-shop overrides at the end if needed.

### Breakpoint ladder

| Width | What changes |
|---|---|
| **≤880px** (tablet) | About / Suites / Roster / Visit / Detail-row grids stack to 1 column. Nav switches to burger menu. Footer goes 2-col. |
| **≤760px** (large phone / small tablet) | Hero meta + lede hidden. Services stack to 1-col. Notice + Rules-grid stack. Masseuse modal switches from split-panel to vertical stack. |
| **≤600px** (phone — main mobile block at end of stylesheet) | Type baseline shrinks. Buttons tighten letter-spacing. Hero CTAs become full-width column. Sub-page hero padding halved. Booking modal goes **full-screen** (100vw × 100svh, no border, no shadow). Masseuse modal goes full-screen with photo on top. Masseuses grid → 2-col. Variant-grid → 1-col (already at 600 from earlier rule). |
| **≤380px** (iPhone SE / Galaxy A class) | Nav wordmark hidden (monogram only). Booking massage cards stack to 1-col. Hero title tightens further. |

### Mobile-specific patterns to copy verbatim

1. **Modals go full-screen on phone.** A centered floating modal at 92vw with internal padding chews up usable space. Set `width: 100vw; max-height: 100svh; height: 100svh; border: 0; border-radius: 0;` at ≤600px for both `.book__panel` and `.masseuse-modal__panel`.

2. **`100svh` — never `100vh`.** iOS Safari's `100vh` includes the URL bar that disappears on scroll, jumping the layout. `100svh` (small viewport height) is the stable address-bar-aware unit. Same for hero `min-height`.

3. **Input font-size 16px to defeat iOS auto-zoom.** Any `<input>` or `<textarea>` smaller than 16px causes iOS to zoom into the field on focus. The template's mobile rules force `font-size: 16px` minimum on form inputs. There's also an `@supports (-webkit-touch-callout: none)` block that doubles down with `font-size: max(16px, 1rem)` for older Safari.

4. **CTAs go full-width column on phone.** `.hero__cta`, `.visit__cta`, `.book__confirm-cta`, `.masseuse-modal__cta` all switch to `flex-direction: column; align-items: stretch;` with `.btn { width: 100% }`. Side-by-side buttons at 360px width get cramped or wrap awkwardly.

5. **Booking modal step indicators tighten.** From `padding: 16px 0; font-size: 10px` → `padding: 12px 2px; font-size: 9px; letter-spacing: 0.14em`. Without this, "MASSAGE · DATUM · TIJD · GEGEVENS" overflows on a 360px screen.

6. **Letter-spacing on buttons gets reduced** from `0.22em` to `0.14–0.16em` on phones. With small font sizes, wide letter-spacing causes labels like "BOEK DE THAISE SUITE →" to overflow or wrap mid-word.

7. **Sfeer scroller uses viewport-relative tile width on phone:** `flex: 0 0 78vw`. Each tile fills most of the screen and the next tile peeks in as a scroll hint.

8. **Visit contact list collapses from 2-col grid to 1-col stack** on phone. The `140px 1fr` definition lists at desktop are unreadable at 360px width.

9. **Masseuse modal close button moves to `top: 10px; right: 10px`** so it doesn't overlap the photo's gold corner.

10. **Hero title minimum is `clamp(54px, 17vw, 92px)` on phone**, dropping to `clamp(40px, 16vw, 64px)` on iPhone SE class. The desktop `clamp(64px, 10vw, 144px)` would crash into the corners on a 320px screen.

### When to extend per shop

Add a final `@media (max-width: 600px)` block at the very end of the stylesheet (after the existing mobile block) for any shop-specific overrides. **Never modify the canonical mobile rules** — keep them as a reference for the next shop.

### Mobile testing checklist

Before hand-off, walk through on a real phone (or DevTools device-mode at 375px and 390px):

- Hero title doesn't overflow the screen edge
- "Boek nu" button in the nav burger works (mobile menu opens, click works)
- Booking modal opens full-screen, all 4 steps scroll cleanly without the page bouncing behind
- Masseuse modal opens full-screen, photo gallery prev/next works, thumbnail strip scrolls horizontally, "Reserveer met deze masseuse" button is full-width
- Suite dropdown opens, options are tappable (44×44pt minimum), closes on outside tap
- Masseuse photo chips scroll horizontally with one finger, "Geen voorkeur" star is the leftmost chip
- Roster cards on the homepage don't overflow on a narrow screen
- Sfeer scroller uses momentum scroll on iOS, snaps cleanly
- Form inputs don't auto-zoom on focus (this is the iOS 16px rule)
- The "Sfeer" audio pill doesn't overlap the booking CTA at the bottom of the hero

## CACHE_BUST gotcha (read this)

`vercel.json` ships with:

```json
{ "source": "/(.*)\\.(jpg|jpeg|png|webp|avif|svg|woff2|mp4|webm)",
  "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] }
```

This means **browsers and Vercel's edge will serve any image/video URL forever** without re-fetching. If you replace `images/sfeer/01.jpg`'s content but keep the path, returning visitors and the edge cache serve the *old* file — for up to a year.

**The fix is built in:** `main.js` defines `const CACHE_BUST = "v=N"`; the `cb()` helper appends `?${CACHE_BUST}` to every URL the JS hydrates. Bump `CACHE_BUST` (and the `?v=N` query strings on `style.css` / `main.js` in HTML) every time you swap asset contents. New URL = cache miss = fresh asset.

Don't remove the immutable cache — it makes repeat visits instant.

## Pitfalls

- **Verify the vertical before sending a demo.** The lead list (`leads/out/massage.csv` in this org) doesn't distinguish therapeutic vs erotic. Google `"<name> <city>"` first.
- **Don't promise Cal.com to erotic shops.** ToS suspension risk. Use request-booking.
- **Vercel AUP risk for adult content.** Document Hetzner+Caddy as Plan B in your client onboarding. Keep imagery suggestive, not explicit.
- **Hero video should never show people in the adult vertical** — legal/discretion. Hands + tables + steam OK for therapeutic.
- **Pricing is often hidden in the erotic vertical.** Design for "Bel voor tarieven" by default. Show prices only when the shop publishes them publicly.
- **The 4-suite pattern is Aurora-specific but transferable** — many small spas have signature rooms. If the shop has 6 suites, the suite dropdown handles it; the homepage `.suite-row` blocks need duplicating.
- **The masseuse roster needs the `weekdays:[]` integer array.** A pure string `days:"Mon Tue"` won't filter the homepage list. Keep both fields in sync.
- **`MASSEUSES_DATA` keys must match `data-masseuse` attributes on cards** — it's how the modal hydrates. Slug typos = silent failure.
- **`<select>` looks awful in this dark theme.** The custom `.book__select` dropdown is the answer; don't let a future change replace it with a native select unless the design system changes.

## Selling Notes

- **Lead with the masseuse profiles.** A clickable detail modal with multi-photo gallery + days-available is a strong "wow" demo on cold outreach.
- **Show the today/tomorrow roster live** — visitors immediately see who's working, no scrolling required.
- **Position WhatsApp confirmation as a feature**, not a fallback. For adult-vertical shops, manual confirmation = customer screening = higher quality bookings.
- **The ambient audio is a small but memorable touch** in the demo — most competitor sites are silent.
- **Custom domain included.** No middleman SaaS fees from you (Vercel Hobby is free for these).

## Future Improvements

- Extract `SHOP` / `SHOP_HOURS` / `SERVICES` / `SUITES` / `MASSEUSES_DATA` into a single `config.js` so per-shop edits don't touch `main.js` proper.
- Add a multi-language switcher (NL / EN / DE) — Aurora has international clientele; out of scope here but useful for a future shop.
- Per-service custom-fields in the booking modal (e.g. "couple's booking → second name field"). Payload JSON shape supports it; UI doesn't yet.
- Astro / Next.js port if multi-page becomes hard to maintain by hand. The current build is intentionally vanilla so it's easy to debug in the browser.
