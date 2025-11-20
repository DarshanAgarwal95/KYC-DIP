# src/main_app.py
import io
from preprocessing import load_image_bytes_to_cv2, preprocess_cv2
from ocr import ocr_from_cv2
from entity_extraction import extract_all
from validation import validate_entities
from visualize import draw_boxes

def process_single_image_bytes(bytes_data, expected=None):
    """
    Process a single image (bytes) and return structured result.
    expected: dict for validation e.g. {"NAME":"Darshan Agarwal","PAN":"ABCDE1234F","DOB":"1994-12-01"}
    """
    # Load image (bytes -> cv2)
    img_cv2 = load_image_bytes_to_cv2(bytes_data)
    preprocessed = preprocess_cv2(img_cv2)
    text, boxes = ocr_from_cv2(preprocessed)
    extracted = extract_all(text)
    is_valid, mismatches = validate_entities(extracted, expected or {})

    # Map boxes to labels using simple matching against extracted candidates
    boxes_with_label = []
    for b in boxes:
        txt = b.get('text','').upper()
        label = 'OTHER'
        if any(pan in txt for pan in [p.replace(" ", "") for p in extracted.get('PAN', [])]):
            label = 'PAN'
        elif any(aad in txt for aad in extracted.get('AADHAAR', [])):
            label = 'AADHAAR'
        elif any(name.upper() in txt for name in extracted.get('NAMES', [])):
            label = 'NAME'
        boxes_with_label.append({'box': b['box'], 'label': label})

    highlighted = draw_boxes(preprocessed if preprocessed is not None else img_cv2, boxes_with_label)

    return {
        "text": text,
        "extracted": extracted,
        "is_valid": is_valid,
        "mismatches": mismatches,
        "highlighted_image": highlighted  # OpenCV image; caller may convert to PIL for display
    }

def process_kyc_from_file(path_or_bytes, expected=None):
    """
    Accepts either bytes or path string to image.
    """
    if isinstance(path_or_bytes, str):
        with open(path_or_bytes, "rb") as f:
            data = f.read()
    else:
        data = path_or_bytes
    return process_single_image_bytes(data, expected=expected)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.main_app <image_path>")
        sys.exit(1)
    path = sys.argv[1]
    res = process_kyc_from_file(path, expected={"NAME":"Darshan Agarwal"})
    print("Extracted:", res['extracted'])
    print("Valid:", res['is_valid'])
