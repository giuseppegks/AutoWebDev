# DESIGN.md — Café De Beurs

> Stitch-format design system (awesome-design-md). Read this before generating UI.
> Adapted from the Billy's Coffee blueprint — same editorial restraint, but a wood-and-brass palette for a 120-year-old bruin café.

---

## 1. Visual Theme & Atmosphere

**Mood:** Oud bruin café in editorial cladding. The Lange Hezelstraat is the oldest shopping street in Nijmegen; De Beurs has stood on it since 1905. The site needs to read as **rooted, unhurried, lived-in** — without leaning into beer-mat kitsch. Think: a dimly-lit bar, dark wood, brass fittings, a parchment menu under glass. The visitor lands and immediately reads: *this is a stamkroeg, and you're welcome at the bar.*

**References:** Café Chris (Amsterdam Jordaan), Café 't Smalle (Amsterdam), De Burgemeester (Nijmegen). Old wood, brass tap handles, a single warm lamp. Editorial photography of historic interiors (FvF on old Dutch cafés).

**Avoid:** Cartoon beer-mug logos. "Gezellig sinds 1905" sign-off curls. Drop-shadowed pint glasses on a generic wood-grain background. Tartan. Anything that looks like a sports bar template. **No coffee-shop vocabulary**: no espresso cups, no latte-art SVGs, no roastery copy.

---

## 2. Color Palette & Roles

**Source brand:** Café De Beurs has no formal brand assets — we derived a palette from the typology: **dark walnut + brass + parchment** is the visual shorthand of an oud bruin café. Brass is the single accent (signage, tap handles, the rim of a jenever glass).

| Token (CSS var) | Hex | Role |
|---|---|---|
| `--coffee-darkest` | `#1A0F08` | Near-black wood — deep section bg (`.section-coffee`) |
| `--coffee-dark` | `#2E1C0E` | Dark walnut — primary text, dark sections, primary buttons |
| `--coffee` | `#4A2F18` | Medium walnut — hover state on primary |
| `--coffee-warm` | `#6E4A2C` | Light walnut — eyebrow + muted text, link hover |
| `--coffee-light` | `#9B7350` | Oak — borders on dark surfaces |
| `--caramel` | `#A87434` | **Brass** — single accent for CTAs, eyebrow tint, italic flourishes |
| `--caramel-light` | `#C99853` | Hover on accent |
| `--gold` | `#8A5E29` | Deep brass — `<em>` words inside headings |
| `--cream` | `#F4ECDA` | Parchment — default page bg |
| `--cream-warm` | `#E8DBC2` | Section-cream alternating bg |
| `--cream-deep` | `#D9C8A6` | Card bg / image placeholder bg |
| `--paper` | `#FAF3E2` | Highest-contrast surface (info cards) |
| `--border` | `#C8B58E` | Default 1px border |
| `--border-strong` | `#9E8859` | Hover/active border |

**60-30-10 distribution:**
- 60 % parchment (`--cream` + `--cream-warm`) — page + section alternation
- 30 % walnut (`--coffee-dark` text and full-bleed deep-mode sections)
- 10 % brass (`--caramel` / `--gold`) for CTAs, eyebrow, italic flourishes

**One accent per section.** Never mix `--caramel` and `--coffee` as two competing accents.

---

## 3. Typography Rules

| Use | Font | Weight | Size mobile | Size desktop |
|---|---|---|---|---|
| Display H1 (hero) | Cormorant Garamond | 500 | 40px | 72px (clamp 2.5–4.5rem) |
| Display XL (`.h-display`) | Cormorant Garamond | 500 | 44px | 88px (clamp 2.75–5.5rem) |
| H2 | Cormorant Garamond | 500 | 32px | 52px (clamp 2–3.25rem) |
| H3 | Cormorant Garamond | 500 | 22px | 30px |
| Wordmark name | Cormorant Garamond | 500 | 1.5rem | 1.85rem |
| Wordmark sub ("Sinds 1905") | Inter | 500 uppercase, ls 0.22em | 0.7rem | 0.7rem |
| Eyebrow / kicker | Inter | 500 uppercase, ls 0.18em | 12px | 12px |
| Lead body | Inter | 400 | 18px | 21px |
| Body | Inter | 400 | 17px | 17px |
| Caption | Inter | 400 | 14px | 14px |

**Italic rule:** One italic word per heading via `<em>`, colored `--gold` — a visual rest-pause. ("Sinds 1905. *Familie* Janssen sinds 1979.")

**Line length:** body + lead capped at 60ch.

**Max 4 sizes per section:** eyebrow + h2 + lead + body.

---

## 4. Component Stylings

### Wordmark (replaces logo PNG)
- Two-line lockup: serif name (`Café De Beurs`) over a small uppercase sub ("Sinds 1905") with the year in italic gold serif.
- Aligned flush-left in the header. No icon, no background, no bevel.

### Buttons (`.btn`)
- Pill radius (`--r-pill: 999px`), min-height 48px.
- `.btn--primary` — solid `--coffee-dark` on parchment. Hover lifts to `--coffee` (medium walnut).
- `.btn--ghost` — transparent + 1px `--border-strong`. Hover fills with `--cream-warm`, border tightens to `--coffee-warm`.
- `.btn--accent` — solid brass `--caramel` on dark — for sections set on `--coffee-dark`.
- Arrow icon (`.btn-arrow`) — right of label, 14–16px, stroke 1.8–2.

### Cards
- Surface: `--paper` (info cards) or `--cream-warm`.
- Border: 1px `--border`. Hover: `--border-strong` + 2px translateY lift. **No drop-shadow on flat cards.**
- Radius: `--r-lg` (20px) for media, `--r-md` (12px) for content cards.

### Tijdlijn (history timeline — De Beurs-specific)
- Vertical rail in `--border-strong`, brass dots (`--caramel`) at each anchor year.
- Placeholder entries get a muted (`--border-strong`) dot to mark them as "still to verify".
- Each entry: year (serif, italic gold) + uppercase eyebrow title + 1 paragraph (≤ 60ch).

### Kaart list (price list — De Beurs-specific)
- No images; the menu is text-only by design. Categories ordered: tap → speciaal → jenever → wijn → borrelhapjes.
- Each item: serif name on the left, Inter-medium price on the right, optional muted description below.
- Category head: eyebrow + h2 + a one-line note, separated by a 1px `--border` divider.

### Image placeholders (`.hero__placeholder`, `.strip__placeholder`)
- Diagonal-stripe parchment + dashed `--border-strong` outline.
- Labelled "Plaatshouder" so the client knows exactly what's expected. Every placeholder names what photo is wanted ("Foto interieur", "Bep & Jan", "Gevel 1905").

### Eyebrow (`.eyebrow`)
- 12px Inter 500 uppercase, 0.18em letter-spacing, `--coffee-warm`. Always above a heading.

### Hero
- Two-column grid 7/5 desktop, stacked mobile.
- Headline + "Sinds 1905, *familie* Janssen sinds 1979." as the editorial anchor.
- Floating badge bottom-left of image: reads "Bel voor openingstijden" until real hours arrive (brass dot since open-status is unknown).

### Sections
- Vertical rhythm: `--section-y: clamp(4rem, 8vw, 7rem)` (64–112px).
- Background alternation: `--cream` → `--cream-warm` → `--cream` → `--coffee-dark` (rare deep break).

---

## 5. Layout Principles

- **Max width:** 1200px content, 880px narrow (`.container--narrow`).
- **Gutters:** `clamp(1.25rem, 4vw, 2.5rem)`.
- **8-point grid:** spacing tokens multiples of 4 — 4 / 8 / 16 / 24 / 32 / 48 / 64.
- **Proximity rules:**
  - Related elements ≤ 16 px apart
  - Unrelated chunks ≥ 48 px apart
- **Whitespace target:** ≥ 40 % of viewport.

---

## 6. Depth & Elevation

| Level | Token | Use case |
|---|---|---|
| 0 | flat | Default surface — borders carry hierarchy |
| 2 | `--shadow-md` | Hero image card |
| 3 | `--shadow-lg` | Modal, dropdown |

**Rule:** borders before shadows. Brass-tinted shadows where shadows are used — `rgba(42, 24, 16, 0.35)` keeps the warmth.

---

## 7. Do's and Don'ts

### Do
- One italic word per heading, in `--gold`. Never two.
- Lean into the **history**: 1905, familie Janssen, Lange Hezelstraat. The age is the story.
- Use a wordmark (serif name + small caps "Sinds 1905") instead of a logo until the café provides one.
- Mark every unknown photo / price / hour with an explicit "Plaatshouder · vragen aan klant" so it can't ship by accident.

### Don't
- Don't use any coffee-shop iconography. **No beans, no espresso cups, no latte hearts.**
- Don't fabricate opening hours or prices. Use `PLACEHOLDER` everywhere they belong.
- Don't add box-shadow to flat cards.
- Don't introduce a second accent color. Brass is the only accent.
- Don't write "gezellig" in the marketing copy. Show it through restraint, don't claim it.

---

## 8. Responsive Behavior

**Breakpoints (CSS):**
- ≤ 480 px — mobile portrait
- 481–767 px — mobile landscape / small tablet
- 768–1023 px — tablet
- 1024–1199 px — desktop
- ≥ 1200 px — wide

**Touch targets:** all interactive `min-height: 48px` (`.btn`) or 44×44 hit area minimum.

**Strategy:** mobile-first. Hero collapses to single column < 768 px. Tijdlijn keeps its rail on all sizes — the indent just narrows.

---

## 9. Agent Prompt Guide

When adding a new section:

```
Add a section that follows DESIGN.md §4 (Component Stylings) and §5 (Layout).
- One idea, glanceable.
- Eyebrow + h2 + 1 paragraph + (optional) CTA — never more than 4 type sizes.
- Background alternates: cream → cream-warm → cream.
- Padding: clamp(4rem, 8vw, 7rem) top + bottom.
- Single accent (brass --caramel OR --gold).
- Body ≤ 60ch line length.
- Use placeholders (.hero__placeholder) for any photo not yet supplied; label what photo is expected.
- No coffee-shop icons — when an icon is needed: beer glass, jenever bottle, clock, calendar, key.
```

When polishing existing copy:

```
Tighten copy so it's glanceable in ≤ 3 seconds.
Italicize ONE evocative word per heading via <em> — wraps in --gold.
Anchor every page in the year 1905 or the Janssen family where it fits naturally.
Remove bullet-heavy paragraphs; convert to 2–3 sentence prose.
Verify all p tags read in ≤ 60ch.
Replace any fabricated fact with PLACEHOLDER + a note about what to ask the client.
```

---

## 10. PLACEHOLDER Tracker (for client questionnaire)

Send these to Café De Beurs before launch:

- **Openingstijden** per dag (ma–zo) — currently shown as `PLACEHOLDER`
- **Bierkaart**: vaste tap-bieren, speciaalbier-selectie, prijzen
- **Jeneverkaart**: jong / oud / vieux / kruiden / oude klare met prijzen
- **Wijnkaart**: huiswijn rood/wit, prosecco met prijzen
- **Borrelhapjes**: bittergarnituur, kaas, worst, olijven met prijzen
- **Foto's**: gevel (huidig + indien beschikbaar 1905), bar/interieur, jeneverkast, Bep & Jan portret
- **Historische details**: eigenaren tussen 1905 en 1979, anekdotes, evenementen
- **E-mailadres** (currently fallback `info@cafedebeurs.nl` in `js/main.js`)
- **Eventueel**: KVK-nummer voor footer
- **Eventueel**: Instagram-handle (alleen Facebook bekend op dit moment)
