#!/usr/bin/env python3
"""Create batch-specific analysis file"""

import json
import os
import sys

def main():
    """Create analysis file for specific batch"""
    batch_num = os.environ.get('BATCH_NUM')
    if not batch_num:
        print("Error: BATCH_NUM environment variable not set")
        sys.exit(1)
    
    try:
        # オリジナルの分析結果を読み込み
        with open('phase1_output.json', 'r') as f:
            original_data = json.load(f)

        # このバッチのクエリを読み込み
        with open(f'research_batch_{batch_num}.json', 'r') as f:
            batch_data = json.load(f)

        # バッチ用の分析ファイルを作成
        batch_analysis = original_data.copy()
        batch_analysis['analysis']['research_queries'] = batch_data['queries']

        with open(f'batch_{batch_num}_analysis.json', 'w') as f:
            json.dump(batch_analysis, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Created batch_{batch_num}_analysis.json with {len(batch_data['queries'])} queries")
        
    except Exception as e:
        print(f"❌ Error creating batch analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()