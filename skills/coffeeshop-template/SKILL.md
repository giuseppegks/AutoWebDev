---
name: Coffeeshop-Template
description: Use when spinning up a website for a Dutch cannabis coffeeshop (NL gedoogbeleid). Strict info-only 3-page variant of `cafe-bar-template` — no menu, no strain names, no prices, no cannabis imagery, no promotional copy. Includes 18+ age-gate modal on every page with localStorage flag. Ingetogen / muted palette (deep olive + amber, or warm terracotta — never psychedelic/green-cliché). Distinct from `cafe-bar-template` (regular cafés with menu) and `barbershop-template` (Cal.com booking). Triggers on phrases like "build a coffeeshop site for [shop]", "Dutch coffeeshop website", "cannabis coffeeshop site", "coffeeshop Ketama / Dakota / Lucky Luke", "coffeeshop info-only site", "age-gate website for cannabis".
---

# Dutch Coffeeshop Template — Spin-Up Workflow

## ⚠️ Legal/content constraints (NL gedoogbeleid)

A Dutch coffeeshop website **MUST NOT** contain:
- **Product menu** publicly visible (strains, prices, weights)
- **Cannabis imagery** (leaves, smoke, joints, cones, pipes)
- **Promotional drug copy** ("kom high worden", "premium kwaliteit", "topstrains")
- **Online ordering** flow
- **Reservation/booking** for product purchase

A Dutch coffeeshop website **MAY** contain:
- Address, opening hours, age requirement (18+, ID required)
- Interior sfeer-foto's **without product visible**
- House rules (AHOJG — geen Affichering, geen Harddrugs, geen Overlast, geen Jeugd, geen handel boven Gedoogvolume)
- Google Maps link + neutral reviews link
- Basic history / about the shop
- Contact form (general inquiry only, no order flow)

This template enforces all of these by:
1. **Removing `menu.html` and `over.html`** from the cafe-bar-template (over is condensed into index hero)
2. **Adding 18+ age-gate modal** that blocks content on first page load
3. **Using cannabis-free icon set** (no leaves, joints) — substitute house/clock/shield/star/dartboard
4. **Replacing reservation form** with general contact form
5. **Using muted palettes** (deep olive or warm terracotta) — never psychedelic

## When to Use

Pick this template when the shop is:
- **Dutch cannabis coffeeshop** (gedoogd onder gedoogbeleid)
- Wants a **professional, info-only web presence** — not a marketing/promo site
- No existing online ordering (because that would be illegal anyway)

**Skip this template if:**
- The "coffeeshop" is actually a specialty-coffee bar (use `cafe-bar-template`)
- The shop operates outside NL (different legal regime — research locally)
- The shop wants a member/loyalty-app integration (different scope)

## Reference builds

`websites/coffeeshops/` contains 2 working examples:

| Slug | Address | Distinctive features |
|---|---|---|
| `coffeeshop-ketama` | de Ruyterstraat 19, Nijmegen | Deep-olive palette, 10-rule huisregels grid, transit-info on contact |
| `coffeeshop-dakota` | Lange Hezelstraat 113A, Nijmegen | Warm-terracotta palette, "voorzaal + achterzaal" feature (TV, dartborden, board games) |

## Architecture (3 pages — reduced from cafe-bar-template's 4)

```
<slug>/
├── index.html         # Hero + over (condensed) + huisregels-teaser + contact-info
├── huisregels.html    # 10 genummerde huisregels (AHOJG-aligned)
├── contact.html       # Address + hours + Maps + transit info (no reservation form)
├── css/style.css      # Custom CSS with muted palette
├── js/main.js         # Open/closed status, mobile nav
├── js/age-gate.js     # 18+ modal — blocks content on first load, localStorage flag
├── images/            # Sfeer-foto's interior — NO product imagery
├── DESIGN.md          # Awesome-design-md format documenting the content-constraints
├── vercel.json
└── package.json
```

**Removed from cafe-bar-template:** `menu.html`, `over.html` (`over` content moves to index hero section).

## 18+ Age Gate Modal

Required on every page. Implementation pattern (`js/age-gate.js`):

```js
// On every pageload:
// 1. Check localStorage['<slug>-age-verified'] === 'yes'
// 2. If yes → don't show modal, allow content
// 3. If no → show modal overlay (z-100), block scroll via body class
// 4. "Ja, 18+" → set localStorage flag, fade out modal
// 5. "Nee" → redirect to google.com (or friendly exit screen)
```

Visual: cream-tinted full-screen overlay, big "18+" badge, centered card with the question, two buttons. Use the site's palette (dark text on cream surface).

**Returning visitors skip the gate** thanks to the localStorage flag — Stripe-style remember-me.

## Design System

### Palette — muted, professional, not psychedelic

**Verified examples:**

| Shop | Style | Dark | Accent | Cream |
|---|---|---|---|---|
| Ketama | Ingetogen olive | `#1F2A1F` deep olive | `#B68B3E` verfijnd amber | `#F4F2EC` cool cream |
| Dakota | Warm terracotta | `#2A1812` deep terracotta-brown | `#B07045` saffron-terracotta | `#F6EFE3` warm cream |

**Don't use:**
- Bright greens (cannabis-cliché)
- Tie-dye / rainbow gradients
- Black-and-purple "stoner" themes
- Neon any color

**Do use:**
- Muted earth tones (deep olive, terracotta-brown, walnut, slate)
- Warm cream surfaces (off-white, parchment, soft cream)
- One accent per section, single italic word per heading

### Typography
Same as `cafe-bar-template` — Cormorant Garamond display + Inter body, 17px+ body, `<em>` italic accent, 60ch line length max.

### Iconography — cannabis-free

Allowed icons:
- 🏠 house / building (location)
- 🕐 clock (hours)
- 🛡️ shield (rules/safety)
- 🆔 ID card (age verification)
- ⭐ star (reviews)
- 🎯 dartboard / 📺 TV / 🎲 board games (vibe features — Dakota-style)
- 📍 pin (Maps)
- 📞 phone

NOT allowed:
- Cannabis leaves, joints, pipes, bongs
- Smoke clouds
- "420" stylization
- Rastafari iconography

## Spin-Up Workflow

### 1. Verify shop facts

- Full name + tolerated since-year (if known)
- Address + postcode
- Phone
- Opening hours per day
- Nearby landmarks (e.g. "vlakbij Kronenburgerpark")
- Public reviews (Google Maps, dutch-coffeeshops.com, greenmeister.nl)
- Vibe descriptors (e.g. "voorzaal + achterzaal", "TV en dartborden", "kleine gezellige bar")

**Sources that work:**
- `dutch-coffeeshops.com` — usually 200 OK, sometimes only logo photos
- `greenmeister.nl` — listings with descriptions
- `wanderlog.com` — reviews
- `inyourpocket.com` — quality short descriptions
- Google Maps — verify address, get reviews
- `coffeeshopmenus.org` — **DO NOT scrape product info from here for the public site**

### 2. Duplicate the cafe-bar blueprint, then reduce

```bash
cp -r websites/cafes-bars/billy-coffee websites/coffeeshops/<slug>
cd websites/coffeeshops/<slug>
rm menu.html over.html
cp contact.html huisregels.html      # template for the new huisregels page
```

### 3. Customize (in this order)

1. **Palette swap** in `css/style.css` `:root { ... }` block. Use muted earth tones (see verified palettes).
2. **Search/replace** across the 3 HTML pages:
   - Shop name, address, postcode, phone, email
   - Photo URLs → cozy_lounge / brown_cafe_bar Pexels from `cafe-bar-template/pexels-cafe-bank.json` (theme: cozy_lounge for Ketama-style, brown_cafe_bar for Dakota-style)
   - Logo: text wordmark, NOT PNG (avoid licensing/branding concerns)
3. **Build `js/age-gate.js`** following the pattern (overlay, localStorage flag, focus management, ESC handler).
4. **Inject age-gate script** in `<head>` of all 3 pages: `<script src="js/age-gate.js" defer></script>`
5. **`index.html`** — restructure to:
   - Hero: shop name + "Aan de [straat], [buurt]"
   - Section 2: "De plek" — interior beschrijving + Maps preview
   - Section 3: "Huisregels" teaser with link to `huisregels.html`
   - Section 4: contact info + opening hours
6. **`huisregels.html`** — 10-rule numbered grid:
   1. 18+ toegang met geldig ID (paspoort / ID-kaart / rijbewijs)
   2. Geen handel buiten de zaak
   3. Maximaal 5 gram per persoon per dag
   4. Geen alcohol op locatie
   5. Geen minderjarigen op locatie
   6. Geen overlast voor de buurt
   7. Geen harddrugs
   8. Geen rookwaar mee naar buiten (in veel gemeenten)
   9. Huisdieren [toegestaan/niet] (per shop)
   10. De medewerker beslist altijd over toegang
7. **`contact.html`** — adres + Maps + transit cards (fiets / OV / auto). Replace reservation form with simple "vraag stellen via mail/telefoon" — no form fields about products.
8. **`DESIGN.md`** — document the muted palette + explicit content constraints (no product imagery, no menu, age-gate modal, AHOJG-aligned huisregels).

### 4. Photos — strict no-product policy

Use `cafe-bar-template/pexels-cafe-bank.json` `cozy_lounge` theme. **Pre-vet every photo:**
- ✅ Bar interior, tables, lamps, plants, wood, books
- ✅ Exterior with house number visible
- ✅ Neighborhood context shots
- ❌ Anything with smoke, paper, leaves, scales, baggies, joints
- ❌ "Mood" shots with neon or psychedelic light

If you can't find clean stock for a slot, use a `[PLACEHOLDER: sfeerfoto interieur — vragen aan klant]` div instead.

### 5. Deploy

```bash
cd websites/coffeeshops/<slug>
rm -rf .vercel    # blueprint collision protection
vercel --prod --yes
```

Verify all 3 pages return 200 AND that the 18+ gate appears on first load (test in incognito).

## ⚠️ Specific gotchas

1. **AHOJG criteria** — the Dutch legal framework is acronymed AHOJG: geen **A**ffichering (no advertising of products), geen **H**arddrugs, geen **O**verlast, geen verkoop aan **J**eugd, geen verkoop boven **G**edoogvolume (500g voorraad / 5g per transactie). Your site copy should reflect this — never imply you sell harddrugs, never market with "kom proeven" promo angles.

2. **Reviews are a legal grey zone** — embedding Google Reviews that mention product names/effects could be considered indirect advertising. Better to LINK to the Google Maps listing rather than embed reviews on-site.

3. **Don't list the shop's age in years** ("Sinds 1985") if you're not 100% sure — coffeeshops change ownership and licenses. Use neutral phrasing ("Al jaren een vertrouwd adres") if uncertain.

4. **Email forms** — keep simple. No "vraag over een product" subject lines. General inquiry only.

5. **Mobile age-gate** — make sure the gate is touch-friendly. Big buttons, `font-size: 16px+` to avoid iOS zoom on focus.

## Files in this skill

```
skills/coffeeshop-template/
└── SKILL.md   # this file
```

Photo bank lives in `skills/cafe-bar-template/pexels-cafe-bank.json` — use the `cozy_lounge` + `brown_cafe_bar` themes only.

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

