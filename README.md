# Flickr Export Album Organizer

Organizes a **Flickr official data export** by recreating your Flickr **albums as folders** and moving photos into them.  
Photos that are not part of any album are placed into a **No Album** folder.

This script is built specifically to handle Flickr’s real-world export behavior, including very large archives.

---

## Features

- Recursively scans **all subdirectories**
- Recreates Flickr albums as folders
- Moves photos into their corresponding albums
- Places unassigned photos into `Albums/No Album`
- Works with **70,000+ photos**
- Safe to re-run (no duplicates)
- No API keys, no login, no external dependencies

---

## Works With Flickr Exports That:

- Split photos across many `data-download-*` folders
- Store metadata JSON files in nested directories
- Do not preserve album structure
- Rename files using Flickr photo IDs

---

## Requirements

- Python 3.8+
- Official Flickr data export
- Linux / macOS / WSL (Windows via WSL recommended)

---

## Expected Directory Layout

Before running:

Flickr/
├── data-download-1/
├── data-download-2/
├── 7215772..._part1/
│ ├── albums.json
│ └── photos_comments_part001.json
└── organize_flickr_export.py

yaml
Copy code

The script will automatically locate `albums.json` anywhere under the root directory.

---

## Usage

1. Place `organize_flickr_export.py` in the **root** of your Flickr export
2. Run:

```bash
python3 organize_flickr_export.py
That’s it.

Output
After running, you will have:

yaml
Copy code
Albums/
├── Vacation 2017/
├── Family/
├── Street Photography/
├── ...
└── No Album/
Each photo will exist in exactly one folder.

Behavior Notes
Photos in multiple albums are moved to the first album encountered

Photos not listed in albums.json go to No Album

Files already moved are skipped on re-run

Only files matching Flickr’s _PHOTOID_o.jpg naming pattern are processed

Why This Exists
Flickr’s official export does not preserve album structure on disk.
This script reconstructs that structure reliably, even for very large and fragmented exports.

License
MIT

sql
Copy code

If you want, I can also:
- Add a `--dry-run` flag
- Add a progress bar
- Add a copy-instead-of-move option
- Add filesystem-safe album name normalization

Just say the word.
