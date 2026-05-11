# Royal Thai Massage & Spa — Massagesalon Blueprint

Premium one-pager voor Royal Thai Massage & Spa (Arnhem + Nijmegen). Tegelijk de **blueprint** voor toekomstige massagesalon-sites in de regio Nijmegen.

---

## Stack

- **Pure HTML + Tailwind CSS** (Play CDN — geen build-step)
- **Google Fonts:** Cormorant Garamond + Manrope + Noto Serif Thai
- **GSAP 3 + ScrollTrigger** voor scroll reveals
- **Lenis** voor smooth scroll
- **Geen dependencies, geen npm install, geen bundler**

## Project structuur

```
royal-thai-massages/
├── index.html              ← homepage met teasers en CTA's naar subpagina's
├── over-ons.html           ← verhaal, 4 method-cards, sfeer-gallery
├── behandelingen.html      ← alle 12 massages, 5 pakketten, spa & sauna, cadeaubon
├── locaties.html           ← beide vestigingen met maps embed + bereikbaarheid
├── DESIGN.md               ← design system (kleuren, typo, components)
├── vercel.json             ← deploy config (clean URLs, security headers)
├── README.md               ← dit bestand
└── images/                 ← lokale assets — momenteel leeg, foto's worden van WP CDN geladen
```

**Multi-page navigatie:** alle pagina's delen dezelfde sticky nav (Over Ons / Behandelingen / Locaties / Reviews) en footer. Klik op een nav-link gaat naar de respectievelijke pagina; de actieve pagina is gemarkeerd in goud.

**Vercel `cleanUrls: true`** → users zien `/over-ons` ipv `/over-ons.html` in de URL.

## Lokaal bekijken

Open simpelweg `index.html` in de browser. Geen build nodig.

Of serveer met een lichte http server (voor correcte font loading):
```bash
cd "royal-thai-massages"
python3 -m http.server 8000
# open http://localhost:8000
```

## Deployen op Vercel

**Optie 1 — Drag & drop:**
1. Ga naar [vercel.com/new](https://vercel.com/new)
2. Sleep deze hele folder erin
3. Klik "Deploy" — klaar in ~10 sec

**Optie 2 — CLI:**
```bash
npm i -g vercel
cd "royal-thai-massages"
vercel --prod
```

Custom domain (royalthaimassages.nl): in Vercel dashboard → Settings → Domains → Add. DNS instellen volgens Vercel's instructies (CNAME of A-record).

---

## Deze blueprint dupliceren voor een nieuwe salon

1. **Kopieer de map**
   ```bash
   cp -r royal-thai-massages nieuwe-salon-naam
   cd nieuwe-salon-naam
   ```

2. **Inventariseer de nieuwe salon**
   - Bestaande website: logo, foto's, openingstijden, behandelingen, prijzen
   - Google Reviews voor échte testimonials (geen fabricaties — de huidige reviews in deze demo zijn placeholders, vervang met echte quotes!)
   - Adres + telefoon + e-mail per locatie

3. **Pas DESIGN.md aan (alleen indien nodig)**
   - Cultureel motief? Pas `--accent-gold` aan (bv. naar koper voor Balinees, blauwgrijs voor Zweeds)
   - Houd palette donker + cream — dat is de premium-aanslag

4. **Vervang in alle 4 HTML-bestanden** (search & replace, project-wide):
   - `Royal Thai Massage &amp; Spa` → nieuwe naam
   - `+31246793443` / `+31267601100` → nieuwe telefoonnummers
   - `info@royalthaimassages.nl` / `nijmegen@...` → nieuwe e-mail(s)
   - `Steenstraat 61, 6828 CD Arnhem` / `Bloemerstraat 62, 6511 EL Nijmegen` → nieuwe adressen
   - Alle `https://royalthaimassages.nl/wp-content/uploads/...` → nieuwe foto-URLs (of lokale `/images/...`)
   - **Heeft de salon één locatie ipv twee?** Verwijder de tweede location-card uit `locaties.html` en vereenvoudig de "Twee studio's" headline naar bijvoorbeeld "Onze studio".
   - **In `behandelingen.html`:** pas treatment-blokken aan (namen, beschrijvingen, prijzen)
   - **In `over-ons.html`:** pas verhaal + 4 method-cards aan op de tone of voice
   - **In `index.html`:** pas hero-copy, featured 3 treatments, en reviews aan

5. **Test in browser** (mobile + desktop viewport)

6. **Deploy naar Vercel** met dezelfde stappen als hierboven

---

## ⚠️ Belangrijk — wat te verifiëren voordat je live gaat

De huidige content komt deels uit de bestaande royalthaimassages.nl-website. Vóór livegang met de echte klant verifieer:

- [ ] **Reviews:** de drie quotes ("Sophie M.", "Mark & Lieke", "Ricardo K.") zijn **placeholders**. Vervang met écht Google review-citaten.
- [ ] **Stats** (15+ jaar ervaring): controleer deze cijfers met de eigenaar
- [ ] **Telefoonnummer-formattering:** `024 679 34 43` (klopt) en `026 760 11 00` (klopt) — verifieer ook dat de `tel:`-links de juiste nummers gebruiken
- [ ] **E-mail Nijmegen:** `nijmegen@royalthaimassages.nl` — bestaat dit echt? Anders vervangen door `info@`
- [ ] **Foto's:** worden direct geladen van royalthaimassages.nl WP CDN. Voor productie download je ze beter naar `/images/` voor performance + onafhankelijkheid van het oude WP-systeem.
- [ ] **Cadeaubon flow:** nu link naar #boeken — als er een echte cadeaubon-shop is (bv. via Booking system), link daar naartoe.

---

## Roadmap (mogelijk volgend werk)

- [ ] Foto's downloaden naar `/images/` + WebP conversie
- [ ] Echte Google reviews ophalen via Places API of handmatig
- [ ] Online boeking integratie (bv. Salonized, Treatwell)
- [ ] FAQ-pagina (parkeren, betaalwijzen, kleding, etc.) — basis staat al in locaties.html "Praktisch"-sectie
- [ ] Beauty-pagina (lashes, fillers — nu niet opgenomen, te commercieel afwijkend)
- [ ] Engelse taalvariant (`/en/index.html`, `/en/over-ons.html` etc.)
- [ ] Schema.org structured data voor lokale SEO (LocalBusiness, MassageTherapy)
- [ ] Gemeenschappelijke nav/footer extraheren naar JS-include (om duplicatie weg te nemen)
