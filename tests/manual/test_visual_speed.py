#!/usr/bin/env python3
"""
Quick test to debug visual mode car movement
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.race_track import RaceTrack
from src.core.racing_car import RacingCar, DriverStyle
from src.llm_drivers.llm_racing_driver import LLMDriver, LLMAction
from src.llm_drivers.llm_race_simulator import LLMRaceSimulator
from ai_config import RacingAI, LLAMA_MODELS

# Create a simple test with one car
car = RacingCar(
    name="Test Car",
    top_speed=350,
    acceleration=3.0,
    handling=0.8,
    fuel_efficiency=12,
    driver_style=DriverStyle.BALANCED
)

# Create a dummy LLM driver that always returns ATTACK
class DummyAI:
    async def make_racing_decision(self, race_state, personality):
        return {"action": "ATTACK", "confidence": 1.0, "reasoning": "Test"}
    
    async def generate_race_commentary(self, event, personality):
        return "Test!"

driver = LLMDriver(
    car=car,
    ai=DummyAI(),
    model_config={"model": "test/model", "personality": "Test driver"},
    name="Test Driver"
)

# Create track and simulator
track = RaceTrack.create_speed_track("Test Track")
sim = LLMRaceSimulator(
    track=track,
    llm_drivers=[driver],
    laps=1,
    enable_graphics=True
)

print("Starting visual test with dummy driver...")
print("Car top speed:", car.top_speed)
print("Track length:", track.total_length, "km")

# Run the race
results = sim.simulate_race()
print("\nTest complete!")
if results and "finishing_order" in results:
    print("Results:", results["finishing_order"])