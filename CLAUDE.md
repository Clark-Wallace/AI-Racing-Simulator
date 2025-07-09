# AI Racing Simulator - Claude AI Assistant Guide

## Project Overview

You are working on an AI car racing simulator where 5 AI agents compete as racing cars. The project follows an 8-phase development plan outlined in `claude_code_prompts.md`.

## Current Phase: Phase 1 - Core Racing Engine

### Completed Components:
- ✅ `racing_car.py`: Car physics and driver styles
- ✅ `race_track.py`: Track types and segment system
- 🔄 Need to complete: Race simulation logic and testing

## Key Project Files:
- `claude_code_prompts.md` - Full project specification
- `developers_log.md` - Detailed development history
- `context_catchup.md` - Quick summary for new AI sessions
- `racing_car.py` - Car implementation
- `race_track.py` - Track implementation

## Development Guidelines:

### Code Style:
- Use type hints and dataclasses
- No external dependencies (stdlib only)
- Comprehensive docstrings
- Physics-based calculations

### Testing Commands:
```bash
# Run tests (once created)
python test_racing.py

# Quick validation
python -m py_compile racing_car.py race_track.py
```

## Next Tasks:
1. Complete race simulation logic
2. Implement lap timing and position tracking
3. Add overtaking mechanics
4. Create comprehensive tests
5. Move to Phase 2: Performance Metrics

## Important Design Decisions:
- Modular architecture (separate files per component)
- Realistic physics with simplified calculations
- 5 distinct driver personalities affecting performance
- Data prize system (winners get loser telemetry)

## Physics Constants:
- Standard fuel tank: 60L
- Gravity: 9.81 m/s²
- Base tire wear: 0.1% per km
- Braking efficiency: 1.5x acceleration

## Project Philosophy:
Create an engaging racing simulator where AI agents have distinct personalities and can learn from each other through the data prize system. Balance realism with computational efficiency.