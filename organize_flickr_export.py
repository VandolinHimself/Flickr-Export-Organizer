import json
import os
import re
import shutil

ROOT = os.getcwd()
ALBUM_ROOT = os.path.join(ROOT, "Albums")
NO_ALBUM_DIR = os.path.join(ALBUM_ROOT, "No Album")

IMAGE_EXTS = ("jpg", "jpeg", "png", "gif")
VIDEO_EXTS = (
    "mp4", "mov", "m4v", "avi", "mkv", "webm",
    "3gp", "3g2", "mts", "m2ts"
)
ALL_EXTS = IMAGE_EXTS + VIDEO_EXTS

photo_id_regex = re.compile(
    r"_([0-9]{8,})_o\.(%s)$" % "|".join(ALL_EXTS),
    re.IGNORECASE
)

photo_files = {}
all_media_files = set()

print("Scanning for media files...")

for root, _, files in os.walk(ROOT):
    if root.startswith(ALBUM_ROOT):
        continue

    for name in files:
        ext = name.lower().split(".")[-1]
        if ext not in ALL_EXTS:
            continue

        full_path = os.path.join(root, name)
        all_media_files.add(full_path)

        match = photo_id_regex.search(name)
        if match:
            photo_id = match.group(1)
            photo_files.setdefault(photo_id, []).append(full_path)

print(f"Found {len(photo_files)} ID-linked items")
print(f"Found {len(all_media_files)} total media files")

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
    albums = data.get("albums") or data.get("sets")
elif isinstance(data, list):
    albums = data
else:
    raise RuntimeError("albums.json format not recognized")

if not albums:
    raise RuntimeError("No albums found")

os.makedirs(ALBUM_ROOT, exist_ok=True)
os.makedirs(NO_ALBUM_DIR, exist_ok=True)

seen_files = set()
seen_ids = set()
album_moved = 0
no_album_moved = 0
orphan_moved = 0

# --- Album pass ---
for album in albums:
    if not isinstance(album, dict):
        continue

    album_name = album.get("title") or album.get("name") or "Untitled Album"
    album_name = album_name.strip() or "Untitled Album"

    album_dir = os.path.join(ALBUM_ROOT, album_name)
    os.makedirs(album_dir, exist_ok=True)

    photos = album.get("photos") or album.get("photo_ids") or []

    for photo in photos:
        photo_id = str(photo.get("id") if isinstance(photo, dict) else photo)
        seen_ids.add(photo_id)

        for src in photo_files.get(photo_id, []):
            if src in seen_files:
                continue

            dst = os.path.join(album_dir, os.path.basename(src))
            if not os.path.exists(dst):
                shutil.move(src, dst)
                album_moved += 1
                seen_files.add(src)

# --- No-album (ID-known) pass ---
print("Moving known no-album media...")

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

# --- FINAL ORPHAN SWEEP (THIS FIXES 3GP ISSUES) ---
print("Moving orphan media (no ID, no album)...")

for src in all_media_files:
    if src in seen_files:
        continue
    if not os.path.exists(src):
        continue

    dst = os.path.join(NO_ALBUM_DIR, os.path.basename(src))
    if not os.path.exists(dst):
        shutil.move(src, dst)
        orphan_moved += 1

print("\n✅ COMPLETE")
print(f"Album media moved: {album_moved}")
print(f"No-album (ID) media moved: {no_album_moved}")
print(f"Orphan media moved: {orphan_moved}")
