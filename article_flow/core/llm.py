#!/usr/bin/env python3
"""
LLM API統一インターフェース - Claude API abstraction
"""

import os
import json
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class LLMProvider:
    """LLM API統一インターフェース"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")
    
    def generate_with_structured_output(
        self,
        prompt: str,
        system_prompt: str = "",
        expected_format: Optional[Dict[str, Any]] = None,
        temperature: float = 0.1,
        metadata: Optional[Dict[str, Any]] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        構造化出力でLLMからレスポンスを取得
        
        Args:
            prompt: ユーザープロンプト
            system_prompt: システムプロンプト
            expected_format: 期待する出力形式
            temperature: 温度パラメータ
            metadata: メタデータ
            max_retries: 最大リトライ回数
            
        Returns:
            Dict: LLMからの構造化レスポンス
        """
        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic package is required. Install with: pip install anthropic")
        
        client = anthropic.Anthropic(api_key=self.api_key)
        
        for attempt in range(max_retries):
            try:
                # Claude APIを呼び出し
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    temperature=temperature,
                    system=system_prompt,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # レスポンステキストを取得
                response_text = response.content[0].text.strip()
                logger.debug(f"Raw LLM response: {response_text[:500]}...")
                
                # JSONとしてパース試行
                try:
                    result = json.loads(response_text)
                    logger.info("Successfully parsed structured output")
                    return result
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON parse failed (attempt {attempt + 1}): {e}")
                    if attempt == max_retries - 1:
                        return {
                            "parse_error": str(e),
                            "raw_response": response_text
                        }
                    time.sleep(2 ** attempt)  # Exponential backoff
                    
            except Exception as e:
                logger.error(f"LLM API call failed (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)
        
        raise RuntimeError("All retry attempts failed")
    
    def generate_text(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.1,
        max_tokens: int = 4000
    ) -> str:
        """
        テキスト生成（非構造化）
        
        Args:
            prompt: ユーザープロンプト
            system_prompt: システムプロンプト
            temperature: 温度パラメータ
            max_tokens: 最大トークン数
            
        Returns:
            str: 生成されたテキスト
        """
        try:
            import anthropic
        except ImportError:
            raise ImportError("anthropic package is required. Install with: pip install anthropic")
        
        client = anthropic.Anthropic(api_key=self.api_key)
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text.strip()


class PromptLoader:
    """プロンプトファイル読み込み"""
    
    @staticmethod
    def load_prompt(prompt_dir: Path, filename: str) -> str:
        """
        指定されたディレクトリからプロンプトファイルを読み込み
        
        Args:
            prompt_dir: プロンプトディレクトリパス
            filename: ファイル名（.md拡張子は自動付与）
            
        Returns:
            str: プロンプト内容
        """
        if not filename.endswith('.md'):
            filename += '.md'
            
        prompt_path = prompt_dir / filename
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logger.debug(f"Loaded prompt from: {prompt_path}")
        return content
    
    @staticmethod
    def format_prompt(template: str, **kwargs) -> str:
        """
        プロンプトテンプレートに変数を代入
        
        Args:
            template: プロンプトテンプレート
            **kwargs: 置換変数
            
        Returns:
            str: フォーマット済みプロンプト
        """
        try:
            # 【】形式のプレースホルダーを{}形式に変換
            formatted_template = template
            for key, value in kwargs.items():
                # 【key】→ value に置換
                placeholder = f"【ここに{key}を入力】"
                if placeholder in formatted_template:
                    formatted_template = formatted_template.replace(placeholder, str(value))
                
                # より一般的なパターンもサポート
                placeholder_generic = f"【{key}】"
                if placeholder_generic in formatted_template:
                    formatted_template = formatted_template.replace(placeholder_generic, str(value))
            
            return formatted_template
        except Exception as e:
            logger.error(f"Prompt formatting failed: {e}")
            raise