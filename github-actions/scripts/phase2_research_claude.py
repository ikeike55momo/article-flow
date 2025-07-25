#!/usr/bin/env python3
"""Phase 2: Research - Using Claude's web search capability (No Bing API required)"""

import argparse
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.claude_api import ClaudeAPI
from utils.claude_web_search import ClaudeWebSearch
from utils.file_utils import read_json, write_json, read_prompt
from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric
from utils.config import Config, validate_environment


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Phase 2: Research with Claude")
    parser.add_argument("--params-file", required=True, help="Phase 1 output JSON file")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--parallel-batches", type=int, default=3, help="Number of parallel search batches")
    parser.add_argument("--searches-per-batch", type=int, default=5, help="Searches per batch")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    return parser.parse_args()


def generate_search_queries(params: dict, claude: ClaudeAPI) -> List[str]:
    """Generate comprehensive search queries based on analysis"""
    
    # Start with queries from Phase 1
    base_queries = params.get("analysis", {}).get("research_queries", [])
    
    # Read research prompt template
    prompt_template = read_prompt("01_research")
    
    # Generate additional queries
    prompt = prompt_template.format(
        topic=params["topic"],
        main_keyword=params["analysis"].get("main_keyword", params["topic"]),
        related_keywords=", ".join(params["analysis"].get("related_keywords", [])),
        target_audience=params.get("target_audience", ""),
        existing_queries="\n".join(base_queries)
    )
    
    # Get additional queries from Claude
    response = claude.generate_with_structured_output(
        prompt=prompt,
        system_prompt="You are a research specialist who generates comprehensive search queries for in-depth article research.",
        expected_format={
            "technical_queries": ["string"],
            "academic_queries": ["string"],
            "practical_queries": ["string"],
            "local_queries": ["string"],
            "competitor_queries": ["string"],
            "statistics_queries": ["string"]
        },
        temperature=0.5,
        metadata={"phase": "research_query_generation"}
    )
    
    # Combine all queries
    all_queries = base_queries.copy()
    for query_type, queries in response.items():
        if isinstance(queries, list):
            all_queries.extend(queries)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_queries = []
    for q in all_queries:
        if q not in seen:
            seen.add(q)
            unique_queries.append(q)
    
    return unique_queries[:25]  # Limit to 25 queries as per requirements


def process_search_batch(
    queries: List[str],
    searcher: ClaudeWebSearch,
    logger
) -> List[Dict[str, Any]]:
    """Process a batch of search queries using Claude"""
    
    batch_results = []
    
    for query in queries:
        try:
            logger.info(f"Searching: {query}")
            results = searcher.search_and_analyze(query, num_results=10)
            
            batch_results.append({
                "query": query,
                "results": results,
                "timestamp": datetime.utcnow().isoformat(),
                "result_count": len(results)
            })
            
            # Small delay between searches
            time.sleep(0.5)
            
        except Exception as e:
            log_error(logger, e, f"Search query: {query}")
            batch_results.append({
                "query": query,
                "results": [],
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
    
    return batch_results


def parallel_research_claude(
    queries: List[str],
    parallel_batches: int,
    searches_per_batch: int,
    logger
) -> Dict[str, Any]:
    """Execute research queries in parallel batches using Claude"""
    
    searcher = ClaudeWebSearch()
    all_results = []
    
    # Split queries into batches
    batches = []
    for i in range(0, len(queries), searches_per_batch):
        batches.append(queries[i:i + searches_per_batch])
    
    # Process batches in parallel
    with ThreadPoolExecutor(max_workers=parallel_batches) as executor:
        # Submit all batches
        future_to_batch = {
            executor.submit(process_search_batch, batch, searcher, logger): batch
            for batch in batches
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_batch):
            batch = future_to_batch[future]
            try:
                batch_results = future.result()
                all_results.extend(batch_results)
                logger.info(f"Completed batch with {len(batch_results)} searches")
            except Exception as e:
                log_error(logger, e, f"Batch processing")
    
    # Analyze and summarize results
    total_results = sum(r.get("result_count", 0) for r in all_results)
    priority_distribution = analyze_priority_distribution(all_results)
    
    return {
        "search_results": all_results,
        "statistics": {
            "total_queries": len(queries),
            "successful_queries": len([r for r in all_results if "error" not in r]),
            "total_results": total_results,
            "priority_distribution": priority_distribution,
            "execution_time": datetime.utcnow().isoformat()
        }
    }


def analyze_priority_distribution(results: List[Dict[str, Any]]) -> Dict[str, int]:
    """Analyze the priority distribution of search results"""
    distribution = {
        "very_high": 0,
        "high": 0,
        "medium_high": 0,
        "medium": 0,
        "low": 0
    }
    
    for search_result in results:
        for result in search_result.get("results", []):
            priority = result.get("priority", "medium")
            if priority in distribution:
                distribution[priority] += 1
    
    return distribution


def extract_and_consolidate_sources(research_data: Dict[str, Any], claude_searcher: ClaudeWebSearch) -> Dict[str, Any]:
    """Extract and categorize key sources from research results"""
    
    # Collect all high-priority sources
    all_sources = []
    
    for search_result in research_data["search_results"]:
        all_sources.extend(search_result.get("results", []))
    
    # Filter high-priority sources
    high_priority_sources = [
        source for source in all_sources
        if source.get("priority") in ["very_high", "high"] or
        source.get("reliability_score", 0) >= 7
    ]
    
    # Limit to top sources
    high_priority_sources = sorted(
        high_priority_sources,
        key=lambda x: (x.get("reliability_score", 0), x.get("priority", "")),
        reverse=True
    )[:30]
    
    # Categorize sources by type
    categorized = {
        "government_sources": [],
        "academic_sources": [],
        "medical_sources": [],
        "industry_sources": [],
        "media_sources": []
    }
    
    for source in high_priority_sources:
        domain = source.get("domain", "").lower()
        
        if any(gov in domain for gov in [".go.jp", ".gov", "mhlw", "pmda"]):
            categorized["government_sources"].append(source)
        elif any(edu in domain for edu in [".ac.jp", ".edu", "研究", "大学"]):
            categorized["academic_sources"].append(source)
        elif any(med in domain for med in ["医学会", "医療", "病院", "クリニック"]):
            categorized["medical_sources"].append(source)
        elif any(ind in domain for ind in ["協会", "団体", "組合"]):
            categorized["industry_sources"].append(source)
        else:
            categorized["media_sources"].append(source)
    
    # Extract consolidated facts
    topic = research_data.get("phase1_params", {}).get("topic", "")
    consolidated_facts = claude_searcher.extract_facts_from_sources(
        high_priority_sources,
        topic
    )
    
    return {
        "high_priority_sources": high_priority_sources,
        "categorized_sources": categorized,
        "consolidated_facts": consolidated_facts,
        "source_count": len(high_priority_sources)
    }


def main():
    """Main execution function"""
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging("phase2_research_claude", args.log_level)
    log_phase_start(logger, "Phase 2: Research (Claude Web Search)")
    
    try:
        # Validate environment (only ANTHROPIC_API_KEY needed now)
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        
        # Load configuration
        config = Config()
        
        # Initialize Claude API
        claude = ClaudeAPI()
        claude_searcher = ClaudeWebSearch()
        
        # Read Phase 1 output
        params = read_json(args.params_file)
        logger.info(f"Starting research for topic: {params.get('topic')}")
        
        # Generate search queries
        queries = generate_search_queries(params, claude)
        logger.info(f"Generated {len(queries)} search queries")
        
        # Execute parallel research using Claude
        start_time = time.time()
        research_data = parallel_research_claude(
            queries,
            args.parallel_batches,
            args.searches_per_batch,
            logger
        )
        elapsed_time = time.time() - start_time
        
        # Log metrics
        log_metric(logger, "research_time", elapsed_time, "seconds")
        log_metric(logger, "total_results", research_data["statistics"]["total_results"])
        log_metric(logger, "high_priority_results", 
                  research_data["statistics"]["priority_distribution"]["very_high"] +
                  research_data["statistics"]["priority_distribution"]["high"])
        
        # Extract and consolidate sources
        source_analysis = extract_and_consolidate_sources(research_data, claude_searcher)
        
        # Combine all research data
        final_output = {
            "phase1_params": params,
            "research_queries": queries,
            "research_data": research_data,
            "source_analysis": source_analysis,
            "metadata": {
                "phase": "research",
                "search_method": "claude_web_search",
                "completed_at": datetime.utcnow().isoformat(),
                "execution_time": elapsed_time
            }
        }
        
        # Save output
        output_file = Path(args.output_dir) / "phase2_research.json"
        write_json(final_output, output_file)
        
        logger.info(f"Research completed with {research_data['statistics']['successful_queries']} successful queries")
        logger.info("Using Claude's web search - No Bing API required")
        
        log_phase_end(logger, "Phase 2: Research (Claude Web Search)", success=True)
        
    except Exception as e:
        log_error(logger, e, "Phase 2")
        log_phase_end(logger, "Phase 2: Research (Claude Web Search)", success=False)
        sys.exit(1)


if __name__ == "__main__":
    import os
    main()