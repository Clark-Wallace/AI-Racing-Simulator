from enum import Enum
from dataclasses import dataclass
from typing import Optional
import math


class DriverStyle(Enum):
    AGGRESSIVE = "aggressive"
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    TECHNICAL = "technical"
    CHAOTIC = "chaotic"


@dataclass
class RacingCar:
    name: str
    top_speed: float  # km/h
    acceleration: float  # 0-100 km/h in seconds
    handling: float  # 0-1 scale (1 being perfect)
    fuel_efficiency: float  # km per liter
    driver_style: DriverStyle
    
    # Dynamic race attributes
    current_speed: float = 0.0
    current_position: int = 0
    current_lap: int = 0
    lap_time: float = 0.0
    total_race_time: float = 0.0
    fuel_level: float = 100.0  # percentage
    tire_wear: float = 0.0  # 0-100 scale
    distance_traveled: float = 0.0
    
    def __post_init__(self):
        # Validate inputs
        if not 150 <= self.top_speed <= 400:
            raise ValueError("Top speed must be between 150 and 400 km/h")
        if not 2 <= self.acceleration <= 10:
            raise ValueError("Acceleration must be between 2 and 10 seconds")
        if not 0 <= self.handling <= 1:
            raise ValueError("Handling must be between 0 and 1")
        if not 5 <= self.fuel_efficiency <= 20:
            raise ValueError("Fuel efficiency must be between 5 and 20 km/l")
    
    def get_style_modifiers(self):
        """Get performance modifiers based on driver style"""
        modifiers = {
            DriverStyle.AGGRESSIVE: {
                "speed_bonus": 1.05,
                "acceleration_bonus": 1.08,
                "handling_penalty": 0.92,
                "fuel_penalty": 0.85,
                "risk_factor": 1.3
            },
            DriverStyle.CONSERVATIVE: {
                "speed_bonus": 0.95,
                "acceleration_bonus": 0.92,
                "handling_penalty": 1.05,
                "fuel_penalty": 1.1,
                "risk_factor": 0.7
            },
            DriverStyle.BALANCED: {
                "speed_bonus": 1.0,
                "acceleration_bonus": 1.0,
                "handling_penalty": 1.0,
                "fuel_penalty": 1.0,
                "risk_factor": 1.0
            },
            DriverStyle.TECHNICAL: {
                "speed_bonus": 0.98,
                "acceleration_bonus": 0.95,
                "handling_penalty": 1.12,
                "fuel_penalty": 1.05,
                "risk_factor": 0.8
            },
            DriverStyle.CHAOTIC: {
                "speed_bonus": 1.02,
                "acceleration_bonus": 1.05,
                "handling_penalty": 0.88,
                "fuel_penalty": 0.9,
                "risk_factor": 1.5
            }
        }
        return modifiers[self.driver_style]
    
    def get_effective_top_speed(self):
        """Calculate effective top speed considering style and tire wear"""
        style_mod = self.get_style_modifiers()
        tire_penalty = 1 - (self.tire_wear / 200)  # Max 50% penalty at full wear
        return self.top_speed * style_mod["speed_bonus"] * tire_penalty
    
    def get_effective_acceleration(self):
        """Calculate effective acceleration considering style and fuel level"""
        style_mod = self.get_style_modifiers()
        # Lighter car (less fuel) accelerates faster
        fuel_bonus = 1 + ((100 - self.fuel_level) / 500)  # Max 20% bonus when empty
        return self.acceleration / (style_mod["acceleration_bonus"] * fuel_bonus)
    
    def get_effective_handling(self):
        """Calculate effective handling considering style and tire wear"""
        style_mod = self.get_style_modifiers()
        tire_penalty = 1 - (self.tire_wear / 150)  # Max 66% penalty at full wear
        return self.handling * style_mod["handling_penalty"] * tire_penalty
    
    def accelerate(self, target_speed: float, time_delta: float) -> float:
        """Accelerate towards target speed based on acceleration stat"""
        effective_accel = self.get_effective_acceleration()
        max_accel_per_second = 100 / effective_accel  # km/h per second
        
        speed_diff = target_speed - self.current_speed
        max_change = max_accel_per_second * time_delta
        
        if speed_diff > 0:
            # Accelerating
            speed_change = min(speed_diff, max_change)
        else:
            # Braking (assumed to be more effective than acceleration)
            speed_change = max(speed_diff, -max_change * 1.5)
        
        self.current_speed = max(0, self.current_speed + speed_change)
        return self.current_speed
    
    def consume_fuel(self, distance: float, aggressive_factor: float = 1.0):
        """Consume fuel based on distance and driving style"""
        style_mod = self.get_style_modifiers()
        consumption = distance / (self.fuel_efficiency * style_mod["fuel_penalty"])
        consumption *= aggressive_factor
        
        # Convert to percentage (assuming 60L tank)
        fuel_used = (consumption / 60) * 100
        self.fuel_level = max(0, self.fuel_level - fuel_used)
    
    def wear_tires(self, distance: float, cornering_stress: float = 1.0):
        """Increase tire wear based on distance and cornering stress"""
        style_mod = self.get_style_modifiers()
        base_wear = distance / 1000  # 0.1% per km
        wear = base_wear * cornering_stress * style_mod["risk_factor"]
        self.tire_wear = min(100, self.tire_wear + wear)
    
    def reset_for_race(self):
        """Reset dynamic attributes for a new race"""
        self.current_speed = 0.0
        self.current_position = 0
        self.current_lap = 0
        self.lap_time = 0.0
        self.total_race_time = 0.0
        self.fuel_level = 100.0
        self.tire_wear = 0.0
        self.distance_traveled = 0.0