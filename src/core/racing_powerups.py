"""
Racing Power-ups System - Mario Kart style items for strategic racing
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
import random


class PowerUpType(Enum):
    """Available power-up types"""
    # Offensive
    LIGHTNING_BOLT = "lightning_bolt"      # Slows all cars ahead
    RED_SHELL = "red_shell"               # Targets car directly ahead
    BLUE_SHELL = "blue_shell"             # Targets race leader
    BANANA = "banana"                     # Defensive/offensive trap
    
    # Defensive/Utility
    SHIELD = "shield"                     # Blocks one attack
    TURBO_BOOST = "turbo_boost"          # Speed boost
    NITRO = "nitro"                      # Extended speed boost
    GHOST = "ghost"                      # Temporary invincibility
    
    # Strategic
    RADAR = "radar"                      # See competitor strategies
    FUEL_BOOST = "fuel_boost"            # Restore fuel
    TIRE_REPAIR = "tire_repair"          # Fix tire wear


@dataclass
class PowerUp:
    """Individual power-up item"""
    type: PowerUpType
    name: str
    description: str
    duration: float = 0.0  # How long it lasts (0 = instant)
    power: float = 1.0     # Effect strength
    defensive: bool = False # Can be used defensively
    
    def get_strategy_value(self, position: int, total_cars: int) -> float:
        """Calculate strategic value based on current position"""
        position_factor = position / total_cars
        
        if self.type == PowerUpType.BLUE_SHELL:
            # More valuable when not in first
            return 1.0 - (1.0 / position) if position > 1 else 0.1
        elif self.type == PowerUpType.LIGHTNING_BOLT:
            # More valuable when behind
            return position_factor
        elif self.type == PowerUpType.SHIELD:
            # More valuable when ahead
            return 1.0 - position_factor
        elif self.type == PowerUpType.TURBO_BOOST:
            # Always useful
            return 0.7
        else:
            return 0.5


class PowerUpManager:
    """Manages power-up distribution and effects"""
    
    # Power-up definitions
    POWER_UPS = {
        PowerUpType.LIGHTNING_BOLT: PowerUp(
            PowerUpType.LIGHTNING_BOLT, "Lightning Bolt", 
            "Slows all cars ahead for 3 seconds", 3.0, 0.7
        ),
        PowerUpType.RED_SHELL: PowerUp(
            PowerUpType.RED_SHELL, "Red Shell", 
            "Targets car directly ahead, 2s penalty", 0.0, 2.0
        ),
        PowerUpType.BLUE_SHELL: PowerUp(
            PowerUpType.BLUE_SHELL, "Blue Shell", 
            "Targets race leader, 3s penalty", 0.0, 3.0
        ),
        PowerUpType.BANANA: PowerUp(
            PowerUpType.BANANA, "Banana Peel", 
            "Defensive trap, 1.5s penalty if hit", 0.0, 1.5, True
        ),
        PowerUpType.SHIELD: PowerUp(
            PowerUpType.SHIELD, "Shield", 
            "Blocks next attack", 10.0, 1.0, True
        ),
        PowerUpType.TURBO_BOOST: PowerUp(
            PowerUpType.TURBO_BOOST, "Turbo Boost", 
            "+30% speed for 4 seconds", 4.0, 1.3
        ),
        PowerUpType.NITRO: PowerUp(
            PowerUpType.NITRO, "Nitro", 
            "+50% speed for 2 seconds", 2.0, 1.5
        ),
        PowerUpType.GHOST: PowerUp(
            PowerUpType.GHOST, "Ghost", 
            "Invincible for 3 seconds", 3.0, 1.0, True
        ),
        PowerUpType.RADAR: PowerUp(
            PowerUpType.RADAR, "Radar", 
            "See opponent strategies", 0.0, 1.0
        ),
        PowerUpType.FUEL_BOOST: PowerUp(
            PowerUpType.FUEL_BOOST, "Fuel Boost", 
            "Restore 25% fuel", 0.0, 25.0
        ),
        PowerUpType.TIRE_REPAIR: PowerUp(
            PowerUpType.TIRE_REPAIR, "Tire Repair", 
            "Reduce tire wear by 30%", 0.0, 30.0
        )
    }
    
    def __init__(self):
        self.active_effects = {}  # car_name -> list of active effects
        self.car_inventories = {}  # car_name -> list of power_ups
        self.track_items = []     # Available items on track
        self.track_pickups = []   # Power-up boxes on track [{position, available, respawn_timer}]
        self.pickup_respawn_time = 5.0  # Seconds before pickup respawns
        
    def get_power_up_for_position(self, position: int, total_cars: int) -> Optional[PowerUpType]:
        """Get appropriate power-up based on race position"""
        position_factor = position / total_cars
        
        # Probability distributions based on position
        if position == 1:  # Leader gets mostly defensive
            weights = {
                PowerUpType.SHIELD: 30,
                PowerUpType.BANANA: 25,
                PowerUpType.FUEL_BOOST: 20,
                PowerUpType.TIRE_REPAIR: 15,
                PowerUpType.TURBO_BOOST: 10
            }
        elif position <= 2:  # Near front
            weights = {
                PowerUpType.SHIELD: 20,
                PowerUpType.TURBO_BOOST: 20,
                PowerUpType.RED_SHELL: 15,
                PowerUpType.BANANA: 15,
                PowerUpType.FUEL_BOOST: 15,
                PowerUpType.NITRO: 15
            }
        elif position >= total_cars - 1:  # Near back
            weights = {
                PowerUpType.LIGHTNING_BOLT: 25,
                PowerUpType.BLUE_SHELL: 20,
                PowerUpType.NITRO: 20,
                PowerUpType.TURBO_BOOST: 15,
                PowerUpType.RED_SHELL: 10,
                PowerUpType.RADAR: 10
            }
        else:  # Middle positions
            weights = {
                PowerUpType.RED_SHELL: 20,
                PowerUpType.TURBO_BOOST: 20,
                PowerUpType.LIGHTNING_BOLT: 15,
                PowerUpType.SHIELD: 15,
                PowerUpType.NITRO: 15,
                PowerUpType.BANANA: 15
            }
        
        # Random selection based on weights
        power_ups = list(weights.keys())
        weight_values = list(weights.values())
        
        return random.choices(power_ups, weights=weight_values)[0]
    
    def give_power_up(self, car_name: str, position: int, total_cars: int):
        """Give a car a power-up based on their position"""
        try:
            if not car_name:
                return None
                
            if car_name not in self.car_inventories:
                self.car_inventories[car_name] = []
                
            # Limit inventory size
            if len(self.car_inventories[car_name]) >= 2:
                return None
                
            power_up_type = self.get_power_up_for_position(position, total_cars)
            if not power_up_type or power_up_type not in self.POWER_UPS:
                return None
                
            power_up = self.POWER_UPS[power_up_type]
            
            if not power_up:
                return None
                
            self.car_inventories[car_name].append(power_up)
            return power_up
        except Exception as e:
            print(f"⚠️ Give power-up error for {car_name}: {e}")
            return None
    
    def use_power_up(self, car_name: str, power_up_index: int = 0, target: str = None) -> Dict:
        """Use a power-up from car's inventory"""
        try:
            if not car_name or car_name not in self.car_inventories:
                return {"success": False, "message": "No inventory"}
                
            inventory = self.car_inventories[car_name]
            if not inventory or power_up_index >= len(inventory):
                return {"success": False, "message": "No power-up at index"}
                
            power_up = inventory.pop(power_up_index)
            
            if not power_up or not hasattr(power_up, 'name'):
                return {"success": False, "message": "Invalid power-up"}
            
            # Apply power-up effect
            effect = self._apply_power_up_effect(car_name, power_up, target)
            
            return {
                "success": True,
                "power_up": power_up.name,
                "effect": effect
            }
        except Exception as e:
            return {"success": False, "message": f"Power-up error: {str(e)[:20]}"}
    
    def _apply_power_up_effect(self, user: str, power_up: PowerUp, target: str = None) -> Dict:
        """Apply the power-up effect"""
        effect = {
            "type": power_up.type.value,
            "user": user,
            "target": target,
            "duration": power_up.duration,
            "power": power_up.power
        }
        
        # Add to active effects if it has duration
        if power_up.duration > 0:
            if user not in self.active_effects:
                self.active_effects[user] = []
            self.active_effects[user].append(effect)
            
        return effect
    
    def update_effects(self, time_delta: float):
        """Update active power-up effects"""
        for car_name in list(self.active_effects.keys()):
            effects = self.active_effects[car_name]
            
            # Reduce duration of all effects
            for effect in effects[:]:  # Copy list to modify during iteration
                effect["duration"] -= time_delta
                if effect["duration"] <= 0:
                    effects.remove(effect)
            
            # Remove empty effect lists
            if not effects:
                del self.active_effects[car_name]
    
    def get_speed_modifier(self, car_name: str) -> float:
        """Get current speed modifier from active effects"""
        modifier = 1.0
        
        if car_name in self.active_effects:
            for effect in self.active_effects[car_name]:
                if effect["type"] in ["turbo_boost", "nitro"]:
                    modifier *= effect["power"]
                elif effect["type"] == "lightning_bolt":
                    modifier *= 0.7  # Slowed by lightning
                    
        return modifier
    
    def is_protected(self, car_name: str) -> bool:
        """Check if car is protected from attacks"""
        if car_name in self.active_effects:
            for effect in self.active_effects[car_name]:
                if effect["type"] in ["shield", "ghost"]:
                    return True
        return False
    
    def get_inventory_status(self, car_name: str) -> List[str]:
        """Get car's current power-up inventory"""
        if car_name not in self.car_inventories:
            return []
        try:
            return [pu.name for pu in self.car_inventories[car_name] if pu and hasattr(pu, 'name')]
        except (AttributeError, TypeError):
            return []
    
    def analyze_power_up_strategy(self, car_name: str, position: int, total_cars: int, 
                                 gaps: Dict[str, float]) -> Dict:
        """Analyze optimal power-up usage strategy"""
        try:
            if not car_name or car_name not in self.car_inventories or not self.car_inventories[car_name]:
                return {"recommendation": "none", "reasoning": "No power-ups available"}
                
            inventory = self.car_inventories[car_name]
            best_item = None
            best_value = 0
            
            for i, power_up in enumerate(inventory):
                if not power_up or not hasattr(power_up, 'get_strategy_value') or not hasattr(power_up, 'type'):
                    continue
                    
                try:
                    strategic_value = power_up.get_strategy_value(position, total_cars)
                    
                    # Adjust value based on race situation
                    if hasattr(power_up, 'type') and gaps:
                        if power_up.type == PowerUpType.RED_SHELL and gaps.get("ahead", 999) < 50:
                            strategic_value += 0.3  # Close enough to use
                        elif power_up.type == PowerUpType.LIGHTNING_BOLT and position > 2:
                            strategic_value += 0.4  # Good for catching up
                        elif power_up.type == PowerUpType.SHIELD and gaps.get("behind", 999) < 30:
                            strategic_value += 0.3  # Under pressure
                            
                    if strategic_value > best_value:
                        best_value = strategic_value
                        best_item = (i, power_up)
                except (AttributeError, TypeError):
                    continue
            
            if best_item and best_value > 0.6:
                try:
                    item_name = best_item[1].name if hasattr(best_item[1], 'name') else "Unknown"
                    return {
                        "recommendation": "use",
                        "item_index": best_item[0],
                        "item_name": item_name,
                        "reasoning": f"High strategic value: {best_value:.1f}",
                        "value": best_value
                    }
                except (AttributeError, TypeError):
                    return {"recommendation": "hold", "reasoning": "Item error", "value": 0}
            else:
                return {
                    "recommendation": "hold",
                    "reasoning": "Wait for better opportunity",
                    "value": best_value if best_item else 0
                }
        except Exception as e:
            return {"recommendation": "none", "reasoning": f"Strategy error: {str(e)[:20]}"}
    
    def initialize_track_pickups(self, track_length: float, num_pickups: int = 8):
        """Place power-up boxes evenly around the track"""
        self.track_pickups = []
        spacing = 1.0 / num_pickups  # Progress spacing between pickups
        
        for i in range(num_pickups):
            progress = (i * spacing + spacing / 2) % 1.0  # Center in each segment
            self.track_pickups.append({
                "progress": progress,  # Position on track (0.0 to 1.0)
                "available": True,
                "respawn_timer": 0.0,
                "id": i
            })
    
    def check_pickup_collection(self, car_name: str, car_progress: float, 
                              collection_radius: float = 0.01) -> Optional[PowerUpType]:
        """Check if car collected a power-up box"""
        for pickup in self.track_pickups:
            if not pickup["available"]:
                continue
                
            # Check if car is close enough to pickup
            distance = abs(car_progress - pickup["progress"])
            # Handle wrap-around at start/finish line
            if distance > 0.5:
                distance = 1.0 - distance
                
            if distance < collection_radius:
                # Collect the pickup
                pickup["available"] = False
                pickup["respawn_timer"] = self.pickup_respawn_time
                
                # Get power-up based on car position
                car_position = self.get_car_position(car_name)
                total_cars = len(self.car_inventories)
                power_up_type = self.get_power_up_for_position(car_position, total_cars)
                
                if power_up_type:
                    self.give_power_up(car_name, car_position, total_cars)
                    return power_up_type
        
        return None
    
    def update_pickups(self, delta_time: float):
        """Update pickup respawn timers"""
        for pickup in self.track_pickups:
            if not pickup["available"] and pickup["respawn_timer"] > 0:
                pickup["respawn_timer"] -= delta_time
                if pickup["respawn_timer"] <= 0:
                    pickup["available"] = True
                    pickup["respawn_timer"] = 0.0
    
    def get_car_position(self, car_name: str) -> int:
        """Get approximate car position (1-based)"""
        # This is a simple approximation - in real implementation, 
        # this should come from the race simulator
        return list(self.car_inventories.keys()).index(car_name) + 1 if car_name in self.car_inventories else 3
    
    def initialize_cars(self, car_names: List[str]):
        """Initialize inventories for all cars"""
        for car_name in car_names:
            if car_name not in self.car_inventories:
                self.car_inventories[car_name] = []