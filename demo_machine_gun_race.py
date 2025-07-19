#!/usr/bin/env python3
"""
Demo script showing machine gun system in action
"""

import asyncio
from src.core.race_track import create_race_track
from src.llm_drivers.llm_race_simulator import LLMRaceSimulator
from src.llm_drivers.llm_racing_driver import create_llm_drivers
from src.graphics.race_renderer import GraphicsSettings

async def run_demo():
    """Run a quick demo race with machine guns"""
    print("\n🏎️ MACHINE GUN RACING DEMO")
    print("=" * 50)
    
    # Create track
    track = create_race_track("Monaco Street Circuit")
    
    # Create LLM drivers
    llm_config = [
        {"name": "Llama Speed", "model": "meta-llama/Llama-3.2-3B-Instruct-Turbo", 
         "personality": "aggressive racer focused on speed and overtaking"},
        {"name": "Llama Strategic", "model": "meta-llama/Llama-3.2-3B-Instruct-Turbo", 
         "personality": "tactical racer who plans moves carefully"},
        {"name": "Hermes Chaos", "model": "NousResearch/Hermes-3-Llama-3.1-8B-Turbo", 
         "personality": "unpredictable racer who takes risks"}
    ]
    
    print("\n🤖 Creating AI drivers...")
    llm_drivers = await create_llm_drivers(llm_config)
    
    # Graphics settings
    graphics_settings = GraphicsSettings(
        width=1200,
        height=800,
        fps=60,
        show_telemetry=True
    )
    
    # Create simulator
    simulator = LLMRaceSimulator(
        track=track,
        llm_drivers=llm_drivers,
        laps=3,  # Short race for demo
        enable_graphics=True,
        graphics_settings=graphics_settings
    )
    
    print("\n🔫 Machine Gun System Active!")
    print("  - Each car has 50 rounds")
    print("  - Cars can fire at targets ahead")
    print("  - Hits slow down the target by 15%")
    print("  - Watch for red bullet trails!")
    
    print("\n🏁 Starting race visualization...")
    print("Press ESC to exit\n")
    
    # Run the race
    results = simulator.simulate_race()
    
    # Show results
    print("\n🏆 RACE RESULTS:")
    print("=" * 50)
    for i, finisher in enumerate(results["finishing_order"], 1):
        print(f"{i}. {finisher['name']} - {finisher['driver']}")
    
    # Show weapon stats
    print("\n🔫 MACHINE GUN STATS:")
    print("=" * 50)
    ammo_status = simulator.weapons_manager.get_all_ammo_status()
    for car_name, ammo in ammo_status.items():
        shots_fired = 50 - ammo
        print(f"{car_name}: {shots_fired} shots fired ({ammo} rounds remaining)")

if __name__ == "__main__":
    print("🔧 Setting up demo...")
    print("\n⚠️ Note: This demo requires Together AI API key in TOGETHER_API_KEY environment variable")
    print("Without it, the race will use fallback AI behavior\n")
    
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("\nMake sure you have:")
        print("1. TOGETHER_API_KEY environment variable set")
        print("2. pygame installed (pip install pygame)")
        print("3. All required dependencies")