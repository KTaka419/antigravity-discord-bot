import os
import shutil
from icrawler.builtin import BingImageCrawler

def collect_images():
    # 画像保存のルートディレクトリ
    base_dir = "pest_images"
    
    # 害虫リスト（フォルダ名: 検索ワード）
    # 検索ワードには「 害虫」などを付加して精度を高める
    pests = {
        "アブラムシ": "アブラムシ 害虫",
        "カイガラムシ": "カイガラムシ 害虫",
        "グンバイムシ": "グンバイムシ 害虫",
        "カメムシ": "カメムシ 害虫",
        "ハダニ": "ハダニ 被害",
        "アメリカシロヒトリ": "アメリカシロヒトリ 幼虫",
        "マイマイガ": "マイマイガ 幼虫",
        "チャドクガ": "チャドクガ 幼虫",
        "イラガ": "イラガ 幼虫",
        "ハマキムシ": "ハマキムシ 害虫",
        "シンクイムシ": "シンクイムシ 幼虫",
        "コガネムシ": "コガネムシ 害虫",
        "カミキリムシ": "カミキリムシ 成虫",
        "テッポウムシ": "テッポウムシ 幼虫" # カミキリムシ幼虫
    }

    # 病気リスト（フォルダ名: 検索ワード）
    # 検索ワードには「 植物 病気」などを付加
    diseases = {
        "うどんこ病": "うどんこ病 植物",
        "黒星病": "黒星病 葉",
        "赤星病": "赤星病 梨",
        "炭疽病": "炭疽病 植物",
        "灰色かび病": "灰色かび病 植物",
        "すす病": "すす病 植物",
        "もち病": "もち病 葉",
        "胴枯病": "胴枯病 木",
        "白紋羽病": "白紋羽病 根",
        "根頭がん腫病": "根頭がん腫病 根",
        "モザイク病": "モザイク病 植物"
    }

    # 収集設定
    max_images_per_keyword = 3

    print("=== 画像収集を開始します ===")

    # 害虫画像の収集
    print("\n[害虫画像の収集]")
    for pest_name, search_word in pests.items():
        save_dir = os.path.join(base_dir, "害虫", pest_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        print(f"Collecting: {pest_name} (Search: {search_word})...")
        crawler = BingImageCrawler(storage={"root_dir": save_dir})
        crawler.crawl(keyword=search_word, max_num=max_images_per_keyword)

    # 病気画像の収集
    print("\n[病気画像の収集]")
    for disease_name, search_word in diseases.items():
        save_dir = os.path.join(base_dir, "病気", disease_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        print(f"Collecting: {disease_name} (Search: {search_word})...")
        crawler = BingImageCrawler(storage={"root_dir": save_dir})
        crawler.crawl(keyword=search_word, max_num=max_images_per_keyword)

    print("\n=== 全ての収集が完了しました ===")
    print(f"保存先: {os.path.abspath(base_dir)}")

if __name__ == "__main__":
    collect_images()
