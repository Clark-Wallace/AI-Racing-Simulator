#!/usr/bin/env python3
"""
Test script to verify machine gun system functionality
"""

from src.core.racing_weapons import WeaponsManager, MachineGun
import time

def test_machine_gun_basics():
    """Test basic machine gun functionality"""
    print("Testing Machine Gun System...")
    
    # Create weapons manager
    weapons_mgr = WeaponsManager()
    
    # Initialize cars
    car_names = ["Llama Speed", "Llama Strategic", "Llama Balanced", "Hermes Chaos", "Qwen Technical"]
    weapons_mgr.initialize_cars(car_names)
    
    print(f"\n✅ Initialized {len(car_names)} cars with machine guns")
    
    # Check initial ammo
    print("\nInitial ammo status:")
    for car, ammo in weapons_mgr.get_all_ammo_status().items():
        print(f"  {car}: {ammo}/50 rounds")
    
    # Test firing
    print("\n🔫 Testing firing mechanism...")
    current_time = time.time()
    
    # Llama Speed fires at Llama Strategic
    if weapons_mgr.attempt_fire("Llama Speed", current_time):
        print("  ✅ Llama Speed fired successfully!")
    
    # Check ammo after firing
    ammo_after = weapons_mgr.get_ammo_status("Llama Speed")
    print(f"  Llama Speed ammo remaining: {ammo_after}/50")
    
    # Test hit detection
    print("\n🎯 Testing hit detection...")
    positions = {
        "Llama Speed": 0.5,
        "Llama Strategic": 0.51,  # Just ahead
        "Llama Balanced": 0.48,   # Behind
        "Hermes Chaos": 0.55,     # Far ahead
        "Qwen Technical": 0.45    # Far behind
    }
    laps = {car: 1 for car in car_names}
    
    # Find car ahead
    target = weapons_mgr.get_car_ahead("Llama Speed", positions, laps)
    if target:
        target_name, distance = target
        print(f"  Target ahead: {target_name} at distance {distance:.3f}")
        
        # Check hit
        hit = weapons_mgr.check_hit("Llama Speed", positions["Llama Speed"],
                                   target_name, positions[target_name], True)
        if hit:
            print(f"  ✅ HIT! {hit['damage']*100:.0f}% speed reduction")
        else:
            print("  ❌ Missed!")
    else:
        print("  No target in range")
    
    # Test rapid fire and cooldown
    print("\n⚡ Testing fire rate limit...")
    rapid_fire_count = 0
    for i in range(5):
        if weapons_mgr.attempt_fire("Llama Strategic", current_time + i * 0.1):
            rapid_fire_count += 1
    
    print(f"  Fired {rapid_fire_count} times in 0.5 seconds (expected ~2-3 due to cooldown)")
    
    # Test ammo depletion
    print("\n📉 Testing ammo depletion...")
    weapon = weapons_mgr.car_weapons["Hermes Chaos"]
    initial_ammo = weapon.ammo
    
    # Fire multiple times
    fire_count = 0
    for i in range(10):
        if weapon.fire(current_time + i * 0.3):
            fire_count += 1
    
    print(f"  Hermes Chaos fired {fire_count} times")
    print(f"  Ammo: {initial_ammo} -> {weapon.ammo}")
    
    # Test visual effects
    print("\n🎨 Testing visual effects system...")
    weapons_mgr.active_hits.append({
        "shooter": "Llama Speed",
        "target": "Llama Strategic",
        "damage": 0.15,
        "time": 0.0
    })
    
    print(f"  Active hit effects: {len(weapons_mgr.active_hits)}")
    
    # Update effects
    weapons_mgr.update_effects(0.3)
    print(f"  After 0.3s: {len(weapons_mgr.active_hits)} effects")
    
    weapons_mgr.update_effects(0.3)
    print(f"  After 0.6s: {len(weapons_mgr.active_hits)} effects (should be cleared)")
    
    print("\n✅ Machine gun system test complete!")
    
    # Summary
    print("\n📊 System Summary:")
    print("  - Each car starts with 50 rounds")
    print("  - Fire rate: 5 rounds per second")
    print("  - Damage: 15% speed reduction per hit")
    print("  - Range: 2% of track length")
    print("  - Hit effects last 0.5 seconds")
    print("  - No ammo refresh during race")

if __name__ == "__main__":
    test_machine_gun_basics()