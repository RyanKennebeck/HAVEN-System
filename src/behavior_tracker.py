# src/behavior_tracker.py

import cv2
import numpy as np

# Persistent frame buffer for motion detection
frame_buffer = []
BUFFER_SIZE = 5
MOTION_THRESHOLD = 50000  # total pixel difference area

def track_behavior(frame):
    behaviors = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    frame_buffer.append(gray)
    if len(frame_buffer) > BUFFER_SIZE:
        frame_buffer.pop(0)

    if len(frame_buffer) < 2:
        return behaviors  # Not enough history to compare

    delta = cv2.absdiff(frame_buffer[-1], frame_buffer[0])
    thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < MOTION_THRESHOLD:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        behaviors.append({
            "box": (x, y, x + w, y + h),
            "type": "Loitering",
            "score": 0.9
        })

    return behaviors
