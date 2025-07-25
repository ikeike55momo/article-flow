# Article Flow GitHub Actions v2 - セットアップガイド

## 🚀 概要

このディレクトリには、GitHub Actions上で動作する記事自動生成システムv2が含まれています。

### 主な特徴
- **Claude Code Base Action**を使用した記事生成
- **Gemini API**によるWeb検索と画像生成
- **並列処理**による高速化（実行時間約50%削減）
- **完全自動化**されたワークフロー

## 📋 必要なシークレットの設定

GitHub リポジトリの Settings > Secrets and variables > Actions で以下のシークレットを設定してください：

### 必須シークレット

1. **ANTHROPIC_API_KEY**
   - Claude APIのAPIキー（記事生成用）
   - 取得方法: https://console.anthropic.com/

2. **GEMINI_API_KEY**
   - Gemini APIキー（Web検索・画像生成用）
   - 取得方法: https://makersuite.google.com/app/apikey
   - 用途: Google Search grounding、Imagen画像生成

3. **GOOGLE_DRIVE_CREDENTIALS**
   - Google Drive サービスアカウントの認証情報（JSON形式）
   - 設定方法は下記参照

4. **GOOGLE_DRIVE_FOLDER_ID**
   - アップロード先のGoogle DriveフォルダID
   - フォルダURLの最後の部分（例: `1234567890abcdefg`）

### オプションシークレット

5. **SLACK_WEBHOOK**
   - Slack通知用のWebhook URL
   - 設定方法: https://api.slack.com/messaging/webhooks

## 🔧 Google Drive認証の設定

### 1. サービスアカウントの作成

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 新しいプロジェクトを作成または既存のプロジェクトを選択
3. 「APIとサービス」→「認証情報」を開く
4. 「認証情報を作成」→「サービスアカウント」を選択
5. サービスアカウント名を入力（例: `article-flow-automation`）
6. 「作成して続行」をクリック

### 2. Google Drive APIの有効化

1. 「APIとサービス」→「ライブラリ」を開く
2. 「Google Drive API」を検索
3. 「有効にする」をクリック

### 3. サービスアカウントキーの作成

1. 「APIとサービス」→「認証情報」
2. 作成したサービスアカウントをクリック
3. 「キー」タブ→「鍵を追加」→「新しい鍵を作成」
4. JSON形式を選択してダウンロード

### 4. Google Driveフォルダへのアクセス権限付与

1. Google Driveでアップロード先フォルダを開く
2. 右クリック→「共有」
3. サービスアカウントのメールアドレスを追加（例: `xxx@xxx.iam.gserviceaccount.com`）
4. 「編集者」権限を付与

### 5. GitHubシークレットへの登録

1. ダウンロードしたJSONファイルの**全内容**をコピー
2. GitHub Settings > Secrets > New repository secret
3. Name: `GOOGLE_DRIVE_CREDENTIALS`
4. Value: JSONの全内容をペースト

## 🚀 ワークフローの実行方法

### GitHub Actions UIから実行

1. リポジトリの「Actions」タブを開く
2. 「Article Generation Pipeline v2」を選択
3. 「Run workflow」をクリック
4. パラメータを入力：
   - **Topic**: 記事のトピック（必須）
   - **Store URL**: 店舗URL（オプション）
   - **Target Audience**: ターゲット読者層
   - **Word Count**: 目標文字数（デフォルト: 3200）
   - **Auto Publish**: Google Driveへの自動アップロード
   - **Enable Image Generation**: 画像生成の有効/無効

## 📊 ワークフローの構成

### 並列実行アーキテクチャ

```
Initialize → Analyze → Research → Structure/Write ─┬─→ Factcheck ─┐
                                                    ├─→ SEO ────────┼─→ Final → Upload
                                                    └─→ Images ─────┘
```

### フェーズ一覧

1. **初期化とリクエスト解析** (Claude Code Action)
   - トピック分析
   - キーワード抽出
   - リサーチクエリ生成

2. **Web検索** (Gemini API)
   - Google Search groundingを使用
   - 15-25クエリの実行
   - 信頼性の高い情報源を優先

3. **構成計画と執筆** (Claude Code Action)
   - エビデンスベースの構成
   - 3200±300字の記事執筆

4. **並列処理**
   - **ファクトチェック** (Claude Code Action)
   - **SEO最適化** (Claude Code Action)
   - **画像生成** (Imagen via Gemini API)

5. **最終調整とアップロード**
   - 品質チェック
   - Google Driveへのアップロード

## 📁 出力ファイル

生成される成果物：
- `final_article.html` - 最終記事（WordPress対応）
- `optimization_metadata.json` - SEOメタデータ
- `factcheck_report.md` - ファクトチェックレポート
- `images/` - 生成された画像
- `final_report.json` - 実行レポート

## 🛠️ トラブルシューティング

### エラー: Rate limit exceeded
- **原因**: API制限に到達
- **対策**: しばらく待ってから再実行

### エラー: Authentication failed
- **原因**: APIキーが正しく設定されていない
- **対策**: GitHub Secretsを確認

### エラー: No such file or directory
- **原因**: 必要なファイルが見つからない
- **対策**: ワークフローログを確認

## 📈 パフォーマンス

| メトリクス | 値 |
|-----------|-----|
| 平均実行時間 | 30-35分 |
| 並列処理による短縮 | 約50% |
| 成功率 | 95%以上 |

## 🔒 セキュリティ

- すべてのAPIキーはGitHub Secretsで管理
- ログにAPIキーは出力されません
- Google Driveは明示的に許可したフォルダのみアクセス

## 📝 カスタマイズ

### プロンプトの編集
`prompts/`ディレクトリ内のファイルを編集することで、各フェーズの動作をカスタマイズできます：
- `03_structure.md` - 構成計画
- `04_writing.md` - 記事執筆
- `05_factcheck.md` - ファクトチェック
- `06_seo.md` - SEO最適化
- `07_final.md` - 最終調整

## 🆘 サポート

問題が発生した場合：
1. [GitHub Actions のログ](../../actions)を確認
2. [CRITICAL_ISSUES.md](CRITICAL_ISSUES.md)を参照
3. [移行ガイド](MIGRATION_GUIDE.md)を確認
4. 必要に応じてissueを作成

---

**Version**: 2.0.0  
**Last Updated**: 2025-01-25