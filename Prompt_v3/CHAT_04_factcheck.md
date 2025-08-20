# チャット用 Phase 4: ファクトチェック・品質スコア算出プロンプト

## 使用方法
Phase 3で生成されたHTML記事とリサーチ結果をもとに、ファクトチェックと品質評価を行ってください。

---

# 記事ファクトチェック・品質スコア算出

記事のファクトチェックを行い、品質スコアを算出してください。

## 入力情報

### Phase 3で生成された記事
【ここにPhase 3で生成されたHTML記事全文を貼り付け】

### リサーチ結果（検証用）
【リサーチで収集した情報を以下の形式で記載】
- **情報1**: 〇〇についての統計データ（出典: https://example1.com）
- **情報2**: 専門家の見解（出典: https://example2.com）
- **情報3**: 研究結果（出典: https://example3.com）
（リサーチした全ての情報）

## チェック観点

### 1. 事実の正確性
- 記載されている数値・統計データの正確性
- リサーチ結果との整合性
- 出典の信頼性

### 2. 薬機法・景表法の遵守
- 効果・効能の過度な表現がないか
- 「必ず」「絶対」などの断定的表現の確認
- 医学的根拠のない主張がないか

### 3. 科学的・医学的妥当性
- 専門的主張の根拠の有無
- 最新の研究結果との整合性
- 誤解を招く表現がないか

### 4. ペルソナへの配慮
- ペルソナが誤解しやすい表現はないか
- より分かりやすい説明が必要な箇所はないか

### 5. ARTICLE-TEMPLATE-README.md仕様準拠（v3追加）
- CSSクラス名が仕様通りか
- strongタグの使用が適切か（文章内の重要ポイントのみ）
- ハイライトボックスが1セクション1個以内か
- FAQの構造が正しいか（checkbox + label + span）
- 出典リンクの形式が正しいか（fn-1, fnref-1等）

## タスク

1. **記事の内容をチェック**
   - 上記4つの観点で詳細に確認
   - 問題箇所があれば具体的に指摘

2. **修正が必要な場合**
   - 問題箇所を修正したHTML記事を再出力
   - 修正理由を明記

3. **品質レポートを作成**
   - 以下のJSON形式で詳細なレポートを出力

## 出力形式

### 1. 修正版HTML記事（修正が必要な場合のみ）
```html
<!-- 修正されたHTML記事全文 -->
```

### 2. 品質レポート（JSON形式・必須）
```json
{
  "overall_quality_score": 85,
  "fact_accuracy_score": 90,
  "legal_compliance_score": 95,
  "scientific_validity_score": 80,
  "source_reliability_score": 85,
  "issues_found": [
    {
      "type": "fact_error|legal_compliance|scientific_validity|clarity",
      "description": "具体的な問題の説明",
      "location": "記事内の該当箇所（見出しやキーワード）",
      "severity": "high|medium|low",
      "corrected": true,
      "correction_detail": "どのように修正したかの説明"
    },
    {
      "type": "legal_compliance",
      "description": "「必ず効果があります」という断定的表現",
      "location": "メインセクション2の効果説明部分",
      "severity": "high",
      "corrected": true,
      "correction_detail": "「効果が期待できます」に修正"
    }
  ],
  "recommendations": [
    "より具体的な統計データの追加を推奨",
    "専門用語の説明をもう少し詳しく"
  ],
  "strengths": [
    "信頼できる出典を5つ以上引用",
    "ペルソナに合わせた分かりやすい表現"
  ],
  "timestamp": "2024-XX-XX XX:XX:XX",
  "total_issues": 3,
  "corrected_issues": 2,
  "factcheck_summary": "記事全体の品質についての総合コメント"
}
```

### スコア基準
- **overall_quality_score** (0-100): 総合品質スコア
- **fact_accuracy_score** (0-100): 事実の正確性
- **legal_compliance_score** (0-100): 薬機法・景表法遵守度
- **scientific_validity_score** (0-100): 科学的・医学的妥当性
- **source_reliability_score** (0-100): 情報源の信頼性

### 修正タイプ
- **fact_error**: 事実の誤り
- **legal_compliance**: 法規制関連
- **scientific_validity**: 科学的妥当性
- **clarity**: 分かりやすさの改善

### 重要度
- **high**: 信頼性に大きく影響、必須修正
- **medium**: 改善推奨
- **low**: 軽微、任意修正

## 注意点

1. **客観的な評価**: 感情的な判断ではなく、事実に基づいて評価
2. **建設的なフィードバック**: 問題点だけでなく改善案も提示
3. **ペルソナ視点**: 読者（ペルソナ）の理解しやすさを重視
4. **法規制の理解**: 健康・美容分野の表現規制を正しく適用

---

## 次のステップ
この品質レポートをもとに、Phase 5（SEOメタ情報生成）に進んでください。修正版記事がある場合は、修正版を使用してください。