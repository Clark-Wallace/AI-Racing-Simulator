#!/usr/bin/env python3
"""
Test script to verify LLMs receive weapon data correctly
"""

import asyncio
from src.llm_drivers.llm_racing_driver import LLMDriver, LLMAction
from src.core.racing_car import RacingCar, DriverStyle
from ai_config import RacingAI

async def test_weapon_decision():
    """Test if LLM makes firing decisions with weapon data"""
    print("Testing LLM Weapon Decision Making...")
    print("=" * 60)
    
    # Create a test AI
    ai = RacingAI()
    
    # Create a test driver
    car = RacingCar("Test Racer", DriverStyle.AGGRESSIVE)
    driver = LLMDriver(
        car=car,
        ai=ai,
        model_config={"model": "test-model", "personality": "aggressive"},
        name="Test Driver"
    )
    
    # Create race state with clear firing opportunity
    race_state = {
        "current_lap": 2,
        "total_laps": 5,
        "gap_ahead": 15,  # Close enough to fire
        "gap_behind": 50,
        "track_segment": "straight",
        "weather": "clear",
        "power_ups": [],
        "collision_risk": {"risk_level": "low", "risk_factor": 0.1},
        "power_up_strategy": {"recommendation": "none"},
        "ammo_remaining": 45,  # Has ammo
        "can_fire": True,  # Can fire
        "target_ahead": "Enemy Car",  # Has target
        "target_distance": 15  # Within range
    }
    
    print("\n📊 Race State for LLM:")
    print(f"  Position: P{car.current_position}")
    print(f"  Ammo: {race_state['ammo_remaining']}/50")
    print(f"  Can Fire: {race_state['can_fire']}")
    print(f"  Target: {race_state['target_ahead']} at {race_state['target_distance']}m")
    print(f"  Gap Ahead: {race_state['gap_ahead']}m")
    
    print("\n🤖 Getting LLM decision...")
    
    try:
        # Get decision
        decision = await driver.make_decision(race_state)
        
        print(f"\n✅ LLM Decision:")
        print(f"  Action: {decision.get('action', 'UNKNOWN')}")
        print(f"  Reasoning: {decision.get('reasoning', 'No reason given')}")
        print(f"  Confidence: {decision.get('confidence', 0)*100:.0f}%")
        
        # Check if it's a firing action
        action_str = decision.get('action', '').upper()
        if action_str in ['FIRE', 'SHOOT']:
            print("\n🔫 LLM chose to FIRE! Weapons system working!")
        else:
            print(f"\n⚠️ LLM chose {action_str} instead of firing")
            print("   Even though target was in range!")
            
    except Exception as e:
        print(f"\n❌ Error getting decision: {e}")
        print("   This might be due to missing API key")
    
    # Show what the AI should see
    print("\n📝 What the AI sees in its prompt:")
    print("-" * 40)
    print("WEAPONS SYSTEM:")
    print(f"Machine Gun Ammo: {race_state['ammo_remaining']}/50 rounds")
    print(f"Can Fire: YES")
    print(f"Target Ahead: {race_state['target_ahead']}")
    print(f"Target Distance: {race_state['target_distance']}m")
    print("⚠️ IMPORTANT: Use FIRE or SHOOT action when you have a target within 20m!")
    print("\nEXAMPLE: If Target Ahead is \"Llama Speed\" at 15m and you Can Fire: YES, then use action: \"FIRE\"")
    print("-" * 40)

if __name__ == "__main__":
    print("\n🔫 LLM WEAPON SYSTEM TEST")
    print("=" * 60)
    print("This test verifies that LLMs receive weapon data")
    print("and are encouraged to fire when appropriate.\n")
    
    asyncio.run(test_weapon_decision())