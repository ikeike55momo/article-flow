# Complete Migration Plan: From Python Scripts to MCP + Imagen4

## Executive Summary

This document provides a comprehensive migration plan to replace the current Python-based image generation system with a Claude Code + MCP + Imagen4 solution. This migration will eliminate Python dependencies, reduce costs, and provide better integration with the existing workflow.

## Current State Analysis

### 1. Existing Implementation
- **Current Tools**: 
  - `generate_images_gpt.py` - Uses OpenAI gpt-image-1 ($0.04/image)
  - `generate_images_imagen.py` - Direct Vertex AI access (403 errors - not allowlisted)
- **Dependencies**: Python 3.11, multiple Python packages, Google Cloud SDK
- **Output Structure**: `output/ARTICLE_ID/images/` with `images_metadata.json`

### 2. Pain Points
- High cost with gpt-image-1 ($0.04/image × 5 images = $0.20 per article)
- Direct Imagen access requires allowlisting
- Complex Python environment setup
- Separate authentication for different services

### 3. MCP + Imagen4 Advantages
- Access Imagen4 through Gemini API without allowlisting
- No Python dependencies
- Native integration with Claude Code
- Better context understanding from article content
- Cost-effective (Gemini API pricing)

## Migration Architecture

### 1. New Workflow Design
```yaml
generate-images:
  if: ${{ inputs.enable_image_generation }}
  needs: [initialize-and-analyze, structure-and-write]
  runs-on: ubuntu-latest
  environment: GA
  timeout-minutes: 20
  
  steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Download artifacts
      uses: actions/download-artifact@v4
      with:
        pattern: phase*-${{ needs.initialize-and-analyze.outputs.article_id }}
        path: output/${{ needs.initialize-and-analyze.outputs.article_id }}
        merge-multiple: true

    - name: Generate Images with MCP + Imagen4
      uses: anthropics/claude-code-base-action@beta
      with:
        anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
        prompt_file: prompts/image_generation_mcp.md
        allowed_tools: "View,Write,WebSearch,mcp__gemini__generate_image"
        claude_env: |
          ARTICLE_ID=${{ needs.initialize-and-analyze.outputs.article_id }}
          TOPIC=${{ inputs.topic }}
          GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}
        max_turns: "15"

    - name: Upload image artifacts
      uses: actions/upload-artifact@v4
      with:
        name: images-${{ needs.initialize-and-analyze.outputs.article_id }}
        path: output/${{ needs.initialize-and-analyze.outputs.article_id }}/images
        retention-days: 30
```

### 2. New Prompt File Structure
Create `prompts/image_generation_mcp.md`:

```markdown
# Image Generation Phase using MCP + Imagen4

## Task Overview
Generate contextually appropriate images for the article using Gemini's Imagen4 model through MCP.

## Input Files
- Article HTML: output/$ARTICLE_ID/04_optimized_draft.html
- Article Structure: output/$ARTICLE_ID/phase3_structure.json
- Analysis Data: output/$ARTICLE_ID/phase1_analysis.json

## Output Requirements
1. Generate 5 images total:
   - 1 hero image (16:9 aspect ratio)
   - 4 section images (4:3 aspect ratio)

2. Save images to: output/$ARTICLE_ID/images/
   - hero.png
   - section-1.png
   - section-2.png
   - section-3.png
   - section-4.png

3. Create metadata file: output/$ARTICLE_ID/images/images_metadata.json

## Image Generation Process

### Step 1: Read and Analyze Article Content
1. Read the optimized HTML draft
2. Extract main topic and key sections
3. Identify visual concepts for each section

### Step 2: Generate Images Using MCP
For each required image:
1. Create a detailed, contextual prompt based on article content
2. Use mcp__gemini__generate_image with Imagen4
3. Save the generated image
4. Handle errors gracefully with retry logic

### Step 3: Create Metadata
Generate a JSON file with:
- Image filenames and paths
- Alt text for accessibility
- Generation parameters
- Timestamps

## Prompt Engineering Guidelines
1. **Hero Image**: Professional, modern, health/wellness focused
2. **Section Images**: Informative, clean, relevant to section content
3. **Style**: Consistent visual language across all images
4. **Safety**: Avoid medical claims, use general wellness imagery

## Error Handling
- Retry failed generations up to 3 times
- If generation fails, create placeholder entry in metadata
- Log all errors for debugging

## Quality Assurance
- Verify all images are saved correctly
- Ensure metadata is complete and valid JSON
- Check file sizes are reasonable (<5MB per image)
```

### 3. Implementation Details

#### 3.1 MCP Configuration
Add to `.claude/mcp_settings.json`:
```json
{
  "mcpServers": {
    "gemini": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gemini"],
      "env": {
        "GEMINI_API_KEY": "${GEMINI_API_KEY}"
      }
    }
  }
}
```

#### 3.2 Image Generation Logic
The Claude Code implementation will:
1. Parse article content to understand context
2. Generate appropriate prompts for each image
3. Call Imagen4 through MCP's Gemini integration
4. Save images with proper naming convention
5. Create compatible metadata structure

## Step-by-Step Migration Plan

### Phase 1: Preparation (Day 1)
1. **Backup Current System**
   - Create branch: `backup/pre-imagen4-migration`
   - Document current image generation metrics

2. **Environment Setup**
   - Verify GEMINI_API_KEY is set in GitHub Secrets
   - Test MCP Gemini server locally
   - Confirm Imagen4 access through Gemini API

### Phase 2: Implementation (Day 2-3)
1. **Create New Workflow Components**
   - Create `prompts/image_generation_mcp.md`
   - Update workflow file with new job configuration
   - Remove Python dependencies from requirements

2. **Parallel Testing**
   - Keep old job disabled but not deleted
   - Run new job in test mode
   - Compare outputs with existing system

### Phase 3: Validation (Day 4)
1. **Quality Checks**
   - Verify image quality meets standards
   - Confirm metadata compatibility
   - Test downstream processes

2. **Performance Testing**
   - Measure generation time
   - Check rate limits and quotas
   - Validate error handling

### Phase 4: Rollout (Day 5)
1. **Gradual Migration**
   - Enable for 10% of workflows
   - Monitor for issues
   - Increase to 100% if stable

2. **Cleanup**
   - Remove Python image generation scripts
   - Update documentation
   - Archive old implementation

## Testing Strategy

### 1. Unit Tests
- Test prompt generation logic
- Verify metadata structure
- Validate image saving

### 2. Integration Tests
```yaml
test-image-generation:
  runs-on: ubuntu-latest
  steps:
    - name: Test MCP Image Generation
      run: |
        # Create test article content
        mkdir -p output/test_article
        echo "<h1>Test Article</h1><h2>Section 1</h2>" > output/test_article/04_optimized_draft.html
        
        # Run image generation
        # Verify outputs exist
        test -f output/test_article/images/hero.png
        test -f output/test_article/images/images_metadata.json
```

### 3. End-to-End Tests
- Run full pipeline with test articles
- Verify image integration in final output
- Check Google Drive upload compatibility

## Rollback Plan

### Immediate Rollback (< 1 hour)
1. Revert workflow file to previous version
2. Re-enable Python scripts
3. Notify team of rollback

### Gradual Rollback
1. Switch back to Python implementation for new runs
2. Keep MCP-generated images for existing articles
3. Investigate and fix issues
4. Re-attempt migration

### Rollback Triggers
- Image generation success rate < 80%
- Generation time > 5 minutes per image
- Critical errors in production
- Quality degradation

## Success Metrics

### 1. Cost Reduction
- Target: 80% reduction in image generation costs
- Metric: Cost per article for images

### 2. Performance
- Target: < 3 minutes for 5 images
- Metric: Average generation time

### 3. Quality
- Target: 95% acceptance rate
- Metric: Manual review scores

### 4. Reliability
- Target: 99% success rate
- Metric: Failed generations / total attempts

## Risk Mitigation

### 1. Technical Risks
- **Risk**: MCP service unavailability
- **Mitigation**: Implement retry logic, fallback to placeholders

### 2. Quality Risks
- **Risk**: Lower image quality than gpt-image-1
- **Mitigation**: A/B testing, quality thresholds

### 3. Operational Risks
- **Risk**: Rate limits on Gemini API
- **Mitigation**: Implement rate limiting, queue management

## Timeline

- **Week 1**: Preparation and implementation
- **Week 2**: Testing and validation
- **Week 3**: Gradual rollout
- **Week 4**: Full migration and cleanup

## Conclusion

This migration plan provides a comprehensive approach to transitioning from expensive Python-based image generation to a cost-effective MCP + Imagen4 solution. The plan minimizes risk through gradual rollout, comprehensive testing, and clear rollback procedures while maintaining backward compatibility with existing systems.