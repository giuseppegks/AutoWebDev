# DESIGN.md — Coffeeshop Ketama

> Stitch-format design system (awesome-design-md). Read this before generating UI.
> Adapted from the Billy's Coffee editorial blueprint, reduced to a strict info-only 3-page variant for a Dutch gedoogde coffeeshop.

---

## 0. Hard Content Constraints (Dutch gedoogbeleid)

This site is for a **Dutch cannabis coffeeshop** and operates under strict legal/social constraints. Future edits MUST respect these rules — they are not stylistic preferences.

**MUST NOT contain:**
- Product menu, strain names, prices, gram weights, or product photos
- Cannabis imagery — no leaves, no buds, no smoke, no joints, no pipes, no rolling papers, no cannabis-icon SVGs
- Promotional drug copy ("get high", "relax", "blaze", "blow your mind", "premium quality", strain reviews, effect descriptions)
- Online ordering, "view menu" CTAs, click-to-buy, basket, or any commerce affordance
- Imagery showing visible product on the bar, in display cases, or in customer hands

**MAY contain:**
- Address, phone, opening hours, age requirement (18+)
- Interior sfeer-foto's that do NOT show product
- House rules (huisregels)
- General "about" / neighbourhood context
- Google Maps embed
- Links to call / open in Maps

**MUST contain:**
- **18+ age gate modal** on every page on first visit (`js/age-gate.js`)
- Explicit ID-verplicht messaging on home + huisregels
- "18+ alleen" badge in footer of every page

---

## 1. Visual Theme & Atmosphere

**Mood:** Ingetogen, professioneel, niet psychedelisch. Een buurt-coffeeshop met een eigen ritme — niet flashy, niet hippy-kitsch, niet stoner-aesthetic. De zaak presenteert zich als een rustige, verzorgde plek met respect voor de wet en de buurt.

**References:** Editorial restaurant-info pages, Dutch local-business sites met sobere palette (donker olijfgroen + warme cream), Aesop's tone of quiet confidence.

**Avoid:** Felle groen-gele "weed colors", hennep-bladmotief, Rasta-kleuren, rook-effecten, psychedelische gradients, slang ("kush", "fire", "gas"), Engelse promotional copy.

---

## 2. Color Palette & Roles

Donker olijfgroen + verfijnd amber + warme grijs. Geen helder gras-groen, geen "weed-green".

| Token (CSS var) | Hex | Role |
|---|---|---|
| `--coffee-darkest` | `#0F1410` | Deep accent surfaces |
| `--coffee-dark` | `#1F2A1F` | Primary text, dark sections, hero bg, primary buttons |
| `--coffee` | `#33422F` | Mid olive, hover on dark |
| `--coffee-warm` | `#52624D` | Eyebrow, muted text, link hover |
| `--coffee-light` | `#82907B` | Soft text, borders on dark |
| `--caramel` | `#B68B3E` | Accent (CTAs op cream, italic flourishes) |
| `--caramel-light` | `#D2A968` | Hover on accent |
| `--gold` | `#8B6627` | Deep accent on cream |
| `--cream` | `#F4F2EC` | Default page bg |
| `--cream-warm` | `#E9E6DC` | Alternating section bg |
| `--cream-deep` | `#D5D0C0` | Card bg / hover |
| `--paper` | `#FAF8F2` | Highest-contrast surface (huisregels cards, modal) |
| `--border` | `#C2BCA8` | Default borders |
| `--border-strong` | `#928871` | Strong borders, age-gate card border |

**60-30-10:**
- 60 % cream + paper
- 30 % deep olive (dark hero, footer CTA section, text)
- 10 % caramel/gold (CTAs, italic em flourishes)

The hero is **deep-olive** (not caramel) to avoid any "fun light coffee shop" vibe. Tone is sober.

---

## 3. Typography

Unchanged from blueprint:
- **Display:** Cormorant Garamond (serif, italic em-flourishes for human warmth)
- **Body:** Inter (clear, neutral, legal-compliant feel)

---

## 4. Page Architecture (3 pages)

```
/                    (index.html)       Hero + about + huisregels teaser + plan-bezoek CTA
/huisregels.html     Full numbered house rules (10 items)
/contact.html        Address, hours, phone, Maps, transit info
```

**Deleted from blueprint:** `menu.html` (illegal), `over.html` (merged into index).

**Nav (3 items + CTA):** Home · Huisregels · Contact · `Plan je bezoek` (→ contact.html)

---

## 5. Age Gate (18+ Modal)

`js/age-gate.js` is loaded on every page. On first visit:
- Renders fullscreen `position: fixed` overlay (`z-index: 100`)
- Card on paper with eyebrow "18+ alleen", title "Ben je 18 jaar of ouder?", short body explaining ID-plicht
- Two buttons: **"Ja, ik ben 18+"** (primary olive) and **"Nee"** (ghost)
- "Ja" → `localStorage.setItem('ketama_age_confirmed', 'yes')`, fade out, removes lock from `body`
- "Nee" → `window.location.href = 'https://www.google.com/'`
- Returning visitors with confirmed flag skip the gate

`body.age-locked { overflow: hidden }` prevents background scrolling during the gate.

---

## 6. Imagery Guidelines

All imagery is **interior sfeer** only:
- Wooden tables, soft lighting, plants, empty bar surfaces
- No products visible, no customers visibly transacting
- Atmospheric over functional

Current image assets in `/images/` are **PLACEHOLDERs from the blueprint** (Billy's Coffee shots) and must be swapped before launch with Ketama-verified interior photography. Alt text already labels them `[PLACEHOLDER]`.

No cannabis-leaf icons, no smoke-cloud SVGs, no rolling-paper graphics.

---

## 7. Tone of Voice

Dutch, sober, factual, friendly. Sentences like:
- "Een vertrouwd adres in Bottendaal."
- "Toegang alleen vanaf 18 jaar, met geldig ID."
- "We zitten in een woonwijk. We vragen onze gasten daar rekening mee te houden."

**Do NOT write:**
- "Premium kwaliteit", "topproducten", "ruime keuze", "beste prijs"
- Anything that reads as marketing of a regulated product

---

## 8. Components Reused from Blueprint

- `.btn`, `.btn--primary`, `.btn--ghost`, `.btn--accent` — recolored via tokens
- `.hero` — overridden to deep-olive background
- `.section-cream`, `.section-coffee`
- `.split`, `.split--reverse`, `.features`, `.banner`
- `.info-grid`, `.info-row`, `.hours-table`, `.map-wrap` (contact)
- `.page-header`, `.page-header__inner`

**New for Ketama:**
- `.age-gate`, `.age-gate__card`, `.age-gate__btn` (modal)
- `.rules`, `.rule`, `.rule__num`, `.rule__title`, `.rule__body` (huisregels list)

**Removed from blueprint:**
- `.menu-*`, `.dish-*` (no menu page)
- `.form` / `[data-mailto-form]` is still in `main.js` but unused (no reservation form on this site)

---

## 9. Footer

3 columns: Bezoek (adres + Maps link), Contact (tel + openingstijden link), Site (Home, Huisregels, Contact). Brand block shows wordmark "Coffeeshop Ketama" (no logo asset) + tagline + 18+ legal reminder. Bottom row: copyright + 18+ + address.

No social media icons in this build — the business has no public web presence yet.
