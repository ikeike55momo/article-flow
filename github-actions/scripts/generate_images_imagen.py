#!/usr/bin/env python3
"""Image Generation using placeholder images - Imagen API is not publicly available yet"""

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
from PIL import Image, ImageDraw
import io

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric
from utils.file_utils import read_json, write_json, ensure_dir


class ImagenGenerator:
    """Google AI image generator using Gemini with image generation prompt"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        
    async def generate_async(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        num_images: int = 1
    ) -> Dict[str, Any]:
        """Generate placeholder image with text description"""
        
        # Parse aspect ratio to get dimensions
        width, height = self._get_dimensions_from_ratio(aspect_ratio)
        
        # Create a placeholder image with PIL
        img = Image.new('RGB', (width, height), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Add text to indicate this is a placeholder
        text = "Placeholder Image"
        subtitle = f"Aspect Ratio: {aspect_ratio}"
        
        # Calculate text position (centered)
        try:
            # Try to use a default font
            from PIL import ImageFont
            font = ImageFont.load_default()
        except:
            font = None
            
        # Draw text
        text_bbox = draw.textbbox((0, 0), text, font=font) if hasattr(draw, 'textbbox') else (0, 0, 200, 30)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2 - 20
        
        draw.text((x, y), text, fill='#666666', font=font)
        draw.text((x, y + 30), subtitle, fill='#999999', font=font)
        
        # Add border
        draw.rectangle([(0, 0), (width-1, height-1)], outline='#cccccc', width=2)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        return {
            "image_data": img_byte_arr,
            "generator": "placeholder",
            "prompt": prompt,
            "note": "This is a placeholder image. Imagen API is not publicly available yet."
        }
    
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
    
    def _get_dimensions_from_ratio(self, ratio_str: str) -> tuple:
        """Get pixel dimensions from aspect ratio"""
        base_width = 1200  # Base width for all images
        
        if ":" in ratio_str:
            # Parse "16:9" format
            width_ratio, height_ratio = map(int, ratio_str.split(':'))
            height = int(base_width * height_ratio / width_ratio)
            return base_width, height
        elif "x" in ratio_str:
            # Parse "1200x630" format
            return tuple(map(int, ratio_str.split('x')))
        else:
            # Default to 16:9
            return base_width, 675
    
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
        logger.info(f"Generating placeholder for {prompt_data['type']} image...")
        
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
            "generator": result.get("generator", "placeholder"),
            "created_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Successfully generated placeholder for {prompt_data['type']} image")
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
                logger.info(f"Generating placeholder for {p['type']} image...")
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
                    "generator": "placeholder",
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
    logger = setup_logging("image_generation_placeholder", args.log_level)
    log_phase_start(logger, "Image Generation (Placeholder)")
    
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
                "generator": "placeholder",
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
        
        log_phase_end(logger, "Image Generation (Placeholder)", success=True)
        
    except Exception as e:
        log_error(logger, e, "Image Generation (Placeholder)")
        log_phase_end(logger, "Image Generation (Placeholder)", success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()