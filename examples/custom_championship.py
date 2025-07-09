#!/usr/bin/env python3
"""
Custom Championship Example - Create and run a custom championship
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.systems.championship import ChampionshipManager
from src.systems.race_config import ChampionshipSettings, RaceSettings
from src.core.race_track import TrackType
from src.intelligence.ai_personalities import AIPersonalitySystem
from src.intelligence.enhanced_ai_racers import create_enhanced_ai_racers


def main():
    """Create and run a custom championship"""
    print("🏆 AI Racing Simulator - Custom Championship Example")
    print("=" * 60)
    
    # Create championship configuration
    championship_config = ChampionshipSettings(
        name="Custom Demo Championship",
        races=[
            RaceSettings(
                track_name="Monaco Street Circuit",
                track_type=TrackType.TECHNICAL_TRACK,
                laps=15,
                weather="clear",
                qualifying_enabled=True
            ),
            RaceSettings(
                track_name="Monza Speed Circuit",
                track_type=TrackType.SPEED_TRACK,
                laps=10,
                weather="rain",
                qualifying_enabled=True
            ),
            RaceSettings(
                track_name="Silverstone Mixed Circuit",
                track_type=TrackType.MIXED_TRACK,
                laps=12,
                weather="clear",
                qualifying_enabled=False,
                reverse_grid=True
            )
        ],
        points_system=[10, 8, 6, 4, 2],  # Simplified points
        fastest_lap_point=True,
        double_points_finale=True
    )
    
    # Create AI racers
    personality_system = AIPersonalitySystem()
    enhanced_racers = create_enhanced_ai_racers(personality_system)
    cars = [racer.car for racer in enhanced_racers]
    drivers = [car.name for car in cars]
    
    # Initialize championship
    championship = ChampionshipManager(
        championship_config,
        drivers,
        personality_system
    )
    
    print(f"\n🏁 Championship: {championship_config.name}")
    print(f"📅 Races: {len(championship_config.races)}")
    print(f"🏆 Points System: {championship_config.points_system}")
    
    # Run championship
    for race_num in range(len(championship_config.races)):
        print(f"\n{'='*50}")
        print(f"🏁 ROUND {race_num + 1}")
        print(f"{'='*50}")
        
        # Run race
        race_record = championship.run_next_race(cars, display_progress=False)
        
        if race_record:
            print(f"\n🏁 Race Results:")
            for pos in range(1, min(6, len(race_record.positions) + 1)):
                if pos in race_record.positions:
                    driver = race_record.positions[pos]
                    points = race_record.points_awarded.get(driver, 0)
                    print(f"  P{pos}: {driver} - {points} points")
        
        # Show current championship standings
        print(f"\n📊 Championship Standings after Round {race_num + 1}:")
        sorted_standings = sorted(
            championship.driver_standings.values(),
            key=lambda x: x.points,
            reverse=True
        )
        
        for i, standing in enumerate(sorted_standings):
            print(f"  {i+1}. {standing.driver_name}: {standing.points} pts")
    
    # Final championship results
    print(f"\n{'='*60}")
    print("🏆 FINAL CHAMPIONSHIP RESULTS")
    print(f"{'='*60}")
    
    champion = sorted_standings[0]
    print(f"\n🥇 CHAMPION: {champion.driver_name}")
    print(f"   Points: {champion.points}")
    print(f"   Wins: {champion.wins}")
    print(f"   Podiums: {champion.podiums}")
    
    print(f"\n📊 Final Standings:")
    for i, standing in enumerate(sorted_standings):
        print(f"  {i+1}. {standing.driver_name}: {standing.points} pts "
              f"({standing.wins}W, {standing.podiums}P)")
    
    # Save championship
    championship.save_championship("custom_championship_results.json")
    print(f"\n💾 Championship results saved!")


if __name__ == "__main__":
    main()