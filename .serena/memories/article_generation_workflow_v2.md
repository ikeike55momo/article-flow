# Article Flow - 記事生成ワークフロー v2

## 概要
健康・美容系記事を高品質に生成するための6段階プロンプトワークフロー。
**v2では`sample/articles`のスタイルガイドに準拠したHTML出力形式を採用。**

## v1→v2の主な変更点
1. **インラインスタイル削除** - 外部CSS前提
2. **ブログカード機能追加** - `[blog_card url="..."]`ショートコード
3. **関連記事セクション** - 記事末尾に関連コンテンツ表示
4. **画像要素の改善** - `<figure>`/`<figcaption>`構造
5. **ステップリスト専用クラス** - `article-steps-list`

## ワークフロー構成（v2）
1. **Phase 1: リクエスト分析** - キーワード分析とリサーチクエリ生成
2. **Phase 2: 記事構成生成** - 構造とコンテンツ計画作成
3. **Phase 3: HTML記事生成【改訂】** - 新スタイル準拠の記事作成
4. **Phase 4: ファクトチェック** - 品質検証と修正
5. **Phase 5: SEOメタデータ** - 検索最適化情報生成
6. **Phase 6: 最終まとめ** - 全成果物の整理とパッケージング

## ファイル構成
```
Prompt_v2/
├── CHAT_01_phase1_analysis.md      # Phase 1（変更なし）
├── CHAT_02_structure_generation.md # Phase 2（変更なし）
├── CHAT_03_content_generation.md   # Phase 3【大幅改訂】
├── CHAT_04_factcheck.md            # Phase 4（変更なし）
├── CHAT_05_seo_metadata.md         # Phase 5（変更なし）
├── CHAT_06_finalize.md             # Phase 6（変更なし）
├── README_CHAT_VERSION.md          # 使用ガイド（更新）
├── article-style.md                 # スタイルガイド（参照用）
└── article-template.html            # テンプレート（参照用）
```

## v2の新要素
- **ブログカード**: 関連記事を視覚的に表示
- **実際の画像要素**: プレースホルダーではなくimg要素
- **セマンティックHTML**: より適切な要素使用
- **クラス名の統一**: sample/articlesスタイル準拠

## 成果物（v1と同じ）
1. research_results.json
2. factcheck_report.json
3. seo_metadata.json
4. final_article.html（新スタイル）
5. deliverables_summary.md

## 実行時間
合計約2-3時間（リサーチ時間含む）