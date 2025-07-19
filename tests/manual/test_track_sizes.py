#!/usr/bin/env python3
"""Test track sizes to ensure they fit on screen"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
pygame.init()

from src.core.race_track import RaceTrack, TrackType
from src.graphics.race_renderer import RaceRenderer, GraphicsSettings
from run_llm_race_menu import (
    create_monaco_track, create_silverstone_track, 
    create_nurburgring_track, create_suzuka_track, 
    create_rainbow_road_track
)

# Create window
settings = GraphicsSettings(width=1200, height=800)
screen = pygame.display.set_mode((settings.width, settings.height))
pygame.display.set_caption("Track Size Test")

# Create renderer
renderer = RaceRenderer(settings)
renderer.screen = screen
renderer.clock = pygame.time.Clock()
renderer.font = pygame.font.Font(None, 36)
renderer.small_font = pygame.font.Font(None, 24)

# Test tracks
test_tracks = [
    ("Speed Track", RaceTrack.create_speed_track()),
    ("Technical Track", RaceTrack.create_technical_track()),
    ("Mixed Track", RaceTrack.create_mixed_track()),
    ("Endurance Track", RaceTrack.create_endurance_track()),
    ("Monaco", create_monaco_track()),
    ("Silverstone", create_silverstone_track()),
    ("Nürburgring", create_nurburgring_track()),
    ("Suzuka", create_suzuka_track()),
    ("Rainbow Road", create_rainbow_road_track()),
]

# Current track index
current_track = 0
running = True
clock = pygame.time.Clock()

print("Track Size Test")
print("===============")
print("Press LEFT/RIGHT arrows to switch tracks")
print("Press SPACE to print track bounds")
print("Press ESC to exit")
print()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                current_track = (current_track - 1) % len(test_tracks)
            elif event.key == pygame.K_RIGHT:
                current_track = (current_track + 1) % len(test_tracks)
            elif event.key == pygame.K_SPACE:
                # Print track bounds
                track_name, track = test_tracks[current_track]
                points = renderer.generate_track_points(track)
                if points:
                    min_x = min(p[0] for p in points)
                    max_x = max(p[0] for p in points)
                    min_y = min(p[1] for p in points)
                    max_y = max(p[1] for p in points)
                    print(f"\n{track_name} Bounds:")
                    print(f"  X: {min_x:.0f} to {max_x:.0f} (width: {max_x - min_x:.0f})")
                    print(f"  Y: {min_y:.0f} to {max_y:.0f} (height: {max_y - min_y:.0f})")
                    print(f"  Screen: {settings.width} x {settings.height}")
                    
                    # Check if track fits
                    fits_x = min_x >= 0 and max_x <= settings.width
                    fits_y = min_y >= 0 and max_y <= settings.height
                    if fits_x and fits_y:
                        print("  ✅ Track fits on screen!")
                    else:
                        if not fits_x:
                            print(f"  ❌ Track too wide! Overflow: {max(0, -min_x) + max(0, max_x - settings.width):.0f}px")
                        if not fits_y:
                            print(f"  ❌ Track too tall! Overflow: {max(0, -min_y) + max(0, max_y - settings.height):.0f}px")
    
    # Clear screen
    screen.fill((50, 150, 50))
    
    # Get current track
    track_name, track = test_tracks[current_track]
    
    # Generate and draw track
    track_points = renderer.generate_track_points(track)
    renderer.draw_track(screen, track_points)
    
    # Draw track info
    title_text = renderer.font.render(f"Track: {track_name}", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(settings.width // 2, 50))
    screen.blit(title_text, title_rect)
    
    # Draw instructions
    instructions = [
        "← → Switch tracks",
        "SPACE Check bounds",
        "ESC Exit"
    ]
    y_offset = settings.height - 100
    for instruction in instructions:
        text = renderer.small_font.render(instruction, True, (200, 200, 200))
        text_rect = text.get_rect(center=(settings.width // 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 25
    
    # Draw track index
    index_text = renderer.small_font.render(f"{current_track + 1}/{len(test_tracks)}", True, (255, 255, 255))
    screen.blit(index_text, (20, 20))
    
    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
print("\nTrack test complete!")