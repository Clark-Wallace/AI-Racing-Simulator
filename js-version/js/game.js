// Main game class
class RacingGame {
    constructor(canvas) {
        this.canvas = canvas;
        this.renderer = new Renderer(canvas);
        
        // Game state
        this.state = 'menu'; // menu, waitingForFlag, racing, paused, finished
        this.config = {
            track: 'monaco',
            laps: 5,
            weather: 'clear'
        };
        
        // Game objects
        this.track = null;
        this.cars = [];
        this.aiDrivers = [];
        
        // Managers
        this.powerUpManager = new PowerUpManager();
        this.weaponsManager = new WeaponsManager();
        
        // Race state
        this.currentLap = 1;
        this.raceTime = 0;
        this.results = [];
        
        // Performance
        this.lastTime = 0;
        this.deltaTime = 0;
        this.fps = 0;
        this.frameCount = 0;
        this.fpsTime = 0;
    }
    
    init(config) {
        this.config = { ...this.config, ...config };
        
        // Create track
        this.track = new RaceTrack(TRACKS[this.config.track]);
        
        // Create cars
        this.cars = [];
        const startPositions = this.getStartingGrid();
        
        CAR_CONFIGS.forEach((config, index) => {
            const pos = startPositions[index];
            const car = new RacingCar(config.name, config.style, pos.x, pos.y);
            car.angle = pos.angle;
            car.trackProgress = 0;
            car.position = index + 1;
            
            this.cars.push(car);
            
            // Create AI driver
            const ai = new AIDriver(car, config.aiType);
            this.aiDrivers.push(ai);
        });
        
        // Initialize power-up pickups
        this.powerUpManager.initializeTrack(this.track.length);
        
        // Start race - wait for flag drop
        this.state = 'waitingForFlag';
        this.raceTime = 0;
        
        console.log('🏁 Race initialized!');
        console.log('Cars:', this.cars.map(c => ({ name: c.name, speed: c.speed })));
        console.log('AI Drivers:', this.aiDrivers.length);
        console.log(`Track: ${this.track.name}`);
        console.log(`Laps: ${this.config.laps}`);
        console.log(`Weather: ${this.config.weather}`);
    }
    
    getStartingGrid() {
        // Simple starting positions - all cars at the start line
        const startPoint = this.track.points[0];
        const nextPoint = this.track.points[1];
        const angle = Utils.angle(startPoint.x, startPoint.y, nextPoint.x, nextPoint.y);
        
        const positions = [];
        
        // Just place all cars at the start with slight spacing
        for (let i = 0; i < 5; i++) {
            const offset = (i - 2) * 30; // Spread cars left/right
            const x = startPoint.x + Math.cos(angle + Math.PI/2) * offset;
            const y = startPoint.y + Math.sin(angle + Math.PI/2) * offset;
            
            positions.push({ 
                x, 
                y, 
                angle
            });
        }
        
        return positions;
    }
    
    update(currentTime) {
        try {
            // Calculate delta time
            if (this.lastTime === 0) {
                this.lastTime = currentTime;
            }
            this.deltaTime = Math.min((currentTime - this.lastTime) / 1000, 0.1); // Cap at 100ms
            this.lastTime = currentTime;
            
            // Update FPS
            this.frameCount++;
            if (currentTime - this.fpsTime >= 1000) {
                this.fps = this.frameCount;
                this.frameCount = 0;
                this.fpsTime = currentTime;
            }
            
            if (this.state !== 'racing' && this.state !== 'waitingForFlag') return;
        
        // Only update race time when actually racing
        if (this.state === 'racing') {
            this.raceTime += this.deltaTime;
        }
        
        // Update game systems (always update for visuals)
        this.powerUpManager.update(this.deltaTime);
        this.weaponsManager.update(this.deltaTime, this.cars);
        
        // Always update cars for positioning
        this.cars.forEach(car => {
            car.update(this.deltaTime, this.track);
        });
        
        // Only update AI and race logic when racing (not during flag wait)
        if (this.state === 'racing') {
            // Update AI drivers
            const gameState = {
                track: this.track,
                cars: this.cars,
                weaponsManager: this.weaponsManager,
                powerUpManager: this.powerUpManager
            };
            
            this.aiDrivers.forEach(ai => ai.update(this.deltaTime, gameState));
            
            // Check power-up collection only when racing
            this.cars.forEach(car => {
                const collected = this.powerUpManager.checkPickupCollection(car, car.trackProgress);
                if (collected) {
                    console.log(`📦 ${car.name} collected ${collected.name}!`);
                }
            });
            
            // Update positions
            this.updateRacePositions();
            
            // Check for race completion
            this.checkRaceCompletion();
        }
        
        // Update HUD
        this.updateHUD();
        } catch (error) {
            console.error('Game update error:', error);
            this.state = 'paused';
        }
    }
    
    updateRacePositions() {
        // Sort cars by total distance (laps + progress)
        const carDistances = this.cars.map(car => ({
            car,
            distance: car.lap + car.trackProgress
        }));
        
        carDistances.sort((a, b) => b.distance - a.distance);
        
        carDistances.forEach((item, index) => {
            item.car.position = index + 1;
        });
    }
    
    checkRaceCompletion() {
        // Check if any car has finished
        this.cars.forEach(car => {
            if (!car.finished && car.lap >= this.config.laps) {
                car.finished = true;
                this.results.push({
                    position: this.results.length + 1,
                    name: car.name,
                    time: this.raceTime,
                    laps: car.lap
                });
                
                console.log(`🏁 ${car.name} finished in position ${this.results.length}!`);
            }
        });
        
        // Check if race is over
        if (this.results.length === this.cars.length) {
            this.endRace();
        }
    }
    
    endRace() {
        this.state = 'finished';
        console.log('🏆 Race finished!');
        console.log('Results:', this.results);
        
        // Show results screen
        this.showResults();
    }
    
    showResults() {
        // This would show a results overlay
        // For now, just log to console
        console.log('\n🏁 RACE RESULTS 🏁');
        console.log('==================');
        this.results.forEach(result => {
            console.log(`${result.position}. ${result.name} - ${Utils.formatTime(result.time * 1000)}`);
        });
    }
    
    updateHUD() {
        // Update lap counter
        const lapCounter = document.getElementById('lapCounter');
        if (lapCounter) {
            if (this.state === 'waitingForFlag') {
                lapCounter.textContent = '🏁 PRESS SPACEBAR TO DROP FLAG! 🏁';
                lapCounter.style.color = '#ff0';
                lapCounter.style.fontSize = '18px';
                lapCounter.style.fontWeight = 'bold';
            } else {
                const maxLap = Math.max(...this.cars.map(c => c.lap + 1));
                lapCounter.textContent = `Lap ${Math.min(maxLap, this.config.laps)}/${this.config.laps}`;
                lapCounter.style.color = '#0ff';
                lapCounter.style.fontSize = '16px';
                lapCounter.style.fontWeight = 'normal';
            }
        }
        
        // Update positions
        const positions = document.getElementById('positions');
        if (positions) {
            const sortedCars = [...this.cars].sort((a, b) => a.position - b.position);
            positions.innerHTML = sortedCars.map(car => 
                `<div class="car-status">P${car.position}: ${car.name}</div>`
            ).join('');
        }
        
        // Update power-ups
        const powerupList = document.getElementById('powerupList');
        if (powerupList) {
            powerupList.innerHTML = this.cars.map(car => 
                `<div class="car-status">
                    <span style="color: ${car.color}">${car.name}:</span>
                    <span>${car.powerUps.map(p => p.icon).join(' ') || 'None'}</span>
                </div>`
            ).join('');
        }
        
        // Update ammo
        const ammoList = document.getElementById('ammoList');
        if (ammoList) {
            ammoList.innerHTML = this.cars.map(car => {
                const percentage = car.machineGun.ammo / CONFIG.WEAPONS.AMMO_COUNT;
                const barClass = percentage > 0.5 ? '' : percentage > 0.2 ? 'low' : 'critical';
                
                return `<div class="car-status">
                    <span style="color: ${car.color}">${car.name}:</span>
                    <div class="ammo-bar">
                        <div class="ammo-fill ${barClass}" style="width: ${percentage * 100}%"></div>
                    </div>
                    <span>${car.machineGun.ammo}/50</span>
                </div>`;
            }).join('');
        }
    }
    
    render() {
        this.renderer.render(this);
    }
    
    handleKeyPress(key) {
        if (this.state === 'waitingForFlag') {
            if (key === ' ') {
                this.dropFlag();
            }
        } else if (this.state === 'racing') {
            switch (key) {
                case 'Escape':
                    this.pause();
                    break;
            }
        }
    }
    
    dropFlag() {
        console.log('🏁 FLAG DROP! RACE STARTED!');
        this.state = 'racing';
        this.raceTime = 0;
        
        // Debug: Check car speeds after flag drop
        setTimeout(() => {
            console.log('Car speeds after flag drop:', this.cars.map(c => ({ name: c.name, speed: c.speed })));
        }, 1000);
    }
    
    pause() {
        if (this.state === 'racing') {
            this.state = 'paused';
            console.log('Game paused');
        } else if (this.state === 'paused') {
            this.state = 'racing';
            console.log('Game resumed');
        }
    }
    
}