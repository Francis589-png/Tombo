"""
TOMBO Config Library - Configuration file parsing and management
Support for INI, YAML-like, and JSON configuration formats.
"""

from typing import Dict, Any, List, Optional


class ConfigParser:
    """Parse configuration files."""
    
    def __init__(self):
        """Initialize parser."""
        self.data: Dict[str, Any] = {}
    
    def parse_ini(self, content: str) -> Dict:
        """Parse INI format.
        
        Args:
            content: INI file content
            
        Returns:
            Parsed configuration
        """
        config = {}
        current_section = "DEFAULT"
        config[current_section] = {}
        
        for line in content.split('\n'):
            line = line.strip()
            
            if not line or line.startswith(';') or line.startswith('#'):
                continue
            
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1].strip()
                config[current_section] = {}
            elif '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Parse value type
                if value.lower() in ('true', 'false'):
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                elif '.' in value and value.replace('.', '').isdigit():
                    value = float(value)
                
                config[current_section][key] = value
        
        self.data = config
        return config
    
    def parse_yaml_like(self, content: str) -> Dict:
        """Parse YAML-like format.
        
        Args:
            content: YAML-like content
            
        Returns:
            Parsed configuration
        """
        config = {}
        stack = [config]
        
        for line in content.split('\n'):
            if not line.strip() or line.strip().startswith('#'):
                continue
            
            indent = len(line) - len(line.lstrip())
            line = line.strip()
            
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Parse value
                if not value:
                    value = {}
                    stack[-1][key] = value
                    stack.append(value)
                else:
                    if value.lower() in ('true', 'false'):
                        value = value.lower() == 'true'
                    elif value.isdigit():
                        value = int(value)
                    elif value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    
                    stack[-1][key] = value
        
        self.data = config
        return config
    
    def parse_json_like(self, content: str) -> Dict:
        """Parse JSON-like format.
        
        Args:
            content: JSON-like content
            
        Returns:
            Parsed configuration
        """
        import json
        
        try:
            config = json.loads(content)
            self.data = config
            return config
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")


class Configuration:
    """Configuration manager."""
    
    def __init__(self):
        """Initialize configuration."""
        self.config: Dict[str, Any] = {}
        self.overrides: Dict[str, Any] = {}
    
    def load_ini(self, filename: str):
        """Load INI configuration.
        
        Args:
            filename: INI file path
        """
        with open(filename, 'r') as f:
            content = f.read()
        
        parser = ConfigParser()
        self.config = parser.parse_ini(content)
    
    def load_yaml(self, filename: str):
        """Load YAML-like configuration.
        
        Args:
            filename: YAML file path
        """
        with open(filename, 'r') as f:
            content = f.read()
        
        parser = ConfigParser()
        self.config = parser.parse_yaml_like(content)
    
    def load_json(self, filename: str):
        """Load JSON configuration.
        
        Args:
            filename: JSON file path
        """
        with open(filename, 'r') as f:
            content = f.read()
        
        parser = ConfigParser()
        self.config = parser.parse_json_like(content)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key (dot notation: section.key)
            default: Default value
            
        Returns:
            Configuration value
        """
        # Check overrides first
        if key in self.overrides:
            return self.overrides[key]
        
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """Set configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.overrides[key] = value
    
    def has(self, key: str) -> bool:
        """Check if configuration key exists.
        
        Args:
            key: Configuration key
            
        Returns:
            True if exists
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return False
        
        return True
    
    def get_section(self, section: str) -> Dict:
        """Get configuration section.
        
        Args:
            section: Section name
            
        Returns:
            Section configuration
        """
        return self.config.get(section, {})
    
    def to_dict(self) -> Dict:
        """Convert configuration to dictionary."""
        return {**self.config, **self.overrides}
    
    def to_ini(self) -> str:
        """Export as INI format."""
        lines = []
        
        for section, values in self.config.items():
            if isinstance(values, dict):
                lines.append(f"[{section}]")
                for key, value in values.items():
                    lines.append(f"{key} = {value}")
                lines.append("")
        
        return "\n".join(lines)


class EnvironmentConfig:
    """Load configuration from environment variables."""
    
    @staticmethod
    def get(key: str, default: str = None) -> str:
        """Get environment variable.
        
        Args:
            key: Environment variable name
            default: Default value
            
        Returns:
            Environment variable value
        """
        import os
        return os.environ.get(key, default)
    
    @staticmethod
    def get_int(key: str, default: int = None) -> int:
        """Get integer environment variable."""
        val = EnvironmentConfig.get(key)
        return int(val) if val else default
    
    @staticmethod
    def get_bool(key: str, default: bool = None) -> bool:
        """Get boolean environment variable."""
        val = EnvironmentConfig.get(key, '').lower()
        if val in ('true', '1', 'yes', 'on'):
            return True
        elif val in ('false', '0', 'no', 'off'):
            return False
        return default
    
    @staticmethod
    def load_to_config(config: Configuration, prefix: str = ""):
        """Load environment variables to configuration.
        
        Args:
            config: Configuration object
            prefix: Optional prefix for variables
        """
        import os
        
        for key, value in os.environ.items():
            if prefix and not key.startswith(prefix):
                continue
            
            config_key = key[len(prefix):].lower() if prefix else key.lower()
            config.set(config_key, value)


class ConfigBuilder:
    """Builder for configuration."""
    
    def __init__(self):
        """Initialize builder."""
        self.config = Configuration()
    
    def with_ini(self, filename: str) -> 'ConfigBuilder':
        """Load INI file."""
        self.config.load_ini(filename)
        return self
    
    def with_yaml(self, filename: str) -> 'ConfigBuilder':
        """Load YAML file."""
        self.config.load_yaml(filename)
        return self
    
    def with_json(self, filename: str) -> 'ConfigBuilder':
        """Load JSON file."""
        self.config.load_json(filename)
        return self
    
    def with_env(self, prefix: str = "") -> 'ConfigBuilder':
        """Load environment variables."""
        EnvironmentConfig.load_to_config(self.config, prefix)
        return self
    
    def with_override(self, key: str, value: Any) -> 'ConfigBuilder':
        """Add configuration override."""
        self.config.set(key, value)
        return self
    
    def build(self) -> Configuration:
        """Build configuration."""
        return self.config
