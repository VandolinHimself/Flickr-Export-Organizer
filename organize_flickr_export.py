import json
import os
import re
import shutil

ROOT = os.getcwd()
ALBUM_ROOT = os.path.join(ROOT, "Albums")
NO_ALBUM_DIR = os.path.join(ALBUM_ROOT, "No Album")

photo_id_regex = re.compile(r"_([0-9]{8,})_o\.")

photo_files = {}

print("Scanning for photo files...")
for root, _, files in os.walk(ROOT):
    for name in files:
        match = photo_id_regex.search(name)
        if match:
            photo_id = match.group(1)
            full_path = os.path.join(root, name)
            photo_files.setdefault(photo_id, []).append(full_path)

print(f"Found {len(photo_files)} unique photo IDs")

albums_json = None
for root, _, files in os.walk(ROOT):
    for name in files:
        if name.lower() == "albums.json":
            albums_json = os.path.join(root, name)
            break

if not albums_json:
    raise RuntimeError("albums.json not found")

print(f"Using album metadata: {albums_json}")

with open(albums_json, "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, dict):
    if "albums" in data:
        albums = data["albums"]
    elif "sets" in data:
        albums = data["sets"]
    else:
        raise RuntimeError("albums.json structure not recognized")
elif isinstance(data, list):
    albums = data
else:
    raise RuntimeError("albums.json is not usable")

os.makedirs(ALBUM_ROOT, exist_ok=True)
os.makedirs(NO_ALBUM_DIR, exist_ok=True)

moved = 0
seen_files = set()
seen_ids = set()

for album in albums:
    if not isinstance(album, dict):
        continue

    album_name = album.get("title") or album.get("name") or "Untitled Album"
    album_name = album_name.strip() or "Untitled Album"

    album_dir = os.path.join(ALBUM_ROOT, album_name)
    os.makedirs(album_dir, exist_ok=True)

    photos = album.get("photos") or album.get("photo_ids") or []
    for photo in photos:
        if isinstance(photo, dict):
            photo_id = str(photo.get("id"))
        else:
            photo_id = str(photo)

        seen_ids.add(photo_id)

        for src in photo_files.get(photo_id, []):
            if src in seen_files:
                continue

            dst = os.path.join(album_dir, os.path.basename(src))
            if not os.path.exists(dst):
                shutil.move(src, dst)
                moved += 1
                seen_files.add(src)

print("Moving photos with no album...")

no_album_moved = 0
for photo_id, paths in photo_files.items():
    if photo_id in seen_ids:
        continue

    for src in paths:
        if src in seen_files:
            continue

        dst = os.path.join(NO_ALBUM_DIR, os.path.basename(src))
        if not os.path.exists(dst):
            shutil.move(src, dst)
            no_album_moved += 1
            seen_files.add(src)

print(f"\n✅ Done.")
print(f"Album photos moved: {moved}")
print(f"No-album photos moved: {no_album_moved}")
