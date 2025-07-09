#!/usr/bin/env python3
"""
Telemetry Analysis Example - Analyze AI performance data
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.racing_car import RacingCar, DriverStyle
from src.core.race_track import RaceTrack
from src.core.intelligent_race_simulator import IntelligentRaceSimulator
from src.systems.telemetry import TelemetrySystem
from src.intelligence.ai_personalities import AIPersonalitySystem
from src.intelligence.enhanced_ai_racers import create_enhanced_ai_racers


def main():
    """Demonstrate telemetry analysis capabilities"""
    print("📊 AI Racing Simulator - Telemetry Analysis Example")
    print("=" * 60)
    
    # Create AI racers
    personality_system = AIPersonalitySystem()
    enhanced_racers = create_enhanced_ai_racers(personality_system)
    cars = [racer.car for racer in enhanced_racers]
    
    # Create track
    track = RaceTrack.create_technical_track()
    
    print(f"\n🏁 Running telemetry analysis race on {track.name}")
    print(f"📏 Track length: {track.length:.2f} km")
    
    # Run race with telemetry
    simulator = IntelligentRaceSimulator(
        track=track,
        cars=cars,
        laps=15,
        enable_telemetry=True,
        enable_intelligence=True
    )
    
    results = simulator.simulate_race()
    telemetry = simulator.telemetry
    
    print("\n📊 TELEMETRY ANALYSIS")
    print("=" * 40)
    
    # Analyze each driver's performance
    for car in cars:
        print(f"\n🏎️  {car.name} Analysis:")
        
        # Get telemetry data
        car_telemetry = telemetry.get_car_telemetry(car.name)
        
        if car_telemetry:
            # Calculate summary statistics
            metrics = telemetry.calculate_final_metrics(car.name)
            
            print(f"   📈 Performance Summary:")
            print(f"      Top Speed: {metrics.get('top_speed', 0):.1f} km/h")
            print(f"      Avg Speed: {metrics.get('avg_speed', 0):.1f} km/h")
            print(f"      Consistency: {metrics.get('consistency_score', 0):.2f}")
            print(f"      Fuel Efficiency: {metrics.get('fuel_efficiency', 0):.2f}")
            print(f"      Cornering: {metrics.get('cornering_speed', 0):.1f} km/h")
            
            # Performance ratings
            print(f"   ⭐ Ratings:")
            print(f"      Speed: {'⭐' * min(5, int(metrics.get('top_speed', 0) / 70))}")
            print(f"      Handling: {'⭐' * min(5, int(metrics.get('stability_index', 0) * 5))}")
            print(f"      Efficiency: {'⭐' * min(5, int(metrics.get('fuel_efficiency', 0)))}")
            
            # Driver style impact
            style_factor = {
                DriverStyle.AGGRESSIVE: "High speed, high risk",
                DriverStyle.CONSERVATIVE: "Consistent, efficient",
                DriverStyle.TECHNICAL: "Precise, methodical",
                DriverStyle.BALANCED: "Well-rounded performance",
                DriverStyle.CHAOTIC: "Unpredictable, entertaining"
            }
            
            print(f"   🎭 Style Impact: {style_factor.get(car.driver_style, 'Unknown')}")
    
    # Compare performances
    print(f"\n🔍 COMPARATIVE ANALYSIS")
    print("=" * 40)
    
    # Speed comparison
    speed_data = []
    for car in cars:
        metrics = telemetry.calculate_final_metrics(car.name)
        speed_data.append((car.name, metrics.get('top_speed', 0)))
    
    speed_data.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n🏎️  Top Speed Rankings:")
    for i, (name, speed) in enumerate(speed_data):
        print(f"   {i+1}. {name}: {speed:.1f} km/h")
    
    # Consistency comparison
    consistency_data = []
    for car in cars:
        metrics = telemetry.calculate_final_metrics(car.name)
        consistency_data.append((car.name, metrics.get('consistency_score', 0)))
    
    consistency_data.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n📊 Consistency Rankings:")
    for i, (name, consistency) in enumerate(consistency_data):
        print(f"   {i+1}. {name}: {consistency:.3f}")
    
    # Export telemetry data
    print(f"\n💾 Exporting telemetry data...")
    telemetry.export_telemetry("telemetry_analysis_results.json")
    
    # Performance insights
    print(f"\n🔍 PERFORMANCE INSIGHTS")
    print("=" * 40)
    
    # Find best performer by category
    categories = {
        'speed': 'top_speed',
        'handling': 'stability_index',
        'efficiency': 'fuel_efficiency',
        'consistency': 'consistency_score'
    }
    
    for category, metric in categories.items():
        best_performer = max(cars, key=lambda car: telemetry.calculate_final_metrics(car.name).get(metric, 0))
        value = telemetry.calculate_final_metrics(best_performer.name).get(metric, 0)
        print(f"   🏆 Best {category.title()}: {best_performer.name} ({value:.3f})")
    
    print(f"\n✅ Telemetry analysis complete!")


if __name__ == "__main__":
    main()