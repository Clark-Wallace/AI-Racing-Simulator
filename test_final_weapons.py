#!/usr/bin/env python3
"""
Final test showing the complete weapon system integration
"""

from src.core.racing_weapons import WeaponsManager

def test_final_integration():
    """Test the complete weapon system with realistic values"""
    print("🏎️ FINAL WEAPON SYSTEM TEST")
    print("=" * 60)
    
    # Setup
    weapons_mgr = WeaponsManager()
    cars = ["Llama Speed", "Llama Strategic", "Llama Balanced"]
    weapons_mgr.initialize_cars(cars)
    
    # Simulate close racing positions (in track progress units)
    positions = {
        "Llama Speed": 0.500,
        "Llama Strategic": 0.502,    # 0.002 ahead = ~20m on 10km track
        "Llama Balanced": 0.498      # Behind
    }
    laps = {car: 1 for car in cars}
    
    print("\n📊 Race Scenario (10km track):")
    for car, pos in sorted(positions.items(), key=lambda x: -x[1]):
        print(f"   {car}: Position {pos:.3f}")
    
    print("\n🎯 Targeting Analysis:")
    track_length_km = 10  # Standard track
    
    for car in cars:
        target = weapons_mgr.get_car_ahead(car, positions, laps)
        if target:
            target_name, distance_progress = target
            distance_meters = distance_progress * track_length_km * 1000
            in_range = distance_progress <= weapons_mgr.car_weapons[car].range
            
            print(f"\n   {car}:")
            print(f"     Target: {target_name}")
            print(f"     Distance: {distance_meters:.0f}m")
            print(f"     In Range: {'YES ✅' if in_range else 'NO ❌'} (max: {weapons_mgr.car_weapons[car].range * track_length_km * 1000:.0f}m)")
            print(f"     Should Fire: {'YES 🔫' if in_range and distance_meters <= 200 else 'NO'}")
        else:
            print(f"\n   {car}: No target ahead")
    
    print("\n📝 AI Prompt Values:")
    print("-" * 40)
    # Show what Llama Speed would see
    target = weapons_mgr.get_car_ahead("Llama Speed", positions, laps)
    if target:
        print("WEAPONS SYSTEM:")
        print(f"Machine Gun Ammo: 50/50 rounds")
        print(f"Can Fire: YES")
        print(f"Target Ahead: {target[0]}")
        print(f"Target Distance: {int(target[1] * track_length_km * 1000)}m")
        print("⚠️ IMPORTANT: Use FIRE or SHOOT action when you have a target within 200m!")
    
    print("\n✅ Summary:")
    print("   - Weapon range: 300m (3% of 10km track)")
    print("   - AI told to fire at targets within 200m")
    print("   - Cars in close racing will have firing opportunities")
    print("   - Debug messages will show when cars SHOULD FIRE")

if __name__ == "__main__":
    test_final_integration()