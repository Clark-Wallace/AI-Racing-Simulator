#!/usr/bin/env python3
"""
LLM Race Demo - Watch Llama models race using Together AI!
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

from src.core.race_track import RaceTrack
from src.llm_drivers.llm_racing_driver import create_llm_drivers
from src.llm_drivers.llm_race_simulator import LLMRaceSimulator
from src.graphics.race_renderer import GraphicsSettings


def check_setup():
    """Check if everything is set up correctly"""
    # Check for API key
    if not os.getenv("TOGETHER_API_KEY"):
        print("❌ TOGETHER_API_KEY not found in environment!")
        print("\nTo set it up:")
        print("1. Create a .env file in the project root")
        print("2. Add: TOGETHER_API_KEY=your_api_key_here")
        print("3. Get your API key from: https://api.together.xyz/")
        return False
        
    # Check for Nexus Connector
    try:
        import nexus
        print("✅ Nexus Connector detected!")
    except ImportError:
        print("❌ Nexus Connector not installed!")
        print("\nTo install:")
        print('pip install -e "/Users/clarkwallace/Libraries/The-Nexus-Connector"')
        return False
        
    # Check for pygame
    try:
        import pygame
        print("✅ Pygame installed for graphics!")
    except ImportError:
        print("⚠️  Pygame not installed - will use text mode")
        print("To install: pip install pygame")
        
    return True


async def main():
    """Run the LLM racing demonstration"""
    print("🤖 AI RACING SIMULATOR - LLM DRIVERS DEMO 🤖")
    print("=" * 60)
    print("Powered by Together AI and your Nexus Connector!")
    print()
    
    # Check setup
    if not check_setup():
        return
        
    print("\n🏎️  LLM DRIVER LINEUP:")
    print("1. 🔴 Llama-3.2 Speed (3B) - Fast decisions, aggressive")
    print("2. 🔵 Llama-70B Strategic - Deep thinking, calculated")  
    print("3. 🟡 Llama-8B Balanced - Adaptive middle ground")
    print("4. 🟣 Hermes Chaos - Unpredictable wildcard")
    print("5. 🟢 Qwen Technical - Precision and efficiency")
    
    # Track selection
    print("\n🏁 TRACK SELECTION:")
    print("1. Speed Circuit - Fast straights")
    print("2. Technical Circuit - Tight corners")
    print("3. Mixed Circuit - Balanced")
    print("4. Endurance Circuit - Long distance")
    
    track_choice = "1"  # Auto-select Speed Circuit for testing
    
    if track_choice == "2":
        track = RaceTrack.create_technical_track("AI Technical Challenge")
    elif track_choice == "3":
        track = RaceTrack.create_mixed_track("AI Mixed Masters")
    elif track_choice == "4":
        track = RaceTrack.create_endurance_track("AI Endurance Test")
    else:
        track = RaceTrack.create_speed_track("AI Speed Arena")
        
    # Number of laps (auto-select 2 for quick testing)
    laps = 2  # Quick test with 2 laps
    
    # Graphics mode (auto-detect)
    use_graphics = False  # Use text mode for testing
    try:
        import pygame
        use_graphics = True  # Enable if pygame is available
    except ImportError:
        use_graphics = False
        print("\n📝 Running in text mode (pygame not installed)")
    
    print(f"\n⚡ RACE SETUP:")
    print(f"  • Track: {track.name}")
    print(f"  • Laps: {laps}")
    print(f"  • Mode: {'Visual' if use_graphics else 'Text'}")
    print(f"  • LLMs will make real-time decisions!")
    
    print("\n⏳ Creating LLM drivers (this loads the AI models)...")
    
    try:
        # Create LLM drivers
        llm_drivers = create_llm_drivers()
        print("✅ LLM drivers ready!")
        
        # Configure graphics
        graphics_settings = GraphicsSettings(
            width=1200,
            height=800,
            fps=60,  # Higher FPS for smoother animation
            show_telemetry=True,
            show_ai_thoughts=True
        ) if use_graphics else None
        
        # Create simulator
        simulator = LLMRaceSimulator(
            track=track,
            llm_drivers=llm_drivers,
            laps=laps,
            enable_graphics=use_graphics,
            graphics_settings=graphics_settings
        )
        
        print("\n🚦 STARTING LLM RACE!")
        print("Watch as real AI models make racing decisions...\n")
        
        if use_graphics:
            print("💡 TIP: Watch the console for LLM decisions!")
            print("Press ESC in the race window to exit\n")
        
        # Run the race with full error tracking
        try:
            results = simulator.simulate_race()
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR during race: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        # Display results
        print("\n🏁 RACE RESULTS 🏁")
        print("=" * 60)
        
        if not results or "finishing_order" not in results or not results["finishing_order"]:
            print("⚠️ No race results available!")
            if "error" in results:
                print(f"Error: {results['error']}")
            return
            
        for result in results["finishing_order"]:
            position = result["position"]
            name = result["driver"]
            model = result["model"]
            time = result["total_time"]
            confidence = result["average_confidence"]
            decisions = result["decisions_made"]
            
            if position == 1:
                print(f"🥇 {name} ({model})")
            elif position == 2:
                print(f"🥈 {name} ({model})")
            elif position == 3:
                print(f"🥉 {name} ({model})")
            else:
                print(f"{position}. {name} ({model})")
                
            print(f"   Time: {time:.2f}s | Decisions: {decisions} | Avg Confidence: {confidence:.2%}")
            print(f"   Final Fuel: {result['final_fuel']:.1f}% | Tire Wear: {result['tire_wear']:.1f}%")
            print()
        
        # LLM Stats
        if "llm_stats" in results:
            print("\n📊 LLM DECISION STATS:")
            print("=" * 60)
            for driver_name, stats in results["llm_stats"].items():
                print(f"{driver_name}:")
                print(f"  • Model: {stats['model'].split('/')[-1]}")
                print(f"  • Total Decisions: {stats['decisions']}")
                print(f"  • Average Confidence: {stats['avg_confidence']:.2%}")
                if "actions" in stats:
                    print(f"  • Actions: {stats['actions']}")
                print()
        
        print("✨ LLM Racing Demo Complete!")
        print("\n💡 Each decision was made by a real AI model analyzing the race state!")
        print("🔄 Run again to see different AI strategies emerge!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your TOGETHER_API_KEY is valid")
        print("2. Ensure Nexus Connector is installed")
        print("3. Check your internet connection")
        print(f"\nFull error: {type(e).__name__}: {str(e)}")


if __name__ == "__main__":
    # Run async main with full error catching
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n\n🚨 UNHANDLED ERROR: {type(e).__name__}")
        print(f"Message: {e}")
        print("\nFull stack trace:")
        import traceback
        traceback.print_exc()
        print("\n💡 This is the error you're seeing that I'm not catching!")