# Shared template patterns

> Cross-cutting patterns referenced by all template-skills in this repo.
> Each template-skill links to specific sections here instead of duplicating the rules.

This file documents five patterns that apply to **every** static-site template in this repo (barbershop, cafe-bar, coffeeshop, massage-shops, nailstudio, premium-spa, solo-massage-practitioner, vet-clinic). Skim before starting a new build.

---

## 1. Power-design rules (apply before deploy)

These are condensed from `github.com/ItsssssJack/power-design` (20 premium-design principles, originally for presentation decks but apply to static editorial sites).

### Hierarchy & content
- **One idea per section** — section heading is glanceable in ≤3 seconds.
- **3–5 chunks per section** — Miller's cognitive-load research caps at 7±2; aim for 3–5 cards/items.
- **≥ 40 % whitespace ratio** — achieved primarily through generous section padding. See spacing rules below.

### Typography
- **Body ≥ 17 px** on web (≥ 24 px for presentations).
- **Headlines ≥ 40 px** for H1 hero, scaled via `clamp(2.5rem, 6vw, 4.5rem)`.
- **Modular scale 1.25–1.618** — H1 / H2 / H3 step ratios respect a consistent multiplier.
- **Max 4 type sizes per section** — eyebrow + heading + lead + body. Anything more is a smell.
- **Line length ≤ 60ch** for `p` + `.lead`. Headings can run wider.
- **One italic word per heading** via `<em>` in the accent color — works as a visual rest-pause.

### Color
- **WCAG 4.5:1 minimum** for body text on its background. Larger display text can drop to 3:1.
- **60-30-10 distribution** — 60% dominant (cream / dark surface), 30% secondary text, 10% accent (CTAs + kicker + italic).
- **One accent per section** — never mix two accent hues on the same strip.
- **Don't encode meaning by color alone** — pair status-color with icon or text.

### Layout
- **8-point grid** — all spacing tokens are multiples of 4 (4/8/16/24/32/48/64).
- **Proximity rules** — related elements ≤ 16 px apart, unrelated chunks ≥ 48 px apart.
- **Section rhythm**: `--section-y: clamp(4rem, 8vw, 7rem)` = 64–112 px. This is the most common power-design fix when polishing a site — many older templates used `clamp(2.25rem, 4.5vw, 4rem)` which felt cramped on desktop.
- **Data-ink ratio ≥ 80 %** — eliminate decoration that doesn't carry meaning. Cards use 1 px border + hover-state translateY, not drop-shadows.

### Anti-patterns to avoid (AI-cliché smells)
- Excessive gradients (especially diagonal corner-to-corner)
- Arbitrary drop shadows on flat cards
- Bullet-heavy paragraphs
- Generic stock photos that don't match the actual shop
- "Premium" / "luxurious" / "ultimate" copywriting
- Three primary CTAs in one section (max one primary + one ghost)

### Pre-deploy checklist

```
[ ] Body 17px+, line-height 1.6+
[ ] Max 4 type sizes per section
[ ] p + .lead capped at 60ch
[ ] Section padding 64–112 px (clamp(4rem, 8vw, 7rem))
[ ] 60-30-10 color: cream dominant, dark text, single accent
[ ] One accent per section (no caramel + gold mixed)
[ ] Cards use 1px border, no default shadow
[ ] WCAG 4.5:1 on body text
[ ] No bullet-heavy paragraphs (2-3 sentence prose instead)
[ ] No "premium" / "ultimate" copy clichés
[ ] One italic <em> word per heading max
```

---

## 2. Awesome-design-md DESIGN.md format

Format from `github.com/VoltAgent/awesome-design-md`. Every template-skill's reference build should ship a `DESIGN.md` with these **9 sections**:

1. **Visual Theme & Atmosphere** — mood, references, anti-references
2. **Color Palette & Roles** — tokens table + WCAG contrast + 60-30-10 distribution
3. **Typography Rules** — fonts, sizes, italic rule, line-length cap
4. **Component Stylings** — buttons, cards, eyebrow, hero, sections (with hover states)
5. **Layout Principles** — max-width, gutters, 8-point grid, proximity, whitespace target
6. **Depth & Elevation** — shadow scale + rule "borders before shadows"
7. **Do's and Don'ts** — concrete guardrails specific to this shop's identity
8. **Responsive Behavior** — breakpoints, touch targets, mobile-first strategy
9. **Agent Prompt Guide** — ready-to-use prompts for adding new sections / polishing copy

A site without a `DESIGN.md` is incomplete. Every new build copies the blueprint's `DESIGN.md` and customizes per shop (mostly the palette table + Do's/Don'ts).

---

## 3. `.vercel` collision protection (CRITICAL)

> **This bug bit us multiple times in the May 2026 batch build.**

When you `cp -r blueprint-folder new-slug-folder`, the blueprint's `.vercel/project.json` link travels with it. The first time you run `vercel --prod` in the new folder, **Vercel pushes the new content to the blueprint's deployment** — overwriting `<blueprint-slug>.vercel.app` with the new shop's HTML.

### Always do this before the first deploy

```bash
cd websites/<niche>/<new-slug>
rm -rf .vercel    # ← REQUIRED
vercel --prod --yes
```

After the first deploy, Vercel creates a fresh `.vercel/project.json` pointing to `<new-slug>.vercel.app`. Subsequent deploys are safe.

**If you forget and overwrite the blueprint:** redeploy the blueprint immediately from its own folder:

```bash
cd websites/<niche>/<blueprint-slug>
rm -rf .vercel
vercel --prod --yes   # restores <blueprint-slug>.vercel.app
```

Then go back to the new slug and `rm -rf .vercel && vercel --prod --yes` to give it its own project.

---

## 4. Source-palette workflow ("similar but better")

Rather than reusing the blueprint's palette on every site, **derive a refined palette from the shop's existing brand colors** (logo, WordPress theme, Joomla customizer, Divi config, brand assets):

### Step 1 — audit the source-site CSS

```bash
curl -s -L -A "Mozilla/5.0" "<source-url>/" -o /tmp/src.html
grep -oE 'href="[^"]*\.css[^"]*"' /tmp/src.html   # find CSS files

curl -s -L -A "Mozilla/5.0" "<css-url>" -o /tmp/style.css
grep -oE '#[0-9a-fA-F]{3,6}' /tmp/style.css | sort | uniq -c | sort -rn | head -15
```

### Step 2 — identify signature non-default colors

Filter out:
- Framework defaults (WordPress blue `#1982d1`, Divi blue `#2ea3f2`, W3CSS theme colors)
- Pure black/white/grey (`#000`, `#fff`, `#373737`)
- Generic semantic colors (`#dd0000` red, `#22c55e` green, etc.)

What's left is the shop's signature — usually 2–4 distinctive hues.

### Step 3 — refine for accessibility + harmony

"Similar but better" means:
- Same family (don't switch sage → terracotta unless brand-warranted)
- Bump contrast to WCAG AA on the target background
- Reduce saturation slightly for editorial restraint
- Map to the template's `--coffee-dark` / `--caramel` / `--cream` token names

### Verified examples from past batches

| Shop | Source signature | Refined accent |
|---|---|---|
| Edith Libbers | `#629a93` WP custom muted teal | `#5C8784` jade |
| Massages InBalans | `#a8b691` Divi sage | `#6B8A52` deeper sage |
| Kanta Massage | `#cbd18f` + `#e3b448` Simplybook brand | `#A8911E` mustard + `#543636` brown |
| B-KwieK | `#fa9b16` vibrant orange | `#D77E1F` refined amber |
| HomeMas | `#808040` old-school olive | `#7E8B3A` refined olive |
| Café De Beurs | (no website — derived from bruin café tradition) | `#A87434` brass + walnut |
| Café Trianon | (Joomla theme not scrapable) | `#15294F` stage navy + `#D89A3E` amber spotlight |

---

## 5. Pexels photo bank pattern

Most prospect mockups + early-stage client sites don't have professional photography yet. Use thematic Pexels CDN URLs as stand-ins:

### Why Pexels CDN

- **No API key required** for hot-linking. Direct CDN URLs work in any `<img src=>`.
- **Free for commercial use**, no attribution required.
- **Stable URLs** — `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg` doesn't expire.
- **Size variants** via query string: `?auto=compress&cs=tinysrgb&w=1200` for 1200px wide.

### Per-skill photo banks

Each template-skill ships (or will ship) a `pexels-<niche>-bank.json` with curated URLs grouped by theme:

```json
{
  "_meta": { "size_suffix": "?auto=compress&cs=tinysrgb&w=1200" },
  "theme_a": [ "https://images.pexels.com/photos/XXX/pexels-photo-XXX.jpeg", ... ],
  "theme_b": [ ... ]
}
```

### Replacement workflow

```python
import json, re
bank = json.load(open('skills/<niche>-template/pexels-<niche>-bank.json'))
SIZE = "?auto=compress&cs=tinysrgb&w=1200"

# Per site, map blueprint photo paths → themed Pexels URLs
mapping = {
    'images/billys-25.jpg':    bank['theme_a'][0] + SIZE,
    'images/billys-17.jpg':    bank['theme_b'][0] + SIZE,
    # ...
}
for page in ['index.html', 'menu.html', 'over.html', 'contact.html']:
    src = open(f'<slug>/{page}').read()
    for old, new in mapping.items():
        src = src.replace(old, new)
    open(f'<slug>/{page}', 'w').write(src)
```

### Audit duplicate-rate

After the replacement, verify per-page diversity:

```bash
grep -hoE 'src="[^"]+\.(jpg|jpeg|png|webp)"' <slug>/*.html | sort | uniq -c | sort -rn
```

Same photo ≤ 1 occurrence per page is the target. Cross-page repetition is acceptable since visitors see one page at a time.

### Don't replace identity moments

Keep the real practitioner / owner / shop photo in 1–2 strategic spots (hero primary, over-page intro). Stock only fills atmosphere / supporting slots.

---

## 6. Floating "Boek nu" FAB (optional add-on)

For templates with online booking (barbershop, nailstudio, solo-massage), a persistent fixed bottom-right CTA improves conversion on long-scroll pages. Uses the site's accent color automatically via Tailwind's `bg-gold` class.

### Snippet — inject before `</body>` on every page

```html
<!-- ============ FLOATING BOOK CTA ============ -->
<a data-book href="#boeken" aria-label="Boek nu"
   class="cta-gold fixed bottom-5 right-5 sm:bottom-6 sm:right-6 z-40
          inline-flex items-center gap-2 bg-gold text-white
          pl-4 pr-5 py-3 sm:pl-5 sm:pr-6 sm:py-3.5
          rounded-full font-semibold text-sm tracking-wide
          shadow-xl hover:bg-gold-soft hover:-translate-y-0.5 transition-all"
   style="box-shadow: 0 10px 30px -8px rgba(0,0,0,0.25);">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="shrink-0">
    <rect x="3" y="4" width="18" height="18" rx="2"/>
    <path d="M16 2v4M8 2v4M3 10h18"/>
  </svg>
  <span>Boek nu</span>
</a>
```

### Notes

- z-40 keeps it under the booking modal (z-100). Modal overlay covers it automatically.
- `data-book` attribute is intercepted by `js/booking.js` (from `booking-system` skill) to open the modal.
- For non-booking sites (cafe-bar, vet-clinic, coffeeshop), substitute `href` with a `tel:` or `mailto:` link and remove `data-book`.
- Don't add this to single-page sites (barbershop template) — the page is too short to warrant a floating CTA.

---

## 7. Reviews fallback chain

When the shop wants real reviews on their site, follow this order:

1. **Google Maps Places API** — most authentic, but requires a paid API key. The client provides their `GOOGLE_PLACES_API_KEY` as a Vercel env var.
2. **Bron-site recensies page** — many existing WP/Joomla sites have a `/reviews/`, `/recensies/`, `/aanbevolen/` or `/testimonials/` page with real client quotes. Scrape verbatim, add "Recensies overgenomen van [bron]" footnote.
3. **Manual paste** — client emails you 3–6 real testimonials they want shown.
4. **Remove the section entirely** — if none of the above is available, do NOT ship PLACEHOLDER review cards. Remove the section + the "Reviews" nav link. Note in README that the client should provide reviews when they have them.

### What NOT to do

- ❌ Make up reviews ("Een hele fijne ervaring — Sarah, 32") — fabrication
- ❌ Ship 3–6 PLACEHOLDER cards as "we'll fill these in later" — looks unprofessional
- ❌ Embed Google Reviews iframe widgets — locked to Google branding, breaks design

---

## Quick links — per skill, which patterns apply

| Skill | §1 power-design | §2 DESIGN.md | §3 .vercel | §4 source-palette | §5 photo bank | §6 FAB | §7 reviews |
|---|---|---|---|---|---|---|---|
| barbershop-template | ✅ | TODO | ✅ | TODO | TODO | optional | TODO |
| cafe-bar-template | ✅ | ✅ | ✅ | ✅ | ✅ | optional | ✅ |
| coffeeshop-template | ✅ | ✅ | ✅ | ✅ | reuse cafe-bar | n/a (no booking) | link-only |
| massage-shops-template | ✅ | TODO | ✅ | TODO | TODO | n/a (own UI) | TODO |
| nailstudio-template | ✅ | TODO | ✅ | TODO | TODO | optional | ✅ |
| premium-spa-template | ✅ | TODO | ✅ | TODO | TODO | n/a (phone-first) | TODO |
| solo-massage-practitioner-template | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| vet-clinic-template | ✅ | TODO | ✅ | TODO | TODO | n/a (phone-first) | TODO |

"TODO" = skill exists but doesn't yet have a worked example of this pattern. Apply when next polishing.
