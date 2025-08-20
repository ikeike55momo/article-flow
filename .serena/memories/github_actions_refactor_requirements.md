# GitHub Actions 記事生成ワークフロー修正要件定義

**作成日**: 2025-08-20
**対象**: article-flow プロジェクト
**目的**: 元々動作していたGitHub Actionsワークフローを最小限の修正でPrompt_v2/v3対応させる

## 現状分析

### 動作していた状態（コミット f8c7a47 付近）
- `C:\article-flow\github-actions\scripts\` 内のPythonスクリプト群が正常動作
- GitHub Actionsワークフローが完全自動化で動作
- MCP imagen画像生成機能が実装済み
- リサーチ、ファクトチェック、SEO最適化等の全機能が動作

### 現在の問題
- プロンプトがPythonスクリプト内にハードコーディング
- 入力フォームが旧形式（target_persona, meta_keywords）
- 新しい4要素（main_keywords, approach_target, eeat_elements）に非対応

### 現在利用可能なリソース
- `C:\article-flow\Prompt_v2\` - 柔軟なプロンプト戦略
- `C:\article-flow\Prompt_v3\` - 厳密なテンプレート準拠戦略
- 既存の全Python utilities（`utils/claude_api.py` 等）
- 動作実績のあるGitHub Actions環境

## 要件定義

### 1. 最小限の修正原則
- **既存の動作するコードは極力変更しない**
- **新機能追加ではなく、必要な箇所のみ修正**
- **動作実績のあるアーキテクチャを維持**

### 2. 具体的な修正要件

#### A. 入力フォーム更新
**対象ファイル**: 
- `.github/workflows/article-generation-v4.yml`
- `.github/workflows/article-generation-v4-free.yml`

**修正内容**:
```yaml
# 変更前
target_persona: 'ターゲットペルソナ（例：30代女性、健康意識が高い、子育て中）'
meta_keywords: 'メタキーワード（カンマ区切り）'

# 変更後  
main_keywords: '主要KW（最大3語、カンマ区切り）'
approach_target: '切り口・ターゲット'
eeat_elements: 'E-E-A-T要素（Experience, Expertise, Authoritativeness, Trustworthiness）'
```

#### B. 環境変数の受け渡し更新
**対象**: 全ジョブの環境変数設定

**修正内容**:
```yaml
# 変更前
TARGET_PERSONA=${{ inputs.target_persona }}
META_KEYWORDS=${{ inputs.meta_keywords }}

# 変更後
MAIN_KEYWORDS=${{ inputs.main_keywords }}
APPROACH_TARGET=${{ inputs.approach_target }}
EEAT_ELEMENTS=${{ inputs.eeat_elements }}
```

#### C. Pythonスクリプトのプロンプト読み込み修正
**対象ファイル**: 
- `github-actions/scripts/phase1_request_analysis.py`
- その他のフェーズスクリプト

**修正内容**:
1. ハードコーディングされたプロンプトを削除
2. `Prompt_v2/` または `Prompt_v3/` からMarkdownファイルを読み込み
3. プロンプト内の変数置換を新4要素に対応

#### D. プロンプトファイル読み込み機能追加
**対象**: `utils/file_utils.py` または新規

**追加機能**:
```python
def read_prompt_from_dir(prompt_dir: str, filename: str) -> str:
    """プロンプトディレクトリからMarkdownファイルを読み込み"""
    
def format_prompt_variables(template: str, **kwargs) -> str:
    """【変数】形式の置換処理"""
```

#### E. v2/v3プロファイル切り替え
**方式**: 環境変数による切り替え
```yaml
# v4 → Prompt_v2 使用
PROMPT_PROFILE: "v2"

# v4-free → Prompt_v3 使用  
PROMPT_PROFILE: "v3"
```

### 3. 保持すべき既存機能
- ✅ MCP imagen画像生成
- ✅ Geminiリサーチ機能
- ✅ ファクトチェック（90点以上要求）
- ✅ SEO最適化
- ✅ Google Drive アップロード
- ✅ エラーハンドリングとリトライ
- ✅ GitHub Actions artifacts
- ✅ 品質レポート生成

### 4. 検証要件
- ✅ 既存テストケースが全て通ること
- ✅ v2（柔軟）とv3（厳密）両方が動作すること
- ✅ 画像生成が正常に動作すること
- ✅ 品質スコア計算が正しく動作すること

## タスク一覧

### Phase 1: 準備作業
1. **現在の状態をバックアップ**
   - 新アーキテクチャをブランチに保存
   - f8c7a47状態に戻す

2. **動作確認**
   - 元のワークフローが動作することを確認
   - 現在の問題点を具体的に特定

### Phase 2: 最小限修正
3. **プロンプト読み込み機能追加**
   - `utils/` にプロンプトファイル読み込み機能を追加
   - 既存の `read_prompt()` 関数を拡張

4. **phase1スクリプト修正**
   - `phase1_request_analysis.py` のプロンプト部分をファイル読み込みに変更
   - 新4要素対応の変数置換

5. **他フェーズスクリプト修正**
   - phase2, phase3, phase4, phase5, phase6 の順次修正

6. **ワークフロー修正**
   - 入力フォームを4要素に変更
   - 環境変数の受け渡しを修正

### Phase 3: テストと検証
7. **動作テスト**
   - v2プロファイルでのテスト実行
   - v3プロファイルでのテスト実行

8. **品質確認**
   - 既存機能が全て動作することを確認
   - 出力品質が維持されていることを確認

### Phase 4: デプロイと完了
9. **本番反映**
   - メインブランチへのマージ
   - 動作確認とドキュメント更新

## 成功基準

### 機能面
- ✅ GitHub Actionsで記事生成が完全自動で動作
- ✅ v2（柔軟）とv3（厳密）両プロファイルが動作
- ✅ 新4要素入力フォームが正常動作
- ✅ MCP imagen画像生成が動作
- ✅ 品質スコア90点以上を維持

### 技術面
- ✅ 既存の動作実績を維持
- ✅ 最小限の変更で最大の効果
- ✅ 保守性を損なわない
- ✅ 拡張性を確保

## リスク管理

### 高リスク項目
- ⚠️ 既存スクリプトの動作に影響する変更
- ⚠️ GitHub Actions環境での依存関係変更
- ⚠️ MCP imagen連携の破損

### 対策
- 🛡️ 段階的な修正とテスト
- 🛡️ バックアップブランチの維持
- 🛡️ 各修正後の動作確認徹底

---

**重要**: この要件定義に基づいて、既存の動作するシステムを最小限の修正で新機能に対応させる。新しいアーキテクチャの作り直しは行わない。