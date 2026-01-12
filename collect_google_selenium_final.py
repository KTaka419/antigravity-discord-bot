import os
import shutil
import time
import base64
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def collect_google_selenium_final():
    base_dir = "pest_images_google_selenium"
    
     # 既存のディレクトリを一旦クリーンアップして、新たに10枚収集する
    if os.path.exists(base_dir):
        print(f"Cleaning up {base_dir}...")
        shutil.rmtree(base_dir)

    # 検索リスト
    pests = {
        "害虫": {
            "アブラムシ": ["ワタアブラムシ 害虫", "モモアカアブラムシ 害虫"],  
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
    options.add_argument("--window-size=1200,800")
    
    print("=== ブラウザを起動しています(10枚収集モード) ===")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        for category, items in pests.items():
            for name, search_words in items.items():
                for search_word in search_words:
                    sub_folder_name = name 
                    if " " in search_word:
                        check_name = search_word.split()[0]
                        if check_name != name:
                            sub_folder_name = os.path.join(name, check_name)
                    
                    save_dir = os.path.join(base_dir, category, sub_folder_name)
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    
                    print(f"\nCollecting (10 images): {search_word} -> {save_dir}")
                    
                    driver.get("https://www.google.co.jp/imghp?hl=ja")
                    time.sleep(2)
                    
                    search_box = driver.find_element(By.NAME, "q")
                    search_box.clear()
                    search_box.send_keys(search_word)
                    search_box.send_keys(Keys.ENTER)
                    time.sleep(3)
                    
                    # 少しスクロールして画像を表示させる
                    driver.execute_script("window.scrollTo(0, 1000);")
                    time.sleep(2)
                    
                    thumbnails = driver.find_elements(By.CSS_SELECTOR, "div.H8Rx8c img")
                    if not thumbnails:
                         thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.rg_i")

                    print(f"  Found {len(thumbnails)} potential images. Downloading top 10...")
                    
                    count = 0
                    for img in thumbnails:
                        if count >= 10:
                            break
                        
                        src = img.get_attribute("src")
                        if not src:
                            src = img.get_attribute("data-src")
                        
                        if not src:
                            continue
                            
                        try:
                            file_path = os.path.join(save_dir, f"{count+1}.jpg")
                            
                            if src.startswith("data:image"):
                                header, encoded = src.split(",", 1)
                                data = base64.b64decode(encoded)
                                with open(file_path, "wb") as f:
                                    f.write(data)
                            elif src.startswith("http"):
                                response = requests.get(src, timeout=10)
                                if response.status_code == 200:
                                    with open(file_path, "wb") as f:
                                        f.write(response.content)
                            
                            count += 1
                            print(f"    Saved: {file_path}")
                            
                        except Exception as e:
                            print(f"    Error saving image: {e}")
                            
                    time.sleep(1)

    finally:
        print("\n=== 終了処理中... ===")
        driver.quit()
        print("=== 完了 ===")

if __name__ == "__main__":
    collect_google_selenium_final()
