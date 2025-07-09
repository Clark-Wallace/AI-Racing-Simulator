from typing import List, Dict, Optional
from racing_car import RacingCar
from race_track import RaceTrack
from race_simulator import RaceSimulator, RaceEvent
from race_intelligence import RacingIntelligence, RaceSituation, RacePhase, TacticalDecision
from data_prizes import DataPrizeSystem
import random


class IntelligentRaceSimulator(RaceSimulator):
    """Enhanced race simulator with AI intelligence system"""
    
    def __init__(self, track: RaceTrack, cars: List[RacingCar], laps: int = 10, 
                 enable_telemetry: bool = True, enable_intelligence: bool = True,
                 prize_system: Optional[DataPrizeSystem] = None):
        super().__init__(track, cars, laps, enable_telemetry)
        
        self.enable_intelligence = enable_intelligence
        self.prize_system = prize_system
        self.ai_systems: Dict[str, RacingIntelligence] = {}
        
        # Initialize AI systems for each car
        if enable_intelligence:
            for car in cars:
                self.ai_systems[car.name] = RacingIntelligence(car, prize_system)
                
    def simulate_race(self) -> Dict:
        """Run race simulation with intelligent AI decisions"""
        print(f"\n🏁 INTELLIGENT RACE START at {self.track.name} - {self.laps} laps")
        print(f"Track Type: {self.track.track_type.value}")
        print(f"Weather: {self.track.weather_conditions}")
        print(f"Track Length: {self.track.total_length:.2f} km")
        print(f"Intelligence: {'ENABLED' if self.enable_intelligence else 'DISABLED'}\n")
        
        # Pre-race analysis
        if self.enable_intelligence:
            print("🧠 Pre-Race Intelligence Analysis:")
            for car in self.cars:
                ai = self.ai_systems[car.name]
                plan = ai.analyze_pre_race(self.cars, self.track.track_type, self.laps)
                print(f"  {car.name}: {plan.overall_strategy} strategy, "
                      f"target P{plan.target_position}, risk {plan.risk_tolerance:.1f}")
            print()
        
        # Run the base race simulation
        return super().simulate_race()
    
    def _apply_driver_style_decision(self, car: RacingCar, optimal_speed: float, 
                                   segment) -> float:
        """Override to use intelligent decision making"""
        if not self.enable_intelligence or car.name not in self.ai_systems:
            # Fall back to base behavior
            return super()._apply_driver_style_decision(car, optimal_speed, segment)
        
        # Get AI system
        ai = self.ai_systems[car.name]
        
        # Analyze current situation
        situation = self._analyze_race_situation(car)
        
        # Get tactical advice
        advice = ai.make_tactical_decision(situation, segment)
        
        # Apply tactical advice to speed decision
        base_speed = super()._apply_driver_style_decision(car, optimal_speed, segment)
        tactical_speed = base_speed * advice.target_speed_modifier
        
        # Handle specific tactical decisions
        if advice.decision == TacticalDecision.ATTACK:
            self._attempt_overtake(car, situation, advice)
        elif advice.decision == TacticalDecision.DEFEND:
            tactical_speed *= 0.98  # Slightly slower for defensive line
        elif advice.decision == TacticalDecision.SLIPSTREAM:
            if situation.gap_ahead < 1.0:
                tactical_speed *= 1.02  # Slipstream boost
                
        # Apply psychological tactics if recommended
        if situation.competitors_near:
            target = situation.competitors_near[0]
            psych_tactic = ai.get_psychological_tactics(target, situation.gap_ahead)
            if psych_tactic == "constant_pressure":
                tactical_speed = self._match_speed_ahead(car, target) * 1.01
            elif psych_tactic == "bait_mistakes":
                # Vary speed to create fake opportunities
                tactical_speed *= (0.98 + random.random() * 0.06)
                
        return tactical_speed
    
    def _analyze_race_situation(self, car: RacingCar) -> RaceSituation:
        """Analyze current race situation for a car"""
        # Determine race phase
        progress = (car.current_lap + 1) / self.laps
        if progress < 0.1:
            phase = RacePhase.START
        elif progress < 0.3:
            phase = RacePhase.EARLY
        elif progress < 0.7:
            phase = RacePhase.MIDDLE
        elif progress < 0.9:
            phase = RacePhase.LATE
        else:
            phase = RacePhase.FINAL
            
        # Calculate gaps
        position = self.current_positions[car.name] + 1
        gap_ahead = self._calculate_gap_ahead(car)
        gap_behind = self._calculate_gap_behind(car)
        
        # Find nearby competitors
        competitors_near = self._find_nearby_competitors(car, 2.0)  # Within 2 seconds
        
        # Track position
        segment_idx, segment_pos = self._get_car_segment(car)
        segment = self.track.segments[segment_idx]
        track_position = (car.distance_traveled % (self.track.total_length * 1000)) / (self.track.total_length * 1000)
        
        return RaceSituation(
            phase=phase,
            position=position,
            gap_ahead=gap_ahead,
            gap_behind=gap_behind,
            laps_remaining=self.laps - car.current_lap,
            fuel_status=car.fuel_level,
            tire_condition=100 - car.tire_wear,
            track_position=track_position,
            is_cornering=not segment.is_straight,
            competitors_near=competitors_near
        )
    
    def _calculate_gap_ahead(self, car: RacingCar) -> float:
        """Calculate time gap to car ahead"""
        position = self.current_positions[car.name]
        if position == 0:  # Leading
            return 999.0
            
        # Find car ahead
        for other_car in self.cars:
            if self.current_positions[other_car.name] == position - 1:
                distance_gap = other_car.distance_traveled - car.distance_traveled
                if distance_gap > 0 and car.current_speed > 0:
                    return distance_gap / (car.current_speed / 3.6)  # Convert to seconds
                    
        return 999.0
    
    def _calculate_gap_behind(self, car: RacingCar) -> float:
        """Calculate time gap to car behind"""
        position = self.current_positions[car.name]
        if position == len(self.cars) - 1:  # Last
            return 999.0
            
        # Find car behind
        for other_car in self.cars:
            if self.current_positions[other_car.name] == position + 1:
                distance_gap = car.distance_traveled - other_car.distance_traveled
                if distance_gap > 0 and other_car.current_speed > 0:
                    return distance_gap / (other_car.current_speed / 3.6)
                    
        return 999.0
    
    def _find_nearby_competitors(self, car: RacingCar, threshold_seconds: float) -> List[str]:
        """Find competitors within threshold seconds"""
        nearby = []
        
        for other_car in self.cars:
            if other_car.name == car.name:
                continue
                
            distance_gap = abs(other_car.distance_traveled - car.distance_traveled)
            avg_speed = (car.current_speed + other_car.current_speed) / 2
            
            if avg_speed > 0:
                time_gap = distance_gap / (avg_speed / 3.6)
                if time_gap <= threshold_seconds:
                    nearby.append(other_car.name)
                    
        return sorted(nearby, key=lambda n: abs(next(c.distance_traveled for c in self.cars if c.name == n) - car.distance_traveled))
    
    def _match_speed_ahead(self, car: RacingCar, target_name: str) -> float:
        """Match speed of car ahead for pressure tactics"""
        for other_car in self.cars:
            if other_car.name == target_name:
                return other_car.current_speed
        return car.current_speed
    
    def _attempt_overtake(self, car: RacingCar, situation: RaceSituation, advice):
        """Handle overtaking attempt"""
        if not situation.competitors_near:
            return
            
        target_name = situation.competitors_near[0]
        ai = self.ai_systems[car.name]
        
        # Calculate success probability
        success_prob = 0.5  # Base probability
        
        # Modify based on advice confidence
        success_prob *= advice.confidence
        
        # Modify based on track position
        if situation.is_cornering:
            success_prob *= 0.6  # Harder in corners
            
        # Modify based on competitor intelligence
        if self.prize_system:
            intel = self.prize_system.analyze_competitor(car.name, target_name)
            if intel:
                if "poor defending" in str(intel.weaknesses):
                    success_prob *= 1.3
                if "strong defending" in str(intel.strengths):
                    success_prob *= 0.7
                    
        # Attempt overtake
        if random.random() < success_prob:
            # Successful overtake
            self._execute_overtake(car, target_name)
            ai.learn_from_outcome(True, True, target_name)
            
            self.events.append(RaceEvent(
                self.race_time,
                "INTELLIGENT_OVERTAKE",
                car.name,
                f"Successfully executed {advice.decision.value} on {target_name}"
            ))
        else:
            # Failed overtake
            ai.learn_from_outcome(True, False, target_name)
            
            # Small time penalty for failed attempt
            car.current_speed *= 0.95
            
            self.events.append(RaceEvent(
                self.race_time,
                "FAILED_OVERTAKE",
                car.name,
                f"Failed {advice.decision.value} attempt on {target_name}"
            ))
    
    def _execute_overtake(self, overtaker: RacingCar, target_name: str):
        """Execute a successful overtake"""
        # Find target car
        target_car = next(c for c in self.cars if c.name == target_name)
        
        # Swap positions if overtaker is behind
        if overtaker.distance_traveled < target_car.distance_traveled:
            # Boost overtaker slightly ahead
            boost_distance = 5  # meters
            overtaker.distance_traveled = target_car.distance_traveled + boost_distance
            
    def _update_positions(self):
        """Update positions and track AI strategy adjustments"""
        super()._update_positions()
        
        # Update AI strategies based on current positions
        if self.enable_intelligence:
            for car in self.cars:
                if car.name in self.ai_systems and car.name not in self.finished_cars:
                    ai = self.ai_systems[car.name]
                    ai.adjust_strategy_mid_race(
                        self.current_positions[car.name] + 1,
                        self.laps - car.current_lap,
                        car.fuel_level,
                        100 - car.tire_wear
                    )
    
    def _compile_race_results(self) -> Dict:
        """Compile results including intelligence metrics"""
        results = super()._compile_race_results()
        
        if self.enable_intelligence:
            results["intelligence_metrics"] = {}
            
            for car_name, ai in self.ai_systems.items():
                results["intelligence_metrics"][car_name] = {
                    "strategy": ai.strategic_plan.overall_strategy if ai.strategic_plan else "none",
                    "target_position": ai.strategic_plan.target_position if ai.strategic_plan else 0,
                    "successful_overtakes": len(ai.successful_overtakes),
                    "failed_overtakes": sum(ai.failed_overtakes.values()),
                    "final_risk_tolerance": ai.strategic_plan.risk_tolerance if ai.strategic_plan else 0
                }
                
        return results
    
    def print_race_summary(self, results: Dict):
        """Print enhanced race summary with intelligence data"""
        super().print_race_summary(results)
        
        if "intelligence_metrics" in results:
            print("\n🧠 INTELLIGENCE METRICS:")
            for car_name, metrics in results["intelligence_metrics"].items():
                print(f"\n{car_name}:")
                print(f"  Strategy: {metrics['strategy']}")
                print(f"  Target: P{metrics['target_position']}")
                print(f"  Overtakes: {metrics['successful_overtakes']} successful, "
                      f"{metrics['failed_overtakes']} failed")
                print(f"  Final Risk Level: {metrics['final_risk_tolerance']:.2f}")
                
            # Show notable intelligent moves
            print("\n💡 INTELLIGENT MOVES:")
            intel_events = [e for e in results["events"] 
                          if e.event_type in ["INTELLIGENT_OVERTAKE", "FAILED_OVERTAKE"]]
            for event in intel_events[-5:]:  # Last 5
                print(f"  {event.time:.1f}s - {event.car_name}: {event.details}")