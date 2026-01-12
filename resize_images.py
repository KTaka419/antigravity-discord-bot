from PIL import Image
import os
import glob

source_dir = r"C:\Users\harunami\Desktop\helloworld\temp_ascii"
dest_dir = r"C:\Users\harunami\Desktop\helloworld\temp_resized"

# 対応する拡張子
exts = ['*.png', '*.jpg', '*.jpeg']
files = []
for ext in exts:
    files.extend(glob.glob(os.path.join(source_dir, ext)))

for file_path in files:
    try:
        filename = os.path.basename(file_path)
        name, _ = os.path.splitext(filename)
        # JPEGとして保存（透過情報がある場合は白背景にする）
        with Image.open(file_path) as img:
            img = img.convert("RGB")
            # 長辺1500pxにリサイズ
            img.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
            
            save_path = os.path.join(dest_dir, name + ".jpg")
            img.save(save_path, "JPEG", quality=85)
            print(f"Processed: {filename} -> {save_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
