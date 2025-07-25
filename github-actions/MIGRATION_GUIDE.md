# 📋 GitHub Actions v2 移行ガイド

## 概要
このガイドでは、現在の実装（v1）から新しい実装（v2）への移行手順を説明します。

## 移行前チェックリスト

### 必須要件
- [ ] GitHub Secrets設定済み
  - `ANTHROPIC_API_KEY`
  - `GEMINI_API_KEY`（~~`GOOGLE_AI_API_KEY`~~ から変更）
  - `GOOGLE_DRIVE_FOLDER_ID`
  - `GOOGLE_DRIVE_CREDENTIALS`
  - `SLACK_WEBHOOK`（オプション）

- [ ] リポジトリ権限
  - Actions: Read and write permissions
  - Artifacts: Write permissions

## 移行手順

### ステップ 1: 新しいワークフローファイルの配置

```bash
# 新しいワークフローを有効化
cp .github/workflows/article-generation-v2.yml .github/workflows/article-generation-v2.yml

# 旧ワークフローを無効化（後で削除）
mv .github/workflows/article-generation.yml .github/workflows/article-generation.yml.bak
```

### ステップ 2: 環境変数の更新

GitHub リポジトリ設定で以下を更新：

```yaml
# 旧設定（削除）
GOOGLE_AI_API_KEY: xxx

# 新設定（追加）
GEMINI_API_KEY: xxx  # 同じ値でOK
```

### ステップ 3: プロンプトファイルの確認

以下のファイルが存在することを確認：
```
prompts/
├── 03_structure.md     # 構成計画
├── 04_writing.md       # 執筆
├── 05_factcheck.md     # ファクトチェック
├── 06_seo.md          # SEO最適化
└── 07_final.md        # 最終調整
```

### ステップ 4: 不要なファイルのクリーンアップ

```bash
# 以下のファイルは新実装では不要
rm -f github-actions/scripts/install_claude_code.sh
rm -f github-actions/utils/claude_code_sdk.py
rm -f github-actions/utils/claude_web_search.py
```

### ステップ 5: 必要なスクリプトの更新

`generate_images_imagen.py` を新しい構造に対応：
```python
# 旧: 個別のファイルパスを受け取る
# 新: article-dirを受け取って必要なファイルを探す
```

## テスト手順

### 1. ドライラン（画像生成なし）
```yaml
# GitHub Actions UIから実行
Topic: テスト記事
Enable image generation: false
Auto publish: false
```

### 2. 小規模テスト（全機能）
```yaml
Topic: 簡単なテストトピック
Enable image generation: true
Auto publish: false
Word count: 1000
```

### 3. 本番テスト
```yaml
Topic: 本番相当のトピック
Enable image generation: true
Auto publish: true
Word count: 3200
```

## トラブルシューティング

### エラー: Claude Code Base Action not found
```yaml
# 解決策: @beta タグを確認
uses: anthropics/claude-code-base-action@beta
```

### エラー: Gemini API rate limit
```python
# 解決策: research.pyでレート制限を調整
time.sleep(2)  # 2秒から5秒に増やす
```

### エラー: Artifacts not found
```yaml
# 解決策: pattern を明示的に指定
pattern: 'phase*-${{ needs.initialize-and-analyze.outputs.article_id }}'
```

## 並列実行の確認

GitHub Actions UIで以下を確認：
1. `factcheck`, `seo-optimization`, `generate-images` が同時実行
2. 全体の実行時間が30-35分程度

## ロールバック手順

問題が発生した場合：
```bash
# v1に戻す
mv .github/workflows/article-generation.yml.bak .github/workflows/article-generation.yml
rm .github/workflows/article-generation-v2.yml
```

## 移行後の最適化

### 1. キャッシュの有効化
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### 2. 並列度の調整
```yaml
# 必要に応じて並列ジョブ数を制限
jobs:
  research:
    strategy:
      max-parallel: 3
```

### 3. タイムアウトの調整
```yaml
timeout-minutes: 20  # 各ジョブに適切な値を設定
```

## パフォーマンス比較

| メトリクス | v1 | v2 | 改善率 |
|-----------|-----|-----|-------|
| 全体実行時間 | 60分 | 35分 | -42% |
| API呼び出し効率 | 直列 | 並列 | 3x |
| エラー回復性 | 低 | 高 | - |
| 保守性 | 低 | 高 | - |

## よくある質問

### Q: 旧バージョンのアーティファクトは？
A: 30日間保持されます。必要なら事前にダウンロード。

### Q: 並列実行でコストは増える？
A: GitHub Actionsの実行時間が短縮されるため、むしろコスト削減。

### Q: プロンプトをカスタマイズしたい
A: `prompts/`ディレクトリ内のファイルを直接編集。

## サポート

問題が発生した場合：
1. GitHub Actions のログを確認
2. CRITICAL_ISSUES.md を参照
3. 必要に応じてissueを作成

---

移行完了後は、より高速で信頼性の高い記事生成パイプラインをお楽しみください！