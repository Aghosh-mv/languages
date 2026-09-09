# Game Development Example

# Initialize game
print "=== Initializing Game ==="
let canvas = gui.createCanvas(800, 600)
let window = gui.createWindow("EasyLang Game", 800, 600)
window.setCanvas(canvas)

# Game state
let running = false
let score = 0
let lives = 3
let level = 1

# Player
let player = {
  x: 400,
  y: 500,
  width: 50,
  height: 50,
  speed: 5,
  color: "blue"
}

# Enemies
let enemies = []
let enemy_spawn_rate = 60  # frames
let enemy_counter = 0

# Bullets
let bullets = []
let bullet_spawn_rate = 10  # frames
let bullet_counter = 0

# Keys pressed
let keys = {}

# Game loop
function gameLoop() then
  while running
    # Handle input
    handleInput()
    
    # Update game state
    update()
    
    # Render
    render()
    
    # Delay
    delay(16)  # ~60 FPS
  end
end

# Handle input
function handleInput() then
  # Player movement
  if keys["LEFT"] then
    player.x = player.x - player.speed
    if player.x < 0 then
      player.x = 0
    end
  end
  
  if keys["RIGHT"] then
    player.x = player.x + player.speed
    if player.x > 800 - player.width then
      player.x = 800 - player.width
    end
  end
  
  if keys["UP"] then
    player.y = player.y - player.speed
    if player.y < 0 then
      player.y = 0
    end
  end
  
  if keys["DOWN"] then
    player.y = player.y + player.speed
    if player.y > 600 - player.height then
      player.y = 600 - player.height
    end
  end
  
  # Shooting
  if keys["SPACE"] then
    if bullet_counter >= bullet_spawn_rate then
      shootBullet()
      bullet_counter = 0
    end
  end
end

# Update game state
function update() then
  # Update bullets
  for i in range(len(bullets) - 1, -1, -1)
    bullets[i].y = bullets[i].y - bullets[i].speed
    
    # Remove off-screen bullets
    if bullets[i].y < 0 then
      bullets.splice(i, 1)
    end
  end
  
  # Update enemies
  enemy_counter = enemy_counter + 1
  if enemy_counter >= enemy_spawn_rate then
    spawnEnemy()
    enemy_counter = 0
  end
  
  for i in range(len(enemies) - 1, -1, -1)
    enemies[i].y = enemies[i].y + enemies[i].speed
    
    # Remove off-screen enemies
    if enemies[i].y > 600 then
      enemies.splice(i, 1)
      lives = lives - 1
      
      if lives <= 0 then
        gameOver()
      end
    end
  end
  
  # Check collisions
  checkCollisions()
end

# Check collisions
function checkCollisions() then
  # Bullet-enemy collisions
  for i in range(len(bullets) - 1, -1, -1)
    for j in range(len(enemies) - 1, -1, -1)
      if checkCollision(bullets[i], enemies[j]) then
        # Remove bullet and enemy
        bullets.splice(i, 1)
        enemies.splice(j, 1)
        
        # Increase score
        score = score + 10
        
        # Check for level up
        if score >= level * 100 then
          levelUp()
        end
        
        break
      end
    end
  end
  
  # Player-enemy collisions
  for i in range(len(enemies) - 1, -1, -1)
    if checkCollision(player, enemies[i]) then
      # Remove enemy
      enemies.splice(i, 1)
      
      # Decrease lives
      lives = lives - 1
      
      if lives <= 0 then
        gameOver()
      end
    end
  end
end

# Check collision between two objects
function checkCollision(obj1, obj2) then
  return obj1.x < obj2.x + obj2.width &&
         obj1.x + obj1.width > obj2.x &&
         obj1.y < obj2.y + obj2.height &&
         obj1.y + obj1.height > obj2.y
end

# Shoot bullet
function shootBullet() then
  let bullet = {
    x: player.x + player.width / 2 - 2,
    y: player.y,
    width: 4,
    height: 10,
    speed: 10,
    color: "red"
  }
  bullets.push(bullet)
end

# Spawn enemy
function spawnEnemy() then
  let enemy = {
    x: random(0, 800 - 30),
    y: -30,
    width: 30,
    height: 30,
    speed: 2 + level * 0.5,
    color: "green"
  }
  enemies.push(enemy)
end

# Level up
function levelUp() then
  level = level + 1
  enemy_spawn_rate = max(30, enemy_spawn_rate - 5)
  print "Level up! Level:", level
end

# Game over
function gameOver() then
  running = false
  print "Game Over! Final Score:", score
  
  # Show game over screen
  canvas.clear()
  canvas.setColor("black")
  canvas.fillRect(0, 0, 800, 600)
  
  canvas.setColor("white")
  canvas.setFont("Arial", 48)
  canvas.drawText("Game Over", 300, 200)
  
  canvas.setFont("Arial", 24)
  canvas.drawText("Final Score: " + str(score), 350, 300)
  canvas.drawText("Press R to restart", 350, 400)
end

# Render game
function render() then
  # Clear canvas
  canvas.clear()
  
  # Draw background
  canvas.setColor("black")
  canvas.fillRect(0, 0, 800, 600)
  
  # Draw player
  canvas.setColor(player.color)
  canvas.fillRect(player.x, player.y, player.width, player.height)
  
  # Draw bullets
  canvas.setColor("red")
  for bullet in bullets
    canvas.fillRect(bullet.x, bullet.y, bullet.width, bullet.height)
  end
  
  # Draw enemies
  canvas.setColor("green")
  for enemy in enemies
    canvas.fillRect(enemy.x, enemy.y, enemy.width, enemy.height)
  end
  
  # Draw UI
  canvas.setColor("white")
  canvas.setFont("Arial", 16)
  canvas.drawText("Score: " + str(score), 10, 30)
  canvas.drawText("Lives: " + str(lives), 10, 50)
  canvas.drawText("Level: " + str(level), 10, 70)
  
  # Update canvas
  canvas.refresh()
end

# Start game
function startGame() then
  # Reset game state
  score = 0
  lives = 3
  level = 1
  enemy_spawn_rate = 60
  enemy_counter = 0
  bullet_counter = 0
  
  # Reset player
  player.x = 400
  player.y = 500
  
  # Clear arrays
  enemies = []
  bullets = []
  
  # Start game loop
  running = true
  gameLoop()
end

# Key event handlers
window.onKeyDown((key) -> {
  keys[key] = true
  
  # Start game on enter
  if key == "ENTER" and not running then
    startGame()
  end
  
  # Restart game on R
  if key == "R" and not running then
    startGame()
  end
})

window.onKeyUp((key) -> {
  keys[key] = false
})

# Show start screen
print "=== Game Started ==="
print "Press ENTER to start"
print "Use arrow keys to move"
print "Press SPACE to shoot"

canvas.setColor("black")
canvas.fillRect(0, 0, 800, 600)

canvas.setColor("white")
canvas.setFont("Arial", 48)
canvas.drawText("Space Invaders", 250, 200)

canvas.setFont("Arial", 24)
canvas.drawText("Press ENTER to start", 300, 300)
canvas.drawText("Arrow keys to move", 300, 350)
canvas.drawText("SPACE to shoot", 300, 400)

canvas.refresh()
window.setVisible(true)

print ""
print "=== Game Development Example Complete ==="
