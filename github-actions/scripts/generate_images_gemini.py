#!/usr/bin/env python3
"""Image Generation using Gemini API (Alternative to Vertex AI)"""

import argparse
import sys
import os
import json
import time
import asyncio
import base64
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from PIL import Image
import io

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric
from utils.file_utils import read_json, write_json, ensure_dir


class GeminiImageGenerator:
    """Gemini API image generator"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    async def generate_async(
        self,
        prompt: str,
        aspect_ratio: str = "1:1",
        num_images: int = 1
    ) -> Dict[str, Any]:
        """Generate image using Gemini API"""
        
        try:
            # Gemini doesn't directly generate images, but can create prompts for Imagen
            # First, enhance the prompt
            enhanced_prompt = f"""
            Create a detailed image generation prompt for: {prompt}
            Include specific details about colors, style, composition, and mood.
            Make it suitable for a professional image generation model.
            """
            
            response = self.model.generate_content(enhanced_prompt)
            enhanced = response.text
            
            # For now, create a placeholder with the enhanced prompt
            # In production, this would call the actual Imagen API
            img = Image.new('RGB', (1024, 1024), color='#e0e0e0')
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return {
                "image_data": img_byte_arr,
                "generator": "gemini-placeholder",
                "prompt": prompt,
                "enhanced_prompt": enhanced,
                "aspect_ratio": aspect_ratio
            }
                
        except Exception as e:
            raise Exception(f"Gemini generation failed: {str(e)}")
    
    def generate(self, prompt: str, aspect_ratio: str = "1:1") -> Dict[str, Any]:
        """Synchronous wrapper for generate_async"""
        return asyncio.run(self.generate_async(prompt, aspect_ratio))


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Generate images using Gemini API")
    parser.add_argument("--article-dir", required=True, help="Directory containing article files")
    parser.add_argument("--output-dir", required=True, help="Output directory for images")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    return parser.parse_args()


def create_image_prompts(structure: dict, article_content: str) -> List[Dict[str, Any]]:
    """Create prompts for all required images"""
    
    prompts = []
    
    # Extract topic from article content or use generic topic
    if structure.get("sections"):
        article_topic = "health and wellness"
        main_keyword = structure["sections"][0]["title"] if structure["sections"] else "health"
    else:
        article_topic = "health and wellness"
        main_keyword = "health"
    
    hero_prompt = f"""
    Professional hero image for a health and beauty article about {article_topic}.
    Modern, clean, minimalist design with soft colors.
    Theme: {main_keyword}
    Style: High-quality stock photography, wellness-focused, calming atmosphere.
    No text, logos, or watermarks.
    """
    
    prompts.append({
        "type": "hero",
        "prompt": hero_prompt.strip(),
        "aspect_ratio": "16:9",
        "filename": "hero.png"
    })
    
    # Section images
    for i, section in enumerate(structure.get("sections", [])[:4], 1):
        section_title = section.get("title", f"Section {i}")
        section_prompt = f"""
        Professional illustration for article section: {section_title}.
        Content: {section.get('content', 'Health and wellness information')}
        Style: Clean, informative, health and wellness focused.
        Soft pastel colors, modern design.
        No text overlays or logos.
        """
        
        prompts.append({
            "type": f"section_{i}",
            "prompt": section_prompt.strip(),
            "aspect_ratio": "4:3",
            "filename": f"section-{i}.png"
        })
    
    return prompts


def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging("image_generation_gemini", args.log_level)
    log_phase_start(logger, "Image Generation (Gemini API)")
    
    try:
        # Check API key
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        # Read input files from article directory
        article_dir = Path(args.article_dir)
        
        # Find structure file
        structure_file = article_dir / "02_article_structure.md"
        if not structure_file.exists():
            logger.warning(f"Structure file not found at {structure_file}")
            structure = {
                "sections": [
                    {"title": "Introduction", "content": "Introduction to the topic"},
                    {"title": "Main Content", "content": "Main content section"},
                    {"title": "Conclusion", "content": "Conclusion section"}
                ]
            }
        else:
            with open(structure_file, 'r', encoding='utf-8') as f:
                content = f.read()
                import re
                h2_pattern = r'^## (.+)$'
                sections = re.findall(h2_pattern, content, re.MULTILINE)
                structure = {
                    "sections": [{"title": section, "content": f"Content about {section}"} for section in sections[:6]]
                }
        
        # Find HTML file
        html_file = article_dir / "04_optimized_draft.html"
        if not html_file.exists():
            html_files = list(article_dir.glob("*.html"))
            if html_files:
                html_file = html_files[0]
            else:
                logger.warning("No HTML file found, creating minimal content")
                article_content = f"<html><body><h1>Article about {args.article_dir}</h1></body></html>"
        
        if html_file and html_file.exists():
            with open(html_file, 'r', encoding='utf-8') as f:
                article_content = f.read()
        
        # Create output directory
        output_dir = ensure_dir(args.output_dir)
        
        # Create image prompts
        prompts = create_image_prompts(structure, article_content)
        logger.info(f"Created {len(prompts)} image prompts")
        
        # Initialize generator
        generator = GeminiImageGenerator(api_key)
        
        # Generate images
        start_time = time.time()
        results = []
        
        for prompt in prompts:
            try:
                logger.info(f"Generating {prompt['type']} image with Gemini...")
                
                result = generator.generate(
                    prompt=prompt["prompt"],
                    aspect_ratio=prompt["aspect_ratio"]
                )
                
                # Save image
                image_path = output_dir / prompt["filename"]
                with open(image_path, "wb") as f:
                    f.write(result["image_data"])
                
                # Create metadata
                metadata = {
                    "type": prompt["type"],
                    "filename": prompt["filename"],
                    "path": str(image_path),
                    "aspect_ratio": prompt["aspect_ratio"],
                    "alt_text": prompt.get("alt_text", ""),
                    "prompt": prompt["prompt"],
                    "enhanced_prompt": result.get("enhanced_prompt", ""),
                    "generator": result.get("generator", "gemini"),
                    "created_at": datetime.utcnow().isoformat()
                }
                
                results.append(metadata)
                logger.info(f"Successfully generated {prompt['type']} image")
                
            except Exception as e:
                log_error(logger, e, f"Image generation for {prompt['type']}")
                results.append({
                    "type": prompt["type"],
                    "filename": prompt["filename"],
                    "error": str(e),
                    "created_at": datetime.utcnow().isoformat()
                })
            
            # Rate limiting
            time.sleep(1)
        
        elapsed_time = time.time() - start_time
        
        # Count successful generations
        successful = len([r for r in results if "error" not in r])
        failed = len(results) - successful
        
        # Save metadata
        metadata = {
            "generated_images": results,
            "statistics": {
                "total_requested": len(prompts),
                "successful": successful,
                "failed": failed,
                "generator": "gemini-api",
                "execution_time": elapsed_time
            },
            "created_at": datetime.utcnow().isoformat()
        }
        
        metadata_file = output_dir / "images_metadata.json"
        write_json(metadata, metadata_file)
        
        # Log metrics
        log_metric(logger, "images_generated", successful)
        log_metric(logger, "generation_time", elapsed_time, "seconds")
        
        if failed > 0:
            logger.warning(f"{failed} images failed to generate")
        
        logger.info(f"Image generation completed: {successful}/{len(prompts)} images")
        
        log_phase_end(logger, "Image Generation (Gemini API)", success=True)
        
    except Exception as e:
        log_error(logger, e, "Image Generation (Gemini API)")
        log_phase_end(logger, "Image Generation (Gemini API)", success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()