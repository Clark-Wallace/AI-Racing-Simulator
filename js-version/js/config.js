// Game configuration
const CONFIG = {
    CANVAS_WIDTH: 1200,
    CANVAS_HEIGHT: 800,
    FPS: 60,
    
    // Physics
    PHYSICS: {
        GRAVITY: 9.81,
        AIR_RESISTANCE: 0.001,
        TIRE_FRICTION: 0.8,
        BRAKE_EFFICIENCY: 1.5
    },
    
    // Car configurations
    CAR: {
        MAX_SPEED: 450, // km/h (increased from 320)
        ACCELERATION: 250, // km/h/s (increased from 150)
        BRAKING: 300, // km/h/s (increased from 200)
        TURN_SPEED: 4, // radians/s (increased from 3)
        SIZE: 30, // pixels
        FUEL_CAPACITY: 60, // liters
        FUEL_CONSUMPTION: 0.03 // liters/second (reduced consumption)
    },
    
    // Track configurations
    TRACK: {
        WIDTH: 120, // pixels
        SEGMENT_LENGTH: 50 // pixels
    },
    
    // Power-up configurations
    POWERUPS: {
        SPAWN_INTERVAL: 5000, // ms
        PICKUP_RADIUS: 0.0001, // 0.01% of track length (slightly increased for easier pickup)
        BOX_SIZE: 15, // pixels (slightly bigger visual but same small pickup radius)
        RESPAWN_TIME: 5000 // ms
    },
    
    // Weapon configurations
    WEAPONS: {
        AMMO_COUNT: 50,
        FIRE_RATE: 200, // ms between shots
        BULLET_SPEED: 1000, // pixels/second
        DAMAGE: 0.15, // 15% speed reduction
        RANGE: 300, // pixels
        HIT_DURATION: 500 // ms to show hit effect
    },
    
    // AI configurations
    AI: {
        DECISION_INTERVAL: 250, // ms between decisions (faster from 500)
        VISION_RANGE: 300, // pixels (increased from 200)
        REACTION_TIME: 50 // ms (faster from 100)
    },
    
    // Visual settings
    VISUALS: {
        SHOW_TELEMETRY: true,
        SHOW_AI_THOUGHTS: true,
        PARTICLE_COUNT: 50,
        TRAIL_LENGTH: 20
    }
};

// Driver personalities
const DRIVER_STYLES = {
    AGGRESSIVE: {
        name: "Aggressive",
        acceleration: 1.2,
        braking: 0.8,
        cornering: 0.9,
        riskTaking: 0.9,
        fuelEfficiency: 0.7,
        color: "#ff0000"
    },
    STRATEGIC: {
        name: "Strategic",
        acceleration: 0.9,
        braking: 1.1,
        cornering: 1.0,
        riskTaking: 0.4,
        fuelEfficiency: 1.2,
        color: "#0064ff"
    },
    BALANCED: {
        name: "Balanced",
        acceleration: 1.0,
        braking: 1.0,
        cornering: 1.0,
        riskTaking: 0.6,
        fuelEfficiency: 1.0,
        color: "#ffd700"
    },
    CHAOTIC: {
        name: "Chaotic",
        acceleration: 1.1,
        braking: 0.9,
        cornering: 0.8,
        riskTaking: 1.0,
        fuelEfficiency: 0.8,
        color: "#b400ff"
    },
    TECHNICAL: {
        name: "Technical",
        acceleration: 0.95,
        braking: 1.2,
        cornering: 1.2,
        riskTaking: 0.3,
        fuelEfficiency: 1.1,
        color: "#00ff80"
    }
};

// Car configurations for each driver
const CAR_CONFIGS = [
    {
        name: "Llama Speed",
        style: DRIVER_STYLES.AGGRESSIVE,
        aiType: "llm",
        model: "speed"
    },
    {
        name: "Llama Strategic",
        style: DRIVER_STYLES.STRATEGIC,
        aiType: "llm",
        model: "strategic"
    },
    {
        name: "Llama Balanced",
        style: DRIVER_STYLES.BALANCED,
        aiType: "llm",
        model: "balanced"
    },
    {
        name: "Hermes Chaos",
        style: DRIVER_STYLES.CHAOTIC,
        aiType: "llm",
        model: "chaos"
    },
    {
        name: "Qwen Technical",
        style: DRIVER_STYLES.TECHNICAL,
        aiType: "llm",
        model: "technical"
    }
];

// Track configurations
const TRACKS = {
    monaco: {
        name: "Monaco Street Circuit",
        length: 3.337, // km
        type: "street",
        difficulty: "hard",
        color: "#666666"
    },
    silverstone: {
        name: "Silverstone Grand Prix",
        length: 5.891,
        type: "technical",
        difficulty: "medium",
        color: "#228822"
    },
    nurburgring: {
        name: "Nürburgring Nordschleife",
        length: 20.832,
        type: "endurance",
        difficulty: "extreme",
        color: "#443322"
    },
    suzuka: {
        name: "Suzuka International",
        length: 5.807,
        type: "mixed",
        difficulty: "hard",
        color: "#882244"
    },
    rainbow: {
        name: "Rainbow Road",
        length: 2.000,
        type: "fantasy",
        difficulty: "chaotic",
        color: "#ff00ff"
    },
    speedway: {
        name: "Big Oval Speedway",
        length: 4.000,
        type: "oval",
        difficulty: "easy",
        color: "#0066cc"
    }
};