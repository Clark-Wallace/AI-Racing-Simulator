"""
Graphics module for AI Racing Simulator
Provides optional Pygame-based visualization
"""

GRAPHICS_AVAILABLE = False

try:
    import pygame
    GRAPHICS_AVAILABLE = True
except ImportError:
    pass