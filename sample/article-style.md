# AI記事生成用ガイド

## 概要
このガイドは、AIに記事生成を依頼する際に使用するコンテキストです。指定されたクラス名を使用することで、美しく構造化された記事HTMLを生成できます。

## 使用方法
1. このREADMEと`article-template.html`をAIに渡す
2. 記事の内容を指定する
3. AIが適切なクラス名を使用してHTMLを生成

## 利用可能なクラス名一覧

### 基本構造
```html
<div class="article-content">
  <!-- 記事本文全体を囲むコンテナ -->
</div>
```

### 基本要素
- `article-expert-badge` - 専門家バッジ
- `article-lead-text` - リードテキスト（記事の導入文）

### 目次・ナビゲーション
- `article-toc` - 目次コンテナ
- `article-toc h2` - 目次のタイトル
- `article-toc ul` - 目次のリスト
- `article-toc a` - 目次のリンク

### 画像・メディア
- `article-content-image` - 画像コンテナ
- `article-content-image img` - 画像本体
- `figcaption` - 画像のキャプション

### ハイライト・強調
- `article-highlight-box` - ハイライトボックス（重要情報の強調）
- `article-highlight-box h4` - ハイライトボックスのタイトル
- `article-highlight-box p` - ハイライトボックスの内容

### 手順・ステップ
- `article-steps-list` - ステップリスト（ol要素）
- `article-steps-list li` - 各ステップ項目
- `article-steps-list h4` - ステップのタイトル
- `article-steps-list p` - ステップの説明

### 比較・テーブル
- `article-comparison-table` - 比較テーブル
- `article-comparison-table th` - テーブルヘッダー
- `article-comparison-table td` - テーブルセル

### FAQ
- `article-faq-section` - FAQセクション全体
- `article-faq-item` - 各FAQ項目
- `article-faq-question` - FAQの質問
- `article-faq-answer` - FAQの回答

### セクション
- `article-summary-section` - まとめセクション
- `article-cta-section` - CTA（行動喚起）セクション
- `article-cta-button` - CTAボタン
- `article-reference-section` - 参考資料セクション
- `article-reliability-info` - 信頼性情報

## 記事構造の例

### 基本的な記事構造
```html
<div class="article-content">
  <!-- 1. 専門家バッジ -->
  <div class="article-expert-badge">
    <p>この記事は専門スタッフが執筆・監修しています。</p>
  </div>
  
  <!-- 2. リードテキスト -->
  <p class="article-lead-text">
    記事の導入文。読者の興味を引く内容。
  </p>
  
  <!-- 3. 目次 -->
  <div class="article-toc">
    <h2>この記事の要点</h2>
    <ul>
      <li><a href="#section1">セクション1</a></li>
      <li><a href="#section2">セクション2</a></li>
    </ul>
  </div>
  
  <!-- 4. 本文セクション -->
  <section id="section1">
    <h2>セクションタイトル</h2>
    <p>本文内容...</p>
  </section>
  
  <!-- 5. FAQ -->
  <div class="article-faq-section">
    <h2>よくあるご質問</h2>
    <div class="article-faq-item">
      <p class="article-faq-question">Q1: 質問内容</p>
      <p class="article-faq-answer">A1: 回答内容</p>
    </div>
  </div>
  
  <!-- 6. まとめ -->
  <div class="article-summary-section">
    <h2>まとめ</h2>
    <p>記事のまとめ...</p>
  </div>
  
  <!-- 7. CTA -->
  <section class="article-cta-section">
    <h2>行動喚起</h2>
    <a href="#" class="article-cta-button">ボタンテキスト</a>
  </section>
</div>
```

## 使用例
```html
<!-- ハイライトボックスの例 -->
<div class="article-highlight-box">
  <h4>重要なポイント</h4>
  <p>ここに重要な情報を記載します。</p>
</div>

<!-- ステップリストの例 -->
<ol class="article-steps-list">
  <li>
    <h4>Step 1: 最初のステップ</h4>
    <p>ステップの詳細説明</p>
  </li>
</ol>

<!-- FAQの例 -->
<div class="article-faq-item">
  <p class="article-faq-question">Q1: よくある質問</p>
  <p class="article-faq-answer">A1: 質問への回答</p>
</div>
```

このガイドと`article-template.html`を参考に、適切なクラス名を使用して記事HTMLを生成してください。 