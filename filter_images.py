#!/usr/bin/env python3
"""
Filter posts to those with images and keep only (post_title, image_url).
Works with your scraper outputs whether the title key is 'title' or 'post_title'.
"""

import json, os, sys
from pathlib import Path

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def is_image_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False
    # Accept common image extensions OR Reddit preview links (often have ?width=…)
    lowered = url.lower()
    return any(lowered.endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".gif", ".webp")) or "preview.redd.it" in lowered or "i.redd.it" in lowered

def filter_posts(rows):
    out = []
    seen = set()
    for r in rows if isinstance(rows, list) else []:
        url = r.get("image_url")
        if not is_image_url(url):
            continue
        title = r.get("post_title") or r.get("title") or "Untitled"
        key = (title, url)
        if key in seen:
            continue
        seen.add(key)
        out.append({"post_title": title, "image_url": url})
    return out

def main():
    if len(sys.argv) < 2:
        print("Usage: python filter_images.py <input_json> [output_json]")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    if not in_path.exists():
        print(f"Input file not found: {in_path}")
        sys.exit(1)

    # Default output path lives in output/ and is named like <input-stem>_images_only.json
    if len(sys.argv) >= 3:
        out_path = Path(sys.argv[2])
    else:
        out_dir = Path("output")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{in_path.stem}_images_only.json"

    data = load_json(in_path)
    filtered = filter_posts(data)

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)

    print(f"Kept {len(filtered)} posts with images")
    print(f"Saved to: {out_path}")

if __name__ == "__main__":
    main()
