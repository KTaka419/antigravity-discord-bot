import os
from icrawler.builtin import BingImageCrawler

def collect_specific_pests():
    base_dir = "pest_images"
    
    # 既存の害虫フォルダ名に対応する具体的な種名リスト
    # {親フォルダ名: [種名1, 種名2, ...]}
    pest_details = {
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
        
        # 以下はフォルダ名自体がほぼ種名だが、念のためそのまま使用するか、幼虫/成虫で分けるなどの対応が可能
        # 今回はユーザーの指示「種名のフォルダを作って」に従い、代表的なものを設定
        "アメリカシロヒトリ": ["アメリカシロヒトリ"],
        "マイマイガ": ["マイマイガ"],
        "チャドクガ": ["チャドクガ"],
        "テッポウムシ": ["ゴマダラカミキリ 幼虫"] # テッポウムシはカミキリムシの幼虫の総称
    }
    
    max_images = 5

    print("=== 具体的な種名の画像収集を開始します ===")

    for group_name, species_list in pest_details.items():
        # 親フォルダ（害虫フォルダ）のパス
        parent_dir = os.path.join(base_dir, "害虫", group_name)
        
        # 親フォルダが存在しない場合はスキップ（念のため）
        if not os.path.exists(parent_dir):
            print(f"Skipping group: {group_name} (Directory not found)")
            continue

        for species in species_list:
            # 具体的な種名のサブフォルダを作成
            # 検索ワード等にスペースが含まれる場合はフォルダ名から除去するなど調整
            folder_name = species.split()[0] # "ゴマダラカミキリ 幼虫" -> "ゴマダラカミキリ"フォルダにするか？
            # ユーザー指示は「種名（具体名）のフォルダ」なので、そのまま使う
            # ただしテッポウムシの場合は「ゴマダラカミキリ幼虫」などが適切かもしれないが
            # ここではシンプルに species をフォルダ名にする
            
            save_dir = os.path.join(parent_dir, species)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            search_word = species + " 害虫" # 検索精度向上のため
            if "幼虫" in species: # すでに幼虫と入っている場合
                 search_word = species

            print(f"Collecting: {species} (in {group_name}) -> {save_dir}")
            
            # 画像収集
            crawler = BingImageCrawler(storage={"root_dir": save_dir})
            crawler.crawl(keyword=search_word, max_num=max_images)

    print("\n=== 詳細収集が完了しました ===")

if __name__ == "__main__":
    collect_specific_pests()
