#!/usr/bin/env python3
"""Research batch execution using Gemini API with google_search tool"""

import os
import sys
import json
import traceback
from google import genai
from google.genai import types
from datetime import datetime

def test_api_connection(client):
    """Test the API connection with a simple query"""
    print("\n🧪 Testing API connection...")
    try:
        # Simple test without search tool
        test_response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="Return a simple JSON: {\"status\": \"ok\", \"message\": \"API working\"}"
        )
        
        print(f"Test response: {test_response}")
        print(f"Test response text: {test_response.text}")
        
        # Test with search tool
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )
        
        config = types.GenerateContentConfig(
            tools=[grounding_tool],
            temperature=1.0,
            max_output_tokens=256
        )
        
        search_response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="Search for 'test query' and return a simple JSON with one result",
            config=config
        )
        
        print(f"\nSearch test response: {search_response}")
        print(f"Search test response text: {search_response.text[:200]}...")
        print("✅ API connection test passed\n")
        return True
        
    except Exception as e:
        print(f"❌ API connection test failed: {e}")
        print(f"Traceback:\n{traceback.format_exc()}")
        return False

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
        
    # Configure the client
    client = genai.Client(api_key=api_key)
    
    # Test API connection
    if not test_api_connection(client):
        print("❌ Exiting due to API connection failure")
        sys.exit(1)
    
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
            # Define the grounding tool
            grounding_tool = types.Tool(
                google_search=types.GoogleSearch()
            )
            
            # Configure generation settings
            config = types.GenerateContentConfig(
                tools=[grounding_tool],
                temperature=1.0,
                max_output_tokens=8192  # Increased to handle full JSON responses
            )
            
            # Make the request
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=config
            )
            
            # Debug: Print raw response
            print(f"\n=== DEBUG: Raw response for query '{query}' ===")
            print(f"Response object: {response}")
            print(f"Response type: {type(response)}")
            
            # Check if response has candidates
            if hasattr(response, 'candidates') and response.candidates:
                print(f"Number of candidates: {len(response.candidates)}")
                for idx, candidate in enumerate(response.candidates):
                    print(f"Candidate {idx}: {candidate}")
                    if hasattr(candidate, 'content'):
                        print(f"Candidate {idx} content: {candidate.content}")
            
            try:
                text = response.text
                print(f"Response text length: {len(text) if text else 'None'}")
                print(f"Raw response text:\n{text[:500]}..." if text and len(text) > 500 else f"Raw response text:\n{text}")
            except AttributeError as attr_error:
                print(f"❌ Response has no 'text' attribute: {attr_error}")
                print(f"Response attributes: {dir(response)}")
                
                # Try alternative ways to get content
                if hasattr(response, 'candidates') and response.candidates:
                    for candidate in response.candidates:
                        if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                            for part in candidate.content.parts:
                                if hasattr(part, 'text'):
                                    text = part.text
                                    print(f"Found text in candidate part: {text[:200]}...")
                                    break
                            if 'text' in locals():
                                break
                    else:
                        raise ValueError("Could not extract text from response candidates")
                else:
                    raise
            except Exception as text_error:
                print(f"❌ Error accessing response content: {text_error}")
                print(f"Response type: {type(response)}")
                print(f"Response attributes: {dir(response)}")
                raise
            
            # Try to extract JSON from response
            # Check if JSON is inside a markdown code block
            if '```json' in text:
                # Extract JSON from markdown code block
                json_block_start = text.find('```json') + 7  # Skip ```json
                json_block_end = text.find('```', json_block_start)
                if json_block_start > 6 and json_block_end > json_block_start:
                    text = text[json_block_start:json_block_end].strip()
            
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = text[json_start:json_end]
                print(f"\n=== DEBUG: Extracted JSON string ===")
                print(f"JSON length: {len(json_str)}")
                print(f"First 200 chars: {json_str[:200]}...")
                
                try:
                    result = json.loads(json_str)
                    results.append(result)
                    print(f"✅ Successfully parsed JSON for query: {query}")
                except json.JSONDecodeError as json_error:
                    print(f"❌ JSON decode error: {json_error}")
                    print(f"JSON string that failed: {json_str}")
                    print(f"Error position: line {json_error.lineno}, column {json_error.colno}")
                    
                    # Create fallback result with raw text
                    fallback_result = {
                        "query": query,
                        "results": [{
                            "url": "error://json-parse-failed",
                            "title": "JSON Parse Error",
                            "source_type": "error",
                            "reliability_score": 0,
                            "key_findings": [f"Failed to parse response: {str(json_error)}"],
                            "raw_response": text[:1000] if len(text) > 1000 else text,
                            "publication_date": datetime.now().strftime("%Y-%m-%d")
                        }]
                    }
                    results.append(fallback_result)
            else:
                print(f"⚠️ No valid JSON structure found in response")
                print(f"JSON start position: {json_start}")
                print(f"JSON end position: {json_end}")
                print(f"Full response text:\n{text}")
                
                # Create fallback result for no JSON
                fallback_result = {
                    "query": query,
                    "results": [{
                        "url": "error://no-json-found",
                        "title": "No JSON Found",
                        "source_type": "error",
                        "reliability_score": 0,
                        "key_findings": ["No JSON structure found in response"],
                        "raw_response": text[:1000] if len(text) > 1000 else text,
                        "publication_date": datetime.now().strftime("%Y-%m-%d")
                    }]
                }
                results.append(fallback_result)
                
        except Exception as e:
            print(f"\n❌ Error searching '{query}':")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print(f"Full traceback:\n{traceback.format_exc()}")
    
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