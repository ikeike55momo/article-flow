# 🚀 GitHub Actions セットアップガイド（クイックスタート版）

## 📝 前提条件
- GitHubリポジトリへの管理者アクセス権限
- 各種APIキー（Claude、Gemini、Google Drive）

## 🔧 ステップ1: GitHub Secretsの設定

### 1-1. リポジトリ設定を開く
1. GitHubリポジトリを開く
2. `Settings` タブをクリック
3. 左メニューの `Secrets and variables` → `Actions` を選択

### 1-2. 必須シークレットを追加
`New repository secret` ボタンをクリックして以下を設定：

#### ANTHROPIC_API_KEY
- **Name**: `ANTHROPIC_API_KEY`
- **Value**: Claudeのアピキー
- 取得: https://console.anthropic.com/

#### GEMINI_API_KEY
- **Name**: `GEMINI_API_KEY`
- **Value**: GeminiのAPIキー
- 取得: https://makersuite.google.com/app/apikey
- 注意: `GOOGLE_AI_API_KEY`から名前変更

#### GOOGLE_DRIVE_FOLDER_ID
- **Name**: `GOOGLE_DRIVE_FOLDER_ID`
- **Value**: アップロード先フォルダのID
- 例: URLが `https://drive.google.com/drive/folders/1234567890abcdefg` なら `1234567890abcdefg`

#### GOOGLE_DRIVE_CREDENTIALS
- **Name**: `GOOGLE_DRIVE_CREDENTIALS`
- **Value**: サービスアカウントのJSON（全内容をコピペ）

### 1-3. オプションシークレット
#### SLACK_WEBHOOK（任意）
- **Name**: `SLACK_WEBHOOK`
- **Value**: SlackのWebhook URL
- 設定すると記事生成完了時に通知

## 🔑 ステップ2: Google Drive認証設定

### 2-1. Google Cloud Consoleでプロジェクト作成
1. https://console.cloud.google.com/ にアクセス
2. 新規プロジェクト作成または既存プロジェクト選択

### 2-2. サービスアカウント作成
1. `APIとサービス` → `認証情報`
2. `認証情報を作成` → `サービスアカウント`
3. 名前: `article-flow-automation`（任意）
4. `作成して続行`

### 2-3. Google Drive API有効化
1. `APIとサービス` → `ライブラリ`
2. `Google Drive API` を検索
3. `有効にする`

### 2-4. 認証キー作成
1. `APIとサービス` → `認証情報`
2. 作成したサービスアカウントをクリック
3. `キー` タブ → `鍵を追加` → `新しい鍵を作成`
4. **JSON形式**を選択してダウンロード

### 2-5. Driveフォルダへアクセス権付与
1. Google Driveで記事保存用フォルダを開く
2. 右クリック → `共有`
3. サービスアカウントのメールアドレスを追加
   - 例: `article-flow@project-id.iam.gserviceaccount.com`
4. **編集者**権限を付与

### 2-6. JSONをGitHub Secretsに登録
1. ダウンロードしたJSONファイルを開く
2. **全内容をコピー**
3. GitHub Secretsの `GOOGLE_DRIVE_CREDENTIALS` に貼り付け

## ✅ ステップ3: 動作確認

### 3-1. ワークフロー実行
1. GitHubリポジトリの `Actions` タブ
2. `Article Generation Pipeline v2` を選択
3. `Run workflow` をクリック

### 3-2. テスト実行（推奨設定）
```yaml
Topic: テスト記事の作成
Store URL: （空欄でOK）
Target Audience: セルフケア志向の女性
Word Count: 1000
Auto Publish: false  # 初回はfalseを推奨
Enable Image Generation: false  # 初回はfalseを推奨
```

### 3-3. 実行状況確認
- 緑のチェック✅: 成功
- 赤の×: エラー（ログを確認）
- 黄色の○: 実行中

## 🚨 よくあるエラーと対処法

### Error: Authentication failed
**原因**: APIキーが正しく設定されていない
**対処**: 
- Secretsのスペルを確認
- APIキーに余分なスペースがないか確認

### Error: Rate limit exceeded
**原因**: API使用制限に到達
**対処**: 
- 15-30分待って再実行
- APIプランをアップグレード

### Error: Permission denied (Google Drive)
**原因**: サービスアカウントにフォルダ権限がない
**対処**: 
- フォルダ共有設定を確認
- 編集者権限になっているか確認

## 📊 実行時間の目安

| 設定 | 実行時間 |
|------|----------|
| 1000字・画像なし | 約15-20分 |
| 3200字・画像なし | 約25-30分 |
| 3200字・画像あり | 約30-35分 |

## 🎯 次のステップ

1. **本番実行**
   - Word Count: 3200
   - Auto Publish: true
   - Enable Image Generation: true

2. **カスタマイズ**
   - `prompts/`フォルダ内のファイルを編集
   - 記事のトーン、スタイルを調整

3. **定期実行設定**
   - GitHub Actionsのschedule機能で自動化

## 📚 関連ドキュメント
- [詳細設定ガイド](README.md)
- [トラブルシューティング](CRITICAL_ISSUES.md)
- [移行ガイド](MIGRATION_GUIDE.md)

---

**質問がある場合**: GitHubでIssueを作成してください。