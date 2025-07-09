from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import math
from enum import Enum


class MetricCategory(Enum):
    SPEED = "speed"
    HANDLING = "handling"
    EFFICIENCY = "efficiency"
    STRATEGIC = "strategic"
    TECHNICAL = "technical"


@dataclass
class TelemetrySnapshot:
    """Single point-in-time telemetry data"""
    timestamp: float
    position: int
    speed: float
    acceleration: float
    fuel_level: float
    tire_wear: float
    distance_traveled: float
    lap_number: int
    segment_index: int
    corner_entry_speed: Optional[float] = None
    corner_exit_speed: Optional[float] = None
    brake_application: float = 0.0
    steering_angle: float = 0.0
    
    
@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics for a racing car"""
    car_name: str
    driver_style: str
    
    # Speed Metrics
    top_speed_achieved: float = 0.0
    average_speed: float = 0.0
    speed_consistency: float = 0.0  # Standard deviation
    acceleration_0_to_60: float = float('inf')
    acceleration_0_to_100: float = float('inf')
    burst_speed_capability: float = 0.0  # Max speed increase over 1 second
    
    # Handling Metrics
    cornering_efficiency: float = 0.0  # Avg corner speed / optimal speed
    steering_precision: float = 0.0  # How close to racing line
    stability_rating: float = 0.0  # Speed variance in corners
    drift_coefficient: float = 0.0  # Controlled slides
    braking_control: float = 0.0  # Braking efficiency
    average_corner_speed: float = 0.0
    
    # Efficiency Metrics
    fuel_efficiency: float = 0.0  # Actual km/l during race
    energy_consumption_rate: float = 0.0  # Fuel per lap
    pit_stop_frequency: int = 0
    endurance_rating: float = 0.0  # Performance consistency over time
    resource_optimization: float = 0.0  # Combined fuel/tire management
    
    # Strategic Metrics
    overtaking_ability: float = 0.0  # Successful overtakes per opportunity
    defensive_maneuvers: int = 0
    risk_tolerance: float = 0.0  # Based on speed vs optimal
    adaptability_index: float = 0.0  # Performance in changing conditions
    race_intelligence: float = 0.0  # Strategic decision quality
    
    # Technical Metrics
    response_latency: float = 0.0  # Time to reach target speed
    consistency_variance: float = 0.0  # Lap time variance
    error_rate: float = 0.0  # Mistakes per lap
    recovery_speed: float = 0.0  # Time to recover from incidents
    technical_precision: float = 0.0  # How well follows optimal line
    
    # Lap and sector data
    lap_times: List[float] = field(default_factory=list)
    sector_times: Dict[int, List[float]] = field(default_factory=dict)
    
    # Telemetry snapshots
    telemetry_data: List[TelemetrySnapshot] = field(default_factory=list)
    
    # Event counters
    total_overtakes: int = 0
    times_overtaken: int = 0
    corners_completed: int = 0
    perfect_corners: int = 0  # Within 5% of optimal speed
    incidents: int = 0
    
    
class TelemetrySystem:
    """Collects and analyzes racing telemetry data"""
    
    def __init__(self):
        self.active_sessions: Dict[str, PerformanceMetrics] = {}
        self.completed_sessions: List[PerformanceMetrics] = []
        self.sampling_rate = 0.1  # seconds between snapshots
        
    def start_session(self, car_name: str, driver_style: str) -> PerformanceMetrics:
        """Initialize telemetry collection for a car"""
        metrics = PerformanceMetrics(car_name, driver_style)
        self.active_sessions[car_name] = metrics
        return metrics
        
    def record_snapshot(self, car_name: str, snapshot: TelemetrySnapshot):
        """Record a telemetry snapshot"""
        if car_name in self.active_sessions:
            metrics = self.active_sessions[car_name]
            metrics.telemetry_data.append(snapshot)
            
            # Update real-time metrics
            self._update_speed_metrics(metrics, snapshot)
            self._update_handling_metrics(metrics, snapshot)
            
    def _update_speed_metrics(self, metrics: PerformanceMetrics, snapshot: TelemetrySnapshot):
        """Update speed-related metrics"""
        # Track top speed
        if snapshot.speed > metrics.top_speed_achieved:
            metrics.top_speed_achieved = snapshot.speed
            
        # Track acceleration times
        if len(metrics.telemetry_data) > 1:
            prev = metrics.telemetry_data[-2]
            if prev.speed < 60 and snapshot.speed >= 60:
                # Find when we started from near 0
                for i in range(len(metrics.telemetry_data) - 2, -1, -1):
                    if metrics.telemetry_data[i].speed < 5:
                        time_to_60 = snapshot.timestamp - metrics.telemetry_data[i].timestamp
                        metrics.acceleration_0_to_60 = min(metrics.acceleration_0_to_60, time_to_60)
                        break
                        
            # Burst speed capability
            if snapshot.timestamp - prev.timestamp <= 1.0:
                speed_increase = snapshot.speed - prev.speed
                metrics.burst_speed_capability = max(metrics.burst_speed_capability, speed_increase)
                
    def _update_handling_metrics(self, metrics: PerformanceMetrics, snapshot: TelemetrySnapshot):
        """Update handling-related metrics"""
        if snapshot.corner_entry_speed is not None and snapshot.corner_exit_speed is not None:
            metrics.corners_completed += 1
            avg_corner_speed = (snapshot.corner_entry_speed + snapshot.corner_exit_speed) / 2
            
            # Update average corner speed
            if metrics.average_corner_speed == 0:
                metrics.average_corner_speed = avg_corner_speed
            else:
                metrics.average_corner_speed = (
                    metrics.average_corner_speed * (metrics.corners_completed - 1) + avg_corner_speed
                ) / metrics.corners_completed
                
    def record_lap_complete(self, car_name: str, lap_time: float, lap_number: int):
        """Record lap completion"""
        if car_name in self.active_sessions:
            metrics = self.active_sessions[car_name]
            metrics.lap_times.append(lap_time)
            
    def record_overtake(self, overtaker: str, overtaken: str):
        """Record an overtaking maneuver"""
        if overtaker in self.active_sessions:
            self.active_sessions[overtaker].total_overtakes += 1
        if overtaken in self.active_sessions:
            self.active_sessions[overtaken].times_overtaken += 1
            
    def record_incident(self, car_name: str, incident_type: str):
        """Record a racing incident"""
        if car_name in self.active_sessions:
            self.active_sessions[car_name].incidents += 1
            
    def finalize_session(self, car_name: str, race_time: float, 
                        final_position: int, total_fuel_used: float):
        """Finalize telemetry collection and calculate final metrics"""
        if car_name not in self.active_sessions:
            return None
            
        metrics = self.active_sessions[car_name]
        
        # Calculate aggregate metrics
        self._calculate_final_speed_metrics(metrics)
        self._calculate_final_handling_metrics(metrics)
        self._calculate_efficiency_metrics(metrics, total_fuel_used)
        self._calculate_strategic_metrics(metrics, final_position)
        self._calculate_technical_metrics(metrics)
        
        # Move to completed sessions
        self.completed_sessions.append(metrics)
        del self.active_sessions[car_name]
        
        return metrics
        
    def _calculate_final_speed_metrics(self, metrics: PerformanceMetrics):
        """Calculate final speed metrics"""
        if not metrics.telemetry_data:
            return
            
        speeds = [snapshot.speed for snapshot in metrics.telemetry_data]
        metrics.average_speed = sum(speeds) / len(speeds)
        
        # Speed consistency (standard deviation)
        variance = sum((s - metrics.average_speed) ** 2 for s in speeds) / len(speeds)
        metrics.speed_consistency = math.sqrt(variance)
        
        # Find 0-100 acceleration
        for i, snapshot in enumerate(metrics.telemetry_data):
            if snapshot.speed >= 100:
                # Find when we were near 0
                for j in range(i, -1, -1):
                    if metrics.telemetry_data[j].speed < 5:
                        metrics.acceleration_0_to_100 = snapshot.timestamp - metrics.telemetry_data[j].timestamp
                        break
                break
                
    def _calculate_final_handling_metrics(self, metrics: PerformanceMetrics):
        """Calculate final handling metrics"""
        corner_speeds = []
        for snapshot in metrics.telemetry_data:
            if snapshot.corner_entry_speed is not None and snapshot.corner_exit_speed is not None:
                corner_speeds.append((snapshot.corner_entry_speed + snapshot.corner_exit_speed) / 2)
                
        if corner_speeds:
            # Stability in corners
            corner_variance = sum((s - metrics.average_corner_speed) ** 2 for s in corner_speeds) / len(corner_speeds)
            metrics.stability_rating = 1.0 / (1.0 + math.sqrt(corner_variance) / 10)
            
        # Cornering efficiency (simplified - would need optimal speeds from track)
        metrics.cornering_efficiency = min(1.0, metrics.average_corner_speed / 150)  # Assume 150 km/h is good corner speed
        
        # Technical precision based on consistency
        if metrics.lap_times:
            lap_variance = sum((t - sum(metrics.lap_times)/len(metrics.lap_times)) ** 2 for t in metrics.lap_times) / len(metrics.lap_times)
            metrics.technical_precision = 1.0 / (1.0 + math.sqrt(lap_variance))
            
    def _calculate_efficiency_metrics(self, metrics: PerformanceMetrics, total_fuel_used: float):
        """Calculate efficiency metrics"""
        if metrics.telemetry_data:
            total_distance = metrics.telemetry_data[-1].distance_traveled / 1000  # Convert to km
            if total_distance > 0 and total_fuel_used > 0:
                # Actual fuel efficiency during race
                metrics.fuel_efficiency = total_distance / (total_fuel_used * 0.6)  # Convert percentage to liters
                
                # Energy consumption per lap
                if metrics.lap_times:
                    metrics.energy_consumption_rate = total_fuel_used / len(metrics.lap_times)
                    
            # Endurance rating based on performance consistency
            if len(metrics.lap_times) > 2:
                first_half_avg = sum(metrics.lap_times[:len(metrics.lap_times)//2]) / (len(metrics.lap_times)//2)
                second_half_avg = sum(metrics.lap_times[len(metrics.lap_times)//2:]) / (len(metrics.lap_times) - len(metrics.lap_times)//2)
                degradation = (second_half_avg - first_half_avg) / first_half_avg
                metrics.endurance_rating = max(0, 1.0 - degradation * 10)
                
    def _calculate_strategic_metrics(self, metrics: PerformanceMetrics, final_position: int):
        """Calculate strategic metrics"""
        # Overtaking ability
        opportunities = metrics.times_overtaken + metrics.total_overtakes
        if opportunities > 0:
            metrics.overtaking_ability = metrics.total_overtakes / opportunities
            
        # Risk tolerance based on speed relative to average
        if metrics.average_speed > 0:
            speed_variance_ratio = metrics.speed_consistency / metrics.average_speed
            metrics.risk_tolerance = 1.0 - min(1.0, speed_variance_ratio)
            
        # Race intelligence (simple heuristic based on position vs incidents)
        if metrics.incidents == 0:
            metrics.race_intelligence = 1.0 - (final_position - 1) / 4  # Assumes 5 cars
        else:
            metrics.race_intelligence = max(0, (1.0 - (final_position - 1) / 4) - metrics.incidents * 0.2)
            
    def _calculate_technical_metrics(self, metrics: PerformanceMetrics):
        """Calculate technical metrics"""
        # Consistency variance already calculated
        if metrics.lap_times:
            avg_lap = sum(metrics.lap_times) / len(metrics.lap_times)
            variance = sum((t - avg_lap) ** 2 for t in metrics.lap_times) / len(metrics.lap_times)
            metrics.consistency_variance = math.sqrt(variance)
            
        # Error rate
        if metrics.lap_times:
            metrics.error_rate = metrics.incidents / len(metrics.lap_times)
            
        # Response latency (average time to reach 90% of target speed changes)
        # This is simplified - would need more detailed tracking in practice
        metrics.response_latency = 1.5  # Placeholder
        
        # Recovery speed (based on incidents and final performance)
        if metrics.incidents > 0:
            metrics.recovery_speed = metrics.race_intelligence / metrics.incidents
        else:
            metrics.recovery_speed = 1.0
            
    def get_metrics_summary(self, car_name: str) -> Dict:
        """Get a summary of key metrics for a car"""
        metrics = None
        for m in self.completed_sessions:
            if m.car_name == car_name:
                metrics = m
                break
                
        if not metrics and car_name in self.active_sessions:
            metrics = self.active_sessions[car_name]
            
        if not metrics:
            return {}
            
        return {
            "car_name": metrics.car_name,
            "driver_style": metrics.driver_style,
            "speed": {
                "top_speed": metrics.top_speed_achieved,
                "average": metrics.average_speed,
                "consistency": metrics.speed_consistency,
                "0_to_100": metrics.acceleration_0_to_100
            },
            "handling": {
                "cornering_efficiency": metrics.cornering_efficiency,
                "stability": metrics.stability_rating,
                "technical_precision": metrics.technical_precision,
                "avg_corner_speed": metrics.average_corner_speed
            },
            "efficiency": {
                "fuel_efficiency": metrics.fuel_efficiency,
                "endurance": metrics.endurance_rating,
                "energy_per_lap": metrics.energy_consumption_rate
            },
            "strategic": {
                "overtaking": metrics.overtaking_ability,
                "risk_tolerance": metrics.risk_tolerance,
                "race_intelligence": metrics.race_intelligence,
                "total_overtakes": metrics.total_overtakes
            },
            "technical": {
                "consistency": metrics.consistency_variance,
                "error_rate": metrics.error_rate,
                "recovery": metrics.recovery_speed
            }
        }
        
    def export_telemetry(self, car_name: str, filename: str):
        """Export telemetry data to JSON file"""
        summary = self.get_metrics_summary(car_name)
        if summary:
            with open(filename, 'w') as f:
                json.dump(summary, f, indent=2)
                
    def compare_metrics(self, car1: str, car2: str) -> Dict:
        """Compare metrics between two cars"""
        metrics1 = self.get_metrics_summary(car1)
        metrics2 = self.get_metrics_summary(car2)
        
        if not metrics1 or not metrics2:
            return {}
            
        comparison = {
            "cars": [car1, car2],
            "advantages": {
                car1: [],
                car2: []
            }
        }
        
        # Compare each category
        categories = ["speed", "handling", "efficiency", "strategic", "technical"]
        for category in categories:
            if category in metrics1 and category in metrics2:
                for metric, value1 in metrics1[category].items():
                    value2 = metrics2[category].get(metric, 0)
                    if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
                        if value1 > value2 * 1.1:  # 10% advantage threshold
                            comparison["advantages"][car1].append(f"{category}.{metric}")
                        elif value2 > value1 * 1.1:
                            comparison["advantages"][car2].append(f"{category}.{metric}")
                            
        return comparison