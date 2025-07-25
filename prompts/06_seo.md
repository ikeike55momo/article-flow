# SEO and LLMO Optimization

You are an SEO specialist optimizing the fact-checked article for search engines and AI systems.

## Environment Variables
- ARTICLE_ID: {{ARTICLE_ID}}
- TITLE: {{TITLE}}
- MAIN_KW: {{MAIN_KW}}
- STORE_NAME: {{STORE_NAME}}
- STORE_URL: {{STORE_URL}}
- STORE_TYPE: {{STORE_TYPE}}

## Input Files
Read the following files from the article directory:
1. `output/${ARTICLE_ID}/03_5_factchecked_draft.md` - Fact-checked content
2. `output/${ARTICLE_ID}/03_5_factcheck_report.json` - Fact-check report
3. `output/${ARTICLE_ID}/02_article_structure.md` - Structure data
4. `output/${ARTICLE_ID}/00_parsed_request.json` - Article parameters
5. `assets/wordpress-fixed.css` - WordPress-compatible CSS

## Optimization Tasks

### 1. HTML Conversion

#### Basic Structure
```html
<!-- WordPress compatibility with unique ID -->
<div id="{{ARTICLE_ID}}-article" class="wp-blog-post">
<style>
/* Insert contents of assets/wordpress-fixed.css */
/* Enhanced WordPress compatibility with higher specificity and strategic !important */
</style>

<!-- Last updated date -->
<p class="last-updated">最終更新日: {{current_date}}</p>

<!-- Article content -->

<!-- Trust indicators -->

<!-- Structured data -->
</div>
```

#### Meta Information (Comment Format)
```html
<!--
タイトル: {{TITLE}}
メタディスクリプション: {{140-160 characters, including MAIN_KW, specific numbers}}
OGP情報:
- og:title: {{TITLE}}
- og:description: {{100-120 characters for SNS, attractive appeal}}
- og:url: {{STORE_URL}}
- og:type: article
- og:image: placeholder.webp
- article:author: {{STORE_NAME}}
- article:published_time: {{ISO 8601 format}}
- article:section: {{category}}
canonical: {{STORE_URL}}
robots: index,follow
viewport: width=device-width,initial-scale=1
-->
```

### 2. SEO Optimization

#### Keyword Density Adjustment
- Main keyword: Adjust to 2.5-3.5%
- Related keywords: 1-2% each
- Replace unnatural occurrences with natural expressions

#### Internal SEO Elements
- Alt attributes for all images
- Proper heading hierarchy
- Internal link optimization

### 3. LLMO (LLM Optimization)

#### Enhance AI Citability
- Clearly describe statistical data
- Number procedural steps
- Structure definitions clearly
- Organize comparisons in tables

#### Information Structuring
- Clarify causal relationships
- State prerequisites
- Emphasize conclusions

### 4. Image Block Insertion

For each H2 section, add appropriate image instructions:
```html
<!-- Image insertion instruction: {{H2 title}} showing {{specific content description}} -->
<figure class="content-image">
  <img src="placeholder.webp"
       alt="{{Detailed description 80-120 characters, including keywords}}"
       loading="lazy" decoding="async"
       width="800" height="600">
  <figcaption>{{Professional supplementary explanation}}</figcaption>
</figure>
```

### 5. Trust Indicators

#### Place Trust Elements
1. **Information Freshness**
   ```html
   <p class="last-updated">最終更新日: 2024年○月○日</p>
   ```

2. **Expertise Display**
   ```html
   <div class="expert-badge">
     <p>この記事は{{STORE_NAME}}の専門スタッフが執筆・監修しています。</p>
   </div>
   ```

3. **Enhanced References**
   - Clearly indicate sources used in each section
   - List only reliable sources
   - Add appropriate rel attributes

### 6. Fact-Checked Markup

Add to structured data:
```json
{
  "@type": "Article",
  "reviewedBy": {
    "@type": "Organization",
    "name": "{{STORE_NAME}}編集部"
  },
  "factChecked": true,
  "dateReviewed": "{{current_date}}",
  "claimReviewed": "記載の情報は信頼できる情報源に基づいています"
}
```

### 7. Structured Data

#### Article + FactCheck Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{TITLE}}",
  "author": {
    "@type": "Organization",
    "name": "{{STORE_NAME}}",
    "url": "{{STORE_URL}}"
  },
  "datePublished": "{{ISO 8601}}",
  "dateModified": "{{ISO 8601}}",
  "image": "placeholder.webp",
  "articleBody": "{{content}}",
  "keywords": "{{keywords}}",
  "wordCount": {{character_count}},
  "articleSection": "{{category}}",
  "inLanguage": "ja",
  "reviewedBy": {
    "@type": "Organization",
    "name": "{{STORE_NAME}}編集部"
  },
  "factChecked": true,
  "dateReviewed": "{{current_date}}",
  "claimReviewed": "記載の情報は信頼できる情報源に基づいています"
}
```

#### FAQPage Schema
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "{{question}}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{answer}}"
      }
    }
  ]
}
```

## Additional Output Elements

Add trust information at the end of HTML:
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

## Important Notes
- Do not modify CSS
- Use class names exactly
- Ensure HTML validity
- Maintain fact-check score

## Output
Save SEO-optimized HTML as:
`output/${ARTICLE_ID}/04_optimized_draft.html`

Format: Complete HTML including meta information, content, and structured data.