# Migration Guide: Fixing GPT-Image-1 Implementation

## Quick Fix Summary

The error "Unknown parameter: 'response_format'" occurs because gpt-image-1 doesn't support this parameter. Here's what needs to be changed:

## Changes Made to `generate_images_gpt.py`

### 1. **Response Handling** (Lines 62-72)
**Before:**
```python
# Get image URL and download it
image_url = result['data'][0]['url']
# Download the image
image_response = requests.get(image_url, timeout=30)
image_data = image_response.content
```

**After:**
```python
# gpt-image-1 returns base64 data, NOT URLs
image_b64 = result['data'][0]['b64_json']
# Decode base64 to binary image data
import base64
image_data = base64.b64decode(image_b64)
```

### 2. **Quality Parameter Default** (Line 36)
**Before:**
```python
quality: str = "medium"
```

**After:**
```python
quality: str = "high"
```

### 3. **Size Mappings** (Lines 98-109)
**Before:**
```python
"16:9": "1792x1024",
"9:16": "1024x1792",
```

**After:**
```python
"16:9": "1536x1024",  # Closest supported size
"9:16": "1024x1536",  # Closest supported size
```

### 4. **API Parameters** (Lines 46-52)
**Before (if you had it):**
```python
data = {
    "model": "gpt-image-1",
    "prompt": prompt,
    "n": 1,
    "size": size,
    "quality": quality,
    "response_format": "url"  # This causes the error!
}
```

**After:**
```python
data = {
    "model": "gpt-image-1",
    "prompt": prompt,
    "n": 1,
    "size": size,
    "quality": quality  # No response_format!
}
```

## Testing the Fix

1. **Set your API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Run the test script:**
   ```bash
   python test_gpt_image_1.py
   ```

3. **Run the main script:**
   ```bash
   python github-actions/scripts/generate_images_gpt.py \
     --article-dir ./articles \
     --output-dir ./output \
     --quality high
   ```

## Troubleshooting

### If you still get the "response_format" error:
1. Check if you have any custom code that adds this parameter
2. Ensure you're not using an outdated OpenAI library that adds it automatically
3. Check environment variables or config files for this parameter

### If you get "Invalid quality" errors:
- Change any "medium" to "standard"
- Change any "high" to "hd"

### If you get "Invalid size" errors:
- Use only: "1024x1024", "1024x1536", or "1536x1024"

## Key Takeaways

1. **gpt-image-1 ≠ DALL-E 3** - They have different APIs
2. **No response_format** - Always returns base64
3. **Different parameters** - Quality and size options differ
4. **Handle base64** - No URL downloading needed

## Need More Help?

- Check `GPT_IMAGE_1_IMPLEMENTATION_GUIDE.md` for detailed documentation
- Run `test_gpt_image_1.py` to verify your setup
- Review the corrected `generate_images_gpt.py` implementation