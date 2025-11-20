# src/validation.py
def simple_match(expected, candidates):
    if not expected:
        return False
    exp = str(expected).lower().strip()
    for c in candidates:
        if exp in str(c).lower():
            return True
    return False

def validate_entities(extracted, expected):
    """
    extracted: dict from extract_all
    expected: dict e.g. {"NAME": "Darshan Agarwal", "PAN": "ABCDE1234F", "DOB": "1994-12-01"}
    Returns: (is_valid(bool), mismatches(dict))
    """
    mismatches = {}
    # NAME
    if "NAME" in expected:
        ok = simple_match(expected["NAME"], extracted.get("NAMES", []))
        if not ok:
            mismatches["NAME"] = {"expected": expected["NAME"], "extracted": extracted.get("NAMES", [])}

    # PAN
    if "PAN" in expected:
        ok = simple_match(expected["PAN"], extracted.get("PAN", []))
        if not ok:
            mismatches["PAN"] = {"expected": expected["PAN"], "extracted": extracted.get("PAN", [])}

    # DOB
    if "DOB" in expected:
        ok = simple_match(expected["DOB"], extracted.get("DATES", []))
        if not ok:
            mismatches["DOB"] = {"expected": expected["DOB"], "extracted": extracted.get("DATES", [])}

    return len(mismatches) == 0, mismatches

