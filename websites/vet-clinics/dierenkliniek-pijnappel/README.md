# Dierenkliniek Pijnappel — Vet Clinic Blueprint

Premium vriendelijk-warme website voor Dierenkliniek Pijnappel (Sint Annastraat 35, Nijmegen). Tegelijk de **referentie-implementatie** voor de vet-clinic-template blueprint in AutoWebDev.

---

## Stack

- **Pure HTML + Tailwind CDN** (geen build)
- **Google Fonts:** Fraunces (display serif) + DM Sans (body)
- **GSAP 3 + ScrollTrigger** voor reveals
- **Lenis** voor smooth scroll
- **Vercel-ready** met `cleanUrls: true`

## Structuur

```
dierenkliniek-pijnappel/
├── index.html              ← Home: hero + over + 5 service-icons + team teaser + indigo CTA + contact strip
├── specialiteiten.html     ← 5 vakgebieden: Algemene zorg, Tandheelkunde, Kruisband, Lasertherapie, Endoscopie
├── team.html               ← 16 teamleden in 3 groepen + partnerships
├── contact.html            ← Adres, openingstijden, Maps embed, parkeerinfo
├── DESIGN.md               ← Design system (peach bg + indigo CTAs + brand red)
├── vercel.json             ← Clean URLs + security headers
├── README.md               ← Dit bestand
└── images/                 ← Logo + KNMVD/LICG/WVT badges (foto's nog vanaf bron-CDN)
```

## Lokaal testen

```bash
cd dierenkliniek-pijnappel
python3 -m http.server 8000
open http://localhost:8000
```

## Deployen op Vercel

```bash
vercel --prod --yes
```

Of via drag-and-drop op vercel.com/new.

## ⚠️ Vóór livegang verifiëren

Belangrijkste copy-claims die we hebben gemaakt en getoetst moeten worden:

- [ ] **Teamfoto's** kloppen met de echte namen (we mappen op de WordPress upload-URLs — graag bevestigen)
- [ ] **Tone of voice** — improved-copywriting variant; check of de eigenaar zich erin herkent
- [ ] **"Op afspraak"-policy** — we hebben "volledig op afspraak" geschreven, conform site-tekst
- [ ] **Stat "3 specialismen"** verwijst naar Tandheelkunde, Kruisband, Lasertherapie (uit /specialiteiten pagina van bron). Wijzigen indien meer
- [ ] **Spoed-info** — we sturen mensen die buiten openingstijden bellen door via voicemail. Dit klopt als er een doorverwijzing is — anders aanpassen naar specifieke spoedkliniek
- [ ] **Foto's komen direct van dierenkliniekpijnappel.nl** WordPress CDN — voor productie downloaden naar `/images/`

## Voor toekomstige dierenklinieken (blueprint-gebruik)

1. Kopieer deze folder → `websites/vet-clinics/{kliniek-slug}/`
2. Logo vervangen in `images/`
3. Search-replace in alle 4 HTML's:
   - Naam, adres, telefoon, email
   - Teamleden en foto-URLs
   - Specialiteiten (sommige klinieken hebben 3, andere 8)
   - Openingstijden
4. DESIGN.md ongewijzigd laten tenzij het brand het echt vereist
5. `vercel --prod --yes`
