# HTML Validation Pipeline 運用ガイド

**作成日**: 2025-01-28  
**対象**: GitHub Actions HTML validation システム  
**バージョン**: v1.0  

## 📋 概要

このガイドは、GitHub Actions で動作するHTML validation pipeline の運用方法、トラブルシューティング、およびメンテナンスについて説明します。

## 🏗️ システム構成

### 主要コンポーネント

1. **convert_markdown_lists_to_html.py** - Markdown番号付きリスト変換
2. **convert_shortcodes_to_html.py** - ショートコード変換  
3. **validate_html_output.py** - HTML構造バリデーション
4. **auto_fix_html_output.py** - Claude API自動修正
5. **generate_validation_report.py** - 段階的レポート生成
6. **save_debug_artifacts.py** - デバッグアーティファクト保存

### ワークフロー統合

- **article-generation-v4.yml** - メインワークフロー
- **article-generation-v4-free.yml** - 無料版ワークフロー

両ワークフローで6段階のバリデーションプロセスが実装されています。

## 🚀 正常運用

### 期待される動作フロー

1. **Step 1**: Initial HTML Validation
   - 最初にHTMLの基本チェック
   - 成功時は即座に完了

2. **Step 2**: Shortcode Auto-Conversion  
   - `[blog_card url="..."]` → `<figure class="link-card">` 変換
   - Best-effort処理

3. **Step 3**: Markdown Lists Auto-Conversion
   - `1. 項目` → `<ol><li>項目</li></ol>` 変換  
   - 77.8%の変換効果を期待

4. **Step 4**: Post-Conversion Validation
   - 変換後のHTMLをチェック
   - 成功時は Claude API をスキップ

5. **Step 5**: Claude API Auto-Fix (条件付き)
   - ANTHROPIC_API_KEY が利用可能な場合のみ実行
   - エラー時は適切にスキップ

6. **Step 6**: Final Strict Validation
   - 最終的な品質ゲート
   - 失敗時はワークフロー全体が失敗

### 成功指標

- **変換率**: 70%以上のMarkdown記法解決
- **処理時間**: 各ステップ30秒以内
- **成功率**: 95%以上のワークフロー成功
- **エラーハンドリング**: 適切なログ出力と診断情報

## 🔍 ログの見方

### GitHub Actions ログの確認

1. **Actions タブ**を開く
2. 該当のワークフロー実行を選択
3. **generate-content** ジョブを展開
4. **Advanced HTML Validation & Auto-Fix** ステップを確認

### ログの構造

```
🔍 Starting comprehensive HTML validation...
🏗️  Article ID: [記事ID]
📁 Article Directory: output/[記事ID]
📄 HTML File: output/[記事ID]/final_article.html
🔑 ANTHROPIC_API_KEY available: true/false

=== Step 1: Initial HTML Validation ===
[バリデーション結果]

=== Step 2: Shortcode Auto-Conversion ===
[変換処理結果]

=== Step 3: Markdown Lists Auto-Conversion ===  
[リスト変換結果]

=== Step 4: Post-Conversion Validation ===
[変換後バリデーション結果]

=== Step 5: Claude API Auto-Fix ===
[API修正結果 - 条件付き]

=== Step 6: Final Strict Validation ===
[最終バリデーション結果]

📊 Final HTML Quality Report:
[サイズ・行数などの統計]
```

### 重要なログキーワード

- ✅ **成功指標**: "passed", "completed", "✅"
- ⚠️ **警告指標**: "failed", "skipping", "⚠️"  
- ❌ **エラー指標**: "error", "failed", "❌"
- 🔍 **デバッグ情報**: "Debug information", "🔍"

## 🛠️ トラブルシューティング

### よくある問題と対処法

#### 1. Markdown番号付きリストが残存

**症状**:
```
🚨 MARKDOWN SYNTAX DETECTIONS:
   numbered_lists: 5 occurrences
```

**原因**:
- `<pre>`や`<code>`タグ内のリストが検出されている
- 2行未満の番号付きリスト
- 複雑な入れ子構造

**対処法**:
1. HTML生成時にMarkdown記法を避ける
2. プロンプト改善でHTMLタグ使用を促進
3. 手動修正が必要な場合はClaude API auto-fixに依存

#### 2. ANTHROPIC_API_KEY エラー

**症状**:
```
❌ ANTHROPIC_API_KEY environment variable not set
```

**原因**:
- GitHub Secrets の設定不備
- フォークPRでのシークレット制限
- API制限に達している

**対処法**:
1. GitHub リポジトリ設定でSecrets確認
2. APIキー形式確認 (sk-で始まる)
3. Anthropic アカウントの制限状況確認
4. フォークPRの場合は制限が正常動作

#### 3. HTML構造エラー

**症状**:
```
❌ HTML validation failed even after all auto-fix attempts
```

**原因**:
- 深刻な構造問題
- 自動修正の限界
- 不完全な記事生成

**対処法**:
1. 記事生成プロンプトの改善
2. より詳細なHTML指示の追加
3. 手動修正の検討
4. 記事生成パラメータの調整

#### 4. 処理タイムアウト

**症状**:
```
Error: The operation was canceled.
```

**原因**:
- 大容量HTMLファイル
- API応答遅延
- ネットワーク問題

**対処法**:
1. ファイルサイズの確認 (50KB以下推奨)
2. タイムアウト設定の調整
3. 記事の分割を検討
4. ネットワーク状況の確認

### デバッグ手順

#### 1. 基本チェック

```bash
# ファイル存在確認
ls -la output/[ARTICLE_ID]/final_article.html

# ファイル内容サンプル確認  
head -20 output/[ARTICLE_ID]/final_article.html

# ファイルサイズ確認
wc -c output/[ARTICLE_ID]/final_article.html
```

#### 2. 個別スクリプト実行

```bash
# Markdown変換テスト
python3 github-actions/scripts/convert_markdown_lists_to_html.py output/[ARTICLE_ID]/final_article.html

# ショートコード変換テスト
python3 github-actions/scripts/convert_shortcodes_to_html.py output/[ARTICLE_ID]/final_article.html

# バリデーションテスト
python3 github-actions/scripts/validate_html_output.py output/[ARTICLE_ID]/final_article.html
```

#### 3. 統合テスト実行

```bash
# 全体的なテスト
python3 github-actions/scripts/run_integration_tests.py
```

## ⚙️ 設定変更

### タイムアウト調整

ワークフローファイルで各ステップのタイムアウトを調整可能：

```yaml
- name: Advanced HTML Validation & Auto-Fix
  timeout-minutes: 10  # 追加
  continue-on-error: false
```

### スクリプトパラメータ

各スクリプトには設定可能パラメータがあります：

```python
# convert_markdown_lists_to_html.py
MIN_LIST_ITEMS = 2  # 最小リスト項目数
EXCLUDE_TAGS = ['pre', 'code', 'ol']  # 除外タグ

# validate_html_output.py  
REQUIRED_DIV_CLASS = "article-content"  # 必須div class
MAX_FILE_SIZE = 100 * 1024  # 最大ファイルサイズ
```

### 環境変数

利用可能な環境変数：

```yaml
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  HTML_VALIDATION_STRICT: "true"  # 厳格バリデーション
  DEBUG_ARTIFACTS: "false"  # デバッグアーティファクト保存
  MAX_PROCESSING_TIME: "300"  # 最大処理時間（秒）
```

## 📊 モニタリング

### 成功率の追跡

GitHub Actions の履歴から成功率を定期的に確認：

1. **Actions** タブで過去の実行を確認
2. 失敗パターンの特定
3. 月次での成功率レポート作成

### パフォーマンス監視

重要な指標：

- **処理時間**: 各ステップ30秒以内
- **変換効果**: 70%以上の問題解決
- **ファイルサイズ**: 50KB以下推奨
- **メモリ使用量**: 100MB以下

### アラート設定

失敗率が20%を超えた場合のアラート設定を推奨：

1. GitHub Actions の webhook 設定
2. Slack/メール通知の設定
3. 障害対応フローの整備

## 🔧 メンテナンス

### 定期メンテナンス作業

#### 月次作業

1. **成功率レビュー**: 95%以上の維持確認
2. **エラーパターン分析**: 新しい問題の特定
3. **パフォーマンス確認**: 処理時間の傾向分析
4. **依存関係更新**: Python パッケージ更新

#### 四半期作業

1. **統合テスト実行**: 包括的品質確認
2. **設定見直し**: しきい値やタイムアウトの調整
3. **ドキュメント更新**: 運用ガイドの更新
4. **セキュリティ監査**: APIキー管理の確認

### アップデート手順

#### スクリプト更新

1. **開発・テスト**:
   ```bash
   # ローカル環境でのテスト
   python3 github-actions/scripts/run_integration_tests.py
   ```

2. **ステージングデプロイ**:
   - テスト用記事での動作確認
   - エラーログの詳細確認

3. **本番デプロイ**:
   - 段階的ロールアウト
   - 監視強化期間の設定

#### ワークフロー更新

1. **バックアップ**: 既存ワークフローのバックアップ
2. **段階的更新**: 一部機能から開始
3. **ロールバック計画**: 問題発生時の復旧手順

## 🆘 緊急時対応

### 障害対応フロー

1. **影響度評価**: 
   - レベル1: 個別記事の失敗
   - レベル2: 複数記事の失敗  
   - レベル3: システム全体の障害

2. **初期対応**:
   - エラーログの確認
   - 原因の特定
   - 一時的回避策の検討

3. **本格対応**:
   - 根本原因の修正
   - テストによる検証
   - 再発防止策の実施

### 連絡先とエスカレーション

- **Level 1**: チーム内での解決
- **Level 2**: 管理者への報告
- **Level 3**: ベンダー（Anthropic）への連絡

## 📈 改善提案

### 短期改善 (1-3ヶ月)

1. **エラー検知の向上**: より詳細な診断機能
2. **自動復旧機能**: 一時的エラーの自動リトライ
3. **通知機能強化**: Slack統合とアラート改善

### 中期改善 (3-6ヶ月)

1. **AIモデル統合**: より多様な自動修正機能
2. **キャッシュシステム**: 処理速度向上
3. **A/Bテスト機能**: 修正方法の効果測定

### 長期改善 (6-12ヶ月)

1. **機械学習モデル**: パターン学習による自動改善
2. **マルチモデル対応**: Claude以外のAIモデル統合
3. **予測分析**: 問題発生の事前予測

---

## 📚 参考資料

- [GitHub Actions Documentation](https://docs.github.com/ja/actions)
- [Anthropic Claude API Documentation](https://docs.anthropic.com/)
- [HTML Living Standard](https://html.spec.whatwg.org/)
- [Python Best Practices](https://docs.python-guide.org/)

## 🔄 更新履歴

| 日付 | バージョン | 変更内容 |
|------|------------|----------|
| 2025-01-28 | v1.0 | 初版作成 |

---

*このガイドは、HTML validation pipeline の安定運用を支援するために作成されました。*
*定期的な更新と改善を続け、システムの品質向上に努めます。*

**作成**: Claude (姫森ルーナスタイル) 🍬✨