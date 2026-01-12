import os

def check_subfolders():
    base_dir = "pest_images"
    parent_category = "害虫"
    
    # チェック対象の親フォルダ名
    target_groups = [
        "アブラムシ", "カイガラムシ", "グンバイムシ", "カメムシ", "ハダニ",
        "ハマキムシ", "シンクイムシ", "コガネムシ", "カミキリムシ", "イラガ",
        "アメリカシロヒトリ", "マイマイガ", "チャドクガ", "テッポウムシ"
    ]

    print("=== サブフォルダ作成状況確認レポート ===")
    
    for group in target_groups:
        group_dir = os.path.join(base_dir, parent_category, group)
        if not os.path.exists(group_dir):
            print(f"X Group dir not found: {group}")
            continue

        # そのフォルダ内のサブフォルダを取得
        subdirs = [d for d in os.listdir(group_dir) if os.path.isdir(os.path.join(group_dir, d))]
        
        if subdirs:
            print(f"\n[{group}]")
            for subdir in subdirs:
                target_dir = os.path.join(group_dir, subdir)
                files = [f for f in os.listdir(target_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
                print(f"  - {subdir}: {len(files)}枚")
        else:
            print(f"\n[{group}] - NO SUBDIRECTORIES (Only {len(os.listdir(group_dir))} files directly inside)")

if __name__ == "__main__":
    check_subfolders()
