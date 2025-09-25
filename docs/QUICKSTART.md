# Quick Guide

1. Prepare data: `bash scripts/prepare_data.sh`
2. Domain PT: `BASE_MODEL=internlm2/internlm2-7b bash scripts/train_pt.sh`
3. SFT (with counterfactuals): `PT_CKPT=artifacts/pt bash scripts/train_sft.sh`
4. Try agent: `python examples/agent_demo.py`
5. Export & build (q4f16): `bash scripts/export_hf.sh && HF_DIR=artifacts/hf_export TARGET=android python -m src.quant.build_mlc`