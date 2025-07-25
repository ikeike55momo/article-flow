# ワークフローでの画像生成 - 実用的なアプローチ

## 📋 現実的な実装方法

Gemini CLIの調査結果を踏まえ、以下の段階的アプローチを推奨します：

### Phase 1: プロンプト自動生成（実装済み）
Gemini CLIが実行できる範囲：
- ✅ 各セクションに最適な画像生成プロンプトを作成
- ✅ SEO最適化されたalt属性を生成
- ✅ 画像配置のHTMLコードを準備
- ✅ 推奨設定とコスト情報を提供

### Phase 2: 外部ツールでの画像生成（手動/半自動）
ユーザーが実行する範囲：
- 生成されたプロンプトを外部ツールにコピー
- 画像を生成（Imagen 3, DALL-E 3, Midjourney等）
- 生成画像をoutput/images/フォルダに保存

### Phase 3: 自動統合（将来的）
- 生成画像を自動でHTMLに統合
- WebP最適化とリサイズ
- alt属性の最終調整

## 🔄 実際のワークフロー

### ステップ1: 記事生成（自動）
```bash
gemini "爪ケアについての記事を作成して"
```

### ステップ2: プロンプト確認（自動出力）
生成される内容：
```
output/2025-01-23-nail-care/
├── 04_5_image_prompts.json    # 各セクションの画像プロンプト
├── 04_5_image_guide.md        # 画像生成手順書
└── final_with_placeholders.html # プレースホルダー付きHTML
```

### ステップ3: 画像生成（手動）
**選択肢1: Google AI Imagen 3**
```bash
# https://aistudio.google.com で実行
# プロンプト: output/*/04_5_image_prompts.json から各プロンプトをコピー
# 設定: 800x600, 高品質, 2バリエーション
```

**選択肢2: DALL-E 3 (ChatGPT Plus)**
```bash
# ChatGPT Plusで実行
# プロンプト例: "爪の構造を示すプロフェッショナルな医療イラスト..."
```

**選択肢3: Midjourney**
```bash
# Discord/Webで実行
# /imagine プロンプト + --ar 4:3 --quality 2
```

**選択肢4: Stable Diffusion（無料）**
```bash
# ComfyUI, Automatic1111, またはHugging Face
# ローカル実行で完全無料
```

### ステップ4: 画像配置（半自動）
```bash
# 生成した画像をリネーム
nail-care-basics-01.webp
nail-care-methods-01.webp
nail-care-tools-01.webp

# imagesフォルダに配置
mv *.webp output/2025-01-23-nail-care/images/

# HTMLの更新（プレースホルダーを実画像に置換）
```

## 💡 推奨ツールとコスト

### 商品質重視
1. **Google AI Imagen 3** - $0.04/画像
   - 最高品質
   - 商用利用安心
   - 新規$300無料クレジット

2. **DALL-E 3** - $0.04/画像
   - ChatGPT Plus($20/月)で利用
   - 優秀な画像理解
   - 簡単な使用方法

### コスト重視
3. **Midjourney** - $10/月で200枚
   - コスパ最強
   - アート品質
   - 商用利用OK

4. **Stable Diffusion** - 完全無料
   - ローカル実行
   - カスタマイズ豊富
   - 学習コストあり

## 🚀 時短のためのテンプレート

### プロンプトテンプレート
```
プロフェッショナルな[業界]向けの画像。
[具体的な内容説明]を視覚的に表現。
スタイル: 清潔、信頼感、明るい色調
品質: 商用利用可能、高解像度
除外: テキスト、ロゴ、透かし
アスペクト比: 4:3
```

### ファイル命名規則
```
{main_keyword}-{section_type}-{version}.webp

例:
nail-care-basics-01.webp
nail-care-methods-01.webp
nail-care-comparison-01.webp
```

## 📊 効率化のコツ

### バッチ処理
- 1記事分の全プロンプトを一度に生成
- 同じツールで連続生成
- 設定値を統一してブランド感を維持

### 品質管理
- 生成後は必ず内容確認
- ブランドガイドラインに準拠
- 不適切な内容は即座に再生成

### コスト管理
- 開発時は低解像度でテスト
- 本番前に品質確認
- 月間予算を設定して使いすぎ防止

この方法により、Gemini CLIの制限を活かしつつ、実用的な画像付き記事生成が可能になります。