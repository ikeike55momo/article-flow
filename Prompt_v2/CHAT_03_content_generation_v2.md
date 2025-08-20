# チャット用 Phase 3: 記事本文生成プロンプト（改訂版v2）

## 使用方法
Phase 2で作成した記事構成とコンテンツ計画をもとに、HTML形式の記事を生成してください。

---

# 記事本文生成（HTML形式）

プロフェッショナルなコンテンツライターとして、Phase 2の構成に従って高品質な記事を生成してください。
CSSクラス名は提供された「スタイル仕様書」から必要に応じて使用します。

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

### 関連記事URL（ブログカード用）
【記事テーマに関連する参考記事のURLを3-4個記載】
- https://example.com/related-article1
- https://example.com/related-article2
- https://example.com/related-article3

## 記事生成ルール

### 1. 基本方針
- **Phase 2の構成を忠実に実装**してください
- 必要に応じて「article-style.md」のクラス名を使用
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

#### 利用可能な主要パーツ（必要に応じて使用）

**導入部分：**
- 専門家バッジ: `<div class="article-expert-badge">`
- リード文: `<p class="article-lead-text">`
- 目次: `<div class="article-toc">` （アンカーリンクを正しく設定）

**本文パーツ：**
- 画像: `<figure class="article-content-image">` + `<figcaption>`
- ハイライト: `<div class="article-highlight-box">`
- ステップ: `<ol class="article-steps-list">`
- 比較表: `<table class="article-comparison-table">`
- 引用: `<div class="article-quote">`
- FAQ: `<div class="article-faq-section">`

**出典・引用：**
- 本文中の引用: `<a class="article-cite" href="#fn-1" id="fnref-1">[1]</a>`
- 末尾の出典リスト: `<ol class="article-citations">`

**ブログカード：**
- シンプルな形式: `[blog_card url="記事URL"]`

**CTA：**
- `<section class="article-cta-section">`

### 3. 出典の扱い方（重要）

本文中で統計データや専門的主張を述べる際は必ず出典を付けてください：

```html
<!-- 本文中 -->
<p>〇〇という研究結果があります<a class="article-cite" href="#fn-1" id="fnref-1">[1]</a>。</p>

<!-- 記事末尾 -->
<div class="article-reliability-info">
  <h3>この記事の信頼性について</h3>
  <ol class="article-citations">
    <li id="fn-1">
      <a href="実際のURL" target="_blank" rel="noopener">出典名</a>
      <a href="#fnref-1" class="fn-back" aria-label="本文へ戻る">↩</a>
    </li>
  </ol>
</div>
```

### 4. Phase 2構成の実装方法

Phase 2で決定した構成（セクション数、内容、文字数配分）に従って記事を作成してください：

1. **導入部**: Phase 2で計画したリード文の内容
2. **目次**: Phase 2で決定したセクションタイトル
3. **各セクション**: Phase 2の計画に基づいた内容
4. **FAQ**: Phase 2で挙げた質問と回答
5. **まとめ**: Phase 2で計画した要点整理

### 5. ブログカードの配置

関連記事への内部リンクとして、適切な場所にブログカードを配置：

```html
<!-- 記事の流れの中で自然に挿入 -->
<p>この方法についてさらに詳しく知りたい方は、こちらの記事も参考にしてください。</p>
[blog_card url="https://example.com/related-article"]
```

### 6. CTAセクション

記事内容に最適化したCTAを記事末尾に配置：

```html
<section class="article-cta-section">
  <h2>【記事テーマに合わせた行動喚起タイトル】</h2>
  <p>【記事内容を踏まえた誘導文】</p>
  <a href="https://beauty.hotpepper.jp/kr/slnH000618948/" class="article-cta-button">ご予約はこちら</a>
</section>
```

## 文字数配分の目安
- Phase 2で決定した文字数配分に従う
- 総文字数: 【指定文字数】±300文字

## 品質チェックリスト

生成時に以下を確認：
- [ ] Phase 2の構成通りのセクション構成
- [ ] リサーチ結果から5つ以上の出典を引用
- [ ] 適切な場所にブログカードを配置
- [ ] CTAが記事内容に最適化されている
- [ ] アンカーリンクが正しく機能する目次
- [ ] 指定文字数を遵守
- [ ] ペルソナに最適化された表現
- [ ] 薬機法・景表法に配慮した表現

## 出力形式

`<div class="article-content">` で開始し `</div>` で終了する完全なHTMLコードを出力してください。
インラインスタイル（`<style>`タグ）は含めないでください。

---

## 次のステップ
この記事をPhase 4（ファクトチェック）で品質確認します。