from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Callable
from enum import Enum
import random
from racing_car import RacingCar, DriverStyle
from race_track import RaceTrack, TrackType, TrackSegment
from race_simulator import RaceSimulator


class ChallengeType(Enum):
    # Speed Challenges
    DRAG_RACE = "drag_race"
    TIME_TRIAL = "time_trial"
    SPRINT_RACE = "sprint_race"
    
    # Technical Challenges
    PRECISION_DRIVING = "precision_driving"
    OBSTACLE_COURSE = "obstacle_course"
    WEATHER_CHALLENGE = "weather_challenge"
    
    # Strategic Challenges
    FUEL_MANAGEMENT = "fuel_management"
    ENDURANCE_RACE = "endurance_race"
    PURSUIT_RACE = "pursuit_race"
    
    # Mixed Challenges
    FORMULA_RACE = "formula_race"
    ELIMINATION_RACE = "elimination_race"
    RELAY_RACE = "relay_race"


class ChallengeDifficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXTREME = 4


@dataclass
class ChallengeConfig:
    """Configuration for a specific challenge"""
    challenge_type: ChallengeType
    difficulty: ChallengeDifficulty
    name: str
    description: str
    track_config: Optional[Dict] = None
    race_config: Optional[Dict] = None
    scoring_weights: Dict[str, float] = field(default_factory=dict)
    success_criteria: Dict[str, float] = field(default_factory=dict)
    special_rules: List[str] = field(default_factory=list)
    

@dataclass
class ChallengeResult:
    """Results from completing a challenge"""
    challenge_name: str
    participants: List[str]
    rankings: Dict[int, str]
    scores: Dict[str, float]
    telemetry_data: Optional[Dict] = None
    success: bool = False
    summary: str = ""
    

class RaceChallengeGenerator:
    """Generates different types of racing challenges"""
    
    def __init__(self):
        self.challenge_configs = self._initialize_challenges()
        
    def _initialize_challenges(self) -> Dict[ChallengeType, Callable]:
        """Initialize challenge generation functions"""
        return {
            # Speed Challenges
            ChallengeType.DRAG_RACE: self._create_drag_race,
            ChallengeType.TIME_TRIAL: self._create_time_trial,
            ChallengeType.SPRINT_RACE: self._create_sprint_race,
            
            # Technical Challenges
            ChallengeType.PRECISION_DRIVING: self._create_precision_driving,
            ChallengeType.OBSTACLE_COURSE: self._create_obstacle_course,
            ChallengeType.WEATHER_CHALLENGE: self._create_weather_challenge,
            
            # Strategic Challenges
            ChallengeType.FUEL_MANAGEMENT: self._create_fuel_management,
            ChallengeType.ENDURANCE_RACE: self._create_endurance_race,
            ChallengeType.PURSUIT_RACE: self._create_pursuit_race,
            
            # Mixed Challenges
            ChallengeType.FORMULA_RACE: self._create_formula_race,
            ChallengeType.ELIMINATION_RACE: self._create_elimination_race,
            ChallengeType.RELAY_RACE: self._create_relay_race,
        }
    
    def generate_challenge(self, challenge_type: ChallengeType, 
                         difficulty: ChallengeDifficulty = ChallengeDifficulty.MEDIUM) -> ChallengeConfig:
        """Generate a specific type of challenge"""
        if challenge_type in self.challenge_configs:
            return self.challenge_configs[challenge_type](difficulty)
        else:
            raise ValueError(f"Unknown challenge type: {challenge_type}")
    
    def run_challenge(self, config: ChallengeConfig, cars: List[RacingCar]) -> ChallengeResult:
        """Run a challenge and return results"""
        # Create appropriate track
        track = self._create_challenge_track(config)
        
        # Configure race parameters
        laps = config.race_config.get("laps", 1)
        enable_telemetry = config.race_config.get("telemetry", True)
        
        # Run the race
        simulator = RaceSimulator(track, cars, laps, enable_telemetry)
        race_results = simulator.simulate_race()
        
        # Calculate challenge-specific scores
        scores = self._calculate_scores(config, race_results, simulator)
        
        # Determine rankings based on challenge type
        rankings = self._determine_rankings(config, scores, race_results)
        
        # Check success criteria
        success = self._check_success_criteria(config, scores, race_results)
        
        # Compile results
        result = ChallengeResult(
            challenge_name=config.name,
            participants=[car.name for car in cars],
            rankings=rankings,
            scores=scores,
            telemetry_data=self._get_telemetry_summaries(simulator, cars) if enable_telemetry else None,
            success=success,
            summary=self._generate_summary(config, rankings, scores)
        )
        
        return result
    
    # Speed Challenge Creators
    
    def _create_drag_race(self, difficulty: ChallengeDifficulty) -> ChallengeConfig:
        """Create a drag race challenge - pure acceleration and top speed"""
        distance = {
            ChallengeDifficulty.EASY: 0.4,  # 400m
            ChallengeDifficulty.MEDIUM: 0.8,  # 800m
            ChallengeDifficulty.HARD: 1.2,   # 1200m
            ChallengeDifficulty.EXTREME: 1.6  # 1600m
        }[difficulty]
        
        return ChallengeConfig(
            challenge_type=ChallengeType.DRAG_RACE,
            difficulty=difficulty,
            name=f"Drag Race - {distance*1000:.0f}m",
            description="Pure straight-line speed test. No corners, just raw acceleration!",
            track_config={
                "type": "drag_strip",
                "length": distance,
                "segments": [TrackSegment(distance * 1000, True)]
            },
            race_config={"laps": 1, "telemetry": True},
            scoring_weights={
                "finish_time": 0.7,
                "top_speed": 0.2,
                "acceleration": 0.1
            },
            success_criteria={
                "finish_time": distance * 10,  # seconds
                "top_speed": 350  # km/h
            },
            special_rules=["No fuel limits", "No tire wear", "Single lap only"]
        )
    
    def _create_time_trial(self, difficulty: ChallengeDifficulty) -> ChallengeConfig:
        """Create a time trial challenge - fastest lap time"""
        laps = {
            ChallengeDifficulty.EASY: 1,
            ChallengeDifficulty.MEDIUM: 3,
            ChallengeDifficulty.HARD: 5,
            ChallengeDifficulty.EXTREME: 10
        }[difficulty]
        
        return ChallengeConfig(
            challenge_type=ChallengeType.TIME_TRIAL,
            difficulty=difficulty,
            name=f"Time Trial - {laps} Lap{'s' if laps > 1 else ''}",
            description="Set the fastest lap time. Consistency is key!",
            track_config={"type": "mixed"},  # Will use existing mixed track
            race_config={"laps": laps, "telemetry": True},
            scoring_weights={
                "best_lap": 0.5,
                "average_lap": 0.3,
                "consistency": 0.2
            },
            success_criteria={
                "best_lap": 50,  # seconds
                "consistency": 2  # variance in seconds
            },
            special_rules=["Solo run - no traffic", "Perfect conditions"]
        )
    
    def _create_sprint_race(self, difficulty: ChallengeDifficulty) -> ChallengeConfig:
        """Create a sprint race - short, intense racing"""
        laps = {
            ChallengeDifficulty.EASY: 3,
            ChallengeDifficulty.MEDIUM: 5,
            ChallengeDifficulty.HARD: 8,
            ChallengeDifficulty.EXTREME: 12
        }[difficulty]
        
        return ChallengeConfig(
            challenge_type=ChallengeType.SPRINT_RACE,
            difficulty=difficulty,
            name=f"Sprint Race - {laps} Laps",
            description="Short, high-intensity race. Push hard from start to finish!",
            track_config={"type": "speed"},
            race_config={"laps": laps, "telemetry": True},
            scoring_weights={
                "position": 0.6,
                "total_time": 0.2,
                "overtakes": 0.2
            },
            success_criteria={
                "position": 3,  # Top 3 finish
                "overtakes": 2  # At least 2 overtakes
            },
            special_rules=["Full racing conditions", "Aggressive driving rewarded"]
        )
    
    # Technical Challenge Creators
    
    def _create_precision_driving(self, difficulty: ChallengeDifficulty) -> ChallengeConfig:
        """Create a precision driving challenge - accuracy over speed"""
        corner_count = {
            ChallengeDifficulty.EASY: 6,
            ChallengeDifficulty.MEDIUM: 10,
            ChallengeDifficulty.HARD: 14,
            ChallengeDifficulty.EXTREME: 20
        }[difficulty]
        
        return ChallengeConfig(
            challenge_type=ChallengeType.PRECISION_DRIVING,
            difficulty=difficulty,
            name=f"Precision Course - {corner_count} Corners",
            description="Navigate tight corners with perfect precision. Speed is secondary to accuracy!",
            track_config={"type": "technical"},
            race_config={"laps": 2, "telemetry": True},
            scoring_weights={
                "cornering_efficiency": 0.4,
                "consistency": 0.3,
                "clean_laps": 0.2,
                "finish_time": 0.1
            },
            success_criteria={
                "cornering_efficiency": 0.85,  # 85% efficiency
                "incidents": 0  # No crashes
            },
            special_rules=["Penalties for leaving track", "Smooth driving rewarded"]
        )
    
    def _create_obstacle_course(self, difficulty: ChallengeDifficulty) -> ChallengeConfig:
        """Create an obstacle course challenge - navigate hazards"""
        obstacles = {
            ChallengeDifficulty.EASY: "Few obstacles",
            ChallengeDifficulty.MEDIUM: "Moderate obstacles",
            ChallengeDifficulty.HARD: "Many obstacles",
            ChallengeDifficulty.EXTREME: "Extreme obstacles"
        }[difficulty]
        
        return ChallengeConfig(
            challenge_type=ChallengeType.OBSTACLE_COURSE,
            difficulty=difficulty,
            name=f"Obstacle Course - {obstacles}",
            description="Navigate through a challenging course with obstacles. Avoid crashes!",
            track_config={"type": "technical", "obstacles": True},
            race_config={"laps": 1, "telemetry": True},
            scoring_weights={
                "completion": 0.4,
                "incidents": 0.3,
                "time": 0.2,
                "precision": 0.1
            },
            success_criteria={
                "completion": 1.0,  # Must finish
                "incidents": 2  # Max 2 incidents
            },
            special_rules=["Random obstacle placement", "Adaptive difficulty"]
        )
    
    def _create_weather_challenge(self, difficulty: ChallengeDifficulty) -> ChallengeConfig:
        """Create a weather challenge - race in difficult conditions"""
        weather = {
            ChallengeDifficulty.EASY: "rain",
            ChallengeDifficulty.MEDIUM: "heavy_rain",
            ChallengeDifficulty.HARD: "storm",
            ChallengeDifficulty.EXTREME: "changing_conditions"
        }[difficulty]
        
        return ChallengeConfig(
            challenge_type=ChallengeType.WEATHER_CHALLENGE,
            difficulty=difficulty,
            name=f"Weather Master - {weather.replace('_', ' ').title()}",
            description="Master challenging weather conditions. Adapt your driving style!",
            track_config={"type": "mixed", "weather": weather},
            race_config={"laps": 5, "telemetry": True},
            scoring_weights={
                "position": 0.3,
                "consistency": 0.3,
                "incidents": 0.2,
                "adaptability": 0.2
            },
            success_criteria={
                "position": 3,
                "incidents": 3
            },
            special_rules=["Weather affects grip", "Visibility reduced", "Strategy matters"]
        )
    
    # Strategic Challenge Creators
    
    def _create_fuel_management(self, difficulty: ChallengeDifficulty) -> ChallengeConfig:
        """Create a fuel management challenge - efficiency is key"""
        fuel_limit = {
            ChallengeDifficulty.EASY: 0.9,
            ChallengeDifficulty.MEDIUM: 0.7,
            ChallengeDifficulty.HARD: 0.5,
            ChallengeDifficulty.EXTREME: 0.3
        }[difficulty]
        
        return ChallengeConfig(
            challenge_type=ChallengeType.FUEL_MANAGEMENT,
            difficulty=difficulty,
            name=f"Eco Challenge - {fuel_limit*100:.0f}% Fuel",
            description="Complete the race with limited fuel. Efficiency beats speed!",
            track_config={"type": "endurance"},
            race_config={"laps": 10, "telemetry": True, "fuel_limit": fuel_limit},
            scoring_weights={
                "completion": 0.4,
                "fuel_remaining": 0.3,
                "position": 0.2,
                "efficiency": 0.1
            },
            success_criteria={
                "completion": 1.0,
                "fuel_remaining": 5  # 5% minimum
            },
            special_rules=["Limited fuel", "No refueling", "Efficiency crucial"]
        )
    
    def _create_endurance_race(self, difficulty: ChallengeDifficulty) -> ChallengeConfig:
        """Create an endurance race - consistency over time"""
        laps = {
            ChallengeDifficulty.EASY: 20,
            ChallengeDifficulty.MEDIUM: 40,
            ChallengeDifficulty.HARD: 60,
            ChallengeDifficulty.EXTREME: 100
        }[difficulty]
        
        return ChallengeConfig(
            challenge_type=ChallengeType.ENDURANCE_RACE,
            difficulty=difficulty,
            name=f"Endurance Test - {laps} Laps",
            description="Long-distance racing. Manage resources and maintain consistency!",
            track_config={"type": "endurance"},
            race_config={"laps": laps, "telemetry": True},
            scoring_weights={
                "position": 0.3,
                "consistency": 0.3,
                "resource_management": 0.2,
                "endurance_rating": 0.2
            },
            success_criteria={
                "completion": 1.0,
                "consistency_variance": 5  # Max 5 second variance
            },
            special_rules=["Tire degradation", "Fuel management", "Mental endurance"]
        )
    
    def _create_pursuit_race(self, difficulty: ChallengeDifficulty) -> ChallengeConfig:
        """Create a pursuit race - catch the leader"""
        gap_seconds = {
            ChallengeDifficulty.EASY: 5,
            ChallengeDifficulty.MEDIUM: 10,
            ChallengeDifficulty.HARD: 20,
            ChallengeDifficulty.EXTREME: 30
        }[difficulty]
        
        return ChallengeConfig(
            challenge_type=ChallengeType.PURSUIT_RACE,
            difficulty=difficulty,
            name=f"Pursuit Mode - {gap_seconds}s Gap",
            description="Start behind and catch the leader. Hunt them down!",
            track_config={"type": "mixed"},
            race_config={"laps": 10, "telemetry": True, "staggered_start": gap_seconds},
            scoring_weights={
                "catch_time": 0.5,
                "final_gap": 0.3,
                "overtakes": 0.2
            },
            success_criteria={
                "catch_leader": 1,  # Must catch leader
                "laps_remaining": 2  # Within last 2 laps
            },
            special_rules=["Staggered start", "Hunter vs prey dynamics"]
        )
    
    # Mixed Challenge Creators
    
    def _create_formula_race(self, difficulty: ChallengeDifficulty) -> ChallengeConfig:
        """Create a formula race - balanced all-round challenge"""
        return ChallengeConfig(
            challenge_type=ChallengeType.FORMULA_RACE,
            difficulty=difficulty,
            name=f"Formula Challenge - Level {difficulty.value}",
            description="Complete Formula-style race. Balance of speed, skill, and strategy!",
            track_config={"type": "mixed"},
            race_config={"laps": 15, "telemetry": True},
            scoring_weights={
                "position": 0.4,
                "fastest_lap": 0.2,
                "consistency": 0.2,
                "strategy": 0.2
            },
            success_criteria={
                "position": 3,
                "incidents": 2
            },
            special_rules=["Full race rules", "Points system", "Strategic elements"]
        )
    
    def _create_elimination_race(self, difficulty: ChallengeDifficulty) -> ChallengeConfig:
        """Create an elimination race - last place eliminated each lap"""
        eliminations = {
            ChallengeDifficulty.EASY: "every 3 laps",
            ChallengeDifficulty.MEDIUM: "every 2 laps",
            ChallengeDifficulty.HARD: "every lap",
            ChallengeDifficulty.EXTREME: "every lap + time limit"
        }[difficulty]
        
        return ChallengeConfig(
            challenge_type=ChallengeType.ELIMINATION_RACE,
            difficulty=difficulty,
            name=f"Elimination - {eliminations}",
            description="Survive the elimination! Last place gets eliminated periodically.",
            track_config={"type": "speed"},
            race_config={"laps": 15, "telemetry": True, "elimination": True},
            scoring_weights={
                "survival_time": 0.5,
                "final_position": 0.3,
                "laps_led": 0.2
            },
            success_criteria={
                "survival": 0.6,  # Survive 60% of race
                "final_position": 3
            },
            special_rules=["Last place eliminated", "Increasing pressure", "No mistakes allowed"]
        )
    
    def _create_relay_race(self, difficulty: ChallengeDifficulty) -> ChallengeConfig:
        """Create a relay race - team-based competition"""
        stages = {
            ChallengeDifficulty.EASY: 2,
            ChallengeDifficulty.MEDIUM: 3,
            ChallengeDifficulty.HARD: 4,
            ChallengeDifficulty.EXTREME: 5
        }[difficulty]
        
        return ChallengeConfig(
            challenge_type=ChallengeType.RELAY_RACE,
            difficulty=difficulty,
            name=f"Relay Race - {stages} Stages",
            description="Team relay race. Each driver completes their stage!",
            track_config={"type": "mixed"},
            race_config={"laps": stages * 5, "telemetry": True, "relay": True},
            scoring_weights={
                "team_time": 0.5,
                "handoff_efficiency": 0.3,
                "consistency": 0.2
            },
            success_criteria={
                "team_position": 2,
                "handoff_time": 5  # seconds
            },
            special_rules=["Team format", "Driver swaps", "Combined performance"]
        )
    
    # Helper methods
    
    def _create_challenge_track(self, config: ChallengeConfig) -> RaceTrack:
        """Create appropriate track for the challenge"""
        track_type = config.track_config.get("type", "mixed")
        
        # Use existing track creators or create custom
        if track_type == "speed":
            track = RaceTrack.create_speed_track()
        elif track_type == "technical":
            track = RaceTrack.create_technical_track()
        elif track_type == "endurance":
            track = RaceTrack.create_endurance_track()
        elif track_type == "mixed":
            track = RaceTrack.create_mixed_track()
        elif track_type == "drag_strip":
            # Create custom drag strip
            segments = config.track_config.get("segments", [])
            track = RaceTrack(
                name="Drag Strip",
                track_type=TrackType.SPEED_TRACK,
                total_length=config.track_config.get("length", 1.0),
                segments=segments
            )
        else:
            track = RaceTrack.create_mixed_track()
        
        # Apply weather if specified
        if "weather" in config.track_config:
            track.weather_conditions = config.track_config["weather"]
            
        return track
    
    def _calculate_scores(self, config: ChallengeConfig, race_results: Dict, 
                         simulator: RaceSimulator) -> Dict[str, float]:
        """Calculate challenge-specific scores"""
        scores = {}
        
        for position, data in race_results["positions"].items():
            car_name = data["name"]
            score = 0.0
            
            # Position-based scoring
            if "position" in config.scoring_weights:
                position_score = (6 - position) / 5  # 1st = 1.0, 5th = 0.2
                score += position_score * config.scoring_weights["position"]
            
            # Time-based scoring
            if "finish_time" in config.scoring_weights:
                time_score = 1.0 / (1 + data["total_time"] / 100)
                score += time_score * config.scoring_weights["finish_time"]
            
            # Get telemetry for advanced scoring
            if simulator.telemetry:
                telemetry = simulator.get_telemetry_summary(car_name)
                
                if telemetry and "top_speed" in config.scoring_weights:
                    speed_score = telemetry["speed"]["top_speed"] / 400  # Normalize to 400 km/h
                    score += speed_score * config.scoring_weights["top_speed"]
                
                if telemetry and "consistency" in config.scoring_weights:
                    consistency_score = 1.0 / (1 + telemetry["technical"]["consistency"])
                    score += consistency_score * config.scoring_weights["consistency"]
            
            scores[car_name] = score * 100  # Scale to 0-100
            
        return scores
    
    def _determine_rankings(self, config: ChallengeConfig, scores: Dict[str, float], 
                           race_results: Dict) -> Dict[int, str]:
        """Determine final rankings based on challenge type"""
        # Sort by scores
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        rankings = {}
        for i, (car_name, score) in enumerate(sorted_scores):
            rankings[i + 1] = car_name
            
        return rankings
    
    def _check_success_criteria(self, config: ChallengeConfig, scores: Dict[str, float], 
                               race_results: Dict) -> bool:
        """Check if challenge success criteria are met"""
        if not config.success_criteria:
            return True
            
        # For now, simple check - can be expanded
        return len(scores) > 0 and max(scores.values()) > 70
    
    def _get_telemetry_summaries(self, simulator: RaceSimulator, cars: List[RacingCar]) -> Dict:
        """Get telemetry summaries for all cars"""
        summaries = {}
        for car in cars:
            summary = simulator.get_telemetry_summary(car.name)
            if summary:
                summaries[car.name] = summary
        return summaries
    
    def _generate_summary(self, config: ChallengeConfig, rankings: Dict[int, str], 
                         scores: Dict[str, float]) -> str:
        """Generate a text summary of the challenge results"""
        winner = rankings.get(1, "Unknown")
        winner_score = scores.get(winner, 0)
        
        summary = f"Challenge: {config.name}\n"
        summary += f"Difficulty: {config.difficulty.name}\n"
        summary += f"Winner: {winner} (Score: {winner_score:.1f})\n"
        summary += f"Challenge Type: {config.challenge_type.value.replace('_', ' ').title()}"
        
        return summary