# AI Racing Simulator - Claude AI Assistant Guide

## Project Overview

You are working on an AI car racing simulator where 5 AI agents compete as racing cars. The project follows an 8-phase development plan outlined in `claude_code_prompts.md`.

## Current Phase: LLM Enhancement & Combat Systems

### Completed Components:
- ✅ Core racing engine with physics simulation
- ✅ LLM-powered drivers using Together AI
- ✅ Mario Kart-style power-up system (11 items)
- ✅ Collision detection with 4 collision types
- ✅ Machine gun combat system (50 rounds/car)
- ✅ Professional sprite graphics at 60 FPS
- ✅ Interactive menu system
- ✅ Precision pickup system (0.2% radius)

## Key Project Files:
- `run_llm_race_menu.py` - Main entry point with interactive menu
- `src/llm_drivers/` - LLM-powered AI drivers
- `src/core/racing_powerups.py` - Power-up system
- `src/core/racing_weapons.py` - Machine gun combat
- `src/graphics/race_renderer.py` - Visual rendering engine
- `ai_config.py` - Together AI configuration

## Development Guidelines:

### Code Style:
- Use type hints and dataclasses
- No external dependencies (stdlib only)
- Comprehensive docstrings
- Physics-based calculations

### Running the Simulator:
```bash
# Start interactive race menu
python3 run_llm_race_menu.py

# Test machine gun system
python3 test_machine_guns.py

# Quick validation
python3 -m py_compile src/core/*.py src/llm_drivers/*.py
```

## Recent Enhancements:
1. ✅ Fixed position tracking with lap counting
2. ✅ Reduced power-up pickup radius to 0.002
3. ✅ Made pickup boxes smaller (10x10 pixels)
4. ✅ Added machine gun system with 50 rounds
5. ✅ Implemented bullet visual effects
6. ✅ Added ammo counter display
7. ✅ Updated AI prompts to encourage weapon use

## Important Design Decisions:
- LLM drivers make natural language decisions
- Power-ups use position-based distribution
- Machine guns have limited ammo (no refills)
- Ultra-precise pickup system prevents monopolization
- Collision detection affects speed realistically

## Key Systems:
- **Power-ups**: 11 types, 0.2% pickup radius
- **Machine guns**: 50 rounds, 300m range, 15% damage
- **Collision**: 4 types with varying penalties
- **LLM decisions**: Every 0.5 seconds, async
- **Graphics**: 60 FPS, sprite-based, 1200x800px

## Project Philosophy:
Create an engaging racing simulator where AI agents have distinct personalities and can learn from each other through the data prize system. Balance realism with computational efficiency.