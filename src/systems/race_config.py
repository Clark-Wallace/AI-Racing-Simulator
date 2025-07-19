from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import os
from datetime import datetime
from ..core.racing_car import DriverStyle
from ..core.race_track import TrackType
from .challenge_generator import ChallengeType, ChallengeDifficulty


class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    AMATEUR = "amateur" 
    PROFESSIONAL = "professional"
    EXPERT = "expert"
    LEGENDARY = "legendary"


class RaceMode(Enum):
    QUICK_RACE = "quick_race"
    CHAMPIONSHIP = "championship"
    CHALLENGE = "challenge"
    TIME_TRIAL = "time_trial"
    CUSTOM = "custom"


@dataclass
class AISettings:
    """AI difficulty and behavior settings"""
    difficulty: DifficultyLevel = DifficultyLevel.PROFESSIONAL
    aggression_multiplier: float = 1.0  # 0.5-1.5
    mistake_probability: float = 0.05  # 0-0.2
    learning_rate: float = 1.0  # How fast AI learns from data
    rubber_band_strength: float = 0.0  # 0-1, catch-up mechanic
    personality_intensity: float = 1.0  # How much personality affects decisions
    
    def apply_difficulty(self):
        """Apply difficulty presets"""
        presets = {
            DifficultyLevel.BEGINNER: {
                "aggression_multiplier": 0.7,
                "mistake_probability": 0.15,
                "learning_rate": 0.5,
                "rubber_band_strength": 0.3
            },
            DifficultyLevel.AMATEUR: {
                "aggression_multiplier": 0.85,
                "mistake_probability": 0.1,
                "learning_rate": 0.75,
                "rubber_band_strength": 0.15
            },
            DifficultyLevel.PROFESSIONAL: {
                "aggression_multiplier": 1.0,
                "mistake_probability": 0.05,
                "learning_rate": 1.0,
                "rubber_band_strength": 0.0
            },
            DifficultyLevel.EXPERT: {
                "aggression_multiplier": 1.15,
                "mistake_probability": 0.02,
                "learning_rate": 1.25,
                "rubber_band_strength": 0.0
            },
            DifficultyLevel.LEGENDARY: {
                "aggression_multiplier": 1.3,
                "mistake_probability": 0.01,
                "learning_rate": 1.5,
                "rubber_band_strength": 0.0
            }
        }
        
        if self.difficulty in presets:
            for key, value in presets[self.difficulty].items():
                setattr(self, key, value)


@dataclass
class RaceSettings:
    """Settings for a single race"""
    track_name: str = "Silverstone Mixed Circuit"
    track_type: TrackType = TrackType.MIXED_TRACK
    laps: int = 10
    weather: str = "clear"
    time_of_day: str = "afternoon"
    
    # Feature toggles
    enable_telemetry: bool = True
    enable_intelligence: bool = True
    enable_personalities: bool = True
    enable_damage: bool = True
    enable_fuel_consumption: bool = True
    enable_tire_wear: bool = True
    
    # Race rules
    mandatory_pit_stops: int = 0
    safety_car_probability: float = 0.1
    yellow_flag_sensitivity: float = 0.5
    
    # Grid settings
    qualifying_enabled: bool = True
    reverse_grid: bool = False
    custom_grid: List[str] = field(default_factory=list)


@dataclass
class ChampionshipSettings:
    """Settings for a championship season"""
    name: str = "AI Racing Championship"
    races: List[RaceSettings] = field(default_factory=list)
    points_system: List[int] = field(default_factory=lambda: [25, 18, 15, 12, 10, 8, 6, 4, 2, 1])
    drop_worst_races: int = 0
    
    # Special rules
    sprint_races: List[int] = field(default_factory=list)  # Indices of sprint races
    double_points_finale: bool = True
    fastest_lap_point: bool = True
    pole_position_point: bool = False
    
    # Team championship
    enable_teams: bool = False
    team_assignments: Dict[str, str] = field(default_factory=dict)


@dataclass
class SimulatorConfig:
    """Complete simulator configuration"""
    mode: RaceMode = RaceMode.QUICK_RACE
    ai_settings: AISettings = field(default_factory=AISettings)
    race_settings: RaceSettings = field(default_factory=RaceSettings)
    championship_settings: Optional[ChampionshipSettings] = None
    
    # Car selection
    enabled_cars: List[str] = field(default_factory=lambda: [
        "Speed Demon", "Tech Precision", "Fuel Master", 
        "Adaptive Racer", "Chaos Cruiser"
    ])
    player_car: Optional[str] = None  # For future player mode
    
    # Display settings
    show_telemetry: bool = True
    show_commentary: bool = True
    update_frequency: float = 10.0  # Seconds between updates
    
    # Performance settings
    simulation_speed: float = 1.0  # 1.0 = real-time, 10.0 = 10x speed
    physics_accuracy: str = "high"  # low, medium, high
    
    # Metadata
    config_name: str = "default"
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    last_modified: str = field(default_factory=lambda: datetime.now().isoformat())


class ConfigurationManager:
    """Manages configuration presets and saving/loading"""
    
    def __init__(self, config_dir: str = "configs"):
        self.config_dir = config_dir
        self.current_config: Optional[SimulatorConfig] = None
        self.presets = self._load_presets()
        
        # Create config directory if it doesn't exist
        os.makedirs(config_dir, exist_ok=True)
        
    def _load_presets(self) -> Dict[str, SimulatorConfig]:
        """Load built-in configuration presets"""
        presets = {}
        
        # Quick Race Preset
        quick_race = SimulatorConfig(
            mode=RaceMode.QUICK_RACE,
            config_name="Quick Race",
            race_settings=RaceSettings(
                laps=5,
                qualifying_enabled=False
            )
        )
        presets["quick_race"] = quick_race
        
        # Endurance Preset
        endurance = SimulatorConfig(
            mode=RaceMode.QUICK_RACE,
            config_name="Endurance Challenge",
            race_settings=RaceSettings(
                track_type=TrackType.ENDURANCE_TRACK,
                laps=50,
                mandatory_pit_stops=2,
                enable_fuel_consumption=True,
                enable_tire_wear=True
            ),
            ai_settings=AISettings(
                difficulty=DifficultyLevel.PROFESSIONAL,
                mistake_probability=0.08  # More mistakes in long races
            )
        )
        presets["endurance"] = endurance
        
        # Sprint Series Preset
        sprint = SimulatorConfig(
            mode=RaceMode.CHAMPIONSHIP,
            config_name="Sprint Series",
            championship_settings=ChampionshipSettings(
                name="Sprint Cup",
                races=[
                    RaceSettings(track_type=TrackType.SPEED_TRACK, laps=10),
                    RaceSettings(track_type=TrackType.TECHNICAL_TRACK, laps=8),
                    RaceSettings(track_type=TrackType.MIXED_TRACK, laps=12),
                    RaceSettings(track_type=TrackType.SPEED_TRACK, laps=10),
                    RaceSettings(track_type=TrackType.MIXED_TRACK, laps=15),
                ],
                sprint_races=[1, 3],  # Races 2 and 4 are sprints
                points_system=[12, 10, 8, 6, 4]  # Reduced points for sprints
            )
        )
        presets["sprint_series"] = sprint
        
        # Beginner Friendly
        beginner = SimulatorConfig(
            mode=RaceMode.QUICK_RACE,
            config_name="Beginner Friendly",
            ai_settings=AISettings(difficulty=DifficultyLevel.BEGINNER),
            race_settings=RaceSettings(
                laps=3,
                enable_damage=False,
                enable_fuel_consumption=False,
                qualifying_enabled=False
            )
        )
        beginner.ai_settings.apply_difficulty()
        presets["beginner"] = beginner
        
        # Chaos Mode
        chaos = SimulatorConfig(
            mode=RaceMode.QUICK_RACE,
            config_name="Chaos Mode",
            ai_settings=AISettings(
                aggression_multiplier=1.5,
                mistake_probability=0.15,
                personality_intensity=2.0
            ),
            race_settings=RaceSettings(
                weather="rain",
                safety_car_probability=0.3,
                reverse_grid=True
            ),
            enabled_cars=["Chaos Cruiser"] * 5  # All Chaos Cruisers!
        )
        presets["chaos"] = chaos
        
        return presets
    
    def create_custom_config(self, name: str) -> SimulatorConfig:
        """Create a new custom configuration"""
        config = SimulatorConfig(
            mode=RaceMode.CUSTOM,
            config_name=name
        )
        self.current_config = config
        return config
    
    def save_config(self, config: SimulatorConfig, filename: Optional[str] = None):
        """Save configuration to file"""
        if filename is None:
            filename = f"{config.config_name.lower().replace(' ', '_')}.json"
            
        filepath = os.path.join(self.config_dir, filename)
        
        # Update last modified
        config.last_modified = datetime.now().isoformat()
        
        # Convert to dict and save
        config_dict = asdict(config)
        
        # Convert enums to strings
        config_dict["mode"] = config.mode.value
        config_dict["ai_settings"]["difficulty"] = config.ai_settings.difficulty.value
        config_dict["race_settings"]["track_type"] = config.race_settings.track_type.value
        
        with open(filepath, 'w') as f:
            json.dump(config_dict, f, indent=2)
            
        print(f"✅ Configuration saved to {filepath}")
        
    def load_config(self, filename: str) -> SimulatorConfig:
        """Load configuration from file"""
        filepath = os.path.join(self.config_dir, filename)
        
        with open(filepath, 'r') as f:
            config_dict = json.load(f)
            
        # Convert back to enums
        config_dict["mode"] = RaceMode(config_dict["mode"])
        config_dict["ai_settings"]["difficulty"] = DifficultyLevel(config_dict["ai_settings"]["difficulty"])
        config_dict["race_settings"]["track_type"] = TrackType(config_dict["race_settings"]["track_type"])
        
        # Reconstruct nested dataclasses
        ai_settings = AISettings(**config_dict["ai_settings"])
        race_settings = RaceSettings(**config_dict["race_settings"])
        
        championship_settings = None
        if config_dict.get("championship_settings"):
            cs_dict = config_dict["championship_settings"]
            # Reconstruct race settings list
            races = []
            for race_dict in cs_dict.get("races", []):
                race_dict["track_type"] = TrackType(race_dict["track_type"])
                races.append(RaceSettings(**race_dict))
            cs_dict["races"] = races
            championship_settings = ChampionshipSettings(**cs_dict)
            
        config = SimulatorConfig(
            mode=config_dict["mode"],
            ai_settings=ai_settings,
            race_settings=race_settings,
            championship_settings=championship_settings,
            enabled_cars=config_dict["enabled_cars"],
            player_car=config_dict.get("player_car"),
            show_telemetry=config_dict["show_telemetry"],
            show_commentary=config_dict["show_commentary"],
            update_frequency=config_dict["update_frequency"],
            simulation_speed=config_dict["simulation_speed"],
            physics_accuracy=config_dict["physics_accuracy"],
            config_name=config_dict["config_name"],
            created_date=config_dict["created_date"],
            last_modified=config_dict["last_modified"]
        )
        
        self.current_config = config
        return config
    
    def list_configs(self) -> List[str]:
        """List available configuration files"""
        configs = []
        
        # List presets
        print("\n📋 Built-in Presets:")
        for name, config in self.presets.items():
            print(f"  - {name}: {config.config_name}")
            configs.append(f"preset:{name}")
            
        # List saved configs
        print("\n💾 Saved Configurations:")
        if os.path.exists(self.config_dir):
            for filename in os.listdir(self.config_dir):
                if filename.endswith('.json'):
                    print(f"  - {filename}")
                    configs.append(f"file:{filename}")
                    
        return configs
    
    def get_preset(self, preset_name: str) -> Optional[SimulatorConfig]:
        """Get a preset configuration"""
        return self.presets.get(preset_name)
    
    def quick_setup_wizard(self) -> SimulatorConfig:
        """Interactive setup wizard for quick configuration"""
        print("\n🏎️  QUICK SETUP WIZARD")
        print("="*40)
        
        # Mode selection
        print("\nSelect Race Mode:")
        modes = list(RaceMode)
        for i, mode in enumerate(modes):
            print(f"{i+1}. {mode.value.replace('_', ' ').title()}")
        
        mode_idx = 2  # Default to Challenge
        selected_mode = modes[mode_idx]
        
        # Difficulty selection
        print("\nSelect Difficulty:")
        difficulties = list(DifficultyLevel)
        for i, diff in enumerate(difficulties):
            print(f"{i+1}. {diff.value.title()}")
            
        diff_idx = 2  # Default to Professional
        selected_difficulty = difficulties[diff_idx]
        
        # Create config
        config = SimulatorConfig(
            mode=selected_mode,
            config_name=f"Quick Setup - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        config.ai_settings.difficulty = selected_difficulty
        config.ai_settings.apply_difficulty()
        
        # Quick options
        config.race_settings.laps = 10
        config.race_settings.weather = "clear"
        
        self.current_config = config
        return config
    
    def apply_config(self, config: SimulatorConfig) -> Dict[str, Any]:
        """Apply configuration and return setup parameters"""
        setup_params = {
            "mode": config.mode,
            "ai_settings": config.ai_settings,
            "race_settings": config.race_settings,
            "cars": config.enabled_cars,
            "features": {
                "telemetry": config.race_settings.enable_telemetry,
                "intelligence": config.race_settings.enable_intelligence,
                "personalities": config.race_settings.enable_personalities,
                "damage": config.race_settings.enable_damage,
                "fuel": config.race_settings.enable_fuel_consumption,
                "tires": config.race_settings.enable_tire_wear
            }
        }
        
        if config.championship_settings:
            setup_params["championship"] = config.championship_settings
            
        return setup_params