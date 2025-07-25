#!/usr/bin/env python3
"""Phase 2: Research - Using Gemini CLI for real web search"""

import argparse
import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import tempfile

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.file_utils import read_json, write_json, write_text
from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Phase 2: Research with Gemini CLI")
    parser.add_argument("--params-file", required=True, help="Phase 1 output JSON file")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    return parser.parse_args()


def setup_gemini_cli(logger):
    """Setup and verify Gemini CLI"""
    try:
        # Install Gemini CLI if not present
        result = subprocess.run(["gemini", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.info("Installing Gemini CLI...")
            subprocess.run(["npm", "install", "-g", "@google/generative-ai-cli"], check=True)
    except FileNotFoundError:
        logger.error("Node.js/npm not found. Cannot install Gemini CLI")
        raise
    
    # Verify API key
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY not found in environment")


def execute_gemini_search(query: str, logger) -> Dict[str, Any]:
    """Execute a single search using Gemini CLI"""
    
    prompt = f"""
    Web検索を実行してください: "{query}"
    
    以下の優先度で信頼性の高い情報源を重視してください：
    - 政府機関（.go.jp, .gov）
    - 学術機関（.ac.jp, .edu）
    - 業界団体、専門協会
    - 大手メディア
    
    各検索結果について以下の形式でJSONで返してください：
    {{
        "query": "{query}",
        "results": [
            {{
                "url": "実際のURL",
                "title": "ページタイトル",
                "source_type": "government/academic/medical/industry/media",
                "reliability_score": 1-10,
                "key_findings": ["重要な発見"],
                "publication_date": "公開日（分かれば）"
            }}
        ]
    }}
    """
    
    try:
        # Execute Gemini CLI with web search tool
        cmd = [
            "gemini", "chat",
            "--model", "gemini-2.0-flash-exp",
            "--tools", "web_search",
            "--temperature", "1.0",  # Recommended for grounding
            "--max-tokens", "2048",
            "--format", "json",
            "-p", prompt
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=60
        )
        
        if result.returncode != 0:
            raise Exception(f"Gemini CLI failed: {result.stderr}")
        
        # Parse JSON response
        try:
            response_data = json.loads(result.stdout)
            return response_data
        except json.JSONDecodeError:
            # Try to extract JSON from output
            output = result.stdout
            json_start = output.find('{')
            json_end = output.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                return json.loads(output[json_start:json_end])
            else:
                raise
                
    except subprocess.TimeoutExpired:
        logger.error(f"Search timeout for query: {query}")
        return {"query": query, "results": [], "error": "timeout"}
    except Exception as e:
        logger.error(f"Search failed for '{query}': {str(e)}")
        return {"query": query, "results": [], "error": str(e)}


def batch_search_with_gemini_cli(queries: List[str], logger, batch_size: int = 5) -> List[Dict[str, Any]]:
    """Execute searches in batches using Gemini CLI"""
    
    all_results = []
    total_queries = len(queries)
    
    for i in range(0, total_queries, batch_size):
        batch = queries[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total_queries + batch_size - 1) // batch_size
        
        logger.info(f"Processing batch {batch_num}/{total_batches}")
        
        for j, query in enumerate(batch):
            logger.info(f"Searching ({i+j+1}/{total_queries}): {query}")
            result = execute_gemini_search(query, logger)
            all_results.append(result)
            
            # Rate limiting
            if j < len(batch) - 1:
                time.sleep(2)  # 2 second delay between searches
    
    return all_results


def process_search_results(raw_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process and structure search results"""
    
    processed = {
        "search_results": [],
        "statistics": {
            "total_queries": len(raw_results),
            "successful_queries": 0,
            "total_results": 0,
            "priority_distribution": {
                "government": 0,
                "academic": 0,
                "medical": 0,
                "industry": 0,
                "media": 0
            }
        }
    }
    
    for search_result in raw_results:
        if "error" not in search_result and search_result.get("results"):
            processed["statistics"]["successful_queries"] += 1
            
            processed_results = []
            for result in search_result.get("results", []):
                source_type = result.get("source_type", "media")
                
                # Map to priority
                priority_map = {
                    "government": "very_high",
                    "academic": "high",
                    "medical": "high",
                    "industry": "medium_high",
                    "media": "medium"
                }
                
                processed_result = {
                    "url": result.get("url", ""),
                    "title": result.get("title", ""),
                    "snippet": " ".join(result.get("key_findings", [])),
                    "priority": priority_map.get(source_type, "medium"),
                    "source_type": source_type,
                    "reliability_score": result.get("reliability_score", 5),
                    "key_facts": result.get("key_findings", []),
                    "publication_date": result.get("publication_date", "")
                }
                
                processed_results.append(processed_result)
                processed["statistics"]["total_results"] += 1
                
                if source_type in processed["statistics"]["priority_distribution"]:
                    processed["statistics"]["priority_distribution"][source_type] += 1
            
            processed["search_results"].append({
                "query": search_result.get("query", ""),
                "results": processed_results,
                "timestamp": datetime.utcnow().isoformat(),
                "result_count": len(processed_results)
            })
        else:
            # Failed search
            processed["search_results"].append({
                "query": search_result.get("query", ""),
                "results": [],
                "error": search_result.get("error", "unknown"),
                "timestamp": datetime.utcnow().isoformat(),
                "result_count": 0
            })
    
    return processed


def extract_key_sources(research_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and categorize key sources"""
    
    all_sources = []
    for search_result in research_data["search_results"]:
        for result in search_result.get("results", []):
            all_sources.append({
                **result,
                "query": search_result["query"]
            })
    
    # Filter high-priority sources
    high_priority_sources = [
        s for s in all_sources 
        if s["priority"] in ["very_high", "high"] or s["reliability_score"] >= 7
    ]
    
    # Sort by reliability and priority
    high_priority_sources.sort(
        key=lambda x: (x["reliability_score"], -["very_high", "high", "medium_high", "medium", "low"].index(x["priority"])),
        reverse=True
    )
    
    # Categorize
    categorized = {
        "government_sources": [s for s in high_priority_sources if s["source_type"] == "government"],
        "academic_sources": [s for s in high_priority_sources if s["source_type"] == "academic"],
        "medical_sources": [s for s in high_priority_sources if s["source_type"] == "medical"],
        "industry_sources": [s for s in high_priority_sources if s["source_type"] == "industry"],
        "media_sources": [s for s in high_priority_sources if s["source_type"] == "media"]
    }
    
    return {
        "high_priority_sources": high_priority_sources[:20],
        "categorized_sources": categorized,
        "source_count": len(high_priority_sources)
    }


def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging("phase2_research_gemini_cli", args.log_level)
    log_phase_start(logger, "Phase 2: Research (Gemini CLI)")
    
    try:
        # Setup Gemini CLI
        setup_gemini_cli(logger)
        
        # Read Phase 1 output
        params = read_json(args.params_file)
        logger.info(f"Starting research for topic: {params.get('topic')}")
        
        # Get research queries from Phase 1
        queries = params.get("analysis", {}).get("research_queries", [])
        
        # Add additional topic-specific queries
        main_keyword = params["analysis"].get("main_keyword", params["topic"])
        additional_queries = [
            f"{main_keyword} 最新情報 2025",
            f"{main_keyword} 効果 研究結果",
            f"{main_keyword} 専門家 意見",
            f"{main_keyword} 注意点 リスク"
        ]
        
        # Combine and deduplicate
        all_queries = list(dict.fromkeys(queries + additional_queries))[:25]
        logger.info(f"Executing {len(all_queries)} search queries")
        
        # Execute searches
        start_time = time.time()
        raw_results = batch_search_with_gemini_cli(all_queries, logger)
        elapsed_time = time.time() - start_time
        
        # Process results
        research_data = process_search_results(raw_results)
        
        # Log metrics
        log_metric(logger, "research_time", elapsed_time, "seconds")
        log_metric(logger, "total_results", research_data["statistics"]["total_results"])
        log_metric(logger, "successful_queries", research_data["statistics"]["successful_queries"])
        
        # Extract sources
        source_analysis = extract_key_sources(research_data)
        
        # Final output
        final_output = {
            "phase1_params": params,
            "research_queries": all_queries,
            "research_data": research_data,
            "source_analysis": source_analysis,
            "metadata": {
                "phase": "research",
                "search_method": "gemini_cli_web_search",
                "completed_at": datetime.utcnow().isoformat(),
                "execution_time": elapsed_time
            }
        }
        
        # Save outputs
        output_file = Path(args.output_dir) / "phase2_research.json"
        write_json(final_output, output_file)
        
        # Save human-readable summary
        summary_file = Path(args.output_dir) / "research_summary.md"
        write_research_summary(final_output, summary_file)
        
        logger.info(f"Research completed: {research_data['statistics']['successful_queries']}/{len(all_queries)} successful")
        logger.info("Using Gemini CLI with real web search")
        
        log_phase_end(logger, "Phase 2: Research (Gemini CLI)", success=True)
        
    except Exception as e:
        log_error(logger, e, "Phase 2")
        log_phase_end(logger, "Phase 2: Research (Gemini CLI)", success=False)
        sys.exit(1)


def write_research_summary(data: Dict[str, Any], output_path: Path):
    """Write a human-readable research summary"""
    lines = [
        f"# Research Summary - {data['phase1_params']['topic']}\n",
        f"Generated: {data['metadata']['completed_at']}",
        f"Method: Gemini CLI Web Search\n",
        f"## Statistics",
        f"- Total queries: {data['research_data']['statistics']['total_queries']}",
        f"- Successful queries: {data['research_data']['statistics']['successful_queries']}",
        f"- Total sources found: {data['research_data']['statistics']['total_results']}\n",
        "## Source Distribution",
        f"- Government: {data['research_data']['statistics']['priority_distribution']['government']}",
        f"- Academic: {data['research_data']['statistics']['priority_distribution']['academic']}",
        f"- Medical: {data['research_data']['statistics']['priority_distribution']['medical']}",
        f"- Industry: {data['research_data']['statistics']['priority_distribution']['industry']}",
        f"- Media: {data['research_data']['statistics']['priority_distribution']['media']}\n",
        "## High-Priority Sources\n"
    ]
    
    for i, source in enumerate(data['source_analysis']['high_priority_sources'][:10], 1):
        lines.append(f"### {i}. {source['title']}")
        lines.append(f"- URL: {source['url']}")
        lines.append(f"- Type: {source['source_type']}")
        lines.append(f"- Reliability: {source['reliability_score']}/10")
        if source.get('publication_date'):
            lines.append(f"- Date: {source['publication_date']}")
        if source.get('key_facts'):
            lines.append("- Key facts:")
            for fact in source['key_facts'][:3]:
                lines.append(f"  - {fact}")
        lines.append("")
    
    write_text('\n'.join(lines), output_path)


if __name__ == "__main__":
    import os
    main()