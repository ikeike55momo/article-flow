# Template Analysis & Best Practices

## Hand Cream Article Analysis

The `hand-cream-article.html` sample demonstrates professional article structure and serves as the gold standard for content generation.

### Article Metrics
- **Total Word Count**: ~3,200 words
- **Reading Time**: ~8-10 minutes
- **Section Count**: 6 main sections
- **FAQ Count**: 5 comprehensive Q&As
- **Citation Count**: 8 reliable sources
- **Image Placements**: 6 strategic locations

### Content Structure Breakdown

#### 1. Header Section (5% of content)
```html
<div class="article-expert-badge">
  <p>この記事は専門スタッフが執筆・監修しています。</p>
</div>
```
- **Purpose**: Establish credibility immediately
- **Best Practice**: Always include professional validation

#### 2. Lead Text (12% of content)
```html
<p class="article-lead-text">
  手は日常生活で最も使用頻度が高い部位でありながら、
  年齢とともに乾燥や小じわが目立ちやすくなります...
</p>
```
- **Features**: Hook + problem statement + article preview
- **Length**: 320-400 words
- **Strategy**: Emotional connection → problem identification → solution preview

#### 3. Table of Contents (3% of content)
```html
<div class="article-toc">
  <h2>この記事の要点</h2>
  <ul>
    <li><a href="#sensitive-skin-basics">敏感肌の基礎知識</a></li>
    <li><a href="#hand-cream-selection">ハンドクリームの選び方</a></li>
    <!-- ... -->
  </ul>
</div>
```
- **Purpose**: Improve user experience and SEO
- **Best Practice**: 4-6 main sections with descriptive anchor text

#### 4. Main Content Sections (60% of content)

**Section Pattern**:
```html
<section id="section-id">
  <h2>Section Title</h2>
  
  <!-- Introduction paragraph -->
  <p>Section introduction...</p>
  
  <!-- Image placement -->
  <div class="article-content-image">
    <img src="..." alt="descriptive text">
    <figcaption>Image caption with context</figcaption>
  </div>
  
  <!-- Content with highlight box -->
  <div class="article-highlight-box">
    <h4>重要なポイント</h4>
    <p>Key takeaway or important information</p>
  </div>
  
  <!-- Detailed content with citations -->
  <p>Content with source<a class="article-cite" href="#fn-1">[1]</a>.</p>
</section>
```

**Effective Section Themes**:
1. **Problem Context**: Background and why it matters
2. **Solution Framework**: Methodology or approach
3. **Detailed Instructions**: Step-by-step guidance
4. **Advanced Tips**: Expert-level insights
5. **Common Mistakes**: What to avoid
6. **Results & Benefits**: Expected outcomes

#### 5. FAQ Section (15% of content)
```html
<div class="article-faq-section">
  <h2>よくあるご質問</h2>
  <div class="article-faq-item">
    <p class="article-faq-question">Q1: 敏感肌用のハンドクリームは本当に効果がありますか？</p>
    <p class="article-faq-answer">A1: はい、敏感肌向けに開発された...</p>
  </div>
</div>
```

**FAQ Best Practices**:
- Address real user concerns and objections
- Include practical application questions
- Provide actionable, specific answers
- Reference main article content where relevant
- Maintain conversational tone while being informative

#### 6. Summary & CTA (5% of content)
```html
<div class="article-summary-section">
  <h2>まとめ</h2>
  <p>敏感肌の方がハンドクリームを選ぶ際は...</p>
</div>

<section class="article-cta-section">
  <h2>プロのハンドケアで手肌を若返らせましょう</h2>
  <p>専門スタッフによる個別カウンセリングで...</p>
  <a href="https://beauty.hotpepper.jp/kr/slnH000618948/" class="article-cta-button">ご予約はこちら</a>
</section>
```

## Citation Excellence

### Citation Strategy in Sample
1. **Authoritative Sources**: Government health agencies, medical associations
2. **Recent Research**: Studies within 2-3 years
3. **Diverse Perspectives**: Multiple expert viewpoints
4. **Practical Application**: Sources that support actionable advice

### Citation Implementation
```html
<!-- In-text citation -->
<a class="article-cite" href="#fn-1" id="fnref-1">[1]</a>

<!-- Reference list -->
<ol class="article-citations">
  <li id="fn-1">
    <a href="https://www.dermatol.or.jp/" target="_blank" rel="noopener">日本皮膚科学会</a>
    <a href="#fnref-1" class="fn-back" aria-label="本文へ戻る">↩</a>
  </li>
</ol>
```

### Source Quality Hierarchy (from sample)
1. **日本皮膚科学会** (Japanese Dermatological Association) - 95% reliability
2. **厚生労働省** (Ministry of Health) - 95% reliability  
3. **Clinical studies** - 90% reliability
4. **Professional dermatologist opinions** - 85% reliability
5. **Industry reports** - 80% reliability

## Visual Design Patterns

### Image Placement Strategy
1. **Hero Image**: After lead text, before main content
2. **Section Images**: Mid-section to break up text
3. **Process Images**: Support step-by-step instructions
4. **Result Images**: Show before/after or outcomes
5. **Summary Image**: Visual conclusion

### Highlight Box Usage
- **1-2 per section**: Avoid overwhelming readers
- **Key Takeaways**: Most important points
- **Safety Information**: Warnings or precautions
- **Pro Tips**: Expert-level insights
- **Quick Summaries**: Complex information simplified

### Typography Hierarchy
```
H1: Article Title (single use)
H2: Main Section Headings (4-6 sections)
H3: FAQ Questions, Subsections
H4: Highlight Box Titles, Step Titles
P: Body text, answers, descriptions
```

## Content Voice & Tone

### Professional Characteristics
- **Authoritative**: Backed by credible sources
- **Accessible**: Complex topics explained simply
- **Practical**: Actionable advice and clear steps
- **Empathetic**: Understanding of user challenges
- **Confident**: Definitive guidance without overselling

### Language Patterns
- **Problem-Solution Structure**: Identify issues, provide solutions
- **Evidence-Based Claims**: Every assertion supported by sources
- **Inclusive Language**: Accessible to diverse audiences
- **Clear Instructions**: Unambiguous action steps
- **Positive Framing**: Focus on benefits and improvements

## Performance Benchmarks

### SEO Performance Indicators
- **Title Optimization**: Primary keyword in H1
- **Meta Description Ready**: First paragraph suitable for excerpts
- **Internal Linking**: Natural opportunities for related content
- **Schema Markup Ready**: Structured for rich snippets
- **Mobile Optimization**: Responsive design implementation

### User Engagement Metrics
- **Time on Page**: Comprehensive content encourages longer reading
- **Scroll Depth**: Well-structured sections promote full article consumption
- **Click-Through Rate**: Compelling CTAs drive action
- **Return Visits**: High-quality content builds audience loyalty

### Technical Performance
- **Load Speed**: Inline CSS and optimized images
- **Accessibility Score**: High compliance with WCAG guidelines
- **Mobile Usability**: Touch-friendly design elements
- **Cross-Browser Compatibility**: Consistent rendering across platforms

This template analysis serves as a benchmark for all future article generation, ensuring consistent quality and effectiveness across the content pipeline.