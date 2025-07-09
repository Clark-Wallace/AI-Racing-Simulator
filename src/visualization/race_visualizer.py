#!/usr/bin/env python3
"""
Race Visualizer - ASCII art visualization of race progress and results
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import math


@dataclass
class RacePosition:
    """Track position data for visualization"""
    car_name: str
    position: int
    lap: int
    distance: float
    gap_to_leader: float
    speed: float
    status: str  # "racing", "pitted", "retired"


class RaceVisualizer:
    """Creates ASCII visualizations of race data"""
    
    def __init__(self, track_length: float = 5.0):
        self.track_length = track_length  # km
        self.car_symbols = {
            "Speed Demon": "🏎️",
            "Tech Precision": "🏁",
            "Fuel Master": "⚡",
            "Adaptive Racer": "🎯",
            "Chaos Cruiser": "🌪️"
        }
        self.position_history = []
        
    def create_track_map(self, positions: List[RacePosition], lap: int, total_laps: int) -> str:
        """Create visual track map showing car positions"""
        track_visual = []
        
        # Header
        track_visual.append(f"\n🏁 LAP {lap}/{total_laps} - TRACK POSITION")
        track_visual.append("=" * 60)
        
        # Create track representation (simple oval)
        track_width = 50
        track_sections = 20
        
        # Place cars on track
        track_display = [" "] * track_sections
        
        for pos_data in positions:
            if pos_data.status == "racing":
                # Calculate position on track (0-1)
                progress = (pos_data.distance % self.track_length) / self.track_length
                section = int(progress * track_sections)
                
                # Get car symbol or abbreviation
                symbol = self.car_symbols.get(pos_data.car_name, "🚗")
                
                # Place on track
                if track_display[section] == " ":
                    track_display[section] = symbol
                else:
                    track_display[section] = "🔥"  # Collision/close racing
        
        # Draw track
        track_visual.append("┌" + "─" * (track_width + 2) + "┐")
        
        # Top straight
        top_line = "│ "
        for i in range(track_sections // 2):
            top_line += track_display[i] + " "
        top_line += " " * (track_width - len(top_line) + 1) + "│"
        track_visual.append(top_line)
        
        # Middle
        track_visual.append("│" + " " * (track_width + 2) + "│")
        
        # Bottom straight (reversed)
        bottom_line = "│ "
        for i in range(track_sections - 1, track_sections // 2 - 1, -1):
            bottom_line += track_display[i] + " "
        bottom_line += " " * (track_width - len(bottom_line) + 1) + "│"
        track_visual.append(bottom_line)
        
        track_visual.append("└" + "─" * (track_width + 2) + "┘")
        
        return "\n".join(track_visual)
    
    def create_standings_board(self, positions: List[RacePosition]) -> str:
        """Create current standings display"""
        board = []
        board.append("\n📊 CURRENT STANDINGS")
        board.append("=" * 50)
        board.append(f"{'Pos':>3} {'Driver':15} {'Gap':>8} {'Speed':>7}")
        board.append("-" * 50)
        
        sorted_positions = sorted(positions, key=lambda x: x.position)
        
        for pos_data in sorted_positions[:10]:  # Top 10
            if pos_data.status == "racing":
                gap_str = "LEADER" if pos_data.position == 1 else f"+{pos_data.gap_to_leader:.1f}s"
                speed_str = f"{pos_data.speed:.0f}kph"
            else:
                gap_str = pos_data.status.upper()
                speed_str = "---"
            
            symbol = self.car_symbols.get(pos_data.car_name, "")
            board.append(f"{pos_data.position:>3}. {symbol} {pos_data.car_name[:12]:12} {gap_str:>8} {speed_str:>7}")
        
        return "\n".join(board)
    
    def create_lap_chart(self, lap_data: Dict[int, List[Tuple[str, int]]]) -> str:
        """Create lap-by-lap position chart"""
        chart = []
        chart.append("\n📈 LAP CHART")
        chart.append("=" * 60)
        
        if not lap_data:
            return "\n".join(chart)
        
        # Get all drivers
        drivers = []
        for positions in lap_data.values():
            for driver, _ in positions:
                if driver not in drivers:
                    drivers.append(driver)
        
        # Header
        header = "Driver         │"
        for lap in sorted(lap_data.keys())[:10]:  # First 10 laps
            header += f" L{lap:>2} │"
        chart.append(header)
        chart.append("─" * len(header))
        
        # Driver rows
        for driver in drivers:
            row = f"{driver[:13]:13} │"
            
            for lap in sorted(lap_data.keys())[:10]:
                positions = lap_data[lap]
                pos = next((p for d, p in positions if d == driver), "-")
                row += f" {pos:>3} │"
            
            chart.append(row)
        
        return "\n".join(chart)
    
    def create_race_summary_graphic(self, race_results: Dict) -> str:
        """Create comprehensive race summary graphic"""
        summary = []
        
        # Title banner
        summary.append("\n" + "🏁" * 30)
        summary.append("🏆 RACE RESULTS SUMMARY 🏆".center(60))
        summary.append("🏁" * 30)
        
        # Podium
        if "positions" in race_results:
            summary.append("\n🥇 PODIUM FINISHERS 🥇")
            summary.append("=" * 40)
            
            podium_display = """
            🥈 2nd 🥈        🥇 1st 🥇        🥉 3rd 🥉
           ┌─────────┐      ┌─────────┐      ┌─────────┐
           │         │      │         │      │         │
           │   {p2}   │      │   {p1}   │      │   {p3}   │
           │         │      │         │      │         │
           └─────────┘      └─────────┘      └─────────┘
            """
            
            p1 = race_results["positions"].get(1, {}).get("name", "---")[:9]
            p2 = race_results["positions"].get(2, {}).get("name", "---")[:9]
            p3 = race_results["positions"].get(3, {}).get("name", "---")[:9]
            
            # Center names in boxes
            p1 = p1.center(9)
            p2 = p2.center(9)
            p3 = p3.center(9)
            
            summary.append(podium_display.format(p1=p1, p2=p2, p3=p3))
        
        # Key statistics
        summary.append("\n📊 RACE STATISTICS")
        summary.append("=" * 40)
        
        if "fastest_lap" in race_results:
            fl = race_results["fastest_lap"]
            summary.append(f"⚡ Fastest Lap: {fl.get('driver', 'Unknown')} - {fl.get('time', 0):.3f}s")
        
        if "events" in race_results:
            overtakes = len([e for e in race_results["events"] if "OVERTAKE" in e.event_type])
            crashes = len([e for e in race_results["events"] if e.event_type == "CRASH"])
            summary.append(f"🔄 Total Overtakes: {overtakes}")
            summary.append(f"💥 Incidents: {crashes}")
        
        # Performance highlights
        summary.append("\n🌟 PERFORMANCE HIGHLIGHTS")
        summary.append("=" * 40)
        
        # Find biggest gainer/loser
        if "positions" in race_results and "starting_grid" in race_results:
            gains = []
            for pos, data in race_results["positions"].items():
                driver = data["name"]
                start_pos = next((i for i, d in enumerate(race_results["starting_grid"]) 
                                if d.name == driver), pos) + 1
                gain = start_pos - pos
                gains.append((driver, gain))
            
            gains.sort(key=lambda x: x[1], reverse=True)
            
            if gains:
                best_gain = gains[0]
                worst_gain = gains[-1]
                
                if best_gain[1] > 0:
                    summary.append(f"📈 Biggest Gainer: {best_gain[0]} (+{best_gain[1]} positions)")
                if worst_gain[1] < 0:
                    summary.append(f"📉 Biggest Loser: {worst_gain[0]} ({worst_gain[1]} positions)")
        
        return "\n".join(summary)
    
    def create_battle_visualization(self, car1: str, car2: str, gap: float) -> str:
        """Visualize close battle between two cars"""
        visual = []
        
        visual.append(f"\n⚔️  BATTLE: {car1} vs {car2}")
        visual.append("─" * 40)
        
        # Create visual gap representation
        gap_visual = ""
        if gap < 0.5:
            gap_visual = f"{self.car_symbols.get(car1, '🏎️')}{self.car_symbols.get(car2, '🏁')} SIDE BY SIDE!"
        elif gap < 1.0:
            gap_visual = f"{self.car_symbols.get(car1, '🏎️')} {'.' * 3} {self.car_symbols.get(car2, '🏁')} Gap: {gap:.2f}s"
        else:
            dots = min(int(gap * 3), 15)
            gap_visual = f"{self.car_symbols.get(car1, '🏎️')} {'.' * dots} {self.car_symbols.get(car2, '🏁')} Gap: {gap:.2f}s"
        
        visual.append(gap_visual)
        
        return "\n".join(visual)
    
    def create_telemetry_display(self, car_name: str, telemetry_data: Dict) -> str:
        """Create telemetry data visualization"""
        display = []
        
        display.append(f"\n📊 TELEMETRY: {car_name}")
        display.append("=" * 50)
        
        # Speed gauge
        speed = telemetry_data.get("speed", 0)
        max_speed = 380
        speed_bars = int((speed / max_speed) * 20)
        speed_gauge = f"Speed: [{'█' * speed_bars}{'░' * (20 - speed_bars)}] {speed:.0f} km/h"
        display.append(speed_gauge)
        
        # Fuel gauge
        fuel = telemetry_data.get("fuel_level", 0)
        fuel_bars = int((fuel / 60) * 20)  # Assuming 60L tank
        fuel_gauge = f"Fuel:  [{'█' * fuel_bars}{'░' * (20 - fuel_bars)}] {fuel:.1f}L"
        display.append(fuel_gauge)
        
        # Tire wear
        tire_wear = telemetry_data.get("tire_wear", 0)
        tire_bars = int((1 - tire_wear) * 20)  # Inverse for tire condition
        tire_gauge = f"Tires: [{'█' * tire_bars}{'░' * (20 - tire_bars)}] {(1-tire_wear)*100:.0f}%"
        display.append(tire_gauge)
        
        # Performance metrics
        display.append("\nPerformance Metrics:")
        display.append(f"  Lap Time: {telemetry_data.get('lap_time', 0):.3f}s")
        display.append(f"  Sector 1: {telemetry_data.get('sector1', 0):.3f}s")
        display.append(f"  Sector 2: {telemetry_data.get('sector2', 0):.3f}s")
        display.append(f"  Sector 3: {telemetry_data.get('sector3', 0):.3f}s")
        
        return "\n".join(display)
    
    def create_championship_progression(self, standings_history: List[Dict[str, int]]) -> str:
        """Create championship points progression chart"""
        chart = []
        
        chart.append("\n📈 CHAMPIONSHIP PROGRESSION")
        chart.append("=" * 60)
        
        if not standings_history:
            return "\n".join(chart)
        
        # Get all drivers
        drivers = list(standings_history[0].keys())
        
        # Find max points for scaling
        max_points = max(max(round_standings.values()) for round_standings in standings_history)
        
        # Create progression for each driver
        for driver in drivers[:5]:  # Top 5
            line = f"{driver[:12]:12} │"
            
            for round_standings in standings_history:
                points = round_standings.get(driver, 0)
                # Simple bar representation
                bars = int((points / max_points) * 10) if max_points > 0 else 0
                line += "█" * bars + "░" * (10 - bars) + f" {points:>3} │"
            
            chart.append(line)
        
        # X-axis labels
        chart.append(" " * 13 + "└" + "─" * (len(standings_history) * 15))
        labels = " " * 15
        for i in range(len(standings_history)):
            labels += f"R{i+1}".center(15)
        chart.append(labels)
        
        return "\n".join(chart)


def demo_visualizer():
    """Demonstrate visualizer capabilities"""
    visualizer = RaceVisualizer()
    
    # Sample race positions
    positions = [
        RacePosition("Speed Demon", 1, 10, 45.5, 0.0, 285, "racing"),
        RacePosition("Tech Precision", 2, 10, 45.1, 0.4, 283, "racing"),
        RacePosition("Fuel Master", 3, 10, 44.8, 0.7, 280, "racing"),
        RacePosition("Adaptive Racer", 4, 10, 44.2, 1.3, 278, "racing"),
        RacePosition("Chaos Cruiser", 5, 10, 43.9, 1.6, 275, "racing")
    ]
    
    # Track map
    print(visualizer.create_track_map(positions, 10, 20))
    
    # Standings board
    print(visualizer.create_standings_board(positions))
    
    # Battle visualization
    print(visualizer.create_battle_visualization("Speed Demon", "Tech Precision", 0.4))
    
    # Sample telemetry
    telemetry = {
        "speed": 285,
        "fuel_level": 45.2,
        "tire_wear": 0.15,
        "lap_time": 92.456,
        "sector1": 28.123,
        "sector2": 35.789,
        "sector3": 28.544
    }
    print(visualizer.create_telemetry_display("Speed Demon", telemetry))


if __name__ == "__main__":
    demo_visualizer()