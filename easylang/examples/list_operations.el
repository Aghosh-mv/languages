# List Operations Example

# Create a list
let fruits = ["apple", "banana", "cherry", "date", "elderberry"]

# Print the list
print "Fruits:", fruits
print ""

# Get length
print "Number of fruits:", len(fruits)
print ""

# Add items
fruits.push("fig")
print "After push:", fruits
print ""

# Remove items
fruits.pop()
print "After pop:", fruits
print ""

# Sort
fruits.sort()
print "After sort:", fruits
print ""

# Reverse
fruits.reverse()
print "After reverse:", fruits
print ""

# Map
let upper_fruits = fruits.map((f) -> f.upper())
print "Uppercase:", upper_fruits
print ""

# Filter
let a_fruits = fruits.filter((f) -> f.startsWith("a"))
print "Starting with 'a':", a_fruits
print ""

# Reduce
let total_length = fruits.reduce((acc, f) -> acc + len(f), 0)
print "Total length:", total_length
print ""

# Find
let found = fruits.find((f) -> f == "cherry")
print "Found:", found
print ""

# Check existence
let has_apple = fruits.includes("apple")
print "Has apple:", has_apple
print ""

# Slice
let sliced = fruits.slice(1, 3)
print "Sliced:", sliced
print ""

# Splice
let spliced = fruits.splice(1, 2, "fig", "grape")
print "Spliced:", spliced
print "Remaining:", fruits
