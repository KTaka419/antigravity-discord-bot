import os

def check_image_counts():
    base_dir = "pest_images"
    categories = ["害虫", "病気"]
    
    print("=== 画像枚数確認レポート ===")
    
    for category in categories:
        cat_dir = os.path.join(base_dir, category)
        if not os.path.exists(cat_dir):
            print(f"Directory not found: {cat_dir}")
            continue

        print(f"\n[{category}]")
        subdirs = sorted([d for d in os.listdir(cat_dir) if os.path.isdir(os.path.join(cat_dir, d))])
        
        for subdir in subdirs:
            target_dir = os.path.join(cat_dir, subdir)
            files = [f for f in os.listdir(target_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
            count = len(files)
            status = "OK" if count >= 10 else "LOW"
            print(f"{subdir}: {count}枚 ({status})")

if __name__ == "__main__":
    check_image_counts()
