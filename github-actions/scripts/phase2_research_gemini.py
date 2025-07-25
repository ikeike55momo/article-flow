#!/usr/bin/env python3
"""Phase 2: Research - Using Gemini CLI for web search"""

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

from utils.claude_api import ClaudeAPI
from utils.file_utils import read_json, write_json, read_prompt, write_text
from utils.logging_utils import setup_logging, log_phase_start, log_phase_end, log_error, log_metric
from utils.config import Config


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Phase 2: Research with Gemini")
    parser.add_argument("--params-file", required=True, help="Phase 1 output JSON file")
    parser.add_argument("--output-dir", required=True, help="Output directory")
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


def create_gemini_research_prompt(queries: List[str], topic: str, target_audience: str) -> str:
    """Create a comprehensive research prompt for Gemini"""
    
    queries_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(queries)])
    
    prompt = f"""
# 記事リサーチタスク

## トピック: {topic}
## ターゲット読者: {target_audience}

以下の検索クエリについて、Web検索を実行し、信頼性の高い情報を収集してください。

## 検索クエリ一覧:
{queries_text}

## リサーチ要件:

### 1. 優先度の高い情報源
- 政府機関（.go.jp, .gov）- 特に厚生労働省、医薬品医療機器総合機構（PMDA）
- 学術機関（.ac.jp, .edu）、医学会、研究所
- 業界団体、専門協会
- 大手メディア（NHK、日経など）

### 2. 収集すべき情報
- 統計データ（数値、パーセンテージ）
- 科学的根拠、研究結果
- 専門家の見解、推奨事項
- 法規制、ガイドライン
- 最新トレンド、業界動向

### 3. 出力形式
各検索結果について、以下の形式でJSON形式で出力してください：

```json
{{
  "search_results": [
    {{
      "query": "検索クエリ",
      "results": [
        {{
          "url": "情報源のURL",
          "title": "ページタイトル",
          "source_type": "government/academic/medical/industry/media",
          "reliability_score": 9,
          "key_findings": [
            "重要な発見1",
            "重要な発見2"
          ],
          "statistics": [
            {{"data": "統計データ", "context": "データの文脈"}}
          ],
          "quotes": [
            {{"quote": "引用文", "author": "発言者/著者"}}
          ]
        }}
      ]
    }}
  ],
  "summary": {{
    "total_sources": 数値,
    "high_reliability_sources": 数値,
    "key_statistics": ["主要な統計データ"],
    "consensus_points": ["複数ソースで一致する点"],
    "areas_needing_verification": ["検証が必要な領域"]
  }}
}}
```

必ず実際のWeb検索を行い、最新かつ正確な情報を収集してください。
架空の情報や推測は含めないでください。
"""
    
    return prompt


def execute_gemini_research(prompt: str, output_dir: Path, logger) -> Dict[str, Any]:
    """Execute research using Gemini CLI"""
    
    # Create temporary file for prompt
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(prompt)
        prompt_file = f.name
    
    try:
        # Prepare Gemini CLI command
        cmd = [
            "gemini",
            "chat",
            "--model", "gemini-pro",
            "--temperature", "0.3",
            "--max-tokens", "8000",
            "--tools", "web_search",
            "--format", "json",
            "--input", prompt_file
        ]
        
        logger.info("Executing Gemini research with web search...")
        
        # Execute Gemini CLI
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            raise Exception(f"Gemini CLI failed: {result.stderr}")
        
        # Parse JSON output
        try:
            research_data = json.loads(result.stdout)
        except json.JSONDecodeError:
            # If not valid JSON, try to extract JSON from output
            output = result.stdout
            json_start = output.find('{')
            json_end = output.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                research_data = json.loads(output[json_start:json_end])
            else:
                raise Exception("Could not parse Gemini output as JSON")
        
        return research_data
        
    except subprocess.TimeoutExpired:
        raise Exception("Gemini research timed out after 5 minutes")
    except Exception as e:
        raise Exception(f"Gemini research failed: {str(e)}")
    finally:
        # Clean up temp file
        if Path(prompt_file).exists():
            Path(prompt_file).unlink()


def process_gemini_results(raw_results: Dict[str, Any]) -> Dict[str, Any]:
    """Process and validate Gemini research results"""
    
    # Ensure required structure
    processed = {
        "search_results": [],
        "statistics": {
            "total_queries": 0,
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
    
    # Process search results
    if "search_results" in raw_results:
        for search_item in raw_results["search_results"]:
            query_results = {
                "query": search_item.get("query", ""),
                "results": [],
                "timestamp": datetime.utcnow().isoformat(),
                "result_count": 0
            }
            
            for result in search_item.get("results", []):
                # Map source type to priority
                source_type = result.get("source_type", "media")
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
                    "statistics": result.get("statistics", []),
                    "quotes": result.get("quotes", [])
                }
                
                query_results["results"].append(processed_result)
                query_results["result_count"] += 1
                
                # Update priority distribution
                if source_type in processed["statistics"]["priority_distribution"]:
                    processed["statistics"]["priority_distribution"][source_type] += 1
            
            processed["search_results"].append(query_results)
            processed["statistics"]["total_queries"] += 1
            if query_results["result_count"] > 0:
                processed["statistics"]["successful_queries"] += 1
            processed["statistics"]["total_results"] += query_results["result_count"]
    
    # Add summary if available
    if "summary" in raw_results:
        processed["summary"] = raw_results["summary"]
    
    return processed


def extract_key_sources(research_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and categorize key sources from research results"""
    
    # Collect all sources
    all_sources = []
    for search_result in research_data["search_results"]:
        for result in search_result.get("results", []):
            all_sources.append({
                "url": result["url"],
                "title": result["title"],
                "snippet": result["snippet"],
                "priority": result["priority"],
                "source_type": result.get("source_type", ""),
                "reliability_score": result.get("reliability_score", 5),
                "key_facts": result.get("key_facts", []),
                "query": search_result["query"]
            })
    
    # Filter high-priority sources
    high_priority_sources = [
        s for s in all_sources 
        if s["priority"] in ["very_high", "high"] or s["reliability_score"] >= 7
    ]
    
    # Sort by reliability and priority
    high_priority_sources.sort(
        key=lambda x: (x["reliability_score"], x["priority"]),
        reverse=True
    )
    
    # Categorize sources
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
    logger = setup_logging("phase2_research_gemini", args.log_level)
    log_phase_start(logger, "Phase 2: Research (Gemini Web Search)")
    
    try:
        # Check Gemini CLI availability
        try:
            subprocess.run(["gemini", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise ValueError("Gemini CLI not found. Please install: npm install -g @google/generative-ai-cli")
        
        # Load configuration
        config = Config()
        
        # Initialize Claude API for query generation
        claude = ClaudeAPI()
        
        # Read Phase 1 output
        params = read_json(args.params_file)
        logger.info(f"Starting research for topic: {params.get('topic')}")
        
        # Generate search queries using Claude
        queries = generate_search_queries(params, claude)
        logger.info(f"Generated {len(queries)} search queries")
        
        # Create Gemini research prompt
        gemini_prompt = create_gemini_research_prompt(
            queries,
            params.get("topic"),
            params.get("target_audience", "")
        )
        
        # Execute research with Gemini
        start_time = time.time()
        raw_results = execute_gemini_research(gemini_prompt, Path(args.output_dir), logger)
        elapsed_time = time.time() - start_time
        
        # Process results
        research_data = process_gemini_results(raw_results)
        
        # Log metrics
        log_metric(logger, "research_time", elapsed_time, "seconds")
        log_metric(logger, "total_results", research_data["statistics"]["total_results"])
        log_metric(logger, "successful_queries", research_data["statistics"]["successful_queries"])
        
        # Extract key sources
        source_analysis = extract_key_sources(research_data)
        
        # Combine all research data
        final_output = {
            "phase1_params": params,
            "research_queries": queries,
            "research_data": research_data,
            "source_analysis": source_analysis,
            "metadata": {
                "phase": "research",
                "search_method": "gemini_web_search",
                "completed_at": datetime.utcnow().isoformat(),
                "execution_time": elapsed_time
            }
        }
        
        # Save output
        output_file = Path(args.output_dir) / "phase2_research.json"
        write_json(final_output, output_file)
        
        # Save human-readable summary
        summary_file = Path(args.output_dir) / "research_summary.md"
        write_research_summary(final_output, summary_file)
        
        logger.info(f"Research completed with {research_data['statistics']['successful_queries']} successful queries")
        logger.info("Using Gemini Web Search - Real web search capability")
        
        log_phase_end(logger, "Phase 2: Research (Gemini Web Search)", success=True)
        
    except Exception as e:
        log_error(logger, e, "Phase 2")
        log_phase_end(logger, "Phase 2: Research (Gemini Web Search)", success=False)
        sys.exit(1)


def write_research_summary(data: Dict[str, Any], output_path: Path):
    """Write a human-readable research summary"""
    lines = [
        f"# Research Summary - {data['phase1_params']['topic']}\n",
        f"Generated: {data['metadata']['completed_at']}\n",
        f"## Statistics",
        f"- Total queries: {data['research_data']['statistics']['total_queries']}",
        f"- Successful queries: {data['research_data']['statistics']['successful_queries']}",
        f"- Total sources found: {data['research_data']['statistics']['total_results']}\n",
        "## High-Priority Sources\n"
    ]
    
    for source in data['source_analysis']['high_priority_sources'][:10]:
        lines.append(f"### {source['title']}")
        lines.append(f"- URL: {source['url']}")
        lines.append(f"- Type: {source['source_type']}")
        lines.append(f"- Reliability: {source['reliability_score']}/10")
        if source.get('key_facts'):
            lines.append("- Key facts:")
            for fact in source['key_facts'][:3]:
                lines.append(f"  - {fact}")
        lines.append("")
    
    write_text('\n'.join(lines), output_path)


if __name__ == "__main__":
    main()