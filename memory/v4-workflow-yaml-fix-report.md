# V4 Workflow YAML修正レポート

## 問題の概要
GitHub ActionsがV4ワークフロー（article-generation-v4.yml）を認識しない問題が発生。ユーザーから「またワークフローとして認識されてないよ。何回同じミスするの」という指摘を受けた。

## 根本原因
1. **Heredoc構文の問題**: YAML内でheredoc（`cat > file << EOF`）を使用していた箇所が複数存在
2. **GitHub Actions変数との競合**: heredoc内で`${{ inputs.variable }}`などのGitHub Actions変数を使用するとYAMLパーサーが構文エラーを起こす
3. **Windows改行コード（CRLF）**: 一部ファイルでWindows形式の改行が混入

## 修正内容

### 1. Heredocの除去
以下の5箇所でheredocを`echo`コマンドに置き換え：

#### a) input_params.json生成（Line 62-70）
```yaml
# 修正前
cat > output/${ARTICLE_ID}/input_params.json << EOJSON
{
  "article_id": "${ARTICLE_ID}",
  "title": "${{ inputs.article_title }}"
}
EOJSON

# 修正後
echo '{' > "output/${ARTICLE_ID}/input_params.json"
echo "  \"article_id\": \"${ARTICLE_ID}\"," >> "output/${ARTICLE_ID}/input_params.json"
echo "  \"title\": \"${{ inputs.article_title }}\"" >> "output/${ARTICLE_ID}/input_params.json"
echo '}' >> "output/${ARTICLE_ID}/input_params.json"
```

#### b) request_params.json生成（Line 110-116）
```yaml
# 修正前
cat > request_params.json << EOJSON
{
  "topic": "${{ inputs.article_title }}",
  "target_audience": "${{ inputs.target_persona }}"
}
EOJSON

# 修正後
echo '{' > request_params.json
echo "  \"topic\": \"${{ inputs.article_title }}\"," >> request_params.json
echo "  \"target_audience\": \"${{ inputs.target_persona }}\"" >> request_params.json
echo '}' >> request_params.json
```

#### c) 記事フォールバック生成（Line 948-952）
```yaml
# 修正前
cat > "$FINAL_DIR/article.md" << 'EOF'
# 記事生成エラー
記事ファイルが見つかりませんでした。
EOF

# 修正後
echo "# 記事生成エラー" > "$FINAL_DIR/article.md"
echo "記事ファイルが見つかりませんでした。" >> "$FINAL_DIR/article.md"
```

#### d) README生成（Line 1058+）
大量のREADME内容を個別の`echo`コマンドに分割

#### e) Pythonスクリプト（Line 276-362）
インラインPythonコードを外部スクリプト`research_batch_gemini.py`に移動

### 2. 改行コードの修正
`dos2unix`コマンドでWindows改行（CRLF）をUnix改行（LF）に変換

### 3. 外部スクリプトの作成
`github-actions/scripts/research_batch_gemini.py`を新規作成し、Gemini API呼び出しロジックを外部化

## 教訓とベストプラクティス

### 1. GitHub Actions YAMLでのheredoc使用を避ける
- heredoc内でGitHub Actions変数（`${{ }}`）を使用するとパーサーエラーが発生
- 小さなテキストは`echo`コマンドで生成
- 大きなスクリプトは外部ファイル化

### 2. YAMLファイルの検証
- コミット前に`python3 -m yaml`でローカル検証
- ただしPyYAMLの`on:`キーワード問題に注意（GitHubでは正常動作）

### 3. 改行コードの統一
- Gitの`core.autocrlf`設定を適切に管理
- WSL環境では特に注意が必要

## 結果
- 2025年7月28日: すべての修正を適用
- GitHub ActionsがV4ワークフローを正しく認識
- コミット: `67f5d29` - "Remove all heredocs from V4 workflow to fix YAML syntax errors"

## 今後の注意点
1. 新しいワークフロー作成時はheredocを使用しない
2. 複雑なスクリプトは外部ファイル化を検討
3. YAMLファイルは定期的に構文チェックを実施