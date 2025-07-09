from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
from race_config import ChampionshipSettings, RaceSettings
from challenge_generator import RaceChallengeGenerator, ChallengeType
from intelligent_race_simulator import IntelligentRaceSimulator
from data_prizes import DataPrizeSystem
from ai_personalities import AIPersonalitySystem


@dataclass
class DriverStanding:
    """Driver championship standing"""
    driver_name: str
    points: int = 0
    wins: int = 0
    podiums: int = 0
    poles: int = 0
    fastest_laps: int = 0
    dnfs: int = 0
    races_completed: int = 0
    best_finish: int = 99
    worst_finish: int = 0
    average_finish: float = 0.0
    current_streak: str = ""  # e.g., "3 wins", "5 podiums"
    
    def add_race_result(self, position: int, points: int, pole: bool = False, 
                       fastest_lap: bool = False, dnf: bool = False):
        """Update standings with race result"""
        self.points += points
        self.races_completed += 1
        
        if dnf:
            self.dnfs += 1
        else:
            if position == 1:
                self.wins += 1
            if position <= 3:
                self.podiums += 1
                
            self.best_finish = min(self.best_finish, position)
            self.worst_finish = max(self.worst_finish, position)
            
        if pole:
            self.poles += 1
        if fastest_lap:
            self.fastest_laps += 1
            
        # Update average
        total_positions = self.average_finish * (self.races_completed - 1) + position
        self.average_finish = total_positions / self.races_completed


@dataclass
class TeamStanding:
    """Team championship standing"""
    team_name: str
    drivers: List[str]
    points: int = 0
    wins: int = 0
    podiums: int = 0
    double_podiums: int = 0  # Both drivers on podium
    
    
@dataclass
class RaceRecord:
    """Record of a single race in the championship"""
    round_number: int
    race_name: str
    track: str
    date: datetime
    weather: str
    laps: int
    
    # Results
    positions: Dict[int, str]  # position -> driver
    points_awarded: Dict[str, int]  # driver -> points
    fastest_lap: Optional[str] = None
    pole_position: Optional[str] = None
    
    # Race highlights
    total_overtakes: int = 0
    safety_cars: int = 0
    dnfs: List[str] = field(default_factory=list)
    notable_events: List[str] = field(default_factory=list)
    
    
class ChampionshipManager:
    """Manages a full championship season"""
    
    def __init__(self, settings: ChampionshipSettings, drivers: List[str], 
                 personality_system: Optional[AIPersonalitySystem] = None):
        self.settings = settings
        self.drivers = drivers
        self.personality_system = personality_system
        
        # Initialize standings
        self.driver_standings: Dict[str, DriverStanding] = {}
        for driver in drivers:
            self.driver_standings[driver] = DriverStanding(driver)
            
        # Team standings if enabled
        self.team_standings: Dict[str, TeamStanding] = {}
        if settings.enable_teams:
            self._initialize_teams()
            
        # Race records
        self.race_records: List[RaceRecord] = []
        self.current_round = 0
        
        # Additional systems
        self.prize_system = DataPrizeSystem()
        self.challenge_generator = RaceChallengeGenerator()
        
        # Championship state
        self.is_complete = False
        self.champion: Optional[str] = None
        self.team_champion: Optional[str] = None
        
    def _initialize_teams(self):
        """Initialize team standings"""
        teams = {}
        for driver, team in self.settings.team_assignments.items():
            if team not in teams:
                teams[team] = []
            teams[team].append(driver)
            
        for team_name, team_drivers in teams.items():
            self.team_standings[team_name] = TeamStanding(team_name, team_drivers)
            
    def run_next_race(self, cars, display_progress: bool = True) -> RaceRecord:
        """Run the next race in the championship"""
        if self.current_round >= len(self.settings.races):
            print("⚠️  Championship is complete!")
            return None
            
        race_config = self.settings.races[self.current_round]
        self.current_round += 1
        
        # Create track based on configuration
        from race_track import RaceTrack
        if race_config.track_type.value == "speed_track":
            track = RaceTrack.create_speed_track()
        elif race_config.track_type.value == "technical_track":
            track = RaceTrack.create_technical_track()
        elif race_config.track_type.value == "mixed_track":
            track = RaceTrack.create_mixed_track()
        else:
            track = RaceTrack.create_endurance_track()
            
        track.weather_conditions = race_config.weather
        
        # Display pre-race info
        if display_progress:
            self._display_pre_race_info(race_config, track)
            
        # Run qualifying if enabled
        grid_order = cars.copy()
        pole_sitter = None
        if race_config.qualifying_enabled:
            grid_order, pole_sitter = self._run_qualifying(cars, track)
            
        # Apply reverse grid if needed
        if race_config.reverse_grid:
            grid_order = grid_order[::-1]
            
        # Run the race
        simulator = IntelligentRaceSimulator(
            track, grid_order, race_config.laps,
            enable_telemetry=race_config.enable_telemetry,
            enable_intelligence=race_config.enable_intelligence,
            prize_system=self.prize_system if race_config.enable_intelligence else None
        )
        
        results = simulator.simulate_race()
        
        # Process results
        race_record = self._process_race_results(results, race_config, track.name, pole_sitter)
        
        # Update standings
        self._update_standings(race_record)
        
        # Update data prizes
        if race_config.enable_telemetry:
            self.prize_system.distribute_prizes(results, simulator.telemetry)
            
        # Display post-race info
        if display_progress:
            self._display_post_race_info(race_record)
            self._display_championship_standings()
            
        # Check if championship is decided
        self._check_championship_status()
        
        return race_record
    
    def _run_qualifying(self, cars, track) -> Tuple[List, Optional[str]]:
        """Run qualifying session"""
        print("\n🏁 QUALIFYING SESSION")
        print("="*40)
        
        # Quick 1-lap qualifying
        qual_sim = IntelligentRaceSimulator(track, cars, laps=1, enable_telemetry=False)
        qual_results = qual_sim.simulate_race()
        
        # Extract grid order
        grid_order = []
        for pos in sorted(qual_results["positions"].keys()):
            driver_name = qual_results["positions"][pos]["name"]
            grid_order.append(next(car for car in cars if car.name == driver_name))
            
        pole_sitter = qual_results["positions"][1]["name"]
        
        print(f"\n⚡ POLE POSITION: {pole_sitter}")
        print("\nStarting Grid:")
        for i, car in enumerate(grid_order[:5]):  # Show top 5
            print(f"  {i+1}. {car.name}")
            
        return grid_order, pole_sitter
    
    def _process_race_results(self, results: Dict, race_config: RaceSettings, 
                            track_name: str, pole_sitter: Optional[str]) -> RaceRecord:
        """Process race results into race record"""
        # Calculate points
        points_awarded = {}
        positions_dict = {}
        
        for position, data in results["positions"].items():
            driver_name = data["name"]
            positions_dict[position] = driver_name
            
            # Base points
            if position <= len(self.settings.points_system):
                points = self.settings.points_system[position - 1]
            else:
                points = 0
                
            # Sprint race reduced points
            if self.current_round - 1 in self.settings.sprint_races:
                points = points // 2
                
            # Double points finale
            if self.settings.double_points_finale and self.current_round == len(self.settings.races):
                points *= 2
                
            points_awarded[driver_name] = points
            
        # Fastest lap point
        fastest_lap_driver = results.get("fastest_lap", {}).get("driver")
        if fastest_lap_driver and self.settings.fastest_lap_point:
            # Only if in top 10
            for pos, driver in positions_dict.items():
                if driver == fastest_lap_driver and pos <= 10:
                    points_awarded[driver] = points_awarded.get(driver, 0) + 1
                    break
                    
        # Create race record
        record = RaceRecord(
            round_number=self.current_round,
            race_name=f"Round {self.current_round}",
            track=track_name,
            date=datetime.now(),
            weather=race_config.weather,
            laps=race_config.laps,
            positions=positions_dict,
            points_awarded=points_awarded,
            fastest_lap=fastest_lap_driver,
            pole_position=pole_sitter,
            total_overtakes=len([e for e in results["events"] if "OVERTAKE" in e.event_type]),
            notable_events=self._extract_notable_events(results)
        )
        
        self.race_records.append(record)
        return record
    
    def _extract_notable_events(self, results: Dict) -> List[str]:
        """Extract notable events from race"""
        notable = []
        
        # Find dramatic moments
        events = results.get("events", [])
        for event in events:
            if event.event_type in ["CRASH", "INTELLIGENT_OVERTAKE"]:
                notable.append(f"{event.car_name}: {event.details}")
                
        # Add rivalry moments if personality system exists
        if self.personality_system:
            intel_events = [e for e in events if "rivalry" in e.details.lower()]
            for event in intel_events[:3]:  # Top 3 rivalry moments
                notable.append(event.details)
                
        return notable[:5]  # Limit to 5 notable events
    
    def _update_standings(self, race_record: RaceRecord):
        """Update championship standings"""
        # Update driver standings
        for position, driver in race_record.positions.items():
            if driver in self.driver_standings:
                standing = self.driver_standings[driver]
                points = race_record.points_awarded.get(driver, 0)
                
                standing.add_race_result(
                    position=position,
                    points=points,
                    pole=(driver == race_record.pole_position),
                    fastest_lap=(driver == race_record.fastest_lap),
                    dnf=(driver in race_record.dnfs)
                )
                
        # Update team standings if enabled
        if self.settings.enable_teams:
            for team_name, team in self.team_standings.items():
                team_points = 0
                team_wins = 0
                team_podiums = 0
                
                for driver in team.drivers:
                    if driver in race_record.points_awarded:
                        team_points += race_record.points_awarded[driver]
                        
                    if driver in race_record.positions.values():
                        pos = next(p for p, d in race_record.positions.items() if d == driver)
                        if pos == 1:
                            team_wins += 1
                        if pos <= 3:
                            team_podiums += 1
                            
                team.points += team_points
                team.wins += team_wins
                team.podiums += team_podiums
                
                # Check for double podium
                team_positions = []
                for driver in team.drivers:
                    if driver in race_record.positions.values():
                        pos = next(p for p, d in race_record.positions.items() if d == driver)
                        team_positions.append(pos)
                        
                if len([p for p in team_positions if p <= 3]) == 2:
                    team.double_podiums += 1
                    
    def _check_championship_status(self):
        """Check if championship is decided"""
        races_remaining = len(self.settings.races) - self.current_round
        max_points_available = races_remaining * max(self.settings.points_system)
        
        if self.settings.fastest_lap_point:
            max_points_available += races_remaining
            
        if self.settings.double_points_finale and races_remaining == 1:
            max_points_available *= 2
            
        # Sort standings
        sorted_standings = sorted(self.driver_standings.values(), 
                                key=lambda x: x.points, reverse=True)
        
        if len(sorted_standings) >= 2:
            leader = sorted_standings[0]
            second = sorted_standings[1]
            
            if leader.points - second.points > max_points_available:
                self.champion = leader.driver_name
                self.is_complete = True
                print(f"\n🏆🏆🏆 {self.champion} IS THE CHAMPION! 🏆🏆🏆")
                
    def _display_pre_race_info(self, race_config: RaceSettings, track):
        """Display pre-race information"""
        print(f"\n{'='*60}")
        print(f"🏁 CHAMPIONSHIP ROUND {self.current_round}/{len(self.settings.races)}")
        print(f"{'='*60}")
        print(f"📍 Track: {track.name}")
        print(f"🌤️  Weather: {race_config.weather}")
        print(f"🏎️  Laps: {race_config.laps}")
        
        if self.current_round - 1 in self.settings.sprint_races:
            print("⚡ SPRINT RACE - Half Points")
        if self.current_round == len(self.settings.races) and self.settings.double_points_finale:
            print("💰 DOUBLE POINTS FINALE")
            
    def _display_post_race_info(self, race_record: RaceRecord):
        """Display post-race information"""
        print(f"\n🏁 RACE RESULTS - Round {race_record.round_number}")
        print("="*40)
        
        # Podium
        for pos in range(1, 4):
            if pos in race_record.positions:
                driver = race_record.positions[pos]
                points = race_record.points_awarded.get(driver, 0)
                print(f"{pos}. {driver} - {points} points")
                
        # Special mentions
        if race_record.fastest_lap:
            print(f"\n⚡ Fastest Lap: {race_record.fastest_lap}")
        if race_record.pole_position:
            print(f"🏁 Pole Position: {race_record.pole_position}")
            
        # Notable events
        if race_record.notable_events:
            print("\n📰 Notable Events:")
            for event in race_record.notable_events[:3]:
                print(f"  - {event}")
                
    def _display_championship_standings(self):
        """Display current championship standings"""
        print(f"\n📊 CHAMPIONSHIP STANDINGS (After Round {self.current_round})")
        print("="*50)
        
        sorted_standings = sorted(self.driver_standings.values(), 
                                key=lambda x: x.points, reverse=True)
        
        for i, standing in enumerate(sorted_standings):
            gap = "" if i == 0 else f"(-{sorted_standings[0].points - standing.points})"
            print(f"{i+1}. {standing.driver_name:15} {standing.points:3} pts {gap:>6} | "
                  f"W:{standing.wins} P:{standing.podiums} FL:{standing.fastest_laps}")
            
        # Team standings if enabled
        if self.settings.enable_teams and self.team_standings:
            print(f"\n🏢 TEAM STANDINGS")
            print("="*50)
            
            sorted_teams = sorted(self.team_standings.values(), 
                                key=lambda x: x.points, reverse=True)
            
            for i, team in enumerate(sorted_teams):
                print(f"{i+1}. {team.team_name:20} {team.points:3} pts | "
                      f"W:{team.wins} P:{team.podiums} DP:{team.double_podiums}")
                
    def get_championship_summary(self) -> Dict:
        """Get comprehensive championship summary"""
        summary = {
            "name": self.settings.name,
            "rounds_completed": self.current_round,
            "total_rounds": len(self.settings.races),
            "is_complete": self.is_complete,
            "champion": self.champion,
            "team_champion": self.team_champion,
            "driver_standings": {},
            "team_standings": {},
            "statistics": self._calculate_statistics()
        }
        
        # Add driver standings
        for driver, standing in self.driver_standings.items():
            summary["driver_standings"][driver] = {
                "points": standing.points,
                "wins": standing.wins,
                "podiums": standing.podiums,
                "average_finish": standing.average_finish,
                "best_finish": standing.best_finish
            }
            
        # Add team standings
        if self.settings.enable_teams:
            for team, standing in self.team_standings.items():
                summary["team_standings"][team] = {
                    "points": standing.points,
                    "wins": standing.wins,
                    "double_podiums": standing.double_podiums
                }
                
        return summary
    
    def _calculate_statistics(self) -> Dict:
        """Calculate championship statistics"""
        stats = {
            "total_overtakes": sum(r.total_overtakes for r in self.race_records),
            "different_winners": len(set(r.positions.get(1) for r in self.race_records if 1 in r.positions)),
            "closest_finish": self._find_closest_finish(),
            "most_overtakes_race": max((r.total_overtakes, r.round_number) for r in self.race_records)[1] if self.race_records else 0,
            "rivalry_score": self._calculate_rivalry_intensity()
        }
        
        return stats
    
    def _find_closest_finish(self) -> Optional[int]:
        """Find the closest championship finish"""
        if self.current_round < 2:
            return None
            
        min_gap = float('inf')
        closest_round = None
        
        for i in range(1, self.current_round):
            # Calculate standings after round i
            temp_standings = {}
            for record in self.race_records[:i]:
                for driver, points in record.points_awarded.items():
                    temp_standings[driver] = temp_standings.get(driver, 0) + points
                    
            sorted_drivers = sorted(temp_standings.items(), key=lambda x: x[1], reverse=True)
            if len(sorted_drivers) >= 2:
                gap = sorted_drivers[0][1] - sorted_drivers[1][1]
                if gap < min_gap:
                    min_gap = gap
                    closest_round = i
                    
        return closest_round
    
    def _calculate_rivalry_intensity(self) -> float:
        """Calculate overall rivalry intensity in championship"""
        if not self.personality_system:
            return 0.0
            
        total_intensity = 0.0
        rivalry_count = 0
        
        for driver in self.drivers:
            profile = self.personality_system.profiles.get(driver)
            if profile:
                for rel in profile.relationships.values():
                    if rel.relationship_type.value in ["rival", "nemesis"]:
                        total_intensity += rel.intensity
                        rivalry_count += 1
                        
        return total_intensity / rivalry_count if rivalry_count > 0 else 0.0
    
    def save_championship(self, filename: str):
        """Save championship state to file"""
        state = {
            "settings": self.settings.__dict__,
            "current_round": self.current_round,
            "race_records": [r.__dict__ for r in self.race_records],
            "driver_standings": {d: s.__dict__ for d, s in self.driver_standings.items()},
            "team_standings": {t: s.__dict__ for t, s in self.team_standings.items()},
            "is_complete": self.is_complete,
            "champion": self.champion
        }
        
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2, default=str)
            
        print(f"✅ Championship saved to {filename}")