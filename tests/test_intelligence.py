#!/usr/bin/env python3
"""
Test file for the Racing Intelligence System - Phase 5
Demonstrates enhanced AI decision-making with competitor intelligence
"""

from racing_car import RacingCar, DriverStyle
from race_track import RaceTrack
from race_simulator import RaceSimulator
from intelligent_race_simulator import IntelligentRaceSimulator
from data_prizes import DataPrizeSystem
from challenge_generator import RaceChallengeGenerator, ChallengeType, ChallengeDifficulty


def create_test_racers():
    """Create racers for intelligence testing"""
    return [
        RacingCar("Speed Demon", 380, 3.2, 0.65, 10, DriverStyle.AGGRESSIVE),
        RacingCar("Tech Precision", 340, 4.5, 0.92, 14, DriverStyle.TECHNICAL),
        RacingCar("Fuel Master", 320, 5.2, 0.78, 18, DriverStyle.CONSERVATIVE),
        RacingCar("Adaptive Racer", 350, 4.0, 0.82, 13, DriverStyle.BALANCED),
        RacingCar("Chaos Cruiser", 360, 3.8, 0.75, 11, DriverStyle.CHAOTIC)
    ]


def test_basic_intelligence():
    """Test basic intelligent racing"""
    print("\n" + "="*60)
    print("TEST 1: Basic Intelligent Racing")
    print("="*60)
    
    racers = create_test_racers()
    track = RaceTrack.create_mixed_track()
    
    # Run race without intelligence
    print("\n🏁 STANDARD RACE (No Intelligence):")
    standard_sim = RaceSimulator(track, racers, laps=3, enable_telemetry=True)
    standard_results = standard_sim.simulate_race()
    
    print("\nStandard Race Results:")
    for pos, data in standard_results["positions"].items():
        print(f"  {pos}. {data['name']} - {data['total_time']:.1f}s")
    
    # Reset cars and run with intelligence
    for car in racers:
        car.reset_for_race()
        
    print("\n🧠 INTELLIGENT RACE:")
    intel_sim = IntelligentRaceSimulator(track, racers, laps=3, enable_telemetry=True, 
                                       enable_intelligence=True)
    intel_results = intel_sim.simulate_race()
    
    print("\nIntelligent Race Results:")
    for pos, data in intel_results["positions"].items():
        print(f"  {pos}. {data['name']} - {data['total_time']:.1f}s")
    
    # Compare overtaking
    standard_overtakes = len([e for e in standard_results["events"] if e.event_type == "OVERTAKE"])
    intel_overtakes = len([e for e in intel_results["events"] if e.event_type in ["OVERTAKE", "INTELLIGENT_OVERTAKE"]])
    
    print(f"\n📊 Comparison:")
    print(f"  Standard race overtakes: {standard_overtakes}")
    print(f"  Intelligent race overtakes: {intel_overtakes}")


def test_intelligence_with_data():
    """Test intelligence system with competitor data"""
    print("\n" + "="*60)
    print("TEST 2: Intelligence with Competitor Data")
    print("="*60)
    
    racers = create_test_racers()
    prize_system = DataPrizeSystem()
    
    # Build up competitor data with multiple races
    print("\n📊 Building competitor intelligence database...")
    
    for i in range(3):
        track = [RaceTrack.create_speed_track(), 
                RaceTrack.create_technical_track(),
                RaceTrack.create_mixed_track()][i]
        
        sim = RaceSimulator(track, racers, laps=2, enable_telemetry=True)
        results = sim.simulate_race()
        prize_system.distribute_prizes(results, sim.telemetry)
        
        print(f"  Race {i+1} winner: {results['positions'][1]['name']}")
    
    # Now run intelligent race with accumulated data
    print("\n🧠 INTELLIGENT RACE WITH COMPETITOR DATA:")
    
    for car in racers:
        car.reset_for_race()
        
    track = RaceTrack.create_mixed_track()
    intel_sim = IntelligentRaceSimulator(track, racers, laps=5, enable_telemetry=True,
                                       enable_intelligence=True, prize_system=prize_system)
    results = intel_sim.simulate_race()
    
    # Show intelligence usage
    print("\n💡 Intelligence-Based Decisions:")
    if "intelligence_metrics" in results:
        for car_name, metrics in results["intelligence_metrics"].items():
            if metrics["successful_overtakes"] > 0 or metrics["failed_overtakes"] > 0:
                success_rate = (metrics["successful_overtakes"] / 
                              (metrics["successful_overtakes"] + metrics["failed_overtakes"]) * 100)
                print(f"  {car_name}: {success_rate:.0f}% overtake success rate")


def test_tactical_decisions():
    """Test specific tactical decision scenarios"""
    print("\n" + "="*60)
    print("TEST 3: Tactical Decision Making")
    print("="*60)
    
    # Create specific scenario - close racing
    racers = [
        RacingCar("Leader", 350, 4.0, 0.82, 13, DriverStyle.BALANCED),
        RacingCar("Attacker", 360, 3.8, 0.75, 11, DriverStyle.AGGRESSIVE),
        RacingCar("Defender", 340, 4.5, 0.85, 14, DriverStyle.TECHNICAL)
    ]
    
    # Short sprint race to see tactical decisions
    track = RaceTrack.create_speed_track()
    intel_sim = IntelligentRaceSimulator(track, racers, laps=2, enable_telemetry=True,
                                       enable_intelligence=True)
    results = intel_sim.simulate_race()
    
    print("\n🎯 Tactical Events:")
    tactical_events = [e for e in results["events"] 
                      if any(keyword in e.event_type for keyword in 
                            ["INTELLIGENT", "OVERTAKE", "DEFEND", "PRESSURE"])]
    
    for event in tactical_events[:10]:  # Show first 10
        print(f"  {event.time:.1f}s - {event.car_name}: {event.details}")
    
    # Show final strategies
    print("\n📋 Final Strategy Analysis:")
    if "intelligence_metrics" in results:
        for car_name, metrics in results["intelligence_metrics"].items():
            print(f"  {car_name}: {metrics['strategy']} strategy")


def test_psychological_warfare():
    """Test psychological tactics between competitors"""
    print("\n" + "="*60)
    print("TEST 4: Psychological Warfare")
    print("="*60)
    
    # Create rivals with history
    racers = create_test_racers()[:3]  # Just 3 for clarity
    prize_system = DataPrizeSystem()
    
    # Build rivalry with multiple encounters
    print("\n🥊 Building rivalry history...")
    
    for i in range(5):
        track = RaceTrack.create_technical_track()  # Technical tracks for close racing
        sim = RaceSimulator(track, racers, laps=3, enable_telemetry=True)
        results = sim.simulate_race()
        prize_system.distribute_prizes(results, sim.telemetry)
        
        # Track positions
        positions = {data["name"]: pos for pos, data in results["positions"].items()}
        print(f"  Race {i+1}: 1.{results['positions'][1]['name']} "
              f"2.{results['positions'][2]['name']} 3.{results['positions'][3]['name']}")
    
    # Final showdown with intelligence
    print("\n🏁 FINAL SHOWDOWN WITH PSYCHOLOGICAL TACTICS:")
    
    for car in racers:
        car.reset_for_race()
        
    track = RaceTrack.create_mixed_track()
    intel_sim = IntelligentRaceSimulator(track, racers, laps=5, enable_telemetry=True,
                                       enable_intelligence=True, prize_system=prize_system)
    results = intel_sim.simulate_race()
    
    # Analyze psychological tactics used
    print("\n🧠 Psychological Tactics Analysis:")
    
    # Check competitor profiles
    for car in racers:
        intel = prize_system.get_spy_network()
        if car.name in intel and intel[car.name]:
            print(f"\n{car.name} has intelligence on: {list(intel[car.name])}")
            
            # Show what they learned
            for target in intel[car.name]:
                competitor_intel = prize_system.analyze_competitor(car.name, target)
                if competitor_intel and competitor_intel.behavioral_patterns:
                    print(f"  vs {target}: Identified '{competitor_intel.behavioral_patterns[0]}'")


def test_adaptive_strategies():
    """Test how AI adapts strategies during race"""
    print("\n" + "="*60)
    print("TEST 5: Adaptive Strategy Changes")
    print("="*60)
    
    racers = create_test_racers()
    
    # Create challenging conditions - endurance race
    track = RaceTrack.create_endurance_track()
    intel_sim = IntelligentRaceSimulator(track, racers, laps=10, enable_telemetry=True,
                                       enable_intelligence=True)
    
    print("\n🏁 ENDURANCE RACE - Watch Strategy Adaptations:")
    results = intel_sim.simulate_race()
    
    print("\n📈 Strategy Evolution:")
    if "intelligence_metrics" in results:
        for car_name, metrics in results["intelligence_metrics"].items():
            print(f"\n{car_name}:")
            print(f"  Initial Strategy: {metrics['strategy']}")
            print(f"  Target Position: P{metrics['target_position']}")
            print(f"  Final Risk Tolerance: {metrics['final_risk_tolerance']:.2f}")
            
            # Show if they met their target
            final_pos = next(pos for pos, data in results["positions"].items() 
                           if data["name"] == car_name)
            target_met = "✅" if final_pos <= metrics['target_position'] else "❌"
            print(f"  Target Met: {target_met} (Finished P{final_pos})")


def test_challenge_intelligence():
    """Test intelligence in specific challenge scenarios"""
    print("\n" + "="*60)
    print("TEST 6: Intelligence in Challenge Scenarios")
    print("="*60)
    
    racers = create_test_racers()
    prize_system = DataPrizeSystem()
    generator = RaceChallengeGenerator()
    
    # Run a pursuit challenge with intelligence
    print("\n🎯 PURSUIT CHALLENGE WITH INTELLIGENCE:")
    
    challenge = generator.generate_challenge(ChallengeType.PURSUIT_RACE, ChallengeDifficulty.MEDIUM)
    
    # Custom implementation for pursuit with intelligence
    track = RaceTrack.create_mixed_track()
    
    # Give leader a head start
    leader = racers[0]
    leader.distance_traveled = 500  # 500m head start
    
    intel_sim = IntelligentRaceSimulator(track, racers, laps=5, enable_telemetry=True,
                                       enable_intelligence=True, prize_system=prize_system)
    
    print(f"\nChallenge: {challenge.name}")
    print(f"Description: {challenge.description}")
    print(f"Leader: {leader.name} with 500m head start")
    
    results = intel_sim.simulate_race()
    
    # Check if pursuit was successful
    print("\n🏆 PURSUIT RESULT:")
    winner = results["positions"][1]["name"]
    if winner == leader.name:
        print(f"  Leader {leader.name} ESCAPED! Held off all challengers.")
    else:
        print(f"  {winner} CAUGHT the leader! Successful pursuit.")
        
    # Show key pursuit moments
    print("\n🔍 Key Pursuit Moments:")
    pursuit_events = [e for e in results["events"] 
                     if "OVERTAKE" in e.event_type and leader.name in e.details]
    for event in pursuit_events:
        print(f"  {event.time:.1f}s - {event.details}")


def main():
    """Run all intelligence tests"""
    print("\n🏎️  AI RACING SIMULATOR - PHASE 5: RACING INTELLIGENCE TESTS 🏎️")
    
    test_basic_intelligence()
    test_intelligence_with_data()
    test_tactical_decisions()
    test_psychological_warfare()
    test_adaptive_strategies()
    test_challenge_intelligence()
    
    print("\n" + "="*60)
    print("✅ Phase 5 Complete: Racing Intelligence System Implemented!")
    print("="*60)
    print("\nKey Features Demonstrated:")
    print("- Pre-race strategic planning based on AI analysis")
    print("- Real-time tactical decision making")
    print("- Adaptive behavior using competitor intelligence")
    print("- Psychological pressure tactics")
    print("- Learning from failed/successful overtakes")
    print("- Mid-race strategy adjustments")
    print("- Predictive opponent modeling")
    
    print("\n🧠 Intelligence Capabilities:")
    print("- ATTACK: Aggressive overtaking with calculated risks")
    print("- DEFEND: Blocking and defensive positioning")
    print("- CONSERVE: Resource management for endurance")
    print("- PRESSURE: Psychological tactics to force errors")
    print("- SLIPSTREAM: Drafting for speed advantage")
    
    print("\n💡 Strategic Impact:")
    print("- AI racers now make informed decisions")
    print("- Past race data influences future behavior")
    print("- Creates emergent rivalries and grudges")
    print("- More realistic and unpredictable racing!")


if __name__ == "__main__":
    main()