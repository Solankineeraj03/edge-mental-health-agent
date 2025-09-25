from src.agent.runtime import step
from src.data.sensor_encoder import SensorWindow
from datetime import datetime, timedelta

if __name__ == "__main__":
    win = SensorWindow(
      start=datetime.now()-timedelta(days=14), end=datetime.now(),
      sleep_efficiency=0.72, avg_sleep_duration_h=6.1, steps=3200, vigorous_min=12,
      resting_hr=62, screen_time_min=210, unlocks=95, locations_visited=12, ema_mood_avg=-0.5
    )
    print(step(win, "I've been anxious after work.", history=[]))