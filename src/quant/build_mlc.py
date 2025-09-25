import subprocess, os

HF_DIR = os.getenv("HF_DIR", "artifacts/hf_export")
MLC_OUT = os.getenv("MLC_OUT", "mobile/mlc-models")
TARGET = os.getenv("TARGET", "android")  # or ios

# Requires: pip install mlc-ai-nightly mlc-llm and Android NDK/Xcode toolchains

preset = "q4f16_1"  # 4‑bit weights with FP16 scales per block
subprocess.check_call([
  "mlc_llm", "convert-weight",
  "--model", HF_DIR,
  "--quantization", preset,
  "--output", os.path.join(MLC_OUT, "mindguard-7b-"+preset)
])

subprocess.check_call([
  "mlc_llm", "build",
  "--model", os.path.join(MLC_OUT, "mindguard-7b-"+preset),
  "--artifact-path", MLC_OUT,
  "--device", TARGET,
])
print("MLC build complete at", MLC_OUT)