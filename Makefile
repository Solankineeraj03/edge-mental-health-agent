# Edge Mental Health Agent Makefile
# Automates the complete workflow from data preparation to mobile deployment

.PHONY: help setup clean test lint format
.PHONY: prepare-data train-pt train-sft demo export-hf build-android build-ios
.PHONY: eval safety-check check-all

# Configuration
BASE_MODEL ?= internlm2/internlm2-7b
PT_CKPT ?= artifacts/pt
SFT_CKPT ?= artifacts/sft
HF_DIR ?= artifacts/hf_export
TARGET ?= android

# Default target
help: ## Show this help message
	@echo "Edge Mental Health Agent Makefile"
	@echo "Usage: make [target] [options]"
	@echo ""
	@echo "Environment Variables:"
	@echo "  BASE_MODEL=$(BASE_MODEL)"
	@echo "  PT_CKPT=$(PT_CKPT)"
	@echo "  SFT_CKPT=$(SFT_CKPT)"
	@echo "  HF_DIR=$(HF_DIR)"
	@echo "  TARGET=$(TARGET)"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

setup: ## Install dependencies and setup environment
	@echo "🔧 Setting up environment..."
	python -m pip install --upgrade pip
	pip install -e .
	pip install pytest black flake8 mypy pre-commit
	@echo "✅ Setup complete!"

clean: ## Clean generated files and cache
	@echo "🧹 Cleaning up..."
	rm -rf __pycache__ .pytest_cache .mypy_cache
	rm -rf src/**/__pycache__ tests/__pycache__
	rm -rf artifacts/ runs/ logs/ mobile/mlc-models/
	rm -rf *.egg-info build/ dist/
	@echo "✅ Cleanup complete!"

# Data and Training Pipeline
prepare-data: ## Prepare training data (creates minimal stubs if no raw data)
	@echo "📊 Preparing training data..."
	bash scripts/prepare_data.sh
	@echo "✅ Data preparation complete!"

train-pt: prepare-data ## Run domain continued pretraining
	@echo "🎓 Starting domain continued pretraining..."
	@echo "Base model: $(BASE_MODEL)"
	BASE_MODEL=$(BASE_MODEL) bash scripts/train_pt.sh
	@echo "✅ Domain pretraining complete!"

train-sft: train-pt ## Run supervised fine-tuning with counterfactuals
	@echo "🎯 Starting supervised fine-tuning..."
	@echo "PT checkpoint: $(PT_CKPT)"
	PT_CKPT=$(PT_CKPT) bash scripts/train_sft.sh
	@echo "✅ Supervised fine-tuning complete!"

# Testing and Demo
demo: ## Run agent demo (requires trained model)
	@echo "🤖 Running agent demo..."
	python examples/agent_demo.py

test: ## Run test suite
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v --tb=short

lint: ## Run linting checks
	@echo "🔍 Running linting checks..."
	python -m compileall -q .
	flake8 --max-line-length=100 --extend-ignore=E203,W503 src/ tests/
	@echo "✅ Linting passed!"

format: ## Format code with black
	@echo "🎨 Formatting code..."
	black --line-length=100 src/ tests/ examples/
	@echo "✅ Code formatted!"

# Model Export and Quantization
export-hf: ## Export trained model to HuggingFace format
	@echo "📦 Exporting model to HuggingFace format..."
	@echo "SFT checkpoint: $(SFT_CKPT)"
	@echo "Export directory: $(HF_DIR)"
	SFT_CKPT=$(SFT_CKPT) HF_DIR=$(HF_DIR) bash scripts/export_hf.sh
	@echo "✅ Model export complete!"

build-android: export-hf ## Build quantized model for Android
	@echo "📱 Building for Android (q4f16)..."
	HF_DIR=$(HF_DIR) TARGET=android python -m src.quant.build_mlc
	@echo "✅ Android build complete!"

build-ios: export-hf ## Build quantized model for iOS  
	@echo "📱 Building for iOS (q4f16)..."
	HF_DIR=$(HF_DIR) TARGET=ios python -m src.quant.build_mlc
	@echo "✅ iOS build complete!"

build-mobile: build-android build-ios ## Build for both Android and iOS

# Evaluation and Safety
eval: ## Run model evaluation
	@echo "📊 Running model evaluation..."
	python -m src.eval.run_evaluation
	@echo "✅ Evaluation complete!"

safety-check: ## Run safety coverage tests
	@echo "🛡️ Running safety checks..."
	python -m pytest tests/test_safety.py -v
	@echo "✅ Safety checks complete!"

# Complete workflows
train-all: prepare-data train-pt train-sft ## Complete training pipeline
	@echo "🎉 Complete training pipeline finished!"

build-all: train-all export-hf build-mobile ## Complete pipeline from training to mobile
	@echo "🎉 Complete build pipeline finished!"

check-all: lint test safety-check ## Run all checks
	@echo "✅ All checks passed!"

# Development helpers
dev-setup: setup ## Setup development environment with pre-commit hooks
	@echo "🔧 Setting up development environment..."
	pre-commit install
	@echo "✅ Development setup complete!"

quick-test: ## Quick test run (basic functionality only)
	@echo "⚡ Running quick tests..."
	python -m pytest tests/test_basic.py -v
	python -c "from src.utils.config import load_config; print('Config loading works!')"
	@echo "✅ Quick tests passed!"

# Documentation
docs: ## Generate documentation
	@echo "📚 This would generate documentation (not implemented yet)"

# Installation verification
verify-install: ## Verify installation is working
	@echo "🔍 Verifying installation..."
	python -c "import src; print('✅ Package imports working')"
	python -c "from src.utils.config import load_config; load_config(); print('✅ Config system working')"
	python -c "from src.data.sensor_encoder import SensorWindow; print('✅ Sensor encoder working')"
	@echo "🎉 Installation verified!"