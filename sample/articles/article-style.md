# AI記事生成用スタイル仕様書

## 概要
このドキュメントは、**CSSクラス名の仕様書**です。記事生成時に使用可能なHTMLパーツとそのクラス名を定義しています。

**重要：これは記事の構成やテンプレートではありません。セマンティックなHTMLマークアップのためのパーツ集です。**

## 使用方法
1. この仕様書をAIに渡す
2. 記事の内容と構成を別途指示する
3. 関連させたいページのURL（あれば）を指定する
4. AIが指示された構成に従い、必要に応じてここで定義されたクラス名を使用してHTMLを生成
5. **生成された記事全体のHTMLコードをWordPressエディタのHTMLブロックまたはコードブロックに貼り付けて使用**

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

**重要：** 目次のリンク（`href="#section1"`）と対応するセクションのID（`id="section1"`）を一致させることで、アンカーリンクが機能します。

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

### 引用・脚注（出典）
- `article-cite` - 本文中の脚注リンク（例: [1]）
- `article-citations` - 末尾の出典リスト（番号付き）
- `fn-back` - 出典から本文へ戻るリンク（↩）

### 引用ブロック
- `article-quote` - 引用用の強調ブロック
- `quote-source` - 引用元の短い注記


## パーツの使用例

**注意：以下は個別パーツの例です。記事全体の構成は別途指示に従ってください。**
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

### 引用・脚注（出典）の使い方

本文側（例）:
```html
…老化現象の一つとされています<a class="article-cite" href="#fn-1" id="fnref-1">[1]</a>。
…改善が期待できると報告されています<a class="article-cite" href="#fn-2" id="fnref-2">[2]</a>。
```

末尾の出典リスト（「この記事の信頼性について」内）:
```html
<ol class="article-citations">
  <li id="fn-1"><a href="https://www.dermatol.or.jp/" target="_blank" rel="noopener">日本皮膚科学会</a><a href="#fnref-1" class="fn-back">↩</a></li>
  <li id="fn-2"><a href="https://example.org/clinical" target="_blank" rel="noopener">臨床的見解</a><a href="#fnref-2" class="fn-back">↩</a></li>
  
</ol>
```

### 引用ブロック（よくあるスタイル）
```html
<div class="article-quote">
  <p>適切な保湿は皮膚バリアを支えます<a class="article-cite" href="#fn-2">[2]</a>。</p>
  <span class="quote-source">参考: 専門機関の一般見解</span>
</div>
```

## ブログカード機能

### ショートコードによる自動生成

記事内の任意の場所にブログカードを挿入できます。URLから自動でタイトル、画像、説明文を取得してブログカードを生成：

```html
[blog_card url="https://example.com/article"]
```

### ショートコードのパラメータ
- `url` - ブログカードを生成したいページのURL（必須）

### 使用例
```html
<p>詳しい手順については、こちらの記事も参考にしてください。</p>

<!-- 記事内にブログカードを挿入 -->
[blog_card url="https://example.com/nail-care-basics"]

<p>上記の方法を試した後で、次のステップに進みます。</p>
```

記事生成時は別途提供される構成指示に従い、必要に応じてこの仕様書で定義されたクラス名を使用してセマンティックなHTMLを生成してください。

---

## 参考：記事の基本構造パターン

**注意：これは参考例です。記事の内容と別途指示に応じて適切に調整してください。**

```html
<div class="article-content">
  <!-- 冒頭部分（比較的固定的） -->
  <div class="article-expert-badge">
    <p>この記事は専門スタッフが執筆・監修しています。</p>
  </div>

  <p class="article-lead-text">
    記事の導入文をここに記載します。
  </p>

  <div class="article-toc">
    <h2>目次タイトル</h2>
    <ul>
      <li><a href="#section1">セクション1のタイトル</a></li>
      <li><a href="#section2">セクション2のタイトル</a></li>
    </ul>
  </div>

  <!-- 記事本文（内容に応じて柔軟に構成） -->
  <section id="section1">
    <h2>セクション1のタイトル</h2>
    <!-- 各種パーツを適切に使用 -->
  </section>

  <!-- 末尾部分（比較的固定的） -->
  <section class="article-cta-section">
    <h2>行動喚起タイトル</h2>
    <p>読者への行動喚起メッセージ</p>
    <a href="#" class="article-cta-button">ボタンテキスト</a>
  </section>

  <div class="article-reliability-info">
    <h3>この記事の信頼性について</h3>
    <ol class="article-citations">
      <!-- 出典リスト -->
    </ol>
  </div>
</div>
``` 