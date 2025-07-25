# フェーズ3.5: ファクトチェック

## 入力情報
- draft_content: {{03_draft.md}}
- research_data: {{01_research.json}}
- factcheck_rules: {{config/factcheck_rules.yaml}}

## ファクトチェックタスク

### 1. 事実確認が必要な要素の抽出

執筆した記事から以下を抽出：

1. **数値・統計データ**
   - すべての数字（％、人数、金額等）
   - 統計的な主張
   - ランキングや順位

2. **専門的主張**
   - 医学的・科学的な説明
   - 効果・効能に関する記述
   - 因果関係の説明

3. **比較・評価**
   - 他の方法との比較
   - 優位性の主張
   - 「最も」「一番」などの表現

4. **時事的情報**
   - 「最新の」「2024年の」等の記述
   - 現在の状況説明
   - トレンドや動向

### 2. 各要素の検証（追加web_search実行）

抽出した各要素について：

1. **情報源の確認**
   ```
   検証項目: [具体的な主張]
   元の情報源: [research_dataから特定]
   信頼性レベル: [very_high/high/medium_high/medium/low]
   ```

2. **追加検証** （必要に応じて5-10回のweb_search）
   - 複数の情報源で確認
   - より信頼できる情報源を探す
   - 最新情報への更新確認

3. **矛盾チェック**
   - 異なる情報源間の矛盾
   - 一般常識との乖離
   - 論理的整合性

### 3. 問題箇所の特定と分類

1. **レッドフラグ（修正必須）**
   - 検証不可能な数値
   - 出典不明な統計
   - 誤った情報
   - 古すぎる情報（3年以上前）
   - 誇大表現

2. **イエローフラグ（要注意）**
   - 単一ソースのみの情報
   - 曖昧な表現
   - 一般論すぎる内容
   - 条件付きで正しい情報

3. **グリーンフラグ（問題なし）**
   - 複数の信頼できるソースで確認
   - 公的機関の情報
   - 最新かつ正確
   - 適切な表現

### 4. 修正提案の作成

各問題箇所について：

```json
{
  "issue_id": "FC001",
  "severity": "red|yellow",
  "location": "セクション名・段落",
  "original_text": "問題のある文章",
  "issue_description": "何が問題か",
  "suggested_fix": "修正案",
  "alternative_approach": "代替アプローチ",
  "supporting_sources": ["裏付けとなる情報源"]
}
```

### 5. 信頼性スコアの算出

```json
{
  "overall_factual_accuracy": 0-100,
  "breakdown": {
    "statistics_accuracy": 0-100,
    "claims_verification": 0-100,
    "source_reliability": 0-100,
    "expression_appropriateness": 0-100
  },
  "pass_fail": "PASS|FAIL",
  "confidence_level": "high|medium|low"
}
```

## 修正の実施

1. **レッドフラグ項目**
   - 即座に修正または削除
   - 代替情報で置き換え
   - どうしても必要な場合は条件付き表現に

2. **イエローフラグ項目**
   - より適切な表現に修正
   - 追加の裏付け情報を付加
   - 断定を避けた表現に変更

## 出力形式

1. **ファクトチェックレポート**
   - 検証項目数
   - 問題発見数
   - 修正実施数
   - 最終スコア

2. **修正済みドラフト**
   - すべての修正を反映
   - 信頼性が確保された内容
   - 店舗公式として適切な表現

## ファイル保存

1. ファクトチェック済み原稿：
   ```
   output/{date}-{title_slug}/03_5_factchecked_draft.md
   ```

2. ファクトチェックレポート：
   ```
   output/{date}-{title_slug}/03_5_factcheck_report.json
   ```

レポート形式：
```json
{
  "total_checks": 数値,
  "issues_found": 数値,
  "fixes_applied": 数値,
  "factual_accuracy_score": 0-100,
  "issues": [
    {
      "type": "red|yellow",
      "location": "場所",
      "original": "元の文",
      "fixed": "修正後",
      "source": "裏付け情報源"
    }
  ]
}
```

## 重要な注意事項

店舗の信頼性を守るため：
- 「たぶん」「おそらく」は使わない
- 検証できない情報は削除
- 医療・健康情報は特に慎重に
- 法的リスクのある表現は回避