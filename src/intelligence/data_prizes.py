from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum
import json
from datetime import datetime
from ..systems.telemetry import PerformanceMetrics, TelemetrySystem


class AccessLevel(Enum):
    NONE = "none"
    BASIC = "basic"  # Summary data only
    DETAILED = "detailed"  # Full metrics
    FULL = "full"  # Complete telemetry including raw data


@dataclass
class DataAccess:
    """Represents data access rights for one car to another's data"""
    accessor: str  # Who has access
    target: str  # Whose data they can access
    level: AccessLevel
    granted_time: datetime
    race_name: str
    reason: str  # Why access was granted (e.g., "1st place prize")


@dataclass
class CompetitorIntelligence:
    """Intelligence gathered about a competitor"""
    competitor_name: str
    driver_style: str
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    preferred_tracks: List[str] = field(default_factory=list)
    average_metrics: Dict[str, float] = field(default_factory=dict)
    behavioral_patterns: List[str] = field(default_factory=list)
    recommended_strategies: List[str] = field(default_factory=list)


class DataPrizeSystem:
    """Manages data access rights and prize distribution after races"""
    
    def __init__(self):
        self.access_rights: List[DataAccess] = []
        self.telemetry_database: Dict[str, Dict[str, PerformanceMetrics]] = {}  # race_id -> car -> metrics
        self.competitor_profiles: Dict[str, CompetitorIntelligence] = {}
        
    def distribute_prizes(self, race_results: Dict, telemetry_system: Optional[TelemetrySystem] = None):
        """Distribute data access rights based on race results"""
        race_name = f"{race_results['track']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Store telemetry data for this race
        if telemetry_system:
            self.telemetry_database[race_name] = {}
            for metrics in telemetry_system.completed_sessions:
                self.telemetry_database[race_name][metrics.car_name] = metrics
        
        # Get positions
        positions = race_results.get("positions", {})
        if not positions:
            return
            
        # Apply prize distribution rules
        # 1st place: Gets own data + 4th place + 5th place data
        if 1 in positions:
            winner = positions[1]["name"]
            self._grant_access(winner, winner, AccessLevel.FULL, race_name, "Own data")
            
            if 4 in positions:
                self._grant_access(winner, positions[4]["name"], AccessLevel.DETAILED, 
                                 race_name, "1st place prize - 4th place data")
            if 5 in positions:
                self._grant_access(winner, positions[5]["name"], AccessLevel.DETAILED, 
                                 race_name, "1st place prize - 5th place data")
        
        # 2nd place: Gets own data + 4th place data
        if 2 in positions:
            second = positions[2]["name"]
            self._grant_access(second, second, AccessLevel.FULL, race_name, "Own data")
            
            if 4 in positions:
                self._grant_access(second, positions[4]["name"], AccessLevel.BASIC, 
                                 race_name, "2nd place prize - 4th place data")
        
        # 3rd place: Gets own data + 5th place data
        if 3 in positions:
            third = positions[3]["name"]
            self._grant_access(third, third, AccessLevel.FULL, race_name, "Own data")
            
            if 5 in positions:
                self._grant_access(third, positions[5]["name"], AccessLevel.BASIC, 
                                 race_name, "3rd place prize - 5th place data")
        
        # 4th and 5th place: Get only own data
        for pos in [4, 5]:
            if pos in positions:
                car_name = positions[pos]["name"]
                self._grant_access(car_name, car_name, AccessLevel.FULL, race_name, "Own data")
    
    def _grant_access(self, accessor: str, target: str, level: AccessLevel, 
                     race_name: str, reason: str):
        """Grant data access rights"""
        access = DataAccess(
            accessor=accessor,
            target=target,
            level=level,
            granted_time=datetime.now(),
            race_name=race_name,
            reason=reason
        )
        self.access_rights.append(access)
    
    def get_accessible_data(self, accessor: str, target: str) -> Optional[Dict]:
        """Get data that accessor is allowed to see about target"""
        # Find highest access level
        highest_access = AccessLevel.NONE
        for access in self.access_rights:
            if access.accessor == accessor and access.target == target:
                if access.level.value > highest_access.value:
                    highest_access = access.level
        
        if highest_access == AccessLevel.NONE:
            return None
            
        # Collect all telemetry data for target across races
        all_metrics = []
        for race_data in self.telemetry_database.values():
            if target in race_data:
                all_metrics.append(race_data[target])
        
        if not all_metrics:
            return None
            
        # Filter data based on access level
        if highest_access == AccessLevel.BASIC:
            return self._get_basic_summary(target, all_metrics)
        elif highest_access == AccessLevel.DETAILED:
            return self._get_detailed_metrics(target, all_metrics)
        else:  # FULL
            return self._get_full_telemetry(target, all_metrics)
    
    def _get_basic_summary(self, car_name: str, metrics_list: List[PerformanceMetrics]) -> Dict:
        """Get basic summary data"""
        latest = metrics_list[-1]  # Most recent race
        
        return {
            "car_name": car_name,
            "driver_style": latest.driver_style,
            "races_analyzed": len(metrics_list),
            "average_top_speed": sum(m.top_speed_achieved for m in metrics_list) / len(metrics_list),
            "average_lap_consistency": sum(m.consistency_variance for m in metrics_list) / len(metrics_list),
            "total_overtakes": sum(m.total_overtakes for m in metrics_list),
            "total_incidents": sum(m.incidents for m in metrics_list),
            "preferred_track_type": self._analyze_track_preference(metrics_list)
        }
    
    def _get_detailed_metrics(self, car_name: str, metrics_list: List[PerformanceMetrics]) -> Dict:
        """Get detailed metrics data"""
        latest = metrics_list[-1]
        
        # Calculate averages across all races
        avg_metrics = {
            "speed": {
                "top_speed": sum(m.top_speed_achieved for m in metrics_list) / len(metrics_list),
                "average_speed": sum(m.average_speed for m in metrics_list) / len(metrics_list),
                "acceleration_0_100": sum(m.acceleration_0_to_100 for m in metrics_list) / len(metrics_list)
            },
            "handling": {
                "cornering_efficiency": sum(m.cornering_efficiency for m in metrics_list) / len(metrics_list),
                "stability_rating": sum(m.stability_rating for m in metrics_list) / len(metrics_list),
                "average_corner_speed": sum(m.average_corner_speed for m in metrics_list) / len(metrics_list)
            },
            "efficiency": {
                "fuel_efficiency": sum(m.fuel_efficiency for m in metrics_list) / len(metrics_list),
                "endurance_rating": sum(m.endurance_rating for m in metrics_list) / len(metrics_list)
            },
            "strategic": {
                "overtaking_ability": sum(m.overtaking_ability for m in metrics_list) / len(metrics_list),
                "risk_tolerance": sum(m.risk_tolerance for m in metrics_list) / len(metrics_list),
                "race_intelligence": sum(m.race_intelligence for m in metrics_list) / len(metrics_list)
            }
        }
        
        return {
            "car_name": car_name,
            "driver_style": latest.driver_style,
            "races_analyzed": len(metrics_list),
            "average_metrics": avg_metrics,
            "performance_trends": self._analyze_performance_trends(metrics_list),
            "strengths": self._identify_strengths(avg_metrics),
            "weaknesses": self._identify_weaknesses(avg_metrics)
        }
    
    def _get_full_telemetry(self, car_name: str, metrics_list: List[PerformanceMetrics]) -> Dict:
        """Get full telemetry data including raw snapshots"""
        detailed = self._get_detailed_metrics(car_name, metrics_list)
        
        # Add raw data
        detailed["raw_metrics"] = []
        for metrics in metrics_list:
            detailed["raw_metrics"].append({
                "lap_times": metrics.lap_times,
                "sector_times": metrics.sector_times,
                "telemetry_snapshots": len(metrics.telemetry_data),  # Count only, not full data
                "incidents": metrics.incidents,
                "overtakes": metrics.total_overtakes,
                "times_overtaken": metrics.times_overtaken
            })
        
        # Add behavioral analysis
        detailed["behavioral_patterns"] = self._analyze_behavior_patterns(metrics_list)
        
        return detailed
    
    def analyze_competitor(self, accessor: str, target: str) -> Optional[CompetitorIntelligence]:
        """Analyze a competitor based on accessible data"""
        data = self.get_accessible_data(accessor, target)
        if not data:
            return None
            
        # Create or update competitor profile
        if target not in self.competitor_profiles:
            self.competitor_profiles[target] = CompetitorIntelligence(
                competitor_name=target,
                driver_style=data.get("driver_style", "unknown")
            )
        
        profile = self.competitor_profiles[target]
        
        # Update with latest analysis
        if "average_metrics" in data:
            profile.average_metrics = self._flatten_metrics(data["average_metrics"])
            profile.strengths = data.get("strengths", [])
            profile.weaknesses = data.get("weaknesses", [])
        
        if "behavioral_patterns" in data:
            profile.behavioral_patterns = data["behavioral_patterns"]
            
        # Generate strategic recommendations
        profile.recommended_strategies = self._generate_counter_strategies(profile)
        
        return profile
    
    def get_spy_network(self) -> Dict[str, Set[str]]:
        """Get visualization of who has access to whose data"""
        network = {}
        
        for access in self.access_rights:
            if access.accessor not in network:
                network[access.accessor] = set()
            if access.target != access.accessor:  # Don't include self-access
                network[access.accessor].add(access.target)
        
        return network
    
    def get_access_history(self, car_name: str) -> List[DataAccess]:
        """Get history of data access for a specific car"""
        history = []
        for access in self.access_rights:
            if access.accessor == car_name or access.target == car_name:
                history.append(access)
        return sorted(history, key=lambda x: x.granted_time, reverse=True)
    
    # Analysis helper methods
    
    def _analyze_track_preference(self, metrics_list: List[PerformanceMetrics]) -> str:
        """Analyze which track types the car performs best on"""
        # Simplified - would need track type info in real implementation
        avg_corner_speed = sum(m.average_corner_speed for m in metrics_list) / len(metrics_list)
        avg_top_speed = sum(m.top_speed_achieved for m in metrics_list) / len(metrics_list)
        
        if avg_top_speed > 370:
            return "speed_tracks"
        elif avg_corner_speed > 140:
            return "technical_tracks"
        else:
            return "mixed_tracks"
    
    def _analyze_performance_trends(self, metrics_list: List[PerformanceMetrics]) -> Dict:
        """Analyze performance trends over time"""
        if len(metrics_list) < 2:
            return {"trend": "insufficient_data"}
            
        # Compare first half to second half
        mid = len(metrics_list) // 2
        first_half = metrics_list[:mid]
        second_half = metrics_list[mid:]
        
        first_avg_speed = sum(m.average_speed for m in first_half) / len(first_half)
        second_avg_speed = sum(m.average_speed for m in second_half) / len(second_half)
        
        improvement = (second_avg_speed - first_avg_speed) / first_avg_speed * 100
        
        return {
            "speed_trend": "improving" if improvement > 2 else "declining" if improvement < -2 else "stable",
            "improvement_percentage": improvement,
            "consistency_trend": self._analyze_consistency_trend(first_half, second_half)
        }
    
    def _analyze_consistency_trend(self, first_half: List[PerformanceMetrics], 
                                   second_half: List[PerformanceMetrics]) -> str:
        """Analyze consistency trend"""
        first_consistency = sum(m.consistency_variance for m in first_half) / len(first_half)
        second_consistency = sum(m.consistency_variance for m in second_half) / len(second_half)
        
        # Lower variance is better
        if second_consistency < first_consistency * 0.9:
            return "improving"
        elif second_consistency > first_consistency * 1.1:
            return "declining"
        else:
            return "stable"
    
    def _identify_strengths(self, avg_metrics: Dict) -> List[str]:
        """Identify strengths from metrics"""
        strengths = []
        
        if avg_metrics["speed"]["top_speed"] > 360:
            strengths.append("Exceptional top speed")
        if avg_metrics["handling"]["cornering_efficiency"] > 0.8:
            strengths.append("Excellent cornering")
        if avg_metrics["efficiency"]["fuel_efficiency"] > 15:
            strengths.append("Superior fuel efficiency")
        if avg_metrics["strategic"]["overtaking_ability"] > 0.7:
            strengths.append("Strong overtaking ability")
        if avg_metrics["strategic"]["race_intelligence"] > 0.8:
            strengths.append("High race intelligence")
            
        return strengths
    
    def _identify_weaknesses(self, avg_metrics: Dict) -> List[str]:
        """Identify weaknesses from metrics"""
        weaknesses = []
        
        if avg_metrics["speed"]["top_speed"] < 340:
            weaknesses.append("Limited top speed")
        if avg_metrics["handling"]["stability_rating"] < 0.5:
            weaknesses.append("Poor stability in corners")
        if avg_metrics["efficiency"]["endurance_rating"] < 0.5:
            weaknesses.append("Struggles in long races")
        if avg_metrics["strategic"]["risk_tolerance"] > 0.9:
            weaknesses.append("Overly aggressive driving")
        if avg_metrics["speed"]["acceleration_0_100"] > 5:
            weaknesses.append("Slow acceleration")
            
        return weaknesses
    
    def _analyze_behavior_patterns(self, metrics_list: List[PerformanceMetrics]) -> List[str]:
        """Analyze behavioral patterns from telemetry"""
        patterns = []
        
        # Analyze overtaking patterns
        avg_overtakes = sum(m.total_overtakes for m in metrics_list) / len(metrics_list)
        if avg_overtakes > 3:
            patterns.append("Aggressive overtaker - attempts many passes")
        elif avg_overtakes < 1:
            patterns.append("Conservative - rarely attempts overtakes")
            
        # Analyze incident patterns
        total_incidents = sum(m.incidents for m in metrics_list)
        if total_incidents == 0:
            patterns.append("Clean driver - no incidents recorded")
        elif total_incidents / len(metrics_list) > 1:
            patterns.append("Incident prone - frequent crashes")
            
        # Analyze consistency
        avg_consistency = sum(m.consistency_variance for m in metrics_list) / len(metrics_list)
        if avg_consistency < 1:
            patterns.append("Highly consistent lap times")
        elif avg_consistency > 3:
            patterns.append("Inconsistent performance between laps")
            
        return patterns
    
    def _flatten_metrics(self, nested_metrics: Dict) -> Dict[str, float]:
        """Flatten nested metrics dictionary"""
        flat = {}
        for category, metrics in nested_metrics.items():
            for metric, value in metrics.items():
                flat[f"{category}_{metric}"] = value
        return flat
    
    def _generate_counter_strategies(self, profile: CompetitorIntelligence) -> List[str]:
        """Generate strategies to counter a competitor"""
        strategies = []
        
        # Based on weaknesses
        for weakness in profile.weaknesses:
            if "top speed" in weakness:
                strategies.append("Challenge on speed tracks with long straights")
            elif "stability" in weakness:
                strategies.append("Force into technical sections and tight corners")
            elif "long races" in weakness:
                strategies.append("Prefer endurance challenges")
            elif "aggressive" in weakness:
                strategies.append("Let them make mistakes through over-aggression")
            elif "acceleration" in weakness:
                strategies.append("Target them at race starts and corner exits")
        
        # Based on behavioral patterns
        for pattern in profile.behavioral_patterns:
            if "Conservative" in pattern:
                strategies.append("Apply pressure to force defensive driving")
            elif "Aggressive overtaker" in pattern:
                strategies.append("Defensive positioning in braking zones")
            elif "Inconsistent" in pattern:
                strategies.append("Wait for performance drops and capitalize")
                
        # Based on average metrics
        if profile.average_metrics.get("strategic_risk_tolerance", 0) > 0.8:
            strategies.append("Bait into risky maneuvers")
        if profile.average_metrics.get("efficiency_fuel_efficiency", 20) < 12:
            strategies.append("Force high fuel consumption early in race")
            
        return strategies
    
    def export_intelligence_report(self, accessor: str, target: str, filename: str):
        """Export competitor intelligence report to file"""
        intelligence = self.analyze_competitor(accessor, target)
        if not intelligence:
            return False
            
        report = {
            "report_date": datetime.now().isoformat(),
            "accessor": accessor,
            "target": target,
            "access_level": self._get_access_level(accessor, target).value,
            "intelligence": {
                "competitor_name": intelligence.competitor_name,
                "driver_style": intelligence.driver_style,
                "strengths": intelligence.strengths,
                "weaknesses": intelligence.weaknesses,
                "average_metrics": intelligence.average_metrics,
                "behavioral_patterns": intelligence.behavioral_patterns,
                "recommended_strategies": intelligence.recommended_strategies
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
            
        return True
    
    def _get_access_level(self, accessor: str, target: str) -> AccessLevel:
        """Get current access level"""
        highest = AccessLevel.NONE
        for access in self.access_rights:
            if access.accessor == accessor and access.target == target:
                if access.level.value > highest.value:
                    highest = access.level
        return highest