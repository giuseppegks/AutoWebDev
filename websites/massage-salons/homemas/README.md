# HomeMas — website

Multi-page presentationsite voor HomeMas, de praktijk van Nienke Poiesz in het centrum van Nijmegen voor Traditionele Chinese Massage (Tui Na), voetreflex, hotstone, ontspanning, taping en pedicure. Gebouwd vanuit de solo-practitioner blueprint van Gerrit Jonker Massage met een licht-cream + terracotta palet (palet ongewijzigd).

---

## Stack

- **Pure HTML + Tailwind CSS** (Play CDN — geen build-step)
- **Google Fonts:** Cormorant Garamond + Manrope
- **GSAP 3 + ScrollTrigger** voor scroll reveals
- **Lenis** voor smooth scroll
- **Geen dependencies, geen npm install, geen bundler**

## Project structuur

```
homemas/
├── index.html              ← homepage: hero, over-teaser, 3 behandelingen, reviews (PLACEHOLDER), praktijk-teaser, boeken-CTA
├── over-ons.html           ← verhaal Nienke, 4 aanpak-cards, opleidingen-timeline (Tui Na 1997, eigen praktijk 2007, pedicure 2012)
├── behandelingen.html      ← 6 behandelingen + tarieven-strip + zwangerschap-strip + praktisch
├── locaties.html           ← single-locatie detail, Google Maps embed, bereikbaarheid (centrum Nijmegen)
├── js/booking.js           ← multi-step booking modal (Cal.com integratie) met SHOP_CONFIG
├── api/                    ← Vercel serverless functies, server-side Cal.com proxy
├── package.json            ← name: homemas, type: module
├── DESIGN.md               ← design system (overgeërfd van blueprint — palet ongewijzigd)
├── vercel.json             ← deploy config (clean URLs, security headers)
└── images/                 ← leeg — foto's worden van homemas.nl geladen (zie PLACEHOLDER)
```

## Wat is anders dan de blueprint?

| Aspect | Gerrit Jonker (blueprint) | HomeMas |
|---|---|---|
| Praktijk | Solo, Nijmegen-Oost | Solo, centrum Nijmegen |
| Specialisatie | Lichaamsgerichte massage, oncologie | Traditionele Chinese Massage (Tui Na), pedicure |
| Behandelvormen | 6 westerse massages | Chinese massage + 4 westerse + pedicure |
| Aparte oncologie-sectie | Ja (`#kanker` op behandelingen + strip op home) | **Verwijderd** — niet van toepassing |
| Pedicure | n.v.t. | Volwaardige zesde dienst (60 min · €35), bookable |
| Sociale links | LinkedIn + Facebook | Geen publiek bekend — PLACEHOLDER |
| Prijsstructuur | 30/60/90 · €37,50 / €65 / €90 | 30/45/60/90 · €32 / €43 / €55 / €77 |
| Voorkeurskanaal | Telefoon | **Sms of WhatsApp** (eigenaarsvoorkeur) |
| Bonus | Stoelmassage op locatie | Behandeling aan huis (€15 voorrijkosten binnen Nijmegen) |

## Boekingssysteem (Cal.com + Vercel proxy)

Architectuur: browser → branded modal (`js/booking.js`) → Vercel serverless proxy (`api/*.js`) → Cal.com v2 API. `CALCOM_API_KEY` blijft server-side.

**Cal.com event types — slug-mapping (1-op-1 met `SERVICES` in `js/booking.js`):**

| Slug              | Lengte | Prijs |
|-------------------|--------|-------|
| `tuina-60`        | 60 min | €55   |
| `tuina-90`        | 90 min | €77   |
| `voetreflex-45`   | 45 min | €43   |
| `voetreflex-60`   | 60 min | €55   |
| `hotstone-60`     | 60 min | €55   |
| `hotstone-90`     | 90 min | €77   |
| `ontspanning-45`  | 45 min | €43   |
| `ontspanning-60`  | 60 min | €55   |
| `taping-30`       | 30 min | €32   |
| `pedicure-60`     | 60 min | €35   |

**Voor livegang:**
1. Cal.com account aanmaken → event types met bovenstaande slugs.
2. Availability instellen → moet matchen met `SHOP_HOURS` in `js/booking.js` (nu PLACEHOLDER ma–za, verifiëren met Nienke).
3. API-key aanmaken in Cal.com → Settings → Developer.
4. Deploy:
   ```bash
   npx vercel
   npx vercel env add CALCOM_API_KEY production
   npx vercel --prod
   ```

Tot Cal.com gekoppeld is werkt de modal tot en met datum/duur — op de tijdstap toont hij: "Online boeken nog niet geactiveerd — bel of WhatsApp 06 28 80 91 49". Sms/WhatsApp/mail/telefoon blijven altijd als alternatief beschikbaar.

## Lokaal bekijken

Poort 8765 is mogelijk in gebruik (parallelle builds) — kies een andere poort:
```bash
cd "homemas"
python3 -m http.server 8123
```

## Deployen

```bash
vercel --prod
```

Custom domain (homemas.nl): Vercel dashboard → Settings → Domains.

---

## Content-bron

Alle content + foto's afgeleid van [homemas.nl](https://www.homemas.nl):

- **Bedrijfsinfo:** HomeMas, Tweede Walstraat 85 Nijmegen, 06-28809149, homemasmassage@gmail.com
- **Bio:** Nienke Poiesz; opleiding Tui Na 1997; eigen praktijk sinds 2007; opleiding pedicure 2012
- **6 behandelingen:** Chinese massage (Tui Na), Voetreflex, Hotstone, Ontspanning, Tapen, Pedicure
- **Tarieven:** 30 min €32 · 45 min €43 · 60 min €55 · 90 min €77 · pedicure 60 min €35 · 5- en 10-strippenkaart · 20% studenten/minderbedeelden-korting
- **Voorrijkosten aan huis:** €15 binnen Nijmegen (tot 20 km), €0,20/km daarbuiten
- **Foto's:** `https://www.homemas.nl/fotoos/praktijk{1,2,4,7}.jpg` (rechtstreeks van de bron-site; voor productie naar `/images/` downloaden)

---

## ⚠️ Belangrijk — verifiëren vóór livegang

- [ ] **Openingstijden** — homemas.nl publiceert geen vaste uren ("op afspraak"). In `js/booking.js` staat nu een aanname (ma–vr 09:00–18:00, za 10:00–15:00). **Verifiëren met Nienke.**
- [ ] **Postcode + huisnummer-suffix** Tweede Walstraat 85 — toevoegen voor schema.org en exacte map-pin.
- [ ] **KvK-nummer** — niet vermeld op de bron-site. Footer toont nu `PLACEHOLDER: KvK-nummer verifiëren`.
- [ ] **Recensies** — alle 6 quotes op de homepage zijn **PLACEHOLDER** (homemas.nl heeft geen reviewpagina). Vraag Nienke om 6 echte (geanonimiseerde) quotes.
- [ ] **Social media** — geen LinkedIn / Facebook / Instagram bekend. Footer toont `PLACEHOLDER: social-links indien aanwezig`. Vraag Nienke.
- [ ] **Annuleringsvoorwaarden** — 24-uur regel is overgenomen uit de blueprint, niet expliciet op homemas.nl. Bevestigen.
- [ ] **Foto's** — `homemas.nl/fotoos/praktijkX.jpg` worden direct geladen. Voor productie: downloaden naar `/images/`, WebP-conversie, en check rechten.
- [ ] **Opleiding-instituten** — opleidingen-timeline op `over-ons.html` toont voor 1997 (Tui Na), 2012 (pedicure) en de aanvullende cursussen `PLACEHOLDER` voor de exacte school/cursus-namen. Aanvullen na navraag.
- [ ] **Homeopathie** — op homemas.nl genoemd als aparte dienst. Op deze site verwezen onderaan de behandelingen-lijst als "homeopathisch advies in aparte afspraak". Niet bookable gemaakt. Wel/niet behouden?
- [ ] **Zwangerschapsmassage** — staat nu impliciet onder Tui Na (Chinese massage tijdens zwangerschap-strip op `behandelingen.html`). Op homemas.nl is dit een aparte pagina. Eventueel als losse 7e dienst toevoegen.
- [ ] **Cadeaubon** — genoemd onder Ontspanningsmassage. Bevestigen of dit nog actief is en hoe te bestellen.

---

## Roadmap

- [ ] Foto's downloaden naar `/images/` + WebP
- [ ] Google reviews ophalen (Places API) ter vervanging van de PLACEHOLDER-quotes
- [ ] Schema.org structured data (LocalBusiness, MassageBusiness/HealthAndBeautyBusiness)
- [ ] Cal.com event types daadwerkelijk aanmaken volgens bovenstaande slug-tabel
- [ ] Pagina toevoegen voor homeopathie + zwangerschap als die diensten zelfstandig genoeg zijn
