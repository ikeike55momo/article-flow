#!/usr/bin/env python3
"""
入出力ユーティリティ - ファイル操作とログ処理
"""

import json
import logging
import sys
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime


class FileManager:
    """ファイル管理クラス"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def save_json(self, data: Dict[str, Any], filename: str) -> Path:
        """
        JSONファイルを保存
        
        Args:
            data: 保存するデータ
            filename: ファイル名
            
        Returns:
            Path: 保存されたファイルパス
        """
        file_path = self.base_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logging.debug(f"JSON saved: {file_path}")
        return file_path
    
    def load_json(self, file_path: Path) -> Dict[str, Any]:
        """
        JSONファイルを読み込み
        
        Args:
            file_path: ファイルパス
            
        Returns:
            Dict: 読み込んだデータ
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logging.debug(f"JSON loaded: {file_path}")
        return data
    
    def save_text(self, content: str, filename: str) -> Path:
        """
        テキストファイルを保存
        
        Args:
            content: ファイル内容
            filename: ファイル名
            
        Returns:
            Path: 保存されたファイルパス
        """
        file_path = self.base_dir / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logging.debug(f"Text saved: {file_path}")
        return file_path
    
    def load_text(self, file_path: Path) -> str:
        """
        テキストファイルを読み込み
        
        Args:
            file_path: ファイルパス
            
        Returns:
            str: ファイル内容
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        logging.debug(f"Text loaded: {file_path}")
        return content


class GitHubActionsLogger:
    """GitHub Actions対応ログ出力"""
    
    @staticmethod
    def setup_logging(level: str = "INFO") -> logging.Logger:
        """
        GitHub Actions対応のログ設定
        
        Args:
            level: ログレベル
            
        Returns:
            Logger: 設定されたロガー
        """
        # ログレベル設定
        log_level = getattr(logging, level.upper(), logging.INFO)
        
        # ロガー設定
        logger = logging.getLogger()
        logger.setLevel(log_level)
        
        # ハンドラー設定（GitHub Actions形式）
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        
        # フォーマッタ（GitHub Actionsで見やすい形式）
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
        
        return logger
    
    @staticmethod
    def log_phase_start(phase_name: str):
        """フェーズ開始ログ"""
        logging.info(f"::group::{phase_name} - Starting")
        logging.info(f"Phase: {phase_name}")
        logging.info(f"Started at: {datetime.utcnow().isoformat()}Z")
    
    @staticmethod
    def log_phase_end(phase_name: str, success: bool = True, **metrics):
        """フェーズ終了ログ"""
        status = "SUCCESS" if success else "FAILED"
        logging.info(f"Phase: {phase_name} - {status}")
        
        # メトリクス出力
        for key, value in metrics.items():
            logging.info(f"{key}: {value}")
        
        logging.info(f"Completed at: {datetime.utcnow().isoformat()}Z")
        logging.info("::endgroup::")
    
    @staticmethod
    def log_error(error: Exception, context: str = ""):
        """エラーログ（GitHub Actionsアノテーション付き）"""
        error_msg = f"{context}: {str(error)}" if context else str(error)
        logging.error(f"::error::{error_msg}")
        logging.error(f"Error type: {type(error).__name__}")
        
        # スタックトレースをデバッグレベルで出力
        import traceback
        logging.debug(f"Stack trace:\n{traceback.format_exc()}")
    
    @staticmethod
    def log_warning(message: str, file: Optional[str] = None, line: Optional[int] = None):
        """警告ログ（GitHub Actionsアノテーション付き）"""
        annotation = "::warning"
        if file:
            annotation += f" file={file}"
        if line:
            annotation += f",line={line}"
        annotation += f"::{message}"
        
        logging.warning(annotation)
    
    @staticmethod
    def log_notice(message: str, title: Optional[str] = None):
        """通知ログ（GitHub Actionsアノテーション付き）"""
        annotation = "::notice"
        if title:
            annotation += f" title={title}"
        annotation += f"::{message}"
        
        logging.info(annotation)


class ProgressTracker:
    """進捗追跡"""
    
    def __init__(self, total_steps: int, description: str = "Processing"):
        self.total_steps = total_steps
        self.current_step = 0
        self.description = description
        self.start_time = datetime.utcnow()
    
    def update(self, step: int = 1, message: str = ""):
        """進捗更新"""
        self.current_step += step
        progress_pct = (self.current_step / self.total_steps) * 100
        
        elapsed = (datetime.utcnow() - self.start_time).total_seconds()
        if self.current_step > 0:
            eta = (elapsed / self.current_step) * (self.total_steps - self.current_step)
            eta_str = f"ETA: {int(eta)}s"
        else:
            eta_str = "ETA: calculating..."
        
        log_msg = f"{self.description}: {self.current_step}/{self.total_steps} ({progress_pct:.1f}%) - {eta_str}"
        if message:
            log_msg += f" - {message}"
        
        logging.info(log_msg)
    
    def finish(self, message: str = "Completed"):
        """進捗完了"""
        elapsed = (datetime.utcnow() - self.start_time).total_seconds()
        logging.info(f"{self.description}: {message} in {elapsed:.1f}s")


class ConfigManager:
    """設定管理"""
    
    @staticmethod
    def load_config(config_path: Path) -> Dict[str, Any]:
        """
        YAML設定ファイルを読み込み
        
        Args:
            config_path: 設定ファイルパス
            
        Returns:
            Dict: 設定データ
        """
        try:
            import yaml
        except ImportError:
            raise ImportError("PyYAML is required. Install with: pip install PyYAML")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        logging.debug(f"Config loaded: {config_path}")
        return config
    
    @staticmethod
    def validate_environment() -> Dict[str, bool]:
        """
        必要な環境変数をチェック
        
        Returns:
            Dict: 検証結果
        """
        import os
        
        required_vars = [
            "ANTHROPIC_API_KEY",
            # "GOOGLE_API_KEY",  # 研究時に必要
            # "GOOGLE_SERVICE_ACCOUNT_KEY"  # Drive upload時に必要
        ]
        
        results = {}
        for var in required_vars:
            results[var] = bool(os.getenv(var))
            if not results[var]:
                GitHubActionsLogger.log_warning(f"Environment variable {var} is not set")
        
        return results