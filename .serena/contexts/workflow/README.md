# Workflow Context

This context contains GitHub Actions workflow files and automation scripts for the article generation pipeline.

## Key Files

### GitHub Actions Workflows
- **article-generation-v4.yml**: Main production workflow with 10 jobs
  - Initialize → Analysis → Research → Merge → Structure → Content → Factcheck → SEO → Images → Finalize
  - Uses Claude Code Base Action for AI processing
  - Supports parallel research with Gemini API
  - Outputs 5 deliverables: HTML article, research results, factcheck report, SEO metadata, images

### Scripts Directory (github-actions/scripts/)
- **Phase 1**: `create_phase1_fallback.py`, `phase1_request_analysis.py`
- **Phase 2**: `research_batch_gemini.py`, `merge_research_results.py`
- **Image Generation**: `generate_images_imagen.py`, `generate_images_gemini.py`
- **Utilities**: File handling, logging, web search utilities

## Workflow Architecture

### Job Flow
1. **initialize**: Create article ID and setup
2. **analysis**: Parse request with Claude (Phase 1)
3. **research**: Parallel Gemini research (3 batches)
4. **research-merge**: Combine research results
5. **generate-structure**: Create article outline with Claude
6. **generate-content**: Write article content with Claude
7. **factcheck**: Quality check and fact verification
8. **generate-seo-meta**: SEO metadata generation
9. **generate-images**: MCP + Imagen4 image generation
10. **finalize**: Package final deliverables

### Environment Variables
- `ANTHROPIC_API_KEY`: Claude API access
- `GEMINI_API_KEY`: Google Gemini API access
- Environment: `GA` (GitHub Actions environment)

### Artifacts
Each job produces artifacts passed to subsequent jobs:
- `init-{article_id}`: Input parameters
- `analysis-{article_id}`: Phase 1 analysis results
- `research-batch-{N}-{article_id}`: Research batches
- `content-{article_id}`: Generated article
- `factcheck-{article_id}`: Quality reports
- `images-{article_id}`: Generated images
- `FINAL_V4_ARTICLE_PACKAGE`: Complete deliverable package