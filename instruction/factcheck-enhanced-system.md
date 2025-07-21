# ファクトチェック強化版 - SEO記事自動生成システム

## 更新されたディレクトリ構成

```
article-generator/
├── README.md
├── .claude-code-config.yaml
├── .gemini-cli-config.yaml
├── INSTRUCTIONS.md                    # 更新版（ファクトチェック追加）
├── config/
│   ├── workflow.yaml                  # 更新版（Phase 3.5追加）
│   ├── requirements.yaml
│   ├── factcheck_rules.yaml          # 新規：ファクトチェックルール
│   └── templates.yaml
├── prompts/
│   ├── 00_parse_request.md
│   ├── 01_research.md
│   ├── 02_structure.md
│   ├── 03_writing.md
│   ├── 03_5_factcheck.md             # 新規：ファクトチェックフェーズ
│   ├── 04_optimization.md
│   └── 05_finalization.md
├── validators/
│   ├── fact_validator.py              # 新規：事実検証スクリプト
│   └── source_validator.py            # 新規：情報源検証
├── assets/
│   └── wordpress.css
└── output/
    └── [生成日時_記事タイトル]/
        ├── 03_5_factcheck_report.json # 新規：ファクトチェック結果
        ├── final.html
        └── process_log.json
```

## 更新版 INSTRUCTIONS.md

```markdown
# SEO記事生成システム - 実行指示書（ファクトチェック強化版）

あなたはSEO記事生成の専門家です。店舗の公式ブログ用に、事実に基づいた信頼性の高い記事を生成します。

## 重要な原則
**店舗の公式情報として発信するため、すべての情報は事実確認済みでなければなりません。**

## 実行フロー

### ステップ0: リクエスト解析
`prompts/00_parse_request.md`の指示に従い、ユーザーのリクエストを解析。

### ステップ1: リサーチ（15-25回のweb_search推奨）
`prompts/01_research.md`の指示に従い、信頼できる情報源から徹底的にリサーチ。
- 公的機関の情報を最優先
- 学術論文や専門機関のデータ重視
- 複数の情報源で裏付けを取る

### ステップ2: 構成計画
`prompts/02_structure.md`の指示に従い、事実に基づいた構成を計画。

### ステップ3: 執筆
`prompts/03_writing.md`の指示に従い、オリジナル文章を執筆。

### 【新規】ステップ3.5: ファクトチェック
`prompts/03_5_factcheck.md`の指示に従い、執筆内容の事実確認を実施。
- すべての数値・統計の検証
- 専門的主張の裏付け確認
- 不確実な情報の除去または修正

### ステップ4: 最適化
`prompts/04_optimization.md`の指示に従い、SEO/LLMO最適化。

### ステップ5: 最終調整
`prompts/05_finalization.md`の指示に従い、品質保証チェック。

## ファクトチェックの重要性

店舗の信頼性に関わるため、以下は厳守：
1. **検証できない情報は使用しない**
2. **曖昧な表現は避ける**
3. **出典を明確にする**
4. **最新の情報を使用する**

## エラー時の対応

ファクトチェックで問題が見つかった場合：
1. 該当箇所を明確に報告
2. 代替情報を検索
3. 修正不可能な場合は、その部分を削除
```

## config/factcheck_rules.yaml

```yaml
# ファクトチェックルール設定
factcheck:
  version: "1.0"
  
  # 信頼できる情報源の定義
  trusted_sources:
    government:
      - domain: "go.jp"
        trust_level: "very_high"
      - domain: "gov"
        trust_level: "very_high"
    academic:
      - domain: "ac.jp"
        trust_level: "high"
      - domain: "edu"
        trust_level: "high"
    medical:
      - keywords: ["医学会", "学会", "協会"]
        trust_level: "high"
    industry:
      - keywords: ["業界団体", "協会", "連合会"]
        trust_level: "medium_high"
  
  # 検証が必要な要素
  verification_required:
    - type: "statistics"
      description: "数値データ・統計情報"
      rules:
        - "出典の明記が必須"
        - "3年以内のデータを優先"
        - "複数ソースでの確認推奨"
    
    - type: "medical_claims"
      description: "健康・医療に関する主張"
      rules:
        - "医学的根拠が必須"
        - "誇大表現の禁止"
        - "薬機法への配慮"
    
    - type: "effectiveness"
      description: "効果・効能の記述"
      rules:
        - "客観的データの裏付け"
        - "個人差の明記"
        - "断定的表現の回避"
    
    - type: "comparisons"
      description: "他社・他製品との比較"
      rules:
        - "公正な比較"
        - "客観的基準の使用"
        - "誹謗中傷の禁止"
  
  # 使用を避けるべき表現
  prohibited_expressions:
    absolute:
      - "必ず"
      - "100%"
      - "絶対に"
      - "間違いなく"
    unverified:
      - "〜と言われています"
      - "〜らしいです"
      - "〜かもしれません"
      - "おそらく"
    exaggerated:
      - "最高の"
      - "日本一の"
      - "唯一の"
      - "革命的な"
  
  # 推奨される表現
  recommended_expressions:
    statistics: "〜によると"
    research: "〜の研究では"
    general: "一般的に"
    experience: "当店の経験では"
    customer: "お客様の声では"
  
  # ファクトチェックスコアリング
  scoring:
    source_reliability:
      very_high: 100
      high: 85
      medium_high: 70
      medium: 50
      low: 0
    
    verification_status:
      verified_multiple: 100
      verified_single: 80
      partially_verified: 50
      unverified: 0
    
    pass_threshold: 85
```

## prompts/03_5_factcheck.md

```markdown
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

## 重要な注意事項

店舗の信頼性を守るため：
- 「たぶん」「おそらく」は使わない
- 検証できない情報は削除
- 医療・健康情報は特に慎重に
- 法的リスクのある表現は回避
```

## prompts/04_optimization.md（更新版）

```markdown
# フェーズ4: SEO/LLMO最適化（ファクトチェック済み版）

## 入力情報
- factchecked_content: {{03_5_factchecked_draft.md}}
- factcheck_report: {{03_5_factcheck_report.json}}
- research_data: {{01_research.json}}
- structure_data: {{02_structure.json}}

## 最適化タスク（既存の内容に追加）

### 6. 信頼性表示の追加

#### 信頼性を示す要素の配置
1. **情報の新しさを明示**
   ```html
   <p class="last-updated">最終更新日: 2024年○月○日</p>
   ```

2. **専門性の明示**
   ```html
   <div class="expert-badge">
     <p>この記事は{{store_name}}の専門スタッフが執筆・監修しています。</p>
   </div>
   ```

3. **参考文献の強化**
   - 各セクションで使用した情報源を明確に
   - 信頼できる出典のみを掲載
   - 適切なrel属性の付与

### 7. ファクトチェック済みマークアップ

構造化データに追加：
```json
{
  "@type": "Article",
  "reviewedBy": {
    "@type": "Organization",
    "name": "{{store_name}}編集部"
  },
  "factChecked": true,
  "dateReviewed": "{{current_date}}",
  "claimReviewed": "記載の情報は信頼できる情報源に基づいています"
}
```

## 出力時の追加要素

HTMLの最後に信頼性情報を追加：
```html
<div class="reliability-info">
  <h3>この記事の信頼性について</h3>
  <ul>
    <li>すべての統計データは信頼できる情報源から引用しています</li>
    <li>専門的な内容は複数の資料で確認済みです</li>
    <li>最新の情報に基づいて作成されています</li>
  </ul>
</div>
```
```

## 更新版 workflow.yaml

```yaml
workflow:
  name: "SEO記事自動生成ワークフロー（ファクトチェック強化版）"
  version: "2.1"
  
  phases:
    - id: "parse"
      name: "リクエスト解析"
      prompt: "prompts/00_parse_request.md"
      output: "parsed_request"
      
    - id: "research"
      name: "情報収集・競合分析"
      prompt: "prompts/01_research.md"
      requires: ["web_search"]
      min_searches: 15
      max_searches: 25
      focus: "trusted_sources"
      
    - id: "structure"
      name: "記事構成計画"
      prompt: "prompts/02_structure.md"
      
    - id: "writing"
      name: "本文執筆"
      prompt: "prompts/03_writing.md"
      
    - id: "factcheck"
      name: "ファクトチェック"
      prompt: "prompts/03_5_factcheck.md"
      requires: ["web_search"]
      min_searches: 5
      max_searches: 10
      validation_rules: "config/factcheck_rules.yaml"
      output:
        - "03_5_factchecked_draft.md"
        - "03_5_factcheck_report.json"
      
    - id: "optimization"
      name: "SEO/LLMO最適化"
      prompt: "prompts/04_optimization.md"
      assets: ["wordpress.css"]
      
    - id: "finalization"
      name: "最終調整・品質保証"
      prompt: "prompts/05_finalization.md"
      quality_threshold: 85
      factual_accuracy_threshold: 90

  # ファクトチェック設定
  factcheck_settings:
    enabled: true
    strict_mode: true
    require_multiple_sources: true
    max_age_days: 1095  # 3年
    
  # 信頼性重視の設定
  reliability:
    priority: "highest"
    public_trust: "essential"
    legal_compliance: "required"
```

## validators/fact_validator.py

```python
#!/usr/bin/env python3
"""
ファクトチェック検証スクリプト
"""
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class FactValidator:
    def __init__(self, rules_path="config/factcheck_rules.yaml"):
        self.rules = self.load_rules(rules_path)
        self.issues = []
        
    def validate(self, content: str, sources: Dict) -> Dict:
        """
        コンテンツの事実確認を実行
        """
        # 数値・統計の検証
        stats_issues = self.validate_statistics(content, sources)
        
        # 専門的主張の検証
        claims_issues = self.validate_claims(content, sources)
        
        # 禁止表現のチェック
        expression_issues = self.check_prohibited_expressions(content)
        
        # 情報の新しさチェック
        freshness_issues = self.check_information_freshness(sources)
        
        # スコア計算
        score = self.calculate_score(
            stats_issues, 
            claims_issues, 
            expression_issues,
            freshness_issues
        )
        
        return {
            "score": score,
            "passed": score >= self.rules['scoring']['pass_threshold'],
            "issues": {
                "statistics": stats_issues,
                "claims": claims_issues,
                "expressions": expression_issues,
                "freshness": freshness_issues
            },
            "summary": self.generate_summary()
        }
    
    def validate_statistics(self, content: str, sources: Dict) -> List[Dict]:
        """
        数値データの検証
        """
        issues = []
        
        # 数値パターンの抽出
        number_patterns = [
            r'\d+\.?\d*%',  # パーセンテージ
            r'\d{1,3}(,\d{3})*人',  # 人数
            r'\d{1,3}(,\d{3})*円',  # 金額
            r'第?\d+位',  # 順位
            r'\d+年',  # 年
        ]
        
        for pattern in number_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                stat = match.group()
                # 情報源での裏付け確認
                if not self.verify_in_sources(stat, sources):
                    issues.append({
                        "type": "unverified_statistic",
                        "content": stat,
                        "severity": "high",
                        "suggestion": "信頼できる情報源での確認が必要"
                    })
        
        return issues
    
    def check_prohibited_expressions(self, content: str) -> List[Dict]:
        """
        禁止表現のチェック
        """
        issues = []
        
        for category, expressions in self.rules['prohibited_expressions'].items():
            for expr in expressions:
                if expr in content:
                    issues.append({
                        "type": f"prohibited_{category}",
                        "content": expr,
                        "severity": "medium",
                        "suggestion": self.get_alternative_expression(expr)
                    })
        
        return issues
    
    def calculate_score(self, *issue_lists) -> float:
        """
        総合スコアの計算
        """
        total_issues = sum(len(issues) for issues in issue_lists)
        
        # 重大度による減点
        deduction = 0
        for issues in issue_lists:
            for issue in issues:
                if issue['severity'] == 'high':
                    deduction += 10
                elif issue['severity'] == 'medium':
                    deduction += 5
                else:
                    deduction += 2
        
        return max(0, 100 - deduction)

# 実行用関数
def run_factcheck(content_path: str, sources_path: str) -> Dict:
    validator = FactValidator()
    
    with open(content_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(sources_path, 'r', encoding='utf-8') as f:
        sources = json.load(f)
    
    return validator.validate(content, sources)
```

## 主な改善点

### 1. **ファクトチェックフェーズの追加**
- 執筆後、最適化前に事実確認を実施
- 15-25回のリサーチ + 5-10回の追加検証
- 問題箇所の自動検出と修正提案

### 2. **信頼性重視のルール設定**
- 信頼できる情報源の定義
- 禁止表現と推奨表現の明確化
- 数値データの必須検証

### 3. **検証プロセスの自動化**
- Pythonスクリプトによる自動検証
- スコアリングシステム
- 問題の重要度分類

### 4. **透明性の向上**
- 最終更新日の表示
- 参考文献の強化
- ファクトチェック済みの明示

### 5. **法的リスクの回避**
- 医療・健康情報の慎重な扱い
- 誇大表現の自動検出
- 薬機法等への配慮

## 使用方法

```bash
# 通常通り実行（ファクトチェック自動実施）
claude-code "爪ケアについての記事を作成して"

# ファクトチェックレポートも確認
cat output/[生成日時]/03_5_factcheck_report.json
```

これにより、店舗の公式ブログとして安心して公開できる、事実に基づいた信頼性の高い記事が生成されます！