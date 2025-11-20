# src/preprocessing.py
import cv2
import numpy as np
from PIL import Image
import io

def pil_to_cv2(img_pil):
    """Convert PIL.Image (RGB) to OpenCV BGR"""
    img = np.array(img_pil)
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

def load_image_bytes_to_cv2(bytes_data):
    """Load bytes -> PIL -> cv2 BGR"""
    img_pil = Image.open(io.BytesIO(bytes_data)).convert("RGB")
    return pil_to_cv2(img_pil)

def preprocess_cv2(image_cv2, target_short_side=800):
    """
    Preprocess OpenCV image:
     - convert to gray
     - resize keeping aspect ratio (short side = target_short_side)
     - bilateral filter / denoise
     - adaptive threshold for OCR robustness
    """
    h, w = image_cv2.shape[:2]
    # Resize (short side to target_short_side)
    if min(h, w) != target_short_side:
        scale = target_short_side / min(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        image_cv2 = cv2.resize(image_cv2, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    gray = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
    denoised = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
    th = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)
    return th

