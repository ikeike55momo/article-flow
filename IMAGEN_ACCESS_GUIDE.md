# Vertex AI Imagen API アクセスガイド

## 現在の状況（2025年1月）

Vertex AI Imagen APIは**限定アクセス**です。価格ページに掲載されていますが、使用するには事前承認が必要です。

## 403エラーの解決手順

### 1. Imagen APIへのアクセス申請

**必須**: [Imagen on Vertex AI access form](https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview) から申請

申請時に必要な情報：
- プロジェクトID: `article-flow-imagen`
- 使用目的の説明
- 予想される月間使用量

### 2. 利用可能なモデル（2025年1月現在）

```python
# アクセス承認後に使用可能
IMAGEN_MODELS = {
    "fast": "imagen-3.0-fast-generate-001",    # 高速版（推奨）
    "standard": "imagen-3.0-generate-001",      # 標準版
    "legacy": "imagegeneration@006"             # レガシー版
}
```

### 3. 重要な日付

- **2025年2月1日**: Imagen 3.0（`imagen-3.0-generate-001`）廃止予定
- 移行先: Imagen 3 Fast（`imagen-3.0-fast-generate-001`）

## 代替ソリューション

### A. Gemini Pro Visionを使用（即座に利用可能）

```python
import google.generativeai as genai

class GeminiImageGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_enhanced_prompt(self, prompt: str) -> str:
        """Geminiを使って画像生成プロンプトを強化"""
        enhanced = self.model.generate_content(
            f"Create a detailed image generation prompt for: {prompt}"
        )
        return enhanced.text
```

### B. 他の画像生成API

1. **OpenAI DALL-E 3**
   ```python
   from openai import OpenAI
   client = OpenAI()
   response = client.images.generate(
       model="dall-e-3",
       prompt=prompt,
       size="1024x1024"
   )
   ```

2. **Stability AI (Stable Diffusion)**
   ```python
   import requests
   response = requests.post(
       "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
       headers={"Authorization": f"Bearer {api_key}"},
       json={"text_prompts": [{"text": prompt}]}
   )
   ```

### C. ハイブリッドアプローチ（推奨）

```python
class HybridImageGenerator:
    def __init__(self, config):
        self.generators = {
            "imagen": ImagenGenerator(config) if config.get("imagen_enabled") else None,
            "dalle": DalleGenerator(config) if config.get("dalle_api_key") else None,
            "placeholder": PlaceholderGenerator()
        }
    
    async def generate(self, prompt: str, preferred: str = "imagen"):
        # 優先順位に従って試行
        for generator_name in [preferred, "dalle", "placeholder"]:
            generator = self.generators.get(generator_name)
            if generator:
                try:
                    return await generator.generate(prompt)
                except Exception as e:
                    logger.warning(f"{generator_name} failed: {e}")
                    continue
        
        raise Exception("All generators failed")
```

## GitHub Actions設定の更新

```yaml
env:
  # Imagen API（承認後）
  GOOGLE_CLOUD_PROJECT: article-flow-imagen
  VERTEX_AI_LOCATION: us-central1
  
  # 代替API
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  STABILITY_API_KEY: ${{ secrets.STABILITY_API_KEY }}
  
  # フラグ
  USE_IMAGEN: ${{ secrets.IMAGEN_ACCESS_APPROVED || 'false' }}
```

## トラブルシューティング

### 問題: 403 IAM_PERMISSION_DENIED
**原因**: プロジェクトがImagenのallowlistに未登録
**解決**: アクセスフォームから申請し、承認を待つ

### 問題: モデルが見つからない
**原因**: 古いモデル名を使用
**解決**: `imagen-3.0-fast-generate-001`に更新

### 問題: リージョンエラー
**原因**: Imagenは`us-central1`のみサポート
**解決**: `VERTEX_AI_LOCATION=us-central1`を使用

## まとめ

1. **Imagen APIは存在するが、事前承認が必要**
2. **承認待ちの間は代替ソリューションを使用**
3. **2025年2月までに新モデルへの移行が必要**
4. **複数のプロバイダーをサポートする柔軟な設計を推奨**