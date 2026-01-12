import os
import glob
import pandas as pd
import shutil

# Paths
BASE_DIR = r"C:\Users\harunami\Desktop\helloworld"
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
CSV_PATH = os.path.join(BASE_DIR, "植栽データ_utf8_bom.csv")
WEB_DIR = os.path.join(BASE_DIR, "docs")
PAGES_DIR = os.path.join(WEB_DIR, "pages")
IMAGES_DIR = os.path.join(WEB_DIR, "images")

# Create directories
os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# 1. Load CSV
try:
    df = pd.read_csv(CSV_PATH)
    # Create a dictionary indexed by tree name
    tree_data = df.set_index("樹木名").to_dict(orient="index")
    print("CSV loaded successfully.")
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# 2. Mapping strategy
# Filename prefix -> CSV Key
name_map = {
    "ichii": "イチイ",
    "icho": "イチョウ",
    "gisgo": "イチョウ", # Handle potential variations
    "itohiba": "イトヒバ",
    "inutsuge": "イヌツゲ",
    "irohamomiji": "イロハモミジ",
    "ume": "ウメ",
    "olive": "オリーブ",
    "abelia": "アベリア",
    "akamatsu": "アカマツ",
    "ajisai": "アジサイ",
    "asebi": "アセビ",
    "aohada": "アオハダ",
    "aoki": "アオキ",
    "gumi": "グミ", # Added
    "confusa": "コンフューサ",
    "sakaki": "サカキ",
    "sakura": "サクラ",
    "satonishiki": "サトウニシキ",
    "kaki": "カキ",
    "kaizukaibuki": "カイヅカイブキ",
    "kakuremino": "カクレミノ",
    "kalmia": "カルミア",
    "gamazumi": "ガマズミ",
    "kyara": "キャラ",
    "kyouchikutou": "キョウチクトウ",
    "kinkan": "キンカン",
    "kinmokusei": "キンモクセイ",
    "kuroganemochi": "クロガネモチ",
    # Add potential Batch 4 keys just in case
    "confusa": "コンフューサ",
    "sakaki": "サカキ",
    "sakura": "サクラ",
    "satonishiki": "サトウニシキ",
    "sazanka": "サザンカ",
    "satsuki": "サツキ", # May need adjustment match CSV
    "sarusuberi": "サルスベリ",
    "sawara": "サワラ",
    "sangoju": "サンゴジュ",
    "sanshuyu": "サンシュユ",
    "sansho": "サンショウ",
    "shikimi": "シキミ",
    "shidarezakura": "シダレザクラ",
    "juneberry": "ジューンベリー"
}

# 3. Scan Images
# dirs_to_scan = [(path, priority)] - later items with same key overwrite earlier ones
ADDITIONAL_DIR = r"C:\Users\harunami\Desktop\helloworld\キャラクター画像\背景追加"
dirs_to_scan = [OUTPUTS_DIR, ADDITIONAL_DIR]

processed_trees = {} # Key: jp_name (primary unique ID), Value: {en_key, img_src_path, data...}

print(f"Scanning directories...")

for search_dir in dirs_to_scan:
    if not os.path.exists(search_dir):
        print(f"Skipping missing directory: {search_dir}")
        continue
        
    # Gather all images
    files = []
    for ext in ["*.png", "*.jpg", "*.jpeg"]:
        files.extend(glob.glob(os.path.join(search_dir, ext)))
        
    print(f"Found {len(files)} images in {search_dir}")

    for img_path in files:
        filename = os.path.basename(img_path)
        name_stem, _ = os.path.splitext(filename)
        lower_name = name_stem.lower()
        
        jp_name = None
        en_key_for_url = None

        # Strategy 1: Check name_map (Prefix match for English/Romaji files)
        matched_map_key = None
        for key in name_map:
            if lower_name.startswith(key):
                matched_map_key = key
                break
        
        if matched_map_key:
            jp_name = name_map[matched_map_key]
            en_key_for_url = matched_map_key
        
        # Strategy 2: Direct Match with CSV (Japanese Filenames)
        if not jp_name:
            if name_stem in tree_data:
                jp_name = name_stem
                en_key_for_url = name_stem # Use Japanese as URL key if English not available
            
            # Strategy 2b: Handle "Name（Detail）" format
            elif '（' in name_stem:
                clean_name = name_stem.split('（')[0]
                if clean_name in tree_data:
                    jp_name = clean_name
                    en_key_for_url = name_stem # Keep distinct URL even if data is same

        # Register if valid
        if jp_name and jp_name in tree_data:
            # Overwrite existing processing for this tree (assuming later dirs = newer/better)
            # OR if from same dir, maybe prefer one over another? 
            # Simple overwriting by scan order (Outputs -> Additional) prioritizes Additional.
            
            processed_trees[jp_name] = {
                "en_key": en_key_for_url, 
                "img_src_path": img_path,
                "img_filename": filename,
                "data": tree_data[jp_name]
            }

# Copy images to web/images
for jp_name, info in processed_trees.items():
    src = info["img_src_path"]
    dst = os.path.join(IMAGES_DIR, info["img_filename"])
    shutil.copy2(src, dst)
    info["web_img_path"] = f"../images/{info['img_filename']}" # For subpages
    info["top_img_path"] = f"images/{info['img_filename']}" # For index

print(f"Processed {len(processed_trees)} valid tree characters.")



# 4. Generate CSS
css_content = """
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&family=Zen+Kaku+Gothic+New:wght@400;700&display=swap');

:root {
    --primary-color: #2D4A3E; /* Deep Green */
    --accent-color: #8DA399; /* Sage */
    --bg-color: #F9F9F7;     /* Off-white */
    --text-color: #333333;
    --card-bg: #FFFFFF;
}

html {
    font-size: 11px;
}

body {
    font-family: 'Zen Kaku Gothic New', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    margin: 0;
    padding: 0;
    line-height: 1.6;
    font-size: 1.2rem;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

header {
    background-color: var(--primary-color);
    color: white;
    padding: 1.5rem 1rem;
    text-align: center;
}

header h1 {
    font-family: 'Zen Kaku Gothic New', sans-serif;
    margin: 0;
    font-weight: 700;
    letter-spacing: 0.05em;
    font-size: 2rem;
}

header a {
    color: white;
    text-decoration: none;
}

main {
    flex: 1;
}

.container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 1rem;
}

footer {
    background-color: #eef2f0;
    text-align: center;
    padding: 2rem;
    margin-top: 3rem;
    font-size: 1rem;
    color: #666;
}

footer a {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 700;
}

/* Home Portal Styles */
.portal-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
    margin-top: 2rem;
}

@media (min-width: 600px) {
    .portal-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

.portal-card {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    text-decoration: none;
    color: var(--text-color);
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    transition: transform 0.3s, box-shadow 0.3s;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 150px;
    border: 1px solid #eee;
}

.portal-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border-color: var(--accent-color);
}

.portal-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: var(--primary-color);
}

.portal-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: var(--primary-color);
}

.portal-desc {
    font-size: 1rem;
    color: #666;
}

.wip-badge {
    background: #eee;
    color: #888;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    margin-top: 0.5rem;
}

/* Grid Layout for Zukan */
.tree-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
}

@media (min-width: 480px) { .tree-grid { grid-template-columns: repeat(3, 1fr); } }
@media (min-width: 768px) { .tree-grid { grid-template-columns: repeat(4, 1fr); } }
@media (min-width: 1024px) { .tree-grid { grid-template-columns: repeat(5, 1fr); } }

.tree-card {
    background: var(--card-bg);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    text-decoration: none;
    color: inherit;
    display: flex;
    flex-direction: column;
}

.tree-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
}

.card-image-wrapper {
    width: 100%;
    padding-top: 100%;
    position: relative;
    background-color: #f0f0f0;
}

.card-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.card-info {
    padding: 0.8rem;
    text-align: center;
}

.card-name-jp {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
    color: var(--primary-color);
}

.card-name-en {
    font-size: 0.85rem;
    color: #666;
    font-family: 'Zen Kaku Gothic New', sans-serif;
    margin-top: 0.3rem;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Detail Page */
.detail-hero-wrapper {
    background-color: #eef2f0;
    text-align: center;
    padding: 1.5rem 1rem;
    margin-bottom: 2rem;
}

.detail-hero {
    max-width: 100%;
    max-height: 70vh;
    width: auto;
    height: auto;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border-radius: 8px;
}

.detail-header {
    text-align: center;
    margin-bottom: 2rem;
}

.detail-title {
    font-size: 2.2rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.data-table-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    overflow: hidden;
    margin-bottom: 3rem;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 1.1rem;
}

.data-table th, .data-table td {
    padding: 0.8rem;
    border-bottom: 1px solid #f0f0f0;
    text-align: left;
    vertical-align: top;
}

.data-table th {
    background-color: #f8f9fa;
    width: 25%;
    color: var(--primary-color);
    font-weight: 700;
    white-space: nowrap;
}

@media (max-width: 600px) {
    .data-table th, .data-table td {
        display: block;
        width: 100%;
    }
    .data-table th {
        background-color: #f0f0f0;
        padding-bottom: 0.3rem;
        border-bottom: none;
    }
    .data-table td {
        padding-top: 0.3rem;
        border-bottom: 1px solid #ddd;
    }
    .detail-title {
        font-size: 1.8rem;
    }
}

.back-link {
    display: inline-block;
    padding: 0.8rem 2.5rem;
    background-color: var(--primary-color);
    color: white;
    text-decoration: none;
    border-radius: 50px;
    font-weight: 700;
    transition: opacity 0.3s;
    font-size: 1.1rem;
}

.back-link:hover {
    opacity: 0.9;
}

/* About Page Specifics */
.profile-box {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}

.profile-name {
    font-size: 1.8rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.profile-loc {
    color: #666;
    margin-bottom: 2rem;
}

.contact-links {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: center;
}

.contact-btn {
    display: block;
    width: 100%;
    max-width: 300px;
    padding: 1rem;
    border-radius: 8px;
    text-decoration: none;
    font-weight: bold;
    color: white;
    transition: transform 0.2s;
}

.contact-btn:hover {
    transform: translateY(-2px);
}

.btn-mail { background: #333; }
.btn-line { background: #06C755; }
.btn-x { background: #000; }

.qr-placeholder {
    width: 150px;
    height: 150px;
    background: #f0f0f0;
    margin: 1rem auto;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #aaa;
    border: 2px dashed #ccc;
    border-radius: 8px;
}
"""

with open(os.path.join(WEB_DIR, "style.css"), "w", encoding="utf-8") as f:
    f.write(css_content)



# 5. Generate Zukan HTML (Previously Index)
def get_gojuuon_row(name):
    first_char = name[0]
    rows = [
        ('ア行', 'アイウエオ'),
        ('カ行', 'カキクケコガギグゲゴ'),
        ('サ行', 'サシスセソザジズゼゾ'),
        ('タ行', 'タチツテトダヂヅデド'),
        ('ナ行', 'ナニヌネノ'),
        ('ハ行', 'ハヒフヘホバビブベボパピプペポ'),
        ('マ行', 'マミムメモ'),
        ('ヤ行', 'ヤユヨ'),
        ('ラ行', 'ラリルレロ'),
        ('ワ行', 'ワヰウヱヲン')
    ]
    for row_name, chars in rows:
        if first_char in chars:
            return row_name
    return 'その他'

# Group by Row
tree_groups = {}
sorted_trees = sorted(processed_trees.items()) # Sort by Japanese Name

for jp_name, info in sorted_trees:
    row = get_gojuuon_row(jp_name)
    if row not in tree_groups:
        tree_groups[row] = []
    tree_groups[row].append((jp_name, info))

# Sort groups Order
row_order = ['ア行', 'カ行', 'サ行', 'タ行', 'ナ行', 'ハ行', 'マ行', 'ヤ行', 'ラ行', 'ワ行', 'その他']


zukan_html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>庭木キャラ図鑑 - 植木屋ハルナミワークス</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* Navigation Styles specific to zukan */
        .nav-scroller {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(249, 249, 247, 0.95);
            backdrop-filter: blur(5px);
            border-bottom: 1px solid #ddd;
            padding: 0.5rem 0;
            margin-bottom: 2rem;
            white-space: nowrap;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .nav-list {{
            display: flex;
            justify-content: center;
            list-style: none;
            padding: 0;
            margin: 0;
            min-width: min-content;
        }}
        
        .nav-item {{ margin: 0 0.2rem; }}
        
        .nav-link {{
            display: block;
            padding: 0.5rem 1rem;
            text-decoration: none;
            color: var(--primary-color);
            font-weight: 700;
            border-radius: 20px;
            font-size: 1rem;
            transition: background 0.2s;
        }}
        
        .nav-link:hover {{
            background-color: var(--accent-color);
            color: white;
        }}

        @media (max-width: 600px) {{
            .nav-list {{ justify-content: flex-start; padding: 0 1rem; }}
        }}

        .section-header {{
            font-size: 1.5rem;
            color: var(--primary-color);
            border-left: 5px solid var(--accent-color);
            padding-left: 1rem;
            margin: 3rem 0 1.5rem 0;
            scroll-margin-top: 80px;
        }}
    </style>
</head>
<body>
    <!-- Banner (Top) -->
    <div style="width:100%; max-height:300px; overflow:hidden;">
        <img src="images/zukan_banner.jpg" alt="庭木キャラ図鑑" style="width:100%; height:auto; object-fit:cover; display:block;">
    </div>

    <!-- Home Link (Below Banner) -->
    <div style="text-align:center; margin: 1rem 0;">
        <a href="index.html" class="back-link" style="padding: 0.5rem 1rem; font-size: 0.9rem;">ホームに戻る</a>
    </div>

    <!-- Index Navigation -->
    <nav class="nav-scroller">
        <ul class="nav-list">
"""

# Generate Menu Links
for row in row_order:
    if row in tree_groups:
        zukan_html += f'<li class="nav-item"><a href="#{row}" class="nav-link">{row[0]}</a></li>'

zukan_html += """
        </ul>
    </nav>

    <main class="container">
"""

# Generate Sections
for row in row_order:
    if row in tree_groups:
        items = tree_groups[row]
        zukan_html += f"""
        <h2 id="{row}" class="section-header">{row}</h2>
        <div class="tree-grid">
        """
        
        for jp_name, info in items:
            en_key = info["en_key"]
            img_path = info["top_img_path"]
            data = info["data"]
            
            zukan_html += f"""
            <a href="pages/{en_key}.html" class="tree-card">
                <div class="card-image-wrapper">
                    <img src="{img_path}" alt="{jp_name}" class="card-image">
                </div>
                <div class="card-info">
                    <div class="card-name-jp">{jp_name}</div>
                    <div class="card-name-en">{data.get('魅力・観賞価値', '')}</div>
                </div>
            </a>
            """
        
        zukan_html += "</div>" # Close grid

zukan_html += """
        <div style="text-align:center; margin-top: 3rem;">
            <a href="index.html" class="back-link">ホームに戻る</a>
        </div>
    </main>

    <footer>
        <div class="container">
            <a href="about.html">運営について (About Us)</a>
            <p>&copy; 2026 Harunami Works</p>
        </div>
    </footer>
</body>
</html>
"""

with open(os.path.join(WEB_DIR, "zukan.html"), "w", encoding="utf-8") as f:
    f.write(zukan_html)


# 6. Generate Detail Pages
for jp_name, info in processed_trees.items():
    en_key = info["en_key"]
    img_path = info["web_img_path"]
    data = info["data"]
    
    # Generate rows for all CSV columns
    table_rows = ""
    for key, value in data.items():
        # Handle nan or empty values
        val_str = str(value) if pd.notna(value) else "ー"
        # Preserve newlines in CSV cells
        val_str = val_str.replace("\\n", "<br>")
        
        table_rows += f"""
                    <tr>
                        <th>{key}</th>
                        <td>{val_str}</td>
                    </tr>
        """

    page_html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{jp_name} - 庭木キャラ図鑑</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="../zukan.html" style="color:white; text-decoration:none;">庭木キャラ図鑑</a></h1>
        </div>
    </header>

    <div class="detail-hero-wrapper">
        <img src="{img_path}" alt="{jp_name}" class="detail-hero">
    </div>

    <main class="container">
        <div class="detail-header">
            <h2 class="detail-title">{jp_name}</h2>
            <div class="card-name-en" style="font-size: 1.1rem; webkit-line-clamp: initial;">{data.get('科・属名', '')}</div>
        </div>

        <div class="data-table-container">
            <table class="data-table">
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>

        <div style="text-align:center; margin-bottom: 3rem;">
            <a href="../zukan.html" class="back-link">図鑑一覧に戻る</a>
        </div>
    </main>

    <footer>
        <div class="container">
            <a href="../about.html">運営について (About Us)</a>
            <p>&copy; 2026 Harunami Works</p>
        </div>
    </footer>
</body>
</html>
"""
    with open(os.path.join(PAGES_DIR, f"{en_key}.html"), "w", encoding="utf-8") as f:
        f.write(page_html)

# 7. Generate About Page (Now in Root)
about_html = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>運営について - 植木屋ハルナミワークス</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="index.html">AI生成植木図鑑　byハルナミ</a></h1>
        </div>
    </header>

    <main class="container">
        <h2 style="text-align:center; margin-bottom:3rem; color:var(--primary-color);">運営について</h2>
        
        <div class="profile-box">
            <div class="profile-name">ハルナミ</div>
            <div class="profile-loc">群馬県高崎市</div>
            
            <p style="margin-bottom: 2rem;">
                植木屋やってます。
            </p>

            <div class="contact-links">
                <!-- 
                <a href="mailto:dummy@example.com" class="contact-btn btn-mail">
                    メールでのお問い合わせ
                </a>
                
                <a href="https://line.me/" target="_blank" class="contact-btn btn-line">
                    公式LINE
                </a>
                <div class="qr-placeholder">
                    QR Code<br>(Placeholder)
                </div>
                -->

                <a href="https://x.com/harunamix" target="_blank" class="contact-btn btn-x">
                    X (Twitter) @harunamix
                </a>
            </div>
        </div>

        <div style="text-align:center; margin-top: 3rem;">
            <a href="index.html" class="back-link">ホームに戻る</a>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 Harunami Works</p>
        </div>
    </footer>
</body>
</html>
"""
with open(os.path.join(WEB_DIR, "about.html"), "w", encoding="utf-8") as f:
    f.write(about_html)


# 8. Generate New Index Portal
index_html = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI生成植木図鑑　byハルナミ</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="container">
            <img src="images/harunami_wide_logo.jpg" alt="AI生成植木図鑑 byハルナミ" style="max-width:100%; height:auto; display:block; margin:0 auto;">
        </div>
    </header>

    <main class="container">
        <div class="portal-grid">
            <a href="zukan.html" class="portal-card" style="padding:0; overflow:hidden; position:relative;">
                <img src="images/zukan_title.jpg" alt="庭木キャラ図鑑" style="width:100%; height:100%; object-fit:cover;">
            </a>
            
            <a href="about.html" class="portal-card">
                <div class="portal-icon">👤</div>
                <div class="portal-title">運営について</div>
                <div class="portal-desc">ハルナミのプロフィール・活動</div>
            </a>
            
            <a href="pests.html" class="portal-card">
                <div class="portal-icon">🐛</div>
                <div class="portal-title">庭木の病害虫<br>病気図鑑</div>
                <div class="portal-desc">（作成中）</div>
                <div class="wip-badge">Coming Soon</div>
            </a>
            
            <a href="compare.html" class="portal-card">
                <div class="portal-icon">🔍</div>
                <div class="portal-title">似てる庭木の<br>見分け方</div>
                <div class="portal-desc">（作成中）</div>
                <div class="wip-badge">Coming Soon</div>
            </a>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 Harunami Works</p>
        </div>
    </footer>
</body>
</html>
"""
with open(os.path.join(WEB_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

# 9. Generate Placeholders
wip_html = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coming Soon - 植木屋ハルナミワークス</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="index.html">AI生成植木図鑑　byハルナミ</a></h1>
        </div>
    </header>

    <main class="container" style="text-align:center; padding-top:4rem;">
        <h2 style="font-size:2rem; margin-bottom:1rem;">準備中</h2>
        <p>このコンテンツは現在作成中です。<br>公開まで今しばらくお待ちください。</p>
        
        <div style="margin-top:3rem;">
            <a href="index.html" class="back-link">ホームに戻る</a>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2026 Harunami Works</p>
        </div>
    </footer>
</body>
</html>
"""
with open(os.path.join(WEB_DIR, "pests.html"), "w", encoding="utf-8") as f:
    f.write(wip_html)

with open(os.path.join(WEB_DIR, "compare.html"), "w", encoding="utf-8") as f:
    f.write(wip_html)


# ---------------------------------------------------------
# NEW: Generate Pests & Diseases Pages
# ---------------------------------------------------------
import re

PESTS_MD_PATH = os.path.join(BASE_DIR, "pest_disease_list.md")
PESTS_PAGES_DIR = os.path.join(PAGES_DIR, "pests")
os.makedirs(PESTS_PAGES_DIR, exist_ok=True)

# English Key Mapping
pest_name_map = {
    "アブラムシ": "aburamushi",
    "カイガラムシ": "kaigaramushi",
    "グンバイムシ": "gunbaimushi",
    "カメムシ": "kamemushi",
    "ハダニ": "hadani",
    "ハマキムシ": "hamakimushi",
    "シンクイムシ": "shinkuimushi",
    "コガネムシ": "koganemushi",
    "カミキリムシ": "kamikirimushi",
    "イラガ": "iraga",
    "アメリカシロヒトリ": "amerikashirohitori",
    "マイマイガ": "maimaiga",
    "チャドクガ": "chadokuga",
    "うどんこ病": "udonko_byou",
    "黒星病": "kurohoshi_byou",
    "赤星病": "akahoshi_byou",
    "炭疽病": "tanso_byou",
    "灰色かび病": "haiirokabi_byou",
    "すす病": "susu_byou",
    "もち病": "mochi_byou",
    "胴枯病": "dougare_byou",
    "白紋羽病": "shiromonpa_byou",
    "根頭がん腫病": "kontouganshu_byou",
    "モザイク病": "mozaiku_byou"
}

def parse_markdown_table(markdown_text, section_header):
    """
    Simple parser for the markdown tables in the specific format.
    Returns list of dicts.
    """
    items = []
    lines = markdown_text.split('\n')
    in_section = False
    headers = []
    
    for line in lines:
        if section_header in line:
            in_section = True
            continue
        if in_section and line.startswith('##'): # Next section
            break
        
        if in_section and line.strip().startswith('|'):
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if '---' in cols[0]: continue # Skip separator
            if not headers:
                headers = cols
                continue
            
            # Create dict
            item = {}
            # Handle row span simulation or just simple mapping
            # The structure is: Name | Details | Prevention
            # Name col might have bolding **Name**
            
            raw_name = cols[0].replace('**', '').replace('<br>', ' ').strip()
            # Clean name for key (remove extra text if any, e.g. " (Larva:...)")
            name_key = raw_name.split(' ')[0] # Simple split might break if name has space, but Japanese usually doesn't
            if '（' in name_key: name_key = name_key.split('（')[0]
            
            item['name'] = raw_name
            item['key'] = name_key
            item['col2'] = cols[1]
            item['col3'] = cols[2]
            items.append(item)
            
    return items, headers

# Read MD
with open(PESTS_MD_PATH, 'r', encoding='utf-8') as f:
    md_content = f.read()

pests_list, pest_headers = parse_markdown_table(md_content, "## 1. 害虫一覧")
diseases_list, disease_headers = parse_markdown_table(md_content, "## 2. 病気一覧")

def generate_pest_detail(item, category, headers):
    jp_name_clean = item['key']
    en_key = pest_name_map.get(jp_name_clean, "unknown")
    if en_key == "unknown":
        print(f"Warning: No English key for {jp_name_clean}")
        return # Skip
        
    html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{item['name']} - 庭木の病害虫図鑑</title>
    <link rel="stylesheet" href="../../style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="../../pests.html" style="color:white; text-decoration:none;">庭木の病害虫図鑑</a></h1>
        </div>
    </header>

    <main class="container">
        <h2 class="detail-title" style="margin-top:2rem;">{item['name']}</h2>
        <div class="wip-badge" style="display:inline-block; margin-bottom:2rem;">{category}</div>

        <div class="detail-hero-wrapper" style="background:#f9f9f7; border:2px dashed #ccc;">
            <div style="padding:4rem; color:#aaa; font-weight:bold;">
                画像準備中<br>(Image Placeholder)
            </div>
        </div>

        <div class="data-table-container">
            <table class="data-table">
                <tbody>
                    <tr>
                        <th style="width:30%;">{headers[1]}</th>
                        <td>{item['col2']}</td>
                    </tr>
                    <tr>
                        <th>{headers[2]}</th>
                        <td>{item['col3']}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div style="text-align:center; margin-bottom: 3rem;">
            <a href="../../pests.html" class="back-link">一覧に戻る</a>
        </div>
    </main>

    <footer>
        <div class="container">
            <a href="../../about.html">運営について</a>
            <p>&copy; 2026 Harunami Works</p>
        </div>
    </footer>
</body>
</html>
"""
    with open(os.path.join(PESTS_PAGES_DIR, f"{en_key}.html"), "w", encoding="utf-8") as f:
        f.write(html)

# Generate Detials
for p in pests_list:
    generate_pest_detail(p, "害虫", pest_headers)

for d in diseases_list:
    generate_pest_detail(d, "病気", disease_headers)

# Generate Index (pests.html)
pests_index_html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>庭木の病害虫・病気図鑑 - 植木屋ハルナミワークス</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .pest-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }}
        .pest-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            text-decoration: none;
            color: #333;
            transition: transform 0.2s;
            border-left: 5px solid #ccc;
        }}
        .pest-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .pest-card.pest {{ border-left-color: #e74c3c; }} /* Red for bugs */
        .pest-card.disease {{ border-left-color: #8e44ad; }} /* Purple for diseases */
        
        .pest-title {{
            font-size: 1.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .pest-tag {{
            font-size: 0.8rem;
            padding: 2px 8px;
            border-radius: 4px;
            color: white;
        }}
        .tag-pest {{ background: #e74c3c; }}
        .tag-disease {{ background: #8e44ad; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="index.html">AI生成植木図鑑　byハルナミ</a></h1>
            <p style="font-size: 1rem; margin-top:0.5rem;">庭木の病害虫・病気図鑑</p>
        </div>
    </header>

    <main class="container">
        
        <h2 class="section-header">害虫一覧</h2>
        <div class="pest-grid">
"""

for p in pests_list:
    key = p['key']
    en_key = pest_name_map.get(key)
    if not en_key: continue
    pests_index_html += f"""
            <a href="pages/pests/{en_key}.html" class="pest-card pest">
                <div class="pest-title">
                    {p['name']}
                    <span class="pest-tag tag-pest">害虫</span>
                </div>
                <div style="font-size:0.9rem; color:#666;">詳細を見る →</div>
            </a>
    """

pests_index_html += """
        </div>

        <h2 class="section-header">病気一覧</h2>
        <div class="pest-grid">
"""

for d in diseases_list:
    key = d['key']
    en_key = pest_name_map.get(key)
    if not en_key: continue
    pests_index_html += f"""
            <a href="pages/pests/{en_key}.html" class="pest-card disease">
                <div class="pest-title">
                    {d['name']}
                    <span class="pest-tag tag-disease">病気</span>
                </div>
                <div style="font-size:0.9rem; color:#666;">詳細を見る →</div>
            </a>
    """

pests_index_html += """
        </div>

        <div style="text-align:center; margin-top: 3rem;">
            <a href="index.html" class="back-link">ホームに戻る</a>
        </div>
    </main>

    <footer>
        <div class="container">
            <a href="about.html">運営について</a>
            <p>&copy; 2026 Harunami</p>
        </div>
    </footer>
</body>
</html>
"""

with open(os.path.join(WEB_DIR, "pests.html"), "w", encoding="utf-8") as f:
    f.write(pests_index_html)


# ---------------------------------------------------------
# NEW: Generate Comparison Pages
# ---------------------------------------------------------
COMPARE_MD_PATH = os.path.join(BASE_DIR, "tree_comparison.md")
COMPARE_PAGES_DIR = os.path.join(PAGES_DIR, "compare")
os.makedirs(COMPARE_PAGES_DIR, exist_ok=True)

def simple_markdown_to_html(text):
    """
    Converts simple markdown (Tables, Bold, Italic, Blockquotes) to HTML.
    Specific to the structure of tree_comparison.md.
    """
    html_lines = []
    lines = text.split('\n')
    
    in_table = False
    table_lines = []
    
    in_list = False
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # 1. Tables
        if line.strip().startswith('|'):
            in_table = True
            table_lines.append(line)
            i += 1
            continue
        else:
            if in_table:
                # Process collected table
                html_lines.append('<div class="data-table-container"><table class="data-table">')
                
                # Header
                header_row = table_lines[0]
                cols = [c.strip() for c in header_row.split('|')[1:-1]]
                html_lines.append('<thead><tr>' + ''.join([f'<th>{c}</th>' for c in cols]) + '</tr></thead>')
                
                # Body
                html_lines.append('<tbody>')
                for row_line in table_lines[2:]: # Skip separator line
                    r_cols = [c.strip() for c in row_line.split('|')[1:-1]]
                    # Handle bolding inside cells
                    r_cols = [re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', c) for c in r_cols]
                    html_lines.append('<tr>' + ''.join([f'<td>{c}</td>' for c in r_cols]) + '</tr>')
                html_lines.append('</tbody></table></div>')
                
                in_table = False
                table_lines = []
        
        # 2. Blockquotes / Alerts
        if line.strip().startswith('>'):
            # Check for specific alert types
            content = line.replace('>', '').strip()
            alert_class = "alert-box"
            icon = "💡"
            
            if "[!TIP]" in content:
                alert_class += " alert-tip"
                content = content.replace('[!TIP]', '').strip()
            elif "[!NOTE]" in content:
                alert_class += " alert-note"
                content = content.replace('[!NOTE]', '').strip()
                icon = "📝"
            
            # Combine multi-line quotes? For now assume usually usually single or block.
            # Simple handling: One line per quote or simplistic merging if needed.
            # Let's just output as div. If it's the start of a block, we might want to check next lines.
            # For this file, usually it's > [!TIP]\n> content...
            
            # Better Blockquote handling loop
            quote_block = []
            quote_type = "TIP"
            
            # If line is just marker
            if "[!TIP]" in line: quote_type = "TIP"; i+=1; continue
            if "[!NOTE]" in line: quote_type = "NOTE"; i+=1; continue
            
            # If line content starts with >
            raw_content = line.replace('>', '').strip()
            # Bolding
            raw_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', raw_content)
            
            if quote_type == "TIP":
                html_lines.append(f'<div class="alert-box alert-tip"><div class="alert-icon">💡</div><div class="alert-content">{raw_content}</div></div>')
            else:
                html_lines.append(f'<div class="alert-box alert-note"><div class="alert-icon">📝</div><div class="alert-content">{raw_content}</div></div>')
            
            i += 1
            continue

        # 3. Lists
        if line.strip().startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            item_text = line.replace('- ', '').strip()
            # Bolding
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item_text)
            html_lines.append(f'<li>{item_text}</li>')
            i += 1
            if i < len(lines) and not lines[i].strip().startswith('- '):
                html_lines.append('</ul>')
                in_list = False
            continue
        elif in_list:
             html_lines.append('</ul>')
             in_list = False

        # 4. Normal Text / Empty Lines
        if line.strip() == "":
            html_lines.append('<br>')
        else:
            # Check for headers inside content (e.g. ###)
            if line.startswith('###'):
                html_lines.append(f'<h3>{line.replace("###", "").strip()}</h3>')
            else:
                text_content = line
                text_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text_content)
                html_lines.append(f'<p>{text_content}</p>')
        
        i += 1
        
    return "\n".join(html_lines)


def generate_comparison_pages():
    try:
        with open(COMPARE_MD_PATH, 'r', encoding='utf-8') as f:
            full_md = f.read()
    except FileNotFoundError:
        print("Comparison MD not found.")
        return

    # Split into sections by "## "
    # Note: convert keys to simple eng paths
    
    sections = full_md.split('\n## ')
    compare_items = []
    
    # Skip preamble (index 0) if it doesn't start with 1.
    start_idx = 1 if not sections[0].strip().startswith('1.') else 0
    
    # Actually, the file starts with title then "## 1. ..."
    # So section 0 is the main title and intro. section 1...N are the items.
    
    for section in sections[1:]: # Skip intro
        lines = section.split('\n')
        title_line = lines[0].strip()
        
        # Extract ID and Title
        # Format: "1. Kyara vs Ichii"
        # We want a safe file name.
        safe_fname = "item_" + str(len(compare_items) + 1) # simple incremental id
        
        body_md = "\n".join(lines[1:])
        body_html = simple_markdown_to_html(body_md)
        
        item_data = {
            "title": title_line,
            "filename": safe_fname,
            "content": body_html
        }
        compare_items.append(item_data)
        
        # Generate Detail Page
        page_html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_line} - 似ている庭木の見分け方</title>
    <link rel="stylesheet" href="../../style.css">
    <style>
        .alert-box {{
            padding: 1rem;
            border-radius: 8px;
            margin: 1.5rem 0;
            display: flex;
            align-items: flex-start;
        }}
        .alert-tip {{ background-color: #e8f5e9; border: 1px solid #c8e6c9; color: #2e7d32; }}
        .alert-note {{ background-color: #fff3e0; border: 1px solid #ffe0b2; color: #ef6c00; }}
        .alert-icon {{ font-size: 1.5rem; margin-right: 1rem; }}
        .alert-content strong {{ font-weight: 700; }}
        
        /* Table Styles override/adjust */
        .data-table th {{ background-color: #eaeaea; }}
        
        .content-body {{ line-height: 1.8; }}
        .content-body p {{ margin-bottom: 1rem; }}
        .content-body ul {{ margin-bottom: 1rem; padding-left: 1.5rem; }}
        .content-body li {{ margin-bottom: 0.5rem; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="../../compare.html" style="color:white; text-decoration:none;">似ている庭木の見分け方</a></h1>
        </div>
    </header>

    <main class="container">
        <h2 class="detail-title" style="margin-top:2rem;">{title_line}</h2>
        
        <div class="content-body" style="background:white; padding:2rem; border-radius:12px; box-shadow:0 2px 5px rgba(0,0,0,0.05);">
            {body_html}
        </div>

        <div style="text-align:center; margin: 3rem 0;">
            <a href="../../compare.html" class="back-link">一覧に戻る</a>
        </div>
    </main>

    <footer>
        <div class="container">
            <a href="../../about.html">運営について</a>
            <p>&copy; 2026 Harunami Works</p>
        </div>
    </footer>
</body>
</html>
"""
        with open(os.path.join(COMPARE_PAGES_DIR, f"{safe_fname}.html"), "w", encoding="utf-8") as f:
            f.write(page_html)

    # Generate Index (compare.html)
    index_html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>似ている庭木の見分け方 - 植木屋ハルナミワークス</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .compare-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
        }}
        @media(min-width:600px) {{ .compare-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        
        .compare-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            text-decoration: none;
            color: #333;
            transition: transform 0.2s;
            border-left: 5px solid var(--accent-color);
            display: flex;
            align-items: center;
        }}
        .compare-card:hover {{
            transform: translateX(5px);
            border-left-color: var(--primary-color);
        }}
        .compare-num {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #ccc;
            margin-right: 1rem;
            min-width: 2rem;
        }}
        .compare-title {{
            font-size: 1.2rem;
            font-weight: 700;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="index.html">AI生成植木図鑑　byハルナミ</a></h1>
            <p style="font-size: 1rem; margin-top:0.5rem;">似ている庭木の見分け方</p>
        </div>
    </header>

    <main class="container">
        
        <div class="profile-box" style="margin-bottom:3rem; max-width:100%;">
            <p>見た目が似ていて区別がつきにくい庭木の見分け方をまとめました。<br>
            花がない時期（冬場など）の識別ポイントも解説しています。</p>
        </div>

        <div class="compare-grid">
"""
    
    for i, item in enumerate(compare_items):
        num = i + 1
        index_html += f"""
        <a href="pages/compare/{item['filename']}.html" class="compare-card">
            <span class="compare-num">{num:02}</span>
            <span class="compare-title">{item['title']}</span>
        </a>
        """
        
    index_html += """
        </div>

        <div style="text-align:center; margin-top: 3rem;">
            <a href="index.html" class="back-link">ホームに戻る</a>
        </div>
    </main>

    <footer>
        <div class="container">
            <a href="about.html">運営について</a>
            <p>&copy; 2026 Harunami</p>
        </div>
    </footer>
</body>
</html>
"""
    
    with open(os.path.join(WEB_DIR, "compare.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

# Execute Generation
generate_comparison_pages()

print("Web site generation complete.")
