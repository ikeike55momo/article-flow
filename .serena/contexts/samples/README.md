# Samples Context

This context contains sample articles, templates, and reference materials that demonstrate the expected output format and quality standards.

## Sample Files Location
All sample files are located in: `sample/articles/`

## Core Sample Files

### 1. Article Style Guide (`article-style.md`)
**Purpose**: Comprehensive documentation of all available CSS classes and HTML structure
**Content**:
- Complete CSS class reference (30+ classes)
- HTML structure examples
- Usage guidelines for each component
- Citation and reference formatting
- Accessibility and SEO considerations

**Key Sections**:
- Basic structure (`article-content` container)
- Navigation elements (`article-toc`)
- Content blocks (`article-highlight-box`, `article-quote`)
- Media handling (`article-content-image`)
- Interactive elements (`article-faq-section`)
- Citations (`article-cite`, `article-citations`)
- Call-to-action (`article-cta-section`)

### 2. HTML Template (`article-template.html`)
**Purpose**: Complete HTML template with embedded CSS styling
**Features**:
- Mobile-responsive design
- Inline CSS for WordPress compatibility
- Accessibility compliance (ARIA labels, semantic markup)
- SEO-optimized structure
- Professional typography and spacing

### 3. Example Article (`hand-cream-article.html`)
**Purpose**: Real-world example demonstrating all template features
**Content**: Complete article about hand cream for sensitive skin
**Demonstrates**:
- Proper citation integration (5+ sources)
- Image placement with captions
- FAQ section with 5 Q&As
- Step-by-step instructions
- Highlight boxes for important information
- Professional CTA section
- Author credibility section

## Template Architecture

### CSS Framework
```css
/* Container */
.article-content { /* Main wrapper */ }

/* Navigation */
.article-toc { /* Table of contents */ }

/* Content Blocks */
.article-highlight-box { /* Important callouts */ }
.article-quote { /* Emphasized quotes */ }
.article-steps-list { /* Numbered procedures */ }

/* Media */
.article-content-image { /* Image containers */ }

/* Interactive */
.article-faq-section { /* FAQ functionality */ }
.article-cta-section { /* Call-to-action */ }

/* Citations */
.article-cite { /* In-text citations */ }
.article-citations { /* Reference list */ }
```

### Responsive Design
- **Mobile-first approach**: Optimized for phones and tablets
- **Flexible layouts**: Adapts to various screen sizes
- **Touch-friendly**: Appropriate button and link sizing
- **Fast loading**: Optimized CSS and minimal external dependencies

### Accessibility Features
- **Semantic HTML**: Proper heading hierarchy and landmark elements
- **ARIA labels**: Screen reader support
- **Keyboard navigation**: Full keyboard accessibility
- **Color contrast**: WCAG 2.1 AA compliance
- **Alternative text**: Comprehensive image descriptions

## Content Standards

### Article Structure Requirements
1. **Expert Badge**: Credibility indicator at the top
2. **Lead Text**: Engaging introduction (10-15% of content)
3. **Table of Contents**: 3-6 main sections with anchor links
4. **Main Sections**: 4-6 content sections with images
5. **Highlight Boxes**: 2-3 important callouts per section
6. **FAQ Section**: Minimum 3 question-answer pairs
7. **Summary**: Conclusion and key takeaways
8. **CTA Section**: Relevant call-to-action
9. **Citations**: Minimum 5 reliable sources
10. **Author Info**: Credibility and expertise information

### Content Quality Standards
- **Word Count**: 3200± words (configurable)
- **Readability**: Appropriate for target audience education level
- **Fact Accuracy**: All claims supported by reliable sources
- **Legal Compliance**: Adheres to 薬機法 and 景表法
- **SEO Optimization**: Natural keyword integration
- **Persona Targeting**: Content adapted to specified audience

### Citation Requirements
- **Source Quality**: Government, academic, professional sources preferred
- **Recency**: Sources within 3 years for trending topics
- **Diversity**: Multiple types of sources (studies, expert opinions, official guidelines)
- **Attribution**: Clear in-text citations with numbered references
- **Accessibility**: Working links with proper target="_blank" and rel="noopener"

## Usage Guidelines

### For AI Prompts
These samples serve as the foundation for article generation:
1. **Reference Reading**: All prompts must reference these files
2. **Format Compliance**: Output must match template structure exactly
3. **Quality Benchmarking**: Generated content should meet sample standards
4. **Style Consistency**: Use established CSS classes and HTML patterns

### For Quality Review
- **Structure Check**: Verify all required sections are present
- **Citation Validation**: Ensure proper source attribution
- **Template Compliance**: Confirm CSS class usage
- **Content Quality**: Review against sample article standards

### For Template Updates
- **Backward Compatibility**: Maintain existing CSS class functionality
- **Documentation Updates**: Update style guide with any changes
- **Example Updates**: Refresh sample article if needed
- **Prompt Updates**: Modify AI prompts to reflect template changes

## Sample File Relationships

### Template Inheritance
```
article-style.md (Documentation)
    ↓ (Implements)
article-template.html (Base Template)
    ↓ (Demonstrates)
hand-cream-article.html (Example Usage)
    ↓ (Referenced by)
AI Prompts (Generation Instructions)
```

### Content Flow
1. **Style Guide**: Defines available components and usage rules
2. **Template**: Provides technical implementation with CSS
3. **Example**: Shows real-world application of all features
4. **AI Generation**: Creates new content following established patterns

## Customization Points

### Visual Customization
- **Color Scheme**: Modify CSS custom properties for brand colors
- **Typography**: Adjust font families and sizing
- **Spacing**: Update margins and padding for different layouts
- **Component Styling**: Customize individual element appearance

### Content Customization
- **CTA Integration**: Update call-to-action URLs and messaging
- **Branding**: Modify expert badges and author information
- **Language**: Adapt for different languages while maintaining structure
- **Industry Focus**: Customize examples for specific content verticals

### Technical Customization
- **WordPress Integration**: Optimize for specific WordPress themes
- **Performance**: Adjust CSS for faster loading
- **Accessibility**: Enhance for specific accessibility requirements
- **SEO**: Optimize markup for better search engine performance