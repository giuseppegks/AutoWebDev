---
name: Barbershop-Template
description: Use when spinning up a new barbershop / salon / massage / beauty website from the proven 080-style template. The template is a single-page, dark-themed, video-hero, gold-accent presentational site with an integrated Cal.com booking modal. Triggers on phrases like "build a barbershop site for [shop]", "spin up a new shop from template", "clone the 080 template for [client]", "new salon site like 080".
---

# Barbershop Template — Spin-Up Workflow

## Overview

Reusable, deployable template for local appointment-based businesses (barber, salon, beauty, massage, fysio). One repo, one config-style edit, one Vercel deploy → live site with working booking system in **under 30 minutes per shop** once content is gathered.

**Reference template:** [github.com/giuseppegks/barbershop-080](https://github.com/giuseppegks/barbershop-080) — the 080 build is the canonical source.

## When to Use

- Local appointment-based business needs a presentational site + online booking
- Single location (or single calendar — multi-barber needs Cal.com Teams plan, see Booking-System skill)
- No e-commerce, no auth, no CMS
- Client willing to use Cal.com (free for single user; ~$15/user/mo for Teams)

**Skip when:** the business needs a custom design system, multi-page editorial content, or a non-Cal.com booking backend.

## What's in the Template

```
barbershop-080/
├── index.html              # single-page site
├── css/style.css           # dark + gold design system
├── js/main.js              # nav, hero video rotator, gallery, booking modal
├── images/                 # photos (swap per shop)
├── videos/                 # hero video clips
├── api/                    # Vercel serverless proxy for Cal.com
│   ├── _cal.js             # shared helper (Bearer auth, v2 versioning)
│   ├── event-types.js      # GET /api/event-types
│   ├── slots.js            # GET /api/slots
│   └── bookings.js         # POST /api/bookings
├── package.json
├── vercel.json
├── .env.example
└── .gitignore
```

### Built-in sections

1. **Hero** — fullscreen video rotator, brand monogram, BOEK NU CTA
2. **About** — eyebrow + display heading + 3-paragraph body
3. **Haircuts gallery** — editorial mosaic (`haircuts__grid`), 8 images
4. **Image break** — full-bleed photo separator
5. **Barbers** — 3-column team cards (photo, role, name, bio)
6. **Services** — 3 service cards with icon, title, body, price
7. **Reviews** — Google reviews section: sticky aggregate card (5.0 ★ + Google mark + CTA) on the left, 6-card testimonial grid on the right. Sits between the second image-break and the gallery.
8. **Sfeerbeelden** — horizontal scroll gallery of shop ambience
9. **Visit** — address + contact (left), opening hours + CTAs (right), map card
9. **CTA strip** — big call-to-action band
10. **Footer** — multi-column with brand, nav, info, socials, Google reviews
11. **Booking modal** — 4-step Cal.com-driven flow: service → date → time → details → confirmation

## Spin-Up Workflow (per shop)

### 1. Gather content (the slow part — ~1–2 hours)

Pull from the client's existing presence:
- Logo (or generate a monogram from the shop name initial)
- Hero video clips (Pexels / their IG / their old site)
- Haircut photos (their Instagram / WhatsApp portfolio)
- Barber portraits + names + 1-line bios
- Address, phone, email, opening hours, social links
- Service list with prices

Save all assets locally — verify against ground truth (their actual site / IG) before writing any copy. **Never invent prices, hours, names, or addresses.**

### 2. Clone the template

```bash
git clone https://github.com/giuseppegks/barbershop-080 <shop-slug>
cd <shop-slug>
rm -rf .git
git init
```

### 3. Replace assets

- `images/` — swap logo, hero stills, haircuts (`images/haircuts/`), barber portraits, ambience shots
- `videos/` — replace hero clips (5 short loops, ~5s each, 1080p, MP4 H.264, < 4 MB each)

### 4. Edit `index.html`

Find-and-replace these in order:

| Field | Where |
|---|---|
| Page title + meta description | `<head>` |
| Brand monogram + wordmark | `.nav__brand` and `.footer__brand-row` |
| Hero title rows (`BARBERSHOP` / `0 8 0`) | `.hero__title-main`, `.hero__title-sub` |
| About copy | `#about .container` |
| Barber cards (3) | `.barbers__grid` |
| Service cards (3) — title, sub, body, price | `.services` |
| Visit address + contact + opening hours table | `#visit` |
| Map iframe `src` (URL-encoded address) | `.visit__map-frame` |
| Reviews — aggregate score, count, shop name in `.reviews__aggregate-shop`, 6 review cards (`.review`) with star count, body, name, time-ago | `#reviews` |
| Footer brand, address, phone, socials, review links | `.footer` |
| All `wa.link/...` WhatsApp links | search-replace |

### 5. Update services in the booking modal

Booking widget services live in `index.html` inside `#book-modal`:

```html
<button class="book__service" data-service="cut" data-label="..." data-duration="30" data-price="30">
```

Each service must map to a Cal.com event-type slug. In `js/main.js` near the top:

```js
const SERVICE_SLUG = {
  'cut': 'haar',
  'cut-beard': 'haar-baard',
  'beard': 'baard'
};
```

The `slug` value must match the Cal.com event-type URL slug (e.g. `cal.com/<user>/haar` → slug is `haar`).

### 6. Update barber list in booking modal

In `index.html`, `.book__barbers`:

```html
<button class="book__barber" data-barber="mo">Mo</button>
```

> Per-barber availability requires a Cal.com Teams plan with one user per barber. Single-account shops: barber selection is recorded as preference metadata on the booking but doesn't filter slots.

### 7. Update shop hours in `js/main.js`

Match Cal.com availability:

```js
const SHOP_HOURS = {
  2: [9, 17], 3: [9, 17], 4: [9, 17], 5: [9, 17], 6: [9, 17]
  // Mon (1) + Sun (0) closed
};
```

Disabled days won't show in the date picker; closed hours won't show in the time grid.

### 8. Booking system setup

Use the **Booking-System** skill — it covers Cal.com event-type creation, availability, API key, Vercel env vars.

### 9. Deploy

```bash
git add . && git commit -m "Initial spin-up for <shop>"
# create new repo on GitHub via UI, then:
git remote add origin <new-repo-url>
git push -u origin main

npx vercel             # link to Vercel
npx vercel env add CALCOM_API_KEY production
npx vercel --prod
```

### 10. Custom domain (optional)

Vercel dashboard → project → Settings → Domains → add the shop's domain. Vercel gives the DNS records to point at — share with the client (or their domain registrar).

## Variations by Vertical

The template covers most appointment-based local businesses with light edits:

| Vertical | Adjustments |
|---|---|
| **Hair salon (women's)** | Rename services (knipbeurt, kleuring, behandeling), longer durations, swap hero |
| **Massage / spa** | Drop "barbers" → "therapeuten", swap palette away from gold (consider muted greens or warm neutrals), longer slots |
| **Nail salon** | Replace haircut gallery → nail art mosaic, services list (manicure, pedicure, gel) |
| **Beauty salon** | Multi-service offering — may need a sub-category step (skincare / lashes / brows) |
| **Fysio / chiro** | Drop haircut gallery entirely, add a "behandelingen" content section, professional tone |

**Tone & language:** keep all copy in the business's region language (NL for Nijmegen). Translate eyebrow labels, button copy, and section headings.

## Pitfalls to Avoid

- **Don't fabricate content.** If a fact (price, hour, owner name) isn't in their public footprint, ask the client or omit. The single biggest credibility-killer in cold outreach is wrong information on the demo.
- **Reviews must be real.** The `#reviews` section ships with placeholder testimonials so the layout is intact during pitch — but before client handoff, replace every card with the shop's actual Google reviews (copy reviewer name, stars, time-ago, body verbatim). Update `.reviews__aggregate-shop`, `.reviews__score`, and the `lees op google` href to the shop's real Google place URL. Fake testimonials on a real client site is the same credibility-killer as fake prices.
- **Don't share API keys in chat or commits.** Cal.com keys go in Vercel env vars only. Never `.env` committed; never pasted in Slack/email/chat.
- **Don't promise per-barber booking on Cal.com free tier** — it requires Teams plan. Be upfront: single calendar = one booking pipeline.
- **Don't hand off without testing the full booking flow end-to-end** on the production URL — service → date → time → details → confirmation → ICS download → Cal.com email arrives.
- **Don't skip the openingstijden table sync.** If `SHOP_HOURS` in `main.js` says 9-17 but the displayed table says 9-18, clients will book slots that disappear. Keep them in lockstep.

## Selling Notes (when pitching to shops)

- **Lead with the booking system.** A working "client books in 30 seconds" demo is the closer.
- **Position the cost honestly:** website is a one-time fee from you; Cal.com is the shop's own subscription (free for single, $15/barber/mo for Teams). You don't middleman the SaaS.
- **Show ICS calendar invite working** — clients picturing the booking land in their existing Google/Apple calendar is a strong moment.
- **Custom domain included** — point their existing domain at Vercel; no monthly hosting fee from you (Vercel Hobby is free for these).

## Future Improvements (when scaling past 10 shops)

- Extract all shop-specific data (name, address, services, etc.) into a single `config.js`
- Build script that renders `index.html` from a Handlebars / EJS template + `config.js`
- Per-shop = edit `config.js` only, no HTML touching
- At that point, consider Astro / Next.js if multi-page becomes common