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
    
    def calculate_corner_speed(self, corner_difficulty: float = 50) -> float:
        """Calculate safe cornering speed based on car handling and corner difficulty"""
        # Base cornering speed as percentage of top speed
        base_corner_ratio = 0.6 + (self.get_effective_handling() * 0.3)
        
        # Adjust for corner difficulty (0-100 scale)
        difficulty_factor = 1.0 - (corner_difficulty / 200)  # Max 50% reduction
        
        # Apply tire wear penalty
        tire_penalty = 1.0 - (self.tire_wear / 200)  # Max 50% reduction when worn
        
        # Calculate final corner speed
        corner_speed = self.get_effective_top_speed() * base_corner_ratio * difficulty_factor * tire_penalty
        
        return max(corner_speed, self.get_effective_top_speed() * 0.3)  # Minimum 30% of top speed
    
    def calculate_pit_stop_value(self, laps_remaining: int, current_position: int) -> dict:
        """Calculate strategic value of pitting now vs later"""
        # Time cost of pit stop
        pit_time_cost = 25.0  # seconds
        
        # Fuel gain if we pit
        fuel_gain = 100 - self.fuel_level
        
        # Tire performance gain
        tire_gain = self.tire_wear  # Reset to 0
        
        # Calculate laps we can do with current fuel
        fuel_per_lap = 100 / 15  # Rough estimate
        laps_possible = self.fuel_level / fuel_per_lap
        
        # Strategic assessment
        must_pit = laps_possible < laps_remaining
        tire_critical = self.tire_wear > 80
        
        return {
            "recommended": must_pit or tire_critical or (tire_gain > 40 and laps_remaining > 3),
            "urgency": "critical" if must_pit else ("high" if tire_critical else "medium"),
            "fuel_gain": fuel_gain,
            "tire_gain": tire_gain,
            "time_cost": pit_time_cost,
            "laps_possible": laps_possible
        }
    
    def analyze_overtaking_opportunity(self, gap_to_ahead: float, relative_speed: float, 
                                      track_section: str = "straight") -> dict:
        """Analyze probability and risk of overtaking maneuver"""
        # Base overtaking factors
        speed_advantage = max(0, relative_speed)  # Only positive relative speed helps
        
        # Track section multipliers
        section_factors = {
            "straight": {"opportunity": 1.0, "risk": 0.3},
            "corner": {"opportunity": 0.6, "risk": 0.8},
            "chicane": {"opportunity": 0.4, "risk": 1.2},
            "long_corner": {"opportunity": 0.7, "risk": 0.6}
        }
        
        section = section_factors.get(track_section, section_factors["straight"])
        
        # Calculate success probability
        if gap_to_ahead > 100:  # Large gap
            success_prob = 0.1
        elif gap_to_ahead > 50:  # Medium gap
            success_prob = 0.3 + (speed_advantage / 20) * section["opportunity"]
        elif gap_to_ahead > 20:  # Close gap
            success_prob = 0.6 + (speed_advantage / 15) * section["opportunity"]
        else:  # Very close
            success_prob = 0.8 + (speed_advantage / 10) * section["opportunity"]
        
        # Calculate risk level
        risk_level = section["risk"] * (1 + self.get_style_modifiers()["risk_factor"])
        
        return {
            "success_probability": min(0.95, success_prob),
            "risk_level": risk_level,
            "recommended": success_prob > 0.6 and risk_level < 1.0,
            "track_section": track_section,
            "speed_advantage": speed_advantage,
            "gap": gap_to_ahead
        }
    
    def predict_tire_degradation(self, laps_remaining: int, aggressive_factor: float = 1.0) -> dict:
        """Predict tire wear over remaining laps"""
        current_wear = self.tire_wear
        wear_per_lap = 5.0 * aggressive_factor * self.get_style_modifiers()["risk_factor"]
        
        predicted_wear = current_wear + (wear_per_lap * laps_remaining)
        
        # Degradation thresholds
        if predicted_wear > 90:
            degradation_level = "critical"
        elif predicted_wear > 70:
            degradation_level = "high"
        elif predicted_wear > 50:
            degradation_level = "medium"
        else:
            degradation_level = "low"
        
        return {
            "current_wear": current_wear,
            "predicted_final_wear": min(100, predicted_wear),
            "wear_per_lap": wear_per_lap,
            "degradation_level": degradation_level,
            "performance_loss": min(30, predicted_wear / 3),  # Max 30% performance loss
            "critical_lap": max(1, (90 - current_wear) / wear_per_lap) if wear_per_lap > 0 else laps_remaining + 1
        }
    
    def calculate_fuel_strategy(self, laps_remaining: int, current_position: int) -> dict:
        """Calculate optimal fuel management strategy"""
        # Fuel consumption rates by driving style
        style_mod = self.get_style_modifiers()
        base_consumption = 100 / 15  # Base: 15 laps per tank
        actual_consumption = base_consumption / style_mod["fuel_penalty"]
        
        # Calculate fuel scenarios
        fuel_needed = actual_consumption * laps_remaining
        fuel_deficit = max(0, fuel_needed - self.fuel_level)
        laps_possible = self.fuel_level / actual_consumption
        
        # Strategy recommendations
        if fuel_deficit > 0:
            strategy = "must_pit"
        elif laps_possible < laps_remaining + 2:  # Close to limit
            strategy = "conserve"
        elif self.fuel_level > 80:
            strategy = "attack"
        else:
            strategy = "manage"
        
        return {
            "current_fuel": self.fuel_level,
            "fuel_needed": fuel_needed,
            "fuel_deficit": fuel_deficit,
            "laps_possible": laps_possible,
            "consumption_rate": actual_consumption,
            "strategy": strategy,
            "can_finish": fuel_deficit == 0
        }
    
    def assess_weather_impact(self, weather: str, track_section: str = "mixed") -> dict:
        """Assess how weather affects car performance"""
        weather_effects = {
            "clear": {"speed": 1.0, "handling": 1.0, "tire_wear": 1.0, "risk": 1.0},
            "rain": {"speed": 0.85, "handling": 0.7, "tire_wear": 0.8, "risk": 1.5},
            "heavy_rain": {"speed": 0.7, "handling": 0.5, "tire_wear": 0.6, "risk": 2.0},
            "fog": {"speed": 0.9, "handling": 0.9, "tire_wear": 1.0, "risk": 1.3},
            "wind": {"speed": 0.95, "handling": 0.85, "tire_wear": 1.1, "risk": 1.1}
        }
        
        effects = weather_effects.get(weather, weather_effects["clear"])
        
        # Car-specific adaptation
        handling_advantage = self.get_effective_handling()
        adaptation_bonus = 1.0 + (handling_advantage - 0.5) * 0.2  # Better handling = better weather adaptation
        
        return {
            "weather": weather,
            "speed_factor": effects["speed"] * adaptation_bonus,
            "handling_factor": effects["handling"] * adaptation_bonus,
            "tire_wear_factor": effects["tire_wear"],
            "risk_factor": effects["risk"] / adaptation_bonus,
            "adaptation_level": "high" if adaptation_bonus > 1.1 else ("medium" if adaptation_bonus > 1.0 else "low")
        }
    
    def get_performance_envelope(self) -> dict:
        """Get comprehensive performance metrics for strategic analysis"""
        return {
            "speed_metrics": {
                "top_speed": self.get_effective_top_speed(),
                "acceleration": self.get_effective_acceleration(),
                "corner_speed_50": self.calculate_corner_speed(50),
                "corner_speed_90": self.calculate_corner_speed(90)
            },
            "efficiency_metrics": {
                "fuel_efficiency": self.fuel_efficiency,
                "current_fuel": self.fuel_level,
                "tire_condition": 100 - self.tire_wear
            },
            "strategic_metrics": {
                "handling": self.get_effective_handling(),
                "driver_style": self.driver_style.value,
                "risk_tolerance": self.get_style_modifiers()["risk_factor"],
                "current_position": self.current_position
            }
        }
    
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