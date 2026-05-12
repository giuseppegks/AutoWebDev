# DESIGN.md — Dierenkliniek Pijnappel (Vet Clinic Template Reference)

> Light & warm dierenarts/dierenkliniek website met perzik-cream achtergrond + indigo CTAs + behoud van de rode Pijnappel brand color. Inspired by the PetsLife (Russian) vet clinic design pattern.

---

## 1. Visual Theme & Atmosphere

**Mood:** Warm, vriendelijk, vertrouwd. Een dierenkliniek voelt soms klinisch — deze stijl voelt juist als binnenstappen bij iemand thuis. Zachte perzik-tinten op de achtergrond, witte kaarten met afgeronde hoeken voor "rustige professionaliteit", levendige indigo CTA-knoppen voor optimisme + actie. De rode wordmark van het Pijnappel-logo zit als warm-tegenwicht in het palet.

**Don't:** Geen koude blauw/wit ziekenhuis-vibes. Geen pure pastels. Geen Comic Sans-vriendelijkheid — we zoeken volwassen + warm.

---

## 2. Color Palette & Roles

| Token | Hex | Rol |
|---|---|---|
| `--bg-base` | `#F7E8D6` | Page background — warm peach cream |
| `--bg-card` | `#FFFFFF` | Cards, elevated panels |
| `--bg-soft` | `#FCF1E2` | Subtle alt-section background |
| `--bg-cta-block` | `#5B47F0` | Indigo callout-box achtergrond (huisbezoek-CTA) |
| `--accent-indigo` | `#5B47F0` | Primary CTA, links, focus states |
| `--accent-indigo-deep` | `#4839C7` | Hover state op indigo |
| `--accent-peach` | `#F0B98E` | Circle backgrounds achter foto's, paw decorations |
| `--accent-peach-light` | `#F8D9BB` | Subtler peach for badges, soft borders |
| `--brand-red` | `#B7242B` | Pijnappel rood — voor 1 accent per pagina max (logo, telefoon-icon, heading underline) |
| `--text-primary` | `#2A1F1A` | Body text — warm dark brown-black |
| `--text-muted` | `#6B5D54` | Secondary text, captions |
| `--text-faint` | `#A8978A` | Disabled, fine print |
| `--border-soft` | `#EBD9C0` | Card borders, dividers |

**Ratio:** 60% peach bg + 30% white cards + 10% indigo accents. Het rood houden we voor max 1 plek per viewport.

**WCAG:** `--text-primary` op `--bg-base` = 12.4:1 ✅. Indigo CTA op white = 5.8:1 ✅. Indigo bg with white text = 7.1:1 ✅.

---

## 3. Typography Rules

| Use | Font | Weight | Size mobile | Size desktop |
|---|---|---|---|---|
| Display H1 | Fraunces | 500 (italic optional) | 40px | 72px |
| H2 | Fraunces | 500 | 30px | 48px |
| H3 | Fraunces | 500 | 22px | 28px |
| Eyebrow | DM Sans | 600 uppercase, tracking 0.14em | 11px | 12px |
| Body | DM Sans | 400 | 16px | 17px |
| Body-large | DM Sans | 400 | 18px | 19px |
| Stat-number | Fraunces | 500 | 48px | 72px |
| Button | DM Sans | 600 | 14px | 15px |

**Imports:**
```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,500&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**Rules:**
- Line-height: 1.1 voor display, 1.6 voor body
- Italic accent op emotionele woorden in headlines ("trouwe", "vriend", "huis")
- Body max line-length: 65ch
- Never bold serifs. Never more than 2 fonts.

---

## 4. Component Stylings

### Button (primary / indigo)
- BG `--accent-indigo`, text white, padding 14px 28px, radius 999px (full pill)
- Hover: BG `--accent-indigo-deep`, lift 2px, shadow `0 8px 24px rgba(91,71,240,0.25)`

### Button (secondary / ghost)
- Border 1.5px `--accent-indigo`, text `--accent-indigo`, transparent bg, radius 999px
- Hover: BG `--accent-indigo`, text white

### Button (white-on-indigo)
- Voor binnen het indigo CTA-blok. White bg, indigo text, radius 999px

### Card
- BG `--bg-card`, radius 28px, padding 24-36px
- Optional subtle border `--border-soft`
- Hover: lift 4px, shadow `0 12px 32px -8px rgba(42,31,26,0.08)`

### Image + peach circle
- Foto inside a `aspect-square` of `aspect-[4/5]` container with `--accent-peach` colored circle behind it (using `::before` pseudo)
- Image radius: 24-32px, image scales 1.03 on hover

### Service icon (row-style)
- Icon in `--bg-card` rounded square (60-72px), behind a peach blob/spot decoration
- Label below in DM Sans 600

### Eyebrow / kicker
- DM Sans 600, uppercase, tracking 0.14em, color `--accent-indigo` or `--brand-red`
- Often paired with a small icon (paw / dot)

### Section title pattern
- Eyebrow (indigo caps)
- H2 (Fraunces, max 2 lines, 1 italic word)
- Optional subtitle (body-large muted)
- Default: left-aligned, larger sections allow centered

### Indigo CTA block
- Full-width card, `--bg-cta-block` indigo, white text
- Layout: text left + image right (split), or stacked on mobile
- Pattern from PetsLife "huisbezoek?" callout

### Paw print decoration
- SVG paw outline, peach color, opacity 0.15-0.25, scattered around hero corners

---

## 5. Layout Principles

- **Grid:** 12-col, 24px gutter, max-width 1240px, side-padding 24px (mobile) / 48px (desktop)
- **Vertical rhythm:** sections 80px (mobile) / 120px (desktop) padding-block
- **Asymmetry:** durf foto's te overlappen secties, gebruik 7/5 col splits
- **Whitespace:** ≥ 45% per scherm — vet-clinic feels rushed if cramped

---

## 6. Depth & Elevation

| Level | Shadow |
|---|---|
| Card resting | `0 1px 3px rgba(42,31,26,0.05)` |
| Card hover | `0 12px 32px -8px rgba(42,31,26,0.10)` |
| CTA button | `0 8px 24px rgba(91,71,240,0.25)` |
| Sticky nav scrolled | `0 4px 24px rgba(42,31,26,0.06)` |

No drop-shadow on text. No glow.

---

## 7. Motion

- GSAP + ScrollTrigger via CDN (same as premium-spa-template)
- Lenis voor smooth scroll
- Reveal-on-scroll: opacity 0 → 1 + slide-up y24 → 0, duration 0.7s, ease `power2.out`
- Image reveal: clip-path `inset(0 100% 0 0)` → `inset(0 0 0 0)`
- Respects `prefers-reduced-motion: reduce`

---

## 8. Do's and Don'ts

✅ **Do:**
- Use real photos van de kliniek + team — geen stockfoto-honden
- Toon openingstijden + telefoon prominent
- Eyebrow + 1 italic Fraunces word in elke section heading
- Paw print decorations sparingly in hero + CTA hoeken (max 2-3 per pagina)
- Echte teamleden bij naam noemen + photo (zelfs zonder bio)

❌ **Don't:**
- Geen carousels of auto-scrollers (afleidend op een zorgsite)
- Geen "lorem ipsum" — placeholders met `{naam}`, `{telefoon}` etc.
- Geen FOMO-tactieken ("Nog 2 plekken vandaag!")
- Geen geanimeerde gradients (gevoelig publiek bij dieren-pijn)
- Geen meer dan één rood accent per viewport

---

## 9. Responsive Behavior

| Breakpoint | Width | Approach |
|---|---|---|
| Mobile | <640px | Single col, stack all grids, hero image goes below text |
| Tablet | 640-1024px | 2-col grids, hero side-by-side |
| Desktop | >1024px | Full 12-col, asymmetric splits |

Tailwind breakpoints: `sm:` `md:` `lg:` `xl:`.

---

## 10. Agent Prompt Guide

Bij dupliceren voor andere dierenklinieken:

1. **Kopieer de folder** → `websites/vet-clinics/{kliniek-slug}/`
2. **Logo invoegen** — sampleer de brand-kleur uit het logo en map op `--brand-red` of vervang het accent
3. **Update content** in alle 4 HTML's: naam, adres, telefoon, team, specialiteiten
4. **Aantal team-secties** — kan met meer/minder rollen (alleen dierenartsen + assistenten, geen waarnemend etc.)
5. **Behoud DESIGN.md** ongewijzigd tenzij het echt vereist is (peach bg + indigo CTAs werkt voor de meeste klinieken)

Variatie-tips:
- **Paardenarts** → meer rust + bruintinten, foto van paarden ipv kleine huisdieren
- **Exotische dierenarts** → behoudt peach maar voeg botanical groen toe
- **Spoedkliniek** → maak de indigo levendiger of voeg een rood "spoed"-strip toe
