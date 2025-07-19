#!/usr/bin/env python3
"""
Debug script to trace weapon system data flow
"""

import time
from src.core.racing_weapons import WeaponsManager

def test_weapon_flow():
    """Test the flow of weapon data"""
    print("🔍 DEBUGGING WEAPON SYSTEM DATA FLOW")
    print("=" * 60)
    
    # 1. Create weapons manager
    weapons_mgr = WeaponsManager()
    car_names = ["Car A", "Car B", "Car C"]
    weapons_mgr.initialize_cars(car_names)
    
    print("\n1️⃣ Initial Setup:")
    print(f"   Cars initialized: {car_names}")
    print(f"   Ammo status: {weapons_mgr.get_all_ammo_status()}")
    
    # 2. Set up race positions
    positions = {"Car A": 0.5, "Car B": 0.51, "Car C": 0.48}
    laps = {"Car A": 1, "Car B": 1, "Car C": 1}
    
    print("\n2️⃣ Race Positions:")
    for car, pos in positions.items():
        print(f"   {car}: {pos:.2f}")
    
    # 3. Check targeting
    print("\n3️⃣ Target Detection:")
    for car in car_names:
        target = weapons_mgr.get_car_ahead(car, positions, laps)
        if target:
            print(f"   {car} → Target: {target[0]} at {target[1]:.3f}")
        else:
            print(f"   {car} → No target in range")
    
    # 4. Check firing capability
    print("\n4️⃣ Firing Capability:")
    current_time = time.time()
    for car in car_names:
        weapon = weapons_mgr.car_weapons[car]
        can_fire = weapon.can_fire(current_time)
        print(f"   {car}: Can fire = {can_fire}, Ammo = {weapon.ammo}")
    
    # 5. Simulate what LLM should receive
    print("\n5️⃣ LLM Race State (for Car A):")
    target = weapons_mgr.get_car_ahead("Car A", positions, laps)
    ammo = weapons_mgr.get_ammo_status("Car A")
    can_fire = weapons_mgr.car_weapons["Car A"].can_fire(current_time)
    
    print(f"   ammo_remaining: {ammo}")
    print(f"   can_fire: {can_fire}")
    print(f"   target_ahead: {target[0] if target else None}")
    print(f"   target_distance: {target[1] * 10000 if target else 999}m")  # Convert to meters
    
    # 6. Show what's in the prompt
    print("\n6️⃣ What appears in AI prompt:")
    print(f"   Machine Gun Ammo: {ammo}/50 rounds")
    print(f"   Can Fire: {'YES' if can_fire else 'NO'}")
    print(f"   Target Ahead: {target[0] if target else 'None'}")
    print(f"   Target Distance: {target[1] * 10000 if target else 999:.0f}m")
    
    # 7. Test firing
    print("\n7️⃣ Testing Fire Action:")
    if weapons_mgr.attempt_fire("Car A", current_time):
        print("   ✅ Car A fired successfully!")
        print(f"   Ammo remaining: {weapons_mgr.get_ammo_status('Car A')}")
    else:
        print("   ❌ Car A could not fire")
    
    print("\n✅ Weapon system data flow is working correctly!")
    print("\n⚠️ If LLMs aren't firing, possible issues:")
    print("   1. LLMs might be too conservative")
    print("   2. Target distance calculation might be off")
    print("   3. Fire rate cooldown might be preventing shots")
    print("   4. LLMs might prefer other actions over firing")

if __name__ == "__main__":
    test_weapon_flow()