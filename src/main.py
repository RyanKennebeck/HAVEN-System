# src/main.py

import cv2
import datetime
import os
import json

from src.overlay_renderer import draw_overlays
from src.face_detector import detect_faces
from src.plate_reader import detect_plates
from src.behavior_tracker import track_behavior
from src.incident_reporter import generate_summary

LOG_PATH = "logs/events.csv"
INPUT_SOURCE = "input/test_footage.mp4"  # or 0 for webcam

def ensure_log_file():
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w") as f:
            f.write("timestamp,event_type,identifier,confidence\n")

def log_event(event_type, identifier, confidence):
    with open(LOG_PATH, "a") as f:
        timestamp = datetime.datetime.now().isoformat()
        f.write(f"{timestamp},{event_type},{identifier},{confidence:.2f}\n")

def main():
    ensure_log_file()
    cap = cv2.VideoCapture(INPUT_SOURCE)

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Face detection + overlay
        faces = detect_faces(frame)
        for face in faces:
            draw_overlays(frame, face, label="Face", color=(0, 255, 0))
            log_event("face", face["id"], face["confidence"])

        # License plate detection
        plates = detect_plates(frame)
        for plate in plates:
            draw_overlays(frame, plate, label="Plate", color=(255, 255, 0))
            log_event("plate", plate["text"], plate["confidence"])

        # Behavior tracking
        behaviors = track_behavior(frame)
        for behavior in behaviors:
            draw_overlays(frame, behavior, label=behavior["type"], color=(0, 0, 255))
            log_event("behavior", behavior["type"], behavior["score"])

        # Show HUD preview
        cv2.imshow("HAVEN Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Auto-generate incident summary
    generate_summary()

if __name__ == "__main__":
    main()
