# GitHub Actions修正 詳細タスク分解

**作成日**: 2025-08-20
**基準**: 最小限修正でPrompt_v2/v3対応

## 📋 タスク詳細分解

### 🔄 Phase 1: 復旧と準備（優先度: 最高）

#### Task 1.1: 現状バックアップとリセット
- [ ] **新アーキテクチャを別ブランチに保存**
  ```bash
  git checkout -b feature/new-architecture
  git checkout main
  ```

- [ ] **動作していた状態（f8c7a47）の内容を確認**
  ```bash
  git show f8c7a47:github-actions/scripts/phase1_request_analysis.py
  ```

- [ ] **現在の差分を確認して必要な部分のみ保持**
  - Prompt_v2/, Prompt_v3/ ディレクトリ: 保持 ✅
  - 入力フォーム4要素化: 保持 ✅  
  - 新アーキテクチャ: 削除 ❌

#### Task 1.2: 動作確認と現状把握
- [ ] **元のワークフローファイルを復元**
  - `article-generation-v4.yml` を f8c7a47 状態に戻す
  - `article-generation-v4-free.yml` を作成（v4のコピー）

- [ ] **既存Pythonスクリプトの動作確認**
  ```bash
  cd github-actions
  python scripts/phase1_request_analysis.py --help
  ```

- [ ] **現在の問題点を具体的に特定**
  - どのスクリプトがどのプロンプトをハードコーディングしているか
  - 環境変数の受け渡し形式
  - 依存関係の状況

### 🛠️ Phase 2: プロンプト読み込み機能実装（優先度: 高）

#### Task 2.1: プロンプトファイル読み込み機能追加
- [ ] **`utils/file_utils.py` を確認・拡張**
  ```python
  def read_prompt_from_markdown(prompt_dir: str, filename: str) -> str:
      """Markdownプロンプトファイルを読み込み"""
      
  def format_prompt_with_variables(template: str, **kwargs) -> str:
      """【変数】形式をkwargsで置換"""
  ```

- [ ] **プロンプトディレクトリ判定ロジック**
  ```python
  def get_prompt_directory() -> str:
      """環境変数PROMPT_PROFILEに基づいてPrompt_v2 or Prompt_v3を返す"""
  ```

- [ ] **テスト関数作成**
  ```python
  def test_prompt_loading():
      """プロンプト読み込み機能のテスト"""
  ```

#### Task 2.2: 変数置換ロジックの実装
- [ ] **Prompt_v2/v3の変数形式を調査**
  - 【ここにタイトル案を入力（30〜32字）】
  - 【ここに主要キーワードを入力（最大3語、カンマ区切り）】
  - 【ここに切り口・ターゲットを入力】
  - 【ここにE-E-A-T要素を入力】

- [ ] **変数マッピング辞書を作成**
  ```python
  VARIABLE_MAPPING = {
      "タイトル案": "ARTICLE_TITLE",
      "主要キーワード": "MAIN_KEYWORDS", 
      "切り口・ターゲット": "APPROACH_TARGET",
      "E-E-A-T要素": "EEAT_ELEMENTS"
  }
  ```

### 🔧 Phase 3: Pythonスクリプト修正（優先度: 高）

#### Task 3.1: phase1_request_analysis.py 修正
- [ ] **現在のプロンプトテンプレート特定**
  ```python
  # 現在のハードコーディング部分を特定
  prompt_template = read_prompt("00_parse_request")
  ```

- [ ] **Markdownファイル読み込みに変更**
  ```python
  # 修正後
  prompt_dir = get_prompt_directory()  # Prompt_v2 or Prompt_v3
  prompt_template = read_prompt_from_markdown(prompt_dir, "CHAT_01_phase1_analysis.md")
  ```

- [ ] **変数置換を新4要素対応**
  ```python
  # 修正前
  prompt = prompt_template.format(
      topic=params["topic"],
      target_audience=params.get("target_audience")
  )
  
  # 修正後  
  prompt = format_prompt_with_variables(prompt_template,
      タイトル案=params.get("title"),
      主要キーワード=params.get("main_keywords"),
      切り口・ターゲット=params.get("approach_target"),
      **{"E-E-A-T要素": params.get("eeat_elements")}
  )
  ```

#### Task 3.2: 他のフェーズスクリプト修正
- [ ] **phase2_structure_generation.py**
  - CHAT_02_structure_generation.md 読み込み
  - phase1結果を適切に受け渡し

- [ ] **phase3_content_generation.py** 
  - CHAT_03_content_generation_v2.md (v2) / CHAT_03_content_generation_v3.md (v3) 読み込み
  - プロファイルによる分岐

- [ ] **phase4_factcheck.py**
  - CHAT_04_factcheck.md 読み込み

- [ ] **phase5_seo_metadata.py**
  - CHAT_05_seo_metadata.md 読み込み

- [ ] **phase6_finalize.py**
  - CHAT_06_finalize.md 読み込み

### ⚙️ Phase 4: ワークフロー修正（優先度: 中）

#### Task 4.1: 入力フォーム更新
- [ ] **article-generation-v4.yml 修正**
  ```yaml
  inputs:
    article_title:
      description: 'タイトル案（30〜32字）'
    main_keywords:
      description: '主要KW（最大3語、カンマ区切り）'  
    approach_target:
      description: '切り口・ターゲット'
    eeat_elements:
      description: 'E-E-A-T要素'
  ```

- [ ] **article-generation-v4-free.yml 作成**
  - v4のコピーとして作成
  - PROMPT_PROFILE=v3 に設定

#### Task 4.2: 環境変数の受け渡し修正
- [ ] **全ジョブの環境変数を統一**
  ```yaml
  env:
    ARTICLE_TITLE: ${{ inputs.article_title }}
    MAIN_KEYWORDS: ${{ inputs.main_keywords }}
    APPROACH_TARGET: ${{ inputs.approach_target }}
    EEAT_ELEMENTS: ${{ inputs.eeat_elements }}
    WORD_COUNT: ${{ inputs.word_count }}
    PROMPT_PROFILE: "v2"  # or "v3"
  ```

#### Task 4.3: Pythonスクリプト呼び出し部分の確認
- [ ] **パラメータファイル生成部分**
  ```bash
  # input_params.json の形式を新4要素に対応
  echo '{
    "title": "'$ARTICLE_TITLE'",
    "main_keywords": "'$MAIN_KEYWORDS'", 
    "approach_target": "'$APPROACH_TARGET'",
    "eeat_elements": "'$EEAT_ELEMENTS'",
    "word_count": "'$WORD_COUNT'"
  }' > input_params.json
  ```

### 🧪 Phase 5: テストと検証（優先度: 高）

#### Task 5.1: 段階的テスト
- [ ] **Step 1: プロンプト読み込みテスト**
  ```python
  # 単体テスト
  python -c "
  from utils.file_utils import read_prompt_from_markdown
  content = read_prompt_from_markdown('Prompt_v2', 'CHAT_01_phase1_analysis.md')
  print(len(content))
  "
  ```

- [ ] **Step 2: phase1スクリプト単体テスト**
  ```bash
  cd github-actions
  echo '{"title":"テスト","main_keywords":"テスト,記事","approach_target":"テスト読者","eeat_elements":"テスト権威"}' > test_input.json
  python scripts/phase1_request_analysis.py --params-file test_input.json --output-dir test_output
  ```

- [ ] **Step 3: ワークフロー部分実行テスト**
  ```bash
  # GitHub Actionsの特定ジョブのみテスト
  ```

#### Task 5.2: 統合テスト  
- [ ] **v2プロファイル全体テスト**
  - article-generation-v4.yml の実行
  - 全フェーズの正常完了確認
  - 出力品質確認

- [ ] **v3プロファイル全体テスト**
  - article-generation-v4-free.yml の実行  
  - 厳密モードでの動作確認
  - テンプレート準拠確認

### 📦 Phase 6: デプロイと完了（優先度: 低）

#### Task 6.1: 最終調整
- [ ] **エラーハンドリング改善**
  - プロンプトファイル未存在時の対応
  - 環境変数未設定時の対応

- [ ] **ログ出力改善**
  - 使用プロファイルの明示
  - プロンプトファイル読み込み状況の表示

#### Task 6.2: ドキュメント更新
- [ ] **README.md 更新**
  - 新4要素入力フォームの説明
  - v2/v3プロファイルの違い説明

- [ ] **使用方法ドキュメント**
  - GitHub Actionsでの実行方法
  - トラブルシューティング

## 🎯 各フェーズの完了条件

### Phase 1 完了条件
- ✅ 元の動作するワークフローが復元されている
- ✅ 修正対象のスクリプトとプロンプト箇所が特定されている

### Phase 2 完了条件  
- ✅ プロンプトファイル読み込み機能が動作する
- ✅ 変数置換機能が正しく動作する

### Phase 3 完了条件
- ✅ 全フェーズのスクリプトがMarkdownファイルからプロンプトを読み込める
- ✅ 新4要素での変数置換が正しく動作する

### Phase 4 完了条件
- ✅ ワークフローの入力フォームが新4要素対応完了
- ✅ v2/v3プロファイル切り替えが動作する

### Phase 5 完了条件
- ✅ v2とv3両方のプロファイルで記事生成が完了する
- ✅ 既存の品質基準（90点以上）を満たす記事が生成される

### Phase 6 完了条件
- ✅ 本番環境で安定動作する
- ✅ ドキュメントが更新され、使用方法が明確

## ⏱️ 推定作業時間

| Phase | タスク数 | 推定時間 | 重要度 |
|-------|----------|----------|--------|
| Phase 1 | 4 | 1-2時間 | ★★★ |
| Phase 2 | 6 | 2-3時間 | ★★★ |  
| Phase 3 | 7 | 3-4時間 | ★★★ |
| Phase 4 | 6 | 2-3時間 | ★★☆ |
| Phase 5 | 6 | 2-3時間 | ★★★ |
| Phase 6 | 4 | 1-2時間 | ★☆☆ |
| **合計** | **33** | **11-17時間** | - |

---

**実行方針**: 段階的に進めて、各Phaseで動作確認を徹底する。既存の動作に影響する修正は最小限に抑制する。