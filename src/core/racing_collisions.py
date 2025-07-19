"""
Racing Collision Detection System
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import random
import math


@dataclass
class CollisionEvent:
    """Represents a collision between cars"""
    primary_car: str
    secondary_car: str
    severity: float  # 0.1 (minor) to 1.0 (major)
    primary_penalty: float  # Time penalty in seconds
    secondary_penalty: float
    collision_type: str  # "side_swipe", "rear_end", "corner_clash"
    track_section: str


class CollisionDetector:
    """Manages collision detection and penalties"""
    
    def __init__(self):
        self.collision_history = []
        self.recent_collisions = {}  # Track recent collisions to prevent spam
        
    def check_for_collisions(self, car_positions: Dict[str, float], 
                           car_speeds: Dict[str, float],
                           track_section: str = "straight") -> List[CollisionEvent]:
        """Check for potential collisions between cars"""
        collisions = []
        car_names = list(car_positions.keys())
        
        for i in range(len(car_names)):
            for j in range(i + 1, len(car_names)):
                car1, car2 = car_names[i], car_names[j]
                
                collision = self._detect_collision(
                    car1, car2, 
                    car_positions[car1], car_positions[car2],
                    car_speeds[car1], car_speeds[car2],
                    track_section
                )
                
                if collision:
                    collisions.append(collision)
                    
        return collisions
    
    def _detect_collision(self, car1: str, car2: str, 
                         pos1: float, pos2: float,
                         speed1: float, speed2: float,
                         track_section: str) -> Optional[CollisionEvent]:
        """Detect collision between two specific cars"""
        
        # Calculate position difference (in track progress units)
        pos_diff = abs(pos1 - pos2)
        
        # Cars need to be very close for collision
        collision_threshold = 0.002  # About 2 car lengths
        
        if pos_diff > collision_threshold:
            return None
            
        # Check if this collision was already processed recently
        collision_key = tuple(sorted([car1, car2]))
        if collision_key in self.recent_collisions:
            if self.recent_collisions[collision_key] > 0:
                self.recent_collisions[collision_key] -= 1
                return None
        
        # Calculate collision probability based on various factors
        speed_diff = abs(speed1 - speed2)
        
        # Base collision probability
        base_prob = 0.1
        
        # Increase probability based on speed difference
        speed_factor = min(speed_diff / 50, 0.3)  # Max 30% increase
        
        # Track section affects collision probability
        section_multipliers = {
            "straight": 0.5,
            "corner": 1.5,
            "chicane": 2.0,
            "long_corner": 1.2
        }
        section_mult = section_multipliers.get(track_section, 1.0)
        
        collision_prob = (base_prob + speed_factor) * section_mult
        
        # Random collision check
        if random.random() > collision_prob:
            return None
            
        # Collision occurred! Calculate details
        severity = random.uniform(0.2, 0.8)
        
        # Determine collision type based on context
        if track_section in ["corner", "chicane"]:
            collision_type = "corner_clash"
        elif speed_diff > 20:
            collision_type = "rear_end"
        else:
            collision_type = "side_swipe"
            
        # Calculate penalties based on severity and type
        base_penalty = severity * 2.0  # 0.4 to 1.6 seconds
        
        # Determine who was "at fault" (usually the faster car)
        if speed1 > speed2:
            primary_car, secondary_car = car1, car2
        else:
            primary_car, secondary_car = car2, car1
            
        # Primary car (at fault) gets higher penalty
        primary_penalty = base_penalty * 1.5
        secondary_penalty = base_penalty * 0.7
        
        # Prevent collision spam
        self.recent_collisions[collision_key] = 5  # 5 frames cooldown
        
        collision = CollisionEvent(
            primary_car=primary_car,
            secondary_car=secondary_car,
            severity=severity,
            primary_penalty=primary_penalty,
            secondary_penalty=secondary_penalty,
            collision_type=collision_type,
            track_section=track_section
        )
        
        self.collision_history.append(collision)
        return collision
    
    def apply_collision_effects(self, collision: CollisionEvent, 
                              car_speeds: Dict[str, float]) -> Dict[str, float]:
        """Apply speed penalties from collision"""
        # Reduce speeds temporarily
        if collision.primary_car in car_speeds:
            car_speeds[collision.primary_car] *= (1.0 - collision.severity * 0.3)
            
        if collision.secondary_car in car_speeds:
            car_speeds[collision.secondary_car] *= (1.0 - collision.severity * 0.2)
            
        return car_speeds
    
    def get_collision_risk(self, car_name: str, car_positions: Dict[str, float],
                          car_speeds: Dict[str, float], track_section: str) -> Dict:
        """Analyze collision risk for a specific car"""
        if car_name not in car_positions:
            return {"risk_level": "none", "risk_factor": 0.0}
            
        my_pos = car_positions[car_name]
        my_speed = car_speeds[car_name]
        
        # Find nearby cars
        nearby_cars = []
        for other_car, other_pos in car_positions.items():
            if other_car == car_name:
                continue
                
            distance = abs(my_pos - other_pos)
            if distance < 0.01:  # Within collision range
                nearby_cars.append({
                    "name": other_car,
                    "distance": distance,
                    "speed": car_speeds[other_car],
                    "speed_diff": abs(my_speed - car_speeds[other_car])
                })
        
        if not nearby_cars:
            return {"risk_level": "none", "risk_factor": 0.0}
            
        # Calculate overall risk
        total_risk = 0.0
        for car in nearby_cars:
            # Risk increases with speed difference and proximity
            distance_risk = (0.01 - car["distance"]) / 0.01  # 0-1 scale
            speed_risk = min(car["speed_diff"] / 50, 1.0)  # 0-1 scale
            car_risk = (distance_risk + speed_risk) / 2
            total_risk += car_risk
            
        risk_factor = min(total_risk, 1.0)
        
        if risk_factor > 0.7:
            risk_level = "high"
        elif risk_factor > 0.4:
            risk_level = "medium"
        elif risk_factor > 0.1:
            risk_level = "low"
        else:
            risk_level = "none"
            
        return {
            "risk_level": risk_level,
            "risk_factor": risk_factor,
            "nearby_cars": len(nearby_cars),
            "track_section": track_section
        }
    
    def update_cooldowns(self):
        """Update collision cooldowns"""
        for key in list(self.recent_collisions.keys()):
            self.recent_collisions[key] -= 1
            if self.recent_collisions[key] <= 0:
                del self.recent_collisions[key]
    
    def get_collision_stats(self, car_name: str) -> Dict:
        """Get collision statistics for a car"""
        collisions_involving = [c for c in self.collision_history 
                              if c.primary_car == car_name or c.secondary_car == car_name]
        
        at_fault = len([c for c in collisions_involving if c.primary_car == car_name])
        victim = len([c for c in collisions_involving if c.secondary_car == car_name])
        
        return {
            "total_collisions": len(collisions_involving),
            "at_fault": at_fault,
            "victim": victim,
            "collision_rate": len(collisions_involving) / max(1, len(self.collision_history))
        }