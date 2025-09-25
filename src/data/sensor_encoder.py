from pydantic import BaseModel
from datetime import datetime
from typing import Optional

SLOT = 14  # days to summarize

class SensorWindow(BaseModel):
    start: datetime
    end: datetime
    sleep_efficiency: float   # 0..1
    avg_sleep_duration_h: float
    steps: int
    vigorous_min: int
    resting_hr: Optional[int] = None
    screen_time_min: int
    unlocks: int
    locations_visited: int
    ema_mood_avg: Optional[float] = None  # -2..+2

RANGES = {
    "sleep_efficiency": (0.7, 0.9),
    "avg_sleep_duration_h": (5.5, 8.5),
    "steps": (2000, 10000),
    "screen_time_min": (60, 240),
    "unlocks": (30, 120),
}

def bucket(name: str, v: float) -> str:
    lo, hi = RANGES.get(name, (None, None))
    if lo is None:
        return str(v)
    if v < lo: return "low"
    if v > hi: return "high"
    return "mid"

TEMPLATE = (
    "# Contextual Well-being Snapshot (last {days} days)\n"
    "sleep_efficiency: {se_bucket} ({se:.2f})\n"
    "sleep_duration: {sd_bucket} ({sd:.1f}h)\n"
    "activity_steps: {st_bucket} ({steps})\n"
    "screen_time: {sc_bucket} ({sc}m)\n"
    "phone_unlocks: {ul_bucket} ({ul})\n"
    "places_visited: {loc}\n"
    "ema_mood_avg: {ema}\n"
)

def encode_for_prompt(w: SensorWindow) -> str:
    return TEMPLATE.format(
        days=(w.end - w.start).days,
        se_bucket=bucket("sleep_efficiency", w.sleep_efficiency), se=w.sleep_efficiency,
        sd_bucket=bucket("avg_sleep_duration_h", w.avg_sleep_duration_h), sd=w.avg_sleep_duration_h,
        st_bucket=bucket("steps", w.steps), steps=w.steps,
        sc_bucket=bucket("screen_time_min", w.screen_time_min), sc=w.screen_time_min,
        ul_bucket=bucket("unlocks", w.unlocks), ul=w.unlocks,
        loc=w.locations_visited,
        ema=w.ema_mood_avg if w.ema_mood_avg is not None else "unknown",
    )