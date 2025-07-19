"""
AI Configuration for LLM Racing Drivers
Uses the Nexus Connector with Together AI for Llama models
"""

import os
from dotenv import load_dotenv
from nexus import NexusConnector, AIProvider

load_dotenv()

class RacingAI:
    """AI configuration for LLM-powered racing drivers"""
    
    def __init__(self, model_name: str = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"):
        """Initialize with specific Together AI model"""
        self.model_name = model_name
        self.agent = NexusConnector(
            provider=AIProvider.OPENAI,
            api_key=os.getenv("TOGETHER_API_KEY"),
            model=model_name,
            base_url="https://api.together.xyz/v1",  # Together AI OpenAI-compatible endpoint
            workspace="./ai_racing_output",
            auto_execute=False,  # We just want responses, not file execution
            max_iterations=1,    # Single response per decision
            verbose=False        # Keep racing output clean
        )
    
    async def make_racing_decision(self, race_state: dict, personality: str) -> dict:
        """Make a racing decision based on comprehensive race state"""
        
        # Extract rich telemetry data
        basic_state = race_state.get('basic', {})
        pit_analysis = race_state.get('pit_analysis', {})
        overtake_analysis = race_state.get('overtake_analysis', {})
        tire_prediction = race_state.get('tire_prediction', {})
        fuel_strategy = race_state.get('fuel_strategy', {})
        weather_impact = race_state.get('weather_impact', {})
        performance = race_state.get('performance_envelope', {})
        power_ups = race_state.get('power_ups', {})
        collision_risk = race_state.get('collision_risk', {})
        weapons = race_state.get('weapons', {})
        
        prompt = f"""You are an AI racing driver with this personality: {personality}

RACE SITUATION:
- Position: {basic_state.get('position', 'unknown')}/{basic_state.get('total_cars', 5)}
- Lap: {basic_state.get('current_lap', 1)}/{basic_state.get('total_laps', 10)}
- Gap ahead: {basic_state.get('gap_ahead', 'unknown')}m | Gap behind: {basic_state.get('gap_behind', 'unknown')}m
- Track: {basic_state.get('track_segment', 'mixed')} | Weather: {basic_state.get('weather', 'clear')}

TELEMETRY ANALYSIS:
Fuel Strategy: {fuel_strategy.get('strategy', 'manage')} - Can finish: {fuel_strategy.get('can_finish', True)}
Tire Condition: {tire_prediction.get('degradation_level', 'unknown')} wear, critical lap {tire_prediction.get('critical_lap', 'N/A')}
Pit Recommendation: {"YES" if pit_analysis.get('recommended', False) else "NO"} ({pit_analysis.get('urgency', 'low')} urgency)
Overtake Opportunity: {overtake_analysis.get('success_probability', 0)*100:.0f}% success, {"HIGH" if overtake_analysis.get('risk_level', 0) > 1 else "LOW"} risk
Weather Impact: {weather_impact.get('adaptation_level', 'medium')} adaptation, {weather_impact.get('speed_factor', 1.0)*100:.0f}% speed

PERFORMANCE ENVELOPE:
Top Speed: {performance.get('speed_metrics', {}).get('top_speed', 'unknown')} km/h
Corner Speed: {performance.get('speed_metrics', {}).get('corner_speed_90', 'unknown')} km/h (hard corners)
Current Fuel: {performance.get('efficiency_metrics', {}).get('current_fuel', 'unknown')}%
Tire Condition: {performance.get('efficiency_metrics', {}).get('tire_condition', 'unknown')}%

MARIO KART POWER-UPS:
Inventory: {power_ups.get('inventory', [])}
Strategy Recommendation: {power_ups.get('strategy', {}).get('recommendation', 'none')} 
Best Item: {power_ups.get('strategy', {}).get('item_name', 'none')}
Strategy Value: {power_ups.get('strategy', {}).get('value', 0)*100:.0f}%

COLLISION RISK:
Risk Level: {collision_risk.get('risk_level', 'none').upper()}
Risk Factor: {collision_risk.get('risk_factor', 0)*100:.0f}%
Nearby Cars: {collision_risk.get('nearby_cars', 0)}
WEAPONS SYSTEM:
Machine Gun Ammo: {weapons.get('ammo', 50)}/50 rounds
Can Fire: {"YES" if weapons.get('can_fire', False) else "NO"}
Target Ahead: {weapons.get('target_ahead', 'None')}
Target Distance: {weapons.get('target_distance', 999)}m
⚠️ IMPORTANT: Use FIRE or SHOOT action when you have a target within 200m!

EXAMPLE: If Target Ahead is "Llama Speed" at 150m and you Can Fire: YES, then use action: "FIRE"

STRATEGIC OPTIONS:
- ATTACK: Aggressive overtake (uses extra fuel/tires, high risk/reward)
- DEFEND: Block passing attempts (moderate energy, positional)
- CONSERVE: Save fuel/tires for late race (slow but sustainable)
- PRESSURE: Apply psychological pressure (slight energy cost, strategic)
- WAIT: Patient approach (minimal energy, opportunity-based)
- USE_POWERUP: Use your best power-up item strategically
- OVERTAKE: Pure overtaking move (high speed, high fuel cost)
- PASS: Clean passing maneuver (aggressive speed boost)
- BLOCK: Defensive blocking (slower speed)
- BOOST: Maximum speed boost (highest fuel consumption)
- HOLD: Maintain position (neutral pace)
- SAVE: Maximum conservation (slowest, saves fuel)
- FIRE/SHOOT: Fire machine gun at target ahead (slows them by 15%, uses ammo)

POWER-UP EFFECTS:
🟢 Defensive: Shield (blocks attacks), Ghost (invincible), Banana (trap)
🔴 Offensive: Lightning (slow leaders), Red Shell (hit ahead), Blue Shell (hit leader)
⚡ Boost: Turbo (+30% speed), Nitro (+50% speed)
🔧 Utility: Fuel Boost, Tire Repair, Radar (intel)

Consider your personality, telemetry data, power-ups, and collision risk.

Respond with ONLY a JSON object:
{{
    "action": "YOUR_CHOSEN_ACTION",
    "confidence": 0.0-1.0,
    "reasoning": "Strategy rationale (max 15 words)",
    "use_powerup": true/false
}}"""

        try:
            result = await self.agent.execute_task(prompt)
            
            # Handle None result
            if result is None:
                return {
                    "action": "WAIT",
                    "confidence": 0.3,
                    "reasoning": "No AI response"
                }
            
            # Parse the response to extract the JSON
            import json
            
            # Extract the actual content from TaskResult
            response_text = None
            if hasattr(result, 'messages') and result.messages:
                # Get the last assistant message
                try:
                    last_msg = result.messages[-1]
                    response_text = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
                except (IndexError, AttributeError):
                    response_text = None
            elif hasattr(result, 'output'):
                response_text = result.output
            elif hasattr(result, 'content'):
                response_text = result.content
            else:
                response_text = str(result)
            
            if response_text is None or response_text == "None":
                return {
                    "action": "WAIT",
                    "confidence": 0.3,
                    "reasoning": "Empty AI response"
                }
            
            # Try to extract JSON from the response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response_text[start:end]
                parsed = json.loads(json_str)
                
                # Ensure required fields exist
                if "action" not in parsed or parsed["action"] is None:
                    parsed["action"] = "WAIT"
                if "confidence" not in parsed:
                    parsed["confidence"] = 0.5
                if "reasoning" not in parsed:
                    parsed["reasoning"] = "AI response"
                    
                return parsed
            else:
                # Fallback if no JSON found
                return {
                    "action": "WAIT", 
                    "confidence": 0.5,
                    "reasoning": "Failed to parse AI response"
                }
        except Exception as e:
            print(f"🚨 AI decision error: {e}")
            return {
                "action": "WAIT",
                "confidence": 0.3,
                "reasoning": f"AI error: {str(e)[:20]}"
            }
    
    async def generate_race_commentary(self, event: dict, personality: str) -> str:
        """Generate race commentary for events"""
        prompt = f"""You are a racing driver with personality: {personality}
        
React to this event: {event['type']}
Details: {event['details']}

Respond with a SHORT racing driver quote (max 10 words) that fits your personality."""

        try:
            result = await self.agent.execute_task(prompt)
            response = result.output if hasattr(result, 'output') else str(result)
            # Clean up the response
            return response.strip()[:50]  # Max 50 chars
        except Exception as e:
            return "Let's race!"

# Pre-configured AI instances for different models
LLAMA_MODELS = {
    "speed": {
        "model": "meta-llama/Llama-3.2-3B-Instruct-Turbo",
        "personality": "Fast and aggressive racer. Takes risks for speed. Hates being behind."
    },
    "strategic": {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo", 
        "personality": "Calculated and strategic. Plans moves ahead. Values efficiency over speed."
    },
    "balanced": {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "personality": "Adaptable racer. Balances risk and reward. Reads the race flow."
    },
    "chaotic": {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "personality": "Unpredictable wildcard. Makes surprising moves. Thrives in chaos."
    },
    "technical": {
        "model": "Qwen/Qwen2.5-72B-Instruct-Turbo",
        "personality": "Precision driver. Perfect racing lines. Maximizes car performance."
    }
}