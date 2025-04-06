import pytest
import sys
import os

# Add the src directory to Python's path so that tests can import modules from there
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# This file can contain shared fixtures and configuration for pytest
@pytest.fixture
def standard_width():
    """Return the standard width used in most test cases."""
    return 150

@pytest.fixture
def standard_thicknesses():
    """Return the list of standard thicknesses to be tested."""
    return [6, 8, 10, 12, 16, 20, 24]

@pytest.fixture
def standard_load_range():
    """Return a range of load values for testing."""
    return range(0, 101, 10)  # 0, 10, 20, ..., 100 