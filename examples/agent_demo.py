#!/usr/bin/env python3
"""Agent demo showing basic usage of the edge mental health agent."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.agent.runtime import step
from src.data.sensor_encoder import SensorWindow
from datetime import datetime, timedelta

def main():
    """Run a simple demo of the agent."""
    print("🧠 Edge Mental Health Agent Demo")
    print("=" * 40)
    
    # Create a sample sensor window
    win = SensorWindow(
        start=datetime.now()-timedelta(days=14), 
        end=datetime.now(),
        sleep_efficiency=0.72, 
        avg_sleep_duration_h=6.1, 
        steps=3200, 
        vigorous_min=12,
        resting_hr=62, 
        screen_time_min=210, 
        unlocks=95, 
        locations_visited=12, 
        ema_mood_avg=-0.5
    )
    
    user_message = "I've been anxious after work."
    
    print(f"User: {user_message}")
    print("\nAgent: ", end="")
    
    try:
        response = step(win, user_message, history=[])
        print(response)
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This demo requires model files. See README for setup instructions.")

if __name__ == "__main__":
    main()