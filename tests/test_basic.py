def test_imports():
    import src.data.sensor_encoder as se
    assert hasattr(se, "SensorWindow")