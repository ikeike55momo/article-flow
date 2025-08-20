# チャット用 Phase 3: 記事本文生成プロンプト（改訂版v3）

## 使用方法
Phase 2で作成した記事構成とコンテンツ計画をもとに、HTML形式の記事を生成してください。
**必ずARTICLE-TEMPLATE-README.mdの仕様に完全準拠してください。**

---

# 記事本文生成（HTML形式）

プロフェッショナルなコンテンツライターとして、Phase 2の構成に従って高品質な記事を生成してください。
**ARTICLE-TEMPLATE-README.mdのCSSクラス仕様を完全に遵守してください。**

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

### 関連記事URL（ブログカード用・任意）
【記事テーマに関連する参考記事のURLを必要に応じて記載】
- https://example.com/related-article1
- https://example.com/related-article2
- https://example.com/related-article3

## 記事生成ルール（ARTICLE-TEMPLATE-README.md準拠）

### 1. 基本方針
- **Phase 2の構成を忠実に実装**してください
- **ARTICLE-TEMPLATE-README.md**のクラス仕様を完全遵守
- WordPressのHTMLブロックに貼り付けることを前提
- セマンティックで読みやすいHTMLを生成

### 2. HTML構造の要件

#### 基本構造（必須）
```html
<div class="article-content">
  <!-- 記事全体をこのコンテナで囲む -->
  
  <!-- 以下、Phase 2の構成に従って記事を展開 -->
  
</div>
```

#### 標準パーツ（ARTICLE-TEMPLATE-README.md準拠）

**導入部分：**
```html
<!-- 信頼性バッジ -->
<div class="article-expert-badge">
  <p>この記事は<strong>実際に体験・調査を行った上で執筆</strong>しています。</p>
</div>

<!-- リードテキスト -->
<p class="article-lead-text">
  記事の導入文をここに記載します。
</p>

<!-- 目次 -->
<div class="article-toc">
  <h2>目次タイトル</h2>
  <ul>
    <li><a href="#section1">セクション1のタイトル</a></li>
    <li><a href="#section2">セクション2のタイトル</a></li>
  </ul>
</div>
```

**本文パーツ：**
```html
<!-- ハイライトボックス（1セクション1個まで） -->
<div class="article-highlight-box">
  <h4>重要なポイント</h4>
  <p>ここに重要な情報を記載します。</p>
</div>

<!-- ステップリスト -->
<ol class="article-steps-list">
  <li>
    <h4>Step 1: タイトル</h4>
    <p>詳細説明</p>
  </li>
</ol>

<!-- 比較テーブル -->
<table class="article-comparison-table">
  <thead>
    <tr>
      <th>項目</th>
      <th>内容</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>データ1</td>
      <td>データ2</td>
    </tr>
  </tbody>
</table>

<!-- 引用ブロック -->
<div class="article-quote">
  <p>引用内容<a class="article-cite" href="#fn-1">[1]</a></p>
  <span class="quote-source">参考: 情報源</span>
</div>
```

### 3. FAQ部分（重要：構造を正確に）

```html
<div class="article-faq-section">
  <h2>よくある質問</h2>
  
  <div class="article-faq-item">
    <input type="checkbox" id="faq1">
    <label for="faq1" class="article-faq-question">
      <span>Q1: 質問内容</span>
    </label>
    <div class="article-faq-answer">A1: 回答内容</div>
  </div>
  
  <div class="article-faq-item">
    <input type="checkbox" id="faq2">
    <label for="faq2" class="article-faq-question">
      <span>Q2: 質問内容</span>
    </label>
    <div class="article-faq-answer">A2: 回答内容</div>
  </div>
</div>
```

### 4. 出典・引用の扱い方

```html
<!-- 本文中 -->
<p>研究結果によると<a class="article-cite" href="#fn-1" id="fnref-1">[1]</a>、〇〇ということが明らかになっています。</p>

<!-- 記事末尾 -->
<div class="article-reliability-info">
  <h3>この記事の信頼性について</h3>
  <ol class="article-citations">
    <li id="fn-1">
      <a href="実際のURL" target="_blank" rel="noopener">出典名</a>
      <a href="#fnref-1" class="fn-back">↩</a>
    </li>
    <li id="fn-2">
      <a href="実際のURL" target="_blank" rel="noopener">出典名</a>
      <a href="#fnref-2" class="fn-back">↩</a>
    </li>
  </ol>
</div>
```

### 5. strongタグの使用ガイドライン

**使用する場所：**
- 文章内の重要なポイント
- 注意点、推奨事項
- 成功のコツ
- 読者の理解を助ける強調

**使用しない場所：**
- ラベル（「住所：」など）
- 項目名・見出し
- 短い単語やラベル
- 専門家バッジ・CTAセクション（既定の場所以外）

### 6. ハイライトボックスの使用制限

- **導入部分（リードテキスト周辺）**: 積極的に使用推奨
- **メインセクション内**: 1セクション1個まで、本当に重要な情報のみ
- **料金・重要情報セクション**: 複雑な情報整理の場合は使用可
- **過度な使用は避ける**: 基本はh3+p構造を使用

### 7. ブログカードの配置（任意）

```html
<!-- 記事の流れの中で自然に挿入 -->
<p>詳しい手順については、こちらの記事も参考にしてください。</p>
[blog_card url="https://example.com/related-article"]
```

### 8. CTAセクション

```html
<section class="article-cta-section">
  <h2>【記事テーマに合わせた行動喚起タイトル】</h2>
  <p>【記事内容を踏まえた誘導文】</p>
  <a href="【適切なURL】" class="article-cta-button">ボタンテキスト</a>
</section>
```

## 品質チェックリスト（v3強化版）

生成時に以下を確認：
- [ ] **ARTICLE-TEMPLATE-README.md仕様に完全準拠**
- [ ] Phase 2の構成通りのセクション構成
- [ ] セマンティックなHTML構造
- [ ] strongタグの適切な使用（文章内の重要ポイントのみ）
- [ ] ハイライトボックスの制限遵守（1セクション1個まで）
- [ ] FAQの構造が標準仕様通り（checkbox + label + span）
- [ ] アンカーリンクが正しく機能する目次
- [ ] リサーチ結果から5つ以上の出典を引用
- [ ] 出典リンクの形式が正しい（fn-1, fnref-1等）
- [ ] 適切な場所にブログカードを配置（任意）
- [ ] CTAが記事内容に最適化されている
- [ ] 指定文字数を遵守
- [ ] ペルソナに最適化された表現
- [ ] 薬機法・景表法に配慮した表現

## 文字数配分の目安
- Phase 2で決定した文字数配分に従う
- 総文字数: 【指定文字数】±300文字
- 基本構成: h3見出し + pテキストを基本とする

## 出力形式

`<div class="article-content">` で開始し `</div>` で終了する完全なHTMLコードを出力してください。
インラインスタイル（`<style>`タグ）は含めないでください。

---

## 次のステップ
この記事をPhase 4（ファクトチェック）で品質確認します。