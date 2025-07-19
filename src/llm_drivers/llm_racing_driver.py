"""
LLM Racing Driver - AI-powered driver using language models for decision making
"""

import asyncio
from dataclasses import dataclass
from typing import Dict, Optional, List
from enum import Enum

from ..core.racing_car import RacingCar, DriverStyle
from ..core.race_track import TrackSegment
from ai_config import RacingAI, LLAMA_MODELS


class LLMAction(Enum):
    """Actions that LLM drivers can take"""
    ATTACK = "ATTACK"
    DEFEND = "DEFEND"
    CONSERVE = "CONSERVE"
    PRESSURE = "PRESSURE"
    WAIT = "WAIT"
    USE_POWERUP = "USE_POWERUP"
    # New actions LLMs are naturally using
    OVERTAKE = "OVERTAKE"
    PASS = "PASS"
    BLOCK = "BLOCK"
    BOOST = "BOOST"
    HOLD = "HOLD"
    SAVE = "SAVE"
    # Weapon actions
    FIRE = "FIRE"
    SHOOT = "SHOOT"


@dataclass
class LLMDriver:
    """Wrapper for an LLM-powered racing driver"""
    car: RacingCar
    ai: RacingAI
    model_config: dict
    name: str
    
    # Performance tracking
    decisions_made: int = 0
    successful_overtakes: int = 0
    failed_overtakes: int = 0
    average_confidence: float = 0.0
    last_action: Optional[LLMAction] = None
    last_reasoning: str = ""
    
    def __post_init__(self):
        """Initialize the AI connection"""
        self.personality = self.model_config["personality"]
        
    async def make_decision(self, race_state: dict) -> dict:
        """Make a racing decision using the LLM with comprehensive telemetry"""
        
        # Calculate laps remaining
        current_lap = race_state.get("current_lap", 1)
        total_laps = race_state.get("total_laps", 10)
        laps_remaining = total_laps - current_lap + 1
        
        # Get gap information
        gap_ahead = race_state.get("gap_ahead", 100)
        gap_behind = race_state.get("gap_behind", 100)
        
        # Calculate relative speed (simplified estimation)
        relative_speed = 5.0 if gap_ahead < 50 else -5.0  # Simplified
        
        # Comprehensive race state with all telemetry including power-ups and collisions
        comprehensive_state = {
            "basic": {
                "position": self.car.current_position,
                "total_cars": race_state.get("total_cars", 5),
                "current_lap": current_lap,
                "total_laps": total_laps,
                "speed": self.car.current_speed,
                "gap_ahead": gap_ahead,
                "gap_behind": gap_behind,
                "track_segment": race_state.get("track_segment", "straight"),
                "weather": race_state.get("weather", "clear")
            },
            "pit_analysis": self.car.calculate_pit_stop_value(laps_remaining, self.car.current_position),
            "overtake_analysis": self.car.analyze_overtaking_opportunity(
                gap_ahead, relative_speed, race_state.get("track_segment", "straight")
            ),
            "tire_prediction": self.car.predict_tire_degradation(laps_remaining),
            "fuel_strategy": self.car.calculate_fuel_strategy(laps_remaining, self.car.current_position),
            "weather_impact": self.car.assess_weather_impact(
                race_state.get("weather", "clear"), 
                race_state.get("track_segment", "mixed")
            ),
            "performance_envelope": self.car.get_performance_envelope(),
            "power_ups": {
                "inventory": race_state.get("power_ups", []),
                "strategy": race_state.get("power_up_strategy", {}),
                "available_actions": ["use_item", "hold_item"] if race_state.get("power_ups") else ["wait_for_item"]
            },
            "collision_risk": race_state.get("collision_risk", {"risk_level": "none", "risk_factor": 0.0}),
            "weapons": {
                "ammo": race_state.get("ammo_remaining", 50),
                "can_fire": race_state.get("can_fire", False),
                "target_ahead": race_state.get("target_ahead", None),
                "target_distance": race_state.get("target_distance", 999)
            }
        }
        
        # Get AI decision with comprehensive data
        decision = await self.ai.make_racing_decision(comprehensive_state, self.personality)
        
        # Handle power-up usage if requested
        if decision.get("use_powerup", False) and race_state.get("power_ups"):
            decision["powerup_used"] = True
        else:
            decision["powerup_used"] = False
        
        # Track performance
        self.decisions_made += 1
        self.average_confidence = (
            (self.average_confidence * (self.decisions_made - 1) + decision.get("confidence", 0.5)) 
            / self.decisions_made
        )
        
        # Store last action - let LLMs use natural language!
        try:
            action_str = decision.get("action", "WAIT").upper()
            self.last_action = LLMAction(action_str)
        except ValueError:
            # If it's not a valid action, default to WAIT
            self.last_action = LLMAction.WAIT
            decision["action"] = "WAIT"
            
        self.last_reasoning = decision.get("reasoning", "")
        
        return decision
    
    async def react_to_event(self, event: dict) -> str:
        """Generate a reaction to a race event"""
        return await self.ai.generate_race_commentary(event, self.personality)
    
    def apply_action_to_car(self, action: LLMAction, base_speed: float) -> float:
        """Apply the LLM's decision to the car's performance"""
        speed_modifier = 1.0
        
        if action == LLMAction.ATTACK:
            speed_modifier = 1.15  # 15% speed boost for attacks
            self.car.fuel_level -= 0.2  # Extra fuel consumption
            self.car.tire_wear += 0.1   # Extra tire wear
            
        elif action == LLMAction.DEFEND:
            speed_modifier = 0.95  # Slightly slower when defending
            
        elif action == LLMAction.CONSERVE:
            speed_modifier = 0.85  # Much slower but saves resources
            self.car.fuel_level = min(100, self.car.fuel_level + 0.05)  # Save some fuel
            self.car.tire_wear = max(0, self.car.tire_wear - 0.02)   # Save tires
            
        elif action == LLMAction.PRESSURE:
            speed_modifier = 1.05  # Slightly faster to pressure
            self.car.fuel_level -= 0.05
            
        elif action == LLMAction.USE_POWERUP:
            speed_modifier = 1.02  # Slight speed boost for using items
            
        # New natural LLM actions
        elif action in [LLMAction.OVERTAKE, LLMAction.PASS]:
            speed_modifier = 1.20  # Aggressive overtaking move
            self.car.fuel_level -= 0.25
            self.car.tire_wear += 0.15
            
        elif action == LLMAction.BLOCK:
            speed_modifier = 0.90  # Defensive blocking
            
        elif action == LLMAction.BOOST:
            speed_modifier = 1.25  # High speed boost
            self.car.fuel_level -= 0.30
            
        elif action in [LLMAction.HOLD, LLMAction.SAVE]:
            speed_modifier = 0.80  # Very conservative
            self.car.fuel_level = min(100, self.car.fuel_level + 0.10)
            
        elif action in [LLMAction.FIRE, LLMAction.SHOOT]:
            speed_modifier = 0.95  # Slight slowdown when firing
            # Firing is handled in the main simulation loop
            
        else:  # WAIT and fallback
            speed_modifier = 0.98  # Neutral pace
            
        # Ensure values stay in bounds
        self.car.fuel_level = max(0, min(100, self.car.fuel_level))
        self.car.tire_wear = max(0, min(100, self.car.tire_wear))
        
        return base_speed * speed_modifier
    
    def get_status_info(self) -> dict:
        """Get current status information for display"""
        return {
            "name": self.name,
            "model": self.model_config["model"].split("/")[-1],  # Short model name
            "position": self.car.current_position,
            "last_action": self.last_action.value if self.last_action else "NONE",
            "last_reasoning": self.last_reasoning,
            "confidence": self.average_confidence,
            "decisions": self.decisions_made,
            "fuel": self.car.fuel_level,
            "tires": 100 - self.car.tire_wear
        }


def create_llm_drivers() -> List[LLMDriver]:
    """Create the 5 LLM-powered racing drivers"""
    drivers = []
    
    # Speed demon - uses fast small model
    speed_car = RacingCar(
        name="Llama Speed",
        top_speed=385,
        acceleration=3.0,
        handling=0.65,
        fuel_efficiency=9,
        driver_style=DriverStyle.AGGRESSIVE
    )
    speed_ai = RacingAI(LLAMA_MODELS["speed"]["model"])
    drivers.append(LLMDriver(
        car=speed_car,
        ai=speed_ai,
        model_config=LLAMA_MODELS["speed"],
        name="Llama-3.2 Speed"
    ))
    
    # Strategic - uses large model
    strategic_car = RacingCar(
        name="Llama Strategic",
        top_speed=355,
        acceleration=2.7,
        handling=0.88,
        fuel_efficiency=16,
        driver_style=DriverStyle.BALANCED
    )
    strategic_ai = RacingAI(LLAMA_MODELS["strategic"]["model"])
    drivers.append(LLMDriver(
        car=strategic_car,
        ai=strategic_ai,
        model_config=LLAMA_MODELS["strategic"],
        name="Llama-70B Strategic"
    ))
    
    # Balanced - medium model
    balanced_car = RacingCar(
        name="Llama Balanced",
        top_speed=365,
        acceleration=2.85,
        handling=0.78,
        fuel_efficiency=13,
        driver_style=DriverStyle.BALANCED
    )
    balanced_ai = RacingAI(LLAMA_MODELS["balanced"]["model"])
    drivers.append(LLMDriver(
        car=balanced_car,
        ai=balanced_ai,
        model_config=LLAMA_MODELS["balanced"],
        name="Llama-8B Balanced"
    ))
    
    # Chaotic - Hermes model
    chaotic_car = RacingCar(
        name="Hermes Chaos",
        top_speed=375,
        acceleration=2.95,
        handling=0.68,
        fuel_efficiency=11,
        driver_style=DriverStyle.CHAOTIC
    )
    chaotic_ai = RacingAI(LLAMA_MODELS["chaotic"]["model"])
    drivers.append(LLMDriver(
        car=chaotic_car,
        ai=chaotic_ai,
        model_config=LLAMA_MODELS["chaotic"],
        name="Hermes Chaos"
    ))
    
    # Technical - Qwen model  
    technical_car = RacingCar(
        name="Qwen Technical",
        top_speed=360,
        acceleration=2.75,
        handling=0.92,
        fuel_efficiency=14,
        driver_style=DriverStyle.TECHNICAL
    )
    technical_ai = RacingAI(LLAMA_MODELS["technical"]["model"])
    drivers.append(LLMDriver(
        car=technical_car,
        ai=technical_ai,
        model_config=LLAMA_MODELS["technical"],
        name="Qwen Technical"
    ))
    
    return drivers