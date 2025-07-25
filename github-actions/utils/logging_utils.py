"""Logging configuration and utilities"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logging(
    name: str,
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """Setup logging configuration"""
    
    # Default format for GitHub Actions
    if format_string is None:
        format_string = "::%(levelname)s file=%(filename)s,line=%(lineno)d::%(message)s"
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)
    
    return logger


def log_phase_start(logger: logging.Logger, phase: str, metadata: dict = None):
    """Log the start of a phase"""
    logger.info(f"Starting phase: {phase}")
    if metadata:
        logger.info(f"Phase metadata: {metadata}")
    
    # GitHub Actions group
    print(f"::group::{phase}")


def log_phase_end(logger: logging.Logger, phase: str, success: bool = True):
    """Log the end of a phase"""
    status = "completed successfully" if success else "failed"
    logger.info(f"Phase {phase} {status}")
    
    # End GitHub Actions group
    print("::endgroup::")


def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """Log error with context"""
    logger.error(f"Error in {context}: {type(error).__name__}: {str(error)}")
    logger.debug("Full traceback:", exc_info=True)
    
    # GitHub Actions error annotation
    print(f"::error::{context}: {str(error)}")


def log_warning(logger: logging.Logger, message: str):
    """Log warning"""
    logger.warning(message)
    print(f"::warning::{message}")


def log_metric(logger: logging.Logger, metric_name: str, value: any, unit: str = ""):
    """Log a metric value"""
    unit_str = f" {unit}" if unit else ""
    logger.info(f"Metric - {metric_name}: {value}{unit_str}")
    
    # Output as GitHub Actions output
    print(f"::set-output name={metric_name}::{value}")