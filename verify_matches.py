import os
import glob
import pandas as pd

BASE_DIR = r"C:\Users\harunami\Desktop\helloworld"
CSV_PATH = os.path.join(BASE_DIR, "植栽データ_utf8_bom.csv")
ADDITIONAL_DIR = r"C:\Users\harunami\Desktop\helloworld\キャラクター画像\背景追加"

# Load CSV keys
try:
    df = pd.read_csv(CSV_PATH)
    csv_keys = set(df["樹木名"].values)
    print(f"Loaded {len(csv_keys)} tree names from CSV.")
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# Scan Additional Dir
files = []
for ext in ["*.png", "*.jpg", "*.jpeg"]:
    files.extend(glob.glob(os.path.join(ADDITIONAL_DIR, ext)))

print(f"Found {len(files)} files in additional dir.")

matched = []
unmatched = []

for f in files:
    name, _ = os.path.splitext(os.path.basename(f))
    if name in csv_keys:
        matched.append(name)
    else:
        unmatched.append(name)

print(f"Direct Matches: {len(matched)}")
print(f"Unmatched: {len(unmatched)}")
if unmatched:
    print(f"Sample unmatched: {unmatched[:10]}")
