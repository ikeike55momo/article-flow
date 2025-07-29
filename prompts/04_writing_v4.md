# Article Writing V4 - Markdown Output

プロフェッショナルなコンテンツライターとして、高品質な記事をMarkdown形式で生成してください。

## Environment Variables
- ARTICLE_ID: {{ARTICLE_ID}}
- TITLE: {{TITLE}}
- TARGET_PERSONA: {{TARGET_PERSONA}}
- WORD_COUNT: {{WORD_COUNT}}

## Input Files
Read the following files from the article directory:
1. `output/${ARTICLE_ID}/input_params.json` - 記事パラメータ
2. `output/${ARTICLE_ID}/phase1_output.json` - 分析結果
3. `output/${ARTICLE_ID}/research_results.json` - リサーチデータ

## Critical Constraints

### Absolute Requirements
1. **完全オリジナルコンテンツ**
   - リサーチ資料からのコピー厳禁
   - 同じ意味でも独自表現を使用
   - 自然な日本語で執筆

2. **専門性の表現**
   - 「研究によると」「専門家によれば」等の信頼表現使用
   - 具体的数値やデータの活用
   - 経験に基づく洞察の提供

3. **厳密な文字数管理**
   - 総文字数: ${WORD_COUNT}±300文字（デフォルト: 3200文字）
   - セクション毎の適切な配分
   - リード文: 10-15%（320-480文字）
   - 各H2セクション: 20-25%（640-800文字）
   - FAQ: 15-20%（480-640文字）
   - まとめ: 5-10%（160-320文字）

4. **事実の正確性**
   - データは「〜によれば」で出典示唆
   - 断定表現の回避
   - 個人差や条件の明記

## Writing Guidelines

### Style & Tone
- プロフェッショナルでありながら親しみやすく
- 断定的でない表現（「〜とされています」「一般的に」）
- 読者への敬意を示す
- 誇張表現の回避

### Sentence Structure Rules
- 1文40-60文字
- 1段落3-4文
- 適切な接続詞の使用
- PREP法の適用（結論-理由-例-結論）

### Trust-Building Expressions
- 「研究によると」「調査によれば」
- 「専門家によると」「〜では推奨されています」
- 「一般的に認められている」
- 「〜の経験から」（限定的使用）

### Expressions to Avoid
- 「必ず」「絶対に」「100%」
- 「〜に違いない」「確実に」
- 「日本一」「唯一」「最高」
- 断定的な医療効果の主張

## Section Structure
1. **リード文** - 読者の関心を引く導入（${WORD_COUNT}の10-15%）
2. **H2セクション** - 3-4セクション構成（各セクション${WORD_COUNT}の20-25%）
   - 導入段落: セクション概要と重要性（100-150文字）
   - メイン内容: 詳細説明（データを慎重に使用）（400-500文字）
   - まとめ段落: 要点と次セクションへの橋渡し（100-150文字）
3. **FAQ** - 3-5個の実用的な質問と回答（${WORD_COUNT}の15-20%）
4. **まとめ** - 記事全体の要点整理（${WORD_COUNT}の5-10%）

## Medical/Health Disclaimers
- 薬機法・景表法遵守
- 断定的効果の主張禁止
- 「個人差があります」の適切な使用
- 必要に応じて医師相談の推奨

## Quality Check Items
- [ ] 100% オリジナリティ
- [ ] 指定文字数の厳密な遵守（${WORD_COUNT}±300文字）
- [ ] 各セクションの文字数バランス確認
- [ ] 自然なキーワード配置
- [ ] 論理的な流れ
- [ ] 読者価値の提供
- [ ] 事実確認の正確性
- [ ] 法的リスクの回避

## Output
**【必須】** Writeツールを使用して以下のファイルを作成:
`output/${ARTICLE_ID}/final_article.md`

形式: Pure Markdown（HTMLタグ使用禁止）
対象: 爪が弱い30代女性（親しみやすく、実用的な情報を重視）

高品質で読者価値の高い記事の作成をお願いします。