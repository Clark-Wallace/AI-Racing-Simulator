#!/usr/bin/env python3
"""Test LLM Race with Visual Mode and Sprites"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.race_track import RaceTrack, TrackType
from src.llm_drivers.llm_racing_driver import create_llm_drivers
from src.llm_drivers.llm_race_simulator import LLMRaceSimulator
from src.graphics.race_renderer import GraphicsSettings

# Create a speed track for testing
from src.core.race_track import TrackSegment
segments = [
    TrackSegment(length=1000, is_straight=True),
    TrackSegment(length=500, is_straight=False, corner_angle=90, corner_radius=100),
    TrackSegment(length=800, is_straight=True),
    TrackSegment(length=700, is_straight=False, corner_angle=120, corner_radius=80),
    TrackSegment(length=1000, is_straight=True),
    TrackSegment(length=1000, is_straight=False, corner_angle=180, corner_radius=60),
]

track = RaceTrack(
    name="Sprite Test Speedway",
    track_type=TrackType.SPEED_TRACK,
    total_length=5.0,  # 5km for quick testing
    segments=segments,
    weather_conditions="clear"
)

# Create LLM drivers
print("🤖 Creating LLM drivers...")
llm_drivers = create_llm_drivers()

# Use only 3 drivers for testing
llm_drivers = llm_drivers[:3]

# Graphics settings
graphics_settings = GraphicsSettings(
    width=1200,
    height=800,
    fps=60,
    show_telemetry=True,
    show_ai_thoughts=True
)

# Create and run simulator
print("🏁 Starting visual race with sprites...")
simulator = LLMRaceSimulator(
    track=track,
    llm_drivers=llm_drivers,
    laps=3,  # Just 3 laps for testing
    enable_graphics=True,
    graphics_settings=graphics_settings
)

# Run the race
results = simulator.simulate_race()

# Print results
print("\n🏆 RACE RESULTS:")
for driver in results["finishing_order"]:
    print(f"{driver['position']}. {driver['name']} ({driver['model']}) - {driver['total_time']:.2f}s")

print("\n✅ Visual race with sprites complete!")