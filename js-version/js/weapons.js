// Weapons system - Machine guns
class Bullet {
    constructor(shooter, target, startX, startY, targetX, targetY) {
        this.id = Utils.generateId();
        this.shooter = shooter;
        this.target = target;
        this.x = startX;
        this.y = startY;
        this.targetX = targetX;
        this.targetY = targetY;
        
        // Calculate velocity
        const angle = Utils.angle(startX, startY, targetX, targetY);
        this.vx = Math.cos(angle) * CONFIG.WEAPONS.BULLET_SPEED;
        this.vy = Math.sin(angle) * CONFIG.WEAPONS.BULLET_SPEED;
        
        this.alive = true;
        this.distance = 0;
        this.trail = [];
    }
    
    update(deltaTime) {
        if (!this.alive) return;
        
        // Update position
        this.x += this.vx * deltaTime;
        this.y += this.vy * deltaTime;
        
        // Track distance traveled
        const dist = Math.sqrt(this.vx * this.vx + this.vy * this.vy) * deltaTime;
        this.distance += dist;
        
        // Add to trail
        this.trail.push({ x: this.x, y: this.y });
        if (this.trail.length > 5) {
            this.trail.shift();
        }
        
        // Check if out of range
        if (this.distance > CONFIG.WEAPONS.RANGE) {
            this.alive = false;
        }
    }
    
    checkHit(target) {
        const distance = Utils.distance(this.x, this.y, target.x, target.y);
        return distance < target.size / 2;
    }
}

class WeaponsManager {
    constructor() {
        this.bullets = [];
        this.hits = [];
    }
    
    update(deltaTime, cars) {
        // Update bullets
        this.bullets = this.bullets.filter(bullet => {
            if (!bullet.alive) return false;
            
            bullet.update(deltaTime);
            
            // Check for hits
            if (bullet.target && bullet.alive) {
                const targetCar = cars.find(c => c.id === bullet.target.id);
                if (targetCar && bullet.checkHit(targetCar)) {
                    // Hit!
                    this.registerHit(bullet, targetCar);
                    bullet.alive = false;
                }
            }
            
            return bullet.alive;
        });
        
        // Update hit effects
        this.hits = this.hits.filter(hit => {
            hit.duration -= deltaTime * 1000;
            return hit.duration > 0;
        });
    }
    
    fire(shooter, target) {
        // Check if can fire
        if (!shooter.fire()) {
            return null;
        }
        
        // Create bullet spread (3 bullets)
        const bullets = [];
        for (let i = -1; i <= 1; i++) {
            const spread = i * 0.05; // Small spread angle
            const angle = Utils.angle(shooter.x, shooter.y, target.x, target.y) + spread;
            
            const startX = shooter.x + Math.cos(angle) * shooter.size;
            const startY = shooter.y + Math.sin(angle) * shooter.size;
            
            const bullet = new Bullet(
                shooter,
                target,
                startX,
                startY,
                target.x,
                target.y
            );
            
            bullets.push(bullet);
            this.bullets.push(bullet);
        }
        
        return bullets;
    }
    
    registerHit(bullet, target) {
        // Apply damage
        const hit = target.takeDamage(CONFIG.WEAPONS.DAMAGE);
        
        if (hit) {
            this.hits.push({
                id: Utils.generateId(),
                shooter: bullet.shooter.name,
                target: target.name,
                x: target.x,
                y: target.y,
                duration: CONFIG.WEAPONS.HIT_DURATION
            });
            
            console.log(`🔫 ${bullet.shooter.name} HIT ${target.name}!`);
        }
    }
    
    getTargetAhead(car, cars, track) {
        // Find cars ahead within range
        const targetsAhead = [];
        
        cars.forEach(other => {
            if (other.id === car.id) return;
            
            // Calculate track distance
            let distance = other.trackProgress - car.trackProgress;
            
            // Handle wrap-around
            if (distance < 0) {
                // Check if other car is actually ahead by a lap
                if (other.lap > car.lap) {
                    distance += 1;
                } else if (other.lap === car.lap) {
                    // Other car is behind on same lap
                    return;
                }
            }
            
            // Convert to meters
            const distanceMeters = distance * track.length * 1000;
            
            if (distanceMeters > 0 && distanceMeters <= CONFIG.WEAPONS.RANGE) {
                targetsAhead.push({
                    car: other,
                    distance: distanceMeters
                });
            }
        });
        
        // Sort by distance and return closest
        targetsAhead.sort((a, b) => a.distance - b.distance);
        return targetsAhead[0] || null;
    }
    
    shouldFire(car, target, aiPersonality) {
        // AI decision logic for firing
        if (!target || car.machineGun.ammo === 0) return false;
        
        const distance = target.distance;
        const ammoPercentage = car.machineGun.ammo / CONFIG.WEAPONS.AMMO_COUNT;
        
        // Different personalities have different firing strategies
        switch (aiPersonality) {
            case 'AGGRESSIVE':
                // Fire whenever possible
                return distance < CONFIG.WEAPONS.RANGE * 0.8;
                
            case 'STRATEGIC':
                // Save ammo for close targets
                return distance < CONFIG.WEAPONS.RANGE * 0.5 && ammoPercentage > 0.3;
                
            case 'BALANCED':
                // Moderate approach
                return distance < CONFIG.WEAPONS.RANGE * 0.6 && ammoPercentage > 0.2;
                
            case 'CHAOTIC':
                // Random firing
                return Math.random() < 0.7;
                
            case 'TECHNICAL':
                // Precise shots only
                return distance < CONFIG.WEAPONS.RANGE * 0.3 && car.speed < target.car.speed;
                
            default:
                return distance < CONFIG.WEAPONS.RANGE * 0.5;
        }
    }
    
    getAmmoStatus(cars) {
        const status = {};
        cars.forEach(car => {
            status[car.id] = {
                name: car.name,
                ammo: car.machineGun.ammo,
                percentage: car.machineGun.ammo / CONFIG.WEAPONS.AMMO_COUNT
            };
        });
        return status;
    }
}