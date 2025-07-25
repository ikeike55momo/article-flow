# SEO記事自動生成システム - Claude Code/Gemini CLI用

## 概要
このシステムは、Claude CodeまたはGemini CLIに「○○についての記事を作成して」と指示するだけで、自動的に高品質なSEO記事を生成します。

## 使用方法

### 基本的な使い方
```bash
# Claude Code
claude-code "爪ケアについての記事を作成して"

# Gemini CLI
gemini "爪ケアについての記事を作成して"
```

### 詳細指定での使い方
```bash
claude-code "爪ケアについての記事を作成して store_url=https://nailsalon-plus1.com/ target=セルフケア志向の女性"
```

## ディレクトリ構成

```
article-generator/
├── .claude-code-config.yaml           # Claude Code用設定
├── .gemini-cli-config.yaml           # Gemini CLI用設定
├── INSTRUCTIONS.md                    # AIへの指示書（最重要）
├── config/
│   ├── workflow.yaml                  # ワークフロー定義
│   ├── requirements.yaml              # 要件定義
│   └── templates.yaml                 # テンプレート設定
├── prompts/
│   ├── 00_parse_request.md           # リクエスト解析
│   ├── 01_research.md                # リサーチフェーズ
│   ├── 02_structure.md               # 構成計画フェーズ
│   ├── 03_writing.md                 # 執筆フェーズ
│   ├── 04_optimization.md            # 最適化フェーズ
│   └── 05_finalization.md            # 最終調整フェーズ
├── assets/
│   └── wordpress.css                  # WordPress用CSS（変更不可）
└── output/
    └── [生成日時_記事タイトル]/
        ├── final.html                 # 最終成果物
        └── process_log.json           # 処理ログ
```

## INSTRUCTIONS.md（AIへの指示書）

```markdown
# SEO記事生成システム - 実行指示書

あなたはSEO記事生成の専門家です。ユーザーから「○○についての記事を作成して」という指示を受けたら、以下のワークフローに従って高品質な記事を生成してください。

## 実行フロー

### ステップ0: リクエスト解析
`prompts/00_parse_request.md`の指示に従い、ユーザーのリクエストから必要な情報を抽出・推測してください。

### ステップ1: リサーチ（web_search使用）
`prompts/01_research.md`の指示に従い、徹底的なリサーチを行ってください。
- 最低10回のweb_search実行
- 信頼できる情報源の確保
- 競合分析の実施

### ステップ2: 構成計画
`prompts/02_structure.md`の指示に従い、記事の詳細な構成を計画してください。

### ステップ3: 執筆
`prompts/03_writing.md`の指示に従い、オリジナルの文章を執筆してください。

### ステップ4: 最適化
`prompts/04_optimization.md`の指示に従い、SEO/LLMO最適化を行ってください。
**重要**: `assets/wordpress.css`のCSSは一切変更せずそのまま使用すること。

### ステップ5: 最終調整
`prompts/05_finalization.md`の指示に従い、品質保証チェックを行ってください。

## 出力形式

最終的に以下の形式で出力してください：

1. **処理サマリー**（最初に表示）
   - 記事タイトル
   - 総文字数
   - 品質スコア
   - 使用したキーワード

2. **最終成果物**（artifactとして出力）
   - WordPress貼り付け用の完全なHTML
   - メタ情報、本文、構造化データすべて含む

## 重要な制約事項

1. **CSSは絶対に変更しない** - assets/wordpress.cssをそのまま使用
2. **オリジナル文章必須** - リサーチ内容の転載は厳禁
3. **文字数厳守** - 3200±300文字
4. **各フェーズを順番に実行** - スキップ禁止

## エラー時の対応

各フェーズでエラーが発生した場合：
1. エラー内容を明確に報告
2. 可能な限り自動修正を試みる
3. 修正不可能な場合は、具体的な対処法を提示
```

## config/workflow.yaml

```yaml
workflow:
  name: "SEO記事自動生成ワークフロー"
  version: "2.0"
  
  # ユーザー入力の解析ルール
  input_parsing:
    patterns:
      - pattern: "(.+)についての記事を作成"
        extract: 
          main_kw: "$1"
      - pattern: "(.+)に関する記事"
        extract:
          main_kw: "$1"
    
    # パラメータ抽出
    parameters:
      - name: "store_url"
        pattern: "store_url=([^ ]+)"
        default: "https://example-store.com/"
      - name: "target"
        pattern: "target=([^ ]+)"
        default: "一般読者"
      - name: "word_count"
        pattern: "文字数=([0-9]+)"
        default: 3200

  # フェーズ定義
  phases:
    - id: "parse"
      name: "リクエスト解析"
      prompt: "prompts/00_parse_request.md"
      output: "parsed_request"
      
    - id: "research"
      name: "情報収集・競合分析"
      prompt: "prompts/01_research.md"
      requires: ["web_search"]
      min_searches: 10
      max_searches: 20
      
    - id: "structure"
      name: "記事構成計画"
      prompt: "prompts/02_structure.md"
      
    - id: "writing"
      name: "本文執筆"
      prompt: "prompts/03_writing.md"
      
    - id: "optimization"
      name: "SEO/LLMO最適化"
      prompt: "prompts/04_optimization.md"
      assets: ["wordpress.css"]
      
    - id: "finalization"
      name: "最終調整・品質保証"
      prompt: "prompts/05_finalization.md"
      quality_threshold: 85

  # 出力設定
  output:
    format: "html"
    encoding: "utf-8"
    artifact: true
    summary: true
```

## config/requirements.yaml

```yaml
# SEO要件
seo:
  keyword_density:
    main_keyword:
      min: 2.5
      max: 3.5
    related_keywords:
      min: 1.0
      max: 2.0
  
  meta_tags:
    title:
      max_length: 60
      include_main_kw: true
    description:
      min_length: 140
      max_length: 160
      include_main_kw: true
  
  headings:
    h1_count: 1
    h2_count: 6
    h3_per_h2: 2-3

# コンテンツ要件
content:
  total_word_count:
    target: 3200
    tolerance: 300
  
  sections:
    lead_text: 200
    h2_sections:
      - name: "基本知識と重要性"
        words: 650
      - name: "具体的な実践方法"
        words: 650
      - name: "関連性と相乗効果"
        words: 650
      - name: "よくある失敗例"
        words: 550
      - name: "選び方・判断基準"
        words: 550
      - name: "継続のコツ"
        words: 550
    faq:
      questions: 7
      answer_length: 200-300
    summary: 200
    cta: 200

# 品質基準
quality:
  originality: 100  # 完全オリジナル
  readability: 85
  value_score: 90
  consistency: 95

# 店舗タイプ別設定
store_types:
  beauty:
    patterns: ["サロン", "エステ", "美容"]
    voice: "私たちのサロンでは"
  medical:
    patterns: ["病院", "クリニック", "医院"]
    voice: "当院では"
  general:
    patterns: ["店", "ショップ"]
    voice: "当店では"
  default:
    voice: "私たちは"
```

## prompts/00_parse_request.md

```markdown
# リクエスト解析フェーズ

ユーザーからのリクエストを解析し、記事生成に必要なパラメータを抽出・推測してください。

## 入力
ユーザーのリクエスト: {{user_request}}

## タスク

### 1. 基本情報の抽出
リクエストから以下を抽出：
- **メインキーワード**: 記事の主題となるキーワード
- **記事タイトル案**: SEOを意識した魅力的なタイトル（28-32文字）
- **想定される検索意図**: 情報収集型/実行型/購買型など

### 2. 不足情報の推測
明示されていない以下の情報を適切に推測：
- **関連キーワード**: メインキーワードに関連する3-5個
- **ターゲット読者**: 想定される読者層
- **E-E-A-T要素**: 提供できる専門性・経験・権威性・信頼性

### 3. 店舗情報の設定
- store_urlが指定されていれば使用
- なければデフォルト値を使用
- URLから店舗タイプを推測

## 出力形式

```json
{
  "title": "推測または生成した記事タイトル",
  "main_kw": "メインキーワード",
  "related_kw": ["関連1", "関連2", "関連3", "関連4", "関連5"],
  "cut_target": "ターゲット読者の詳細",
  "eeat_elements": ["専門性の要素", "経験の要素"],
  "store_url": "https://...",
  "store_type": "beauty|medical|general|default",
  "search_intent": "informational|transactional|navigational",
  "estimated_difficulty": "easy|medium|hard"
}
```

## 推測のガイドライン

### タイトル生成のルール
- 数字を含める（例：5つの方法、2024年版）
- ベネフィットを明確に（例：簡単、プロ直伝、初心者向け）
- 感情に訴える要素（例：失敗しない、今すぐできる）

### 関連キーワードの推測
- 同義語・類義語
- 上位概念・下位概念
- 関連する行動や状態
- 解決したい課題

### ターゲット読者の設定
- 年齢層・性別（必要に応じて）
- 知識レベル（初心者/中級者/上級者）
- 抱える課題や悩み
- 求める結果
```

## prompts/01_research.md

```markdown
# フェーズ1: 情報収集・競合分析

## 入力情報
前フェーズで解析した情報を使用：
- title: {{title}}
- main_kw: {{main_kw}}
- related_kw: {{related_kw}}
- その他の解析情報

## 実行要件
**必須**: 最低10回、最大20回のweb_search実行

## リサーチタスク

### 1. キーワード詳細分析（2-3回のsearch）

1. **「{{main_kw}}とは」で検索**
   - 基本的な定義と概念
   - 一般的な認識と誤解
   - 最新の解釈や定義

2. **「{{main_kw}} 方法」「{{main_kw}} やり方」で検索**
   - 実践的なアプローチ
   - 手順やステップ
   - 必要なツールや準備

3. **「{{main_kw}} 効果」「{{main_kw}} メリット」で検索**
   - 期待できる結果
   - 科学的根拠
   - 実例や体験談

### 2. 競合記事分析（3-4回のsearch）

各検索で上位記事を分析：
- 「{{main_kw}}」単体で検索
- 「{{main_kw}} {{related_kw[0]}}」で検索
- 「{{main_kw}} 2024」または「{{main_kw}} 最新」で検索

分析ポイント：
- タイトルの付け方
- 見出し構成（H2/H3）
- 提供している価値
- 不足している情報

### 3. 統計・データ収集（2-3回のsearch）

信頼できるデータを探す：
- 「{{main_kw}} 統計」「{{main_kw}} データ」
- 「{{main_kw}} 調査結果」「{{main_kw}} 研究」
- 政府機関や業界団体のサイトを優先

### 4. 最新トレンド調査（2-3回のsearch）

- 「{{main_kw}} 2024」「{{main_kw}} 最新」
- 「{{main_kw}} トレンド」「{{main_kw}} 今後」
- SNSやニュースサイトの情報も参考に

### 5. 関連情報の深堀り（2-3回のsearch）

関連キーワードごとに：
- 「{{related_kw[i]}} {{main_kw}}」で検索
- 相互の関係性を理解
- 組み合わせの効果

## 情報の整理と出力

収集した情報を以下の形式で整理：

1. **コア情報**
   - 定義と基本概念
   - 重要性と必要性
   - 一般的な誤解と正しい理解

2. **実践情報**
   - 具体的な方法・手順
   - 必要なもの・準備
   - 注意点とコツ

3. **差別化ポイント**
   - 競合が書いていない情報
   - 独自の視点や切り口
   - 付加価値となる要素

4. **信頼性を高める要素**
   - 統計データ（出典付き）
   - 専門家の見解
   - 公的機関の情報

5. **最新性を示す要素**
   - 2024年の最新情報
   - 最近の変化や傾向
   - 今後の展望

## 注意事項
- すべての情報源のURLを記録
- 情報の新しさを確認（できれば1年以内）
- 矛盾する情報があれば両論併記
- 憶測や不確かな情報は避ける
```

## prompts/02_structure.md

```markdown
# フェーズ2: 記事構成計画

## 入力情報
- リサーチ結果全体
- 記事パラメータ（title, main_kw等）

## 構成設計タスク

### 1. 記事コンセプトの確立

リサーチ結果を踏まえて：
- **独自の価値提案**: 他記事にない独自性は何か
- **読者への約束**: この記事を読んで得られるもの
- **トーン&マナー**: 専門的かつ親しみやすい文体

### 2. 詳細な見出し構成

#### リード文（200字）
- 読者の共感を得る問いかけや状況設定
- 記事を読む価値の明確な提示
- 続きを読みたくなる仕掛け

#### H2セクション構成（6つ）

1. **{{main_kw}}の基本知識と重要性**（650字）
   - H3: 基本的な定義と仕組み
   - H3: なぜ重要なのか（数値データ含む）
   - H3: よくある誤解と正しい理解

2. **{{main_kw}}の具体的な実践方法**（650字）
   - H3: 準備するもの・事前知識
   - H3: ステップバイステップの手順
   - H3: 成功のポイントとコツ

3. **{{related_kw[0]}}との関連性と相乗効果**（650字）
   - H3: 関連性の科学的根拠
   - H3: 組み合わせることのメリット
   - H3: 実践時の注意点

4. **よくある失敗例と改善策**（550字）
   - H3: 失敗パターンTop3
   - H3: 失敗を防ぐ予防策
   - H3: 失敗した場合の対処法

5. **プロが教える選び方・判断基準**（550字）
   - H3: 選択時の重要ポイント
   - H3: 状況別のおすすめ
   - H3: コストパフォーマンスの考え方

6. **継続のコツと成果測定**（550字）
   - H3: モチベーション維持の方法
   - H3: 成果の見える化
   - H3: 長期的な習慣化へのロードマップ

#### FAQ（7問）
競合分析とリサーチから、読者が本当に知りたい質問を選定

#### まとめ（200字）
- 重要ポイントの再確認
- 実践への後押し
- 前向きなメッセージ

#### CTA（200字）
- 店舗の専門性をアピール
- 具体的な行動提案
- 連絡への心理的ハードルを下げる

### 3. キーワード配置計画

各セクションでの配置数を明確に：
- メインキーワード: 各H2に3-4回
- 関連キーワード: 各H2に1-2回
- 自然な文脈での使用

### 4. 視覚的要素の計画

各H2セクションに：
- 画像挿入位置の指定
- 表やリストの使用箇所
- 強調ボックスの配置

## 出力
詳細な構成計画書として、各セクションの：
- 見出し文言
- 含むべき内容ポイント
- 使用するデータや事例
- キーワード配置数
- 文字数配分
```

## prompts/03_writing.md

```markdown
# フェーズ3: 本文執筆

## 重要な制約事項

### 絶対厳守事項
1. **完全オリジナル文章**
   - リサーチ内容の転載・コピーは厳禁
   - 同じ意味でも独自の表現を使用
   - 自然な日本語で執筆

2. **店舗視点での執筆**
   - 店舗タイプに応じた一人称使用
   - 専門家としての立場を明確に
   - 読者との適切な距離感

3. **文字数の厳密な管理**
   - 各セクション指定文字数の±10%
   - 全体3200±300字を確保

## 執筆ガイドライン

### 文体・トーン
- 専門的かつ親しみやすい
- 断定的すぎない表現
- 読者を尊重する姿勢

### 文章構成のルール
- 1文は40-60字程度
- 1段落は3-4文程度
- 適切な接続詞の使用
- PREP法（Point-Reason-Example-Point）の活用

### 専門性の表現方法
- 具体的な数値やデータ
- 実例やケーススタディ
- 専門用語には説明を付加
- 経験に基づく独自の見解

### 読者エンゲージメント
- 問いかけの使用
- 共感を示す表現
- 具体的なイメージを描写
- 行動を促す表現

## セクション別執筆ポイント

### リード文
- 最初の一文で心をつかむ
- 読者の現状に共感
- 解決への期待を醸成

### 各H2セクション
1. **導入段落**: セクションの概要と重要性
2. **本論**: H3に沿った詳細解説
3. **まとめ段落**: 要点整理と次セクションへの橋渡し

### FAQ
- 実際によくある質問を想定
- 専門的かつ実践的な回答
- 追加の価値情報を含める

### CTA
- 押しつけがましくない誘導
- 具体的なベネフィット提示
- 行動への心理的障壁を下げる

## 品質チェック項目
- [ ] オリジナリティ100%
- [ ] 指定文字数の遵守
- [ ] キーワードの自然な配置
- [ ] 論理的な流れ
- [ ] 読者価値の提供

## 出力形式
マークダウン形式で、見出し構造を明確にした本文
```

## prompts/04_optimization.md

```markdown
# フェーズ4: SEO/LLMO最適化

## 最適化タスク

### 1. HTML変換

#### 基本構造
```html
<div class="wp-blog-post">
<style>
/* assets/wordpress.cssの内容をそのまま挿入 */
/* 絶対に変更しないこと */
</style>

<!-- 記事本文 -->

<!-- 構造化データ -->
</div>
```

#### メタ情報（コメントアウト形式）
```html
<!--
タイトル: {{title}}
メタディスクリプション: {{140-160字、main_kw含む、具体的な数値}}
OGP情報:
- og:title: {{title}}
- og:description: {{SNS用100-120字、魅力的な訴求}}
- og:url: {{store_url}}
- og:type: article
- og:image: placeholder.webp
- article:author: {{店舗名}}
- article:published_time: {{ISO 8601形式}}
- article:section: {{カテゴリ}}
canonical: {{store_url}}
robots: index,follow
viewport: width=device-width,initial-scale=1
-->
```

### 2. SEO最適化

#### キーワード密度の調整
- メインキーワード: 2.5-3.5%に調整
- 関連キーワード: 各1-2%に調整
- 不自然な箇所を自然な表現に

#### 内部SEO要素
- すべての画像にalt属性
- 適切な見出し階層
- 内部リンクの最適化

### 3. LLMO（LLM最適化）

#### AI引用性の向上
- 統計データを明確に記述
- 手順を番号付きリストで
- 定義を明確に構造化
- 比較を表形式で整理

#### 情報の構造化
- 因果関係の明確化
- 前提条件の明示
- 結論の強調

### 4. 画像ブロックの挿入

各H2セクションに適切な画像指示：
```html
<!-- 画像挿入指示: {{H2タイトル}}の{{具体的な内容説明}} -->
<figure class="content-image">
  <img src="placeholder.webp"
       alt="{{詳細な説明80-120字、キーワード含む}}"
       loading="lazy" decoding="async"
       width="800" height="600">
  <figcaption>{{専門的な補足説明}}</figcaption>
</figure>
```

### 5. 構造化データ

#### Article
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{title}}",
  "author": {
    "@type": "Organization",
    "name": "{{店舗名}}",
    "url": "{{store_url}}"
  },
  "datePublished": "{{ISO 8601}}",
  "dateModified": "{{ISO 8601}}",
  "image": "placeholder.webp",
  "articleBody": "{{本文}}",
  "keywords": "{{keywords}}",
  "wordCount": {{文字数}},
  "articleSection": "{{カテゴリ}}",
  "inLanguage": "ja"
}
```

#### FAQPage
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{{質問}}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{回答}}"
      }
    }
  ]
}
```

## 重要な注意事項
- CSSは一切変更しない
- クラス名は正確に使用
- HTML構文の妥当性を確保
```

## prompts/05_finalization.md

```markdown
# フェーズ5: 最終調整・品質保証

## 品質チェックタスク

### 1. コンテンツ品質（30点）
- [ ] 見出しと内容の一致（5点）
- [ ] 論理的な流れ（5点）
- [ ] オリジナリティ（10点）
- [ ] 読みやすさ（5点）
- [ ] 価値提供度（5点）

### 2. SEO最適化（30点）
- [ ] キーワード密度適正（10点）
- [ ] メタ情報完備（5点）
- [ ] 構造化データ正確（5点）
- [ ] 内部SEO要素（5点）
- [ ] LLMO対応（5点）

### 3. 技術的要件（20点）
- [ ] HTML妥当性（5点）
- [ ] CSS適用確認（5点）
- [ ] レスポンシブ対応（5点）
- [ ] 表示速度考慮（5点）

### 4. 文字数要件（20点）
- [ ] 全体文字数（10点）
- [ ] 各セクション文字数（10点）

### 合計スコア: {{total}}/100点

## 修正が必要な項目

スコアが85点未満の場合、以下を修正：

1. **70点未満の項目**
   - 該当箇所を特定
   - 具体的な修正案
   - 修正後の再チェック

2. **文字数不足/超過**
   - 該当セクションを特定
   - 追加/削除する内容
   - 全体バランスの調整

3. **SEO要件未達**
   - キーワード密度の調整
   - メタ情報の改善
   - 構造化データの修正

## 最終確認事項

### 参考文献
- [ ] すべてのURLが有効
- [ ] 信頼できる情報源のみ
- [ ] 適切なrel属性

### ユーザビリティ
- [ ] 目次のリンクが正確
- [ ] CTAが明確
- [ ] モバイル表示確認

### WordPress互換性
- [ ] エディターでの表示確認
- [ ] CSSの適用確認
- [ ] プレビューでの最終確認

## 最終出力

品質スコア85点以上を達成した、完全なWordPress用HTML。

### 出力前の最終チェック
1. メタ情報がコメントアウトされているか
2. CSSが正確に含まれているか
3. 構造化データが有効なJSON-LDか
4. 全体が.wp-blog-postで囲まれているか

## 完了報告

```
✅ 記事生成完了
- タイトル: {{title}}
- 総文字数: {{word_count}}
- 品質スコア: {{score}}/100
- メインキーワード: {{main_kw}}
- 最適化完了項目: SEO, LLMO, WordPress互換性
```
```

## .claude-code-config.yaml

```yaml
# Claude Code用設定ファイル
project_name: "SEO Article Generator"
version: "2.0"

# 実行時の自動設定
on_request:
  match: "についての記事を作成"
  execute: "INSTRUCTIONS.md"
  
# 使用するツール
tools:
  - web_search
  - artifacts
  
# ファイル読み込み設定
include_files:
  - "config/*.yaml"
  - "prompts/*.md"
  - "assets/wordpress.css"

# 出力設定
output:
  create_artifact: true
  artifact_type: "text/html"
  artifact_title: "WordPress用SEO記事"
```

## assets/wordpress.css

```css
/* WordPress専用CSS - 絶対に変更しないこと */
.wp-blog-post {
  font-family: "Noto Sans JP", "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
  line-height: 1.8;
  color: #333;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  font-size: 16px;
}
.wp-blog-post h1 {
  font-size: 2.2rem;
  font-weight: 700;
  margin: 2rem 0 1.5rem;
  border-left: 6px solid #0068d9;
  padding-left: 1rem;
  line-height: 1.3;
  color: #1a1a1a;
}
.wp-blog-post h2 {
  font-size: 1.6rem;
  font-weight: 700;
  margin: 3rem 0 1.5rem;
  position: relative;
  color: #0068d9;
  padding-bottom: 0.5rem;
}
.wp-blog-post h2::after {
  content: "";
  display: block;
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #0068d9, #4dabf7);
  margin-top: 0.5rem;
  border-radius: 2px;
}
.wp-blog-post h3 {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 2rem 0 1rem;
  color: #333;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 0.5rem;
}
.wp-blog-post h4 {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 1.5rem 0 0.8rem;
  color: #495057;
}
.wp-blog-post p {
  margin: 1.2rem 0;
  line-height: 1.8;
}
.wp-blog-post a {
  color: #0068d9;
  text-decoration: none;
  font-weight: 500;
}
.wp-blog-post a:hover {
  text-decoration: underline;
  color: #0056b3;
}
.wp-blog-post .lead-text {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #495057;
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin: 2rem 0;
  border-left: 4px solid #0068d9;
}
.wp-blog-post .toc {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 2rem;
  margin: 2.5rem 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.wp-blog-post .toc h2 {
  margin-top: 0;
  font-size: 1.2rem;
  color: #495057;
  text-align: center;
}
.wp-blog-post .toc ul {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0 0;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}
.wp-blog-post .toc a {
  padding: 0.8rem 1.2rem;
  border: 2px solid #0068d9;
  border-radius: 25px;
  font-size: 0.9rem;
  display: block;
  text-align: center;
  transition: all 0.3s ease;
  background: #fff;
}
.wp-blog-post .toc a:hover {
  background: #0068d9;
  color: #fff;
  text-decoration: none;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,104,217,0.3);
}
.wp-blog-post .content-image {
  margin: 2.5rem 0;
  text-align: center;
}
.wp-blog-post .content-image img {
  max-width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
.wp-blog-post figcaption {
  font-size: 0.9rem;
  color: #6c757d;
  margin-top: 1rem;
  font-style: italic;
  padding: 0 1rem;
}
.wp-blog-post .highlight-box {
  background: linear-gradient(135deg, #fff3cd, #ffeaa7);
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 2rem 0;
  position: relative;
}
.wp-blog-post .highlight-box::before {
  content: "💡";
  position: absolute;
  top: 1rem;
  left: 1rem;
  font-size: 1.2rem;
}
.wp-blog-post .highlight-box h4 {
  margin-top: 0;
  padding-left: 2rem;
  color: #856404;
}
.wp-blog-post .steps-list {
  counter-reset: step-counter;
  list-style: none;
  padding: 0;
}
.wp-blog-post .steps-list li {
  counter-increment: step-counter;
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #0068d9;
  position: relative;
}
.wp-blog-post .steps-list li::before {
  content: "Step " counter(step-counter);
  position: absolute;
  top: -0.5rem;
  left: 1rem;
  background: #0068d9;
  color: #fff;
  padding: 0.3rem 0.8rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}
.wp-blog-post .comparison-table {
  width: 100%;
  border-collapse: collapse;
  margin: 2rem 0;
  background: #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border-radius: 12px;
  overflow: hidden;
}
.wp-blog-post .comparison-table th,
.wp-blog-post .comparison-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}
.wp-blog-post .comparison-table th {
  background: linear-gradient(135deg, #0068d9, #4dabf7);
  color: #fff;
  font-weight: 600;
}
.wp-blog-post .comparison-table tr:hover {
  background: #f8f9fa;
}
.wp-blog-post .faq-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 2.5rem;
  margin: 3rem 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.wp-blog-post .faq-section h2 {
  margin-top: 0;
  text-align: center;
}
.wp-blog-post .faq-item {
  margin-bottom: 2rem;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 1.5rem;
}
.wp-blog-post .faq-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}
.wp-blog-post .faq-question {
  font-weight: 600;
  color: #0068d9;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}
.wp-blog-post .faq-answer {
  color: #495057;
  line-height: 1.7;
}
.wp-blog-post .summary-section {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  border-radius: 12px;
  padding: 2rem;
  margin: 3rem 0;
  border: 1px solid #90caf9;
}
.wp-blog-post .summary-section h2 {
  margin-top: 0;
  color: #1565c0;
  text-align: center;
}
.wp-blog-post .cta-section {
  background: linear-gradient(135deg, #ff6b4d, #ff8a65);
  color: #fff;
  padding: 2.5rem;
  border-radius: 15px;
  margin: 3rem 0;
  text-align: center;
  box-shadow: 0 8px 25px rgba(255,107,77,0.4);
}
.wp-blog-post .cta-section h2 {
  color: #fff;
  margin-top: 0;
}
.wp-blog-post .cta-section h2::after {
  background: #fff;
}
.wp-blog-post .cta-button {
  display: inline-block;
  background: #fff;
  color: #ff6b4d;
  padding: 1.2rem 2.5rem;
  border-radius: 30px;
  font-weight: 600;
  margin-top: 1.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  font-size: 1.1rem;
}
.wp-blog-post .cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.2);
  text-decoration: none;
}
.wp-blog-post .reference-section {
  background: #f8f9fa;
  border-left: 4px solid #0068d9;
  padding: 2rem;
  margin: 3rem 0;
  border-radius: 0 8px 8px 0;
}
.wp-blog-post .reference-section h2 {
  margin-top: 0;
  font-size: 1.2rem;
}
.wp-blog-post .reference-section ul {
  margin: 1.5rem 0 0;
  padding-left: 2rem;
}
.wp-blog-post .reference-section li {
  margin-bottom: 0.8rem;
}
.wp-blog-post .author-info {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 2rem;
  margin: 3rem 0;
  text-align: center;
  border: 1px solid #e9ecef;
}
.wp-blog-post .author-info h3 {
  margin-top: 0;
  color: #0068d9;
}
.wp-blog-post .author-info p {
  font-size: 0.9rem;
  color: #6c757d;
  margin: 0.5rem 0;
}
@media (max-width: 768px) {
  .wp-blog-post {
    padding: 0 0.8rem;
    font-size: 15px;
  }
  .wp-blog-post h1 {
    font-size: 1.8rem;
  }
  .wp-blog-post h2 {
    font-size: 1.4rem;
  }
  .wp-blog-post .toc ul {
    grid-template-columns: 1fr;
  }
  .wp-blog-post .cta-section {
    padding: 2rem;
  }
  .wp-blog-post .comparison-table {
    font-size: 0.9rem;
  }
  .wp-blog-post .comparison-table th,
  .wp-blog-post .comparison-table td {
    padding: 0.8rem;
  }
}
```

## 使用例

### 基本的な使用
```bash
# Claude Codeの場合
claude-code "爪ケアについての記事を作成して"

# 詳細指定
claude-code "爪ケアについての記事を作成して store_url=https://nailsalon-plus1.com/ target=セルフケア志向の女性"
```

### Claude Codeでの実行フロー
1. 「○○についての記事を作成して」と入力
2. Claude CodeがINSTRUCTIONS.mdを読み込み
3. 各promptsフォルダのファイルに従って順次実行
4. 最終的にartifactとしてWordPress用HTMLを出力

### 期待される動作
- リクエスト解析から最終調整まで自動実行
- 各フェーズで必要なweb_searchを実施
- CSSは変更せずそのまま使用
- 品質スコア85点以上で完成

このシステムにより、Claude CodeやGemini CLIに簡単な指示をするだけで、プロフェッショナルなSEO記事が自動生成されます。