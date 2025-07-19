// Utility functions
const Utils = {
    // Convert degrees to radians
    degToRad(degrees) {
        return degrees * Math.PI / 180;
    },
    
    // Convert radians to degrees
    radToDeg(radians) {
        return radians * 180 / Math.PI;
    },
    
    // Calculate distance between two points
    distance(x1, y1, x2, y2) {
        const dx = x2 - x1;
        const dy = y2 - y1;
        return Math.sqrt(dx * dx + dy * dy);
    },
    
    // Calculate angle between two points
    angle(x1, y1, x2, y2) {
        return Math.atan2(y2 - y1, x2 - x1);
    },
    
    // Normalize angle to 0-2π
    normalizeAngle(angle) {
        while (angle < 0) angle += Math.PI * 2;
        while (angle > Math.PI * 2) angle -= Math.PI * 2;
        return angle;
    },
    
    // Linear interpolation
    lerp(start, end, t) {
        return start + (end - start) * t;
    },
    
    // Clamp value between min and max
    clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    },
    
    // Random float between min and max
    randomFloat(min, max) {
        return Math.random() * (max - min) + min;
    },
    
    // Random integer between min and max (inclusive)
    randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    },
    
    // Check if two rectangles collide
    rectCollision(x1, y1, w1, h1, x2, y2, w2, h2) {
        return x1 < x2 + w2 &&
               x1 + w1 > x2 &&
               y1 < y2 + h2 &&
               y1 + h1 > y2;
    },
    
    // Check if two circles collide
    circleCollision(x1, y1, r1, x2, y2, r2) {
        const dx = x2 - x1;
        const dy = y2 - y1;
        const distance = Math.sqrt(dx * dx + dy * dy);
        return distance < r1 + r2;
    },
    
    // Get color with alpha
    colorWithAlpha(color, alpha) {
        if (color.startsWith('#')) {
            const r = parseInt(color.slice(1, 3), 16);
            const g = parseInt(color.slice(3, 5), 16);
            const b = parseInt(color.slice(5, 7), 16);
            return `rgba(${r}, ${g}, ${b}, ${alpha})`;
        }
        return color;
    },
    
    // Format time in MM:SS.mmm
    formatTime(milliseconds) {
        const minutes = Math.floor(milliseconds / 60000);
        const seconds = Math.floor((milliseconds % 60000) / 1000);
        const ms = milliseconds % 1000;
        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${ms.toString().padStart(3, '0')}`;
    },
    
    // Get track position from progress (0-1)
    getTrackPosition(track, progress) {
        const index = Math.floor(progress * track.points.length);
        const nextIndex = (index + 1) % track.points.length;
        const t = (progress * track.points.length) % 1;
        
        const current = track.points[index];
        const next = track.points[nextIndex];
        
        return {
            x: Utils.lerp(current.x, next.x, t),
            y: Utils.lerp(current.y, next.y, t),
            angle: Utils.angle(current.x, current.y, next.x, next.y)
        };
    },
    
    // Apply lane offset to position
    applyLaneOffset(x, y, angle, offset) {
        const perpAngle = angle + Math.PI / 2;
        return {
            x: x + Math.cos(perpAngle) * offset,
            y: y + Math.sin(perpAngle) * offset
        };
    },
    
    // Generate unique ID
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
};