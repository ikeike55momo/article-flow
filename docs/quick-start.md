# クイックスタートガイド

## ✅ .envファイル作成済み

次は以下の手順で進めてください：

## 1. APIキーの設定

`.env`ファイルを開いて、以下の項目を設定：

```env
# 必須項目
GOOGLE_AI_API_KEY=あなたのAPIキーをここに貼り付け
GOOGLE_CLOUD_PROJECT=your-project-id（省略可）

# 推奨設定
ENVIRONMENT=development
MONTHLY_BUDGET_USD=50
```

### APIキーの取得方法
1. [Google AI Studio](https://aistudio.google.com)にアクセス
2. Googleアカウントでログイン
3. 「Get API key」→「Create API key」
4. 生成されたキーをコピー（一度だけ表示）

## 2. セキュリティ確認

```bash
# Bashで実行（Git Bash推奨）
cd /mnt/c/article-flow
bash scripts/setup-security.sh
```

## 3. 動作テスト

### 簡単なテスト
```bash
# 短い記事でテスト（画像生成も含む）
gemini "爪の健康についての短い記事を作成して"
```

### 出力確認
```bash
# 生成されたディレクトリを確認
ls -la output/

# 最新の出力を確認
ls -la output/$(date +%Y-%m-%d)-*/
```

## 4. トラブルシューティング

### APIキーエラーの場合
```bash
# .envが読み込まれているか確認
cat .env | grep GOOGLE_AI_API_KEY

# 環境変数として設定
export GOOGLE_AI_API_KEY="your-key-here"
```

### MCPエラーの場合
```bash
# VS Codeを使用している場合は再起動
# または、npmが必要な場合：
npm install -g @modelcontextprotocol/server-google-ai
```

## 5. 本格的な記事生成

準備ができたら：
```bash
gemini "爪ケアについての記事を作成して store_url=https://example.com target=30代女性"
```

## 次のアクション

1. APIキーを`.env`に設定
2. テスト記事を1本生成
3. `output/`フォルダで結果確認
4. 問題があれば報告

設定が完了したら教えてください！