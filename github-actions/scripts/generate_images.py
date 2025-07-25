#!/usr/bin/env python3
"""Image Generation - Generate article images using DALL-E 3 and other services"""

import argparse
import sys
import os
import json
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import io

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric
from utils.file_utils import read_json, write_json, ensure_dir


class ImageGenerator:
    """Base class for image generation"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def generate(self, prompt: str, size: str = "1024x1024") -> bytes:
        raise NotImplementedError


class DallE3Generator(ImageGenerator):
    """DALL-E 3 image generator"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI package not installed")
    
    def generate(
        self, 
        prompt: str, 
        size: str = "1024x1024",
        quality: str = "standard",
        style: str = "natural"
    ) -> Dict[str, Any]:
        """Generate image using DALL-E 3"""
        
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                style=style,
                n=1
            )
            
            image_url = response.data[0].url
            revised_prompt = response.data[0].revised_prompt
            
            # Download image
            image_response = requests.get(image_url, timeout=30)
            image_response.raise_for_status()
            
            return {
                "image_data": image_response.content,
                "url": image_url,
                "revised_prompt": revised_prompt,
                "generator": "dall-e-3"
            }
            
        except Exception as e:
            raise Exception(f"DALL-E 3 generation failed: {str(e)}")


class StableDiffusionGenerator(ImageGenerator):
    """Stable Diffusion API generator (fallback)"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.api_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    
    def generate(self, prompt: str, size: str = "1024x1024") -> Dict[str, Any]:
        """Generate image using Stable Diffusion"""
        
        width, height = map(int, size.split('x'))
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        body = {
            "text_prompts": [{"text": prompt, "weight": 1}],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": 1,
            "steps": 30
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=body,
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            image_data = data["artifacts"][0]["base64"]
            
            # Decode base64
            import base64
            image_bytes = base64.b64decode(image_data)
            
            return {
                "image_data": image_bytes,
                "generator": "stable-diffusion"
            }
            
        except Exception as e:
            raise Exception(f"Stable Diffusion generation failed: {str(e)}")


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Generate images for article")
    parser.add_argument("--article-file", required=True, help="Article HTML file")
    parser.add_argument("--structure-file", required=True, help="Article structure JSON file")
    parser.add_argument("--output-dir", required=True, help="Output directory for images")
    parser.add_argument("--parallel", action="store_true", help="Generate images in parallel")
    parser.add_argument("--generator", default="dalle3", choices=["dalle3", "stable", "both"])
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    return parser.parse_args()


def create_image_prompts(structure: dict, article_content: str) -> List[Dict[str, Any]]:
    """Create prompts for all required images"""
    
    prompts = []
    
    # Hero image
    article_topic = structure.get("title", "")
    main_keyword = structure.get("metadata", {}).get("main_keyword", "")
    
    hero_prompt = f"""
    Create a professional, high-quality hero image for an article about {article_topic}.
    The image should be modern, clean, and visually appealing for a health/beauty blog.
    Key theme: {main_keyword}
    Style: Minimalist, professional photography, soft lighting, calming colors
    No text or logos in the image.
    """
    
    prompts.append({
        "type": "hero",
        "prompt": hero_prompt.strip(),
        "size": "1200x630",  # Optimal for social media sharing
        "filename": "hero.png"
    })
    
    # Section images
    for i, section in enumerate(structure.get("main_sections", [])[:4], 1):
        section_prompt = f"""
        Create an informative, professional image illustrating: {section['h2_title']}
        Purpose: {section['section_purpose']}
        Style: Clean infographic or lifestyle photography, educational, health/beauty focused
        Color scheme: Consistent with health and wellness theme
        No text overlays.
        """
        
        prompts.append({
            "type": f"section_{i}",
            "prompt": section_prompt.strip(),
            "size": "800x600",
            "filename": f"section-{i}.png"
        })
    
    # Additional images from structure requirements
    for i, img_req in enumerate(structure.get("image_requirements", []), 1):
        if img_req.get("type") not in ["hero", "section"]:
            prompts.append({
                "type": img_req.get("type", f"custom_{i}"),
                "prompt": img_req.get("description", ""),
                "size": "800x600",
                "filename": f"image-{i}.png",
                "alt_text": img_req.get("alt_text", "")
            })
    
    return prompts


def generate_single_image(
    prompt_data: dict,
    generator: ImageGenerator,
    output_dir: Path,
    logger
) -> Dict[str, Any]:
    """Generate a single image"""
    
    try:
        logger.info(f"Generating {prompt_data['type']} image...")
        
        # Generate image
        result = generator.generate(
            prompt=prompt_data["prompt"],
            size=prompt_data["size"]
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
            "size": prompt_data["size"],
            "alt_text": prompt_data.get("alt_text", ""),
            "prompt": prompt_data["prompt"],
            "generator": result.get("generator", "unknown"),
            "created_at": datetime.utcnow().isoformat()
        }
        
        if "revised_prompt" in result:
            metadata["revised_prompt"] = result["revised_prompt"]
        
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


def generate_images_parallel(
    prompts: List[Dict[str, Any]],
    generator: ImageGenerator,
    output_dir: Path,
    logger,
    max_workers: int = 4
) -> List[Dict[str, Any]]:
    """Generate multiple images in parallel"""
    
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_prompt = {
            executor.submit(
                generate_single_image,
                prompt,
                generator,
                output_dir,
                logger
            ): prompt
            for prompt in prompts
        }
        
        # Collect results
        for future in as_completed(future_to_prompt):
            prompt = future_to_prompt[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                log_error(logger, e, f"Parallel generation for {prompt['type']}")
                results.append({
                    "type": prompt["type"],
                    "filename": prompt["filename"],
                    "error": str(e)
                })
    
    return results


def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging("image_generation", args.log_level)
    log_phase_start(logger, "Image Generation")
    
    try:
        # Check API keys
        openai_key = os.environ.get("OPENAI_API_KEY")
        stability_key = os.environ.get("STABILITY_API_KEY")
        
        if not openai_key and args.generator in ["dalle3", "both"]:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        # Read input files
        structure = read_json(args.structure_file)
        
        with open(args.article_file, 'r', encoding='utf-8') as f:
            article_content = f.read()
        
        # Create output directory
        output_dir = ensure_dir(args.output_dir)
        
        # Create image prompts
        prompts = create_image_prompts(structure, article_content)
        logger.info(f"Created {len(prompts)} image prompts")
        
        # Initialize generator
        if args.generator == "dalle3":
            generator = DallE3Generator(openai_key)
        elif args.generator == "stable":
            generator = StableDiffusionGenerator(stability_key)
        else:
            # Default to DALL-E 3
            generator = DallE3Generator(openai_key)
        
        # Generate images
        start_time = time.time()
        
        if args.parallel:
            results = generate_images_parallel(
                prompts,
                generator,
                output_dir,
                logger
            )
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
                "generator": args.generator,
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
        
        log_phase_end(logger, "Image Generation", success=True)
        
    except Exception as e:
        log_error(logger, e, "Image Generation")
        log_phase_end(logger, "Image Generation", success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()