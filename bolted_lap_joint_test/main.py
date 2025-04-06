#!/usr/bin/env python
"""
Main entry point for the Bolted Lap Joint Design tool.
This script provides a simple wrapper around the CLI functionality.
"""

import sys
import os

# Add the src directory to the path if not already there
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
if src_dir not in sys.path:
    sys.path.append(src_dir)

# Import the CLI module
from src.cli import main

if __name__ == "__main__":
    sys.exit(main()) 