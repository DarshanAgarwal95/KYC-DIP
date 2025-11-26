# src/streamlit_app.py
import streamlit as st
from main_app import process_kyc_from_file
from visualize import cv2_to_pil
from PIL import Image
import io

st.set_page_config(page_title="KYC-DIP Demo", layout="wide")
st.title("KYC Document Intelligence Platform (KYC-DIP) — Demo (EasyOCR only)")

col1, col2 = st.columns([1,1])
with col1:
    uploaded = st.file_uploader("sUpload KYC Document (image)", type=['png','jpg','jpeg'])
    st.write("Example expected data (for validation)")
    name = st.text_input("Expected NAME", value="")
    pan = st.text_input("Expected PAN", value="")
    dob = st.text_input("Expected DOB (DD-MM-YYYY)", value="")
    run_btn = st.button("Run KYC")

with col2:
    st.write("Results")
    result_area = st.empty()
    image_area = st.empty()

if uploaded and run_btn:
    data = uploaded.read()
    expected = {"NAME": name, "PAN": pan, "DOB": dob}
    with st.spinner("Processing... OCR + Extraction + Validation"):
        res = process_kyc_from_file(data, expected=expected)
    # Show text
    st.subheader("Extracted Text (first 800 chars)")
    st.text(res['text'][:800])

    st.subheader("Extracted Fields")
    st.json(res['extracted'])

    st.subheader("Validation")
    if res['is_valid']:
        st.success("KYC VALIDATED ✅")
    else:
        st.error("KYC MISMATCH ❌")
        st.json(res['mismatches'])

    # Show highlighted image
    highlighted_cv2 = res['highlighted_image']
    pil_img = cv2_to_pil(highlighted_cv2)
    st.subheader("Highlighted Entities")
    st.image(pil_img, use_column_width=True)
    


