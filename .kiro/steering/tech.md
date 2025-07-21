# 技術スタック

## ビルドシステム・ツール

- **Claude Code**: メインのAIインターフェース（`.claude-code-config.yaml`で設定）
- **Gemini CLI**: 代替AIインターフェース（`.gemini-cli-config.yaml`で設定）
- **Web Search**: リサーチ・ファクトチェック段階で必須のツール
- **YAML設定**: すべての設定とワークフローをYAMLファイルで定義

## 主要技術

- **出力形式**: WordPress互換性のためのインラインCSS付きHTML
- **CSSフレームワーク**: WordPress最適化カスタムCSS（インライン必須）
- **コンテンツ形式**: SEO最適化された日本語テキスト
- **エンコーディング**: UTF-8
- **レスポンシブデザイン**: モバイルファースト設計

## 共通コマンド

### 記事生成
```bash
# Claude Code使用
claude-code "爪ケアについての記事を作成して"

# Gemini CLI使用
gemini "爪ケアについての記事を作成して"

# パラメータ付き
claude-code "爪ケアについての記事を作成して store_url=https://example.com/ target=セルフケア志向の女性"
```

### 設定管理
- 設定ファイルはYAML形式
- ビルドやコンパイル手順は不要
- 設定ファイルの変更は即座に反映

## WordPress統合

### CSS要件
- **重要**: すべてのCSSは`<style>`タグでインライン記述必須
- **絶対に**外部CSSファイルを参照しない
- `.wp-blog-post`をルートコンテナクラスとして使用
- CSSは事前定義済みで変更禁止

### 出力形式
- 単一HTMLブロックのみ出力
- HTML外部に説明文なし
- WordPressメタ情報はHTMLコメント内
- SEO用構造化データを含む

## 開発ワークフロー

1. **コンパイル不要** - YAMLとMarkdownの直接編集
2. **テスト**: 記事生成コマンドで変更をテスト
3. **検証**: WordPress環境での出力確認
4. **バージョン管理**: 標準的なGitベース管理