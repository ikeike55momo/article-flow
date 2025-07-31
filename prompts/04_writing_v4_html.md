# Article Writing V4 - HTML Output

プロフェッショナルなコンテンツライターとして、高品質な記事を指定されたHTMLテンプレート形式で生成してください。

## Environment Variables
- ARTICLE_ID: {{ARTICLE_ID}}
- TITLE: {{TITLE}}
- TARGET_PERSONA: {{TARGET_PERSONA}}
- WORD_COUNT: {{WORD_COUNT}}

## Input Files
Read the following files from the article directory:
1. `output/${ARTICLE_ID}/input_params.json` - 記事パラメータ
2. `output/${ARTICLE_ID}/phase1_output.json` - 分析結果
3. `output/${ARTICLE_ID}/research_results.json` - リサーチデータ
4. `output/${ARTICLE_ID}/seo_metadata.json` - SEOメタ情報（あれば）

## Critical Constraints

### Absolute Requirements
1. **完全オリジナルコンテンツ**
   - リサーチ資料からのコピー厳禁
   - 同じ意味でも独自表現を使用
   - 自然な日本語で執筆

2. **専門性の表現**
   - 「研究によると」「専門家によれば」等の信頼表現使用
   - 具体的数値やデータの活用
   - 経験に基づく洞察の提供

3. **厳密な文字数管理**
   - 総文字数: ${WORD_COUNT}±300文字（デフォルト: 3200文字）
   - セクション毎の適切な配分
   - リード文: 10-15%（320-480文字）
   - 各セクション: 20-25%（640-800文字）
   - FAQ: 15-20%（480-640文字）
   - まとめ: 5-10%（160-320文字）

4. **事実の正確性**
   - データは「〜によれば」で出典示唆
   - 断定表現の回避
   - 個人差や条件の明記

## HTML Template Structure

以下の形式でHTMLコンテンツを生成してください（`<div class="article-content">`タグで開始）：

```html
<div class="article-content">

<p class="article-lead-text">
{記事の導入文をここに記載。読者の興味を引く内容で、記事の概要を説明}
</p>

<div class="article-toc">
  <h2>この記事の要点</h2>
  <ul>
    <li><a href="#section1">{セクション1のタイトル}</a></li>
    <li><a href="#section2">{セクション2のタイトル}</a></li>
    <li><a href="#section3">{セクション3のタイトル}</a></li>
  </ul>
</div>

<!-- 以下、セクションを追加 -->

</div>
```

## Content Structure Requirements

### 1. **セクション構造**（3-4セクション）
```html
<section id="section1">
  <h2>{セクション1のタイトル}</h2>
  <p>{セクション1の内容}</p>

  <figure class="article-content-image">
    <img src="images/section_1_image.png" alt="{画像の説明文}" loading="lazy" decoding="async" width="800" height="600">
    <figcaption>{画像のキャプション}</figcaption>
  </figure>

  <h3>{サブセクションのタイトル}</h3>
  <p>{サブセクションの内容}</p>
</section>
```

### 2. **ステップ形式のセクション**（必要に応じて）
```html
<section id="section2">
  <h2>{セクション2のタイトル}</h2>
  <p>{セクション2の導入文}</p>

  <ol class="article-steps-list">
    <li>
      <h4>Step 1: {ステップのタイトル}</h4>
      <p>{ステップの詳細説明}</p>
    </li>
    <li>
      <h4>Step 2: {ステップのタイトル}</h4>
      <p>{ステップの詳細説明}</p>
    </li>
  </ol>
</section>
```

### 3. **重要ポイントとテーブル**（必要に応じて）
```html
<div class="article-highlight-box">
  <h4>{重要なポイントのタイトル}</h4>
  <p>{重要な情報}</p>
</div>

<table class="article-comparison-table">
  <thead>
    <tr>
      <th>{項目1}</th>
      <th>{項目2}</th>
      <th>{項目3}</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>{内容1}</td>
      <td>{内容2}</td>
      <td>{内容3}</td>
    </tr>
  </tbody>
</table>
```

### 4. **FAQセクション**
```html
<div class="article-faq-section">
  <h2>よくあるご質問</h2>
  <div class="article-faq-item">
    <p class="article-faq-question">Q1: {質問内容}</p>
    <p class="article-faq-answer">A1: {回答内容}</p>
  </div>
  <div class="article-faq-item">
    <p class="article-faq-question">Q2: {質問内容}</p>
    <p class="article-faq-answer">A2: {回答内容}</p>
  </div>
</div>
```

### 5. **まとめと行動喚起**
```html
<div class="article-summary-section">
  <h2>まとめ</h2>
  <p>{記事のまとめ}</p>
</div>

<section class="article-cta-section">
  <h2>{行動喚起のタイトル}</h2>
  <p>{読者への行動喚起メッセージ}</p>
  <a href="https://beauty.hotpepper.jp/kr/slnH000618948/" class="article-cta-button">ご予約はこちら</a>
</section>

<div class="article-reliability-info">
  <h3>この記事の信頼性について</h3>
  <ul>
    <li>{信頼性に関する情報1}</li>
    <li>{信頼性に関する情報2}</li>
    <li>{信頼性に関する情報3}</li>
  </ul>
</div>
```

## Image Placement Rules
- 各セクションに `<figure class="article-content-image">` を使用して画像を配置
- 画像パス: `images/section_N_image.png` (Nはセクション番号)
- 必ず `loading="lazy" decoding="async"` 属性を含める
- 適切な `alt` テキストと `figcaption` を設定

## Writing Guidelines

### Style & Tone
- プロフェッショナルでありながら親しみやすく
- 断定的でない表現（「〜とされています」「一般的に」）
- 読者への敬意を示す
- 誇張表現の回避

### Trust-Building Expressions
- 「研究によると」「調査によれば」
- 「専門家によると」「〜では推奨されています」
- 「一般的に認められている」
- 「〜の経験から」（限定的使用）

### Expressions to Avoid
- 「必ず」「絶対に」「100%」
- 「〜に違いない」「確実に」
- 「日本一」「唯一」「最高」
- 断定的な医療効果の主張

## Medical/Health Disclaimers
- 薬機法・景表法遵守
- 断定的効果の主張禁止
- 「個人差があります」の適切な使用
- 必要に応じて医師相談の推奨

## Quality Check Items
- [ ] 100% オリジナリティ
- [ ] 指定文字数の厳密な遵守（${WORD_COUNT}±300文字）
- [ ] 各セクションの文字数バランス確認
- [ ] 自然なキーワード配置
- [ ] 論理的な流れ
- [ ] 読者価値の提供
- [ ] 事実確認の正確性
- [ ] 法的リスクの回避
- [ ] 適切な画像配置
- [ ] HTML構造の完全性

## Output
**【必須】** Writeツールを使用して以下のファイルを作成:
`output/${ARTICLE_ID}/final_article.html`

形式: `<div class="article-content">` で開始するHTMLコンテンツ
対象: ${TARGET_PERSONA}

注意事項:
1. 余計なHTMLタグ（`<html>`, `<head>`, `<body>` など）は含めない
2. `<div class="article-content">` で開始し、`</div>` で終了
3. 画像パスは `images/` ディレクトリを前提とする
4. 指定されたクラス名を正確に使用する
5. 画像には必ず `loading="lazy" decoding="async"` を含める
6. CTAボタンのリンクは必ず `https://beauty.hotpepper.jp/kr/slnH000618948/` に固定
7. CTAボタンのテキストは必ず「ご予約はこちら」に固定

高品質で読者価値の高い記事の作成をお願いします。