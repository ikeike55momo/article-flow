# Gemini CLI 使用ガイド

## 概要

Gemini CLIは、Google製のオープンソースAIエージェントです。このガイドでは、記事生成ワークフローでGemini CLIを正しく使用する方法を説明します。

## 設定ファイル

### 1. GEMINI.md（コンテキストファイル）

**場所**: `/mnt/c/article-flow/GEMINI.md`

Gemini CLIは自動的にこのファイルを読み込み、プロジェクト固有の指示として使用します。

### 2. .gemini/settings.json（プロジェクト設定）

**場所**: `/mnt/c/article-flow/.gemini/settings.json`

```json
{
  "mcpServers": {
    "google-ai-imagen": {
      "command": "bash",
      "args": [
        "-c",
        "cd /mnt/c/article-flow && source .env && python3 scripts/imagen-mcp-server.py"
      ]
    }
  }
}
```

### 3. 環境変数（.env）

**場所**: `/mnt/c/article-flow/.env`

```bash
GOOGLE_AI_API_KEY=your_api_key_here
GOOGLE_CLOUD_PROJECT=article-flow-imagen
```

## 正しい使用方法

### 方法1: 自動実行（GEMINI.mdを利用）

```bash
gemini "爪ケアについて記事を作成して"
```

GEMINI.mdファイルが存在する場合、Geminiは自動的にワークフローを実行します。

### 方法2: 明示的な指示

```bash
gemini "INSTRUCTIONS_v2.mdのワークフローに従って爪ケアについて記事を作成して"
```

### 方法3: ファイルメンション

```bash
gemini "@INSTRUCTIONS_v2.md 爪ケアについて記事を作成して"
```

## MCPサーバーの確認

```bash
# MCPサーバーの状態を確認
gemini --list-mcp-servers

# または会話中に
/mcp
```

## トラブルシューティング

### 問題: ワークフローが実行されない

**原因**: GEMINI.mdファイルが読み込まれていない

**解決策**:
1. GEMINI.mdがプロジェクトルートに存在することを確認
2. Geminiを再起動
3. 明示的にINSTRUCTIONS_v2.mdをメンション

### 問題: MCPサーバーが"Disconnected"

**原因**: 環境変数が読み込まれていない

**解決策**:
1. `.env`ファイルの改行コードをLF（Unix形式）に変換
   ```bash
   dos2unix .env
   ```
2. Geminiを再起動

### 問題: 画像が生成されない

**原因**: MCPサーバーが接続されていない

**解決策**:
1. MCPサーバーの状態を確認（`/mcp`）
2. Pythonの依存関係をインストール
   ```bash
   pip install mcp httpx
   ```

## 期待される出力

記事作成を依頼すると、以下のディレクトリ構造が作成されます：

```
output/2025-07-23-{title}/
├── 00_parsed_request.json      # リクエスト解析
├── 01_research_data.md         # リサーチ結果
├── 02_article_structure.md     # 記事構成
├── 03_draft.md                 # 初稿
├── 03_5_factchecked_draft.md   # ファクトチェック済み
├── 03_5_factcheck_report.json  # ファクトチェックレポート
├── 04_optimized_draft.html     # SEO最適化版
├── 04_5_image_metadata.json    # 画像メタデータ
├── 04_5_with_images.html       # 画像統合版
├── 05_quality_report.json      # 品質レポート
└── final.html                  # 最終版（WordPress対応）
```

## 重要な注意事項

1. **`.gemini-cli-config.yaml`は使用しない**
   - Gemini CLIは`.gemini/settings.json`を使用します
   - トリガーパターンはClaude Code専用の機能です

2. **GEMINI.mdファイルが重要**
   - このファイルでワークフロー実行を指示
   - プロジェクトルートに配置必須

3. **画像生成はMCP経由**
   - google-ai-imagenサーバーが接続されている必要があります
   - 外部ツールでの手動生成も可能

## チーム共有時の設定

新しいチームメンバーがプロジェクトを使用する場合：

1. リポジトリをクローン
2. `.env`ファイルを作成（API keyを設定）
3. Python依存関係をインストール
   ```bash
   pip install mcp httpx
   ```
4. Gemini CLIで記事作成を実行

これで、Gemini CLIが正しくワークフローを実行するようになります。