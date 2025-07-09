#!/usr/bin/env python3
"""
Simple Visual Race Demo - Standalone ASCII visualization
"""

import time
import random


class SimpleRacer:
    """Simple racer for visual demo"""
    def __init__(self, name, symbol, style, speed_factor=1.0):
        self.name = name
        self.symbol = symbol
        self.style = style
        self.speed_factor = speed_factor
        self.position = 0
        self.personality_quotes = {
            "Speed Demon": ["Maximum attack!", "Brakes are for quitters!", "Victory or Valhalla!"],
            "Tech Precision": ["Precision is perfection", "Calculating optimal line", "Every millisecond counts"],
            "Fuel Master": ["Efficiency is elegance", "Slow and steady wins", "Conservation is key"],
            "Adaptive Racer": ["Adapting to conditions", "Strike at weakness", "Be like water"],
            "Chaos Cruiser": ["Chaos is opportunity!", "Unpredictable is unstoppable", "Let's get crazy!"]
        }
    
    def get_quote(self):
        """Get a random personality quote"""
        return random.choice(self.personality_quotes.get(self.name, ["Let's race!"]))


def run_visual_race():
    """Run a visual race with ASCII track display"""
    print('🏎️  AI RACING SIMULATOR - VISUAL RACE!')
    print('='*60)
    
    # Create AI racers with different characteristics
    racers = [
        SimpleRacer("Speed Demon", "🏎️", "aggressive", 1.2),
        SimpleRacer("Tech Precision", "🏁", "technical", 1.0),
        SimpleRacer("Fuel Master", "⚡", "conservative", 0.9),
        SimpleRacer("Adaptive Racer", "🎯", "balanced", 1.1),
        SimpleRacer("Chaos Cruiser", "🌪️", "chaotic", 1.0)
    ]
    
    print('🏁 STARTING LINEUP:')
    print('='*30)
    for racer in racers:
        print(f'{racer.symbol} {racer.name} "{racer.style}" racer')
    print()
    
    print('🎙️  PRE-RACE QUOTES:')
    print('='*30)
    for racer in racers:
        print(f'{racer.symbol} {racer.name}: "{racer.get_quote()}"')
    print()
    
    print('🚦 LIGHTS OUT AND AWAY WE GO!')
    print('='*40)
    
    # Race simulation
    race_length = 100
    updates = 10
    
    for update in range(updates):
        print(f'⏱️ RACE UPDATE {update + 1}/{updates}:')
        
        # Update racer positions based on their characteristics
        for racer in racers:
            base_speed = 8
            
            if racer.style == "aggressive":
                # Speed demon: fast but inconsistent
                speed = base_speed * racer.speed_factor * random.uniform(0.8, 1.4)
            elif racer.style == "technical":
                # Tech precision: very consistent
                speed = base_speed * racer.speed_factor * random.uniform(0.95, 1.05)
            elif racer.style == "conservative":
                # Fuel master: steady progress
                speed = base_speed * racer.speed_factor * random.uniform(0.9, 1.1)
            elif racer.style == "balanced":
                # Adaptive racer: adapts to conditions
                speed = base_speed * racer.speed_factor * random.uniform(0.85, 1.25)
            else:  # chaotic
                # Chaos cruiser: wildly unpredictable
                speed = base_speed * racer.speed_factor * random.uniform(0.5, 1.6)
            
            racer.position += speed
            racer.position = min(racer.position, race_length)
        
        # Sort racers by position
        racers.sort(key=lambda x: x.position, reverse=True)
        
        # Create visual track
        track_width = 50
        track = [' '] * track_width
        
        # Place racers on track
        for racer in racers:
            track_pos = min(int((racer.position / race_length) * track_width), track_width - 1)
            if track[track_pos] == ' ':
                track[track_pos] = racer.symbol
            else:
                track[track_pos] = '🔥'  # Battle indicator
        
        # Display track
        print('START' + '┌' + '─' * track_width + '┐' + 'FINISH')
        print('     │' + ''.join(track) + '│')
        print('     └' + '─' * track_width + '┘')
        
        # Show current standings
        print('POSITIONS:')
        for i, racer in enumerate(racers):
            progress = min(int((racer.position / race_length) * 100), 100)
            if progress >= 100:
                status = "FINISHED! 🏁"
            else:
                status = f"{progress}% complete"
            print(f'  {i+1}. {racer.symbol} {racer.name} - {status}')
        
        # Add some personality during the race
        if update == 3:
            leader = racers[0]
            print(f'   💭 {leader.name}: "{leader.get_quote()}"')
        elif update == 6:
            if len(racers) > 1:
                second = racers[1]
                print(f'   💭 {second.name}: "{second.get_quote()}"')
        
        print()
        
        # Check if race is finished
        if any(racer.position >= race_length for racer in racers):
            break
        
        time.sleep(1.2)  # Pause between updates
    
    # Final results
    print('🏁 RACE FINISHED!')
    print('='*40)
    print('🏆 FINAL RESULTS:')
    
    # Sort by final position
    racers.sort(key=lambda x: x.position, reverse=True)
    
    for i, racer in enumerate(racers):
        if i == 0:
            print(f'  🥇 1st: {racer.symbol} {racer.name} - WINNER!')
        elif i == 1:
            print(f'  🥈 2nd: {racer.symbol} {racer.name}')
        elif i == 2:
            print(f'  🥉 3rd: {racer.symbol} {racer.name}')
        else:
            print(f'     {i+1}th: {racer.symbol} {racer.name}')
    
    # Winner celebration
    winner = racers[0]
    print(f'\n🏆 CHAMPION: {winner.name}!')
    print(f'   Style: {winner.style.title()} Racing')
    print(f'   Victory Quote: "{winner.get_quote()}"')
    
    print('\n🎭 PERSONALITY IMPACT:')
    print('  • Speed Demon: Aggressive but risky')
    print('  • Tech Precision: Consistent and reliable')
    print('  • Fuel Master: Steady and efficient')
    print('  • Adaptive Racer: Flexible and strategic')
    print('  • Chaos Cruiser: Unpredictable wildcard')
    
    print('\n✅ Visual race demo complete!')
    print('🏁 This demonstrates the AI personalities in action!')


def main():
    """Main function"""
    try:
        run_visual_race()
    except KeyboardInterrupt:
        print('\n\n🏁 Race interrupted!')
    except Exception as e:
        print(f'\n❌ Error: {e}')


if __name__ == "__main__":
    main()