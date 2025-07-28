# GPT-Image-1 Implementation Guide

## Overview
GPT-Image-1 is OpenAI's latest image generation model, released in April 2025. It's a completely new model, NOT an alias for DALL-E 3, and offers significant improvements in quality and cost-effectiveness.

## Key Differences from DALL-E 3

### 1. **Response Format**
- **GPT-Image-1**: Always returns base64-encoded images (`b64_json`)
- **DALL-E 3**: Can return either URLs or base64
- **CRITICAL**: Do NOT include `response_format` parameter for gpt-image-1 - it will cause an error!

### 2. **Quality Options**
- **GPT-Image-1**: `"low"`, `"medium"`, `"high"`, or `"auto"`
- **DALL-E 3**: `"standard"` or `"hd"` 
- **Note**: Do not use `"standard"` or `"hd"` - these are DALL-E 3 values and invalid for gpt-image-1

### 3. **Size Options**
- **GPT-Image-1**: 
  - `"1024x1024"` (square)
  - `"1024x1536"` (portrait)
  - `"1536x1024"` (landscape)
- **DALL-E 3**: Has additional sizes like `"1792x1024"`, `"1024x1792"`

### 4. **Pricing**
- **GPT-Image-1**: $0.015 per standard 1024×1024 image (75% cheaper than DALL-E 3)
- **High quality**: 2x the cost of low quality

## Correct API Implementation

### Using OpenAI Python Library
```python
from openai import OpenAI
import base64

client = OpenAI()

result = client.images.generate(
    model="gpt-image-1",
    prompt="Your prompt here",
    n=1,
    size="1024x1024",
    quality="high"
    # NO response_format parameter!
)

# Always access as base64
image_b64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_b64)

# Save to file
with open("output.png", "wb") as f:
    f.write(image_bytes)
```

### Using Raw HTTP Requests
```python
import requests
import base64

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-image-1",
    "prompt": "Your prompt here",
    "n": 1,
    "size": "1024x1024",
    "quality": "high"
    # NO response_format parameter!
}

response = requests.post(
    "https://api.openai.com/v1/images/generations",
    headers=headers,
    json=data
)

if response.status_code == 200:
    result = response.json()
    image_b64 = result['data'][0]['b64_json']
    image_bytes = base64.b64decode(image_b64)
```

## Common Errors and Solutions

### Error: "Unknown parameter: 'response_format'"
**Cause**: Including the `response_format` parameter in the API call
**Solution**: Remove this parameter entirely - gpt-image-1 always returns base64

### Error: "Invalid quality value"
**Cause**: Using `"standard"` or `"hd"` as quality values (these are DALL-E 3 values)
**Solution**: Use only `"low"`, `"medium"`, `"high"`, or `"auto"`

### Error: "Invalid size"
**Cause**: Using unsupported size dimensions
**Solution**: Use only: `"1024x1024"`, `"1024x1536"`, or `"1536x1024"`

## Implementation Checklist

✅ **DO:**
- Use `model="gpt-image-1"`
- Use quality values: `"low"`, `"medium"`, `"high"`, or `"auto"`
- Use supported sizes only
- Always handle base64 response
- Include proper error handling
- Implement retry logic for rate limits

❌ **DON'T:**
- Include `response_format` parameter
- Expect URL responses
- Use `"standard"` or `"hd"` quality (these are DALL-E 3 values)
- Use DALL-E 3 specific sizes

## Test Script
Run the provided `test_gpt_image_1.py` script to verify your implementation:

```bash
export OPENAI_API_KEY="your-api-key"
python test_gpt_image_1.py
```

## Additional Notes

1. **Rate Limits**: Implement 12-second delays between requests to avoid rate limiting
2. **Timeouts**: Use 120-second timeouts for complex prompts
3. **Error Handling**: Always check for API errors and handle them gracefully
4. **Organization Verification**: Using gpt-image-1 requires organization verification on OpenAI platform

## Summary

The main issue causing the "Unknown parameter: 'response_format'" error is that gpt-image-1 doesn't support this parameter. The model always returns base64-encoded images, and attempting to specify a response format will cause the API to reject the request.

The implementation in `generate_images_gpt.py` has been corrected to:
1. Remove any `response_format` parameter
2. Handle base64 responses instead of URLs
3. Use correct quality values (`"low"`, `"medium"`, `"high"`, or `"auto"`)
4. Use only supported image sizes