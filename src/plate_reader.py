# src/plate_reader.py

import cv2
import pytesseract
from ultralytics import YOLO

# Load YOLOv8 model trained on license plates
yolo_plate_model = YOLO("models/yolov8_plate.pt")

# Configure pytesseract path if needed (Windows-specific)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def detect_plates(frame):
    results = yolo_plate_model(frame)
    plates = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])

            cropped = frame[y1:y2, x1:x2]
            gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            plate_text = pytesseract.image_to_string(gray, config='--psm 8').strip()

            if plate_text:
                plates.append({
                    "box": (x1, y1, x2, y2),
                    "text": plate_text,
                    "confidence": confidence
                })

    return plates
