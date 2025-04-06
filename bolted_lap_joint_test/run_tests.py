#!/usr/bin/env python
import os
import sys
import pytest

def main():
    """Run the PyTest tests with specified options."""
    print("Running bolted lap joint design tests...")
    
    # Define the path to the tests directory
    tests_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    # Run PyTest with coverage and verbose output
    args = [
        "-v",  # Verbose output
        "--cov=src",  # Coverage report for src directory
        "--cov-report=term",  # Terminal coverage report
        tests_dir  # Path to tests directory
    ]
    
    # Execute the tests
    return pytest.main(args)

if __name__ == "__main__":
    sys.exit(main()) 