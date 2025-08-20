# Prompt Evolution & Version History

## Current Production Stack (V4)

### Active Prompts (December 2024)
- **Writing**: `04_writing_v4_html_updated.md` - HTML output with citations
- **Analysis**: Inline YAML prompts in workflow
- **Structure**: Inline YAML prompts in workflow  
- **Factcheck**: Inline YAML prompts in workflow
- **SEO**: Inline YAML prompts in workflow
- **Images**: Inline YAML prompts in workflow
- **Finalization**: Inline YAML prompts in workflow

### Key Improvements in V4
1. **Integrated Citations**: Mandatory source attribution with research_results.json
2. **HTML-First Output**: Direct HTML generation with proper CSS classes
3. **Quality Scoring**: Built-in fact-checking with numerical scores
4. **Dynamic CTA**: Context-aware call-to-action generation
5. **MCP Image Generation**: Imagen4 integration via MCP servers
6. **Parallel Research**: 3-batch concurrent Gemini API research

## Evolution Timeline

### V1 (Early 2024)
- Sequential phases with separate prompts
- Markdown output only
- Manual fact-checking
- Basic SEO optimization
- Single-threaded research

### V2 (Mid 2024)  
- Enhanced factcheck prompts (03_5_factcheck.md)
- Improved optimization (04_optimization_v2.md)
- WordPress compatibility focus
- Citation system introduction

### V3 (Late 2024)
- HTML template integration
- Advanced image generation
- Multi-language support
- Enhanced persona targeting

### V4 (Current - December 2024)
- **Breakthrough**: Direct HTML output with embedded styling
- **Research Revolution**: Gemini API parallel processing
- **Quality Focus**: Comprehensive fact-checking with scores
- **Image Innovation**: MCP + Imagen4 integration
- **Production Ready**: Simplified 5-deliverable output

## Prompt Design Patterns

### Template Integration Pattern
```markdown
## Reference Files
必ず以下のファイルを読み込んで出力形式を理解してください：
1. `sample/articles/hand-cream-article.html` - 実際の出力サンプル
2. `sample/articles/article-style.md` - 記事作成ガイド
```

### Citation Requirements Pattern
```markdown
### 出典の扱い方（最重要）
- research_results.jsonから信頼できるソースを5つ以上選定
- 本文中に `<a class="article-cite" href="#fn-1">[1]</a>` 形式で追加
```

### Quality Validation Pattern
```markdown
## Quality Check
- [ ] research_results.jsonから実際のURLを5つ以上引用
- [ ] 指定文字数の遵守
- [ ] ペルソナに最適化された内容
```

### Environment Variable Pattern
```markdown
## Environment Variables
- ARTICLE_ID: {{ARTICLE_ID}}
- TITLE: {{TITLE}}
- TARGET_PERSONA: {{TARGET_PERSONA}}
```

## Future Considerations

### Potential V5 Features
- Real-time fact-checking integration
- Advanced image prompt optimization
- Multi-modal output (video thumbnails)
- International SEO support
- Advanced competitor analysis
- Voice tone adaptation
- Interactive content elements

### Technical Debt
- Legacy prompt files (need cleanup)
- Inconsistent variable naming
- Duplicate functionality across versions
- Missing error handling in some prompts

### Performance Optimization
- Token usage reduction
- Faster research processing
- Better image generation prompts
- Reduced API calls where possible