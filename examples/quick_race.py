#!/usr/bin/env python3
"""
Quick Race Example - Run a simple race with AI personalities
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.racing_car import RacingCar, DriverStyle
from src.core.race_track import RaceTrack
from src.core.intelligent_race_simulator import IntelligentRaceSimulator
from src.intelligence.ai_personalities import AIPersonalitySystem
from src.intelligence.enhanced_ai_racers import create_enhanced_ai_racers


def main():
    """Run a quick demonstration race"""
    print("🏎️  AI Racing Simulator - Quick Race Example")
    print("=" * 50)
    
    # Create AI personalities
    personality_system = AIPersonalitySystem()
    enhanced_racers = create_enhanced_ai_racers(personality_system)
    cars = [racer.car for racer in enhanced_racers]
    
    # Create track
    track = RaceTrack.create_mixed_track()
    track.weather_conditions = "clear"
    
    print(f"\n🏁 Track: {track.name}")
    print(f"🌤️  Weather: {track.weather_conditions}")
    print(f"📏 Length: {track.length:.2f} km")
    
    # Show racers
    print("\n🎭 Racers:")
    for i, racer in enumerate(enhanced_racers):
        print(f"  {i+1}. {racer.car.name} ({racer.car.driver_style.value})")
    
    # Run race
    print("\n🚦 Starting 10-lap race...")
    simulator = IntelligentRaceSimulator(
        track=track,
        cars=cars,
        laps=10,
        enable_telemetry=True,
        enable_intelligence=True
    )
    
    results = simulator.simulate_race()
    
    # Show results
    print("\n🏁 RACE RESULTS:")
    print("=" * 30)
    
    for position in sorted(results["positions"].keys()):
        driver_data = results["positions"][position]
        print(f"P{position}: {driver_data['name']} - {driver_data['time']:.3f}s")
    
    # Show fastest lap
    if "fastest_lap" in results:
        fl = results["fastest_lap"]
        print(f"\n⚡ Fastest Lap: {fl['driver']} - {fl['time']:.3f}s")
    
    # Show some race events
    if "events" in results:
        print("\n📰 Race Highlights:")
        for event in results["events"][:3]:  # Show first 3 events
            print(f"  • {event.details}")
    
    print("\n🏆 Race complete!")


if __name__ == "__main__":
    main()