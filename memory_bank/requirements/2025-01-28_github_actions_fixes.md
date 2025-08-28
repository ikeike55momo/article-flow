# GitHub Actions ワークフロー修正要件定義書

## 1. 問題概要

### 1.1 発生している問題
1. **generate-imagesジョブ**: 画像アーティファクトアップロード失敗
2. **factcheckジョブ**: ファイル拡張子不一致によるジョブ失敗（exit code 1）
3. **finalizeジョブ**: 画像が最終パッケージに含まれない

### 1.2 影響範囲
- v4およびv4-freeワークフローの両方で発生
- 記事生成は成功するが、画像と品質チェックが機能不全
- 最終成果物の品質低下

## 2. 根本原因分析

### 2.1 問題1: upload-artifact@v4の複数パス指定エラー
**現在の実装（誤り）**:
```yaml
path: |
  output/${{ needs.initialize.outputs.article_id }}/images
  imagen/
```

**エラー詳細**:
- 複数パスが `output/20250828_022625_/images imagen/` という単一の無効なパスとして解釈される
- YAMLのパイプ（`|`）を使っているが、末尾のグロブ指定が不足

### 2.2 問題2: MD/HTML拡張子の不整合
**現在の実装**:
- generate-content: `final_article.html` を生成
- factcheck: `final_article.md` を探す
- 結果: ファイルが見つからずジョブ失敗

### 2.3 問題3: ジョブ間のデータ共有失敗
**現在の実装の問題点**:
- GitHub Actionsのジョブは独立したコンテナで実行される
- アーティファクトが唯一のジョブ間データ共有手段
- アーティファクトアップロード失敗により、後続ジョブがデータにアクセス不可

## 3. 修正要件

### 3.1 問題1の修正要件

#### 方針A: 最小修正（推奨）
```yaml
- name: Upload image artifacts
  uses: actions/upload-artifact@v4
  with:
    name: images-${{ needs.initialize.outputs.article_id }}
    path: |
      output/${{ needs.initialize.outputs.article_id }}/images/**
      imagen/**
    if-no-files-found: warn
```

**要件**:
- パスの末尾に `/**` を追加してグロブパターンを使用
- `if-no-files-found: warn` で画像がない場合も継続
- YAMLの literal block（`|`）を維持

#### 方針B: 堅牢性重視
```yaml
- name: Collect all images to single directory
  run: |
    set -euo pipefail
    ART_ID="${{ needs.initialize.outputs.article_id }}"
    DEST="output/${ART_ID}/all_images"
    mkdir -p "$DEST"
    
    # imagen/フォルダから収集
    if [ -d "imagen" ]; then
      cp -a imagen/* "$DEST/" 2>/dev/null || true
    fi
    
    # output/images/から収集
    if [ -d "output/${ART_ID}/images" ]; then
      cp -a "output/${ART_ID}/images/"* "$DEST/" 2>/dev/null || true
    fi
    
    # 画像数をカウント
    IMAGE_COUNT=$(find "$DEST" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | wc -l)
    echo "Found ${IMAGE_COUNT} images"
    echo "image_count=${IMAGE_COUNT}" >> $GITHUB_OUTPUT

- name: Upload image artifacts
  if: steps.collect_images.outputs.image_count > 0
  uses: actions/upload-artifact@v4
  with:
    name: images-${{ needs.initialize.outputs.article_id }}
    path: output/${{ needs.initialize.outputs.article_id }}/all_images/**
    if-no-files-found: error
```

### 3.2 問題2の修正要件

#### 方針A: factcheckジョブを柔軟に（推奨）
```bash
# factcheckジョブのDebugステップを修正
- name: Debug - Check files before factcheck
  run: |
    echo "📁 Files before factcheck:"
    ls -la output/${{ needs.initialize.outputs.article_id }}/
    
    # HTMLとMD両方をチェック
    ARTICLE_FILE=""
    if [ -f "output/${{ needs.initialize.outputs.article_id }}/final_article.html" ]; then
      echo "✅ final_article.html exists"
      ARTICLE_FILE="output/${{ needs.initialize.outputs.article_id }}/final_article.html"
    elif [ -f "output/${{ needs.initialize.outputs.article_id }}/final_article.md" ]; then
      echo "✅ final_article.md exists"
      ARTICLE_FILE="output/${{ needs.initialize.outputs.article_id }}/final_article.md"
    else
      echo "❌ No final article found (.html or .md)"
      exit 1
    fi
    
    echo "article_file=${ARTICLE_FILE}" >> $GITHUB_OUTPUT
```

#### 方針B: 生成側で両形式を出力
```yaml
# generate-contentジョブで両形式を生成
- name: Ensure both HTML and MD formats exist
  run: |
    ART_ID="${{ needs.initialize.outputs.article_id }}"
    HTML_FILE="output/${ART_ID}/final_article.html"
    MD_FILE="output/${ART_ID}/final_article.md"
    
    # HTMLが存在する場合、MDも生成（簡易変換）
    if [ -f "${HTML_FILE}" ] && [ ! -f "${MD_FILE}" ]; then
      # 簡易的なHTMLタグ除去（本番環境では pandoc 推奨）
      sed 's/<[^>]*>//g' "${HTML_FILE}" > "${MD_FILE}"
      echo "✅ Created MD version from HTML"
    fi
```

### 3.3 問題3の修正要件

#### ジョブ出力による画像有無の明示化
**generate-imagesジョブ**:
```yaml
outputs:
  images_found: ${{ steps.check_images.outputs.found }}
  images_count: ${{ steps.check_images.outputs.count }}

steps:
  # ... 既存の画像生成処理 ...
  
  - name: Check and validate images
    id: check_images
    run: |
      set -euo pipefail
      ART_ID="${{ needs.initialize.outputs.article_id }}"
      
      # 画像をカウント
      shopt -s nullglob
      files=(output/${ART_ID}/images/* imagen/*)
      IMAGE_COUNT=${#files[@]}
      
      if (( IMAGE_COUNT > 0 )); then
        echo "found=true" >> "$GITHUB_OUTPUT"
        echo "count=${IMAGE_COUNT}" >> "$GITHUB_OUTPUT"
        echo "✅ Found ${IMAGE_COUNT} images"
      else
        echo "found=false" >> "$GITHUB_OUTPUT"
        echo "count=0" >> "$GITHUB_OUTPUT"
        echo "⚠️ No images found"
      fi
```

**finalizeジョブ**:
```yaml
- name: Download image artifacts conditionally
  if: needs.generate-images.outputs.images_found == 'true'
  uses: actions/download-artifact@v4
  with:
    name: images-${{ needs.initialize.outputs.article_id }}
    path: output/${{ needs.initialize.outputs.article_id }}/images
    
- name: Handle missing images
  if: needs.generate-images.outputs.images_found != 'true'
  run: |
    echo "⚠️ No images available from generate-images job"
    mkdir -p output/${{ needs.initialize.outputs.article_id }}/images
    # プレースホルダー画像の生成や警告メッセージの追加
```

## 4. 実装優先度

### 優先度1（緊急・必須）
1. **問題2の修正**: factcheckジョブの拡張子不整合を解消
   - ワークフロー全体が失敗する直接原因
   - 方針A（柔軟なチェック）を推奨

### 優先度2（重要）
2. **問題1の修正**: upload-artifactのパス指定修正
   - 画像が最終パッケージに含まれない原因
   - 方針A（最小修正）を推奨

### 優先度3（改善）
3. **問題3の修正**: ジョブ間の画像有無明示化
   - エラーハンドリングの改善
   - フォールバック処理の実装

## 5. テスト要件

### 5.1 単体テスト
- [ ] generate-imagesジョブで画像アーティファクトが正しくアップロードされること
- [ ] factcheckジョブがHTMLファイルでも動作すること
- [ ] finalizeジョブで画像が最終パッケージに含まれること

### 5.2 統合テスト
- [ ] 画像生成が有効な場合の完全なワークフロー実行
- [ ] 画像生成が無効な場合の完全なワークフロー実行
- [ ] 画像生成が失敗した場合のフォールバック動作

### 5.3 検証項目
- [ ] 最終パッケージ（FINAL_V4_ARTICLE_PACKAGE）に画像が含まれる
- [ ] factcheckジョブが正常に完了する
- [ ] 全ジョブが成功ステータスで終了する

## 6. リスクと対策

### 6.1 後方互換性
- **リスク**: 既存のワークフロー実行に影響
- **対策**: 段階的な修正適用、各修正後の動作確認

### 6.2 パフォーマンス
- **リスク**: 画像収集処理の追加による実行時間増加
- **対策**: 並列処理の維持、不要なファイルコピーの削減

### 6.3 エラーハンドリング
- **リスク**: 想定外のファイル構造での失敗
- **対策**: フォールバック処理、詳細なログ出力

## 7. 実装スケジュール

### Phase 1: 緊急修正（即座に実施）
- factcheckジョブの拡張子不整合修正
- upload-artifactのパス指定修正

### Phase 2: 改善実装（1週間以内）
- ジョブ間の画像有無明示化
- フォールバック処理の追加
- エラーメッセージの改善

### Phase 3: 最適化（2週間以内）
- 画像収集処理の最適化
- 詳細なログとメトリクス追加
- ドキュメント更新

## 8. 成功基準

### 技術的成功基準
- ✅ 全ジョブが正常に完了する
- ✅ 画像が最終パッケージに含まれる
- ✅ エラー発生率が5%未満

### ビジネス的成功基準
- ✅ 記事生成の成功率が95%以上
- ✅ 生成された記事に適切な画像が含まれる
- ✅ ワークフロー実行時間が20分以内

## 9. 承認事項

この要件定義書に基づいて実装を進めることを承認します。

- 作成者: Claude (ルーナ)
- レビュー: GPT-5 (ぽるか)
- 作成日: 2025-01-28
- バージョン: 1.0

---

## 付録A: 参考情報

### GitHub Actions upload-artifact@v4 仕様
- 複数パスはYAMLのliteral block（`|`）で改行区切り
- グロブパターン（`**`）のサポート
- `if-no-files-found` オプション: error, warn, ignore

### GitHub Actions ジョブ間データ共有
- アーティファクトが唯一の共有手段
- ジョブは独立したコンテナで実行
- outputs を使った軽量データの受け渡し

### ベストプラクティス
- エラーハンドリングの明示化
- フォールバック処理の実装
- 詳細なログ出力
- 段階的な修正適用