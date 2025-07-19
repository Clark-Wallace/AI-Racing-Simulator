#!/usr/bin/env python3
"""
Test file for the Challenge Generator System - Phase 3
Demonstrates different racing challenge types
"""

from src.core.racing_car import RacingCar, DriverStyle
from src.systems.challenge_generator import RaceChallengeGenerator, ChallengeType, ChallengeDifficulty
import random


def create_test_racers():
    """Create diverse racers for challenge testing"""
    return [
        RacingCar("Speed Demon", 380, 3.2, 0.65, 10, DriverStyle.AGGRESSIVE),
        RacingCar("Tech Precision", 340, 4.5, 0.92, 14, DriverStyle.TECHNICAL),
        RacingCar("Fuel Master", 320, 5.2, 0.78, 18, DriverStyle.CONSERVATIVE),
        RacingCar("Adaptive Racer", 350, 4.0, 0.82, 13, DriverStyle.BALANCED),
        RacingCar("Chaos Cruiser", 360, 3.8, 0.75, 11, DriverStyle.CHAOTIC)
    ]


def test_speed_challenges():
    """Test speed-focused challenges"""
    print("\n" + "="*60)
    print("TEST 1: Speed Challenges")
    print("="*60)
    
    generator = RaceChallengeGenerator()
    racers = create_test_racers()
    
    # Test Drag Race
    print("\n🏁 DRAG RACE CHALLENGE")
    drag_config = generator.generate_challenge(ChallengeType.DRAG_RACE, ChallengeDifficulty.MEDIUM)
    print(f"Challenge: {drag_config.name}")
    print(f"Description: {drag_config.description}")
    print(f"Special Rules: {', '.join(drag_config.special_rules)}")
    
    # Run drag race
    drag_result = generator.run_challenge(drag_config, racers[:3])  # Use 3 racers
    print(f"\nResults:")
    for pos, name in drag_result.rankings.items():
        print(f"  {pos}. {name} - Score: {drag_result.scores[name]:.1f}")
    
    # Test Time Trial
    print("\n⏱️  TIME TRIAL CHALLENGE")
    time_config = generator.generate_challenge(ChallengeType.TIME_TRIAL, ChallengeDifficulty.EASY)
    print(f"Challenge: {time_config.name}")
    print(f"Description: {time_config.description}")
    
    # Test Sprint Race
    print("\n🏃 SPRINT RACE CHALLENGE")
    sprint_config = generator.generate_challenge(ChallengeType.SPRINT_RACE, ChallengeDifficulty.HARD)
    print(f"Challenge: {sprint_config.name}")
    print(f"Description: {sprint_config.description}")
    print(f"Success Criteria: Top {sprint_config.success_criteria['position']} finish")


def test_technical_challenges():
    """Test technical/skill challenges"""
    print("\n" + "="*60)
    print("TEST 2: Technical Challenges")
    print("="*60)
    
    generator = RaceChallengeGenerator()
    
    # Test Precision Driving
    print("\n🎯 PRECISION DRIVING CHALLENGE")
    precision_config = generator.generate_challenge(ChallengeType.PRECISION_DRIVING, ChallengeDifficulty.MEDIUM)
    print(f"Challenge: {precision_config.name}")
    print(f"Description: {precision_config.description}")
    print(f"Scoring Weights:")
    for metric, weight in precision_config.scoring_weights.items():
        print(f"  - {metric}: {weight*100:.0f}%")
    
    # Test Weather Challenge
    print("\n🌧️  WEATHER CHALLENGE")
    weather_config = generator.generate_challenge(ChallengeType.WEATHER_CHALLENGE, ChallengeDifficulty.HARD)
    print(f"Challenge: {weather_config.name}")
    print(f"Description: {weather_config.description}")
    print(f"Special Rules: {', '.join(weather_config.special_rules)}")


def test_strategic_challenges():
    """Test strategy-focused challenges"""
    print("\n" + "="*60)
    print("TEST 3: Strategic Challenges")
    print("="*60)
    
    generator = RaceChallengeGenerator()
    racers = create_test_racers()
    
    # Test Fuel Management
    print("\n⛽ FUEL MANAGEMENT CHALLENGE")
    fuel_config = generator.generate_challenge(ChallengeType.FUEL_MANAGEMENT, ChallengeDifficulty.HARD)
    print(f"Challenge: {fuel_config.name}")
    print(f"Description: {fuel_config.description}")
    
    # Run with appropriate racers
    fuel_racers = [
        racers[2],  # Fuel Master - should excel
        racers[0],  # Speed Demon - should struggle
        racers[3]   # Adaptive Racer - middle ground
    ]
    
    fuel_result = generator.run_challenge(fuel_config, fuel_racers)
    print(f"\nResults:")
    for pos, name in fuel_result.rankings.items():
        print(f"  {pos}. {name} - Score: {fuel_result.scores[name]:.1f}")
    print(f"Challenge Success: {'✅' if fuel_result.success else '❌'}")
    
    # Test Endurance Race
    print("\n🏃 ENDURANCE CHALLENGE")
    endurance_config = generator.generate_challenge(ChallengeType.ENDURANCE_RACE, ChallengeDifficulty.EASY)
    print(f"Challenge: {endurance_config.name}")
    print(f"Success Criteria: {endurance_config.success_criteria}")


def test_mixed_challenges():
    """Test mixed/complex challenges"""
    print("\n" + "="*60)
    print("TEST 4: Mixed Challenges")
    print("="*60)
    
    generator = RaceChallengeGenerator()
    
    # Test Formula Race
    print("\n🏎️  FORMULA RACE CHALLENGE")
    formula_config = generator.generate_challenge(ChallengeType.FORMULA_RACE, ChallengeDifficulty.MEDIUM)
    print(f"Challenge: {formula_config.name}")
    print(f"Description: {formula_config.description}")
    print(f"Scoring breakdown:")
    for metric, weight in formula_config.scoring_weights.items():
        print(f"  - {metric}: {weight*100:.0f}%")
    
    # Test Elimination Race
    print("\n💀 ELIMINATION RACE CHALLENGE")
    elimination_config = generator.generate_challenge(ChallengeType.ELIMINATION_RACE, ChallengeDifficulty.EXTREME)
    print(f"Challenge: {elimination_config.name}")
    print(f"Description: {elimination_config.description}")
    print(f"Special Rules: {', '.join(elimination_config.special_rules)}")


def test_difficulty_scaling():
    """Test how difficulty affects challenges"""
    print("\n" + "="*60)
    print("TEST 5: Difficulty Scaling")
    print("="*60)
    
    generator = RaceChallengeGenerator()
    
    print("\n📊 DRAG RACE - DIFFICULTY COMPARISON")
    for difficulty in ChallengeDifficulty:
        config = generator.generate_challenge(ChallengeType.DRAG_RACE, difficulty)
        print(f"\n{difficulty.name}:")
        print(f"  Name: {config.name}")
        print(f"  Track Length: {config.track_config['length']*1000:.0f}m")
        print(f"  Success Time: {config.success_criteria['finish_time']:.1f}s")


def test_challenge_variety():
    """Test random challenge generation"""
    print("\n" + "="*60)
    print("TEST 6: Challenge Variety Showcase")
    print("="*60)
    
    generator = RaceChallengeGenerator()
    racers = create_test_racers()
    
    # Generate 5 random challenges
    challenge_types = list(ChallengeType)
    selected_challenges = random.sample(challenge_types, 5)
    
    print("\n🎲 RANDOM CHALLENGE SELECTION:")
    
    for i, challenge_type in enumerate(selected_challenges, 1):
        difficulty = random.choice(list(ChallengeDifficulty))
        config = generator.generate_challenge(challenge_type, difficulty)
        
        print(f"\n{i}. {config.name}")
        print(f"   Type: {challenge_type.value.replace('_', ' ').title()}")
        print(f"   Difficulty: {difficulty.name}")
        print(f"   Description: {config.description}")


def test_full_challenge_run():
    """Run a complete challenge with all features"""
    print("\n" + "="*60)
    print("TEST 7: Complete Challenge Demonstration")
    print("="*60)
    
    generator = RaceChallengeGenerator()
    racers = create_test_racers()
    
    # Run a Technical Precision Challenge
    print("\n🏆 RUNNING FULL PRECISION CHALLENGE")
    config = generator.generate_challenge(ChallengeType.PRECISION_DRIVING, ChallengeDifficulty.MEDIUM)
    
    print(f"\nChallenge Details:")
    print(f"  Name: {config.name}")
    print(f"  Type: {config.challenge_type.value}")
    print(f"  Difficulty: {config.difficulty.name}")
    
    print(f"\nParticipants:")
    for car in racers:
        print(f"  - {car.name} ({car.driver_style.value})")
    
    # Run the challenge
    result = generator.run_challenge(config, racers)
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"Success: {'✅ YES' if result.success else '❌ NO'}")
    
    print(f"\nRankings:")
    for pos, name in result.rankings.items():
        score = result.scores[name]
        print(f"  {pos}. {name}: {score:.1f} points")
    
    # Show telemetry insights if available
    if result.telemetry_data:
        print(f"\n📈 Performance Insights:")
        winner = result.rankings[1]
        if winner in result.telemetry_data:
            winner_data = result.telemetry_data[winner]
            print(f"  Winner's cornering efficiency: {winner_data['handling']['cornering_efficiency']:.2%}")
            print(f"  Winner's consistency: ±{winner_data['technical']['consistency']:.2f}s")
            print(f"  Winner's top speed: {winner_data['speed']['top_speed']:.1f} km/h")
    
    print(f"\n💬 Summary:")
    print(result.summary)


def main():
    """Run all challenge tests"""
    print("\n🏎️  AI RACING SIMULATOR - PHASE 3: CHALLENGE GENERATOR TESTS 🏎️")
    
    test_speed_challenges()
    test_technical_challenges()
    test_strategic_challenges()
    test_mixed_challenges()
    test_difficulty_scaling()
    test_challenge_variety()
    test_full_challenge_run()
    
    print("\n" + "="*60)
    print("✅ Phase 3 Complete: Challenge Generator System Implemented!")
    print("="*60)
    print("\nKey Features Demonstrated:")
    print("- 12 different challenge types across 4 categories")
    print("- Configurable difficulty levels (Easy to Extreme)")
    print("- Custom scoring systems for each challenge type")
    print("- Success criteria and special rules")
    print("- Integration with telemetry for advanced scoring")
    print("- Modular design for easy expansion")
    
    print("\nChallenge Categories:")
    print("  🏁 Speed: Drag Race, Time Trial, Sprint")
    print("  🎯 Technical: Precision, Obstacles, Weather")
    print("  ⚡ Strategic: Fuel Management, Endurance, Pursuit")
    print("  🏆 Mixed: Formula, Elimination, Relay")


if __name__ == "__main__":
    main()