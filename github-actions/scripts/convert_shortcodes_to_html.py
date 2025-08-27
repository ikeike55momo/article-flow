#!/usr/bin/env python3
"""
Markdown Shortcode to HTML Converter
ショートコード記法をHTMLに自動変換するスクリプト
"""

import re
import sys
import os
from urllib.parse import urlparse

def convert_blog_card(match):
    """blog_card ショートコードをHTMLに変換"""
    url = match.group(1)
    
    # URLを解析してドメインを取得
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or "関連記事"
        title = f"{domain}の関連記事"
    except:
        title = "関連記事"
    
    return f'''<figure class="link-card">
  <a href="{url}" target="_blank" rel="noopener">
    <div class="link-card-content">
      <p class="link-card-title">{title}</p>
      <p class="link-card-url">{url}</p>
    </div>
  </a>
</figure>'''

def convert_shortcodes_to_html(content):
    """
    各種ショートコードをHTMLに変換
    
    対応ショートコード:
    - [blog_card url="..."]
    - [link_card url="..." title="..."]
    - [video url="..."]
    - [embed url="..."]
    """
    
    # blog_card変換
    content = re.sub(
        r'\[blog_card\s+url="([^"]+)"\s*\]',
        convert_blog_card,
        content,
        flags=re.MULTILINE
    )
    
    # link_card変換（titleオプション付き）
    def convert_link_card(match):
        url = match.group(1)
        title = match.group(2) if match.group(2) else "関連記事"
        return f'''<figure class="link-card">
  <a href="{url}" target="_blank" rel="noopener">
    <div class="link-card-content">
      <p class="link-card-title">{title}</p>
      <p class="link-card-url">{url}</p>
    </div>
  </a>
</figure>'''
    
    content = re.sub(
        r'\[link_card\s+url="([^"]+)"(?:\s+title="([^"]*)")?\s*\]',
        convert_link_card,
        content,
        flags=re.MULTILINE
    )
    
    # video埋め込み変換
    def convert_video(match):
        url = match.group(1)
        return f'''<figure class="video-embed">
  <iframe src="{url}" frameborder="0" allowfullscreen loading="lazy"></iframe>
  <figcaption>動画コンテンツ</figcaption>
</figure>'''
    
    content = re.sub(
        r'\[video\s+url="([^"]+)"\s*\]',
        convert_video,
        content,
        flags=re.MULTILINE
    )
    
    # embed汎用埋め込み変換
    def convert_embed(match):
        url = match.group(1)
        return f'''<figure class="embed-content">
  <iframe src="{url}" frameborder="0" loading="lazy"></iframe>
  <figcaption>埋め込みコンテンツ</figcaption>
</figure>'''
    
    content = re.sub(
        r'\[embed\s+url="([^"]+)"\s*\]',
        convert_embed,
        content,
        flags=re.MULTILINE
    )
    
    return content

def detect_remaining_shortcodes(content):
    """残存するショートコードを検出"""
    
    # 汎用ショートコード検出パターン（ぽるか提案）
    shortcode_pattern = r'\[[A-Za-z_][\w-]*(?:\s+[^\]]*)?\]'
    
    matches = re.findall(shortcode_pattern, content, re.MULTILINE)
    return matches

def main():
    """メイン処理"""
    if len(sys.argv) != 2:
        print("Usage: python3 convert_shortcodes_to_html.py <html_file>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    if not os.path.exists(html_file):
        print(f"❌ File not found: {html_file}")
        sys.exit(1)
    
    print(f"🔄 Converting shortcodes in: {html_file}")
    
    # ファイル読み込み
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Failed to read file: {e}")
        sys.exit(1)
    
    # 変換前の検出
    before_shortcodes = detect_remaining_shortcodes(content)
    if before_shortcodes:
        print(f"📝 Detected shortcodes before conversion: {len(before_shortcodes)}")
        for sc in before_shortcodes[:5]:  # 最初の5個を表示
            print(f"   - {sc}")
    
    # ショートコード変換
    converted_content = convert_shortcodes_to_html(content)
    
    # 変換後の検出
    after_shortcodes = detect_remaining_shortcodes(converted_content)
    
    # 結果出力
    if before_shortcodes and not after_shortcodes:
        print("✅ All shortcodes converted successfully")
    elif after_shortcodes:
        print(f"⚠️  Remaining shortcodes after conversion: {len(after_shortcodes)}")
        for sc in after_shortcodes[:3]:
            print(f"   - {sc}")
    else:
        print("✅ No shortcodes detected")
    
    # ファイル書き込み
    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        print(f"💾 File updated: {html_file}")
    except Exception as e:
        print(f"❌ Failed to write file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()