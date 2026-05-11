# Gerrit Jonker Massage — website

Multi-page presentationsite voor de massagepraktijk van Gerrit Jonker in Nijmegen-Oost. Gebouwd vanuit de Royal Thai massagesalon-blueprint (zie `../royal-thai-massages/README.md`) met een warm-earth variant op het palet en aangepast voor een solo-practitioner met één locatie.

---

## Stack

- **Pure HTML + Tailwind CSS** (Play CDN — geen build-step)
- **Google Fonts:** Cormorant Garamond + Manrope
- **GSAP 3 + ScrollTrigger** voor scroll reveals
- **Lenis** voor smooth scroll
- **Geen dependencies, geen npm install, geen bundler**

## Project structuur

```
gerrit-jonker-massage/
├── index.html              ← homepage: hero, teasers, reviews, CTA
├── over-ons.html           ← verhaal Gerrit, 4 aanpak-cards, opleidingen-timeline
├── behandelingen.html      ← 6 massagevormen, tarieven, massage bij kanker, praktisch
├── locaties.html           ← single-locatie detail, map, bereikbaarheid
├── js/
│   └── booking.js          ← multi-step booking modal (Cal.com integratie)
├── api/                    ← Vercel serverless functies, server-side Cal.com proxy
│   ├── _cal.js             ← shared Bearer-auth + version header helper
│   ├── event-types.js      ← GET — lijst event-types (slug → ID map voor de modal)
│   ├── slots.js            ← GET — beschikbare tijdslots per dag
│   └── bookings.js         ← POST — boeking aanmaken
├── package.json            ← type: module (Vercel verwacht ESM in api/*.js)
├── DESIGN.md               ← design system + verschillen met Royal Thai-instance
├── vercel.json             ← deploy config (clean URLs, security headers)
├── README.md               ← dit bestand
└── images/                 ← leeg — foto's worden van gerritjonkermassage.nl WP CDN geladen
```

## Boekingssysteem (Cal.com + Vercel proxy)

Volgens de [booking-system skill](https://github.com/giuseppegks/AutoWebDev/blob/main/skills/booking-system/SKILL.md):

**Architectuur:** browser → branded modal (`js/booking.js`) → Vercel serverless proxy (`api/*.js`) → Cal.com v2 API. De `CALCOM_API_KEY` blijft server-side; klanten zien nooit een Cal.com-iframe of -branding.

**Wat de klant moet doen vóór livegang:**

1. **Cal.com account aanmaken** ([cal.com](https://cal.com)) — gratis voor single user
2. **Event Types maken** met deze slugs (1-op-1 met `SERVICES` in `js/booking.js`):

   | Slug          | Lengte | Prijs     |
   |---------------|--------|-----------|
   | `intuitief-60`| 60 min | €65       |
   | `intuitief-90`| 90 min | €90       |
   | `sport-60`    | 60 min | €65       |
   | `sport-90`    | 90 min | €90       |
   | `mer-60`      | 60 min | €65       |
   | `mer-90`      | 90 min | €90       |
   | `psoas-60`    | 60 min | €65       |
   | `psoas-90`    | 90 min | €90       |
   | `cranio-60`   | 60 min | €65       |
   | `cranio-90`   | 90 min | €90       |
   | `stoel-30`    | 30 min | €37,50    |
   | `intake-30`   | 30 min | gratis    |

3. **Availability instellen** in Cal.com → Settings → My Availability — **moet matchen** met `SHOP_HOURS` in `js/booking.js` (ma–vr 08:00–18:00). Desync = klanten zien slots die niet echt vrij zijn.
4. **API-key aanmaken** in Cal.com → Settings → Developer → API Keys. Eenmalig kopiëren.
5. **Deploy met env var:**
   ```bash
   npx vercel                               # initial link
   npx vercel env add CALCOM_API_KEY production
   # plak de key — invoer is niet zichtbaar, dat klopt
   npx vercel --prod
   ```

**End-to-end test:** open de productie-URL → "Boek online" → loop door massage → duur → datum → tijd → gegevens → bevestig. Verifieer dat de boeking in Cal.com verschijnt en de bevestigingsmail aankomt.

**Wanneer Cal.com nog niet is gekoppeld** (zoals nu): de modal opent en alle stappen tot en met datum werken; op de tijdstap toont hij "Online boeken nog niet geactiveerd — bel of WhatsApp …". Bel/WhatsApp/mail blijven dus altijd functioneel als alternatief.

**Vercel `cleanUrls: true`** → users zien `/over-ons` ipv `/over-ons.html`.

## Lokaal bekijken

```bash
cd "gerrit-jonker-massage"
python3 -m http.server 8000
# open http://localhost:8000
```

## Deployen op Vercel

```bash
vercel --prod
```

Custom domain (gerritjonkermassage.nl): Vercel dashboard → Settings → Domains → Add.

---

## Content-bron

Alle content + foto's zijn afgeleid van [gerritjonkermassage.nl](https://gerritjonkermassage.nl):

- **Bedrijfsinfo:** naam, tagline, adres, telefoon, mail, KvK
- **6 massagevormen:** Sport, Intuïtief, MER, Psoas, Craniosacraal, Stoel
- **Tarieven:** 30/60/90 min · €37,50 / €65 / €90 · 10-strippen-stamgastvoordeel
- **Opleidingen:** 2008 Margrit Siemerink, 2012 Helder & Kadira (oncologie), 2013 Serenora (craniosacraal), 2015 Positive Touch (deep tissue), 2019 MER
- **Reviews:** 9 testimonials uit `/recensies/`, beroepsmatig gelabeld zonder voornamen
- **Foto's:** 4 stuks van de WP CDN

---

## ⚠️ Belangrijk — verifiëren vóór livegang

- [ ] **Postcode** bij `Cees de Jongstraat 6` — niet expliciet op de bron-site; vul aan na bevestiging eigenaar.
- [ ] **Foto's:** worden direct geladen van gerritjonkermassage.nl WP CDN. Voor productie: download naar `/images/`, eventueel WebP-conversie.
- [ ] **17+ jaar ervaring** — afgeleid van opleidingsdatum 2008. Verifiëren met Gerrit.
- [ ] **Tikkie/contant betalen** — aanname; checken of dit klopt.
- [ ] **Bereikbaarheid (locaties.html):** afstanden tot CS en buslijnen zijn algemene aannames — laat Gerrit dit naast een Google Maps-route checken.
- [ ] **Stoelmassage op locatie / zakelijke offerte** — bevestigen of dit nog steeds aangeboden wordt.
- [ ] **Reviews zonder voornamen** — bevestigen of de geanonimiseerde quotes zo akkoord zijn (de teksten komen 1-op-1 van /recensies/).

---

## Verschillen t.o.v. Royal Thai blueprint

Zie `DESIGN.md` §9 voor de volledige diff. Belangrijkste:

- Palet verschoven van burgundy → warm aardse bruin/koper
- Twee locaties → één locatie
- 12 massages + 5 pakketten → 6 massagevormen + prijs per duur
- Voice van "wij" → "ik"
- Logo: typografische wordmark + `gj`-ringmarker i.p.v. PNG-logo
- Nieuwe sectie: massage bij kanker (eigen anchor `#kanker`)
- Nieuwe sectie: opleidingen-timeline (2008–2019)

---

## Roadmap

- [ ] Foto's downloaden naar `/images/` + WebP
- [ ] Echte Google reviews ophalen (Places API) ter vervanging van de geanonimiseerde quotes
- [ ] FAQ-pagina (basis-praktisch staat al in `behandelingen.html` en `locaties.html`)
- [ ] Schema.org structured data (LocalBusiness, MedicalBusiness/MassageTherapy type) voor lokale SEO
- [ ] Online boekingsmodule (Salonized, Treatwell of soortgelijk)
