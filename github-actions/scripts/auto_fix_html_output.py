#!/usr/bin/env python3
"""
Automatic HTML Output Fixer
バリデーション失敗時にClaude API経由で自動修正を実行
"""

import os
import sys
import json
import requests
from typing import Dict, Optional

class HTMLAutoFixer:
    """HTML出力の自動修正クラス"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
        
        # 修正用システムプロンプト（ぽるか提案）
        self.system_prompt = """あなたは「HTML修正専門エージェント」です。

## 任務
不適切なMarkdown記法やショートコードを含むHTMLを、完全なHTMLに修正してください。

## 修正ルール
1. **ショートコード変換**:
   - [blog_card url="..."] → <figure class="link-card"><a href="URL">関連記事</a></figure>
   - [link_card url="..." title="..."] → <figure class="link-card"><a href="URL">TITLE</a></figure>
   - [video url="..."] → <figure class="video-embed"><iframe src="URL"></iframe></figure>
   - [embed url="..."] → <figure class="embed-content"><iframe src="URL"></iframe></figure>

2. **Markdown記法変換**:
   - # 見出し → <h1>見出し</h1>
   - ## 見出し → <h2>見出し</h2>
   - **太字** → <strong>太字</strong>
   - *斜体* → <em>斜体</em>
   - [リンク](URL) → <a href="URL">リンク</a>
   - ![画像](URL) → <img src="URL" alt="画像" loading="lazy">
   - ``` コード ``` → <pre><code>コード</code></pre>
   - - リスト → <ul><li>リスト</li></ul>
   - 1. リスト → <ol><li>リスト</li></ol>

3. **構造の維持**:
   - <div class="article-content">で開始し</div>で終了
   - CSSクラス名は既存のまま維持
   - HTMLの構造と階層は崩さない

4. **品質保証**:
   - 全てのタグを正しく閉じる
   - 属性値はダブルクォートで囲む
   - HTMLエスケープが必要な箇所は適切にエスケープ
   - 不要な空行や余分な改行は除去

## 出力形式
修正されたHTMLのみを出力してください。説明文や前置き、後置きは不要です。"""

    def fix_html_content(self, html_content: str) -> Optional[str]:
        """Claude APIを使用してHTML修正"""
        
        prompt = f"""以下のHTMLを修正してください：

{html_content}

上記のHTMLに含まれるMarkdown記法やショートコードを、適切なHTMLタグに変換してください。"""

        payload = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 8000,
            "temperature": 0,
            "system": self.system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            print("🤖 Calling Claude API for HTML correction...")
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'content' in result and len(result['content']) > 0:
                    fixed_content = result['content'][0]['text']
                    print("✅ HTML fixed successfully by Claude API")
                    return fixed_content.strip()
                else:
                    print("❌ No content in Claude API response")
                    return None
            else:
                print(f"❌ Claude API error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ Claude API timeout")
            return None
        except Exception as e:
            print(f"❌ Claude API request failed: {e}")
            return None
    
    def fix_file(self, file_path: str) -> bool:
        """HTMLファイルの修正"""
        print(f"🔧 Auto-fixing HTML file: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return False
        
        # 元ファイルのバックアップ
        backup_path = f"{file_path}.backup"
        try:
            import shutil
            shutil.copy2(file_path, backup_path)
            print(f"💾 Backup created: {backup_path}")
        except Exception as e:
            print(f"⚠️  Failed to create backup: {e}")
        
        # ファイル読み込み
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            print(f"❌ Failed to read file: {e}")
            return False
        
        # Claude APIで修正
        fixed_content = self.fix_html_content(original_content)
        
        if not fixed_content:
            print("❌ Failed to fix HTML content")
            return False
        
        # 修正内容の保存
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"💾 Fixed content saved: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to write fixed content: {e}")
            return False

def main():
    """メイン処理"""
    if len(sys.argv) != 2:
        print("Usage: python3 auto_fix_html_output.py <html_file>")
        print("Environment: ANTHROPIC_API_KEY must be set")
        sys.exit(1)
    
    html_file = sys.argv[1]
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        sys.exit(1)
    
    fixer = HTMLAutoFixer(api_key)
    success = fixer.fix_file(html_file)
    
    if success:
        print("✅ HTML auto-fix completed successfully")
        sys.exit(0)
    else:
        print("❌ HTML auto-fix failed")
        sys.exit(1)

if __name__ == "__main__":
    main()