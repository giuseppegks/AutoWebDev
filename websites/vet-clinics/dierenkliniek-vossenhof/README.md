# Dierenkliniek Vossenhof — Prospect Mockup

Demo-site voor Dierenkliniek Vossenhof (Vossenhof 46, 6534 VH Nijmegen — Hatert). Gemaakt voor cold-outreach pitching; nog niet besteld door de kliniek.

---

## Status: PROSPECT MOCKUP (niet verkocht)

- Gekloond van `websites/vet-clinics/dierenkliniek-pijnappel/` via de `vet-clinic-template` skill (one-prompt spin-up workflow)
- Pijnappel's Higgsfield-animaties zijn **hergebruikt** (Pixar story in hero, watercolor + LEGO variants in `/images/`) — geen nieuwe credits gespendeerd
- Echte clinic content (logo, team, openingstijden detail) is **placeholder of nog te verifiëren**

---

## Verified facts (uit prospects.csv / WebSearch)

| Veld | Waarde | Bron |
|---|---|---|
| Naam | Dierenkliniek Vossenhof | OSM + meerdere directories |
| Adres | Vossenhof 46, 6534 VH Nijmegen | OSM + Telefoonboek + Zooplus |
| Wijk | Hatert | Opendi (vermelding "Dierenartsenpraktijk Hatert") |
| Telefoon | 024-3559351 | Telefoonboek + Opendi |
| Eigen website | Geen — alleen directory-listings | WebSearch verified |

## Placeholders (te bevestigen indien prospect converteert)

| Veld | Huidige waarde | Te doen |
|---|---|---|
| Email | `info@dierenkliniekvossenhof.nl` | Vragen aan kliniek (mogelijk hebben ze er geen) |
| Openingstijden | Ma-vr 9:00-17:00 (Pijnappel's tijden) | Bevestigen — kan afwijken |
| Team-pagina | Generic placeholder ("kennismaking bij eerste bezoek") | Echte foto's + namen wanneer ze tekenen |
| Logo | Text-wordmark in Fraunces serif | Echte logo vervangen indien beschikbaar |
| Specialiteiten | 5 vakgebieden van Pijnappel | Bevestigen welke Vossenhof écht doet |
| Mission quote | "Samen sterk voor dier én mens" (van Pijnappel) | Vossenhof's eigen waarden indien beschikbaar |
| Spoed-info | Generiek "voicemail verwijst door" | Bevestigen of dit bij Vossenhof zo werkt |

---

## Pitch-angle voor cold outreach

Dierenkliniek Vossenhof heeft **geen eigen website**, alleen verspreide vermeldingen op directory-sites (Zooplus, Opendi, Telefoonboek, Tipaw, etc.). Klanten die zoeken naar "Dierenkliniek Vossenhof Nijmegen" zien een hoop verschillende half-correcte info, maar geen centrale plek waar de kliniek zelf zijn verhaal vertelt.

**Concrete pitch-punten:**
- Eén plek waar mensen jullie diensten, team en openingstijden vinden — i.p.v. dat ze 5 verschillende sites moeten doorzoeken
- Telefonisch boeken werkt prima — geen ingewikkeld systeem nodig
- Mobiel-friendly, snel laadt, eigen domein (`dierenkliniekvossenhof.nl` is waarschijnlijk vrij)
- Live demo is al klaar — ze kunnen 'm vandaag bekijken
- Korte Pixar-animatie als hero (placeholder; krijgen ze gepersonaliseerde versie bij oplevering)

---

## Stack

- Pure HTML + Tailwind CDN
- Google Fonts: Fraunces (display) + DM Sans (body)
- GSAP + Lenis voor reveals + smooth scroll
- 4 pagina's: `index.html`, `specialiteiten.html`, `team.html`, `contact.html`
- Vercel-ready (`cleanUrls: true`)

## Lokaal bekijken

```bash
cd "/Users/giuseppegeukes/Website Klanten Projecten/dierenkliniek-vossenhof"
python3 -m http.server 8000
open http://localhost:8000/
```

## Deployen

```bash
vercel --prod --yes
```

## Mocht de kliniek converteren

1. Vraag verified facts uit (echte team, email, openingstijden, specialiteiten, eventueel eigen mission)
2. Genereer een client-specifieke Higgsfield-animatie (via `higgsfield-ai-animations` skill) met hun eigen brand-kleuren
3. Werk team.html uit met echte mensen + foto's
4. Vervang text-wordmark met echt logo
5. Update spoed-info met hun specifieke doorverwijzing
6. Configureer eigen domein in Vercel
