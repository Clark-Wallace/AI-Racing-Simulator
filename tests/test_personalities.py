#!/usr/bin/env python3
"""
Test file for the Enhanced AI Personalities System - Phase 6
Demonstrates personality traits, emotions, and relationships
"""

from racing_car import RacingCar, DriverStyle
from race_track import RaceTrack
from intelligent_race_simulator import IntelligentRaceSimulator
from ai_personalities import AIPersonalitySystem, EmotionalState, PersonalityTrait
from enhanced_ai_racers import create_enhanced_ai_racers, EnhancedAIRacer
from data_prizes import DataPrizeSystem
import random


def test_personality_profiles():
    """Test basic personality profiles"""
    print("\n" + "="*60)
    print("TEST 1: AI Personality Profiles")
    print("="*60)
    
    personality_system = AIPersonalitySystem()
    
    for name, profile in personality_system.profiles.items():
        print(f"\n{'='*40}")
        print(f"🏎️  {profile.name} - '{profile.nickname}'")
        print(f"{'='*40}")
        print(f"\n📖 Backstory:")
        print(f"   {profile.backstory}")
        print(f"\n🎭 Personality Traits:")
        print(f"   Primary: {', '.join([t.value for t in profile.primary_traits])}")
        print(f"   Quirks: {', '.join([t.value for t in profile.quirks])}")
        print(f"\n💬 Catchphrases:")
        for phrase in profile.catchphrases[:2]:
            print(f"   '{phrase}'")
        print(f"\n🎯 Signature Moves:")
        print(f"   {', '.join(profile.signature_moves)}")
        print(f"\n🏁 Racing Philosophy:")
        print(f"   {profile.racing_philosophy}")


def test_emotional_responses():
    """Test emotional state changes"""
    print("\n" + "="*60)
    print("TEST 2: Emotional Responses")
    print("="*60)
    
    personality_system = AIPersonalitySystem()
    enhanced_racers = create_enhanced_ai_racers(personality_system)
    
    # Test various events
    events = [
        ("overtaken", {"by": "rival"}),
        ("overtake_success", {"on": "leader"}),
        ("crash", {"severity": "minor"}),
        ("leading", {"gap": 2.0}),
        ("final_lap", {"position": 2})
    ]
    
    for racer in enhanced_racers[:3]:  # Test first 3 racers
        print(f"\n🎭 {racer.profile.name}'s Emotional Journey:")
        print(f"   Starting state: {racer.profile.emotional_state.value}")
        
        for event, context in events:
            reaction = racer.react_to_event(event, context)
            print(f"   {event}: → {racer.profile.emotional_state.value}")
            if reaction:
                print(f"      '{reaction}'")


def test_performance_modifiers():
    """Test how emotions affect performance"""
    print("\n" + "="*60)
    print("TEST 3: Emotional Performance Impact")
    print("="*60)
    
    personality_system = AIPersonalitySystem()
    
    # Test Speed Demon in different states
    speed_demon = personality_system.profiles["Speed Demon"]
    
    states_to_test = [
        EmotionalState.CALM,
        EmotionalState.ANGRY,
        EmotionalState.CONFIDENT,
        EmotionalState.RECKLESS
    ]
    
    print("\n🏎️  Speed Demon Performance Modifiers:")
    for state in states_to_test:
        speed_demon.emotional_state = state
        modifiers = personality_system.apply_emotional_modifiers(speed_demon)
        
        print(f"\n   When {state.value}:")
        print(f"      Speed: {modifiers['speed']:.2f}x")
        print(f"      Handling: {modifiers['handling']:.2f}x")
        print(f"      Risk Taking: {modifiers['risk_taking']:.2f}x")


def test_rivalries():
    """Test rivalry system"""
    print("\n" + "="*60)
    print("TEST 4: Rivalry Development")
    print("="*60)
    
    personality_system = AIPersonalitySystem()
    
    # Simulate incidents between racers
    print("\n🥊 Creating Racing Rivalries:")
    
    # Speed Demon vs Tech Precision
    print("\n   Speed Demon vs Tech Precision:")
    personality_system.update_relationship("Speed Demon", "Tech Precision", "collision", {"track": "Monaco"})
    personality_system.update_relationship("Speed Demon", "Tech Precision", "collision", {"track": "Silverstone"})
    
    rel = personality_system.profiles["Speed Demon"].relationships["Tech Precision"]
    print(f"      Relationship: {rel.relationship_type.value}")
    print(f"      Intensity: {rel.intensity:.1f}")
    print(f"      Respect: {rel.respect_level:.1f}")
    
    # Tech Precision vs Adaptive Racer
    print("\n   Tech Precision vs Adaptive Racer:")
    personality_system.update_relationship("Tech Precision", "Adaptive Racer", "clean_battle", {"track": "Spa"})
    personality_system.update_relationship("Tech Precision", "Adaptive Racer", "clean_battle", {"track": "Monza"})
    
    rel = personality_system.profiles["Tech Precision"].relationships["Adaptive Racer"]
    print(f"      Relationship: {rel.relationship_type.value}")
    print(f"      Respect: {rel.respect_level:.1f}")


def test_race_with_personalities():
    """Test a race with full personality integration"""
    print("\n" + "="*60)
    print("TEST 5: Personality-Driven Race")
    print("="*60)
    
    personality_system = AIPersonalitySystem()
    enhanced_racers = create_enhanced_ai_racers(personality_system)
    
    # Extract just the cars for the simulator
    cars = [racer.car for racer in enhanced_racers]
    
    # Run a short race
    track = RaceTrack.create_technical_track()
    
    print("\n🏁 PERSONALITY SHOWCASE RACE:")
    print("\n💭 Pre-Race Thoughts:")
    for racer in enhanced_racers:
        quote = personality_system.generate_pre_race_quote(
            racer.profile, 
            {"track_type": "technical", "main_rival": None}
        )
        print(f"   {racer.profile.nickname}: '{quote}'")
    
    # Simulate race (simplified for demo)
    print("\n🏎️  Racing...")
    
    # Simulate some race events
    race_time = 0
    for lap in range(3):
        print(f"\n📍 Lap {lap + 1}:")
        
        # Random events
        for racer in enhanced_racers:
            if random.random() < 0.3:  # 30% chance of notable event
                events = ["overtake_success", "overtaken", "near_miss"]
                event = random.choice(events)
                
                reaction = racer.react_to_event(event, {"time": race_time})
                if reaction:
                    print(f"   {race_time:.1f}s - {racer.profile.nickname}: '{reaction}'")
                    
            # Update fatigue
            racer.update_fatigue(lap + 1, 3)
            
        race_time += 30  # 30 seconds per lap
    
    # Post-race quotes
    print("\n🏁 Post-Race Interviews:")
    positions = list(range(1, 6))
    random.shuffle(positions)
    
    for i, racer in enumerate(enhanced_racers):
        quote = personality_system.generate_post_race_quote(
            racer.profile,
            positions[i],
            {}
        )
        print(f"   P{positions[i]} {racer.profile.nickname}: '{quote}'")


def test_signature_moves():
    """Test signature move system"""
    print("\n" + "="*60)
    print("TEST 6: Signature Moves")
    print("="*60)
    
    personality_system = AIPersonalitySystem()
    enhanced_racers = create_enhanced_ai_racers(personality_system)
    
    print("\n⚡ Signature Move Opportunities:")
    
    # Test different situations
    situations = [
        {"gap_ahead": 0.3, "is_corner": False, "laps_remaining": 1, "racer": "Speed Demon"},
        {"gap_ahead": 0.4, "is_corner": True, "laps_remaining": 5, "racer": "Tech Precision"},
        {"gap_ahead": 1.0, "fuel_critical": True, "laps_remaining": 3, "racer": "Fuel Master"},
        {"gap_ahead": 0.2, "is_corner": False, "laps_remaining": 1, "racer": "Chaos Cruiser"}
    ]
    
    for situation in situations:
        racer_name = situation.pop("racer")
        racer = next(r for r in enhanced_racers if r.profile.name == racer_name)
        
        # Set confident state for signature moves
        racer.profile.emotional_state = EmotionalState.CONFIDENT
        racer.profile.confidence_level = 0.8
        
        move = personality_system.get_signature_move_decision(racer.profile, situation)
        if move:
            print(f"\n   {racer.profile.nickname} executes '{move}'!")
            print(f"      Situation: Gap {situation.get('gap_ahead', 0)}s ahead, "
                  f"{'Corner' if situation.get('is_corner') else 'Straight'}")
        else:
            print(f"\n   {racer.profile.nickname}: No signature move opportunity")


def test_memorable_moments():
    """Test memorable moment creation"""
    print("\n" + "="*60)
    print("TEST 7: Creating Memorable Moments")
    print("="*60)
    
    personality_system = AIPersonalitySystem()
    
    # Create some memorable moments
    moments = [
        ("epic_battle", ["Speed Demon", "Tech Precision"], {"duration": 7, "track": "Monaco"}),
        ("comeback_victory", ["Chaos Cruiser"], {"start_pos": "5th", "track": "Silverstone"}),
        ("controversial_overtake", ["Speed Demon", "Fuel Master"], {"track": "Monza"}),
        ("perfect_race", ["Tech Precision"], {"track_type": "technical", "track": "Monaco"})
    ]
    
    print("\n📸 Memorable Moments Created:")
    
    for event_type, participants, context in moments:
        moment = personality_system.create_memorable_moment(event_type, participants, context)
        print(f"\n   🏆 {moment['description']}")
        print(f"      Significance: {'⭐' * int(moment['significance'] * 5)}")
        print(f"      Track: {moment['track']}")


def test_personality_evolution():
    """Test long-term personality development"""
    print("\n" + "="*60)
    print("TEST 8: Personality Evolution")
    print("="*60)
    
    personality_system = AIPersonalitySystem()
    
    # Simulate a season for Chaos Cruiser
    chaos = personality_system.profiles["Chaos Cruiser"]
    
    print(f"\n📈 {chaos.nickname}'s Career Evolution:")
    print(f"\n   Starting Traits: {[t.value for t in chaos.primary_traits]}")
    print(f"   Starting Quirks: {[t.value for t in chaos.quirks]}")
    
    # Simulate successful season
    season_results = {
        "races": 20,
        "wins": 8,
        "crashes": 2,
        "podiums": 15
    }
    
    personality_system.evolve_personality(chaos, season_results)
    
    print(f"\n   After {season_results['races']} races ({season_results['wins']} wins):")
    print(f"   Updated Traits: {[t.value for t in chaos.primary_traits]}")
    print(f"   Career Stats: {chaos.races_completed} races, {chaos.wins} wins")
    
    # Check for veteran status
    chaos.races_completed = 51  # Force veteran eligibility
    personality_system.evolve_personality(chaos, {"races": 1})
    
    print(f"\n   After 50+ races:")
    print(f"   Veteran Status: {'Yes' if PersonalityTrait.VETERAN in chaos.primary_traits else 'No'}")


def main():
    """Run all personality tests"""
    print("\n🏎️  AI RACING SIMULATOR - PHASE 6: ENHANCED PERSONALITIES TESTS 🏎️")
    
    test_personality_profiles()
    test_emotional_responses()
    test_performance_modifiers()
    test_rivalries()
    test_race_with_personalities()
    test_signature_moves()
    test_memorable_moments()
    test_personality_evolution()
    
    print("\n" + "="*60)
    print("✅ Phase 6 Complete: Enhanced AI Personalities Implemented!")
    print("="*60)
    print("\nKey Features Demonstrated:")
    print("- Rich backstories and personality traits")
    print("- Dynamic emotional states affecting performance")
    print("- Rivalry and relationship systems")
    print("- Signature moves and catchphrases")
    print("- Memorable moment creation")
    print("- Long-term personality evolution")
    print("- Radio messages and internal thoughts")
    
    print("\n🎭 Personality Impact:")
    print("- Each racer feels unique and memorable")
    print("- Emotions drive performance variations")
    print("- Rivalries create ongoing narratives")
    print("- Personalities evolve over careers")
    print("- Creates emergent storytelling in races")


if __name__ == "__main__":
    main()