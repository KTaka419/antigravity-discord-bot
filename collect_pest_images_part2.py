import os
from icrawler.builtin import BingImageCrawler

def collect_remaining_images():
    base_dir = "pest_images"
    
    # 未収集の病気リスト
    diseases = {
        "灰色かび病": "灰色かび病 植物",
        "すす病": "すす病 植物",
        "もち病": "もち病 葉",
        "胴枯病": "胴枯病 木",
        "白紋羽病": "白紋羽病 根",
        "根頭がん腫病": "根頭がん腫病 根",
        "モザイク病": "モザイク病 植物"
    }

    max_images_per_keyword = 3

    print("=== 残りの病気画像の収集を開始します ===")

    for disease_name, search_word in diseases.items():
        save_dir = os.path.join(base_dir, "病気", disease_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        print(f"Collecting: {disease_name} (Search: {search_word})...")
        crawler = BingImageCrawler(storage={"root_dir": save_dir})
        crawler.crawl(keyword=search_word, max_num=max_images_per_keyword)

    print("\n=== 追加収集が完了しました ===")
    print(f"保存先: {os.path.abspath(base_dir)}")

if __name__ == "__main__":
    collect_remaining_images()
