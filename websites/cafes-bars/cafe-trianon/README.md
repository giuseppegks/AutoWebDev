# Café Trianon — website

Static 4-page site geadapteerd van de Billy's Coffee blueprint. Stage-navy + amber spotlight palet. Pure HTML/CSS/JS — geen backend.

## Pagina's

- `index.html` — Home (hero + intro + **agenda-sectie** + photostrip + de plek + zaalhuur banner + footer CTA)
- `menu.html` — Lunchkaart (broodjes, salades, koffie/thee, borrel/bier)
- `over.html` — Geschiedenis 1910–heden (Buitenlust → Trianon → dansavonden → nu)
- `contact.html` — Adres, openingstijden, mailto-form, Google Maps embed

## PLACEHOLDERs (te vervangen door klant)

**Foto's** — alle `images/billys-*.jpg`, `lunch.jpg`, `hangovertosti.jpg`, `vierkant-*.jpg`, `foto-04.jpg` zijn Billy's Coffee blueprint-foto's. Vervang door eigen foto's van Trianon (interieur Art Nouveau-zaal, podium, lunchgerechten, concertsfeer).

**Agenda-events** op `index.html#agenda` — vier dummy-events (Monday Jazz 21/05, Jam Session 24/05, Tribute 31/05, Trianon-debat 07/06). Vervang door actuele programmering of koppel aan Facebook/Songkick feed.

**Menu-prijzen** in `menu.html` — alle prijzen `€ —`. Gerechtnamen zijn aannames op basis van "ongecompliceerd, smaakvol, wereldinvloeden" — bevestig met de keuken.

**Logo** `images/trianon-logo.svg` — SVG tekstlogo. Vervang door officieel logo wanneer beschikbaar.

## Geverifieerde data (uit research)

- Adres: Berg en Dalseweg 33, 6522 BA Nijmegen *(brief; cross-check: openbare bronnen geven ook 6521 BA — brief-waarde gehanteerd)*
- Tel: 024 322 9189 · Mail: info@trianonnijmegen.nl
- Lunch: ma–vr 11:30–14:30, weekend 13:00–16:00
- Pand: 1910 ontworpen door P.G. Buskens voor Phoenix-brouwerij, rijksmonument 522989
- Vroegere namen: café Buitenlust, café Cornelissen
- 1989–1999 dansavonden + bands in de kelder
- Twee zalen: tussenzaal (50 pers.) + grote zaal (170 pers.) met eigen bar/podium/PA/projector
- Bekend voor: Monday Jazz, jam sessions, tribute-avonden, debatten

## JS gedrag

- `data-today` toont vandaag's lunch-uren in hero
- `data-open-status` badge: "Lunch geopend" tijdens lunchuren, anders "Check de agenda"
- Reservering form opent mailto naar `info@trianonnijmegen.nl`

## Deploy

```
cd cafe-trianon
vercel --prod --yes
```
