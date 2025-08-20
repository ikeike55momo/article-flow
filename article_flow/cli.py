#!/usr/bin/env python3
"""
Article Flow CLI - メインエントリーポイント
Strategy パターンによる v2/v3 対応
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# 相対インポート
from .core.pipeline import ArticlePipeline, PhaseRunner
from .core.io_utils import GitHubActionsLogger, FileManager, ConfigManager
from .strategies.v2 import PromptV2Strategy
from .strategies.v3 import PromptV3Strategy


def setup_logging(level: str = "INFO") -> logging.Logger:
    """ログ設定"""
    return GitHubActionsLogger.setup_logging(level)


def load_strategy(profile: str):
    """Strategy を読み込み"""
    if profile == "v2":
        return PromptV2Strategy()
    elif profile == "v3":
        return PromptV3Strategy()
    else:
        raise ValueError(f"Unknown profile: {profile}. Supported: v2, v3")


def load_config(config_path: Path) -> Dict[str, Any]:
    """設定ファイルを読み込み"""
    if config_path.exists():
        return ConfigManager.load_config(config_path)
    else:
        # デフォルト設定
        return {
            "enable_image_generation": True,
            "enable_research": False,
            "quality": {"minimum_scores": {"overall": 85}}
        }


def create_input_params(args) -> Dict[str, Any]:
    """CLI引数から入力パラメータを作成"""
    from datetime import datetime
    import uuid
    
    # 記事IDを生成
    if args.article_id:
        article_id = args.article_id
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_title = args.title.replace(' ', '_')[:30] if args.title else "article"
        article_id = f"{timestamp}_{clean_title}"
    
    return {
        "article_id": article_id,
        "title": args.title,
        "main_keywords": args.main_keywords,
        "approach_target": args.approach_target,
        "eeat_elements": args.eeat_elements,
        "word_count": str(args.word_count),
        "created_at": datetime.now().isoformat(),
        "profile": args.profile
    }


def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(
        description="Article Flow - AI-powered article generation system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # v2 profile で記事生成
  python -m article_flow.cli --profile v2 \\
    --title "セルフジェルネイルの基本テクニック" \\
    --main-keywords "ジェルネイル,セルフ,初心者" \\
    --approach-target "20-30代女性、ネイル初心者" \\
    --eeat-elements "専門家監修、実体験based" \\
    --prompt-dir Prompt_v2 \\
    --output-dir output/v2_test

  # v3 profile で厳密な記事生成
  python -m article_flow.cli --profile v3 \\
    --title "健康的なダイエット習慣の作り方" \\
    --main-keywords "ダイエット,習慣,健康" \\
    --approach-target "30-40代女性、健康志向" \\
    --eeat-elements "管理栄養士監修、科学的根拠" \\
    --prompt-dir Prompt_v3 \\
    --output-dir output/v3_test \\
    --config article_flow/config/v3.yaml

  # 単一フェーズ実行
  python -m article_flow.cli --profile v2 --phase phase1 \\
    --input-file input_params.json \\
    --output-dir output/phase1_only
        """
    )
    
    # 基本オプション
    parser.add_argument("--profile", 
                       required=True, 
                       choices=["v2", "v3"],
                       help="Strategy profile (v2: flexible, v3: strict)")
    
    parser.add_argument("--prompt-dir",
                       type=Path,
                       required=True,
                       help="Prompt directory (e.g., Prompt_v2, Prompt_v3)")
    
    parser.add_argument("--output-dir",
                       type=Path,
                       required=True,
                       help="Output directory")
    
    parser.add_argument("--config",
                       type=Path,
                       help="Config file (YAML)")
    
    # 実行モード
    parser.add_argument("--phase",
                       choices=["phase1", "phase2", "phase3", "phase4", "phase5", "phase6"],
                       help="Run single phase only")
    
    parser.add_argument("--full-pipeline",
                       action="store_true",
                       default=True,
                       help="Run full pipeline (default)")
    
    # 記事パラメータ
    parser.add_argument("--title",
                       help="記事タイトル (30-32文字推奨)")
    
    parser.add_argument("--main-keywords",
                       help="主要キーワード (カンマ区切り、最大3語)")
    
    parser.add_argument("--approach-target", 
                       help="切り口・ターゲット")
    
    parser.add_argument("--eeat-elements",
                       help="E-E-A-T要素")
    
    parser.add_argument("--word-count",
                       type=int,
                       default=3200,
                       help="目標文字数 (default: 3200)")
    
    parser.add_argument("--article-id",
                       help="記事ID (未指定時は自動生成)")
    
    # 単一フェーズ実行用
    parser.add_argument("--input-file",
                       type=Path,
                       help="Input JSON file (for single phase execution)")
    
    parser.add_argument("--output-file",
                       type=Path,
                       help="Output file (for single phase execution)")
    
    # オプション
    parser.add_argument("--enable-image-generation",
                       action="store_true",
                       default=True,
                       help="Enable image generation")
    
    parser.add_argument("--log-level",
                       default="INFO",
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="Log level")
    
    parser.add_argument("--dry-run",
                       action="store_true",
                       help="Dry run (validate inputs only)")
    
    args = parser.parse_args()
    
    # ログ設定
    logger = setup_logging(args.log_level)
    
    try:
        GitHubActionsLogger.log_phase_start("Article Flow CLI")
        
        # 基本情報表示
        logger.info(f"Article Flow CLI - Profile: {args.profile}")
        logger.info(f"Prompt directory: {args.prompt_dir}")
        logger.info(f"Output directory: {args.output_dir}")
        
        # プロンプトディレクトリ存在確認
        if not args.prompt_dir.exists():
            raise FileNotFoundError(f"Prompt directory not found: {args.prompt_dir}")
        
        # 出力ディレクトリ作成
        args.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 設定読み込み
        if args.config:
            config = load_config(args.config)
            logger.info(f"Config loaded from: {args.config}")
        else:
            # デフォルト設定ファイルを試す
            default_config_path = Path(f"article_flow/config/{args.profile}.yaml")
            if default_config_path.exists():
                config = load_config(default_config_path)
                logger.info(f"Default config loaded: {default_config_path}")
            else:
                config = {"enable_image_generation": args.enable_image_generation}
                logger.info("Using minimal config")
        
        # Strategy読み込み
        strategy = load_strategy(args.profile)
        logger.info(f"Strategy loaded: {strategy.__class__.__name__}")
        
        # パイプライン初期化
        pipeline = ArticlePipeline(
            strategy=strategy,
            prompt_dir=args.prompt_dir,
            output_dir=args.output_dir,
            config=config
        )
        
        # Dry run チェック
        if args.dry_run:
            logger.info("Dry run mode - validating inputs only")
            if args.phase:
                logger.info(f"Would run phase: {args.phase}")
            else:
                logger.info("Would run full pipeline")
            
            # 入力パラメータ検証
            if not args.phase or args.phase == "phase1":
                if not all([args.title, args.main_keywords, args.approach_target, args.eeat_elements]):
                    logger.warning("Some required parameters are missing")
            
            logger.info("Dry run completed successfully")
            return
        
        # 実行モード判定
        if args.phase:
            # 単一フェーズ実行
            logger.info(f"Running single phase: {args.phase}")
            
            if not args.input_file:
                # パラメータから入力データ作成
                input_data = create_input_params(args)
            else:
                # ファイルから入力データ読み込み
                file_manager = FileManager(args.output_dir)
                input_data = file_manager.load_json(args.input_file)
            
            # フェーズ実行
            phase_runner = PhaseRunner(pipeline)
            result = phase_runner.run_single_phase(
                args.phase, 
                input_data if isinstance(input_data, Path) else None,
                args.output_file
            )
            
            logger.info(f"Phase {args.phase} completed successfully")
            
        else:
            # フルパイプライン実行
            logger.info("Running full pipeline")
            
            # 必須パラメータチェック
            if not all([args.title, args.main_keywords, args.approach_target, args.eeat_elements]):
                parser.error("Full pipeline requires: --title, --main-keywords, --approach-target, --eeat-elements")
            
            # 入力パラメータ作成
            input_params = create_input_params(args)
            
            # パイプライン実行
            result = pipeline.run_full_pipeline(input_params)
            
            logger.info("Full pipeline completed successfully")
            
            # 結果サマリー表示
            if "phases" in result:
                for phase_name, phase_result in result["phases"].items():
                    if phase_result:
                        status = "✓" if not phase_result.get("error") else "✗"
                        logger.info(f"{status} {phase_name}: {phase_result.get('status', 'completed')}")
        
        GitHubActionsLogger.log_phase_end("Article Flow CLI", success=True)
        
    except Exception as e:
        GitHubActionsLogger.log_error(e, "CLI execution")
        GitHubActionsLogger.log_phase_end("Article Flow CLI", success=False)
        sys.exit(1)


if __name__ == "__main__":
    main()