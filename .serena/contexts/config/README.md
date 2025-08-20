# Configuration Context

This context contains configuration files, rules, and settings for the article generation workflow.

## Configuration Files

### Core Configuration
- **workflow.yaml**: Main workflow configuration with phase definitions
- **requirements.yaml**: Content requirements and standards
- **factcheck_rules.yaml**: Fact-checking validation rules
- **templates.yaml**: Template selection and configuration

### WordPress Integration
- **wordpress-compatibility.yaml**: WordPress-specific settings
- **wordpress-inline-css.md**: CSS inline styling guidelines
- **wordpress-fixed.css**: Production CSS styles
- **wordpress.css**: Base WordPress styles

## Workflow Configuration (workflow.yaml)

### Phase Definition
```yaml
phases:
  - id: "parse"
    name: "リクエスト解析"
    prompt: "prompts/00_parse_request.md"
    output: "parsed_request"
```

### Research Settings
```yaml
factcheck_settings:
  enabled: true
  strict_mode: true
  require_multiple_sources: true
  max_age_days: 1095  # 3 years
```

### Quality Thresholds
```yaml
quality_threshold: 85
factual_accuracy_threshold: 90
```

## Fact-checking Rules

### Content Validation
- Medical claims require peer-reviewed sources
- Statistics need government or academic backing
- Product recommendations need multiple independent sources
- Safety information requires official health authority confirmation

### Source Quality Requirements
- **Primary Sources**: Government agencies, medical journals (95%+ reliability)
- **Secondary Sources**: Established health websites, expert articles (80%+ reliability)
- **Supporting Sources**: News with expert quotes, educational content (70%+ reliability)

### Legal Compliance (Health/Beauty Content)
- 薬機法 (Pharmaceutical and Medical Device Act) compliance
- 景表法 (Act against Unjustifiable Premiums and Misleading Representations) compliance
- No unsubstantiated medical claims
- Clear disclaimers for health-related advice

## Template Configuration

### HTML Template Settings
```yaml
template:
  type: "html5"
  css_inline: true
  mobile_responsive: true
  accessibility_compliant: true
  seo_optimized: true
```

### Required Sections
- Expert badge for credibility
- Lead text with hook (10-15% of content)
- Table of contents (3-6 sections)
- Main content sections with images
- FAQ section (minimum 3 Q&As)
- Summary/conclusion section
- CTA section with dynamic content
- Citations and reliability information

## SEO Configuration

### Keyword Integration
- Natural keyword density (1-3%)
- Semantic keyword variations
- Long-tail keyword optimization
- User intent matching

### Meta Data Requirements
- Title: 50-60 characters
- Meta description: 120-160 characters
- Focus keyword identification
- Secondary keyword list
- Schema markup preparation

### Content Structure
- H1: Single use for main title
- H2: Section headings (4-6 sections)
- H3: Subsections and FAQ questions
- H4: Highlight boxes and step titles

## Image Generation Settings

### Default Image Configuration
```yaml
images:
  hero_image:
    aspect_ratio: "16:9"
    size: "1200x675"
    type: "primary_visual"
  
  section_images:
    aspect_ratio: "4:3"
    size: "800x600"
    type: "content_support"
    
  count: 4-5
  model: "imagen-4"
```

### Style Guidelines
- Professional, clean aesthetic
- Consistent color palette
- High quality, stock-photo style
- No text overlay
- Appropriate for target demographic

## Performance Configuration

### API Limits
- Claude API: Standard rate limits
- Gemini API: 3 concurrent batches
- Image generation: 5 images per article
- Research queries: 15-25 per article

### Timeout Settings
- Initialize: 5 minutes
- Analysis: 10 minutes
- Research (per batch): 15 minutes
- Content generation: 20 minutes
- Fact-checking: 15 minutes
- Image generation: 20 minutes
- Finalization: 10 minutes

### Artifact Retention
- GitHub Artifacts: 30 days
- Final package: Permanent until manual deletion
- Development files: Local cleanup after success

## Security Configuration

### API Key Management
- All keys stored in GitHub Secrets
- No keys in workflow files or logs
- Environment-specific key rotation
- Access logging for audit trails

### Content Security
- No personal information collection
- External link validation
- Safe content generation
- Privacy-compliant practices

## Error Handling

### Fallback Strategies
- Research batch failure → retry with reduced queries
- Image generation failure → continue without images
- Fact-check failure → manual review required
- Template compliance failure → format correction

### Quality Gates
- Research reliability score ≥ 80%
- Fact-checking score ≥ 85%
- Citation count ≥ 5 sources
- Template format validation
- SEO requirements compliance

## Environment-Specific Settings

### Development
- Extended timeouts for debugging
- Detailed logging enabled
- Test data generation
- Local file preservation

### Production (GA Environment)
- Optimized timeouts
- Error-only logging
- Real API usage
- Automatic cleanup

### Testing
- Mock API responses
- Simplified validation
- Fast execution
- Repeatable results