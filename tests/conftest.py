"""Test configuration and fixtures."""

import pytest
import os
import sys

# Add the src directory to the Python path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def sample_username():
    """Sample username for testing."""
    return "testuser"

@pytest.fixture
def sample_message():
    """Sample message for testing."""
    return "This is a test message"

@pytest.fixture
def sample_device_id():
    """Sample device ID for testing."""
    return "12345678-1234-1234-1234-123456789012"
