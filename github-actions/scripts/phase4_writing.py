#!/usr/bin/env python3
"""Phase 4: Writing - Generate high-quality article content based on structure and research"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.claude_api import ClaudeAPI
from utils.file_utils import read_json, write_json, write_text, read_prompt
from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric
from utils.config import Config, validate_environment


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Phase 4: Writing")
    parser.add_argument("--structure-file", required=True, help="Phase 3 structure JSON file")
    parser.add_argument("--research-file", required=True, help="Phase 2 research JSON file")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    return parser.parse_args()


def write_section(
    section: dict,
    structure: dict,
    research_data: dict,
    claude: ClaudeAPI,
    config: Config
) -> dict:
    """Write a single section of the article"""
    
    # Get relevant sources for this section
    relevant_sources = get_relevant_sources_for_section(
        section,
        research_data["source_analysis"]["categorized_sources"]
    )
    
    # Read writing prompt template
    prompt_template = read_prompt("03_writing")
    
    # Prepare section context
    section_context = {
        "title": section["h2_title"],
        "purpose": section["section_purpose"],
        "target_keywords": section.get("target_keywords", []),
        "word_count_target": section["word_count_target"],
        "subsections": section.get("subsections", [])
    }
    
    # Format the prompt
    prompt = prompt_template.format(
        section_title=section["h2_title"],
        section_purpose=section["section_purpose"],
        word_count=section["word_count_target"],
        keywords=", ".join(section.get("target_keywords", [])),
        subsections=json.dumps(section.get("subsections", []), ensure_ascii=False, indent=2),
        relevant_sources=json.dumps(relevant_sources, ensure_ascii=False, indent=2),
        main_keyword=structure["metadata"].get("main_keyword", ""),
        target_audience=research_data["phase1_params"].get("target_audience", "")
    )
    
    # Generate section content
    content = claude.generate_completion(
        prompt=prompt,
        system_prompt="""You are an expert content writer specializing in creating 
        high-quality, SEO-optimized articles. Write in a natural, engaging style while 
        maintaining factual accuracy and incorporating evidence from provided sources.
        
        Important guidelines:
        - Write in Japanese
        - Use natural keyword integration (2.5-3.5% density)
        - Avoid absolute statements (絶対に、必ず、100%)
        - Avoid vague expressions
        - Cite sources naturally within the text
        - Maintain consistent tone throughout""",
        temperature=0.7,
        max_tokens=4000,
        metadata={"phase": "writing", "section": section["section_id"]}
    )
    
    # Count words and validate
    word_count = count_japanese_characters(content)
    
    return {
        "section_id": section["section_id"],
        "title": section["h2_title"],
        "content": content,
        "word_count": word_count,
        "target_word_count": section["word_count_target"],
        "keywords_used": extract_keywords_from_content(content, section.get("target_keywords", []))
    }


def get_relevant_sources_for_section(section: dict, categorized_sources: dict) -> List[dict]:
    """Get sources relevant to a specific section"""
    relevant_sources = []
    
    # Keywords to search for in sources
    search_terms = [section["h2_title"]] + section.get("target_keywords", [])
    
    for category, sources in categorized_sources.items():
        for source in sources:
            # Check if source is relevant to this section
            source_text = f"{source.get('title', '')} {source.get('key_info', '')}".lower()
            
            for term in search_terms:
                if term.lower() in source_text:
                    relevant_sources.append({
                        "category": category,
                        "title": source.get("title"),
                        "url": source.get("url"),
                        "key_info": source.get("key_info")
                    })
                    break
    
    # Limit to most relevant sources
    return relevant_sources[:5]


def write_introduction(structure: dict, research_data: dict, claude: ClaudeAPI) -> str:
    """Write the article introduction"""
    
    intro_data = structure["introduction"]
    
    prompt = f"""
    以下の構成に基づいて、魅力的な記事の導入部を書いてください：
    
    フック: {intro_data["hook"]}
    背景: {intro_data["background"]}
    論旨: {intro_data["thesis"]}
    プレビュー: {json.dumps(intro_data["preview"], ensure_ascii=False)}
    
    ターゲット読者: {research_data["phase1_params"].get("target_audience", "")}
    メインキーワード: {research_data["phase1_params"]["analysis"]["main_keyword"]}
    
    要件:
    - 300-400文字
    - 読者の興味を引く
    - 記事の価値を明確に伝える
    - 自然にキーワードを含める
    """
    
    return claude.generate_completion(
        prompt=prompt,
        temperature=0.8,
        max_tokens=1000,
        metadata={"phase": "writing", "section": "introduction"}
    )


def write_faq_section(structure: dict, research_data: dict, claude: ClaudeAPI) -> str:
    """Write the FAQ section"""
    
    faq_data = structure["faq_section"]["questions"]
    
    faq_content = []
    faq_content.append("## よくある質問")
    
    for i, qa in enumerate(faq_data, 1):
        prompt = f"""
        以下のFAQ項目について、簡潔で有益な回答を書いてください：
        
        質問: {qa["question"]}
        回答の概要: {qa["answer_outline"]}
        エビデンスソース: {qa.get("evidence_source", "")}
        
        要件:
        - 150-200文字
        - 具体的で実用的な回答
        - 信頼性のある情報源に基づく
        """
        
        answer = claude.generate_completion(
            prompt=prompt,
            temperature=0.6,
            max_tokens=500,
            metadata={"phase": "writing", "section": f"faq_{i}"}
        )
        
        faq_content.append(f"\n### Q{i}. {qa['question']}")
        faq_content.append(answer)
    
    return "\n".join(faq_content)


def write_conclusion(structure: dict, article_sections: List[dict], claude: ClaudeAPI) -> str:
    """Write the article conclusion"""
    
    conclusion_data = structure["conclusion"]
    
    # Summarize key points from sections
    section_summaries = [
        f"- {section['title']}: {section['content'][:100]}..."
        for section in article_sections[:3]
    ]
    
    prompt = f"""
    以下の構成に基づいて、効果的な記事の結論を書いてください：
    
    要約ポイント: {json.dumps(conclusion_data["summary_points"], ensure_ascii=False)}
    CTA: {conclusion_data["call_to_action"]}
    将来の展望: {conclusion_data["future_outlook"]}
    
    記事の主要セクション:
    {chr(10).join(section_summaries)}
    
    要件:
    - 300-400文字
    - 記事の価値を再確認
    - 行動を促す
    - 前向きなトーンで締める
    """
    
    return claude.generate_completion(
        prompt=prompt,
        temperature=0.7,
        max_tokens=1000,
        metadata={"phase": "writing", "section": "conclusion"}
    )


def count_japanese_characters(text: str) -> int:
    """Count characters in Japanese text (excluding spaces and punctuation)"""
    # Simple character count - can be enhanced with proper Japanese text processing
    import re
    # Remove spaces, newlines, and common punctuation
    cleaned = re.sub(r'[\s\n。、！？「」『』（）【】〈〉《》・…]', '', text)
    return len(cleaned)


def extract_keywords_from_content(content: str, target_keywords: List[str]) -> Dict[str, int]:
    """Extract and count keyword occurrences in content"""
    keyword_counts = {}
    content_lower = content.lower()
    
    for keyword in target_keywords:
        count = content_lower.count(keyword.lower())
        if count > 0:
            keyword_counts[keyword] = count
    
    return keyword_counts


def calculate_keyword_density(content: str, keyword: str) -> float:
    """Calculate keyword density percentage"""
    word_count = count_japanese_characters(content)
    if word_count == 0:
        return 0.0
    
    keyword_count = content.lower().count(keyword.lower())
    keyword_length = len(keyword)
    
    return (keyword_count * keyword_length / word_count) * 100


def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging("phase4_writing", args.log_level)
    log_phase_start(logger, "Phase 4: Writing")
    
    try:
        # Validate environment
        validate_environment()
        
        # Load configuration
        config = Config()
        
        # Initialize Claude API
        claude = ClaudeAPI()
        
        # Read input data
        structure = read_json(args.structure_file)
        research_data = read_json(args.research_file)
        
        logger.info(f"Writing article: {structure['title']}")
        
        # Write introduction
        logger.info("Writing introduction...")
        introduction = write_introduction(structure, research_data, claude)
        
        # Write main sections
        article_sections = []
        total_word_count = count_japanese_characters(introduction)
        
        for i, section in enumerate(structure["main_sections"], 1):
            logger.info(f"Writing section {i}/{len(structure['main_sections'])}: {section['h2_title']}")
            
            section_result = write_section(
                section,
                structure,
                research_data,
                claude,
                config
            )
            
            article_sections.append(section_result)
            total_word_count += section_result["word_count"]
            
            # Log progress
            log_metric(logger, f"section_{i}_words", section_result["word_count"])
        
        # Write FAQ section
        logger.info("Writing FAQ section...")
        faq_content = write_faq_section(structure, research_data, claude)
        total_word_count += count_japanese_characters(faq_content)
        
        # Write conclusion
        logger.info("Writing conclusion...")
        conclusion = write_conclusion(structure, article_sections, claude)
        total_word_count += count_japanese_characters(conclusion)
        
        # Assemble full article
        article_parts = [
            f"# {structure['title']}",
            "",
            introduction,
            ""
        ]
        
        for section in article_sections:
            article_parts.extend([
                f"## {section['title']}",
                "",
                section['content'],
                ""
            ])
        
        article_parts.extend([
            faq_content,
            "",
            "## まとめ",
            "",
            conclusion
        ])
        
        full_article = "\n".join(article_parts)
        
        # Calculate final metrics
        main_keyword = research_data["phase1_params"]["analysis"]["main_keyword"]
        keyword_density = calculate_keyword_density(full_article, main_keyword)
        
        # Save outputs
        output_file = Path(args.output_dir) / "phase4_article.md"
        write_text(full_article, output_file)
        
        # Save metadata
        metadata = {
            "title": structure["title"],
            "total_word_count": total_word_count,
            "target_word_count": int(research_data["phase1_params"].get("word_count", 3200)),
            "main_keyword": main_keyword,
            "keyword_density": round(keyword_density, 2),
            "sections": article_sections,
            "created_at": datetime.utcnow().isoformat()
        }
        
        metadata_file = Path(args.output_dir) / "phase4_metadata.json"
        write_json(metadata, metadata_file)
        
        # Log final metrics
        log_metric(logger, "total_words", total_word_count)
        log_metric(logger, "keyword_density", keyword_density, "%")
        
        # Check word count
        if abs(total_word_count - 3200) > 300:
            logger.warning(f"Word count {total_word_count} is outside target range (3200±300)")
        
        logger.info(f"Article writing completed: {total_word_count} characters")
        
        log_phase_end(logger, "Phase 4: Writing", success=True)
        
    except Exception as e:
        log_error(logger, e, "Phase 4")
        log_phase_end(logger, "Phase 4: Writing", success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()