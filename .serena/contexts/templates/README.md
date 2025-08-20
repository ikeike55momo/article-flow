# Templates Context

This context contains article templates, HTML structures, and styling guidelines for consistent article generation.

## Key Files

### Article Templates
- **article-template.html**: Base HTML template with complete styling
- **article-style.md**: Comprehensive style guide with CSS class documentation
- **hand-cream-article.html**: Complete example article demonstrating all features

### Location
All template files are located in: `sample/articles/`

## HTML Structure Overview

### Root Container
```html
<div class="article-content">
  <!-- All article content goes here -->
</div>
```

### Essential Components

#### 1. Expert Badge & Lead Text
```html
<div class="article-expert-badge">
  <p>この記事は専門スタッフが執筆・監修しています。</p>
</div>
<p class="article-lead-text">
  記事の導入文。読者の興味を引く内容。
</p>
```

#### 2. Table of Contents
```html
<div class="article-toc">
  <h2>この記事の要点</h2>
  <ul>
    <li><a href="#section1">セクション1</a></li>
  </ul>
</div>
```

#### 3. Images with Captions
```html
<div class="article-content-image">
  <img src="image.jpg" alt="画像の説明">
  <figcaption>画像のキャプション</figcaption>
</div>
```

#### 4. Highlight Boxes
```html
<div class="article-highlight-box">
  <h4>重要なポイント</h4>
  <p>重要な情報をハイライト</p>
</div>
```

#### 5. Step Lists
```html
<ol class="article-steps-list">
  <li>
    <h4>Step 1: タイトル</h4>
    <p>詳細説明</p>
  </li>
</ol>
```

#### 6. FAQ Section
```html
<div class="article-faq-section">
  <h2>よくあるご質問</h2>
  <div class="article-faq-item">
    <p class="article-faq-question">Q1: 質問</p>
    <p class="article-faq-answer">A1: 回答</p>
  </div>
</div>
```

#### 7. Citations and References
```html
<!-- In-text citation -->
<a class="article-cite" href="#fn-1" id="fnref-1">[1]</a>

<!-- Reference list at end -->
<div class="article-reliability-info">
  <h3>この記事の信頼性について</h3>
  <ol class="article-citations">
    <li id="fn-1">
      <a href="URL" target="_blank" rel="noopener">ソース名</a>
      <a href="#fnref-1" class="fn-back">↩</a>
    </li>
  </ol>
</div>
```

#### 8. CTA Section
```html
<section class="article-cta-section">
  <h2>行動喚起タイトル</h2>
  <p>誘導文</p>
  <a href="#" class="article-cta-button">ボタンテキスト</a>
</section>
```

## Usage in Workflow

### Prompt Integration
Templates are referenced in prompts:
- `04_writing_v4_html_updated.md` uses these templates
- Claude reads template files for structure understanding
- Output must match template format exactly

### Quality Requirements
- Valid HTML5 structure
- Responsive design (mobile-first)
- Accessibility compliance
- SEO-optimized markup
- Fast loading performance

### Customization Points
- CTA button URLs and text
- Color scheme variables
- Typography settings
- Image aspect ratios
- Section ordering