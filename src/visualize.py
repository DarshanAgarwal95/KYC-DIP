# src/visualize.py
import cv2
import numpy as np
from PIL import Image

COLOR_MAP = {'NAME': (255, 0, 0), 'PAN': (0, 255, 0), 'AADHAAR': (0, 0, 255), 'OTHER': (0,255,255)}

def box_to_rect(box):
    # box: list of 4 points [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
    xs = [int(p[0]) for p in box]
    ys = [int(p[1]) for p in box]
    x1, y1 = min(xs), min(ys)
    x2, y2 = max(xs), max(ys)
    return (x1, y1, x2, y2)

def draw_boxes(image_cv2, boxes_with_label):
    img = image_cv2.copy()
    for item in boxes_with_label:
        box = item.get('box')
        label = item.get('label', 'OTHER')
        x1,y1,x2,y2 = box_to_rect(box)
        color = COLOR_MAP.get(label, (0,255,255))
        cv2.rectangle(img, (x1,y1), (x2,y2), color, 2)
        cv2.putText(img, label, (x1, max(10,y1-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return img

def cv2_to_pil(image_cv2):
    if len(image_cv2.shape) == 2:
        arr = image_cv2
    else:
        arr = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)
    return Image.fromarray(arr)
