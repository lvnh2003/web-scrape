
# Webスクレイパー（Selenium + YAML設定）

このプロジェクトは、Selenium を用いた汎用的な Web スクレイパーです。
構成可能な `web_config.yml` ファイルにより、複数の異なるサイトを柔軟にスクレイピングできます。

## 必要条件

- Python 3.8+
- Google Chrome（ブラウザ）
- `chromedriver` が環境にインストールされていること

## インストール

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 設定ファイルの作成

`config/web_config.yml` にスクレイピング対象のサイトの設定を記述します。

例:

```yaml
website:
  start_url: "https://example.com/listing"
  item_selector: //div[@class="item"]/a
  next_button_selector: //a[@class="next"]
  detail_selectors:
    title: //h1[@class="title"]
    description:
      xpath: //div[@class="desc"]
    features:
      xpath: //ul[@class="features"]/li/span
      is_multi: true
    pr:
      sub_elements:
        - xpath: //div[@class="pr"]/p
        - xpath: //div[@class="pr"]/ul/li
```
### 各フィールドの意味

| フィールド名 | 説明 |
|--------------|------|
| `start_url` | スクレイピング開始URL |
| `item_selector` | 一覧ページ上のリンクXPath |
| `next_button_selector` | 次ページへのボタンXPath |
| `detail_selectors` | 詳細ページから取得する要素の指定 |

#### `detail_selectors` のパターン

1. **単一要素の指定：**

```yaml
title: //*[@class="job-title"]
```

2. **複数要素を取得したい場合（is_multi: true）：**

```yaml
tags:
  xpath: //*[@class="tags"]/span
  is_multi: true
```

3. **複数のXPathを順に試す場合（sub_elements）：**

```yaml
pr:
  sub_elements:
    - xpath: //*[@id="jobRelatedPR"]/td/div/span
    - xpath: //*[@id="jobRelatedPR"]/td/div/span/div
```

---
### 2. スクレイピングの実行

```bash
python main.py
```

データは `output/` フォルダに以下の形式で保存されます：

- CSV: `output/output.csv`
- JSON: `output/output.json`

## フォルダ構成

```
.
├── config/
│   └── web_config.yml        # スクレイピング設定ファイル
├── scrapers/
│   └── web_scraper.py        # WebScraper クラス本体
├── utils/
│   └── function.py           # 補助関数（例：random_delay）
├── output/                   # 結果保存フォルダ
├── main.py                   # エントリポイント
└── requirements.txt          # 依存パッケージ
```