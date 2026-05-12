---
name: Premium-Spa-Template
description: Use when spinning up a new massage salon, day spa, or wellness studio website that wants a premium dark-luxury editorial feel — warm wine/burgundy background with gold accents, cream typography, calm pace, no video, phone-first booking. Multi-page (home + about + treatments + locations) with serif display fonts, asymmetric atmosphere galleries, numbered method-cards, multi-duration price-pills per treatment, and dual-location support out of the box. Distinct from `massage-shops-template` (Aurora — video-heavy editorial with masseuse profile modals + request-booking) and from `barbershop-template` (single-page Cal.com calendar). Triggers on phrases like "build a premium massage salon site", "thai spa website", "wellness studio website like Royal Thai", "dark luxury spa template", "multi-page massage salon for [client]", "warm spa site with gold accents".
---

# Premium Spa Template — Spin-Up Workflow

## ⚡ One-prompt spin-up (for `claude --dangerously-skip-permissions` sessions)

When the user pastes a single short prompt like:

> *"Build a massage salon site for **Soyokaze** in **Nijmegen**. Address: **Mariënburg 92, 6511 PS**. Phone: **[verify]**. Vertical: **Japanese head spa**. Bestseller: **kuchi konjac head ritual**."*

…the agent should crank through the whole 4-page build in **one continuous pass**, no checkpoints, no permission prompts. The recipe:

1. **Verify facts in ~30 sec** — single `WebSearch` for the shop name + city. Confirm address, phone, any social handles. If unverified, mark `PLACEHOLDER` in the README and proceed — don't loop.

2. **`cp -r websites/massage-salons/royal-thai-massages websites/massage-salons/<slug>`** — that's the blueprint. Reference build: `websites/massage-salons/sukhothai-thaise-massage` shows what a finished single-location adaptation looks like.

3. **Run the consolidated PowerShell** (template below). It does brand / phone / address / footer-brand / studios-list / social-links / Pexels-photo rotation / Arnhem-removal in one script. Don't do 30 small Edits.

4. **Overwrite `locaties.html`** with the lean single-location template (snippet below). Don't try to regex-delete the Arnhem section from royal-thai's 2-location version — that approach broke last time. Just `Write` a fresh 1-location locaties.html.

5. **Targeted Edits** only for: hero headline (3-line poetic statement in shop's voice), 3 featured-treatment cards (names + descriptions), 3 review cards (placeholder names, shop's bestseller themes), DESIGN.md palette if shifting away from wine/gold.

6. **Rewrite README.md** as shop-specific (use Sukhothai's README at `websites/massage-salons/sukhothai-thaise-massage/README.md` as the template — verified-facts table + placeholder checklist + pitch angle).

7. **Commit + don't push** unless the user explicitly says deploy. `git -C D:/AntiGravity/AutoWebDev add websites/massage-salons/<slug>` and stop.

### Consolidated PowerShell — copy this verbatim, change only the `$cfg` block at top

```powershell
$cfg = @{
  slug       = "soyokaze"   # folder name in websites/massage-salons/
  brandFull  = "Soyokaze"   # display name everywhere
  street     = "Mariënburg 92"
  postcode   = "6511 PS"
  city       = "Nijmegen"
  phoneRaw   = "+316XXXXXXXX"          # tel: link
  phoneDisp  = "06 XX XX XX XX"        # human format
  # Optional palette swap (Japanese sumi+indigo). Leave $null to keep wine/gold.
  paletteSwap = $null
}
$base = "D:\AntiGravity\AutoWebDev\websites\massage-salons\$($cfg.slug)"
$files = @("index.html","over-ons.html","behandelingen.html","locaties.html")

# Pexels stock rotation for every WP CDN URL.
$pexels = @(
  "https://images.pexels.com/photos/3865711/pexels-photo-3865711.jpeg?auto=compress&cs=tinysrgb&w=900",
  "https://images.pexels.com/photos/3997991/pexels-photo-3997991.jpeg?auto=compress&cs=tinysrgb&w=900",
  "https://images.pexels.com/photos/3865792/pexels-photo-3865792.jpeg?auto=compress&cs=tinysrgb&w=900",
  "https://images.pexels.com/photos/3998010/pexels-photo-3998010.jpeg?auto=compress&cs=tinysrgb&w=900",
  "https://images.pexels.com/photos/3865795/pexels-photo-3865795.jpeg?auto=compress&cs=tinysrgb&w=900",
  "https://images.pexels.com/photos/6663537/pexels-photo-6663537.jpeg?auto=compress&cs=tinysrgb&w=900"
)

foreach ($f in $files) {
  $path = Join-Path $base $f
  if (-not (Test-Path $path)) { continue }
  $c = Get-Content $path -Raw -Encoding UTF8
  $idx = 0
  $c = [regex]::Replace($c, 'https://royalthaimassages\.nl/wp-content/uploads/[^"]+', {
    param($m); $url = $pexels[$script:idx % $pexels.Length]; $script:idx++; return $url
  })
  # Brand
  $c = $c.Replace("Royal Thai Massage &amp; Spa", $cfg.brandFull)
  $c = $c.Replace("Royal Thai", $cfg.brandFull)
  # Phone
  $c = $c.Replace("+31246793443", $cfg.phoneRaw)
  $c = $c.Replace("024 679 34 43", $cfg.phoneDisp)
  # Address
  $c = $c.Replace("Bloemerstraat 62", $cfg.street)
  $c = $c.Replace("6511 EL Nijmegen", "$($cfg.postcode) $($cfg.city)")
  # Email
  $c = $c.Replace("info@royalthaimassages.nl", "—")
  $c = $c.Replace("nijmegen@royalthaimassages.nl", "—")
  # Arnhem location <li> in footer
  $c = [regex]::Replace($c, '\s*<li>Steenstraat 61, Arnhem<br/><a href="tel:\+31267601100"[^>]*>026 760 11 00</a></li>', '')
  # 2nd "Bel Arnhem" CTA button
  $c = [regex]::Replace($c, '\s*<a href="tel:\+31267601100"[^>]*>[\s\S]*?Bel Arnhem[\s\S]*?</a>', '')
  # Royal Thai social links → MG Visuals credit
  $c = [regex]::Replace($c, '<div class="flex items-center gap-5">\s*<a href="https://www\.facebook\.com/royalthaimassagearnhem/"[^>]*>Facebook</a>\s*<a href="https://www\.instagram\.com/royal_thai_massages_spa/"[^>]*>Instagram</a>\s*</div>', '<p>Site by MG Visuals</p>')
  # In-text "in Arnhem en Nijmegen"
  $c = $c.Replace(" in Arnhem en Nijmegen", " in $($cfg.city)")
  $c = $c.Replace("Arnhem en Nijmegen", $cfg.city)
  $c = $c.Replace("twee studio's", "één studio")
  $c = $c.Replace("Twee studio's", "Eén studio")
  # Nav-logo img → text wordmark
  $navOld = '<img src="images/royal-thai-logo-light.png" alt="' + $cfg.brandFull + '" class="h-12 lg:h-14 w-auto" />'
  $navNew = '<span class="font-display text-2xl lg:text-[28px] tracking-wide text-ink-primary group-hover:text-gold transition-colors">' + $cfg.brandFull + '</span>'
  $c = $c.Replace($navOld, $navNew)
  # Footer-logo img → text wordmark
  $footerImgOld = '<img src="images/royal-thai-logo-light.png" alt="' + $cfg.brandFull + '" class="h-16 w-auto mb-6" />'
  $footerImgNew = '<div class="font-display text-4xl text-ink-primary mb-2">' + $cfg.brandFull + '</div>'
  $c = $c.Replace($footerImgOld, $footerImgNew)

  Set-Content -Path $path -Value $c -Encoding UTF8 -NoNewline
}

# Sanity sweep — should print 0 for every file
foreach ($f in $files) {
  $hits = (Select-String -Path (Join-Path $base $f) -Pattern "Royal Thai|Arnhem|Steenstraat|royalthaimassages|royal-thai-logo").Count
  Write-Host "$f remaining refs: $hits"
}
```

### Lean `locaties.html` — copy this whole file then swap shop facts

The reference implementation lives at `websites/massage-salons/sukhothai-thaise-massage/locaties.html`. It's a single-location, single-section, dark-map page — way cleaner than royal-thai's 2-location version. Read it, copy it, swap:
- Brand name in nav + footer wordmark
- Street + postcode + city in hero h1 + page title + Maps iframe `src` + footer studio list
- Phone in `tel:` links + display text

That's it. No regex deletion needed.

### Lessons from the Sukhothai production run

- **NEVER use `-SimpleMatch` for compound patterns** in Select-String. It treats `|` as a literal character, so `Pattern "Arnhem|Steenstraat" -SimpleMatch` will silently match nothing and report "0 hits". Use regex mode (the default) for verification sweeps.
- **`<!-- ARNHEM -->[\s\S]*?(?=<!-- NIJMEGEN -->)` regex deletion is brittle.** The lookahead boundary marker may not exist in the file, the comment text might have an extra space, or PowerShell's regex engine may interpret differently than expected. **Just overwrite `locaties.html`** with the lean single-location template — half the lines, no regex risk.
- **PowerShell `@'...'@` heredocs are whitespace-sensitive.** A trailing newline mismatch will silently fail the `.Replace()`. For multi-line replacements, prefer regex with `[regex]::Replace()` or break into smaller single-line replaces.
- **The `Royal Thai` → brand replace can produce awkward Dutch.** `"Bij Royal Thai geloven we"` → `"Bij Soyokaze geloven we"` reads fine; `"de Royal Thai studio's"` → `"de Soyokaze studio's"` reads less so. Spot-check after the bulk replace and rewrite a few sentences in the new brand's voice.
- **Pexels stock IDs** — the 6 in the consolidated PowerShell above are confirmed-working spa/massage photos. Don't guess new IDs without verification.
- **Subagents inherit a restricted permission sandbox.** Don't dispatch agents for site builds unless the user is in `--dangerously-skip-permissions` mode — they get Read/Bash/WebSearch denials and abort cleanly without producing output. Build sequentially in the main thread instead.

## Overview

A reusable, deployable **multi-page** template for premium massage salons, Thai spas, day spas, and wellness studios that want a calm, editorial feel. Distinct from `massage-shops-template` (which is Aurora's video-heavy editorial with masseuse profile modals) and from `barbershop-template` (single-page Cal.com).

**Reference implementation:** [`websites/massage-salons/royal-thai-massages/`](../../websites/massage-salons/royal-thai-massages/) — Royal Thai Massage & Spa (Arnhem + Nijmegen). Live at https://royal-thai-massages.vercel.app.

**Design inspiration:** Pinterest reference (Russian massage salon, dark navy + warm gold) reinterpreted with a Thai/wellness palette, plus MediSpa-style numbered method-cards and "charming atmosphere" gallery patterns from `awesome-design-md`.

## When to Use

Use this skill (instead of `massage-shops-template` or `barbershop-template`) when the salon has:

- A **calm, editorial brand** — Thai spa, Ayurveda studio, Hammam, Day spa — not edgy/erotic
- A **logo with warm tones** (burgundy / wine / terracotta / dark gold) that drives the palette
- A **transparent, structured menu** of named treatments with **multiple durations per treatment** (30/60/90/120 min) where price-per-duration matters
- **Phone or in-person booking** as the preferred channel — no calendar widget, no booking form
- **One or two physical locations** — template is dual-location-ready, easily simplified to single
- Dutch / English / German copy in the same eyebrow + display-serif pattern

| Compared to | Use this when | Use the other when |
|---|---|---|
| `massage-shops-template` (Aurora) | Calm, premium, no masseuse profile modals, no hero video | Editorial with team-grid + per-masseuse modals + ambient video rotator |
| `barbershop-template` | Multi-page with separate treatments + locations + about | Single-page with embedded Cal.com booking |
| `building-local-business-website` | Aesthetic is the priority and you want the canonical multi-page spa shell | You want the generic 4-page workflow without committing to a specific aesthetic |

## Stack (no build step)

- **Pure HTML + Tailwind CSS** (Play CDN — `<script src="https://cdn.tailwindcss.com"></script>`)
- **Google Fonts:** Cormorant Garamond (display serif) + Manrope (body sans) + Noto Serif Thai (decorative, optional)
- **GSAP 3 + ScrollTrigger** (CDN) for fade-in + image-clip reveals
- **Lenis** (CDN) for smooth scroll
- **No npm, no bundler, no React, no build.** Deploy = upload folder.
- **Vercel-ready** out of the box (`vercel.json` with `cleanUrls: true` + cache headers + security headers).

## Architecture (4 pages)

```
{salon-slug}/
├── index.html           # Homepage — Hero + condensed teasers + Reviews + Booking CTA + Footer
├── over-ons.html        # About — Story + 4 numbered method-cards + atmosphere gallery
├── behandelingen.html   # Treatments — Hero with category-pills + all treatments + packages + spa+sauna + cadeaubon
├── locaties.html        # Locations — Per-location: photo grid + opening hours + contact + Maps embed
├── DESIGN.md            # Design tokens + component rules (do not delete — agents read this)
├── README.md            # Per-shop deploy notes + duplication checklist
├── vercel.json          # cleanUrls + security headers + image caching
└── images/              # Local logos + (optionally) downloaded shop photos
    ├── {brand}-logo-light.png    # Cream/light variant for dark backgrounds
    └── {brand}-logo.png          # Dark/burgundy variant (backup, light-bg use)
```

### Why each subpage exists

- **Homepage** is a teaser-driven funnel: each major topic (about / treatments / locations) gets a **compact teaser block + CTA button to its detail page**. Don't put the full content on home — it kills the editorial calm.
- **Over Ons (`over-ons.html`)** carries the brand story, 4-step "our approach" cards, and a "charming atmosphere" gallery. This is where you *earn* trust before the visitor sees prices.
- **Behandelingen (`behandelingen.html`)** is the price/menu page — must list every treatment, every duration, every price. Anchored category-jumps in the page-hero so visitors land on what they want.
- **Locaties (`locaties.html`)** has full opening hours per day, contact methods, transport notes, parking, and Google Maps embed (with the dark-mode CSS filter trick — see Components below).

## Design System (refer to DESIGN.md inside each project)

### Palette — derived from the salon's logo

Always sample the brand colors directly from the logo. The Royal Thai reference uses:

| Token | Hex | Role |
|---|---|---|
| `bg.deep` | `#1A0E14` | Page background — deep wine-black |
| `bg.surface` | `#28161E` | Cards, elevated panels |
| `bg.elevated` | `#371F2A` | Hover state |
| `border.subtle` | `#4A2935` | Dividers, card borders |
| `ink.primary` | `#EFE5D2` | Body text — warm cream (matches logo cream) |
| `ink.muted` | `#B09A82` | Secondary text |
| `gold.DEFAULT` | `#D4A55A` | CTAs, eyebrows, dividers — warm gold from logo accent |
| `gold.soft` | `#A88542` | Hover state |
| `burgundy.DEFAULT` | `#6B1F3B` | Brand secondary (logo letter color) |

**For other brands:** keep the dark-luxury structure (deep + surface + elevated + cream text + 1 accent), but swap the hue to match the logo. Some examples:
- **Balinese spa** → deep teal + copper accent + cream
- **Hammam / Moroccan** → midnight blue + brass + ivory
- **Scandinavian** → near-black + birch-gold + warm white
- **Japanese** → sumi-black + indigo accent + paper-cream

### Typography

- **Display:** Cormorant Garamond (italic 500 for emotional words like "stilte", "rust", "ritueel")
- **Body:** Manrope 400/500/600
- **Eyebrow / kicker:** Manrope 600 uppercase, `tracking: 0.18em`, in gold
- **Stats:** Cormorant Garamond 400, sizes 56-84px in gold

Italics on emotional words inside display headings is the signature move — don't skip it. `Een moment van <em>stilte</em>` reads as branded, `Een moment van stilte` reads generic.

### Built-in components (don't rebuild — copy and adapt)

1. **Sticky transparent → blurred nav** (`#site-nav`) — adds `.nav-scrolled` class after 40px scroll. On subpages, start with `.nav-scrolled` already applied so the nav has contrast above the page-hero.

2. **Light-logo on dark backgrounds** — `<img src="images/{brand}-logo-light.png" class="h-12 lg:h-14 w-auto">` in nav. Always use a **real cream/white logo file** — never apply `filter: invert(1)` to a dark logo (kills anti-aliased edges and any colored accents). If the brand only ships a dark logo, generate a light variant with the Pillow snippet from `building-local-business-website/SKILL.md`.

3. **Hero with image-collage** — text col left + main image right (4:5 aspect, rounded-32) with a smaller secondary image absolutely positioned at `-bottom-8 -left-8` overlapping. Both images get the `.img-vignette` overlay for legibility.

4. **Eyebrow → display heading → body lede pattern** — every section opens with this trio. Eyebrow is the kicker (gold caps), display is the H2 (serif with one italic word), body is the description (muted cream).

5. **Numbered method-cards** (Over Ons "Onze aanpak") — 4 cards in 2x2 grid, each with a **huge background number** in serif. Pattern:
   ```html
   <span class="method-num">1</span>  <!-- absolute, top-right, 180px serif, opacity 0.08 -->
   ```
   Inspired by the MediSpa reference. Drives the "process / ritual" narrative without imagery.

6. **Asymmetric atmosphere gallery** (Over Ons) — `grid-cols-2 lg:grid-cols-4` with mixed `aspect-[3/4]` (row-span-2) and `aspect-square` and `col-span-2 aspect-[4/3]` images. Use `loading="lazy"` on every gallery image. Wrap each in `.reveal-img` for the clip-path slide-in.

7. **Treatment cards with price-pills** — image (4:3) + eyebrow + heading + 1-line description + flex-wrapped `.price-pill` chips, one per duration. Hover: lift 4px + border becomes `gold/40` + image scales 1.05.

8. **Category-pills page-nav** (behandelingen.html hero) — `<a href="#massages">` style pills jumping to in-page anchors. Use `scroll-mt-32` on each anchor target so the sticky nav doesn't cover it.

9. **Cadeaubon strip** — single full-width card with `bg-gradient-to-br from-gold/15 to-gold/5 border border-gold/30`. Goes on home + behandelingen.

10. **Dark Google Maps embed** — wrap iframe and apply CSS filter:
    ```css
    .map-frame {
      filter: invert(0.92) hue-rotate(180deg) saturate(0.7) brightness(0.92);
      border: 0;
    }
    ```
    No API key needed. Looks like a custom dark-mode map.

11. **Pulse "open now" indicator** — small `botanical`-colored dot with `pulse-dot` keyframe, paired with text. The current implementation always says "Nu geopend" — for production, gate it with `new Date().getDay()` + `getHours()` against opening hours so it tells the truth on closed days.

12. **CTA gold pill with shimmer** — `.cta-gold` adds a light gradient sweep on hover (left → right). Use sparingly: max one per viewport.

13. **GSAP reveal patterns** — two classes: `.reveal` (opacity + y28) and `.reveal-img` (clip-path inset). Both gated by `prefers-reduced-motion: reduce` (CSS reset, no JS animation).

14. **Lenis smooth scroll** — included via CDN, uses `requestAnimationFrame`. Disabled if `prefers-reduced-motion`. Calls `ScrollTrigger.update()` on scroll so GSAP triggers fire correctly through the smooth scroller.

## Spin-Up Workflow (per shop)

### 1. Brand inventory (before writing any code)

Use `WebFetch` against the existing site (or socials) to extract:

- **Logo files** — both dark and light variants. Download to `/tmp` first, view with `Read` to confirm transparency + colors.
- **All photos** — gallery, treatment shots, location interior/exterior, reception. List every URL. Don't fabricate, don't pull stock.
- **Treatments** — exact names (in original language + translation if relevant), descriptions, available durations, prices per duration. Capture the pricing matrix exactly.
- **Locations** — full addresses, phone numbers (one per location), email(s), opening hours per day.
- **Social links** — Facebook, Instagram, Google Maps URL.

If the existing site is broken / blocked / 404 on common paths (`/treatments/`, `/services/`), grep the homepage HTML for internal links to discover the real URL pattern (often Dutch-language WP slugs like `/behandelingen/`, `/galerij/`, `/over-ons/`, `/contact/`).

### 2. Confirm scope with the user (briefly)

Default scope = full multi-page (4 pages). Ask only if uncertain about:

- **One location vs two** — adjust locaties.html accordingly. If one, change all "Twee studio's" copy to "Onze studio".
- **Beauty add-ons** (lashes / fillers / mesotherapy) — exclude by default unless the brand leads with them. They clash with the calm-spa positioning.
- **Reviews approach** — placeholder vs Google Places API vs scraped quotes. **Default to placeholder + flag in README** so the user verifies before launch.

### 3. Copy the template

```bash
cp -r websites/massage-salons/royal-thai-massages websites/massage-salons/{salon-slug}
cd websites/massage-salons/{salon-slug}
```

### 4. Customize palette (DESIGN.md + Tailwind config + body bg)

Replace the 9 color tokens in **all 4 HTML files** (search-replace across `tailwind.config.colors`, body `background:`, `.nav-scrolled` rgba, `.img-vignette` rgba, `.price-pill` colors, `::selection`, leaf-deco `fill="..."`). Update `DESIGN.md` palette table.

If you keep the same dark-wine+gold palette, no color changes needed.

### 5. Replace content (search-replace across all 4 HTML files)

In a single project-wide search:

- `Royal Thai Massage &amp; Spa` → `{Salon Name}`
- `+31246793443`, `+31267601100` → new phone numbers
- `info@royalthaimassages.nl`, `nijmegen@...` → new email(s)
- `Steenstraat 61, 6828 CD Arnhem`, `Bloemerstraat 62, 6511 EL Nijmegen` → new addresses
- All `https://royalthaimassages.nl/wp-content/uploads/...` → new image URLs (or `/images/...` if downloaded locally)
- Hero copy + about copy + 4 method-cards: rewrite to match new tone of voice
- Treatments: replace 12 cards with the new salon's menu (delete cards if fewer, copy-paste an existing card if more)
- Packages: same
- Reviews: replace 3 placeholder quotes with real ones (or add a "TODO" comment if not yet collected)

### 6. Logo

Drop the new salon's logo files into `images/`:
- `{brand}-logo-light.png` — required (used in nav + footer)
- `{brand}-logo.png` — backup (light-bg use cases)

If the brand only ships a dark logo, generate the light variant — see `building-local-business-website/SKILL.md` "Logo on dark backgrounds" for the Pillow snippet.

### 7. Test locally

```bash
python3 -m http.server 8000
open http://localhost:8000/
```

Click through every nav link. Verify:
- All 4 pages load
- Logo shows in nav + footer
- Treatment images all load (no broken-image icons)
- Maps embeds render (and have the dark filter applied)
- Mobile drawer opens/closes
- Reveals animate on scroll
- "Open now" indicator shows correct state (or note this for production gating)

### 8. Deploy to Vercel

From the project folder:
```bash
vercel --prod --yes
```

First deploy creates the project. Default subdomain = `{folder-name}.vercel.app`.

For custom domain: `vercel domains add {domain}.com` then follow DNS prompts. Or do it via the dashboard.

### 9. Verify the live deploy

```bash
for page in "" over-ons behandelingen locaties; do
  echo "/$page → $(curl -s -o /dev/null -w '%{http_code}' https://{slug}.vercel.app/$page)"
done
```

All 4 should return 200. Clean URLs work because of `cleanUrls: true` in `vercel.json`.

### 10. Git-connect for future auto-deploy (optional)

If the project lives in a monorepo (like AutoWebDev), connect Vercel to the GitHub repo with **root directory = path to this folder** (e.g., `websites/massage-salons/{salon-slug}`). Then `git push` → auto-deploy.

## ⚠️ Verify-before-launch checklist

Echoing the `building-local-business-website` skill's most important rule: **don't fabricate facts**. Before going live with the real client:

- [ ] **Reviews** — every quote in the reviews section is verifiable against a Google review or written client testimonial. Default placeholders (e.g., "Sophie M.", "Mark & Lieke") MUST be replaced.
- [ ] **Stats** (years of experience, number of treatments, etc.) — confirmed with the owner.
- [ ] **Phone numbers** in `tel:` links match the displayed numbers and actually ring through.
- [ ] **Email addresses** exist (test by sending a real email).
- [ ] **Opening hours** are accurate per day, including holiday closures if applicable.
- [ ] **Photos** are downloaded to `/images/` (don't depend on the old WordPress CDN — when they migrate, the photos vanish).
- [ ] **"Open now" badge** is gated by real opening hours via JS, not always-on.
- [ ] **Cadeaubon CTA** links to actual gift-card flow (online shop or "request via mail"), not just `#boeken`.

## Roadmap / known gaps in the Royal Thai reference build

- Photos are still loaded from `royalthaimassages.nl/wp-content/uploads/...` (WordPress CDN) — should be downloaded to `/images/` for production resilience and conversion to WebP.
- Reviews are placeholder quotes — see "Verify-before-launch" above.
- "Open now" indicator is hardcoded — needs JS gate.
- No FAQ page yet — basics are in `locaties.html` "Goed om te weten" but a full FAQ would help (parking, payment, attire, what to bring).
- No English variant — pattern would be `/en/index.html`, `/en/over-ons.html` etc.
- No Schema.org structured data — adding `LocalBusiness` + `MassageTherapy` JSON-LD would boost local SEO.
- Nav + footer are duplicated across 4 HTML files — extracting to a shared JS-include or moving to a SSG (Astro / 11ty) becomes worth it once the template grows past 6 pages.

---

## Cross-cutting patterns

This template uses (or should use, when polishing) the shared patterns documented in [`../_shared-template-patterns.md`](../_shared-template-patterns.md). Skim that file when starting a new build for:

1. **Power-design rules** — ≥40% whitespace, 60-30-10 color, max 4 type sizes, borders-first cards, anti-pattern checklist
2. **Awesome-design-md DESIGN.md format** — 9 mandatory sections (Visual Theme, Color, Typography, Components, Layout, Depth, Do/Dont, Responsive, Agent Prompt Guide)
3. **`.vercel` collision protection** — always `rm -rf .vercel` before first `vercel --prod` in a copied folder
4. **Source-palette workflow** — derive "similar but better" palette from the bron-site CSS instead of reusing the blueprint default
5. **Pexels photo bank** — see `pexels-<niche>-bank.json` next to this SKILL.md, hot-link without API key
6. **Floating "Boek nu" FAB** — snippet for templates with online booking
7. **Reviews fallback chain** — Google Places API → bron-site → manual → remove section (never PLACEHOLDER cards)

See the quick-links table at the bottom of `_shared-template-patterns.md` to find which patterns specifically apply to this template.

