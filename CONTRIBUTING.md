# Contributing to AI Racing Simulator

We welcome contributions to the AI Racing Simulator! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please read it before contributing.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a branch for your changes
5. Make your changes
6. Test your changes
7. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git

### Installation

```bash
# Clone your fork
git clone https://github.com/yourusername/ai-racing-simulator.git
cd ai-racing-simulator

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install the package in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
python tests/test_racing.py
```

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-track-type`
- `bugfix/fix-fuel-consumption`
- `enhancement/improve-ai-personalities`
- `docs/update-readme`

### Commit Messages

Write clear, concise commit messages:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 50 characters
- Reference issues and pull requests when applicable

Example:
```
Add weather effects to track performance

- Implement rain, fog, and storm conditions
- Add performance modifiers for each weather type
- Update track visualization for weather states
- Add tests for weather system

Closes #123
```

### Code Style

We use several tools to maintain code quality:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## Testing

### Test Structure

- Place tests in the `tests/` directory
- Mirror the source structure in tests
- Use descriptive test names
- Include both positive and negative test cases

### Test Categories

1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test component interactions
3. **System Tests**: Test complete workflows
4. **Performance Tests**: Test efficiency and scalability

### Writing Tests

```python
import pytest
from src.core.racing_car import RacingCar, DriverStyle

def test_racing_car_acceleration():
    """Test that racing car accelerates correctly"""
    car = RacingCar("Test Car", 300, 3.5, 0.8, 12, DriverStyle.BALANCED)
    
    initial_speed = car.current_speed
    car.accelerate(1.0)  # 1 second
    
    assert car.current_speed > initial_speed
    assert car.current_speed <= car.top_speed

def test_racing_car_fuel_consumption():
    """Test fuel consumption during racing"""
    car = RacingCar("Test Car", 300, 3.5, 0.8, 12, DriverStyle.BALANCED)
    initial_fuel = car.fuel_level
    
    car.consume_fuel(10.0)  # 10 km
    
    assert car.fuel_level < initial_fuel
    assert car.fuel_level >= 0
```

## Submitting Changes

### Pull Request Process

1. Update documentation if needed
2. Add tests for new functionality
3. Ensure all tests pass
4. Update the changelog if significant changes
5. Submit pull request with clear description

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## Project Structure

```
ai-racing-simulator/
├── src/
│   ├── core/           # Core racing engine
│   ├── intelligence/   # AI systems
│   ├── systems/        # Supporting systems
│   └── visualization/  # Demos and graphics
├── tests/              # Test suite
├── docs/               # Documentation
├── examples/           # Usage examples
└── data/               # Configuration files
```

## Coding Standards

### Python Style Guide

- Follow PEP 8
- Use type hints for all functions
- Write docstrings for all public functions
- Use dataclasses for data structures
- Use enums for constants

### Documentation

- Update README.md for significant changes
- Add docstrings to all public functions
- Include examples in docstrings
- Update API documentation

### Performance Considerations

- Profile performance-critical code
- Use appropriate data structures
- Minimize memory allocations in tight loops
- Consider algorithmic complexity

## Areas for Contribution

### High Priority

- **Performance Optimization**: Improve simulation speed
- **New Track Types**: Add more racing circuits
- **AI Personalities**: Expand personality system
- **Visualization**: Enhance graphics and displays

### Medium Priority

- **Testing**: Increase test coverage
- **Documentation**: Improve examples and guides
- **Configuration**: Add more customization options
- **Data Analysis**: Enhance telemetry features

### Low Priority

- **Multiplayer**: Add human vs AI racing
- **Export Features**: Add data export formats
- **Advanced AI**: Machine learning integration
- **Mobile Support**: Optimize for mobile devices

## Resources

- [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Type Hints](https://docs.python.org/3/library/typing.html)
- [Testing Best Practices](https://docs.pytest.org/en/stable/)
- [Git Workflow](https://guides.github.com/introduction/flow/)

## Questions?

If you have questions about contributing:

1. Check existing issues and discussions
2. Create a new issue for bugs or feature requests
3. Start a discussion for general questions
4. Contact the maintainers directly

Thank you for contributing to AI Racing Simulator! 🏎️