import os
import shutil
from icrawler.builtin import BingImageCrawler

def collect_retry_images():
    base_dir = "pest_images"
    
    # うどんこ病ともち病を再収集
    diseases = {
        "うどんこ病": "うどんこ病 植物",
        "もち病": "もち病 葉"
    }

    # 念のため max_num を少し多めに設定して確実に確保する
    max_images_per_keyword = 15

    print("=== 画像収集(再試行)を開始します ===")

    print("\n[病気画像の収集]")
    for disease_name, search_word in diseases.items():
        save_dir = os.path.join(base_dir, "病気", disease_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        print(f"Collecting: {disease_name} (Search: {search_word})...")
        crawler = BingImageCrawler(storage={"root_dir": save_dir})
        crawler.crawl(keyword=search_word, max_num=max_images_per_keyword)

    print("\n=== 再試行が完了しました ===")

if __name__ == "__main__":
    collect_retry_images()
