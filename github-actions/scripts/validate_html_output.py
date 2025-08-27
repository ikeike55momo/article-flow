#!/usr/bin/env python3
"""
Advanced HTML Output Validator
HTMLの出力を高度に検証し、Markdown記法やショートコードを検出する
"""

import re
import sys
import os
from html.parser import HTMLParser
from typing import List, Dict, Set

class HTMLContentExtractor(HTMLParser):
    """HTMLからテキストコンテンツのみを抽出するパーサー"""
    
    def __init__(self):
        super().__init__()
        self.text_content = []
        self.in_script_or_style = False
        self.current_tag = None
    
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag.lower() in ['script', 'style']:
            self.in_script_or_style = True
    
    def handle_endtag(self, tag):
        if tag.lower() in ['script', 'style']:
            self.in_script_or_style = False
        self.current_tag = None
    
    def handle_data(self, data):
        if not self.in_script_or_style:
            self.text_content.append(data.strip())
    
    def get_text_content(self):
        return '\n'.join([text for text in self.text_content if text])

class HTMLValidator:
    """HTML出力の包括的バリデーター"""
    
    def __init__(self):
        # ぽるか提案：汎用ショートコード検出パターン
        self.shortcode_patterns = {
            'generic_shortcode': r'\[[A-Za-z_][\w-]*(?:\s+[^\]]*)?\]',
            'blog_card': r'\[blog_card\s+[^\]]*\]',
            'link_card': r'\[link_card\s+[^\]]*\]',
            'video': r'\[video\s+[^\]]*\]',
            'embed': r'\[embed\s+[^\]]*\]',
            'gallery': r'\[gallery\s+[^\]]*\]',
            'button': r'\[button\s+[^\]]*\]'
        }
        
        # 厳密なMarkdown記法パターン
        self.markdown_patterns = {
            'headers': r'^\s{0,3}#{1,6}\s+.+$',
            'bullet_lists': r'^\s{0,3}[-*+]\s+.+$',
            'numbered_lists': r'^\s{0,3}\d+\.\s+.+$',
            'code_fences': r'^```[\w]*$',
            'code_inline': r'`[^`]+`',
            'markdown_links': r'\[[^\]]+\]\([^)]+\)',
            'markdown_images': r'!\[[^\]]*\]\([^)]+\)',
            'bold_markdown': r'\*\*[^*]+\*\*',
            'italic_markdown': r'(?<!\*)\*[^*\s][^*]*[^*\s]\*(?!\*)',
            'strikethrough': r'~~[^~]+~~',
            'blockquotes': r'^\s{0,3}>\s+.+$',
            'hr_markdown': r'^\s{0,3}([-*_])\s*\1\s*\1[\s\1]*$'
        }
        
        # 必須HTML構造
        self.required_structures = [
            r'<div\s+class="article-content"[^>]*>',
            r'</div>'
        ]
        
        # 禁止パターン
        self.forbidden_patterns = {
            'triple_backticks': r'```',
            'markdown_headers': r'^#{1,6}\s',
            'markdown_emphasis': r'\*\*|\*(?!\*)',
            'markdown_lists': r'^\s*[-*+]\s|^\s*\d+\.\s'
        }
    
    def extract_text_content(self, html_content: str) -> str:
        """HTMLからテキストコンテンツのみを抽出"""
        try:
            parser = HTMLContentExtractor()
            parser.feed(html_content)
            return parser.get_text_content()
        except Exception as e:
            print(f"⚠️  HTML parsing failed: {e}")
            return html_content  # フォールバック：元のコンテンツを返す
    
    def detect_patterns(self, content: str, patterns: Dict[str, str]) -> Dict[str, List[str]]:
        """パターンを検出して詳細情報を返す"""
        detections = {}
        
        for name, pattern in patterns.items():
            matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
            if matches:
                detections[name] = matches
        
        return detections
    
    def validate_html_structure(self, html_content: str) -> Dict[str, bool]:
        """HTML基本構造の検証"""
        results = {}
        
        # 必須構造の確認
        for i, pattern in enumerate(self.required_structures):
            results[f'required_structure_{i+1}'] = bool(re.search(pattern, html_content))
        
        # div class="article-content"の検証
        article_content_divs = len(re.findall(r'<div\s+class="article-content"', html_content))
        results['single_article_content_div'] = article_content_divs == 1
        
        # 基本的なHTMLタグの整合性
        results['well_formed_tags'] = self.check_tag_balance(html_content)
        
        return results
    
    def check_tag_balance(self, html_content: str) -> bool:
        """基本的なタグの開始・終了バランスをチェック"""
        # 簡易的なタグバランスチェック
        important_tags = ['div', 'section', 'article', 'figure', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        
        for tag in important_tags:
            open_count = len(re.findall(f'<{tag}(?:\s[^>]*)?>', html_content, re.IGNORECASE))
            close_count = len(re.findall(f'</{tag}>', html_content, re.IGNORECASE))
            
            if open_count != close_count:
                print(f"⚠️  Tag balance issue: <{tag}> opens:{open_count} closes:{close_count}")
                return False
        
        return True
    
    def validate_file(self, file_path: str) -> Dict:
        """ファイルの包括的バリデーション"""
        print(f"🔍 Validating HTML file: {file_path}")
        
        # ファイル存在確認
        if not os.path.exists(file_path):
            return {
                'success': False,
                'error': f"File not found: {file_path}",
                'shortcodes': {},
                'markdown': {},
                'html_structure': {},
                'recommendations': []
            }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to read file: {e}",
                'shortcodes': {},
                'markdown': {},
                'html_structure': {},
                'recommendations': []
            }
        
        # テキストコンテンツを抽出（ぽるか提案）
        text_content = self.extract_text_content(html_content)
        
        # 各種検証の実行
        shortcode_detections = self.detect_patterns(text_content, self.shortcode_patterns)
        markdown_detections = self.detect_patterns(text_content, self.markdown_patterns)
        html_structure_results = self.validate_html_structure(html_content)
        
        # 推奨事項の生成
        recommendations = self.generate_recommendations(
            shortcode_detections, markdown_detections, html_structure_results
        )
        
        # 成功判定
        success = (
            len(shortcode_detections) == 0 and 
            len(markdown_detections) == 0 and 
            all(html_structure_results.values())
        )
        
        return {
            'success': success,
            'error': None,
            'shortcodes': shortcode_detections,
            'markdown': markdown_detections,
            'html_structure': html_structure_results,
            'recommendations': recommendations,
            'file_size': os.path.getsize(file_path),
            'total_issues': len(shortcode_detections) + len(markdown_detections) + 
                           sum(1 for v in html_structure_results.values() if not v)
        }
    
    def generate_recommendations(self, shortcodes, markdown, html_structure) -> List[str]:
        """検出結果に基づく推奨事項を生成"""
        recommendations = []
        
        if shortcodes:
            recommendations.append("🔧 ショートコード変換スクリプトの実行を推奨")
            recommendations.append("📝 システムプロンプトにショートコード変換例を追加")
        
        if markdown:
            recommendations.append("🚨 Claude Code Actionによる自動リライトが必要")
            recommendations.append("💡 システムプロンプトの強化を検討")
        
        if not html_structure.get('single_article_content_div', True):
            recommendations.append("🏗️  article-content divの重複または不足を修正")
        
        if not html_structure.get('well_formed_tags', True):
            recommendations.append("🔗 HTMLタグの開始・終了バランスを修正")
        
        return recommendations

def main():
    """メイン処理"""
    if len(sys.argv) != 2:
        print("Usage: python3 validate_html_output.py <html_file>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    validator = HTMLValidator()
    result = validator.validate_file(html_file)
    
    print("=" * 60)
    print("📊 HTML VALIDATION REPORT")
    print("=" * 60)
    
    if result['error']:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    # ファイル情報
    print(f"📁 File: {html_file}")
    print(f"📏 Size: {result['file_size']} bytes")
    print(f"🔢 Total issues: {result['total_issues']}")
    print()
    
    # ショートコード検出結果
    if result['shortcodes']:
        print("🚨 SHORTCODE DETECTIONS:")
        for name, matches in result['shortcodes'].items():
            print(f"   {name}: {len(matches)} occurrences")
            for match in matches[:3]:  # 最初の3つを表示
                print(f"      - {match}")
        print()
    
    # Markdown記法検出結果
    if result['markdown']:
        print("🚨 MARKDOWN SYNTAX DETECTIONS:")
        for name, matches in result['markdown'].items():
            print(f"   {name}: {len(matches)} occurrences")
            for match in matches[:3]:  # 最初の3つを表示
                print(f"      - {match}")
        print()
    
    # HTML構造検証結果
    print("🏗️  HTML STRUCTURE VALIDATION:")
    for key, passed in result['html_structure'].items():
        status = "✅" if passed else "❌"
        print(f"   {status} {key}")
    print()
    
    # 推奨事項
    if result['recommendations']:
        print("💡 RECOMMENDATIONS:")
        for rec in result['recommendations']:
            print(f"   {rec}")
        print()
    
    # 最終判定
    if result['success']:
        print("✅ VALIDATION PASSED - HTML output is clean!")
        sys.exit(0)
    else:
        print("❌ VALIDATION FAILED - Issues detected!")
        sys.exit(1)

if __name__ == "__main__":
    main()