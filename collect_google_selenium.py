import os
import time
import base64
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def collect_google_selenium():
    # 保存先
    base_dir = "pest_images_google_selenium"
    
    # 検索リスト (改良版キーワード)
    pests = {
        "害虫": {
            "アブラムシ": ["ワタアブラムシ 害虫", "モモアカアブラムシ 害虫"],  # アブラムシは具体的な2種のみに集中
            "アメリカシロヒトリ": ["アメリカシロヒトリ 幼虫 虫 -地図 -国旗 -USA"],
            "マイマイガ": ["マイマイガ 幼虫 害虫"],
            "チャドクガ": ["チャドクガ 幼虫 害虫"],
            "イラガ": ["イラガ 幼虫 害虫"],
            "ハマキムシ": ["ハマキムシ 害虫"],
            "シンクイムシ": ["シンクイムシ 幼虫"],
            "コガネムシ": ["コガネムシ 害虫"],
            "カミキリムシ": ["カミキリムシ 害虫"],
            "テッポウムシ": ["ゴマダラカミキリ 幼虫"],
            "カイガラムシ": ["カイガラムシ 害虫"],
            "グンバイムシ": ["グンバイムシ 害虫"],
            "カメムシ": ["カメムシ 害虫"],
            "ハダニ": ["ハダニ 被害 葉"]
        },
        "病気": {
             "うどんこ病": ["うどんこ病 植物"],
             "黒星病": ["黒星病 葉"],
             "赤星病": ["赤星病 梨"],
             "炭疽病": ["炭疽病 植物"],
             "灰色かび病": ["灰色かび病 植物"],
             "すす病": ["すす病 植物"],
             "もち病": ["もち病 葉"],
             "胴枯病": ["胴枯病 木"],
             "白紋羽病": ["白紋羽病 根"],
             "根頭がん腫病": ["根頭がん腫病 根"],
             "モザイク病": ["モザイク病 植物"]
        }
    }

    # Selenium設定
    options = Options()
    # options.add_argument("--headless") # 動作確認のため画面を表示させる場合はコメントアウト
    options.add_argument("--window-size=1200,800")
    
    print("=== ブラウザを起動しています... ===")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        for category, items in pests.items():
            for name, search_words in items.items():
                for search_word in search_words:
                    # 保存フォルダ
                    # 具体的な名前（ワタアブラムシ）ではなく、親フォルダ（アブラムシ）に入れるか、
                    # あるいはここで一括して親フォルダ（アブラムシ）にまとめて入れるか。
                    # 今回はユーザーの「種名（具体名）のフォルダを作って」という要望と、
                    # アメリカシロヒトリの例に合わせて、name(=アブラムシ)の下にフォルダを作る形にするが、
                    # 検索ワードがリストになっているので、検索ワードの先頭の単語をフォルダ名にするなど工夫が必要。
                    
                    # リストの1つ目だけをフォルダ名にする簡易ロジック
                    sub_folder_name = name 
                    if " " in search_word:
                        check_name = search_word.split()[0]
                        # 検索ワードの先頭がリストのキー(アブラムシ)と違うなら、それをサブフォルダ名とする
                        if check_name != name:
                            sub_folder_name = os.path.join(name, check_name)
                    
                    save_dir = os.path.join(base_dir, category, sub_folder_name)
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    
                    print(f"\nCollecting: {search_word} -> {save_dir}")
                    
                    # Google画像検索へ移動
                    driver.get("https://www.google.co.jp/imghp?hl=ja")
                    time.sleep(2)
                    
                    # 検索ボックスに入力
                    search_box = driver.find_element(By.NAME, "q")
                    search_box.clear()
                    search_box.send_keys(search_word)
                    search_box.send_keys(Keys.ENTER)
                    time.sleep(3)
                    
                    # 画像要素を取得 (Googleのクラス名は変わりやすいので、imgタグで取得してフィルタリング)
                    thumbnails = driver.find_elements(By.CSS_SELECTOR, "div.H8Rx8c img") # 最近のGoogle画像検索のサムネイルコンテナ
                    if not thumbnails:
                         thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.rg_i") # 古い/別のパターンのクラス

                    print(f"  Found {len(thumbnails)} potential images. Downloading top 5...")
                    
                    count = 0
                    for img in thumbnails:
                        if count >= 5:
                            break
                        
                        src = img.get_attribute("src")
                        if not src:
                            src = img.get_attribute("data-src")
                        
                        if not src:
                            continue
                            
                        # URLかBase64か判定して保存
                        try:
                            file_path = os.path.join(save_dir, f"{count+1}.jpg")
                            
                            if src.startswith("data:image"):
                                # Base64の場合
                                header, encoded = src.split(",", 1)
                                data = base64.b64decode(encoded)
                                with open(file_path, "wb") as f:
                                    f.write(data)
                            elif src.startswith("http"):
                                # URLの場合
                                response = requests.get(src, timeout=10)
                                if response.status_code == 200:
                                    with open(file_path, "wb") as f:
                                        f.write(response.content)
                            
                            count += 1
                            print(f"    Saved: {file_path}")
                            
                        except Exception as e:
                            print(f"    Error saving image: {e}")
                            
                    time.sleep(1) # 少し待機

    finally:
        print("\n=== 終了処理中... ===")
        driver.quit()
        print("=== 完了 ===")

if __name__ == "__main__":
    collect_google_selenium()
