#!/usr/bin/env python3
"""Phase 3: Structure Planning - Create evidence-based article structure"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.claude_api import ClaudeAPI
from utils.file_utils import read_json, write_json, read_prompt
from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric
from utils.config import Config, validate_environment


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Phase 3: Structure Planning")
    parser.add_argument("--research-file", required=True, help="Phase 2 research output JSON file")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    return parser.parse_args()


def create_article_structure(research_data: dict, claude: ClaudeAPI, config: Config) -> dict:
    """Create comprehensive article structure based on research"""
    
    # Read structure planning prompt
    prompt_template = read_prompt("02_structure")
    
    # Extract key information from research
    params = research_data["phase1_params"]
    sources = research_data["source_analysis"]["categorized_sources"]
    high_priority_sources = research_data["source_analysis"]["high_priority_sources"]
    
    # Format sources for prompt
    sources_summary = format_sources_for_prompt(sources)
    
    # Generate structure
    prompt = prompt_template.format(
        topic=params["topic"],
        main_keyword=params["analysis"]["main_keyword"],
        target_audience=params.get("target_audience", "セルフケア志向の女性"),
        word_count=params.get("word_count", "3200"),
        research_summary=sources_summary,
        key_points="\n".join(params["analysis"].get("key_points", [])),
        content_type=params["analysis"].get("content_type", "informational")
    )
    
    structure = claude.generate_with_structured_output(
        prompt=prompt,
        system_prompt="You are an expert content strategist specializing in creating SEO-optimized article structures based on comprehensive research.",
        expected_format={
            "title": "string",
            "meta_description": "string",
            "introduction": {
                "hook": "string",
                "background": "string",
                "thesis": "string",
                "preview": ["string"]
            },
            "main_sections": [
                {
                    "h2_title": "string",
                    "section_id": "string",
                    "subsections": [
                        {
                            "h3_title": "string",
                            "key_points": ["string"],
                            "evidence_needed": ["string"],
                            "word_count_target": "number"
                        }
                    ],
                    "section_purpose": "string",
                    "target_keywords": ["string"],
                    "word_count_target": "number"
                }
            ],
            "faq_section": {
                "questions": [
                    {
                        "question": "string",
                        "answer_outline": "string",
                        "evidence_source": "string"
                    }
                ]
            },
            "conclusion": {
                "summary_points": ["string"],
                "call_to_action": "string",
                "future_outlook": "string"
            },
            "internal_linking_plan": [
                {
                    "anchor_text": "string",
                    "target_section": "string",
                    "purpose": "string"
                }
            ],
            "image_requirements": [
                {
                    "placement": "string",
                    "type": "string",
                    "description": "string",
                    "alt_text": "string"
                }
            ]
        },
        temperature=0.4,
        max_tokens=6000,
        metadata={"phase": "structure_planning"}
    )
    
    # Validate structure requirements
    validation_results = validate_structure(structure, config)
    
    # Add metadata
    structure["metadata"] = {
        "created_at": datetime.utcnow().isoformat(),
        "total_sections": len(structure.get("main_sections", [])),
        "total_faqs": len(structure.get("faq_section", {}).get("questions", [])),
        "validation": validation_results,
        "source_distribution": analyze_source_usage(sources)
    }
    
    return structure


def format_sources_for_prompt(sources: dict) -> str:
    """Format categorized sources for the prompt"""
    formatted = []
    
    for category, source_list in sources.items():
        if source_list:
            formatted.append(f"\n【{category.replace('_', ' ').title()}】")
            for source in source_list[:3]:  # Limit to top 3 per category
                formatted.append(f"- {source.get('title', 'No title')}")
                if source.get('key_info'):
                    formatted.append(f"  Key info: {source['key_info']}")
    
    return "\n".join(formatted)


def validate_structure(structure: dict, config: Config) -> dict:
    """Validate the structure against requirements"""
    requirements = config.requirements
    
    validation = {
        "passed": True,
        "issues": []
    }
    
    # Check H2 count
    h2_count = len(structure.get("main_sections", []))
    if h2_count != 6:
        validation["issues"].append(f"H2 count is {h2_count}, should be 6")
        validation["passed"] = False
    
    # Check FAQ count
    faq_count = len(structure.get("faq_section", {}).get("questions", []))
    if faq_count != 7:
        validation["issues"].append(f"FAQ count is {faq_count}, should be 7")
        validation["passed"] = False
    
    # Check word count distribution
    total_word_target = sum(
        section.get("word_count_target", 0) 
        for section in structure.get("main_sections", [])
    )
    
    if total_word_target < 2900 or total_word_target > 3500:
        validation["issues"].append(
            f"Total word count target is {total_word_target}, should be 3200±300"
        )
        validation["passed"] = False
    
    # Check required elements
    if not structure.get("meta_description"):
        validation["issues"].append("Missing meta description")
        validation["passed"] = False
    
    if not structure.get("internal_linking_plan"):
        validation["issues"].append("Missing internal linking plan")
        validation["passed"] = False
    
    return validation


def analyze_source_usage(sources: dict) -> dict:
    """Analyze the distribution of source types"""
    distribution = {
        "government": len(sources.get("government_sources", [])),
        "academic": len(sources.get("academic_sources", [])),
        "medical": len(sources.get("medical_sources", [])),
        "industry": len(sources.get("industry_sources", [])),
        "media": len(sources.get("media_sources", []))
    }
    
    total = sum(distribution.values())
    if total > 0:
        distribution["percentages"] = {
            k: round(v / total * 100, 1) 
            for k, v in distribution.items()
        }
    
    return distribution


def generate_section_keywords(structure: dict, claude: ClaudeAPI) -> dict:
    """Generate specific keywords for each section"""
    
    section_keywords = {}
    
    for section in structure.get("main_sections", []):
        prompt = f"""
        For the article section titled "{section['h2_title']}" about {section['section_purpose']},
        generate 5-7 specific long-tail keywords that should be naturally incorporated.
        
        Return as JSON: {{"keywords": ["keyword1", "keyword2", ...]}}
        """
        
        response = claude.generate_with_structured_output(
            prompt=prompt,
            temperature=0.5,
            metadata={"phase": "keyword_generation", "section": section['section_id']}
        )
        
        section_keywords[section['section_id']] = response.get("keywords", [])
    
    return section_keywords


def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging("phase3_structure_planning", args.log_level)
    log_phase_start(logger, "Phase 3: Structure Planning")
    
    try:
        # Validate environment
        validate_environment()
        
        # Load configuration
        config = Config()
        
        # Initialize Claude API
        claude = ClaudeAPI()
        
        # Read research data
        research_data = read_json(args.research_file)
        logger.info(f"Creating structure for topic: {research_data['phase1_params']['topic']}")
        
        # Create article structure
        structure = create_article_structure(research_data, claude, config)
        
        # Generate section-specific keywords
        section_keywords = generate_section_keywords(structure, claude)
        structure["section_keywords"] = section_keywords
        
        # Log metrics
        log_metric(logger, "h2_sections", len(structure.get("main_sections", [])))
        log_metric(logger, "faq_questions", len(structure.get("faq_section", {}).get("questions", [])))
        log_metric(logger, "internal_links", len(structure.get("internal_linking_plan", [])))
        log_metric(logger, "image_requirements", len(structure.get("image_requirements", [])))
        
        # Validation results
        validation = structure["metadata"]["validation"]
        if not validation["passed"]:
            logger.warning(f"Structure validation issues: {validation['issues']}")
        
        # Save output
        output_file = Path(args.output_dir) / "phase3_structure.json"
        write_json(structure, output_file)
        
        # Also save a human-readable outline
        outline_file = Path(args.output_dir) / "article_outline.md"
        write_outline_markdown(structure, outline_file)
        
        logger.info(f"Structure planning completed successfully")
        
        log_phase_end(logger, "Phase 3: Structure Planning", success=True)
        
    except Exception as e:
        log_error(logger, e, "Phase 3")
        log_phase_end(logger, "Phase 3: Structure Planning", success=False)
        sys.exit(1)


def write_outline_markdown(structure: dict, output_path: Path):
    """Write a human-readable markdown outline"""
    lines = []
    
    lines.append(f"# {structure['title']}\n")
    lines.append(f"**Meta Description**: {structure['meta_description']}\n")
    lines.append("## Article Outline\n")
    
    # Introduction
    lines.append("### Introduction")
    lines.append(f"- Hook: {structure['introduction']['hook']}")
    lines.append(f"- Thesis: {structure['introduction']['thesis']}\n")
    
    # Main sections
    for i, section in enumerate(structure['main_sections'], 1):
        lines.append(f"### {i}. {section['h2_title']}")
        lines.append(f"- Purpose: {section['section_purpose']}")
        lines.append(f"- Target words: {section['word_count_target']}")
        
        if section.get('subsections'):
            for subsection in section['subsections']:
                lines.append(f"  - {subsection['h3_title']}")
        
        lines.append("")
    
    # FAQ
    lines.append("### FAQ Section")
    for i, qa in enumerate(structure['faq_section']['questions'], 1):
        lines.append(f"{i}. {qa['question']}")
    
    lines.append("")
    
    # Save
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


if __name__ == "__main__":
    main()