# Google Cloud Platform & Imagen API セットアップガイド

## 前提条件
- Googleアカウント
- クレジットカード（無料枠の認証用）
- 新規アカウントの場合、$300の無料クレジット（90日間）

## セットアップ手順

### 1. Google AI Studioでの準備

1. **Google AI Studioにアクセス**
   ```
   https://aistudio.google.com
   ```

2. **APIキーの生成**
   - 左サイドバーの「Get API key」をクリック
   - 「Create API key」を選択
   - プロジェクトを選択または新規作成
   - APIキーをコピー（一度しか表示されません）

3. **APIキーの確認**
   ```bash
   # ターミナルでテスト
   curl -H "Content-Type: application/json" \
        -H "x-goog-api-key: YOUR_API_KEY" \
        -X POST https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent \
        -d '{"contents": [{"parts": [{"text": "Hello"}]}]}'
   ```

### 2. Google Cloud Projectの設定（必要な場合）

1. **Google Cloud Consoleにアクセス**
   ```
   https://console.cloud.google.com
   ```

2. **新規プロジェクト作成**
   - プロジェクト名: `article-flow-imagen`
   - 組織: 個人の場合は「組織なし」
   - 請求先アカウントを設定

3. **Vertex AI APIの有効化**
   ```bash
   # Cloud Shell または ローカルのgcloud CLIで実行
   gcloud services enable aiplatform.googleapis.com
   ```

### 3. 料金設定の確認

#### 現在の料金（2025年1月）
```
Imagen 3（最新モデル）:
- 1024×1024画像: 約$0.04/画像
- 512×512画像: 約$0.02/画像

月間見積もり:
- 100画像/月: 約$4
- 500画像/月: 約$20
- 1000画像/月: 約$40
```

#### 予算アラートの設定
1. Cloud Console > 請求 > 予算とアラート
2. 「予算を作成」をクリック
3. 月額予算: $50
4. アラート: 50%, 90%, 100%で通知

### 4. 環境変数の設定

1. **プロジェクトルートに.envファイルを作成**
   ```bash
   cd /mnt/c/article-flow
   touch .env
   ```

2. **.envファイルに追加**
   ```env
   # Google AI API設定
   GOOGLE_AI_API_KEY=your_api_key_here
   GOOGLE_CLOUD_PROJECT=article-flow-imagen
   GOOGLE_AI_LOCATION=us-central1
   
   # セキュリティ設定
   API_KEY_ROTATION_DAYS=30
   ```

3. **.gitignoreの確認**
   ```bash
   # .envが除外されていることを確認
   grep -E "^\.env$" .gitignore || echo ".env" >> .gitignore
   ```

### 5. APIキーのセキュリティ設定

1. **APIキーの制限**
   - Google Cloud Console > APIとサービス > 認証情報
   - APIキーをクリック
   - 「APIの制限」を設定:
     - Generative Language API
     - Vertex AI API
   - 「アプリケーションの制限」を設定:
     - IPアドレス制限（本番環境）
     - HTTPリファラー（開発環境）

2. **サービスアカウント（推奨）**
   ```bash
   # サービスアカウント作成
   gcloud iam service-accounts create article-flow-imagen \
     --display-name="Article Flow Imagen Service"
   
   # キーファイル生成
   gcloud iam service-accounts keys create ./credentials/service-account.json \
     --iam-account=article-flow-imagen@${PROJECT_ID}.iam.gserviceaccount.com
   ```

### 6. 動作確認

1. **MCP接続テスト**
   ```bash
   # Gemini CLIでMCPサーバーの確認
   gemini --list-mcp-servers
   ```

2. **画像生成テスト**
   ```bash
   # テスト記事で画像生成を確認
   gemini "テスト用の短い記事を作成して（画像生成テスト付き）"
   ```

## トラブルシューティング

### エラー: "API key not valid"
- APIキーが正しくコピーされているか確認
- APIが有効化されているか確認
- プロジェクトIDが正しいか確認

### エラー: "Quota exceeded"
- 無料枠を超過している可能性
- Cloud Consoleで使用量を確認
- 必要に応じて課金を有効化

### エラー: "MCP server not found"
- VS Codeを再起動
- .vscode/mcp.jsonが正しく配置されているか確認
- npmがインストールされているか確認

## コスト管理のベストプラクティス

1. **開発環境での制限**
   - 低解像度（512×512）でテスト
   - 生成数を1枚に制限
   - キャッシュの活用

2. **本番環境での最適化**
   - 必要な画像のみ生成
   - 一度生成した画像は再利用
   - 月次レビューで使用量確認

3. **予算超過の防止**
   - Cloud Functionsでの使用量監視
   - 自動停止の設定
   - チーム内での使用量共有

## 次のステップ

設定が完了したら、[チーム向けセットアップガイド](./team-setup-guide.md)を参照してください。