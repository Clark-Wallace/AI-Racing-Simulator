#!/usr/bin/env python3
"""Test sprite loading for the AI Racing Simulator"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Initialize pygame first
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sprite Loading Test")

# Now import and test sprite manager
from src.graphics.sprite_manager import SpriteManager
from src.core.racing_car import RacingCar, DriverStyle
from src.core.race_track import RaceTrack, TrackType
from src.llm_drivers.llm_racing_driver import create_llm_drivers
from src.llm_drivers.llm_race_simulator import LLMRaceSimulator
from src.graphics.race_renderer import GraphicsSettings

print("🎮 Testing sprite loading...")

# Test sprite manager
sprite_manager = SpriteManager()
sprite_manager.load_sprites()

# Create a simple test to show sprites
running = True
clock = pygame.time.Clock()
angle = 0

# Test car names
test_cars = ["Llama Speed", "Llama Strategic", "Llama Balanced", "Hermes Chaos", "Qwen Technical"]
car_index = 0

# Background
screen.fill((50, 150, 50))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                car_index = (car_index + 1) % len(test_cars)
            elif event.key == pygame.K_ESCAPE:
                running = False
    
    # Clear screen
    screen.fill((50, 150, 50))
    
    # Get current car sprite
    car_name = test_cars[car_index]
    sprite = sprite_manager.get_car_sprite(car_name, angle, scale=0.3)
    
    if sprite:
        # Draw sprite in center
        sprite_rect = sprite.get_rect(center=(400, 300))
        screen.blit(sprite, sprite_rect)
        
        # Show car name
        font = pygame.font.Font(None, 36)
        text = font.render(f"Car: {car_name}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 100))
        screen.blit(text, text_rect)
        
        instructions = font.render("Press SPACE to change car, ESC to exit", True, (255, 255, 255))
        instructions_rect = instructions.get_rect(center=(400, 500))
        screen.blit(instructions, instructions_rect)
    else:
        # Show error message
        font = pygame.font.Font(None, 48)
        text = font.render("No sprite loaded!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(400, 300))
        screen.blit(text, text_rect)
    
    # Update display
    pygame.display.flip()
    clock.tick(30)
    
    # Rotate sprite
    angle += 0.02

pygame.quit()
print("✅ Sprite test complete!")