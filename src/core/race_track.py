from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple
import math


class TrackType(Enum):
    SPEED_TRACK = "speed_track"
    TECHNICAL_TRACK = "technical_track"
    MIXED_TRACK = "mixed_track"
    ENDURANCE_TRACK = "endurance_track"


@dataclass
class TrackSegment:
    """Represents a segment of the track (straight, corner, etc.)"""
    length: float  # meters
    is_straight: bool
    corner_angle: float = 0.0  # degrees (0 for straights)
    corner_radius: float = 0.0  # meters (0 for straights)
    elevation_change: float = 0.0  # meters
    
    def get_optimal_speed(self, car_handling: float) -> float:
        """Calculate optimal speed through this segment"""
        if self.is_straight:
            return 400.0  # Max speed on straights
        else:
            # Cornering speed based on physics: v = sqrt(μ * g * r)
            # μ (friction coefficient) is approximated by car handling
            g = 9.81  # gravity
            base_speed = math.sqrt(car_handling * g * self.corner_radius) * 3.6  # m/s to km/h
            
            # Adjust for corner angle (sharper corners = slower)
            angle_factor = 1 - (abs(self.corner_angle) / 180) * 0.3
            
            return min(base_speed * angle_factor, 300)  # Cap at 300 km/h


@dataclass
class RaceTrack:
    name: str
    track_type: TrackType
    total_length: float  # kilometers
    segments: List[TrackSegment]
    pit_lane_time_penalty: float = 20.0  # seconds
    weather_conditions: str = "clear"
    
    def __post_init__(self):
        # Calculate actual total length from segments
        actual_length = sum(segment.length for segment in self.segments) / 1000
        if abs(actual_length - self.total_length) > 0.1:
            self.total_length = actual_length
    
    def get_track_characteristics(self):
        """Get track characteristics based on type"""
        characteristics = {
            TrackType.SPEED_TRACK: {
                "speed_importance": 0.7,
                "acceleration_importance": 0.2,
                "handling_importance": 0.1,
                "fuel_importance": 0.0,
                "description": "Long straights favor high top speed"
            },
            TrackType.TECHNICAL_TRACK: {
                "speed_importance": 0.1,
                "acceleration_importance": 0.3,
                "handling_importance": 0.5,
                "fuel_importance": 0.1,
                "description": "Tight corners and technical sections"
            },
            TrackType.MIXED_TRACK: {
                "speed_importance": 0.3,
                "acceleration_importance": 0.3,
                "handling_importance": 0.3,
                "fuel_importance": 0.1,
                "description": "Balanced mix of straights and corners"
            },
            TrackType.ENDURANCE_TRACK: {
                "speed_importance": 0.2,
                "acceleration_importance": 0.2,
                "handling_importance": 0.2,
                "fuel_importance": 0.4,
                "description": "Long races requiring fuel management"
            }
        }
        return characteristics[self.track_type]
    
    @classmethod
    def create_speed_track(cls, name: str = "Monza Speed Circuit"):
        """Create a speed-focused track with long straights"""
        segments = [
            TrackSegment(1200, True),  # Main straight
            TrackSegment(150, False, corner_angle=45, corner_radius=80),
            TrackSegment(800, True),
            TrackSegment(200, False, corner_angle=90, corner_radius=60),
            TrackSegment(600, True),
            TrackSegment(100, False, corner_angle=30, corner_radius=100),
            TrackSegment(1000, True),
            TrackSegment(250, False, corner_angle=120, corner_radius=40),
            TrackSegment(400, True),
            TrackSegment(150, False, corner_angle=60, corner_radius=70),
        ]
        return cls(name, TrackType.SPEED_TRACK, 5.65, segments)
    
    @classmethod
    def create_technical_track(cls, name: str = "Monaco Technical Circuit"):
        """Create a technical track with many tight corners"""
        segments = [
            TrackSegment(300, True),  # Short main straight
            TrackSegment(80, False, corner_angle=90, corner_radius=25),
            TrackSegment(150, True),
            TrackSegment(120, False, corner_angle=180, corner_radius=20),  # Hairpin
            TrackSegment(200, True),
            TrackSegment(100, False, corner_angle=75, corner_radius=35),
            TrackSegment(180, True),
            TrackSegment(150, False, corner_angle=135, corner_radius=30),
            TrackSegment(250, True),
            TrackSegment(90, False, corner_angle=60, corner_radius=40),
            TrackSegment(160, True),
            TrackSegment(110, False, corner_angle=90, corner_radius=30),
            TrackSegment(140, True),
            TrackSegment(130, False, corner_angle=120, corner_radius=25),
        ]
        return cls(name, TrackType.TECHNICAL_TRACK, 2.08, segments)
    
    @classmethod
    def create_mixed_track(cls, name: str = "Silverstone Mixed Circuit"):
        """Create a balanced track with varied challenges"""
        segments = [
            TrackSegment(800, True),  # Good straight
            TrackSegment(180, False, corner_angle=90, corner_radius=50),
            TrackSegment(400, True),
            TrackSegment(200, False, corner_angle=135, corner_radius=35),
            TrackSegment(600, True),
            TrackSegment(150, False, corner_angle=60, corner_radius=60),
            TrackSegment(350, True),
            TrackSegment(250, False, corner_angle=180, corner_radius=25),  # Hairpin
            TrackSegment(500, True),
            TrackSegment(170, False, corner_angle=75, corner_radius=55),
            TrackSegment(700, True),
            TrackSegment(140, False, corner_angle=45, corner_radius=70),
        ]
        return cls(name, TrackType.MIXED_TRACK, 4.49, segments)
    
    @classmethod
    def create_endurance_track(cls, name: str = "Le Mans Endurance Circuit"):
        """Create a long endurance track"""
        segments = [
            TrackSegment(2000, True),  # Very long straight
            TrackSegment(200, False, corner_angle=70, corner_radius=60),
            TrackSegment(1500, True),
            TrackSegment(300, False, corner_angle=90, corner_radius=40),
            TrackSegment(800, True),
            TrackSegment(180, False, corner_angle=120, corner_radius=35),
            TrackSegment(1200, True),
            TrackSegment(250, False, corner_angle=45, corner_radius=80),
            TrackSegment(900, True),
            TrackSegment(220, False, corner_angle=135, corner_radius=30),
            TrackSegment(600, True),
            TrackSegment(150, False, corner_angle=60, corner_radius=65),
            TrackSegment(1800, True),
            TrackSegment(280, False, corner_angle=90, corner_radius=45),
        ]
        return cls(name, TrackType.ENDURANCE_TRACK, 10.48, segments)
    
    def calculate_segment_time(self, segment: TrackSegment, current_speed: float, 
                             target_speed: float, car_acceleration: float) -> Tuple[float, float]:
        """Calculate time to complete a segment and exit speed"""
        # Simple physics model for segment traversal
        avg_speed = (current_speed + target_speed) / 2
        
        # Time to reach target speed (or as close as possible within segment)
        accel_time = abs(target_speed - current_speed) / (100 / car_acceleration)
        accel_distance = avg_speed * accel_time / 3.6  # Convert to m/s
        
        if accel_distance >= segment.length:
            # Can't reach target speed in this segment
            final_speed = current_speed + (segment.length / accel_distance) * (target_speed - current_speed)
            time = segment.length / (avg_speed / 3.6)
        else:
            # Reach target speed then maintain
            final_speed = target_speed
            remaining_distance = segment.length - accel_distance
            maintain_time = remaining_distance / (target_speed / 3.6)
            time = accel_time + maintain_time
        
        return time, final_speed
    
    def get_weather_modifiers(self):
        """Get performance modifiers based on weather"""
        modifiers = {
            "clear": {"speed": 1.0, "handling": 1.0},
            "rain": {"speed": 0.85, "handling": 0.7},
            "fog": {"speed": 0.9, "handling": 0.85},
            "hot": {"speed": 0.95, "handling": 0.95},
        }
        return modifiers.get(self.weather_conditions, modifiers["clear"])