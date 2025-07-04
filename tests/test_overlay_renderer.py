import numpy as np
import cv2
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from overlay_renderer import draw_overlays

def test_plate_text_rendered(monkeypatch):
    frame = np.zeros((20, 20, 3), dtype=np.uint8)
    plate = {'box': (0, 0, 10, 10), 'text': 'ABC123', 'confidence': 0.9}
    captured = {}

    def fake_putText(img, text, org, fontFace, fontScale, color, thickness, lineType):
        captured['text'] = text
        return img

    # Monkeypatch OpenCV drawing functions to avoid actual rendering requirements
    monkeypatch.setattr(cv2, 'putText', fake_putText)
    monkeypatch.setattr(cv2, 'rectangle', lambda *args, **kwargs: None)
    monkeypatch.setattr(cv2, 'getTextSize', lambda *args, **kwargs: ((1, 1), None))

    draw_overlays(frame, plate, label='Plate')

    assert 'ABC123' in captured.get('text', '')
    assert 'Unknown' not in captured.get('text', '')
