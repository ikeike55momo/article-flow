# Workflow Files Reference

## GitHub Actions Workflows

### Main Workflow: article-generation-v4.yml
- **Location**: `.github/workflows/article-generation-v4.yml`
- **Purpose**: Complete article generation pipeline
- **Inputs**:
  - `article_title`: Article title (required)
  - `target_persona`: Target audience description (required)
  - `meta_keywords`: SEO keywords, comma-separated (required)
  - `word_count`: Target word count (default: 3200)
  - `enable_image_generation`: Enable/disable images (default: true)

### Test Workflows
- `test-mcp-imagen4.yml`: Image generation testing
- `test-seo-only.yml`: SEO metadata testing
- `test-v4-factcheck-seo.yml`: Factcheck and SEO testing
- `article-generation-v2.yml`, `article-generation-v3.yml`: Legacy versions

## Script Dependencies

### Python Requirements (github-actions/requirements.txt)
```
requests>=2.31.0
python-dotenv>=1.0.0
google-genai>=0.3.0
beautifulsoup4>=4.12.0
anthropic>=0.7.0
```

### Package.json (Node.js dependencies)
```json
{
  "dependencies": {
    "gemini-imagen-mcp-server": "latest"
  }
}
```

## Environment Setup
- Python 3.11
- Ubuntu latest runner
- 30-day artifact retention
- Timeout limits: 5-20 minutes per job

## Security Considerations
- All API keys stored in GitHub Secrets
- No sensitive data in logs
- Artifacts automatically expire after 30 days
- External API rate limiting respected