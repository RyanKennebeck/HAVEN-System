# src/face_detector.py

import cv2
import numpy as np
import json

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

WATCHLIST_PATH = "data/watchlist.json"

# Load known faces from watchlist
try:
    with open(WATCHLIST_PATH, "r") as f:
        watchlist = json.load(f)
        known_encodings = [np.array(person["encoding"], dtype=np.float32) for person in watchlist]
        known_names = [person["name"] for person in watchlist]
except Exception as e:
    print(f"Error loading watchlist: {e}")
    known_encodings = []
    known_names = []

def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    detected_faces = []

    for (x, y, w, h) in faces:
        face_roi = gray[y : y + h, x : x + w]
        face_roi = cv2.resize(face_roi, (100, 100))
        hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()

        name = "Unknown"
        confidence = 0.0

        if known_encodings:
            sims = [cv2.compareHist(hist, enc.astype(np.float32), cv2.HISTCMP_CORREL) for enc in known_encodings]
            best_idx = int(np.argmax(sims))
            best_score = float(sims[best_idx])
            if best_score > 0.7:
                name = known_names[best_idx]
                confidence = best_score

        detected_faces.append({
            "box": (x, y, x + w, y + h),
            "id": name,
            "confidence": confidence
        })

    return detected_faces
