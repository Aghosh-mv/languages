// EasyLang v2 - The Human Programming Language
// Example: Simple calculator with functions

// Define a function to add two numbers
function add(a, b)
  return a + b
end

// Define a function to subtract
function subtract(a, b)
  return a - b
end

// Define a function to multiply
function multiply(a, b)
  return a * b
end

// Define a function to divide
function divide(a, b)
  if b == 0
    print "Error: Division by zero!"
    return 0
  end
  return a / b
end

// Main program
print "=== EasyLang v2 Calculator ==="
print ""

// Test the functions
let x = 10
let y = 5

print "x =", x
print "y =", y
print ""

print "x + y =", add(x, y)
print "x - y =", subtract(x, y)
print "x * y =", multiply(x, y)
print "x / y =", divide(x, y)
print ""

// Array operations
let numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print "Array:", numbers
print "Length:", len(numbers)
print "Sum:", sum(numbers)
print "Max:", max(numbers)
print "Min:", min(numbers)
print ""

// Loop example
print "Counting:"
for i in range(5)
  print "  ", i + 1
end
print ""

// Conditional example
let age = 25
if age >= 18
  print "You are an adult."
else
  print "You are a minor."
end
print ""

// Lambda example
let square = (x) -> x * x
let cube = (x) -> x * x * x

print "Square of 5:", square(5)
print "Cube of 5:", cube(5)
print ""

// Map example
let person = {name: "Alice", age: 30, city: "New York"}
print "Person:", person
print "Name:", person.name
print "Age:", person.age
print ""

// String operations
let greeting = "Hello, World!"
print "Greeting:", greeting
print "Length:", len(greeting)
print "Uppercase:", greeting.upper()
print ""

// Error handling
try
  let result = 10 / 0
  print "Result:", result
catch error
  print "Caught error:", error
end

print ""
print "=== Program Complete ==="
