"""Configuration management for the edge mental health agent."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid YAML
    """
    if not os.path.exists(config_path):
        # Try relative to project root
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / config_path
        
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
    # Override with environment variables
    config = _override_with_env(config)
    
    return config


def _override_with_env(config: Dict[str, Any]) -> Dict[str, Any]:
    """Override configuration with environment variables."""
    
    # Model overrides
    if "BASE_MODEL" in os.environ:
        config["model"]["base_model"] = os.environ["BASE_MODEL"]
    if "PT_CKPT" in os.environ:
        config["model"]["pt_checkpoint"] = os.environ["PT_CKPT"]  
    if "SFT_CKPT" in os.environ:
        config["model"]["sft_checkpoint"] = os.environ["SFT_CKPT"]
    if "HF_DIR" in os.environ:
        config["model"]["hf_export_dir"] = os.environ["HF_DIR"]
        
    # Quantization overrides
    if "MLC_OUT" in os.environ:
        config["quantization"]["mlc_output_dir"] = os.environ["MLC_OUT"]
    if "TARGET" in os.environ:
        config["quantization"]["targets"] = [os.environ["TARGET"]]
        
    return config


def get_model_config() -> Dict[str, Any]:
    """Get model-specific configuration."""
    config = load_config()
    return config["model"]


def get_training_config() -> Dict[str, Any]:
    """Get training-specific configuration."""
    config = load_config()
    return config["training"]


def get_data_config() -> Dict[str, Any]:
    """Get data-specific configuration."""
    config = load_config()
    return config["data"]


def get_safety_config() -> Dict[str, Any]:
    """Get safety-specific configuration."""  
    config = load_config()
    return config["safety"]
