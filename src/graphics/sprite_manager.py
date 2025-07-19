"""
Sprite Manager for AI Racing Simulator
Handles loading and managing all game sprites
"""

import os
import pygame
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class SpriteManager:
    """Manages all sprites and animations for the racing game"""
    
    def __init__(self, assets_path: str = None):
        """Initialize sprite manager with path to assets"""
        if assets_path is None:
            # Default to assets folder relative to project root
            project_root = Path(__file__).parent.parent.parent
            assets_path = os.path.join(project_root, "assets", "PNG")
            
        self.assets_path = assets_path
        self.sprites = {}
        self.animations = {}
        self.car_sprites = {}
        self.effect_sprites = {}
        
        # Car to sprite mapping (which car design for each driver)
        self.car_sprite_mapping = {
            "Llama Speed": "Car_1",      # Red aggressive car
            "Llama Strategic": "Car_2",   # Blue strategic car
            "Llama Balanced": "Car_3",    # Yellow balanced car
            "Hermes Chaos": "Car_4",      # Purple chaotic car
            "Qwen Technical": "Car_5",    # Green technical car
        }
        
    def load_sprites(self):
        """Load all sprites from assets folder"""
        print(f"🎨 Loading sprites from: {self.assets_path}")
        
        if not os.path.exists(self.assets_path):
            print(f"❌ Assets path not found: {self.assets_path}")
            return
            
        # Load car sprites
        self._load_car_sprites()
        
        # Load effect sprites
        self._load_effect_sprites()
        
        print(f"✅ Loaded {len(self.car_sprites)} car designs")
        print(f"✅ Loaded {len(self.animations)} animations")
        for name, frames in self.animations.items():
            print(f"  - {name}: {len(frames)} frames")
        
    def _load_car_sprites(self):
        """Load all car sprites"""
        for i in range(1, 7):  # Cars 1-6
            car_name = f"Car_{i}"
            car_path = os.path.join(self.assets_path, f"{car_name}_Main_Positions")
            
            if os.path.exists(car_path):
                self.car_sprites[car_name] = {}
                
                # Load each car part
                for j in range(1, 6):  # Parts 01-05
                    part_file = f"{car_name}_{j:02d}.png"
                    part_path = os.path.join(car_path, part_file)
                    
                    if os.path.exists(part_path):
                        try:
                            # Load without convert_alpha() first - will convert when display is ready
                            sprite = pygame.image.load(part_path)
                            self.car_sprites[car_name][f"part_{j:02d}"] = sprite  # Keep 01, 02 format
                            print(f"  ✓ Loaded {car_name} part {j:02d}")
                        except Exception as e:
                            print(f"  ✗ Error loading {part_path}: {e}")
                            
    def _load_effect_sprites(self):
        """Load all effect sprites and animations"""
        effects_path = os.path.join(self.assets_path, "Car_Effects")
        
        if not os.path.exists(effects_path):
            return
            
        # Load Nitro animation
        self._load_animation("nitro", os.path.join(effects_path, "Nitro"), "Nitro_")
        self._load_animation("nitro_low", os.path.join(effects_path, "Nitro_Low"), "Nitro_Low_")
        
        # Load smoke animation
        self._load_animation("smoke", os.path.join(effects_path, "Smoke"), "Smoke_")
        
        # Load tire tracks
        tracks_path = os.path.join(effects_path, "Tire_Tracks")
        if os.path.exists(tracks_path):
            self.effect_sprites["tire_tracks"] = []
            for i in range(1, 4):
                track_path = os.path.join(tracks_path, f"Tire_Track_{i:02d}.png")
                if os.path.exists(track_path):
                    try:
                        # Load without convert_alpha() first
                        track = pygame.image.load(track_path)
                        self.effect_sprites["tire_tracks"].append(track)
                    except Exception as e:
                        print(f"Error loading tire track: {e}")
                        
    def _load_animation(self, name: str, folder_path: str, prefix: str):
        """Load an animation sequence"""
        if not os.path.exists(folder_path):
            return
            
        frames = []
        frame_num = 0
        
        while True:
            frame_path = os.path.join(folder_path, f"{prefix}{frame_num:03d}.png")
            if not os.path.exists(frame_path):
                break
                
            try:
                # Load without convert_alpha() first
                frame = pygame.image.load(frame_path)
                frames.append(frame)
                frame_num += 1
            except Exception as e:
                print(f"Error loading animation frame: {e}")
                break
                
        if frames:
            self.animations[name] = frames
            
    def get_car_sprite(self, car_name: str, angle: float, scale: float = 1.0) -> Optional[pygame.Surface]:
        """Get assembled and rotated car sprite"""
        # Get the car design for this driver
        car_design = self.car_sprite_mapping.get(car_name, "Car_1")
        
        if car_design not in self.car_sprites:
            return None
            
        car_parts = self.car_sprites[car_design]
        if not car_parts:
            return None
            
        # Use the first part as the main car body for now
        # In a full implementation, you'd composite all parts
        main_part = car_parts.get("part_01")
        if not main_part:
            return None
            
        # Convert to display format if needed
        try:
            if not hasattr(main_part, '_converted'):
                main_part = main_part.convert_alpha()
                car_parts["part_01"] = main_part
                main_part._converted = True
        except:
            pass
            
        # Scale the sprite
        if scale != 1.0:
            width = int(main_part.get_width() * scale)
            height = int(main_part.get_height() * scale)
            main_part = pygame.transform.scale(main_part, (width, height))
            
        # Rotate the sprite (convert angle from radians to degrees)
        import math
        angle_degrees = -math.degrees(angle) - 90  # Adjust for sprite orientation
        rotated = pygame.transform.rotate(main_part, angle_degrees)
        
        return rotated
        
    def get_effect_animation(self, effect_name: str, frame: int) -> Optional[pygame.Surface]:
        """Get a specific frame from an effect animation"""
        if effect_name not in self.animations:
            return None
            
        frames = self.animations[effect_name]
        if not frames:
            return None
            
        # Loop the animation
        frame_index = frame % len(frames)
        return frames[frame_index]
        
    def get_tire_track(self, index: int = 0) -> Optional[pygame.Surface]:
        """Get a tire track sprite"""
        tracks = self.effect_sprites.get("tire_tracks", [])
        if not tracks:
            return None
            
        return tracks[index % len(tracks)]