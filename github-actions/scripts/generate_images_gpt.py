#!/usr/bin/env python3
"""Image Generation using OpenAI gpt-image-1 API"""

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
import requests
from PIL import Image
import io

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric
from utils.file_utils import read_json, write_json, ensure_dir


class DallEGenerator:
    """OpenAI gpt-image-1 image generator (latest model)"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/images/generations"
        
    async def generate_async(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "high"
    ) -> Dict[str, Any]:
        """Generate image using gpt-image-1 API"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # gpt-image-1 parameters - NO response_format parameter!
        data = {
            "model": "gpt-image-1",
            "prompt": prompt,
            "n": 1,
            "size": size,
            "quality": quality  # "low", "medium", "high", or "auto"
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=120  # 2 minutes timeout for complex prompts
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # gpt-image-1 returns base64 data, NOT URLs
                # Access using b64_json from the data array
                image_b64 = result['data'][0]['b64_json']
                revised_prompt = result['data'][0].get('revised_prompt', prompt)
                
                # Decode base64 to binary image data
                image_data = base64.b64decode(image_b64)
                
                return {
                    "image_data": image_data,
                    "generator": "gpt-image-1",
                    "prompt": prompt,
                    "revised_prompt": revised_prompt,
                    "size": size,
                    "quality": quality
                }
            else:
                error_msg = response.json().get('error', {}).get('message', response.text)
                raise Exception(f"gpt-image-1 API Error {response.status_code}: {error_msg}")
                
        except requests.exceptions.Timeout:
            raise Exception("gpt-image-1 API request timed out after 120 seconds")
        except Exception as e:
            raise Exception(f"gpt-image-1 generation failed: {str(e)}")
    
    def generate(self, prompt: str, size: str = "1024x1024", quality: str = "high") -> Dict[str, Any]:
        """Synchronous wrapper for generate_async"""
        return asyncio.run(self.generate_async(prompt, size, quality))
    
    def _get_size_for_aspect_ratio(self, aspect_ratio: str) -> str:
        """Convert aspect ratio to gpt-image-1 supported size"""
        # gpt-image-1 only supports these specific sizes
        size_mapping = {
            "1:1": "1024x1024",
            "16:9": "1536x1024",  # Wide landscape (closest to 16:9)
            "9:16": "1024x1536",  # Portrait (closest to 9:16)
            "4:3": "1024x1024",   # Default to square
            "3:4": "1024x1024",   # Default to square
            "square": "1024x1024",
            "landscape": "1536x1024",
            "portrait": "1024x1536",
            "wide": "1536x1024",
            "3:2": "1536x1024",   # Landscape
            "2:3": "1024x1536"    # Portrait
        }
        return size_mapping.get(aspect_ratio, "1024x1024")


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Generate images using OpenAI gpt-image-1")
    parser.add_argument("--article-dir", required=True, help="Directory containing article files")
    parser.add_argument("--output-dir", required=True, help="Output directory for images")
    parser.add_argument("--quality", default="high", choices=["low", "medium", "high", "auto"], help="Image quality")
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
    
    # gpt-image-1 works best with detailed, specific prompts
    hero_prompt = f"""
    Create a professional hero image for a health and beauty article about {article_topic}.
    The image should have a modern, clean, minimalist design with soft pastel colors.
    Main theme: {main_keyword}
    Style: High-quality stock photography, wellness-focused, calming atmosphere.
    Include subtle visual elements that suggest health and wellbeing.
    Absolutely no text, logos, or watermarks in the image.
    Photorealistic style with professional lighting.
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
        Create a professional illustration for an article section about: {section_title}.
        Context: {section.get('content', 'Health and wellness information')}
        Style: Clean, informative, health and wellness focused.
        Use soft pastel colors with a modern, minimalist design.
        The image should visually represent the concept without any text overlays or logos.
        Photorealistic or semi-realistic style with good composition.
        """
        
        prompts.append({
            "type": f"section_{i}",
            "prompt": section_prompt.strip(),
            "aspect_ratio": "4:3",
            "filename": f"section-{i}.png"
        })
    
    return prompts


def generate_single_image(
    prompt_data: dict,
    generator: DallEGenerator,
    output_dir: Path,
    quality: str,
    logger
) -> Dict[str, Any]:
    """Generate a single image"""
    
    try:
        logger.info(f"Generating {prompt_data['type']} image with gpt-image-1...")
        
        # Convert aspect ratio to gpt-image-1 size
        size = generator._get_size_for_aspect_ratio(prompt_data["aspect_ratio"])
        
        # Generate image
        result = generator.generate(
            prompt=prompt_data["prompt"],
            size=size,
            quality=quality
        )
        
        # Save image
        image_path = output_dir / prompt_data["filename"]
        with open(image_path, "wb") as f:
            f.write(result["image_data"])
        
        # Optimize image
        optimize_image(image_path)
        
        # Create metadata
        metadata = {
            "type": prompt_data["type"],
            "filename": prompt_data["filename"],
            "path": str(image_path),
            "aspect_ratio": prompt_data["aspect_ratio"],
            "size": size,
            "quality": quality,
            "alt_text": prompt_data.get("alt_text", ""),
            "prompt": prompt_data["prompt"],
            "revised_prompt": result.get("revised_prompt", ""),
            "generator": result.get("generator", "gpt-image-1"),
            "created_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Successfully generated {prompt_data['type']} image")
        return metadata
        
    except Exception as e:
        log_error(logger, e, f"Image generation for {prompt_data['type']}")
        return {
            "type": prompt_data["type"],
            "filename": prompt_data["filename"],
            "error": str(e),
            "created_at": datetime.utcnow().isoformat()
        }


def optimize_image(image_path: Path):
    """Optimize image file size and format"""
    try:
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if necessary
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        
        # Save with optimization
        img.save(
            image_path,
            'PNG',
            optimize=True,
            quality=85
        )
        
    except Exception as e:
        # Log but don't fail if optimization fails
        print(f"Warning: Image optimization failed: {e}")


def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging("image_generation_gpt", args.log_level)
    log_phase_start(logger, "Image Generation (gpt-image-1)")
    
    try:
        # Check API key
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        logger.info(f"Using gpt-image-1 for image generation")
        logger.info(f"Quality setting: {args.quality}")
        
        # Read input files from article directory
        article_dir = Path(args.article_dir)
        
        # Find structure file - it's a markdown file, not JSON
        structure_file = article_dir / "02_article_structure.md"
        if not structure_file.exists():
            logger.warning(f"Structure file not found at {structure_file}")
            # Create a minimal structure
            structure = {
                "sections": [
                    {"title": "Introduction", "content": "Introduction to the topic"},
                    {"title": "Main Content", "content": "Main content section"},
                    {"title": "Conclusion", "content": "Conclusion section"}
                ]
            }
        else:
            # Parse markdown structure file to extract sections
            with open(structure_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract H2 sections from markdown
                import re
                h2_pattern = r'^## (.+)$'
                sections = re.findall(h2_pattern, content, re.MULTILINE)
                structure = {
                    "sections": [{"title": section, "content": f"Content about {section}"} for section in sections[:6]]
                }
        
        # Find HTML file - look for optimized draft
        html_file = article_dir / "04_optimized_draft.html"
        if not html_file.exists():
            # Try to find any HTML file
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
        generator = DallEGenerator(api_key)
        
        # Generate images
        start_time = time.time()
        results = []
        
        for i, prompt in enumerate(prompts):
            result = generate_single_image(
                prompt,
                generator,
                output_dir,
                args.quality,
                logger
            )
            results.append(result)
            
            # Rate limiting - gpt-image-1 has rate limits
            if i < len(prompts) - 1:
                logger.info("Waiting 12 seconds for rate limiting...")
                time.sleep(12)  # Be conservative with rate limits
        
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
                "generator": "gpt-image-1",
                "quality": args.quality,
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
        
        log_phase_end(logger, "Image Generation (gpt-image-1)", success=True)
        
    except Exception as e:
        log_error(logger, e, "Image Generation (gpt-image-1)")
        log_phase_end(logger, "Image Generation (gpt-image-1)", success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()