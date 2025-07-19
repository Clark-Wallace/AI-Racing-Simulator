#!/usr/bin/env python3
"""
LLM Racing Menu System - Select tracks, laps, and race settings
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.race_track import RaceTrack, TrackType, TrackSegment
from src.llm_drivers.llm_racing_driver import create_llm_drivers
from src.llm_drivers.llm_race_simulator import LLMRaceSimulator
from src.graphics.race_renderer import GraphicsSettings


def create_monaco_track():
    """Create a Monaco-style street circuit"""
    segments = [
        TrackSegment(length=800, is_straight=True),     # Start/finish straight
        TrackSegment(length=300, is_straight=False, corner_angle=90, corner_radius=50),   # Tight hairpin
        TrackSegment(length=400, is_straight=True),
        TrackSegment(length=200, is_straight=False, corner_angle=45, corner_radius=80),   # Medium corner
        TrackSegment(length=600, is_straight=True),     # Tunnel section
        TrackSegment(length=400, is_straight=False, corner_angle=135, corner_radius=40),  # Chicane
        TrackSegment(length=350, is_straight=True),
        TrackSegment(length=250, is_straight=False, corner_angle=90, corner_radius=60),   # Swimming pool
        TrackSegment(length=500, is_straight=True),
        TrackSegment(length=300, is_straight=False, corner_angle=180, corner_radius=30),  # Rascasse hairpin
    ]
    
    # Using TECHNICAL_TRACK type ensures proper screen fitting
    return RaceTrack(
        name="Monaco Street Circuit",
        track_type=TrackType.TECHNICAL_TRACK,
        total_length=4.1,
        segments=segments,
        weather_conditions="clear"
    )


def create_silverstone_track():
    """Create a Silverstone-style high-speed circuit"""
    segments = [
        TrackSegment(length=1200, is_straight=True),    # Hamilton straight
        TrackSegment(length=400, is_straight=False, corner_angle=60, corner_radius=150),  # Copse
        TrackSegment(length=800, is_straight=True),     # Wellington straight
        TrackSegment(length=350, is_straight=False, corner_angle=90, corner_radius=100),  # Brooklands
        TrackSegment(length=600, is_straight=True),
        TrackSegment(length=450, is_straight=False, corner_angle=120, corner_radius=80),  # Luffield
        TrackSegment(length=700, is_straight=True),
        TrackSegment(length=300, is_straight=False, corner_angle=45, corner_radius=200),  # Woodcote
    ]
    
    return RaceTrack(
        name="Silverstone Grand Prix",
        track_type=TrackType.SPEED_TRACK,
        total_length=5.9,
        segments=segments,
        weather_conditions="clear"
    )


def create_nurburgring_track():
    """Create a Nürburgring-style endurance circuit"""
    segments = [
        TrackSegment(length=2000, is_straight=True),    # Döttinger Höhe
        TrackSegment(length=500, is_straight=False, corner_angle=90, corner_radius=100),
        TrackSegment(length=800, is_straight=True),
        TrackSegment(length=600, is_straight=False, corner_angle=180, corner_radius=50),  # Carousel
        TrackSegment(length=1500, is_straight=True),
        TrackSegment(length=400, is_straight=False, corner_angle=45, corner_radius=150),
        TrackSegment(length=1000, is_straight=True),
        TrackSegment(length=700, is_straight=False, corner_angle=135, corner_radius=70),
        TrackSegment(length=1200, is_straight=True),
        TrackSegment(length=800, is_straight=False, corner_angle=90, corner_radius=90),
    ]
    
    return RaceTrack(
        name="Nürburgring Nordschleife",
        track_type=TrackType.ENDURANCE_TRACK,
        total_length=20.8,
        segments=segments,
        weather_conditions="clear"
    )


def create_suzuka_track():
    """Create a Suzuka-style figure-8 circuit"""
    segments = [
        TrackSegment(length=1000, is_straight=True),    # Start/finish
        TrackSegment(length=400, is_straight=False, corner_angle=90, corner_radius=120),  # Turn 1-2
        TrackSegment(length=500, is_straight=True),
        TrackSegment(length=600, is_straight=False, corner_angle=180, corner_radius=60),  # S-curves
        TrackSegment(length=700, is_straight=True),
        TrackSegment(length=350, is_straight=False, corner_angle=45, corner_radius=100),  # Dunlop
        TrackSegment(length=800, is_straight=True),     # Back straight
        TrackSegment(length=500, is_straight=False, corner_angle=135, corner_radius=40),  # Spoon
        TrackSegment(length=600, is_straight=True),
        TrackSegment(length=450, is_straight=False, corner_angle=90, corner_radius=80),   # 130R
    ]
    
    return RaceTrack(
        name="Suzuka International",
        track_type=TrackType.MIXED_TRACK,
        total_length=5.8,
        segments=segments,
        weather_conditions="clear"
    )


def create_rainbow_road_track():
    """Create a Mario Kart Rainbow Road style track"""
    segments = [
        TrackSegment(length=1500, is_straight=True),    # Launch straight
        TrackSegment(length=600, is_straight=False, corner_angle=270, corner_radius=100), # Loop
        TrackSegment(length=800, is_straight=True),
        TrackSegment(length=400, is_straight=False, corner_angle=90, corner_radius=150),  # Banking
        TrackSegment(length=1000, is_straight=True),    # Jump section
        TrackSegment(length=700, is_straight=False, corner_angle=180, corner_radius=50),  # Hairpin
        TrackSegment(length=900, is_straight=True),
        TrackSegment(length=500, is_straight=False, corner_angle=360, corner_radius=80),  # Corkscrew
    ]
    
    return RaceTrack(
        name="Rainbow Road",
        track_type=TrackType.MIXED_TRACK,
        total_length=7.4,
        segments=segments,
        weather_conditions="clear"
    )


def select_track():
    """Interactive track selection menu"""
    tracks = {
        "1": ("Monaco Street Circuit", create_monaco_track),
        "2": ("Silverstone Grand Prix", create_silverstone_track),
        "3": ("Nürburgring Nordschleife", create_nurburgring_track),
        "4": ("Suzuka International", create_suzuka_track),
        "5": ("Rainbow Road", create_rainbow_road_track),
    }
    
    print("\n🏁 SELECT YOUR TRACK:")
    print("=" * 50)
    for key, (name, _) in tracks.items():
        print(f"{key}. {name}")
    print("=" * 50)
    
    while True:
        choice = input("Enter track number (1-5): ").strip()
        if choice in tracks:
            track_name, track_creator = tracks[choice]
            print(f"\n✅ Selected: {track_name}")
            return track_creator()
        else:
            print("❌ Invalid choice. Please enter 1-5.")


def select_laps():
    """Interactive lap count selection"""
    print("\n🔄 SELECT NUMBER OF LAPS:")
    print("=" * 50)
    print("1. Sprint Race (3 laps)")
    print("2. Short Race (5 laps)")
    print("3. Standard Race (10 laps)")
    print("4. Long Race (20 laps)")
    print("5. Endurance Race (50 laps)")
    print("6. Custom")
    print("=" * 50)
    
    lap_options = {
        "1": 3,
        "2": 5,
        "3": 10,
        "4": 20,
        "5": 50
    }
    
    while True:
        choice = input("Enter choice (1-6): ").strip()
        if choice in lap_options:
            laps = lap_options[choice]
            print(f"\n✅ Selected: {laps} laps")
            return laps
        elif choice == "6":
            try:
                laps = int(input("Enter number of laps (1-100): "))
                if 1 <= laps <= 100:
                    print(f"\n✅ Selected: {laps} laps")
                    return laps
                else:
                    print("❌ Please enter a number between 1 and 100.")
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
        else:
            print("❌ Invalid choice. Please enter 1-6.")


def select_weather():
    """Weather selection menu"""
    print("\n🌤️ SELECT WEATHER CONDITIONS:")
    print("=" * 50)
    print("1. Clear ☀️")
    print("2. Rain 🌧️")
    print("3. Storm ⛈️")
    print("4. Random")
    print("=" * 50)
    
    weather_options = {
        "1": "clear",
        "2": "rain",
        "3": "storm",
        "4": "random"
    }
    
    while True:
        choice = input("Enter choice (1-4): ").strip()
        if choice in weather_options:
            weather = weather_options[choice]
            if weather == "random":
                import random
                weather = random.choice(["clear", "rain", "storm"])
                print(f"\n✅ Random weather selected: {weather}")
            else:
                print(f"\n✅ Selected: {weather}")
            return weather
        else:
            print("❌ Invalid choice. Please enter 1-4.")


def select_drivers():
    """Driver selection menu"""
    print("\n🤖 SELECT NUMBER OF DRIVERS:")
    print("=" * 50)
    print("1. 3 Drivers (Quick race)")
    print("2. 5 Drivers (Full grid)")
    print("=" * 50)
    
    while True:
        choice = input("Enter choice (1-2): ").strip()
        if choice == "1":
            print("\n✅ Selected: 3 drivers")
            return 3
        elif choice == "2":
            print("\n✅ Selected: 5 drivers")
            return 5
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")


def main():
    """Main menu system"""
    print("\n🏎️ AI RACING SIMULATOR - LLM GRAND PRIX")
    print("=" * 50)
    print("Welcome to the ultimate AI racing experience!")
    print("Configure your race and watch LLMs compete!")
    print("=" * 50)
    
    # Get race configuration
    track = select_track()
    laps = select_laps()
    weather = select_weather()
    num_drivers = select_drivers()
    
    # Update track weather
    track.weather_conditions = weather
    
    # Create LLM drivers
    print("\n🤖 Creating LLM drivers...")
    all_drivers = create_llm_drivers()
    drivers = all_drivers[:num_drivers]
    
    # Display race summary
    print("\n📋 RACE CONFIGURATION:")
    print("=" * 50)
    print(f"Track: {track.name} ({track.total_length:.1f} km)")
    print(f"Laps: {laps}")
    print(f"Weather: {weather}")
    print(f"Drivers: {num_drivers}")
    print("\nDrivers lineup:")
    for i, driver in enumerate(drivers, 1):
        print(f"  {i}. {driver.name} - {driver.car.name}")
    print("=" * 50)
    
    # Start race confirmation
    input("\nPress ENTER to start the race! 🏁")
    
    # Graphics settings
    graphics_settings = GraphicsSettings(
        width=1200,
        height=800,
        fps=60,
        show_telemetry=True,
        show_ai_thoughts=True
    )
    
    # Create and run simulator
    print("\n🏁 STARTING RACE...")
    simulator = LLMRaceSimulator(
        track=track,
        llm_drivers=drivers,
        laps=laps,
        enable_graphics=True,
        graphics_settings=graphics_settings
    )
    
    # Set the weather in the simulator
    simulator.weather = weather
    
    # Run the race
    results = simulator.simulate_race()
    
    # Display results
    if results and "finishing_order" in results:
        print("\n🏆 RACE RESULTS:")
        print("=" * 50)
        for driver in results["finishing_order"]:
            position = driver["position"]
            trophy = "🥇" if position == 1 else "🥈" if position == 2 else "🥉" if position == 3 else "🏁"
            print(f"{trophy} P{position}: {driver['name']} ({driver['model']}) - {driver['total_time']:.2f}s")
        print("=" * 50)
        
        # Ask if they want to race again
        again = input("\nRace again? (y/n): ").strip().lower()
        if again == 'y':
            main()
    else:
        print("\n❌ Race was interrupted or failed to complete.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for racing! See you next time!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()