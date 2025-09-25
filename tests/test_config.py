"""Tests for configuration management."""

import pytest
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent  
sys.path.insert(0, str(project_root))

from src.utils.config import load_config, get_model_config, get_safety_config


def test_load_config():
    """Test basic config loading."""
    config = load_config()
    
    # Check required sections exist
    assert "model" in config
    assert "training" in config
    assert "data" in config
    assert "safety" in config
    assert "quantization" in config
    
    # Check model config structure
    model_config = config["model"]
    assert "base_model" in model_config
    assert "max_new_tokens" in model_config
    assert "temperature" in model_config


def test_env_override():
    """Test environment variable overrides."""
    # Set environment variable
    os.environ["BASE_MODEL"] = "test/model"
    
    try:
        config = load_config()
        assert config["model"]["base_model"] == "test/model"
    finally:
        # Clean up
        if "BASE_MODEL" in os.environ:
            del os.environ["BASE_MODEL"]


def test_get_model_config():
    """Test model config getter."""
    model_config = get_model_config()
    
    assert "base_model" in model_config
    assert "max_new_tokens" in model_config
    assert isinstance(model_config["max_new_tokens"], int)
    assert isinstance(model_config["temperature"], float)


def test_get_safety_config():
    """Test safety config getter."""
    safety_config = get_safety_config()
    
    assert "emergency_keywords" in safety_config
    assert "emergency_helplines" in safety_config
    assert isinstance(safety_config["emergency_keywords"], list)
    assert len(safety_config["emergency_keywords"]) > 0


def test_config_validation():
    """Test that config has expected values."""
    config = load_config()
    
    # Model settings validation
    assert config["model"]["max_new_tokens"] > 0
    assert 0 < config["model"]["temperature"] <= 2.0
    assert 0 < config["model"]["top_p"] <= 1.0
    
    # Training settings validation
    assert config["training"]["domain_pt"]["learning_rate"] > 0
    assert config["training"]["sft"]["learning_rate"] > 0
    assert config["training"]["domain_pt"]["num_train_epochs"] > 0
    
    # Safety settings validation
    assert len(config["safety"]["emergency_keywords"]) > 0
    assert "us" in config["safety"]["emergency_helplines"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])