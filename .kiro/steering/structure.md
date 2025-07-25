# プロジェクト構造

## ルートディレクトリ構成

```
/
├── .claude-code-config.yaml     # Claude Code AIインターフェース設定
├── .gemini-cli-config.yaml      # Gemini CLI AIインターフェース設定
├── INSTRUCTIONS.md              # 旧実行指示書
├── INSTRUCTIONS_v2.md           # 現行WordPress最適化指示書
├── README.md                    # プロジェクト文書
├── config/                      # 設定ファイル
├── prompts/                     # フェーズ別プロンプトテンプレート
├── assets/                      # 静的アセット（CSS等）
├── instruction/                 # システム指示書文書
└── output/                      # 生成記事出力
```

## 設定ディレクトリ（`config/`）

- `workflow.yaml` - 7段階記事生成ワークフローの定義
- `requirements.yaml` - 記事品質・技術要件
- `factcheck_rules.yaml` - ファクトチェック検証ルール
- `templates.yaml` - コンテンツテンプレート・構造
- `wordpress-compatibility.yaml` - WordPress固有設定
- `wordpress-inline-css.md` - CSS統合文書

## プロンプトディレクトリ（`prompts/`）

順次実行ワークフロープロンプト（順序厳守）：
- `00_parse_request.md` - ユーザーリクエスト解析
- `01_research.md` - 情報収集（15-25回のweb検索）
- `02_structure.md` - 記事構造計画
- `03_writing.md` - コンテンツ作成
- `03_5_factcheck.md` - 事実検証（5-10回の追加検索）
- `04_optimization.md` - 旧SEO最適化
- `04_optimization_v2.md` - 現行WordPress最適化SEO
- `05_finalization.md` - 品質保証・最終出力

## アセットディレクトリ（`assets/`）

- `wordpress.css` - ベースCSSスタイル（変更禁止）
- `wordpress-fixed.css` - !important宣言付き強化CSS

## 主要ファイル関係

- **メイン指示書**: `INSTRUCTIONS_v2.md`が現行アクティブ指示セット
- **ワークフロー制御**: `config/workflow.yaml`でフェーズ実行順序を定義
- **CSS統合**: アセットはインライン必須、外部参照禁止
- **出力場所**: 生成記事は`output/`に日付ベースフォルダで保存

## 命名規則

- 設定ファイル: アンダースコア付き小文字
- プロンプトファイル: 実行順序の番号プレフィックス
- 出力ファイル: date_title形式で整理
- すべての日本語コンテンツはUTF-8エンコーディング

## ファイル依存関係

- 指示書はすべての設定・プロンプトファイルを参照
- プロンプトは検証ルール用設定ファイルを参照可能
- CSSアセットは最終HTML出力に埋め込み必須
- 生成記事に外部ファイル依存関係なし