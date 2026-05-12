---
name: Vet-Clinic-Template
description: Use when spinning up a new veterinary clinic / dierenkliniek website that wants a warm, friendly, family-oriented feel — light peach/cream background with indigo CTAs and a brand-red accent. Multi-page (home + specialiteiten + team + contact) with Fraunces display serif + DM Sans body, paw-print decorations, picture-book-style hero animation, team grid with role groupings, and Maps embed. No booking system — phone-first with optional external link to existing online-afspraak page. Re-uses the Pijnappel Pixar story animation across all prospect mockups (cost-saving — only generate fresh animations after a sale closes). Triggers on phrases like "build a vet clinic site", "dierenkliniek website voor [name]", "veterinary clinic for [client]", "warm vet site like Pijnappel", "small animal clinic website", "spin up a vet mockup".
---

# Vet Clinic Template — Spin-Up Workflow

## ⚡ One-prompt spin-up

When the user says something like:

> *"Build a vet clinic mockup for **Dierenkliniek Vossenhof** at **Vossenhof 46, 6534 VH Nijmegen**. Phone: **024-3559351**."*

…run the whole build in one continuous pass, no checkpoints needed:

1. **Verify facts in ~30 sec** — single `WebSearch` for the clinic name + city. Confirm address, phone, opening hours, any social handles. Things to look up: is there a real team list anywhere (Facebook, Google Business)? If unverified, mark `PLACEHOLDER` in the README and proceed.

2. **`cp -r websites/vet-clinics/dierenkliniek-pijnappel websites/vet-clinics/<slug> && rm -rf websites/vet-clinics/<slug>/.vercel`** — that's the blueprint. The Pijnappel build IS the reference implementation; treat its 4 HTML files + `images/` folder as the canonical baseline. **Critical: strip the inherited `.vercel/` project-link folder** — otherwise the first `vercel --prod` deploy will overwrite the Pijnappel production site instead of creating a new project.

3. **CRITICAL: don't regenerate AI animations.** The `images/` folder includes pre-generated Higgsfield assets (`vet-dog-pixar-story.mp4`, `scene-1-pixar.png`, `vet-dog-cartoon-animation.mp4`, `vet-dog-lego-animation.mp4`) that are **reusable across all vet prospects** — they show a generic vet+dog+assistant Pixar narrative that works for any clinic. Only call Higgsfield API when a prospect converts to a paying client. See "Reuse vs regenerate rule" section below.

4. **Run the consolidated bash script** (template below) — handles brand / phone / address / email / booking-link removal / district replacement / Pexels rotation for team photos. One script, not 30 small Edits.

5. **Overwrite `team.html` if the clinic has fewer staff** — most prospects have 4-6 people total, not Pijnappel's 16. Use the lean single-section template (snippet below). Don't try to regex-remove the paraveterinairen + waarnemend sections.

6. **Targeted Edits only for:** hero headline (3-line poetic Dutch in clinic's voice), specialties (some clinics only do small-animal general care, others do equine / exotic / dental specialist work), one-line clinic story for the "over de kliniek" home teaser.

7. **Rewrite README.md** as clinic-specific (verified-facts table + placeholder checklist + pitch angle). Reference Pijnappel's README at `websites/vet-clinics/dierenkliniek-pijnappel/README.md` as the template.

8. **Commit + don't push** unless the user explicitly says deploy.

### Consolidated bash script — change only the `# CONFIG` block

This runs on macOS/zsh (the user's environment). Save as `/tmp/vet-build.sh`, then `bash /tmp/vet-build.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# ============ CONFIG ============
SLUG="dierenkliniek-vossenhof"          # folder name
BRAND="Dierenkliniek Vossenhof"         # display name everywhere
STREET="Vossenhof 46"
POSTCODE="6534 VH"
CITY="Nijmegen"
DISTRICT="Hatert"                       # neighborhood reference, used in copy
PHONE_RAW="+31243559351"                # for tel: links
PHONE_DISP="024 - 355 93 51"            # human format
EMAIL="info@dierenkliniekvossenhof.nl"  # placeholder if unknown — use the format
# ============ /CONFIG ============

REPO="/tmp/AutoWebDev-deploy"   # adjust to your local AutoWebDev clone
BASE="$REPO/websites/vet-clinics/$SLUG"
FILES=("index.html" "specialiteiten.html" "team.html" "contact.html")

# Optional Pexels stock for team photos when the clinic's real photos aren't available.
# These are verified vet/pet stock images that read as warm + clinical.
PEXELS=(
  "https://images.pexels.com/photos/6235241/pexels-photo-6235241.jpeg?auto=compress&cs=tinysrgb&w=900"
  "https://images.pexels.com/photos/6235651/pexels-photo-6235651.jpeg?auto=compress&cs=tinysrgb&w=900"
  "https://images.pexels.com/photos/6235236/pexels-photo-6235236.jpeg?auto=compress&cs=tinysrgb&w=900"
  "https://images.pexels.com/photos/6235112/pexels-photo-6235112.jpeg?auto=compress&cs=tinysrgb&w=900"
  "https://images.pexels.com/photos/4426537/pexels-photo-4426537.jpeg?auto=compress&cs=tinysrgb&w=900"
  "https://images.pexels.com/photos/4587959/pexels-photo-4587959.jpeg?auto=compress&cs=tinysrgb&w=900"
)

for f in "${FILES[@]}"; do
  path="$BASE/$f"
  [ -f "$path" ] || continue

  python3 - "$path" "$BRAND" "$STREET" "$POSTCODE" "$CITY" "$DISTRICT" "$PHONE_RAW" "$PHONE_DISP" "$EMAIL" "${PEXELS[@]}" <<'PY'
import sys, re, pathlib
path, BRAND, STREET, POSTCODE, CITY, DISTRICT, PHONE_RAW, PHONE_DISP, EMAIL, *PEXELS = sys.argv[1:]
p = pathlib.Path(path)
c = p.read_text(encoding="utf-8")

# Brand
c = c.replace("Dierenkliniek Pijnappel", BRAND)

# Phone (tel: link uses +31..., display uses formatted)
c = c.replace("+31243230320", PHONE_RAW)
c = c.replace("024 - 323 03 20", PHONE_DISP)
c = c.replace("024-3230320", PHONE_DISP)

# Address
c = c.replace("Sint Annastraat 35", STREET)
c = c.replace("6524 EE Nijmegen", f"{POSTCODE} {CITY}")
c = c.replace("Nijmegen-Oost", f"{CITY}-{DISTRICT}" if DISTRICT else CITY)

# Email
c = c.replace("info@dierenkliniekpijnappel.nl", EMAIL)
c = c.replace("nijmegen@dierenkliniekpijnappel.nl", EMAIL)

# Booking link — replace ALL external afspraak-boeken links with tel: link to phone
c = re.sub(
    r'href="https://dierenkliniekpijnappel\.nl/online-afspraak-boeken"[^>]*target="_blank"[^>]*rel="noopener"',
    f'href="tel:{PHONE_RAW}"',
    c,
)
# Catch any leftover variants
c = c.replace("https://dierenkliniekpijnappel.nl/online-afspraak-boeken", f"tel:{PHONE_RAW}")

# External uitleg-page anchors — Pijnappel has "Lees meer over X" links to
# /kruisband-uitleg, /lasertherapie, /tandheelkunde_uitleg, /kruisbandoperatie
# These pages don't exist for the new clinic. Strip the entire <a>...</a> block.
c = re.sub(
    r'<a\s+href="https://dierenkliniekpijnappel\.nl/(?:kruisband-uitleg|kruisbandoperatie|lasertherapie|tandheelkunde_uitleg|thuisinslapen|gratis-parkeren)"\s+target="_blank"\s+rel="noopener"\s+class="[^"]*"\s*>\s*[^<]*\s*<svg[^>]*>.*?</svg>\s*</a>',
    '',
    c, flags=re.DOTALL
)

# CTA label swap — "Online afspraak boeken" → "Bel voor afspraak" since no booking system
c = c.replace("Online afspraak boeken", "Bel voor afspraak")
c = c.replace("Afspraak maken", "Bel ons")
c = c.replace("Boek online", "Bel ons")
c = c.replace("24/7 boeken →", "Bel direct")
c = c.replace("Reserveer 24/7 een tijdstip dat past", "Bel ons direct")

# Footer "VetPartners" — Pijnappel-specific, remove or replace
c = c.replace("Onderdeel van VetPartners.", "Persoonlijke zorg, dag in dag uit.")
c = c.replace(" · Onderdeel van VetPartners.", "")
c = c.replace(". Onderdeel van VetPartners.", ".")

# Body-copy partial matches the address-replace missed
# "Aan de Sint Annastraat staat een kliniek" → "Aan de {STREET-base} staat een kliniek"
# Extract the street name (without house number) for body-copy substitution
street_base = STREET.split()[0] if STREET else "ons adres"
c = c.replace("Aan de Sint Annastraat staat", f"Aan de {street_base} staat")
c = c.replace("We zitten aan de Sint Annastraat", f"We zitten aan de {street_base}")

# Pijnappel-specific landmark — Goffertpark is near Sint Annastraat
# Replace with a generic "in een rustige woonbuurt" or similar
c = c.replace(
    "vlak bij het Goffertpark",
    "in een rustige woonbuurt"
)

# Animal-scope claim — Pijnappel treats honden/katten/konijnen/cavia's/ratten.
# Most prospect clinics only do honden+katten. Trim to be safe (verify per clinic).
c = c.replace(
    "Voor honden, katten, konijnen, cavia's en ratten",
    "Voor honden en katten"
)
c = c.replace(
    "Voor honden, katten, konijnen en knaagdieren.",
    "Voor honden en katten."
)
c = c.replace(
    "Honden, katten, konijnen, cavia's, hamsters, ratten en andere kleine huisdieren. Geen exoten of paarden.",
    "Honden en katten. Voor exoten, knaagdieren of paarden verwijzen we door naar gespecialiseerde collega's in de regio."
)
c = c.replace(
    "honden, katten en knaagdieren",
    "honden en katten"
)

# Equipment claims in about-teaser — Pijnappel-specific (eigen OK, in-house lab,
# moderne tandheelkunde-set). Replace with neutral copy that any clinic can claim.
c = c.replace(
    "Met eigen OK, in-house lab en moderne tandheelkunde-set — alles wat we nodig hebben om je huisdier hier ter plekke te helpen.",
    "Een vertrouwd buurtadres met de tijd en aandacht die jouw huisdier verdient."
)

# Team-count phrase — Pijnappel has 16 staff (4 vets + 7 para + 4 waarnemend + stagiaire).
# Smaller clinics have fewer. Replace with neutral phrasing.
c = c.replace(
    "Vier dierenartsen, zeven paraveterinairen en een team waarnemers — verbonden door één gedeelde liefde voor wat ze doen. Bij ons spreek je geen \"nummer\", maar Yvonne, John of Bouke.",
    "Een klein, betrokken team van dierenartsen en assistenten — verbonden door één gedeelde liefde voor wat ze doen. Bij ons spreek je geen \"nummer\", maar mensen die je leert kennen."
)
c = c.replace(
    "Zestien mensen, gedreven door dezelfde liefde voor wat ze doen. Geen \"nummers achter het bureau\" — wel Yvonne aan de balie, John in de OK en Bouke met de röntgenfoto's. Hieronder vind je wie je tegenkomt als je langsloopt.",
    "Een klein, betrokken team van dierenartsen en assistenten. Geen \"nummers achter het bureau\" — wel mensen die je leert kennen bij het eerste bezoek."
)
# Meta description team-count
c = c.replace(
    "vier dierenartsen, zeven paraveterinairen en een team waarnemers — verbonden door één liefde voor diergeneeskunde.",
    "een klein, betrokken team voor honden en katten."
)

# Floating "16+ mensen team" badge — replace with mission-quote variant
# (or removed if team-count isn't a USP for the new clinic)
c = re.sub(
    r'<p class="font-display text-3xl leading-none text-ink-primary">16<span class="text-brand-red">\+</span></p>\s*<p class="text-xs text-ink-muted mt-1">mensen in ons team,<br/>klaar voor je huisdier</p>',
    f'<p class="font-display text-xl leading-none text-ink-primary">Voor je</p>\n            <p class="font-display text-xl leading-none italic text-brand-red mt-1">hond &amp; kat</p>',
    c
)

# Floating "3 specialismen" badge — Pijnappel-specific (laser+kruisband+tand).
# Replace with neutral "Voor hond & kat" focus.
c = re.sub(
    r'<p class="font-display text-4xl leading-none text-ink-primary">3</p>\s*<p class="text-\[10px\] tracking-kicker uppercase text-ink-primary font-semibold mt-1">specialismen</p>',
    '<p class="font-display text-2xl leading-tight text-ink-primary">Voor je</p>\n            <p class="font-display text-2xl leading-tight italic text-brand-red">hond &amp; kat</p>',
    c
)

# Pexels stock rotation for any leftover wp-content URLs (team photos especially)
idx = [0]
def replace_wp(_m):
    url = PEXELS[idx[0] % len(PEXELS)]
    idx[0] += 1
    return url
c = re.sub(r'https://dierenkliniekpijnappel\.nl/wp-content/uploads/[^"]+', replace_wp, c)

# Logo: nav + footer fall back to text wordmark (the clinic may not have a logo file ready)
c = re.sub(
    r'<img src="images/pijnappel-logo\.png" alt="[^"]*" class="h-12 lg:h-14 w-auto" />',
    f'<span class="font-display text-2xl lg:text-[28px] text-ink-primary group-hover:text-indigo transition-colors">{BRAND}</span>',
    c,
)
c = re.sub(
    r'<img src="images/pijnappel-logo\.png" alt="[^"]*" class="h-14 w-auto mb-5" />',
    f'<div class="font-display text-3xl text-ink-primary mb-5">{BRAND}</div>',
    c,
)
c = re.sub(
    r'<link rel="icon" href="images/pijnappel-logo\.png" />',
    '<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 64 64%27%3E%3Cpath fill=%27%23B7242B%27 d=%27M22 26c-3.3 0-6-3.4-6-7.5S18.7 11 22 11s6 3.4 6 7.5S25.3 26 22 26zm20 0c-3.3 0-6-3.4-6-7.5S38.7 11 42 11s6 3.4 6 7.5S45.3 26 42 26zM10 36c-2.8 0-5-2.7-5-6s2.2-6 5-6 5 2.7 5 6-2.2 6-5 6zm44 0c-2.8 0-5-2.7-5-6s2.2-6 5-6 5 2.7 5 6-2.2 6-5 6zM32 30c-7.7 0-14 6.7-14 15 0 4.6 3.4 8 8 8 2.6 0 3.7-1 6-1s3.4 1 6 1c4.6 0 8-3.4 8-8 0-8.3-6.3-15-14-15z%27/%3E%3C/svg%3E" />',
    c,
)

p.write_text(c, encoding="utf-8")
print(f"  ✓ {p.name}")
PY
done

# Sanity sweep — should print 0 references for every file
echo ""
echo "=== Sanity sweep (should be 0 for all) ==="
for f in "${FILES[@]}"; do
  hits=$(grep -cE "Pijnappel|Sint Annastraat|dierenkliniekpijnappel\.nl|pijnappel-logo" "$BASE/$f" 2>/dev/null || echo 0)
  echo "  $f: $hits remaining refs"
done
```

### Specialty-rewrite per clinic-type (CRITICAL fork)

The Pijnappel build advertises **specialist-level** procedures: knieoperaties / lasertherapie / endoscopie / TTA-Rapid surgery. **These are NOT generic vet services** — they require expensive equipment and specialist certification that most small buurtdierenarts clinics don't have. Cloning the Pijnappel build without rewriting these claims = misrepresenting the prospect = embarrassing pitch.

Decide which fork applies BEFORE running the script:

| Clinic type | Approach |
|---|---|
| **Specialist praktijk** (multi-vet, has OK, has laser, performs orthopedic surgery, possibly published prices) | Keep Pijnappel-style 5 specialty detail-sections + advanced service icons |
| **Buurtdierenarts** (small general practice, honden+katten only, no specialist equipment) | Replace 5 specialty sections with general-practice services (default) |

For 90%+ of cold-outreach prospects, the **buurtdierenarts fork** is correct. Use the script below AFTER the consolidated bash script.

#### Buurtdierenarts specialty-rewrite (Python follow-up)

```bash
python3 - "$BASE/specialiteiten.html" "$BASE/index.html" "$PHONE_RAW" "$PHONE_DISP" <<'PY'
import sys, re, pathlib

spec_path, idx_path, PHONE_RAW, PHONE_DISP = sys.argv[1:]

# === specialiteiten.html ===
p = pathlib.Path(spec_path)
c = p.read_text(encoding="utf-8")

# Hero h1 + subtitle
c = c.replace(
    'Waar wij<br/><em class="italic text-brand-red">goed in</em> zijn.',
    'Wat wij<br/><em class="italic text-brand-red">aanbieden.</em>'
)
c = c.replace(
    "Naast algemene zorg en check-ups hebben we ons in een aantal vakgebieden extra gespecialiseerd. Voor sommige ingrepen worden dieren zelfs vanuit andere klinieken naar ons doorverwezen.",
    "Algemene zorg voor honden en katten — vaccinaties, sterilisatie, tand- en mondzorg en kleine operaties. Voor specialistische ingrepen werken we samen met collega-klinieken in de regio."
)

# Meta description
c = re.sub(
    r'<meta name="description" content="[^"]*Tandheelkunde[^"]*"',
    '<meta name="description" content="Algemene zorg, vaccinaties, sterilisatie & castratie, tand- en mondzorg en kleine operaties voor honden en katten."',
    c
)

# Anchor pills row — 5 new IDs
old_pills_marker = 'href="#algemene-zorg"'
new_pills = '''<a href="#algemene-zorg" class="inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-semibold bg-bg-card border border-border-soft hover:border-indigo hover:text-indigo transition-colors">Algemene zorg</a>
        <a href="#vaccinaties" class="inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-semibold bg-bg-card border border-border-soft hover:border-indigo hover:text-indigo transition-colors">Vaccinaties</a>
        <a href="#sterilisatie" class="inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-semibold bg-bg-card border border-border-soft hover:border-indigo hover:text-indigo transition-colors">Sterilisatie</a>
        <a href="#tandheelkunde" class="inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-semibold bg-bg-card border border-border-soft hover:border-indigo hover:text-indigo transition-colors">Tandheelkunde</a>
        <a href="#operaties" class="inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-semibold bg-bg-card border border-border-soft hover:border-indigo hover:text-indigo transition-colors">Operaties</a>'''
c = re.sub(
    r'<a href="#algemene-zorg"[\s\S]*?>Endoscopie</a>',
    new_pills,
    c
)

# Replace section TANDHEELKUNDE → VACCINATIES, KNIEOPERATIES → STERILISATIE,
# LASERTHERAPIE → TANDHEELKUNDE, ENDOSCOPIE → OPERATIES
# (See full snippet templates in vet-clinic-template skill repo, websites/vet-clinics/dierenkliniek-vossenhof for reference)

# Section 02: was Tandheelkunde, becomes VACCINATIES
SEC_VACCINATIES = '''  <!-- ============ VACCINATIES ============ -->
  <section id="vaccinaties" class="py-16 lg:py-24 bg-bg-card scroll-mt-32">
    <div class="max-w-[1240px] mx-auto px-6 lg:px-12">
      <article class="reveal relative grid lg:grid-cols-12 gap-10 items-center">
        <span class="specialty-num">02</span>
        <div class="lg:col-span-5 lg:order-2 relative">
          <p class="text-[11px] tracking-kicker uppercase text-indigo font-semibold mb-3">Dienst 02</p>
          <h2 class="font-display text-3xl lg:text-5xl leading-tight mb-6">Vaccinaties &amp; <em class="italic text-brand-red">preventie</em></h2>
          <div class="space-y-4 text-ink-muted text-base lg:text-lg leading-relaxed">
            <p>De jaarlijkse vaccinatie is meer dan een prikje — het is het ideale moment voor een algeheel gezondheidschecken.</p>
          </div>
        </div>
        <div class="lg:col-span-7 lg:order-1">
          <div class="reveal-img overflow-hidden rounded-[28px] aspect-[4/3]">
            <img src="https://images.pexels.com/photos/6235651/pexels-photo-6235651.jpeg?auto=compress&cs=tinysrgb&w=900" alt="Vaccinaties" class="w-full h-full object-cover bg-peach-light" loading="lazy" />
          </div>
        </div>
      </article>
    </div>
  </section>

'''
c = re.sub(
    r'  <!-- ============ TANDHEELKUNDE ============ -->.*?(?=  <!-- ============ KNIEOPERATIES ============ -->)',
    SEC_VACCINATIES, c, flags=re.DOTALL
)

# … and so on for STERILISATIE / TANDHEELKUNDE (rewrite) / OPERATIES sections.
# Full templates: see websites/vet-clinics/dierenkliniek-vossenhof/specialiteiten.html
# for the reference structure.

p.write_text(c, encoding="utf-8")

# === index.html service-icons ===
# 5 icons: Algemene zorg / Vaccinaties / Sterilisatie / Tandheelkunde / Operaties
# Each with: anchor link to the new section ID + appropriate SVG icon + label
# See websites/vet-clinics/dierenkliniek-vossenhof/index.html lines 337-377 for the snippet
print("✓ specialiteiten.html rewritten for buurtdierenarts services")
print("⚠️  Manual step: verify index.html service-icons row matches new section IDs")
PY
```

**Reference implementation:** the complete buurtdierenarts rewrite is in `websites/vet-clinics/dierenkliniek-vossenhof/specialiteiten.html` and `index.html` — copy section blocks from there rather than maintaining them inline in this skill. Saves churn when service-icon icons change.

#### Specialty-icon SVG paths (Lucide-derived, 24×24 viewBox)

For the 5 buurtdierenarts services in `index.html`:

| Service | Anchor | SVG path |
|---|---|---|
| Algemene zorg | `#algemene-zorg` | Heart: `M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z` |
| Vaccinaties | `#vaccinaties` | Syringe (custom): `M16 6l-8 8 4 4 8-8M11 9l-3-3-3 3 3 3M14 12l4 4M9 19a2 2 0 11-2-2` |
| Sterilisatie | `#sterilisatie` | Cross/medical: `M12 2v8m0 0a5 5 0 105 5h-5V10zM6 16l-2 2M18 16l2 2` |
| Tandheelkunde | `#tandheelkunde` | Tooth: `M12 2C8 2 6 4 6 7c0 3 1 4 1 7 0 4 1 8 3 8s2-3 2-5 1-3 2-3 0 0 0 0 0 1 0 3 0 5 2 5 3-4 3-8c0-3 1-4 1-7 0-3-2-5-6-5h-2z` |
| Operaties | `#operaties` | Scalpel: `M14.7 6.3l3 3M5 19l9-9 3 3-9 9H5v-3zM18 5l1.5 1.5` |

### Lean `team.html` for small clinics

Pijnappel's `team.html` has 16 people in 3 sections (dierenartsen / paraveterinairen / waarnemend). Most prospects have 4-6 people total. **Don't try to regex-delete sections** — overwrite `team.html` with this lean structure:

- Single page-hero
- One "Ons team" section with 4-6 cards in a 2-3 col grid
- Partnerships strip (KNMVD / LICG / WVT if applicable) — keep or remove based on whether the clinic is a member

Open Pijnappel's `team.html`, copy the head/nav/footer, replace the body with a simpler single-section. If you don't have the team list yet, use Pexels portraits + name="Naam {N}" + role="Dierenarts" placeholders + flag in README.

### Lessons learned (from Pijnappel + future builds)

- **Scrape the FULL sitemap, not just homepage + 4 obvious pages.** The biggest content-extraction miss on the first Pijnappel pass: we WebFetched home/team/services/contact/about and stopped. The site has **7 more pages** with major USPs — `/thuisinslapen` (home euthanasia), `/kruisband-uitleg` (1000+ words + TTA-Rapid surgeon credential — only 34 worldwide), `/lasertherapie` (€32.50 published price + 15 indications), `/tandheelkunde_uitleg` (specialism since 1995 + 13 dental photos), `/gratis-parkeren` (license-plate auto-system). **Always start with `sitemap_index.xml` and pull every page.** See the sitemap-first scrape recipe in step 1 of the workflow.
- **Vet clinics often publish prices.** Pijnappel surfaces €1.975 for kniekirurgie and €32.50/laser session publicly. **Surface this in the prospect build** — pricing transparency is a strong differentiator vs. "vraag bij de balie".
- **Look for specialist credentials.** Pijnappel's John J.L. Pijnappel is 1 of 34 TTA-Rapid surgeons worldwide (3 in NL since 2013). These credentials are buried in `*uitleg*` pages but are massive credibility for the build's "expertise" sections.
- **Many vet clinics offer home euthanasia.** It's almost never on the main nav but lives as a dedicated page (often `/thuisinslapen`, `/inslapen`, `/euthanasie-thuis`). Worth featuring — emotionally weighty service that customers value.
- **Don't generate fresh AI animations for prospect mockups.** The Pijnappel `vet-dog-pixar-story.mp4` works for ANY vet clinic — vet+dog+assistant is generic enough. Higgsfield Kling pro is ~$1-2 per 5-sec clip; speculative spend burns budget. See "Reuse vs regenerate rule" below.
- **The Pijnappel logo is brand-specific** — replace with text wordmark (Fraunces serif, 28px) for prospects without a logo. The script does this automatically.
- **Booking-link substitution must catch both the URL and the CTA label.** A `<a href="...online-afspraak-boeken" target="_blank">` without label substitution leaves "Boek online" buttons that link to phone. The consolidated script handles both.
- **"Onderdeel van VetPartners"** is Pijnappel-specific. Most other clinics aren't part of that network — remove or replace with generic line.
- **Team-page placeholders should look intentional.** Avoid generic stock smiles — use mid-pose pet-handling photos so it reads as "team in action" rather than "we used stock". The Pexels IDs in the script are chosen for that.
- **Image count sanity check.** A typical Dutch vet clinic has 30-60 unique images in their WP uploads (team portraits + interior + diagrams for any specialism pages). If your scrape returns <15, you missed pages — re-check the sitemap.
- **Reference content archive:** Pijnappel's complete archive lives at `/Users/giuseppegeukes/Website Klanten Projecten/pijnappel-content/` — 49 images + 12 HTML pages + `CONTENT-INVENTORY.md` summary. Use as a template for building per-clinic content archives BEFORE writing copy.

## Overview

A reusable, deployable **multi-page** template for veterinary clinics that want a warm, friendly, family-vet feel. Models the PetsLife (Russian vet clinic) Pinterest reference: light peach background + indigo CTAs + paw-print decorations + cartoon hero animation.

**Reference implementation:** [`websites/vet-clinics/dierenkliniek-pijnappel/`](../../websites/vet-clinics/dierenkliniek-pijnappel/) — Dierenkliniek Pijnappel (Sint Annastraat, Nijmegen). Live at https://dierenkliniek-pijnappel.vercel.app.

**Design inspiration:** PetsLife Pinterest reference (peach + indigo + paw decorations) + Pixar-style animated hero (generated via `higgsfield-ai-animations` skill, reused across all vet prospects).

## When to Use

| Use this when | Use the other |
|---|---|
| Small-animal vet clinic (honden, katten, knaagdieren) — gezinsvriendelijke vibe | `premium-spa-template` for adult-only/luxury services with dark editorial feel |
| 1 location, 4-16 team members | Single-page sites — this is multi-page by design |
| No real-time booking — phone-first with optional external afspraak link | `barbershop-template` for clinics that DO have Cal.com or Salonized integration |
| Warm light palette (peach + indigo + brand-red accent) | When the brand demands a dark luxury feel |
| Pinterest reference: PetsLife or similar cartoon/illustration-heavy vet sites | Hyper-clinical / hospital-grade sites with sterile blue/white aesthetic |

## Stack (no build step)

- **Pure HTML + Tailwind CSS** (Play CDN — `<script src="https://cdn.tailwindcss.com"></script>`)
- **Google Fonts:** Fraunces (display serif, variable) + DM Sans (body)
- **GSAP 3 + ScrollTrigger** (CDN) for reveals
- **Lenis** (CDN) for smooth scroll
- **Inline SVG `<symbol>` for paw prints** — reused across all decoration spots
- **Vercel-ready** with `cleanUrls: true` in `vercel.json`
- **No npm, no bundler, no booking-system JS, no calendar integration.**

## Architecture (4 pages)

```
{vet-slug}/
├── index.html              # Hero with autoplay video + about teaser + 5 service icons + team teaser + indigo CTA + contact strip
├── specialiteiten.html     # 5 vakgebieden in alternating-bg articles (Algemene zorg, Tand, Knie, Laser, Endoscopie)
├── team.html               # Team members (1-3 sections depending on clinic size) + partnerships strip
├── contact.html            # Address card + opening hours table + Maps embed + practical info
├── DESIGN.md               # Design tokens + component rules
├── README.md               # Per-clinic notes, verified facts, placeholder checklist
├── vercel.json             # cleanUrls + security headers + immutable cache on /images/
└── images/
    ├── pijnappel-logo.png              # Replace per-clinic OR remove and use text wordmark
    ├── knmvd.png, licg.png, wvt.jpg    # Partnership logos (keep if applicable)
    ├── vet-dog-pixar-story.mp4         # ⚡ REUSE — generic vet+dog Pixar narrative (14 sec)
    ├── vet-dog-cartoon-animation.mp4   # ⚡ REUSE — watercolor 5-sec loop variant
    ├── vet-dog-lego-animation.mp4      # ⚡ REUSE — LEGO movie 5-sec variant
    ├── scene-1-pixar.png               # ⚡ REUSE — poster for hero video
    ├── scene-2-pixar.png, scene-3-pixar.png    # ⚡ REUSE — individual scene stills
    ├── vet-dog-illustration.png        # ⚡ REUSE — watercolor still
    └── vet-dog-lego-illustration.png   # ⚡ REUSE — LEGO still
```

## Reuse vs regenerate rule

**Default behavior: REUSE all AI-generated assets in `images/`.**

The Pixar story animation (`vet-dog-pixar-story.mp4`) and its companion stills are designed to be generic enough for ANY vet clinic mockup — the scene shows a worried owner, a vet examining with a stethoscope, and a happy resolution. That fits every general-practice clinic.

| Situation | Action |
|---|---|
| Prospect mockup (cold outreach demo) | Copy `images/` as-is — no Higgsfield calls. Total cost: $0. |
| Client signed and paid | Use `higgsfield-ai-animations` skill to generate a fresh client-specific animation (custom team appearance, clinic's actual logo, brand-matched palette). |
| Client explicitly asks "make ours different from Pijnappel" | Generate a fresh variant — different style (LEGO / Ghibli / watercolor) or different scene structure. |

**Why this matters:** Higgsfield Kling-pro costs ~$1-2 per 5-sec clip. A 3-scene narrative = ~$5-8. Across 10 prospect mockups that's $50-80 in pure speculation. Reuse keeps prospect-pipeline costs at $0 and reserves the Higgsfield budget for converted clients only.

## Design System (refer to DESIGN.md inside each project)

### Palette — light peach + indigo + brand-red

Default tokens (Pijnappel build, works for ~80% of vet clinics):

| Token | Hex | Role |
|---|---|---|
| `bg.base` | `#F7E8D6` | Page background — warm peach |
| `bg.card` | `#FFFFFF` | Cards, elevated panels |
| `bg.soft` | `#FCF1E2` | Subtle alt-section background |
| `bg.cta` | `#5B47F0` | Indigo CTA block background |
| `indigo.DEFAULT` | `#5B47F0` | Primary CTA, links, focus states |
| `indigo.deep` | `#4839C7` | Hover state on indigo |
| `peach.DEFAULT` | `#F0B98E` | Circle backgrounds behind images, paw decorations |
| `peach.light` | `#F8D9BB` | Subtle peach for badges |
| `brand.red` | `#B7242B` | Clinic's brand-color accent (sampled from logo). For Pijnappel = red |
| `ink.primary` | `#2A1F1A` | Body text — warm dark brown-black |
| `ink.muted` | `#6B5D54` | Secondary text |
| `border.soft` | `#EBD9C0` | Card borders, dividers |

**For other clinics:** keep peach + indigo + cream structure. Swap `brand.red` to match the clinic's logo accent — e.g.:
- Logo with green → swap brand-red to `#3A7D44`
- Logo with blue → swap to `#1E5F8B`
- Logo with terracotta → keep red but warmer `#C45131`

### Typography
- **Display:** Fraunces (italic 500 on emotional words — "trouwe vriend", "altijd", "zorg")
- **Body:** DM Sans 400/500/600
- **Eyebrow:** DM Sans 600 uppercase tracking 0.14em in indigo

### Built-in components (don't rebuild)

1. **Sticky transparent → blurred-peach nav** with `.nav-scrolled` class after 40px scroll
2. **Logo or text wordmark** — text fallback when no logo file
3. **Hero with autoplay video + floating quote card** — Pixar story autoplays muted-looped in a 16:9 rounded container
4. **Decorative paw-cluster** in empty hero space (9 paws at varied sizes/rotations/colors)
5. **Service-icon row** — 5 services in pill-cards with peach-light icon containers
6. **Team member cards** — photo in `aspect-[4/5]` peach-bg container, name + role below, hover lift
7. **Partnerships strip** — KNMVD / LICG / WVT logos in equal-width cards (keep if clinic is member, remove otherwise)
8. **Indigo CTA block** — full-width gradient indigo card with paw decorations, white CTA buttons inside
9. **Light Maps embed** — minimal CSS filter `filter: saturate(0.85) hue-rotate(-10deg)` to warm up the embed
10. **Inline SVG `<symbol id="paw">`** — single source of truth for all paw decoration instances
11. **GSAP `.reveal` + `.reveal-img`** — same pattern as premium-spa-template; gated by `prefers-reduced-motion`
12. **Mission quote badge** — floating card with quote + "ONZE BELOFTE" kicker, positioned bottom-right of hero video

## Spin-Up Workflow (detailed)

### 1. Brand inventory — go DEEP, not just homepage

**Critical lesson from the Pijnappel build:** Don't WebFetch only the homepage + the obvious 4 pages (team / services / about / contact). Vet clinic sites consistently have **5-7 hidden detail-pages** with major USPs that the homepage doesn't surface. Pijnappel had a `/thuisinslapen` (home euthanasia) page, three uitleg-pages (`kruisband-uitleg`, `lasertherapie`, `tandheelkunde_uitleg`), and a parkeer-systeem page — none discoverable from the homepage menu.

**Always start with the sitemap.** WordPress sites (which is ~90% of Dutch vet clinics) auto-publish their full sitemap at `sitemap_index.xml`.

#### Sitemap-first scrape recipe

```bash
DOMAIN="https://dierenkliniekpijnappel.nl"  # adjust per client
DEST="/Users/{you}/Website Klanten Projecten/{clinic-slug}-content"
mkdir -p "$DEST/images" "$DEST/copy"

# 1. Get all pages from sitemap
/usr/bin/curl -sL "$DOMAIN/page-sitemap.xml" \
  | grep -oE '<loc>[^<]+</loc>' \
  | sed 's|<[^>]*>||g' \
  | tee "$DEST/pages.txt"

# 2. Fetch every page's raw HTML
> "$DEST/all-raw.html"
while read url; do
  /usr/bin/curl -sL "$url" >> "$DEST/all-raw.html"
  fname=$(basename "$url")
  /usr/bin/curl -sL "$url" -o "$DEST/copy/${fname:-home}.html"
done < "$DEST/pages.txt"

# 3. Extract all image URLs (dedupe + strip srcset variants)
grep -oE "$DOMAIN/wp-content/uploads/[^\"]+\.(jpg|jpeg|png|webp|svg)" "$DEST/all-raw.html" \
  | python3 -c "
import re, sys
seen = set()
for line in sys.stdin:
    for url in re.split(r'[\s,]+', line.strip()):
        # Normalize size variants — keep full-res only
        base = re.sub(r'-\d+x\d+(\.[a-z]+)$', r'\1', url)
        if base.startswith('http') and base not in seen:
            seen.add(base)
            print(base)
" > "$DEST/images.txt"

# 4. Download all images
cd "$DEST/images"
while read url; do
  fname=$(basename "$url")
  [ -f "$fname" ] || /usr/bin/curl -sL "$url" -o "$fname"
done < "$DEST/images.txt"

echo "✓ Archived $(wc -l < $DEST/pages.txt) pages, $(ls "$DEST/images" | wc -l) images"
```

This takes ~30 seconds per clinic and gives you a complete content archive locally.

#### What to look for in the scraped content (per page-type)

| Page slug | What it might hold | Why it matters |
|---|---|---|
| `*uitleg*`, `*detail*`, `*meer*` | 1000+ word condition-explainer pages | Specialism credibility — surgeon certifications, technique names |
| `thuisinslapen`, `euthanasie`, `inslapen` | Home-euthanasia service | Big emotional service many vets quietly offer |
| `tarieven`, `prijzen`, `kosten` | Public pricing | Transparency = USP. Many clinics publish prices |
| `gratis-parkeren`, `parkeren`, `bereikbaarheid` | Access/parking system details | Service-friendliness signal |
| `kruisband*`, `orthopedie*`, `chirurgie*` | Orthopedic specialism + technique names | If they're TPLO / TTA-Rapid certified, that's rare credibility |
| `laser*`, `acupunctuur*`, `fysio*` | Alternative-therapy specialism | Often €30-50/session, listed publicly |
| `tand*`, `gebit*` | Dental specialism — sometimes since-year | "Specialisme sinds 1995" = 30-year track record |
| `team`, `medewerkers` | Real photos + names — usually 1 page | Don't fabricate; if missing, use placeholder section |
| `over*`, `historie`, `praktijk` | Founding year, owner names, partnerships | Use if surfaced; never invent |
| Blog `/post-sitemap.xml` | Mostly placeholder ("hallo wereld"), but occasionally case studies | Skip unless meaty |

#### Sanity check before writing copy

Open the `CONTENT-INVENTORY.md` (write one — see Pijnappel's at `/Users/giuseppegeukes/Website Klanten Projecten/pijnappel-content/CONTENT-INVENTORY.md` for the template). Note specifically:

- Any published **pricing** — surface this prominently. Vet clients HATE pricing-hide-and-seek.
- Any **specialist credentials** (surgeon certification, society membership, since-year) — these are pitch gold
- Any **emotional services** (home euthanasia, hospice care) — don't bury, give a dedicated page
- **All photo URLs** counted — should be 30-60 for a typical Dutch vet clinic. If <15, the original site is sparse and you'll lean more on Pexels stock.

#### What NOT to fabricate

Per the asset-reuse memory + honesty rules:
- ❌ Don't invent prices that aren't on the source site
- ❌ Don't invent credentials ("gespecialiseerd in X") if not stated
- ❌ Don't invent partnerships or memberships
- ❌ Don't invent team bios beyond name + role
- ✅ Do mark "placeholder" in the README for anything to verify with the clinic later

### 2. Run the consolidated script

Set the CONFIG block at top, run, done. ~5 seconds. Sanity sweep confirms zero leftover Pijnappel references.

### 3. Decide team page structure

| Team size | Approach |
|---|---|
| 16+ people (large urban clinic) | Keep Pijnappel's 3-section structure (Dierenartsen / Paraveterinairen / Waarnemend) |
| 6-15 people | Collapse to 2 sections (Dierenartsen / Ondersteunend team) |
| 1-5 people | Single "Ons team" section, 2-3 col grid, larger photos |

### 4. Customize copy

Targeted edits for clinic voice — don't try to script these:
- **Hero H1** — 3-line poetic statement. Pijnappel: *"Voor een vriend die altijd trouw is gebleven."* Generic alternative: *"Persoonlijke zorg, voor wie het meest om je geeft."* / *"Een dierenarts die de tijd neemt."*
- **About teaser** — 2 short paragraphs about the clinic's approach. Lead with concrete differentiators (eigen OK, in-house lab, free parking, weekend availability) not generic warmth-language.
- **Specialty descriptions** — 5 sections in `specialiteiten.html`. Match the clinic's actual specialties; remove sections they don't offer (e.g., a small clinic without dental X-ray should drop the "Tandheelkunde" section or simplify it).
- **Mission quote badge** — Pijnappel uses *"Samen sterk voor dier én mens."* (their actual mission statement from the source site). Find the clinic's real mission if posted anywhere; otherwise use a generic vet-care line like *"Met evenveel zorg als jij geeft."* or *"Geen nummers, alleen vrienden."*

### 5. Rewrite README.md

Use Pijnappel's `README.md` as the template. Sections:
- Live URL placeholder
- Stack notes
- Folder structure
- Local test instructions
- Vercel deploy commands
- **Verified-facts table** — what's confirmed vs what's placeholder
- **Pitch angle for cold outreach** — why this prospect specifically would benefit from a new site

### 6. Local test

```bash
cd websites/vet-clinics/{slug}
python3 -m http.server 8000
open http://localhost:8000/
```

Click through every nav link. Verify:
- All 4 pages load
- Video autoplays in hero (Pixar story still works since you kept the MP4)
- Paw cluster renders in hero top-right (desktop only)
- No "Pijnappel" or "Sint Annastraat" leftover anywhere
- No broken images (the Pexels rotation should have covered all wp-content URLs)
- "Bel voor afspraak" CTAs link to `tel:` not the old afspraak URL

### 7. Deploy (only when user asks)

```bash
vercel --prod --yes
```

Subdomain defaults to `{folder-name}.vercel.app`. For custom domain: `vercel domains add` + DNS prompt.

### 8. Mobile + Lighthouse optimization (post-conversion only)

**Don't bother for prospect mockups** — they're meant to be sent as a quick demo, not to win Lighthouse scores. The Tailwind CDN + external Pexels images are fine for showing the concept.

**When the prospect converts to a paying client**, run the full mobile + Lighthouse optimization workflow before going live. See the dedicated memory entry [`feedback_mobile_lighthouse_workflow.md`](../../../../.claude/projects/-Users-giuseppegeukes-Website-Klanten-Projecten/memory/feedback_mobile_lighthouse_workflow.md) — 7-step recipe that took Pijnappel to mobile Lighthouse 98 across pages.

Summary of the 7 steps:

1. **Tailwind CDN → local CLI build** — `npx tailwindcss@3 -i ./src/input.css -o ./output.css --minify` (~20KB). Strip the `<script src="cdn.tailwindcss.com">` + inline config from every HTML file, replace with `<link rel="stylesheet" href="output.css" />`.
2. **Async Google Fonts** — `<link rel="preload" as="style" onload="this.onload=null;this.rel='stylesheet'">` pattern with `<noscript>` fallback.
3. **Download all images locally + WebP-convert** — Pexels stock and any client photos. Resize: hero 1600px / portraits 800px / illustrations 1200px. WebP quality 82.
4. **Rewrite `<img>` tags** in one Python pass — add `width`/`height` to prevent CLS, `loading="lazy" decoding="async"` for below-fold, `fetchpriority="high"` for hero.
5. **Strip `.reveal` class from above-fold hero elements** — GSAP opacity:0 on the LCP element kills Lighthouse score by 15-30 points. Above-fold gets no reveal animation; below-fold keeps it.
6. **Mobile UX fixes** — `pt-32 → pt-24 sm:pt-32`, hero h1 smaller on mobile, hamburger `p-2 → p-3` for 44px tap-target, service-grid `sm:grid-cols-3` for tablet.
7. **Verify with Lighthouse** — `npx lighthouse@12 <url> --form-factor=mobile --throttling.cpuSlowdownMultiplier=4 --quiet --chrome-flags="--headless=new"`. Localhost scores ±10 points noisier than production Vercel.

Lighthouse-killers, in impact order:
- Tailwind CDN: **-25 to -35 perf**
- `.reveal` opacity:0 on LCP element: **-15 to -30 perf** (LCP +10s)
- Render-blocking Google Fonts: **-10 to -15 perf**
- PNG instead of WebP: -5 to -10 perf per big image
- Missing width/height on `<img>`: -5 to -10 perf (CLS)
- External image CDN (no local cache): -5 perf

**Do not** waste time moving GSAP/Lenis (already at body bottom, not render-blocking) or adding `font-display: swap` (already in Google Fonts URL).

## Verify-before-launch checklist

When the prospect converts to a real client, before going live:

- [ ] **Real team list collected** — names + roles + photos from the actual clinic
- [ ] **Logo file added** to `/images/` — replace the text wordmark with `<img>` tag (or generate light variant if logo is dark)
- [ ] **Custom AI animation generated** (optional, via `higgsfield-ai-animations` skill) — to match the clinic's actual brand colors / specific team appearance
- [ ] **Phone + email tested** — both ring through / receive
- [ ] **Opening hours verified** with the owner (some clinics have lunch breaks, monthly closures, summer hours)
- [ ] **Specialties match reality** — don't list services they don't offer
- [ ] **Mission statement is the clinic's own, not Pijnappel's** — replace "Samen sterk voor dier én mens" with their actual values
- [ ] **Partnership logos** — only show KNMVD / LICG / WVT / VetPartners if the clinic is actually a member
- [ ] **Pexels stock photos replaced** with the clinic's real photos (interior, exterior, team in action)
- [ ] **Reviews** — pull 3 real Google reviews or remove the review section (the prospect mockup uses placeholders)

## Pitfalls & fallbacks

- **Spoed-info wording** — Pijnappel's `contact.html` says "voicemail verwijst je door naar dichtstbijzijnde dierenarts met avond/weekenddienst". This assumes a doorverwijzing system exists. If the clinic doesn't have one, replace with: *"Voor spoed buiten openingstijden bel je 113 Dierhulp"* (the national emergency line for animals) or the specific regional emergency clinic.
- **VetPartners** — chain-only line. Remove for independent clinics.
- **"Volledig op afspraak"** — Pijnappel works appointment-only. If the new clinic has walk-in hours, change this in 2 places: contact.html "Praktisch" + the hero "Nu geopend" badge area.
- **Booking-link substitution gotcha** — if the script's regex doesn't catch a variant, search manually for `online-afspraak-boeken` after running and replace any leftover with `tel:` links.
- **Maps iframe** — `src` URL contains the address with `+` for spaces. The Python script handles this correctly if you don't have weird characters in the new address. Verify embed renders.

## Cleanup

Per [feedback memory](../../README.md): for prospect mockups, reuse all AI animations. For converted clients:
- Generate a fresh `vet-dog-{client-style}-animation.mp4` via `higgsfield-ai-animations`
- Swap in the new MP4 in `index.html` hero `<source>` and update `poster` to match
- Remove the inherited Pijnappel-specific assets if no longer used

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

