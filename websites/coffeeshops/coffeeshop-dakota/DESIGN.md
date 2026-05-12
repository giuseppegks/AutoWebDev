# Coffeeshop Dakota — Design Document

> Driepagina presentatie-site voor Coffeeshop Dakota aan de Lange Hezelstraat in Nijmegen. Adapted from the Billy's Coffee blueprint into a strict info-only, gedoogbeleid-compliant variant.

---

## 1. Project basics

- **Klant:** Coffeeshop Dakota (Nijmegen)
- **Adres:** Lange Hezelstraat 113A, 6511 CG Nijmegen
- **Tel:** 024 322 2537
- **Openingstijden:** Dagelijks 09:00 — 00:00
- **Type:** Statische 3-pagina website (info-only)
- **Stack:** Pure HTML/CSS/JS — geen build, geen CMS, geen backend
- **Hosting target:** Vercel static deploy

---

## 2. Legal / content constraints (Nederlands gedoogbeleid)

Coffeeshops vallen onder Nederlands gedoogbeleid en mogen **niet publiekelijk adverteren** voor cannabis. De site respecteert daarom strikt:

**Niet aanwezig op de site:**

- Geen menukaart, geen productnamen, geen strains, geen prijzen
- Geen cannabis-imagery (geen blad, geen rook, geen joints, geen plantfoto's)
- Geen promotionele copy over middelen
- Geen online bestelmogelijkheid

**Wel aanwezig:**

- Adres, openingstijden, telefoonnummer
- Sfeer-foto's van het interieur (geen product zichtbaar — placeholder café-interieur shots overgenomen uit blueprint)
- Volledige huisregels-pagina
- Google Maps embed naar Lange Hezelstraat
- 18+ age gate op elke pagina (eerste pageload)

Voor productinformatie en prijzen wordt bezoekers actief verwezen naar fysiek bezoek aan de zaak.

---

## 3. Architectuur (3 pagina's)

```
coffeeshop-dakota/
├── index.html        ← Home: hero, intro, "de plek" (voor/achterzaal), huisregels-teaser, route-CTA
├── huisregels.html   ← 10 genummerde huisregels (rule-card grid)
├── contact.html      ← Adres, route, Maps embed, openingstijden, kort contactformulier (mailto)
├── css/style.css
├── js/
│   ├── main.js       ← header scroll, mobile drawer, today-hours, open-status, reveal-on-scroll, mailto
│   └── age-gate.js   ← 18+ modal met localStorage flag
├── images/           ← Placeholder interieur-foto's (gedeeld met blueprint — sfeer-only)
└── DESIGN.md
```

Pagina's `menu.html` en `over.html` uit de blueprint zijn **bewust verwijderd**. Het "over" verhaal is gecondenseerd naar een sectie binnen `index.html`.

---

## 4. Visual identity

### 4.1 Color palette — Warm terracotta editorial

Een wat warmere, vriendelijke maar nog steeds ingetogen palet. Donkere terracotta-bruin als basis, saffraan als accent, ruime cream-tinten voor body. Onderscheidend ten opzichte van een groene "specialty coffee" sfeer (zoals de Billy's blueprint) en ook bewust apart van Ketama (donkerder/bruiner spectrum vs Dakota's terracotta-saffraan).

```
--coffee-darkest #140E0A   /* deep near-black */
--coffee-dark    #2A1812   /* hoofd-donker, headers, footer */
--coffee         #46261D
--coffee-warm    #6A4233
--coffee-light   #9C7060

--caramel        #B07045   /* saffraan-terracotta accent */
--caramel-light  #CC8E63
--gold           #8B4F2E

--cream          #F6EFE3   /* page background */
--cream-warm     #ECDFC9   /* section-cream */
--cream-deep     #DCC8A6
--paper          #FCF6E9

--border         #C9B58E
--border-strong  #A0875E
```

### 4.2 Typography

Overgenomen van blueprint — past goed bij de warm-editoriale toon:

- **Display:** Cormorant Garamond (h1–h4, hero, eyebrows in italic em)
- **Body:** Inter (paragrafen, UI, knoppen)

Italic `em` binnen koppen blijft het signature accent (in `--caramel` op de meeste plekken).

### 4.3 Component patterns (overgenomen uit blueprint)

- Sticky header met scroll-bg-change (op `body.home` is de header bij top de caramel-tint, fade naar cream bij scroll)
- Hero met content + media split, "today's hours" + live open/closed badge
- `.split` / `.split--reverse` voor alternerende intro-blokken
- `.features.features--three` met SVG-icon-tiles (huis, TV, dartboard — geen cannabis-iconografie)
- `.strip` photo-strip met 4 vierkante sfeerbeelden
- `.banner` accent-banner voor CTA
- `.section-coffee` (donkere terracotta) als footer-CTA
- `.info-grid` (info-block + contact-card) op contact-pagina
- Map-wrap met Google Maps iframe embed

### 4.4 Nieuwe componenten voor Dakota

- **`.age-gate` modal** — overlay met `rgba(20,14,10,0.92)` backdrop + blur, paper card, 18+ badge, twee acties (Ja / Nee). "Nee" toont een vriendelijke afwijzing met externe escape-link.
- **`.rules-grid` + `.rule-card`** — twee-koloms grid met genummerde regels (38px circle badge + h3 + p).

---

## 5. Interaction & behavior

- **18+ age gate** (`js/age-gate.js`): toont op elke pagina bij eerste load. Bij "Ja" wordt `dakota-age-verified` in localStorage gezet — daarna blijft de gate weg. Bij "Nee" verschijnt een afscheidsscherm met "verlaat de site"-link. Bij private-browsing (geen localStorage) toont de gate elke pageview.
- **Open-status badge** in hero — leest huidige tijd, vergelijkt met 09:00–00:00, toont groene of grijze dot.
- **Today-hours** in hero — toont vandaag's tijden (altijd 09:00–00:00 want dagelijks geopend).
- **Hours table** op contact — highlight `is-today` rij via JS.
- **Reveal-on-scroll** via IntersectionObserver — alle `.reveal` elementen faden/sliden in.
- **Mailto contact form** op contact-pagina — pure clientside, geen storage, opent gebruikers mail-client met vooringevulde subject + body.

---

## 6. Accessibility

- Lang `nl` op `<html>`
- Hero `<img>` met `loading="eager"` + `fetchpriority="high"`; overige `loading="lazy"`
- Age-gate modal met `role="dialog"`, `aria-modal="true"`, `aria-labelledby`
- Focus management: bij open age-gate gaat focus naar "Ja"-knop, body krijgt `age-locked` klasse om scroll te blokkeren
- `prefers-reduced-motion` honored in basis-CSS (overgenomen uit blueprint)
- Min. 48px touch-target op `.btn`
- Alle interactieve elementen hebben zichtbare focus-ring (`outline: 2px solid var(--caramel)`)

---

## 7. PLACEHOLDERs

Items die nog door de klant aangeleverd moeten worden:

- **Foto's:** Alle afbeeldingen in `/images/` zijn placeholder-interieurfoto's overgenomen uit de Billy's-blueprint. Voor productie: vervangen door eigen sfeerfoto's van Dakota (front + back room, dartboards, kunst aan de muur). **Belangrijk:** geen producten in beeld.
- **E-mailadres:** `info@coffeeshopdakota.nl` is een aangenomen adres voor de mailto-link — bevestigen of vervangen.
- **Logo:** Er is geen merk-logo beschikbaar — momenteel renderen we de naam "Dakota" in Cormorant Garamond als wordmark in nav + footer. Een eigen logo zou hier ingevoegd kunnen worden.
- **KVK / juridische voettekst:** niet opgenomen — toe te voegen wanneer aangeleverd.
- **Geverifieerde feestdagensluitingen:** niet gespecificeerd in bronnen, dus huidige hours-table = 7 dagen 09:00–00:00.

---

## 8. Bronnen (publieke info gebruikt — uitsluitend sfeer/context)

- inyourpocket.com/Nijmegen/Dakota — voorzaal/achterzaal-beschrijving, dartborden + roterende kunst, "voormalige danszaal"
- greenmeister.com/coffeeshop/dakota-nijmegen — openingstijden, kaartbetaling, board games
- wanderlog.com/place/details/13604224/dakota — review-quotes over rustige sfeer en vriendelijke bediening

Geen enkele productinformatie of prijsinformatie is van deze bronnen overgenomen op de site.
