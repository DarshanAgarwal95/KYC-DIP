# src/entity_extraction.py
import re
from dateutil  import parser as dateparser

def extract_pan(text):
    # PAN pattern: 5 letters + 4 digits + 1 letter
    # Many PANs are uppercase; remove spaces to match patterns
    cleaned = text.replace(" ", "").upper()
    matches = re.findall(r'\b[A-Z]{5}[0-9]{4}[A-Z]\b', cleaned)
    return matches

def extract_aadhaar(text):
    # Aadhaar: 12 digits possibly with spaces
    matches = re.findall(r'\b\d{4}\s?\d{4}\s?\d{4}\b', text)
    return matches

def extract_dates(text):
    # find simple date formats and parse
    candidates = re.findall(r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b', text)
    parsed = []
    for c in candidates:
        try:
            d = dateparser.parse(c, dayfirst=True)
            parsed.append(d.date().isoformat())
        except Exception:
            pass
    return parsed

def extract_names_simple(text):
    """
    Heuristic: look for 'Name' label or two capitalized words
    """
    # look for Name: pattern
    name_patterns = re.findall(r'(?:Name|NAME|Holder Name|Applicant Name|S/o|D/o|C/o)[:\s]*([A-Za-z\s]{2,60})', text)
    if name_patterns:
        return [n.strip() for n in name_patterns if n.strip()]

    # fallback: two capitalized words
    capital_pairs = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b', text)
    if capital_pairs:
        return [capital_pairs[0]]

    return []

def extract_all(text):
    return {
        "PAN": extract_pan(text),
        "AADHAAR": extract_aadhaar(text),
        "DATES": extract_dates(text),
        "NAMES": extract_names_simple(text)
    }

