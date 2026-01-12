from PIL import Image
import os
import glob

# Source and Dest (using absolute paths provided in context)
src_dir = r"C:\Users\harunami\Desktop\helloworld\キャラクター画像"
dest_dir = r"C:\Users\harunami\Desktop\helloworld\temp_resized"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# File mapping (filename prefix -> english key for tracking, optional but good for debugging)
# We just process everything in the folder.

valid_exts = ['*.png', '*.jpg', '*.jpeg']
files = []
for ext in valid_exts:
    files.extend(glob.glob(os.path.join(src_dir, ext)))

print(f"Found {len(files)} images to process.")

for file_path in files:
    try:
        filename = os.path.basename(file_path)
        name, _ = os.path.splitext(filename)
        
        # Save as jpg
        save_path = os.path.join(dest_dir, name + ".jpg")
        
        with Image.open(file_path) as img:
            # Convert to RGB
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            else:
                img = img.convert("RGB")
            
            # Resize logic: max dimension 800px (Safety first)
            max_size = 800
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            img.save(save_path, "JPEG", quality=85)
            # print(f"Processed: {filename}")

    except Exception as e:
        print(f"Failed to process {filename}: {e}")

print("Resize complete.")
