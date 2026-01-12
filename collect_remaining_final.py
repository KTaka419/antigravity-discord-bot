import os
import shutil
from icrawler.builtin import BingImageCrawler

def collect_remaining_final():
    base_dir = "pest_images"
    
    # 害虫リスト（まだ10枚に達していない可能性のあるもの）
    pests = {
        "コガネムシ": "コガネムシ 害虫",
        "カメムシ": "カメムシ 害虫",
        "グンバイムシ": "グンバイムシ 害虫",
        "ハダニ": "ハダニ 被害",
        "ハマキムシ": "ハマキムシ 害虫",
        "シンクイムシ": "シンクイムシ 幼虫",
        "チャドクガ": "チャドクガ 幼虫",
        "マイマイガ": "マイマイガ 幼虫",
        "テッポウムシ": "テッポウムシ 幼虫"
    }

    # 病気リスト（まだ10枚に達していない可能性のあるもの）
    diseases = {
        "黒星病": "黒星病 葉",
        "赤星病": "赤星病 梨",
        "炭疽病": "炭疽病 植物",
        "灰色かび病": "灰色かび病 植物",
        "すす病": "すす病 植物",
        "胴枯病": "胴枯病 木",
        "白紋羽病": "白紋羽病 根",
        "根頭がん腫病": "根頭がん腫病 根",
        "モザイク病": "モザイク病 植物"
    }

    # 確実に10枚以上にするため少し余裕を持たせる
    max_images_per_keyword = 15

    print("=== 画像収集(最終確認・追加)を開始します ===")

    # 害虫画像の収集
    print("\n[害虫画像の収集]")
    for pest_name, search_word in pests.items():
        save_dir = os.path.join(base_dir, "害虫", pest_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # 既存ファイル数を確認
        files = [f for f in os.listdir(save_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        if len(files) < 10:
            print(f"Collecting: {pest_name} (Current: {len(files)}, Search: {search_word})...")
            crawler = BingImageCrawler(storage={"root_dir": save_dir})
            # ダウンロード済みはスキップされるので、max_numを増やすだけでOK
            crawler.crawl(keyword=search_word, max_num=max_images_per_keyword)
        else:
             print(f"Skipping: {pest_name} (Current: {len(files)} >= 10)")


    # 病気画像の収集
    print("\n[病気画像の収集]")
    for disease_name, search_word in diseases.items():
        save_dir = os.path.join(base_dir, "病気", disease_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # 既存ファイル数を確認
        files = [f for f in os.listdir(save_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        if len(files) < 10:
            print(f"Collecting: {disease_name} (Current: {len(files)}, Search: {search_word})...")
            crawler = BingImageCrawler(storage={"root_dir": save_dir})
            crawler.crawl(keyword=search_word, max_num=max_images_per_keyword)
        else:
             print(f"Skipping: {disease_name} (Current: {len(files)} >= 10)")

    print("\n=== 全ての収集が完了しました ===")
    print(f"保存先: {os.path.abspath(base_dir)}")

if __name__ == "__main__":
    collect_remaining_final()
