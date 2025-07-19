#!/usr/bin/env python3
"""Test power-up pickup visibility"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.race_track import RaceTrack, TrackType, TrackSegment
from src.llm_drivers.llm_racing_driver import create_llm_drivers
from src.llm_drivers.llm_race_simulator import LLMRaceSimulator
from src.graphics.race_renderer import GraphicsSettings

# Create a simple track
segments = [
    TrackSegment(length=1000, is_straight=True),
    TrackSegment(length=500, is_straight=False, corner_angle=90, corner_radius=100),
    TrackSegment(length=800, is_straight=True),
    TrackSegment(length=700, is_straight=False, corner_angle=120, corner_radius=80),
]

track = RaceTrack(
    name="Power-Up Test Track",
    track_type=TrackType.SPEED_TRACK,
    total_length=3.0,
    segments=segments,
    weather_conditions="clear"
)

# Create LLM drivers (just 2 for testing)
print("🤖 Creating test drivers...")
llm_drivers = create_llm_drivers()[:2]

# Graphics settings
graphics_settings = GraphicsSettings(
    width=1200,
    height=800,
    fps=60,
    show_telemetry=True,
    show_ai_thoughts=True
)

# Create and run simulator
print("🏁 Starting race with visible power-up pickups...")
print("\n📦 Power-up boxes should appear as golden/white/cyan rotating boxes with '?' marks")
print("Cars can collect them by driving through them!")
print("\nPress ESC to exit\n")

simulator = LLMRaceSimulator(
    track=track,
    llm_drivers=llm_drivers,
    laps=5,
    enable_graphics=True,
    graphics_settings=graphics_settings
)

# Run the race
results = simulator.simulate_race()

print("\n✅ Power-up pickup test complete!")