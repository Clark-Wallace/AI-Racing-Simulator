#!/usr/bin/env python3
"""
Test file for the Data Prize Distribution System - Phase 4
Demonstrates telemetry data access rights and competitor intelligence
"""

from src.core.racing_car import RacingCar, DriverStyle
from src.core.race_track import RaceTrack
from src.core.race_simulator import RaceSimulator
from src.intelligence.data_prizes import DataPrizeSystem, AccessLevel
from src.systems.challenge_generator import RaceChallengeGenerator, ChallengeType, ChallengeDifficulty
import json


def create_test_racers():
    """Create racers for testing data prizes"""
    return [
        RacingCar("Speed Demon", 380, 3.2, 0.65, 10, DriverStyle.AGGRESSIVE),
        RacingCar("Tech Precision", 340, 4.5, 0.92, 14, DriverStyle.TECHNICAL),
        RacingCar("Fuel Master", 320, 5.2, 0.78, 18, DriverStyle.CONSERVATIVE),
        RacingCar("Adaptive Racer", 350, 4.0, 0.82, 13, DriverStyle.BALANCED),
        RacingCar("Chaos Cruiser", 360, 3.8, 0.75, 11, DriverStyle.CHAOTIC)
    ]


def test_basic_prize_distribution():
    """Test basic data prize distribution after a race"""
    print("\n" + "="*60)
    print("TEST 1: Basic Prize Distribution")
    print("="*60)
    
    # Run a race
    racers = create_test_racers()
    track = RaceTrack.create_mixed_track()
    simulator = RaceSimulator(track, racers, laps=3, enable_telemetry=True)
    results = simulator.simulate_race()
    
    # Initialize prize system
    prize_system = DataPrizeSystem()
    
    # Distribute prizes
    prize_system.distribute_prizes(results, simulator.telemetry)
    
    print("\n🏆 DATA PRIZE DISTRIBUTION:")
    print("\nRace Results:")
    for pos, data in results["positions"].items():
        print(f"  {pos}. {data['name']}")
    
    print("\n📊 Access Rights Granted:")
    for access in prize_system.access_rights:
        if access.accessor != access.target:  # Skip self-access
            print(f"  {access.accessor} → {access.target}: {access.level.value} access")
            print(f"    Reason: {access.reason}")
    
    # Test access levels
    print("\n🔍 Testing Access Levels:")
    
    # 1st place should have access to 4th and 5th
    winner = results["positions"][1]["name"]
    if 4 in results["positions"]:
        fourth = results["positions"][4]["name"]
        data = prize_system.get_accessible_data(winner, fourth)
        if data:
            print(f"\n{winner} accessing {fourth}'s data:")
            print(f"  Driver Style: {data['driver_style']}")
            print(f"  Average Top Speed: {data['average_metrics']['speed']['top_speed']:.1f} km/h")
            print(f"  Weaknesses: {', '.join(data['weaknesses']) if data['weaknesses'] else 'None identified'}")


def test_competitor_intelligence():
    """Test competitor intelligence analysis"""
    print("\n" + "="*60)
    print("TEST 2: Competitor Intelligence Analysis")
    print("="*60)
    
    # Run multiple races to build data
    racers = create_test_racers()
    prize_system = DataPrizeSystem()
    
    print("\n🏁 Running 3 races to build intelligence data...")
    
    for i in range(3):
        # Vary track types
        if i == 0:
            track = RaceTrack.create_speed_track()
        elif i == 1:
            track = RaceTrack.create_technical_track()
        else:
            track = RaceTrack.create_mixed_track()
            
        simulator = RaceSimulator(track, racers, laps=2, enable_telemetry=True)
        results = simulator.simulate_race()
        prize_system.distribute_prizes(results, simulator.telemetry)
        
        print(f"  Race {i+1} on {track.name}: Winner - {results['positions'][1]['name']}")
    
    # Analyze competitors
    print("\n🕵️ COMPETITOR INTELLIGENCE REPORTS:")
    
    # Get winner from last race
    winner = results["positions"][1]["name"]
    
    # Analyze each competitor the winner has access to
    spy_network = prize_system.get_spy_network()
    if winner in spy_network:
        for target in spy_network[winner]:
            intelligence = prize_system.analyze_competitor(winner, target)
            if intelligence:
                print(f"\n📋 Intelligence Report: {target}")
                print(f"  Driver Style: {intelligence.driver_style}")
                print(f"  Strengths: {', '.join(intelligence.strengths) if intelligence.strengths else 'Unknown'}")
                print(f"  Weaknesses: {', '.join(intelligence.weaknesses) if intelligence.weaknesses else 'Unknown'}")
                print(f"  Behavioral Patterns:")
                for pattern in intelligence.behavioral_patterns[:3]:  # Show first 3
                    print(f"    - {pattern}")
                print(f"  Recommended Counter-Strategies:")
                for strategy in intelligence.recommended_strategies[:3]:  # Show first 3
                    print(f"    → {strategy}")


def test_spy_network_visualization():
    """Test spy network visualization"""
    print("\n" + "="*60)
    print("TEST 3: Spy Network Visualization")
    print("="*60)
    
    # Run a race with challenges for varied results
    racers = create_test_racers()
    generator = RaceChallengeGenerator()
    
    # Run a Formula race
    challenge_config = generator.generate_challenge(ChallengeType.FORMULA_RACE, ChallengeDifficulty.MEDIUM)
    challenge_result = generator.run_challenge(challenge_config, racers)
    
    # Create prize system and distribute
    prize_system = DataPrizeSystem()
    
    # Convert challenge result to race result format
    race_results = {
        "track": challenge_config.name,
        "positions": {}
    }
    for pos, car_name in challenge_result.rankings.items():
        race_results["positions"][pos] = {"name": car_name}
    
    prize_system.distribute_prizes(race_results, None)  # No telemetry for visualization test
    
    # Get spy network
    spy_network = prize_system.get_spy_network()
    
    print("\n🕸️  SPY NETWORK - Who Has Access to Whose Data:")
    print("\n    " + "  ".join(f"{name:15}" for name in racers[:5]))
    print("    " + "-"*80)
    
    for i, accessor in enumerate([car.name for car in racers]):
        row = f"{accessor:15} "
        for j, target in enumerate([car.name for car in racers]):
            if accessor == target:
                row += " [SELF]        "
            elif target in spy_network.get(accessor, set()):
                # Get access level
                level = "?"
                for access in prize_system.access_rights:
                    if access.accessor == accessor and access.target == target:
                        if access.level == AccessLevel.FULL:
                            level = "FULL"
                        elif access.level == AccessLevel.DETAILED:
                            level = "DETAIL"
                        elif access.level == AccessLevel.BASIC:
                            level = "BASIC"
                        break
                row += f" {level:6}        "
            else:
                row += "   -           "
        print(row)
    
    print("\n📝 Legend: FULL = Complete telemetry, DETAIL = Detailed metrics, BASIC = Summary only")


def test_access_history():
    """Test access history tracking"""
    print("\n" + "="*60)
    print("TEST 4: Access History Tracking")
    print("="*60)
    
    racers = create_test_racers()
    prize_system = DataPrizeSystem()
    
    # Run 2 quick races
    for i in range(2):
        track = RaceTrack.create_speed_track() if i == 0 else RaceTrack.create_technical_track()
        simulator = RaceSimulator(track, racers[:3], laps=1, enable_telemetry=True)  # Just 3 racers
        results = simulator.simulate_race()
        prize_system.distribute_prizes(results, simulator.telemetry)
    
    # Check access history for first racer
    car_name = racers[0].name
    history = prize_system.get_access_history(car_name)
    
    print(f"\n📜 Access History for {car_name}:")
    for access in history[:10]:  # Show last 10
        if access.accessor == car_name:
            print(f"  → Gained access to {access.target}'s data ({access.level.value})")
        else:
            print(f"  ← {access.accessor} gained access to your data ({access.level.value})")
        print(f"     Race: {access.race_name}")
        print(f"     Reason: {access.reason}")


def test_strategic_advantages():
    """Test how data access provides strategic advantages"""
    print("\n" + "="*60)
    print("TEST 5: Strategic Advantages from Data Access")
    print("="*60)
    
    # Create specific scenario
    racers = [
        RacingCar("Aggressive Andy", 380, 3.2, 0.65, 10, DriverStyle.AGGRESSIVE),
        RacingCar("Technical Tom", 340, 4.5, 0.92, 14, DriverStyle.TECHNICAL),
        RacingCar("Consistent Carl", 350, 4.0, 0.82, 13, DriverStyle.BALANCED)
    ]
    
    prize_system = DataPrizeSystem()
    
    # Run races on different track types
    track_types = [
        ("Speed Track", RaceTrack.create_speed_track()),
        ("Technical Track", RaceTrack.create_technical_track()),
        ("Mixed Track", RaceTrack.create_mixed_track())
    ]
    
    print("\n🏁 Running races on different track types...")
    
    for track_name, track in track_types:
        simulator = RaceSimulator(track, racers, laps=3, enable_telemetry=True)
        results = simulator.simulate_race()
        prize_system.distribute_prizes(results, simulator.telemetry)
        
        winner = results["positions"][1]["name"]
        print(f"\n{track_name}: {winner} wins!")
    
    # Now show strategic insights
    print("\n💡 STRATEGIC INSIGHTS FROM DATA:")
    
    # Check who has most intelligence
    spy_network = prize_system.get_spy_network()
    for accessor_name, targets in spy_network.items():
        if len(targets) > 0:
            print(f"\n{accessor_name} has intelligence on: {', '.join(targets)}")
            
            # Show key insights about each target
            for target in targets:
                data = prize_system.get_accessible_data(accessor_name, target)
                if data and "preferred_track_type" in data:
                    print(f"  → {target} prefers: {data['preferred_track_type']}")
                    
                intelligence = prize_system.analyze_competitor(accessor_name, target)
                if intelligence and intelligence.recommended_strategies:
                    print(f"  → Best strategy vs {target}: {intelligence.recommended_strategies[0]}")


def test_intelligence_export():
    """Test exporting intelligence reports"""
    print("\n" + "="*60)
    print("TEST 6: Intelligence Report Export")
    print("="*60)
    
    # Quick setup
    racers = create_test_racers()[:3]
    track = RaceTrack.create_mixed_track()
    simulator = RaceSimulator(track, racers, laps=2, enable_telemetry=True)
    results = simulator.simulate_race()
    
    prize_system = DataPrizeSystem()
    prize_system.distribute_prizes(results, simulator.telemetry)
    
    # Export intelligence report
    winner = results["positions"][1]["name"]
    if 3 in results["positions"]:
        target = results["positions"][3]["name"]
        
        if winner in prize_system.get_spy_network() and target in prize_system.get_spy_network()[winner]:
            filename = f"intelligence_{target.replace(' ', '_')}.json"
            success = prize_system.export_intelligence_report(winner, target, filename)
            
            if success:
                print(f"\n✅ Intelligence report exported to: {filename}")
                
                # Read and display part of it
                with open(filename, 'r') as f:
                    report = json.load(f)
                    print(f"\n📄 Report Preview:")
                    print(f"  Target: {report['intelligence']['competitor_name']}")
                    print(f"  Access Level: {report['access_level']}")
                    print(f"  Identified Weaknesses: {len(report['intelligence']['weaknesses'])}")
                    print(f"  Strategic Recommendations: {len(report['intelligence']['recommended_strategies'])}")
                
                # Clean up
                import os
                os.remove(filename)


def main():
    """Run all data prize tests"""
    print("\n🏎️  AI RACING SIMULATOR - PHASE 4: DATA PRIZE SYSTEM TESTS 🏎️")
    
    test_basic_prize_distribution()
    test_competitor_intelligence()
    test_spy_network_visualization()
    test_access_history()
    test_strategic_advantages()
    test_intelligence_export()
    
    print("\n" + "="*60)
    print("✅ Phase 4 Complete: Data Prize Distribution System Implemented!")
    print("="*60)
    print("\nKey Features Demonstrated:")
    print("- Position-based data access rights (1st gets 4th+5th, etc.)")
    print("- Three access levels: Basic, Detailed, Full")
    print("- Competitor intelligence analysis")
    print("- Behavioral pattern recognition")
    print("- Strategic counter-recommendations")
    print("- Spy network visualization")
    print("- Access history tracking")
    print("- Intelligence report export")
    
    print("\n🎯 Strategic Value:")
    print("- Winners gain valuable insights into competitor weaknesses")
    print("- Data accumulates over multiple races for deeper analysis")
    print("- Creates interesting risk/reward dynamics")
    print("- Encourages strategic racing for data collection")


if __name__ == "__main__":
    main()