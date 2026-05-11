# Sukhothai Thaise Massage — Pitch Demo

Pitch-mockup site for **Sukhothai Thaise Massage** at Javastraat 9, Nijmegen — built from the `premium-spa-template` blueprint. Used for cold walk-in outreach: shop owner sees a polished editorial multi-page demo with their name + address + phone already in place.

**Built:** 2026-05-11 · **Status:** Demoable. Not yet shown to owner.

## Verified facts (safe on this site)

| Field | Value | Source |
|---|---|---|
| Name | Sukhothai Thaise Massage | Goudengids |
| Address | Javastraat 9, 6524 LS Nijmegen | Goudengids |
| Phone | +31 6 29 408 148 | Goudengids |
| Vertical | Thai massage (traditional, hot stone, herbal compress) | Inferred from name |

## Placeholder content — verify with owner before launch

- [ ] **Exact opening hours** per day — site currently says "Op afspraak — bel"
- [ ] **Treatment prices** — every treatment shows "Op aanvraag" instead of a number
- [ ] **Full treatment list** — site lists Traditional Thai / Hot Stone / Herbal Compress as the featured 3; `behandelingen.html` carries the full Royal Thai list as a starting menu, owner needs to confirm what they actually offer
- [ ] **Photos** — every image is a Pexels stock photo (`images.pexels.com/photos/...`). Owner should send their real studio + treatment photos
- [ ] **Reviews** — 3 review cards on `index.html` are placeholders (Lisa B. / Tim D. / Sanne K.). Replace with real Google reviews before launch
- [ ] **Email** — not listed; site has no `mailto:` anywhere
- [ ] **Social links** — Facebook / Instagram links are absent. Add if they have accounts
- [ ] **KvK number** — not yet on the site

## Stack & structure

- **Pure HTML + Tailwind CSS** (Play CDN — no build step)
- **GSAP 3 + Lenis** for scroll reveals + smooth scroll
- **Google Fonts:** Cormorant Garamond (display) + Manrope (body) + Noto Serif Thai (accent)
- **Vercel-ready** — `vercel.json` with `cleanUrls: true` + cache + security headers
- 4 pages: `index.html` / `over-ons.html` / `behandelingen.html` / `locaties.html`
- Palette: wine-burgundy + gold (`#1A0E14` + `#D4A55A`) — kept identical to Royal Thai blueprint since it suits the Thai-heritage positioning

## Deploy

```powershell
cd "D:\AntiGravity\AutoWebDev\websites\massage-salons\sukhothai-thaise-massage"
vercel --prod
```

Default subdomain: `sukhothai-thaise-massage.vercel.app`. For a real launch domain, add via Vercel dashboard.

## What changed vs the Royal Thai template

- Brand name + phone + address swapped to Sukhothai facts (Javastraat 9, 06 29 408 148)
- Locations simplified from 2 (Arnhem + Nijmegen) to **1** (Nijmegen only)
- `locaties.html` rewritten from scratch as a lean single-location page (image grid + practical info + dark Google Maps embed)
- Nav logo image swapped for a serif text wordmark ("Sukhothai")
- Hero copy + about teaser + cadeaubon copy rewritten in Sukhothai's voice (Sukhothai = ancient Thai kingdom, heritage angle)
- Reviews rewritten as clearly placeholder cards labelled by treatment + Nijmegen
- All photos swapped from Royal Thai's WordPress CDN to Pexels stock URLs
- Footer credit: "Site by MG Visuals"

## Pitch angle

Sukhothai has **no website at all** — just a Goudengids listing + phone. The site is the entire pitch:
- "Here's what your business looks like online when someone Googles you tonight"
- "You can keep your phone-only intake — site just sends people to your number"
- "Photos and prices we'll do together once you say yes"
