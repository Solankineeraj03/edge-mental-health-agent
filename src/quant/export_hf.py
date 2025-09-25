from transformers import AutoModelForCausalLM, AutoTokenizer

CKPT = "artifacts/sft"
OUT = "artifacts/hf_export"

tok = AutoTokenizer.from_pretrained(CKPT, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(CKPT)
model.save_pretrained(OUT)
tok.save_pretrained(OUT)
print("Saved to", OUT)