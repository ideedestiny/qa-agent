import sys
import os

# Add the project root to Python's module search path
# This allows tests in subdirectories to import from the root
sys.path.insert(0, os.path.dirname(__file__))