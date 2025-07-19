// Racing Car class
class RacingCar {
    constructor(name, style, x = 0, y = 0) {
        this.id = Utils.generateId();
        this.name = name;
        this.style = style;
        
        // Position and movement
        this.x = x;
        this.y = y;
        this.angle = 0; // radians
        this.speed = 0; // pixels/second
        this.maxSpeed = CONFIG.CAR.MAX_SPEED * style.acceleration;
        this.acceleration = CONFIG.CAR.ACCELERATION * style.acceleration;
        this.braking = CONFIG.CAR.BRAKING * style.braking;
        this.turnSpeed = CONFIG.CAR.TURN_SPEED * style.cornering;
        
        // Track progress
        this.trackProgress = 0; // 0-1
        this.lap = 0;
        this.position = 1;
        this.finished = false;
        
        // Car state
        this.fuel = CONFIG.CAR.FUEL_CAPACITY;
        this.tireWear = 0; // 0-100
        this.damage = 0; // 0-100
        
        // Lane management
        this.currentLane = 0; // -1, 0, 1
        this.targetLane = 0;
        this.laneTransition = 0; // 0-1
        
        // Visual
        this.color = style.color;
        this.size = CONFIG.CAR.SIZE;
        this.trail = []; // Position history for visual effects
        
        // Combat
        this.machineGun = {
            ammo: CONFIG.WEAPONS.AMMO_COUNT,
            lastFireTime: 0,
            canFire: true
        };
        
        // Power-ups
        this.powerUps = [];
        this.activeEffects = [];
        this.shieldActive = false;
        
        // AI data
        this.lastDecisionTime = 0;
        this.currentAction = 'WAIT';
        this.targetCar = null;
        
    }
    
    update(deltaTime, track) {
        // Apply speed modifiers from effects
        const speedModifier = this.getSpeedModifier();
        const effectiveSpeed = this.speed * speedModifier;
        
        // Simple movement calculation - increased speed
        const pixelsPerSecond = effectiveSpeed * 0.8; // Increased from 0.5 for faster racing
        const distance = pixelsPerSecond * deltaTime;
        
        
        // Get track length
        const trackLength = track.points.length * CONFIG.TRACK.SEGMENT_LENGTH;
        
        // Update track progress
        this.trackProgress += distance / trackLength;
        
        // Check for lap completion
        if (this.trackProgress >= 1) {
            this.trackProgress -= 1;
            this.lap++;
            this.onLapComplete();
        }
        
        // Get position on track
        const trackPos = Utils.getTrackPosition(track, this.trackProgress);
        
        // Update lane transition
        if (this.currentLane !== this.targetLane) {
            this.laneTransition = Math.min(1, this.laneTransition + deltaTime * 2);
            if (this.laneTransition >= 1) {
                this.currentLane = this.targetLane;
                this.laneTransition = 0;
            }
        }
        
        // Calculate lane offset
        const laneOffset = Utils.lerp(
            this.currentLane * CONFIG.TRACK.WIDTH / 3,
            this.targetLane * CONFIG.TRACK.WIDTH / 3,
            this.laneTransition
        );
        
        // Apply position with lane offset
        const pos = Utils.applyLaneOffset(trackPos.x, trackPos.y, trackPos.angle, laneOffset);
        
        // Direct position update
        this.x = pos.x;
        this.y = pos.y;
        this.angle = trackPos.angle;
        
        // Update trail
        this.trail.push({ x: this.x, y: this.y, time: Date.now() });
        if (this.trail.length > CONFIG.VISUALS.TRAIL_LENGTH) {
            this.trail.shift();
        }
        
        // Update fuel and tire wear
        this.fuel = Math.max(0, this.fuel - CONFIG.CAR.FUEL_CONSUMPTION * deltaTime * (this.speed / this.maxSpeed));
        this.tireWear = Math.min(100, this.tireWear + 0.01 * deltaTime * (this.speed / this.maxSpeed));
        
        // Update active effects
        this.updateEffects(deltaTime);
    }
    
    accelerate(deltaTime) {
        if (this.fuel > 0) {
            this.speed = Math.min(this.maxSpeed, this.speed + this.acceleration * deltaTime);
        }
    }
    
    brake(deltaTime) {
        this.speed = Math.max(0, this.speed - this.braking * deltaTime);
    }
    
    turnLeft(deltaTime) {
        this.targetLane = Math.max(-1, this.currentLane - 1);
    }
    
    turnRight(deltaTime) {
        this.targetLane = Math.min(1, this.currentLane + 1);
    }
    
    fire() {
        const now = Date.now();
        if (this.machineGun.ammo > 0 && 
            now - this.machineGun.lastFireTime >= CONFIG.WEAPONS.FIRE_RATE) {
            this.machineGun.ammo--;
            this.machineGun.lastFireTime = now;
            return true;
        }
        return false;
    }
    
    takeDamage(amount) {
        if (!this.shieldActive) {
            this.speed *= (1 - amount);
            this.damage = Math.min(100, this.damage + amount * 100);
            return true;
        }
        return false;
    }
    
    usePowerUp(index = 0) {
        if (this.powerUps.length > index) {
            const powerUp = this.powerUps.splice(index, 1)[0];
            return powerUp;
        }
        return null;
    }
    
    addPowerUp(powerUp) {
        // Only allow one power-up per car at a time
        if (this.powerUps.length === 0 && !this.hasTurboActive()) {
            this.powerUps.push(powerUp);
            // Immediately activate the turbo boost
            this.activateEffect({
                type: powerUp.id,
                power: powerUp.power,
                duration: powerUp.duration
            });
            return true;
        }
        return false;
    }
    
    hasTurboActive() {
        return this.activeEffects.some(effect => effect.type === 'TURBO_BOOST');
    }
    
    activateEffect(effect) {
        this.activeEffects.push({
            ...effect,
            startTime: Date.now()
        });
        
        // Apply immediate effects
        switch (effect.type) {
            case 'SHIELD':
                this.shieldActive = true;
                break;
            case 'TURBO':
            case 'NITRO':
                this.speed = Math.min(this.maxSpeed * effect.power, this.speed * effect.power);
                break;
        }
    }
    
    updateEffects(deltaTime) {
        const now = Date.now();
        this.activeEffects = this.activeEffects.filter(effect => {
            const elapsed = (now - effect.startTime) / 1000;
            if (elapsed >= effect.duration) {
                // Remove effect
                if (effect.type === 'SHIELD') {
                    this.shieldActive = false;
                } else if (effect.type === 'TURBO_BOOST') {
                    // Remove the power-up from inventory when turbo ends
                    this.powerUps = this.powerUps.filter(p => p.id !== 'TURBO_BOOST');
                }
                return false;
            }
            return true;
        });
    }
    
    getSpeedModifier() {
        let modifier = 1;
        this.activeEffects.forEach(effect => {
            if (effect.type === 'TURBO_BOOST' || effect.type === 'TURBO' || effect.type === 'NITRO') {
                modifier *= effect.power;
            }
        });
        return modifier;
    }
    
    onLapComplete() {
        console.log(`${this.name} completed lap ${this.lap}!`);
    }
    
    getStatus() {
        return {
            name: this.name,
            position: this.position,
            lap: this.lap,
            speed: Math.round(this.speed),
            fuel: Math.round(this.fuel),
            ammo: this.machineGun.ammo,
            powerUps: this.powerUps.map(p => p.name),
            effects: this.activeEffects.map(e => e.type)
        };
    }
}