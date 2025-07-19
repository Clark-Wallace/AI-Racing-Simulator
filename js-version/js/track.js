// Race Track class
class RaceTrack {
    constructor(config) {
        this.name = config.name;
        this.length = config.length; // km
        this.type = config.type;
        this.difficulty = config.difficulty;
        this.color = config.color;
        
        this.points = [];
        this.width = CONFIG.TRACK.WIDTH;
        
        // Generate track based on type
        this.generateTrack();
    }
    
    generateTrack() {
        const centerX = CONFIG.CANVAS_WIDTH / 2;
        const centerY = CONFIG.CANVAS_HEIGHT / 2;
        // Use bigger radius for oval tracks
        const maxRadius = this.type === 'oval' ? 
            Math.min(CONFIG.CANVAS_WIDTH, CONFIG.CANVAS_HEIGHT) * 0.4 : 
            Math.min(CONFIG.CANVAS_WIDTH, CONFIG.CANVAS_HEIGHT) * 0.35;
        
        switch (this.type) {
            case 'oval':
                this.generateOvalCircuit(centerX, centerY, maxRadius);
                break;
            case 'street':
                this.generateStreetCircuit(centerX, centerY, maxRadius);
                break;
            case 'technical':
                this.generateTechnicalCircuit(centerX, centerY, maxRadius);
                break;
            case 'endurance':
                this.generateEnduranceCircuit(centerX, centerY, maxRadius);
                break;
            case 'mixed':
                this.generateMixedCircuit(centerX, centerY, maxRadius);
                break;
            case 'fantasy':
                this.generateFantasyCircuit(centerX, centerY, maxRadius);
                break;
            default:
                this.generateOvalCircuit(centerX, centerY, maxRadius);
        }
    }
    
    generateOvalCircuit(centerX, centerY, radius) {
        // Create a big NASCAR-style oval
        const points = 200; // More points for smoother racing
        const radiusX = radius * 1.4; // Make it wider
        const radiusY = radius * 0.8; // Keep height reasonable
        
        for (let i = 0; i < points; i++) {
            const angle = (i / points) * Math.PI * 2;
            
            // Create proper oval with banking on turns
            let x = centerX + Math.cos(angle) * radiusX;
            let y = centerY + Math.sin(angle) * radiusY;
            
            // Add slight banking effect on the curves
            const isOnCurve = (angle > Math.PI * 0.25 && angle < Math.PI * 0.75) || 
                             (angle > Math.PI * 1.25 && angle < Math.PI * 1.75);
            
            if (isOnCurve) {
                // Slightly tighter radius on curves for banking
                x = centerX + Math.cos(angle) * radiusX * 0.95;
                y = centerY + Math.sin(angle) * radiusY * 0.95;
            }
            
            this.points.push({ x, y });
        }
    }
    
    generateStreetCircuit(centerX, centerY, radius) {
        // Monaco-style with tight corners and straights
        const points = 120;
        for (let i = 0; i < points; i++) {
            const t = i / points;
            const angle = t * Math.PI * 2;
            
            // Create a more angular shape
            const r = radius * (0.8 + 0.2 * Math.sin(angle * 6));
            const x = centerX + Math.cos(angle) * r;
            const y = centerY + Math.sin(angle) * r * 0.8;
            
            // Add some sharp corners
            const cornerSharpness = Math.sin(angle * 8) * 0.1;
            this.points.push({
                x: x + cornerSharpness * radius,
                y: y
            });
        }
    }
    
    generateTechnicalCircuit(centerX, centerY, radius) {
        // Figure-8 style technical track
        const points = 150;
        for (let i = 0; i < points; i++) {
            const t = i / points;
            const angle = t * Math.PI * 2;
            
            this.points.push({
                x: centerX + Math.sin(angle) * radius * 0.8,
                y: centerY + Math.sin(angle * 2) * radius * 0.6
            });
        }
    }
    
    generateEnduranceCircuit(centerX, centerY, radius) {
        // Large complex circuit with many curves
        const points = 200;
        for (let i = 0; i < points; i++) {
            const t = i / points;
            const angle = t * Math.PI * 2;
            
            const r1 = radius * 0.8;
            const r2 = radius * 0.3;
            
            this.points.push({
                x: centerX + Math.cos(angle) * r1 + Math.cos(angle * 3) * r2,
                y: centerY + Math.sin(angle) * r1 + Math.sin(angle * 5) * r2
            });
        }
    }
    
    generateMixedCircuit(centerX, centerY, radius) {
        // Combination of straights and curves
        const points = 140;
        for (let i = 0; i < points; i++) {
            const t = i / points;
            const angle = t * Math.PI * 2;
            
            const variation = Math.sin(angle * 7) * 0.15;
            const r = radius * (0.85 + variation);
            
            this.points.push({
                x: centerX + Math.cos(angle) * r,
                y: centerY + Math.sin(angle) * r * 0.85 + Math.cos(angle * 5) * radius * 0.1
            });
        }
    }
    
    generateFantasyCircuit(centerX, centerY, radius) {
        // Rainbow Road style - wavy and wild
        const points = 180;
        for (let i = 0; i < points; i++) {
            const t = i / points;
            const angle = t * Math.PI * 2;
            
            // Create rainbow-like waves
            const wave1 = Math.sin(angle * 3) * 0.2;
            const wave2 = Math.cos(angle * 7) * 0.1;
            const r = radius * (0.8 + wave1);
            
            this.points.push({
                x: centerX + Math.cos(angle) * r + wave2 * radius,
                y: centerY + Math.sin(angle) * r + Math.sin(angle * 11) * radius * 0.1
            });
        }
    }
    
    getNearestPoint(x, y) {
        let minDist = Infinity;
        let nearestIndex = 0;
        
        this.points.forEach((point, index) => {
            const dist = Utils.distance(x, y, point.x, point.y);
            if (dist < minDist) {
                minDist = dist;
                nearestIndex = index;
            }
        });
        
        return {
            index: nearestIndex,
            point: this.points[nearestIndex],
            distance: minDist,
            progress: nearestIndex / this.points.length
        };
    }
    
    getSegmentType(progress) {
        // Determine if we're on a straight or corner
        const index = Math.floor(progress * this.points.length);
        const prevIndex = (index - 5 + this.points.length) % this.points.length;
        const nextIndex = (index + 5) % this.points.length;
        
        const angle1 = Utils.angle(
            this.points[prevIndex].x,
            this.points[prevIndex].y,
            this.points[index].x,
            this.points[index].y
        );
        
        const angle2 = Utils.angle(
            this.points[index].x,
            this.points[index].y,
            this.points[nextIndex].x,
            this.points[nextIndex].y
        );
        
        const angleDiff = Math.abs(Utils.normalizeAngle(angle2 - angle1));
        
        return angleDiff > 0.2 ? 'corner' : 'straight';
    }
}