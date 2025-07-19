"""
Supporting systems for racing simulation
"""

# Commented out to avoid circular imports - import directly from modules when needed
# from .telemetry import TelemetrySystem, TelemetrySnapshot
# from .challenge_generator import RaceChallengeGenerator, ChallengeType
# from .race_config import ConfigurationManager, DifficultyLevel, RaceMode
# from .championship import ChampionshipManager, DriverStanding

__all__ = [
    'TelemetrySystem',
    'TelemetrySnapshot',
    'RaceChallengeGenerator',
    'ChallengeType',
    'ConfigurationManager',
    'DifficultyLevel',
    'RaceMode',
    'ChampionshipManager',
    'DriverStanding'
]