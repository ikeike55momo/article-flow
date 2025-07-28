# Claude Code + MCP + Imagen4でGitHub Actions画像生成ワークフロー構築ガイド

## 📋 概要

このガイドでは、Claude CodeをGitHub Actions上で実行し、MCPサーバー経由でGoogle Imagen4を使用して画像生成を行う方法を解説します。Kamuicodeを使用せずに、オープンソースのツールを組み合わせて同等の機能を実現します。

## 🎯 実現できること

- GitHub Actions上でClaude Codeを実行
- MCPサーバーを介してImagen4にアクセス
- プロンプトから自動的に画像を生成
- 生成画像をGitHubリポジトリに保存
- PR/Issueからの`@claude`メンションで画像生成

## 🛠️ 必要なコンポーネント

### 1. **Claude Code GitHub Action**
- Anthropic公式のGitHub Action
- `anthropics/claude-code-action@beta`を使用

### 2. **MCPサーバー（Imagen4対応）**
以下のいずれかを選択：
- `gemini-imagen-mcp-server` - Gemini API経由でImagen4アクセス
- `replicate-imagen4-mcp-server` - Replicate経由でImagen4 Ultraアクセス
- カスタムMCPサーバー

### 3. **APIキー**
- Anthropic API Key（Claude Code用）
- Google API Key（Gemini/Imagen用）またはReplicate API Token

## 📝 セットアップ手順

### ステップ1: GitHub Secretsの設定

リポジトリの Settings > Secrets and variables > Actions で以下を追加：

```
ANTHROPIC_API_KEY: あなたのAnthropic APIキー
GEMINI_API_KEY: あなたのGoogle APIキー（Gemini用）
```

### ステップ2: ワークフロー権限の設定

Settings > Actions > General で：
- Workflow permissions: "Read and write permissions" を選択
- "Allow GitHub Actions to create and approve pull requests" にチェック

### ステップ3: GitHub Actionsワークフローの作成

`.github/workflows/claude-imagen-generation.yml` を作成：

```yaml
name: Claude Image Generation with Imagen4
on:
  # 手動実行用
  workflow_dispatch:
    inputs:
      prompt:
        description: '画像生成プロンプト'
        required: true
        type: string
      
  # PRコメントからの実行用
  issue_comment:
    types: [created]

jobs:
  generate-image:
    # PRコメントの場合は@claudeメンションを含む場合のみ実行
    if: |
      github.event_name == 'workflow_dispatch' || 
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude'))
    
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Generate Image with Claude Code
        id: claude-generate
        uses: anthropics/claude-code-action@beta
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          
          # プロンプトの設定（手動実行とコメントで分岐）
          prompt: |
            ${{ github.event_name == 'workflow_dispatch' && format('以下のプロンプトで画像を生成してください: "{0}"', github.event.inputs.prompt) || github.event.comment.body }}
            
            タスク:
            1. プロンプトを分析して、より詳細で効果的な画像生成プロンプトに最適化
            2. MCPサーバーのgemini-imagenツールを使用してImagen4で画像を生成
            3. 生成された画像をimages/ディレクトリに保存
            4. 生成結果をサマリーとして出力
          
          # MCPサーバー設定
          mcp_config: |
            {
              "mcpServers": {
                "gemini-imagen": {
                  "command": "npx",
                  "args": ["-y", "gemini-imagen-mcp-server"],
                  "env": {
                    "GEMINI_API_KEY": "${{ secrets.GEMINI_API_KEY }}"
                  }
                }
              }
            }
          
          # 使用可能なツールの指定
          allowed_tools: |
            Bash(git:*),
            View,
            Edit,
            WriteFile,
            mcp__gemini-imagen__generate_image,
            mcp__gemini-imagen__list_models,
            mcp__gemini-imagen__get_history
          
          # タイムアウト設定（分）
          timeout_minutes: 10
          
      - name: Commit generated images
        if: success()
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add images/
          git diff --staged --quiet || git commit -m "Add generated images via Claude Code"
          git push
```

## 🎨 高度な使用例

### 複数画像の一括生成

```yaml
- name: Batch Image Generation
  uses: anthropics/claude-code-action@beta
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: |
      以下のバリエーションで画像を生成してください:
      1. "サイバーパンク風の東京の夜景"
      2. "浮世絵スタイルの富士山"
      3. "未来的なロボットの肖像画"
      
      各画像について:
      - Imagen4 Ultraモデルを使用
      - アスペクト比は16:9
      - 高品質設定で生成
    mcp_config: |
      {
        "mcpServers": {
          "gemini-imagen": {
            "command": "npx",
            "args": ["-y", "gemini-imagen-mcp-server", "--model", "imagen-4-ultra"],
            "env": {
              "GEMINI_API_KEY": "${{ secrets.GEMINI_API_KEY }}"
            }
          }
        }
      }
```

### 動画生成への拡張

```yaml
- name: Image to Video Pipeline
  uses: anthropics/claude-code-action@beta
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: |
      1. "夕焼けの海岸線"というプロンプトで静止画を生成
      2. 生成された画像をベースにViduで動画を作成
      3. 結果をvideos/ディレクトリに保存
    mcp_config: |
      {
        "mcpServers": {
          "gemini-imagen": {
            "command": "npx",
            "args": ["-y", "gemini-imagen-mcp-server"],
            "env": {
              "GEMINI_API_KEY": "${{ secrets.GEMINI_API_KEY }}"
            }
          },
          "vidu": {
            "command": "npx",
            "args": ["-y", "vidu-mcp-server"],
            "env": {
              "VIDU_API_KEY": "${{ secrets.VIDU_API_KEY }}"
            }
          }
        }
      }
```

## 🔧 MCPサーバーオプション

### オプション1: gemini-imagen-mcp-server（推奨）

**特徴:**
- Gemini API直接統合
- Imagen 3, 4, 4 Ultraサポート
- バッチ処理対応
- プロジェクトフォルダへの自動保存

**設定例:**
```json
{
  "mcpServers": {
    "gemini-imagen": {
      "command": "npx",
      "args": [
        "-y", 
        "gemini-imagen-mcp-server",
        "--model", "imagen-4-ultra",
        "--batch",
        "--max-batch-size", "5"
      ],
      "env": {
        "GEMINI_API_KEY": "${{ secrets.GEMINI_API_KEY }}"
      }
    }
  }
}
```

### オプション2: replicate-imagen4-mcp-server

**特徴:**
- Replicate経由でImagen4 Ultraアクセス
- 自動画像ダウンロード
- 複数アスペクト比サポート

**設定例:**
```json
{
  "mcpServers": {
    "replicate-imagen4": {
      "command": "npx",
      "args": ["-y", "https://github.com/PierrunoYT/replicate-imagen4-mcp-server.git"],
      "env": {
        "REPLICATE_API_TOKEN": "${{ secrets.REPLICATE_API_TOKEN }}"
      }
    }
  }
}
```

## 📊 プロンプト最適化のベストプラクティス

Claude Codeにプロンプト最適化を任せる場合の指示例：

```yaml
prompt: |
  ユーザープロンプト: "${{ github.event.inputs.prompt }}"
  
  このプロンプトを以下の観点で最適化してください:
  1. 具体的な視覚的詳細を追加
  2. 照明、色彩、構図の指定
  3. アートスタイルや参照の追加
  4. ネガティブプロンプトの考慮
  
  最適化後、Imagen4で画像を生成してください。
```

## 🚨 トラブルシューティング

### よくある問題と解決方法

1. **"Credit balance is too low"エラー**
   - Anthropic ConsoleでAPIクレジットを追加
   - Claude ProとAPI利用は別料金

2. **MCPサーバー接続エラー**
   - APIキーが正しく設定されているか確認
   - MCPサーバーのnpmパッケージが最新版か確認

3. **画像生成失敗**
   - プロンプトがコンテンツポリシーに準拠しているか確認
   - APIの利用制限に達していないか確認

4. **権限エラー**
   - Workflow permissionsが正しく設定されているか確認
   - GitHub Tokenの権限を確認

## 📚 参考リンク

- [Claude Code GitHub Actions公式ドキュメント](https://docs.anthropic.com/en/docs/claude-code/github-actions)
- [Anthropic Claude Code Action](https://github.com/anthropics/claude-code-action)
- [gemini-imagen-mcp-server](https://github.com/serkanhaslak/gemini-imagen-mcp-server)
- [MCP (Model Context Protocol)仕様](https://modelcontextprotocol.io/)

## 💡 次のステップ

1. **カスタムMCPサーバーの開発**
   - 独自の画像処理ロジックを実装
   - 複数の画像生成APIを統合

2. **ワークフローの拡張**
   - Slackへの通知統合
   - 生成画像の自動最適化
   - A/Bテストの実装

3. **コスト最適化**
   - キャッシュの実装
   - 条件付き実行の追加
   - リソース使用量のモニタリング

---

このガイドに従うことで、Kamuicodeに依存せずに、オープンソースツールを組み合わせた柔軟な画像生成ワークフローを構築できます。各コンポーネントは独立して更新・カスタマイズ可能なため、将来的な拡張も容易です。