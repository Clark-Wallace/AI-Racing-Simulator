# AI Racing Simulator - JavaScript Edition 🏎️

A browser-based racing game featuring AI drivers, Mario Kart-style power-ups, and machine gun combat!

## 🚀 Features

### 🤖 AI-Powered Racing
- **5 Unique AI Drivers** with distinct personalities
- **Smart Decision Making** - AI drivers adapt to race conditions
- **LLM Simulation** - Mimics natural language reasoning

### 🎮 Power-Up System
- **11 Power-Ups** - From Turbo Boost to Blue Shells
- **Position-Based Distribution** - Catch-up mechanics
- **Visual Effects** - Shields, boosts, and more

### 🔫 Machine Gun Combat
- **50 Rounds Per Car** - Limited ammo, no refills
- **Auto-Targeting** - Targets cars ahead within 300m
- **Damage System** - 15% speed reduction per hit

### 🎨 Visual Features
- **Canvas Rendering** - Smooth 60 FPS
- **Dynamic Tracks** - 5 unique track layouts
- **Real-time Effects** - Bullet trails, nitro flames
- **HUD Displays** - Race positions, ammo, power-ups

## 🎯 How to Play

1. **Open `index.html`** in a modern web browser
2. **Select Options:**
   - Track (Monaco, Silverstone, etc.)
   - Number of laps (3-10)
   - Weather conditions
3. **Click "START RACE"**
4. **Watch the AI battle!**

### Controls
- **ESC** - Return to menu
- **Space** - Fire (if controlling a car - future feature)

## 🏁 The Drivers

### Llama Family
- **Llama Speed** 🔴 - Aggressive speedster
- **Llama Strategic** 🔵 - Tactical planner  
- **Llama Balanced** 🟡 - Adaptive racer

### Special Guests
- **Hermes Chaos** 🟣 - Unpredictable wildcard
- **Qwen Technical** 🟢 - Precision driver

## 🛠️ Technical Details

### No Dependencies!
Pure JavaScript - no frameworks or libraries required. Just open and play!

### File Structure
```
js-version/
├── index.html          # Main game page
├── js/
│   ├── config.js      # Game configuration
│   ├── utils.js       # Utility functions
│   ├── car.js         # Car physics & logic
│   ├── track.js       # Track generation
│   ├── powerups.js    # Power-up system
│   ├── weapons.js     # Machine gun combat
│   ├── renderer.js    # Canvas rendering
│   ├── ai.js          # AI driver logic
│   ├── game.js        # Game controller
│   └── main.js        # Entry point
└── README.md          # This file
```

### Performance
- Runs at 60 FPS on modern browsers
- Optimized rendering with minimal overdraw
- Efficient collision detection
- Smart AI updates (2Hz decision rate)

## 🎮 Power-Up Guide

### Offensive 
- ⚡ **Lightning Bolt** - Slows all cars ahead
- 🔴 **Red Shell** - Hits car directly ahead
- 🔵 **Blue Shell** - Targets race leader
- 🍌 **Banana Peel** - Drops trap behind

### Defensive
- 🛡️ **Shield** - Blocks attacks
- 👻 **Ghost** - 3 seconds invincibility

### Boost
- 🚀 **Turbo Boost** - +30% speed for 4s
- 💨 **Nitro** - +50% speed for 2s

### Strategic
- 📡 **Radar** - See opponent data
- ⛽ **Fuel Boost** - +25% fuel
- 🔧 **Tire Repair** - -30% wear

## 🔫 Combat Strategy

- **Limited Ammo** - Use wisely!
- **Range Matters** - Max 300m effective range
- **Target Selection** - AI auto-targets nearest car ahead
- **Damage Stacks** - Multiple hits slow enemies more

## 🏆 Winning Tips

1. **Position Matters** - Different positions get different power-ups
2. **Save Ammo** - Don't waste shots on distant targets
3. **Use Power-Ups Wisely** - Timing is everything
4. **Watch Fuel** - Running out means game over
5. **Lane Changes** - AI will try to overtake

## 🚀 Future Features

- Player control option
- Online multiplayer
- Track editor
- Real LLM integration
- Mobile touch controls
- Replay system

## 📝 Notes

This is a JavaScript port of the Python AI Racing Simulator. While the Python version uses actual LLM APIs (Together AI), this JS version simulates LLM behavior for easy browser play.

Enjoy the race! 🏁