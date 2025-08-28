#!/usr/bin/env python3
"""
Markdown Lists to HTML Converter
Markdown番号付きリスト記法をHTMLに自動変換するスクリプト
"""

import re
import sys
import os
from bs4 import BeautifulSoup, NavigableString

def detect_numbered_lists(content):
    """
    番号付きリスト（Markdown記法）を検出
    
    検出条件:
    - 行頭に「数字. 半角スペース」を持つ行が2行以上連続
    - 正規表現: ^\\s*\\d+\\.\\s+(.+)$
    
    Returns:
        list: 検出された番号付きリストブロック
    """
    # 番号付きリスト行を検出
    list_pattern = r'^\s*(\d+)\.\s+(.+)$'
    lines = content.split('\n')
    detected_blocks = []
    current_block = []
    
    for i, line in enumerate(lines):
        match = re.match(list_pattern, line)
        if match:
            current_block.append({
                'line_number': i + 1,
                'number': int(match.group(1)),
                'text': match.group(2).strip(),
                'full_line': line
            })
        else:
            # 連続が途切れた場合、2行以上なら有効なブロックとして保存
            if len(current_block) >= 2:
                detected_blocks.append(current_block)
            current_block = []
    
    # 最後のブロックもチェック
    if len(current_block) >= 2:
        detected_blocks.append(current_block)
    
    return detected_blocks

def convert_numbered_lists_to_html(content):
    """
    Markdown番号付きリストをHTMLの<ol><li>タグに変換
    
    シンプルな文字列置換アプローチを使用
    除外条件はコンテキストで判断
    
    Args:
        content (str): HTMLコンテンツ
        
    Returns:
        tuple: (変換後のHTMLコンテンツ, 変換されたブロック数)
    """
    converted_count = 0
    result_content = content
    
    # 番号付きリストブロックを検出
    list_blocks = detect_numbered_lists(content)
    
    if not list_blocks:
        return content, 0
    
    # 各ブロックを<ol><li>に変換
    for block in reversed(list_blocks):  # 後ろから処理して位置ずれを防ぐ
        # 元のMarkdown記法
        block_lines = [item['full_line'] for item in block]
        block_text = '\n'.join(block_lines)
        
        # <pre>や<code>内に含まれているかチェック
        # 簡単な方法：前後にタグがあるかチェック
        block_start = result_content.find(block_text)
        if block_start == -1:
            continue
            
        # ブロック前後のコンテキストを確認
        context_before = result_content[max(0, block_start-100):block_start]
        context_after = result_content[block_start+len(block_text):block_start+len(block_text)+100]
        
        # <pre>や<code>タグ内かチェック
        if ('<pre' in context_before and '</pre>' in context_after) or \
           ('<code' in context_before and '</code>' in context_after):
            print(f"   ⏭️  Skipping list block inside pre/code tags")
            continue
        
        # 既存の<ol>タグ内かチェック
        if ('<ol' in context_before and '</ol>' in context_after):
            print(f"   ⏭️  Skipping list block inside existing <ol> tags")
            continue
        
        # <ol><li>構造を生成
        ol_content = []
        for item in block:
            escaped_text = item['text'].replace('<', '&lt;').replace('>', '&gt;')
            ol_content.append(f"  <li>{escaped_text}</li>")
        
        ol_html = f"<ol>\n" + "\n".join(ol_content) + "\n</ol>"
        
        # 元のMarkdown記法を置換
        result_content = result_content.replace(block_text, ol_html)
        converted_count += 1
        print(f"   ✅ Converted block with {len(block)} items")
    
    return result_content, converted_count

def validate_html_structure(content):
    """HTMLの基本構造をチェック"""
    issues = []
    
    try:
        soup = BeautifulSoup(content, 'html.parser')
        
        # <ol>タグの妥当性チェック
        ol_tags = soup.find_all('ol')
        for ol in ol_tags:
            li_children = ol.find_all('li', recursive=False)
            if not li_children:
                issues.append(f"Empty <ol> tag found")
            
            # <li>以外の直接子要素をチェック
            for child in ol.children:
                if hasattr(child, 'name') and child.name and child.name != 'li':
                    issues.append(f"Invalid child '{child.name}' in <ol> tag")
    
    except Exception as e:
        issues.append(f"HTML parsing error: {e}")
    
    return issues

def main():
    """メイン処理"""
    if len(sys.argv) != 2:
        print("Usage: python3 convert_markdown_lists_to_html.py <html_file>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    if not os.path.exists(html_file):
        print(f"❌ File not found: {html_file}")
        sys.exit(1)
    
    print(f"🔄 Converting Markdown numbered lists to HTML in: {html_file}")
    
    # ファイル読み込み
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Failed to read file: {e}")
        sys.exit(1)
    
    # 変換前の検出
    before_blocks = detect_numbered_lists(content)
    total_items_before = sum(len(block) for block in before_blocks)
    
    if before_blocks:
        print(f"📝 Detected numbered list blocks before conversion: {len(before_blocks)}")
        print(f"📝 Total numbered list items: {total_items_before}")
        
        # 最初のブロックの例を表示
        if before_blocks[0]:
            print("📝 Example items:")
            for item in before_blocks[0][:3]:  # 最初の3項目
                print(f"   - {item['number']}. {item['text'][:50]}{'...' if len(item['text']) > 50 else ''}")
    
    # Markdown番号付きリスト変換
    converted_content, converted_count = convert_numbered_lists_to_html(content)
    
    # 変換後の検出
    after_blocks = detect_numbered_lists(converted_content)
    total_items_after = sum(len(block) for block in after_blocks)
    
    # HTML構造の妥当性チェック
    html_issues = validate_html_structure(converted_content)
    
    # 結果出力
    if converted_count > 0:
        print(f"✅ Converted {converted_count} numbered list blocks to HTML")
        print(f"✅ Remaining Markdown lists: {len(after_blocks)} blocks ({total_items_after} items)")
        
        if html_issues:
            print("⚠️  HTML structure warnings:")
            for issue in html_issues:
                print(f"   - {issue}")
        else:
            print("✅ HTML structure validation passed")
    else:
        print("✅ No numbered lists detected or conversion needed")
    
    # 変換効果の確認
    if total_items_before > total_items_after:
        conversion_rate = ((total_items_before - total_items_after) / total_items_before) * 100
        print(f"📊 Conversion effectiveness: {conversion_rate:.1f}% of items converted")
    
    # ファイル書き込み
    try:
        # バックアップ作成（安全対策）
        backup_file = f"{html_file}.backup"
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 変換後のファイル保存
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        print(f"💾 File updated: {html_file}")
        print(f"💾 Backup created: {backup_file}")
        
        # バックアップファイルを削除（成功時）
        os.remove(backup_file)
        
    except Exception as e:
        print(f"❌ Failed to write file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()