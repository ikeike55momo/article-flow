# 画像生成機能実装プラン - チーム共有対応版

## 実装方針

### 🎯 目標
1. **チーム全員が簡単にセットアップできる**
2. **コスト効率を重視**（初期は無料、本格運用時のみ有料）
3. **セキュリティを確保**（APIキー管理）
4. **フォールバック機能**（画像生成失敗時の対応）

## Phase 1: 無料代替案での実装

### 選択肢1: Hugging Face API（推奨）

**メリット:**
- 完全無料
- 高品質なモデル（Stable Diffusion等）
- 簡単なAPI
- チーム共有が容易

**実装:**

```yaml
# .gemini-cli-config.yaml
image_generation:
  enabled: true
  provider: "hugging_face"
  fallback_provider: "placeholder"
  api_settings:
    base_url: "https://api-inference.huggingface.co"
    model: "stabilityai/stable-diffusion-xl-base-1.0"
    timeout: 30
```

**セットアップ手順:**

1. **Hugging Face登録**
   ```bash
   # 1. https://huggingface.co でアカウント作成
   # 2. Settings > Access Tokens でトークン生成
   # 3. Read権限のみでOK
   ```

2. **環境変数設定**
   ```bash
   # .env.example をコピー
   cp .env.example .env
   
   # APIキーを設定
   echo "HUGGINGFACE_API_KEY=your_token_here" >> .env
   ```

3. **即座に利用開始**
   ```bash
   gemini "爪ケアについての記事を作成して"
   # 画像生成も自動実行
   ```

### 選択肢2: starryai API

**メリット:**
- 月100枚無料
- 商用利用可能
- クレジットカード不要

**デメリット:**
- 月間制限あり
- アート寄りのスタイル

## Phase 2: 商用グレードの実装

### Imagen + MCP実装

**前提条件:**
```bash
# Google Cloud Platformアカウント必須
# $300無料クレジット（新規のみ）
```

**MCP設定例:**
```json
// .vscode/mcp.json
{
  "mcpServers": {
    "imagen-server": {
      "command": "python",
      "args": ["-m", "imagen_mcp_server"],
      "env": {
        "GOOGLE_API_KEY": "${GOOGLE_AI_API_KEY}",
        "PROJECT_ID": "${GOOGLE_CLOUD_PROJECT}"
      }
    }
  }
}
```

## チーム共有の仕組み

### ディレクトリ構造
```
article-flow/
├── .env.example              # 環境変数サンプル
├── .gitignore               # 認証情報除外
├── setup/
│   ├── team-setup.md        # チーム向けセットアップガイド
│   ├── api-key-setup.md     # APIキー取得手順
│   └── troubleshooting.md   # トラブルシューティング
├── config/
│   ├── image-generation.yaml # 画像生成設定
│   └── fallback-rules.yaml  # フォールバック設定
└── scripts/
    └── verify-setup.sh      # 設定確認スクリプト
```

### セキュリティ対策

**必須設定:**
```gitignore
# .gitignore
.env
.env.local
*.key
*_api_key*
.vscode/mcp.json.local
google-credentials.json
```

**APIキー管理:**
```bash
# 個人の設定ディレクトリ
~/.gemini/
├── credentials.env  # 個人のAPIキー
└── config.json     # 個人設定
```

**ローテーション設定:**
```yaml
# config/security.yaml
api_key_rotation:
  interval_days: 30
  notification: true
  auto_rotation: false  # 手動確認を推奨
```

## 実装優先順位

### 🚀 即座に実装（推奨）
1. **Hugging Face API統合**
   - コスト: $0
   - セットアップ時間: 10分
   - チーム展開: 即日可能

### 📈 中期実装
2. **starryai追加**
   - 品質向上
   - バリエーション増加

### 🎯 本格運用時
3. **Imagen + MCP**
   - プロレベルの品質
   - 月$20-50程度の予算確保後

## 推定コスト

### Phase 1（無料期間）
```
Hugging Face API: $0/月
starryai: $0/月（100枚まで）
合計: $0/月
```

### Phase 2（本格運用）
```
Google AI Studio: ~$30/月（1000枚生成）
フォールバック: $0/月
合計: $30/月程度
```

## 次のアクション

1. **即座に実装可能**: Hugging Face API統合
2. **チーム配布**: セットアップガイド作成
3. **品質確認**: 生成画像のテスト
4. **将来計画**: 商用プランへの移行準備

どのPhaseから開始しますか？