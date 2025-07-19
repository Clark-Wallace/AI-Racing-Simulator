#!/usr/bin/env python3
"""
Pygame Visual Race Demo - Real graphical racing with AI personalities!
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.racing_car import RacingCar, DriverStyle
from src.core.race_track import RaceTrack, TrackType
from src.graphics.graphical_race_simulator import GraphicalRaceSimulator
from src.graphics.race_renderer import GraphicsSettings


def create_personality_cars():
    """Create the 5 AI racing personalities with their unique characteristics"""
    return [
        RacingCar(
            name="Speed Demon Max",
            top_speed=380,
            acceleration=3.2,
            handling=0.65,
            fuel_efficiency=10,
            driver_style=DriverStyle.AGGRESSIVE
        ),
        RacingCar(
            name="The Professor",
            top_speed=350,
            acceleration=2.8,
            handling=0.90,
            fuel_efficiency=15,
            driver_style=DriverStyle.BALANCED  
        ),
        RacingCar(
            name="Fuel Master Eco",
            top_speed=340,
            acceleration=2.5,
            handling=0.75,
            fuel_efficiency=20,
            driver_style=DriverStyle.CONSERVATIVE
        ),
        RacingCar(
            name="The Chameleon",
            top_speed=360,
            acceleration=2.9,
            handling=0.80,
            fuel_efficiency=14,
            driver_style=DriverStyle.TECHNICAL
        ),
        RacingCar(
            name="Chaos Tornado",
            top_speed=370,
            acceleration=3.0,
            handling=0.70,
            fuel_efficiency=12,
            driver_style=DriverStyle.CHAOTIC
        )
    ]


def main():
    """Run the Pygame visual race demonstration"""
    print("🏎️  AI RACING SIMULATOR - PYGAME GRAPHICS DEMO 🏎️")
    print("=" * 60)
    
    # Check if Pygame is available
    try:
        import pygame
        print("✅ Pygame is installed! Starting graphical mode...")
    except ImportError:
        print("❌ Pygame not installed. Please install it first:")
        print("   pip install pygame")
        print("\nAlternatively, run the ASCII visual demo (option 4 in main menu)")
        return
        
    print("\n📋 RACE SETUP:")
    print("  • 5 AI personalities with unique driving styles")
    print("  • Each car has a distinct color matching their personality")
    print("  • Watch how different personalities affect racing behavior!")
    
    # Create cars and select track
    cars = create_personality_cars()
    
    print("\n🏁 TRACK SELECTION:")
    print("1. Speed Circuit (High-speed track)")
    print("2. Technical Circuit (Tight corners)")
    print("3. Mixed Circuit (Balanced layout)")
    print("4. Endurance Circuit (Long distance)")
    
    track_choice = input("\nSelect track (1-4, default=1): ").strip() or "1"
    
    if track_choice == "2":
        track = RaceTrack.create_technical_track("Monaco")
    elif track_choice == "3":
        track = RaceTrack.create_mixed_track("Silverstone")
    elif track_choice == "4":
        track = RaceTrack.create_endurance_track("Le Mans")
    else:
        track = RaceTrack.create_speed_track("Monza")
        
    print(f"\n✅ Selected: {track.name}")
    
    # Configure graphics settings
    settings = GraphicsSettings(
        width=1200,
        height=800,
        fps=60,
        show_telemetry=True,
        show_ai_thoughts=True,
        camera_mode="follow"
    )
    
    # Get number of laps
    num_laps = input("\nNumber of laps (1-10, default=5): ").strip()
    num_laps = int(num_laps) if num_laps.isdigit() else 5
    num_laps = max(1, min(10, num_laps))
    
    print(f"\n🎮 CONTROLS:")
    print("  • ESC - Exit race")
    print("  • Watch the AI personalities compete!")
    
    print("\n🚦 STARTING RACE...")
    print(f"  • Track: {track.name} ({track.total_length}km)")
    print(f"  • Laps: {num_laps}")
    print(f"  • Weather: Clear")
    
    # Show AI personalities
    print("\n🎭 AI PERSONALITIES:")
    print("  • 🔴 Speed Demon (Red) - Aggressive, high-risk racing")
    print("  • 🔵 The Professor (Blue) - Technical, precise lines")
    print("  • 🟢 Fuel Master (Green) - Conservative, efficient")
    print("  • 🟡 The Chameleon (Yellow) - Adaptive, strategic")
    print("  • 🟣 Chaos Tornado (Magenta) - Unpredictable wildcard")
    
    input("\nPress Enter to start the race...")
    
    # Create and run graphical simulator
    simulator = GraphicalRaceSimulator(
        track=track,
        cars=cars,
        laps=num_laps,
        enable_telemetry=True,
        enable_intelligence=True,
        enable_graphics=True,
        graphics_settings=settings
    )
    
    # Run the race
    results = simulator.simulate_race()
    
    # Display results
    if results.get("visualization_completed"):
        print("\n🏁 RACE RESULTS 🏁")
        print("=" * 60)
        
        print("\n🏆 FINAL STANDINGS:")
        for result in results["finishing_order"]:
            position = result["position"]
            name = result["name"]
            time = result["total_time"]
            style = result["driver_style"]
            fuel = result["final_fuel"]
            
            # Position emojis
            if position == 1:
                pos_emoji = "🥇"
            elif position == 2:
                pos_emoji = "🥈"
            elif position == 3:
                pos_emoji = "🥉"
            else:
                pos_emoji = f"{position}."
                
            print(f"{pos_emoji} {name:<20} - Time: {time:.2f}s")
            print(f"   Style: {style}, Final Fuel: {fuel:.1f}%")
            
        # Show personality impact
        print("\n🎭 PERSONALITY ANALYSIS:")
        winner = results["finishing_order"][0]
        print(f"Winner: {winner['name']} ({winner['driver_style']})")
        
        if winner['driver_style'] == "AGGRESSIVE":
            print("  → Aggressive style paid off! High risk, high reward.")
        elif winner['driver_style'] == "BALANCED":
            print("  → Technical precision led to victory!")
        elif winner['driver_style'] == "CONSERVATIVE":
            print("  → Steady and efficient driving won the day!")
        elif winner['driver_style'] == "TECHNICAL":
            print("  → Adaptive strategy proved successful!")
        else:  # CHAOTIC
            print("  → Chaos reigned supreme! Unpredictability wins!")
            
        print("\n✨ Graphical race demo completed successfully!")
        print("💡 Try different tracks and lap counts to see how AI adapts!")
        
    else:
        print("\n⚠️  Race visualization was interrupted.")
        

if __name__ == "__main__":
    main()