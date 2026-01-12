from PIL import Image
import os

src_path = r"C:\Users\harunami\Desktop\helloworld\temp_resized\confusa_char.jpg"
dest_path = r"C:\Users\harunami\Desktop\helloworld\temp_resized\confusa_char_small.png"

try:
    with Image.open(src_path) as img:
        # すでにリサイズ済みですが、念のためさらに小さくしてPNG保存
        img.thumbnail((1000, 1000), Image.Resampling.LANCZOS)
        img.save(dest_path, "PNG")
        print(f"Saved: {dest_path}")
except Exception as e:
    print(f"Error: {e}")
