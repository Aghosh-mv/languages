# Animations Example

# CSS animations
print "=== CSS Animations ==="

# Define animation keyframes
let keyframes = """
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

@keyframes bounce {
  0%, 20%, 53%, 80%, 100% { transform: translateY(0); }
  40%, 43% { transform: translateY(-20px); }
  70% { transform: translateY(-10px); }
  90% { transform: translateY(-4px); }
}
"""

# Apply animation to element
let element = gui.createDiv()
element.setStyle("animation", "fadeIn 1s ease-in-out")
element.setText("Animated content")

print "CSS animations defined"
print ""

# JavaScript animations
print "=== JavaScript Animations ==="

# Simple animation
function animate(element, property, start, end, duration) then
  let startTime = Date.now()
  
  function update() then
    let elapsed = Date.now() - startTime
    let progress = min(elapsed / duration, 1)
    
    # Easing function
    let easeProgress = progress * (2 - progress)
    
    let currentValue = start + (end - start) * easeProgress
    element.setStyle(property, currentValue + "px")
    
    if progress < 1 then
      requestAnimationFrame(update)
    end
  end
  
  update()
end

# Test animation
let box = gui.createDiv()
box.setStyle("width", "100px")
box.setStyle("height", "100px")
box.setStyle("background-color", "blue")

animate(box, "left", 0, 500, 1000)
print "Simple animation started"
print ""

# Complex animations
print "=== Complex Animations ==="

# Animation sequence
function animateSequence(elements, duration) then
  let delay = duration / len(elements)
  
  for i in range(len(elements))
    setTimeout(() -> {
      elements[i].setStyle("opacity", "1")
      elements[i].setStyle("transform", "translateY(0)")
    }, i * delay)
  end
end

# Create elements
let items = []
for i in range(5)
  let item = gui.createDiv()
  item.setStyle("opacity", "0")
  item.setStyle("transform", "translateY(20px)")
  item.setStyle("transition", "all 0.5s ease")
  item.setText("Item " + (i + 1))
  items.push(item)
end

# Animate sequence
animateSequence(items, 1000)
print "Complex animation started"
print ""

# Physics-based animations
print "=== Physics-based Animations ==="

# Spring animation
function springAnimation(element, property, target, stiffness, damping) then
  let position = parseFloat(element.getStyle(property)) || 0
  let velocity = 0
  
  function update() then
    let force = (target - position) * stiffness
    let dampingForce = -velocity * damping
    let acceleration = force + dampingForce
    
    velocity = velocity + acceleration * 0.016
    position = position + velocity * 0.016
    
    element.setStyle(property, position + "px")
    
    if abs(velocity) > 0.01 or abs(target - position) > 0.01 then
      requestAnimationFrame(update)
    end
  end
  
  update()
end

# Test spring animation
let ball = gui.createDiv()
ball.setStyle("width", "50px")
ball.setStyle("height", "50px")
ball.setStyle("background-color", "red")
ball.setStyle("border-radius", "50%")
ball.setStyle("position", "absolute")

springAnimation(ball, "left", 500, 0.1, 0.8)
print "Spring animation started"
print ""

# Parallax scrolling
print "=== Parallax Scrolling ==="

# Create parallax container
let container = gui.createDiv()
container.setStyle("height", "2000px")
container.setStyle("position", "relative")

# Create background layers
let background = gui.createDiv()
background.setStyle("position", "absolute")
background.setStyle("top", "0")
background.setStyle("left", "0")
background.setStyle("width", "100%")
background.setStyle("height", "100%")
background.setStyle("background", "linear-gradient(to bottom, #000000, #0000ff)")

let midground = gui.createDiv()
midground.setStyle("position", "absolute")
midground.setStyle("top", "0")
midground.setStyle("left", "0")
midground.setStyle("width", "100%")
midground.setStyle("height", "100%")

let foreground = gui.createDiv()
foreground.setStyle("position", "absolute")
foreground.setStyle("top", "0")
foreground.setStyle("left", "0")
foreground.setStyle("width", "100%")
foreground.setStyle("height", "100%")

# Parallax effect
window.onScroll(() => {
  let scrollY = window.scrollY
  
  background.setStyle("transform", "translateY(" + (scrollY * 0.1) + "px)")
  midground.setStyle("transform", "translateY(" + (scrollY * 0.3) + "px)")
  foreground.setStyle("transform", "translateY(" + (scrollY * 0.6) + "px)")
})

print "Parallax scrolling set up"
print ""

# Scroll animations
print "=== Scroll Animations ==="

# Intersection Observer
let observer = new IntersectionObserver((entries) -> {
  for entry in entries
    if entry.isIntersecting then
      entry.target.classList.add("animate-in")
    else
      entry.target.classList.remove("animate-in")
    end
  end
}, {threshold: 0.1})

# Observe elements
let elements = document.querySelectorAll(".animate-on-scroll")
for element in elements
  observer.observe(element)
end

print "Scroll animations set up"
print ""

# SVG animations
print "=== SVG Animations ==="

# Create SVG
let svg = gui.createSVG(200, 200)

# Create circle
let circle = svg.createCircle(100, 100, 50)
circle.setAttribute("fill", "blue")

# Animate circle
let animate = svg.createAnimate(circle, "r", "50;80;50", "2s", "infinite")
animate.setAttribute("repeatCount", "infinite")

print "SVG animation created"
print ""

# Canvas animations
print "=== Canvas Animations ==="

# Create canvas
let canvas = gui.createCanvas(800, 600)
let ctx = canvas.getContext("2d")

# Animation loop
let animationId = null
let angle = 0

function animate() then
  # Clear canvas
  ctx.clearRect(0, 0, 800, 600)
  
  # Draw rotating square
  ctx.save()
  ctx.translate(400, 300)
  ctx.rotate(angle)
  ctx.fillStyle = "blue"
  ctx.fillRect(-50, -50, 100, 100)
  ctx.restore()
  
  # Update angle
  angle += 0.01
  
  # Continue animation
  animationId = requestAnimationFrame(animate)
end

# Start animation
animate()
print "Canvas animation started"
print ""

# Stop animation
function stopAnimation() then
  if animationId then
    cancelAnimationFrame(animationId)
    animationId = null
  end
end

# GIF-like animations
print "=== GIF-like Animations ==="

# Create sprite sheet
let spriteSheet = gui.createImage("sprites.png")
let frameWidth = 64
let frameHeight = 64
let totalFrames = 8
let currentFrame = 0
let frameRate = 1000 / 12  # 12 FPS

# Animation timer
let animationTimer = setInterval(() -> {
  # Calculate position
  let x = (currentFrame % 8) * frameWidth
  let y = Math.floor(currentFrame / 8) * frameHeight
  
  # Update sprite position
  spriteSheet.setStyle("background-position", -x + "px " + -y + "px")
  
  # Update frame
  currentFrame = (currentFrame + 1) % totalFrames
}, frameRate)

print "GIF-like animation started"
print ""

# Transition effects
print "=== Transition Effects ==="

# Hover transitions
let button = gui.createButton("Hover me")
button.setStyle("transition", "all 0.3s ease")
button.onMouseEnter(() -> {
  button.setStyle("background-color", "darkblue")
  button.setStyle("color", "white")
  button.setStyle("transform", "scale(1.1)")
})
button.onMouseLeave(() -> {
  button.setStyle("background-color", "blue")
  button.setStyle("color", "white")
  button.setStyle("transform", "scale(1)")
})

print "Transition effects set up"
print ""

# Loading animations
print "=== Loading Animations ==="

# Spinner
let spinner = gui.createDiv()
spinner.setStyle("width", "50px")
spinner.setStyle("height", "50px")
spinner.setStyle("border", "5px solid #f3f3f3")
spinner.setStyle("border-top", "5px solid #3498db")
spinner.setStyle("border-radius", "50%")
spinner.setStyle("animation", "spin 1s linear infinite")

# Keyframe for spinner
let spinKeyframes = """
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
"""

print "Loading animation created"
print ""

# Page transitions
print "=== Page Transitions ==="

# Create page transition
function transitionToPage(newContent) then
  let currentPage = document.querySelector(".current-page")
  let newPage = gui.createDiv()
  newPage.classList.add("page")
  newPage.setHTML(newContent)
  
  # Animate out current page
  currentPage.setStyle("opacity", "0")
  currentPage.setStyle("transform", "translateX(-100%)")
  
  # After animation, replace content
  setTimeout(() -> {
    currentPage.remove()
    newPage.setStyle("opacity", "0")
    newPage.setStyle("transform", "translateX(100%)")
    document.body.add(newPage)
    
    # Animate in new page
    setTimeout(() -> {
      newPage.setStyle("opacity", "1")
      newPage.setStyle("transform", "translateX(0)")
    }, 50)
  }, 500)
end

print "Page transitions set up"
print ""

print "=== Animations Example Complete ==="
