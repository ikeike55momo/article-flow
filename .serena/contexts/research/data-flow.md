# Research Data Flow Architecture

## Overview
The research data flow in article-flow V4 uses a parallel processing architecture with Gemini API for efficient web research and fact validation.

## Phase-by-Phase Data Flow

### Phase 1: Request Analysis
**Input**: User request (title, persona, keywords)
**Process**: Claude analyzes request and generates research queries
**Output**: `phase1_output.json`

```json
{
  "analysis": {
    "main_keyword": "extracted keyword",
    "related_keywords": ["keyword1", "keyword2"],
    "research_queries": ["query1", "query2", ..., "query20"],
    "search_intent": "informational",
    "content_type": "how-to"
  }
}
```

### Phase 2: Query Batch Processing
**Input**: `phase1_output.json`
**Process**: Split queries into 3 parallel batches
**Output**: Individual batch directories

```
batch_0/
├── queries.json      # Batch-specific queries
├── analysis.json     # Analysis subset for this batch
└── results.json      # Research results (created by Gemini)

batch_1/
├── queries.json
├── analysis.json
└── results.json

batch_2/
├── queries.json
├── analysis.json
└── results.json
```

### Phase 3: Parallel Research Execution
**Input**: Batch queries and analysis
**Process**: Gemini API performs web research for each batch
**Output**: Structured research results per batch

```json
{
  "batch_id": 0,
  "query_results": [
    {
      "query": "research question",
      "sources": [
        {
          "url": "https://source.com",
          "title": "Source Title",
          "content": "Relevant excerpt",
          "reliability_score": 85,
          "source_type": "academic"
        }
      ]
    }
  ],
  "batch_stats": {
    "total_queries": 7,
    "total_sources": 45,
    "avg_reliability": 82
  }
}
```

### Phase 4: Research Merge & Scoring
**Input**: All batch result files
**Process**: Combine results and apply quality scoring
**Output**: `research_results.json`

```json
{
  "research_summary": {
    "total_sources": 150,
    "avg_reliability_score": 83,
    "source_types": {
      "academic": 45,
      "government": 30,
      "professional": 50,
      "news": 25
    }
  },
  "query_results": [
    {
      "query": "combined query",
      "best_sources": [
        {
          "url": "https://reliable-source.com",
          "title": "Authoritative Title",
          "excerpt": "Key information",
          "reliability_score": 95,
          "citation_ready": true
        }
      ]
    }
  ],
  "recommended_citations": [
    {
      "citation_id": 1,
      "url": "https://source1.com",
      "title": "Source 1 Title",
      "reliability": 95
    }
  ]
}
```

## Content Generation Data Flow

### Phase 5: Article Structure
**Input**: `research_results.json`, `phase1_output.json`
**Process**: Claude creates article outline using research
**Output**: `01_article_structure.md`, `02_content_plan.md`

### Phase 6: Content Writing
**Input**: All previous files + templates
**Process**: Claude writes HTML article with citations
**Output**: `final_article.html`

```html
<!-- Article with embedded citations -->
<div class="article-content">
  <p>Content with citation<a class="article-cite" href="#fn-1">[1]</a>.</p>
  
  <!-- Citations at end -->
  <div class="article-reliability-info">
    <ol class="article-citations">
      <li id="fn-1">
        <a href="https://source.com" target="_blank">Source Title</a>
        <a href="#fnref-1" class="fn-back">↩</a>
      </li>
    </ol>
  </div>
</div>
```

### Phase 7: Fact-checking & Quality Validation
**Input**: `final_article.html`, `research_results.json`
**Process**: Claude validates article against research
**Output**: `factcheck_report.json`

```json
{
  "overall_quality_score": 87,
  "fact_accuracy_score": 92,
  "legal_compliance_score": 95,
  "source_reliability_score": 89,
  "issues_found": [
    {
      "type": "minor_accuracy",
      "description": "Statistic needs verification",
      "corrected": true
    }
  ],
  "recommendations": [
    "Consider adding more recent studies",
    "Expand safety information section"
  ]
}
```

## Final Package Assembly

### Phase 8: SEO Metadata Generation
**Output**: `seo_metadata.json`

```json
{
  "title": "SEO-optimized title (60 chars)",
  "meta_description": "Compelling description (160 chars)",
  "focus_keyword": "primary keyword",
  "secondary_keywords": ["keyword2", "keyword3"],
  "schema_type": "Article",
  "estimated_reading_time": "8 minutes"
}
```

### Phase 9: Image Generation
**Output**: `images/` directory with generated images

### Phase 10: Final Package
**Output**: Complete deliverable package

```
FINAL_V4_ARTICLE_PACKAGE/
├── README.md                  # Package documentation
├── article.html              # Complete article
├── research_results.json     # Research data
├── factcheck_report.json     # Quality scores
├── seo_metadata.json         # SEO data
└── images/                   # Generated images
    ├── hero_image.png
    ├── section_1_image.png
    └── ...
```

## Data Quality Assurance

### Validation Points
1. **Research Query Generation**: 15-25 queries required
2. **Batch Processing**: All 3 batches must complete
3. **Source Reliability**: Average score ≥ 80
4. **Citation Count**: Minimum 5 citations in article
5. **Fact-checking**: Overall quality score ≥ 85
6. **SEO Compliance**: All required metadata present

### Error Recovery
- Batch failure: Retry with reduced query count
- Low quality scores: Additional research round
- Missing citations: Automatic source integration
- Template compliance: Format validation and correction

### Performance Metrics
- Research completion time: ~15 minutes
- Source collection: 100-200 sources per article
- Citation integration: 5-10 citations per article
- Quality scores: Consistently above 85%