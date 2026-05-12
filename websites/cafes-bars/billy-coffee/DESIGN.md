# DESIGN.md — Billy's Coffee

> Stitch-format design system (awesome-design-md). Read this before generating UI.
> Page-specific overrides live in `design-system/billy's-coffee/pages/<page>.md` and take precedence over this file.

---

## 1. Visual Theme & Atmosphere

**Mood:** Modern editorial with warm artisan touch. Specialty-coffee bar in Nijmegen-Oost that feels rooted (matte deep-green walls, paper menus, warm wood) but not vintage-kitsch. The visitor lands and immediately reads: *this is a place where people who care about coffee gather, and you're welcome too.*

**References:** Tartine Bakery (SF), Manhattan Coffee Roasters (Rotterdam), Kaffemik (Copenhagen). Editorial, generous, restrained.

**Avoid:** Heavy chalk-board lettering. "Wake up and smell the coffee" copywriting. Overlapping coffee-bean SVG decorations. Stock photos of latte art that don't match the actual bar. Cream + brown gradients that scream "WordPress coffee template".

---

## 2. Color Palette & Roles

**Source brand:** Billy's logo combines deep evergreen + caramel-gold on cream paper.

| Token (CSS var) | Hex | Role | Contrast on cream |
|---|---|---|---|
| `--coffee-darkest` | `#0F2624` | Section bg (rare — "deep" mode strip) | n/a |
| `--coffee-dark` | `#1C413C` | Primary text, dark sections, primary buttons | 12.4 : 1 ✓ |
| `--coffee` | `#2A5A53` | Hover state on dark buttons | 8.1 : 1 ✓ |
| `--coffee-warm` | `#3F726C` | Eyebrow + muted text, link hover | 5.2 : 1 ✓ |
| `--coffee-light` | `#5A8C85` | Borders on dark surfaces | 3.4 : 1 (display only) |
| `--caramel` | `#C28832` | **Accent** — CTAs on cream, highlight tags | 3.8 : 1 (display only) |
| `--caramel-light` | `#DBA857` | Hover on accent | n/a |
| `--gold` | `#B07820` | Italic display flourishes | 4.6 : 1 ✓ |
| `--cream` | `#FAF6F0` | Default page bg | base |
| `--cream-warm` | `#F5EDE0` | Alternating section bg ("section-cream") | base |
| `--cream-deep` | `#EBE0CD` | Card bg / hover on light surfaces | base |
| `--paper` | `#FFFCF7` | Highest-contrast surface (menu cards) | base |

**60-30-10 distribution:**
- 60 % `--cream` + `--cream-warm` (page + section alternation)
- 30 % `--coffee-dark` text, dark inversion sections
- 10 % `--caramel` / `--gold` accent (CTAs, eyebrow, italic flourishes)

**One accent per section.** Never mix `--caramel` and `--coffee` as both accents on the same section — pick one role.

---

## 3. Typography Rules

| Use | Font | Weight | Size mobile | Size desktop |
|---|---|---|---|---|
| Display H1 (hero) | Cormorant Garamond | 500 | 40px | 72px (clamp 2.5–4.5rem) |
| Display XL (hero variant `.h-display`) | Cormorant Garamond | 500 | 44px | 88px (clamp 2.75–5.5rem) |
| H2 | Cormorant Garamond | 500 | 32px | 52px (clamp 2–3.25rem) |
| H3 | Cormorant Garamond | 500 | 22px | 30px (clamp 1.4–1.85rem) |
| H4 | Inter | 600 | 18px | 18px |
| Eyebrow / kicker | Inter | 500 uppercase, letter-spacing 0.18em | 12px | 12px |
| Lead body | Inter | 400 | 18px | 21px (clamp 1.1–1.3rem) |
| Body | Inter | 400 | 17px | 17px |
| Caption | Inter | 400 | 14px | 14px |

**Italic rule:** One italic word per heading via `<em>`, in `--gold` — acts as a visual rest-pause. ("Een goeie bak koffie. *Aan de Daalseweg.*")

**Line length:** body + lead capped at 60ch. Headings can go wider on hero.

**Max 4 sizes per section:** eyebrow + h2 + lead + body. Anything more is a smell.

---

## 4. Component Stylings

### Buttons (`.btn`)
- Pill radius (`--r-pill: 999px`), min-height 48px.
- `.btn--primary` — solid `--coffee-dark` on cream / solid `--cream` on coffee. Hover lifts to `--coffee` (lighter green), not a darker shade. White-shimmer overlay on hover via `::before` is acceptable but only when surrounded by enough whitespace.
- `.btn--ghost` — transparent + 1px `--coffee-dark` border. Hover fills with `--coffee-dark` and inverts text.
- Arrow icon (`.btn-arrow`) sits to the right of label, 14–16px, stroke-width 1.8–2.

### Cards
- Surface: `--paper` or `--cream-warm`.
- Border: 1px `--border` (`#E0D8C5`).
- Radius: `--r-lg` (20px) for media cards; `--r-md` (12px) for compact cards.
- Hover: `border-color: --border-strong` + 2px lift via translateY. No bigger shadow.
- **No drop-shadows on cards by default.** Use border instead. Only modal/dropdown gets `--shadow-lg`.

### Eyebrow (`.eyebrow`)
- 12px Inter 500 uppercase 0.18em letter-spacing, color `--coffee-warm`.
- Sits 8–12px above the section heading. Always paired with a heading — never standalone.

### Hero
- Two-column grid 7/5 on desktop, stacked on mobile.
- Text col uses `.h-display` headline. Image col uses 4:5 portrait `--r-lg` radius with `--shadow-lg`.
- Floating "Nu geopend" badge in bottom-left of image with pulsing dot.

### Sections
- Vertical rhythm — `--section-y: clamp(4rem, 8vw, 7rem)` (64–112 px). **This is the power-design refresh value** — was 36–64 px which was too tight.
- Background alternation: `--cream` → `--cream-warm` → `--cream` → `--coffee-dark` (rare deep break).

---

## 5. Layout Principles

- **Max width:** 1200px content, 880px narrow (`.container--narrow` for prose).
- **Gutters:** `clamp(1.25rem, 4vw, 2.5rem)` — 20–40 px each side.
- **8-point grid:** all spacing tokens are multiples of 4 (`--space-xs`/sm/md/lg/xl/2xl/3xl = 4 / 8 / 16 / 24 / 32 / 48 / 64). Custom inline spacing should snap to these multiples.
- **Proximity rules:**
  - Related elements ≤ 16 px apart (h2 ↔ paragraph: ~16 px)
  - Unrelated chunks ≥ 48 px apart (eyebrow group ↔ next section)
- **Whitespace target:** ≥ 40 % of viewport. Achieved through section padding 64–112 px + 60ch line length cap.

---

## 6. Depth & Elevation

| Level | Token | Value | Use case |
|---|---|---|---|
| 0 | flat | `none` | Default surface — borders carry hierarchy |
| 1 | `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | (Reserved — currently unused; only re-introduce if borders insufficient) |
| 2 | `--shadow-md` | `0 4px 12px rgba(15,38,36,0.06)` | Hero image, featured image card |
| 3 | `--shadow-lg` | `0 16px 48px rgba(15,38,36,0.10)` | Modal, dropdown menu |

**Rule:** borders before shadows. Only escalate to shadow when the surface needs to read as "floating above" rather than "next to".

---

## 7. Do's and Don'ts

### Do
- One italic word per heading, in `--gold`, never two.
- Use real photos of the bar / staff / food. Stock-coffee photos look generic.
- Pair every eyebrow with a heading directly below it.
- Keep all body paragraphs at 60ch max so they read like editorial copy.

### Don't
- Don't stack three primary CTAs in one section. One primary + one ghost is max.
- Don't use `--caramel` for body text. It dips below WCAG 4.5:1 on cream.
- Don't add box-shadow to flat cards. Borders only.
- Don't use a gradient unless it has a structural purpose (e.g. fading image-to-text edge, badge depth).
- Don't pad sections under 64 px on desktop — kills the editorial breath.

---

## 8. Responsive Behavior

**Breakpoints (CSS):**
- `≤ 480 px` — mobile portrait
- `481–767 px` — mobile landscape / small tablet
- `768–1023 px` — tablet
- `1024–1199 px` — desktop standard
- `≥ 1200 px` — wide

**Touch targets:** all interactive elements `min-height: 48px` (`.btn`) or 44×44 hit area minimum.

**Strategy:** mobile-first — site assumes phone first, layers up via clamp() and grid template fallbacks. Hero grid collapses to single column < 768 px. Three-up features collapse to single-column < 640 px.

---

## 9. Agent Prompt Guide

When adding a new section:

```
Add a section that follows DESIGN.md §4 (Component Stylings) and §5 (Layout).
- One idea, glanceable.
- Eyebrow + h2 + 1 paragraph + (optional) CTA — never more than 4 type sizes.
- Background alternates: cream → cream-warm → cream.
- Padding: clamp(4rem, 8vw, 7rem) top + bottom.
- Single accent per section (caramel OR gold, not both).
- Body ≤ 60ch line length.
- No shadow on cards by default — use --border-strong on hover instead.
```

When polishing existing copy:

```
Tighten copy so it's glanceable in ≤ 3 seconds.
Italicize ONE evocative word per heading via <em> — wraps in --gold.
Remove bullet-heavy paragraphs; convert to 2–3 sentence prose.
Verify all p tags read in ≤ 60ch.
```
