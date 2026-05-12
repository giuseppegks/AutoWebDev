# DESIGN.md — Park Café

> Stitch-format design system (awesome-design-md). Read this before generating UI.
> Page-specific overrides live in `design-system/park-cafe/pages/<page>.md` and take precedence over this file.

---

## 1. Visual Theme & Atmosphere

**Mood:** Brunch-spot warmth with editorial restraint. Aubergine-purple walls meet warm peach-coral light through park-facing windows. The visitor reads: *easy, generous, this is where you order a juice and stay for two hours.* Not boutique-cool. Not chain-warm. Honest.

**References:** Lente (Amsterdam) for the soft purple-cream pairing, Bluestone Lane (NYC) for the brunch energy, Pavilion (London) for the park-side ease.

**Avoid:** Pinterest-lavender pastels. "Brunch goals" copywriting. Stock juice photography that doesn't match the actual glasses. Pink-on-pink gradients. Heavy floral SVG flourishes. Coffee-bean illustrations (this is brunch, not roastery).

---

## 2. Color Palette & Roles

**Source brand:** Park Café logo combines deep aubergine + warm peach-coral on warm cream paper.

| Token (CSS var) | Hex | Role | Contrast on cream |
|---|---|---|---|
| `--coffee-darkest` | `#261622` | Section bg (rare — "deep" mode strip) | n/a |
| `--coffee-dark` | `#482638` | Primary text, dark sections, primary buttons | 9.8 : 1 ✓ |
| `--coffee` | `#6C3D4F` | Hover state on dark buttons | 6.2 : 1 ✓ |
| `--coffee-warm` | `#885A6C` | Eyebrow + muted text | 4.6 : 1 ✓ |
| `--coffee-light` | `#B18B9A` | Borders on dark surfaces | 2.4 : 1 (display only) |
| `--caramel` | `#E89357` | **Accent** — CTAs on cream, highlight tags | 3.2 : 1 (display only) |
| `--caramel-light` | `#F4B893` | Hover on accent | n/a |
| `--gold` | `#C87436` | Italic display flourishes, link underline | 4.6 : 1 ✓ |
| `--cream` | `#FBF6ED` | Default page bg | base |
| `--cream-warm` | `#F4EAD8` | Alternating section bg | base |
| `--cream-deep` | `#E8D8C4` | Card bg / hover on light surfaces | base |
| `--paper` | `#FFFDF7` | Highest-contrast surface (menu cards) | base |

**60-30-10 distribution:**
- 60 % `--cream` + `--cream-warm` (page + section alternation)
- 30 % `--coffee-dark` (aubergine) text, dark inversion sections
- 10 % `--caramel` / `--gold` (peach-coral) accent (CTAs, eyebrow, italic flourishes)

**One accent per section.** Aubergine + peach-coral is the brand pair; pick the role per section, don't mix both as accents on one strip.

---

## 3. Typography Rules

Identical to Billy's (shared design language, sibling cafés). See `../billy-coffee/DESIGN.md` §3 for the table. Only the colors differ.

**Italic rule:** One italic word per heading via `<em>`, in `--gold` (warm copper — the peach-coral darkened). ("Het fijnste plekje *aan het park.*")

**Line length:** body + lead capped at 60ch.

**Max 4 sizes per section:** eyebrow + h2 + lead + body.

---

## 4. Component Stylings

Identical token + class system as Billy's. Differences:

- **Hero badge** ("Nu geopend"): green pulse-dot replaced by `--gold` (peach-coral) to harmonise with brand instead of generic green.
- **Photo strip / gallery** — Park has more lifestyle photos (food on tables, juices in glasses). Use 5–6 image strip on home, 16:9 ratio for primary, square for details.
- **Menu cards** — Park's menu is brunch-heavy (juices, sandwiches, sweets). Cards group by category with a thin `--gold` underline under the category heading instead of a coffee-cup icon.

---

## 5. Layout Principles

Same as Billy's — 1200 max-width, 8-point grid, 64–112 px section rhythm, ≥ 40 % whitespace target.

**Park-specific:**
- Hero image should show the park view, not the bar interior. The park is part of the brand promise.
- Menu page uses 2-column grid on desktop (brunch vs. coffee/juices). 1-column collapse < 720 px.

---

## 6. Depth & Elevation

Same scale as Billy's. **Rule:** borders before shadows.

---

## 7. Do's and Don'ts

### Do
- Use real photos of the park view + food.
- Pair every eyebrow with a heading directly below.
- Show the park in at least one image per page.
- Keep aubergine as the dominant brand color, peach-coral as accent only.

### Don't
- Don't stack two warm-tones together — aubergine + coral need cream between them to breathe.
- Don't use `--caramel` for body text (below WCAG 4.5:1).
- Don't add gradient overlays on park photos — the natural light is the asset.
- Don't pad sections under 64 px on desktop.

---

## 8. Responsive Behavior

Identical to Billy's. Touch targets 48 px min. Mobile-first.

---

## 9. Agent Prompt Guide

When adding a section for Park Café:

```
Follow ../park-cafe/DESIGN.md §4 + §5.
- Aubergine dominant, peach-coral accent only.
- One italic word per heading via <em>, --gold color.
- Eyebrow + h2 + lead + body — max 4 sizes.
- Section padding clamp(4rem, 8vw, 7rem).
- Body ≤ 60ch.
- Border-first on cards, not box-shadow.
- If the section is brunch-themed, include at least one food/juice photo.
```
