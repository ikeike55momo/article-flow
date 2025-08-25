# 🚀 AI記事自動生成システム - Article Flow

## 📋 概要

GitHub Actionsを使用して、高品質なSEO最適化済み記事を自動生成するワークフローシステムです。
ARTICLE-TEMPLATE-README.mdの仕様に完全準拠したHTML出力を生成します。

## ✨ 特徴

- 🤖 **Claude API統合** - 高品質な記事生成
- 🔍 **Gemini APIリサーチ** - 信頼性の高い情報収集
- ✅ **ファクトチェック機能** - 品質スコア付き検証
- 📊 **SEO最適化** - メタデータ自動生成
- 🎨 **画像生成対応** - MCP Imagen4による画像生成
- 📱 **WordPress対応** - そのまま貼り付け可能なHTML出力

## 🎯 ワークフローバージョン

### 1. article-generation-v4-free.yml（推奨）
- **特徴**: 無料版・シンプルな構成
- **用途**: 基本的な記事生成
- **必要なシークレット**: 
  - `ANTHROPIC_API_KEY`
  - `GEMINI_API_KEY`

### 2. article-generation-v4.yml
- **特徴**: フル機能版（有料機能含む）
- **用途**: 高度な記事生成・画像生成
- **追加機能**: Google Drive連携、詳細な品質管理

## 🔧 セットアップ

### 1. リポジトリをフォーク/クローン
```bash
git clone https://github.com/yourusername/article-flow.git
cd article-flow
```

### 2. GitHub Secretsの設定
リポジトリの Settings → Secrets and variables → Actions で以下を設定：

```yaml
ANTHROPIC_API_KEY: your_claude_api_key
GEMINI_API_KEY: your_gemini_api_key
```

### 3. GitHub Actionsの有効化
- リポジトリの Actions タブを開く
- ワークフローを有効化

## 📝 使い方

### GitHub Actions経由での実行

1. **Actions タブを開く**
2. **ワークフローを選択**
   - `Article Generation V4 Free (Simplified Output)`を選択
3. **Run workflow をクリック**
4. **パラメータを入力**：
   - **タイトル案**: 記事のタイトル（30-32字推奨）
   - **主要KW**: メインキーワード（カンマ区切り、最大3語）
   - **切り口・ターゲット**: ターゲット層の説明
   - **E-E-A-T要素**: 専門性・経験・権威性・信頼性の要素
   - **目標文字数**: デフォルト3200文字
   - **画像生成**: 有効/無効の選択

### 実行例
```yaml
タイトル案: "40代女性のための効果的なスキンケア完全ガイド"
主要KW: "スキンケア,40代,アンチエイジング"
切り口・ターゲット: "肌の変化に悩む40代女性"
E-E-A-T要素: "皮膚科医監修、20年の美容経験"
```

## 📁 ディレクトリ構造

```
article-flow/
├── .github/
│   └── workflows/          # GitHub Actionsワークフロー
│       ├── article-generation-v4-free.yml
│       └── article-generation-v4.yml
├── Prompt_v2/             # バージョン2用プロンプト
│   ├── CHAT_01_phase1_analysis.md
│   ├── CHAT_02_structure_generation.md
│   └── ...
├── Prompt_v3/             # バージョン3用プロンプト（最新）
│   ├── ARTICLE-TEMPLATE-README.md  # HTML仕様書
│   └── ...
├── github-actions/        # ワークフロー用スクリプト
│   └── scripts/
│       ├── create_batch_analysis.py
│       ├── merge_research_results.py
│       └── ...
└── output/               # 生成された記事の出力先

```

## 📊 出力形式

### 生成される成果物

1. **final_article.html** - WordPress貼り付け用HTML
2. **research_results.json** - リサーチ結果（信頼性スコア付き）
3. **factcheck_report.json** - ファクトチェックレポート
4. **seo_metadata.json** - SEOメタ情報
5. **images/** - 生成された画像

### HTML仕様準拠

ARTICLE-TEMPLATE-README.mdの仕様に完全準拠：
- 全CSSクラス対応
- エラー防止チェック実装
- ハイライトボックス制限（1セクション1個）
- strongタグ使用ガイドライン準拠

## 🛠️ トラブルシューティング

### よくある問題

1. **API Key エラー**
   - GitHub Secretsが正しく設定されているか確認
   - APIキーの有効性を確認

2. **ワークフロー失敗**
   - Actionsログを確認
   - 必要なファイルが存在するか確認

3. **出力が期待通りでない**
   - Prompt_v3/のプロンプトファイルを確認
   - パラメータが適切か確認

## 📚 関連ドキュメント

- [WORKFLOW_USER_GUIDE.md](./WORKFLOW_USER_GUIDE.md) - 詳細な使用ガイド
- [CLAUDE.md](./CLAUDE.md) - Claude設定と開発ルール
- [GEMINI.md](./GEMINI.md) - Gemini設定ガイド
- [Prompt_v3/ARTICLE-TEMPLATE-README.md](./Prompt_v3/ARTICLE-TEMPLATE-README.md) - HTML仕様書

## 🤝 コントリビューション

プルリクエスト歓迎です！
1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

## 📝 ライセンス

MIT License - 詳細は[LICENSE](./LICENSE)を参照

## 💬 サポート

問題が発生した場合は、[Issues](https://github.com/yourusername/article-flow/issues)で報告してください。

---

🤖 Generated with [Claude Code](https://claude.ai/code)