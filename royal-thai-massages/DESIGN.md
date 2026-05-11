# DESIGN.md — Massagesalon Blueprint (Royal Thai instance)

> Design system voor premium massagesalon-websites. Gemodelleerd naar [awesome-design-md](https://github.com/VoltAgent/awesome-design-md). Lees dit bestand voordat je een nieuwe sectie of variant bouwt.

---

## 1. Visual Theme & Atmosphere

**Mood:** Donkere, verstilde luxe-spa. Diep teal-zwart fond met warme cremekleurige typografie en spaarzame gouden accenten. Voelt als een verlichte massagestudio bij avond — rustig, premium, sensueel-zonder-kitsch. Botanische motieven (bladeren, dampen) als subtiele decoratie.

**Inspiratie:** Pinterest-referentie van Russische massagesalon (donker navy + warm goud). Vertaald naar Thai-spa context: gouden accent als knipoog naar Thaise tempelarchitectuur, deep green vanwege jungle/kruiden.

**Don't:** Stockfoto-cliché met witte handdoeken op witte achtergrond. Geen Comic Sans-achtige "wellness" fonts. Geen pastel.

---

## 2. Color Palette & Roles

> Afgeleid van het Royal Thai logo: burgundy/wine + warm gold + cream.

| Token | Hex | Rol |
|---|---|---|
| `--bg-deep` | `#1A0E14` | Page background — diepe wine-black met burgundy ondertoon |
| `--bg-surface` | `#28161E` | Cards, elevated panels |
| `--bg-elevated` | `#371F2A` | Hover state, secondary cards |
| `--border-subtle` | `#4A2935` | Divider lines, card borders |
| `--text-primary` | `#EFE5D2` | Body text — warm cream (matches logo cream) |
| `--text-muted` | `#B09A82` | Secondary text, captions |
| `--text-faint` | `#6F5C4F` | Disabled, fine print |
| `--accent-gold` | `#D4A55A` | Primary CTA, statlines, dividers — warm gold uit lotus |
| `--accent-gold-soft` | `#A88542` | Hover state op gold |
| `--accent-burgundy` | `#6B1F3B` | Brand secondary — uit "ROYAL THAI" letters in logo |
| `--accent-burgundy-soft` | `#8B2C4B` | Hover/lighter burgundy variant |
| `--accent-warm-glow` | `#C49A6E` | "Geopend"-indicator, subtle highlights (vervangt botanical groen) |

**Ratio (60-30-10):**
- 60% `--bg-deep` + `--bg-surface` (page + cards)
- 30% `--text-primary` (typografie)
- 10% `--accent-gold` (CTAs, accenten)

**WCAG check:** `--text-primary` op `--bg-deep` = 11.8:1 ✅. Gold op deep bg = 7.2:1 ✅.

---

## 3. Typography Rules

| Use | Font | Weight | Size mobile | Size desktop |
|---|---|---|---|---|
| Display H1 | Cormorant Garamond | 500 (italic optional) | 44px | 76px |
| H2 | Cormorant Garamond | 500 | 32px | 52px |
| H3 | Cormorant Garamond | 500 | 24px | 32px |
| Eyebrow / kicker | Manrope | 600 (uppercase, tracking 0.18em) | 12px | 13px |
| Body | Manrope | 400 | 16px | 17px |
| Body-large | Manrope | 400 | 18px | 19px |
| Stat-number | Cormorant Garamond | 400 | 56px | 84px |
| Label / button | Manrope | 600 | 14px | 14px |

**Rules:**
- Line-height: 1.15 voor display headings, 1.6 voor body
- Max line-length: 60ch voor body, 24ch voor display headings
- Italic accent: gebruik italic voor emotionele woorden in headlines ("ontspanning", "rust", "ritueel")
- Never: meer dan 2 fonts. Never: bold serifs (gebruik medium 500).

**Google Fonts import:**
```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## 4. Component Stylings

### Button (primary / gold)
- BG `--accent-gold`, text `--bg-deep`, padding 14px 28px, radius 999px (full pill)
- Hover: BG `--accent-gold-soft`, lift 2px, shadow `0 8px 24px rgba(201,169,110,0.25)`
- Transition 250ms cubic-bezier(0.4, 0, 0.2, 1)

### Button (ghost)
- Border 1px `--border-subtle`, text `--text-primary`, radius 999px
- Hover: border `--accent-gold`, text `--accent-gold`

### Card
- BG `--bg-surface`, border 1px `--border-subtle`, radius 24px, padding 28-40px
- Hover (interactive cards): BG `--bg-elevated`, border `--accent-gold` at 30% opacity, lift 4px

### Image
- Default radius: **32px** voor hero images, 20px voor cards, 16px voor thumbnails
- Always `loading="lazy"` behalve hero
- Subtle vignette overlay op donkere images: `linear-gradient(180deg, transparent 60%, rgba(14,31,31,0.4))`

### Stat block
- Number in display serif, gold color, geen suffix-styling
- Label below in eyebrow style (kicker), muted color
- Divider above: 1px gold line, 40px wide

### Nav
- Sticky transparent → blurred dark on scroll (`backdrop-filter: blur(12px)`, BG `rgba(14,31,31,0.85)`)
- Logo left, links center (uppercase Manrope 600, tracking 0.12em), CTA right (gold pill)
- Mobile: hamburger → full-screen drawer met fade-in

### Section title pattern
- Eyebrow (gold uppercase) op 1 lijn
- H2 onder (display serif), max 2 regels
- Optionele subtitle (body-large muted), max 1 regel
- Center- of left-aligned, never both per pagina

---

## 5. Layout Principles

- **Grid:** 12-col, 24px gutter, max-width 1280px, side-padding 24px (mobile) / 48px (desktop)
- **Vertical rhythm:** sections 96px (mobile) / 160px (desktop) padding-block
- **8pt grid:** alle spacing in multiples of 4 of 8 (klein detail) of 8/16/24/32/48/64/96/128/160 (lay-out)
- **Whitespace ratio:** target ≥ 40% per scherm
- **Asymmetry:** durf images te overlappen secties, gebruik 7/5 of 8/4 col splits voor narrative blokken

---

## 6. Depth & Elevation

| Level | Box-shadow |
|---|---|
| Flat | `none` (default cards) |
| Hover | `0 12px 32px -8px rgba(0,0,0,0.5)` |
| CTA | `0 8px 24px rgba(201,169,110,0.2)` |
| Sticky nav (scrolled) | `0 4px 24px rgba(0,0,0,0.4)` |

Geen drop-shadows op tekst. Geen glow-effects (geen Tron-vibes).

---

## 7. Motion

- **Library:** GSAP 3 + ScrollTrigger via CDN, plus Lenis voor smooth scroll
- **Reveal-on-scroll:** elements fade-in (opacity 0 → 1) + slide-up (y: 24 → 0), duration 0.8s, ease `power2.out`, staggered 0.08s
- **Image reveals:** clip-path `inset(0 100% 0 0)` → `inset(0 0 0 0)`, duration 1.1s, ease `power3.inOut`
- **Hover micro-interactions:** scale 1.02 op image cards, 250ms
- **Respects `prefers-reduced-motion`:** disable parallax + reveals, behoud alleen opacity transitions

---

## 8. Do's and Don'ts

✅ **Do:**
- Use real photography van de salon zelf — geen iStock
- Combineer image + text in 7/5 splits voor verhalende secties
- Eyebrows in gold caps boven elke sectie-titel
- Toon prijzen transparent in een nette tabel — niet "vraag op afspraak"
- Gebruik Thai script (ไทย) als decoratief detail max 1× per pagina

❌ **Don't:**
- Geen carousels die auto-scrollen (frustrerend, verlaagt engagement)
- Geen "lorem ipsum" — placeholders moeten benoemd zijn als `{salon_name}`, `{phone}` etc.
- Geen popup-newsletters of cookie-banners groter dan 60px hoog
- Geen geanimeerde gradients op text
- Geen WhatsApp green/blue iconen die clashen met palette — gebruik gold variant

---

## 9. Responsive Behavior

| Breakpoint | Width | Approach |
|---|---|---|
| Mobile | <640px | Single col, stack all grids, reduce hero to 1 image |
| Tablet | 640-1024px | 2-col grids, full nav inline, hero 60vh |
| Desktop | >1024px | Full 12-col, hero 80vh, parallax enabled |

Tailwind breakpoints: `sm:` `md:` `lg:` `xl:` (default values).

---

## 10. Agent Prompt Guide

Wanneer je deze blueprint dupliceert voor een nieuwe salon:

1. **Kopieer** de hele folder, hernoem naar `{salon-slug}/`
2. **Inventariseer** de nieuwe salon (logo, foto's, behandelingen, openingstijden) volgens `building-local-business-website` skill
3. **Update** alleen `index.html` (search-replace placeholders) en `images/` (vervang foto-URLs)
4. **Behoud** dit DESIGN.md ongewijzigd — kleuren mogen alleen wijzigen als de brand het echt dicteert
5. **Test** in browser + mobile viewport voordat je naar Vercel pusht
6. **Deploy:** `vercel --prod` vanuit de folder, of drag-and-drop op vercel.com

**Variatie-richtlijnen:** als de salon een ander cultureel motief heeft (Balinees, Zweeds, Japans), pas alleen `--accent-gold` en eventueel `--accent-thai-red` aan. Houd het palette donker en cream.
