# 樹種別キャラクター背景生成ガイド

これまでの検証で確立した、**「特定の樹木の正確な特徴を背景に反映させつつ、キャラクターを引き立てる画像」**を生成するための共通ワークフローです。
ユーザーからの追加要望（構図・スケール感）を反映しています。

---

## 1. 準備フェーズ (Preparation)

生成を始める前に、素材と情報を揃えます。

### A. 参照画像の選定
`C:\Users\harunami\Desktop\helloworld\plant_images` ディレクトリ内の、対象樹種のフォルダを確認します。
*   **選定基準**:
    *   葉の形状、実、花などの「その木らしさ」がはっきり写っているもの。
    *   日本語ファイル名でエラーが出る場合は、適宜同種の英語名ファイルを探すか代替画像を使用する。

### B. 樹木データの確認 (重要)
キャラクター（人間大）とのサイズ感を合わせるため、以下を確認します。
*   **平均樹高**: その木が通常どのくらいの高さに育つか。
*   **季節の特徴**: その時期に実がなるか、花が咲くか。

---

## 2. 生成設定 (Generation Settings)

### 基本方針 (New!)
*   **構図**: 必ずしも背景全体を指定の樹木で覆う必要はありません。**1本～3本程度の樹木**と、それに馴染む**自然な風景・情景**（空、庭園、森の小道など）を組み合わせます。
*   **スケール感**: キャラクターを人間大とし、樹木は**「庭木としての平均的な大きさの半分程度のサイズ感」**で配置します。（威圧感を与えず、背景として程よい大きさに収めるため）。

### プロンプト構築 (Prompt Template)

```markdown
(基本スタイル)
Anime style, high quality illustration,

(キャラクター指示 - 中央配置・強調)
Character from the first image placed in the center, large and prominent, human scale,

(樹種と特徴の指定)
Background features [樹木名 (英語/学名)] explicitly,
[特徴的なディテール (例: speckled leaves, red berries)],

(配置と構図 - New!)
[1-3 trees only], integrated into a [自然な情景 (e.g., natural garden scene, open sky, forest path)],
Composition is balanced, trees are NOT overwhelming,

(スケール調整 - New!)
[スケール指示 (e.g., Trees are scaled to approx half of average garden size, looking like young or manicured trees)],
[Height relationship (e.g., slightly taller than character / waist high shrubs)],

(雰囲気と背景の主張コントロール)
[背景の主張 (e.g., soft focus, depth of field, unobstructed view of character)],
[光と空気感 (e.g., soft sunlight, airy atmosphere)]
```

---

## 3. 調整のポイント (Refinement Tips)

| 課題 | 解決策のプロンプト例 |
| :--- | :--- |
| **背景がうるさい / キャラが埋もれる** | ・`soft focus`, `muted colors` (色味を抑える)<br>・`1-3 trees only` (本数を絞る)<br>・`open space`, `blue sky` (抜けを作る) |
| **木のサイズが大きすぎる** | ・`small tree`, `young tree` (若木)<br>・`half size of average tree`<br>・`pruned garden tree` (手入れされた庭木) |
| **「その木らしさ」が足りない** | ・植物の参照画像の `Denoising Strength` (変更度) を下げる。<br>・プロンプトで特徴を具体的に記述 (例: `jagged leaves`, `smooth bark`) |

---

## 実践例：アオキの場合のパラメータ

*   **Tree Name**: Japanese Aucuba (Aoki)
*   **Scale**: Small shrub (approx 1-1.5m, waist to chest high)
*   **Features**: Spotted/Speckled leaves, Red berries
*   **composition**: Single bush next to a stone lantern, soft garden background.
