# src/face_detector.py

import face_recognition
import cv2
import numpy as np
import json

WATCHLIST_PATH = "data/watchlist.json"

# Load known faces from watchlist
try:
    with open(WATCHLIST_PATH, "r") as f:
        watchlist = json.load(f)
        known_encodings = [np.array(person["encoding"]) for person in watchlist]
        known_names = [person["name"] for person in watchlist]
except Exception as e:
    print(f"Error loading watchlist: {e}")
    known_encodings = []
    known_names = []

def detect_faces(frame):
    rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    detected_faces = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"
        confidence = 0.0

        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]
            confidence = 0.99  # face_recognition doesn't provide actual confidence, so this is symbolic

        detected_faces.append({
            "box": (left, top, right, bottom),
            "id": name,
            "confidence": confidence
        })

    return detected_faces
