# Gemini CLI 使用ガイド

## 記事生成の指示方法

### 基本的な使い方
```bash
gemini "爪ケアについての記事を作成して"
```

### より確実な実行方法

1. **ワークフローを明示的に指定**
```bash
gemini "@/mnt/c/article-flow 爪ケアについての記事を作成して"
```

2. **設定ファイルとINSTRUCTIONSを参照**
```bash
gemini "爪ケアについての記事を作成して。.gemini-cli-config.yamlとINSTRUCTIONS.mdに従ってください"
```

3. **完全な指示**
```bash
gemini "爪ケアについての記事を作成して。以下のワークフローを実行：
1. outputディレクトリに日付-タイトルでフォルダ作成
2. 各フェーズの成果物をすべて保存
3. 最終的にfinal.htmlを出力"
```

### パラメータ指定

**店舗情報を含める場合**
```bash
gemini "爪ケアについての記事を作成して store_url=https://nailsalon.com target=セルフケア初心者"
```

**文字数を指定する場合**
```bash
gemini "爪ケアについての記事を作成して word_count=4000"
```

### トラブルシューティング

**ワークフローが起動しない場合**
1. 現在のディレクトリを確認
   ```bash
   cd /mnt/c/article-flow
   gemini "記事を作成して"
   ```

2. 設定ファイルを明示的に指定
   ```bash
   gemini --config .gemini-cli-config.yaml "記事を作成して"
   ```

3. INSTRUCTIONSを直接参照
   ```bash
   gemini "INSTRUCTIONS.mdの手順で爪ケアの記事を作成"
   ```

### 出力の確認

生成完了後、以下のコマンドで確認：
```bash
# 最新の出力ディレクトリを表示
ls -la output/

# final.htmlの存在確認
find output/ -name "final.html" -type f

# 生成された記事を確認
cat output/*/final.html
```

### 推奨フロー

1. **記事生成を実行**
   ```bash
   gemini "爪ケアについての記事を作成して"
   ```

2. **進行状況を確認**
   - リサーチフェーズ: 15-25回のWeb検索
   - ファクトチェック: 追加5-10回の検索
   - 画像生成: 各H2セクションに1枚

3. **完了後の確認**
   ```bash
   # 出力ディレクトリを確認
   ls -la output/2025-01-23-nail-care/
   
   # 最終HTMLを開く
   open output/2025-01-23-nail-care/final.html
   ```

## 注意事項

- Gemini CLIは`.gemini-cli-config.yaml`を自動的に読み込みます
- 「についての記事を作成」というフレーズがトリガーになります
- すべての成果物は`output/YYYY-MM-DD-{title}/`に保存されます
- 最重要ファイルは`final.html`です

## よくある質問

**Q: ワークフローが途中で止まった場合は？**
A: `gemini --resume`で再開できます

**Q: 生成された画像を確認したい**
A: `output/*/images/`ディレクトリを確認してください

**Q: ファクトチェックレポートを見たい**
A: `output/*/03_5_factcheck_report.json`を確認してください