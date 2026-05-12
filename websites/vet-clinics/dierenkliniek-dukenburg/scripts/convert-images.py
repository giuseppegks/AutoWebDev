#!/usr/bin/env python3
"""Download externe images, convert naar WebP, save met semantische namen."""
import urllib.request
from pathlib import Path
from PIL import Image
import io

BASE = "https://dierenkliniekpijnappel.nl/wp-content/uploads/sites/160"
OUT  = Path(__file__).parent.parent / "images"

# (source URL fragment, output filename, max width)
JOBS = [
    ("/2025/05/Dierenkliniek-Pijnappel-Dierenfotograaf-Knap-Dier-36-scaled.jpg", "hero-onderzoek.webp", 1600),
    ("/2025/12/Pijnappel_klein_20.jpg",                                          "team-teaser.webp",   1200),
    ("/2025/07/2.png",                                                           "specialiteit-tandheelkunde.webp", 1200),
    ("/2025/07/4.png",                                                           "specialiteit-laser.webp",          1200),
    ("/2025/07/Ontwerp-zonder-titel-1.png",                                      "specialiteit-knie.webp",           1200),
    ("/2025/12/Pijnappel_klein_15.jpg",                                          "specialiteit-algemeen.webp",       1200),
    ("/2026/03/Gemini_Generated_Image_ocz5cnocz5cnocz5-e1772723593684.png",      "team-bouke.webp",    800),
    ("/2026/03/Maaike-e1772722480169.jpg",                                       "team-maaike.webp",   800),
    ("/2026/03/Miranda-e1772724477371.jpg",                                      "team-miranda.webp",  800),
    ("/2026/03/Pijnappel_origineel_02-scaled.jpg",                               "team-hetty.webp",    800),
    ("/2026/03/Pijnappel_origineel_05-scaled.jpg",                               "team-nancy.webp",    800),
    ("/2026/03/Pijnappel_origineel_06-scaled.jpg",                               "team-yvonne.webp",   800),
    ("/2026/03/Pijnappel_origineel_07-scaled.jpg",                               "team-renate.webp",   800),
    ("/2026/03/Pijnappel_origineel_08-scaled-e1772711480840.jpg",                "team-john.webp",     800),
    ("/2026/03/Pijnappel_origineel_09-scaled.jpg",                               "team-hester.webp",   800),
    ("/2026/03/Pijnappel_origineel_10-scaled.jpg",                               "team-pollyanne.webp",800),
    ("/2026/03/Pijnappel_origineel_12-scaled-e1772711400996.jpg",                "team-dagmar.webp",   800),
    ("/2026/03/Pijnappel_origineel_13-scaled-e1772711513474.jpg",                "team-yvonne-2.webp", 800),
    ("/2026/03/Pijnappel_origineel_14-scaled-e1772711345849.jpg",                "team-sofie.webp",    800),
    ("/2026/03/Saskia-e1772719699734.jpg",                                       "team-saskia.webp",   800),
]

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 Safari/605.1.15"

def process(src_frag: str, out_name: str, max_w: int) -> None:
    out_path = OUT / out_name
    if out_path.exists():
        print(f"  [skip] {out_name} exists")
        return
    url = BASE + src_frag
    print(f"  [get ] {url}")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    img = Image.open(io.BytesIO(data))
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")
    if img.width > max_w:
        h = round(img.height * max_w / img.width)
        img = img.resize((max_w, h), Image.LANCZOS)
    img.save(out_path, "WEBP", quality=82, method=6)
    kb = out_path.stat().st_size / 1024
    print(f"  [save] {out_name}  {img.width}x{img.height}  {kb:.0f} KB")

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for src, name, w in JOBS:
        try:
            process(src, name, w)
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
