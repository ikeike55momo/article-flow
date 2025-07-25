# 📁 GitHub Actions ファイル構造ガイド

## ファイル命名規則

このワークフローでは、各フェーズで以下のファイル名が使用されます：

### Phase 1: リクエスト解析
- **入力**: ユーザー入力パラメータ
- **出力**: `output/{article_id}/phase1_analysis.json`

### Phase 2: リサーチ
- **入力**: `phase1_analysis.json`
- **出力**: `output/{article_id}/phase2_research.json`

### Phase 3: 構成計画
- **入力**: 
  - `phase1_analysis.json`
  - `phase2_research.json`
- **出力**: `output/{article_id}/02_article_structure.md`
- **注意**: Claude Code Base Actionのプロンプトに従い、マークダウン形式で保存

### Phase 4: 執筆
- **入力**:
  - `02_article_structure.md`
  - `01_research_data.md`（phase2_research.jsonから生成）
  - `00_parsed_request.json`（phase1_analysis.jsonから生成）
- **出力**: `output/{article_id}/03_draft.md`

### Phase 5: ファクトチェック
- **入力**: `03_draft.md`
- **出力**: 
  - `output/{article_id}/03_5_factchecked_draft.md`
  - `output/{article_id}/03_5_factcheck_report.json`

### Phase 6: SEO最適化
- **入力**: `03_5_factchecked_draft.md`
- **出力**: `output/{article_id}/04_optimized_draft.html`

### Phase 7: 最終調整
- **入力**: すべての中間ファイル
- **出力**: 
  - `output/{article_id}/final.html`
  - `output/{article_id}/05_quality_report.json`

### 画像生成（並列実行）
- **入力**:
  - `02_article_structure.md`（セクション情報を抽出）
  - `04_optimized_draft.html`（記事内容）
- **出力**: `output/{article_id}/images/`

## ディレクトリ構造の例

```
output/20250125_123456_example_topic/
├── phase1_analysis.json          # Phase 1の出力（内部用）
├── phase2_research.json          # Phase 2の出力（内部用）
├── 00_parsed_request.json        # Phase 1の出力（Claude用）
├── 01_research_data.md          # Phase 2の出力（Claude用）
├── 02_article_structure.md      # Phase 3の出力
├── 03_draft.md                  # Phase 4の出力
├── 03_5_factchecked_draft.md   # Phase 5の出力
├── 03_5_factcheck_report.json  # Phase 5のレポート
├── 04_optimized_draft.html     # Phase 6の出力
├── 05_quality_report.json      # Phase 7のレポート
├── final.html                   # 最終成果物
└── images/                      # 生成画像
    ├── hero-image.webp
    ├── section-1.webp
    ├── section-2.webp
    └── ...
```

## 重要な注意事項

1. **ファイル名の不整合に注意**
   - 一部のフェーズでは `phase{N}_*.json` 形式
   - Claude Code Base Actionでは `0{N}_*.{md,json,html}` 形式
   - これは歴史的経緯によるもので、両方が混在しています

2. **画像生成の特殊性**
   - 構造ファイルはJSON形式ではなくマークダウン形式
   - 画像生成スクリプトはマークダウンからH2セクションを抽出

3. **並列実行のタイミング**
   - 画像生成はPhase 4（執筆）完了後に開始
   - Phase 5（ファクトチェック）と並列実行される

## 今後の改善案

1. **ファイル名の統一**
   - すべてのフェーズで一貫した命名規則を使用
   - 例：`{phase_number}_{phase_name}.{format}`

2. **構造データのJSON化**
   - 構造情報をJSONとしても保存
   - 他のツールとの互換性向上

3. **メタデータファイル**
   - 各フェーズの実行状況を記録
   - エラー時の再開を容易に