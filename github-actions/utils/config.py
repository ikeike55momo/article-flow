"""Configuration management utilities"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
from .file_utils import read_yaml, read_json


class Config:
    """Configuration manager for article generation"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path("/mnt/c/article-flow")
        self._config_cache = {}
        
    def load_config(self, config_name: str) -> Dict[str, Any]:
        """Load configuration file"""
        if config_name in self._config_cache:
            return self._config_cache[config_name]
        
        # Try different paths
        config_paths = [
            self.base_path / "config" / f"{config_name}.yaml",
            self.base_path / "config" / f"{config_name}.yml",
            Path("config") / f"{config_name}.yaml",
            Path("../config") / f"{config_name}.yaml"
        ]
        
        for path in config_paths:
            if path.exists():
                config = read_yaml(path)
                self._config_cache[config_name] = config
                return config
        
        raise FileNotFoundError(f"Config file '{config_name}' not found")
    
    @property
    def requirements(self) -> Dict[str, Any]:
        """Get requirements configuration"""
        return self.load_config("requirements")
    
    @property
    def templates(self) -> Dict[str, Any]:
        """Get templates configuration"""
        return self.load_config("templates")
    
    @property
    def factcheck_rules(self) -> Dict[str, Any]:
        """Get factcheck rules"""
        return self.load_config("factcheck_rules")
    
    @property
    def workflow(self) -> Dict[str, Any]:
        """Get workflow configuration"""
        return self.load_config("workflow")
    
    @property
    def wordpress_compatibility(self) -> Dict[str, Any]:
        """Get WordPress compatibility rules"""
        return self.load_config("wordpress-compatibility")


def get_env_var(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """Get environment variable with validation"""
    value = os.environ.get(name, default)
    
    if required and not value:
        raise ValueError(f"Required environment variable '{name}' not set")
    
    return value


def get_api_keys() -> Dict[str, str]:
    """Get all required API keys"""
    return {
        "anthropic": get_env_var("ANTHROPIC_API_KEY", required=True),
        "openai": get_env_var("OPENAI_API_KEY", required=True),
        "bing_search": get_env_var("BING_SEARCH_KEY", required=True),
        "google_drive": get_env_var("GOOGLE_DRIVE_CREDENTIALS"),
        "stability": get_env_var("STABILITY_API_KEY"),
        "slack_webhook": get_env_var("SLACK_WEBHOOK")
    }


def validate_environment():
    """Validate that all required environment variables are set"""
    required_vars = [
        "ANTHROPIC_API_KEY",
        "OPENAI_API_KEY", 
        "BING_SEARCH_KEY"
    ]
    
    missing = []
    for var in required_vars:
        if not os.environ.get(var):
            missing.append(var)
    
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")