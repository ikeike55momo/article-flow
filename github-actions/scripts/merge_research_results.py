#!/usr/bin/env python3
"""Merge research results from all batches"""

import json
import os
from pathlib import Path
from datetime import datetime

def main():
    """Merge all batch research results"""
    try:
        # 全バッチの結果を収集
        all_results = []
        all_sources = []
        all_key_findings = []

        # バッチディレクトリを探索
        batch_dirs = sorted(Path('batches').glob('research-batch-*'))

        for batch_dir in batch_dirs:
            # 各バッチのphase2_research.jsonを読み込み
            research_file = batch_dir / 'phase2_research.json'
            if research_file.exists():
                with open(research_file, 'r') as f:
                    batch_data = json.load(f)
                    
                    # 結果を統合
                    if 'results' in batch_data:
                        all_results.extend(batch_data['results'])
                    if 'sources' in batch_data:
                        all_sources.extend(batch_data['sources'])
                    if 'key_findings' in batch_data:
                        all_key_findings.extend(batch_data['key_findings'])

        # 統合された結果を保存
        merged_research = {
            'results': all_results,
            'sources': list(set(all_sources)),  # 重複を除去
            'key_findings': all_key_findings,
            'total_queries': len(all_results),
            'timestamp': str(datetime.now())
        }

        with open('phase2_research.json', 'w') as f:
            json.dump(merged_research, f, ensure_ascii=False, indent=2)

        print(f'✅ Merged {len(batch_dirs)} batches with {len(all_results)} total results')
        
    except Exception as e:
        print(f"❌ Error merging research results: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()