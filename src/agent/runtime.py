import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from .prompts import build_prompt
from ..data.sensor_encoder import SensorWindow, encode_for_prompt

MODEL_DIR = os.getenv("SFT_CKPT", "artifacts/sft")

tok = AutoTokenizer.from_pretrained(MODEL_DIR, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)

def step(sensor_window: SensorWindow, user_msg: str, history: list[str]):
    ctx = encode_for_prompt(sensor_window)
    prompt = build_prompt(ctx, user_msg, history)
    ids = tok(prompt, return_tensors="pt")
    out = model.generate(**ids, max_new_tokens=300, temperature=0.7, do_sample=True, top_p=0.9)
    reply = tok.decode(out[0], skip_special_tokens=True).split("<|assistant|>")[-1].strip()
    return reply