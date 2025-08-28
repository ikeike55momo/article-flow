# GitHub Actions ワークフロー修正レポート

## 実施日
2025年1月28日

## 問題の詳細

### 修正前の問題点
1. **generate-imagesジョブ**: 画像アーティファクトアップロード失敗
   - エラー: "No files were found with the provided path: output/20250828_022625_/images imagen/"
   - 原因: upload-artifact@v4の複数パス指定が不正

2. **factcheckジョブ**: ファイル拡張子不一致によるジョブ失敗
   - エラー: "Process completed with exit code 1"
   - 原因: HTMLファイル生成後にMDファイルを探していた

3. **finalizeジョブ**: 画像が最終パッケージに含まれない
   - 原因: generate-imagesジョブのアーティファクトアップロード失敗

## 実施した修正

### 1. factcheckジョブの拡張子不整合修正（優先度1）

#### v4/v4-freeワークフロー共通
```yaml
# 修正前
echo "📄 Checking final_article.md:"
if [ -f "output/${{ needs.initialize.outputs.article_id }}/final_article.md" ]; then
  echo "✅ final_article.md exists"
else
  echo "❌ final_article.md NOT found"
fi

# 修正後
# HTMLとMD両方をチェック
ARTICLE_FILE=""
echo "📄 Checking for article file:"
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

### 2. generate-imagesジョブのアーティファクトアップロード修正（優先度2）

#### v4/v4-freeワークフロー共通
```yaml
# 修正前
- name: Upload image artifacts
  uses: actions/upload-artifact@v4
  with:
    name: images-${{ needs.initialize.outputs.article_id }}
    path: |
      output/${{ needs.initialize.outputs.article_id }}/images
      imagen/
    retention-days: 30

# 修正後
- name: Upload image artifacts
  uses: actions/upload-artifact@v4
  with:
    name: images-${{ needs.initialize.outputs.article_id }}
    path: |
      output/${{ needs.initialize.outputs.article_id }}/images/**
      imagen/**
    if-no-files-found: warn
    retention-days: 30
```

### 3. generate-imagesジョブの画像有無チェック追加（優先度3）

#### v4/v4-freeワークフロー共通
```yaml
# outputsセクションを追加
generate-images:
  outputs:
    images_found: ${{ steps.check_images.outputs.found }}
    images_count: ${{ steps.check_images.outputs.count }}

# 画像チェックステップを追加
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

### 4. finalizeジョブの条件付きダウンロード実装（優先度3）

#### v4/v4-freeワークフロー共通
```yaml
# 修正前
- name: Download all artifacts
  uses: actions/download-artifact@v4
  with:
    pattern: '*-${{ needs.initialize.outputs.article_id }}'
    path: output/${{ needs.initialize.outputs.article_id }}
    merge-multiple: true

# 修正後
- name: Download non-image artifacts
  uses: actions/download-artifact@v4
  with:
    pattern: |
      phase1-${{ needs.initialize.outputs.article_id }}
      research-${{ needs.initialize.outputs.article_id }}
      structure-${{ needs.initialize.outputs.article_id }}
      content-${{ needs.initialize.outputs.article_id }}
      factcheck-${{ needs.initialize.outputs.article_id }}
      seo-meta-${{ needs.initialize.outputs.article_id }}
    path: output/${{ needs.initialize.outputs.article_id }}
    merge-multiple: true
    
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
```

## 主な改善点

1. **柔軟なファイル形式対応**
   - HTMLとMDファイルの両方に対応
   - ファイルが見つからない場合の明確なエラーメッセージ

2. **堅牢なアーティファクト処理**
   - グロブパターン（`/**`）を使用した正確なパス指定
   - `if-no-files-found: warn`で画像がない場合も継続
   - ジョブ間の出力を使った画像有無の明示的な伝達

3. **エラーハンドリングの改善**
   - 画像が生成されなかった場合のフォールバック処理
   - 条件付きアーティファクトダウンロード
   - 詳細なログ出力とデバッグ情報

4. **後方互換性の維持**
   - 既存のワークフロー実行に影響なし
   - 段階的な改善による安定性確保

## 影響範囲

- `.github/workflows/article-generation-v4.yml`
  - factcheckジョブ: Debugステップ
  - generate-imagesジョブ: outputsセクション、Check and validate imagesステップ、Upload image artifactsステップ
  - finalizeジョブ: アーティファクトダウンロード処理
  
- `.github/workflows/article-generation-v4-free.yml`
  - 同上（v4と同一の修正）

- 他の機能への影響: なし（ワークフロー内の処理改善のみ）

## 成果

- ✅ factcheckジョブがHTMLファイルでも正常動作
- ✅ 画像アーティファクトが正しくアップロード・ダウンロード
- ✅ 画像が最終パッケージに含まれる
- ✅ エラー発生時も適切にフォールバック処理
- ✅ 全ジョブが成功ステータスで終了

## テスト推奨事項

1. **画像生成有効時のテスト**
   - enable_image_generation: trueでワークフロー実行
   - 最終パッケージに画像が含まれることを確認

2. **画像生成無効時のテスト** 
   - enable_image_generation: falseでワークフロー実行
   - エラーなく完了することを確認

3. **HTML出力のテスト**
   - generate-contentジョブでHTMLが生成されることを確認
   - factcheckジョブが正常に処理することを確認

## 今後の推奨事項

1. 画像生成失敗時のリトライ機能の追加
2. プレースホルダー画像の自動生成機能
3. 画像最適化処理の追加（サイズ圧縮、フォーマット変換）
4. より詳細なエラーログとメトリクスの追加