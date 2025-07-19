#!/usr/bin/env python3
"""
Test file for the AI Racing Simulator
Demonstrates all core functionality from Phase 1
"""

from src.core.racing_car import RacingCar, DriverStyle
from src.core.race_track import RaceTrack, TrackType
from src.core.race_simulator import RaceSimulator


def create_ai_racers():
    """Create the 5 AI racing personalities"""
    racers = [
        RacingCar(
            name="Speed Demon",
            top_speed=380,
            acceleration=3.2,
            handling=0.65,
            fuel_efficiency=10,
            driver_style=DriverStyle.AGGRESSIVE
        ),
        RacingCar(
            name="Tech Precision",
            top_speed=340,
            acceleration=4.5,
            handling=0.92,
            fuel_efficiency=14,
            driver_style=DriverStyle.TECHNICAL
        ),
        RacingCar(
            name="Fuel Master",
            top_speed=320,
            acceleration=5.2,
            handling=0.78,
            fuel_efficiency=18,
            driver_style=DriverStyle.CONSERVATIVE
        ),
        RacingCar(
            name="Adaptive Racer",
            top_speed=350,
            acceleration=4.0,
            handling=0.82,
            fuel_efficiency=13,
            driver_style=DriverStyle.BALANCED
        ),
        RacingCar(
            name="Chaos Cruiser",
            top_speed=360,
            acceleration=3.8,
            handling=0.75,
            fuel_efficiency=11,
            driver_style=DriverStyle.CHAOTIC
        )
    ]
    return racers


def test_car_creation():
    """Test car creation and basic functionality"""
    print("\n" + "="*60)
    print("TEST 1: Car Creation and Properties")
    print("="*60)
    
    racers = create_ai_racers()
    
    for car in racers:
        print(f"\n{car.name}:")
        print(f"  Driver Style: {car.driver_style.value}")
        print(f"  Top Speed: {car.top_speed} km/h")
        print(f"  Acceleration: {car.acceleration}s (0-100)")
        print(f"  Handling: {car.handling:.2f}")
        print(f"  Fuel Efficiency: {car.fuel_efficiency} km/l")
        
        # Test style modifiers
        mods = car.get_style_modifiers()
        print(f"  Style Effects:")
        print(f"    Speed Bonus: {(mods['speed_bonus']-1)*100:+.0f}%")
        print(f"    Handling: {(mods['handling_penalty']-1)*100:+.0f}%")
        print(f"    Risk Factor: {mods['risk_factor']}")


def test_track_creation():
    """Test track creation and properties"""
    print("\n" + "="*60)
    print("TEST 2: Track Creation and Properties")
    print("="*60)
    
    tracks = [
        RaceTrack.create_speed_track(),
        RaceTrack.create_technical_track(),
        RaceTrack.create_mixed_track(),
        RaceTrack.create_endurance_track()
    ]
    
    for track in tracks:
        print(f"\n{track.name}:")
        print(f"  Type: {track.track_type.value}")
        print(f"  Length: {track.total_length:.2f} km")
        print(f"  Segments: {len(track.segments)}")
        
        # Count straights vs corners
        straights = sum(1 for s in track.segments if s.is_straight)
        corners = len(track.segments) - straights
        print(f"  Straights: {straights}, Corners: {corners}")
        
        # Get characteristics
        chars = track.get_track_characteristics()
        print(f"  Description: {chars['description']}")
        print(f"  Key Requirements:")
        print(f"    Speed: {chars['speed_importance']*100:.0f}%")
        print(f"    Handling: {chars['handling_importance']*100:.0f}%")
        print(f"    Fuel: {chars['fuel_importance']*100:.0f}%")


def test_quick_race():
    """Test a quick 3-lap race"""
    print("\n" + "="*60)
    print("TEST 3: Quick Race Simulation (3 laps)")
    print("="*60)
    
    # Create racers and track
    racers = create_ai_racers()
    track = RaceTrack.create_mixed_track()
    
    # Run race
    simulator = RaceSimulator(track, racers, laps=3)
    results = simulator.simulate_race()
    
    # Print summary
    simulator.print_race_summary(results)


def test_different_tracks():
    """Test how different cars perform on different tracks"""
    print("\n" + "="*60)
    print("TEST 4: Track Suitability Analysis")
    print("="*60)
    
    racers = create_ai_racers()
    
    # Test each track type with 1 lap
    track_types = [
        ("Speed Track", RaceTrack.create_speed_track()),
        ("Technical Track", RaceTrack.create_technical_track()),
        ("Mixed Track", RaceTrack.create_mixed_track()),
    ]
    
    for track_name, track in track_types:
        print(f"\n{track_name} Results (1 lap):")
        
        # Quick 1-lap race
        for car in racers:
            car.reset_for_race()
        
        simulator = RaceSimulator(track, racers, laps=1)
        results = simulator.simulate_race()
        
        # Show top 3
        for pos in range(1, 4):
            if pos in results["positions"]:
                data = results["positions"][pos]
                print(f"  {pos}. {data['name']} - {data['total_time']:.2f}s")


def test_weather_effects():
    """Test weather effects on racing"""
    print("\n" + "="*60)
    print("TEST 5: Weather Effects")
    print("="*60)
    
    racers = create_ai_racers()[:3]  # Just use 3 cars for brevity
    
    # Create track with different weather
    track_clear = RaceTrack.create_technical_track()
    track_rain = RaceTrack(
        name="Monaco Technical Circuit (Rain)",
        track_type=TrackType.TECHNICAL_TRACK,
        total_length=track_clear.total_length,
        segments=track_clear.segments,
        weather_conditions="rain"
    )
    
    # Race in clear weather
    print("\nClear Weather (1 lap):")
    for car in racers:
        car.reset_for_race()
    sim_clear = RaceSimulator(track_clear, racers, laps=1)
    results_clear = sim_clear.simulate_race()
    
    for pos in range(1, 4):
        if pos in results_clear["positions"]:
            data = results_clear["positions"][pos]
            print(f"  {pos}. {data['name']} - {data['total_time']:.2f}s")
    
    # Race in rain
    print("\nRainy Weather (1 lap):")
    for car in racers:
        car.reset_for_race()
    sim_rain = RaceSimulator(track_rain, racers, laps=1)
    results_rain = sim_rain.simulate_race()
    
    for pos in range(1, 4):
        if pos in results_rain["positions"]:
            data = results_rain["positions"][pos]
            print(f"  {pos}. {data['name']} - {data['total_time']:.2f}s")
    
    print("\nNote: Rain reduces speed by 15% and handling by 30%")


def main():
    """Run all tests"""
    print("\n🏎️  AI RACING SIMULATOR - PHASE 1 TESTS 🏎️")
    
    test_car_creation()
    test_track_creation()
    test_quick_race()
    test_different_tracks()
    test_weather_effects()
    
    print("\n" + "="*60)
    print("✅ Phase 1 Complete: Core Racing Engine Implemented!")
    print("="*60)
    print("\nNext Phase: Performance Metrics System")
    print("- Detailed telemetry tracking")
    print("- Real-time performance analysis")
    print("- Data collection for prize system")


if __name__ == "__main__":
    main()