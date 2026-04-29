from pathlib import Path
import json
from typing import Dict, Any

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages application configuration."""

    DEFAULT_CONFIG = {
        "crdp": {
            "url": "http://localhost:32085",
            "timeout": 10,
            "ssl_verify": False,
            "default_policy": "CRDP_Protection"
        },
        "ciphertrust": {
            "url": "http://localhost",
            "port": 5696
        },
        "ui": {
            "window_width": 800,
            "window_height": 700,
            "theme": "default",
            "font_size": 10
        },
        "logging": {
            "level": "INFO",
            "file": "crdp_app.log"
        }
    }

    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration manager.

        Args:
            config_file: Path to configuration file (relative or absolute)
        """
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults.

        Returns:
            Configuration dictionary
        """
        config_path = Path(self.config_file)

        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"Configuration loaded from {config_path}")
                return config
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load config from {config_path}: {e}. Using defaults.")
                return self.DEFAULT_CONFIG.copy()
        else:
            logger.warning(f"Config file not found at {config_path}. Using default configuration.")
            return self.DEFAULT_CONFIG.copy()

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.

        Args:
            key_path: Dot-separated key path (e.g., "crdp.url")
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key_path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default

        return value
