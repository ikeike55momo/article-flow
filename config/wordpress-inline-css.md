# WordPress インラインCSS定義

## 概要
このファイルは、WordPressで確実にCSSが適用されるよう、プロンプトに直接埋め込むCSS全文を管理します。

## 使用方法
- `prompts/04_optimization_v2.md`内に完全に記載済み
- **このCSSは改変禁止**
- **必ず`<style>`タグ内に完全に記述**

## CSS適用成功の要因
1. **完全なインライン記述**：外部ファイル参照を使わない
2. **改変禁止の明記**：AIがCSSを変更する余地をなくす
3. **`.wp-blog-post`による限定**：WordPress内での競合を回避
4. **!importantの不使用**：自然な詳細度で動作

## 元のプロンプトとの同一性
元の成功プロンプトのCSS部分を完全に再現：
- フォントファミリー: "Noto Sans JP", "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif
- すべてのクラス定義を同一に保持
- メディアクエリも含めて完全一致

## 注意事項
- このCSSは実績のある動作確認済みのものです
- 一切の改変を加えないでください
- WordPress環境での動作を最優先に設計されています