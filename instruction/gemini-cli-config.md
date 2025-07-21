# Gemini CLI用追加設定

## .gemini-cli-config.yaml

```yaml
# Gemini CLI用設定ファイル
project:
  name: "SEO Article Generator"
  version: "2.0"
  description: "SEO最適化記事自動生成システム"

# コマンド設定
commands:
  article:
    description: "SEO記事を生成"
    trigger_patterns:
      - "についての記事を作成"
      - "に関する記事"
      - "のSEO記事"
    execute: "INSTRUCTIONS.md"

# Gemini特有の設定
gemini_settings:
  model: "gemini-pro"
  temperature: 0.7
  max_output_tokens: 8000
  
# ツール設定
tools:
  web_search:
    enabled: true
    max_queries_per_phase: 20
  
# ファイル読み込み
context_files:
  - path: "INSTRUCTIONS.md"
    priority: "high"
  - path: "config/*.yaml"
    priority: "medium"
  - path: "prompts/*.md"
    priority: "high"
  - path: "assets/wordpress.css"
    priority: "high"

# 出力設定
output:
  format: "html"
  save_to_file: true
  create_artifact: true
```

## INSTRUCTIONS_GEMINI.md（Gemini用に最適化）

```markdown
# SEO記事生成システム - Gemini CLI実行指示書

あなたはSEO記事生成の専門家です。ユーザーから「○○についての記事を作成して」という指示を受けたら、以下のワークフローに従って高品質な記事を生成してください。

## Gemini CLI特有の注意事項

1. **web検索の実行**
   - Geminiの検索機能を使用
   - 各フェーズで指定された回数を実行
   - 検索結果を適切に要約して使用

2. **ファイル読み込み**
   - prompts/フォルダ内の各指示を順次読み込み
   - assets/wordpress.cssは変更せずそのまま使用

3. **出力形式**
   - 最終成果物はHTMLコードブロックで出力
   - ファイル保存も同時に実行

## 実行フロー

### ステップ0: リクエスト解析
`prompts/00_parse_request.md`の指示に従い、以下を実行：
- ユーザーリクエストの解析
- 不足情報の推測と補完
- パラメータの設定

### ステップ1: リサーチ
`prompts/01_research.md`の指示に従い：
- 最低10回、最大20回のweb検索
- 競合分析と最新情報収集
- 信頼できる情報源の確保

### ステップ2: 構成計画
`prompts/02_structure.md`の指示に従い：
- 記事の詳細構成を設計
- キーワード配置計画
- 各セクションの内容決定

### ステップ3: 執筆
`prompts/03_writing.md`の指示に従い：
- 完全オリジナルの文章作成
- 指定文字数の厳守
- 専門性と読みやすさの両立

### ステップ4: 最適化
`prompts/04_optimization.md`の指示に従い：
- HTML形式への変換
- SEO/LLMO最適化
- **重要**: CSSは変更せず`assets/wordpress.css`をそのまま使用

### ステップ5: 最終調整
`prompts/05_finalization.md`の指示に従い：
- 品質スコアのチェック（85点以上必須）
- 最終的な調整と確認
- WordPress用HTMLの完成

## Gemini CLI用の出力フォーマット

```
=== 処理完了サマリー ===
📝 記事タイトル: [生成したタイトル]
📊 総文字数: [文字数]
✅ 品質スコア: [スコア]/100
🔍 メインキーワード: [キーワード]
🎯 ターゲット: [読者層]

=== 最終成果物（WordPress用HTML）===
```html
[完全なHTML]
```

💾 ファイル保存先: output/[日時]_[タイトル]/final.html
```

## エラーハンドリング

Gemini CLIで発生しやすいエラーと対処：

1. **検索制限エラー**
   - 検索回数を調整
   - 重要な検索を優先

2. **出力文字数制限**
   - 必要に応じて分割出力
   - 重要部分を優先

3. **ファイル読み込みエラー**
   - 代替手段で内容を参照
   - エラー内容を明示

## 品質保証

必ず以下を確認：
- [ ] オリジナル文章100%
- [ ] CSS変更なし
- [ ] 文字数3200±300
- [ ] キーワード密度適正
- [ ] 構造化データ正確
```

## 使い方の違い

### Claude Code
```bash
claude-code "爪ケアについての記事を作成して"
```

### Gemini CLI
```bash
# 基本的な使い方
gemini article "爪ケアについての記事を作成して"

# 設定ファイルを指定
gemini --config .gemini-cli-config.yaml "爪ケアについての記事を作成して"

# 詳細パラメータ指定
gemini article "爪ケアについての記事を作成して" \
  --param store_url=https://nailsalon-plus1.com/ \
  --param target=セルフケア志向の女性
```

## Gemini CLI特有の考慮事項

### 1. **検索機能の違い**
- Geminiの検索APIを使用
- 検索結果の形式が異なる可能性
- 適切な結果の抽出と要約が必要

### 2. **出力制限**
- Geminiの出力トークン制限を考慮
- 必要に応じて段階的出力

### 3. **ファイル操作**
- Gemini CLIのファイル保存機能を活用
- 中間成果物の保存にも対応

### 4. **エラーハンドリング**
- Gemini特有のエラーに対応
- 適切なリトライ処理

## セットアップ手順

```bash
# 1. ディレクトリ構造を作成
mkdir -p article-generator/{config,prompts,assets,output}

# 2. 設定ファイルをコピー
cp .gemini-cli-config.yaml article-generator/
cp INSTRUCTIONS_GEMINI.md article-generator/INSTRUCTIONS.md

# 3. 各ファイルを配置
# (config, prompts, assetsの各ファイル)

# 4. 実行
cd article-generator
gemini --config .gemini-cli-config.yaml "爪ケアについての記事を作成して"
```

## 互換性のポイント

1. **基本構造は同じ**
   - プロンプトファイルは共通
   - ワークフローも同一
   - CSSも同じものを使用

2. **違いは設定ファイルのみ**
   - Claude Code: `.claude-code-config.yaml`
   - Gemini CLI: `.gemini-cli-config.yaml`
   - 指示書も若干の調整

3. **出力は同じ品質**
   - どちらも同じ品質基準
   - 同じチェックリスト
   - 同じ最終成果物

これにより、Claude CodeでもGemini CLIでも、同じシステムで高品質なSEO記事を生成できます！