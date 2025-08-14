# チャット用 Phase 3: 記事本文生成プロンプト

## 使用方法
Phase 2で作成した記事構成とコンテンツ計画をもとに、HTML形式の記事を生成してください。

---

# 記事本文生成（HTML形式）

プロフェッショナルなコンテンツライターとして、高品質な記事を指定されたHTMLテンプレート形式で生成してください。

## 入力情報

### 基本情報
- **記事タイトル**: 【ここに記事タイトルを入力】
- **ターゲットペルソナ**: 【ここにペルソナ情報を入力】
- **目標文字数**: 【ここに文字数を入力】

### Phase 1の分析結果
【Phase 1で出力されたJSONをここに貼り付け】

### Phase 2の構成・計画
【Phase 2で作成した記事構成とコンテンツ計画をここに貼り付け】

### リサーチ結果（重要：出典URL含む）
【リサーチで収集した情報を以下の形式で記載】
- **情報1**: 〇〇についての統計データ（出典: https://example1.com）
- **情報2**: 専門家の見解（出典: https://example2.com）
- **情報3**: 研究結果（出典: https://example3.com）
（以下続く...最低5つ以上の信頼できるソース）

## 重要要件

### 1. HTML基本構造（必須）
```html
<div class="article-content">
<style>
/* 最小限のスタイル */
.article-content { font-family: -apple-system, BlinkMacSystemFont, sans-serif; line-height: 1.7; }
.article-expert-badge { background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 20px 0; }
.article-lead-text { font-size: 18px; margin: 20px 0; background: #f8f9fa; padding: 20px; }
.article-toc { background: #fafafa; padding: 20px; margin: 20px 0; }
.article-content-image { text-align: center; margin: 20px 0; }
.article-highlight-box { background: #fff3e0; padding: 20px; border: 2px solid #ff9800; margin: 20px 0; }
.article-quote { background: #f5f5f5; padding: 15px; border-left: 3px solid #666; margin: 20px 0; font-style: italic; }
.quote-source { font-size: 14px; color: #666; display: block; margin-top: 10px; }
.article-comparison-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
.article-comparison-table th, .article-comparison-table td { border: 1px solid #ddd; padding: 12px; text-align: left; }
.article-comparison-table th { background: #f2f2f2; }
.article-faq-section { margin: 30px 0; }
.article-faq-item { margin: 15px 0; padding: 15px; background: #f9f9f9; }
.article-summary-section { background: #e8f5e8; padding: 20px; margin: 30px 0; }
.article-cta-section { background: #fff3e0; padding: 30px; text-align: center; margin: 30px 0; }
.article-cta-button { display: inline-block; background: #ff6b35; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; }
.article-reliability-info { margin: 40px 0; padding: 20px; background: #f0f8ff; }
.article-citations { list-style: decimal; }
.article-cite { color: #2196f3; text-decoration: none; font-weight: bold; }
.fn-back { color: #666; margin-left: 10px; }
</style>

<!-- 専門家バッジ -->
<div class="article-expert-badge">
<strong>【専門性の表示】</strong> 【記事テーマに関連する専門分野】の専門知識をもとに執筆しています。
</div>

<!-- リード文（統計・研究データ含む） -->
<div class="article-lead-text">
【ペルソナの悩みに共感する導入文】
【統計データや研究結果を含む】<a class="article-cite" href="#fn-1" id="fnref-1">[1]</a>
</div>

<!-- 以下、記事本文 -->
...

</div>
```

### 2. 出典の扱い方（最重要）

**本文中の引用：**
- 専門的な主張や統計データには必ず `<a class="article-cite" href="#fn-1" id="fnref-1">[1]</a>` を追加
- リサーチ結果から信頼できるソースを5つ以上選定

**引用ブロック（適宜使用）：**
```html
<div class="article-quote">
  <p>重要な見解や専門家の言葉<a class="article-cite" href="#fn-2">[2]</a>。</p>
  <span class="quote-source">参考: 本文の注記 [2] の出典を参照</span>
</div>
```

**末尾の出典リスト（必須）：**
```html
<div class="article-reliability-info">
  <h3>この記事の信頼性について</h3>
  <p>本記事は以下の信頼できる情報源をもとに作成しています。</p>
  <ol class="article-citations">
    <li id="fn-1">
      <a href="【実際のURL】" target="_blank" rel="noopener">【ソース名・記事タイトル】</a>
      <a href="#fnref-1" class="fn-back" aria-label="本文へ戻る">↩</a>
    </li>
    <li id="fn-2">
      <a href="【実際のURL】" target="_blank" rel="noopener">【ソース名・記事タイトル】</a>
      <a href="#fnref-2" class="fn-back" aria-label="本文へ戻る">↩</a>
    </li>
    <!-- 最低5つ以上 -->
  </ol>
</div>
```

### 3. CTAセクション（記事内容に最適化）

記事テーマに基づいて適切な文言を生成：

```html
<section class="article-cta-section">
  <h2>【記事テーマに合わせた行動喚起タイトル】</h2>
  <p>【記事内容を踏まえた具体的で説得力のある誘導文】</p>
  <a href="https://beauty.hotpepper.jp/kr/slnH000618948/" class="article-cta-button">ご予約はこちら</a>
</section>
```

**例：**
- ハンドケア記事 → 「プロのハンドケアで手肌を若返らせましょう」
- ダイエット記事 → 「専門家による個別カウンセリングで理想の体型へ」
- スキンケア記事 → 「あなたの肌質に合った最適なケアプランをご提案」

### 4. 必須要素の配置

1. **目次（article-toc）**
2. **各セクションに画像プレースホルダー**:
   ```html
   <div class="article-content-image">
   [画像: 【画像の説明】]
   </div>
   ```
3. **ハイライトボックス（重要なポイント）**
4. **比較表（必要に応じて）**
5. **FAQセクション（最低3つ）**
6. **まとめセクション**

### 5. 文字数配分
- 総文字数: 【入力した文字数】±300文字
- リード文: 10-15%
- 各セクション: 20-25%
- FAQ: 15-20%
- まとめ: 5-10%

## 品質チェックリスト

- [ ] リサーチ結果から実際のURLを5つ以上引用
- [ ] CTAセクションが記事内容に最適化されている
- [ ] 専門家バッジに適切な表現
- [ ] 引用番号と出典リストが正しくリンクされている
- [ ] 指定文字数を遵守している
- [ ] ペルソナに最適化された内容・表現
- [ ] 薬機法・景表法に配慮した表現
- [ ] 読みやすい構成と流れ

## 出力形式

`<div class="article-content">` で開始し `</div>` で終了する完全なHTMLコードを出力してください。

---

## 次のステップ
この記事をPhase 4（ファクトチェック）で品質確認します。