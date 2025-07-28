# MCP + Imagen4 Setup Validation Guide

## Pre-Migration Testing Checklist

### 1. Local Environment Testing

#### Step 1: Install MCP Gemini Server
```bash
# Test MCP Gemini server installation
npx -y @modelcontextprotocol/server-gemini --version

# If not installed, install globally
npm install -g @modelcontextprotocol/server-gemini
```

#### Step 2: Test Gemini API Access
```bash
# Set your API key
export GEMINI_API_KEY="your-gemini-api-key"

# Test basic Gemini API access
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{
        "text": "Hello, Gemini!"
      }]
    }]
  }'
```

#### Step 3: Test Imagen4 Access via Gemini
Create `test_imagen4.py`:
```python
import google.generativeai as genai
import os

# Configure API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Test Imagen access
model = genai.GenerativeModel('gemini-1.5-flash')

# Try to generate with Imagen
response = model.generate_content(
    "Generate an image of a serene Japanese garden",
    generation_config=genai.GenerationConfig(
        temperature=1.0,
    )
)

print("Gemini API works:", response.text[:100])
```

### 2. GitHub Actions Testing

#### Create Test Workflow
Create `.github/workflows/test-mcp-imagen.yml`:
```yaml
name: Test MCP Imagen4 Setup

on:
  workflow_dispatch:

jobs:
  test-mcp-setup:
    runs-on: ubuntu-latest
    environment: GA
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Create test article structure
        run: |
          mkdir -p output/test_article_001
          
          # Create test HTML content
          cat > output/test_article_001/04_optimized_draft.html << 'EOF'
          <!DOCTYPE html>
          <html lang="ja">
          <head>
              <title>健康的なライフスタイルの始め方</title>
          </head>
          <body>
              <h1>健康的なライフスタイルの始め方</h1>
              
              <h2>はじめに</h2>
              <p>健康的な生活習慣を身につけることは、長期的な健康維持に重要です。</p>
              
              <h2>バランスの取れた食事</h2>
              <p>栄養バランスを考えた食事は健康の基本です。</p>
              
              <h2>適度な運動</h2>
              <p>毎日30分の運動が推奨されています。</p>
              
              <h2>十分な睡眠</h2>
              <p>質の良い睡眠は心身の回復に不可欠です。</p>
              
              <h2>ストレス管理</h2>
              <p>適切なストレス管理が重要です。</p>
          </body>
          </html>
          EOF
          
          # Create test structure JSON
          cat > output/test_article_001/phase3_structure.json << 'EOF'
          {
            "sections": [
              {"title": "はじめに", "content": "Introduction to healthy lifestyle"},
              {"title": "バランスの取れた食事", "content": "Balanced nutrition"},
              {"title": "適度な運動", "content": "Regular exercise"},
              {"title": "十分な睡眠", "content": "Quality sleep"},
              {"title": "ストレス管理", "content": "Stress management"}
            ]
          }
          EOF

      - name: Test MCP Image Generation
        uses: anthropics/claude-code-base-action@beta
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Test the MCP Imagen4 setup by generating a single test image.
            
            1. Use mcp__gemini__generate_image to create one test image
            2. Save it as output/test_article_001/images/test.png
            3. Create a simple metadata file
            
            This is just a test - generate one image with the prompt:
            "Professional health and wellness photography, serene spa setting with natural elements, soft lighting, minimalist style"
            
            Report any errors encountered.
          allowed_tools: "View,Write,mcp__gemini__generate_image"
          claude_env: |
            GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}
          max_turns: "5"
          mcp_servers: |
            {
              "gemini": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-gemini"],
                "env": {
                  "GEMINI_API_KEY": "${{ secrets.GEMINI_API_KEY }}"
                }
              }
            }

      - name: Check test results
        run: |
          echo "Checking test results..."
          if [ -f "output/test_article_001/images/test.png" ]; then
            echo "✓ Test image generated successfully!"
            ls -la output/test_article_001/images/
          else
            echo "✗ Test image not found"
            exit 1
          fi
```

### 3. Manual Testing Commands

#### Test via Claude CLI (if available locally)
```bash
# Set up environment
export ANTHROPIC_API_KEY="your-anthropic-api-key"
export GEMINI_API_KEY="your-gemini-api-key"

# Create test directory
mkdir -p test_output/images

# Run Claude with MCP
claude --mcp-server gemini="npx -y @modelcontextprotocol/server-gemini" \
  "Generate a test image using mcp__gemini__generate_image with prompt 'peaceful zen garden' and save to test_output/images/test.png"
```

### 4. Validation Checklist

Before proceeding with migration, ensure:

- [ ] GEMINI_API_KEY is set in GitHub Secrets
- [ ] Test workflow runs successfully
- [ ] MCP server can be installed via npx
- [ ] Imagen4 generates images without errors
- [ ] Generated images meet quality standards
- [ ] Metadata format is compatible
- [ ] Error handling works correctly

### 5. Performance Benchmarks

Track these metrics during testing:

1. **Image Generation Time**
   - Target: < 30 seconds per image
   - Acceptable: < 60 seconds per image

2. **Success Rate**
   - Target: > 95%
   - Minimum: > 80%

3. **Image Quality**
   - Resolution: Appropriate for web
   - Style: Consistent with prompts
   - Safety: No inappropriate content

### 6. Troubleshooting Guide

#### Common Issues and Solutions

**Issue**: MCP server not found
```bash
# Solution: Install globally
npm install -g @modelcontextprotocol/server-gemini
```

**Issue**: Gemini API authentication fails
```bash
# Check API key
echo $GEMINI_API_KEY
# Verify key is valid in Google Cloud Console
```

**Issue**: Imagen4 not available
```text
Solution: Imagen4 should be available through Gemini API.
If not working, check:
1. API key has necessary permissions
2. Using correct model endpoint
3. Region restrictions
```

**Issue**: Rate limits
```text
Solution: Implement delays between requests:
- Add 5-10 second delays between images
- Use exponential backoff for retries
```

### 7. Rollback Testing

Test the rollback procedure:

1. **Simulate Failure**
   - Disable MCP in workflow
   - Verify Python fallback works

2. **Quick Switch**
   - Have both implementations ready
   - Test switching between them

3. **Data Compatibility**
   - Ensure metadata formats match
   - Verify downstream processes work

### 8. Success Criteria

The setup is ready for production when:

1. ✓ All test images generate successfully
2. ✓ Generation time is under 3 minutes for 5 images
3. ✓ Error rate is below 5%
4. ✓ Image quality meets standards
5. ✓ Rollback procedure is tested
6. ✓ Monitoring is in place

## Next Steps

Once all tests pass:

1. Schedule migration during low-traffic period
2. Notify team of upcoming changes
3. Prepare rollback plan
4. Execute migration following the main plan
5. Monitor closely for 24 hours post-migration