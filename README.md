# Edge Mental Health Agent (MindGuard-style)

End-to-end starter implementation that matches the paper's recipe:
- Domain continued pretraining on mental-health corpus
- Supervised fine-tuning with counterfactual robustness
- Sensor→prompt encoder to fuse objective logs + EMA
- q4f16 block quantization + on-device MLC-LLM build
- Autonomous agent loop (perceive → decide → act) with safety prompts

## Quickstart

### 0) Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# (Optional) Or use pyproject with: pip install .
```

### 1) Data
Put wearable/app logs in `data/raw/`. Prepare processed files:
- `data/processed/domain_corpus.jsonl`  (continued pretraining text)
- `data/processed/sft.jsonl` and `data/processed/val.jsonl` (SFT pairs)

Or run the stubs:
```bash
bash scripts/prepare_data.sh
```

### 2) Continued pretraining
```bash
BASE_MODEL=internlm2/internlm2-7b bash scripts/train_pt.sh
```

### 3) Supervised fine-tuning with counterfactuals
```bash
PT_CKPT=artifacts/pt bash scripts/train_sft.sh
```

### 4) Try the agent loop
```python
from src.agent.runtime import step
from src.data.sensor_encoder import SensorWindow
from datetime import datetime, timedelta

win = SensorWindow(
  start=datetime.now()-timedelta(days=14), end=datetime.now(),
  sleep_efficiency=0.72, avg_sleep_duration_h=6.1, steps=3200, vigorous_min=12,
  resting_hr=62, screen_time_min=210, unlocks=95, locations_visited=12, ema_mood_avg=-0.5
)
print(step(win, "I've been anxious after work.", history=[]))
```

### 5) Export & q4f16 build for mobile
```bash
bash scripts/export_hf.sh
HF_DIR=artifacts/hf_export TARGET=android python -m src.quant.build_mlc
# For iOS: TARGET=ios
```

### 6) Mobile
Open `mobile/react-native-shell/` and wire the provided artifacts in `mobile/mlc-models/` to your RN bridge.

## Safety
This software is **not** a medical device. It must not issue diagnoses, emergency instructions, or medication advice.
If a user indicates imminent harm, the assistant should show local emergency resources and prompt contacting professionals.