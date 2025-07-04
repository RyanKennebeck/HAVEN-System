# src/overlay_renderer.py

import cv2

def draw_overlays(frame, obj, label="Object", color=(0, 255, 255)):
    if "box" not in obj:
        return

    left, top, right, bottom = obj["box"]
    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

    text = f"{label}: {obj.get('id', 'Unknown')} ({obj.get('confidence', 0):.2f})"
    (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

    cv2.rectangle(frame, (left, top - text_height - 10), (left + text_width, top), color, -1)
    cv2.putText(
        frame,
        text,
        (left, top - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 0),
        1,
        cv2.LINE_AA
    )
