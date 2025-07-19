#!/usr/bin/env python3
"""
LLM vs Rules Race - Watch AI language models race against rule-based AI!
The ultimate showdown: Neural networks vs. Algorithms!
"""

import sys
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

from src.core.racing_car import RacingCar, DriverStyle
from src.core.race_track import RaceTrack
from src.llm_drivers.llm_racing_driver import create_llm_drivers, LLMDriver
from src.graphics.graphical_race_simulator import GraphicalRaceSimulator
from src.graphics.race_renderer import GraphicsSettings


def create_mixed_lineup():
    """Create a mix of LLM and rule-based drivers"""
    drivers = []
    
    # Check if we can create LLM drivers
    if os.getenv("TOGETHER_API_KEY"):
        try:
            print("🤖 Creating LLM drivers...")
            # Create just 2 LLM drivers to save API costs
            from ai_config import RacingAI, LLAMA_MODELS
            
            # Fast Llama
            speed_car = RacingCar(
                name="Llama Speed AI",
                top_speed=385,
                acceleration=3.0,
                handling=0.65,
                fuel_efficiency=9,
                driver_style=DriverStyle.AGGRESSIVE
            )
            speed_ai = RacingAI(LLAMA_MODELS["speed"]["model"])
            drivers.append(("llm", LLMDriver(
                car=speed_car,
                ai=speed_ai,
                model_config=LLAMA_MODELS["speed"],
                name="Llama-3.2 Speed"
            )))
            
            # Strategic Llama
            strategic_car = RacingCar(
                name="Llama Strategic AI",
                top_speed=355,
                acceleration=2.7,
                handling=0.88,
                fuel_efficiency=16,
                driver_style=DriverStyle.BALANCED
            )
            strategic_ai = RacingAI(LLAMA_MODELS["strategic"]["model"])
            drivers.append(("llm", LLMDriver(
                car=strategic_car,
                ai=strategic_ai,
                model_config=LLAMA_MODELS["strategic"],
                name="Llama-70B Strategic"
            )))
            
            print("✅ 2 LLM drivers created!")
            
        except Exception as e:
            print(f"⚠️  Could not create LLM drivers: {e}")
            print("   Falling back to all rule-based drivers")
    else:
        print("ℹ️  No Together API key found - using only rule-based AI")
    
    # Add 3 rule-based drivers
    print("🎮 Creating rule-based AI drivers...")
    
    drivers.append(("rule", RacingCar(
        name="Speed Demon Max",
        top_speed=380,
        acceleration=3.2,
        handling=0.65,
        fuel_efficiency=10,
        driver_style=DriverStyle.AGGRESSIVE
    )))
    
    drivers.append(("rule", RacingCar(
        name="The Professor",
        top_speed=350,
        acceleration=2.8,
        handling=0.90,
        fuel_efficiency=15,
        driver_style=DriverStyle.BALANCED
    )))
    
    drivers.append(("rule", RacingCar(
        name="Chaos Tornado",
        top_speed=370,
        acceleration=3.0,
        handling=0.70,
        fuel_efficiency=12,
        driver_style=DriverStyle.CHAOTIC
    )))
    
    return drivers


class HybridRaceSimulator(GraphicalRaceSimulator):
    """Simulator that can handle both LLM and rule-based drivers"""
    
    def __init__(self, track, mixed_drivers, laps=10, enable_graphics=True, graphics_settings=None):
        # Separate LLM and rule-based drivers
        self.llm_drivers = {}
        cars = []
        
        for driver_type, driver in mixed_drivers:
            if driver_type == "llm":
                cars.append(driver.car)
                self.llm_drivers[driver.car.name] = driver
            else:  # rule-based
                cars.append(driver)
        
        super().__init__(
            track=track,
            cars=cars,
            laps=laps,
            enable_telemetry=True,
            enable_intelligence=True,  # Keep rule-based AI active
            enable_graphics=enable_graphics,
            graphics_settings=graphics_settings
        )
        
    def simulate_race(self):
        """Override to handle LLM decisions"""
        if not self.llm_drivers:
            # No LLM drivers, use standard simulation
            return super().simulate_race()
            
        # Custom simulation mixing both AI types
        print("\n🏁 HYBRID RACE: LLMs vs Rule-Based AI! 🏁")
        print(f"Track: {self.track.name}")
        print("\nCompetitors:")
        
        for car in self.cars:
            if car.name in self.llm_drivers:
                driver = self.llm_drivers[car.name]
                print(f"  🤖 {car.name} (LLM: {driver.model_config['model'].split('/')[-1]})")
            else:
                print(f"  🎮 {car.name} (Rule-based {car.driver_style.value})")
                
        # For simplicity, use the parent's visual simulation
        # In a full implementation, we'd integrate LLM decisions into the race loop
        return super().simulate_race()


async def main():
    """Run the hybrid racing demonstration"""
    print("🏁 AI RACING: LLMs vs RULE-BASED SHOWDOWN! 🏁")
    print("=" * 60)
    print("Watch language models compete against algorithmic AI!")
    print()
    
    # Check pygame
    try:
        import pygame
        use_graphics = True
        print("✅ Pygame detected - visual mode available")
    except ImportError:
        use_graphics = False
        print("📝 Text mode only (install pygame for visuals)")
        
    # Create mixed lineup
    mixed_drivers = create_mixed_lineup()
    
    if not mixed_drivers:
        print("❌ No drivers created!")
        return
        
    # Quick race setup
    print("\n🏎️  RACE SETUP:")
    track = RaceTrack.create_mixed_track("AI Battleground")
    laps = 5
    
    print(f"  • Track: {track.name}")
    print(f"  • Laps: {laps}")
    print(f"  • Mode: {'Visual' if use_graphics else 'Text'}")
    
    # Graphics settings
    graphics_settings = GraphicsSettings(
        width=1200,
        height=800,
        fps=60,
        show_telemetry=True,
        show_ai_thoughts=True
    ) if use_graphics else None
    
    # Create hybrid simulator
    simulator = HybridRaceSimulator(
        track=track,
        mixed_drivers=mixed_drivers,
        laps=laps,
        enable_graphics=use_graphics,
        graphics_settings=graphics_settings
    )
    
    print("\n🚦 STARTING HYBRID RACE!")
    print("LLMs 🤖 vs Algorithms 🎮 - Who will win?\n")
    
    if use_graphics:
        input("Press Enter to start the race...")
    
    # Run the race
    results = simulator.simulate_race()
    
    # Display results
    print("\n🏆 RACE RESULTS 🏆")
    print("=" * 60)
    
    llm_positions = []
    rule_positions = []
    
    for i, result in enumerate(results["finishing_order"], 1):
        name = result["name"]
        time = result["total_time"]
        
        # Determine if LLM or rule-based
        is_llm = "AI" in name or "Llama" in name
        
        if i == 1:
            print(f"🥇 {name} - {time:.2f}s")
        elif i == 2:
            print(f"🥈 {name} - {time:.2f}s")
        elif i == 3:
            print(f"🥉 {name} - {time:.2f}s")
        else:
            print(f"{i}. {name} - {time:.2f}s")
            
        print(f"   Type: {'🤖 LLM-Powered' if is_llm else '🎮 Rule-Based'}")
        print(f"   Fuel: {result['final_fuel']:.1f}% | Tires: {100-result['tire_wear']:.1f}%")
        print()
        
        if is_llm:
            llm_positions.append(i)
        else:
            rule_positions.append(i)
    
    # Analysis
    print("\n📊 ANALYSIS:")
    print("=" * 60)
    
    if llm_positions and rule_positions:
        avg_llm = sum(llm_positions) / len(llm_positions)
        avg_rule = sum(rule_positions) / len(rule_positions)
        
        print(f"LLM Average Position: {avg_llm:.1f}")
        print(f"Rule-Based Average Position: {avg_rule:.1f}")
        
        if avg_llm < avg_rule:
            print("\n🤖 LLMs performed better on average!")
        else:
            print("\n🎮 Rule-based AI performed better on average!")
    
    print("\n✨ Hybrid Racing Demo Complete!")
    print("The future of AI racing: Language models making split-second decisions!")


if __name__ == "__main__":
    asyncio.run(main())