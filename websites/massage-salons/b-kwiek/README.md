# B-KwieK Sport- & Herstelmassages — website

Multi-page presentationsite voor de massagepraktijk **B-KwieK** in Zwolle-Stadshagen. Gebouwd vanuit dezelfde solo-practitioner blueprint als `gerrit-jonker-massage` — light cream + terracotta palet, Cal.com booking via `/api`-proxy, geen build-step.

⚠️ **Dit is een ROUW-CONCEPT.** De bron-site (b-kwiek.nl) bevat heel weinig content — geen praktijkfoto's, geen volledig adres, geen telefoonnummer, geen openingstijden, geen testimonials. Veel onderdelen staan momenteel als `[PLACEHOLDER]`-tekst in de HTML en zijn voor de klant zichtbaar tijdens review. Pas op met liveganname zonder eerst de PLACEHOLDER-checklist hieronder te behandelen.

---

## Stack

- **Pure HTML + Tailwind CSS** (Play CDN — geen build-step)
- **Google Fonts:** Cormorant Garamond + Manrope
- **GSAP 3 + ScrollTrigger** voor scroll reveals
- **Lenis** voor smooth scroll
- **Geen dependencies, geen npm install, geen bundler**

## Project structuur

```
b-kwiek/
├── index.html              ← homepage: hero, teasers, reviews (PLACEHOLDER), CTA
├── over-ons.html           ← B-KwieK introductie, 4 aanpak-cards, opleidingen
├── behandelingen.html      ← Sport- + Herstelmassage + aanvullende behandelingen
├── locaties.html           ← single-locatie, map (PLACEHOLDER), bereikbaarheid
├── js/
│   └── booking.js          ← booking modal, SHOP_CONFIG bovenin
├── api/                    ← Vercel serverless functies (Cal.com proxy)
├── package.json
├── vercel.json
├── README.md               ← dit bestand
└── images/                 ← leeg
```

## Content-bron

Inhoud is afgeleid van [b-kwiek.nl](https://b-kwiek.nl). Wat we *wel* konden vinden:

- **Bedrijfsnaam:** B-KwieK Sport- & Herstelmassages
- **Locatie (wijk):** Zwolle-Stadshagen
- **E-mail:** info@b-kwiek.nl
- **Social:** instagram.com/bkwiek01 · facebook.com/BKwieK01
- **Diensten:** Sport- & herstelmassage · therapeutisch tape · hoofdpijnmassage · bindweefselmassage · artrose-massage · sportverzorging
- **Tarieven (bron):** Hele rug 60min €70 · Deelmassage 30min €40 · Hoofdpijn 60min €70 · Bindweefsel+rug 60min €70 · Artrose 60min €70 · Tape intake €17,50 / vervolg €12,50
- **Opleidingen:** Sportmassage hardlopers (mei 2025) · Artrose (jan 2024) · Bindweefsel (nov 2023) · Hoofdpijn (sep 2023) · Topsportmasseur (in afronding)
- **Certificering:** EHBO & AED
- **Externe booking:** [bkwieksportherstelmassages.setmore.com](https://bkwieksportherstelmassages.setmore.com)

Wat we **niet** konden vinden (zie PLACEHOLDER-checklist):

- Naam van de therapeut zelf
- Volledig straatadres
- Telefoonnummer
- Openingstijden
- KvK-nummer
- Praktijkfoto's en therapeut-foto
- 90-min tarieven (alleen 60min vermeld)
- Annulerings- en betaalbeleid
- Eventuele strippenkaart / pakketten
- Bestaande reviews

---

## ⚠️ PLACEHOLDER-checklist (vragen aan klant vóór livegang)

De HTML bevat overal zichtbare `[PLACEHOLDER: ...]`-tekst zodat de klant tijdens review precies ziet wat ontbreekt. Onderstaande items moeten ingevuld of bevestigd worden:

### Identiteit
- [ ] **Naam therapeut** — staat op geen enkele pagina van b-kwiek.nl
- [ ] **Korte persoonlijke intro** (1–2 alinea's) — voor `index.html` hero, `over-ons.html` intro
- [ ] **Praktijkfoto's** — minimaal 3: behandelruimte, therapeut, tape/behandeling in uitvoering
- [ ] **Therapeut-portretfoto** — voor over-ons hero en homepage teaser
- [ ] **KvK-nummer** — voor footer

### Contact
- [ ] **Volledig adres** (straat, huisnummer, postcode) — voor `locaties.html`, footers, `js/booking.js` (`SHOP_CONFIG.addressICS`) en de Google Maps embed
- [ ] **Telefoonnummer** (zowel display als +31-formaat E.164) — voor footers, CTA-knoppen, en `js/booking.js` (`SHOP_CONFIG.phoneDisplay` + `phoneE164`)
- [ ] **Openingstijden** — voor hero-strip, footer en `SHOP_HOURS` in `js/booking.js`
- [ ] **Of er WhatsApp wordt aangeboden** — momenteel verwijderd uit CTA's omdat er geen nummer is

### Tarieven
- [ ] **Tarief 90-min sport- en herstelmassage** — bron noemt alleen 60min €70
- [ ] **Eventuele strippenkaart / pakketten** — bron noemt deze niet, in de praktijk soms wel
- [ ] **Sport- & herstel: tarief voor benen-30min / rug-schouders-nek-30min** — bron noemt €40, te bevestigen

### Beleid
- [ ] **Annuleringsbeleid** (24 uur kosteloos? Boetes?)
- [ ] **Betaalmethodes** (Tikkie / pin / contant)
- [ ] **Eerste-keer-intake** procedure

### Reviews
- [ ] **Google Reviews of testimonials** — momenteel 3 PLACEHOLDER-kaarten op homepage. Vragen of er bestaande quotes beschikbaar zijn, of dat we deze sectie volledig weghalen tot er reviews zijn

### Bereikbaarheid (locaties.html)
- [ ] Bevestigen fietspad / fietsenstalling
- [ ] Dichtstbijzijnde bushalte vanaf Zwolle Centraal
- [ ] Parkeerinfo (betaald/vrij, blauwe zone, bezoekerskaarten?)

---

## Booking — twee paden

Er zijn twee parallele booking-flows in de site:

1. **Cal.com via eigen modal** (zoals blueprint). Slugs: `sport-60`, `sport-90`, `herstel-60`, `herstel-90`. Klant moet een Cal.com account opzetten met deze 4 Event Types. **Nog niet gekoppeld — zonder API-key toont de modal nette fallback-message.**
2. **Setmore (huidig systeem)** — bestaande boekingslink van b-kwiek.nl. Knop verwijst naar `https://bkwieksportherstelmassages.setmore.com`. Werkt direct, zonder configuratie.

Aanbeveling aan de klant: óf doorgaan met Setmore (knop is al actief), óf migreren naar Cal.com voor de eigen domein-experience. Tijdens migratie kunnen beide naast elkaar lopen.

### Cal.com setup (indien gewenst)

1. Account: cal.com — gratis voor single user
2. Event Types aanmaken:

   | Slug         | Duur   | Indicatieve prijs |
   |--------------|--------|-------------------|
   | `sport-60`   | 60 min | €70 (te bevestigen)|
   | `sport-90`   | 90 min | [PLACEHOLDER]     |
   | `herstel-60` | 60 min | €70               |
   | `herstel-90` | 90 min | [PLACEHOLDER]     |

3. Availability in Cal.com **moet matchen** met `SHOP_HOURS` in `js/booking.js`. Beide zijn momenteel placeholder (default ma–vr 08:00–18:00).
4. API-key kopiëren uit Cal.com → Settings → Developer → API Keys.
5. Deploy:
   ```bash
   npx vercel
   npx vercel env add CALCOM_API_KEY production
   npx vercel --prod
   ```

---

## Lokaal bekijken

```bash
cd "b-kwiek"
python3 -m http.server 8000
# open http://localhost:8000
```

(Port 8765 is in gebruik door een parallelle build — gebruik 8000.)

## Deployen

```bash
vercel --prod
```

Custom domain (b-kwiek.nl): in Vercel-dashboard koppelen.

---

## Verschillen t.o.v. de Gerrit-Jonker blueprint

| Aspect | Gerrit Jonker | B-KwieK |
|---|---|---|
| Focus | Lichaamsgerichte holistische massage | Sport- & herstelmassage |
| Massages | 6 (sport, intuïtief, MER, psoas, cranio, stoel) | 2 (sport, herstel) + 4 specialisaties |
| Specialisatie-sectie | Massage bij kanker (verwijderd) | Sportverzorging / preventie |
| Tarieven | €37,50 / €65 / €90 | €40 / €70 / [PLACEHOLDER 90min] |
| Therapeut-info | Volledig verhaal | Veel PLACEHOLDERS |
| Foto's | 4 stuks uit WP CDN | Alleen logo + 1 generieke foto |
| Adres | Cees de Jongstraat 6 Nijmegen | [PLACEHOLDER] Zwolle-Stadshagen |
| Booking | Cal.com (geconfigureerd nodig) | Setmore actief + Cal.com optioneel |

---

## Roadmap

- [ ] Klantintake-vragenlijst rondsturen (zie PLACEHOLDER-checklist)
- [ ] Foto's ontvangen + naar `/images/` plaatsen
- [ ] Beslissing Setmore vs. Cal.com
- [ ] Volledig adres invullen + map-embed verfijnen
- [ ] Reviews ophalen (Google Places API of bestaande quotes)
- [ ] Schema.org structured data (LocalBusiness, MassageTherapy)
- [ ] Live testen op b-kwiek.nl (na DNS-switch)
