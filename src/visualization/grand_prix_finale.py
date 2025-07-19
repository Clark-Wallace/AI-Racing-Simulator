#!/usr/bin/env python3
"""
AI Racing Simulator - Grand Prix Finale
The ultimate showcase of all systems working in harmony
"""

import time
import random
from datetime import datetime
from typing import Dict, List, Optional

# Import all our systems
from ..core.racing_car import RacingCar, DriverStyle
from ..core.race_track import RaceTrack, TrackType
from ..systems.race_config import (
    ConfigurationManager, ChampionshipSettings, RaceSettings,
    DifficultyLevel, AISettings
)
from ..systems.championship import ChampionshipManager
from ..intelligence.ai_personalities import AIPersonalitySystem, EmotionalState
from ..intelligence.enhanced_ai_racers import create_enhanced_ai_racers
from ..intelligence.data_prizes import DataPrizeSystem
from ..systems.challenge_generator import RaceChallengeGenerator, ChallengeType
import json


class GrandPrixFinale:
    """Orchestrates the ultimate AI racing championship showcase"""
    
    def __init__(self):
        self.personality_system = AIPersonalitySystem()
        self.enhanced_racers = create_enhanced_ai_racers(self.personality_system)
        self.cars = [racer.car for racer in self.enhanced_racers]
        self.prize_system = DataPrizeSystem()
        self.challenge_generator = RaceChallengeGenerator()
        
        # Championship configuration
        self.championship_config = self._create_ultimate_championship()
        self.championship = None
        
        # Display settings
        self.dramatic_pause = 1.0  # Seconds between dramatic moments
        
    def _create_ultimate_championship(self) -> ChampionshipSettings:
        """Create the ultimate championship configuration"""
        return ChampionshipSettings(
            name="🏆 AI GRAND PRIX WORLD CHAMPIONSHIP 🏆",
            races=[
                # Race 1: Speed Challenge - Monza
                RaceSettings(
                    track_name="Monza Temple of Speed",
                    track_type=TrackType.SPEED_TRACK,
                    laps=15,
                    weather="clear",
                    qualifying_enabled=True,
                    enable_telemetry=True,
                    enable_intelligence=True,
                    enable_personalities=True
                ),
                # Race 2: Technical Mastery - Monaco
                RaceSettings(
                    track_name="Monaco Street Circuit",
                    track_type=TrackType.TECHNICAL_TRACK,
                    laps=20,
                    weather="rain",
                    qualifying_enabled=True,
                    reverse_grid=False,
                    safety_car_probability=0.3
                ),
                # Race 3: Endurance Test - Le Mans
                RaceSettings(
                    track_name="Circuit de la Sarthe",
                    track_type=TrackType.ENDURANCE_TRACK,
                    laps=30,
                    weather="foggy",
                    mandatory_pit_stops=2,
                    enable_fuel_consumption=True,
                    enable_tire_wear=True
                ),
                # Race 4: Sprint Showdown - Silverstone
                RaceSettings(
                    track_name="Silverstone Sprint",
                    track_type=TrackType.MIXED_TRACK,
                    laps=8,
                    weather="clear",
                    qualifying_enabled=False,
                    reverse_grid=True  # Reverse grid sprint!
                ),
                # Race 5: Championship Decider - Spa
                RaceSettings(
                    track_name="Spa-Francorchamps Finale",
                    track_type=TrackType.MIXED_TRACK,
                    laps=25,
                    weather="storm",
                    qualifying_enabled=True,
                    safety_car_probability=0.4
                )
            ],
            points_system=[25, 18, 15, 12, 10, 8, 6, 4, 2, 1],
            sprint_races=[3],  # Silverstone is a sprint
            double_points_finale=True,  # Double points at Spa!
            fastest_lap_point=True,
            enable_teams=True,
            team_assignments={
                "Speed Demon": "RedBull Racing",
                "Tech Precision": "Mercedes AMG",
                "Fuel Master": "Ferrari Scuderia",
                "Adaptive Racer": "McLaren F1",
                "Chaos Cruiser": "Alpine Racing"
            }
        )
    
    def _display_championship_intro(self):
        """Display dramatic championship introduction"""
        print("\n" + "="*80)
        print("🏎️  AI RACING SIMULATOR - GRAND PRIX FINALE 🏎️".center(80))
        print("="*80)
        
        time.sleep(self.dramatic_pause)
        
        print("\n📺 Welcome to the ultimate showcase of AI racing excellence!")
        print("   Five AI personalities. Five unique racing styles.")
        print("   One championship to rule them all.")
        
        time.sleep(self.dramatic_pause)
        
        print("\n🎭 MEET THE COMPETITORS:")
        for racer in self.enhanced_racers:
            profile = racer.profile
            print(f"\n   🏎️  {profile.name} - \"{profile.nickname}\"")
            print(f"      {profile.backstory.split('.')[0]}.")
            print(f"      Signature: {profile.signature_moves[0]}")
            print(f"      Philosophy: \"{profile.racing_philosophy}\"")
            time.sleep(0.5)
        
        time.sleep(self.dramatic_pause)
        
        print("\n🏆 THE CHAMPIONSHIP:")
        print(f"   {self.championship_config.name}")
        print(f"   {len(self.championship_config.races)} Races across legendary circuits")
        print(f"   Points: {self.championship_config.points_system[:5]} ...")
        print(f"   Special: Sprint race, Double points finale, Fastest lap bonus")
        
        time.sleep(self.dramatic_pause)
        
        print("\n💾 DATA PRIZE SYSTEM:")
        print("   Winners gain access to competitor telemetry")
        print("   Strategic advantages accumulate over the season")
        print("   Every position matters for intelligence gathering")
        
        time.sleep(self.dramatic_pause)
    
    def _pre_race_buildup(self, round_num: int, race_config: RaceSettings):
        """Create pre-race atmosphere and storylines"""
        print("\n" + "🏁"*40)
        print(f"\n⚡ ROUND {round_num}: {race_config.track_name.upper()}")
        
        # Weather drama
        if race_config.weather != "clear":
            weather_emoji = {"rain": "🌧️", "storm": "⛈️", "foggy": "🌫️"}.get(race_config.weather, "🌤️")
            print(f"\n{weather_emoji} WARNING: {race_config.weather.upper()} conditions expected!")
            print("   This could shake up the championship...")
        
        # Special race features
        if round_num - 1 in self.championship_config.sprint_races:
            print("\n⚡ SPRINT RACE - Reduced points, maximum attack!")
        
        if race_config.reverse_grid:
            print("\n🔄 REVERSE GRID - Leaders start at the back!")
        
        if round_num == len(self.championship_config.races) and self.championship_config.double_points_finale:
            print("\n💰 DOUBLE POINTS FINALE - Everything on the line!")
        
        # Show current rivalries
        print("\n🥊 Key Rivalries:")
        rivalries = []
        for name, profile in self.personality_system.profiles.items():
            for rival_name, relationship in profile.relationships.items():
                if relationship.relationship_type.value in ["rival", "nemesis"]:
                    if relationship.intensity > 0.5:
                        rivalries.append((name, rival_name, relationship))
        
        for r1, r2, rel in rivalries[:2]:  # Show top 2 rivalries
            print(f"   {r1} vs {r2} - Intensity: {'🔥' * int(rel.intensity * 5)}")
        
        # Pre-race quotes
        print("\n🎙️ Pre-Race Comments:")
        for racer in random.sample(self.enhanced_racers, 3):
            context = {
                "track_type": race_config.track_type.value,
                "weather": race_config.weather,
                "position": random.randint(1, 5)
            }
            quote = self.personality_system.generate_pre_race_quote(racer.profile, context)
            print(f"   {racer.profile.nickname}: \"{quote}\"")
        
        time.sleep(self.dramatic_pause * 2)
    
    def _analyze_championship_situation(self, round_num: int):
        """Analyze championship dynamics"""
        if round_num < 2:
            return
        
        print("\n📊 CHAMPIONSHIP SITUATION:")
        
        sorted_standings = sorted(
            self.championship.driver_standings.values(),
            key=lambda x: x.points,
            reverse=True
        )
        
        # Points gap analysis
        if len(sorted_standings) >= 2:
            leader = sorted_standings[0]
            second = sorted_standings[1]
            gap = leader.points - second.points
            
            if gap == 0:
                print("   🔥 TIED AT THE TOP! Every point crucial!")
            elif gap < 10:
                print(f"   ⚡ Only {gap} points separate the top two!")
            elif gap > 30:
                print(f"   👑 {leader.driver_name} has a commanding {gap} point lead")
        
        # Form analysis
        print("\n📈 Current Form:")
        for standing in sorted_standings[:3]:
            if standing.races_completed >= 2:
                # Check recent results
                momentum = "🔥 ON FIRE" if standing.average_finish < 2.5 else \
                          "📈 Strong" if standing.average_finish < 4 else \
                          "📊 Steady" if standing.average_finish < 6 else "📉 Struggling"
                print(f"   {standing.driver_name}: {momentum} (Avg P{standing.average_finish:.1f})")
    
    def _post_race_drama(self, race_record, round_num: int):
        """Create post-race storylines and drama"""
        print("\n🏁 RACE CLASSIFICATION:")
        
        # Podium with drama
        for pos in range(1, 4):
            if pos in race_record.positions:
                driver = race_record.positions[pos]
                points = race_record.points_awarded.get(driver, 0)
                
                # Find the racer
                racer = next(r for r in self.enhanced_racers if r.car.name == driver)
                
                # Special callouts
                special = ""
                if pos == 1:
                    special = " 🏆 VICTORY!"
                    if racer.profile.wins == 0:
                        special += " - FIRST CAREER WIN!"
                elif driver == race_record.fastest_lap:
                    special = " + Fastest Lap"
                
                print(f"   P{pos}: {driver} - {points} pts{special}")
        
        # Notable events
        if race_record.notable_events:
            print("\n📰 KEY MOMENTS:")
            for event in race_record.notable_events[:3]:
                print(f"   • {event}")
        
        # Emotional reactions
        print("\n💭 Post-Race Reactions:")
        
        # Winner celebration
        if 1 in race_record.positions:
            winner_name = race_record.positions[1]
            winner = next(r for r in self.enhanced_racers if r.car.name == winner_name)
            winner.profile.emotional_state = EmotionalState.CONFIDENT
            quote = self.personality_system.generate_post_race_quote(winner.profile, 1, {})
            print(f"   🏆 {winner.profile.nickname}: \"{quote}\"")
        
        # Random others
        for pos in [2, 5]:
            if pos in race_record.positions:
                driver_name = race_record.positions[pos]
                racer = next(r for r in self.enhanced_racers if r.car.name == driver_name)
                quote = self.personality_system.generate_post_race_quote(racer.profile, pos, {})
                print(f"   P{pos} {racer.profile.nickname}: \"{quote}\"")
        
        # Data prize revelations
        if self.prize_system.race_count > 0:
            print("\n🔍 INTELLIGENCE GATHERED:")
            
            # Show who gained what data
            for driver_name, access_list in self.prize_system.driver_access.items():
                if access_list:
                    latest_access = access_list[-1]
                    if latest_access.race_id == self.prize_system.race_count - 1:
                        targets = list(latest_access.data_access.keys())
                        if targets:
                            print(f"   {driver_name} gained data on: {', '.join(targets)}")
    
    def _championship_finale(self):
        """Epic championship conclusion"""
        print("\n" + "="*80)
        print("🏆 CHAMPIONSHIP FINAL STANDINGS 🏆".center(80))
        print("="*80)
        
        time.sleep(self.dramatic_pause)
        
        # Drum roll...
        print("\n🥁 The moment of truth...")
        time.sleep(self.dramatic_pause * 2)
        
        # Final standings
        sorted_standings = sorted(
            self.championship.driver_standings.values(),
            key=lambda x: x.points,
            reverse=True
        )
        
        # Champion announcement
        champion = sorted_standings[0]
        print(f"\n🏆🏆🏆 {champion.driver_name.upper()} IS THE WORLD CHAMPION! 🏆🏆🏆")
        
        champion_racer = next(r for r in self.enhanced_racers if r.car.name == champion.driver_name)
        print(f"\n   \"{champion_racer.profile.nickname}\" - {champion_racer.profile.backstory.split('.')[0]}.")
        print(f"   Championship Points: {champion.points}")
        print(f"   Wins: {champion.wins} | Podiums: {champion.podiums} | Poles: {champion.poles}")
        
        time.sleep(self.dramatic_pause)
        
        # Full standings
        print("\n📊 FINAL DRIVER STANDINGS:")
        for i, standing in enumerate(sorted_standings):
            symbol = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
            gap = f"(-{sorted_standings[0].points - standing.points})" if i > 0 else ""
            
            print(f"{symbol} {i+1}. {standing.driver_name:15} {standing.points:3} pts {gap:>6}")
            print(f"      Wins: {standing.wins} | Podiums: {standing.podiums} | " +
                  f"Avg: P{standing.average_finish:.1f}")
        
        # Team championship
        if self.championship.settings.enable_teams:
            print("\n🏢 TEAM CHAMPIONSHIP:")
            sorted_teams = sorted(
                self.championship.team_standings.values(),
                key=lambda x: x.points,
                reverse=True
            )
            
            for i, team in enumerate(sorted_teams):
                symbol = "🏆" if i == 0 else "  "
                print(f"{symbol} {i+1}. {team.team_name:20} {team.points:3} pts")
        
        # Season statistics
        stats = self.championship._calculate_statistics()
        print("\n📈 SEASON STATISTICS:")
        print(f"   Total Overtakes: {stats['total_overtakes']}")
        print(f"   Different Winners: {stats['different_winners']}")
        print(f"   Average Rivalry Intensity: {stats['rivalry_score']:.1f}/10")
        
        # Final thoughts
        print("\n🎭 SEASON REFLECTIONS:")
        for racer in sorted_standings[:3]:
            driver = next(r for r in self.enhanced_racers if r.car.name == racer.driver_name)
            profile = driver.profile
            
            # Season summary quote
            if racer == champion:
                quote = "This championship proves that " + profile.racing_philosophy.lower()
            elif racer.points > 100:
                quote = "A strong season, but next year we'll come back stronger!"
            else:
                quote = "We learned a lot this year. The data will make us faster."
            
            print(f"   {profile.nickname}: \"{quote}\"")
        
        # Save championship data
        print("\n💾 Saving championship data...")
        self.championship.save_championship("championship_finale.json")
        
        # Create season summary
        self._create_season_summary()
    
    def _create_season_summary(self):
        """Create detailed season summary file"""
        summary = {
            "championship": self.championship.get_championship_summary(),
            "personality_evolution": {},
            "memorable_moments": self.personality_system.memorable_moments,
            "data_intelligence": self._summarize_data_prizes(),
            "timestamp": datetime.now().isoformat()
        }
        
        # Track personality changes
        for name, profile in self.personality_system.profiles.items():
            summary["personality_evolution"][name] = {
                "emotional_state": profile.emotional_state.value,
                "races_completed": profile.races_completed,
                "wins": profile.wins,
                "traits": [t.value for t in profile.primary_traits],
                "relationships": {
                    rival: {
                        "type": rel.relationship_type.value,
                        "intensity": rel.intensity
                    }
                    for rival, rel in profile.relationships.items()
                }
            }
        
        with open("season_summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print("✅ Season summary saved to season_summary.json")
    
    def _summarize_data_prizes(self) -> Dict:
        """Summarize data prize distribution"""
        summary = {
            "total_races": self.prize_system.race_count,
            "data_collected": {},
            "intelligence_reports": len(self.prize_system.competitor_intelligence)
        }
        
        for driver, access_list in self.prize_system.driver_access.items():
            total_targets = set()
            for access in access_list:
                total_targets.update(access.data_access.keys())
            
            summary["data_collected"][driver] = {
                "unique_targets": len(total_targets),
                "total_accesses": len(access_list)
            }
        
        return summary
    
    def run_championship(self):
        """Run the complete championship showcase"""
        # Introduction
        self._display_championship_intro()
        
        # Initialize championship
        drivers = [car.name for car in self.cars]
        self.championship = ChampionshipManager(
            self.championship_config,
            drivers,
            self.personality_system
        )
        
        # Run each race
        for round_num in range(1, len(self.championship_config.races) + 1):
            # Pre-race buildup
            race_config = self.championship_config.races[round_num - 1]
            self._pre_race_buildup(round_num, race_config)
            
            # Championship situation
            self._analyze_championship_situation(round_num)
            
            # Run the race
            print("\n🏁 LIGHTS OUT AND AWAY WE GO!")
            time.sleep(self.dramatic_pause)
            
            race_record = self.championship.run_next_race(self.cars, display_progress=True)
            
            # Post-race drama
            if race_record:
                self._post_race_drama(race_record, round_num)
            
            # Pause between races
            if round_num < len(self.championship_config.races):
                print("\n" + "="*60)
                print("Press Enter to continue to the next race...")
                input()
        
        # Championship finale
        self._championship_finale()
        
        print("\n" + "="*80)
        print("🏁 Thank you for experiencing the AI Racing Grand Prix Finale! 🏁".center(80))
        print("="*80)


def main():
    """Run the grand finale"""
    print("\n🎮 AI RACING SIMULATOR - GRAND PRIX FINALE")
    print("=" * 50)
    print("\nThis is the ultimate showcase of all systems:")
    print("- 5 AI personalities with emotions and rivalries")
    print("- 5 legendary racing circuits")
    print("- Dynamic weather and race conditions")
    print("- Strategic data prize system")
    print("- Full championship with teams and special rules")
    print("\nReady to witness AI racing at its finest?")
    print("\nPress Enter to begin the championship...")
    input()
    
    # Run the grand finale
    finale = GrandPrixFinale()
    finale.run_championship()


if __name__ == "__main__":
    main()