#!/usr/bin/env python3
"""Quick sprite display test with screenshot capability"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialize pygame first
import pygame
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("AI Racing - Sprite Demo")

from src.graphics.sprite_manager import SpriteManager
from src.graphics.race_renderer import RaceRenderer, GraphicsSettings
from src.core.racing_car import RacingCar, DriverStyle
from src.core.race_track import RaceTrack, TrackType, TrackSegment
import math

# Create sprite manager
sprite_manager = SpriteManager()
sprite_manager.load_sprites()

# Create renderer
settings = GraphicsSettings(width=1200, height=800)
renderer = RaceRenderer(settings)
renderer.sprite_manager = sprite_manager

# Create a simple track
segments = [
    TrackSegment(length=1000, is_straight=True),
    TrackSegment(length=500, is_straight=False, corner_angle=90, corner_radius=100),
    TrackSegment(length=800, is_straight=True),
    TrackSegment(length=700, is_straight=False, corner_angle=120, corner_radius=80),
]

track = RaceTrack(
    name="Demo Track",
    track_type=TrackType.SPEED_TRACK,
    total_length=3.0,
    segments=segments
)

# Create test cars
cars = [
    RacingCar("Llama Speed", 385, 3.0, 0.65, 9, DriverStyle.AGGRESSIVE),
    RacingCar("Llama Strategic", 355, 2.7, 0.88, 16, DriverStyle.BALANCED),
    RacingCar("Llama Balanced", 365, 2.85, 0.78, 13, DriverStyle.BALANCED),
    RacingCar("Hermes Chaos", 375, 2.95, 0.68, 11, DriverStyle.CHAOTIC),
    RacingCar("Qwen Technical", 360, 2.75, 0.92, 14, DriverStyle.TECHNICAL),
]

# Initialize positions
for i, car in enumerate(cars):
    car.current_position = i + 1

# Generate track points
track_points = renderer.generate_track_points(track)

# Main display loop
clock = pygame.time.Clock()
running = True
frame = 0
positions = {car.name: i * 0.15 for i, car in enumerate(cars)}  # Spread cars out
screenshot_taken = False

# Test power-up effects
test_powerup_manager = type('PowerUpManager', (), {
    'active_effects': {
        'Llama Speed': [{'type': 'turbo_boost'}],  # Give first car turbo
        'Hermes Chaos': [{'type': 'nitro'}]       # Give fourth car nitro
    }
})()

# Create a dummy simulator with power-up manager
simulator = type('Simulator', (), {
    'cars': cars,
    'track': track,
    'powerup_manager': test_powerup_manager
})()

while running and frame < 300:  # Run for 300 frames (5 seconds)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_s:  # Take screenshot
                pygame.image.save(screen, "sprite_demo_screenshot.png")
                print("📸 Screenshot saved!")
    
    # Clear screen
    screen.fill((50, 150, 50))  # Grass green
    
    # Draw track
    renderer.draw_track(screen, track_points)
    
    # Update positions (cars moving at different speeds)
    for i, car in enumerate(cars):
        speed_factor = 0.002 + i * 0.0003  # Different speeds
        positions[car.name] = (positions[car.name] + speed_factor) % 1.0
    
    # Draw cars with sprites
    for car in cars:
        progress = positions[car.name]
        x, y, angle = renderer.calculate_car_position(car, progress, track_points)
        color = renderer.AI_COLORS.get(car.driver_style, (255, 255, 255))
        renderer.draw_car(screen, x, y, angle, color, car.name)
        
        # Draw power-up effects if active
        if car.name in test_powerup_manager.active_effects:
            for effect in test_powerup_manager.active_effects[car.name]:
                if effect['type'] in ['turbo_boost', 'nitro']:
                    renderer.draw_power_up_effect(screen, x, y, 'turbo', angle)
    
    # Draw title
    font = pygame.font.Font(None, 48)
    title = font.render("AI Racing - Sprite Demo", True, (255, 255, 255))
    title_rect = title.get_rect(center=(600, 50))
    screen.blit(title, title_rect)
    
    # Draw car names
    small_font = pygame.font.Font(None, 24)
    y_offset = 100
    for car in cars:
        color = renderer.AI_COLORS.get(car.driver_style, (255, 255, 255))
        text = small_font.render(f"{car.name}", True, color)
        screen.blit(text, (50, y_offset))
        y_offset += 30
    
    # Draw instructions
    inst_text = small_font.render("Press S to save screenshot, ESC to exit", True, (200, 200, 200))
    inst_rect = inst_text.get_rect(center=(600, 750))
    screen.blit(inst_text, inst_rect)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)
    
    # Update animation frame for effects
    renderer.animation_frame += 1
    
    # Auto-screenshot at frame 120 (2 seconds)
    if frame == 120 and not screenshot_taken:
        pygame.image.save(screen, "sprite_demo_auto.png")
        print("📸 Auto-screenshot saved as sprite_demo_auto.png!")
        screenshot_taken = True
    
    frame += 1

pygame.quit()
print(f"✅ Demo complete! Ran for {frame} frames")