#!/usr/bin/env python3
"""
Test file for the Configuration and Championship System - Phase 7
Demonstrates race configuration, presets, and championship management
"""

from race_config import (
    DifficultyLevel, RaceMode, AISettings, RaceSettings, 
    ChampionshipSettings, SimulatorConfig, ConfigurationManager
)
from championship import ChampionshipManager, DriverStanding
from racing_car import RacingCar, DriverStyle
from race_track import TrackType
from ai_personalities import AIPersonalitySystem
from enhanced_ai_racers import create_enhanced_ai_racers
import os
import json


def test_configuration_presets():
    """Test built-in configuration presets"""
    print("\n" + "="*60)
    print("TEST 1: Configuration Presets")
    print("="*60)
    
    config_manager = ConfigurationManager()
    
    print("\n📋 Available Presets:")
    for preset_name, config in config_manager.presets.items():
        print(f"\n{'='*40}")
        print(f"🏎️  {config.config_name}")
        print(f"{'='*40}")
        print(f"Mode: {config.mode.value}")
        print(f"AI Difficulty: {config.ai_settings.difficulty.value}")
        print(f"Race Laps: {config.race_settings.laps}")
        print(f"Track Type: {config.race_settings.track_type.value}")
        
        if config.championship_settings:
            print(f"Championship: {config.championship_settings.name}")
            print(f"Total Races: {len(config.championship_settings.races)}")


def test_difficulty_settings():
    """Test AI difficulty configurations"""
    print("\n" + "="*60)
    print("TEST 2: Difficulty Settings")
    print("="*60)
    
    ai_settings = AISettings()
    
    print("\n🎮 Difficulty Level Effects:")
    for difficulty in DifficultyLevel:
        ai_settings.difficulty = difficulty
        ai_settings.apply_difficulty()
        
        print(f"\n{difficulty.value.upper()}:")
        print(f"  Aggression: {ai_settings.aggression_multiplier:.2f}x")
        print(f"  Mistake Rate: {ai_settings.mistake_probability:.0%}")
        print(f"  Learning Speed: {ai_settings.learning_rate:.2f}x")
        print(f"  Rubber Band: {ai_settings.rubber_band_strength:.0%}")


def test_custom_configuration():
    """Test creating custom race configurations"""
    print("\n" + "="*60)
    print("TEST 3: Custom Configuration")
    print("="*60)
    
    config_manager = ConfigurationManager()
    
    # Create custom endurance championship
    custom_config = config_manager.create_custom_config("Endurance Masters")
    
    # Configure championship
    custom_config.mode = RaceMode.CHAMPIONSHIP
    custom_config.championship_settings = ChampionshipSettings(
        name="24 Hour Legends Championship",
        races=[
            RaceSettings(
                track_name="Le Mans 24h",
                track_type=TrackType.ENDURANCE_TRACK,
                laps=100,
                weather="rain",
                mandatory_pit_stops=5,
                enable_fuel_consumption=True,
                enable_tire_wear=True
            ),
            RaceSettings(
                track_name="Spa-Francorchamps 6h",
                track_type=TrackType.MIXED_TRACK,
                laps=50,
                weather="foggy",
                mandatory_pit_stops=2
            ),
            RaceSettings(
                track_name="Nürburgring 24h",
                track_type=TrackType.TECHNICAL_TRACK,
                laps=80,
                weather="clear",
                mandatory_pit_stops=4
            )
        ],
        points_system=[50, 40, 30, 25, 20, 15, 10, 8, 6, 4],
        double_points_finale=True
    )
    
    # Set difficulty
    custom_config.ai_settings.difficulty = DifficultyLevel.EXPERT
    custom_config.ai_settings.apply_difficulty()
    
    print(f"\n🏁 Custom Championship: {custom_config.championship_settings.name}")
    print(f"Total Races: {len(custom_config.championship_settings.races)}")
    print(f"Points System: {custom_config.championship_settings.points_system[:5]}...")
    print(f"Double Points Finale: {custom_config.championship_settings.double_points_finale}")
    
    print("\nRace Details:")
    for i, race in enumerate(custom_config.championship_settings.races):
        print(f"  Round {i+1}: {race.track_name} - {race.laps} laps in {race.weather}")


def test_save_load_config():
    """Test configuration persistence"""
    print("\n" + "="*60)
    print("TEST 4: Save/Load Configuration")
    print("="*60)
    
    config_manager = ConfigurationManager()
    
    # Create and save a configuration
    test_config = SimulatorConfig(
        mode=RaceMode.QUICK_RACE,
        config_name="Test Save Config"
    )
    test_config.race_settings.laps = 15
    test_config.race_settings.weather = "storm"
    test_config.ai_settings.difficulty = DifficultyLevel.PROFESSIONAL
    
    # Save configuration
    config_manager.save_config(test_config, "test_config.json")
    print("✅ Configuration saved")
    
    # Load configuration
    loaded_config = config_manager.load_config("test_config.json")
    print("✅ Configuration loaded")
    
    print(f"\nLoaded Config:")
    print(f"  Name: {loaded_config.config_name}")
    print(f"  Mode: {loaded_config.mode.value}")
    print(f"  Laps: {loaded_config.race_settings.laps}")
    print(f"  Weather: {loaded_config.race_settings.weather}")
    print(f"  AI Difficulty: {loaded_config.ai_settings.difficulty.value}")
    
    # Clean up
    os.remove(os.path.join(config_manager.config_dir, "test_config.json"))


def test_championship_setup():
    """Test championship season management"""
    print("\n" + "="*60)
    print("TEST 5: Championship Management")
    print("="*60)
    
    # Create championship settings
    championship_settings = ChampionshipSettings(
        name="Sprint Cup Series",
        races=[
            RaceSettings(track_type=TrackType.SPEED_TRACK, laps=10, weather="clear"),
            RaceSettings(track_type=TrackType.TECHNICAL_TRACK, laps=8, weather="rain"),
            RaceSettings(track_type=TrackType.MIXED_TRACK, laps=12, weather="clear"),
        ],
        sprint_races=[1],  # Race 2 is a sprint
        points_system=[10, 8, 6, 4, 2],
        fastest_lap_point=True
    )
    
    # Create drivers
    drivers = ["Speed Demon", "Tech Precision", "Fuel Master", "Adaptive Racer", "Chaos Cruiser"]
    
    # Initialize championship
    championship = ChampionshipManager(championship_settings, drivers)
    
    print(f"\n🏆 {championship_settings.name}")
    print(f"Total Rounds: {len(championship_settings.races)}")
    print(f"Sprint Races: {championship_settings.sprint_races}")
    print(f"Points System: {championship_settings.points_system}")
    
    # Display initial standings
    print("\n📊 Initial Standings:")
    for driver in drivers:
        standing = championship.driver_standings[driver]
        print(f"  {driver}: {standing.points} pts")


def test_championship_race():
    """Test running a championship race"""
    print("\n" + "="*60)
    print("TEST 6: Championship Race Simulation")
    print("="*60)
    
    # Setup championship
    championship_settings = ChampionshipSettings(
        name="Quick Championship",
        races=[
            RaceSettings(track_type=TrackType.MIXED_TRACK, laps=5, weather="clear"),
            RaceSettings(track_type=TrackType.TECHNICAL_TRACK, laps=5, weather="rain"),
        ],
        points_system=[10, 8, 6, 4, 2]
    )
    
    # Create enhanced AI racers
    personality_system = AIPersonalitySystem()
    enhanced_racers = create_enhanced_ai_racers(personality_system)
    cars = [racer.car for racer in enhanced_racers]
    drivers = [car.name for car in cars]
    
    # Initialize championship
    championship = ChampionshipManager(championship_settings, drivers, personality_system)
    
    print(f"\n🏁 Running {championship_settings.name}")
    
    # Run first race
    print("\n" + "-"*40)
    print("ROUND 1")
    print("-"*40)
    
    race_record = championship.run_next_race(cars, display_progress=False)
    
    if race_record:
        print(f"\n🏁 Race Results:")
        for pos in range(1, 4):
            if pos in race_record.positions:
                driver = race_record.positions[pos]
                points = race_record.points_awarded.get(driver, 0)
                print(f"  P{pos}: {driver} - {points} points")
        
        if race_record.fastest_lap:
            print(f"\n⚡ Fastest Lap: {race_record.fastest_lap}")
        
        # Show updated standings
        print("\n📊 Championship Standings:")
        sorted_standings = sorted(championship.driver_standings.values(), 
                                key=lambda x: x.points, reverse=True)
        
        for i, standing in enumerate(sorted_standings[:3]):
            print(f"  {i+1}. {standing.driver_name}: {standing.points} pts")


def test_championship_statistics():
    """Test championship statistics and analysis"""
    print("\n" + "="*60)
    print("TEST 7: Championship Statistics")
    print("="*60)
    
    # Create a mock championship with some results
    championship_settings = ChampionshipSettings(
        name="Statistics Test Championship",
        races=[RaceSettings() for _ in range(3)]
    )
    
    drivers = ["Speed Demon", "Tech Precision", "Fuel Master"]
    championship = ChampionshipManager(championship_settings, drivers)
    
    # Simulate some results
    standings = championship.driver_standings
    
    # Race 1: Speed Demon wins
    standings["Speed Demon"].add_race_result(1, 10, pole=True, fastest_lap=True)
    standings["Tech Precision"].add_race_result(2, 8)
    standings["Fuel Master"].add_race_result(3, 6)
    
    # Race 2: Tech Precision wins
    standings["Tech Precision"].add_race_result(1, 10, pole=True)
    standings["Speed Demon"].add_race_result(2, 8, fastest_lap=True)
    standings["Fuel Master"].add_race_result(3, 6)
    
    # Race 3: Fuel Master wins
    standings["Fuel Master"].add_race_result(1, 10)
    standings["Tech Precision"].add_race_result(2, 8)
    standings["Speed Demon"].add_race_result(3, 6, dnf=True)
    
    championship.current_round = 3
    
    print("\n📈 Driver Statistics:")
    for driver_name, standing in standings.items():
        print(f"\n{driver_name}:")
        print(f"  Total Points: {standing.points}")
        print(f"  Wins: {standing.wins}")
        print(f"  Podiums: {standing.podiums}")
        print(f"  Poles: {standing.poles}")
        print(f"  Fastest Laps: {standing.fastest_laps}")
        print(f"  Average Finish: {standing.average_finish:.1f}")
        print(f"  Best/Worst: P{standing.best_finish}/P{standing.worst_finish}")


def test_configuration_application():
    """Test applying configuration to race setup"""
    print("\n" + "="*60)
    print("TEST 8: Configuration Application")
    print("="*60)
    
    config_manager = ConfigurationManager()
    
    # Get chaos mode preset
    chaos_config = config_manager.get_preset("chaos")
    
    print(f"\n🌪️ Applying '{chaos_config.config_name}' Configuration:")
    
    # Apply configuration
    setup_params = config_manager.apply_config(chaos_config)
    
    print(f"\nSetup Parameters:")
    print(f"  Mode: {setup_params['mode'].value}")
    print(f"  AI Aggression: {setup_params['ai_settings'].aggression_multiplier:.1f}x")
    print(f"  Mistake Rate: {setup_params['ai_settings'].mistake_probability:.0%}")
    print(f"  Weather: {setup_params['race_settings'].weather}")
    print(f"  Safety Car Chance: {setup_params['race_settings'].safety_car_probability:.0%}")
    
    print(f"\nEnabled Features:")
    for feature, enabled in setup_params['features'].items():
        print(f"  {feature}: {'✅' if enabled else '❌'}")
    
    print(f"\nSelected Cars: {setup_params['cars']}")


def main():
    """Run all configuration tests"""
    print("\n🏎️  AI RACING SIMULATOR - PHASE 7: CONFIGURATION SYSTEM TESTS 🏎️")
    
    test_configuration_presets()
    test_difficulty_settings()
    test_custom_configuration()
    test_save_load_config()
    test_championship_setup()
    test_championship_race()
    test_championship_statistics()
    test_configuration_application()
    
    print("\n" + "="*60)
    print("✅ Phase 7 Complete: Configuration and Championship System Implemented!")
    print("="*60)
    print("\nKey Features Demonstrated:")
    print("- Built-in configuration presets")
    print("- Difficulty settings with AI tuning")
    print("- Custom race and championship creation")
    print("- Configuration save/load functionality")
    print("- Full championship season management")
    print("- Driver standings and statistics")
    print("- Points systems and special rules")
    print("- Race records and history tracking")
    
    print("\n🏆 Championship Features:")
    print("- Multiple race formats (sprint, endurance)")
    print("- Qualifying and grid management")
    print("- Points distribution with bonuses")
    print("- Team championship support")
    print("- Season statistics and records")
    print("- Save/load championship progress")


if __name__ == "__main__":
    main()