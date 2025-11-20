# src/ocr.py
import easyocr
import numpy as np
from PIL import Image
import cv2

# Lazy init of EasyOCR reader
_reader = None
def get_easyocr_reader(langs=["en"]):
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(langs, gpu=False)  # set gpu=True if you have CUDA & installed
    return _reader

def ocr_from_cv2(image_cv2):
    """
    Run EasyOCR on image_cv2 (grayscale or BGR).
    Returns (text, boxes)
    boxes: list of {'box': [[x1,y1]..[x4,y4]], 'text': '...', 'conf': float}
    """
    reader = get_easyocr_reader()
    # EasyOCR expects RGB array
    if len(image_cv2.shape) == 2:
        arr = cv2.cvtColor(image_cv2, cv2.COLOR_GRAY2RGB)
    else:
        arr = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)

    results = reader.readtext(arr, detail=1)
    texts = []
    boxes = []
    for bbox, text, conf in results:
        texts.append(text)
        boxes.append({'box': bbox, 'text': text, 'conf': float(conf)})
    joined_text = " ".join(texts)
    return joined_text, boxes
