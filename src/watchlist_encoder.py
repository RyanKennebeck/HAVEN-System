# src/watchlist_encoder.py

"""Utility for encoding faces from watchlist images.

This script scans the ``watchlist_images`` directory for images of people to
monitor. For each image it extracts face encodings using ``face_recognition``
and stores the name and encoding in ``data/watchlist.json``.
"""

import json
import os
from pathlib import Path
from typing import List, Dict

import face_recognition

DATA_DIR = Path("data")
IMAGES_DIR = DATA_DIR / "watchlist_images"
OUTPUT_JSON = DATA_DIR / "watchlist.json"


def encode_watchlist() -> List[Dict[str, object]]:
    """Generate face encodings for all images in ``IMAGES_DIR``.

    Returns
    -------
    List[Dict[str, object]]
        List of dictionaries containing ``name`` and ``encoding`` keys.
    """
    encodings = []
    if not IMAGES_DIR.exists():
        print(f"Watchlist image directory not found: {IMAGES_DIR}")
        return encodings

    patterns = ["*.jpg", "*.jpeg", "*.png"]
    for pattern in patterns:
        for img_path in IMAGES_DIR.glob(pattern):
            image = face_recognition.load_image_file(str(img_path))
            faces = face_recognition.face_encodings(image)
            if not faces:
                print(f"No faces found in {img_path}")
                continue
            name = img_path.stem
            encodings.append({"name": name, "encoding": faces[0].tolist()})

    return encodings


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    encodings = encode_watchlist()
    with open(OUTPUT_JSON, "w") as f:
        json.dump(encodings, f, indent=2)
    print(f"✅ Encoded {len(encodings)} faces to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
