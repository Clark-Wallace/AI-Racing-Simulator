"""
LLM Race Simulator - Handles races with AI language model drivers
"""

import asyncio
import time
from typing import List, Dict, Optional
from dataclasses import dataclass

from ..graphics.graphical_race_simulator import GraphicalRaceSimulator
from ..core.race_track import RaceTrack
from ..core.racing_car import RacingCar
from ..core.racing_powerups import PowerUpManager, PowerUpType
from ..core.racing_collisions import CollisionDetector
from ..core.racing_weapons import WeaponsManager
from .llm_racing_driver import LLMDriver, LLMAction, create_llm_drivers
from ..graphics.race_renderer import GraphicsSettings


class LLMRaceSimulator(GraphicalRaceSimulator):
    """Race simulator for LLM-powered drivers"""
    
    def __init__(self, track: RaceTrack, llm_drivers: List[LLMDriver],
                 laps: int = 10, enable_graphics: bool = True,
                 graphics_settings: GraphicsSettings = None):
        """Initialize with LLM drivers"""
        # Extract cars from LLM drivers
        cars = [driver.car for driver in llm_drivers]
        
        # Initialize parent with cars
        super().__init__(
            track=track,
            cars=cars,
            laps=laps,
            enable_telemetry=True,
            enable_intelligence=False,  # Disable rule-based AI
            enable_graphics=enable_graphics,
            graphics_settings=graphics_settings
        )
        
        self.llm_drivers = {driver.car.name: driver for driver in llm_drivers}
        self.race_events = []
        
        # Initialize Mario Kart-style systems
        self.powerup_manager = PowerUpManager()
        self.collision_detector = CollisionDetector()
        self.power_up_timer = 0  # Timer for power-up distribution
        
        # Initialize weapons system
        self.weapons_manager = WeaponsManager()
        
        # Initialize power-up pickups on track
        self.powerup_manager.initialize_track_pickups(track.total_length, num_pickups=8)
        
        # Initialize car inventories and weapons
        car_names = [car.name for car in cars]
        self.powerup_manager.initialize_cars(car_names)
        self.weapons_manager.initialize_cars(car_names)
    
    def _safe_analyze_powerup_strategy(self, car, gap_ahead, gap_behind):
        """Safely analyze power-up strategy with error handling"""
        try:
            if car is None or not hasattr(car, 'name') or not hasattr(car, 'current_position'):
                return {"recommendation": "none", "reasoning": "Invalid car"}
            
            strategy = self.powerup_manager.analyze_power_up_strategy(
                car.name, car.current_position, len(self.cars), 
                {"ahead": gap_ahead, "behind": gap_behind}
            )
            return strategy if strategy is not None else {"recommendation": "none", "reasoning": "No strategy"}
        except Exception as e:
            print(f"⚠️ Power-up strategy error for {getattr(car, 'name', 'unknown')}: {e}")
            return {"recommendation": "none", "reasoning": "Strategy error"}
        
    def simulate_race(self) -> Dict:
        """Run race simulation with LLM decision making"""
        if not self.enable_graphics or not self.renderer:
            # Fall back to async text simulation
            try:
                # Try to get existing loop
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is running, create a task
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(self._run_async_race)
                        return future.result()
                else:
                    return loop.run_until_complete(self.simulate_race_async())
            except RuntimeError:
                # No event loop exists, create one
                return asyncio.run(self.simulate_race_async())
        
        # Visual race simulation with LLM decisions
        print("\n🤖 LLM RACE STARTING! (Visual Mode) 🤖")
        print(f"Track: {self.track.name}")
        print(f"Weather: {self.weather}")
        print("\nLLM Drivers:")
        for driver in self.llm_drivers.values():
            print(f"  • {driver.name} ({driver.model_config['model'].split('/')[-1]})")
        print("\nPress ESC to exit visualization\n")
        
        # Initialize race
        for car in self.cars:
            car.reset_for_race()
            
        race_log = []
        lap_times = {}
        try:
            for car in self.cars:
                if car and hasattr(car, 'name') and car.name:
                    lap_times[car.name] = []
        except Exception as e:
            print(f"🚨 Error initializing lap_times: {e}")
            lap_times = {}
        
        # Simulation loop
        current_lap = 1
        time_step = 0.1  # 100ms time steps for smoother animation
        positions = {car.name: 0.0 for car in self.cars}
        laps_completed = {car.name: 0 for car in self.cars}  # Track laps per car
        decision_counter = 0  # Only make LLM decisions every few frames
        
        # Create futures for async LLM calls
        import concurrent.futures
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        pending_futures = {}  # Track pending LLM decisions
        
        while current_lap <= self.laps and self.renderer.is_running():
            # Get LLM decisions only every 30 frames (0.5 second intervals at 60 FPS)
            decision_counter += 1
            if decision_counter >= 30:  # Make decisions every 0.5 seconds
                decision_counter = 0
                
                for i, car in enumerate(self.cars):
                    if not getattr(car, 'has_mechanical_failure', False) and car.fuel_level > 0:
                        driver = self.llm_drivers[car.name]
                        
                        # Calculate gaps (considering laps)
                        gap_ahead = 100  # Default
                        gap_behind = 100
                        
                        # Sort cars by actual race position for correct gap calculation
                        cars_by_position = sorted(self.cars, 
                            key=lambda c: -(laps_completed.get(c.name, 0) + positions.get(c.name, 0)))
                        car_index = cars_by_position.index(car)
                        
                        if car_index > 0:
                            ahead_car = cars_by_position[car_index - 1]
                            # Calculate distance considering laps
                            ahead_total = laps_completed.get(ahead_car.name, 0) + positions.get(ahead_car.name, 0)
                            car_total = laps_completed.get(car.name, 0) + positions.get(car.name, 0)
                            gap_ahead = (ahead_total - car_total) * self.track.total_length * 1000
                        
                        if car_index < len(cars_by_position) - 1:
                            behind_car = cars_by_position[car_index + 1]
                            car_total = laps_completed.get(car.name, 0) + positions.get(car.name, 0)
                            behind_total = laps_completed.get(behind_car.name, 0) + positions.get(behind_car.name, 0)
                            gap_behind = (car_total - behind_total) * self.track.total_length * 1000
                        
                        # Prepare enhanced race state with power-ups and collision info
                        car_positions_for_collision = {c.name: positions[c.name] for c in self.cars}
                        car_speeds_for_collision = {c.name: c.current_speed for c in self.cars}
                        
                        try:
                            collision_risk = self.collision_detector.get_collision_risk(
                                car.name, car_positions_for_collision, car_speeds_for_collision, 
                                "straight" if i % 2 == 0 else "corner"
                            )
                            if collision_risk is None:
                                collision_risk = {"risk_level": "none", "risk_factor": 0.0}
                        except Exception as e:
                            print(f"⚠️ Collision risk error for {car.name}: {e}")
                            collision_risk = {"risk_level": "none", "risk_factor": 0.0}
                        
                        # Get weapon information
                        ammo_remaining = self.weapons_manager.get_ammo_status(car.name)
                        target_ahead = self.weapons_manager.get_car_ahead(
                            car.name, positions, laps_completed
                        )
                        can_fire = self.weapons_manager.car_weapons[car.name].can_fire(
                            time.time()
                        ) if car.name in self.weapons_manager.car_weapons else False
                        
                        race_state = {
                            "total_cars": len(self.cars),
                            "current_lap": current_lap,
                            "total_laps": self.laps,
                            "gap_ahead": gap_ahead,
                            "gap_behind": gap_behind,
                            "track_segment": "straight" if i % 2 == 0 else "corner",
                            "weather": self.weather,
                            "power_ups": self.powerup_manager.get_inventory_status(car.name),
                            "collision_risk": collision_risk,
                            "power_up_strategy": self._safe_analyze_powerup_strategy(
                                car, gap_ahead, gap_behind
                            ),
                            "ammo_remaining": ammo_remaining,
                            "can_fire": can_fire,
                            "target_ahead": target_ahead[0] if target_ahead else None,
                            "target_distance": target_ahead[1] * self.track.total_length * 1000 if target_ahead else 999
                        }
                        
                        # Debug weapon info
                        if target_ahead and can_fire and ammo_remaining > 0:
                            target_distance_m = target_ahead[1] * self.track.total_length * 1000
                            if target_distance_m <= 200:
                                print(f"🎯 {car.name} SHOULD FIRE at {target_ahead[0]} ({target_distance_m:.0f}m away) - Ammo: {ammo_remaining}")
                        
                        # Submit LLM decision request (non-blocking)
                        if car.name not in pending_futures:
                            future = executor.submit(
                                asyncio.run, 
                                driver.make_decision(race_state)
                            )
                            pending_futures[car.name] = future
            
            # Check for completed LLM decisions (non-blocking)
            completed_futures = []
            for car_name, future in pending_futures.items():
                if future.done():
                    try:
                        decision = future.result()
                        # Ensure decision is valid
                        if decision is None:
                            decision = {"action": "WAIT", "confidence": 0.5, "reasoning": "None response"}
                        elif not isinstance(decision, dict):
                            decision = {"action": "WAIT", "confidence": 0.5, "reasoning": "Invalid response type"}
                        elif "action" not in decision:
                            decision["action"] = "WAIT"
                        elif decision["action"] is None:
                            decision["action"] = "WAIT"
                        
                        if 'decisions' not in locals():
                            decisions = {}
                        decisions[car_name] = decision
                        completed_futures.append(car_name)
                    except Exception as e:
                        print(f"🚨 Error with {car_name}: {e}")
                        if 'decisions' not in locals():
                            decisions = {}
                        decisions[car_name] = {"action": "WAIT", "confidence": 0.3, "reasoning": f"Error: {str(e)[:20]}"}
                        completed_futures.append(car_name)
            
            # Remove completed futures
            for car_name in completed_futures:
                del pending_futures[car_name]
            
            # Initialize decisions if not set
            if 'decisions' not in locals():
                decisions = {car.name: {"action": "WAIT", "confidence": 0.5, "reasoning": "Starting"} for car in self.cars}
            
            # Check for collisions before moving cars
            car_positions_for_collision = {c.name: positions[c.name] for c in self.cars}
            car_speeds_for_collision = {c.name: c.current_speed for c in self.cars}
            track_section = "corner" if decision_counter % 3 == 0 else "straight"
            
            collisions = self.collision_detector.check_for_collisions(
                car_positions_for_collision, car_speeds_for_collision, track_section
            )
            
            # Apply collision effects (use a copy to avoid modifying the original)
            collision_speeds = car_speeds_for_collision.copy()
            if collisions:
                for collision in collisions:
                    collision_speeds = self.collision_detector.apply_collision_effects(
                        collision, collision_speeds
                    )
                    print(f"💥 COLLISION! {collision.primary_car} vs {collision.secondary_car} - {collision.collision_type}")
            
            # Apply machine gun hit effects
            for hit in self.weapons_manager.get_active_hits():
                collision_speeds = self.weapons_manager.apply_hit_effect(collision_speeds, hit)
            
            # Apply decisions and update positions
            for i, car in enumerate(self.cars):
                try:
                    if not car or not hasattr(car, 'name') or not decisions:
                        continue
                    
                    if car.name not in decisions or decisions[car.name] is None:
                        continue
                    driver = self.llm_drivers[car.name]
                    decision = decisions[car.name]
                    
                    # Ensure decision is a dict
                    if not isinstance(decision, dict):
                        decision = {"action": "WAIT", "confidence": 0.5, "reasoning": "Invalid decision"}
                    
                    # Handle power-up usage (also check if USE_POWERUP action was chosen)
                    if (decision.get("use_powerup", False) or 
                        decision.get("powerup_used", False) or
                        decision.get("action") == "USE_POWERUP"):
                        try:
                            powerup_result = self.powerup_manager.use_power_up(car.name, 0)  # Use first item
                            if powerup_result and isinstance(powerup_result, dict) and powerup_result.get("success"):
                                power_up_name = powerup_result.get('power_up', 'unknown')
                                print(f"\n⚡⚡⚡ {car.name} USED {power_up_name.upper()}! ⚡⚡⚡")
                                
                                # Add visual effects based on power-up type
                                if "TURBO" in power_up_name.upper() or "NITRO" in power_up_name.upper():
                                    print(f"💨 {car.name} is BOOSTING!")
                                elif "SHELL" in power_up_name.upper():
                                    print(f"🎯 {car.name} fired a {power_up_name}!")
                                elif "SHIELD" in power_up_name.upper():
                                    print(f"🛡️ {car.name} activated protection!")
                                elif "LIGHTNING" in power_up_name.upper():
                                    print(f"⚡ LIGHTNING STRIKE! All cars ahead slowed!")
                        except Exception as e:
                            print(f"⚠️ Power-up error for {car.name}: {e}")
                    
                    # Handle machine gun firing
                    try:
                        action_str = decision.get("action", "WAIT")
                        if action_str is None:
                            action_str = "WAIT"
                        action = LLMAction(str(action_str).upper())
                    except (ValueError, AttributeError) as e:
                        print(f"⚠️ Action error for {car.name}: {e}, using WAIT")
                        action = LLMAction.WAIT
                    
                    # Check if car wants to fire machine gun
                    if action in [LLMAction.FIRE, LLMAction.SHOOT] or decision.get("fire_weapon", False):
                        if self.weapons_manager.attempt_fire(car.name, time.time()):
                            # Find target ahead
                            target_info = self.weapons_manager.get_car_ahead(
                                car.name, positions, laps_completed
                            )
                            if target_info:
                                target_name, distance = target_info
                                # Check if hit
                                hit = self.weapons_manager.check_hit(
                                    car.name, positions[car.name],
                                    target_name, positions[target_name],
                                    True  # is_target_ahead
                                )
                                if hit:
                                    hit["time"] = 0.0
                                    print(f"🔫 {car.name} HIT {target_name}! (-{int(hit['damage']*100)}% speed)")
                                    # Speed reduction will be applied in next section
                                else:
                                    print(f"🔫 {car.name} fired but missed {target_name}!")
                            else:
                                print(f"🔫 {car.name} fired but no target in range!")
                    
                    # Apply action - let LLMs be creative!
                    # Use average of top speed and corner speed for a balanced base speed
                    base_speed = (car.top_speed + car.calculate_corner_speed(30)) / 2
                    weather_factor = 0.9 if self.weather == "rain" else 1.0
                    
                    # Apply power-up speed modifiers
                    power_up_modifier = self.powerup_manager.get_speed_modifier(car.name)
                    
                    # Check if protected from collisions
                    is_protected = self.powerup_manager.is_protected(car.name)
                    
                    # Apply collision speed penalties (unless protected)
                    collision_modifier = 1.0
                    if not is_protected and car.current_speed > 10:  # Only apply penalty if already moving
                        collision_speed = collision_speeds.get(car.name, car.current_speed)
                        if collision_speed < car.current_speed:
                            collision_modifier = collision_speed / car.current_speed
                    
                    actual_speed = (driver.apply_action_to_car(action, base_speed * weather_factor) 
                                   * power_up_modifier * collision_modifier)
                    
                    # Update car's current speed
                    car.current_speed = actual_speed
                    
                    # Update position
                    # Convert km/h to m/s, then calculate distance in meters
                    speed_ms = actual_speed / 3.6  # km/h to m/s
                    distance = speed_ms * time_step  # meters traveled
                    progress = distance / (self.track.total_length * 1000)  # track length is in km
                    positions[car.name] += progress
                    
                    # Check for power-up pickup collection
                    if hasattr(self, 'powerup_manager'):
                        collected = self.powerup_manager.check_pickup_collection(
                            car.name, positions[car.name] % 1.0, collection_radius=0.002  # Even smaller - 0.2% of track
                        )
                        if collected:
                            print(f"📦 {car.name} collected a power-up box!")
                    
                    
                    # Check for lap completion
                    if positions[car.name] >= 1.0:
                        positions[car.name] -= 1.0
                        laps_completed[car.name] += 1  # Track individual car laps
                        lap_time = 45 + (5 - i) * 1  # Much faster lap times!
                        lap_times[car.name].append(lap_time)
                        
                        # Generate event
                        if driver.last_action == LLMAction.ATTACK and i > 0:
                            event = {
                                "type": "overtake_success",
                                "details": f"Passed position {i+1} to {i}"
                            }
                            try:
                                reaction_future = executor.submit(asyncio.run, driver.react_to_event(event))
                                reaction = reaction_future.result(timeout=0.5)
                                print(f"💬 {driver.name}: \"{reaction}\"")
                            except Exception:
                                pass  # Skip reaction on error
                        
                        if len(lap_times[car.name]) >= self.laps:
                            car.race_complete = True
                            
                    # Update car state
                    car.fuel_level -= 0.15 * time_step
                    car.tire_wear += 0.08 * time_step
                    
                except Exception as e:
                    print(f"🚨 Car update error for {getattr(car, 'name', 'unknown')}: {e}")
                    # Continue with next car
                    continue
            
            # Power-up system updates
            try:
                
                # Update power-up effects and collision cooldowns
                self.powerup_manager.update_effects(0.016)  # Actual frame time
                self.powerup_manager.update_pickups(0.016)  # Update pickup respawns
                self.collision_detector.update_cooldowns()
                self.weapons_manager.update_effects(0.016)  # Update weapon effects
            except Exception as e:
                print(f"⚠️ Power-up system error: {e}")
                    
            # Update positions based on progress and laps completed
            try:
                valid_cars = [c for c in self.cars if c and hasattr(c, 'name') and c.name in positions]
                # Sort by total distance (laps + current progress)
                sorted_cars = sorted(valid_cars, 
                    key=lambda c: -(laps_completed.get(c.name, 0) + positions.get(c.name, 0)))
                for pos, car in enumerate(sorted_cars, 1):
                    if car and hasattr(car, 'current_position'):
                        car.current_position = pos
            except Exception as e:
                print(f"⚠️ Position update error: {e}")
                
            # Render frame
            self.renderer.render_frame(self, positions, current_lap, self.laps)
            
            # Show LLM decisions in console
            if current_lap == 1 or current_lap == self.laps:
                print(f"\n⚡ LAP {current_lap} DECISIONS:")
                for car in sorted_cars[:3]:  # Top 3
                    if car.name in decisions:
                        driver = self.llm_drivers[car.name]
                        decision = decisions[car.name]
                        print(f"  {driver.name}: {decision['action']} - {decision['reasoning']}")
            
            # Check lap progression
            min_laps = min(len(lap_times[car.name]) for car in self.cars)
            if min_laps >= current_lap:
                current_lap += 1
                
            time.sleep(0.016)  # 60 FPS target
            
        # Clean up
        executor.shutdown(wait=True)
        if self.renderer:
            self.renderer.cleanup()
            
        # Generate results
        try:
            results = self._generate_results(lap_times)
            results["llm_stats"] = self._generate_llm_stats()
            return results
        except Exception as e:
            print(f"🚨 Error generating results: {e}")
            import traceback
            traceback.print_exc()
            # Return minimal results
            return {
                "finishing_order": [],
                "lap_times": lap_times,
                "error": str(e)
            }
    
    def _run_async_race(self) -> Dict:
        """Helper to run async race in a new event loop"""
        return asyncio.run(self.simulate_race_async())
    
    async def simulate_race_async(self) -> Dict:
        """Async race simulation for non-visual mode"""
        print("\n🤖 LLM RACE (Text Mode) 🤖")
        
        # Initialize
        for car in self.cars:
            car.reset_for_race()
            
        lap_times = {}
        positions = {}
        for car in self.cars:
            if car and hasattr(car, 'name') and car.name:
                lap_times[car.name] = []
                positions[car.name] = 0.0
        
        for lap in range(1, self.laps + 1):
            print(f"\n📍 LAP {lap}/{self.laps}")
            
            # Make decisions for all drivers
            tasks = []
            for i, car in enumerate(self.cars):
                driver = self.llm_drivers[car.name]
                race_state = {
                    "total_cars": len(self.cars),
                    "current_lap": lap,
                    "total_laps": self.laps,
                    "gap_ahead": 50 if i > 0 else 999,
                    "gap_behind": 50 if i < len(self.cars)-1 else 999,
                    "track_segment": "mixed",
                    "weather": self.weather
                }
                tasks.append(driver.make_decision(race_state))
            
            # Wait for all decisions
            decisions = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Apply decisions
            for car, decision in zip(self.cars, decisions):
                if isinstance(decision, dict):
                    driver = self.llm_drivers[car.name]
                    action = LLMAction(decision.get("action", "WAIT"))
                    print(f"  {driver.name}: {action.value} - {decision.get('reasoning', '')}")
                    
                    # Simulate lap time based on action
                    base_time = 85
                    if action == LLMAction.ATTACK:
                        base_time -= 3
                    elif action == LLMAction.CONSERVE:
                        base_time += 2
                        
                    lap_times[car.name].append(base_time)
            
        return self._generate_results(lap_times)
    
    def _generate_results(self, lap_times: Dict[str, List[float]]) -> Dict:
        """Generate race results"""
        finishing_order = []
        
        for car in sorted(self.cars, key=lambda c: sum(lap_times.get(c.name, [999]))):
            driver = self.llm_drivers[car.name]
            total_time = sum(lap_times.get(car.name, []))
            
            finishing_order.append({
                "position": len(finishing_order) + 1,
                "name": car.name,
                "driver": driver.name,
                "model": driver.model_config["model"].split("/")[-1],
                "total_time": total_time,
                "laps_completed": len(lap_times.get(car.name, [])),
                "average_confidence": driver.average_confidence,
                "decisions_made": driver.decisions_made,
                "final_fuel": max(0, car.fuel_level),
                "tire_wear": car.tire_wear
            })
            
        return {
            "finishing_order": finishing_order,
            "lap_times": lap_times,
            "track": self.track.name,
            "weather": self.weather,
            "total_laps": self.laps,
            "visualization_completed": self.enable_graphics
        }
    
    def _generate_llm_stats(self) -> Dict:
        """Generate LLM-specific statistics"""
        stats = {}
        
        for name, driver in self.llm_drivers.items():
            stats[name] = {
                "model": driver.model_config["model"],
                "decisions": driver.decisions_made,
                "avg_confidence": driver.average_confidence,
                "actions": {
                    "attacks": sum(1 for _ in range(driver.decisions_made) if driver.last_action == LLMAction.ATTACK),
                    "defends": sum(1 for _ in range(driver.decisions_made) if driver.last_action == LLMAction.DEFEND),
                    "conserves": sum(1 for _ in range(driver.decisions_made) if driver.last_action == LLMAction.CONSERVE),
                }
            }
            
        return stats