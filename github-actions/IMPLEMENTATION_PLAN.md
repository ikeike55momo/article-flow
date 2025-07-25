# GitHub Actions実装計画書 - Claude Code SDK + Gemini統合

## 1. 現状分析と課題

### 1.1 調査結果
#### Claude Code SDK
- **問題点**: `claude -p --resume`が非対話モードで動作しない既知の問題
- **推奨方法**: GitHub Actions内では`anthropics/claude-code-action@beta`を使用
- **ベストプラクティス**: 
  - CLAUDE.mdファイルでプロジェクト固有のガイドライン設定
  - MCPサーバー統合による機能拡張
  - ツール制限による安全性確保

#### Gemini API Web Grounding
- **最新版**: Gemini 2.0以降は`google_search`ツールを使用
- **特徴**: 
  - リアルタイムWeb検索
  - 自動的な複数クエリ実行
  - 引用メタデータ付き応答
  - 1日100万クエリまで（デフォルト）

### 1.2 現在の実装の課題
1. Python SDKの直接使用（Claude Code SDKではない）
2. 架空のClaude Web Search実装
3. APIキーの重複（GOOGLE_AI_API_KEY vs GEMINI_API_KEY）
4. エラーハンドリングの不足

## 2. 新アーキテクチャ設計

### 2.1 技術スタック
```yaml
記事生成エンジン:
  - Claude Code Action (GitHub Actions専用)
  - ANTHROPIC_API_KEY

Web検索エンジン:
  - Gemini API with Google Search Tool
  - GEMINI_API_KEY

画像生成:
  - Imagen via Gemini API
  - GEMINI_API_KEY (共用)

ストレージ:
  - Google Drive API
  - サービスアカウント認証
```

### 2.2 ワークフロー構成
```
1. Claude Code Action → リクエスト解析
2. Gemini API → Web検索（並列実行）
3. Claude Code Action → 構成計画
4. Claude Code Action → 執筆
5. Claude Code Action → ファクトチェック
6. Claude Code Action → SEO最適化
7. Claude Code Action → 最終調整
8. Imagen (Gemini) → 画像生成
9. Google Drive → アップロード
```

## 3. 実装方針

### 3.1 Claude Code統合方法

#### オプション1: Claude Code Action使用（推奨）
```yaml
- uses: anthropics/claude-code-action@beta
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    allowed_tools: "Write,Edit,View"
    claude_env: |
      PHASE=article_writing
      OUTPUT_DIR=${{ steps.init.outputs.article_id }}
```

#### オプション2: カスタムアクション作成
```yaml
- name: Run Claude Code
  run: |
    # Claude Code CLIを直接実行
    claude -p "$(cat prompt.txt)" \
      --output-format json \
      --max-tokens 4096 > output.json
```

### 3.2 Gemini Web検索実装

```python
# 正しいGemini 2.0実装
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Google Search toolを有効化
response = model.generate_content(
    prompt,
    tools=[genai.Tool.from_google_search()],
    generation_config=genai.GenerationConfig(
        temperature=1.0,  # 推奨値
        max_output_tokens=2048
    )
)

# groundingMetadataから引用情報を抽出
grounding_metadata = response.grounding_metadata
```

### 3.3 エラーハンドリング強化

```yaml
# リトライ戦略
retry-strategy:
  matrix:
    phase: [1, 2, 3, 4, 5, 6, 7]
  fail-fast: false
  max-parallel: 1
```

## 4. 実装手順

### Phase 1: 基盤整備（優先度: 高）
1. [ ] Claude Code Actionの設定
2. [ ] CLAUDE.mdファイルの作成
3. [ ] Gemini API統合スクリプトの修正
4. [ ] 環境変数の統一（GEMINI_API_KEY）

### Phase 2: コア機能実装（優先度: 高）
1. [ ] フェーズ1-7をClaude Code Actionに移行
2. [ ] Gemini Web検索の正しい実装
3. [ ] 並列処理の最適化
4. [ ] エラーハンドリングの実装

### Phase 3: 統合とテスト（優先度: 中）
1. [ ] ワークフロー全体のテスト
2. [ ] パフォーマンス測定
3. [ ] コスト分析
4. [ ] ドキュメント更新

### Phase 4: 最適化（優先度: 低）
1. [ ] Depotランナーの導入（コスト削減）
2. [ ] キャッシュ戦略の実装
3. [ ] 監視とアラートの設定

## 5. 移行計画

### 5.1 段階的移行
1. **Week 1**: 開発環境でのテスト
2. **Week 2**: ステージング環境での検証
3. **Week 3**: 本番環境への段階的デプロイ
4. **Week 4**: 旧システムの廃止

### 5.2 ロールバック計画
- 各フェーズは独立して実行可能
- 旧実装との並行運用期間を設定
- フィーチャーフラグによる切り替え

## 6. 成功指標

### 6.1 技術指標
- [ ] 全フェーズの正常動作率: 95%以上
- [ ] 平均処理時間: 30分以内
- [ ] APIエラー率: 1%未満

### 6.2 品質指標
- [ ] ファクトチェックスコア: 90点以上
- [ ] SEO品質スコア: 85点以上
- [ ] 画像生成成功率: 98%以上

### 6.3 コスト指標
- [ ] 1記事あたりコスト: $0.60以下
- [ ] APIコスト削減: 30%以上

## 7. リスクと対策

### 7.1 技術リスク
| リスク | 影響度 | 対策 |
|--------|--------|------|
| Claude Code Action非互換 | 高 | カスタムアクション作成 |
| Gemini APIレート制限 | 中 | バッチ処理とキューイング |
| GitHub Actions制限 | 低 | Depotランナー使用 |

### 7.2 運用リスク
- **APIキー漏洩**: GitHub Secretsの適切な管理
- **コスト超過**: 使用量監視とアラート設定
- **サービス停止**: フォールバック機能の実装

## 8. 実装状況

### 完了項目 ✓
1. **調査とリサーチ**
   - Claude Code Action仕様調査
   - Gemini API Web Grounding調査
   - 実装計画書作成

2. **ガイドライン作成**
   - CLAUDE.md - プロジェクトガイドライン
   - GEMINI.md - Gemini固有の設定

3. **基本実装**
   - GitHub Actionsワークフロー
   - Gemini CLI統合（Web検索）
   - 環境変数統一（GEMINI_API_KEY）

### 次のステップ
1. **Claude Code Base Action統合**
   - 各フェーズをBase Actionに移行
   - プロンプトファイル方式に変更

2. **テストと検証**
   - エンドツーエンドテスト
   - パフォーマンス測定

3. **ドキュメント更新**
   - READMEの最終更新
   - 運用手順書作成

---

この計画に基づいて、段階的かつ確実な実装を進めていきます。