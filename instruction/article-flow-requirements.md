# 記事自動生成システム要件定義書 - GitHub Actions版

## 1. システム概要

### 1.1 プロジェクト名
Article Flow Automation System (AFAS)

### 1.2 目的
高品質なSEO最適化記事を自動生成し、ファクトチェック済みの信頼性の高いコンテンツをGoogle Driveに自動納品するシステム

### 1.3 スコープ
- 記事生成の完全自動化（リサーチから納品まで）
- 画像生成と記事への統合
- 品質保証プロセスの自動化
- Google Driveへの自動アップロード

## 2. 機能要件

### 2.1 記事生成プロセス（7フェーズ）

#### フェーズ1: リクエスト解析
- **入力**: トピック、店舗URL（オプション）、ターゲット読者（オプション）、目標文字数
- **処理**: パラメータ抽出と検証
- **出力**: 構造化された記事パラメータ

#### フェーズ2: リサーチ
- **要件**: 15-25回のWeb検索実行
- **優先順位**: 
  - very_high: 政府機関（.go.jp, .gov）
  - high: 学術機関（.ac.jp, .edu）、医学会
  - medium_high: 業界団体、大手メディア
- **並列処理**: 5バッチで並列実行

#### フェーズ3: 構成計画
- **要件**: エビデンスベースの記事構成
- **出力**: 
  - H2見出し: 6個
  - FAQ: 7問
  - 内部リンク計画

#### フェーズ4: 執筆
- **要件**: 
  - 文字数: 3200±300字
  - オリジナリティ: 100%
  - メインキーワード密度: 2.5-3.5%
- **制約**: 
  - 絶対的表現の禁止
  - 曖昧表現の禁止
  - 誇大表現の禁止

#### フェーズ5: ファクトチェック
- **検証項目**:
  - 数値・統計データ
  - 医学的・科学的主張
  - 効果・効能の記述
  - 比較・評価表現
- **目標スコア**: 90点以上

#### フェーズ6: SEO最適化
- **要件**:
  - HTML変換
  - メタディスクリプション: 140-160字
  - 構造化データマークアップ
  - WordPress CSS適用

#### フェーズ7: 最終調整
- **品質チェック**: 
  - 品質スコア: 85点以上
  - ファクトチェックスコア: 90点以上
- **最終確認**: 論理的流れ、文字数バランス

### 2.2 画像生成要件

#### 生成する画像
1. **アイキャッチ画像**: 1枚（1200x630px推奨）
2. **セクション画像**: 3-5枚（800x600px推奨）
3. **図解・インフォグラフィック**: 必要に応じて

#### 画像生成サービス
- **第一選択**: DALL-E 3（高品質、$0.04-0.08/枚）
- **第二選択**: Stable Diffusion API（低コスト、$0.002/枚）
- **第三選択**: Replicate（多様なモデル）

### 2.3 納品要件

#### Google Driveフォルダ構造
```
/article-flow-output/
├── 2025-01-24_爪ケア/
│   ├── article.html
│   ├── article.md
│   ├── images/
│   │   ├── hero.png
│   │   ├── section-1.png
│   │   └── section-2.png
│   ├── metadata.json
│   ├── quality-report.json
│   └── factcheck-report.json
```

#### メタデータ内容
```json
{
  "title": "記事タイトル",
  "topic": "爪ケア",
  "generated_at": "2025-01-24T10:30:00Z",
  "word_count": 3215,
  "quality_score": 92,
  "factcheck_score": 95,
  "keywords": ["爪ケア", "ネイルケア", "健康"],
  "target_audience": "セルフケア志向の女性",
  "store_url": "https://example.com",
  "images": {
    "hero": "images/hero.png",
    "sections": ["images/section-1.png", "images/section-2.png"]
  }
}
```

## 3. 非機能要件

### 3.1 パフォーマンス
- **処理時間**: 30-45分/記事（画像生成含む）
- **並列処理**: 最大5記事同時生成可能
- **タイムアウト**: 各フェーズ最大10分

### 3.2 信頼性
- **エラーハンドリング**: 各フェーズでリトライ機能（最大3回）
- **部分的失敗の処理**: 失敗フェーズのみ再実行可能
- **ログ記録**: 全処理の詳細ログ保存

### 3.3 拡張性
- **プロンプトのカスタマイズ**: 外部ファイルで管理
- **新しい画像生成サービスの追加**: プラグイン形式
- **出力先の追加**: インターフェース定義済み

### 3.4 使いやすさ
- **手動トリガー**: GitHub ActionsのUIから簡単実行
- **自動トリガー**: スケジュール実行、Webhook対応
- **進捗確認**: リアルタイムステータス表示

## 4. 技術スタック

### 4.1 コア技術
- **CI/CD**: GitHub Actions
- **言語**: Python 3.11+, Node.js 18+
- **AI/ML**: 
  - Claude API（記事生成）
  - OpenAI API（画像生成）
  - Bing Search API（リサーチ）

### 4.2 必要なAPIキー/認証
```yaml
secrets:
  ANTHROPIC_API_KEY      # Claude API（必須）
  OPENAI_API_KEY         # DALL-E 3（必須）
  BING_SEARCH_KEY        # Web検索（必須）
  GOOGLE_DRIVE_CREDENTIALS # Google Drive（必須）
  STABILITY_API_KEY      # Stable Diffusion（オプション）
  SLACK_WEBHOOK          # 通知（オプション）
```

### 4.3 主要ライブラリ
- **Python**:
  - anthropic（Claude API）
  - openai（画像生成）
  - google-api-python-client（Drive）
  - beautifulsoup4（HTML処理）
  - pandas（データ処理）
  
- **Node.js**:
  - @anthropic-ai/sdk
  - @google/generative-ai
  - puppeteer（必要に応じて）

## 5. ワークフロー実装

### 5.1 メインワークフロー構造
```yaml
name: Article Generation Pipeline
on:
  workflow_dispatch:
    inputs:
      topic:
        description: '記事のトピック'
        required: true
        type: string
      store_url:
        description: '店舗URL'
        required: false
        type: string
      target_audience:
        description: 'ターゲット読者'
        required: false
        type: choice
        options:
          - 'セルフケア志向の女性'
          - '健康意識の高い男性'
          - 'シニア層'
          - '若年層'
          - 'ファミリー層'
      word_count:
        description: '目標文字数'
        required: false
        type: string
        default: '3200'
      auto_publish:
        description: 'Google Driveに自動アップロード'
        type: boolean
        default: true

jobs:
  generate-article:
    runs-on: ubuntu-latest
    timeout-minutes: 60
```

### 5.2 トリガーパターン

#### パターン1: 手動実行（推奨）
- GitHub Actions UIから直接実行
- パラメータを細かく指定可能

#### パターン2: スケジュール実行
```yaml
on:
  schedule:
    # 毎週月・水・金の朝10時（JST）
    - cron: '0 1 * * 1,3,5'
```

#### パターン3: API/Webhook
```yaml
on:
  repository_dispatch:
    types: [generate-article]
```

#### パターン4: プルリクエストコメント
```yaml
on:
  issue_comment:
    types: [created]
# コメント例: @generate-article 爪ケア
```

### 5.3 並列処理戦略

#### リサーチフェーズの並列化
```yaml
research:
  strategy:
    matrix:
      batch: [1, 2, 3, 4, 5]
    max-parallel: 5
```

#### 画像生成の並列化
```yaml
image-generation:
  strategy:
    matrix:
      image_type: [hero, section1, section2, section3]
    max-parallel: 4
```

## 6. エラーハンドリングと監視

### 6.1 リトライ戦略
```yaml
- name: API Call with Retry
  uses: nick-invision/retry@v3
  with:
    timeout_minutes: 10
    max_attempts: 3
    retry_wait_seconds: 30
    command: python generate_content.py
```

### 6.2 通知設定
- **成功時**: Slack通知 + メール（オプション）
- **失敗時**: 詳細エラーログ + 管理者通知
- **部分的成功**: 成功部分の保存 + 失敗箇所の明示

### 6.3 ログ管理
- **実行ログ**: GitHub Actions内で90日保存
- **詳細ログ**: Google Driveに永続保存
- **メトリクス**: 処理時間、成功率、品質スコアの追跡

## 7. セキュリティ要件

### 7.1 認証情報管理
- すべてのAPIキーはGitHub Secretsで管理
- ローテーション推奨期間: 90日
- 最小権限の原則を適用

### 7.2 データ保護
- 生成コンテンツの暗号化転送
- Google Driveの適切な共有設定
- 個人情報・機密情報の自動検出と除外

### 7.3 アクセス制御
- ワークフロー実行権限の制限
- 監査ログの有効化
- 不正アクセスの検知と通知

## 8. 運用要件

### 8.1 初期セットアップ
1. リポジトリのフォーク/クローン
2. 必要なAPIキーの取得と設定
3. Google Drive認証の設定
4. 初回テスト実行

### 8.2 日常運用
- **記事生成**: workflow_dispatchから実行
- **結果確認**: Google Driveで確認
- **品質管理**: レポートの定期レビュー

### 8.3 メンテナンス
- **プロンプト更新**: prompts/フォルダ内のファイル編集
- **設定変更**: config/フォルダ内のYAML編集
- **依存関係更新**: 月1回の定期更新推奨

## 9. コスト見積もり

### 9.1 API利用料（記事1本あたり）
- **Claude API**: 約$0.30-0.50（3-5万トークン）
- **DALL-E 3**: 約$0.20-0.40（5枚）
- **Bing Search**: 約$0.05（25回検索）
- **合計**: 約$0.55-0.95/記事

### 9.2 月間コスト予測
- **10記事/月**: 約$5.5-9.5
- **30記事/月**: 約$16.5-28.5
- **100記事/月**: 約$55-95

### 9.3 インフラコスト
- **GitHub Actions**: パブリックリポジトリは無料
- **Google Drive**: 既存プランで対応可能
- **追加コスト**: なし

## 10. 今後の拡張計画

### 10.1 短期（3ヶ月以内）
- 多言語対応（英語、中国語）
- 動画コンテンツの自動生成
- A/Bテスト機能の追加

### 10.2 中期（6ヶ月以内）
- リアルタイムプレビュー機能
- コンテンツ管理システム（CMS）統合
- 複数サイトへの同時配信

### 10.3 長期（1年以内）
- AIによる記事改善提案
- 読者行動分析との連携
- 完全自律型コンテンツ生成

## 11. 成功指標（KPI）

### 11.1 品質指標
- **品質スコア平均**: 90点以上
- **ファクトチェックスコア**: 95点以上
- **エラー率**: 5%未満

### 11.2 効率指標
- **平均生成時間**: 30分以内
- **自動化率**: 95%以上
- **人的介入頻度**: 10%未満

### 11.3 ビジネス指標
- **コンテンツ生産性**: 300%向上
- **コスト削減**: 70%削減
- **品質向上**: 20%向上

---

この要件定義書に基づいて、段階的な実装を進めることを推奨します。
まずは最小構成（MVP）から始め、徐々に機能を追加していくアプローチが効果的です。