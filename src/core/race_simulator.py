from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import random
import math
from racing_car import RacingCar, DriverStyle
from race_track import RaceTrack, TrackSegment
from telemetry import TelemetrySystem, TelemetrySnapshot


@dataclass
class RaceEvent:
    """Represents events that happen during a race"""
    time: float
    event_type: str
    car_name: str
    details: str


class RaceSimulator:
    def __init__(self, track: RaceTrack, cars: List[RacingCar], laps: int = 10, enable_telemetry: bool = True):
        self.track = track
        self.cars = cars
        self.laps = laps
        self.current_positions = {car.name: i for i, car in enumerate(cars)}
        self.lap_times = {car.name: [] for car in cars}
        self.events = []
        self.time_step = 0.1  # seconds
        self.race_time = 0.0
        self.finished_cars = []
        
        # Initialize telemetry system
        self.enable_telemetry = enable_telemetry
        self.telemetry = TelemetrySystem() if enable_telemetry else None
        self.car_fuel_at_start = {car.name: car.fuel_level for car in cars}
        
    def simulate_race(self) -> Dict:
        """Run the complete race simulation"""
        print(f"\n🏁 RACE START at {self.track.name} - {self.laps} laps")
        print(f"Track Type: {self.track.track_type.value}")
        print(f"Weather: {self.track.weather_conditions}")
        print(f"Track Length: {self.track.total_length:.2f} km\n")
        
        # Reset all cars and initialize telemetry
        for car in self.cars:
            car.reset_for_race()
            car.current_position = self.current_positions[car.name]
            if self.telemetry:
                self.telemetry.start_session(car.name, car.driver_style.value)
        
        # Race loop
        while len(self.finished_cars) < len(self.cars):
            self.race_time += self.time_step
            self._simulate_time_step()
            
            # Print updates every 10 seconds
            if int(self.race_time) % 10 == 0 and int(self.race_time * 10) % 100 == 0:
                self._print_race_update()
        
        return self._compile_race_results()
    
    def _simulate_time_step(self):
        """Simulate one time step of the race"""
        # Update each car
        for car in self.cars:
            if car.name in self.finished_cars:
                continue
                
            # Get current segment
            segment_index, segment_position = self._get_car_segment(car)
            segment = self.track.segments[segment_index]
            
            # Calculate target speed for segment
            weather_mod = self.track.get_weather_modifiers()
            optimal_speed = segment.get_optimal_speed(car.get_effective_handling())
            optimal_speed *= weather_mod["speed"]
            
            # Apply driver style decisions
            target_speed = self._apply_driver_style_decision(car, optimal_speed, segment)
            
            # Update car physics
            previous_speed = car.current_speed
            car.accelerate(target_speed, self.time_step)
            
            # Calculate distance traveled
            avg_speed = (previous_speed + car.current_speed) / 2
            distance = (avg_speed / 3.6) * self.time_step  # Convert km/h to m/s
            
            # Update car position
            car.distance_traveled += distance
            
            # Record telemetry snapshot
            if self.telemetry and int(self.race_time * 10) % int(self.telemetry.sampling_rate * 10) == 0:
                corner_entry = None
                corner_exit = None
                if not segment.is_straight:
                    # Track corner entry and exit speeds
                    corner_entry = car.current_speed if segment_position < segment.length * 0.5 else None
                    corner_exit = car.current_speed if segment_position > segment.length * 0.5 else None
                        
                snapshot = TelemetrySnapshot(
                    timestamp=self.race_time,
                    position=self.current_positions[car.name] + 1,
                    speed=car.current_speed,
                    acceleration=(car.current_speed - previous_speed) / self.time_step,
                    fuel_level=car.fuel_level,
                    tire_wear=car.tire_wear,
                    distance_traveled=car.distance_traveled,
                    lap_number=car.current_lap,
                    segment_index=segment_index,
                    corner_entry_speed=corner_entry,
                    corner_exit_speed=corner_exit,
                    brake_application=max(0, (previous_speed - car.current_speed) / previous_speed) if previous_speed > 0 else 0
                )
                self.telemetry.record_snapshot(car.name, snapshot)
            
            # Update fuel and tires
            aggressive_factor = 1.0 if segment.is_straight else 1.3
            car.consume_fuel(distance / 1000, aggressive_factor)
            
            cornering_stress = 1.0 if segment.is_straight else 2.0
            car.wear_tires(distance / 1000, cornering_stress)
            
            # Check for events
            self._check_for_events(car, segment)
            
            # Update lap count
            if car.distance_traveled >= self.track.total_length * 1000 * car.current_lap + self.track.total_length * 1000:
                car.current_lap += 1
                lap_time = self.race_time - sum(self.lap_times[car.name])
                self.lap_times[car.name].append(lap_time)
                
                self.events.append(RaceEvent(
                    self.race_time,
                    "LAP_COMPLETE",
                    car.name,
                    f"Lap {car.current_lap} completed in {lap_time:.2f}s"
                ))
                
                if self.telemetry:
                    self.telemetry.record_lap_complete(car.name, lap_time, car.current_lap)
                
                if car.current_lap >= self.laps:
                    self.finished_cars.append(car.name)
                    car.total_race_time = self.race_time
                    self.events.append(RaceEvent(
                        self.race_time,
                        "FINISH",
                        car.name,
                        f"Finished in position {len(self.finished_cars)}"
                    ))
        
        # Update positions based on distance
        self._update_positions()
    
    def _get_car_segment(self, car: RacingCar) -> Tuple[int, float]:
        """Determine which track segment the car is currently on"""
        distance_in_lap = car.distance_traveled % (self.track.total_length * 1000)
        
        cumulative_distance = 0
        for i, segment in enumerate(self.track.segments):
            if cumulative_distance + segment.length > distance_in_lap:
                position_in_segment = distance_in_lap - cumulative_distance
                return i, position_in_segment
            cumulative_distance += segment.length
        
        # Should not reach here, but return last segment if it does
        return len(self.track.segments) - 1, 0
    
    def _apply_driver_style_decision(self, car: RacingCar, optimal_speed: float, segment: TrackSegment) -> float:
        """Apply driver personality to speed decisions"""
        style_mod = car.get_style_modifiers()
        risk_factor = style_mod["risk_factor"]
        
        if car.driver_style == DriverStyle.AGGRESSIVE:
            # Push beyond optimal, especially on straights
            if segment.is_straight:
                return min(optimal_speed * 1.1, car.get_effective_top_speed())
            else:
                return optimal_speed * (0.95 + risk_factor * 0.05)
                
        elif car.driver_style == DriverStyle.CONSERVATIVE:
            # Stay safely below optimal
            return optimal_speed * 0.92
            
        elif car.driver_style == DriverStyle.TECHNICAL:
            # Perfect optimal speed in corners, push on straights
            if segment.is_straight:
                return min(optimal_speed * 1.05, car.get_effective_top_speed())
            else:
                return optimal_speed
                
        elif car.driver_style == DriverStyle.CHAOTIC:
            # Random variations
            variation = random.uniform(0.85, 1.15)
            return optimal_speed * variation
            
        else:  # BALANCED
            # Slight push beyond optimal
            return optimal_speed * 1.02
    
    def _check_for_events(self, car: RacingCar, segment: TrackSegment):
        """Check for race events (crashes, mechanical issues, etc.)"""
        style_mod = car.get_style_modifiers()
        risk_factor = style_mod["risk_factor"]
        
        # Check for crashes (more likely in corners with high risk)
        if not segment.is_straight:
            crash_chance = (risk_factor - 1.0) * 0.001 * (100 - car.tire_wear) / 100
            if car.current_speed > segment.get_optimal_speed(car.get_effective_handling()) * 1.2:
                crash_chance *= 3
                
            if random.random() < crash_chance:
                car.current_speed = 0
                self.events.append(RaceEvent(
                    self.race_time,
                    "CRASH",
                    car.name,
                    f"Spun out in corner! Lost time recovering."
                ))
                if self.telemetry:
                    self.telemetry.record_incident(car.name, "CRASH")
        
        # Check for fuel issues
        if car.fuel_level < 5:
            self.events.append(RaceEvent(
                self.race_time,
                "LOW_FUEL",
                car.name,
                f"Running on fumes! Speed limited."
            ))
            car.current_speed = min(car.current_speed, 150)
    
    def _update_positions(self):
        """Update race positions based on distance traveled"""
        # Sort cars by distance traveled (accounting for laps)
        car_distances = [(car.name, car.distance_traveled) for car in self.cars]
        car_distances.sort(key=lambda x: x[1], reverse=True)
        
        for position, (car_name, _) in enumerate(car_distances):
            old_position = self.current_positions[car_name]
            new_position = position
            
            if old_position != new_position and car_name not in self.finished_cars:
                self.current_positions[car_name] = new_position
                
                # Find who was overtaken
                for other_name, other_pos in self.current_positions.items():
                    if other_pos == old_position and other_name != car_name:
                        self.events.append(RaceEvent(
                            self.race_time,
                            "OVERTAKE",
                            car_name,
                            f"Overtook {other_name} for position {new_position + 1}"
                        ))
                        if self.telemetry:
                            self.telemetry.record_overtake(car_name, other_name)
                        break
    
    def _print_race_update(self):
        """Print current race standings"""
        print(f"\n⏱️  Race Time: {self.race_time:.1f}s")
        
        # Sort by position
        sorted_cars = sorted(self.cars, key=lambda c: self.current_positions[c.name])
        
        for i, car in enumerate(sorted_cars):
            if car.name in self.finished_cars:
                status = "FINISHED"
            else:
                status = f"Lap {car.current_lap + 1}/{self.laps}"
            
            print(f"{i+1}. {car.name:15} - {status:12} | "
                  f"Speed: {car.current_speed:3.0f} km/h | "
                  f"Fuel: {car.fuel_level:3.0f}% | "
                  f"Tires: {100-car.tire_wear:3.0f}%")
    
    def _compile_race_results(self) -> Dict:
        """Compile final race results and statistics"""
        # Finalize telemetry for all cars
        if self.telemetry:
            for i, car_name in enumerate(self.finished_cars):
                car = next(c for c in self.cars if c.name == car_name)
                fuel_used = self.car_fuel_at_start[car_name] - car.fuel_level
                self.telemetry.finalize_session(car_name, car.total_race_time, i + 1, fuel_used)
        
        results = {
            "track": self.track.name,
            "weather": self.track.weather_conditions,
            "laps": self.laps,
            "total_time": self.race_time,
            "positions": {},
            "lap_times": self.lap_times,
            "fastest_lap": {},
            "events": self.events,
            "telemetry_available": self.telemetry is not None
        }
        
        # Final positions
        for i, car_name in enumerate(self.finished_cars):
            car = next(c for c in self.cars if c.name == car_name)
            results["positions"][i + 1] = {
                "name": car_name,
                "driver_style": car.driver_style.value,
                "total_time": car.total_race_time,
                "avg_lap_time": sum(self.lap_times[car_name]) / len(self.lap_times[car_name]),
                "fuel_remaining": car.fuel_level,
                "tire_wear": car.tire_wear
            }
        
        # Find fastest lap
        fastest_time = float('inf')
        fastest_driver = None
        for car_name, times in self.lap_times.items():
            if times and min(times) < fastest_time:
                fastest_time = min(times)
                fastest_driver = car_name
        
        results["fastest_lap"] = {
            "driver": fastest_driver,
            "time": fastest_time
        }
        
        return results
    
    def print_race_summary(self, results: Dict):
        """Print a formatted race summary"""
        print("\n" + "="*60)
        print("🏁 RACE RESULTS 🏁")
        print("="*60)
        print(f"Track: {results['track']}")
        print(f"Weather: {results['weather']}")
        print(f"Total Race Time: {results['total_time']:.2f}s\n")
        
        print("FINAL POSITIONS:")
        for position, data in results["positions"].items():
            print(f"{position}. {data['name']:15} ({data['driver_style']:12}) - "
                  f"Time: {data['total_time']:.2f}s | "
                  f"Avg Lap: {data['avg_lap_time']:.2f}s | "
                  f"Fuel: {data['fuel_remaining']:.1f}% | "
                  f"Tires: {100-data['tire_wear']:.1f}%")
        
        print(f"\n🏆 FASTEST LAP: {results['fastest_lap']['driver']} - "
              f"{results['fastest_lap']['time']:.2f}s")
        
        # Print notable events
        print("\nNOTABLE EVENTS:")
        for event in results["events"][-10:]:  # Last 10 events
            if event.event_type in ["OVERTAKE", "CRASH", "FINISH"]:
                print(f"  {event.time:.1f}s - {event.car_name}: {event.details}")
                
    def get_telemetry_summary(self, car_name: str) -> Dict:
        """Get telemetry summary for a specific car"""
        if self.telemetry:
            return self.telemetry.get_metrics_summary(car_name)
        return {}
        
    def export_telemetry(self, car_name: str, filename: str):
        """Export telemetry data for a car to file"""
        if self.telemetry:
            self.telemetry.export_telemetry(car_name, filename)
            
    def compare_telemetry(self, car1: str, car2: str) -> Dict:
        """Compare telemetry between two cars"""
        if self.telemetry:
            return self.telemetry.compare_metrics(car1, car2)
        return {}