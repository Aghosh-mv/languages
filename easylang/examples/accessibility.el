# Accessibility Example

# ARIA attributes
print "=== ARIA Attributes ==="

# Create accessible button
let button = gui.createButton("Click me")
button.setAttribute("aria-label", "Click this button to perform an action")
button.setAttribute("aria-describedby", "button-description")

# Create description element
let description = gui.createLabel("This button performs an important action")
description.setAttribute("id", "button-description")
description.setAttribute("aria-hidden", "true")

print "Accessible button created"
print ""

# Keyboard navigation
print "=== Keyboard Navigation ==="

# Handle keyboard events
window.onKeyDown((event) -> {
  # Tab navigation
  if event.key == "Tab" then
    if event.shiftKey then
      # Move focus to previous element
      let current = document.activeElement
      let previous = current.previousElementSibling
      if previous then
        previous.focus()
      end
    else
      # Move focus to next element
      let current = document.activeElement
      let next = current.nextElementSibling
      if next then
        next.focus()
      end
    end
    event.preventDefault()
  end
  
  # Enter/Space to activate
  if event.key == "Enter" or event.key == " " then
    if document.activeElement.tagName == "BUTTON" then
      document.activeElement.click()
      event.preventDefault()
    end
  end
  
  # Escape to close
  if event.key == "Escape" then
    let modal = document.querySelector("[aria-modal='true']")
    if modal then
      modal.close()
    end
  end
})

print "Keyboard navigation set up"
print ""

# Screen reader support
print "=== Screen Reader Support ==="

# Live regions
let liveRegion = gui.createDiv()
liveRegion.setAttribute("aria-live", "polite")
liveRegion.setAttribute("aria-atomic", "true")

# Announce messages
function announce(message) then
  liveRegion.setText("")
  setTimeout(() -> {
    liveRegion.setText(message)
  }, 100)
end

# Test announcement
announce("Form submitted successfully")
print "Screen reader announcement made"
print ""

# Focus management
print "=== Focus Management ==="

# Trap focus in modal
function trapFocus(modal) then
  let focusableElements = modal.querySelectorAll(
    "button, [href], input, select, textarea, [tabindex]:not([tabindex='-1'])"
  )
  
  let firstElement = focusableElements[0]
  let lastElement = focusableElements[focusableElements.length - 1]
  
  modal.addEventListener("keydown", (event) => {
    if event.key == "Tab" then
      if event.shiftKey then
        if document.activeElement == firstElement then
          lastElement.focus()
          event.preventDefault()
        end
      else
        if document.activeElement == lastElement then
          firstElement.focus()
          event.preventDefault()
        end
      end
    end
  })
end

# Set initial focus
function setInitialFocus(modal) then
  let firstFocusable = modal.querySelector(
    "button, [href], input, select, textarea, [tabindex]:not([tabindex='-1'])"
  )
  if firstFocusable then
    firstFocusable.focus()
  end
end

print "Focus management set up"
print ""

# Color contrast
print "=== Color Contrast ==="

# Check color contrast
function checkContrast(foreground, background) then
  let ratio = getContrastRatio(foreground, background)
  
  # WCAG 2.1 requirements
  let aaNormal = ratio >= 4.5
  let aaLarge = ratio >= 3
  let aaaNormal = ratio >= 7
  let aaaLarge = ratio >= 4.5
  
  return {
    ratio: ratio,
    aaNormal: aaNormal,
    aaLarge: aaLarge,
    aaaNormal: aaaNormal,
    aaaLarge: aaaLarge
  }
end

# Test colors
let result = checkContrast("#000000", "#FFFFFF")
print "Contrast ratio:", result.ratio
print "AA Normal:", result.aaNormal
print "AA Large:", result.aaLarge
print "AAA Normal:", result.aaaNormal
print "AAA Large:", result.aaaLarge
print ""

# Alternative text
print "=== Alternative Text ==="

# Image with alt text
let image = gui.createImage("photo.jpg")
image.setAttribute("alt", "A beautiful sunset over the ocean")
image.setAttribute("role", "img")

# Decorative image
let decorativeImage = gui.createImage("background.jpg")
decorativeImage.setAttribute("alt", "")
decorativeImage.setAttribute("role", "presentation")

print "Alternative text set"
print ""

# Forms
print "=== Accessible Forms ==="

# Form with labels
let form = gui.createForm()

let nameLabel = gui.createLabel("Name")
nameLabel.setAttribute("for", "name-input")
let nameInput = gui.createInput("text")
nameInput.setAttribute("id", "name-input")
nameInput.setAttribute("aria-required", "true")
nameInput.setAttribute("aria-describedby", "name-error")

let nameError = gui.createLabel("")
nameError.setAttribute("id", "name-error")
nameError.setAttribute("aria-live", "polite")

form.add(nameLabel)
form.add(nameInput)
form.add(nameError)

# Validation
nameInput.onBlur(() -> {
  if nameInput.value == "" then
    nameError.setText("Name is required")
    nameInput.setAttribute("aria-invalid", "true")
  else
    nameError.setText("")
    nameInput.setAttribute("aria-invalid", "false")
  end
})

print "Accessible form created"
print ""

# Tables
print "=== Accessible Tables ==="

# Create accessible table
let table = gui.createTable()
table.setAttribute("role", "table")
table.setAttribute("aria-label", "User information")

let thead = gui.createTableHead()
let headerRow = gui.createTableRow()
let nameHeader = gui.createTableHeader("Name")
nameHeader.setAttribute("scope", "col")
let ageHeader = gui.createTableHeader("Age")
ageHeader.setAttribute("scope", "col")
headerRow.add(nameHeader)
headerRow.add(ageHeader)
thead.add(headerRow)
table.add(thead)

let tbody = gui.createTableBody()
let row1 = gui.createTableRow()
let nameCell1 = gui.createTableCell("Alice")
nameCell1.setAttribute("scope", "row")
let ageCell1 = gui.createTableCell("30")
row1.add(nameCell1)
row1.add(ageCell1)
tbody.add(row1)
table.add(tbody)

print "Accessible table created"
print ""

# Navigation
print "=== Accessible Navigation ==="

# Create accessible navigation
let nav = gui.createNavigation()
nav.setAttribute("role", "navigation")
nav.setAttribute("aria-label", "Main navigation")

let ul = gui.createList()
ul.setAttribute("role", "menubar")

let li1 = gui.createListItem()
li1.setAttribute("role", "none")
let link1 = gui.createLink("Home", "#home")
link1.setAttribute("role", "menuitem")
li1.add(link1)
ul.add(li1)

let li2 = gui.createListItem()
li2.setAttribute("role", "none")
let link2 = gui.createLink("About", "#about")
link2.setAttribute("role", "menuitem")
li2.add(link2)
ul.add(li2)

nav.add(ul)
print "Accessible navigation created"
print ""

# ARIA landmarks
print "=== ARIA Landmarks ==="

# Create landmarks
let header = gui.createHeader()
header.setAttribute("role", "banner")

let main = gui.createMain()
main.setAttribute("role", "main")

let footer = gui.createFooter()
footer.setAttribute("role", "contentinfo")

let aside = gui.createAside()
aside.setAttribute("role", "complementary")

print "ARIA landmarks created"
print ""

# Live regions
print "=== Live Regions ==="

# Polite announcements
let politeRegion = gui.createDiv()
politeRegion.setAttribute("aria-live", "polite")
politeRegion.setAttribute("aria-atomic", "true")

# Assertive announcements
let assertiveRegion = gui.createDiv()
assertiveRegion.setAttribute("aria-live", "assertive")
assertiveRegion.setAttribute("aria-atomic", "true")

# Status messages
function showStatus(message) then
  politeRegion.setText(message)
end

# Error messages
function showError(message) then
  assertiveRegion.setText(message)
end

# Test messages
showStatus("Form saved successfully")
showError("Please correct the errors")

print "Live regions set up"
print ""

# Reduced motion
print "=== Reduced Motion ==="

# Check for reduced motion preference
let prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)")

if prefersReducedMotion.matches then
  print "User prefers reduced motion"
  # Disable animations
  document.documentElement.style.setProperty("--animation-duration", "0s")
else
  print "User does not prefer reduced motion"
end

print ""

# High contrast mode
print "=== High Contrast Mode ==="

# Check for high contrast mode
let isHighContrast = window.matchMedia("(prefers-contrast: more)")

if isHighContrast.matches then
  print "User prefers high contrast"
  # Apply high contrast styles
  document.documentElement.classList.add("high-contrast")
else
  print "User does not prefer high contrast"
end

print ""

print "=== Accessibility Example Complete ==="
