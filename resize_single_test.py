from PIL import Image
import os

src_path = r"C:\Users\harunami\Desktop\helloworld\temp_resized\gumi_test.jpg"
dest_path = r"C:\Users\harunami\Desktop\helloworld\temp_resized\gumi_small.jpg"

try:
    with Image.open(src_path) as img:
        # Convert to RGB
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        else:
            img = img.convert("RGB")
        
        # Resize logic: max dimension 800px (smaller to be safe)
        max_size = 800
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        img.save(dest_path, "JPEG", quality=80)
        print(f"Resized: {src_path} -> {dest_path}")

except Exception as e:
    print(f"Failed to process: {e}")
