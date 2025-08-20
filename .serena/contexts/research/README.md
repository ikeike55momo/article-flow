# Research Context

This context manages research data, source validation, and output data flow for the article generation pipeline.

## Research Architecture

### Research Pipeline (V4)
1. **Request Analysis** → Extract research queries (15-25 queries)
2. **Query Splitting** → Divide into 3 parallel batches
3. **Gemini Research** → Concurrent web research via Gemini API
4. **Results Merging** → Combine batch results with reliability scoring
5. **Fact-checking** → Validate research against generated content

### Key Components

#### Research Data Flow
```
Input → Analysis → Query Generation → Batch Processing → Merge → Validation
```

#### File Structure
```
output/{ARTICLE_ID}/
├── phase1_output.json          # Analysis with research queries
├── research_meta.json          # Research metadata
├── batch_0/                    # Research batch 0
│   ├── queries.json
│   └── results.json
├── batch_1/                    # Research batch 1
├── batch_2/                    # Research batch 2
├── research_results.json       # Merged final results
└── factcheck_report.json       # Quality validation
```

## Research Sources & Reliability

### Source Categories
1. **Primary Sources** (Reliability: 90-100%)
   - Government health agencies
   - Medical journals and studies
   - Professional associations
   - Clinical research institutions

2. **Secondary Sources** (Reliability: 70-90%)
   - Established health websites
   - Expert-authored articles
   - Peer-reviewed publications
   - Industry reports

3. **Supporting Sources** (Reliability: 50-70%)
   - News articles with expert quotes
   - Professional blogs
   - Educational institutions
   - Verified social media content

### Quality Scoring System
```json
{
  "overall_quality_score": 85,
  "fact_accuracy_score": 90,
  "legal_compliance_score": 95,
  "scientific_validity_score": 80,
  "source_reliability_score": 85
}
```

## Research Scripts

### Core Research Scripts
- **research_batch_gemini.py**: Parallel Gemini API research
- **merge_research_results.py**: Combine and score research batches
- **split_research_queries.py**: Divide queries into batches
- **create_batch_analysis.py**: Prepare batch-specific analysis

### Research Query Types
1. **Factual Queries**: "What are the benefits of X?"
2. **Statistical Queries**: "How many people experience Y?"
3. **Comparative Queries**: "X vs Y effectiveness"
4. **Safety Queries**: "Side effects of Z"
5. **Expert Opinion**: "Dermatologist recommendations for..."
6. **Recent Studies**: "Latest research on..."

## Output Data Management

### Deliverable Files (V4)
1. **research_results.json**: Complete research data with sources
2. **factcheck_report.json**: Quality scores and validation
3. **seo_metadata.json**: SEO-optimized metadata
4. **final_article.html**: Complete article with citations
5. **images/**: Generated article images

### Data Retention
- **GitHub Artifacts**: 30 days automatic retention
- **Final Package**: `FINAL_V4_ARTICLE_PACKAGE` artifact
- **Development**: Local `output/` directory for testing

### Quality Metrics
- **Citation Count**: Minimum 5 reliable sources required
- **Fact Accuracy**: 90%+ accuracy threshold
- **Legal Compliance**: 95%+ for health/beauty content
- **Source Diversity**: Multiple source types required
- **Recency**: Prefer sources within 3 years

## Research Configuration

### Gemini API Settings
- Model: `gemini-2.5-flash`
- Batch Size: 3 parallel batches
- Rate Limiting: Managed automatically
- Timeout: 15 minutes per batch

### Search Parameters
- Query Count: 15-25 queries per article
- Batch Division: Even distribution across 3 batches
- Source Validation: Automatic reliability scoring
- Fact-checking: Cross-reference with generated content

### Error Handling
- Batch failure recovery
- Source validation fallbacks
- Research timeout handling
- Quality threshold enforcement

## Usage Guidelines

### For Content Creators
- Research results provide factual foundation
- Citations must link to original sources
- Quality scores indicate content reliability
- Recent sources preferred for trending topics

### For Developers
- Research pipeline is fully automated
- Monitor Gemini API usage and costs
- Validate research result format compliance
- Ensure proper source attribution in output

### For Quality Assurance
- Review fact-checking scores before publication
- Verify source URLs are accessible
- Check legal compliance for health content
- Validate citation format and numbering