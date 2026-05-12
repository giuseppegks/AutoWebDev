---
name: Cafe-Bar-Template
description: Use when spinning up a website for a café, brown bar (bruin café), brunch spot, lunchroom, broodjeszaak, music café, or small specialty-coffee bar. Multi-page (home + menu + over + contact) editorial template — Cormorant Garamond + Inter on cream/paper, single accent per shop (coffee-green / aubergine / brown-walnut / espresso / stage-navy / olive), with awesome-design-md DESIGN.md and power-design principles (≥40% whitespace, 60-30-10 color, max 4 type sizes, borders-first cards). Photo bank with 60 themed Pexels CDN URLs (brown_cafe_bar / beer_glass_bar / sandwich_shop / live_music_venue / cozy_lounge / dutch_cafe) for sites without their own photos. Distinct from `barbershop-template` (single-page video Cal.com), `coffeeshop-template` (cannabis legal-compliant 3-page variant), and `nailstudio-template` (nail-art masonry). Triggers on phrases like "build a café site for [shop]", "brunch website", "broodjeszaak site", "bruin café site", "lunchroom website", "specialty coffee site", "café Trianon", "Billy's-style café".
---

# Café / Bar Template — Spin-Up Workflow

## When to Use

Pick this template when the shop is:
- **Café / koffiebar / specialty coffee** (Billy's Coffee, Park Café)
- **Bruin café** (Café De Beurs — historic Dutch brown pub)
- **Café-met-podium** (Café Trianon — café + small live music venue)
- **Broodjeszaak / lunchroom** (Broodje Dennis)
- **Brunch spot** with a structured menu
- One location, no e-commerce, no CMS

**Skip this template if:**
- The shop is a **cannabis coffeeshop** (NL gedoogbeleid) → use `coffeeshop-template`
- The shop is a **barbershop with online Cal.com booking** → use `barbershop-template`
- The shop is a **nail studio** with masonry portfolio → use `nailstudio-template`

## Reference builds

`websites/cafes-bars/` contains 5 working examples:

| Slug | Type | Distinctive features |
|---|---|---|
| `billy-coffee` | Specialty coffee | Coffee-green + caramel-gold, original blueprint |
| `park-cafe` | Brunch + coffee | Aubergine + peach-coral, sibling design language |
| `cafe-de-beurs` | Bruin café 1905 | Walnut-brown + brass, tijdlijn 1905 → 1979 → vandaag |
| `cafe-trianon` | Café + poppodium | Stage-navy + amber spotlight, **agenda-sectie** for concerts |
| `broodje-dennis` | Broodjeszaak | Espresso + tomato-orange punchy, catering-CTA |

Read `websites/cafes-bars/billy-coffee/DESIGN.md` first to understand the awesome-design-md 9-section format + power-design principles.

## Architecture (4 pages — standard)

```
<slug>/
├── index.html         # Hero + intro split + 3-USP features + photo strip + de plek + footer CTA
├── menu.html          # Categorized menu (food + drink) with price-row layout
├── over.html          # Story + tijdlijn + values
├── contact.html       # Address + hours + Maps embed + reservation form
├── css/style.css      # 944-line custom CSS — variable tokens, no Tailwind
├── js/main.js         # Open/closed status badge, mobile nav toggle, reveal animations
├── images/            # Real shop photos or thematic Pexels stock
├── DESIGN.md          # Awesome-design-md 9-section design system
├── vercel.json        # cleanUrls + security headers
└── package.json       # Minimal — no build step needed
```

**Variant: café-met-podium (Trianon style)** — keep the same 4 pages but add a prominent agenda-section on the homepage (4 event-cards with datum-block + text + zaal). Include lunch-hours vs concert-hours distinction in the open-badge logic.

**Variant: broodjeszaak (Dennis style)** — `menu.html` becomes a sandwich-category grid (Klassiekers, Vegetarisch, Specials, Drank). `contact.html` reservation form becomes a "Catering aanvragen" form.

## Design System Principles

The template enforces **power-design** rules in CSS and HTML:

### Typography (Cormorant Garamond + Inter)
| Use | Font | Size mobile | Size desktop |
|---|---|---|---|
| Display H1 | Cormorant Garamond 500 | 40px | 72px (`clamp(2.5rem, 6vw, 4.5rem)`) |
| H2 | Cormorant Garamond 500 | 32px | 52px |
| H3 | Cormorant Garamond 500 | 22px | 30px |
| H4 | Inter 600 | 18px | 18px |
| Eyebrow | Inter 500 uppercase 0.18em | 12px | 12px |
| Lead body | Inter 400 | 18px | 21px |
| Body | Inter 400 | 17px | 17px |
| Caption | Inter 400 | 14px | 14px |

**Italic rule:** one italic word per heading via `<em>`, in `--gold`. ("Een goeie bak koffie. *Aan de Daalseweg.*")

**Line length:** `p` + `.lead` capped at 60ch.

### Color tokens (the only block you customize per shop)

```css
:root {
  /* Dark shades — body text + dark sections */
  --coffee-darkest: #...;
  --coffee-dark: #...;
  --coffee: #...;
  --coffee-warm: #...;
  --coffee-light: #...;

  /* Accent — CTAs, kicker, italic flourish */
  --caramel: #...;
  --caramel-light: #...;
  --gold: #...;

  /* Cream / neutral surfaces */
  --cream: #...;
  --cream-warm: #...;
  --cream-deep: #...;
  --paper: #...;

  /* UI */
  --border: #...;
  --border-strong: #...;
}
```

**Verified palette examples (use as reference, NOT defaults — pick per shop):**

| Shop | Style | Dark | Accent | Cream |
|---|---|---|---|---|
| Billy's | Specialty coffee | `#1C413C` evergreen | `#C28832` caramel | `#FAF6F0` paper |
| Park Café | Brunch | `#482638` aubergine | `#E89357` peach-coral | `#FBF6ED` warm cream |
| De Beurs | Bruin café | `#2E1C0E` dark walnut | `#A87434` brass | `#F4ECDA` parchment |
| Trianon | Café + podium | `#15294F` stage navy | `#D89A3E` amber spotlight | `#FBF6EC` cream |
| Broodje Dennis | Broodjeszaak | `#3B2613` espresso korst | `#E0651F` tomato-orange punch | `#FBF5E8` warm wit |

**60-30-10:** 60% cream surfaces, 30% dark text/dark-mode sections, 10% accent (kicker + CTA + italic).

**One accent per section.** Never mix `--caramel` + `--gold` as both accents on the same strip — pick one role.

### Section rhythm — power-design ≥40% whitespace
```css
--section-y: clamp(4rem, 8vw, 7rem);  /* 64–112 px */
```
Was originally `clamp(2.25rem, 4.5vw, 4rem)` = 36–64 px which felt cramped. The new value gives editorial breath.

### Depth & elevation — borders first
- Cards: 1px `--border`, hover lifts to `--border-strong` + 2px translateY. **No shadow by default.**
- Hero image: `--shadow-lg` is acceptable for visual lift.
- Modal/dropdown: `--shadow-xl` only.

## Spin-Up Workflow

### 1. Verify shop facts
- Name (exact, with apostrophes)
- Address + postcode
- Phone (E.164 + display)
- Email (or fallback `info@<domain>`)
- Opening hours per day
- KvK (if scrapable from KvK.nl)
- Menu categories + prices
- Story (history, owner, USP)
- Photos from source (Facebook / Instagram / Joomla / WordPress)

**Scrape sources (in order of reliability):**
1. `curl -L -A "Mozilla/5.0 ..." <url>` — most reliable for Joomla/WP
2. WebFetch — works for many static sites
3. Bing image search / Google reviews — for photos
4. **Facebook/Instagram return 403** for both curl and WebFetch — don't waste time, mark as PLACEHOLDER

### 2. Duplicate the blueprint

```bash
cp -r websites/cafes-bars/billy-coffee websites/cafes-bars/<slug>
cd websites/cafes-bars/<slug>
```

### 3. Customize (in this order)

1. **Palette swap in `css/style.css`** — only the `:root { ... }` token block. Pick from verified palettes above or design fresh, but stay within 5 dark shades + 2-3 accents + 4 cream surfaces.
2. **All 4 HTML files** — search/replace:
   - `Billy's Coffee` → new shop name
   - `Daalseweg 31` → new address
   - `6521 GG` → new postcode
   - Phone in `tel:+31...` links + display format
   - Photo URLs (see step 5)
   - Logo: `images/BillysCoffee_Logo_RGB.png` → text wordmark or new PNG
3. **Hero copy** — three-line poetic statement with one italic word per heading.
4. **`menu.html`** — category structure + price-row layout. PLACEHOLDER prices if not verified.
5. **`over.html`** — story + tijdlijn. For De Beurs-style historic pubs, the tijdlijn IS the page.
6. **`contact.html`** — Maps embed URL with new address, opening-hours table, reservation form (or catering form for broodjeszaak).
7. **`DESIGN.md`** — rewrite in awesome-design-md 9-section format with this shop's palette. Reference Billy's DESIGN.md as structural template.

### 4. Photos — use the photo bank for missing slots

If the shop hasn't supplied photos yet, use `pexels-cafe-bank.json` (in this skill folder). 60 themed URLs across 6 themes:

| Theme | Use case |
|---|---|
| `brown_cafe_bar` | Bruin-café interior, dark wood + brass |
| `beer_glass_bar` | Beer pours, bar counter |
| `sandwich_shop` | Sandwiches on plates, deli counter |
| `live_music_venue` | Small stages, intimate club |
| `cozy_lounge` | Warm interiors, dim lighting |
| `dutch_cafe` | Cafés in Dutch cities |

Append `?auto=compress&cs=tinysrgb&w=1200` for sized variants. License is Pexels (free commercial, no attribution required).

**Don't replace owner/practitioner identity moments with stock.** If the shop has a real owner-photo, use it on `over.html` even if the rest of the site is stock.

### 5. Power-design audit before deploy

Run through this checklist:
- [ ] Body text 17px+, line-height 1.6+
- [ ] Headings: max 4 type sizes per section
- [ ] `p` + `.lead` capped at 60ch
- [ ] Section padding 64–112 px (`clamp(4rem, 8vw, 7rem)`)
- [ ] 60-30-10 color distribution: cream dominant, dark text, single accent
- [ ] One accent per section (not caramel + gold mixed)
- [ ] Cards use 1px border, no default shadow
- [ ] WCAG 4.5:1 on body text
- [ ] No latte-art / coffee-bean clichés (unless that IS the brand)
- [ ] No bullet-heavy paragraphs — 2-3 sentence prose

### 6. Deploy

```bash
cd websites/cafes-bars/<slug>
rm -rf .vercel    # CRITICAL: blueprint's .vercel link will hijack the deploy otherwise
vercel --prod --yes
```

Verify `<slug>.vercel.app` returns 200 on all 4 pages.

## ⚠️ Common gotchas

1. **`.vercel` blueprint collision** — the blueprint folder has a pre-linked `.vercel/` directory. If you don't `rm -rf .vercel` before deploying the new site, your first `vercel --prod` will **overwrite the blueprint's deployment** (you'll push your new content to `billy-coffee.vercel.app` by accident). Always remove `.vercel` first.

2. **Facebook/Instagram source-scrape:** return 403 for both curl and WebFetch. Don't waste agent cycles trying. Mark photos and copy as PLACEHOLDER if FB/IG is the only source.

3. **Joomla DNS-restricted from CDN egress** — sites like `trianonnijmegen.nl` may give `ECONNREFUSED` from Vercel/Cloudflare egress. Use WebSearch for descriptions and Pexels for photos.

4. **One italic word per heading** — if you put two `<em>` per h1/h2 it looks like a markup error. Pick the most evocative word and only italicize that.

5. **Logo:** prefer text wordmark over PNG. Saves bandwidth, scales perfectly, no licensing concerns for prospect mockups. Use Cormorant Garamond italic for the wordmark.

## Files in this skill

```
skills/cafe-bar-template/
├── SKILL.md                # this file
└── pexels-cafe-bank.json   # 60 Pexels CDN URLs in 6 themes
```

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

