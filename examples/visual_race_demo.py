#!/usr/bin/env python3
"""
Visual Race Demo - ASCII visualization of AI racing action
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'intelligence'))

from racing_car import RacingCar, DriverStyle
from race_track import RaceTrack
from ai_personalities import AIPersonalitySystem
from enhanced_ai_racers import create_enhanced_ai_racers
import time
import random


def run_visual_race():
    """Run a visual race with ASCII track display"""
    print('🏎️  AI RACING SIMULATOR - VISUAL RACE!')
    print('='*60)

    # Create AI racers
    personality_system = AIPersonalitySystem()
    enhanced_racers = create_enhanced_ai_racers(personality_system)
    cars = [racer.car for racer in enhanced_racers]

    # Car symbols and colors
    car_symbols = ['🏎️', '🏁', '⚡', '🎯', '🌪️']
    car_positions = [0, 0, 0, 0, 0]  # Track position for each car

    print('🏁 STARTING LINEUP:')
    print('='*30)
    for i, car in enumerate(cars):
        racer = enhanced_racers[i]
        print(f'{car_symbols[i]} {car.name} "{racer.profile.nickname}" ({car.driver_style.value})')
    print()

    print('🚦 LIGHTS OUT AND AWAY WE GO!')
    print('='*40)
    
    # Simulate 8 race updates for a full race
    for update in range(8):
        print(f'⏱️ RACE PROGRESS - Update {update + 1}/8:')
        
        # Update positions based on car characteristics and personality
        for i, car in enumerate(cars):
            base_speed = 7  # Base progress per update
            
            # Speed demon advances more aggressively
            if 'Speed Demon' in car.name:
                car_positions[i] += random.randint(9, 14)
            # Chaos cruiser varies wildly (high risk, high reward)
            elif 'Chaos Cruiser' in car.name:
                car_positions[i] += random.randint(4, 16)
            # Tech precision is very consistent
            elif 'Tech Precision' in car.name:
                car_positions[i] += random.randint(8, 10)
            # Fuel master is steady and efficient
            elif 'Fuel Master' in car.name:
                car_positions[i] += random.randint(7, 9)
            # Adaptive racer adapts to conditions
            else:  # Adaptive Racer
                car_positions[i] += random.randint(7, 12)
        
        # Sort by position for standings
        car_data = [(car_positions[i], cars[i], car_symbols[i], enhanced_racers[i]) for i in range(5)]
        car_data.sort(key=lambda x: x[0], reverse=True)
        
        # Create visual track
        track_length = 60
        track = [' '] * track_length
        
        # Place cars on track
        for pos, car, symbol, racer in car_data:
            track_pos = min(int((pos / 80) * track_length), track_length - 1)
            if track[track_pos] == ' ':
                track[track_pos] = symbol
            else:
                track[track_pos] = '🔥'  # Close battle indicator
        
        # Display track
        print('┌' + '─' * track_length + '┐')
        print('│' + ''.join(track) + '│')
        print('└' + '─' * track_length + '┘')
        
        # Show current standings with personality reactions
        print('CURRENT STANDINGS:')
        for i, (pos, car, symbol, racer) in enumerate(car_data):
            progress_percent = min(int((pos / 80) * 100), 100)
            print(f'  {i+1}. {symbol} {car.name} - {progress_percent}% complete')
        
        # Show some AI personality reactions during the race
        if update == 2:
            leader = car_data[0][3]  # Get the racer object
            print(f'   💭 {leader.profile.nickname}: "I\'m in the zone!"')
        elif update == 4:
            if len(car_data) > 1:
                second_place = car_data[1][3]
                print(f'   💭 {second_place.profile.nickname}: "Time to make my move!"')
        elif update == 6:
            last_place = car_data[-1][3]
            print(f'   💭 {last_place.profile.nickname}: "Not giving up yet!"')
        
        print()
        time.sleep(1.5)  # Pause for dramatic effect

    # Final results
    print('🏁 RACE FINISHED!')
    final_standings = sorted(car_data, key=lambda x: x[0], reverse=True)
    print('='*40)
    print('🏆 FINAL RESULTS:')
    
    for i, (pos, car, symbol, racer) in enumerate(final_standings):
        if i == 0:
            print(f'  🥇 P{i+1}: {symbol} {car.name} - WINNER!')
        elif i == 1:
            print(f'  🥈 P{i+1}: {symbol} {car.name}')
        elif i == 2:
            print(f'  🥉 P{i+1}: {symbol} {car.name}')
        else:
            print(f'     P{i+1}: {symbol} {car.name}')

    # Winner celebration
    winner_car, winner_racer = final_standings[0][1], final_standings[0][3]
    print(f'\n🏆 CHAMPION: {winner_car.name}!')
    print(f'   Nickname: "{winner_racer.profile.nickname}"')
    print(f'   Style: {winner_car.driver_style.value.title()}')
    print(f'   Signature Move: {winner_racer.profile.signature_moves[0]}')
    
    # Post-race quote
    personality_system = AIPersonalitySystem()
    victory_quote = personality_system.generate_post_race_quote(winner_racer.profile, 1, {})
    print(f'   Victory Quote: "{victory_quote}"')
    
    print('\n🏁 Visual race demo complete!')
    print('✅ All AI personalities performed according to their characteristics!')


def main():
    """Main function to run the visual race demo"""
    try:
        run_visual_race()
    except KeyboardInterrupt:
        print('\n\n🏁 Race interrupted by user!')
    except Exception as e:
        print(f'\n❌ Error during race: {e}')
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()