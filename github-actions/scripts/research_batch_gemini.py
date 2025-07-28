#!/usr/bin/env python3
"""Research batch execution using Gemini API with google_search tool"""

import os
import sys
import json
import google.generativeai as genai
from datetime import datetime

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 research_batch_gemini.py <batch_number>")
        sys.exit(1)
    
    batch_num = int(sys.argv[1])
    
    # Configure Gemini
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found")
        sys.exit(1)
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # バッチクエリを読み込み
    try:
        with open(f'research_batch_{batch_num}.json', 'r') as f:
            batch_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: research_batch_{batch_num}.json not found")
        sys.exit(1)
    
    queries = batch_data.get('queries', [])
    results = []
    
    print(f"🔍 Starting batch {batch_num} with {len(queries)} queries...")
    
    for i, query in enumerate(queries):
        print(f"Searching batch {batch_num} ({i+1}/{len(queries)}): {query}")
        
        prompt = f"""
Web検索を実行: "{query}"

優先順位：
1. 政府機関（.go.jp, .gov）
2. 学術機関（.ac.jp, .edu）  
3. 医学会・専門団体
4. 大手メディア

以下の形式でJSONで返してください：
{{
  "query": "{query}",
  "results": [
    {{
      "url": "URL",
      "title": "タイトル", 
      "source_type": "government/academic/medical/industry/media",
      "reliability_score": 1-10,
      "key_findings": ["重要な発見"],
      "publication_date": "YYYY-MM-DD"
    }}
  ]
}}
"""
        
        try:
            response = model.generate_content(
                prompt,
                tools=['google_search'],
                generation_config=genai.GenerationConfig(
                    temperature=1.0,
                    max_output_tokens=2048
                )
            )
            
            text = response.text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                result = json.loads(text[json_start:json_end])
                results.append(result)
            else:
                print(f"⚠️ No valid JSON in response for: {query}")
                
        except Exception as e:
            print(f"❌ Error searching '{query}': {e}")
    
    # バッチ結果を保存
    os.makedirs(f'batch_{batch_num}', exist_ok=True)
    output_data = {
        'batch_id': batch_num,
        'results': results,
        'sources': [r.get('results', [{}])[0].get('url', '') for r in results if r.get('results')],
        'key_findings': [finding for r in results for result in r.get('results', []) for finding in result.get('key_findings', [])],
        'timestamp': datetime.now().isoformat(),
        'total_queries': len(queries),
        'successful_queries': len(results)
    }
    
    with open(f'batch_{batch_num}/phase2_research.json', 'w') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Batch {batch_num} completed: {len(results)}/{len(queries)} successful")

if __name__ == "__main__":
    main()