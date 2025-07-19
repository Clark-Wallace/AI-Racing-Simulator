"""
Main graphics engine for AI Racing Simulator
Renders races using Pygame for 2D visualization
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import math
import time

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

from ..core.racing_car import RacingCar, DriverStyle
from ..core.race_track import RaceTrack, TrackType
from ..core.race_simulator import RaceSimulator
from .sprite_manager import SpriteManager


@dataclass
class GraphicsSettings:
    """Configuration for graphics rendering"""
    width: int = 1200
    height: int = 800
    fps: int = 60
    show_telemetry: bool = True
    show_ai_thoughts: bool = True
    camera_mode: str = "follow"  # fixed, follow, free
    quality: str = "medium"  # low, medium, high


class RaceRenderer:
    """Main graphics renderer for AI Racing"""
    
    # Color scheme for AI personalities (fallback)
    AI_COLORS = {
        DriverStyle.AGGRESSIVE: (220, 20, 20),     # Red for Speed Demon
        DriverStyle.CONSERVATIVE: (20, 200, 20),   # Green for Fuel Master
        DriverStyle.BALANCED: (20, 20, 220),       # Blue for Tech Precision
        DriverStyle.TECHNICAL: (220, 220, 20),     # Yellow for Adaptive Racer
        DriverStyle.CHAOTIC: (220, 20, 220)        # Magenta for Chaos Cruiser
    }
    
    # Specific colors for LLM drivers based on car names
    CAR_NAME_COLORS = {
        "Llama Speed": (255, 0, 0),          # Pure Red (matches "Speed")
        "Llama Strategic": (0, 100, 255),    # Deep Blue (strategic thinking)
        "Llama Balanced": (255, 215, 0),     # Gold/Yellow (balanced approach)
        "Hermes Chaos": (180, 0, 255),       # Purple (chaotic/magical)
        "Qwen Technical": (0, 255, 128),     # Green/Teal (technical precision)
        # Traditional AI cars
        "Speed Demon": (220, 20, 20),        # Dark Red
        "Fuel Master": (20, 200, 20),        # Green
        "Tech Precision": (20, 20, 220),     # Blue
        "Adaptive Racer": (220, 220, 20),    # Yellow
        "Chaos Cruiser": (220, 20, 220)      # Magenta
    }
    
    def __init__(self, settings: GraphicsSettings = None):
        if not PYGAME_AVAILABLE:
            raise ImportError("Pygame is required for graphics. Install with: pip install pygame")
            
        self.settings = settings or GraphicsSettings()
        self.screen = None
        self.clock = None
        self.font = None
        self.small_font = None
        self.running = False
        
        # Track and car positions
        self.track_points = []
        self.car_positions = {}
        self.car_angles = {}
        
        # Lane tracking for smooth transitions
        self.car_lanes = {}  # car_name -> current_lane_offset
        self.target_lanes = {}  # car_name -> target_lane_offset
        self.lane_transition_speed = 0.15  # How fast cars change lanes
        
        # Camera settings
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
        
        # Sprite manager
        self.sprite_manager = None
        self.use_sprites = True
        self.animation_frame = 0
        
    def initialize(self):
        """Initialize Pygame and create window"""
        pygame.init()
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption("AI Racing Simulator - Visual Mode")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize sprite manager
        self.sprite_manager = SpriteManager()
        self.sprite_manager.load_sprites()
        
        self.running = True
        
    def generate_track_points(self, track: RaceTrack) -> List[Tuple[float, float]]:
        """Generate visual points for track based on track type"""
        points = []
        center_x = self.settings.width // 2
        center_y = self.settings.height // 2
        
        # Calculate maximum dimensions based on screen size with padding
        max_width = (self.settings.width - 200) / 2    # Leave 100px padding on each side
        max_height = (self.settings.height - 200) / 2   # Leave 100px padding on top/bottom
        
        if track.track_type == TrackType.SPEED_TRACK:
            # Oval circuit for speed tracks
            for i in range(100):
                angle = (i / 100) * 2 * math.pi
                x = center_x + max_width * 0.9 * math.cos(angle)   # 90% of max width
                y = center_y + max_height * 0.7 * math.sin(angle)  # 70% of max height for oval
                points.append((x, y))
                
        elif track.track_type == TrackType.TECHNICAL_TRACK:
            # Figure-8 technical circuit
            for i in range(100):
                t = (i / 100) * 2 * math.pi
                x = center_x + max_width * 0.75 * math.sin(t)      # 75% for figure-8 width
                y = center_y + max_height * 0.6 * math.sin(2 * t)  # 60% for figure-8 height
                points.append((x, y))
                
        elif track.track_type == TrackType.ENDURANCE_TRACK:
            # Large complex circuit - scale to fit
            for i in range(150):
                t = (i / 150) * 2 * math.pi
                # Scale down the complex pattern to fit screen
                x = center_x + max_width * 0.8 * math.cos(t) + max_width * 0.2 * math.cos(3 * t)
                y = center_y + max_height * 0.8 * math.sin(t) + max_height * 0.2 * math.sin(5 * t)
                points.append((x, y))
                
        else:  # MIXED_TRACK
            # Twisty mixed course
            for i in range(120):
                t = (i / 120) * 2 * math.pi
                x = center_x + max_width * 0.85 * math.cos(t) + max_width * 0.15 * math.sin(7 * t)
                y = center_y + max_height * 0.85 * math.sin(t) + max_height * 0.15 * math.cos(5 * t)
                points.append((x, y))
                
        return points
        
    def calculate_car_position(self, car: RacingCar, progress: float, 
                             track_points: List[Tuple[float, float]]) -> Tuple[float, float, float]:
        """Calculate car position and angle on track"""
        # Find position on track based on progress
        total_points = len(track_points)
        point_index = int(progress * total_points) % total_points
        next_index = (point_index + 1) % total_points
        
        # Interpolate between points
        t = (progress * total_points) % 1
        current_point = track_points[point_index]
        next_point = track_points[next_index]
        
        x = current_point[0] + t * (next_point[0] - current_point[0])
        y = current_point[1] + t * (next_point[1] - current_point[1])
        
        # Calculate angle
        dx = next_point[0] - current_point[0]
        dy = next_point[1] - current_point[1]
        angle = math.atan2(dy, dx)
        
        # Add lane offset with smooth transitions
        # Calculate target lane based on race position
        normalized_pos = (car.current_position - 1) / 4.0 * 2 - 1  # Maps 1-5 to -1 to 1
        target_lane_offset = normalized_pos * 25  # Increased to match wider track
        
        # Initialize lane tracking if needed
        if car.name not in self.car_lanes:
            self.car_lanes[car.name] = target_lane_offset
            self.target_lanes[car.name] = target_lane_offset
        
        # Update target lane
        self.target_lanes[car.name] = target_lane_offset
        
        # Smoothly transition to target lane
        current_lane = self.car_lanes[car.name]
        if abs(current_lane - target_lane_offset) > 0.1:
            # Move towards target lane
            direction = 1 if target_lane_offset > current_lane else -1
            self.car_lanes[car.name] = current_lane + (direction * self.lane_transition_speed)
        else:
            self.car_lanes[car.name] = target_lane_offset
        
        # Apply the smooth lane offset
        lane_offset = self.car_lanes[car.name]
        x += lane_offset * math.sin(angle)
        y -= lane_offset * math.cos(angle)
        
        return x, y, angle
        
    def draw_track(self, surface, track_points: List[Tuple[float, float]]):
        """Draw the race track"""
        if len(track_points) < 2:
            return
            
        # Draw track outline
        track_width = 120  # Increased from 80 to match bigger tracks
        
        # Draw outer edge
        outer_points = []
        inner_points = []
        
        for i, point in enumerate(track_points):
            next_i = (i + 1) % len(track_points)
            prev_i = (i - 1) % len(track_points)
            
            # Calculate normal vector
            dx = track_points[next_i][0] - track_points[prev_i][0]
            dy = track_points[next_i][1] - track_points[prev_i][1]
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                nx = -dy / length
                ny = dx / length
                
                outer_points.append((
                    point[0] + nx * track_width/2,
                    point[1] + ny * track_width/2
                ))
                inner_points.append((
                    point[0] - nx * track_width/2,
                    point[1] - ny * track_width/2
                ))
                
        # Draw track surface
        if outer_points and inner_points:
            pygame.draw.polygon(surface, (60, 60, 60), outer_points)
            pygame.draw.polygon(surface, (200, 200, 200), inner_points)
            
        # Draw center line
        for i in range(0, len(track_points), 5):
            pygame.draw.circle(surface, (255, 255, 255), 
                             (int(track_points[i][0]), int(track_points[i][1])), 2)
                             
    def draw_car(self, surface, x: float, y: float, 
                angle: float, color: Tuple[int, int, int], name: str):
        """Draw a racing car"""
        # Try to use sprite first
        if self.use_sprites and self.sprite_manager:
            sprite = self.sprite_manager.get_car_sprite(name, angle, scale=0.0375)  # 25% of 0.15 = 0.0375
            if sprite:
                # Center the sprite on the car position
                sprite_rect = sprite.get_rect(center=(int(x), int(y)))
                surface.blit(sprite, sprite_rect)
                return
        
        # Fallback to polygon drawing if no sprite available
        # Car dimensions
        car_length = 40
        car_width = 20
        
        # Create car shape
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        
        # Car corners (before rotation)
        corners = [
            (-car_length/2, -car_width/2),
            (car_length/2, -car_width/2),
            (car_length/2, car_width/2),
            (-car_length/2, car_width/2)
        ]
        
        # Rotate and translate corners
        rotated_corners = []
        for cx, cy in corners:
            rx = cx * cos_a - cy * sin_a + x
            ry = cx * sin_a + cy * cos_a + y
            rotated_corners.append((rx, ry))
            
        # Draw car body
        pygame.draw.polygon(surface, color, rotated_corners)
        pygame.draw.polygon(surface, (0, 0, 0), rotated_corners, 2)
        
        # Draw windshield
        windshield_x = x + car_length/4 * cos_a
        windshield_y = y + car_length/4 * sin_a
        pygame.draw.circle(surface, (100, 100, 255), 
                         (int(windshield_x), int(windshield_y)), 5)
    
    def draw_power_up_pickup(self, surface, x: float, y: float, available: bool = True):
        """Draw a power-up pickup box on the track"""
        box_size = 10  # Extra small to match tiny collection radius
        
        if available:
            # Draw rotating mystery box
            # Outer box
            colors = [
                (255, 215, 0),   # Gold
                (255, 255, 255), # White
                (0, 255, 255),   # Cyan
            ]
            color_index = (self.animation_frame // 10) % len(colors)
            box_color = colors[color_index]
            
            # Draw box with gradient effect
            pygame.draw.rect(surface, box_color, 
                           (x - box_size//2, y - box_size//2, box_size, box_size))
            pygame.draw.rect(surface, (0, 0, 0), 
                           (x - box_size//2, y - box_size//2, box_size, box_size), 2)
            
            # Draw question mark
            font = pygame.font.Font(None, 16)
            text = font.render("?", True, (0, 0, 0))
            text_rect = text.get_rect(center=(x, y))
            surface.blit(text, text_rect)
            
            # Draw glow effect
            glow_radius = box_size // 2 + 3 + int(2 * math.sin(self.animation_frame * 0.1))
            for i in range(2):
                alpha = 50 - i * 20
                pygame.draw.circle(surface, (*box_color, alpha), (int(x), int(y)), 
                                 glow_radius + i * 2, 1)
        else:
            # Draw respawning indicator
            respawn_alpha = 100
            pygame.draw.rect(surface, (100, 100, 100, respawn_alpha),
                           (x - box_size//2, y - box_size//2, box_size, box_size), 1)
    
    def draw_power_up_indicator(self, surface, x: float, y: float, power_up_type: str, size: int = 20):
        """Draw power-up indicator above car"""
        # Power-up colors and symbols
        power_up_visuals = {
            "turbo_boost": ("🚀", (255, 165, 0)),      # Orange
            "nitro": ("⚡", (255, 255, 0)),            # Yellow
            "shield": ("🛡️", (0, 255, 255)),          # Cyan
            "lightning_bolt": ("⚡", (255, 255, 100)),  # Light yellow
            "red_shell": ("🔴", (255, 0, 0)),         # Red
            "blue_shell": ("🔵", (0, 0, 255)),        # Blue
            "banana": ("🍌", (255, 255, 0)),          # Yellow
            "ghost": ("👻", (200, 200, 255)),         # Light blue
            "fuel_boost": ("⛽", (100, 255, 100)),     # Light green
            "tire_repair": ("🔧", (150, 150, 150)),   # Gray
            "radar": ("📡", (150, 100, 255))          # Purple
        }
        
        if power_up_type.lower() in power_up_visuals:
            emoji, color = power_up_visuals[power_up_type.lower()]
            # Draw colored circle background (closer to smaller cars)
            indicator_y = y - 20  # Reduced from 30
            pygame.draw.circle(surface, color, (int(x), int(indicator_y)), size)
            pygame.draw.circle(surface, (0, 0, 0), (int(x), int(indicator_y)), size, 2)
            # Draw text representation (since pygame doesn't support emojis well)
            text = self.small_font.render(power_up_type[:3].upper(), True, (0, 0, 0))
            text_rect = text.get_rect(center=(int(x), int(indicator_y)))
            surface.blit(text, text_rect)
    
    def draw_power_up_effect(self, surface, x: float, y: float, effect_type: str, car_angle: float):
        """Draw active power-up effects on car"""
        if effect_type == "turbo" or effect_type == "nitro":
            # Use nitro sprite animation if available
            if self.sprite_manager:
                nitro_sprite = self.sprite_manager.get_effect_animation("nitro", self.animation_frame)
                if nitro_sprite:
                    # Position nitro behind car (opposite direction of car's facing)
                    # Since car faces in the direction of angle, we add π to go backwards
                    offset_dist = 15  # Reduced for smaller cars
                    back_angle = car_angle + math.pi
                    nitro_x = x + offset_dist * math.cos(back_angle)
                    nitro_y = y + offset_dist * math.sin(back_angle)
                    
                    # Rotate nitro effect to match car angle (pointing backwards)
                    angle_degrees = -math.degrees(car_angle) + 90  # Adjusted for correct orientation
                    rotated_nitro = pygame.transform.rotate(nitro_sprite, angle_degrees)
                    
                    # Scale down the effect to match smaller cars
                    scaled_nitro = pygame.transform.scale(rotated_nitro, 
                        (int(rotated_nitro.get_width() * 0.125),  # 25% of 0.5 = 0.125
                         int(rotated_nitro.get_height() * 0.125)))
                    
                    nitro_rect = scaled_nitro.get_rect(center=(int(nitro_x), int(nitro_y)))
                    surface.blit(scaled_nitro, nitro_rect)
                    return
            
            # Fallback to drawn effect
            for i in range(3):
                flame_x = x - (20 + i * 10) * math.cos(car_angle)
                flame_y = y - (20 + i * 10) * math.sin(car_angle)
                size = 8 - i * 2
                color = (255, 200 - i * 50, 0)
                pygame.draw.circle(surface, color, (int(flame_x), int(flame_y)), size)
        
        elif effect_type == "shield":
            # Draw shield bubble around car
            pygame.draw.circle(surface, (0, 255, 255), (int(x), int(y)), 35, 3)
            for i in range(0, 360, 30):
                angle = math.radians(i)
                spark_x = x + 35 * math.cos(angle)
                spark_y = y + 35 * math.sin(angle)
                pygame.draw.circle(surface, (255, 255, 255), (int(spark_x), int(spark_y)), 2)
        
        elif effect_type == "ghost":
            # Draw ghostly aura
            for i in range(3):
                alpha = 100 - i * 30
                pygame.draw.circle(surface, (200, 200, 255), (int(x), int(y)), 25 + i * 5, 2)
    
    def draw_bullet_trail(self, surface, shooter_x: float, shooter_y: float, 
                         target_x: float, target_y: float, hit: bool = False):
        """Draw machine gun bullet trail effect"""
        # Draw multiple bullet streaks for machine gun effect
        for i in range(3):
            # Slightly offset each bullet for spread effect
            offset_angle = (i - 1) * 0.05
            cos_offset = math.cos(offset_angle)
            sin_offset = math.sin(offset_angle)
            
            # Calculate endpoints with offset
            start_x = shooter_x + 10 * cos_offset
            start_y = shooter_y + 10 * sin_offset
            end_x = target_x + 20 * cos_offset
            end_y = target_y + 20 * sin_offset
            
            # Draw bullet trail
            if hit:
                # Red trail for hits
                pygame.draw.line(surface, (255, 100, 0), 
                               (int(start_x), int(start_y)), 
                               (int(end_x), int(end_y)), 2)
                # Impact flash
                pygame.draw.circle(surface, (255, 200, 0), (int(end_x), int(end_y)), 8)
                pygame.draw.circle(surface, (255, 255, 100), (int(end_x), int(end_y)), 5)
            else:
                # Yellow trail for misses
                pygame.draw.line(surface, (255, 255, 0), 
                               (int(start_x), int(start_y)), 
                               (int(end_x), int(end_y)), 1)
        
        # Muzzle flash at shooter position
        pygame.draw.circle(surface, (255, 255, 200), (int(shooter_x), int(shooter_y)), 6)
        pygame.draw.circle(surface, (255, 200, 0), (int(shooter_x), int(shooter_y)), 4)
                         
    def draw_hud(self, surface, cars: List[RacingCar], 
                lap: int, total_laps: int):
        """Draw heads-up display with race information"""
        # Background for HUD
        hud_rect = pygame.Rect(10, 10, 300, 200)
        pygame.draw.rect(surface, (0, 0, 0), hud_rect)
        pygame.draw.rect(surface, (255, 255, 255), hud_rect, 2)
        
        # Title
        title_text = self.small_font.render("Race Status", True, (255, 255, 255))
        surface.blit(title_text, (20, 20))
        
        # Lap counter
        lap_text = self.small_font.render(f"Lap {lap}/{total_laps}", True, (255, 255, 255))
        surface.blit(lap_text, (20, 50))
        
        # Car positions
        y_offset = 80
        for i, car in enumerate(sorted(cars, key=lambda c: c.current_position)):
            # Use car name colors first, then fall back to driver style colors
            color = self.CAR_NAME_COLORS.get(car.name, self.AI_COLORS.get(car.driver_style, (255, 255, 255)))
            pos_text = self.small_font.render(
                f"P{car.current_position + 1}: {car.name[:15]}", True, color
            )
            surface.blit(pos_text, (20, y_offset + i * 25))
    
    def draw_power_up_inventory(self, surface, simulator):
        """Draw power-up inventory panel"""
        # Background for power-up panel
        panel_rect = pygame.Rect(self.settings.width - 320, 10, 300, 250)
        pygame.draw.rect(surface, (0, 0, 0), panel_rect)
        pygame.draw.rect(surface, (255, 255, 255), panel_rect, 2)
        
        # Title
        title_text = self.small_font.render("Power-Up Inventory", True, (255, 255, 255))
        surface.blit(title_text, (self.settings.width - 310, 20))
        
        # Draw each car's power-ups
        y_offset = 50
        for i, car in enumerate(sorted(simulator.cars, key=lambda c: c.current_position)):
            # Car name - use car name colors first
            color = self.CAR_NAME_COLORS.get(car.name, self.AI_COLORS.get(car.driver_style, (255, 255, 255)))
            name_text = self.small_font.render(f"{car.name[:12]}:", True, color)
            surface.blit(name_text, (self.settings.width - 310, y_offset))
            
            # Power-ups
            inventory = simulator.powerup_manager.get_inventory_status(car.name)
            if inventory:
                items_text = ", ".join(inventory[:2])  # Show up to 2 items
                item_text = self.small_font.render(items_text, True, (200, 200, 200))
                surface.blit(item_text, (self.settings.width - 180, y_offset))
            else:
                no_item_text = self.small_font.render("None", True, (100, 100, 100))
                surface.blit(no_item_text, (self.settings.width - 180, y_offset))
            
            y_offset += 35
    
    def draw_ammo_display(self, surface, simulator):
        """Draw ammo counter for each car"""
        # Background for ammo panel
        panel_rect = pygame.Rect(self.settings.width - 320, 280, 300, 200)
        pygame.draw.rect(surface, (0, 0, 0), panel_rect)
        pygame.draw.rect(surface, (255, 255, 255), panel_rect, 2)
        
        # Title
        title_text = self.small_font.render("Machine Gun Ammo", True, (255, 255, 255))
        surface.blit(title_text, (self.settings.width - 310, 290))
        
        # Draw each car's ammo
        y_offset = 320
        if hasattr(simulator, 'weapons_manager'):
            ammo_status = simulator.weapons_manager.get_all_ammo_status()
            for car in sorted(simulator.cars, key=lambda c: c.current_position):
                # Car name and color
                color = self.CAR_NAME_COLORS.get(car.name, self.AI_COLORS.get(car.driver_style, (255, 255, 255)))
                name_text = self.small_font.render(f"{car.name[:12]}:", True, color)
                surface.blit(name_text, (self.settings.width - 310, y_offset))
                
                # Ammo bar
                ammo_count = ammo_status.get(car.name, 0)
                bar_width = int((ammo_count / 50) * 120)  # 120 pixels for full ammo
                bar_color = (0, 255, 0) if ammo_count > 25 else (255, 255, 0) if ammo_count > 10 else (255, 0, 0)
                
                # Draw ammo bar background
                pygame.draw.rect(surface, (50, 50, 50), 
                               (self.settings.width - 180, y_offset, 120, 15))
                # Draw ammo bar fill
                if bar_width > 0:
                    pygame.draw.rect(surface, bar_color, 
                                   (self.settings.width - 180, y_offset, bar_width, 15))
                # Draw ammo bar border
                pygame.draw.rect(surface, (200, 200, 200), 
                               (self.settings.width - 180, y_offset, 120, 15), 1)
                
                # Ammo count text
                ammo_text = self.small_font.render(f"{ammo_count}/50", True, (200, 200, 200))
                surface.blit(ammo_text, (self.settings.width - 50, y_offset))
                
                y_offset += 30
            
    def render_frame(self, simulator: RaceSimulator, current_positions: Dict[str, float],
                    lap: int = 1, total_laps: int = 10):
        """Render a single frame of the race"""
        if not self.running:
            return
            
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
        # Clear screen
        self.screen.fill((50, 150, 50))  # Grass green background
        
        # Draw track
        if not self.track_points:
            self.track_points = self.generate_track_points(simulator.track)
        self.draw_track(self.screen, self.track_points)
        
        # Draw power-up pickups on track
        if hasattr(simulator, 'powerup_manager') and simulator.powerup_manager.track_pickups:
            for pickup in simulator.powerup_manager.track_pickups:
                # Calculate pickup position on track
                pickup_progress = pickup.get("progress", 0)
                # Calculate position directly without needing a car
                total_points = len(self.track_points)
                point_index = int(pickup_progress * total_points) % total_points
                next_index = (point_index + 1) % total_points
                
                # Interpolate between points
                t = (pickup_progress * total_points) % 1
                current_point = self.track_points[point_index]
                next_point = self.track_points[next_index]
                
                pickup_x = current_point[0] + t * (next_point[0] - current_point[0])
                pickup_y = current_point[1] + t * (next_point[1] - current_point[1])
                
                self.draw_power_up_pickup(self.screen, pickup_x, pickup_y, pickup.get("available", True))
        
        # Draw cars with power-ups
        for car in simulator.cars:
            if car.name in current_positions:
                progress = current_positions[car.name]
                x, y, angle = self.calculate_car_position(car, progress, self.track_points)
                # Use car name colors first, then fall back to driver style colors
                color = self.CAR_NAME_COLORS.get(car.name, self.AI_COLORS.get(car.driver_style, (255, 255, 255)))
                self.draw_car(self.screen, x, y, angle, color, car.name)
                
                # Draw power-up indicators if simulator has powerup_manager
                if hasattr(simulator, 'powerup_manager'):
                    # Show power-up inventory above car
                    inventory = simulator.powerup_manager.get_inventory_status(car.name)
                    if inventory:
                        # Draw the first power-up in inventory
                        power_up_name = inventory[0]
                        # Convert from display name to type (e.g., "Turbo Boost" -> "turbo_boost")
                        power_up_type = power_up_name.lower().replace(" ", "_")
                        self.draw_power_up_indicator(self.screen, x, y, power_up_type, size=10)  # Smaller for smaller cars
                    
                    # Draw active power-up effects
                    if car.name in simulator.powerup_manager.active_effects:
                        for effect in simulator.powerup_manager.active_effects[car.name]:
                            effect_type = effect["type"]
                            if effect_type in ["turbo_boost", "nitro"]:
                                self.draw_power_up_effect(self.screen, x, y, "turbo", angle)
                            elif effect_type == "shield":
                                self.draw_power_up_effect(self.screen, x, y, "shield", angle)
                            elif effect_type == "ghost":
                                self.draw_power_up_effect(self.screen, x, y, "ghost", angle)
                
        # Draw HUD
        self.draw_hud(self.screen, simulator.cars, lap, total_laps)
        
        # Draw bullet trails for active hits
        if hasattr(simulator, 'weapons_manager'):
            # Store car positions for bullet drawing
            car_positions_screen = {}
            for car in simulator.cars:
                if car.name in current_positions:
                    progress = current_positions[car.name]
                    x, y, angle = self.calculate_car_position(car, progress, self.track_points)
                    car_positions_screen[car.name] = (x, y)
            
            # Draw active bullet trails
            for hit in simulator.weapons_manager.get_active_hits():
                shooter_name = hit["shooter"]
                target_name = hit["target"]
                
                if shooter_name in car_positions_screen and target_name in car_positions_screen:
                    shooter_x, shooter_y = car_positions_screen[shooter_name]
                    target_x, target_y = car_positions_screen[target_name]
                    
                    # Draw the bullet trail
                    self.draw_bullet_trail(self.screen, shooter_x, shooter_y, 
                                         target_x, target_y, hit=True)
        
        # Draw power-up inventory panel if available
        if hasattr(simulator, 'powerup_manager'):
            self.draw_power_up_inventory(self.screen, simulator)
        
        # Draw ammo display if available
        if hasattr(simulator, 'weapons_manager'):
            self.draw_ammo_display(self.screen, simulator)
        
        # Update display
        pygame.display.flip()
        self.clock.tick(self.settings.fps)
        
        # Increment animation frame
        self.animation_frame += 1
        
    def cleanup(self):
        """Clean up Pygame resources"""
        if PYGAME_AVAILABLE:
            pygame.quit()
            
    def is_running(self) -> bool:
        """Check if renderer is still running"""
        return self.running