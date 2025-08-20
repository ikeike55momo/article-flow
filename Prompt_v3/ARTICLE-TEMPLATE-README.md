# AI記事生成用スタイル仕様書

## 概要
このドキュメントは、**CSSクラス名の仕様書**です。記事生成時に使用可能なHTMLパーツとそのクラス名を定義しています。

**重要：これは記事の構成やテンプレートではありません。セマンティックなHTMLマークアップのためのパーツ集です。**

## 使用方法
1. この仕様書をAIに渡す
2. 記事のタイトルや書きたい内容(あれば)を指定する（基本的にはタイトルのみで十分）
3. 関連させたいページのURL（あれば）を指定する
4. AIがタイトルに基づいて記事を作成し、必要に応じてここで定義されたクラス名を使用してHTMLを生成
5. **生成された記事全体のHTMLコードをWordPressエディタのHTMLブロックまたはコードブロックに貼り付けて使用**
6. **目立たせたいテキストには`<strong>`タグを使用して強調表示する**

## 利用可能なクラス名一覧

### 基本構造
```html
<div class="article-content">
  <!-- 記事本文全体を囲むコンテナ -->
</div>
```

### 基本要素
- `article-expert-badge` - 信頼性バッジ（筆者が実際に体験・調査した記事であることを示す）
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

**使用制限：** ハイライトボックスは1つのセクション内で1個まで。基本的にはh3見出し+pテキストの構造を使用し、本当に重要な情報のみハイライトボックスで強調する。

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
- `article-faq-question` - FAQの質問（label要素）
- `article-faq-answer` - FAQの回答（div要素）

### セクション
- `article-summary-section` - まとめセクション
- `article-cta-section` - CTA（行動喚起）セクション
- `article-cta-button` - CTAボタン
- `article-related-section` - 関連記事セクション
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
<!-- 信頼性バッジの例（汎用的） -->
<div class="article-expert-badge">
  <p>この記事は実際に体験・調査を行った上で執筆しています。</p>
</div>

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
  <input type="checkbox" id="faq1">
  <label for="faq1" class="article-faq-question">
    <span>Q1: よくある質問</span>
  </label>
  <div class="article-faq-answer">A1: 質問への回答</div>
</div>
```

### 引用・脚注（出典）の使い方

本文側（例）:
```html
…詳しく解説しています<a class="article-cite" href="#fn-1" id="fnref-1">[1]</a>。
…効果的な方法として推奨されています<a class="article-cite" href="#fn-2" id="fnref-2">[2]</a>。
```

末尾の出典リスト（「この記事の信頼性について」内）:
```html
<ol class="article-citations">
  <li id="fn-1"><a href="https://example.org/reference1" target="_blank" rel="noopener">参考資料1</a><a href="#fnref-1" class="fn-back">↩</a></li>
  <li id="fn-2"><a href="https://example.org/reference2" target="_blank" rel="noopener">参考資料2</a><a href="#fnref-2" class="fn-back">↩</a></li>
</ol>
```

### 引用ブロック（よくあるスタイル）
```html
<div class="article-quote">
  <p>引用したい内容をここに記載します<a class="article-cite" href="#fn-2">[2]</a>。</p>
  <span class="quote-source">参考: 関連機関の見解</span>
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
[blog_card url="https://example.com/related-guide"]

<p>上記の方法を試した後で、次のステップに進みます。</p>
```

## 重要な注意点

### 基本的な記事構造
- **基本構成：** h3見出し + pテキストを基本とする
- **シンプルな構造：** 過度な装飾を避け、読みやすさを重視

### ハイライトボックスの使用指針
- **導入部分（リードテキスト周辺）：** キャッチーさを演出するため積極的に使用推奨
- **メインセクション内：** 基本的にh3+p構造を使用。本当に重要な情報のみ1個まで使用可
- **料金・重要情報セクション：** 複雑な情報を整理する場合は使用可
- **過度な使用は避ける：** 読み手に負担をかけないよう配慮

### テキストの強調表示
- **`<strong>`タグは文章内の重要なポイントのみに使用する**
- 重要なポイント、注意点、推奨事項、成功のコツなど、文章中で強調したい部分に使用
- 読者の理解を助け、記事の価値を高める
- 多用しすぎないこと（強調しすぎると読みにくくなる）
- **以下の場所では使用しない：**
  - ラベル（「住所：」など）
  - 項目名・見出し
  - 短い単語やラベル
  - 専門家バッジ・CTAセクション

### FAQセクションの構造
- 各FAQ項目で一意のIDを設定（faq1, faq2, faq3...）
- `input[type="checkbox"]`と`label[for]`のIDを一致させる
- 質問文は必ず`<span>`要素で囲む
- チェックボックスは非表示（CSSで制御）

### 構造化データの抽出
- FAQ: `label.article-faq-question span`のテキスト + `.article-faq-answer`のテキスト
- 手順: `.article-steps-list`から手順情報
- 料金: `.article-comparison-table`から価格情報
- 商品・サービス: `.article-highlight-box`から商品・サービス情報

記事生成時はタイトルに基づいて適切な構成を判断し、必要に応じてこの仕様書で定義されたクラス名を使用してセマンティックなHTMLを生成してください。

---

## 参考：記事の基本構造パターン

**注意：これは参考例です。記事のタイトルや内容に応じて適切に調整してください。**

```html
<div class="article-content">
  <!-- 冒頭部分（比較的固定的） -->
  <div class="article-expert-badge">
    <p>この記事は<strong>実際に体験・調査を行った上で執筆</strong>しています。</p>
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