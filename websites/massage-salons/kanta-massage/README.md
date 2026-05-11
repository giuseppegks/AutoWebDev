# Kanta Massage — website

Multi-page presentatiesite voor de Thaise massagepraktijk van Pimchaya in Nijmegen. Gebouwd vanuit de massagesalon-blueprint (`../gerrit-jonker-massage/`) met een warm cream + terracotta palet en aangepast voor een solo Thai-practitioner met één locatie in Gezondheidscentrum Danielsplein.

---

## Stack

- **Pure HTML + Tailwind CSS** (Play CDN — geen build-step)
- **Google Fonts:** Cormorant Garamond + Manrope
- **GSAP 3 + ScrollTrigger** voor scroll reveals
- **Lenis** voor smooth scroll
- **Geen dependencies, geen npm install, geen bundler**

## Project structuur

```
kanta-massage/
├── index.html              ← homepage: hero, teasers, reviews, CTA
├── over-ons.html           ← verhaal Pimchaya, 4 aanpak-cards, opleidingen-overzicht
├── behandelingen.html      ← 7 Thaise massagevormen, tarieven, praktisch
├── locaties.html           ← single-locatie detail, map, bereikbaarheid
├── js/
│   └── booking.js          ← multi-step booking modal (Cal.com integratie)
├── api/                    ← Vercel serverless functies, server-side Cal.com proxy
│   ├── _cal.js
│   ├── event-types.js
│   ├── slots.js
│   └── bookings.js
├── package.json
├── DESIGN.md               ← design system (warm cream + terracotta + sage)
├── vercel.json
├── README.md               ← dit bestand
└── images/                 ← leeg — foto's worden direct van kantamassage.nl geladen
```

## Boekingssysteem (Cal.com + Vercel proxy)

**Architectuur:** browser → branded modal (`js/booking.js`) → Vercel serverless proxy (`api/*.js`) → Cal.com v2 API. De `CALCOM_API_KEY` blijft server-side; klanten zien nooit een Cal.com-iframe.

**Wat Pimchaya moet doen vóór livegang:**

1. **Cal.com account aanmaken** ([cal.com](https://cal.com))
2. **Event Types maken** met deze slugs (1-op-1 met `SERVICES` in `js/booking.js`):

   | Slug                | Lengte  | Prijs  |
   |---------------------|---------|--------|
   | `thai-30`           | 30 min  | €50    |
   | `thai-60`           | 60 min  | €60    |
   | `thai-90`           | 90 min  | €85    |
   | `thai-120`          | 120 min | €115   |
   | `thai-180`          | 180 min | €165   |
   | `olie-60`           | 60 min  | €60    |
   | `olie-90`           | 90 min  | €85    |
   | `hotstone-90`       | 90 min  | €105   |
   | `kruidenstempel-90` | 90 min  | €105   |
   | `deeptissue-60`     | 60 min  | €60    |
   | `deeptissue-90`     | 90 min  | €85    |
   | `antimigraine-60`   | 60 min  | €60    |
   | `zwangerschap-60`   | 60 min  | €60    |

3. **Availability instellen** in Cal.com → moet matchen met `SHOP_HOURS` in `js/booking.js`:
   - Ma, di, wo: 09:00–21:00
   - Do: gesloten
   - Vr, za, zo: 09:00–21:00
4. **API-key aanmaken** in Cal.com → Settings → Developer → API Keys
5. **Deploy met env var:**
   ```bash
   npx vercel
   npx vercel env add CALCOM_API_KEY production
   npx vercel --prod
   ```

**End-to-end test:** open productie-URL → "Boek online" → loop door massage → duur → datum → tijd → gegevens → bevestig. Verifieer dat boeking in Cal.com verschijnt.

**Vercel `cleanUrls: true`** → users zien `/over-ons` i.p.v. `/over-ons.html`.

## Lokaal bekijken

```bash
cd "kanta-massage"
python3 -m http.server 8000
# open http://localhost:8000
```

## Deployen op Vercel

```bash
vercel --prod
```

Custom domain (kantamassage.nl): Vercel dashboard → Settings → Domains.

---

## Content-bron

Alle content + foto's zijn afgeleid van [kantamassage.nl](https://kantamassage.nl):

- **Bedrijfsinfo:** naam, adres, telefoon, mail
- **7 massagevormen:** Traditionele Thai, Hotstone, Kruidenstempel, Deep Tissue, Anti-migraine, Zwangerschap, Olie
- **Tarieven:** Thai 30–180 min · €50–€165 · Hotstone/Kruiden €105 · andere vormen op Thai-schaal
- **Opleidingen:** Thaise traditionele massage, Lymfedrainage, PaiParin, Thai medische massage, Gezichtsmassage, Diepe bindweefsel, Zwangerschapsmassage, Strektechnieken, Manuele lymfedrainage, Sportmassage
- **Foto's:** direct van kantamassage.nl (`PimchayaPortret.webp`, `GezondheidscentrumDanielsplein.webp`, `strekken.webp`, `hotstone.webp`, `kruiden.webp`)

---

## ⚠️ Belangrijk — verifiëren vóór livegang

- [ ] **PLACEHOLDER: verify volledige naam Pimchaya** — alleen voornaam op bron-site; vraag achternaam.
- [ ] **PLACEHOLDER: verify postcode** bij Danielsplein 3D — niet bevestigd op bron; aangenomen 6543 AB (gehanteerd in `js/booking.js`).
- [ ] **PLACEHOLDER: verify KvK-nummer** — niet vermeld op bron-site; staat als PLACEHOLDER in footers.
- [ ] **PLACEHOLDER: verify prijzen** voor olie, deep tissue, anti-migraine, zwangerschap — op de bron-site niet expliciet vermeld; aangenomen dat dezelfde schaal als Thai geldt (€60/60min, €85/90min). Bevestigen met Pimchaya.
- [ ] **PLACEHOLDER: verify duur** van olie / deep tissue — aangenomen 60 én 90 min; anti-migraine en zwangerschap alleen 60 min. Bevestigen.
- [ ] **PLACEHOLDER: verify reviews** — zes voorbeeld-quotes; alle vervangen door echte testimonials zodra beschikbaar (Google Maps, e-mail).
- [ ] **PLACEHOLDER: verify openingstijden** — ma-wo en vr-zo 09:00–21:00, do gesloten. Bevestigen of dit klopt in alle weken (i.v.m. Cal.com availability).
- [ ] **PLACEHOLDER: verify fietsroute / OV / parkeren** op locaties.html — laat Pimchaya checken naast Google Maps.
- [ ] **PLACEHOLDER: verify betaalmethoden** — aangenomen "contant of Tikkie"; bevestig pin/iDEAL.
- [ ] **PLACEHOLDER: verify cadeaubon-procedure** — bestaat ja; bevestig bedragen, format en levering.
- [ ] **PLACEHOLDER: verify of deep tissue met olie wordt gegeven** — niet bevestigd op bron.
- [ ] **Foto's:** worden direct van kantamassage.nl geladen. Voor productie: downloaden naar `/images/` met WebP-conversie.

---

## Verschillen t.o.v. Gerrit Jonker blueprint

| Aspect | Gerrit Jonker | Kanta Massage |
|---|---|---|
| Practitioner | Gerrit Jonker (NL, holistisch) | Pimchaya (TH, traditioneel Thai) |
| Behandelingen | 6 NL-lichaamsgerichte vormen | 7 Thaise vormen + 5 duurvarianten op Thai |
| Specialisatie | Oncologische massage (#kanker sectie) | Verwijderd — geen oncologische focus |
| Tarief-strip | 3 kolommen (30/60/90) | 5 kolommen (30/60/90/120/180) + override-noot voor hotstone/kruidenstempel |
| Openingstijden | Ma-vr 08:00-18:00 | Ma-wo, vr-zo 09:00-21:00 — donderdag gesloten |
| Wordmark | `gj` | `km` |
| Adres | Cees de Jongstraat 6, Nijmegen-Oost | Danielsplein 3D, Gezondheidscentrum, Nijmegen (ingang De la Reystraat) |
| Reviews | 6 reëel, beroepsmatig gelabeld | 6 PLACEHOLDER — geen reviews op bron |

---

## Roadmap

- [ ] Foto's downloaden naar `/images/` + WebP-conversie
- [ ] Echte reviews ophalen (Google Maps + direct vragen aan vaste klanten)
- [ ] FAQ-pagina toevoegen
- [ ] Schema.org structured data (LocalBusiness, MassageTherapy) voor lokale SEO
- [ ] Cadeaubon-systeem koppelen (e-mail-flow of digitale voucher)
- [ ] Engelse versie overwegen — Pimchaya bedient ook expats
