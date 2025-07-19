from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum
import random
import math
from datetime import datetime
from ..core.racing_car import DriverStyle


class EmotionalState(Enum):
    CALM = "calm"
    FOCUSED = "focused"
    FRUSTRATED = "frustrated"
    CONFIDENT = "confident"
    NERVOUS = "nervous"
    ANGRY = "angry"
    DETERMINED = "determined"
    RECKLESS = "reckless"
    EXHAUSTED = "exhausted"


class RelationshipType(Enum):
    RIVAL = "rival"
    NEMESIS = "nemesis"
    RESPECTED = "respected"
    NEUTRAL = "neutral"
    TEAMMATE = "teammate"
    MENTOR = "mentor"
    STUDENT = "student"


class PersonalityTrait(Enum):
    # Core traits
    AGGRESSIVE = "aggressive"
    PATIENT = "patient"
    PERFECTIONIST = "perfectionist"
    SHOWBOAT = "showboat"
    UNDERDOG = "underdog"
    VETERAN = "veteran"
    HOTHEAD = "hothead"
    CALCULATOR = "calculator"
    WILDCARD = "wildcard"
    INTIMIDATOR = "intimidator"
    
    # Quirks
    LATE_BRAKER = "late_braker"
    EARLY_STARTER = "early_starter"
    RAIN_MASTER = "rain_master"
    PRESSURE_LOVER = "pressure_lover"
    COMEBACK_KID = "comeback_kid"
    LUCKY = "lucky"
    UNLUCKY = "unlucky"
    CLUTCH = "clutch"
    CHOKER = "choker"


@dataclass
class Relationship:
    """Relationship between two racers"""
    target: str
    relationship_type: RelationshipType
    intensity: float  # 0-1, how strong the relationship is
    history: List[str] = field(default_factory=list)  # Notable events
    respect_level: float = 0.5  # 0-1, independent of relationship type
    
    
@dataclass
class PersonalityProfile:
    """Complete personality profile for a racer"""
    name: str
    nickname: str
    backstory: str
    primary_traits: List[PersonalityTrait]
    quirks: List[PersonalityTrait]
    signature_moves: List[str]
    catchphrases: List[str]
    strengths_description: str
    weaknesses_description: str
    racing_philosophy: str
    
    # Dynamic attributes
    emotional_state: EmotionalState = EmotionalState.CALM
    confidence_level: float = 0.7  # 0-1
    momentum: float = 0.0  # -1 to 1, affects performance
    fatigue_level: float = 0.0  # 0-1
    pressure_handling: float = 0.7  # 0-1
    
    # Career stats
    races_completed: int = 0
    wins: int = 0
    podiums: int = 0
    crashes: int = 0
    comebacks: int = 0
    bitter_defeats: int = 0
    
    # Relationships
    relationships: Dict[str, Relationship] = field(default_factory=dict)
    
    
class AIPersonalitySystem:
    """Enhanced personality system for AI racers"""
    
    def __init__(self):
        self.profiles: Dict[str, PersonalityProfile] = {}
        self.memorable_moments: List[Dict] = []
        self._initialize_personalities()
        
    def _initialize_personalities(self):
        """Create the 5 distinct AI personalities"""
        
        # Speed Demon - Max Velocity
        self.profiles["Speed Demon"] = PersonalityProfile(
            name="Speed Demon",
            nickname="Mad Max",
            backstory="Born with gasoline in his veins, Max discovered his need for speed at age 5 when he crashed his father's go-kart trying to break the track record. Never learned the meaning of 'brake pedal.'",
            primary_traits=[PersonalityTrait.AGGRESSIVE, PersonalityTrait.HOTHEAD, PersonalityTrait.SHOWBOAT],
            quirks=[PersonalityTrait.LATE_BRAKER, PersonalityTrait.PRESSURE_LOVER],
            signature_moves=["The Demon Dive", "Afterburner Overtake", "No-Lift Challenge"],
            catchphrases=["Brakes are for quitters!", "If you're not first, you're last!", "Speed is my religion!"],
            strengths_description="Unmatched straight-line speed and fearless overtaking",
            weaknesses_description="Prone to spectacular crashes and tire destruction",
            racing_philosophy="Maximum attack, all the time. The track is my playground."
        )
        
        # Tech Precision - Dr. Apex
        self.profiles["Tech Precision"] = PersonalityProfile(
            name="Tech Precision",
            nickname="The Professor",
            backstory="Former aerospace engineer who calculated the perfect racing line in his PhD thesis. Approaches racing like a mathematical equation. Has memorized every track down to the millimeter.",
            primary_traits=[PersonalityTrait.PERFECTIONIST, PersonalityTrait.CALCULATOR, PersonalityTrait.PATIENT],
            quirks=[PersonalityTrait.RAIN_MASTER, PersonalityTrait.CLUTCH],
            signature_moves=["The Surgical Strike", "Apex Perfection", "The Chess Move"],
            catchphrases=["Precision beats power.", "I've already calculated your next move.", "Racing is 90% mental."],
            strengths_description="Flawless technique and unshakeable consistency",
            weaknesses_description="Can be too cautious and struggles with chaos",
            racing_philosophy="Every millisecond counts. Perfection through preparation."
        )
        
        # Fuel Master - Eco Eddie
        self.profiles["Fuel Master"] = PersonalityProfile(
            name="Fuel Master",
            nickname="The Economist",
            backstory="Started racing during the fuel crisis and learned to squeeze every drop. Once finished a race on fumes with the engine cutting out as he crossed the line. Environmental activist off-track.",
            primary_traits=[PersonalityTrait.PATIENT, PersonalityTrait.VETERAN, PersonalityTrait.CALCULATOR],
            quirks=[PersonalityTrait.LUCKY, PersonalityTrait.COMEBACK_KID],
            signature_moves=["The Fuel Stretch", "Slipstream Savior", "The Long Game"],
            catchphrases=["Slow and steady wins the race.", "Every drop counts.", "Patience is a virtue."],
            strengths_description="Unmatched fuel efficiency and endurance racing master",
            weaknesses_description="Lacks explosive speed and struggles in short races",
            racing_philosophy="Racing is a marathon, not a sprint. Efficiency is elegance."
        )
        
        # Adaptive Racer - The Chameleon
        self.profiles["Adaptive Racer"] = PersonalityProfile(
            name="Adaptive Racer",
            nickname="The Chameleon",
            backstory="Mystery driver who appeared from nowhere. Rumored to be a former spy who uses racing to stay sharp. Adapts to any situation and seems to have a sixth sense for strategy.",
            primary_traits=[PersonalityTrait.CALCULATOR, PersonalityTrait.INTIMIDATOR, PersonalityTrait.VETERAN],
            quirks=[PersonalityTrait.CLUTCH, PersonalityTrait.EARLY_STARTER],
            signature_moves=["The Shape Shift", "Mirror Match", "The Counter"],
            catchphrases=["I am whatever you need me to be.", "Adaptation is survival.", "Your strength is my opportunity."],
            strengths_description="Incredible adaptability and strategic thinking",
            weaknesses_description="Jack of all trades, master of none",
            racing_philosophy="Be water. Flow around obstacles, strike at weakness."
        )
        
        # Chaos Cruiser - Wild Bill
        self.profiles["Chaos Cruiser"] = PersonalityProfile(
            name="Chaos Cruiser",
            nickname="The Tornado",
            backstory="Former stunt driver who got banned from movies for being 'too unpredictable'. Believes that if you can predict it, it's not worth doing. Has a lucky dice hanging from his mirror.",
            primary_traits=[PersonalityTrait.WILDCARD, PersonalityTrait.SHOWBOAT, PersonalityTrait.UNDERDOG],
            quirks=[PersonalityTrait.LUCKY, PersonalityTrait.UNLUCKY, PersonalityTrait.CHOKER],
            signature_moves=["The Chaos Theory", "Random Number Generator", "The Wild Card"],
            catchphrases=["Chaos is a ladder!", "Nobody expects the unexpected!", "Let's roll the dice!"],
            strengths_description="Completely unpredictable and thrives in chaos",
            weaknesses_description="Inconsistent and prone to self-destruction",
            racing_philosophy="If you don't know what you're doing, neither does your opponent."
        )
        
    def get_emotional_response(self, profile: PersonalityProfile, event: str, 
                             context: Dict) -> Tuple[EmotionalState, Optional[str]]:
        """Get emotional response to an event"""
        old_state = profile.emotional_state
        new_state = old_state
        reaction = None
        
        # Event-based emotional transitions
        if event == "overtaken":
            if PersonalityTrait.HOTHEAD in profile.primary_traits:
                new_state = EmotionalState.ANGRY
                reaction = random.choice(["That's it, gloves are off!", "You'll pay for that!", "Nobody passes ME!"])
            elif PersonalityTrait.PATIENT in profile.primary_traits:
                new_state = EmotionalState.FOCUSED
                reaction = "Patience... my time will come."
            else:
                new_state = EmotionalState.FRUSTRATED
                
        elif event == "overtake_success":
            if PersonalityTrait.SHOWBOAT in profile.primary_traits:
                new_state = EmotionalState.CONFIDENT
                reaction = random.choice(["Too easy!", "See ya!", "Another one bites the dust!"])
            else:
                new_state = EmotionalState.FOCUSED
                
        elif event == "crash":
            if PersonalityTrait.COMEBACK_KID in profile.quirks:
                new_state = EmotionalState.DETERMINED
                reaction = "This isn't over yet!"
            else:
                new_state = EmotionalState.FRUSTRATED
                reaction = "Not like this!"
                
        elif event == "leading":
            if profile.confidence_level > 0.8:
                new_state = EmotionalState.CONFIDENT
            else:
                new_state = EmotionalState.NERVOUS
                reaction = "Don't look back, don't look back..."
                
        elif event == "final_lap":
            if PersonalityTrait.CLUTCH in profile.quirks:
                new_state = EmotionalState.DETERMINED
                reaction = "This is my moment!"
            elif PersonalityTrait.CHOKER in profile.quirks:
                new_state = EmotionalState.NERVOUS
                reaction = "Don't mess this up..."
                
        elif event == "low_fuel":
            if profile.name == "Fuel Master":
                new_state = EmotionalState.CALM
                reaction = "All according to plan."
            else:
                new_state = EmotionalState.NERVOUS
                
        profile.emotional_state = new_state
        return new_state, reaction
    
    def update_relationship(self, racer1: str, racer2: str, event: str, context: Dict):
        """Update relationship between two racers"""
        if racer1 not in self.profiles or racer2 not in self.profiles:
            return
            
        profile1 = self.profiles[racer1]
        
        # Initialize relationship if needed
        if racer2 not in profile1.relationships:
            profile1.relationships[racer2] = Relationship(
                target=racer2,
                relationship_type=RelationshipType.NEUTRAL,
                intensity=0.0
            )
            
        rel = profile1.relationships[racer2]
        
        # Update based on event
        if event == "collision":
            rel.intensity = min(1.0, rel.intensity + 0.3)
            if rel.intensity > 0.7:
                rel.relationship_type = RelationshipType.NEMESIS
            else:
                rel.relationship_type = RelationshipType.RIVAL
            rel.history.append(f"Collision at {context.get('track', 'unknown')} - {datetime.now()}")
            rel.respect_level = max(0, rel.respect_level - 0.2)
            
        elif event == "clean_battle":
            rel.respect_level = min(1.0, rel.respect_level + 0.1)
            if rel.respect_level > 0.8:
                rel.relationship_type = RelationshipType.RESPECTED
            rel.history.append(f"Epic battle at {context.get('track', 'unknown')}")
            
        elif event == "helped":
            rel.relationship_type = RelationshipType.TEAMMATE
            rel.respect_level = min(1.0, rel.respect_level + 0.3)
            rel.history.append(f"{racer2} helped in race")
            
    def apply_emotional_modifiers(self, profile: PersonalityProfile) -> Dict[str, float]:
        """Get performance modifiers based on emotional state"""
        modifiers = {
            "speed": 1.0,
            "acceleration": 1.0,
            "handling": 1.0,
            "risk_taking": 1.0,
            "consistency": 1.0
        }
        
        # Emotional state effects
        state_modifiers = {
            EmotionalState.CALM: {"consistency": 1.05},
            EmotionalState.FOCUSED: {"handling": 1.08, "consistency": 1.05},
            EmotionalState.FRUSTRATED: {"risk_taking": 1.2, "consistency": 0.9},
            EmotionalState.CONFIDENT: {"speed": 1.05, "acceleration": 1.05},
            EmotionalState.NERVOUS: {"handling": 0.95, "consistency": 0.9},
            EmotionalState.ANGRY: {"speed": 1.08, "risk_taking": 1.3, "handling": 0.92},
            EmotionalState.DETERMINED: {"speed": 1.06, "acceleration": 1.06, "consistency": 1.03},
            EmotionalState.RECKLESS: {"speed": 1.1, "risk_taking": 1.5, "handling": 0.85},
            EmotionalState.EXHAUSTED: {"speed": 0.95, "handling": 0.92, "consistency": 0.88}
        }
        
        # Apply state modifiers
        if profile.emotional_state in state_modifiers:
            for key, value in state_modifiers[profile.emotional_state].items():
                modifiers[key] *= value
                
        # Apply momentum
        if profile.momentum > 0:
            modifiers["speed"] *= (1 + profile.momentum * 0.05)
            modifiers["confidence"] = 1 + profile.momentum * 0.1
        else:
            modifiers["consistency"] *= (1 + profile.momentum * 0.1)  # Negative momentum hurts consistency
            
        # Apply fatigue
        fatigue_penalty = profile.fatigue_level * 0.1
        modifiers["speed"] *= (1 - fatigue_penalty)
        modifiers["handling"] *= (1 - fatigue_penalty * 1.5)  # Handling suffers more
        
        return modifiers
    
    def get_signature_move_decision(self, profile: PersonalityProfile, 
                                   situation: Dict) -> Optional[str]:
        """Decide if a signature move should be attempted"""
        if profile.emotional_state not in [EmotionalState.CONFIDENT, 
                                          EmotionalState.DETERMINED,
                                          EmotionalState.RECKLESS]:
            return None
            
        if profile.confidence_level < 0.6:
            return None
            
        # Check situation for signature move opportunity
        if situation.get("gap_ahead", 999) < 0.5:  # Very close to car ahead
            if "The Demon Dive" in profile.signature_moves and random.random() < 0.3:
                return "The Demon Dive"
            elif "The Surgical Strike" in profile.signature_moves and situation.get("is_corner"):
                return "The Surgical Strike"
                
        if situation.get("laps_remaining", 999) == 1:  # Final lap
            if "The Chess Move" in profile.signature_moves:
                return "The Chess Move"
                
        if situation.get("fuel_critical") and "The Fuel Stretch" in profile.signature_moves:
            return "The Fuel Stretch"
            
        return None
    
    def update_momentum(self, profile: PersonalityProfile, event: str):
        """Update racer's momentum based on events"""
        momentum_changes = {
            "overtake_success": 0.2,
            "fastest_lap": 0.15,
            "defended_position": 0.1,
            "overtaken": -0.15,
            "mistake": -0.2,
            "crash": -0.5,
            "mechanical_issue": -0.3
        }
        
        if event in momentum_changes:
            profile.momentum = max(-1, min(1, profile.momentum + momentum_changes[event]))
            
    def update_confidence(self, profile: PersonalityProfile, results: Dict):
        """Update confidence based on race results"""
        position = results.get("position", 5)
        expected = results.get("expected_position", 3)
        
        # Base confidence change
        if position < expected:
            confidence_boost = (expected - position) * 0.1
        else:
            confidence_boost = (expected - position) * 0.05  # Losses hurt more
            
        # Trait modifiers
        if PersonalityTrait.CONFIDENT in profile.primary_traits:
            confidence_boost *= 0.7  # Less affected by results
        elif PersonalityTrait.UNDERDOG in profile.primary_traits:
            if position <= 3:
                confidence_boost *= 1.5  # Bigger boost from good results
                
        profile.confidence_level = max(0.1, min(1.0, profile.confidence_level + confidence_boost))
        
    def generate_pre_race_quote(self, profile: PersonalityProfile, context: Dict) -> str:
        """Generate pre-race quote based on personality and context"""
        rival = context.get("main_rival")
        track_type = context.get("track_type")
        
        # Check for rival-specific quotes
        if rival and rival in profile.relationships:
            rel = profile.relationships[rival]
            if rel.relationship_type == RelationshipType.NEMESIS:
                return f"I see {rival} is here. This time, it's personal."
            elif rel.relationship_type == RelationshipType.RESPECTED:
                return f"{rival} brings out the best in me. May the best racer win."
                
        # Personality-based quotes
        if profile.emotional_state == EmotionalState.CONFIDENT:
            return random.choice(profile.catchphrases)
            
        if PersonalityTrait.VETERAN in profile.primary_traits:
            return "I've raced this track a hundred times. Experience will show."
            
        if PersonalityTrait.UNDERDOG in profile.primary_traits:
            return "They don't expect much from me. Perfect."
            
        # Default to catchphrase
        return random.choice(profile.catchphrases)
    
    def generate_post_race_quote(self, profile: PersonalityProfile, 
                                position: int, context: Dict) -> str:
        """Generate post-race quote based on results"""
        if position == 1:
            if PersonalityTrait.SHOWBOAT in profile.primary_traits:
                return "Too easy! Who's next?"
            elif PersonalityTrait.PERFECTIONIST in profile.primary_traits:
                return "A calculated victory. Everything went according to plan."
            else:
                return "What a race! This one's for the team!"
                
        elif position <= 3:
            if profile.momentum > 0.5:
                return "Podium today, victory tomorrow. We're building something."
            else:
                return "Not quite there yet, but we're getting closer."
                
        else:
            if PersonalityTrait.COMEBACK_KID in profile.quirks:
                return "Today wasn't our day, but I'll be back stronger."
            elif profile.emotional_state == EmotionalState.ANGRY:
                return "This isn't over. Not by a long shot."
            else:
                return "We'll analyze what went wrong and come back fighting."
                
    def evolve_personality(self, profile: PersonalityProfile, season_results: Dict):
        """Long-term personality evolution based on career"""
        total_races = season_results.get("races", 0)
        wins = season_results.get("wins", 0)
        crashes = season_results.get("crashes", 0)
        
        # Update career stats
        profile.races_completed += total_races
        profile.wins += wins
        profile.crashes += crashes
        
        # Personality evolution
        if wins > total_races * 0.3:  # Winning a lot
            if PersonalityTrait.UNDERDOG in profile.primary_traits:
                profile.primary_traits.remove(PersonalityTrait.UNDERDOG)
                profile.primary_traits.append(PersonalityTrait.VETERAN)
                
        if crashes > total_races * 0.2:  # Crashing too much
            if PersonalityTrait.RECKLESS not in profile.quirks:
                profile.quirks.append(PersonalityTrait.UNLUCKY)
                
        if profile.races_completed > 50 and PersonalityTrait.VETERAN not in profile.primary_traits:
            profile.primary_traits.append(PersonalityTrait.VETERAN)
            
    def create_memorable_moment(self, event_type: str, participants: List[str], 
                               context: Dict) -> Dict:
        """Create a memorable moment for race history"""
        moment = {
            "timestamp": datetime.now(),
            "event_type": event_type,
            "participants": participants,
            "track": context.get("track", "Unknown"),
            "description": self._generate_moment_description(event_type, participants, context),
            "significance": self._calculate_moment_significance(event_type, context)
        }
        
        self.memorable_moments.append(moment)
        
        # Update relationships based on moment
        if event_type in ["epic_battle", "controversial_overtake", "collision"]:
            self.update_relationship(participants[0], participants[1], event_type, context)
            
        return moment
    
    def _generate_moment_description(self, event_type: str, participants: List[str], 
                                    context: Dict) -> str:
        """Generate description for memorable moment"""
        descriptions = {
            "epic_battle": f"{participants[0]} and {participants[1]} engaged in a {context.get('duration', 5)}-lap duel that will be remembered for years",
            "comeback_victory": f"{participants[0]} fought from {context.get('start_pos', 'last')} to win in spectacular fashion",
            "controversial_overtake": f"{participants[0]}'s aggressive move on {participants[1]} sparked debate in the paddock",
            "perfect_race": f"{participants[0]} dominated from start to finish, a masterclass in {context.get('track_type', 'racing')}",
            "dramatic_finish": f"A three-way battle between {', '.join(participants)} came down to the final corner"
        }
        
        return descriptions.get(event_type, f"A memorable moment involving {', '.join(participants)}")
    
    def _calculate_moment_significance(self, event_type: str, context: Dict) -> float:
        """Calculate how significant a moment is (0-1)"""
        base_significance = {
            "championship_decider": 1.0,
            "first_win": 0.9,
            "comeback_victory": 0.8,
            "epic_battle": 0.7,
            "perfect_race": 0.7,
            "controversial_overtake": 0.6,
            "dramatic_finish": 0.8,
            "collision": 0.5
        }
        
        significance = base_significance.get(event_type, 0.5)
        
        # Modifiers
        if context.get("final_lap"):
            significance *= 1.2
        if context.get("championship_implications"):
            significance *= 1.3
            
        return min(1.0, significance)