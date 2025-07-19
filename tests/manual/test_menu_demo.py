#!/usr/bin/env python3
"""Test the menu system with automated inputs"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock input for testing
test_inputs = iter([
    "1",  # Monaco track
    "1",  # 3 laps (sprint)
    "1",  # Clear weather
    "1",  # 3 drivers
    "",   # Start race
    "n"   # Don't race again
])

def mock_input(prompt):
    response = next(test_inputs)
    print(f"{prompt}{response}")
    return response

# Monkey patch input
import builtins
builtins.input = mock_input

# Import and run the menu
from run_llm_race_menu import main

try:
    main()
except StopIteration:
    print("\n✅ Menu test completed successfully!")
except Exception as e:
    print(f"\n❌ Menu test failed: {e}")
    import traceback
    traceback.print_exc()