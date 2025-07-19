// AI driver logic
class AIDriver {
    constructor(car, model = 'rule-based') {
        this.car = car;
        this.model = model;
        this.personality = car.style.name.toUpperCase();
        
        // Decision making
        this.lastDecisionTime = 0;
        this.currentDecision = { action: 'ACCELERATE', confidence: 1.0 }; // Start racing immediately!
        
        // For LLM simulation (in real implementation, would call API)
        this.decisionHistory = [];
    }
    
    update(deltaTime, gameState) {
        const now = Date.now();
        
        // Always ensure car is moving if too slow
        if (this.car.speed < 30) {
            this.currentDecision = { action: 'ACCELERATE', confidence: 1.0 };
        }
        
        // Make decisions at regular intervals
        if (now - this.lastDecisionTime >= CONFIG.AI.DECISION_INTERVAL) {
            this.lastDecisionTime = now;
            this.makeDecision(gameState);
        }
        
        // Execute current decision
        this.executeDecision(deltaTime, gameState);
    }
    
    makeDecision(gameState) {
        if (this.model === 'llm') {
            // Simulate LLM decision (in real implementation, would call Together AI)
            this.makeLLMDecision(gameState);
        } else {
            // Rule-based AI
            this.makeRuleBasedDecision(gameState);
        }
    }
    
    makeRuleBasedDecision(gameState) {
        const { track, cars, weaponsManager, powerUpManager } = gameState;
        
        // Get race situation
        const position = this.car.position;
        const fuel = this.car.fuel / CONFIG.CAR.FUEL_CAPACITY;
        const ammo = this.car.machineGun.ammo / CONFIG.WEAPONS.AMMO_COUNT;
        
        // Find target ahead
        const targetInfo = weaponsManager.getTargetAhead(this.car, cars, track);
        
        // Default to accelerate to prevent stuck cars
        let action = 'ACCELERATE';
        let confidence = 0.7;
        
        // Ensure car is moving
        if (this.car.speed < 50) {
            action = 'ACCELERATE';
            confidence = 0.9;
        } else {
            switch (this.personality) {
                case 'AGGRESSIVE':
                    action = 'ACCELERATE'; // Always pushing
                    if (targetInfo && targetInfo.distance < 100) {
                        if (weaponsManager.shouldFire(this.car, targetInfo, this.personality)) {
                            action = 'FIRE';
                        }
                    }
                    confidence = 0.9;
                    break;
                    
                case 'STRATEGIC':
                    action = 'ACCELERATE'; // Default to moving
                    if (fuel < 0.2 && this.car.speed > 200) {
                        action = 'CONSERVE';
                        confidence = 0.8;
                    } else if (targetInfo && targetInfo.distance < 50 && this.car.speed > 100) {
                        // Only defend if we're already moving well
                        action = 'DEFEND';
                    }
                    break;
                    
                case 'BALANCED':
                    action = 'ACCELERATE';
                    if (targetInfo && targetInfo.distance < 150) {
                        if (Math.random() > 0.5) { // More aggressive
                            action = 'ATTACK';
                        }
                    }
                    confidence = 0.8;
                    break;
                    
                case 'CHAOTIC':
                    // Mostly accelerate with occasional chaos
                    const actions = ['ACCELERATE', 'ACCELERATE', 'ACCELERATE', 'ATTACK', 'FIRE'];
                    action = actions[Math.floor(Math.random() * actions.length)];
                    confidence = 0.7 + Math.random() * 0.3;
                    // Don't swerve if going too slow
                    if (this.car.speed < 100 && action === 'SWERVE') {
                        action = 'ACCELERATE';
                    }
                    break;
                    
                case 'TECHNICAL':
                    // Precise driving but always moving
                    action = 'ACCELERATE'; // Default
                    const segmentType = track.getSegmentType(this.car.trackProgress);
                    if (segmentType === 'corner' && this.car.speed > 250) {
                        // Only brake in corners if going very fast
                        action = 'BRAKE';
                        confidence = 0.7;
                    }
                    break;
                    
                default:
                    action = 'ACCELERATE';
            }
        }
        
        // Power-ups are now permanent, no need to use them
        
        this.currentDecision = { action, confidence };
    }
    
    makeLLMDecision(gameState) {
        // Simulate LLM reasoning
        const { track, cars, weaponsManager } = gameState;
        
        // Prepare race state for LLM
        const targetInfo = weaponsManager.getTargetAhead(this.car, cars, track);
        const raceState = {
            position: this.car.position,
            totalCars: cars.length,
            lap: this.car.lap,
            fuel: Math.round(this.car.fuel),
            ammo: this.car.machineGun.ammo,
            targetAhead: targetInfo ? targetInfo.car.name : null,
            targetDistance: targetInfo ? Math.round(targetInfo.distance) : 999,
            powerUps: this.car.powerUps.map(p => p.name),
            speed: Math.round(this.car.speed)
        };
        
        // Simulate LLM response based on model
        let action = 'WAIT';
        let reasoning = '';
        
        // Ensure cars are always moving forward
        if (this.car.speed < 30) {
            action = 'ACCELERATE';
            reasoning = 'Need to get moving!';
        } else {
            switch (this.car.name) {
                case 'Llama Speed':
                    action = 'ACCELERATE';
                    if (targetInfo && targetInfo.distance < 200) {
                        action = 'FIRE';
                        reasoning = 'Target in range, engaging!';
                    } else {
                        reasoning = 'Full speed ahead!';
                    }
                    break;
                    
                case 'Llama Strategic':
                    action = 'ACCELERATE'; // Default to moving
                    if (this.car.fuel < 20) {
                        action = 'CONSERVE';
                        reasoning = 'Managing fuel for finish';
                    } else if (targetInfo && targetInfo.distance < 100) {
                        action = 'FIRE';
                        reasoning = 'Tactical shot opportunity';
                    } else {
                        reasoning = 'Strategic positioning';
                    }
                    break;
                    
                case 'Llama Balanced':
                    action = 'ACCELERATE'; // Always be moving
                    if (raceState.position > 3) {
                        action = 'ATTACK';
                        reasoning = `Pushing from P${raceState.position}`;
                    } else {
                        reasoning = `Maintaining P${raceState.position}`;
                    }
                    break;
                    
                case 'Hermes Chaos':
                    // Weight towards movement actions - less swerving
                    const chaosActions = ['ACCELERATE', 'ACCELERATE', 'ACCELERATE', 'ATTACK', 'FIRE'];
                    action = chaosActions[Math.floor(Math.random() * chaosActions.length)];
                    // Only occasionally swerve when at good speed
                    if (Math.random() < 0.1 && this.car.speed > 150) {
                        action = 'SWERVE';
                    }
                    reasoning = 'Controlled chaos!';
                    break;
                    
                case 'Qwen Technical':
                    const segment = track.getSegmentType(this.car.trackProgress);
                    // Only brake in corners if going too fast
                    if (segment === 'corner' && this.car.speed > 250) {
                        action = 'BRAKE';
                        reasoning = 'Corner braking';
                    } else {
                        action = 'ACCELERATE';
                        reasoning = `Accelerating through ${segment}`;
                    }
                    break;
                    
                default:
                    action = 'ACCELERATE';
                    reasoning = 'Moving forward';
            }
        }
        
        this.currentDecision = {
            action,
            confidence: 0.7 + Math.random() * 0.3,
            reasoning
        };
        
        // Log decision (only occasionally to avoid spam)
        if (Math.random() < 0.05) {
            console.log(`💭 ${this.car.name}: ${action} - ${reasoning}`);
        }
    }
    
    executeDecision(deltaTime, gameState) {
        const { weaponsManager, powerUpManager, cars, track } = gameState;
        const action = this.currentDecision.action;
        
        // Always try to accelerate if stopped
        if (this.car.speed < 10) {
            this.car.accelerate(deltaTime);
        }
        
        switch (action) {
            case 'ACCELERATE':
            case 'ATTACK':
            case 'WAIT':  // Even on WAIT, keep moving
            default:     // Any unknown action, just accelerate
                this.car.accelerate(deltaTime);
                break;
                
            case 'BRAKE':
                this.car.brake(deltaTime);
                break;
                
            case 'DEFEND':
                // Defend by maintaining position, not stopping
                if (this.car.speed > 150) {
                    this.car.brake(deltaTime * 0.5); // Light braking
                } else {
                    this.car.accelerate(deltaTime * 0.8); // Keep moving
                }
                break;
                
            case 'CONSERVE':
                // Conserve fuel but keep moving
                if (this.car.speed < 100) {
                    this.car.accelerate(deltaTime);
                } else if (this.car.speed > 180) {
                    this.car.brake(deltaTime * 0.3);
                }
                // Otherwise maintain speed
                break;
                
            case 'FIRE':
            case 'SHOOT':
                const targetInfo = weaponsManager.getTargetAhead(this.car, cars, track);
                if (targetInfo) {
                    weaponsManager.fire(this.car, targetInfo.car);
                }
                break;
                
            case 'USE_POWERUP':
                // Power-ups are permanent now, no action needed
                break;
                
            case 'SWERVE':
                // Random lane change
                if (Math.random() > 0.5) {
                    this.car.turnLeft(deltaTime);
                } else {
                    this.car.turnRight(deltaTime);
                }
                break;
        }
        
        // Smart lane changes to avoid obstacles or overtake
        if (action === 'ATTACK' || action === 'OVERTAKE') {
            const targetInfo = weaponsManager.getTargetAhead(this.car, cars, track);
            if (targetInfo && targetInfo.distance < 50) {
                // Try to change lanes for overtaking
                if (this.car.currentLane === targetInfo.car.currentLane) {
                    if (this.car.currentLane === 0) {
                        this.car.turnLeft(deltaTime);
                    } else {
                        this.car.turnRight(deltaTime);
                    }
                }
            }
        }
    }
}