#!/usr/bin/env python3
"""
Vervang externe img src door lokale webp + voeg width/height + loading=lazy toe.
Hero image (hero-onderzoek) blijft eager geladen, alle andere lazy.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

# (external URL substring, local path, width, height, eager-load?)
MAP = {
    "wp-content/uploads/sites/160/2025/05/Dierenkliniek-Pijnappel-Dierenfotograaf-Knap-Dier-36-scaled.jpg":
        ("images/hero-onderzoek.webp",            1600, 1067, True),
    "wp-content/uploads/sites/160/2025/12/Pijnappel_klein_20.jpg":
        ("images/team-teaser.webp",               1200, 1800, False),
    "wp-content/uploads/sites/160/2025/07/2.png":
        ("images/specialiteit-tandheelkunde.webp",1080, 1080, False),
    "wp-content/uploads/sites/160/2025/07/4.png":
        ("images/specialiteit-laser.webp",        1080, 1080, False),
    "wp-content/uploads/sites/160/2025/07/Ontwerp-zonder-titel-1.png":
        ("images/specialiteit-knie.webp",         1080, 1080, False),
    "wp-content/uploads/sites/160/2025/12/Pijnappel_klein_15.jpg":
        ("images/specialiteit-algemeen.webp",     1200, 800,  False),
    "wp-content/uploads/sites/160/2026/03/Gemini_Generated_Image_ocz5cnocz5cnocz5-e1772723593684.png":
        ("images/team-bouke.webp",                577,  577,  False),
    "wp-content/uploads/sites/160/2026/03/Maaike-e1772722480169.jpg":
        ("images/team-maaike.webp",               800,  798,  False),
    "wp-content/uploads/sites/160/2026/03/Miranda-e1772724477371.jpg":
        ("images/team-miranda.webp",              800,  800,  False),
    "wp-content/uploads/sites/160/2026/03/Pijnappel_origineel_02-scaled.jpg":
        ("images/team-hetty.webp",                800,  1200, False),
    "wp-content/uploads/sites/160/2026/03/Pijnappel_origineel_05-scaled.jpg":
        ("images/team-nancy.webp",                800,  1200, False),
    "wp-content/uploads/sites/160/2026/03/Pijnappel_origineel_06-scaled.jpg":
        ("images/team-yvonne.webp",               800,  1200, False),
    "wp-content/uploads/sites/160/2026/03/Pijnappel_origineel_07-scaled.jpg":
        ("images/team-renate.webp",               800,  1200, False),
    "wp-content/uploads/sites/160/2026/03/Pijnappel_origineel_08-scaled-e1772711480840.jpg":
        ("images/team-john.webp",                 800,  801,  False),
    "wp-content/uploads/sites/160/2026/03/Pijnappel_origineel_09-scaled.jpg":
        ("images/team-hester.webp",               800,  1200, False),
    "wp-content/uploads/sites/160/2026/03/Pijnappel_origineel_10-scaled.jpg":
        ("images/team-pollyanne.webp",            800,  1200, False),
    "wp-content/uploads/sites/160/2026/03/Pijnappel_origineel_12-scaled-e1772711400996.jpg":
        ("images/team-dagmar.webp",               800,  730,  False),
    "wp-content/uploads/sites/160/2026/03/Pijnappel_origineel_13-scaled-e1772711513474.jpg":
        ("images/team-yvonne-2.webp",             800,  801,  False),
    "wp-content/uploads/sites/160/2026/03/Pijnappel_origineel_14-scaled-e1772711345849.jpg":
        ("images/team-sofie.webp",                800,  796,  False),
    "wp-content/uploads/sites/160/2026/03/Saskia-e1772719699734.jpg":
        ("images/team-saskia.webp",               682,  683,  False),
}

# Local images: filename -> (width, height, eager?)
LOCAL_DIMS = {
    "images/pijnappel-logo.png":            (200,  200,  True),   # nav logo — above fold
    "images/knmvd.png":                     (200,  80,   False),
    "images/licg.png":                      (200,  80,   False),
    "images/wvt.jpg":                       (200,  80,   False),
    "images/scene-1-pixar.png":             (1024, 1024, False),
    "images/scene-2-pixar.png":             (1024, 1024, False),
    "images/scene-3-pixar.png":             (1024, 1024, False),
    "images/vet-dog-illustration.png":      (1024, 1024, False),
    "images/vet-dog-lego-illustration.png": (1024, 1024, False),
}

def rewrite_img_tag(tag: str) -> str:
    # Find src
    m = re.search(r'src="([^"]+)"', tag)
    if not m:
        return tag
    src = m.group(1)

    # Match external URL
    new_src = None
    w = h = None
    eager = False
    for frag, (local, ww, hh, eg) in MAP.items():
        if frag in src:
            new_src, w, h, eager = local, ww, hh, eg
            break

    # Local image lookup
    if new_src is None:
        for local, (ww, hh, eg) in LOCAL_DIMS.items():
            if src == local or src == "/" + local:
                w, h, eager = ww, hh, eg
                break

    if new_src:
        tag = tag.replace(src, new_src)

    if w and h:
        # Replace existing width/height to ensure intrinsic dims (overrides incorrect ones)
        tag = re.sub(r'\s+width="\d+"', '', tag)
        tag = re.sub(r'\s+height="\d+"', '', tag)
        tag = re.sub(r'(<img\b)', rf'\1 width="{w}" height="{h}"', tag, count=1)
        # loading attr
        if eager:
            tag = re.sub(r'\s*loading="lazy"', '', tag)
            tag = re.sub(r'\s*decoding="async"', ' decoding="async"', tag) if 'decoding=' in tag else tag
            if 'decoding=' not in tag:
                tag = re.sub(r'(<img\b)', r'\1 decoding="async"', tag, count=1)
        else:
            if 'loading=' not in tag:
                tag = re.sub(r'(<img\b)', r'\1 loading="lazy" decoding="async"', tag, count=1)

    return tag

IMG_RE = re.compile(r'<img\b[^>]*?/?>', re.DOTALL)

def process_file(path: Path) -> tuple[int, int]:
    text = path.read_text()
    count_changed = 0
    def repl(m):
        nonlocal count_changed
        original = m.group(0)
        new = rewrite_img_tag(original)
        if new != original:
            count_changed += 1
        return new
    new_text = IMG_RE.sub(repl, text)
    if new_text != text:
        path.write_text(new_text)
    total = len(IMG_RE.findall(text))
    return count_changed, total

if __name__ == "__main__":
    for f in sorted(ROOT.glob("*.html")):
        changed, total = process_file(f)
        print(f"{f.name}: {changed}/{total} img tags rewritten")
