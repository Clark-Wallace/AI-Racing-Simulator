// Main entry point
let game = null;
let animationId = null;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('gameCanvas');
    game = new RacingGame(canvas);
    
    setupMenuHandlers();
    setupKeyboardHandlers();
});

function setupMenuHandlers() {
    // Track selection
    document.querySelectorAll('.track-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.track-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
        });
    });
    
    // Laps selection
    document.querySelectorAll('.laps-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.laps-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
        });
    });
    
    // Weather selection
    document.querySelectorAll('.weather-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.weather-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
        });
    });
    
    // Start button
    document.getElementById('startButton').addEventListener('click', startRace);
}

function setupKeyboardHandlers() {
    document.addEventListener('keydown', (e) => {
        if (game) {
            game.handleKeyPress(e.key);
        }
        
        // Global escape to return to menu
        if (e.key === 'Escape' && game.state === 'racing') {
            stopRace();
            showMenu();
        }
    });
}

function startRace() {
    // Get selected options
    const track = document.querySelector('.track-btn.selected').dataset.track;
    const laps = parseInt(document.querySelector('.laps-btn.selected').dataset.laps);
    const weather = document.querySelector('.weather-btn.selected').dataset.weather;
    
    // Hide menu
    document.getElementById('menu').style.display = 'none';
    
    // Show HUD elements
    document.getElementById('hud').style.display = 'block';
    document.getElementById('powerups').style.display = 'block';
    document.getElementById('ammo').style.display = 'block';
    document.getElementById('controls').style.display = 'block';
    
    // Initialize game
    game.init({ track, laps, weather });
    
    // Start game loop
    gameLoop();
}

function stopRace() {
    if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
    }
}

function showMenu() {
    // Show menu
    document.getElementById('menu').style.display = 'block';
    
    // Hide HUD elements
    document.getElementById('hud').style.display = 'none';
    document.getElementById('powerups').style.display = 'none';
    document.getElementById('ammo').style.display = 'none';
    document.getElementById('controls').style.display = 'none';
    
    // Reset game state
    game.state = 'menu';
}

function gameLoop(currentTime = 0) {
    // Update game
    game.update(currentTime);
    
    // Render game
    game.render();
    
    // Continue loop
    if (game.state === 'racing' || game.state === 'paused' || game.state === 'waitingForFlag') {
        animationId = requestAnimationFrame(gameLoop);
    } else if (game.state === 'finished') {
        // Show results after a delay
        setTimeout(() => {
            stopRace();
            showMenu();
        }, 5000);
    }
}

// Demo mode - show a preview race in the background
function runDemoMode() {
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    let angle = 0;
    function drawDemo() {
        // Simple animated background
        ctx.fillStyle = '#0a0a0a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw some moving shapes
        ctx.strokeStyle = '#0ff';
        ctx.lineWidth = 2;
        ctx.globalAlpha = 0.3;
        
        for (let i = 0; i < 5; i++) {
            ctx.beginPath();
            const radius = 100 + i * 50;
            const x = canvas.width / 2 + Math.cos(angle + i * 0.5) * 50;
            const y = canvas.height / 2 + Math.sin(angle + i * 0.5) * 50;
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.stroke();
        }
        
        ctx.globalAlpha = 1;
        angle += 0.01;
        
        if (game.state === 'menu') {
            requestAnimationFrame(drawDemo);
        }
    }
    
    drawDemo();
}

// Start demo mode on load
runDemoMode();