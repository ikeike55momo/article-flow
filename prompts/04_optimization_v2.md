# フェーズ4: SEO/LLMO最適化（WordPress完全対応版）

## 入力情報
- factchecked_content: {{03_5_factchecked_draft.md}}
- factcheck_report: {{03_5_factcheck_report.json}}
- research_data: {{01_research.json}}
- structure_data: {{02_structure.json}}

## 最重要事項
**単一HTMLブロックのみを返す（説明文なし）**
**WordPress専用CSS（改変禁止）を完全にインライン記述**

## 最適化タスク

### 1. HTML変換（WordPress エディター完全対応）

#### 文字コードと特殊文字の処理
- **最重要**: 出力するHTML全体について、特殊文字（例: ©, ™, →, • など）は必ず文字実体参照（例: `&copy;`, `&trade;`, `&rarr;`, `&bull;`）に変換してください。これにより、環境による文字化けを完全に防ぎます。
- 文字エンコーディングはUTF-8を想定していますが、文字実体参照への変換を優先してください。

#### 出力形式
```html
<!-- WordPress必須メタ情報 -->
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

<div class="wp-blog-post">
<style>
/* ★ WordPress 専用 CSS（改変禁止・性能最適化済み）★ */
/* エディター競合回避のため全CSSを.wp-blog-post内に限定 */
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
.wp-blog-post .reliability-info {
  background: #e8f5e9;
  border: 1px solid #81c784;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 2rem 0;
}
.wp-blog-post .reliability-info h3 {
  color: #2e7d32;
  margin-top: 0;
  font-size: 1.2rem;
}
.wp-blog-post .reliability-info ul {
  margin: 1rem 0 0;
  padding-left: 1.5rem;
}
.wp-blog-post .reliability-info li {
  margin-bottom: 0.5rem;
  color: #388e3c;
}
.wp-blog-post .last-updated {
  text-align: right;
  font-size: 0.9rem;
  color: #6c757d;
  margin: 1rem 0;
  font-style: italic;
}
.wp-blog-post .expert-badge {
  background: #f0f7ff;
  border: 1px solid #0068d9;
  border-radius: 8px;
  padding: 1rem;
  margin: 1.5rem 0;
  text-align: center;
}
.wp-blog-post .expert-badge p {
  margin: 0;
  color: #0068d9;
  font-weight: 500;
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
</style>

<!-- 記事本文 -->
<p class="last-updated">最終更新日: {{current_date}}</p>

<div class="expert-badge">
  <p>この記事は{{store_name}}の専門スタッフが執筆・監修しています。</p>
</div>

{{記事本文のHTML}}

<div class="reliability-info">
  <h3>この記事の信頼性について</h3>
  <ul>
    <li>すべての統計データは信頼できる情報源から引用しています</li>
    <li>専門的な内容は複数の資料で確認済みです</li>
    <li>最新の情報に基づいて作成されています</li>
  </ul>
</div>

<!-- 構造化データ -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{title}}",
  "author": {
    "@type": "Organization",
    "name": "{{store_name}}",
    "url": "{{store_url}}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "{{store_name}}"
  },
  "datePublished": "{{publish_date}}",
  "dateModified": "{{modified_date}}",
  "reviewedBy": {
    "@type": "Organization",
    "name": "{{store_name}}編集部"
  },
  "factChecked": true,
  "dateReviewed": "{{current_date}}",
  "claimReviewed": "記載の情報は信頼できる情報源に基づいています"
}
</script>

</div>
```

### 2. SEO最適化（変更なし）

#### キーワード密度の調整
- メインキーワード: 2.5-3.5%に調整
- 関連キーワード: 各1-2%に調整
- 不自然な箇所を自然な表現に

#### 内部SEO要素
- すべての画像にalt属性
- 適切な見出し階層
- 内部リンクの最適化

### 3. LLMO（LLM最適化）（変更なし）

#### AI引用性の向上
- 統計データを明確に記述
- 手順を番号付きリストで
- 定義を明確に構造化
- 比較を表形式で整理

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

## 重要な注意事項
- **単一HTMLブロックのみを返す（説明文なし）**
- **CSS改変は絶対に禁止**
- **WordPress エディター競合回避のためCSS全体を.wp-blog-post内に限定**
- **HTMLは上記フォーマットを厳守**