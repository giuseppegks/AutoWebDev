# Edith Libbers Sportmassage & Voetreflextherapie — website

Multi-page presentatiesite voor de praktijk van Edith Libbers in Nijmegen. Gebouwd vanuit de Gerrit Jonker-blueprint (solo-practitioner massagesalon) en aangepast voor Ediths NGS-aangesloten sportmassage-praktijk aan de Groesbeekseweg 204.

---

## Stack

- **Pure HTML + Tailwind CSS** (Play CDN — geen build-step)
- **Google Fonts:** Cormorant Garamond + Manrope
- **GSAP 3 + ScrollTrigger** voor scroll reveals
- **Lenis** voor smooth scroll
- **Geen dependencies, geen npm install, geen bundler**

## Projectstructuur

```
edith-libbers/
├── index.html              ← homepage: hero, teasers, reviews, CTA
├── over-ons.html           ← verhaal Edith, 4 aanpak-cards, timeline
├── behandelingen.html      ← 4 massagevormen + tarieven + praktisch
├── locaties.html           ← praktijk Groesbeekseweg + map + bereikbaarheid
├── js/
│   └── booking.js          ← multi-step booking modal (Cal.com integratie)
├── api/                    ← Vercel serverless functies, server-side Cal.com proxy
│   ├── _cal.js
│   ├── event-types.js
│   ├── slots.js
│   └── bookings.js
├── package.json
├── DESIGN.md               ← (uit blueprint — beschrijft donkere variant; deze instance is cream-light)
├── vercel.json
├── README.md
└── images/                 ← leeg — foto's worden van edithlibbers.nl WP CDN geladen
```

## Boekingssysteem (Cal.com + Vercel proxy)

**Architectuur:** browser → branded modal (`js/booking.js`) → Vercel serverless proxy (`api/*.js`) → Cal.com v2 API. De `CALCOM_API_KEY` blijft server-side; klanten zien nooit een Cal.com-iframe.

**Wat Edith moet doen vóór livegang:**

1. **Cal.com account aanmaken** ([cal.com](https://cal.com)) — gratis voor single user
2. **Event Types maken** met deze slugs (1-op-1 met `SHOP_CONFIG.services` in `js/booking.js`):

   | Slug             | Lengte | Prijs    |
   |------------------|--------|----------|
   | `sport-45`       | 45 min | €49      |
   | `sport-60`       | 60 min | €65      |
   | `sport-90`       | 90 min | €95      |
   | `ontspanning-45` | 45 min | €49      |
   | `ontspanning-60` | 60 min | €65      |
   | `ontspanning-90` | 90 min | €95      |
   | `voetzone-60`    | 60 min | €65      |
   | `stoel-15`       | 15 min | €17,50   |
   | `stoel-30`       | 30 min | €33,50   |

3. **Availability instellen** in Cal.com → Settings → My Availability — **moet matchen** met `SHOP_CONFIG.hours` in `js/booking.js`. Aanname nu: ma–vr 09:00–18:00. **PLACEHOLDER: verify openingstijden** met Edith.
4. **API-key aanmaken** in Cal.com → Settings → Developer → API Keys.
5. **Deploy met env var:**
   ```bash
   npx vercel
   npx vercel env add CALCOM_API_KEY production
   npx vercel --prod
   ```

**End-to-end test:** productie-URL → "Boek online" → loop door massage → duur → datum → tijd → gegevens → bevestig. Verifieer in Cal.com.

**Wanneer Cal.com nog niet is gekoppeld:** modal opent, alle stappen tot en met datum werken; op de tijdstap toont hij "Online boeken nog niet geactiveerd — bel of WhatsApp 06 18 18 17 96".

## Lokaal bekijken

```bash
cd "edith-libbers"
python3 -m http.server 8000
# open http://localhost:8000
```

## Deployen op Vercel

```bash
vercel --prod
```

Custom domain (edithlibbers.nl): Vercel dashboard → Settings → Domains → Add.

---

## Content-bron

Content + foto's afgeleid van [edithlibbers.nl](https://www.edithlibbers.nl):

- **Bedrijfsinfo:** naam, telefoon, adres, NGS-aansluiting, 2003 zelfstandig, 2024 nieuwe locatie
- **4 massagevormen:** Sportmassage, Ontspanningsmassage, Voetzonereflextherapie, Stoelmassage
- **Tarieven:** 30/45/60/90 min (€33,50 / €49 / €65 / €95); strippen 10×60 €600 of 10×45 €475; stoel 15/30 (€17,50 / €33,50)
- **Aanbevelingen:** 5 testimonials van /aanbevolen/ + 1 placeholder-kaart
- **Foto's:** 3 stuks van de WP CDN (`fotowebsite.jpg` + crops) + NGS-logo

---

## ⚠️ Verifiëren vóór livegang

- [ ] **E-mailadres** — niet expliciet op bron-site; momenteel verwijst alles naar het contactformulier op edithlibbers.nl. Voeg toe in `SHOP_CONFIG.email` en op alle pagina's wanneer bekend.
- [ ] **KvK-nummer** — staat nergens publiek; PLACEHOLDER in footer.
- [ ] **Exacte openingstijden** — bron-site noemt geen tijden. Aanname nu: ma–vr 09:00–18:00. Pas `SHOP_CONFIG.hours` aan in `js/booking.js` én de tekst op `index.html`, `behandelingen.html`, `locaties.html`.
- [ ] **Annulerings- en betaalvoorwaarden** — Tikkie/contant aangenomen; afstemmen met Edith.
- [ ] **Strippenkaart-voorwaarden** — geldigheid en aankoop bevestigen.
- [ ] **Foto's:** worden direct geladen van edithlibbers.nl WP CDN. Voor productie: download naar `/images/` (WebP) — vraag Edith of er meer/recentere foto's beschikbaar zijn.
- [ ] **Reviews:** 5 testimonials komen 1-op-1 van /aanbevolen/. Eén kaart is PLACEHOLDER — vervangen of verwijderen.
- [ ] **Social media URL's:** `https://www.facebook.com/edithlibbers` en `https://www.linkedin.com/in/edithlibbers` zijn aangenomen — verifiëren en zo nodig corrigeren.
- [ ] **Opleidingen-timeline:** alleen NGS en publieke feiten staan vast. Jaartallen voor voetzonereflex/stoel staan op PLACEHOLDER — invullen op `over-ons.html`.
- [ ] **Bereikbaarheidsteksten (locaties.html):** afstanden naar CS en busroutes zijn algemene aannames voor Nijmegen-Oost/Berg en Dal. Laat Edith dit naast Google Maps checken.

---

## Verschillen t.o.v. Gerrit Jonker-blueprint

| Aspect | Gerrit Jonker | Edith Libbers |
|---|---|---|
| Behandelingen | 6 massages + intake bij kanker | 4 massages (sport, ontspanning, voetzone, stoel) |
| Specialisatie | Lichaamsgericht, oncologisch | Sportmassage (NGS), voetzonereflex |
| Voice | "Aandacht, verbinding, lichaam" | "Vakvrouw, no-nonsense, periodiek onderhoud" |
| Strippenkaart | 10 sessies +€25 korting | 10×60 €600 of 10×45 €475 (kale prijs) |
| #kanker-sectie | Ja, eigen anchor | Verwijderd — niet Ediths specialisatie |
| Hours | Ma–vr 08:00–18:00 | Ma–vr 09:00–18:00 (PLACEHOLDER) |
| Logo-initialen | `gj` | `el` |

---

## Roadmap

- [ ] Foto's downloaden naar `/images/` + WebP
- [ ] Echte Google reviews ophalen (Places API) ter aanvulling
- [ ] Schema.org structured data (LocalBusiness + SportsActivityLocation/HealthAndBeautyBusiness)
- [ ] Online boekingsmodule activeren (zie boven)
