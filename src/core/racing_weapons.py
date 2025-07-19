"""
Racing Weapons System - Machine guns and other weapon mechanics
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import math


@dataclass
class MachineGun:
    """Machine gun weapon for racing cars"""
    ammo: int = 50
    fire_rate: float = 0.2  # Seconds between shots
    last_fire_time: float = 0.0
    damage: float = 0.15  # Speed reduction factor per hit
    range: float = 0.03  # Range in track progress units (3% of track = ~300m on 10km track)
    
    def can_fire(self, current_time: float) -> bool:
        """Check if gun can fire based on ammo and cooldown"""
        return (self.ammo > 0 and 
                current_time - self.last_fire_time >= self.fire_rate)
    
    def fire(self, current_time: float) -> bool:
        """Fire the gun if possible"""
        if self.can_fire(current_time):
            self.ammo -= 1
            self.last_fire_time = current_time
            return True
        return False
    
    def get_ammo_percentage(self) -> float:
        """Get remaining ammo as percentage"""
        return (self.ammo / 50) * 100


class WeaponsManager:
    """Manages all weapon systems in the race"""
    
    def __init__(self):
        self.car_weapons: Dict[str, MachineGun] = {}
        self.active_hits: List[Dict] = []  # Track recent hits for visual effects
        self.hit_effects_duration = 0.5  # How long hit effects last
        
    def initialize_cars(self, car_names: List[str]):
        """Initialize weapons for all cars"""
        for car_name in car_names:
            self.car_weapons[car_name] = MachineGun()
    
    def attempt_fire(self, shooter_name: str, current_time: float) -> bool:
        """Attempt to fire machine gun"""
        if shooter_name not in self.car_weapons:
            return False
        
        weapon = self.car_weapons[shooter_name]
        return weapon.fire(current_time)
    
    def check_hit(self, shooter_name: str, shooter_progress: float,
                  target_name: str, target_progress: float,
                  is_target_ahead: bool) -> Optional[Dict]:
        """Check if a shot hits the target"""
        if not is_target_ahead:
            return None
        
        # Calculate distance considering track wrap-around
        distance = target_progress - shooter_progress
        if distance < 0:
            distance += 1.0  # Handle wrap-around
        
        weapon = self.car_weapons.get(shooter_name)
        if not weapon:
            return None
        
        # Check if target is in range
        if distance <= weapon.range:
            hit_info = {
                "shooter": shooter_name,
                "target": target_name,
                "damage": weapon.damage,
                "time": 0.0,  # Will be set by caller
                "shooter_pos": shooter_progress,
                "target_pos": target_progress
            }
            self.active_hits.append(hit_info)
            return hit_info
        
        return None
    
    def get_car_ahead(self, car_name: str, car_positions: Dict[str, float],
                      car_laps: Dict[str, int]) -> Optional[Tuple[str, float]]:
        """Find the car directly ahead of the given car"""
        if car_name not in car_positions:
            return None
        
        my_progress = car_positions[car_name]
        my_lap = car_laps.get(car_name, 0)
        
        closest_ahead = None
        min_distance = float('inf')
        
        for other_name, other_progress in car_positions.items():
            if other_name == car_name:
                continue
            
            other_lap = car_laps.get(other_name, 0)
            
            # Check if other car is ahead
            if other_lap > my_lap:
                # Other car is at least one lap ahead
                distance = (other_lap - my_lap) + (other_progress - my_progress)
            elif other_lap == my_lap:
                # Same lap
                if other_progress > my_progress:
                    # Simple case: other car is ahead on same lap
                    distance = other_progress - my_progress
                else:
                    # Other car is behind on same lap
                    continue
            else:
                # Other car is behind in laps
                continue
            
            if distance < min_distance:
                min_distance = distance
                closest_ahead = (other_name, distance)
        
        # Only return if car is reasonably close (within 10% of track)
        if closest_ahead and closest_ahead[1] < 0.1:
            return closest_ahead
        
        return None
    
    def apply_hit_effect(self, target_speeds: Dict[str, float], hit_info: Dict) -> Dict[str, float]:
        """Apply speed reduction from machine gun hit"""
        target = hit_info["target"]
        if target in target_speeds:
            # Reduce speed by damage percentage
            new_speed = target_speeds[target] * (1.0 - hit_info["damage"])
            target_speeds[target] = max(new_speed, 10.0)  # Minimum speed of 10 km/h
        
        return target_speeds
    
    def update_effects(self, delta_time: float):
        """Update visual effects and remove expired ones"""
        # Update hit effect timers
        for hit in self.active_hits[:]:  # Copy to allow modification
            hit["time"] += delta_time
            if hit["time"] >= self.hit_effects_duration:
                self.active_hits.remove(hit)
    
    def get_ammo_status(self, car_name: str) -> int:
        """Get remaining ammo for a car"""
        if car_name in self.car_weapons:
            return self.car_weapons[car_name].ammo
        return 0
    
    def get_all_ammo_status(self) -> Dict[str, int]:
        """Get ammo status for all cars"""
        return {name: weapon.ammo for name, weapon in self.car_weapons.items()}
    
    def get_active_hits(self) -> List[Dict]:
        """Get list of active hit effects for rendering"""
        return self.active_hits.copy()