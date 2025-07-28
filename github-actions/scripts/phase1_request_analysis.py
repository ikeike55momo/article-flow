#!/usr/bin/env python3
"""Phase 1: Request Analysis - Parse and validate article generation request"""

import argparse
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.claude_api import ClaudeAPI
from utils.file_utils import read_json, write_json, read_prompt
from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error
from utils.config import Config, validate_environment


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Phase 1: Request Analysis")
    parser.add_argument("--params-file", required=True, help="Input parameters JSON file")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    return parser.parse_args()


def analyze_request(params: dict, config: Config, claude: ClaudeAPI) -> dict:
    """Analyze and enhance the request parameters"""
    
    # Read the prompt template
    # V3の場合は新しいプロンプトテンプレートを使用
    if os.environ.get("ENABLE_GEMINI_RESEARCH") == "true":
        prompt_template = read_prompt("00_parse_request_v3")
    else:
        prompt_template = read_prompt("00_parse_request")
    
    # Prepare the prompt
    if os.environ.get("ENABLE_GEMINI_RESEARCH") == "true":
        # V3: keywords パラメータを使用
        prompt = prompt_template.format(
            topic=params["topic"],
            target_audience=params.get("target_audience", "セルフケア志向の女性"),
            keywords=params.get("keywords", ""),
            word_count=params.get("word_count", "3200")
        )
    else:
        # V2: 既存のパラメータ
        prompt = prompt_template.format(
            topic=params["topic"],
            store_url=params.get("store_url", "なし"),
            target_audience=params.get("target_audience", "セルフケア志向の女性"),
            word_count=params.get("word_count", "3200")
        )
    
    # Get structured analysis from Claude
    analysis = claude.generate_with_structured_output(
        prompt=prompt,
        system_prompt="You are an expert content strategist specializing in SEO-optimized article planning.",
        expected_format={
            "main_keyword": "string",
            "related_keywords": ["string"],
            "search_intent": "string",
            "content_type": "string",
            "tone": "string",
            "key_points": ["string"],
            "research_queries": ["string"],
            "competitor_analysis_needed": "boolean",
            "local_seo_focus": "boolean",
            "estimated_sections": "number"
        },
        temperature=0.3,
        metadata={"phase": "request_analysis"}
    )
    
    # Check if JSON parsing failed
    if "parse_error" in analysis:
        logger.error(f"Failed to parse Claude's response: {analysis.get('parse_error')}")
        logger.debug(f"Raw response: {analysis.get('raw_response', 'No response available')}")
        raise ValueError(f"Failed to parse analysis response: {analysis.get('parse_error')}")
    
    # Validate required fields in analysis
    required_fields = ["main_keyword", "related_keywords", "search_intent"]
    missing_fields = [field for field in required_fields if field not in analysis]
    if missing_fields:
        logger.error(f"Missing required fields in analysis: {missing_fields}")
        logger.debug(f"Analysis received: {json.dumps(analysis, indent=2)}")
        raise ValueError(f"Analysis missing required fields: {', '.join(missing_fields)}")
    
    # Enhance parameters with analysis results
    enhanced_params = params.copy()
    enhanced_params.update({
        "analysis": analysis,
        "processed_at": datetime.utcnow().isoformat(),
        "workflow_version": "1.0.0"
    })
    
    return enhanced_params


def validate_parameters(params: dict) -> list:
    """Validate input parameters"""
    errors = []
    
    # Required fields
    if not params.get("topic"):
        errors.append("Topic is required")
    
    # Word count validation
    word_count = params.get("word_count", "3200")
    try:
        wc = int(word_count)
        if wc < 2000 or wc > 5000:
            errors.append(f"Word count {wc} is outside acceptable range (2000-5000)")
    except ValueError:
        errors.append(f"Invalid word count: {word_count}")
    
    # URL validation
    store_url = params.get("store_url", "")
    if store_url and not (store_url.startswith("http://") or store_url.startswith("https://")):
        errors.append(f"Invalid store URL: {store_url}")
    
    return errors


def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging("phase1_request_analysis", args.log_level)
    log_phase_start(logger, "Phase 1: Request Analysis")
    
    try:
        # Validate environment
        validate_environment()
        
        # Load configuration
        config = Config()
        
        # Initialize Claude API
        claude = ClaudeAPI()
        
        # Read input parameters
        params = read_json(args.params_file)
        logger.info(f"Processing request for topic: {params.get('topic')}")
        
        # Validate parameters
        errors = validate_parameters(params)
        if errors:
            for error in errors:
                log_error(logger, ValueError(error), "Parameter validation")
            sys.exit(1)
        
        # Analyze request
        enhanced_params = analyze_request(params, config, claude)
        
        # Save output
        output_file = Path(args.output_dir) / "phase1_output.json"
        write_json(enhanced_params, output_file)
        
        # Log summary
        analysis = enhanced_params.get('analysis', {})
        if isinstance(analysis, dict):
            logger.info(f"Main keyword identified: {analysis.get('main_keyword', 'Not available')}")
            logger.info(f"Research queries generated: {len(analysis.get('research_queries', []))}")
        else:
            logger.warning(f"Analysis data is not in expected format: {type(analysis)}")
        
        log_phase_end(logger, "Phase 1: Request Analysis", success=True)
        
    except Exception as e:
        log_error(logger, e, "Phase 1")
        log_phase_end(logger, "Phase 1: Request Analysis", success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()