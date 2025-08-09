"""Tests for device ID generator."""

import pytest
from ngl_spammer.generators.device_generator import DeviceIDGenerator


class TestDeviceIDGenerator:
    """Test cases for DeviceIDGenerator."""
    
    def test_generate_device_id_format(self):
        """Test that generated device ID follows correct format."""
        device_id = DeviceIDGenerator.generate()
        
        # Should be in format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        parts = device_id.split('-')
        assert len(parts) == 5
        assert len(parts[0]) == 8
        assert len(parts[1]) == 4
        assert len(parts[2]) == 4
        assert len(parts[3]) == 4
        assert len(parts[4]) == 12
    
    def test_generate_device_id_uniqueness(self):
        """Test that generated device IDs are unique."""
        device_ids = set()
        for _ in range(1000):
            device_id = DeviceIDGenerator.generate()
            assert device_id not in device_ids
            device_ids.add(device_id)
    
    def test_generate_device_id_characters(self):
        """Test that device ID contains only valid characters."""
        device_id = DeviceIDGenerator.generate()
        
        # Remove dashes and check remaining characters
        chars = device_id.replace('-', '')
        valid_chars = set('abcdefghijklmnopqrstuvwxyz0123456789')
        
        for char in chars:
            assert char in valid_chars
    
    def test_generate_batch(self):
        """Test batch generation of device IDs."""
        count = 10
        device_ids = DeviceIDGenerator.generate_batch(count)
        
        assert len(device_ids) == count
        assert len(set(device_ids)) == count  # All should be unique
