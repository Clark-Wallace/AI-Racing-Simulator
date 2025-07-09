from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
import math
import random
from racing_car import RacingCar, DriverStyle
from race_track import TrackSegment, TrackType
from data_prizes import DataPrizeSystem, CompetitorIntelligence


class TacticalDecision(Enum):
    ATTACK = "attack"  # Aggressive overtaking attempt
    DEFEND = "defend"  # Block passing attempts
    CONSERVE = "conserve"  # Save resources
    PRESSURE = "pressure"  # Apply psychological pressure
    WAIT = "wait"  # Bide time for better opportunity
    SLIPSTREAM = "slipstream"  # Use draft for speed boost


class RacePhase(Enum):
    START = "start"  # First 10% of race
    EARLY = "early"  # 10-30% of race
    MIDDLE = "middle"  # 30-70% of race
    LATE = "late"  # 70-90% of race
    FINAL = "final"  # Last 10% of race


@dataclass
class RaceSituation:
    """Current race situation analysis"""
    phase: RacePhase
    position: int
    gap_ahead: float  # seconds to car ahead
    gap_behind: float  # seconds to car behind
    laps_remaining: int
    fuel_status: float  # percentage remaining
    tire_condition: float  # 100 = fresh, 0 = worn
    track_position: float  # 0-1 position on track
    is_cornering: bool
    competitors_near: List[str]  # Names of nearby competitors


@dataclass
class StrategicPlan:
    """Strategic plan for the race"""
    overall_strategy: str
    target_position: int
    fuel_target_per_lap: float
    tire_preservation_level: float  # 0-1, higher = more preservation
    risk_tolerance: float  # 0-1, higher = more risk
    priority_targets: List[str]  # Competitors to focus on
    avoid_battles_with: List[str]  # Competitors to avoid fighting


@dataclass
class TacticalAdvice:
    """Tactical advice for current situation"""
    decision: TacticalDecision
    target_speed_modifier: float  # Multiplier for target speed
    aggression_level: float  # 0-1, affects overtaking attempts
    defensive_positioning: bool
    use_slipstream: bool
    recommended_line: str  # "racing", "defensive", "overtaking"
    confidence: float  # 0-1, confidence in the decision


class RacingIntelligence:
    """Enhanced AI decision-making using competitor intelligence"""
    
    def __init__(self, car: RacingCar, prize_system: Optional[DataPrizeSystem] = None):
        self.car = car
        self.prize_system = prize_system
        self.competitor_profiles: Dict[str, CompetitorIntelligence] = {}
        self.strategic_plan: Optional[StrategicPlan] = None
        self.race_history: List[RaceSituation] = []
        self.successful_overtakes: Set[str] = set()
        self.failed_overtakes: Dict[str, int] = {}  # Count of failed attempts
        
    def analyze_pre_race(self, competitors: List[RacingCar], track_type: TrackType, 
                        total_laps: int) -> StrategicPlan:
        """Analyze competitors and create race strategy"""
        # Gather intelligence on competitors
        if self.prize_system:
            for competitor in competitors:
                if competitor.name != self.car.name:
                    intel = self.prize_system.analyze_competitor(self.car.name, competitor.name)
                    if intel:
                        self.competitor_profiles[competitor.name] = intel
        
        # Determine overall strategy based on car strengths and track
        strategy = self._determine_race_strategy(track_type, total_laps)
        
        # Identify priority targets and threats
        priority_targets = self._identify_priority_targets(competitors)
        avoid_battles = self._identify_threats(competitors)
        
        # Calculate resource management targets
        fuel_per_lap = 100.0 / (total_laps * 1.1)  # 10% safety margin
        tire_preservation = self._calculate_tire_preservation(track_type, total_laps)
        
        # Set risk tolerance based on position goals and car characteristics
        risk_tolerance = self._calculate_risk_tolerance(len(competitors))
        
        self.strategic_plan = StrategicPlan(
            overall_strategy=strategy,
            target_position=self._calculate_target_position(len(competitors)),
            fuel_target_per_lap=fuel_per_lap,
            tire_preservation_level=tire_preservation,
            risk_tolerance=risk_tolerance,
            priority_targets=priority_targets,
            avoid_battles_with=avoid_battles
        )
        
        return self.strategic_plan
    
    def make_tactical_decision(self, situation: RaceSituation, 
                             current_segment: TrackSegment) -> TacticalAdvice:
        """Make tactical decision based on current situation"""
        # Store situation for learning
        self.race_history.append(situation)
        
        # Determine base tactical approach
        if situation.gap_ahead < 1.0 and not situation.is_cornering:
            # Close enough to attempt overtake
            decision = self._evaluate_overtaking_opportunity(situation, current_segment)
        elif situation.gap_behind < 0.5:
            # Under pressure, need to defend
            decision = TacticalDecision.DEFEND
        elif situation.phase == RacePhase.FINAL and situation.position > self.strategic_plan.target_position:
            # Final push needed
            decision = TacticalDecision.ATTACK
        elif situation.fuel_status < self.strategic_plan.fuel_target_per_lap * situation.laps_remaining:
            # Fuel saving needed
            decision = TacticalDecision.CONSERVE
        else:
            # Normal racing
            decision = self._evaluate_normal_racing(situation)
        
        # Get specific tactical advice
        advice = self._generate_tactical_advice(decision, situation, current_segment)
        
        return advice
    
    def _determine_race_strategy(self, track_type: TrackType, total_laps: int) -> str:
        """Determine overall race strategy"""
        # Base strategy on car strengths and track type
        if self.car.driver_style == DriverStyle.AGGRESSIVE:
            if track_type == TrackType.SPEED_TRACK:
                return "early_attack"  # Use speed advantage early
            else:
                return "opportunistic"  # Wait for mistakes
                
        elif self.car.driver_style == DriverStyle.CONSERVATIVE:
            if total_laps > 20:
                return "endurance_focus"  # Conserve and strike late
            else:
                return "consistent_pace"  # Steady performance
                
        elif self.car.driver_style == DriverStyle.TECHNICAL:
            if track_type == TrackType.TECHNICAL_TRACK:
                return "technical_mastery"  # Exploit handling advantage
            else:
                return "strategic_positioning"  # Smart track position
                
        elif self.car.driver_style == DriverStyle.CHAOTIC:
            return "disruptive"  # Create chaos and capitalize
            
        else:  # BALANCED
            return "adaptive"  # Adjust based on race development
    
    def _identify_priority_targets(self, competitors: List[RacingCar]) -> List[str]:
        """Identify which competitors to target"""
        targets = []
        
        for competitor in competitors:
            if competitor.name == self.car.name:
                continue
                
            # Check if we have intelligence showing weaknesses
            if competitor.name in self.competitor_profiles:
                intel = self.competitor_profiles[competitor.name]
                
                # Target if they have exploitable weaknesses
                if any(w in str(intel.weaknesses) for w in ["acceleration", "stability", "aggressive"]):
                    targets.append(competitor.name)
                    
            # Also target similar performance cars
            elif abs(competitor.top_speed - self.car.top_speed) < 20:
                targets.append(competitor.name)
                
        return targets[:2]  # Focus on top 2 targets
    
    def _identify_threats(self, competitors: List[RacingCar]) -> List[str]:
        """Identify competitors to avoid direct battles with"""
        threats = []
        
        for competitor in competitors:
            if competitor.name == self.car.name:
                continue
                
            # Check intelligence for superior capabilities
            if competitor.name in self.competitor_profiles:
                intel = self.competitor_profiles[competitor.name]
                
                # Avoid if they're stronger in key areas
                if any(s in str(intel.strengths) for s in ["overtaking", "defending", "speed"]):
                    if competitor.name not in self.failed_overtakes or self.failed_overtakes[competitor.name] < 2:
                        continue  # Still try once or twice
                    threats.append(competitor.name)
                    
            # Avoid much faster cars in early race
            elif competitor.top_speed > self.car.top_speed + 30:
                threats.append(competitor.name)
                
        return threats
    
    def _calculate_tire_preservation(self, track_type: TrackType, total_laps: int) -> float:
        """Calculate optimal tire preservation level"""
        base_preservation = 0.5
        
        # Adjust for track type
        if track_type == TrackType.TECHNICAL_TRACK:
            base_preservation += 0.2  # More tire wear on technical tracks
        elif track_type == TrackType.SPEED_TRACK:
            base_preservation -= 0.1  # Less wear on speed tracks
            
        # Adjust for race length
        if total_laps > 30:
            base_preservation += 0.2
        elif total_laps < 10:
            base_preservation -= 0.2
            
        # Adjust for driving style
        style_modifiers = {
            DriverStyle.AGGRESSIVE: -0.2,
            DriverStyle.CONSERVATIVE: 0.2,
            DriverStyle.TECHNICAL: 0.1,
            DriverStyle.CHAOTIC: -0.1,
            DriverStyle.BALANCED: 0.0
        }
        base_preservation += style_modifiers.get(self.car.driver_style, 0)
        
        return max(0.1, min(0.9, base_preservation))
    
    def _calculate_risk_tolerance(self, num_competitors: int) -> float:
        """Calculate risk tolerance based on goals and competition"""
        base_risk = 0.5
        
        # Adjust for driving style
        style_risks = {
            DriverStyle.AGGRESSIVE: 0.3,
            DriverStyle.CONSERVATIVE: -0.2,
            DriverStyle.TECHNICAL: -0.1,
            DriverStyle.CHAOTIC: 0.4,
            DriverStyle.BALANCED: 0.0
        }
        base_risk += style_risks.get(self.car.driver_style, 0)
        
        # Adjust based on competition level
        if num_competitors > 4:
            base_risk += 0.1  # More risk needed in larger fields
            
        return max(0.1, min(0.9, base_risk))
    
    def _calculate_target_position(self, num_competitors: int) -> int:
        """Calculate realistic target position"""
        # Base on car performance percentile
        performance_score = (
            self.car.top_speed / 400 * 0.3 +
            self.car.handling * 0.3 +
            (10 - self.car.acceleration) / 8 * 0.2 +
            self.car.fuel_efficiency / 20 * 0.2
        )
        
        # Higher score = better car
        if performance_score > 0.8:
            return 1  # Aim for win
        elif performance_score > 0.65:
            return min(2, num_competitors // 2)  # Aim for podium
        elif performance_score > 0.5:
            return min(3, (num_competitors * 2) // 3)  # Aim for points
        else:
            return min(4, num_competitors - 1)  # Aim to not be last
    
    def _evaluate_overtaking_opportunity(self, situation: RaceSituation, 
                                       segment: TrackSegment) -> TacticalDecision:
        """Evaluate whether to attempt an overtake"""
        if not situation.competitors_near:
            return TacticalDecision.WAIT
            
        target = situation.competitors_near[0]
        
        # Check if target is in our priority list
        if target in self.strategic_plan.avoid_battles_with:
            return TacticalDecision.WAIT
            
        # Check previous attempts
        if target in self.failed_overtakes and self.failed_overtakes[target] > 2:
            return TacticalDecision.PRESSURE  # Just pressure instead
            
        # Evaluate opportunity quality
        opportunity_score = 0.0
        
        # Track position factors
        if not segment.is_straight:
            opportunity_score -= 0.3  # Harder in corners
        if segment.length > 500:
            opportunity_score += 0.2  # Better on long segments
            
        # Performance advantage
        if target in self.competitor_profiles:
            intel = self.competitor_profiles[target]
            if "acceleration" in str(intel.weaknesses):
                opportunity_score += 0.3
            if "defensive" in str(intel.behavioral_patterns):
                opportunity_score -= 0.2
                
        # Race situation
        if situation.phase in [RacePhase.LATE, RacePhase.FINAL]:
            opportunity_score += 0.2  # More urgent
        if situation.tire_condition > 80:
            opportunity_score += 0.1  # Fresh tires
            
        # Risk assessment
        if situation.gap_behind < 1.0:
            opportunity_score -= 0.2  # Risk of losing position
            
        if opportunity_score > 0.3:
            return TacticalDecision.ATTACK
        elif opportunity_score > 0:
            return TacticalDecision.PRESSURE
        else:
            return TacticalDecision.WAIT
    
    def _evaluate_normal_racing(self, situation: RaceSituation) -> TacticalDecision:
        """Evaluate decision for normal racing conditions"""
        # Check if we should hunt the car ahead
        if situation.gap_ahead < 3.0 and situation.position > self.strategic_plan.target_position:
            return TacticalDecision.PRESSURE
            
        # Check if we should manage resources
        if situation.phase == RacePhase.MIDDLE:
            if situation.fuel_status < self.strategic_plan.fuel_target_per_lap * situation.laps_remaining * 1.05:
                return TacticalDecision.CONSERVE
                
        # Check for slipstream opportunities
        if situation.gap_ahead < 2.0 and not situation.is_cornering:
            return TacticalDecision.SLIPSTREAM
            
        return TacticalDecision.WAIT
    
    def _generate_tactical_advice(self, decision: TacticalDecision, 
                                situation: RaceSituation, 
                                segment: TrackSegment) -> TacticalAdvice:
        """Generate specific tactical advice"""
        advice_params = {
            TacticalDecision.ATTACK: {
                "speed_mod": 1.05,
                "aggression": 0.9,
                "defensive": False,
                "slipstream": True,
                "line": "overtaking",
                "confidence": 0.7
            },
            TacticalDecision.DEFEND: {
                "speed_mod": 0.98,
                "aggression": 0.3,
                "defensive": True,
                "slipstream": False,
                "line": "defensive",
                "confidence": 0.8
            },
            TacticalDecision.CONSERVE: {
                "speed_mod": 0.92,
                "aggression": 0.1,
                "defensive": False,
                "slipstream": True,
                "line": "racing",
                "confidence": 0.9
            },
            TacticalDecision.PRESSURE: {
                "speed_mod": 1.02,
                "aggression": 0.6,
                "defensive": False,
                "slipstream": True,
                "line": "racing",
                "confidence": 0.8
            },
            TacticalDecision.WAIT: {
                "speed_mod": 1.0,
                "aggression": 0.4,
                "defensive": False,
                "slipstream": True,
                "line": "racing",
                "confidence": 0.9
            },
            TacticalDecision.SLIPSTREAM: {
                "speed_mod": 0.98,
                "aggression": 0.5,
                "defensive": False,
                "slipstream": True,
                "line": "racing",
                "confidence": 0.85
            }
        }
        
        params = advice_params[decision]
        
        # Adjust for race phase
        if situation.phase == RacePhase.FINAL:
            params["speed_mod"] *= 1.03
            params["aggression"] = min(1.0, params["aggression"] * 1.2)
            
        # Adjust for competitor intelligence
        if situation.competitors_near and situation.competitors_near[0] in self.competitor_profiles:
            intel = self.competitor_profiles[situation.competitors_near[0]]
            if "aggressive" in str(intel.behavioral_patterns):
                params["defensive"] = True
                params["confidence"] *= 0.9
                
        return TacticalAdvice(
            decision=decision,
            target_speed_modifier=params["speed_mod"],
            aggression_level=params["aggression"],
            defensive_positioning=params["defensive"],
            use_slipstream=params["slipstream"],
            recommended_line=params["line"],
            confidence=params["confidence"]
        )
    
    def learn_from_outcome(self, attempted_overtake: bool, success: bool, target: str):
        """Learn from overtaking attempts"""
        if attempted_overtake:
            if success:
                self.successful_overtakes.add(target)
                # Reset failed counter on success
                if target in self.failed_overtakes:
                    del self.failed_overtakes[target]
            else:
                if target not in self.failed_overtakes:
                    self.failed_overtakes[target] = 0
                self.failed_overtakes[target] += 1
    
    def adjust_strategy_mid_race(self, current_position: int, laps_remaining: int,
                                fuel_status: float, tire_condition: float):
        """Adjust strategy based on race progress"""
        if not self.strategic_plan:
            return
            
        # Check if we're meeting targets
        position_delta = current_position - self.strategic_plan.target_position
        
        if position_delta > 1 and laps_remaining > 5:
            # Behind target, increase risk
            self.strategic_plan.risk_tolerance = min(0.9, self.strategic_plan.risk_tolerance + 0.1)
            
        elif position_delta < -1:
            # Ahead of target, can be more conservative
            self.strategic_plan.risk_tolerance = max(0.3, self.strategic_plan.risk_tolerance - 0.1)
            
        # Adjust fuel targets if needed
        required_fuel_per_lap = fuel_status / laps_remaining
        if required_fuel_per_lap < self.strategic_plan.fuel_target_per_lap * 0.9:
            # Need to save more fuel
            self.strategic_plan.fuel_target_per_lap = required_fuel_per_lap
            
    def get_psychological_tactics(self, target: str, gap: float) -> Optional[str]:
        """Get psychological tactics to use against a competitor"""
        if target not in self.competitor_profiles:
            return None
            
        intel = self.competitor_profiles[target]
        
        # Identify psychological pressure points
        if "inconsistent" in str(intel.behavioral_patterns):
            if gap < 0.5:
                return "constant_pressure"  # Stay very close to induce mistakes
                
        if "aggressive" in str(intel.behavioral_patterns):
            return "bait_mistakes"  # Show fake opportunities to bait errors
            
        if "conservative" in str(intel.behavioral_patterns):
            return "force_defensive"  # Make them waste time defending
            
        if intel.average_metrics.get("technical_error_rate", 0) > 0.5:
            return "exploit_corners"  # Pressure in technical sections
            
        return None
    
    def predict_competitor_move(self, competitor: str, situation: RaceSituation) -> Optional[str]:
        """Predict what a competitor might do"""
        if competitor not in self.competitor_profiles:
            return None
            
        intel = self.competitor_profiles[competitor]
        
        # Predict based on patterns
        predictions = []
        
        if situation.phase == RacePhase.FINAL:
            if "aggressive" in str(intel.behavioral_patterns):
                predictions.append("desperate_overtake")
            elif "conservative" in str(intel.behavioral_patterns):
                predictions.append("maintain_position")
                
        if situation.fuel_status < 20:
            if intel.average_metrics.get("efficiency_fuel_efficiency", 15) < 12:
                predictions.append("fuel_saving_mode")
                
        if situation.is_cornering:
            if "poor stability" in str(intel.weaknesses):
                predictions.append("wide_corner_exit")
                
        return predictions[0] if predictions else None