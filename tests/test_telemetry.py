#!/usr/bin/env python3
"""
Test file for the Telemetry System - Phase 2
Demonstrates performance metrics collection and analysis
"""

from racing_car import RacingCar, DriverStyle
from race_track import RaceTrack
from race_simulator import RaceSimulator
import json


def create_test_racers():
    """Create a small set of racers for telemetry testing"""
    return [
        RacingCar("Speed Demon", 380, 3.2, 0.65, 10, DriverStyle.AGGRESSIVE),
        RacingCar("Tech Precision", 340, 4.5, 0.92, 14, DriverStyle.TECHNICAL),
        RacingCar("Adaptive Racer", 350, 4.0, 0.82, 13, DriverStyle.BALANCED)
    ]


def test_telemetry_collection():
    """Test basic telemetry collection during a race"""
    print("\n" + "="*60)
    print("TEST 1: Telemetry Collection During Race")
    print("="*60)
    
    # Setup
    racers = create_test_racers()
    track = RaceTrack.create_technical_track()  # Good for testing handling metrics
    
    # Run a short race with telemetry
    simulator = RaceSimulator(track, racers, laps=2, enable_telemetry=True)
    results = simulator.simulate_race()
    
    print("\n📊 TELEMETRY DATA COLLECTED:")
    
    # Get telemetry for each car
    for car in racers:
        summary = simulator.get_telemetry_summary(car.name)
        if summary:
            print(f"\n{car.name} ({summary['driver_style']}):")
            print(f"  Speed Metrics:")
            print(f"    Top Speed: {summary['speed']['top_speed']:.1f} km/h")
            print(f"    Average Speed: {summary['speed']['average']:.1f} km/h")
            print(f"    Speed Consistency: ±{summary['speed']['consistency']:.1f} km/h")
            print(f"    0-100 km/h: {summary['speed']['0_to_100']:.2f}s")
            
            print(f"  Handling Metrics:")
            print(f"    Cornering Efficiency: {summary['handling']['cornering_efficiency']:.2%}")
            print(f"    Stability Rating: {summary['handling']['stability']:.2f}")
            print(f"    Technical Precision: {summary['handling']['technical_precision']:.2f}")
            print(f"    Avg Corner Speed: {summary['handling']['avg_corner_speed']:.1f} km/h")


def test_performance_comparison():
    """Test performance comparison between different driver styles"""
    print("\n" + "="*60)
    print("TEST 2: Performance Comparison")
    print("="*60)
    
    # Create identical cars with different driver styles
    racers = [
        RacingCar("Aggressive Driver", 350, 4.0, 0.80, 12, DriverStyle.AGGRESSIVE),
        RacingCar("Technical Driver", 350, 4.0, 0.80, 12, DriverStyle.TECHNICAL),
        RacingCar("Conservative Driver", 350, 4.0, 0.80, 12, DriverStyle.CONSERVATIVE)
    ]
    
    track = RaceTrack.create_mixed_track()
    simulator = RaceSimulator(track, racers, laps=3, enable_telemetry=True)
    results = simulator.simulate_race()
    
    print("\n🔍 COMPARING IDENTICAL CARS WITH DIFFERENT STYLES:")
    
    # Compare aggressive vs technical
    comparison = simulator.compare_telemetry("Aggressive Driver", "Technical Driver")
    if comparison:
        print(f"\nAggressive vs Technical:")
        print(f"  Aggressive advantages: {', '.join(comparison['advantages']['Aggressive Driver'])}")
        print(f"  Technical advantages: {', '.join(comparison['advantages']['Technical Driver'])}")
    
    # Show key differences
    for car in racers:
        summary = simulator.get_telemetry_summary(car.name)
        if summary:
            print(f"\n{car.name}:")
            print(f"  Overtakes: {summary['strategic']['total_overtakes']}")
            print(f"  Risk Tolerance: {summary['strategic']['risk_tolerance']:.2f}")
            print(f"  Race Intelligence: {summary['strategic']['race_intelligence']:.2f}")
            print(f"  Error Rate: {summary['technical']['error_rate']:.2f} per lap")


def test_track_specific_metrics():
    """Test how different tracks affect performance metrics"""
    print("\n" + "="*60)
    print("TEST 3: Track-Specific Performance Analysis")
    print("="*60)
    
    # Use same car on different tracks
    test_car = RacingCar("Test Driver", 360, 3.8, 0.75, 12, DriverStyle.BALANCED)
    
    track_results = {}
    
    # Test on speed track
    print("\n🏁 Testing on Speed Track...")
    track = RaceTrack.create_speed_track()
    simulator = RaceSimulator(track, [test_car], laps=1, enable_telemetry=True)
    results = simulator.simulate_race()
    track_results["speed"] = simulator.get_telemetry_summary(test_car.name)
    
    # Reset car and test on technical track
    print("🏁 Testing on Technical Track...")
    test_car.reset_for_race()
    track = RaceTrack.create_technical_track()
    simulator = RaceSimulator(track, [test_car], laps=1, enable_telemetry=True)
    results = simulator.simulate_race()
    track_results["technical"] = simulator.get_telemetry_summary(test_car.name)
    
    # Compare results
    print("\n📈 TRACK-SPECIFIC PERFORMANCE:")
    
    print(f"\nSpeed Track Performance:")
    if track_results["speed"]:
        print(f"  Top Speed: {track_results['speed']['speed']['top_speed']:.1f} km/h")
        print(f"  Average Speed: {track_results['speed']['speed']['average']:.1f} km/h")
        print(f"  Fuel Efficiency: {track_results['speed']['efficiency']['fuel_efficiency']:.1f} km/l")
    
    print(f"\nTechnical Track Performance:")
    if track_results["technical"]:
        print(f"  Top Speed: {track_results['technical']['speed']['top_speed']:.1f} km/h")
        print(f"  Average Speed: {track_results['technical']['speed']['average']:.1f} km/h")
        print(f"  Cornering Efficiency: {track_results['technical']['handling']['cornering_efficiency']:.2%}")


def test_telemetry_export():
    """Test exporting telemetry data"""
    print("\n" + "="*60)
    print("TEST 4: Telemetry Export")
    print("="*60)
    
    # Quick race for data
    racers = create_test_racers()
    track = RaceTrack.create_mixed_track()
    simulator = RaceSimulator(track, racers, laps=2, enable_telemetry=True)
    results = simulator.simulate_race()
    
    # Export winner's telemetry
    winner = results["positions"][1]["name"]
    filename = f"telemetry_{winner.replace(' ', '_')}.json"
    simulator.export_telemetry(winner, filename)
    
    print(f"\n✅ Exported telemetry for {winner} to {filename}")
    
    # Load and display some data
    with open(filename, 'r') as f:
        data = json.load(f)
        print(f"\n📄 Sample exported data:")
        print(f"  Car: {data['car_name']}")
        print(f"  Driver Style: {data['driver_style']}")
        print(f"  Top Speed: {data['speed']['top_speed']:.1f} km/h")
        print(f"  Race Intelligence: {data['strategic']['race_intelligence']:.2f}")


def test_comprehensive_metrics():
    """Test all metric categories with a longer race"""
    print("\n" + "="*60)
    print("TEST 5: Comprehensive Metrics (5-lap race)")
    print("="*60)
    
    racers = [
        RacingCar("Speed Demon", 380, 3.2, 0.65, 10, DriverStyle.AGGRESSIVE),
        RacingCar("Tech Precision", 340, 4.5, 0.92, 14, DriverStyle.TECHNICAL),
        RacingCar("Fuel Master", 320, 5.2, 0.78, 18, DriverStyle.CONSERVATIVE),
        RacingCar("Adaptive Racer", 350, 4.0, 0.82, 13, DriverStyle.BALANCED),
        RacingCar("Chaos Cruiser", 360, 3.8, 0.75, 11, DriverStyle.CHAOTIC)
    ]
    
    track = RaceTrack.create_endurance_track()
    simulator = RaceSimulator(track, racers, laps=5, enable_telemetry=True)
    results = simulator.simulate_race()
    
    print("\n📊 COMPREHENSIVE METRICS SUMMARY:")
    
    # Show detailed metrics for top 3
    for pos in range(1, 4):
        if pos in results["positions"]:
            car_name = results["positions"][pos]["name"]
            summary = simulator.get_telemetry_summary(car_name)
            
            if summary:
                print(f"\n{'='*40}")
                print(f"Position {pos}: {car_name}")
                print(f"{'='*40}")
                
                # Speed metrics
                print("SPEED METRICS:")
                for key, value in summary["speed"].items():
                    if isinstance(value, float):
                        print(f"  {key}: {value:.2f}")
                
                # Efficiency metrics
                print("\nEFFICIENCY METRICS:")
                print(f"  Fuel Efficiency: {summary['efficiency']['fuel_efficiency']:.2f} km/l")
                print(f"  Endurance Rating: {summary['efficiency']['endurance']:.2f}")
                print(f"  Energy per Lap: {summary['efficiency']['energy_per_lap']:.2f}%")
                
                # Strategic metrics
                print("\nSTRATEGIC METRICS:")
                print(f"  Overtaking Ability: {summary['strategic']['overtaking']:.2%}")
                print(f"  Risk Tolerance: {summary['strategic']['risk_tolerance']:.2f}")
                print(f"  Race Intelligence: {summary['strategic']['race_intelligence']:.2f}")
                print(f"  Total Overtakes: {summary['strategic']['total_overtakes']}")
                
                # Technical metrics
                print("\nTECHNICAL METRICS:")
                print(f"  Lap Consistency: ±{summary['technical']['consistency']:.2f}s")
                print(f"  Error Rate: {summary['technical']['error_rate']:.2f}/lap")
                print(f"  Recovery Speed: {summary['technical']['recovery']:.2f}")


def main():
    """Run all telemetry tests"""
    print("\n🏎️  AI RACING SIMULATOR - PHASE 2: TELEMETRY TESTS 🏎️")
    
    test_telemetry_collection()
    test_performance_comparison()
    test_track_specific_metrics()
    test_telemetry_export()
    test_comprehensive_metrics()
    
    print("\n" + "="*60)
    print("✅ Phase 2 Complete: Performance Metrics System Implemented!")
    print("="*60)
    print("\nKey Features Demonstrated:")
    print("- Real-time telemetry collection during races")
    print("- Comprehensive performance metrics across 5 categories")
    print("- Driver style impact on performance")
    print("- Track-specific performance analysis")
    print("- Telemetry export and comparison tools")
    print("- Data ready for Phase 5 prize distribution system")
    
    # Clean up test file
    import os
    try:
        os.remove("telemetry_Speed_Demon.json")
    except:
        pass


if __name__ == "__main__":
    main()