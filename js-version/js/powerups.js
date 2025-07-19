// Power-up types - ONLY TURBO BOOST NOW
const POWERUP_TYPES = {
    TURBO_BOOST: {
        id: 'TURBO_BOOST',
        name: 'Turbo Boost',
        description: '+80% speed for 6 seconds',
        icon: '🚀',
        color: '#ff8800',
        duration: 6, // 6 seconds (longer)
        power: 1.8, // 80% speed boost (more powerful)
        rarity: { 1: 100, 2: 100, 3: 100, 4: 100, 5: 100 } // Equal chance for all
    }
};


// Power-up pickup on track
class PowerUpPickup {
    constructor(progress) {
        this.id = Utils.generateId();
        this.progress = progress; // Position on track (0-1)
        this.available = true;
        this.respawnTimer = 0;
        this.size = CONFIG.POWERUPS.BOX_SIZE;
        this.animationFrame = 0;
    }
    
    update(deltaTime) {
        this.animationFrame++;
        
        if (!this.available) {
            this.respawnTimer -= deltaTime * 1000;
            if (this.respawnTimer <= 0) {
                this.available = true;
                this.respawnTimer = 0;
            }
        }
    }
    
    collect() {
        if (this.available) {
            this.available = false;
            this.respawnTimer = CONFIG.POWERUPS.RESPAWN_TIME;
            return true;
        }
        return false;
    }
    
    getVisuals() {
        const colors = ['#ffd700', '#ffffff', '#00ffff'];
        const colorIndex = Math.floor(this.animationFrame / 10) % colors.length;
        const glowRadius = this.size / 2 + 3 + Math.sin(this.animationFrame * 0.1) * 2;
        
        return {
            color: colors[colorIndex],
            glowRadius: glowRadius,
            alpha: this.available ? 1 : 0.3
        };
    }
}

// Power-up manager
class PowerUpManager {
    constructor() {
        this.pickups = [];
        this.activeEffects = new Map(); // carId -> effects
    }
    
    initializeTrack(trackLength, numPickups = 8) {
        this.pickups = [];
        const spacing = 1 / numPickups;
        
        for (let i = 0; i < numPickups; i++) {
            const progress = (i * spacing + spacing / 2) % 1;
            this.pickups.push(new PowerUpPickup(progress));
        }
    }
    
    update(deltaTime) {
        // Update all pickups
        this.pickups.forEach(pickup => pickup.update(deltaTime));
        
        // Update active effects
        for (const [carId, effects] of this.activeEffects.entries()) {
            const updatedEffects = effects.filter(effect => {
                effect.remainingTime -= deltaTime;
                return effect.remainingTime > 0;
            });
            
            if (updatedEffects.length > 0) {
                this.activeEffects.set(carId, updatedEffects);
            } else {
                this.activeEffects.delete(carId);
            }
        }
    }
    
    checkPickupCollection(car, trackProgress) {
        const collectionRadius = CONFIG.POWERUPS.PICKUP_RADIUS;
        
        for (const pickup of this.pickups) {
            if (!pickup.available) continue;
            
            let distance = Math.abs(trackProgress - pickup.progress);
            // Handle wrap-around
            if (distance > 0.5) {
                distance = 1 - distance;
            }
            
            if (distance < collectionRadius) {
                if (pickup.collect()) {
                    const powerUp = this.generatePowerUp(car.position, 5); // Assume 5 cars
                    if (car.addPowerUp(powerUp)) {
                        return powerUp;
                    }
                }
            }
        }
        
        return null;
    }
    
    generatePowerUp(position, totalCars) {
        // Safety check
        if (!position || position < 1 || position > totalCars) {
            position = 3; // Default middle position
        }
        
        // Get weighted random power-up based on position
        const weights = {};
        let totalWeight = 0;
        
        for (const [key, powerUp] of Object.entries(POWERUP_TYPES)) {
            const weight = powerUp.rarity[position] || powerUp.rarity[3] || 1;
            weights[key] = weight;
            totalWeight += weight;
        }
        
        // Safety check
        if (totalWeight === 0) {
            return { ...POWERUP_TYPES.TURBO_BOOST };
        }
        
        // Random selection
        let random = Math.random() * totalWeight;
        for (const [key, weight] of Object.entries(weights)) {
            random -= weight;
            if (random <= 0) {
                return { ...POWERUP_TYPES[key] };
            }
        }
        
        // Fallback
        return { ...POWERUP_TYPES.TURBO_BOOST };
    }
    
    usePowerUp(car, powerUp, targetCar = null) {
        const effect = {
            type: powerUp.id,
            power: powerUp.power,
            remainingTime: powerUp.duration,
            startTime: Date.now()
        };
        
        switch (powerUp.id) {
            case 'LIGHTNING_BOLT':
                // Affect all cars ahead
                return { type: 'LIGHTNING', targets: 'ahead', effect };
                
            case 'RED_SHELL':
                // Target car directly ahead
                return { type: 'PROJECTILE', target: targetCar, damage: powerUp.power };
                
            case 'BLUE_SHELL':
                // Target race leader
                return { type: 'PROJECTILE', target: 'leader', damage: powerUp.power };
                
            case 'BANANA':
                // Drop banana behind
                return { type: 'TRAP', position: car.trackProgress };
                
            case 'SHIELD':
            case 'GHOST':
            case 'TURBO_BOOST':
            case 'NITRO':
                // Apply effect to car
                car.activateEffect(effect);
                return { type: 'SELF', effect };
                
            case 'FUEL_BOOST':
                car.fuel = Math.min(CONFIG.CAR.FUEL_CAPACITY, car.fuel + powerUp.power);
                return { type: 'INSTANT', stat: 'fuel', amount: powerUp.power };
                
            case 'TIRE_REPAIR':
                car.tireWear = Math.max(0, car.tireWear - powerUp.power);
                return { type: 'INSTANT', stat: 'tires', amount: powerUp.power };
                
            case 'RADAR':
                return { type: 'INFO', data: 'telemetry' };
        }
    }
    
    getSpeedModifier(carId) {
        const effects = this.activeEffects.get(carId) || [];
        let modifier = 1;
        
        effects.forEach(effect => {
            if (effect.type === 'TURBO_BOOST' || effect.type === 'NITRO') {
                modifier *= effect.power;
            } else if (effect.type === 'LIGHTNING') {
                modifier *= effect.power;
            }
        });
        
        return modifier;
    }
}