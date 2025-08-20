#!/usr/bin/env python3
"""
共通パイプライン - Phase処理の骨格
"""

import json
import logging
from typing import Dict, Any, Optional, List, Protocol
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod

from .llm import LLMProvider, PromptLoader
from .image import ImageProvider
from .io_utils import FileManager

logger = logging.getLogger(__name__)


class Strategy(Protocol):
    """Strategy pattern interface"""
    
    def get_phase_config(self, phase: str) -> Dict[str, Any]:
        """フェーズ設定を取得"""
        ...
    
    def format_input(self, phase: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """入力データをフォーマット"""
        ...
    
    def process_output(self, phase: str, raw_output: Any) -> Dict[str, Any]:
        """出力データを処理"""
        ...


class ArticlePipeline:
    """記事生成パイプライン"""
    
    def __init__(
        self,
        strategy: Strategy,
        prompt_dir: Path,
        output_dir: Path,
        config: Dict[str, Any]
    ):
        self.strategy = strategy
        self.prompt_dir = prompt_dir
        self.output_dir = output_dir
        self.config = config
        
        # コアコンポーネント初期化
        self.llm = LLMProvider()
        self.prompt_loader = PromptLoader()
        self.image_provider = ImageProvider() if config.get("enable_image_generation") else None
        self.file_manager = FileManager(output_dir)
        
        logger.info(f"Pipeline initialized with strategy: {strategy.__class__.__name__}")
    
    def run_full_pipeline(self, input_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        全フェーズを実行
        
        Args:
            input_params: 入力パラメータ
            
        Returns:
            Dict: 最終結果
        """
        logger.info("Starting full article generation pipeline")
        
        try:
            # Phase 1: Request Analysis
            phase1_result = self.run_phase("phase1", input_params)
            
            # Phase 2: Research (if needed)
            phase2_result = None
            if self.config.get("enable_research", True):
                phase2_result = self.run_phase("phase2", phase1_result)
            
            # Phase 3: Structure Generation
            structure_input = phase2_result or phase1_result
            phase3_result = self.run_phase("phase3", structure_input)
            
            # Phase 4: Content Generation
            phase4_result = self.run_phase("phase4", phase3_result)
            
            # Phase 5: Fact Check
            phase5_result = self.run_phase("phase5", phase4_result)
            
            # Phase 6: SEO & Finalization
            phase6_result = self.run_phase("phase6", phase5_result)
            
            # Image Generation (if enabled)
            if self.image_provider and self.config.get("enable_image_generation"):
                image_result = self.generate_images(phase6_result)
                phase6_result["images"] = image_result
            
            # Final summary
            final_result = {
                "article_id": input_params.get("article_id"),
                "status": "completed",
                "phases": {
                    "phase1": phase1_result,
                    "phase2": phase2_result,
                    "phase3": phase3_result,
                    "phase4": phase4_result,
                    "phase5": phase5_result,
                    "phase6": phase6_result
                },
                "completed_at": datetime.utcnow().isoformat()
            }
            
            # Save final result
            self.file_manager.save_json(final_result, "final_result.json")
            
            logger.info("Full pipeline completed successfully")
            return final_result
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise
    
    def run_phase(self, phase: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        指定されたフェーズを実行
        
        Args:
            phase: フェーズ名 (phase1, phase2, etc.)
            input_data: 入力データ
            
        Returns:
            Dict: フェーズの出力結果
        """
        logger.info(f"Running {phase}")
        
        try:
            # Strategy から設定を取得
            phase_config = self.strategy.get_phase_config(phase)
            
            # 入力データをフォーマット
            formatted_input = self.strategy.format_input(phase, input_data)
            
            # プロンプトを読み込み
            prompt_filename = phase_config.get("prompt_file")
            if not prompt_filename:
                raise ValueError(f"No prompt file specified for {phase}")
            
            prompt_template = self.prompt_loader.load_prompt(self.prompt_dir, prompt_filename)
            
            # プロンプトに変数を代入
            formatted_prompt = self.prompt_loader.format_prompt(prompt_template, **formatted_input)
            
            # LLM API呼び出し
            if phase_config.get("structured_output"):
                result = self.llm.generate_with_structured_output(
                    prompt=formatted_prompt,
                    system_prompt=phase_config.get("system_prompt", ""),
                    expected_format=phase_config.get("expected_format"),
                    temperature=phase_config.get("temperature", 0.1)
                )
            else:
                result_text = self.llm.generate_text(
                    prompt=formatted_prompt,
                    system_prompt=phase_config.get("system_prompt", ""),
                    temperature=phase_config.get("temperature", 0.1)
                )
                result = {"content": result_text}
            
            # 出力を処理
            processed_result = self.strategy.process_output(phase, result)
            
            # ファイルに保存
            output_filename = f"{phase}_output.json"
            self.file_manager.save_json(processed_result, output_filename)
            
            logger.info(f"{phase} completed successfully")
            return processed_result
            
        except Exception as e:
            logger.error(f"{phase} failed: {e}")
            raise
    
    def generate_images(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        記事用画像を生成
        
        Args:
            article_data: 記事データ
            
        Returns:
            Dict: 画像生成結果
        """
        if not self.image_provider:
            logger.warning("Image provider not available")
            return {"status": "skipped", "reason": "Image provider not enabled"}
        
        logger.info("Starting image generation")
        
        try:
            # 記事から画像プロンプトを生成
            article_content = article_data.get("content", "")
            sections = article_data.get("sections", [])
            style_guide = self.config.get("image_style", {})
            
            image_prompts = self.image_provider.create_image_prompts(
                article_content, sections, style_guide
            )
            
            # 画像生成実行
            image_results = self.image_provider.generate_images(
                prompts=image_prompts,
                output_dir=self.output_dir / "images",
                style=style_guide.get("style", "article"),
                size=style_guide.get("size", "1024x1024")
            )
            
            # メタデータ作成
            from .image import ImageMetadata
            metadata = ImageMetadata.create_metadata(
                image_results, article_data.get("article_id", "unknown")
            )
            
            logger.info(f"Image generation completed: {metadata['success_rate']:.1%} success rate")
            return metadata
            
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return {"status": "failed", "error": str(e)}


class PhaseRunner:
    """個別フェーズ実行用クラス"""
    
    def __init__(self, pipeline: ArticlePipeline):
        self.pipeline = pipeline
    
    def run_single_phase(
        self,
        phase: str,
        input_file: Path,
        output_file: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        単一フェーズを実行
        
        Args:
            phase: フェーズ名
            input_file: 入力ファイルパス
            output_file: 出力ファイルパス (Noneの場合は自動設定)
            
        Returns:
            Dict: 実行結果
        """
        # 入力データ読み込み
        input_data = self.pipeline.file_manager.load_json(input_file)
        
        # フェーズ実行
        result = self.pipeline.run_phase(phase, input_data)
        
        # 出力ファイル保存
        if output_file:
            self.pipeline.file_manager.save_json(result, output_file)
        
        return result