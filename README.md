# Flickr Image Export Album Organizer

Organizes an **official Flickr image export** by reconstructing your Flickr **albums as folders** and moving exported images and videos into the correct album directories.  
Any Flickr photos or videos that are **not assigned to an album** are placed into a **No Album** folder.

This script is designed specifically for **real-world Flickr image exports**, including very large archives split across many folders.

---

## Features

- Recursively scans **all subdirectories** of a Flickr export
- Recreates Flickr **albums as folders**
- Moves exported Flickr **images and videos** into their matching albums
- Places unassigned files into `Albums/No Album`
- Safe to re-run (no duplicates, idempotent)

---

## Works With Flickr Image Exports That:

- Split files across many `data-download-*` folders
- Store album and photo metadata JSON files in nested directories
- Do **not** preserve album structure on disk
- Rename files using Flickr photo IDs
- Include mixed media (JPEG, MP4, MOV, 3GP, etc.)

---

## Requirements

- Python 3.8+
- Official **Flickr image export**

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
```
## Output

After running, you will have:

Albums/
├── Vacation 2017/
├── Family/
├── Street Photography/
├── ...
└── No Album/


Each photo will exist in exactly one folder.

## Behavior Notes

Photos in multiple albums are moved to the first album encountered

Photos not listed in albums.json go to No Album

Files already moved are skipped on re-run

Only files matching Flickr’s _PHOTOID_o.jpg naming pattern are processed

## Why This Exists

Flickr’s official export does not preserve album structure on disk.
This script reconstructs that structure reliably, even for very large and fragmented exports.

## License

MIT
