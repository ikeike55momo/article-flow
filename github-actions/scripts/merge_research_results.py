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

        # 一次情報の優先順位に基づいてソート
        def get_source_priority(result):
            """信頼性スコアと情報源タイプに基づく優先順位を返す"""
            source_priorities = {
                'government': 1,  # 政府機関
                'academic': 2,    # 学術機関
                'medical': 3,     # 医学会・専門団体
                'media': 4,       # 大手メディア
                'industry': 5     # 業界関連
            }
            
            # 各検索結果内のソート
            if 'results' in result and result['results']:
                for r in result['results']:
                    source_type = r.get('source_type', 'industry')
                    r['priority'] = source_priorities.get(source_type, 6)
                
                # 結果を優先順位でソート
                result['results'].sort(key=lambda x: (x.get('priority', 6), -x.get('reliability_score', 0)))
            
            return result
        
        # 全結果をソート
        sorted_results = [get_source_priority(r) for r in all_results]
        
        # 高信頼性ソースの抽出
        high_reliability_sources = []
        for result in all_results:
            if 'results' in result:
                for r in result['results']:
                    if r.get('source_type') in ['government', 'academic', 'medical'] and r.get('reliability_score', 0) >= 8:
                        high_reliability_sources.append({
                            'url': r.get('url'),
                            'title': r.get('title'),
                            'source_type': r.get('source_type'),
                            'reliability_score': r.get('reliability_score'),
                            'domain': r.get('domain', '')
                        })
        
        # 統合された結果を保存
        merged_research = {
            'results': sorted_results,
            'sources': list(set(all_sources)),  # 重複を除去
            'high_reliability_sources': high_reliability_sources,  # 高信頼性ソースのリスト
            'key_findings': all_key_findings,
            'total_queries': len(all_results),
            'primary_sources_count': len(high_reliability_sources),
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