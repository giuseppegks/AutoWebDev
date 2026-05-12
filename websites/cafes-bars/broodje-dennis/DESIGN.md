# Broodje Dennis — Design System

> Warm editorial met een punchy broodjeszaak-energie. Vijftien jaar Nijmegen, nu ook in het centrum. Geen poespas, wel een rij.

## 1. Brand voice

**Tone:** Direct, eerlijk, een tikje rauw. Zoals Dennis zelf praat — geen marketing-taal, geen overdreven beloftes. "Een goed broodje, en daar gaat het om."

**Voorbeelden:**
- "Hete kip, krokante pistolets, huisgemaakte salades en een rij die zichzelf bewijst."
- "Geen poespas. Wel een rij."
- "De broodjes waar mensen voor terugkomen."

## 2. Palette — Warm + Punchy

De keuze voor dit palet komt voort uit het broodje zelf: gegrilde-broodje-korst-bruin als basis, een vrolijke tomaten-rood-oranje als accent voor de hete-kip-energie, en een warm crème voor de "huiskamer-broodjeszaak" sfeer. Geen bakery-cream-saai — punchy en eigentijds.

### Coffee (basis — donker naar licht)
- `--coffee-darkest: #1F1305` — espresso bruin near-black (footer, tekst)
- `--coffee-dark:    #3B2613` — gegrilde-broodje-korst donker (h1, h2)
- `--coffee:         #5C3F22` — medium hout (body tekst)
- `--coffee-warm:    #8F6738` — warm middenbruin
- `--coffee-light:   #B89466` — licht hout, voor subtiele accenten

### Caramel (accent — punchy tomaten-rood-oranje)
- `--caramel:       #E0651F` — signature tomaten-rood-oranje (CTAs, eyebrow accents)
- `--caramel-light: #F08745` — lichter, voor hover-states en gradients
- `--gold:          #B04C12` — donkerder tomaat, voor focus rings

### Cream (paper / neutraal)
- `--cream:        #FBF5E8` — warm wit, body background
- `--cream-warm:   #F4E8CE` — section-cream blocks
- `--cream-deep:   #E5D2A8` — dieper crème, voor banners
- `--paper:        #FFFCF3` — papieren wit, cards

### UI tokens
- `--border:        #D9C28F` — zachte lijn
- `--border-strong: #A88B58` — uitgesproken lijn

### Tekst
- `--text:        #1F1305` — body
- `--text-muted:  #5C3F22` — secondair
- `--text-soft:   #8F6738` — tertiair / metadata

## 3. Typography

| Rol | Font | Why |
|-----|------|-----|
| Display | Cormorant Garamond (400–700) | Editorial elegantie — contrast met de rauwe broodje-energie |
| Body | Inter (300–700) | Helder, modern, leest snel op een lunchtelefoon |

**Stijl-trucs:**
- H1/H2 hebben vaak een `<em>` met cursief — voor de "spreektaal-pauze"
- Eyebrow labels in `text-transform: uppercase`, `letter-spacing: 0.18em`, kleur `--coffee-warm` of `--caramel`

## 4. Spacing — editorial breath

- `--section-y: clamp(4rem, 8vw, 7rem)` — 64–112px voor luchtige editorial-ritmiek
- 40%+ whitespace target op desktop
- `--container: 1200px`, `--container-narrow: 880px`

## 5. Componenten

- **Hero**: groot beeld rechts, content links, meta-strip onder (adres, vandaag, USP)
- **Open-status badge**: live indicator op hero-foto — do–zo 10:00–17:00
- **Split sections**: 60/40 beeld+tekst, afwisselend links/rechts
- **Strip**: 4-foto rij, klikbaar naar relevante pagina
- **Banner**: caramel-gradient block voor catering-CTA
- **Section-coffee**: donker espresso footer-CTA voor warm afscheid

## 6. Logo

Tekstueel wordmark — "Broodje Dennis" in Cormorant Garamond 600, kleur `--coffee-dark`. Geen PNG logo (echt logo nog niet beschikbaar via Instagram/FB scraping).

## 7. Wat afwijkt van Billy's blueprint

| Element | Billy's | Broodje Dennis |
|---------|---------|----------------|
| Palette | Forest groen + caramel-goud | Espresso-bruin + tomaten-oranje |
| Uren | Wo–Ma 8:30–16:30, di dicht | Do–Zo 10:00–17:00, ma–wo dicht |
| Logo | PNG | Tekst-wordmark |
| Hoofd-CTA | "Reserveer een tafel" | "Catering aanvragen" |
| Menu-pagina | Image slider (kaart-foto's) | Tekst-cards per categorie |
| Verhaal | Festivals → buurtcafé | Lindenholt → Hezelstraat (15 jaar) |
| Email | info@billys.coffee | info@broodjedennis.nl (PLACEHOLDER) |

## 8. PLACEHOLDERs

- Telefoonnummer
- E-mailadres (huidig: info@broodjedennis.nl — moet verified)
- Foto's (huidig: reused van Billy's blueprint — moeten echte Broodje Dennis foto's worden)
- Prijzen op het menu
- Echte broodje-namen waar onbekend (lijst gebaseerd op Nederlands broodjeszaak-standaard)
