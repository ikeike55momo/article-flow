#!/usr/bin/env python3
"""
Prompt_v2 Strategy Implementation
柔軟なプロンプト戦略
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class PromptV2Strategy:
    """Prompt_v2用Strategy実装"""
    
    def __init__(self):
        self.version = "v2"
        logger.info("Initialized Prompt V2 Strategy")
    
    def get_phase_config(self, phase: str) -> Dict[str, Any]:
        """
        各フェーズの設定を返す
        
        Args:
            phase: フェーズ名 (phase1, phase2, etc.)
            
        Returns:
            Dict: フェーズ設定
        """
        configs = {
            "phase1": {
                "prompt_file": "CHAT_01_phase1_analysis.md",
                "structured_output": True,
                "system_prompt": "You are an expert content strategist. Return ONLY valid JSON with no additional text, explanations, or formatting. Do not include any markdown code blocks or extra characters.",
                "expected_format": {
                    "analysis": {
                        "main_keyword": "string",
                        "related_keywords": ["string"],
                        "search_intent": "string",
                        "content_type": "string",
                        "tone": "string",
                        "key_points": ["string"],
                        "research_queries": ["string"],
                        "competitor_analysis_needed": "boolean",
                        "local_seo_focus": "boolean",
                        "estimated_sections": "number"
                    },
                    "input_info": {
                        "title": "string",
                        "main_keywords": "string",
                        "approach_target": "string",
                        "eeat_elements": "string",
                        "word_count": "string"
                    },
                    "processed_at": "string",
                    "workflow_version": "string"
                },
                "temperature": 0.1
            },
            "phase2": {
                "prompt_file": "CHAT_02_structure_generation.md",
                "structured_output": False,
                "system_prompt": "You are a professional content strategist creating article structures.",
                "temperature": 0.2
            },
            "phase3": {
                "prompt_file": "CHAT_03_content_generation_v2.md",
                "structured_output": False,
                "system_prompt": "You are a professional content writer creating high-quality HTML articles.",
                "temperature": 0.3
            },
            "phase4": {
                "prompt_file": "CHAT_04_factcheck.md",
                "structured_output": True,
                "system_prompt": "You are a fact-checking specialist. Return valid JSON only.",
                "expected_format": {
                    "overall_score": "number",
                    "factual_accuracy": "number",
                    "regulatory_compliance": "number",
                    "scientific_validity": "number",
                    "issues": ["object"],
                    "recommendations": ["string"]
                },
                "temperature": 0.1
            },
            "phase5": {
                "prompt_file": "CHAT_05_seo_metadata.md",
                "structured_output": True,
                "system_prompt": "You are an SEO specialist. Return valid JSON only.",
                "expected_format": {
                    "meta_title": "string",
                    "meta_description": "string",
                    "keywords": ["string"],
                    "schema_markup": "object"
                },
                "temperature": 0.1
            },
            "phase6": {
                "prompt_file": "CHAT_06_finalize.md",
                "structured_output": False,
                "system_prompt": "You are finalizing a high-quality article.",
                "temperature": 0.2
            }
        }
        
        return configs.get(phase, {})
    
    def format_input(self, phase: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        入力データをフェーズに応じてフォーマット
        
        Args:
            phase: フェーズ名
            input_data: 生の入力データ
            
        Returns:
            Dict: フォーマット済み入力データ
        """
        if phase == "phase1":
            # Phase 1: リクエスト分析用の入力
            return {
                "タイトル案": input_data.get("title", input_data.get("article_title", "")),
                "主要キーワード": input_data.get("main_keywords", ""),
                "切り口・ターゲット": input_data.get("approach_target", ""),
                "E-E-A-T要素": input_data.get("eeat_elements", ""),
                "目標文字数": input_data.get("word_count", "3200")
            }
        
        elif phase == "phase2":
            # Phase 2: 構成生成用の入力
            return {
                "phase1_analysis": input_data.get("analysis", {}),
                "research_results": input_data.get("research_results", [])
            }
        
        elif phase == "phase3":
            # Phase 3: コンテンツ生成用の入力
            return {
                "記事タイトル": input_data.get("title", ""),
                "基本情報": {
                    "title": input_data.get("title", ""),
                    "main_keywords": input_data.get("main_keywords", ""),
                    "approach_target": input_data.get("approach_target", ""),
                    "eeat_elements": input_data.get("eeat_elements", ""),
                    "word_count": input_data.get("word_count", "3200")
                },
                "phase1_analysis": input_data.get("analysis", {}),
                "article_structure": input_data.get("structure", ""),
                "research_results": input_data.get("research_results", [])
            }
        
        elif phase == "phase4":
            # Phase 4: ファクトチェック用の入力
            return {
                "article_content": input_data.get("content", ""),
                "research_sources": input_data.get("research_results", [])
            }
        
        elif phase == "phase5":
            # Phase 5: SEO用の入力
            return {
                "article_content": input_data.get("content", ""),
                "main_keyword": input_data.get("main_keyword", ""),
                "target_audience": input_data.get("approach_target", "")
            }
        
        elif phase == "phase6":
            # Phase 6: 最終調整用の入力
            return {
                "article_content": input_data.get("content", ""),
                "seo_metadata": input_data.get("seo_metadata", {}),
                "factcheck_results": input_data.get("factcheck_results", {})
            }
        
        else:
            # デフォルトはそのまま返す
            return input_data
    
    def process_output(self, phase: str, raw_output: Any) -> Dict[str, Any]:
        """
        LLM出力を処理してフェーズ固有のフォーマットに変換
        
        Args:
            phase: フェーズ名
            raw_output: LLMからの生出力
            
        Returns:
            Dict: 処理済み出力
        """
        processed = {
            "phase": phase,
            "version": self.version,
            "raw_output": raw_output
        }
        
        if phase == "phase1":
            # Phase 1: 分析結果の処理
            if isinstance(raw_output, dict) and "analysis" in raw_output:
                processed.update({
                    "analysis": raw_output["analysis"],
                    "input_info": raw_output.get("input_info", {}),
                    "main_keyword": raw_output["analysis"].get("main_keyword", ""),
                    "research_queries": raw_output["analysis"].get("research_queries", [])
                })
            else:
                logger.warning("Phase 1 output format unexpected")
        
        elif phase == "phase2":
            # Phase 2: 構成の処理
            if isinstance(raw_output, dict) and "content" in raw_output:
                processed.update({
                    "structure": raw_output["content"],
                    "sections": self._extract_sections_from_structure(raw_output["content"])
                })
        
        elif phase == "phase3":
            # Phase 3: コンテンツの処理
            if isinstance(raw_output, dict) and "content" in raw_output:
                processed.update({
                    "content": raw_output["content"],
                    "word_count": len(raw_output["content"].split()) if raw_output["content"] else 0
                })
        
        elif phase == "phase4":
            # Phase 4: ファクトチェック結果の処理
            if isinstance(raw_output, dict):
                processed.update({
                    "factcheck_results": raw_output,
                    "overall_score": raw_output.get("overall_score", 0),
                    "passed": raw_output.get("overall_score", 0) >= 85
                })
        
        elif phase == "phase5":
            # Phase 5: SEO結果の処理
            if isinstance(raw_output, dict):
                processed.update({
                    "seo_metadata": raw_output
                })
        
        elif phase == "phase6":
            # Phase 6: 最終結果の処理
            if isinstance(raw_output, dict) and "content" in raw_output:
                processed.update({
                    "final_content": raw_output["content"],
                    "status": "completed"
                })
        
        return processed
    
    def _extract_sections_from_structure(self, structure_text: str) -> list:
        """構成テキストからセクションを抽出"""
        sections = []
        lines = structure_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('## ') or line.startswith('### '):
                section_title = line.replace('## ', '').replace('### ', '')
                if section_title and section_title not in sections:
                    sections.append(section_title)
        
        return sections