import os
import glob
import pandas as pd

# Paths
IMG_DIR = r"C:\Users\harunami\Desktop\helloworld\キャラクター画像\背景追加"
CSV_PATH = r"C:\Users\harunami\Desktop\helloworld\植栽データ_utf8_bom.csv"

# Load CSV
try:
    df = pd.read_csv(CSV_PATH, encoding='utf-8-sig', index_col=0)
    csv_names = set(df.index)
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# Get Images
image_files = glob.glob(os.path.join(IMG_DIR, "*.*"))
file_tree_names = []

print(f"--- Images in {os.path.basename(IMG_DIR)} ---")
for f in image_files:
    # Basic filename extraction
    basename = os.path.basename(f)
    name_no_ext = os.path.splitext(basename)[0]
    file_tree_names.append(name_no_ext)
    print(f"- {name_no_ext}")

print("\n--- Missing Data (In Folder but Not in CSV) ---")
missing_count = 0
for name in file_tree_names:
    # Logic from generate_web.py: exact match or parenthesis match
    # generate_web.py logic:
    # 1. Exact match
    # 2. Split by '（' and check first part
    
    match_found = False
    if name in csv_names:
        match_found = True
    else:
        # Try cleaning parentheses (e.g. "ツツジ（オオムラサキ）" -> "ツツジ")
        if '（' in name:
            clean_name = name.split('（')[0]
            if clean_name in csv_names:
                match_found = True
                # print(f"  (Matched '{name}' as '{clean_name}')")

    if not match_found:
        print(f"- {name}")
        missing_count += 1

if missing_count == 0:
    print("(None - All images have data)")
