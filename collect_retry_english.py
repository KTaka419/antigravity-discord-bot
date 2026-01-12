import os
import shutil
from icrawler.builtin import BingImageCrawler

def collect_retry_english():
    base_dir = "pest_images"
    
    # 日本語でうまくいかないものを英語でトライ
    # 既存フォルダに追加保存される
    diseases = {
        "うどんこ病": "Powdery Mildew",
        "もち病": "Exobasidium" # もち病菌の属名
    }

    max_images_per_keyword = 15

    print("=== 画像収集(英語キーワードで再試行)を開始します ===")

    for disease_name, search_word in diseases.items():
        save_dir = os.path.join(base_dir, "病気", disease_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        print(f"Collecting: {disease_name} (Search: {search_word})...")
        crawler = BingImageCrawler(storage={"root_dir": save_dir})
        crawler.crawl(keyword=search_word, max_num=max_images_per_keyword)

if __name__ == "__main__":
    collect_retry_english()
