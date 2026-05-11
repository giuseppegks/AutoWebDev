# Massages InBalans — website

Multi-page presentationsite voor de massagepraktijk van **Gaiane Abrahamian** aan de Groesbeekseweg 246b in Nijmegen. Gebouwd vanuit de solo-practitioner-blueprint van Gerrit Jonker Massage, met aangepaste content, services en tarieven.

---

## Stack

- **Pure HTML + Tailwind CSS** (Play CDN — geen build-step)
- **Google Fonts:** Cormorant Garamond + Manrope
- **GSAP 3 + ScrollTrigger** voor scroll reveals
- **Lenis** voor smooth scroll
- **Geen dependencies, geen npm install, geen bundler**

## Project structuur

```
massages-inbalans/
├── index.html              ← homepage: hero, teasers, 6 reviews, CTA
├── over-ons.html           ← verhaal Gaiane, 4 aanpak-cards, opleidingen/ervaring
├── behandelingen.html      ← 4 massagevormen, tarieven, abonnementen, praktisch
├── locaties.html           ← single-locatie detail, map, bereikbaarheid
├── js/
│   └── booking.js          ← multi-step booking modal (Cal.com integratie) — bevat één SHOP_CONFIG block
├── api/                    ← Vercel serverless functies, server-side Cal.com proxy
│   ├── _cal.js
│   ├── event-types.js
│   ├── slots.js
│   └── bookings.js
├── package.json
├── vercel.json
└── images/                 ← leeg — foto's worden van massagesinbalans.nl WP CDN geladen
```

## Boekingssysteem (Cal.com + Vercel proxy)

Volgens de booking-system skill: browser → branded modal (`js/booking.js`) → Vercel serverless proxy (`api/*.js`) → Cal.com v2 API. De `CALCOM_API_KEY` blijft server-side.

**Cal.com Event Types die de klant moet aanmaken** (slug → exacte match met `SHOP_CONFIG.services` in `js/booking.js`):

| Slug                | Lengte | Prijs   |
|---------------------|--------|---------|
| `ontspanning-60`    | 60 min | €85     |
| `ontspanning-75`    | 75 min | €100    |
| `ontspanning-90`    | 90 min | €115    |
| `peace-calming-60`  | 60 min | €100    |
| `peace-calming-75`  | 75 min | €115    |
| `peace-calming-90`  | 90 min | €130    |
| `voetreflex-45`     | 45 min | €65     |
| `voetreflex-60`     | 60 min | €80     |
| `voetreflex-75`     | 75 min | €100    |
| `metamorfose-60`    | 60 min | €85     |

**Stappen vóór livegang:**
1. Cal.com-account aanmaken op [cal.com](https://cal.com).
2. Event Types aanmaken met bovenstaande slugs.
3. Availability instellen in Cal.com → Settings → My Availability — **moet matchen** met `SHOP_CONFIG.hours` in `js/booking.js`. Op dit moment staat dit op ma–vr 09:00–18:00 + za 10:00–15:00 als PLACEHOLDER.
4. API-key aanmaken in Cal.com → Settings → Developer → API Keys.
5. Deploy met env var:
   ```bash
   npx vercel
   npx vercel env add CALCOM_API_KEY production
   npx vercel --prod
   ```

**End-to-end test:** open de productie-URL → "Boek online" → loop door massage → duur → datum → tijd → gegevens → bevestig. Verifieer dat de boeking in Cal.com verschijnt en de bevestigingsmail aankomt.

**Vercel `cleanUrls: true`** → users zien `/over-ons` ipv `/over-ons.html`.

## Lokaal bekijken

```bash
cd "massages-inbalans"
python3 -m http.server 8000
# open http://localhost:8000
```

## Deployen op Vercel

```bash
vercel --prod
```

Custom domain (`massagesinbalans.nl`): Vercel dashboard → Settings → Domains → Add.

---

## Content-bron

Alle content + foto's zijn afgeleid van [massagesinbalans.nl](https://massagesinbalans.nl):

- **Bedrijfsinfo:** naam, adres, telefoon, e-mail
- **Practitioner:** Gaiane Abrahamian — stress- en burn-outcoach, orthomoleculair therapeut, ex-Sanadome
- **4 massagevormen:** Ontspanning, Peace & Calming (uniek/hot stone), Voetreflexmassage, Metamorfosemassage
- **Tarieven:** per 1 januari 2026
- **Abonnementen:** InBalans Relax-Deal (kwartaal/halfjaar/jaar — 5/7/10% korting)
- **Reviews:** 6 testimonials geselecteerd uit `/reviews/`, geanonimiseerd zonder voornamen
- **Foto's:** geladen van massagesinbalans.nl WP CDN

---

## ⚠️ Belangrijk — verifiëren vóór livegang

- [ ] **PLACEHOLDER: openingstijden** — Op de bron-site staat alleen "op afspraak", geen vaste tijden. In `js/booking.js` staat nu ma–vr 09:00–18:00 + za 10:00–15:00 als aanname. **Verifiëren met Gaiane** en `SHOP_CONFIG.hours` aanpassen.
- [ ] **PLACEHOLDER: KvK-nummer** — niet aangetroffen op bron-site. Toevoegen in footer en/of behandelingen.html zodra bekend.
- [ ] **PLACEHOLDER: BTW-status / vergoeding-werkgever** — De site vermeldt vergoeding via werkgever en aftrekbaarheid voor ZZP'ers; verifiëren dat dit zo klopt.
- [ ] **Foto's:** worden direct geladen van massagesinbalans.nl WP CDN. Voor productie: download naar `/images/`, eventueel WebP-conversie.
- [ ] **Bereikbaarheid (locaties.html):** afstanden tot CS en richting Groesbeek zijn algemene aannames — laat Gaiane dit naast een Google Maps-route checken.
- [ ] **Reviews zonder voornamen:** bevestigen of de geanonimiseerde quotes zo akkoord zijn (de teksten komen 1-op-1 of bijna 1-op-1 van /reviews/).
- [ ] **Logo:** typografische wordmark "Massages InBalans" + ronde "ga"-mark. Als Gaiane een echt logo heeft (PNG/SVG), kan dat de mark vervangen.
- [ ] **Social media-links:** in de footer staan nu alleen WhatsApp en e-mail. Voeg LinkedIn/Facebook/Instagram toe als die er zijn.
- [ ] **Voice switch:** Op de bron-site staat plaatselijk "wij" en "ons team van masseurs" (legacy copy). In deze site is alles "ik" — past beter bij een solo-praktijk. Verifieer dat Gaiane het hiermee eens is.
- [ ] **Verwijzing naar InBalans Nano CellCare** — Gaiane biedt op een tweede site (`inbalansnanocellcare.nl`) ook behandelingen voor chronische klachten (long-COVID, burn-out, buikklachten). Overweeg een verwijslink op de homepage of behandelingenpagina.

---

## Verschillen t.o.v. de Gerrit Jonker-blueprint

| Aspect              | Gerrit Jonker (blueprint)   | Massages InBalans                  |
|---------------------|-----------------------------|------------------------------------|
| Specialisatie       | Oncologie + sport           | Stress/burn-out + diepe ontspanning |
| Massagevormen       | 6 (sport, intuïtief, MER, psoas, cranio, stoel) | 4 (ontspanning, Peace & Calming, voetreflex, metamorfose) |
| Sectie `#kanker`    | Aanwezig                    | **Verwijderd** — geen oncologie-specialisatie |
| Tarieven            | €37,50 / €65 / €90          | €65 — €130 (afhankelijk van massage en duur) |
| USP                 | 17+ jaar lichaamsgericht    | Unieke Peace & Calming + holistische coach-achtergrond |
| Voice               | "Ik" (solo)                 | "Ik" (solo) — switch t.o.v. bron-site "wij" |
| Wordmark / mark     | `gj`                        | `ga` (Gaiane Abrahamian)           |
| Locatie             | Nijmegen-Oost · Cees de Jongstraat | Nijmegen · Groesbeekseweg 246b |

---

## Roadmap

- [ ] Foto's downloaden naar `/images/` + WebP
- [ ] Echte Google reviews ophalen (Places API) ter vervanging van geanonimiseerde quotes
- [ ] FAQ-pagina (basis-praktisch staat al in `behandelingen.html` en `locaties.html`)
- [ ] Schema.org structured data (LocalBusiness, MassageTherapy) voor lokale SEO
- [ ] Cal.com Event Types daadwerkelijk aanmaken en API key in Vercel zetten
- [ ] Link toevoegen naar InBalans Nano CellCare voor cliënten met chronische klachten
