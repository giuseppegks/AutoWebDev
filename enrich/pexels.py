"""pexels.py — Pexels API client + per-branche photo cache.

Setup (one-time, free):
    1. Sign up at https://www.pexels.com/api/
    2. Get your API key
    3. Export it:  export PEXELS_API_KEY="your-key-here"
                   (or add to ~/.zshrc / ~/.bashrc)

Free tier: 200 requests/hour, unlimited photos.

This module:
- Searches Pexels per branche keyword (from BRANCHES table)
- Picks 12 photos with mixed orientations (hero=landscape, about=portrait, gallery=square-ish)
- Caches per query to JSON so we don't re-fetch on every run
- Each photo carries: id, url variants, photographer, photographer_url (for credit)
- Honesty: if API key is missing, returns empty list with warning — never makes up IDs

Output shape per photo:
    {
      "id": 18173343,
      "url_large": "https://images.pexels.com/photos/18173343/pexels-photo-18173343.jpeg?auto=compress&cs=tinysrgb&w=1600",
      "url_medium": "...?w=1200",
      "url_small": "...?w=600",
      "alt": "Stylish barbershop interior featuring iconic red leather chairs",
      "width": 6000, "height": 4000,
      "orientation": "landscape" | "portrait" | "square",
      "photographer": "Pixabay",
      "photographer_url": "https://www.pexels.com/@pixabay",
    }
"""

from __future__ import annotations
import os
import json
import urllib.request
import urllib.parse
import urllib.error
import time
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

PEXELS_API = "https://api.pexels.com/v1/search"
CACHE_DIR = Path("~/.cache/autowebdev-enrich/pexels").expanduser()


def _api_key() -> Optional[str]:
    return os.environ.get("PEXELS_API_KEY") or os.environ.get("PEXELS_KEY")


def _cache_path(query: str, per_page: int) -> Path:
    safe = urllib.parse.quote(query.lower(), safe="")[:80]
    return CACHE_DIR / f"{safe}__{per_page}.json"


def _orient(w: int, h: int) -> str:
    if w > h * 1.2:
        return "landscape"
    if h > w * 1.2:
        return "portrait"
    return "square"


def _to_record(photo: Dict[str, Any]) -> Dict[str, Any]:
    src = photo.get("src", {})
    base = src.get("original", "")
    # Pexels supports sizing via query params on the URL; build sensible variants
    return {
        "id": photo["id"],
        "url_large":  f"{base}?auto=compress&cs=tinysrgb&w=1600",
        "url_medium": f"{base}?auto=compress&cs=tinysrgb&w=1200",
        "url_small":  f"{base}?auto=compress&cs=tinysrgb&w=600",
        "alt": photo.get("alt", ""),
        "width": photo["width"],
        "height": photo["height"],
        "orientation": _orient(photo["width"], photo["height"]),
        "photographer": photo.get("photographer", "Pexels"),
        "photographer_url": photo.get("photographer_url", "https://www.pexels.com/"),
    }


def search(query: str, *, per_page: int = 12, max_age_days: int = 30) -> List[Dict[str, Any]]:
    """Search Pexels for `query`, returning normalized photo records.

    Result is cached to disk for `max_age_days` days. Subsequent calls are
    instant. Returns [] if API key missing (with stderr warning).
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = _cache_path(query, per_page)

    # Cache hit
    if cache.exists() and (time.time() - cache.stat().st_mtime) < max_age_days * 86400:
        return json.loads(cache.read_text())

    # Need to call the API
    key = _api_key()
    if not key:
        print(
            "  ⚠️  pexels: PEXELS_API_KEY env var not set — skipping photo fetch.\n"
            "     Get a free key at https://www.pexels.com/api/ then:\n"
            "     export PEXELS_API_KEY='your-key-here'",
            file=sys.stderr,
        )
        return []

    url = f"{PEXELS_API}?query={urllib.parse.quote_plus(query)}&per_page={per_page}"
    req = urllib.request.Request(url, headers={
        "Authorization": key,
        "User-Agent": "AutoWebDev-enrich/1.0 (+https://github.com/giuseppegks/AutoWebDev)",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            print(f"  ⚠️  pexels: API key rejected ({e.code} {e.reason})", file=sys.stderr)
            return []
        if e.code == 429:
            print("  ⚠️  pexels: rate-limited (429), try again in an hour", file=sys.stderr)
            return []
        raise
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"  ⚠️  pexels: network error — {e}", file=sys.stderr)
        return []

    photos = [_to_record(p) for p in data.get("photos", [])]
    cache.write_text(json.dumps(photos, indent=2, ensure_ascii=False))
    return photos


def for_branche(branche_key: str, *, per_page: int = 12) -> List[Dict[str, Any]]:
    """Fetch photos for a BRANCHES table key (e.g. "kapper", "cafe", "dakdekker").

    Reads the BRANCHES dict from the building-prospect-mockups skill if importable;
    otherwise uses a small built-in fallback table.
    """
    # Try to import from the skill (if installed in ~/.claude/skills)
    try:
        sys.path.insert(0, str(Path("~/.claude/skills/building-prospect-mockups").expanduser()))
        from template_generator import BRANCHES  # type: ignore
        keyword = BRANCHES.get(branche_key, {}).get("pexels_keyword")
    except (ImportError, FileNotFoundError):
        keyword = None

    if not keyword:
        # Fallback: friendly defaults for common branches
        FALLBACK = {
            "kapper": "barbershop",
            "cafe": "cafe interior",
            "restaurant": "restaurant interior",
            "bar": "cocktail bar",
            "bakkerij": "bakery bread",
            "slager": "butcher shop",
            "schoonheidssalon": "beauty salon",
            "bloemist": "flower shop",
            "fysio": "physiotherapy clinic",
            "tandarts": "dental clinic",
            "garage": "auto mechanic shop",
            "boekhandel": "independent bookstore",
            "apotheek": "pharmacy interior",
            "dakdekker": "roofer roof construction",
            "cheese": "cheese shop",
            "jewelry": "jewelry boutique",
            "music": "vinyl record store",
            "furniture": "vintage furniture shop",
            "clothes": "clothing boutique interior",
            "alcohol": "craft beer shop",
        }
        keyword = FALLBACK.get(branche_key, branche_key)

    return search(keyword, per_page=per_page)


def pick_for_template(photos: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Choose hero (landscape), about (portrait), and 6 gallery photos.

    Returns:
        {
          "hero_image": <pexels-id>,
          "about_image": {"id": <id>, "credit": "Photographer"},
          "gallery": [{"id": ..., "label": "..."}, x6],
        }

    If not enough photos for a category, falls back to whatever's available.
    """
    if not photos:
        return {}

    landscape = [p for p in photos if p["orientation"] == "landscape"]
    portrait = [p for p in photos if p["orientation"] == "portrait"]
    others = [p for p in photos if p["orientation"] == "square"]
    pool_for_gallery = landscape + others + portrait

    out: Dict[str, Any] = {}
    if landscape:
        out["hero_image"] = landscape[0]["id"]
    elif photos:
        out["hero_image"] = photos[0]["id"]

    if portrait:
        p = portrait[0]
    elif len(photos) > 1:
        p = photos[1]
    else:
        p = photos[0]
    out["about_image"] = {"id": p["id"], "credit": p.get("photographer", "Pexels")}

    # 6 distinct gallery photos, prefer landscape first
    used_ids = {out.get("hero_image"), p["id"]}
    gallery = []
    for cand in pool_for_gallery:
        if cand["id"] in used_ids:
            continue
        gallery.append({
            "id": cand["id"],
            "label": (cand.get("alt", "Sfeerbeeld")[:40].strip() or "Sfeerbeeld"),
        })
        used_ids.add(cand["id"])
        if len(gallery) >= 6:
            break
    out["gallery"] = gallery
    return out


# --------------------------------------------------------------------------- CLI
if __name__ == "__main__":
    if not _api_key():
        print("Set PEXELS_API_KEY first.")
        sys.exit(1)

    branche = sys.argv[1] if len(sys.argv) > 1 else "kapper"
    print(f"Fetching photos for branche: {branche}…")
    photos = for_branche(branche)
    print(f"  → {len(photos)} photos")
    selection = pick_for_template(photos)
    print(json.dumps(selection, indent=2, ensure_ascii=False))
