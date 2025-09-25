#!/usr/bin/env bash
set -euo pipefail
HF_DIR=${HF_DIR:-artifacts/hf_export} TARGET=${TARGET:-android} python -m src.quant.build_mlc