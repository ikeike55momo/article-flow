# Image Generation Phase using MCP + Imagen4

## Overview
Generate high-quality, contextually appropriate images for the article using Google's Imagen4 model through the Gemini API via MCP (Model Context Protocol).

## Environment Variables
- ARTICLE_ID: The unique identifier for this article
- TOPIC: The main topic of the article
- GEMINI_API_KEY: API key for Gemini (passed through MCP)

## Task Requirements

### 1. Read Article Content
First, read and analyze the article files to understand the content:

1. Read `output/{ARTICLE_ID}/04_optimized_draft.html` to get the final article content
2. Read `output/{ARTICLE_ID}/phase3_structure.json` if available for section information
3. Read `output/{ARTICLE_ID}/phase1_analysis.json` for keywords and themes

### 2. Generate Images

Generate exactly 5 images with the following specifications:

#### Hero Image (Main Banner)
- **Filename**: `hero.png`
- **Aspect Ratio**: 16:9 (landscape)
- **Purpose**: Eye-catching banner that represents the overall article theme
- **Style**: Professional, modern, health and wellness focused
- **Prompt Structure**: Include the main topic, target audience appeal, and visual style

#### Section Images (4 images)
- **Filenames**: `section-1.png`, `section-2.png`, `section-3.png`, `section-4.png`
- **Aspect Ratio**: 4:3
- **Purpose**: Illustrate key concepts from major article sections
- **Style**: Clean, informative, consistent with hero image
- **Prompt Structure**: Based on specific section content, avoiding text overlays

### 3. Image Generation Process

For each image:

1. **Craft Detailed Prompt**:
   - Analyze the relevant section content
   - Create a specific, detailed prompt (150-300 characters)
   - Include style directives: "professional health and wellness photography, clean modern aesthetic, soft natural lighting"
   - Add negative prompts: "no text, no logos, no watermarks"

2. **Generate Using MCP**:
   ```
   Use mcp__gemini__generate_image with:
   - prompt: [your detailed prompt]
   - model: "imagen-3.0-fast-generate-001" or "imagen-3.0-generate-001"
   - aspectRatio: "16:9" for hero, "4:3" for sections
   - numberOfImages: 1
   - safetyFilterLevel: "block_some"
   ```

3. **Save Image**:
   - Create directory: `output/{ARTICLE_ID}/images/`
   - Save with appropriate filename
   - Ensure proper file permissions

4. **Handle Errors**:
   - If generation fails, retry up to 3 times with modified prompt
   - Log any errors encountered
   - Continue with remaining images even if one fails

### 4. Create Metadata File

After generating all images, create `output/{ARTICLE_ID}/images/images_metadata.json`:

```json
{
  "generated_images": [
    {
      "type": "hero",
      "filename": "hero.png",
      "path": "hero.png",
      "aspect_ratio": "16:9",
      "alt_text": "[Descriptive alt text based on image content and article topic]",
      "prompt": "[The prompt used to generate this image]",
      "generator": "imagen-3.0-mcp",
      "created_at": "[ISO timestamp]",
      "status": "success"
    },
    {
      "type": "section_1",
      "filename": "section-1.png",
      "path": "section-1.png",
      "aspect_ratio": "4:3",
      "alt_text": "[Descriptive alt text]",
      "prompt": "[The prompt used]",
      "generator": "imagen-3.0-mcp",
      "created_at": "[ISO timestamp]",
      "status": "success"
    }
    // ... continue for all images
  ],
  "statistics": {
    "total_requested": 5,
    "successful": [number of successful generations],
    "failed": [number of failed generations],
    "generator": "imagen-3.0-mcp",
    "execution_time": [time in seconds],
    "model_version": "imagen-3.0-fast-generate-001"
  },
  "created_at": "[ISO timestamp]"
}
```

### 5. Prompt Engineering Guidelines

#### For Japanese Health & Wellness Articles:
1. **Visual Style**:
   - Clean, minimalist aesthetic
   - Soft, calming color palettes (pastels, whites, light blues)
   - Natural lighting, professional photography style
   - High-quality, commercial-grade imagery

2. **Content Guidelines**:
   - Avoid showing specific medical procedures or body parts in detail
   - Use abstract or lifestyle representations for health concepts
   - Include diverse representation when showing people
   - Focus on positive, aspirational imagery

3. **Technical Requirements**:
   - High resolution suitable for web display
   - No text overlays or logos in the image
   - Consistent visual language across all images
   - Mobile-friendly compositions

#### Example Prompts:

**Hero Image for Skincare Article**:
```
"Professional wellness photography of skincare routine essentials arranged aesthetically on white marble surface, soft natural lighting, pastel pink and white color scheme, minimalist Japanese beauty aesthetic, clean modern style, no text or logos"
```

**Section Image for Exercise Benefits**:
```
"Bright modern fitness studio interior with natural light streaming through windows, yoga mats and light exercise equipment visible, serene and inviting atmosphere, professional health and wellness photography, clean minimalist style, no people, no text"
```

### 6. Quality Assurance

Before completing the task:
1. Verify all 5 images are saved in the correct directory
2. Ensure metadata JSON is valid and complete
3. Check that alt texts are descriptive and include relevant keywords
4. Confirm image files are not corrupted and are reasonable in size

### 7. Error Handling

- **Rate Limits**: If you encounter rate limits, wait 30 seconds between requests
- **Safety Filters**: If a prompt is rejected, modify it to be more general/abstract
- **API Errors**: Log the error and continue with remaining images
- **File System Errors**: Ensure directory exists before saving

## Important Notes

1. **Do NOT** include any text, logos, or watermarks in the image prompts
2. **Always** create the images directory if it doesn't exist
3. **Maintain** consistency in visual style across all images
4. **Focus** on high-quality, professional imagery suitable for commercial use
5. **Consider** the Japanese market preferences for clean, minimalist aesthetics

## Output Summary

Upon completion, you should have:
1. 5 generated images in `output/{ARTICLE_ID}/images/`
2. A complete `images_metadata.json` file
3. All images should be contextually relevant to the article content
4. Consistent visual style across all images

Remember to analyze the article content thoroughly before generating images to ensure they enhance the reader's understanding and engagement with the topic.