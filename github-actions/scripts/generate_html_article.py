#!/usr/bin/env python3
"""
Markdown記事をスタイル付きHTMLに変換し、画像を適切に配置する
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
import markdown
from markdown.extensions import tables, fenced_code, nl2br, attr_list

def generate_html_template(title, content, metadata, css_style):
    """HTMLテンプレートを生成"""
    
    # メタデータからSEO情報を抽出
    seo_title = metadata.get('title', title)
    meta_description = metadata.get('meta_description', '')
    meta_keywords = ', '.join(metadata.get('meta_keywords', []))
    og_title = metadata.get('og_title', seo_title)
    og_description = metadata.get('og_description', meta_description)
    
    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta_description}">
    <meta name="keywords" content="{meta_keywords}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{og_title}">
    <meta property="og:description" content="{og_description}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:title" content="{og_title}">
    <meta property="twitter:description" content="{og_description}">
    
    <title>{seo_title}</title>
    
    <style>
        {css_style}
    </style>
</head>
<body>
    <div class="container">
        <article class="article-main">
            {content}
        </article>
        
        <footer class="article-footer">
            <p>作成日: {datetime.now().strftime('%Y年%m月%d日')}</p>
        </footer>
    </div>
</body>
</html>"""
    
    return html_template

def generate_css_style():
    """記事用のCSSスタイルを生成"""
    
    css = """
/* リセットとベース設定 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, "Noto Sans JP", sans-serif;
    line-height: 1.8;
    color: #333;
    background-color: #f8f9fa;
}

/* コンテナ */
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

/* 記事メイン */
.article-main {
    background: #fff;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 30px;
}

/* 見出しスタイル */
h1 {
    font-size: 2.5em;
    color: #2c3e50;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 3px solid #3498db;
    font-weight: 700;
}

h2 {
    font-size: 1.8em;
    color: #34495e;
    margin-top: 40px;
    margin-bottom: 20px;
    padding-left: 15px;
    border-left: 5px solid #3498db;
    font-weight: 600;
}

h3 {
    font-size: 1.4em;
    color: #555;
    margin-top: 30px;
    margin-bottom: 15px;
    font-weight: 600;
}

/* 段落とテキスト */
p {
    margin-bottom: 20px;
    text-align: justify;
}

/* リスト */
ul, ol {
    margin-bottom: 20px;
    padding-left: 30px;
}

li {
    margin-bottom: 10px;
}

/* 画像スタイル */
.article-image {
    width: 100%;
    max-width: 100%;
    height: auto;
    margin: 30px 0;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.hero-image {
    width: 100%;
    height: auto;
    margin-bottom: 40px;
    border-radius: 10px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

.section-image {
    width: 100%;
    max-width: 600px;
    height: auto;
    margin: 25px auto;
    display: block;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* 引用 */
blockquote {
    background: #f4f7f8;
    border-left: 5px solid #3498db;
    margin: 20px 0;
    padding: 15px 20px;
    font-style: italic;
    color: #555;
}

/* テーブル */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    background: #fff;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

th, td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

th {
    background: #3498db;
    color: #fff;
    font-weight: 600;
}

tr:hover {
    background: #f5f5f5;
}

/* コード */
code {
    background: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: "Consolas", "Monaco", "Andale Mono", monospace;
    font-size: 0.9em;
}

pre {
    background: #2c3e50;
    color: #ecf0f1;
    padding: 20px;
    border-radius: 5px;
    overflow-x: auto;
    margin: 20px 0;
}

pre code {
    background: none;
    color: inherit;
    padding: 0;
}

/* 強調 */
strong {
    font-weight: 600;
    color: #2c3e50;
}

em {
    font-style: italic;
    color: #555;
}

/* フッター */
.article-footer {
    text-align: center;
    color: #7f8c8d;
    font-size: 0.9em;
    padding: 20px;
}

/* レスポンシブ対応 */
@media (max-width: 768px) {
    .article-main {
        padding: 20px;
    }
    
    h1 {
        font-size: 2em;
    }
    
    h2 {
        font-size: 1.5em;
    }
    
    h3 {
        font-size: 1.2em;
    }
}

/* アニメーション */
.article-main {
    animation: fadeIn 0.8s ease-in;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* カスタムハイライト */
.highlight {
    background: #fff3cd;
    padding: 2px 6px;
    border-radius: 3px;
}

/* セクション区切り */
.section-divider {
    height: 2px;
    background: linear-gradient(to right, transparent, #3498db, transparent);
    margin: 40px 0;
}
"""
    
    return css

def insert_images_into_content(content, images_dir):
    """記事内容に画像を適切に挿入"""
    
    # ヒーロー画像の挿入（最初のh1の後）
    hero_image_path = os.path.join(images_dir, 'hero_image.png')
    if os.path.exists(hero_image_path):
        # h1タグの後に画像を挿入
        content = re.sub(
            r'(^# [^\n]+\n)',
            r'\1\n<img src="images/hero_image.png" alt="ヒーロー画像" class="hero-image">\n\n',
            content,
            count=1,
            flags=re.MULTILINE
        )
    
    # セクション画像の挿入（各h2の後）
    section_count = 0
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # h2見出しの検出
        if line.startswith('## ') and section_count < 4:
            section_count += 1
            section_image_path = os.path.join(images_dir, f'section_{section_count}_image.png')
            
            # 画像が存在する場合、次の段落の後に挿入
            if os.path.exists(section_image_path):
                # 次の空行を探す
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() == '':
                        continue
                    elif j + 1 < len(lines) and lines[j + 1].strip() == '':
                        # 段落の終わりを見つけた
                        new_lines.append('')
                        new_lines.append(f'<img src="images/section_{section_count}_image.png" alt="セクション{section_count}の画像" class="section-image">')
                        break
    
    return '\n'.join(new_lines)

def convert_markdown_to_html(article_dir):
    """MarkdownをHTMLに変換"""
    
    # 必要なファイルのパスを設定
    article_path = os.path.join(article_dir, 'final_article.md')
    seo_metadata_path = os.path.join(article_dir, 'seo_metadata.json')
    images_dir = os.path.join(article_dir, 'images')
    output_html_path = os.path.join(article_dir, 'article.html')
    
    # Markdown記事を読み込む
    if not os.path.exists(article_path):
        print(f"エラー: {article_path} が見つかりません")
        return False
    
    with open(article_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # タイトルを抽出
    title_match = re.search(r'^# (.+)$', markdown_content, re.MULTILINE)
    title = title_match.group(1) if title_match else 'Article'
    
    # SEOメタデータを読み込む
    metadata = {}
    if os.path.exists(seo_metadata_path):
        with open(seo_metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    
    # 画像を内容に挿入
    if os.path.exists(images_dir):
        markdown_content = insert_images_into_content(markdown_content, images_dir)
    
    # MarkdownをHTMLに変換
    md = markdown.Markdown(extensions=[
        'tables',
        'fenced_code',
        'nl2br',
        'attr_list',
        'extra'
    ])
    
    html_content = md.convert(markdown_content)
    
    # セクション区切りを追加
    html_content = re.sub(
        r'</h2>',
        r'</h2>\n<div class="section-divider"></div>',
        html_content
    )
    
    # CSSスタイルを生成
    css_style = generate_css_style()
    
    # 完全なHTMLを生成
    full_html = generate_html_template(title, html_content, metadata, css_style)
    
    # HTMLファイルを保存
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ HTMLファイルを生成しました: {output_html_path}")
    
    # スタンドアロン版も作成（画像をBase64エンコード）
    if os.path.exists(images_dir):
        create_standalone_html(article_dir, full_html)
    
    return True

def create_standalone_html(article_dir, html_content):
    """画像を埋め込んだスタンドアロンHTMLを作成"""
    import base64
    
    standalone_html = html_content
    images_dir = os.path.join(article_dir, 'images')
    
    # 画像ファイルを検索してBase64に変換
    for image_file in os.listdir(images_dir):
        if image_file.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(images_dir, image_file)
            
            with open(image_path, 'rb') as img_file:
                image_data = base64.b64encode(img_file.read()).decode('utf-8')
            
            # HTMLの画像参照をBase64データURLに置換
            mime_type = 'image/png' if image_file.endswith('.png') else 'image/jpeg'
            data_url = f'data:{mime_type};base64,{image_data}'
            standalone_html = standalone_html.replace(
                f'src="images/{image_file}"',
                f'src="{data_url}"'
            )
    
    # スタンドアロン版を保存
    standalone_path = os.path.join(article_dir, 'article_standalone.html')
    with open(standalone_path, 'w', encoding='utf-8') as f:
        f.write(standalone_html)
    
    print(f"✅ スタンドアロンHTMLファイルを生成しました: {standalone_path}")

def main():
    """メイン処理"""
    if len(sys.argv) < 2:
        print("使用方法: python generate_html_article.py <article_directory>")
        sys.exit(1)
    
    article_dir = sys.argv[1]
    
    if not os.path.exists(article_dir):
        print(f"エラー: ディレクトリ {article_dir} が見つかりません")
        sys.exit(1)
    
    # HTMLを生成
    success = convert_markdown_to_html(article_dir)
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()