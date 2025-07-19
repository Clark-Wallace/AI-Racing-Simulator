#!/usr/bin/env python3
"""Visual reference for car sprites and their colors"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
pygame.init()

from src.graphics.sprite_manager import SpriteManager
import math

# Create window
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Car Sprite Color Reference")
clock = pygame.time.Clock()

# Load sprites
sprite_manager = SpriteManager()
sprite_manager.load_sprites()

# Car mappings with expected colors
car_info = [
    ("Car_1", "Llama Speed", "Red aggressive car", (255, 0, 0)),
    ("Car_2", "Llama Strategic", "Blue strategic car", (0, 100, 255)),
    ("Car_3", "Llama Balanced", "Yellow balanced car", (255, 215, 0)),
    ("Car_4", "Hermes Chaos", "Purple chaotic car", (180, 0, 255)),
    ("Car_5", "Qwen Technical", "Green technical car", (0, 255, 128)),
    ("Car_6", "Unused", "Extra car design", (128, 128, 128)),
]

# Font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Main loop
running = True
angle = 0

print("\nCar Sprite Reference:")
print("=" * 50)
for car_id, name, desc, color in car_info:
    print(f"{car_id}: {name} - {desc}")
print("=" * 50)
print("\nPress ESC to exit")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Clear screen
    screen.fill((50, 50, 50))
    
    # Draw title
    title = font.render("Car Sprite Color Reference", True, (255, 255, 255))
    title_rect = title.get_rect(center=(600, 40))
    screen.blit(title, title_rect)
    
    # Draw each car
    x_start = 150
    y_start = 120
    x_spacing = 180
    y_spacing = 200
    
    for i, (car_id, name, desc, expected_color) in enumerate(car_info):
        # Calculate position
        row = i // 3
        col = i % 3
        x = x_start + col * x_spacing * 2
        y = y_start + row * y_spacing
        
        # Get car sprite
        car_parts = sprite_manager.car_sprites.get(car_id, {})
        if car_parts and "part_01" in car_parts:
            sprite = car_parts["part_01"]
            
            # Convert and scale
            try:
                if not hasattr(sprite, '_converted'):
                    sprite = sprite.convert_alpha()
                    sprite._converted = True
            except:
                pass
            
            # Scale down
            scaled = pygame.transform.scale(sprite, 
                (int(sprite.get_width() * 0.15), 
                 int(sprite.get_height() * 0.15)))
            
            # Rotate
            rotated = pygame.transform.rotate(scaled, -math.degrees(angle))
            
            # Draw sprite
            sprite_rect = rotated.get_rect(center=(x, y))
            screen.blit(rotated, sprite_rect)
        else:
            # Draw placeholder
            pygame.draw.rect(screen, (100, 100, 100), (x-30, y-20, 60, 40))
        
        # Draw info
        # Car ID
        id_text = small_font.render(car_id, True, (200, 200, 200))
        id_rect = id_text.get_rect(center=(x, y + 50))
        screen.blit(id_text, id_rect)
        
        # Name
        name_text = small_font.render(name, True, expected_color)
        name_rect = name_text.get_rect(center=(x, y + 70))
        screen.blit(name_text, name_rect)
        
        # Color sample
        pygame.draw.rect(screen, expected_color, (x - 40, y + 85, 80, 15))
        pygame.draw.rect(screen, (255, 255, 255), (x - 40, y + 85, 80, 15), 1)
    
    # Instructions
    inst_text = small_font.render("This shows which car sprite (visual) goes with which name/color", True, (200, 200, 200))
    inst_rect = inst_text.get_rect(center=(600, 750))
    screen.blit(inst_text, inst_rect)
    
    # Update
    pygame.display.flip()
    clock.tick(30)
    angle += 0.02

pygame.quit()
print("\nDone!")