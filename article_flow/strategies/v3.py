#!/usr/bin/env python3
"""
Prompt_v3 Strategy Implementation  
より厳密なテンプレート準拠戦略
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class PromptV3Strategy:
    """Prompt_v3用Strategy実装 - より厳密版"""
    
    def __init__(self):
        self.version = "v3"
        logger.info("Initialized Prompt V3 Strategy")
    
    def get_phase_config(self, phase: str) -> Dict[str, Any]:
        """
        各フェーズの設定を返す - v3は厳密なテンプレート準拠
        
        Args:
            phase: フェーズ名 (phase1, phase2, etc.)
            
        Returns:
            Dict: フェーズ設定
        """
        configs = {
            "phase1": {
                "prompt_file": "CHAT_01_phase1_analysis.md",
                "structured_output": True,
                "system_prompt": "You are an expert content strategist following ARTICLE-TEMPLATE-README.md specifications. Return ONLY valid JSON with no additional text, explanations, or formatting. Do not include any markdown code blocks or extra characters.",
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
                        "estimated_sections": "number",
                        "template_compliance_score": "number"  # v3独自
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
                "temperature": 0.05  # v3はより一貫性重視
            },
            "phase2": {
                "prompt_file": "CHAT_02_structure_generation.md",
                "structured_output": False,
                "system_prompt": "You are a professional content strategist creating article structures in strict compliance with ARTICLE-TEMPLATE-README.md guidelines.",
                "temperature": 0.1  # v3はより厳密
            },
            "phase3": {
                "prompt_file": "CHAT_03_content_generation_v3.md",  # v3専用ファイル
                "structured_output": False,
                "system_prompt": "You are a professional content writer creating high-quality HTML articles in strict compliance with ARTICLE-TEMPLATE-README.md specifications.",
                "temperature": 0.2  # v3はより一貫性重視
            },
            "phase4": {
                "prompt_file": "CHAT_04_factcheck.md",
                "structured_output": True,
                "system_prompt": "You are a fact-checking specialist ensuring strict compliance with ARTICLE-TEMPLATE-README.md quality standards. Return valid JSON only.",
                "expected_format": {
                    "overall_score": "number",
                    "factual_accuracy": "number",
                    "regulatory_compliance": "number", 
                    "scientific_validity": "number",
                    "template_compliance": "number",  # v3独自
                    "issues": ["object"],
                    "recommendations": ["string"]
                },
                "temperature": 0.05
            },
            "phase5": {
                "prompt_file": "CHAT_05_seo_metadata.md",
                "structured_output": True,
                "system_prompt": "You are an SEO specialist following ARTICLE-TEMPLATE-README.md SEO guidelines. Return valid JSON only.",
                "expected_format": {
                    "meta_title": "string",
                    "meta_description": "string", 
                    "keywords": ["string"],
                    "schema_markup": "object",
                    "template_seo_score": "number"  # v3独自
                },
                "temperature": 0.05
            },
            "phase6": {
                "prompt_file": "CHAT_06_finalize.md",
                "structured_output": False,
                "system_prompt": "You are finalizing a high-quality article with strict adherence to ARTICLE-TEMPLATE-README.md standards.",
                "temperature": 0.1
            }
        }
        
        return configs.get(phase, {})
    
    def format_input(self, phase: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        入力データをフェーズに応じてフォーマット - v3は厳密なバリデーション付き
        
        Args:
            phase: フェーズ名
            input_data: 生の入力データ
            
        Returns:
            Dict: フォーマット済み入力データ
        """
        # v3は入力検証を厳しく行う
        self._validate_input_data(phase, input_data)
        
        if phase == "phase1":
            # Phase 1: より厳密な入力チェック
            formatted = {
                "タイトル案": input_data.get("title", input_data.get("article_title", "")),
                "主要キーワード": input_data.get("main_keywords", ""),
                "切り口・ターゲット": input_data.get("approach_target", ""),
                "E-E-A-T要素": input_data.get("eeat_elements", ""),
                "目標文字数": input_data.get("word_count", "3200"),
                "テンプレート準拠要求": "ARTICLE-TEMPLATE-README.md に完全準拠すること"  # v3独自
            }
            
            # タイトル長チェック（30-32文字）
            title_length = len(formatted["タイトル案"])
            if not (30 <= title_length <= 32):
                logger.warning(f"Title length {title_length} not in optimal range (30-32)")
            
            return formatted
        
        elif phase == "phase2":
            # Phase 2: 構成生成 - テンプレート準拠強化
            return {
                "phase1_analysis": input_data.get("analysis", {}),
                "research_results": input_data.get("research_results", []),
                "template_requirements": "ARTICLE-TEMPLATE-README.md の構造に厳密に従うこと",
                "quality_threshold": 90  # v3はより高い品質要求
            }
        
        elif phase == "phase3":
            # Phase 3: コンテンツ生成 - 厳密なHTML要求
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
                "research_results": input_data.get("research_results", []),
                "template_compliance": "ARTICLE-TEMPLATE-README.md に100%準拠",
                "html_validation": "厳密なHTML5構造とセマンティック要素の使用",
                "quality_target": "95点以上"  # v3はより高い目標
            }
        
        elif phase == "phase4":
            # Phase 4: より厳しいファクトチェック
            return {
                "article_content": input_data.get("content", ""),
                "research_sources": input_data.get("research_results", []),
                "quality_standard": "ARTICLE-TEMPLATE-README.md 準拠品質",
                "minimum_score": 90  # v3はより厳しい基準
            }
        
        elif phase == "phase5":
            # Phase 5: より精密なSEO最適化
            return {
                "article_content": input_data.get("content", ""),
                "main_keyword": input_data.get("main_keyword", ""),
                "target_audience": input_data.get("approach_target", ""),
                "seo_standard": "ARTICLE-TEMPLATE-README.md SEO要件準拠"
            }
        
        elif phase == "phase6":
            # Phase 6: 厳密な最終チェック
            return {
                "article_content": input_data.get("content", ""),
                "seo_metadata": input_data.get("seo_metadata", {}),
                "factcheck_results": input_data.get("factcheck_results", {}),
                "final_quality_check": "ARTICLE-TEMPLATE-README.md 完全準拠確認"
            }
        
        else:
            return input_data
    
    def process_output(self, phase: str, raw_output: Any) -> Dict[str, Any]:
        """
        LLM出力を処理 - v3は厳密な品質チェック付き
        
        Args:
            phase: フェーズ名
            raw_output: LLMからの生出力
            
        Returns:
            Dict: 処理済み出力
        """
        processed = {
            "phase": phase,
            "version": self.version,
            "raw_output": raw_output,
            "template_compliance": "v3_strict"  # v3識別子
        }
        
        if phase == "phase1":
            # Phase 1: より厳しい分析結果検証
            if isinstance(raw_output, dict) and "analysis" in raw_output:
                analysis = raw_output["analysis"]
                
                # v3独自の品質チェック
                compliance_score = self._calculate_template_compliance_score(analysis)
                analysis["template_compliance_score"] = compliance_score
                
                processed.update({
                    "analysis": analysis,
                    "input_info": raw_output.get("input_info", {}),
                    "main_keyword": analysis.get("main_keyword", ""),
                    "research_queries": analysis.get("research_queries", []),
                    "quality_validated": compliance_score >= 85
                })
                
                if compliance_score < 85:
                    logger.warning(f"Phase 1 template compliance below threshold: {compliance_score}")
            else:
                logger.error("Phase 1 output format invalid for v3")
                processed["error"] = "Invalid output format"
        
        elif phase == "phase2":
            # Phase 2: 構成の厳密検証
            if isinstance(raw_output, dict) and "content" in raw_output:
                structure = raw_output["content"]
                sections = self._extract_sections_from_structure(structure)
                
                # v3独自の構造検証
                structure_quality = self._validate_article_structure(structure)
                
                processed.update({
                    "structure": structure,
                    "sections": sections,
                    "structure_quality_score": structure_quality,
                    "template_compliant": structure_quality >= 90
                })
        
        elif phase == "phase3":
            # Phase 3: HTML品質とテンプレート準拠の厳密チェック
            if isinstance(raw_output, dict) and "content" in raw_output:
                content = raw_output["content"]
                word_count = len(content.split()) if content else 0
                
                # v3独自のHTML品質チェック
                html_quality = self._validate_html_quality(content)
                template_adherence = self._check_template_adherence(content)
                
                processed.update({
                    "content": content,
                    "word_count": word_count,
                    "html_quality_score": html_quality,
                    "template_adherence_score": template_adherence,
                    "quality_passed": html_quality >= 90 and template_adherence >= 90
                })
        
        elif phase == "phase4":
            # Phase 4: より厳しいファクトチェック評価
            if isinstance(raw_output, dict):
                overall_score = raw_output.get("overall_score", 0)
                template_compliance = raw_output.get("template_compliance", 0)
                
                processed.update({
                    "factcheck_results": raw_output,
                    "overall_score": overall_score,
                    "template_compliance_score": template_compliance,
                    "passed": overall_score >= 90 and template_compliance >= 85,  # v3はより厳しい
                    "v3_quality_standard": True
                })
        
        elif phase == "phase5":
            # Phase 5: SEO結果の厳密評価
            if isinstance(raw_output, dict):
                seo_score = raw_output.get("template_seo_score", 0)
                
                processed.update({
                    "seo_metadata": raw_output,
                    "seo_quality_score": seo_score,
                    "seo_compliant": seo_score >= 90
                })
        
        elif phase == "phase6":
            # Phase 6: 最終品質保証
            if isinstance(raw_output, dict) and "content" in raw_output:
                final_quality = self._final_quality_assessment(raw_output["content"])
                
                processed.update({
                    "final_content": raw_output["content"], 
                    "final_quality_score": final_quality,
                    "status": "completed" if final_quality >= 95 else "needs_revision",
                    "v3_certified": final_quality >= 95
                })
        
        return processed
    
    def _validate_input_data(self, phase: str, input_data: Dict[str, Any]):
        """v3用の厳密な入力データ検証"""
        if phase == "phase1":
            required_fields = ["title", "main_keywords", "approach_target", "eeat_elements"]
            for field in required_fields:
                if not input_data.get(field):
                    raise ValueError(f"Required field '{field}' is missing or empty")
    
    def _calculate_template_compliance_score(self, analysis: Dict[str, Any]) -> float:
        """テンプレート準拠スコア計算"""
        score = 85.0  # ベーススコア
        
        # 必要な要素がある場合スコア加算
        if analysis.get("main_keyword"):
            score += 2
        if len(analysis.get("related_keywords", [])) >= 5:
            score += 3
        if analysis.get("research_queries") and len(analysis["research_queries"]) >= 15:
            score += 5
        if analysis.get("key_points") and len(analysis["key_points"]) >= 3:
            score += 5
        
        return min(score, 100.0)
    
    def _validate_article_structure(self, structure: str) -> float:
        """記事構造の品質スコア算出"""
        score = 80.0
        
        # セクション数チェック
        sections = structure.count('##')
        if 5 <= sections <= 7:
            score += 10
        
        # FAQ含有チェック
        if 'FAQ' in structure or 'よくある質問' in structure:
            score += 5
        
        # まとめセクション存在チェック
        if 'まとめ' in structure or 'おわりに' in structure:
            score += 5
        
        return min(score, 100.0)
    
    def _validate_html_quality(self, content: str) -> float:
        """HTML品質スコア算出"""
        score = 85.0
        
        # 必要なHTML要素チェック
        if '<div class="article-content">' in content:
            score += 5
        if '<h2' in content and '</h2>' in content:
            score += 3
        if '<figure' in content or '<img' in content:
            score += 2
        if 'class="article-' in content:
            score += 5
        
        return min(score, 100.0)
    
    def _check_template_adherence(self, content: str) -> float:
        """テンプレート準拠度チェック"""
        score = 85.0
        
        # ARTICLE-TEMPLATE-README.md 準拠要素チェック
        template_elements = [
            'article-content',
            'article-lead-text',
            'article-toc',
            'article-faq-section'
        ]
        
        for element in template_elements:
            if element in content:
                score += 3.75  # 15点を4分割
        
        return min(score, 100.0)
    
    def _final_quality_assessment(self, content: str) -> float:
        """最終品質評価"""
        score = 90.0
        
        # 基本品質チェック
        if len(content) > 3000:
            score += 2
        if content.count('<h2>') >= 4:
            score += 2
        if 'E-E-A-T' in content or '専門性' in content:
            score += 3
        if 'class="article-' in content:
            score += 3
        
        return min(score, 100.0)
    
    def _extract_sections_from_structure(self, structure_text: str) -> list:
        """構成テキストからセクションを抽出 - v3版はより厳密"""
        sections = []
        lines = structure_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('## ') and not line.startswith('### '):
                section_title = line.replace('## ', '').strip()
                if section_title and section_title not in sections:
                    sections.append(section_title)
        
        # v3は最低5セクション要求
        if len(sections) < 5:
            logger.warning(f"v3 requires at least 5 sections, got {len(sections)}")
        
        return sections