# Deployment Guide

## GitHub Actions Setup

### Required Secrets
Configure these secrets in your GitHub repository settings:

```
ANTHROPIC_API_KEY=your_claude_api_key_here
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### Environment Configuration
- **Environment Name**: `GA` (GitHub Actions)
- **Required Reviewers**: Optional (for production protection)
- **Deployment Protection Rules**: Optional

### Repository Settings
- **Actions**: Enabled
- **Workflow Permissions**: Read and write permissions
- **Artifact Retention**: 30 days (configurable)

## Workflow Execution

### Manual Trigger
1. Go to **Actions** tab in GitHub
2. Select **"Article Generation V4 (Simplified Output)"**
3. Click **"Run workflow"**
4. Fill in required parameters:
   - **記事タイトル** (Article Title): Required
   - **ターゲットペルソナ** (Target Persona): Required
   - **メタキーワード** (Meta Keywords): Required, comma-separated
   - **目標文字数** (Word Count): Optional, default 3200
   - **画像生成を有効にする** (Enable Image Generation): Optional, default true

### Workflow Parameters Example
```
Article Title: "敏感肌向けハンドクリームの選び方完全ガイド"
Target Persona: "30代女性、敏感肌に悩む、忙しい働く母親"
Meta Keywords: "敏感肌,ハンドクリーム,選び方,おすすめ,保湿"
Word Count: 3200
Enable Images: true
```

## Monitoring & Debugging

### Workflow Status
- **Duration**: Typically 45-60 minutes for complete execution
- **Success Rate**: Monitor via GitHub Actions dashboard
- **Cost Tracking**: Monitor API usage in respective dashboards

### Common Issues & Solutions

#### Research Phase Failures
**Issue**: Gemini API rate limiting
**Solution**: 
- Reduce batch size from 3 to 2
- Increase timeout from 15 to 20 minutes
- Check API quota limits

#### Content Generation Failures
**Issue**: Claude API timeout
**Solution**:
- Increase max_turns from 15 to 20
- Split large prompts into smaller sections
- Check template file accessibility

#### Image Generation Failures
**Issue**: MCP server startup issues
**Solution**:
- Verify gemini-imagen-mcp-server package
- Check GEMINI_API_KEY configuration
- Ensure imagen-4 model access

#### Artifact Issues
**Issue**: Files not found between jobs
**Solution**:
- Check artifact upload/download patterns
- Verify file paths in workflow
- Review artifact naming consistency

### Log Analysis
Key log sections to monitor:
1. **Initialization**: Article ID generation
2. **Analysis**: Phase 1 output validation
3. **Research**: Batch completion status
4. **Content**: Article generation success
5. **Images**: MCP server startup and generation
6. **Finalization**: Package assembly

## Performance Optimization

### Speed Improvements
- **Parallel Processing**: Research runs in 3 concurrent batches
- **Efficient Prompts**: Optimized token usage
- **Smart Caching**: Reuse analysis across phases
- **Minimal Dependencies**: Reduced package installation time

### Cost Management
- **API Usage**: Monitor Claude and Gemini token consumption
- **Artifact Storage**: 30-day automatic cleanup
- **Image Generation**: Limit to 5 images per article
- **Research Queries**: Cap at 25 queries maximum

### Quality Assurance
- **Validation Points**: Built into each phase
- **Fallback Mechanisms**: Automatic error recovery
- **Quality Scoring**: Numerical quality metrics
- **Format Compliance**: Template validation

## Scaling Considerations

### Multiple Articles
- Each workflow run handles one article
- No batch processing of multiple articles
- Consider workflow_dispatch scheduling for bulk generation

### Team Usage
- Multiple team members can trigger workflows
- Unique article IDs prevent conflicts
- Shared artifact access via GitHub interface

### Production Deployment
- Use repository environments for staging/production
- Implement approval workflows for production runs
- Monitor API rate limits across team usage

## Maintenance

### Regular Tasks
- **Monthly**: Review API usage and costs
- **Quarterly**: Update dependencies in requirements.txt
- **Bi-annually**: Review and update prompt templates
- **Annually**: Audit security and access permissions

### Updates & Versioning
- **Workflow Updates**: Test in separate branch first
- **Prompt Changes**: Validate output format compatibility
- **Dependency Updates**: Test thoroughly before merging
- **API Changes**: Monitor provider changelog for breaking changes

### Backup & Recovery
- **Workflow Files**: Version controlled in Git
- **Artifacts**: Download important packages locally
- **Configuration**: Document all secret values securely
- **Templates**: Maintain backup copies of working templates

## Troubleshooting Checklist

### Pre-flight Checks
- [ ] All required secrets configured
- [ ] Repository permissions set correctly
- [ ] Workflow file syntax valid
- [ ] Template files accessible

### Runtime Checks
- [ ] Article ID generated successfully
- [ ] Phase 1 analysis completed
- [ ] Research batches all completed
- [ ] Article HTML generated
- [ ] Images generated (if enabled)
- [ ] Final package assembled

### Post-execution Checks
- [ ] All artifacts uploaded successfully
- [ ] Final package contains 5 required deliverables
- [ ] Quality scores meet thresholds
- [ ] Citations properly formatted
- [ ] Images properly integrated