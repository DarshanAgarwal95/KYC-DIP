# app.py (root)
import sys
import os

# Insert src to path so we can import modules by name
SRC = os.path.join(os.path.dirname(__file__), "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

import argparse

parser = argparse.ArgumentParser(description="KYC-DIP Launcher")
parser.add_argument("--streamlit", action="store_true", help="Run Streamlit demo")
parser.add_argument("--cli", action="store_true", help="Run CLI demo")
parser.add_argument("--image", type=str, help="Path to image for CLI processing")
args = parser.parse_args()

if args.streamlit:
    # Launch Streamlit app
    import subprocess
    subprocess.run(["streamlit", "run", "src/streamlit_app.py"])
elif args.cli:
    # simple CLI run
    from main_app import process_kyc_from_file
    if not args.image:
        print("Provide --image <path> for CLI")
        sys.exit(1)
    res = process_kyc_from_file(args.image, expected={"NAME":"Darshan Agarwal"})
    print("Extracted:", res['extracted'])
    print("Valid:", res['is_valid'])
else:
    print("No mode selected. Use --streamlit or --cli. Example:")
    print("  python app.py --streamlit   # run Streamlit demo")
    print("  python app.py --cli --image data/raw/sample.jpg  # run CLI on sample")
