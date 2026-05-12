# DESIGN.md — Café Trianon

> Stitch-format design system (awesome-design-md). Read this before generating UI.
> Adapted from the Billy's Coffee blueprint for a café-met-podium in Nijmegen-Oost.

---

## 1. Visual Theme & Atmosphere

**Mood:** Monumentaal café met podium. Trianon is een rijksmonument uit 1910 — gepleisterde I-balken, Art Nouveau-detaillering — én een klein poppodium waar al decennia gespeeld, gedanst en geluisterd wordt. De site moet beide kanten dragen: rust en lunch in het daglicht, jazz en kaarslicht 's avonds.

De bezoeker leest binnen drie seconden: *dit is meer dan een café — dit is een plek waar muziek vanzelf op tafel komt.*

**References:** Paradiso (Amsterdam) en LantarenVenster (Rotterdam) qua sfeer, met de editorial restraint van Tartine en Kaffemik. Stage-blue + amber spotlight, niet "kroegrood-en-houtbruin".

**Avoid:** Donker bruin Joomla-template, overlappende muzieknoot-SVG's, "live music venue" stockfoto's met paarse spotlights, neon. Geen disco-glitter. Geen koffieboon-illustraties.

---

## 2. Color Palette & Roles

**Source brand:** Trianon = navy stage curtains + amber spotlight + cream paper programma's.

| Token (CSS var) | Hex | Role |
|---|---|---|
| `--coffee-darkest` | `#0A1830` | Section bg (rare — "stage" mode strip) |
| `--coffee-dark` | `#15294F` | Primary text, dark sections, primary buttons |
| `--coffee` | `#2A4475` | Hover state on dark buttons |
| `--coffee-warm` | `#4A6394` | Eyebrow + muted text, link hover |
| `--coffee-light` | `#7C95BD` | Borders on dark surfaces |
| `--caramel` | `#D89A3E` | **Accent — spotlight amber** — CTAs, eventtags, eyebrow accents |
| `--caramel-light` | `#E8B968` | Hover on accent |
| `--gold` | `#B07820` | Italic display flourishes (één per heading) |
| `--cream` | `#FBF6EC` | Default page bg |
| `--cream-warm` | `#F2E9D4` | Alternating section bg ("section-cream") |
| `--cream-deep` | `#E2D2B0` | Card bg / hover op licht oppervlak |
| `--paper` | `#FFFCF4` | Highest-contrast surface (menukaart card) |
| `--border` | `#C8B894` | Default borders |
| `--border-strong` | `#A0876A` | Hover borders |

**60-30-10:** 60 % cream / cream-warm pagina, 30 % navy tekst + één diepe sectie, 10 % amber accent (agenda-eyebrow, "Reserveer een tafel", `.btn--accent`).

**One accent per section.** Eventkaart-eyebrows mogen amber. Reguliere section-headings: `--coffee-warm`. Niet beide tegelijk.

---

## 3. Typography Rules

Identical aan blueprint:

| Use | Font | Weight | Mobile | Desktop |
|---|---|---|---|---|
| Display H1 (hero) | Cormorant Garamond | 500 | 40px | 72px |
| H-display | Cormorant Garamond | 500 | 44px | 88px |
| H2 | Cormorant Garamond | 500 | 32px | 52px |
| H3 | Cormorant Garamond | 500 | 22px | 30px |
| H4 | Inter | 600 | 18px | 18px |
| Eyebrow | Inter | 500 uppercase, 0.18em tracking | 12px | 12px |
| Lead | Inter | 400 | 18px | 21px |
| Body | Inter | 400 | 17px | 17px |
| Caption | Inter | 400 | 14px | 14px |

**Italic rule:** Eén italic woord per heading via `<em>` in `--gold`. ("Een huiskamer met *podium.*", "Van Buitenlust *tot Trianon.*")

**Eventdatum (agenda-kaarten):** Cormorant 32px in `--coffee-dark`, met kleine Inter-eyebrow "Mei" eronder — voelt als programmaboekje.

**Line length:** body + lead cap 60ch.

---

## 4. Component Stylings (Trianon-specifiek)

### Agenda-kaart (`.feature` met grid override)
- Layout: `auto 1fr auto` — datum-blok | tekst | zaalindicatie.
- Datumblok rechts begrensd met `border-right: 1px solid var(--border-strong)`.
- Datum: Cormorant 2rem, kleur `--coffee-dark`. Maand: Inter 0.8rem uppercase 0.18em tracking.
- Eyebrow op kaart krijgt `color: var(--caramel)` — markeert event-type (Jazz / Concert / Debat).
- Geen schaduw — border + hover state.

### Buttons
- `.btn--primary` — `--coffee-dark` (navy) op cream. Hover: `--coffee` (medium navy).
- `.btn--accent` — `--caramel` (amber) op cream. Text: `--coffee-darkest`. Hover: `--gold` + cream text. Gebruikt voor "Vraag beschikbaarheid op" en hero-CTA op donkere sectie.
- `.btn--ghost` — transparent + border-strong. Hover: cream-warm fill.

### Hero
- Tweekolom 7/5 zoals blueprint.
- Hero badge: status-dot logica check op lunch-uren (zie §JS), niet 24/7 café.

### Sections — alternation
- `cream` → `cream-warm` (agenda + dansavonden) → `cream` → `coffee-dark` (footer-CTA "Tot zo bij Trianon")
- Agenda krijgt `cream-warm` voor lichte programmafold

---

## 5. Layout Principles

Identical aan blueprint:
- Max-width 1200 px content, 880 px narrow (menu card, debat-pagina's).
- Gutters: `clamp(1.25rem, 4vw, 2.5rem)`.
- `--section-y: clamp(4rem, 8vw, 7rem)`.
- 8-point grid, proximity rules onveranderd.

---

## 6. Depth & Elevation

Borders before shadows. Hero foto + featured concert poster mogen `--shadow-md`. Modal/dropdown only krijgt `--shadow-lg`.

---

## 7. Do's and Don'ts

### Do
- Markeer event-type via amber eyebrow op agenda-kaarten.
- Toon "Lunch geopend" of "Check de agenda" in badge — eerlijker dan blueprint's binaire open/dicht.
- Eén italic woord per heading in `--gold`. Gebruik woorden uit het muziek-veld: *podium, spotlight, tribute, debat, samenkomt.*
- Verwijs naar het rijksmonument-aspect in over.html — dat is Trianon's USP boven concurrenten.

### Don't
- Geen "wij zijn een poppodium" zonder context. Trianon is een café dat óók podium is, niet andersom.
- Geen prijzen verzinnen op menu.html — alles tot bekend "€ —" met PLACEHOLDER note.
- Geen concrete artiestnamen/data zonder bron — agenda-events markeren als PLACEHOLDER.
- Geen 70's-disco purpur of paarse spotlights — palet houdt sober blijven.

---

## 8. Responsive Behavior

Idem blueprint. Agenda-kaarten:
- ≥ 640 px: drie-kolom layout binnen kaart (datum | tekst | zaal).
- < 640 px: zaalindicatie wraps onder tekst, datum blijft links.

---

## 9. Agent Prompt Guide

**Adding an event to agenda:**

```
Add een agenda-kaart binnen #agenda — vorm `<article class="feature">`
met grid 'auto 1fr auto'. Datum links (Cormorant 2rem + Inter eyebrow maand),
tekst midden (amber eyebrow event-type + h3 + 1 zin), zaal rechts.
Markeer als PLACEHOLDER tot bron bevestigd.
```

**Updating openingstijden:**

```
Trianon lunch: ma–vr 11:30–14:30, weekend 13:00–16:00. Avondopening
alleen op concertavonden — niet automatiseren. Badge logic in js/main.js
toont "Lunch geopend" of "Check de agenda".
```
