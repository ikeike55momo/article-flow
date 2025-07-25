#!/usr/bin/env python3
"""Image Generation using Google Vertex AI Imagen API"""

import argparse
import sys
import os
import json
import time
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import io
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric
from utils.file_utils import read_json, write_json, ensure_dir


class ImagenGenerator:
    """Google Vertex AI Imagen image generator"""
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        vertexai.init(project=project_id, location=location)
        # Try different model names
        try:
            # First try the newer model name
            self.model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        except Exception as e:
            print(f"Failed to load imagen-3.0-generate-001, trying imagegeneration@006: {e}")
            try:
                self.model = ImageGenerationModel.from_pretrained("imagegeneration@006")
            except Exception as e2:
                print(f"Failed to load imagegeneration@006, trying imagegeneration@005: {e2}")
                self.model = ImageGenerationModel.from_pretrained("imagegeneration@005")
        
    async def generate_async(
        self,
        prompt: str,
        aspect_ratio: str = "1:1",
        num_images: int = 1
    ) -> Dict[str, Any]:
        """Generate image using Google Vertex AI Imagen API"""
        
        try:
            # Generate image using Vertex AI
            response = self.model.generate_images(
                prompt=prompt,
                number_of_images=num_images,
                aspect_ratio=aspect_ratio,
                safety_filter_level="block_some",
                person_generation="allow_adult"
            )
            
            if response.images:
                # Get the first generated image
                image = response.images[0]
                image_bytes = image._image_bytes
                
                return {
                    "image_data": image_bytes,
                    "generator": "imagen-vertex-ai",
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio
                }
            else:
                raise Exception("No images returned from Vertex AI")
                
        except Exception as e:
            raise Exception(f"Vertex AI Imagen generation failed: {str(e)}")
    
    def generate(self, prompt: str, aspect_ratio: str = "1:1") -> Dict[str, Any]:
        """Synchronous wrapper for generate_async"""
        return asyncio.run(self.generate_async(prompt, aspect_ratio))
    
    def _get_supported_aspect_ratio(self, ratio_str: str) -> str:
        """Convert aspect ratio to Vertex AI supported format"""
        # Vertex AI supports: 1:1, 9:16, 16:9, 4:3, 3:4
        supported_ratios = ["1:1", "9:16", "16:9", "4:3", "3:4"]
        
        if ratio_str in supported_ratios:
            return ratio_str
        
        # Map common formats to supported ones
        ratio_mapping = {
            "square": "1:1",
            "portrait": "9:16",
            "landscape": "16:9",
            "wide": "16:9"
        }
        
        return ratio_mapping.get(ratio_str, "1:1")  # Default to square


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


def generate_single_image(
    prompt_data: dict,
    generator: ImagenGenerator,
    output_dir: Path,
    logger
) -> Dict[str, Any]:
    """Generate a single image"""
    
    try:
        logger.info(f"Generating {prompt_data['type']} image with Vertex AI Imagen...")
        
        # Generate image
        supported_ratio = generator._get_supported_aspect_ratio(prompt_data["aspect_ratio"])
        result = generator.generate(
            prompt=prompt_data["prompt"],
            aspect_ratio=supported_ratio
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
            "generator": result.get("generator", "imagen-vertex-ai"),
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
                logger.info(f"Generating {p['type']} image with Vertex AI Imagen...")
                supported_ratio = generator._get_supported_aspect_ratio(p["aspect_ratio"])
                result = await generator.generate_async(
                    prompt=p["prompt"],
                    aspect_ratio=supported_ratio
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
                    "generator": "imagen-vertex-ai",
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
    log_phase_start(logger, "Image Generation (Vertex AI Imagen)")
    
    try:
        # Check required environment variables
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT environment variable is required")
        
        location = os.environ.get("VERTEX_AI_LOCATION", "us-central1")
        
        # Debug: Print authentication info
        logger.info(f"Using project: {project_id}")
        logger.info(f"Using location: {location}")
        
        # Check if credentials file exists
        creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if creds_path and os.path.exists(creds_path):
            logger.info(f"Using credentials file: {creds_path}")
            with open(creds_path, 'r') as f:
                import json
                creds_data = json.load(f)
                logger.info(f"Service account: {creds_data.get('client_email', 'Unknown')}")
        else:
            logger.warning("No GOOGLE_APPLICATION_CREDENTIALS found")
        
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
        generator = ImagenGenerator(project_id, location)
        
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
                "generator": "imagen-vertex-ai",
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
        
        log_phase_end(logger, "Image Generation (Vertex AI Imagen)", success=True)
        
    except Exception as e:
        log_error(logger, e, "Image Generation (Vertex AI Imagen)")
        log_phase_end(logger, "Image Generation (Vertex AI Imagen)", success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()