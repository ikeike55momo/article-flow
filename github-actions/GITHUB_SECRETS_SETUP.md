# 🔑 GitHub Secrets設定ガイド（必須）

## ⚠️ 重要：この設定がないとワークフローは動作しません

## 1. ANTHROPIC_API_KEY の設定

### 手順：
1. **GitHubリポジトリを開く**
   - https://github.com/ikeike55momo/article-flow

2. **Settings（設定）タブをクリック**
   - リポジトリ上部のメニューから

3. **左サイドバーから選択**
   - `Secrets and variables` → `Actions`

4. **New repository secret をクリック**

5. **以下を入力**：
   - **Name**: `ANTHROPIC_API_KEY`
   - **Secret**: あなたのClaude APIキー

6. **Add secret をクリック**

### APIキーの取得方法：
1. https://console.anthropic.com/ にアクセス
2. ログイン（アカウントがない場合は作成）
3. 左メニューの「API Keys」をクリック
4. 「Create Key」ボタンをクリック
5. キーをコピー（一度しか表示されません！）

## 2. その他の必須Secrets

### GEMINI_API_KEY
- **取得**: https://makersuite.google.com/app/apikey
- **用途**: Web検索と画像生成

### GOOGLE_DRIVE_FOLDER_ID
- **例**: URLが `https://drive.google.com/drive/folders/1234567890abcdefg` なら
- **値**: `1234567890abcdefg`

### GOOGLE_DRIVE_CREDENTIALS
- **形式**: サービスアカウントのJSON全体をコピペ
- **取得方法**: Google Cloud Consoleで作成

## 3. 設定の確認

設定後、以下のように表示されるはずです：

```
Repository secrets (4)
• ANTHROPIC_API_KEY         Updated 1 minute ago
• GEMINI_API_KEY           Updated 1 minute ago
• GOOGLE_DRIVE_CREDENTIALS Updated 1 minute ago
• GOOGLE_DRIVE_FOLDER_ID   Updated 1 minute ago
```

## ⚡ トラブルシューティング

### まだエラーが出る場合：
1. **スペルミスを確認**
   - `ANTHROPIC_API_KEY` (大文字・アンダースコア)
   - 余分なスペースがないか

2. **APIキーの形式を確認**
   - 通常 `sk-ant-...` で始まる
   - 前後にスペースや改行がないか

3. **権限を確認**
   - リポジトリの管理者権限があるか
   - Organizationの場合、Secrets設定が許可されているか

## 🆘 それでも動かない場合

以下の情報を確認してissueを作成：
- エラーメッセージのスクリーンショット
- 設定したSecretsの名前（値は不要）
- 使用しているブラウザ

---

**重要**: APIキーは機密情報です。絶対に他人と共有しないでください。