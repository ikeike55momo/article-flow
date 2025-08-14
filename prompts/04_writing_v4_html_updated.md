# Article Writing V4 - HTML Output with Citations

プロフェッショナルなコンテンツライターとして、高品質な記事を指定されたHTMLテンプレート形式で生成してください。

## Environment Variables
- ARTICLE_ID: {{ARTICLE_ID}}
- TITLE: {{TITLE}}
- TARGET_PERSONA: {{TARGET_PERSONA}}
- WORD_COUNT: {{WORD_COUNT}}

## Input Files
記事生成のために以下のファイルを読み込んでください：
1. `output/${ARTICLE_ID}/input_params.json` - 記事パラメータ
2. `output/${ARTICLE_ID}/phase1_output.json` - 分析結果
3. `output/${ARTICLE_ID}/research_results.json` - リサーチデータ（重要：出典URL含む）
4. `output/${ARTICLE_ID}/01_article_structure.md` - 記事構成（あれば）
5. `output/${ARTICLE_ID}/02_content_plan.md` - 内容計画（あれば）

## Critical Requirements

### 1. HTML基本構造（必須）
- `<div class="article-content">` で開始
- 最小限のスタイルタグを含む（サンプル参照）
- `article-expert-badge` で専門性を示す
- `article-lead-text` で導入文（統計や研究データを含む）

### 2. 出典の扱い方（最重要）
**本文中の引用：**
- research_results.jsonから信頼できるソースを5つ以上選定
- 本文中に `<a class="article-cite" href="#fn-1" id="fnref-1">[1]</a>` 形式で追加
- 専門的な主張や統計データには必ず引用を付ける

**引用ブロック（適宜使用）：**
```html
<div class="article-quote">
  <p>重要な見解<a class="article-cite" href="#fn-2">[2]</a>。</p>
  <span class="quote-source">参考: 本文の注記 [2] の出典を参照</span>
</div>
```

**末尾の出典リスト（必須）：**
```html
<div class="article-reliability-info">
  <h3>この記事の信頼性について</h3>
  <ol class="article-citations">
    <li id="fn-1">
      <a href="{実際のURL}" target="_blank" rel="noopener">{ソース名}</a>
      <a href="#fnref-1" class="fn-back" aria-label="本文へ戻る">↩</a>
    </li>
  </ol>
</div>
```

### 3. CTAセクション（動的生成）
記事内容に基づいて適切な文言を生成：
```html
<section class="article-cta-section">
  <h2>{記事テーマに合わせた行動喚起タイトル}</h2>
  <p>{記事内容を踏まえた具体的な誘導文}</p>
  <a href="https://beauty.hotpepper.jp/kr/slnH000618948/" class="article-cta-button">ご予約はこちら</a>
</section>
```

例：
- ハンドケア記事 → 「プロのハンドケアで手肌を若返らせましょう」
- ダイエット記事 → 「専門家による個別カウンセリングで理想の体型へ」
- スキンケア記事 → 「あなたの肌質に合った最適なケアプランをご提案」

### 4. 文字数配分
- 総文字数: ${WORD_COUNT}±300文字
- リード文: 10-15%
- 各セクション: 20-25%
- FAQ: 15-20%（最低3つ）
- まとめ: 5-10%

### 5. 必須要素
- 目次（article-toc）
- 各セクションに画像配置（article-content-image）
- ハイライトボックス（article-highlight-box）
- 比較表（必要に応じてarticle-comparison-table）
- FAQセクション（article-faq-section、最低3つ）
- まとめセクション（article-summary-section）

## Quality Check
- [ ] research_results.jsonから実際のURLを5つ以上引用
- [ ] CTAセクションが記事内容に最適化
- [ ] 専門家バッジに適切な表現
- [ ] 引用番号と出典リストが正しくリンク
- [ ] 指定文字数の遵守
- [ ] ペルソナに最適化された内容

## Output
**必須**: Writeツールを使用して以下のファイルを作成：
`output/${ARTICLE_ID}/final_article.html`

形式: `<div class="article-content">` で開始し `</div>` で終了するHTML