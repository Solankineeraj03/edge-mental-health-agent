import os
import logging
from typing import Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
from .prompts import build_prompt
from ..data.sensor_encoder import SensorWindow, encode_for_prompt
from ..utils.logging_setup import get_logger

logger = get_logger("runtime")

MODEL_DIR = os.getenv("SFT_CKPT", "artifacts/sft")

# Global model and tokenizer (lazy loaded)
_tok: Optional[AutoTokenizer] = None
_model: Optional[AutoModelForCausalLM] = None

def _load_model():
    """Load model and tokenizer with proper error handling."""
    global _tok, _model
    
    if _tok is not None and _model is not None:
        return _tok, _model
        
    try:
        logger.info(f"Loading model from {MODEL_DIR}")
        _tok = AutoTokenizer.from_pretrained(MODEL_DIR, use_fast=True)
        _model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)
        logger.info("Model loaded successfully") 
        return _tok, _model
    except Exception as e:
        logger.error(f"Failed to load model from {MODEL_DIR}: {e}")
        raise RuntimeError(f"Model loading failed: {e}. Please check that the model is trained and available at {MODEL_DIR}")

def step(sensor_window: SensorWindow, user_msg: str, history: list[str]) -> str:
    """Execute one step of the agent loop: perceive → decide → act.
    
    Args:
        sensor_window: Sensor data context window
        user_msg: User's message/query
        history: Previous conversation history
        
    Returns:
        Agent's response
        
    Raises:
        RuntimeError: If model loading fails
        ValueError: If inputs are invalid
    """
    if not user_msg.strip():
        raise ValueError("User message cannot be empty")
        
    try:
        tok, model = _load_model()
        
        # Encode sensor context and build prompt
        ctx = encode_for_prompt(sensor_window)
        prompt = build_prompt(ctx, user_msg, history)
        
        logger.debug(f"Generated prompt length: {len(prompt)} chars")
        
        # Generate response
        ids = tok(prompt, return_tensors="pt")
        out = model.generate(
            **ids, 
            max_new_tokens=300, 
            temperature=0.7, 
            do_sample=True, 
            top_p=0.9,
            pad_token_id=tok.eos_token_id
        )
        reply = tok.decode(out[0], skip_special_tokens=True).split("<|assistant|>")[-1].strip()
        
        logger.info(f"Generated response length: {len(reply)} chars")
        return reply
        
    except Exception as e:
        logger.error(f"Step execution failed: {e}")
        raise