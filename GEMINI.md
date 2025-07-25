# Gemini CLI 設定ガイド

このファイルは、Gemini CLIがプロジェクトのコンテキストとして自動的に読み込むファイルです。

## プロジェクト概要

このプロジェクトは、SEO最適化された記事を自動生成するワークフローシステムです。
「○○について記事を作成して」と指示すると、7つのフェーズを通じて高品質な記事を生成します。

## 重要な指示

### 記事作成リクエストの処理

以下のパターンでリクエストされた場合は、必ず`INSTRUCTIONS_v2.md`のワークフローを実行してください：
- 「について記事を作成」
- 「についての記事を作成」
- 「に関する記事」
- 「のSEO記事」

### ワークフロー実行手順

1. **INSTRUCTIONS_v2.md**ファイルの内容を完全に読み込む
2. 7つのフェーズを順番に実行：
   - ステップ0: リクエスト解析
   - ステップ1: リサーチ
   - ステップ2: 構成計画
   - ステップ3: 執筆
   - ステップ3.5: ファクトチェック
   - ステップ4: 最適化
   - ステップ4.5: 画像生成（MCPサーバー使用）
   - ステップ5: 最終調整

3. **出力ディレクトリ構造**を必ず作成：
   ```
   output/YYYY-MM-DD-{title_slug}/
   ├── 00_parsed_request.json
   ├── 01_research_data.md
   ├── 02_article_structure.md
   ├── 03_draft.md
   ├── 03_5_factchecked_draft.md
   ├── 03_5_factcheck_report.json
   ├── 04_optimized_draft.html
   ├── 04_5_image_metadata.json
   ├── 04_5_with_images.html
   ├── 05_quality_report.json
   └── final.html
   ```

### 画像生成

MCPサーバー「google-ai-imagen」が利用可能な場合：
- 各H2セクションに対して画像を生成
- `generate_image`ツールを使用
- 生成した画像はHTMLに統合

### 品質基準

- ファクトチェックスコア: 90点以上
- 品質スコア: 85点以上
- これらの基準を満たさない場合は再実行

## プロジェクトファイル構造

```
/mnt/c/article-flow/
├── INSTRUCTIONS_v2.md      # メインワークフロー定義
├── config/                 # 各種設定ファイル
│   ├── workflow.yaml      # ワークフロー設定
│   ├── requirements.yaml  # 要件定義
│   ├── templates.yaml     # テンプレート
│   └── factcheck_rules.yaml # ファクトチェックルール
├── prompts/               # 各フェーズのプロンプト
│   ├── 00_parse_request.md
│   ├── 01_research.md
│   ├── 02_structure.md
│   ├── 03_writing.md
│   ├── 03_5_factcheck.md
│   ├── 04_optimization.md
│   ├── 04_5_image_generation.md
│   └── 05_finalization.md
└── assets/               # スタイルシート
    └── wordpress.css     # WordPress用CSS

## 実行例

ユーザー: 「爪ケアについて記事を作成して」

期待される動作:
1. INSTRUCTIONS_v2.mdを読み込む
2. 7フェーズのワークフローを実行
3. output/2025-07-23-nail-care/に全ファイルを保存
4. 最終的なfinal.htmlを生成

## 注意事項

- 単純な記事作成ではなく、必ずワークフローを実行すること
- 各フェーズの出力を確実に保存すること
- MCPサーバーが利用可能な場合は画像生成を実行すること
- WordPress用のインラインCSSを必ず含めること

このファイルの指示に従って、高品質な記事生成ワークフローを実行してください。