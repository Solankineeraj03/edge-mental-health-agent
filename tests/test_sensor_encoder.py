"""Tests for sensor data encoding."""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data.sensor_encoder import SensorWindow, encode_for_prompt, bucket


class TestSensorEncoder:
    """Test cases for sensor data encoding."""
    
    def test_sensor_window_creation(self):
        """Test SensorWindow creation with valid data."""
        window = SensorWindow(
            start=datetime.now() - timedelta(days=14),
            end=datetime.now(),
            sleep_efficiency=0.75,
            avg_sleep_duration_h=7.0,
            steps=5000,
            vigorous_min=20,
            resting_hr=65,
            screen_time_min=180,
            unlocks=60,
            locations_visited=10,
            ema_mood_avg=0.0
        )
        
        assert window.sleep_efficiency == 0.75
        assert window.avg_sleep_duration_h == 7.0
        assert window.steps == 5000
        assert window.ema_mood_avg == 0.0
    
    def test_bucket_function(self):
        """Test the bucket categorization function."""
        # Test sleep efficiency bucketing (range: 0.7-0.9)
        assert bucket("sleep_efficiency", 0.6) == "low"
        assert bucket("sleep_efficiency", 0.8) == "mid"
        assert bucket("sleep_efficiency", 0.95) == "high"
        
        # Test steps bucketing (range: 2000-10000)
        assert bucket("steps", 1500) == "low"
        assert bucket("steps", 5000) == "mid" 
        assert bucket("steps", 12000) == "high"
        
        # Test unknown metric (should return string representation)
        assert bucket("unknown_metric", 42) == "42"
    
    def test_encode_for_prompt(self):
        """Test encoding sensor window to prompt text."""
        window = SensorWindow(
            start=datetime.now() - timedelta(days=14),
            end=datetime.now(),
            sleep_efficiency=0.85,  # high
            avg_sleep_duration_h=6.0,  # mid
            steps=1800,  # low
            vigorous_min=25,
            resting_hr=68,
            screen_time_min=250,  # high
            unlocks=45,  # mid
            locations_visited=8,
            ema_mood_avg=-0.5
        )
        
        encoded = encode_for_prompt(window)
        
        # Check that encoded text contains expected elements
        assert "14 days" in encoded
        assert "sleep_efficiency: mid (0.85)" in encoded  # 0.85 is in mid range
        assert "sleep_duration: mid (6.0h)" in encoded
        assert "activity_steps: low (1800)" in encoded
        assert "screen_time: high (250m)" in encoded
        assert "phone_unlocks: mid (45)" in encoded
        assert "places_visited: 8" in encoded
        assert "ema_mood_avg: -0.5" in encoded
        
        # Check overall structure
        assert encoded.startswith("# Contextual Well-being Snapshot")
        assert len(encoded) > 100  # Should be substantial
    
    def test_encode_with_missing_ema(self):
        """Test encoding when EMA data is missing."""
        window = SensorWindow(
            start=datetime.now() - timedelta(days=7),
            end=datetime.now(),
            sleep_efficiency=0.75,
            avg_sleep_duration_h=7.0,
            steps=5000,
            vigorous_min=20,
            screen_time_min=120,
            unlocks=50,
            locations_visited=5,
            ema_mood_avg=None  # Missing EMA data
        )
        
        encoded = encode_for_prompt(window)
        assert "ema_mood_avg: unknown" in encoded
    
    def test_edge_cases(self):
        """Test edge cases in sensor data."""
        # Test with extreme values
        window = SensorWindow(
            start=datetime.now() - timedelta(days=1),
            end=datetime.now(), 
            sleep_efficiency=0.0,  # Very low
            avg_sleep_duration_h=12.0,  # Very high
            steps=0,  # No steps
            vigorous_min=0,
            screen_time_min=500,  # Very high
            unlocks=200,  # Very high
            locations_visited=0,
            ema_mood_avg=-2.0  # Very negative
        )
        
        encoded = encode_for_prompt(window)
        
        # Should handle extreme values gracefully
        assert "1 days" in encoded
        assert "sleep_efficiency: low (0.00)" in encoded
        assert "sleep_duration: high (12.0h)" in encoded
        assert "activity_steps: low (0)" in encoded
        assert "ema_mood_avg: -2.0" in encoded
    
    def test_window_duration_calculation(self):
        """Test that window duration is calculated correctly."""
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 15)  # 14 days difference
        
        window = SensorWindow(
            start=start_date,
            end=end_date,
            sleep_efficiency=0.75,
            avg_sleep_duration_h=7.0,
            steps=5000,
            vigorous_min=20,
            screen_time_min=120,
            unlocks=50,
            locations_visited=5,
            ema_mood_avg=0.0
        )
        
        encoded = encode_for_prompt(window)
        assert "14 days" in encoded


if __name__ == "__main__":
    pytest.main([__file__, "-v"])