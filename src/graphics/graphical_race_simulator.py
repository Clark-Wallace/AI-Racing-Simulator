"""
Graphical Race Simulator - Extends intelligent simulator with visual rendering
"""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass

from ..core.intelligent_race_simulator import IntelligentRaceSimulator
from ..core.racing_car import RacingCar
from ..core.race_track import RaceTrack
from ..intelligence.race_intelligence import RacingIntelligence
from .race_renderer import RaceRenderer, GraphicsSettings, PYGAME_AVAILABLE


class GraphicalRaceSimulator(IntelligentRaceSimulator):
    """Race simulator with optional graphical visualization"""
    
    def __init__(self, track: RaceTrack, cars: List[RacingCar], 
                 laps: int = 10, enable_telemetry: bool = True,
                 enable_intelligence: bool = True,
                 enable_graphics: bool = True,
                 graphics_settings: GraphicsSettings = None):
        """Initialize with optional graphics support"""
        super().__init__(track, cars, laps, enable_telemetry, enable_intelligence)
        
        self.enable_graphics = enable_graphics and PYGAME_AVAILABLE
        self.graphics_settings = graphics_settings or GraphicsSettings()
        self.renderer = None
        self.weather = self.track.weather_conditions
        
        if self.enable_graphics:
            try:
                self.renderer = RaceRenderer(self.graphics_settings)
                self.renderer.initialize()
            except Exception as e:
                print(f"Failed to initialize graphics: {e}")
                self.enable_graphics = False
                self.renderer = None
                
    def simulate_race(self) -> Dict:
        """Run race simulation with optional graphics"""
        if not self.enable_graphics or not self.renderer:
            # Fall back to text-based simulation
            return super().simulate_race()
            
        # Initialize race
        for car in self.cars:
            car.reset_for_race()
            
        race_log = []
        lap_times = {car.name: [] for car in self.cars}
        
        # Visual race simulation
        print("\n🏎️  GRAPHICAL RACE STARTING! 🏎️")
        print(f"Track: {self.track.name}")
        print(f"Weather: {self.weather}")
        print("\nPress ESC to exit visualization\n")
        
        # Simulation loop
        current_lap = 1
        time_step = 0.1  # 100ms time steps
        positions = {car.name: 0.0 for car in self.cars}  # Track progress (0-1)
        
        while current_lap <= self.laps and self.renderer.is_running():
            # Update each car
            for i, car in enumerate(self.cars):
                if car.fuel_level > 0:
                    # Get AI decision if intelligence is enabled
                    if self.enable_intelligence and car.name in self.ai_systems:
                        intel = self.ai_systems[car.name]
                        situation = self._analyze_race_situation(car)
                    
                    # Calculate speed based on various factors
                    base_speed = car.get_effective_top_speed() * 0.85  # Average corner speed
                    weather_factor = 0.9 if self.weather == "rain" else 1.0
                    
                    # Apply AI personality effects
                    if car.driver_style.name == "AGGRESSIVE":
                        base_speed *= 1.1
                    elif car.driver_style.name == "CONSERVATIVE":
                        base_speed *= 0.95
                        
                    # Update position
                    distance = (base_speed * weather_factor * time_step) / 3600  # km/h to km/0.1s
                    progress = distance / self.track.total_length
                    positions[car.name] += progress
                    
                    # Check for lap completion
                    if positions[car.name] >= 1.0:
                        positions[car.name] -= 1.0
                        lap_time = 80 + (5 - i) * 2  # Simplified lap time
                        lap_times[car.name].append(lap_time)
                        
                        if len(lap_times[car.name]) >= self.laps:
                            pass  # Race complete for this car
                            
                    # Update car fuel and tires
                    car.consume_fuel(distance, 1.0)
                    car.wear_tires(distance, 1.0)
                    
            # Update car positions based on track progress
            sorted_cars = sorted(self.cars, key=lambda c: -positions[c.name])
            for pos, car in enumerate(sorted_cars):
                car.current_position = pos
                
            # Render frame
            self.renderer.render_frame(self, positions, current_lap, self.laps)
            
            # Check if all cars on next lap
            min_laps = min(len(lap_times[car.name]) for car in self.cars)
            if min_laps >= current_lap:
                current_lap += 1
                
            # Small delay for smooth animation
            time.sleep(time_step)
            
        # Clean up graphics
        if self.renderer:
            self.renderer.cleanup()
            
        # Generate results
        results = self._generate_results(lap_times)
        results["visualization_completed"] = True
        
        return results
        
    def _generate_results(self, lap_times: Dict[str, List[float]]) -> Dict:
        """Generate race results from lap times"""
        finishing_order = []
        
        for car in sorted(self.cars, key=lambda c: c.current_position):
            total_time = sum(lap_times.get(car.name, []))
            finishing_order.append({
                "position": car.current_position + 1,
                "name": car.name,
                "total_time": total_time,
                "laps_completed": len(lap_times.get(car.name, [])),
                "driver_style": car.driver_style.name,
                "final_fuel": max(0, car.fuel_level),
                "tire_wear": car.tire_wear
            })
            
        return {
            "finishing_order": finishing_order,
            "lap_times": lap_times,
            "track": self.track.name,
            "weather": self.weather,
            "total_laps": self.laps
        }