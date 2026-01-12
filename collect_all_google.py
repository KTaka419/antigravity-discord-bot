import os
from icrawler.builtin import GoogleImageCrawler

def collect_all_google():
    # Google検索用の新しい保存先
    base_dir = "pest_images_google"
    
    # 1. 大分類のリスト
    pests_general = {
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
        "テッポウムシ": "テッポウムシ 幼虫"
    }

    diseases_general = {
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

    # 2. 具体的な種名リスト（サブフォルダ用）
    pest_specific = {
        "アブラムシ": ["ワタアブラムシ", "モモアカアブラムシ"],
        "カイガラムシ": ["ルビーロウムシ", "イセリアカイガラムシ", "ツノロウムシ"],
        "グンバイムシ": ["ツツジグンバイ", "ナシグンバイ"],
        "カメムシ": ["チャバネアオカメムシ", "クサギカメムシ", "ツヤアオカメムシ"],
        "ハダニ": ["ミカンハダニ", "カンザワハダニ"],
        "ハマキムシ": ["チャハマキ", "リンゴコカクモンハマキ"],
        "シンクイムシ": ["モモシンクイガ", "ナシヒメシンクイ"],
        "コガネムシ": ["マメコガネ", "ドウガネブイブイ", "アオドウガネ"],
        "カミキリムシ": ["ゴマダラカミキリ", "キボシカミキリ"],
        "イラガ": ["ヒロヘリアオイラガ", "イラガ"],
        
        # フォルダ名と同じ種名のものも念のためサブフォルダ作る
        "アメリカシロヒトリ": ["アメリカシロヒトリ"],
        "マイマイガ": ["マイマイガ"],
        "チャドクガ": ["チャドクガ"],
        "テッポウムシ": ["ゴマダラカミキリ 幼虫"]
    }

    print("=== Google検索エンジンでの画像収集を開始します ===")
    print(f"保存先: {os.path.abspath(base_dir)}\n")

    # --- 大分類の収集 ---
    print("[1. 大分類の収集 (各10枚)]")
    
    # 害虫
    for pest_name, search_word in pests_general.items():
        save_dir = os.path.join(base_dir, "害虫", pest_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        print(f"Collecting: {pest_name} (Search: {search_word})...")
        crawler = GoogleImageCrawler(storage={"root_dir": save_dir})
        crawler.crawl(keyword=search_word, max_num=10)

    # 病気
    for disease_name, search_word in diseases_general.items():
        save_dir = os.path.join(base_dir, "病気", disease_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        print(f"Collecting: {disease_name} (Search: {search_word})...")
        crawler = GoogleImageCrawler(storage={"root_dir": save_dir})
        crawler.crawl(keyword=search_word, max_num=10)


    # --- 具体的な種名の収集 ---
    print("\n[2. 具体的な種名の収集 (各5枚)]")
    
    for group_name, species_list in pest_specific.items():
        parent_dir = os.path.join(base_dir, "害虫", group_name)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        for species in species_list:
            save_dir = os.path.join(parent_dir, species)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            search_word = species + " 害虫"
            if "幼虫" in species:
                 search_word = species
            
            print(f"Collecting: {species} (in {group_name}) -> {save_dir}")
            crawler = GoogleImageCrawler(storage={"root_dir": save_dir})
            crawler.crawl(keyword=search_word, max_num=5)

    print("\n=== 全てのGoogle収集が完了しました ===")

if __name__ == "__main__":
    collect_all_google()
