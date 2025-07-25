#!/usr/bin/env python3
"""Image Generation using Google AI Imagen - No OpenAI API required"""

import argparse
import sys
import os
import json
import time
import base64
import httpx
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import io

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric
from utils.file_utils import read_json, write_json, ensure_dir


class ImagenGenerator:
    """Google AI Imagen image generator"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        
    async def generate_async(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        num_images: int = 1
    ) -> Dict[str, Any]:
        """Generate image using Google AI Imagen API"""
        
        # Parse aspect ratio to ensure correct format
        formatted_aspect_ratio = self._parse_aspect_ratio(aspect_ratio)
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/imagen-3:generateImages",
                    headers={
                        "x-goog-api-key": self.api_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": prompt,
                        "aspectRatio": formatted_aspect_ratio,
                        "numberOfImages": num_images,
                        "responseFormat": "base64"
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    images = result.get("images", [])
                    
                    if images:
                        # Return first image
                        image_data = base64.b64decode(images[0]["base64"])
                        return {
                            "image_data": image_data,
                            "generator": "imagen-3",
                            "prompt": prompt
                        }
                    else:
                        raise Exception("No images returned from API")
                else:
                    raise Exception(f"API Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                raise Exception(f"Imagen generation failed: {str(e)}")
    
    def generate(self, prompt: str, aspect_ratio: str = "16:9") -> Dict[str, Any]:
        """Synchronous wrapper for generate_async"""
        return asyncio.run(self.generate_async(prompt, aspect_ratio))
    
    def _parse_aspect_ratio(self, ratio_str: str) -> str:
        """Parse aspect ratio string to standard format"""
        if "x" in ratio_str:
            # Handle "1200x630" format
            width, height = map(int, ratio_str.split('x'))
            # Convert to aspect ratio
            gcd = self._gcd(width, height)
            return f"{width//gcd}:{height//gcd}"
        else:
            # Already in "16:9" format
            return ratio_str
    
    def _gcd(self, a: int, b: int) -> int:
        """Calculate greatest common divisor"""
        while b:
            a, b = b, a % b
        return a


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Generate images for article using Imagen")
    parser.add_argument("--article-dir", required=True, help="Directory containing article files")
    parser.add_argument("--output-dir", required=True, help="Output directory for images")
    parser.add_argument("--parallel", action="store_true", help="Generate images in parallel")
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
        "aspect_ratio": "16:9",  # Better for hero images
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
            "aspect_ratio": "4:3",  # Better for content images
            "filename": f"section-{i}.png"
        })
    
    return prompts


def generate_single_image(
    prompt_data: dict,
    generator: ImagenGenerator,
    output_dir: Path,
    logger
) -> Dict[str, Any]:
    """Generate a single image"""
    
    try:
        logger.info(f"Generating {prompt_data['type']} image with Imagen...")
        
        # Generate image
        result = generator.generate(
            prompt=prompt_data["prompt"],
            aspect_ratio=prompt_data["aspect_ratio"]
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
            "alt_text": prompt_data.get("alt_text", ""),
            "prompt": prompt_data["prompt"],
            "generator": result.get("generator", "imagen"),
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


async def generate_images_parallel_async(
    prompts: List[Dict[str, Any]],
    generator: ImagenGenerator,
    output_dir: Path,
    logger
) -> List[Dict[str, Any]]:
    """Generate multiple images in parallel using async"""
    
    tasks = []
    
    for prompt in prompts:
        async def generate_and_save(p):
            try:
                logger.info(f"Generating {p['type']} image...")
                result = await generator.generate_async(
                    prompt=p["prompt"],
                    aspect_ratio=p["aspect_ratio"]
                )
                
                # Save image
                image_path = output_dir / p["filename"]
                with open(image_path, "wb") as f:
                    f.write(result["image_data"])
                
                # Optimize in thread to not block
                await asyncio.get_event_loop().run_in_executor(
                    None, optimize_image, image_path
                )
                
                return {
                    "type": p["type"],
                    "filename": p["filename"],
                    "path": str(image_path),
                    "aspect_ratio": p["aspect_ratio"],
                    "alt_text": p.get("alt_text", ""),
                    "prompt": p["prompt"],
                    "generator": "imagen",
                    "created_at": datetime.utcnow().isoformat()
                }
            except Exception as e:
                return {
                    "type": p["type"],
                    "filename": p["filename"],
                    "error": str(e),
                    "created_at": datetime.utcnow().isoformat()
                }
        
        tasks.append(generate_and_save(prompt))
    
    # Execute all tasks concurrently
    results = await asyncio.gather(*tasks)
    return results


def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging("image_generation_imagen", args.log_level)
    log_phase_start(logger, "Image Generation (Imagen)")
    
    try:
        # Check API key
        google_ai_key = os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if not google_ai_key:
            raise ValueError("GOOGLE_AI_API_KEY or GEMINI_API_KEY not found in environment")
        
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
        generator = ImagenGenerator(google_ai_key)
        
        # Generate images
        start_time = time.time()
        
        if args.parallel:
            # Use async for parallel generation
            results = asyncio.run(generate_images_parallel_async(
                prompts,
                generator,
                output_dir,
                logger
            ))
        else:
            results = []
            for prompt in prompts:
                result = generate_single_image(
                    prompt,
                    generator,
                    output_dir,
                    logger
                )
                results.append(result)
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
                "generator": "imagen",
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
        
        log_phase_end(logger, "Image Generation (Imagen)", success=True)
        
    except Exception as e:
        log_error(logger, e, "Image Generation (Imagen)")
        log_phase_end(logger, "Image Generation (Imagen)", success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()