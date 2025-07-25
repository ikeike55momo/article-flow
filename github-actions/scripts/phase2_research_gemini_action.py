#!/usr/bin/env python3
"""Phase 2: Research - Using Gemini API directly in GitHub Actions"""

import argparse
import sys
import os
import json
import time
import asyncio
import aiohttp
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.claude_api import ClaudeAPI
from utils.file_utils import read_json, write_json, read_prompt, write_text
from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric
from utils.config import Config


class GeminiSearchAPI:
    """Direct Gemini API integration for web search"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-pro"
        
    async def search_and_analyze(self, query: str, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Perform web search using Gemini with grounding"""
        
        prompt = f"""
        Perform a web search for the following query and return accurate, up-to-date results from reliable sources:
        
        Query: {query}
        
        Requirements:
        1. Use web grounding to find real, current information
        2. Prioritize official sources (.gov, .edu, academic journals)
        3. Include publication dates and source credibility
        4. Return structured data with URLs, titles, and key findings
        
        Format the response as JSON:
        {{
            "results": [
                {{
                    "url": "actual URL",
                    "title": "page title",
                    "source_type": "government/academic/medical/industry/media",
                    "date": "publication date if available",
                    "reliability_score": 1-10,
                    "key_findings": ["finding 1", "finding 2"],
                    "relevant_quote": "exact quote if important"
                }}
            ]
        }}
        """
        
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }
        
        data = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 2048,
                "topP": 0.8,
                "topK": 10
            },
            "tools": [{
                "googleSearchRetrieval": {
                    "dynamicRetrievalConfig": {
                        "mode": "MODE_DYNAMIC",
                        "dynamicThreshold": 0.3
                    }
                }
            }]
        }
        
        try:
            async with session.post(
                f"{self.base_url}/{self.model}:generateContent",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    # Extract text from response
                    text_response = result['candidates'][0]['content']['parts'][0]['text']
                    
                    # Parse JSON from response
                    json_start = text_response.find('{')
                    json_end = text_response.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        search_results = json.loads(text_response[json_start:json_end])
                        return {
                            "query": query,
                            "results": search_results.get("results", []),
                            "timestamp": datetime.utcnow().isoformat()
                        }
                else:
                    error_text = await response.text()
                    raise Exception(f"Gemini API error {response.status}: {error_text}")
                    
        except Exception as e:
            print(f"Search error for '{query}': {str(e)}")
            return {
                "query": query,
                "results": [],
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Phase 2: Research with Gemini API")
    parser.add_argument("--params-file", required=True, help="Phase 1 output JSON file")
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument("--parallel-searches", type=int, default=5, help="Number of parallel searches")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    return parser.parse_args()


def generate_search_queries(params: dict, claude: ClaudeAPI) -> List[str]:
    """Generate comprehensive search queries based on analysis"""
    
    base_queries = params.get("analysis", {}).get("research_queries", [])
    prompt_template = read_prompt("01_research")
    
    prompt = prompt_template.format(
        topic=params["topic"],
        main_keyword=params["analysis"].get("main_keyword", params["topic"]),
        related_keywords=", ".join(params["analysis"].get("related_keywords", [])),
        target_audience=params.get("target_audience", ""),
        existing_queries="\n".join(base_queries)
    )
    
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
    
    all_queries = base_queries.copy()
    for query_type, queries in response.items():
        if isinstance(queries, list):
            all_queries.extend(queries)
    
    seen = set()
    unique_queries = []
    for q in all_queries:
        if q not in seen:
            seen.add(q)
            unique_queries.append(q)
    
    return unique_queries[:25]


async def perform_parallel_searches(
    queries: List[str],
    api_key: str,
    max_concurrent: int = 5
) -> List[Dict[str, Any]]:
    """Perform searches in parallel using Gemini API"""
    
    gemini = GeminiSearchAPI(api_key)
    results = []
    
    async with aiohttp.ClientSession() as session:
        # Process in batches
        for i in range(0, len(queries), max_concurrent):
            batch = queries[i:i + max_concurrent]
            
            # Create tasks for batch
            tasks = [
                gemini.search_and_analyze(query, session)
                for query in batch
            ]
            
            # Execute batch
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            
            # Small delay between batches
            if i + max_concurrent < len(queries):
                await asyncio.sleep(1)
    
    return results


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
            
            # Process each result
            processed_results = []
            for result in search_result["results"]:
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
                    "publication_date": result.get("date", ""),
                    "relevant_quote": result.get("relevant_quote", "")
                }
                
                processed_results.append(processed_result)
                processed["statistics"]["total_results"] += 1
                
                if source_type in processed["statistics"]["priority_distribution"]:
                    processed["statistics"]["priority_distribution"][source_type] += 1
            
            processed["search_results"].append({
                "query": search_result["query"],
                "results": processed_results,
                "timestamp": search_result["timestamp"],
                "result_count": len(processed_results)
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
    
    logger = setup_logging("phase2_research_gemini", args.log_level)
    log_phase_start(logger, "Phase 2: Research (Gemini API)")
    
    try:
        # Check API key
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_AI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_AI_API_KEY not found in environment")
        
        # Initialize
        config = Config()
        claude = ClaudeAPI()
        
        # Read Phase 1 output
        params = read_json(args.params_file)
        logger.info(f"Starting research for topic: {params.get('topic')}")
        
        # Generate queries
        queries = generate_search_queries(params, claude)
        logger.info(f"Generated {len(queries)} search queries")
        
        # Perform searches
        start_time = time.time()
        raw_results = asyncio.run(perform_parallel_searches(
            queries,
            api_key,
            args.parallel_searches
        ))
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
            "research_queries": queries,
            "research_data": research_data,
            "source_analysis": source_analysis,
            "metadata": {
                "phase": "research",
                "search_method": "gemini_api_grounding",
                "completed_at": datetime.utcnow().isoformat(),
                "execution_time": elapsed_time
            }
        }
        
        # Save outputs
        output_file = Path(args.output_dir) / "phase2_research.json"
        write_json(final_output, output_file)
        
        logger.info(f"Research completed with {research_data['statistics']['successful_queries']} successful queries")
        logger.info("Using Gemini API with web grounding")
        
        log_phase_end(logger, "Phase 2: Research (Gemini API)", success=True)
        
    except Exception as e:
        log_error(logger, e, "Phase 2")
        log_phase_end(logger, "Phase 2: Research (Gemini API)", success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()