"""File handling utilities"""
import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Union
import logging

logger = logging.getLogger(__name__)


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure directory exists"""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Read JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(data: Dict[str, Any], file_path: Union[str, Path], indent: int = 2) -> None:
    """Write JSON file"""
    ensure_dir(Path(file_path).parent)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
    logger.info(f"Wrote JSON to {file_path}")


def read_yaml(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Read YAML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def write_yaml(data: Dict[str, Any], file_path: Union[str, Path]) -> None:
    """Write YAML file"""
    ensure_dir(Path(file_path).parent)
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    logger.info(f"Wrote YAML to {file_path}")


def read_text(file_path: Union[str, Path]) -> str:
    """Read text file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_text(content: str, file_path: Union[str, Path]) -> None:
    """Write text file"""
    ensure_dir(Path(file_path).parent)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.info(f"Wrote text to {file_path}")


def read_prompt(prompt_name: str) -> str:
    """Read prompt template from prompts directory"""
    # Try multiple possible locations
    possible_paths = [
        Path("prompts") / f"{prompt_name}.md",
        Path("..") / "prompts" / f"{prompt_name}.md",
        Path("/mnt/c/article-flow/prompts") / f"{prompt_name}.md"
    ]
    
    for path in possible_paths:
        if path.exists():
            return read_text(path)
    
    raise FileNotFoundError(f"Prompt template '{prompt_name}' not found in any of: {possible_paths}")


def get_output_path(output_dir: Union[str, Path], filename: str) -> Path:
    """Get output file path"""
    return ensure_dir(output_dir) / filename