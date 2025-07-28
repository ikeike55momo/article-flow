#!/usr/bin/env python3
"""Generate fallback article when Claude Code Action fails"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Generate fallback article")
    parser.add_argument("--article-dir", required=True, help="Article output directory")
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--persona", default="爪が弱い30代女性", help="Target persona")
    return parser.parse_args()

def load_article_data(article_dir: Path):
    """Load article data from input files"""
    data = {}
    
    # Load input parameters
    input_file = article_dir / "input_params.json"
    if input_file.exists():
        with open(input_file, 'r', encoding='utf-8') as f:
            data['input'] = json.load(f)
    
    # Load analysis results
    phase1_file = article_dir / "phase1_output.json"
    if phase1_file.exists():
        with open(phase1_file, 'r', encoding='utf-8') as f:
            data['analysis'] = json.load(f)
    
    # Load research results
    research_file = article_dir / "research_results.json"
    if research_file.exists():
        with open(research_file, 'r', encoding='utf-8') as f:
            data['research'] = json.load(f)
    
    return data

def generate_fallback_article(title: str, persona: str, data: dict) -> str:
    """Generate a basic fallback article"""
    
    article_content = f"""# {title}

{persona}の皆さんにとって、爪の健康は日常生活における重要な関心事の一つです。この記事では、専門的な観点から実践的なケア方法について解説いたします。

## 爪が薄い・割れやすい原因とは

爪が薄くなったり割れやすくなったりする原因は、一般的に以下のような要因が考えられています。

### 栄養不足による影響

研究によると、タンパク質やビタミン、ミネラルの不足が爪の健康に大きく影響することが知られています。特に以下の栄養素が重要とされています：

- **タンパク質**: 爪の主成分であるケラチンの生成に必要
- **ビオチン**: 爪の強度向上に関連があるとされる
- **鉄分**: 不足すると爪が薄くなる可能性がある
- **亜鉛**: 細胞の新陳代謝に重要な役割を果たす

### 外的要因の影響

日常生活における外的要因も爪の状態に影響を与えるとされています：

- 過度な水仕事や洗剤の使用
- 頻繁なマニキュアの使用
- 爪を道具として使用する習慣
- 乾燥した環境での生活

## 専門的なケア方法

### 基本的なお手入れ

専門家が推奨する基本的なケア方法をご紹介します：

1. **適切な爪切り**
   - 爪が湿っている状態で切ることが推奨されています
   - 一度に大きく切らず、少しずつカットする
   - やすりで形を整える

2. **保湿ケア**
   - ハンドクリームやキューティクルオイルの使用
   - 就寝前の集中ケアが効果的とされる
   - 手袋の着用による保護

3. **栄養バランスの改善**
   - バランスの取れた食事を心がける
   - 必要に応じてサプリメントの検討
   - 十分な水分摂取

### 避けるべき習慣

以下のような習慣は爪の健康に悪影響を与える可能性があります：

- 爪を噛む習慣
- 無理な甘皮処理
- 過度なネイルアート
- 不適切な除光液の使用

## よくある質問

### Q: どのくらいで効果が現れますか？

A: 個人差がありますが、一般的に爪の成長サイクルは約6ヶ月とされています。適切なケアを継続することで、数週間から数ヶ月で変化を感じる方が多いようです。

### Q: サプリメントは効果的ですか？

A: 栄養不足が原因の場合、適切なサプリメントが有効な場合があります。ただし、医師や専門家に相談されることをお勧めします。

### Q: 市販のケア用品の選び方は？

A: 成分表を確認し、保湿成分が含まれているものを選ぶことが推奨されています。使用前にパッチテストを行うことも大切です。

## まとめ

爪の健康は日々のケアの積み重ねによって維持されるものです。今回ご紹介した方法を参考に、ご自身に合ったケア方法を見つけていただければと思います。

症状が改善されない場合や、気になる変化がある場合は、専門医に相談されることをお勧めします。個人差があるため、無理をせず、継続的なケアを心がけましょう。

*本記事の内容は一般的な情報提供を目的としており、個別の診断や治療に代わるものではありません。気になる症状がある場合は、医療専門家にご相談ください。*
"""
    
    return article_content

def main():
    """Main execution function"""
    args = parse_arguments()
    
    article_dir = Path(args.article_dir)
    
    print(f"🔄 Generating fallback article for: {args.title}")
    
    # Load existing data if available
    data = load_article_data(article_dir)
    
    # Generate fallback article
    article_content = generate_fallback_article(args.title, args.persona, data)
    
    # Write the fallback article
    output_file = article_dir / "final_article.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(article_content)
    
    print(f"✅ Fallback article generated: {output_file}")
    print(f"📊 Article length: {len(article_content)} characters")

if __name__ == "__main__":
    main()