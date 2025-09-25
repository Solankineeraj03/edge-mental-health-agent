#!/usr/bin/env bash
set -euo pipefail
mkdir -p data/processed
if [ ! -f data/processed/domain_corpus.jsonl ]; then
  cat > data/processed/domain_corpus.jsonl <<EOF
{"text": "Therapist: I hear you’re feeling overwhelmed. Let’s take a slow breath together."}
{"text": "CBT tip: Notice the thought, label it, gently reframe, and test it against evidence."}
EOF
fi
if [ ! -f data/processed/sft.jsonl ]; then
  cat > data/processed/sft.jsonl <<EOF
{"sensor_prompt":"# Contextual Well-being Snapshot (last 14 days)\nsleep_efficiency: low (0.68)\nsleep_duration: low (5.6h)\nactivity_steps: low (2800)\nscreen_time: high (240m)\nphone_unlocks: high (110)\nplaces_visited: 8\nema_mood_avg: -0.5\n","dialogue":"User: I keep waking up and doomscrolling.","target_response":"It makes sense you’re feeling drained with broken sleep and late-night scrolling. Would you like a 2‑minute wind-down exercise tonight and a gentle phone curfew reminder?"}
EOF
fi
if [ ! -f data/processed/val.jsonl ]; then
  cp data/processed/sft.jsonl data/processed/val.jsonl
fi
echo "Prepared minimal processed dataset."