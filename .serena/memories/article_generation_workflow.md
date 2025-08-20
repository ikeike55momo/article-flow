# Article Flow - 記事生成ワークフロー

## 概要
健康・美容系記事を高品質に生成するための6段階プロンプトワークフロー。
元々GitHub Actionsで自動化されていたものを、チャット形式で手動実行できるように最適化。

## ワークフロー構成
1. **Phase 1: リクエスト分析** - キーワード分析とリサーチクエリ生成
2. **Phase 2: 記事構成生成** - 構造とコンテンツ計画作成
3. **Phase 3: HTML記事生成** - 完全な記事本文作成（出典付き）
4. **Phase 4: ファクトチェック** - 品質検証と修正
5. **Phase 5: SEOメタデータ** - 検索最適化情報生成  
6. **Phase 6: 最終まとめ** - 全成果物の整理とパッケージング

## 主要特徴
- **ペルソナ最適化**: ターゲット読者に合わせた内容・表現調整
- **法規制対応**: 薬機法・景表法への配慮（日本の健康・美容分野規制）
- **信頼性重視**: 必ず5つ以上の出典URLを含める
- **SEO最適化**: キーワード密度2-4%、メタデータ完備
- **品質保証**: ファクトチェックで70点以上のスコアを確保

## 成果物
1. research_results.json - リサーチ結果
2. factcheck_report.json - 品質レポート
3. seo_metadata.json - SEOメタ情報
4. final_article.html - 最終記事
5. deliverables_summary.md - 成果物説明書

## 実行時間
- 合計約2-3時間（リサーチ時間含む）
- 各フェーズ10-30分程度

## プロンプトファイル
- Prompt/README_CHAT_VERSION.md - 使用ガイド
- Prompt/CHAT_01_phase1_analysis.md - Phase 1プロンプト
- Prompt/CHAT_02_structure_generation.md - Phase 2プロンプト
- Prompt/CHAT_03_content_generation.md - Phase 3プロンプト
- Prompt/CHAT_04_factcheck.md - Phase 4プロンプト
- Prompt/CHAT_05_seo_metadata.md - Phase 5プロンプト
- Prompt/CHAT_06_finalize.md - Phase 6プロンプト