#!/usr/bin/env python3
"""Prospect-mockup template generator (skill: building-prospect-mockups).

Public API:
    from template_generator import render_all, BRANCHES
    render_all(targets=[...], output_dir="sites", port=8912)

Honesty rules (non-negotiable):
- Only verified facts in user-facing copy (verify via 2 directories)
- Activity check via Oozo BEFORE generating (skip inactive businesses)
- Footer-only mockup disclaimer; no visual stock-photo labels in body
- robots noindex,nofollow always
"""

from __future__ import annotations
import re, csv, json, urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional

# These get set by render_all(); kept module-level for backwards-compat.
ROOT: Path = Path(".")
SITES: Path = Path("./sites")


# =============================================================================
# BRANCHES — per-branche presets. Add a new business type by extending.
# =============================================================================
BRANCHES: Dict[str, Dict[str, Any]] = {
    "kapper": {
        "schema_type": "HairSalon",
        "default_palette": "navy",
        "pexels_keyword": "barbershop",
        "default_branche_label": "Dames-, heren- en kinderkapper",
        "service_icon_default": "scissors",
    },
    "cafe": {
        "schema_type": "CafeOrCoffeeShop",
        "default_palette": "sienna",
        "pexels_keyword": "cafe interior",
        "default_branche_label": "Café · koffiebar",
        "service_icon_default": "coffee",
    },
    "restaurant": {
        "schema_type": "Restaurant",
        "default_palette": "rose",
        "pexels_keyword": "restaurant interior",
        "default_branche_label": "Restaurant",
        "service_icon_default": "plate",
    },
    "bar": {
        "schema_type": "BarOrPub",
        "default_palette": "graphite",
        "pexels_keyword": "cocktail bar",
        "default_branche_label": "Bar · kroeg",
        "service_icon_default": "glass",
    },
    "bakkerij": {
        "schema_type": "Bakery",
        "default_palette": "sienna",
        "pexels_keyword": "bakery bread",
        "default_branche_label": "Bakkerij",
        "service_icon_default": "bread",
    },
    "slager": {
        "schema_type": "Store",
        "default_palette": "sienna",
        "pexels_keyword": "butcher shop",
        "default_branche_label": "Slager",
        "service_icon_default": "knife",
    },
    "schoonheidssalon": {
        "schema_type": "BeautySalon",
        "default_palette": "rose",
        "pexels_keyword": "beauty salon",
        "default_branche_label": "Schoonheidssalon",
        "service_icon_default": "drop",
    },
    "bloemist": {
        "schema_type": "Florist",
        "default_palette": "sage",
        "pexels_keyword": "flower shop",
        "default_branche_label": "Bloemist",
        "service_icon_default": "flower",
    },
    "fysio": {
        "schema_type": "MedicalClinic",
        "default_palette": "sage",
        "pexels_keyword": "physiotherapy clinic",
        "default_branche_label": "Fysiotherapie",
        "service_icon_default": "hand",
    },
    "tandarts": {
        "schema_type": "Dentist",
        "default_palette": "navy",
        "pexels_keyword": "dental clinic",
        "default_branche_label": "Tandarts",
        "service_icon_default": "tooth",
    },
    "garage": {
        "schema_type": "AutoRepair",
        "default_palette": "graphite",
        "pexels_keyword": "auto mechanic shop",
        "default_branche_label": "Autogarage",
        "service_icon_default": "car",
    },
    "boekhandel": {
        "schema_type": "BookStore",
        "default_palette": "olive",
        "pexels_keyword": "independent bookstore",
        "default_branche_label": "Boekhandel",
        "service_icon_default": "book",
    },
    "apotheek": {
        "schema_type": "Pharmacy",
        "default_palette": "navy",
        "pexels_keyword": "pharmacy interior",
        "default_branche_label": "Apotheek",
        "service_icon_default": "plus",
    },
    "dakdekker": {
        "schema_type": "RoofingContractor",
        "default_palette": "graphite",
        "pexels_keyword": "roofer roof construction",
        "default_branche_label": "Dakdekker · dakwerken",
        "service_icon_default": "tools",
    },
    "cheese": {
        "schema_type": "Store",
        "default_palette": "olive",
        "pexels_keyword": "cheese shop",
        "default_branche_label": "Kaashandel · delicatessen",
        "service_icon_default": "plate",
    },
    "jewelry": {
        "schema_type": "JewelryStore",
        "default_palette": "rose",
        "pexels_keyword": "jewelry boutique",
        "default_branche_label": "Sieraden · juwelier",
        "service_icon_default": "flower",
    },
    "music": {
        "schema_type": "Store",
        "default_palette": "graphite",
        "pexels_keyword": "vinyl record store",
        "default_branche_label": "Platenzaak · vinyl",
        "service_icon_default": "music",
    },
    "furniture": {
        "schema_type": "FurnitureStore",
        "default_palette": "sienna",
        "pexels_keyword": "vintage furniture shop",
        "default_branche_label": "Wonen · meubels",
        "service_icon_default": "plate",
    },
    "clothes": {
        "schema_type": "ClothingStore",
        "default_palette": "rose",
        "pexels_keyword": "clothing boutique interior",
        "default_branche_label": "Kleding · boutique",
        "service_icon_default": "smile",
    },
    "alcohol": {
        "schema_type": "Store",
        "default_palette": "sienna",
        "pexels_keyword": "craft beer shop",
        "default_branche_label": "Speciaaldrank · bier &amp; wijn",
        "service_icon_default": "glass",
    },
}


def slugify(name: str) -> str:
    """URL-safe slug: decode HTML entities, strip accents, then dash-join."""
    import html as _html, unicodedata
    s = _html.unescape(name)                                    # &amp; -> &
    s = s.replace("&", " en ")                                  # & -> "en"
    s = unicodedata.normalize("NFD", s)                         # ê -> e + ́
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")  # strip accents
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return re.sub(r"-+", "-", s)


def pexels_url(photo_id: int, w: int = 1200) -> str:
    """Stable hotlink-friendly Pexels CDN URL."""
    return f"https://images.pexels.com/photos/{photo_id}/pexels-photo-{photo_id}.jpeg?auto=compress&cs=tinysrgb&w={w}"


PALETTES = {
    "navy":    {"primary": "#243558", "primary_dark": "#13203a", "accent": "#c79a52", "paper": "#faf6ed", "paper_dim": "#f0e9d8", "ink": "#15171c"},
    "sienna":  {"primary": "#7d3a26", "primary_dark": "#561f10", "accent": "#d9a86d", "paper": "#fbf6ee", "paper_dim": "#f1e8d2", "ink": "#1c1612"},
    "sage":    {"primary": "#3d4d34", "primary_dark": "#23301c", "accent": "#c9a87a", "paper": "#f7f5ee", "paper_dim": "#ece8d8", "ink": "#1c1d18"},
    "olive":   {"primary": "#605a2c", "primary_dark": "#3e3a18", "accent": "#d4b35c", "paper": "#fbf8eb", "paper_dim": "#f0ebd5", "ink": "#1c1c14"},
    "rose":    {"primary": "#7a3548", "primary_dark": "#54222f", "accent": "#d9a098", "paper": "#fbf3f1", "paper_dim": "#f5e3df", "ink": "#1c1416"},
    "graphite": {"primary": "#22272e", "primary_dark": "#13171c", "accent": "#c8a979", "paper": "#f6f3ec", "paper_dim": "#e9e3d4", "ink": "#16181d"},
}

# Inline SVG icons keyed by service category — drawn deliberately simple
ICONS = {
    "scissors": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/></svg>',
    "drop":     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>',
    "comb":     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="9" width="18" height="3" rx="1"/><line x1="6" y1="12" x2="6" y2="18"/><line x1="10" y1="12" x2="10" y2="20"/><line x1="14" y1="12" x2="14" y2="20"/><line x1="18" y1="12" x2="18" y2="18"/></svg>',
    "razor":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="6" height="14" rx="1.5"/><path d="M9 6h7l5 6-5 6H9"/></svg>',
    "smile":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>',
    "spray":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="9" width="9" height="13" rx="1.5"/><line x1="11.5" y1="6" x2="11.5" y2="9"/><circle cx="20" cy="4" r="1"/><circle cx="17" cy="3" r="1"/><circle cx="20" cy="8" r="1"/></svg>',
    "kid":      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M5 21v-2a4 4 0 0 1 4-4h6a4 4 0 0 1 4 4v2"/></svg>',
    "wash":     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12c2-3 5-3 8-3s6 0 8 3"/><path d="M4 12v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-6"/><line x1="9" y1="3" x2="9" y2="6"/><line x1="13" y1="3" x2="13" y2="6"/></svg>',
    # Café / restaurant / bar / bakery
    "coffee":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M17 8h1a3 3 0 1 1 0 6h-1"/><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V8z"/><line x1="6" y1="2" x2="6" y2="4"/><line x1="10" y1="2" x2="10" y2="4"/><line x1="14" y1="2" x2="14" y2="4"/></svg>',
    "plate":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/></svg>',
    "knife":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21l9-9 6-6 3 3-6 6-9 9z"/><path d="M14 8l4 4"/></svg>',
    "glass":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3h14l-2 8a5 5 0 0 1-10 0L5 3z"/><line x1="12" y1="16" x2="12" y2="21"/><line x1="8" y1="21" x2="16" y2="21"/></svg>',
    "bread":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12c0-3 3-5 9-5s9 2 9 5c0 1.5-1 2.5-2 3v3a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-3c-1-.5-2-1.5-3-3z"/><line x1="8" y1="14" x2="8" y2="18"/><line x1="12" y1="14" x2="12" y2="18"/><line x1="16" y1="14" x2="16" y2="18"/></svg>',
    "oven":     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="17" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/><circle cx="7" cy="7" r="1"/><circle cx="11" cy="7" r="1"/><circle cx="15" cy="7" r="1"/></svg>',
    "music":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9 17V5l12-2v12"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
    # Beauty / wellness / florist
    "flower":   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 9V3M12 21v-6M9 12H3M21 12h-6M7 7l-3-3M20 20l-3-3M7 17l-3 3M20 4l-3 3"/></svg>',
    # Healthcare
    "tooth":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 5a4 4 0 0 1 4-2 5 5 0 0 1 3 1 5 5 0 0 1 3-1 4 4 0 0 1 4 2c1 2 0 5-1 9-.5 2-1 4-2 5-1 1-3 0-3-2-.2-2-.4-3-1-3s-.8 1-1 3c0 2-2 3-3 2-1-1-1.5-3-2-5-1-4-2-7-1-9z"/></svg>',
    "plus":     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
    "hand":     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11V5.5a1.5 1.5 0 1 1 3 0V11M12 11V4a1.5 1.5 0 1 1 3 0v7M15 11V6a1.5 1.5 0 1 1 3 0v8a7 7 0 0 1-7 7h-1a7 7 0 0 1-6.7-5l-1-3.5a1.5 1.5 0 1 1 2.7-1.3L7 14V8a1.5 1.5 0 1 1 3 0v3"/></svg>',
    "heart":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    # Books / retail
    "book":     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    # Auto
    "car":      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17h2l1.5-5h11l1.5 5h2v-3l-2-1-1.5-3a2 2 0 0 0-1.8-1H7.8a2 2 0 0 0-1.8 1L4.5 13l-2 1v3z"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/></svg>',
    "tools":    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 1 1 5 5L18 13l-5-5 1.7-1.7z"/><path d="M13 8L4 17v3h3l9-9"/></svg>',
}


PAGE_TEMPLATE = """<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{name} · {branche_label} · {city}</title>
  <meta name="description" content="{meta_description}">
  <meta name="robots" content="noindex,nofollow">
  <meta property="og:title" content="{name} · {city}">
  <meta property="og:description" content="{meta_description}">
  <meta property="og:type" content="website">
  <meta name="theme-color" content="{primary}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script type="application/ld+json">{schema_jsonld}</script>
  <style>
    :root {{
      --primary:{primary}; --primary-dark:{primary_dark}; --accent:{accent};
      --paper:{paper}; --paper-dim:{paper_dim}; --ink:{ink};
      --hairline:rgba(20,22,30,.13); --shadow:0 18px 40px -22px rgba(20,22,30,.18); --shadow-lg:0 36px 70px -30px rgba(20,22,30,.25);
      --section-y:clamp(2.75rem,5vw,5rem);
    }}
    *{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
    body{{margin:0;font-family:'Inter Tight',ui-sans-serif,system-ui,sans-serif;color:var(--ink);background:var(--paper);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased;font-feature-settings:"ss01","cv11"}}
    a{{color:var(--primary);text-decoration:none;transition:color .2s}} a:hover{{color:var(--accent)}}
    h1,h2,h3{{font-family:'Fraunces',ui-serif,Georgia,serif;font-weight:500;letter-spacing:-.025em;color:var(--primary);margin:0 0 .5em;line-height:1.05;font-variation-settings:"opsz" 144,"SOFT" 50;font-feature-settings:"ss01","ss02"}}
    h1{{font-size:clamp(2.6rem,6.5vw,5.4rem);font-weight:500;letter-spacing:-.035em}} h2{{font-size:clamp(1.8rem,3.4vw,2.8rem);letter-spacing:-.025em}} h3{{font-size:1.3rem;letter-spacing:-.015em;line-height:1.2}}
    p{{margin:0 0 1em}} img{{max-width:100%;display:block;height:auto}}
    .container{{max-width:1180px;margin:0 auto;padding:0 clamp(1rem,3vw,2rem)}}
    .container--narrow{{max-width:820px}}
    .eyebrow{{display:inline-block;font-size:.78rem;letter-spacing:.22em;text-transform:uppercase;font-weight:700;color:var(--accent);margin-bottom:1rem}}
    .italic{{font-style:italic;color:var(--accent);font-family:'Fraunces',ui-serif,Georgia,serif;font-weight:500}}
    /* HEADER */
    header.site{{position:sticky;top:0;z-index:50;background:rgba(250,246,237,.95);backdrop-filter:blur(10px);border-bottom:1px solid var(--hairline)}}
    .site-inner{{display:flex;align-items:center;justify-content:space-between;padding:1.1rem 0;gap:1rem}}
    .wordmark{{display:inline-flex;align-items:center;gap:.85rem;text-decoration:none}}
    .wordmark__monogram{{width:46px;height:46px;border-radius:14px;background:var(--primary);color:var(--paper);display:inline-flex;align-items:center;justify-content:center;font-family:'Fraunces',ui-serif,Georgia,serif;font-weight:600;font-size:1.55rem;letter-spacing:-.02em;flex-shrink:0;box-shadow:inset 0 0 0 2px rgba(255,255,255,.08)}}
    .wordmark__monogram span{{display:inline-block;transform:translateY(-1px)}}
    .wordmark__text{{font-family:'Fraunces',ui-serif,Georgia,serif;font-size:1.4rem;font-weight:600;color:var(--primary);letter-spacing:.005em;line-height:1.1}}
    .wordmark__text small{{display:block;font-family:'Inter Tight',ui-sans-serif,system-ui,sans-serif;font-size:.6rem;letter-spacing:.28em;text-transform:uppercase;font-weight:600;color:var(--ink);opacity:.55;margin-top:2px}}
    .nav-links{{display:flex;gap:1.6rem;align-items:center;font-size:.93rem;font-weight:500}}
    .nav-links a{{color:var(--ink)}}
    .cta-call{{background:var(--primary);color:var(--paper);padding:.55rem 1.1rem;border-radius:999px;font-size:.85rem;font-weight:600;letter-spacing:.04em}}
    .cta-call:hover{{background:var(--primary-dark);color:var(--paper)}}
    @media (max-width:780px){{.nav-links a:not(.cta-call){{display:none}}}}
    /* HERO */
    .hero{{background:var(--primary);color:var(--paper);padding:clamp(4.5rem,10vw,8rem) 0 clamp(3.5rem,7vw,6rem);position:relative;overflow:hidden}}
    .hero__bg{{position:absolute;inset:0;background-size:cover;background-position:center;opacity:.22;filter:saturate(.9) contrast(1.05)}}
    .hero::before{{content:"";position:absolute;inset:0;background:linear-gradient(135deg,rgba(20,32,58,.94) 0%,rgba(20,32,58,.78) 45%,rgba(20,32,58,.65) 100%);pointer-events:none}}
    .hero::after{{content:"";position:absolute;inset:0;background:radial-gradient(circle at 88% 12%,rgba(199,154,82,.18) 0,transparent 50%),radial-gradient(circle at 5% 95%,rgba(199,154,82,.16) 0,transparent 55%);pointer-events:none}}
    .hero-grid{{position:relative;display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(2rem,5vw,4rem);align-items:center}}
    @media (max-width:820px){{.hero-grid{{grid-template-columns:1fr}}}}
    .hero h1{{color:var(--paper);max-width:14ch;margin-bottom:1.3rem}}
    .hero p.lead{{font-size:clamp(1.05rem,1.4vw,1.2rem);max-width:46ch;color:rgba(250,246,237,.85)}}
    .hero .eyebrow{{color:rgba(199,154,82,.95)}}
    .hero-cta{{display:flex;flex-wrap:wrap;gap:.85rem;margin-top:2rem}}
    .hero-card{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:1.8rem;backdrop-filter:blur(4px)}}
    .hero-card h4{{margin:0 0 1rem;font-family:'Inter Tight',ui-sans-serif,system-ui,sans-serif;font-size:.78rem;letter-spacing:.22em;text-transform:uppercase;color:rgba(199,154,82,1)}}
    .hero-card .row{{display:flex;justify-content:space-between;padding:.5rem 0;border-bottom:1px dashed rgba(255,255,255,.18);font-size:.93rem;color:rgba(250,246,237,.85)}}
    .hero-card .row:last-child{{border-bottom:0}}
    .hero-card .row.is-today{{color:var(--accent);font-weight:600}}
    /* STATUS BADGE */
    .status{{display:inline-flex;align-items:center;gap:.5rem;padding:.4rem .9rem;border-radius:999px;font-size:.78rem;font-weight:700;letter-spacing:.04em;background:rgba(255,255,255,.08);color:rgba(250,246,237,.9);border:1px solid rgba(255,255,255,.14);text-transform:uppercase;margin-bottom:1.4rem}}
    .status::before{{content:"";width:8px;height:8px;border-radius:50%;background:currentColor;flex-shrink:0}}
    .status.open{{background:rgba(70,160,90,.16);color:#9ed8a9;border-color:rgba(70,160,90,.4)}}
    .status.closed{{background:rgba(180,60,60,.18);color:#ecb1b1;border-color:rgba(180,60,60,.4)}}
    /* SINCE BADGE */
    .since-badge{{display:inline-flex;align-items:center;gap:.5rem;font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;font-weight:600;color:rgba(250,246,237,.65)}}
    .since-badge::before{{content:"";width:24px;height:1px;background:rgba(250,246,237,.4)}}
    /* BTN */
    .btn{{display:inline-flex;align-items:center;gap:.5rem;padding:.85rem 1.6rem;border-radius:999px;font-weight:600;font-size:.95rem;border:1.5px solid transparent;transition:all .2s;font-family:inherit;cursor:pointer}}
    .btn--primary{{background:var(--accent);color:var(--primary-dark)}} .btn--primary:hover{{background:#fff;color:var(--primary-dark);transform:translateY(-1px)}}
    .btn--ghost{{background:transparent;color:var(--paper);border-color:rgba(250,246,237,.35)}} .btn--ghost:hover{{background:rgba(250,246,237,.1);border-color:rgba(250,246,237,.7);color:var(--paper)}}
    .btn--blau{{background:var(--primary);color:var(--paper)}} .btn--blau:hover{{background:var(--primary-dark);color:var(--paper)}}
    .btn--outline{{background:transparent;color:var(--primary);border-color:var(--primary)}} .btn--outline:hover{{background:var(--primary);color:var(--paper)}}
    /* SECTIONS */
    section{{padding:var(--section-y) 0}}
    section.alt{{background:var(--paper-dim)}}
    section.dark{{background:var(--primary);color:var(--paper)}}
    section.dark h2,section.dark h3{{color:var(--paper)}} section.dark .eyebrow{{color:rgba(199,154,82,.95)}}
    section.dark .section-head p{{color:rgba(250,246,237,.78)}}
    /* Cards inside dark sections keep dark text (white-card on navy) */
    section.dark .step h3,section.dark .card h3,section.dark .svc h3,section.dark .review__text,section.dark .atst__name{{color:var(--primary)}}
    .section-head{{text-align:center;max-width:680px;margin:0 auto clamp(2rem,4vw,3rem)}}
    .divider{{width:48px;height:2px;background:var(--accent);margin:1rem auto 1.5rem;border:0}}
    /* QUOTE */
    /* SERVICE CARDS */
    .grid{{display:grid;gap:1.25rem;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}
    .svc{{background:#fff;border:1px solid var(--hairline);border-radius:14px;padding:1.5rem 1.5rem 1.6rem;transition:transform .25s,box-shadow .25s,border-color .25s}}
    .svc:hover{{transform:translateY(-3px);box-shadow:var(--shadow);border-color:transparent}}
    .svc-icon{{width:46px;height:46px;border-radius:12px;background:var(--primary);color:var(--paper);display:inline-flex;align-items:center;justify-content:center;margin-bottom:1.1rem}}
    .svc-icon svg{{width:24px;height:24px}}
    .svc h3{{margin:0 0 .35rem;font-size:1.25rem}} .svc p{{color:var(--ink);opacity:.72;font-size:.93rem;margin-bottom:0}}
    /* CONTACT */
    .contact-row{{display:grid;gap:clamp(1.5rem,4vw,3rem);grid-template-columns:1fr 1fr;align-items:start}}
    @media (max-width:760px){{.contact-row{{grid-template-columns:1fr}}}}
    .contact-card{{background:#fff;border:1px solid var(--hairline);border-radius:14px;padding:1.8rem;border-left:4px solid var(--accent)}}
    .contact-card h3{{margin:0 0 .5rem}}
    .contact-card .row{{display:flex;justify-content:space-between;gap:1rem;padding:.55rem 0;border-bottom:1px dashed var(--hairline);font-size:.95rem}}
    .contact-card .row:last-child{{border-bottom:0}}
    .contact-card .row span:first-child{{color:var(--ink);opacity:.55;font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;font-weight:700;flex-shrink:0}}
    .contact-card .row.is-today{{color:var(--accent);font-weight:600}}
    .map{{aspect-ratio:4/3;border-radius:14px;overflow:hidden;border:1px solid var(--hairline);box-shadow:var(--shadow)}}
    .map iframe{{width:100%;height:100%;border:0;display:block}}
    /* TAGS */
    .tag-row{{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.5rem;justify-content:center}}
    .tag{{background:#fff;color:var(--primary);padding:.45rem 1rem;border-radius:999px;font-size:.85rem;font-weight:500;border:1px solid var(--hairline)}}
    /* CTA STRIP */
    .cta-strip{{background:var(--primary);color:var(--paper);padding:clamp(2rem,4vw,3.5rem) clamp(1.5rem,4vw,3rem);border-radius:18px;display:grid;grid-template-columns:1.3fr .7fr;gap:1.5rem;align-items:center;margin:0 auto;max-width:1100px}}
    @media (max-width:680px){{.cta-strip{{grid-template-columns:1fr;text-align:center}}}}
    .cta-strip h2{{color:var(--paper);margin:0 0 .5rem}}
    .cta-strip p{{margin:0;color:rgba(250,246,237,.85)}}
    .cta-strip .actions{{display:flex;flex-wrap:wrap;gap:.75rem;justify-content:flex-end}}
    @media (max-width:680px){{.cta-strip .actions{{justify-content:center}}}}
    /* GALLERY — simple 3×2 grid */
    .gallery{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
    .gallery__cell{{position:relative;overflow:hidden;border-radius:14px;background:var(--paper-dim);aspect-ratio:4/3}}
    .gallery__cell img{{width:100%;height:100%;object-fit:cover;transition:transform .55s cubic-bezier(.2,.7,.2,1);display:block}}
    .gallery__cell:hover img{{transform:scale(1.04)}}
    @media (max-width:740px){{.gallery{{grid-template-columns:repeat(2,1fr)}}}}
    /* ABOUT WITH IMAGE */
    .about-row{{display:grid;grid-template-columns:1fr 1fr;gap:clamp(2rem,5vw,4rem);align-items:center}}
    @media (max-width:780px){{.about-row{{grid-template-columns:1fr}}}}
    .about-img{{aspect-ratio:4/5;border-radius:18px;overflow:hidden;box-shadow:var(--shadow-lg)}}
    .about-img img{{width:100%;height:100%;object-fit:cover;display:block}}
    /* REVIEWS */
    .review-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.5rem;margin-top:2rem}}
    .review{{background:#fff;border:1px solid var(--hairline);border-radius:14px;padding:1.8rem 1.7rem;display:flex;flex-direction:column;gap:1rem}}
    .review__stars{{color:var(--accent);font-size:1.05rem;letter-spacing:.1em}}
    .review__text{{font-family:'Fraunces',ui-serif,Georgia,serif;font-size:1.25rem;line-height:1.45;color:var(--primary);font-style:italic;font-weight:500;margin:0}}
    .review__author{{margin-top:auto;font-size:.85rem;color:var(--ink);opacity:.65;font-weight:600;letter-spacing:.06em;text-transform:uppercase}}
    .rating-summary{{display:inline-flex;align-items:center;gap:.85rem;background:#fff;padding:.85rem 1.4rem;border-radius:999px;border:1px solid var(--hairline);margin-top:1.5rem;font-size:.93rem}}
    .rating-summary strong{{font-family:'Fraunces',ui-serif,Georgia,serif;font-size:1.4rem;font-weight:700;color:var(--primary)}}
    /* Star rating with proper partial-fill (real percentages, no rounding) */
    .rs-stars{{position:relative;display:inline-block;line-height:1;font-family:Georgia,'Times New Roman',serif;font-size:1.05rem;letter-spacing:.06em}}
    .rs-stars__bg{{color:rgba(20,22,30,.18)}}
    .rs-stars__fg{{position:absolute;top:0;left:0;color:var(--accent);overflow:hidden;white-space:nowrap}}
    .rating-summary small{{color:var(--ink);opacity:.6}}
    /* TESTIMONIALS — compact 2-col: intro left, white card right */
    .atst{{padding:clamp(2.25rem,4.5vw,4rem) 0;background:var(--paper-dim)}}
    .atst__inner{{max-width:1080px;margin:0 auto;padding:0 clamp(1rem,3vw,2rem);display:grid;grid-template-columns:.42fr .58fr;gap:clamp(2rem,5vw,4rem);align-items:center}}
    @media (max-width:760px){{.atst__inner{{grid-template-columns:1fr;gap:1.75rem}}}}
    /* Left intro */
    .atst__intro{{display:flex;flex-direction:column;align-items:flex-start;text-align:left}}
    .atst__intro h2{{font-size:clamp(1.6rem,3vw,2.3rem);margin:.4rem 0 0}}
    .atst__intro .divider{{margin:1rem 0 1.1rem!important;margin-left:0!important}}
    .atst__lead{{color:var(--ink);opacity:.7;font-size:.98rem;line-height:1.55;margin:0;max-width:36ch}}
    .atst__intro .rating-summary{{margin-top:1.3rem}}
    /* Right card */
    .atst__card-wrap{{display:flex;flex-direction:column;gap:1rem}}
    .atst__card{{position:relative;background:#fff;border-radius:18px;padding:clamp(1.5rem,2.6vw,2rem);box-shadow:0 24px 60px -28px rgba(20,32,58,.18),0 1px 0 rgba(20,22,30,.04);border:1px solid var(--hairline);transition:opacity .35s,transform .35s;min-height:240px;display:flex;flex-direction:column}}
    .atst--changing .atst__card{{opacity:0;transform:translateY(8px)}}
    .atst__card-stars{{margin-bottom:1rem;line-height:1}}
    .atst__card-stars .rs-stars{{font-size:1rem}}
    .atst__quote{{font-family:'Fraunces',ui-serif,Georgia,serif;font-size:clamp(1.02rem,1.55vw,1.22rem);line-height:1.5;color:var(--primary);font-style:italic;font-weight:500;margin:0 0 1.4rem;letter-spacing:-.005em;flex:1}}
    .atst__attribution{{padding-top:1rem;border-top:1px solid var(--hairline);display:flex;flex-direction:column;gap:.2rem}}
    .atst__name{{font-family:'Fraunces',ui-serif,Georgia,serif;font-size:1.1rem;font-weight:600;color:var(--primary);letter-spacing:-.015em;line-height:1.1}}
    .atst__designation{{font-family:'Inter Tight',ui-sans-serif,system-ui,sans-serif;font-size:.72rem;color:var(--ink);opacity:.55;letter-spacing:.1em;text-transform:uppercase;font-weight:600}}
    /* Nav */
    .atst__nav{{display:flex;align-items:center;gap:.5rem}}
    .atst__nav button{{width:38px;height:38px;border-radius:50%;border:1.5px solid var(--hairline);background:#fff;color:var(--primary);cursor:pointer;font-size:1.05rem;font-family:inherit;transition:all .2s;display:inline-flex;align-items:center;justify-content:center;-webkit-tap-highlight-color:transparent}}
    .atst__nav button:hover{{background:var(--primary);color:var(--paper);transform:translateY(-1px);border-color:transparent}}
    .atst__dots{{display:flex;gap:.35rem;margin-left:.5rem;align-items:center}}
    .atst__dot{{width:6px;height:6px;border-radius:50%;background:var(--hairline);transition:all .25s;cursor:pointer;border:0;padding:0}}
    .atst__dot[data-active]{{background:var(--primary);width:20px;border-radius:999px}}
    /* PROCESS / 3-STEPS */
    .steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:1.5rem;counter-reset:step}}
    .step{{position:relative;padding:2.2rem 1.6rem 1.6rem;background:#fff;border:1px solid var(--hairline);border-radius:14px;counter-increment:step}}
    .step::before{{content:counter(step,decimal-leading-zero);position:absolute;top:-.65rem;left:1.5rem;background:var(--accent);color:var(--primary-dark);padding:.2rem .65rem;border-radius:999px;font-family:'Fraunces',ui-serif,Georgia,serif;font-weight:700;font-size:.95rem;letter-spacing:.05em}}
    .step h3{{margin:.25rem 0 .35rem;font-size:1.2rem}}
    .step p{{margin:0;color:var(--ink);opacity:.72;font-size:.94rem}}
    /* WHATSAPP */
    .btn--whatsapp{{background:#25d366;color:#fff;border-color:transparent}}
    .btn--whatsapp:hover{{background:#1fb858;color:#fff;transform:translateY(-1px)}}
    .btn--whatsapp svg{{width:18px;height:18px}}
    /* WHATSAPP FLOATING ACTION BUTTON (desktop) */
    .wapp-fab{{position:fixed;bottom:max(24px,env(safe-area-inset-bottom));right:max(24px,env(safe-area-inset-right));z-index:80;width:60px;height:60px;border-radius:50%;background:#25d366;color:#fff;display:inline-flex;align-items:center;justify-content:center;box-shadow:0 14px 28px -8px rgba(37,211,102,.5),0 4px 10px -2px rgba(20,22,30,.2);transition:transform .25s,box-shadow .25s,color .25s;text-decoration:none}}
    .wapp-fab:hover{{transform:translateY(-2px) scale(1.05);box-shadow:0 18px 36px -8px rgba(37,211,102,.6),0 6px 14px -2px rgba(20,22,30,.24);color:#fff}}
    .wapp-fab svg{{width:30px;height:30px;display:block;position:relative;z-index:1}}
    .wapp-fab::before{{content:"";position:absolute;inset:-4px;border-radius:50%;border:2px solid rgba(37,211,102,.5);animation:wapp-pulse 2.4s ease-out infinite;pointer-events:none}}
    @keyframes wapp-pulse{{0%{{transform:scale(.92);opacity:.7}} 100%{{transform:scale(1.5);opacity:0}}}}
    @media (prefers-reduced-motion:reduce){{.wapp-fab::before{{animation:none}}}}
    @media (max-width:680px){{.wapp-fab{{display:none}}}}
    /* STICKY MOBILE CTA */
    .sticky-cta{{display:none}}
    @media (max-width:680px){{
      .sticky-cta{{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:90;background:var(--primary);color:var(--paper);padding:.7rem 1rem;justify-content:space-between;align-items:center;gap:.75rem;box-shadow:0 -10px 24px -8px rgba(0,0,0,.18)}}
      .sticky-cta__name{{font-family:'Fraunces',ui-serif,Georgia,serif;font-size:1.05rem;font-weight:600;line-height:1.1}}
      .sticky-cta__name small{{display:block;font-family:'Inter Tight',ui-sans-serif,system-ui,sans-serif;font-size:.68rem;font-weight:500;opacity:.7}}
      .sticky-cta__buttons{{display:flex;gap:.5rem}}
      .sticky-cta a{{padding:.6rem .9rem;border-radius:999px;font-size:.85rem;font-weight:600;text-decoration:none}}
      .sticky-cta a.call{{background:var(--accent);color:var(--primary-dark)}}
      .sticky-cta a.wapp{{background:#25d366;color:#0a3a1a}}
      body{{padding-bottom:64px}}
    }}
    /* FOOTER */
    footer.site{{background:var(--primary-dark);color:rgba(250,246,237,.78);padding:2.5rem 0 1.5rem;font-size:.92rem;margin-top:clamp(2rem,4vw,3rem)}}
    footer .disclaimer{{background:var(--accent);color:var(--primary-dark);padding:1.1rem 1.4rem;border-radius:10px;font-size:.86rem;line-height:1.55;margin-bottom:1.5rem}}
    footer .disclaimer strong{{display:block;text-transform:uppercase;letter-spacing:.14em;font-size:.76rem;margin-bottom:.3rem;font-weight:800}}
    footer .legal{{font-size:.78rem;opacity:.6;margin-top:1rem;line-height:1.6}}
    footer a{{color:rgba(250,246,237,.85)}} footer a:hover{{color:var(--accent)}}
  </style>
</head>
<body>

<header class="site">
  <div class="container site-inner">
    <a href="#top" class="wordmark" aria-label="{name} – naar boven">
      <span class="wordmark__monogram" aria-hidden="true"><span>{monogram}</span></span>
      <span class="wordmark__text">{name}<small>{branche_label} · {city}</small></span>
    </a>
    <div class="nav-links">
      <a href="#diensten">Diensten</a>
      <a href="#klanten">Klanten</a>
      <a href="#bezoek">Bezoek</a>
      <a href="tel:{tel_link}" class="cta-call">{tel_short}</a>
    </div>
  </div>
</header>

<main id="top">

<section class="hero">
  {hero_bg_div}
  <div class="container hero-grid">
    <div>
      <span class="status" data-status>Openingstijden</span>
      <span class="eyebrow">{branche_label} · {neighborhood}</span>
      <h1>{tagline_h1}</h1>
      <p class="lead">{lead}</p>
      <div class="hero-cta">
        <a class="btn btn--primary" href="tel:{tel_link}">Bel voor afspraak</a>
        {whatsapp_button}
        <a class="btn btn--ghost" href="#bezoek">Adres &amp; tijden</a>
      </div>
      {since_badge_html}
    </div>
    <div class="hero-card">
      <h4>Vandaag · deze week</h4>
      {hero_hours}
    </div>
  </div>
</section>

<section id="diensten">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Diensten</span>
      <h2>{services_heading}</h2>
      <hr class="divider">
      <p style="opacity:.7">{services_intro}</p>
    </div>
    <div class="grid">
      {service_cards}
    </div>
    {tags_block}
  </div>
</section>

{reviews_section}

<section class="dark" id="hoe">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Hoe werkt het</span>
      <h2>In drie simpele stappen</h2>
      <hr class="divider">
    </div>
    <div class="steps">
      {steps_html}
    </div>
  </div>
</section>

<section id="verhaal">
  <div class="container">
    <div class="about-row">
      <div>
        <span class="eyebrow">Wie zijn we</span>
        <h2>{about_heading}</h2>
        <hr class="divider" style="margin:1rem auto 1.5rem 0">
        <p style="font-size:1.08rem;color:var(--ink);opacity:.78">{about_body}</p>
      </div>
      {about_image_html}
    </div>
  </div>
</section>

{gallery_section}

<section id="bezoek">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Bezoek ons</span>
      <h2>Even langskomen?</h2>
      <hr class="divider">
    </div>
    <div class="contact-row">
      <div class="contact-card">
        <h3>{name}</h3>
        <div class="row"><span>Adres</span><span>{addr}, {city}</span></div>
        <div class="row"><span>Telefoon</span><a href="tel:{tel_link}">{tel_clean}</a></div>
        {email_row}
        {socials_row}
        {hours_block}
        <div style="margin-top:1.4rem;display:flex;flex-wrap:wrap;gap:.6rem">
          <a class="btn btn--blau" href="tel:{tel_link}">Direct bellen</a>
          <a class="btn btn--outline" href="https://maps.google.com/?q={addr_q}+{city}" target="_blank" rel="noopener">Route in Maps</a>
        </div>
      </div>
      <div class="map">
        <iframe loading="lazy" title="Kaart {name}"
          src="https://www.openstreetmap.org/export/embed.html?bbox={bbox}&layer=mapnik&marker={lat}%2C{lon}"></iframe>
      </div>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="container">
    <div class="cta-strip">
      <div>
        <span class="eyebrow" style="color:var(--accent)">Klaar voor je nieuwe kapsel?</span>
        <h2>Bel even langs en je staat in de agenda.</h2>
        <p>Eerlijk, betaalbaar, en met aandacht.</p>
      </div>
      <div class="actions">
        <a class="btn btn--primary" href="tel:{tel_link}">{tel_clean}</a>
      </div>
    </div>
  </div>
</section>

</main>

{wapp_fab_html}

<div class="sticky-cta" aria-hidden="false">
  <div class="sticky-cta__name">{name}<small>{branche_label}</small></div>
  <div class="sticky-cta__buttons">
    <a class="call" href="tel:{tel_link}">📞 Bel</a>
    {sticky_wapp}
  </div>
</div>

<footer class="site">
  <div class="container">
    <div class="disclaimer">
      <strong>Voorbeeld-mockup · Geen officiële site</strong>
      Een vrijblijvend ontwerp-voorstel voor <strong>{name}</strong>. Geen officiële online-uitgave. Bel de eigenaar voor de échte zaak.
      Eigen website? <a href="mailto:giuseppegeukes@gmail.com?subject=Website voor {name}" style="color:var(--primary-dark);text-decoration:underline">giuseppegeukes@gmail.com</a>
    </div>
    <div>© <span id="y"></span> {name} · {addr}, {city} · <a href="tel:{tel_link}">{tel_clean}</a></div>
    <div class="legal">
      Bronnen: OpenStreetMap (CC-BY-SA), publieke directorypagina's. Foto's: <a href="https://www.pexels.com/" target="_blank" rel="noopener">Pexels</a> (gratis, hotlink toegestaan, fotografen gecrediteerd in galerij). Geen tracking, geen cookies, geen analytics. Robots: noindex.
    </div>
  </div>
</footer>

<script>
  document.getElementById('y').textContent=new Date().getFullYear();
  // Hours map (must mirror server-side hours)
  var HOURS={hours_js};
  var DAYNAMES={{0:'Zondag',1:'Maandag',2:'Dinsdag',3:'Woensdag',4:'Donderdag',5:'Vrijdag',6:'Zaterdag'}};
  var now=new Date();
  var d=now.getDay();
  var label=DAYNAMES[d];
  document.querySelectorAll('[data-day]').forEach(function(r){{
    if(r.dataset.day===label) r.classList.add('is-today');
  }});
  // Testimonial card carousel (rotates verified quotes)
  (function(){{
    var sec = document.querySelector('.atst');
    if(!sec) return;
    var data;
    try {{ data = JSON.parse((sec.dataset.testimonials||'[]').replace(/&quot;/g,'"')); }} catch(e){{ return; }}
    if(!Array.isArray(data) || data.length < 1) return;
    var dots = sec.querySelectorAll('.atst__dot');
    var name = sec.querySelector('.atst__name');
    var desg = sec.querySelector('.atst__designation');
    var quote = sec.querySelector('.atst__quote');
    var stars = sec.querySelector('[data-card-stars]');
    var idx = 0, timer;
    function paint(){{
      dots.forEach(function(d,i){{ if(i===idx) d.setAttribute('data-active','true'); else d.removeAttribute('data-active'); }});
      sec.classList.add('atst--changing');
      setTimeout(function(){{
        var t = data[idx]||{{}};
        if(name) name.textContent = t.name || '';
        if(desg) desg.textContent = t.designation || '';
        if(quote) quote.textContent = t.quote ? ('"' + t.quote + '"') : '';
        if(stars) {{ var s = (t.stars==null?5:t.stars); stars.style.width = (Math.max(0,Math.min(5,s))/5*100) + '%'; }}
        sec.classList.remove('atst--changing');
      }}, 200);
    }}
    function next(){{ idx=(idx+1)%data.length; paint(); restart(); }}
    function prev(){{ idx=(idx-1+data.length)%data.length; paint(); restart(); }}
    function restart(){{ clearTimeout(timer); timer=setTimeout(next, 7000); }}
    var pBtn = sec.querySelector('.atst__prev'), nBtn = sec.querySelector('.atst__next');
    if(pBtn) pBtn.addEventListener('click', prev);
    if(nBtn) nBtn.addEventListener('click', next);
    dots.forEach(function(d,i){{ d.addEventListener('click', function(){{ idx=i; paint(); restart(); }}); }});
    paint(); restart();
  }})();
  // Status badge
  document.querySelectorAll('[data-status]').forEach(function(el){{
    var t=HOURS[d];
    var hour=now.getHours()+now.getMinutes()/60;
    var txt='', cls='';
    if(!t || t.closed){{ txt='Vandaag gesloten'; cls='closed'; }}
    else if(hour>=t.open && hour<t.close){{ txt='Nu geopend · tot '+String(t.close).padStart(2,'0')+':00'; cls='open'; }}
    else if(hour<t.open){{ txt='Vandaag vanaf '+String(t.open).padStart(2,'0')+':00'; cls=''; }}
    else{{ txt='Voor vandaag gesloten'; cls='closed'; }}
    el.textContent=txt; if(cls) el.classList.add(cls);
  }});
</script>
</body>
</html>
"""


def hours_to_rows_html(hours):
    """Build a list of <div class="row" data-day="..."> rows."""
    if not hours:
        return ""
    return "\n        ".join(
        f'<div class="row" data-day="{day}"><span>{day}</span><span>{hrs}</span></div>'
        for day, hrs in hours
    )


def render(target):
    # Resolve per-branche defaults from BRANCHES table
    branche_cfg = BRANCHES.get(target.get("branche", ""), {})
    palette_key = target.get("palette") or branche_cfg.get("default_palette", "navy")
    pal = PALETTES[palette_key]
    default_icon = branche_cfg.get("service_icon_default", "scissors")
    schema_type = target.get("schema_type") or branche_cfg.get("schema_type", "LocalBusiness")
    if not target.get("branche_label") and branche_cfg.get("default_branche_label"):
        target["branche_label"] = branche_cfg["default_branche_label"]

    tel_raw = target.get("tel") or ""
    tel_link = re.sub(r"[^\d+]", "", tel_raw)
    tel_clean = tel_raw or (target.get("email") or "stuur een mail")
    tel_short = re.sub(r"^\+31\s?", "0", tel_clean) if tel_raw else (target.get("email", "Mail"))

    # service_cards (icon falls back to branche default)
    service_cards = "\n      ".join(
        f'<div class="svc"><span class="svc-icon">{ICONS.get(c.get("icon", default_icon), ICONS[default_icon])}</span><h3>{c["title"]}</h3><p>{c["body"]}</p></div>'
        for c in target["services"]
    )

    # tags
    tags_block = ""
    if target.get("tags"):
        tags_html = "".join(f'<span class="tag">{t}</span>' for t in target["tags"])
        tags_block = f'<div class="tag-row">{tags_html}</div>'

    # hours
    hours_html = hours_to_rows_html(target.get("hours"))
    if hours_html:
        hero_hours = hours_html
        hours_block = f'<div style="margin-top:.6rem;padding-top:.6rem;border-top:1px dashed var(--hairline)"><div style="font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;font-weight:700;color:var(--ink);opacity:.55;margin-bottom:.4rem">Openingstijden</div>{hours_html}</div>'
    else:
        hero_hours = '<p style="margin:0;font-size:.95rem;color:rgba(250,246,237,.78)">Bel voor afspraak: <strong>' + tel_clean + '</strong></p>'
        hours_block = '<div class="row"><span>Openingstijden</span><span>Bel voor afspraak</span></div>'

    email_row = (
        f'<div class="row"><span>E-mail</span><a href="mailto:{target["email"]}">{target["email"]}</a></div>'
        if target.get("email") else ""
    )

    socials = []
    if target.get("facebook"):
        socials.append(f'<a href="{target["facebook"]}" target="_blank" rel="noopener">Facebook</a>')
    if target.get("instagram"):
        socials.append(f'<a href="{target["instagram"]}" target="_blank" rel="noopener">Instagram</a>')
    socials_row = (
        f'<div class="row"><span>Online</span><span>{" · ".join(socials)}</span></div>'
        if socials else ""
    )

    lat, lon = target["lat"], target["lon"]
    delta = 0.005
    bbox = f"{lon - delta}%2C{lat - delta}%2C{lon + delta}%2C{lat + delta}"
    addr_q = urllib.parse.quote_plus(target["addr"])

    sources_label = ", ".join(target.get("sources", ["OSM"]))

    # Hero background image (stock placeholder)
    hero_bg_div = ""
    if target.get("hero_image"):
        url = pexels_url(target["hero_image"], w=1920)
        hero_bg_div = f'<div class="hero__bg" style="background-image:url(\'{url}\')" aria-hidden="true"></div>'

    # About image (stock placeholder — credit only in HTML alt)
    about_image_html = ""
    if target.get("about_image"):
        url = pexels_url(target["about_image"]["id"], w=900)
        about_image_html = (
            f'<div class="about-img"><img src="{url}" alt="Sfeerbeeld kapsalon" loading="lazy"></div>'
        )

    # Gallery section — clean 3×2 grid, no inline stock labels
    gallery_section = ""
    if target.get("gallery"):
        cells = []
        for item in target["gallery"]:
            url = pexels_url(item["id"], w=1200)
            label = item.get("label", "Sfeerbeeld")
            cells.append(
                f'<figure class="gallery__cell"><img src="{url}" alt="{label}" loading="lazy"></figure>'
            )
        cells_html = "\n      ".join(cells)
        gallery_section = f'''
<section class="alt" id="sfeerbeelden">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Sfeerbeelden</span>
      <h2>Een idee van wat je mag verwachten</h2>
      <hr class="divider">
    </div>
    <div class="gallery">
      {cells_html}
    </div>
  </div>
</section>'''

    # Monogram = first letter of meaningful word
    words = target["name"].split()
    monogram = words[-1][0].upper() if words else "·"

    # WhatsApp button (only if phone is mobile-style or explicitly enabled)
    whatsapp_button = ""
    sticky_wapp = ""
    wapp_fab_html = ""
    if target.get("whatsapp"):
        wa_link = f"https://wa.me/{target['whatsapp']}?text=Hallo!%20Ik%20wil%20graag%20een%20afspraak%20maken."
        wa_svg = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>'
        whatsapp_button = f'<a class="btn btn--whatsapp" href="{wa_link}" target="_blank" rel="noopener">{wa_svg} WhatsApp</a>'
        sticky_wapp = f'<a class="wapp" href="{wa_link}" target="_blank" rel="noopener">💬 WhatsApp</a>'
        wapp_fab_html = f'<a class="wapp-fab" href="{wa_link}" target="_blank" rel="noopener" aria-label="Chat met ons via WhatsApp" title="Chat via WhatsApp">{wa_svg}</a>'

    # Since badge
    since_badge_html = ""
    if target.get("since_year"):
        since_badge_html = f'<div style="margin-top:1.6rem"><span class="since-badge">Sinds {target["since_year"]} · {target.get("city","")}</span></div>'

    # Helper: real percentage star-fill (works for 5- and 10-point scales)
    def _rating_summary(rating):
        if not rating:
            return ""
        max_score = rating.get("max", 10 if rating.get("score", 0) > 5 else 5)
        pct = max(0, min(100, (rating["score"] / max_score) * 100))
        return (
            f'<div class="rating-summary">'
            f'<strong>{rating["score"]}</strong>'
            f'<span class="rs-stars" aria-label="{rating["score"]} van {max_score} sterren">'
            f'<span class="rs-stars__bg">★★★★★</span>'
            f'<span class="rs-stars__fg" style="width:{pct:.1f}%">★★★★★</span>'
            f'</span>'
            f'<small>{rating["count"]} beoordelingen op {rating["source"]}</small>'
            f'</div>'
        )

    # Reviews — animated carousel takes precedence over static grid if set
    reviews_section = ""
    if target.get("animated_testimonials"):
        atst_data = target["animated_testimonials"]
        rating_summary = _rating_summary(target.get("rating", {}))
        dots_html = "".join(f'<button class="atst__dot" data-i="{i}" aria-label="Ga naar review {i+1}"></button>' for i in range(len(atst_data)))
        atst_json = json.dumps(atst_data, ensure_ascii=False).replace('"', '&quot;')
        reviews_intro = target.get(
            "reviews_intro",
            "Verifieerbare citaten van klanten — letterlijk overgenomen uit publieke reviews.",
        )
        reviews_section = f'''
<section class="atst" id="klanten" data-testimonials="{atst_json}">
  <div class="atst__inner">
    <div class="atst__intro">
      <span class="eyebrow">Wat klanten zeggen</span>
      <h2>{target.get("reviews_heading", "Goede ervaringen, jaar in jaar uit")}</h2>
      <hr class="divider">
      <p class="atst__lead">{reviews_intro}</p>
      {rating_summary}
    </div>
    <div class="atst__card-wrap">
      <article class="atst__card">
        <div class="atst__card-stars" aria-hidden="true">
          <span class="rs-stars">
            <span class="rs-stars__bg">★★★★★</span>
            <span class="rs-stars__fg" data-card-stars style="width:100%">★★★★★</span>
          </span>
        </div>
        <blockquote class="atst__quote"></blockquote>
        <div class="atst__attribution">
          <span class="atst__name"></span>
          <span class="atst__designation"></span>
        </div>
      </article>
      <div class="atst__nav">
        <button class="atst__prev" aria-label="Vorige">←</button>
        <button class="atst__next" aria-label="Volgende">→</button>
        <div class="atst__dots" role="tablist">{dots_html}</div>
      </div>
    </div>
  </div>
</section>'''
    elif target.get("reviews"):
        review_cards = "\n      ".join(
            f'<article class="review"><div class="review__stars">{"★" * r["stars"]}{"☆" * (5 - r["stars"])}</div><blockquote class="review__text">"{r["text"]}"</blockquote><div class="review__author">— {r["author"]}</div></article>'
            for r in target["reviews"]
        )
        rating_summary = _rating_summary(target.get("rating", {}))
        reviews_section = f'''
<section id="klanten">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Wat klanten zeggen</span>
      <h2>{target.get("reviews_heading", "Goede ervaringen, jaar in jaar uit")}</h2>
      <hr class="divider">
      {rating_summary}
    </div>
    <div class="review-grid">
      {review_cards}
    </div>
  </div>
</section>'''

    # Steps section
    default_steps = [
        ("Bel of app even", "Snel een afspraak vastleggen — telefonisch of via WhatsApp."),
        ("Kom langs", "Op je gemak in de stoel — koffie of thee erbij."),
        ("Klaar voor de spiegel", "Tevreden naar buiten, verzorgd kapsel mee."),
    ]
    steps = target.get("steps") or default_steps
    steps_html = "\n      ".join(
        f'<div class="step"><h3>{s[0]}</h3><p>{s[1]}</p></div>' for s in steps
    )

    # Hours map for JS (must match Python source of truth)
    hours_js = "{}"
    if target.get("hours"):
        # Day mapping: Sun=0, Mon=1, ...
        hour_lookup = {h[0]: h[1] for h in target["hours"]}
        nl_to_idx = {"Zondag": 0, "Maandag": 1, "Dinsdag": 2, "Woensdag": 3, "Donderdag": 4, "Vrijdag": 5, "Zaterdag": 6}
        js_obj = {}
        for nl_name, idx in nl_to_idx.items():
            hrs = hour_lookup.get(nl_name, "Gesloten")
            if hrs.lower().strip() in ("gesloten", "closed", "ruhetag"):
                js_obj[idx] = {"closed": True}
            else:
                m = re.match(r"(\d+)(?::(\d+))?\s*[-–]\s*(\d+)(?::(\d+))?", hrs)
                if m:
                    open_h = int(m.group(1)) + (int(m.group(2)) / 60 if m.group(2) else 0)
                    close_h = int(m.group(3)) + (int(m.group(4)) / 60 if m.group(4) else 0)
                    js_obj[idx] = {"open": open_h, "close": close_h, "closed": False}
                else:
                    js_obj[idx] = {"closed": True}
        hours_js = json.dumps(js_obj)

    # Schema.org JSON-LD (type from BRANCHES, defaulting to LocalBusiness)
    schema = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": target["name"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": target["addr"],
            "addressLocality": target["city"],
            "addressCountry": "NL",
        },
        "telephone": tel_link,
        "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lon},
    }
    if target.get("since_year"):
        schema["foundingDate"] = str(target["since_year"])
    if target.get("rating"):
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": target["rating"]["score"],
            "bestRating": "10",
            "reviewCount": target["rating"]["count"],
        }
    schema_jsonld = json.dumps(schema, ensure_ascii=False)

    meta_description = target.get(
        "meta_description",
        f'{target["name"]} – {target["branche_label"]} aan de {target["addr"]}, {target["city"]}. Bel {tel_clean} voor een afspraak.',
    )

    html = PAGE_TEMPLATE.format(
        name=target["name"],
        monogram=monogram,
        hero_bg_div=hero_bg_div,
        about_image_html=about_image_html,
        gallery_section=gallery_section,
        city=target["city"],
        neighborhood=target.get("neighborhood") or target["city"],
        addr=target["addr"],
        tel_clean=tel_clean,
        tel_link=tel_link,
        tel_short=tel_short,
        branche_label=target["branche_label"],
        tagline_h1=target["tagline_h1"],
        lead=target["lead"],
        hero_hours=hero_hours,
        reviews_section=reviews_section,
        steps_html=steps_html,
        services_heading=target.get("services_heading", "Wat we voor je doen"),
        services_intro=target.get("services_intro", "Onze prijslijst hoor je het beste persoonlijk — bel ons voor een afspraak."),
        service_cards=service_cards,
        tags_block=tags_block,
        about_heading=target.get("about_heading", "Een vertrouwd adres"),
        about_body=target["about_body"],
        email_row=email_row,
        socials_row=socials_row,
        hours_block=hours_block,
        bbox=bbox,
        lat=lat,
        lon=lon,
        addr_q=addr_q,
        sources_label=sources_label,
        whatsapp_button=whatsapp_button,
        sticky_wapp=sticky_wapp,
        wapp_fab_html=wapp_fab_html,
        since_badge_html=since_badge_html,
        schema_jsonld=schema_jsonld,
        meta_description=meta_description,
        hours_js=hours_js,
        **pal,
    )

    slug = slugify(target["name"])
    out_dir = SITES / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"  built  sites/{slug}/index.html  ({len(html):,} chars)")
    target["_slug"] = slug
    return slug


# =============================================================================
# Public API
# =============================================================================
def render_all(
    targets: List[Dict[str, Any]],
    output_dir: str = "sites",
    port: int = 8912,
    csv_in: str | None = None,
    csv_out: str | None = None,
    base_dir: str = ".",
) -> None:
    """Render mockups for a list of targets and (optionally) update a CSV.

    Args:
        targets:    List of target dicts (data contract — see TARGET_EXAMPLE).
                    Each target must have already passed verify + activity-check.
        output_dir: Subfolder under base_dir where sites are written.
        port:       Port for the local URL emitted into results.csv.
        csv_in:     Optional source CSV with prospect rows (must contain `name`).
        csv_out:    Optional output CSV with new status/URL columns.
        base_dir:   Project root (defaults to current dir).

    Skip-categories the caller is expected to have already handled:
        - has_website   (verify step found a real site)
        - inactive_business (oozo step found inactive listing)
        - skipped_other (caller's choice)
    """
    global ROOT, SITES
    ROOT = Path(base_dir).resolve()
    SITES = ROOT / output_dir
    SITES.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(targets)} mockup(s) into {SITES}/ ...")
    built: Dict[str, str] = {}
    for t in targets:
        slug = render(t)
        built[t["name"]] = f"http://127.0.0.1:{port}/{output_dir}/{slug}/"

    if csv_in and csv_out:
        rows = list(csv.DictReader(open(ROOT / csv_in, encoding="utf-8")))
        extra_cols = ["verification_status", "found_url", "build_status", "local_url", "note"]
        fieldnames = list(rows[0].keys()) + [c for c in extra_cols if c not in rows[0].keys()]
        with open(ROOT / csv_out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in rows:
                if r["name"] in built:
                    r.setdefault("verification_status", "no_website")
                    r.setdefault("build_status", "built")
                    r["local_url"] = built[r["name"]]
                else:
                    r.setdefault("verification_status", "pending")
                    r.setdefault("build_status", "pending")
                    r.setdefault("local_url", "")
                for c in extra_cols:
                    r.setdefault(c, "")
                w.writerow(r)
        print(f"Wrote {ROOT / csv_out}")


# =============================================================================
# TARGET DATA CONTRACT — copy this dict, fill verified fields, run render_all().
# Anything optional can be omitted; section is then skipped gracefully.
# =============================================================================
TARGET_EXAMPLE: Dict[str, Any] = {
    # --- required ---
    "name":          "Bedrijfsnaam",
    "branche":       "kapper",          # key into BRANCHES (kapper|cafe|restaurant|...)
    "city":          "Nijmegen",
    "addr":          "Straatnaam 123",
    "tel":           "024 350 1735",
    "lat":           51.8254,
    "lon":           5.8439,
    "tagline_h1":    "Sinds 1996 — een begrip in <city>.",
    "lead":          "Korte intro op basis van directorytekst.",
    "about_body":    "Verhaal-paragraaf, alleen verifieerbare feiten.",
    "services":      [                  # 6-8 items recommended
        {"icon": "scissors", "title": "Knippen", "body": "Klassiek of modern."},
    ],

    # --- optional but strongly recommended ---
    "neighborhood":     "Wijk · Nijmegen",
    "branche_label":    "Dames-, heren- en kinderkapper",   # falls back to BRANCHES
    "palette":          "navy",                             # falls back to BRANCHES
    "since_year":       1996,
    "whatsapp":         "31243501735",  # E.164 without +
    "facebook":         "https://...",
    "instagram":        "https://...",
    "email":            "info@example.nl",
    "tags":             ["Dames", "Heren", "Kleur"],
    "hours":            [               # day → "9:00 – 18:00" / "Gesloten"
        ("Maandag", "Gesloten"),
        ("Dinsdag", "9:00 – 18:00"),
    ],
    "rating":           {"score": 7.2, "count": 9, "source": "Telefoonboek.nl"},
    "reviews":          [               # 1-3 real reviews, NEVER invent
        {"stars": 5, "text": "...", "author": "Naam · Bron"},
    ],
    "reviews_heading":  "Wat klanten zeggen",
    "steps":            [               # 3-step "hoe werkt het" section
        ("Bel of app even", "Snel een afspraak vastleggen."),
        ("Kom langs",       "Op je gemak in de stoel."),
        ("Klaar",           "Tevreden naar buiten."),
    ],
    "about_heading":    "Een vertrouwd adres",
    "services_heading": "Wat we voor je doen",
    "services_intro":   "Onze prijslijst hoor je het beste persoonlijk.",
    "meta_description": "...",
    "sources":          ["haar.expert", "telefoonboek.nl"],
    "schema_type":      "HairSalon",    # falls back to BRANCHES

    # --- stock photos (Pexels IDs only — placeholders, mention verbally in pitch) ---
    "hero_image":  18173343,
    "about_image": {"id": 19664875},
    "gallery": [                        # exactly 6 for the 3×2 grid
        {"id": 18173343, "label": "Salon-interieur"},
        {"id": 7697200,  "label": "Vakkundig gereedschap"},
        {"id": 32351050, "label": "Modern & precies"},
        {"id": 19664875, "label": "Voor jong en oud"},
        {"id": 18991957, "label": "Vertrouwde sfeer"},
        {"id": 30911662, "label": "Aandacht voor detail"},
    ],
}


if __name__ == "__main__":
    # Self-test: render the example target into ./demo-output/sites/
    print("Running self-test render with TARGET_EXAMPLE …")
    render_all(targets=[TARGET_EXAMPLE], output_dir="sites", base_dir="./demo-output")

