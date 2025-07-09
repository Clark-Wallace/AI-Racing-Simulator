from typing import List, Dict, Optional
from racing_car import RacingCar, DriverStyle
from ai_personalities import AIPersonalitySystem, PersonalityProfile, EmotionalState
from race_intelligence import RacingIntelligence, TacticalDecision, RaceSituation
import random


class EnhancedAIRacer:
    """AI Racer with full personality integration"""
    
    def __init__(self, car: RacingCar, personality_system: AIPersonalitySystem):
        self.car = car
        self.personality_system = personality_system
        self.profile = personality_system.profiles[car.name]
        self.intelligence = None  # Set during race
        self.race_quotes = []
        self.internal_monologue = []
        
    def get_current_thought(self, situation: RaceSituation) -> str:
        """Get what the racer is thinking"""
        thoughts = {
            EmotionalState.ANGRY: [
                "I'll show them who's boss!",
                "Nobody makes a fool of me!",
                "Time for some payback!"
            ],
            EmotionalState.FOCUSED: [
                "Stay on the racing line...",
                "Patience, wait for the opportunity...",
                "Precision is key here..."
            ],
            EmotionalState.CONFIDENT: [
                "I've got this in the bag!",
                "They can't touch me today!",
                "Everything's going perfectly!"
            ],
            EmotionalState.NERVOUS: [
                "Don't mess this up...",
                "Too much pressure...",
                "Just need to survive this..."
            ],
            EmotionalState.DETERMINED: [
                "I won't give up!",
                "This is my moment!",
                "Push through the pain!"
            ],
            EmotionalState.RECKLESS: [
                "All or nothing!",
                "Who needs brakes?",
                "YOLO!"
            ]
        }
        
        base_thoughts = thoughts.get(self.profile.emotional_state, ["..."])
        
        # Add situation-specific thoughts
        if situation.gap_ahead < 0.5:
            base_thoughts.append("I can take them here!")
        if situation.fuel_status < 10:
            base_thoughts.append("Running on fumes...")
        if situation.phase.value == "final":
            base_thoughts.append("Final push!")
            
        return random.choice(base_thoughts)
    
    def make_personality_adjusted_decision(self, base_decision: TacticalDecision,
                                         situation: RaceSituation) -> TacticalDecision:
        """Adjust tactical decision based on personality"""
        # Get emotional modifiers
        modifiers = self.personality_system.apply_emotional_modifiers(self.profile)
        
        # High risk-taking might override conservative decisions
        if modifiers["risk_taking"] > 1.3 and base_decision in [TacticalDecision.WAIT, TacticalDecision.CONSERVE]:
            if random.random() < 0.4:  # 40% chance to be more aggressive
                return TacticalDecision.ATTACK
                
        # Low confidence might make aggressive moves more conservative
        if self.profile.confidence_level < 0.3 and base_decision == TacticalDecision.ATTACK:
            if random.random() < 0.5:
                return TacticalDecision.PRESSURE
                
        # Signature move opportunity
        signature = self.personality_system.get_signature_move_decision(
            self.profile,
            {
                "gap_ahead": situation.gap_ahead,
                "is_corner": situation.is_cornering,
                "laps_remaining": situation.laps_remaining,
                "fuel_critical": situation.fuel_status < 5
            }
        )
        
        if signature:
            self.internal_monologue.append(f"Time for {signature}!")
            return TacticalDecision.ATTACK  # Signature moves are always aggressive
            
        return base_decision
    
    def react_to_event(self, event: str, context: Dict) -> Optional[str]:
        """React to race events with personality"""
        emotional_state, reaction = self.personality_system.get_emotional_response(
            self.profile, event, context
        )
        
        # Update momentum
        self.personality_system.update_momentum(self.profile, event)
        
        # Generate additional personality-specific reactions
        if not reaction and event == "near_miss":
            if self.profile.name == "Speed Demon":
                reaction = "That was close! I love it!"
            elif self.profile.name == "Tech Precision":
                reaction = "Unacceptable. Recalculating approach."
            elif self.profile.name == "Chaos Cruiser":
                reaction = "Wheee! Let's do that again!"
                
        if reaction:
            self.race_quotes.append({"time": context.get("time", 0), "quote": reaction})
            
        return reaction
    
    def get_performance_multipliers(self) -> Dict[str, float]:
        """Get performance multipliers based on personality state"""
        base_multipliers = self.personality_system.apply_emotional_modifiers(self.profile)
        
        # Add personality-specific bonuses
        if self.profile.name == "Speed Demon" and self.profile.emotional_state == EmotionalState.ANGRY:
            base_multipliers["speed"] *= 1.05  # Extra speed when angry
            
        elif self.profile.name == "Tech Precision" and self.profile.emotional_state == EmotionalState.FOCUSED:
            base_multipliers["handling"] *= 1.05  # Extra precision when focused
            
        elif self.profile.name == "Fuel Master" and self.profile.momentum > 0.5:
            base_multipliers["efficiency"] = 1.1  # Better fuel efficiency with momentum
            
        elif self.profile.name == "Chaos Cruiser" and self.profile.emotional_state == EmotionalState.RECKLESS:
            base_multipliers["speed"] *= 1.08  # Chaos bonus
            base_multipliers["handling"] *= 0.9  # But less control
            
        return base_multipliers
    
    def update_fatigue(self, laps_completed: int, total_laps: int):
        """Update fatigue based on race progress"""
        base_fatigue = laps_completed / total_laps
        
        # Personality affects fatigue accumulation
        if "VETERAN" in [t.name for t in self.profile.primary_traits]:
            base_fatigue *= 0.8  # Veterans handle fatigue better
        elif "HOTHEAD" in [t.name for t in self.profile.primary_traits]:
            base_fatigue *= 1.2  # Hotheads burn out faster
            
        # Emotional state affects fatigue
        if self.profile.emotional_state in [EmotionalState.ANGRY, EmotionalState.RECKLESS]:
            base_fatigue *= 1.15
        elif self.profile.emotional_state == EmotionalState.CALM:
            base_fatigue *= 0.9
            
        self.profile.fatigue_level = min(1.0, base_fatigue)
    
    def handle_rivalry_encounter(self, rival_name: str, situation: str) -> Optional[str]:
        """Special handling for encounters with rivals"""
        if rival_name not in self.profile.relationships:
            return None
            
        relationship = self.profile.relationships[rival_name]
        
        if relationship.relationship_type.value == "nemesis":
            if situation == "overtaking_opportunity":
                self.profile.emotional_state = EmotionalState.DETERMINED
                return "This one's personal!"
            elif situation == "being_overtaken":
                self.profile.emotional_state = EmotionalState.ANGRY
                return "Not by YOU!"
                
        elif relationship.relationship_type.value == "respected":
            if situation == "side_by_side":
                return "May the best racer win, old friend."
                
        return None
    
    def generate_radio_message(self, situation: str, context: Dict) -> Optional[str]:
        """Generate radio communication based on personality"""
        messages = {
            "leading_race": {
                "Speed Demon": "Eat my dust, slowpokes!",
                "Tech Precision": "Maintaining optimal pace. Everything under control.",
                "Fuel Master": "Right on fuel target. Smooth sailing.",
                "Adaptive Racer": "Adapting strategy. They won't catch me.",
                "Chaos Cruiser": "I have no idea how I got here, but I love it!"
            },
            "under_pressure": {
                "Speed Demon": "They want some? Come get some!",
                "Tech Precision": "Executing defensive protocol.",
                "Fuel Master": "Let them waste their fuel attacking.",
                "Adaptive Racer": "Interesting. Let's see what they've got.",
                "Chaos Cruiser": "Pressure makes diamonds! Or explosions!"
            },
            "mechanical_issue": {
                "Speed Demon": "The car can't handle my speed!",
                "Tech Precision": "Anomaly detected. Adjusting parameters.",
                "Fuel Master": "Every setback is a setup for a comeback.",
                "Adaptive Racer": "Time to improvise.",
                "Chaos Cruiser": "The car's joining in on the chaos!"
            }
        }
        
        if situation in messages and self.profile.name in messages[situation]:
            return messages[situation][self.profile.name]
            
        return None
    
    def celebrate_victory(self) -> str:
        """Generate victory celebration based on personality"""
        celebrations = {
            "Speed Demon": "YEAAAH! SPEED WINS AGAIN! *burns out tires*",
            "Tech Precision": "Calculated to perfection. *adjusts glasses* Elementary.",
            "Fuel Master": "Efficiency triumphs! And we still have fuel left!",
            "Adaptive Racer": "Adapted, evolved, conquered. Just as planned.",
            "Chaos Cruiser": "I WON?! I MEAN... OF COURSE I WON! CHAOS REIGNS!"
        }
        
        # Add emotional flavor
        if self.profile.emotional_state == EmotionalState.CONFIDENT:
            return celebrations[self.profile.name] + " Never doubted it!"
        elif self.profile.emotional_state == EmotionalState.EXHAUSTED:
            return celebrations[self.profile.name] + " *collapses* Worth it..."
            
        return celebrations.get(self.profile.name, "Yes! What a race!")


def create_enhanced_ai_racers(personality_system: AIPersonalitySystem) -> List[EnhancedAIRacer]:
    """Create the enhanced AI racers with full personalities"""
    cars = [
        RacingCar("Speed Demon", 380, 3.2, 0.65, 10, DriverStyle.AGGRESSIVE),
        RacingCar("Tech Precision", 340, 4.5, 0.92, 14, DriverStyle.TECHNICAL),
        RacingCar("Fuel Master", 320, 5.2, 0.78, 18, DriverStyle.CONSERVATIVE),
        RacingCar("Adaptive Racer", 350, 4.0, 0.82, 13, DriverStyle.BALANCED),
        RacingCar("Chaos Cruiser", 360, 3.8, 0.75, 11, DriverStyle.CHAOTIC)
    ]
    
    enhanced_racers = []
    for car in cars:
        enhanced_racers.append(EnhancedAIRacer(car, personality_system))
        
    return enhanced_racers