#!/usr/bin/env python3
"""Split research queries into batches"""

import json
import math
import sys

def main():
    """Split research queries into 5 batches"""
    try:
        # 分析結果を読み込み
        with open('phase1_output.json', 'r') as f:
            data = json.load(f)
        
        queries = data.get('analysis', {}).get('research_queries', [])
        total_queries = len(queries)
        batch_size = math.ceil(total_queries / 5)
        
        print(f"Total queries: {total_queries}, Batch size: {batch_size}")
        
        # 各バッチのクエリを保存
        for i in range(5):
            start_idx = i * batch_size
            end_idx = min((i + 1) * batch_size, total_queries)
            batch_queries = queries[start_idx:end_idx]
            
            batch_data = {
                'batch_id': i,
                'queries': batch_queries,
                'total_batches': 5
            }
            
            with open(f'research_batch_{i}.json', 'w') as f:
                json.dump(batch_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Created batch {i} with {len(batch_queries)} queries")
        
        # メタ情報を保存
        meta = {
            'total_queries': total_queries,
            'batch_count': 5,
            'batch_size': batch_size,
            'main_keyword': data.get('analysis', {}).get('main_keyword', '')
        }
        with open('research_meta.json', 'w') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Created research_meta.json with main keyword: {meta['main_keyword']}")
        
    except Exception as e:
        print(f"❌ Error splitting queries: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()