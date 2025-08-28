# HTML バリデーション処理改善要件定義書

## 1. 問題概要

### 1.1 現在発生している問題
1. **Markdown番号付きリスト残存**: HTMLファイル内に `1. 〜` `2. 〜` 形式が14個残存
2. **Claude API自動修正の環境変数エラー**: `ANTHROPIC_API_KEY environment variable not set`
3. **ワークフロー全体失敗**: 中間検証失敗でexit code 1により後続処理が実行されない

### 1.2 影響範囲
- generate-contentジョブが失敗してワークフロー全体が停止
- HTML専用出力の品質保証が機能不全
- 記事生成プロセスが不安定

## 2. 根本原因分析

### 2.1 問題1: Markdown番号付きリスト残存の原因
**現象**: 
```
1. 甘皮・ささくれトラブルの原因を正しく理解しよう
2. プロが実践する正しい甘皮処理の基本手順  
3. ささくれの適切な対処法と応急処置
```

**原因分析**:
- HTMLブロック内のMarkdownは通常のMarkdownパーサの対象外
- ショートコード変換（`[blog_card]`）は成功したが番号付きリストは未処理
- `convert_shortcodes_to_html.py`では番号付きリストに対応していない

### 2.2 問題2: 環境変数エラーの原因
**エラーメッセージ**: `❌ ANTHROPIC_API_KEY environment variable not set`

**想定原因**:
- フォークPRではSecretsが提供されない（セキュリティ制約）
- envのスコープ（job/step）設定が不適切
- Composite Actionへのenv受け渡し漏れ
- pull_requestトリガーでのSecrets制限

### 2.3 問題3: ワークフロー設計の課題
**現在の処理フロー**:
1. HTMLバリデーション → 失敗
2. ショートコード変換 → 成功
3. 再バリデーション → 失敗（番号付きリスト残存）
4. Claude API自動修正 → 環境変数エラーで失敗
5. exit 1で全体終了 → 後続ジョブもスキップ

**設計課題**:
- 中間失敗が全体を止める設計
- ベストエフォート処理ができない構造
- エラーハンドリングの柔軟性不足

## 3. 修正要件

### 3.1 問題1の修正要件: Markdown番号付きリスト自動変換

#### 新機能要件
- **機能名**: `convert_markdown_lists_to_html.py`
- **目的**: HTMLファイル内のMarkdown番号付きリストを`<ol><li>`タグに変換

#### 変換仕様
```
【変換前】
1. テキスト1
2. テキスト2  
3. テキスト3

【変換後】
<ol>
<li>テキスト1</li>
<li>テキスト2</li>
<li>テキスト3</li>
</ol>
```

#### 技術要件
- **依存関係**: beautifulsoup4（既存環境に合わせる）
- **検出条件**: 
  - 行頭に「数字. 半角スペース」を持つ行が2行以上連続
  - 正規表現: `^\s*\d+\.\s+(.+)$`
- **除外条件**:
  - `<pre>`, `<code>`タグ内は対象外（誤変換防止）
  - 既存の`<ol>`, `<ul>`, `<li>`タグ配下は対象外
- **対象要素**: `div`, `section`, `article`, `p`等のブロック要素内のテキスト

### 3.2 問題2の修正要件: 環境変数エラー根本解決

#### 環境変数設定要件
```yaml
- name: Check ANTHROPIC_API_KEY presence
  id: keycheck
  run: |
    if [ -n "${{ secrets.ANTHROPIC_API_KEY }}" ]; then
      echo "has_key=true" >> $GITHUB_OUTPUT
    else
      echo "has_key=false" >> $GITHUB_OUTPUT
    fi

- name: Auto-fix (best-effort)
  if: |
    steps.validate1.outcome == 'failure' && 
    steps.keycheck.outputs.has_key == 'true' && 
    (github.event_name != 'pull_request' || 
     github.event.pull_request.head.repo.fork == false)
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### 3.3 問題3の修正要件: 堅牢なワークフロー設計

#### エラーハンドリング要件
```yaml
- name: Validate HTML (1st)
  id: validate1
  continue-on-error: true
  
- name: Convert shortcodes
  continue-on-error: true
  
- name: Convert markdown lists
  continue-on-error: true
  
- name: Auto-fix (best-effort)
  if: steps.validate1.outcome == 'failure'
  continue-on-error: true
  
- name: Final validation gate
  run: |
    # 最後に一度だけ厳密判定
    python3 github-actions/scripts/validate_html_output.py "${HTML_FILE}"
```

## 4. 実装優先度

### 優先度1（緊急・必須）
1. **番号付きリスト変換機能**: 主要エラー原因の解消
2. **ワークフローの continue-on-error 設定**: 処理継続の確保

### 優先度2（重要・安定性）  
3. **環境変数エラー解決**: Auto-fix機能の安定化
4. **Secrets存在チェック機能**: フォークPR対応

### 優先度3（改善・堅牢性）
5. **段階的バリデーション**: より詳細な品質管理
6. **アーティファクト保存**: デバッグ情報の蓄積

## 5. 成功基準

### 技術的成功基準
- ✅ 番号付きリスト（`1. 〜`形式）が100%HTML変換される
- ✅ 環境変数エラーによるワークフロー失敗が0%になる  
- ✅ 中間処理失敗でも最終成果物が生成される
- ✅ HTMLバリデーション成功率が95%以上

### ビジネス的成功基準
- ✅ 記事生成ワークフローの成功率が98%以上
- ✅ HTML品質検証が確実に機能する
- ✅ エラー発生時も適切なフォールバック処理が動作

## 6. 承認事項

この要件定義書に基づいて実装を進めることを承認します。

- 作成者: Claude (ルーナ)
- 協力: GPT-5 (ぽるか)  
- 作成日: 2025-01-28
- バージョン: 1.0