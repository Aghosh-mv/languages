# Error Handling Example

# Basic try/catch
print "=== Basic Error Handling ==="
try
  let result = 10 / 0
  print "Result:", result
catch error
  print "Caught error:", error
end

print ""

# Custom errors
print "=== Custom Errors ==="
function divide(a, b) then
  if b == 0 then
    throw "Division by zero"
  end
  return a / b
end

try
  let result = divide(10, 0)
  print "Result:", result
catch error
  print "Error:", error
end

print ""

# Multiple catch blocks
print "=== Multiple Catch Blocks ==="
try
  let data = null
  print data.length
catch TypeError as e
  print "Type error:", e
catch ReferenceError as e
  print "Reference error:", e
catch error
  print "Unknown error:", error
end

print ""

# Finally block
print "=== Finally Block ==="
function riskyOperation() then
  try
    print "Starting operation..."
    let result = 10 / 0
    print "Result:", result
  catch error
    print "Error occurred:", error
  finally
    print "Cleaning up..."
  end
end

riskyOperation()

print ""

# Nested try/catch
print "=== Nested Try/Catch ==="
try
  try
    let result = 10 / 0
    print "Inner result:", result
  catch error
    print "Inner error:", error
    throw "Re-throwing error"
  end
catch error
  print "Outer error:", error
end

print ""

# Error propagation
print "=== Error Propagation ==="
function level1() then
  try
    level2()
  catch error
    print "Level 1 caught:", error
  end
end

function level2() then
  try
    level3()
  catch error
    print "Level 2 caught:", error
    throw error
  end
end

function level3() then
  throw "Error from level 3"
end

level1()

print ""

# Custom error classes
print "=== Custom Error Classes ==="
class ValidationError extends Error then
  let field = ""
  
  function init(field, message) then
    super.init(message)
    this.field = field
  end
end

function validateAge(age) then
  if age < 0 then
    throw new ValidationError("age", "Age cannot be negative")
  end
  if age > 150 then
    throw new ValidationError("age", "Age seems unrealistic")
  end
  return true
end

try
  validateAge(-5)
  print "Age is valid"
catch ValidationError as e
  print "Validation error:", e.field, "-", e.message
catch error
  print "Error:", error
end

try
  validateAge(200)
  print "Age is valid"
catch ValidationError as e
  print "Validation error:", e.field, "-", e.message
catch error
  print "Error:", error
end

print ""
print "=== Error Handling Complete ==="
