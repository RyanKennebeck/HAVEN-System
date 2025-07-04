# src/watchlist_encoder.py

"""Utility for encoding faces from watchlist images.

This script scans the ``watchlist_images`` directory for images of people to
monitor. For each image it extracts a simple grayscale histogram
representation using OpenCV and stores the name and encoding in
``data/watchlist.json``.
"""

import json
import os
from pathlib import Path
from typing import List, Dict

import cv2

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

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    patterns = ["*.jpg", "*.jpeg", "*.png"]
    for pattern in patterns:
        for img_path in IMAGES_DIR.glob(pattern):
            image = cv2.imread(str(img_path))
            if image is None:
                print(f"Unable to read {img_path}")
                continue
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            if len(faces) == 0:
                print(f"No faces found in {img_path}")
                continue
            x, y, w, h = faces[0]
            face_roi = gray[y : y + h, x : x + w]
            face_roi = cv2.resize(face_roi, (100, 100))
            hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
            hist = cv2.normalize(hist, hist).flatten()
            name = img_path.stem
            encodings.append({"name": name, "encoding": hist.tolist()})

    return encodings


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    encodings = encode_watchlist()
    with open(OUTPUT_JSON, "w") as f:
        json.dump(encodings, f, indent=2)
    print(f"✅ Encoded {len(encodings)} faces to {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
