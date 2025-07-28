#!/usr/bin/env python3
"""Create fallback phase1_output.json file"""

import json
import os
import sys
from datetime import datetime

def main():
    """Create fallback phase1 output file"""
    title = os.environ.get('TITLE', '')
    persona = os.environ.get('PERSONA', '')
    keywords = os.environ.get('KEYWORDS', '')
    timestamp = os.environ.get('TIMESTAMP', datetime.utcnow().isoformat())
    
    if not title:
        print("Error: TITLE environment variable not set")
        sys.exit(1)
    
    data = {
        "analysis": {
            "main_keyword": title,
            "related_keywords": [keywords, "健康", "美容", "セルフケア", "効果"],
            "search_intent": "informational",
            "content_type": "how-to",
            "tone": "friendly",
            "key_points": ["基本情報", "実践方法", "注意点"],
            "research_queries": [
                f"{title} とは",
                f"{title} 方法",
                f"{title} 効果",
                f"{title} 注意点",
                f"{title} おすすめ",
                f"{title} 初心者",
                f"{title} やり方",
                f"{title} コツ",
                f"{title} 失敗",
                f"{title} 安全",
                f"{title} 専門家",
                f"{title} 研究",
                f"{title} 統計",
                f"{title} 2024",
                f"{title} 最新"
            ],
            "competitor_analysis_needed": True,
            "local_seo_focus": False,
            "estimated_sections": 5
        },
        "topic": title,
        "target_audience": persona,
        "keywords": keywords,
        "processed_at": timestamp,
        "workflow_version": "3.0.0"
    }
    
    # 出力先のディレクトリを環境変数から取得、デフォルトは現在のディレクトリ
    output_dir = os.environ.get('OUTPUT_DIR', '.')
    output_path = os.path.join(output_dir, 'phase1_output.json')
    
    with open(output_path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Created fallback phase1_output.json at {output_path} for: {title}")

if __name__ == "__main__":
    main()