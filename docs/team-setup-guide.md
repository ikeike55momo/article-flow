# チーム向けセットアップガイド - Imagen画像生成

## 概要
このガイドでは、チームメンバーがarticle-flowプロジェクトでImagen画像生成機能を使えるようにするための手順を説明します。

## セットアップ時間: 約15分

## 必要なもの
- Googleアカウント
- Google AI StudioのAPIキー（管理者から提供 or 個人で取得）
- VS Code（推奨）

## セットアップ手順

### Step 1: プロジェクトのクローン
```bash
# リポジトリをクローン
git clone <repository-url>
cd article-flow

# 最新の状態に更新
git pull origin main
```

### Step 2: 環境変数の設定

#### オプション1: 個人APIキーを使用（推奨）
```bash
# .envファイルを作成
cp .env.example .env

# エディタで.envを開いて編集
# GOOGLE_AI_API_KEY=your_personal_api_key_here
```

#### オプション2: チーム共有APIキーを使用
```bash
# 管理者から提供されたAPIキーを設定
# セキュリティ上、Slackなどの安全な経路で共有
```

### Step 3: VS Code設定（MCP利用時）

1. **VS Codeで開く**
   ```bash
   code .
   ```

2. **拡張機能の確認**
   - Gemini Code Extension がインストールされているか確認
   - 必要に応じてインストール

3. **MCP設定の確認**
   - `.vscode/mcp.json`が存在することを確認
   - 環境変数が正しく参照されているか確認

### Step 4: 動作確認

```bash
# 環境変数が設定されているか確認
echo $GOOGLE_AI_API_KEY | head -c 10

# Gemini CLIでテスト実行
gemini "テスト記事を作成して（画像生成確認用）"
```

## APIキーの取得方法（個人用）

### 無料で始める場合
1. [Google AI Studio](https://aistudio.google.com)にアクセス
2. Googleアカウントでログイン
3. 「Get API key」→「Create API key」
4. 新規プロジェクトを作成または既存を選択
5. APIキーをコピー（**一度しか表示されません**）

### 注意事項
- 新規アカウントは$300の無料クレジット（90日間）
- 画像1枚あたり約$0.04（1024×1024）
- 月100枚で約$4のコスト

## セキュリティ設定

### 必須設定
```bash
# APIキーが.gitignoreに含まれているか確認
grep ".env" .gitignore || echo ".env" >> .gitignore

# 誤ってコミットしないように
git config --local core.excludesfile .gitignore
```

### 推奨設定
1. **APIキーのローテーション**
   - 30日ごとに更新を推奨
   - カレンダーリマインダーを設定

2. **使用量の監視**
   - [Google Cloud Console](https://console.cloud.google.com)で確認
   - 月次レポートをチームで共有

## トラブルシューティング

### よくある問題と解決方法

#### 1. "API key not valid"エラー
```bash
# APIキーが正しく設定されているか確認
cat .env | grep GOOGLE_AI_API_KEY

# 環境変数を再読み込み
source .env
```

#### 2. "MCP server not found"エラー
```bash
# npmがインストールされているか確認
npm --version

# なければインストール
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 3. 画像が生成されない
- `.vscode/mcp.json`の設定を確認
- VS Codeを再起動
- Gemini CLIを最新版に更新

## ベストプラクティス

### 開発時の推奨事項
1. **テスト時は低解像度で**
   ```yaml
   # 開発環境での設定
   image_settings:
     width: 512
     height: 512
     quality: "high"
   ```

2. **画像キャッシュの活用**
   - 一度生成した画像は`output/*/images/`に保存
   - 同じプロンプトでの再生成を避ける

3. **コスト管理**
   - 月間使用量をチームで共有
   - 必要な画像のみ生成
   - プレースホルダーの併用

## チーム運用ルール

### 1. APIキー管理
- **個人キー推奨**: 各自のGoogle AI StudioアカウントでAPIキー取得
- **共有キー**: 必要最小限のメンバーのみアクセス
- **ローテーション**: 月1回の定期更新

### 2. コスト配分
- 個人キー使用時: 各自負担（月$5程度）
- 共有キー使用時: プロジェクト予算から支出
- 月次レビューでコスト最適化

### 3. 品質管理
- 生成画像は`images/`フォルダに自動保存
- 不適切な画像は即座に削除
- 品質基準を満たさない場合は再生成

## サポート

### 問題が解決しない場合
1. プロジェクトのSlackチャンネルで質問
2. [GitHub Issues](https://github.com/your-repo/issues)に報告
3. 管理者に直接連絡

### 参考リンク
- [Google AI Studio Documentation](https://ai.google.dev/docs)
- [MCP Documentation](https://github.com/modelcontextprotocol/docs)
- [Gemini CLI Guide](https://github.com/google/generative-ai-docs)

## 更新履歴
- 2025-01-23: 初版作成
- Phase 3 (Imagen) 実装に対応