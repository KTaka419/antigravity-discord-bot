import os
from icrawler.builtin import BingImageCrawler

def collect_all_refined():
    # 改良版の保存先
    base_dir = "pest_images_refined"
    
    # 1. 大分類のリスト (検索ワードを改良)
    pests_general = {
        "アブラムシ": "アブラムシ 害虫",
        "カイガラムシ": "カイガラムシ 害虫",
        "グンバイムシ": "グンバイムシ 害虫",
        "カメムシ": "カメムシ 害虫",
        "ハダニ": "ハダニ 被害 葉",
        
        # アメリカシロヒトリ等、地名と混ざりやすいものに除外ワードや追加ワードを設定
        "アメリカシロヒトリ": "アメリカシロヒトリ 幼虫 虫 -地図 -国旗 -USA",
        "マイマイガ": "マイマイガ 幼虫 害虫",
        "チャドクガ": "チャドクガ 幼虫 害虫",
        "イラガ": "イラガ 幼虫 害虫",
        
        "ハマキムシ": "ハマキムシ 害虫",
        "シンクイムシ": "シンクイムシ 幼虫",
        "コガネムシ": "コガネムシ 害虫",
        "カミキリムシ": "カミキリムシ 害虫 成虫",
        "テッポウムシ": "テッポウムシ 幼虫 カミキリムシ"
    }

    diseases_general = {
        "うどんこ病": "うどんこ病 植物 葉",
        "黒星病": "黒星病 葉 植物",
        "赤星病": "赤星病 梨 葉",
        "炭疽病": "炭疽病 植物 病気",
        "灰色かび病": "灰色かび病 植物",
        "すす病": "すす病 植物 葉",
        "もち病": "もち病 葉 ツツジ",
        "胴枯病": "胴枯病 木",
        "白紋羽病": "白紋羽病 根 果樹",
        "根頭がん腫病": "根頭がん腫病 根 こぶ",
        "モザイク病": "モザイク病 植物 ウイルス"
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
        
        # サブフォルダも検索ワードを強化
        "アメリカシロヒトリ": ["アメリカシロヒトリ"], # 検索時に調整する
        "マイマイガ": ["マイマイガ"],
        "チャドクガ": ["チャドクガ"],
        "テッポウムシ": ["ゴマダラカミキリ 幼虫"]
    }

    print("=== 画像収集(検索ワード改良版)を開始します ===")
    print(f"保存先: {os.path.abspath(base_dir)}\n")

    # --- 大分類の収集 ---
    print("[1. 大分類の収集 (各10枚)]")
    
    # 害虫
    for pest_name, search_word in pests_general.items():
        save_dir = os.path.join(base_dir, "害虫", pest_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        print(f"Collecting: {pest_name} (Search: {search_word})...")
        crawler = BingImageCrawler(storage={"root_dir": save_dir})
        crawler.crawl(keyword=search_word, max_num=10)

    # 病気
    for disease_name, search_word in diseases_general.items():
        save_dir = os.path.join(base_dir, "病気", disease_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        print(f"Collecting: {disease_name} (Search: {search_word})...")
        crawler = BingImageCrawler(storage={"root_dir": save_dir})
        crawler.crawl(keyword=search_word, max_num=10)


    # --- 具体的な種名の収集 ---
    print("\n[2. 具体的な種名の収集 (各5枚)]")
    
    for group_name, species_list in pest_specific.items():
        parent_dir = os.path.join(base_dir, "害虫", group_name)
        
        # 親ディレクトリがなければ一応作る
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        for species in species_list:
            save_dir = os.path.join(parent_dir, species)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # 検索ワードの組み立て
            search_word = species + " 害虫"
            if "幼虫" in species: # すでに幼虫と入っている場合
                 search_word = species
            
            # アメリカシロヒトリの特別対応
            if "アメリカシロヒトリ" in species:
                search_word = species + " 幼虫 虫 -地図 -国旗 -USA"

            print(f"Collecting: {species} (in {group_name}) -> {save_dir}")
            print(f"  Search Word: {search_word}")
            crawler = BingImageCrawler(storage={"root_dir": save_dir})
            crawler.crawl(keyword=search_word, max_num=5)

    print("\n=== 全ての収集が完了しました ===")

if __name__ == "__main__":
    collect_all_refined()
