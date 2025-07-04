# src/alert_manager.py

import cv2

# Draw a flashing alert box on the frame

def draw_alert(frame, text, color=(0, 0, 255), thickness=3):
    h, w = frame.shape[:2]
    overlay = frame.copy()

    # Flashing border
    cv2.rectangle(overlay, (10, 10), (w - 10, h - 10), color, thickness)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Centered alert text
    font_scale = 1.2
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, 2)
    x = int((w - text_width) / 2)
    y = int(h / 8)

    cv2.putText(
        frame,
        text,
        (x, y),
        font,
        font_scale,
        color,
        2,
        cv2.LINE_AA
    )

    return frame
