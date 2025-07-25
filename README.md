# SEO記事自動生成システム（ファクトチェック強化版）

## 概要
このシステムは、Claude CodeまたはGemini CLIに「○○についての記事を作成して」と指示するだけで、ファクトチェック済みの高品質なSEO記事を自動生成します。

## 特徴
- 🔍 **徹底的なファクトチェック**: すべての数値・統計・主張を検証
- 📊 **信頼できる情報源**: 公的機関・学術機関の情報を優先
- ✅ **品質保証**: 品質スコア85点以上、ファクトチェックスコア90点以上
- 🎯 **SEO/LLMO最適化**: 検索エンジンとAIに最適化
- 📱 **WordPress対応**: そのまま貼り付け可能なHTML出力

## 使用方法

### Claude Code
```bash
claude-code "爪ケアについての記事を作成して"
```

### Gemini CLI
```bash
gemini "爪ケアについての記事を作成して"
```

### 詳細指定
```bash
claude-code "爪ケアについての記事を作成して store_url=https://example.com/ target=セルフケア志向の女性"
```

### 出力確認
生成された記事は以下に保存されます：
```bash
# 例：2025年1月23日に「爪ケア」の記事を生成した場合
output/2025-01-23-nail-care-guide/
├── final.html          # WordPressに貼り付ける最終HTML
├── 01_research_data.md # リサーチ結果
├── 03_draft.md        # 初稿
└── その他の中間ファイル
```

## システム構成

```
/Users/nu/article/
├── .claude-code-config.yaml      # Claude Code設定
├── .gemini-cli-config.yaml       # Gemini CLI設定
├── INSTRUCTIONS.md               # AI実行指示書
├── README.md                     # このファイル
├── config/                       # 設定ファイル
│   ├── workflow.yaml            # ワークフロー定義
│   ├── requirements.yaml        # 要件定義
│   ├── factcheck_rules.yaml     # ファクトチェックルール
│   └── templates.yaml           # テンプレート
├── prompts/                      # フェーズ別プロンプト
│   ├── 00_parse_request.md      # リクエスト解析
│   ├── 01_research.md           # リサーチ（15-25回検索）
│   ├── 02_structure.md          # 構成計画
│   ├── 03_writing.md            # 執筆
│   ├── 03_5_factcheck.md        # ファクトチェック
│   ├── 04_optimization.md       # SEO最適化
│   └── 05_finalization.md       # 最終調整
├── assets/                       
│   └── wordpress.css            # WordPress用CSS
└── output/                      # 出力ディレクトリ
    └── YYYY-MM-DD-{title}/      # 日付とタイトルのディレクトリ
        ├── 00_parsed_request.json
        ├── 01_research_data.md
        ├── 02_article_structure.md
        ├── 03_draft.md
        ├── 03_5_factchecked_draft.md
        ├── 03_5_factcheck_report.json
        ├── 04_optimized_draft.html
        ├── 04_5_image_metadata.json
        ├── 05_quality_report.json
        ├── final.html          # 最終成果物
        └── images/             # 生成画像
```

## ワークフロー

1. **リクエスト解析**: ユーザー入力から記事パラメータを抽出
2. **リサーチ**: 15-25回のweb検索で信頼できる情報収集
3. **構成計画**: エビデンスベースの記事構成
4. **執筆**: 完全オリジナルの文章作成
5. **ファクトチェック**: すべての事実を検証・修正
6. **SEO最適化**: HTML変換とSEO/LLMO対応
7. **最終調整**: 品質チェックと最終確認

## ファクトチェック機能

### 検証対象
- 数値・統計データ
- 医学的・科学的主張
- 効果・効能の記述
- 比較・評価表現

### 信頼性評価
- **very_high**: 政府機関（.go.jp, .gov）
- **high**: 学術機関（.ac.jp, .edu）、医学会
- **medium_high**: 業界団体、大手メディア
- **medium**: 一般的なWebサイト
- **low**: 出典不明、個人ブログ

### 禁止表現
- 絶対的表現：「必ず」「100%」「絶対に」
- 曖昧表現：「〜らしい」「〜かもしれない」
- 誇大表現：「最高の」「日本一の」「唯一の」

## 出力品質基準

### 必須要件
- 文字数: 3200±300字
- 品質スコア: 85点以上
- ファクトチェックスコア: 90点以上
- オリジナリティ: 100%

### SEO要件
- メインキーワード密度: 2.5-3.5%
- H2見出し: 6個
- FAQ: 7問
- メタディスクリプション: 140-160字

## カスタマイズ

### 店舗情報の設定
`store_url`パラメータで店舗URLを指定すると、適切な一人称や専門性表現が自動調整されます。

### ターゲット読者の指定
`target`パラメータで想定読者を指定できます。

### 文字数の調整
`word_count`パラメータで目標文字数を変更可能です。

## トラブルシューティング

### ファクトチェックで低スコアの場合
- より信頼できる情報源を追加検索
- 曖昧な表現を具体的に修正
- 古い情報を最新のものに更新

### 品質スコアが低い場合
- 各セクションの文字数バランスを調整
- キーワード密度を最適化
- 論理的な流れを改善

### WordPressでCSSが適用されない場合
1. **即座の対応**
   - `wordpress-fixed.css`を使用（!important付き）
   - 記事のdivに`id="nail-care-article"`を追加

2. **詳細な対処**
   - Chrome DevToolsで競合するCSSを特定
   - テーマのセレクタより高い詳細度に調整
   - `config/wordpress-compatibility.yaml`の設定を確認

3. **代替案**
   - ステップリストで`::before`が効かない場合は`<span class="step-number">`を使用
   - カスタムCSSをWordPressの追加CSSに直接記述
   - 子テーマでの管理を検討

## 注意事項

1. **医療・健康情報**: 薬機法に配慮し、断定的表現は避けています
2. **個人差の明記**: 効果には個人差があることを適切に表現
3. **最新情報の使用**: 3年以内の情報を優先的に使用
4. **法的コンプライアンス**: 景表法、薬機法に準拠

## ライセンス

このシステムは店舗の公式ブログ用に開発されています。
生成された記事の著作権は使用者に帰属します。

## 更新履歴

- v2.2 (2025): WordPress CSS適用問題を完全解決
  - CSSを完全インライン化
  - 単一HTMLブロック出力を徹底
  - 外部ファイル参照を廃止
- v2.1 (2024): ファクトチェック機能追加
- v2.0 (2024): 初回リリース