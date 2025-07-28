#!/usr/bin/env python3
"""V4 Simple Research - V2 style single process research"""

import os
import sys
import json
import google.generativeai as genai
from datetime import datetime
import time

def main():
    print("🔍 Starting V4 simple research process...")
    
    # Configure Gemini
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found")
        sys.exit(1)
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Load phase1 analysis
    try:
        with open('phase1_output.json', 'r') as f:
            phase1_data = json.load(f)
        
        queries = phase1_data.get('analysis', {}).get('research_queries', [])
        if not queries:
            print("⚠️ No research queries found in phase1_output.json - using fallback queries")
            queries = [
                "爪が薄い・割れやすい悩みを解決する専門ケアとは？ とは",
                "爪が薄い・割れやすい悩みを解決する専門ケアとは？ 方法",
                "爪が薄い・割れやすい悩みを解決する専門ケアとは？ 効果",
                "爪が薄い・割れやすい悩みを解決する専門ケアとは？ 注意点",
                "爪が薄い・割れやすい悩みを解決する専門ケアとは？ おすすめ",
                "爪が薄い・割れやすい悩みを解決する専門ケアとは？ 初心者",
                "爪が薄い・割れやすい悩みを解決する専門ケアとは？ やり方",
                "爪が薄い・割れやすい悩みを解決する専門ケアとは？ コツ",
                "爪が薄い・割れやすい悩みを解決する専門ケアとは？ 専門家",
                "爪が薄い・割れやすい悩みを解決する専門ケアとは？ 最新"
            ]
        
        print(f"📋 Using {len(queries)} research queries from analysis")
        
    except Exception as e:
        print(f"❌ Error loading phase1 data: {e}")
        queries = [
            "爪が薄い・割れやすい悩みを解決する専門ケアとは？ とは",
            "爪が薄い・割れやすい悩みを解決する専門ケアとは？ 方法", 
            "爪が薄い・割れやすい悩みを解決する専門ケアとは？ 効果",
            "爪が薄い・割れやすい悩みを解決する専門ケアとは？ 注意点",
            "爪が薄い・割れやすい悩みを解決する専門ケアとは？ おすすめ"
        ]
    
    print(f"🚀 Processing {len(queries)} research queries...")
    
    search_results = []
    successful_searches = 0
    
    for i, query in enumerate(queries):
        print(f"🔍 Searching ({i+1}/{len(queries)}): {query}")
        
        try:
            # Use updated Gemini API syntax
            response = model.generate_content(
                query,
                tools=['google_search'],
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2048
                )
            )
            
            # Process the response
            content = response.text if response.text else ""
            
            if content:
                print(f"✅ Got response for '{query}': {len(content)} chars")
                successful_searches += 1
                
                search_results.append({
                    "query": query,
                    "results": [content],
                    "content": content,
                    "success": True,
                    "timestamp": datetime.utcnow().isoformat()
                })
            else:
                print(f"⚠️ Empty response for '{query}'")
                search_results.append({
                    "query": query,
                    "results": [],
                    "content": "",
                    "success": False,
                    "error": "Empty response",
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            # Add delay to avoid rate limiting (V2 style)
            time.sleep(3)
            
        except Exception as e:
            print(f"❌ Error searching '{query}': {e}")
            search_results.append({
                "query": query,
                "results": [],
                "content": "",
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            })
    
    # Create V2-style research_results.json
    research_output = {
        "results": search_results,
        "sources": [r["content"] for r in search_results if r["success"]],
        "key_findings": [r["query"] for r in search_results if r["success"]],
        "total_queries": len(queries),
        "successful_queries": successful_searches,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    with open('research_results.json', 'w', encoding='utf-8') as f:
        json.dump(research_output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Research completed: {successful_searches}/{len(queries)} successful searches")
    print(f"📄 Research results saved to research_results.json ({len(json.dumps(research_output))} bytes)")
    
    # Verify file was created successfully
    if os.path.exists('research_results.json'):
        file_size = os.path.getsize('research_results.json')
        print(f"✅ File verification: research_results.json exists ({file_size} bytes)")
        
        if successful_searches == 0:
            print("⚠️ WARNING: No successful searches - research_results.json contains empty data")
        else:
            print(f"🎯 SUCCESS: {successful_searches} successful searches completed")
    else:
        print("❌ ERROR: research_results.json was not created!")
        sys.exit(1)

if __name__ == "__main__":
    main()