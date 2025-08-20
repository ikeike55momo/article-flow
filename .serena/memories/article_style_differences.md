# Article Flow スタイル差分分析

## 現行ワークフロー vs sample/articles スタイルの違い

### 主要な変更点

#### 1. スタイル定義
- **現行**: インラインスタイル（`<style>`タグ含む）
- **新版**: スタイルなし（外部CSS前提）

#### 2. 画像要素
- **現行**: `<div class="article-content-image">[画像: 説明]</div>`
- **新版**: `<figure>`と`<figcaption>`を使用した実際の画像

#### 3. ブログカード機能
- **現行**: なし
- **新版**: `[blog_card url="..."]`ショートコード

#### 4. 関連記事セクション
- **現行**: なし
- **新版**: `article-related-section`クラス

#### 5. ステップリスト
- **現行**: 通常のolタグ
- **新版**: `article-steps-list`専用クラス

#### 6. CTAセクション
- **現行**: divタグ
- **新版**: sectionタグ

### 改変が必要なフェーズ
- **Phase 3（CHAT_03_content_generation.md）**: HTML生成部分の全面改訂
- 他のフェーズは基本的に変更不要