// Canvas renderer for the racing game
class Renderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;
        
        // Camera settings
        this.camera = {
            x: this.width / 2,
            y: this.height / 2,
            zoom: 1
        };
        
        // Visual settings
        this.showEffects = true;
        this.particleSystem = [];
        this.frameCount = 0;
    }
    
    clear() {
        // Dark background with gradient
        const gradient = this.ctx.createLinearGradient(0, 0, 0, this.height);
        gradient.addColorStop(0, '#0a0a0a');
        gradient.addColorStop(1, '#1a1a1a');
        this.ctx.fillStyle = gradient;
        this.ctx.fillRect(0, 0, this.width, this.height);
    }
    
    renderTrack(track) {
        const ctx = this.ctx;
        
        // Draw track surface
        ctx.strokeStyle = '#444';
        ctx.lineWidth = track.width + 10;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        
        ctx.beginPath();
        track.points.forEach((point, index) => {
            if (index === 0) {
                ctx.moveTo(point.x, point.y);
            } else {
                ctx.lineTo(point.x, point.y);
            }
        });
        ctx.closePath();
        ctx.stroke();
        
        // Draw track edges
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        
        // Outer edge
        ctx.beginPath();
        track.points.forEach((point, index) => {
            const nextIndex = (index + 1) % track.points.length;
            const prevIndex = (index - 1 + track.points.length) % track.points.length;
            
            const angle = Utils.angle(
                track.points[prevIndex].x,
                track.points[prevIndex].y,
                track.points[nextIndex].x,
                track.points[nextIndex].y
            );
            
            const perpAngle = angle + Math.PI / 2;
            const offsetX = Math.cos(perpAngle) * (track.width / 2 + 5);
            const offsetY = Math.sin(perpAngle) * (track.width / 2 + 5);
            
            if (index === 0) {
                ctx.moveTo(point.x + offsetX, point.y + offsetY);
            } else {
                ctx.lineTo(point.x + offsetX, point.y + offsetY);
            }
        });
        ctx.closePath();
        ctx.stroke();
        
        // Inner edge
        ctx.beginPath();
        track.points.forEach((point, index) => {
            const nextIndex = (index + 1) % track.points.length;
            const prevIndex = (index - 1 + track.points.length) % track.points.length;
            
            const angle = Utils.angle(
                track.points[prevIndex].x,
                track.points[prevIndex].y,
                track.points[nextIndex].x,
                track.points[nextIndex].y
            );
            
            const perpAngle = angle + Math.PI / 2;
            const offsetX = Math.cos(perpAngle) * (-track.width / 2 - 5);
            const offsetY = Math.sin(perpAngle) * (-track.width / 2 - 5);
            
            if (index === 0) {
                ctx.moveTo(point.x + offsetX, point.y + offsetY);
            } else {
                ctx.lineTo(point.x + offsetX, point.y + offsetY);
            }
        });
        ctx.closePath();
        ctx.stroke();
        
        // Draw start/finish line
        const startPoint = track.points[0];
        const nextPoint = track.points[1];
        const angle = Utils.angle(startPoint.x, startPoint.y, nextPoint.x, nextPoint.y);
        const perpAngle = angle + Math.PI / 2;
        
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 4;
        ctx.setLineDash([10, 10]);
        ctx.beginPath();
        ctx.moveTo(
            startPoint.x + Math.cos(perpAngle) * track.width / 2,
            startPoint.y + Math.sin(perpAngle) * track.width / 2
        );
        ctx.lineTo(
            startPoint.x - Math.cos(perpAngle) * track.width / 2,
            startPoint.y - Math.sin(perpAngle) * track.width / 2
        );
        ctx.stroke();
        ctx.setLineDash([]);
    }
    
    renderPowerUpPickups(powerUpManager, track) {
        const ctx = this.ctx;
        
        powerUpManager.pickups.forEach(pickup => {
            const pos = Utils.getTrackPosition(track, pickup.progress);
            const visuals = pickup.getVisuals();
            
            if (pickup.available) {
                // Draw glow effect
                const gradient = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, visuals.glowRadius);
                gradient.addColorStop(0, Utils.colorWithAlpha(visuals.color, 0.5));
                gradient.addColorStop(1, Utils.colorWithAlpha(visuals.color, 0));
                ctx.fillStyle = gradient;
                ctx.fillRect(
                    pos.x - visuals.glowRadius,
                    pos.y - visuals.glowRadius,
                    visuals.glowRadius * 2,
                    visuals.glowRadius * 2
                );
            }
            
            // Draw box
            ctx.fillStyle = Utils.colorWithAlpha(visuals.color, visuals.alpha);
            ctx.strokeStyle = Utils.colorWithAlpha('#000', visuals.alpha);
            ctx.lineWidth = 2;
            
            const size = pickup.size;
            ctx.fillRect(pos.x - size/2, pos.y - size/2, size, size);
            ctx.strokeRect(pos.x - size/2, pos.y - size/2, size, size);
            
            // Draw question mark
            if (pickup.available) {
                ctx.fillStyle = '#000';
                ctx.font = '12px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText('?', pos.x, pos.y);
            }
        });
    }
    
    renderCar(car) {
        const ctx = this.ctx;
        
        // Draw trail
        if (car.trail.length > 1) {
            ctx.strokeStyle = Utils.colorWithAlpha(car.color, 0.3);
            ctx.lineWidth = 2;
            ctx.beginPath();
            car.trail.forEach((point, index) => {
                if (index === 0) {
                    ctx.moveTo(point.x, point.y);
                } else {
                    ctx.lineTo(point.x, point.y);
                }
            });
            ctx.stroke();
        }
        
        // Draw car shadow
        ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.beginPath();
        ctx.ellipse(car.x + 5, car.y + 5, car.size * 0.8, car.size * 0.6, car.angle, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw car body
        ctx.save();
        ctx.translate(car.x, car.y);
        ctx.rotate(car.angle);
        
        // Car shape
        ctx.fillStyle = car.color;
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        
        // Simple car shape
        ctx.beginPath();
        ctx.moveTo(-car.size/2, -car.size/3);
        ctx.lineTo(car.size/2, -car.size/4);
        ctx.lineTo(car.size/2, car.size/4);
        ctx.lineTo(-car.size/2, car.size/3);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        
        // Windshield
        ctx.fillStyle = 'rgba(100, 100, 255, 0.7)';
        ctx.fillRect(car.size/4 - 5, -car.size/6, 10, car.size/3);
        
        ctx.restore();
        
        // Draw effects
        this.renderCarEffects(car);
        
        // Draw car name
        ctx.fillStyle = '#fff';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'bottom';
        ctx.fillText(car.name, car.x, car.y - car.size - 10);
    }
    
    renderCarEffects(car) {
        const ctx = this.ctx;
        
        // Shield effect
        if (car.shieldActive) {
            ctx.strokeStyle = '#00ffff';
            ctx.lineWidth = 3;
            ctx.globalAlpha = 0.5 + Math.sin(this.frameCount * 0.1) * 0.2;
            ctx.beginPath();
            ctx.arc(car.x, car.y, car.size + 10, 0, Math.PI * 2);
            ctx.stroke();
            ctx.globalAlpha = 1;
        }
        
        // Boost effects
        const hasBoost = car.activeEffects.some(e => 
            e.type === 'TURBO_BOOST' || e.type === 'NITRO'
        );
        
        if (hasBoost) {
            // Nitro flames
            for (let i = 0; i < 3; i++) {
                const flameAngle = car.angle + Math.PI;
                const flameX = car.x + Math.cos(flameAngle) * (car.size + i * 10);
                const flameY = car.y + Math.sin(flameAngle) * (car.size + i * 10);
                
                const gradient = ctx.createRadialGradient(flameX, flameY, 0, flameX, flameY, 10 - i * 2);
                gradient.addColorStop(0, 'rgba(255, 200, 0, 0.8)');
                gradient.addColorStop(0.5, 'rgba(255, 100, 0, 0.5)');
                gradient.addColorStop(1, 'rgba(255, 0, 0, 0)');
                
                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(flameX, flameY, 10 - i * 2, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        
        // Ghost effect
        if (car.activeEffects.some(e => e.type === 'GHOST')) {
            ctx.strokeStyle = 'rgba(200, 200, 255, 0.5)';
            ctx.lineWidth = 2;
            for (let i = 0; i < 3; i++) {
                ctx.globalAlpha = 0.3 - i * 0.1;
                ctx.beginPath();
                ctx.arc(car.x, car.y, car.size + 5 + i * 5, 0, Math.PI * 2);
                ctx.stroke();
            }
            ctx.globalAlpha = 1;
        }
    }
    
    renderBullets(weaponsManager) {
        const ctx = this.ctx;
        
        // Render bullets
        weaponsManager.bullets.forEach(bullet => {
            // Bullet trail
            ctx.strokeStyle = '#ffff00';
            ctx.lineWidth = 2;
            ctx.globalAlpha = 0.8;
            
            if (bullet.trail.length > 1) {
                ctx.beginPath();
                bullet.trail.forEach((point, index) => {
                    if (index === 0) {
                        ctx.moveTo(point.x, point.y);
                    } else {
                        ctx.lineTo(point.x, point.y);
                    }
                });
                ctx.stroke();
            }
            
            // Bullet head
            ctx.fillStyle = '#ffff00';
            ctx.globalAlpha = 1;
            ctx.beginPath();
            ctx.arc(bullet.x, bullet.y, 3, 0, Math.PI * 2);
            ctx.fill();
        });
        
        // Render hit effects
        weaponsManager.hits.forEach(hit => {
            const alpha = hit.duration / CONFIG.WEAPONS.HIT_DURATION;
            
            // Impact flash
            const gradient = ctx.createRadialGradient(hit.x, hit.y, 0, hit.x, hit.y, 20);
            gradient.addColorStop(0, `rgba(255, 200, 0, ${alpha})`);
            gradient.addColorStop(0.5, `rgba(255, 100, 0, ${alpha * 0.5})`);
            gradient.addColorStop(1, 'rgba(255, 0, 0, 0)');
            
            ctx.fillStyle = gradient;
            ctx.fillRect(hit.x - 20, hit.y - 20, 40, 40);
            
            // Hit marker
            ctx.strokeStyle = `rgba(255, 0, 0, ${alpha})`;
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(hit.x - 10, hit.y - 10);
            ctx.lineTo(hit.x + 10, hit.y + 10);
            ctx.moveTo(hit.x - 10, hit.y + 10);
            ctx.lineTo(hit.x + 10, hit.y - 10);
            ctx.stroke();
        });
    }
    
    renderHUD(game) {
        // This is handled by HTML elements in our implementation
        // But we could add canvas-based HUD elements here if needed
    }
    
    render(game) {
        this.frameCount++;
        
        this.clear();
        this.renderTrack(game.track);
        this.renderPowerUpPickups(game.powerUpManager, game.track);
        
        // Sort cars by position for proper layering
        const sortedCars = [...game.cars].sort((a, b) => b.position - a.position);
        sortedCars.forEach(car => this.renderCar(car));
        
        this.renderBullets(game.weaponsManager);
    }
}