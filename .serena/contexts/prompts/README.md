# Prompts Context

This context contains all AI prompt files used in the article generation workflow phases.

## Workflow Phases

### Phase 0: Request Analysis
- **00_parse_request.md**: Original request parsing
- **00_parse_request_v3.md**: Enhanced request analysis with keyword extraction

### Phase 1: Research & Investigation  
- **01_research.md**: Web research and competitive analysis
- Research is now handled by Gemini API in parallel batches (3 concurrent)

### Phase 2: Structure Planning
- **02_structure.md**: Article outline and content planning
- **03_structure.md**: Alternative structure planning approach

### Phase 3: Content Writing
- **03_writing.md**: Basic article writing
- **04_writing.md**: Enhanced writing with SEO focus
- **04_writing_v4.md**: Latest writing approach
- **04_writing_v4_html.md**: HTML-focused writing
- **04_writing_v4_html_updated.md**: ✅ **CURRENT PRODUCTION VERSION**

### Phase 4: Quality Assurance
- **03_5_factcheck.md**: Fact-checking and verification
- **05_factcheck.md**: Alternative fact-checking approach

### Phase 5: Optimization
- **04_optimization.md**: SEO and content optimization
- **04_optimization_v2.md**: Enhanced optimization with LLMO
- **06_seo.md**: SEO-specific metadata generation

### Phase 6: Image Generation
- **04_5_image_generation.md**: Traditional image generation
- **08_image_generation_mcp.md**: MCP-based image generation
- **image_generation_mcp.md**: MCP image generation reference

### Phase 7: Finalization
- **05_finalization.md**: Final review and packaging
- **07_final.md**: Final output preparation

## Current Production Workflow (V4)

### Active Prompts
1. **Request Analysis**: Embedded in workflow YAML (inline prompt)
2. **Structure Planning**: Embedded in workflow YAML (inline prompt)  
3. **Content Writing**: `04_writing_v4_html_updated.md`
4. **Fact-checking**: Embedded in workflow YAML (inline prompt)
5. **SEO Metadata**: Embedded in workflow YAML (inline prompt)
6. **Image Generation**: Embedded in workflow YAML (inline prompt)
7. **Finalization**: Embedded in workflow YAML (inline prompt)

### Key Features of Current Prompts
- **Template Integration**: All prompts reference sample files
- **Citation Requirements**: Minimum 5 sources with proper attribution
- **HTML Output**: Structured output with specific CSS classes
- **Quality Metrics**: Built-in quality scoring and validation
- **Persona Optimization**: Target audience adaptation
- **Multi-language Support**: Japanese content generation

## Prompt Variables

### Standard Environment Variables
- `ARTICLE_ID`: Unique identifier for current article
- `TITLE`: Article title from user input
- `TARGET_PERSONA`: Target audience description
- `WORD_COUNT`: Target word count (default: 3200)
- `WORKSPACE`: GitHub Actions workspace path

### File References
- Input files: `input_params.json`, `phase1_output.json`
- Research data: `research_results.json`
- Structure files: `01_article_structure.md`, `02_content_plan.md`
- Template files: `sample/articles/` directory
- Output files: Various JSON and HTML outputs

## Usage Guidelines

### For Workflow Maintenance
- Test prompt changes in separate workflow files first
- Validate output format compatibility
- Ensure all required files are referenced
- Check token limits and complexity

### For Content Quality
- Maintain citation requirements (minimum 5 sources)
- Enforce HTML structure compliance
- Preserve accessibility standards
- Validate persona targeting effectiveness

### For Performance
- Optimize prompt length vs. detail balance
- Monitor Claude API usage and costs
- Track generation success rates
- Measure output quality consistency