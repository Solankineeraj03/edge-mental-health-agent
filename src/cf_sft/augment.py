import random
from typing import Dict

NOISE = {
    "sleep_efficiency": [
        lambda v: max(0.0, min(1.0, v + random.uniform(-0.2, 0.2))),
    ],
    "screen_time_min": [
        lambda v: max(0, int(v * random.uniform(0.5, 1.8))),
    ],
    "ema_mood_avg": [
        lambda v: None if random.random() < 0.2 else max(-2, min(2, (v or 0) + random.uniform(-1, 1)))
    ],
}

TEMPLATES = [
    "User misremembers duration of sleep.",
    "User downplays stress level while screen time is elevated.",
    "EMA missing or contradictory to behavior logs.",
]

def perturb(example: Dict) -> Dict:
    e = dict(example)
    for k, fs in NOISE.items():
        if k in e and random.random() < 0.6:
            e[k] = random.choice(fs)(e[k])
    e["counterfactual_note"] = random.choice(TEMPLATES)
    return e