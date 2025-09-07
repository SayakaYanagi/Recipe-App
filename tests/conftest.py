# tests/conftest.py
import sys
import os

# Add the project root to sys.path so "import utils" works
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
