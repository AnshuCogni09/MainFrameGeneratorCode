"""
Configuration module for MainFrame Code Generator.
Loads settings from config.yaml and environment variables.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration manager for the MainFrame Code Generator."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration from file and environment.
        
        Args:
            config_path: Path to configuration file. Defaults to config.yaml
        """
        self.config_path = config_path or self._get_default_config_path()
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _get_default_config_path(self) -> str:
        """Get default config file path."""
        # Try multiple locations
        possible_paths = [
            "config.yaml",
            Path(__file__).parent.parent / "config.yaml",
            Path.cwd() / "config.yaml"
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                return str(path)
        
        return "config.yaml"

    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        if Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                self._config = yaml.safe_load(f) or {}
        else:
            # Use defaults if no config file found
            self._config = self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY", ""),
                "model": "gpt-4o",
                "temperature": 0.2,
                "max_tokens": 4000
            },
            "generation": {
                "default_language": "COBOL",
                "include_comments": True,
                "validation_enabled": True
            },
            "output": {
                "default_directory": "./output",
                "file_extension_map": {
                    "cobol": ".cbl",
                    "jcl": ".jcl",
                    "db2": ".sql",
                    "cics": ".cics"
                }
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file": "mainframe_generator.log"
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'openai.model')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
                
        # Handle environment variable substitution
        if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
            env_var = value[2:-1]
            return os.getenv(env_var, default)
            
        return value

    @property
    def openai_api_key(self) -> str:
        """Get OpenAI API key."""
        return self.get("openai.api_key", "")

    @property
    def openai_model(self) -> str:
        """Get OpenAI model name."""
        return self.get("openai.model", "gpt-4o")

    @property
    def temperature(self) -> float:
        """Get temperature setting."""
        return float(self.get("openai.temperature", 0.2))

    @property
    def max_tokens(self) -> int:
        """Get max tokens setting."""
        return int(self.get("openai.max_tokens", 4000))

    @property
    def default_language(self) -> str:
        """Get default mainframe language."""
        return self.get("generation.default_language", "COBOL")

    @property
    def output_directory(self) -> str:
        """Get output directory."""
        return self.get("output.default_directory", "./output")

    @property
    def log_level(self) -> str:
        """Get logging level."""
        return self.get("logging.level", "INFO")

    @property
    def log_format(self) -> str:
        """Get logging format."""
        return self.get("logging.format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def get_file_extension(self, language: str) -> str:
        """Get file extension for a language.
        
        Args:
            language: Mainframe language name
            
        Returns:
            File extension including dot
        """
        extensions = self.get("output.file_extension_map", {})
        return extensions.get(language.lower(), ".txt")

