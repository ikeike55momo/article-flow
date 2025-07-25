# フェーズ4: SEO/LLMO最適化（ファクトチェック済み版）

## 入力情報
- factchecked_content: {{03_5_factchecked_draft.md}}
- factcheck_report: {{03_5_factcheck_report.json}}
- research_data: {{01_research.json}}
- structure_data: {{02_structure.json}}

## 最適化タスク

### 1. HTML変換

#### 基本構造
```html
<!-- WordPress互換性を考慮したID追加 -->
<div id="nail-care-article" class="wp-blog-post">
<style>
/* assets/wordpress-fixed.cssの内容を挿入（WordPress互換性強化版） */
/* 詳細度を上げ、!importantを戦略的に使用 */
</style>

<!-- 最終更新日 -->
<p class="last-updated">最終更新日: {{current_date}}</p>

<!-- 記事本文 -->

<!-- 信頼性情報 -->

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

### 5. 信頼性表示の追加

#### 信頼性を示す要素の配置
1. **情報の新しさを明示**
   ```html
   <p class="last-updated">最終更新日: 2024年○月○日</p>
   ```

2. **専門性の明示**
   ```html
   <div class="expert-badge">
     <p>この記事は{{store_name}}の専門スタッフが執筆・監修しています。</p>
   </div>
   ```

3. **参考文献の強化**
   - 各セクションで使用した情報源を明確に
   - 信頼できる出典のみを掲載
   - 適切なrel属性の付与

### 6. ファクトチェック済みマークアップ

構造化データに追加：
```json
{
  "@type": "Article",
  "reviewedBy": {
    "@type": "Organization",
    "name": "{{store_name}}編集部"
  },
  "factChecked": true,
  "dateReviewed": "{{current_date}}",
  "claimReviewed": "記載の情報は信頼できる情報源に基づいています"
}
```

### 7. 構造化データ

#### Article + FactCheck
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
  "inLanguage": "ja",
  "reviewedBy": {
    "@type": "Organization",
    "name": "{{store_name}}編集部"
  },
  "factChecked": true,
  "dateReviewed": "{{current_date}}",
  "claimReviewed": "記載の情報は信頼できる情報源に基づいています"
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

## 出力時の追加要素

HTMLの最後に信頼性情報を追加：
```html
<div class="reliability-info">
  <h3>この記事の信頼性について</h3>
  <ul>
    <li>すべての統計データは信頼できる情報源から引用しています</li>
    <li>専門的な内容は複数の資料で確認済みです</li>
    <li>最新の情報に基づいて作成されています</li>
  </ul>
</div>
```

## 重要な注意事項
- CSSは一切変更しない
- クラス名は正確に使用
- HTML構文の妥当性を確保
- ファクトチェックスコアを維持

## ファイル保存

SEO最適化されたHTMLを以下のファイルに保存：
```
output/{date}-{title_slug}/04_optimized_draft.html
```

保存形式：完全なHTML形式（メタ情報、本文、構造化データすべて含む）