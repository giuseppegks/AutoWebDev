---
name: Building-Local-Business-Website
description: Use when a small local or regional business needs a presentational website — café, restaurant, retail, salon, gym, or service provider — with no e-commerce checkout, no CMS, and no user accounts.
---

# Building a Local Business Website

## Overview

Repeatable workflow for shipping a static, accessible, brand-aligned 4-page site for a small local business. **Core principle: inventory before invention.** Verify every fact before it touches the page.

## When to Use

- Local business needs a fresh marketing site (4–5 pages max)
- Existing logo and photos available somewhere (their old site, IG, FB)
- No CMS, no checkout, no auth, no database needed
- Static hosting acceptable (Vercel, Netlify, GitHub Pages, plain webhost)

**Skip when:** auth required, e-commerce checkout, dashboards, >10 pages, or non-technical staff need to update content regularly.

## Workflow

### 1. Inventory the brand (before anything else)

WebFetch + WebSearch these sources:
- Their current website — logo URL, all photos, address, hours, socials, KVK/legal
- Google reviews, Instagram, Facebook
- Local directories and industry guides for verified context (e.g. European Coffee Trip, Eet.nu, Yelp, koffietje.nl)

Download every photo and the logo locally to `images/`. Save real address, hours, owners' names, suppliers, founding date — only what is actually published.

### 2. Verify before writing — non-negotiable

**The biggest failure mode is fabricating facts.** Before writing any copy:

1. List every claim you intend to make
2. Mark each: ✅ verified · ⚠️ plausible · ❌ speculation
3. Drop all ❌. Replace ⚠️ with vague-but-true ("Vraag aan de bar" beats inventing a price)
4. **Show this audit to the user before writing copy** — they catch fabrication faster than you

### 3. Confirm scope with the user

Ask explicitly before writing one line of code:
- Which pages? (default: Home / Menu·Services / About / Contact)
- Backend allowed? (default: **no — mailto only**)
- Which business quirks are worth highlighting? (e.g. "no laptop weekend", "appointment only", "closed during August")
- Language? (match the business region — NL, EN, DE, FR)

### 4. Generate the design system

Use `/ui-ux-pro-max` with `--design-system --persist`. Sample exact brand colors directly from their logo or palette image (a Python `zlib` PNG decoder works without dependencies).

**Override the typography suggestion if the vibe mismatches.** A coffee bar is not an Amatic-SC handwritten brand. Cross-check the recommended fonts against the business personality before committing.

Final palette pattern: brand color(s) + cream/paper neutrals + dark for body text. Reserve a contrasting tone (often cream) for italic accents on brand-color backgrounds.

### 5. Generate copy

Use `/copywriting` with the brand inventory + voice notes from step 1. Output everything to one `content/copy.md` so every claim lives in one auditable place.

### 6. Build (pure HTML/CSS/JS)

```
project/
  index.html  menu.html  over.html  contact.html
  css/style.css       (design tokens at top, BEM-style class naming)
  js/main.js          (one file, no dependencies)
  images/             (logo + photos, hosted locally)
  content/copy.md
```

Reusable patterns to include:
- **Sticky header that adapts on home** — `body.home` modifier matches hero color until scrolled
- **Mobile nav drawer** with focus trap, Escape key, body-scroll lock
- **Day-aware "Today's hours" via `new Date().getDay()`** — never hardcode (wrong on closed days)
- **Open/closed status badge** — JS compares current time to hours table
- **Scroll-snap image slider** (no library), prev/next arrows + dots, optional click-to-enlarge lightbox
- **Mailto form via JS-built `mailto:?subject=…&body=…`** — never `<form action="mailto:" method="post">` (unreliable across browsers)
- **Reveal-on-scroll** via IntersectionObserver, respects `prefers-reduced-motion`

### 6b. Logo on dark backgrounds — never use CSS filters

Footers / dark hero bands almost always need a *white* version of the logo. **Do not** use `filter: brightness(0) invert(1)` or `filter: invert(1)` to fake one — it leaves a grey/washed block wherever the source PNG has near-transparent anti-aliased edges or a non-pure-white background, and it kills any colour the logo had.

Always generate a real white variant once and reference it directly:

```python
# scripts/make-white-logo.py — run once when adding the logo
from PIL import Image
src = Image.open("images/logo.png").convert("RGBA")
out = Image.new("RGBA", src.size, (255, 255, 255, 0))
sp, dp = src.load(), out.load()
for y in range(src.size[1]):
    for x in range(src.size[0]):
        r, g, b, a = sp[x, y]
        if a == 0: continue
        dp[x, y] = (255, 255, 255, a)  # repaint visible pixels white, keep alpha
out.save("images/logo-white.png", "PNG", optimize=True)
```

Then in markup: `<img src="images/logo-white.png">` with no filter. Same rule applies to monochrome SVGs — set `fill="currentColor"` and let the parent's `color` decide, or ship two files. **Never** ship a logo on a dark band that you haven't actually viewed in a browser.

### 7. Pre-delivery audit (do not skip)

```bash
# All pages return 200
for p in index menu over contact; do curl -sI "http://127.0.0.1:8000/${p}.html" | head -1; done

# All images load
grep -hoE 'src="images/[^"]+"' *.html | sort -u | sed 's/src="//;s/"//' | xargs -I {} test -f {} && echo OK

# Final fabrication grep
grep -nE "(€[0-9]|[0-9]+ ?gram|vacuüm|binnen een paar uur|verse jus)" *.html
```

Plus visual: mobile (375px), tablet (768px), desktop. WCAG AA contrast on every text colour. Mailto form opens email client with all fields prefilled.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Inventing prices, weights, specific menu items | "Vraag aan de bar" or remove |
| `<form action="mailto:">` POST | JS-built `mailto:?subject=…&body=…` URL |
| Hardcoded "Vandaag open 8:30 — 16:30" | `Date().getDay()` switch including closed days |
| Speculation: "vers gebakken brood", "salades op bestelling" | Only claim what's published |
| Section padding > 5rem feels empty | `clamp(2.25rem, 4.5vw, 4rem)` for `--section-y` |
| Duplicate CSS selectors silently override each other | `grep -n "\.selector"` before adding rule |
| Accepting `/ui-ux-pro-max` typography blindly | Override when vibe mismatches |
| Coding before scope + backend stance confirmed | Confirm pages + backend before writing |
| Insisting on a structural page the client doesn't want | Ask first; remove rather than persuade |
| `filter: brightness(0) invert(1)` on logo in footer/dark hero | Generate a real white PNG variant via PIL (alpha preserved); reference it directly, no filter |

## Defaults (no-decision-needed)

- Stack: HTML + custom-property CSS + vanilla JS, no framework
- Pages: Home / Menu (or Services) / About / Contact
- Form: mailto only — zero backend, zero storage
- Container: 1200px max, narrow variant 880px
- Section padding: `clamp(2.25rem, 4.5vw, 4rem)`
- Hero on home: brand-color background, dark text, optional cream italic accent
- Lang: match business region
- A11y: WCAG AA, focus-visible, reduced-motion respected, semantic HTML

## Red Flags — STOP and verify

- About to write a specific price, weight, or time → did you verify?
- "I'll just put a typical X" → ask the user or remove
- Generic process claims ("vers gebakken", "huisgemaakt brood") → only if confirmed
- Hardcoded today's hours → switch to `Date().getDay()` JS
- `<form action="mailto:" method="post">` → JS-built URL instead
- About to add a backend service (Supabase, Formspree) without explicit user permission
- Logo on dark band rendered with a CSS `filter` instead of a real white asset → swap before shipping

## Honesty Principles (non-negotiable)

1. **Never invent specific facts** — prices, weights, times, founder names, suppliers, dishes
2. **Verify via 2+ sources** for story elements (founding year, owners, partners)
3. **Vague-but-true beats specific-and-fake**
4. **Show the fact audit (✅/⚠️/❌) to the user** before writing copy
5. **No backend means no backend** — mailto + tel only by default; never silently add Supabase/Formspree
