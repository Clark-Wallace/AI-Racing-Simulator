# AI Racing Simulator 🏎️

A comprehensive AI racing simulator where 5 unique AI personalities compete in dynamic races with realistic physics, telemetry analysis, and strategic intelligence gathering.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🌟 Features

### 🎭 AI Personalities
- **5 Unique Characters** with distinct driving styles, emotions, and backstories
- **Dynamic Relationships** including rivalries and respect systems
- **Emotional States** that affect performance and decision-making
- **Signature Moves** and catchphrases unique to each personality

### 🏎️ Racing Physics
- **Realistic Simulation** with fuel consumption, tire wear, and weather effects
- **4 Track Types** - Speed, Technical, Mixed, and Endurance circuits
- **Dynamic Conditions** including weather changes and track evolution
- **Strategic Elements** like pit stops, fuel management, and tire strategy

### 📊 Advanced Analytics
- **Comprehensive Telemetry** with 20+ performance metrics across 5 categories
- **Intelligence Gathering** where race winners gain access to competitor data
- **Strategic Analysis** with weakness identification and counter-strategies
- **Performance Tracking** with detailed race history and statistics

### 🏆 Championship Management
- **Full Season Support** with multi-race championships and standings
- **Team Championships** with constructor standings and team dynamics
- **Flexible Configuration** with 5 difficulty levels and custom presets
- **Special Rules** including sprint races, double points, and fastest lap bonuses

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-racing-simulator.git
cd ai-racing-simulator

# No additional dependencies needed - pure Python!
```

### Running the Simulator

#### Easy Demo Runner
```bash
python run_demo.py
```

This will show you a menu with options:
1. Quick Race Example
2. Custom Championship  
3. Telemetry Analysis
4. **Visual Race Demo (NEW!)** - See the cars race with ASCII graphics
5. Complete System Showcase
6. Grand Prix Finale
7. Run All Tests

#### Direct Examples
```bash
python examples/quick_race.py           # Quick race demo
python examples/visual_race_demo.py     # Visual ASCII race
python examples/custom_championship.py  # Championship demo
python examples/telemetry_analysis.py   # Performance analysis
```

#### Individual System Tests
```bash
python tests/test_racing.py      # Phase 1: Core Racing
python tests/test_telemetry.py   # Phase 2: Telemetry
python tests/test_challenges.py  # Phase 3: Challenges
python tests/test_data_prizes.py # Phase 4: Data Prizes
python tests/test_intelligence.py # Phase 5: Intelligence
python tests/test_personalities.py # Phase 6: Personalities
python tests/test_config.py      # Phase 7: Configuration
```

## 🎭 Meet the AI Racers

### 🔥 Speed Demon - "Mad Max"
- **Style**: Aggressive, risk-taking hothead
- **Strengths**: Overtaking, high-speed sections
- **Weaknesses**: Crash-prone, poor fuel efficiency
- **Quote**: "Brakes are for quitters!"

### 🔧 Tech Precision - "The Professor"
- **Style**: Calculated, precise, analytical
- **Strengths**: Cornering, consistency, technical tracks
- **Weaknesses**: Struggles with unpredictable situations
- **Quote**: "Precision is perfection."

### 🌱 Fuel Master - "The Economist"
- **Style**: Conservative, efficient, strategic
- **Strengths**: Fuel efficiency, tire management, endurance
- **Weaknesses**: Lacks outright speed
- **Quote**: "Efficiency is the ultimate performance."

### 🎯 Adaptive Racer - "The Chameleon"
- **Style**: Mysterious, strategic, adaptable
- **Strengths**: Adapts to any situation, strategic thinking
- **Weaknesses**: Unpredictable performance
- **Quote**: "Adaptation is evolution."

### 🌪️ Chaos Cruiser - "The Tornado"
- **Style**: Unpredictable, entertaining, wild
- **Strengths**: Thrives in chaotic conditions
- **Weaknesses**: Inconsistent, unreliable
- **Quote**: "Chaos is just another word for opportunity!"

## 📁 Project Structure

```
ai-racing-simulator/
├── src/
│   ├── core/                    # Core racing engine
│   │   ├── racing_car.py        # Car physics and AI drivers
│   │   ├── race_track.py        # Track modeling and weather
│   │   ├── race_simulator.py    # Basic race simulation
│   │   └── intelligent_race_simulator.py  # Enhanced simulation
│   ├── intelligence/            # AI personality and intelligence
│   │   ├── ai_personalities.py  # Personality system
│   │   ├── enhanced_ai_racers.py # Personality integration
│   │   ├── race_intelligence.py # Strategic AI decisions
│   │   └── data_prizes.py       # Intelligence gathering
│   ├── systems/                 # Supporting systems
│   │   ├── telemetry.py         # Performance metrics
│   │   ├── challenge_generator.py # Challenge creation
│   │   ├── race_config.py       # Configuration management
│   │   └── championship.py      # Season management
│   └── visualization/           # Demos and visualization
│       ├── race_visualizer.py   # ASCII race graphics
│       ├── showcase_finale.py   # System demonstration
│       └── grand_prix_finale.py # Ultimate championship
├── tests/                       # Comprehensive test suite
├── docs/                        # Documentation
├── examples/                    # Usage examples
├── data/                        # Configuration and data files
└── README.md                    # This file
```

## 🎮 Usage Examples

### Custom Race Configuration
```python
from src.systems.race_config import ConfigurationManager, RaceSettings
from src.systems.race_config import DifficultyLevel, TrackType

# Create configuration manager
config_manager = ConfigurationManager()

# Create custom race
config = config_manager.create_custom_config("My Custom Race")
config.race_settings.track_type = TrackType.TECHNICAL_TRACK
config.race_settings.laps = 20
config.race_settings.weather = "rain"
config.ai_settings.difficulty = DifficultyLevel.EXPERT

# Save configuration
config_manager.save_config(config)
```

### Running a Championship
```python
from src.systems.championship import ChampionshipManager
from src.systems.race_config import ChampionshipSettings, RaceSettings
from src.intelligence.enhanced_ai_racers import create_enhanced_ai_racers
from src.intelligence.ai_personalities import AIPersonalitySystem

# Create AI racers
personality_system = AIPersonalitySystem()
enhanced_racers = create_enhanced_ai_racers(personality_system)
cars = [racer.car for racer in enhanced_racers]

# Create championship
settings = ChampionshipSettings(
    name="My Championship",
    races=[
        RaceSettings(track_type=TrackType.SPEED_TRACK, laps=10),
        RaceSettings(track_type=TrackType.TECHNICAL_TRACK, laps=15),
        RaceSettings(track_type=TrackType.MIXED_TRACK, laps=12)
    ]
)

# Run championship
drivers = [car.name for car in cars]
championship = ChampionshipManager(settings, drivers, personality_system)

for race in range(len(settings.races)):
    race_record = championship.run_next_race(cars)
    print(f"Race {race + 1} winner: {race_record.positions[1]}")
```

### Analyzing Performance Data
```python
from src.intelligence.data_prizes import DataPrizeSystem
from src.systems.telemetry import TelemetrySystem

# Create systems
prize_system = DataPrizeSystem()
telemetry = TelemetrySystem()

# After a race, analyze competitor
intelligence = prize_system.analyze_competitor("Speed Demon")
print(f"Strengths: {intelligence.strengths}")
print(f"Weaknesses: {intelligence.weaknesses}")
print(f"Counter-strategy: {intelligence.counter_strategy}")
```

## 🏆 Technical Achievements

### Zero Dependencies
- **Pure Python**: No external libraries required
- **Lightweight**: ~6000+ lines of efficient code
- **Portable**: Runs on any Python 3.7+ environment

### Advanced AI Systems
- **Personality Simulation**: Complex emotional and behavioral modeling
- **Strategic Intelligence**: Multi-layered decision-making systems
- **Emergent Narratives**: AI interactions create compelling storylines

### Performance Optimized
- **Real-time Simulation**: Efficient physics calculations
- **Scalable Architecture**: Modular design supports expansion
- **Memory Efficient**: Optimized data structures and algorithms

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python tests/test_racing.py        # Core racing engine
python tests/test_personalities.py # AI personality system
python tests/test_config.py        # Configuration system
```

## 📊 Performance Metrics

### Telemetry Categories
- **Speed Metrics**: Top speed, acceleration, consistency
- **Handling Metrics**: Cornering, stability, precision
- **Efficiency Metrics**: Fuel consumption, tire management
- **Strategic Metrics**: Overtaking, defensive ability, intelligence
- **Technical Metrics**: Consistency, error rate, adaptability

### Data Prize System
- **Position-based Access**: Winners gain competitor intelligence
- **Intelligence Analysis**: Automated weakness identification
- **Counter-strategies**: AI-generated tactical recommendations
- **Behavioral Patterns**: Performance trend analysis

## 🎯 Future Enhancements

### Potential Additions
- **Multiplayer Support**: Human vs AI racing
- **Advanced Graphics**: 2D/3D visualization
- **Machine Learning**: Adaptive AI improvement
- **Online Leagues**: Multiplayer championships
- **VR Integration**: Immersive racing experience

### Extensibility
- **Plugin System**: Custom challenges and tracks
- **Mod Support**: User-defined AI personalities
- **API Integration**: External data sources
- **Export Tools**: Advanced analytics platforms

## 🤝 Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-racing-simulator.git

# Install development dependencies
pip install -e .[dev]

# Run tests
python -m pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Acknowledgments

- Inspired by real-world Formula 1 racing dynamics
- Built with love for AI and motorsports
- Special thanks to the Python community

---

**🏁 Ready to race? Choose your champion and may the best AI win! 🏆**

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-racing-simulator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-racing-simulator/discussions)
- **Documentation**: [Full Documentation](docs/README.md)