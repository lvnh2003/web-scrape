
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

#### .env ファイルの設定する内容
```bash
cp .env.example .env
```
.env ファイルには以下のような環境変数を記述します

例:
```
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=your_database_name
  DB_USER=your_username
  DB_PASSWORD=your_password
```

データベース設定ファイル `config/db_config.yml`

このファイルでは、PostgreSQL の保存に関する詳細なマッピング設定を行います。
.env ファイルが接続情報を定義するのに対し、db_config.yml は「どの項目をどのカラムに保存するか」を制御します。

例:

```yaml
table: job_listings
columns:
  title: TEXT
  description: TEXT
  features: TEXT
```

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
│   ├── db_config.yml        # DB設定ファイル（保存先テーブルやカラムマッピングを定義）
│   └── web_config.yml       # スクレイピング対象サイトのセレクターや構造設定
│
├── output/                  # スクレイピング結果の保存先（CSVやJSONなど）
│
├── scrapers/
│   ├── driver.py            # Seleniumのドライバー初期化など
│   ├── extractor.py         # セレクターに従ってデータを抽出
│   └── process.py           # データ整形・加工・構造調整など
│
├── utils/
│   ├── db.py                # PostgreSQLとの接続・保存処理
│   └── function.py          # 汎用的な関数（delay, loggingなど）
│
├── main.py                  # メインの実行スクリプト（エントリーポイント）
│
├── .env                     # DB接続情報などの環境変数
├── .env.example             # .envのサンプルファイル
├── requirements.txt         # Pythonパッケージの依存関係
├── README.md                # 本ファイル（ドキュメント）
└── .gitignore               # Gitで無視するファイル
```