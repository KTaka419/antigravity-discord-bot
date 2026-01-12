from PIL import Image
import os
import glob

src_dir = r"C:\Users\harunami\Desktop\helloworld\キャラクター画像"
dest_dir = r"C:\Users\harunami\Desktop\helloworld\temp_resized"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Support common image formats
files = []
for ext in ['*.png', '*.jpg', '*.jpeg']:
    files.extend(glob.glob(os.path.join(src_dir, ext)))

print(f"Found {len(files)} images to process.")

for file_path in files:
    try:
        filename = os.path.basename(file_path)
        name, _ = os.path.splitext(filename)
        # Use simple ascii names if possible or keep original if system handles utf-8 well (Windows Python usually does)
        # We will save as [filename].jpg. 
        # Note: 'コンフューサ.png' -> 'コンフューサ.jpg'
        
        save_path = os.path.join(dest_dir, name + ".jpg")
        
        with Image.open(file_path) as img:
            # Convert to RGB (handle transparency)
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            else:
                img = img.convert("RGB")
            
            # Resize logic: max dimension 1000px
            max_size = 1000
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            img.save(save_path, "JPEG", quality=85)
            print(f"Processed: {filename} -> {save_path}")

    except Exception as e:
        print(f"Failed to process {filename}: {e}")
