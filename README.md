# 喜界島オノマトペ・言語アーカイブ

## 概要

このプロジェクトは、鹿児島県喜界島で話されている消滅危機言語「喜界語」を記録・保存するためのデジタルアーカイブシステムです。特にオノマトペ(擬音語・擬態語)を中心に、話者の音声・映像、地理情報、話者属性を紐づけて記録し、継承することを目的としています。

## 主な機能

### 言語記録管理
- **言語記録の閲覧**: オノマトペ・意味・用例、またはYouTube動画のタイトル・説明と音声・映像データを一覧・詳細表示
- **詳細なフィルタリング**: 集落、ファイルの種類、オノマトペ型で絞り込み（一覧リロードでフィルターをクリア可能）
- **話者別・集落別閲覧**: 特定の話者や集落に紐づく記録を一覧表示
- **ページネーション**: 言語記録一覧・地理データ一覧・話者別・集落別で1ページ12件のページネーション
- **言語使用頻度の記録**: ファイル登録時は各記録の言語使用頻度(日常的/よく使用/たまに使用/ほとんど使用しない)を記録可能

### 地図機能
- **インタラクティブな地図表示**: 喜界島の地図上で話者と地理環境データをビジュアル表示
- **年代フィルタリング**: 収録年でデータを絞り込んで表示
- **マーカークラスタリング**: 多数のデータポイントを効率的に表示
- **ポップアップ詳細表示**: マーカーをクリックすると詳細情報を確認可能

### データアップロード
- **言語記録のアップロード**:
  - **ファイルアップロード**: 音声(mp3, wav)、映像(mp4, mov)、画像(jpg, png)をSupabase Storageに保存。オノマトペ・意味・用例・型などの言語情報を入力
  - **YouTube URL登録**: YouTubeの動画URLとタイトル・説明を登録。言語系項目は非表示で、埋め込み表示と「YouTubeで開く」で利用
- **地理環境データのアップロード**: ドローン映像・画像やその他の地理データを登録
  - **ファイル直接アップロード**: Supabase Storageにファイルを保存
  - **YouTube URL登録**: YouTubeにアップロード済みの動画URLを登録して埋め込み表示
- **直感的なUI**: ドラッグ&ドロップに対応したファイルアップロード、アップロード方法（ファイル/YouTube）の切り替えで表示項目を出し分け
- **位置情報取得**: 地理データ登録時に現在地の緯度・経度を自動取得する機能

### その他
- **YouTube動画の埋め込み再生**: 言語記録一覧・話者別・集落別・地理データ一覧・詳細ページ・地図でYouTube動画を埋め込み表示
- **レスポンシブデザイン**: PC、タブレット、スマートフォンに対応

## 技術スタック

本プロジェクトは以下の技術を使用して構築されています。

- **バックエンド**: Django 5.2.4
- **フロントエンド**: HTML5, CSS3, JavaScript, Bootstrap 5.3.0
- **地図**: Folium, Leaflet.js
- **データベース**: PostgreSQL (Supabase)
- **ファイルストレージ**: Supabase Storage
- **外部サービス連携**: YouTube iframe API
- **Webサーバー**: gunicorn
- **静的ファイル処理**: whitenoise
- **その他のライブラリ**: requests（Supabase API・サービス内）, python-dotenv

## セットアップ手順

### 1. 前提条件

以下がインストールされていることを確認してください:
- Python 3.10以上
- Git

### 2. リポジトリのクローン

```bash
git clone https://github.com/miru57o/kikai_language_archive.git
cd kikai_language_archive
```

### 3. 仮想環境の作成と有効化

```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 5. 環境変数の設定

プロジェクトのルートディレクトリに `.env` ファイルを作成し、以下の内容を記述します。

```env
# Django設定
SECRET_KEY='your-secret-key-here'
DEBUG=True
ALLOWED_HOSTS='127.0.0.1,localhost'

# Supabase設定
DATABASE_URL='postgresql://user:password@host:port/database'
SUPABASE_URL='https://your-project.supabase.co'
SUPABASE_SERVICE_ROLE_KEY='your-service-role-key'
```

**注意事項:**
- `SECRET_KEY` には強力なランダム文字列を設定してください(例: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- Supabaseの認証情報は、[Supabaseダッシュボード](https://app.supabase.com/)から取得できます
  - `DATABASE_URL`: Settings > Database > Connection string (URI形式)
  - `SUPABASE_URL`: Settings > API > Project URL
  - `SUPABASE_SERVICE_ROLE_KEY`: Settings > API > service_role key
- 本番環境では `DEBUG=False` に設定してください

### 6. Supabase Storageの設定

Supabaseダッシュボードで以下のバケットを作成してください:
- `audio-files` (音声ファイル用)
- `video-files` (映像ファイル用)
- `image-files` (画像ファイル用)
- `drone-video-files` (ドローン映像用)
- `drone-photo-files` (ドローン画像用)
- `other-geo-files` (その他地理データ用)

各バケットを**パブリック**に設定してください。

### 7. データベースのマイグレーション

```bash
python manage.py migrate
```

指示に従ってユーザー名、メールアドレス、パスワードを入力してください。

### 8. 静的ファイルの収集

```bash
python manage.py collectstatic --no-input
```

### 9. 開発サーバーの起動

```bash
python manage.py runserver
```

ブラウザで `http://127.0.0.1:8000/` にアクセスすると、アプリケーションが表示されます。

管理画面は `http://127.0.0.1:8000/admin/` からアクセスできます。

## データモデル

本システムの主要なデータモデルは以下の通りです。

### Village (集落)
喜界島の集落情報を管理します。
- `name`: 集落名
- `latitude`: 緯度
- `longitude`: 経度
- `description`: 説明(オプション)

### Speaker (話者)
話し手の匿名化された情報を管理します。
- `speaker_id`: 話者ID(例: SPK001)
- `age_range`: 年代(30代、40代など)
- `gender`: 性別(男性/女性/その他)
- `village`: 所属集落(外部キー)
- `consent_video`: 映像公開同意フラグ
- `notes`: 備考

### OnomatopoeiaType (オノマトペ型)
オノマトペの分類を管理します。
- `type_code`: 型コード(例: AABB)
- `type_name`: 型名
- `description`: 説明

### LanguageRecord (言語記録)
オノマトペの音声・映像・画像、またはYouTube動画の記録を管理します。**YouTube URLで登録した場合はタイトル・説明を使用し、言語系項目は未定義にします。**
- `onomatopoeia_text`: オノマトペ表記（YouTubeのみの場合は null）
- `meaning`: 意味（YouTubeのみの場合は null）
- `usage_example`: 用例（YouTubeのみの場合は null）
- `phonetic_notation`: 音声記号（オプション、null 可）
- `language_frequency`: 言語使用頻度（オプション、null 可）
- `file_type`: ファイル種類(音声/映像/画像)
- `file_path`: ファイルURL(Supabase Storage、オプション)
- `thumbnail_path`: サムネイルURL(オプション)
- `youtube_url`: YouTube URL（オプション。設定時は file_path と排他）
- `title`: タイトル（YouTube登録時などに使用、オプション）
- `description`: 説明（YouTube登録時などに使用、オプション）
- `speaker`: 話者(外部キー、PROTECT)
- `onomatopoeia_type`: オノマトペ型(外部キー、オプション)
- `village`: 関連集落(外部キー、オプション)
- `recorded_date`: 収録日
- `notes`: 備考
- `created_at` / `updated_at`: 登録・更新日時

### GeographicRecord (地理環境データ)
ドローン映像や写真などの地理環境データを管理します。
- `title`: タイトル
- `content_type`: コンテンツ種類(ドローン映像/ドローン画像/その他)
- `file_path`: ファイルURL(Supabase Storage、オプション)
- `thumbnail_path`: サムネイルURL(オプション)
- `youtube_url`: YouTube URL(オプション)
- `description`: 説明
- `village`: 関連集落(外部キー)
- `latitude`: 緯度
- `longitude`: 経度
- `captured_date`: 撮影日

**注意:** `file_path` と `youtube_url` はどちらか一方のみを使用します。

## プロジェクト構成

```
kikai_language_archive/
├── kikai_archive_project/      # プロジェクト設定
│   ├── settings.py             # Django設定
│   ├── urls.py                 # URLルーティング
│   └── wsgi.py                 # WSGIエントリーポイント
├── language_archive/           # メインアプリケーション
│   ├── models.py               # データモデル
│   ├── views.py                # ビュー関数
│   ├── forms.py                # フォーム定義
│   ├── services.py             # Supabase連携サービス
│   ├── utils.py                # ユーティリティ（将来拡張用）
│   ├── admin.py                # 管理画面設定
│   ├── templates/              # HTMLテンプレート
│   ├── templatetags/           # カスタムテンプレートタグ
│   └── migrations/             # データベースマイグレーション
├── manage.py                   # Django管理コマンド
├── requirements.txt            # Python依存パッケージ
├── build.sh                    # デプロイ用ビルドスクリプト
├── .gitignore                  # Git除外設定
└── README.md                   # このファイル
```

## 主要な機能の使い方

### 言語記録の登録

**ファイルで登録する場合**
1. ナビゲーションバーから「アップロード」→「言語記録」を選択
2. 「ファイルをアップロード」を選び、ファイルを選択またはドラッグ&ドロップ
3. ファイル種類を選択し、オノマトペ・意味・用例・オノマトペ型などの言語情報を入力
4. 話者・収録日を選択・入力し、「アップロード」をクリック

**YouTubeで登録する場合**
1. 「YouTube URLで登録」を選び、YouTubeの動画URLを入力
2. タイトル（必須）と説明（任意）を入力
3. 話者・収録日を選択・入力し、「アップロード」をクリック  
   （言語系項目は表示されず、登録後は一覧で「説明」として表示されます）

### 地理環境データの登録

1. ナビゲーションバーから「アップロード」→「地理データ」を選択
2. アップロード方法を選択:
   - **ファイルをアップロード**: ドローン映像や画像ファイルを直接アップロード
   - **YouTube URLを入力**: YouTubeにアップロード済みの動画URLを使用
3. タイトル、説明、撮影日などを入力
4. 集落を選択、または緯度・経度を手動入力/現在地取得
5. 「アップロード」ボタンをクリック

**YouTube動画の登録について:**
- YouTubeの動画URL (`https://www.youtube.com/watch?v=...` または `https://youtu.be/...`) をそのまま入力
- 登録後、地理データ一覧や地図上で埋め込み再生が可能
- ファイルストレージの容量を節約できます

### 地図での閲覧

1. ナビゲーションバーから「地図」を選択
2. 収録年でフィルタリング(オプション)
3. マーカーをクリックして詳細情報を表示
   - 青いマーカー: 地理環境データ
   - 赤いマーカー: 話者情報
4. ポップアップ内のリンクから詳細ページへ遷移
   - YouTube動画の場合は「YouTubeで開く」ボタンが表示されます

### 言語記録・地理環境データの閲覧

- **言語記録一覧**: 「言語記録」から一覧表示。集落・ファイル種類・オノマトペ型でフィルター、ページネーション対応。YouTube登録はカードに埋め込みと「説明」表示、「YouTubeで開く」のみ。ファイル登録は「意味」表示と「詳細を見る」。
- **話者別・集落別**: 地図や詳細から話者・集落を選ぶと同様のカード一覧とページネーションで表示。
- **地理環境データ一覧**: 「地理データ」から集落・コンテンツ種類でフィルター、ページネーション。YouTube動画は埋め込みと「YouTubeで開く」、ファイルはサムネイル/プレビューと「表示」。

## トラブルシューティング

### データベース接続エラー

```
FATAL ERROR: DATABASE_URL is not set in production!
```

環境変数 `DATABASE_URL` が設定されていることを確認してください。

### Supabaseアップロードエラー

Supabaseの環境変数が正しく設定されているか確認してください:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

また、Storageバケットが作成され、パブリックアクセスが有効になっているか確認してください。

### 静的ファイルが表示されない

```bash
python manage.py collectstatic --no-input
```

を実行して静的ファイルを収集してください。

### YouTube動画が表示されない

- 入力したYouTube URLの形式が正しいか確認してください
  - 対応形式: `https://www.youtube.com/watch?v=...` または `https://youtu.be/...`
- YouTube動画が公開設定になっているか確認してください（限定公開やプライベートでは埋め込み表示されません）
- ブラウザのコンソールにエラーが表示されていないか確認してください

## 問い合わせ先

本プロジェクトに関するご質問やご意見がございましたら、以下までお気軽にお問い合わせください。

### 研究チーム
- **所属**: 関西学院大学 総合政策学部
- **メールアドレス**: imanishi.ling.lab@gmail.com
