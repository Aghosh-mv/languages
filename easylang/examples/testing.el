# Testing Example

# Unit testing framework
print "=== Unit Testing ==="

# Test function
function add(a, b) then
  return a + b
end

# Test case
function test_add() then
  assert(add(2, 3) == 5, "2 + 3 should be 5")
  assert(add(-1, 1) == 0, "-1 + 1 should be 0")
  assert(add(0, 0) == 0, "0 + 0 should be 0")
  print "✓ test_add passed"
end

# Run test
test_add()
print ""

# More complex tests
print "=== Complex Tests ==="

# Test class
class Calculator then
  function add(a, b) then
    return a + b
  end
  
  function subtract(a, b) then
    return a - b
  end
  
  function multiply(a, b) then
    return a * b
  end
  
  function divide(a, b) then
    if b == 0 then
      throw "Division by zero"
    end
    return a / b
  end
end

# Test cases
function test_calculator() then
  let calc = new Calculator()
  
  # Test add
  assert(calc.add(2, 3) == 5, "Addition failed")
  assert(calc.add(-1, 1) == 0, "Addition with negative failed")
  
  # Test subtract
  assert(calc.subtract(5, 3) == 2, "Subtraction failed")
  assert(calc.subtract(3, 5) == -2, "Subtraction with negative failed")
  
  # Test multiply
  assert(calc.multiply(2, 3) == 6, "Multiplication failed")
  assert(calc.multiply(-2, 3) == -6, "Multiplication with negative failed")
  
  # Test divide
  assert(calc.divide(6, 3) == 2, "Division failed")
  assert(calc.divide(5, 2) == 2.5, "Division with decimal failed")
  
  # Test division by zero
  try
    calc.divide(1, 0)
    assert(false, "Should throw division by zero error")
  catch error
    assert(error == "Division by zero", "Wrong error message")
  end
  
  print "✓ test_calculator passed"
end

test_calculator()
print ""

# Integration testing
print "=== Integration Testing ==="

# Test API endpoint
function test_api_endpoint() then
  let response = http.get("https://api.example.com/health")
  
  assert(response.status == 200, "Health check failed")
  assert(response.body.status == "ok", "Health status not ok")
  
  print "✓ test_api_endpoint passed"
end

test_api_endpoint()
print ""

# Mocking
print "=== Mocking ==="

# Mock function
function mock_http_get(url) then
  return {
    status: 200,
    body: {data: "mocked data"}
  }
end

# Test with mock
function test_with_mock() then
  # Save original function
  let original_get = http.get
  
  # Replace with mock
  http.get = mock_http_get
  
  # Run test
  let response = http.get("https://api.example.com/data")
  assert(response.status == 200, "Mock test failed")
  assert(response.body.data == "mocked data", "Mock data failed")
  
  # Restore original function
  http.get = original_get
  
  print "✓ test_with_mock passed"
end

test_with_mock()
print ""

# Parameterized testing
print "=== Parameterized Testing ==="

# Test function
function is_even(n) then
  return n % 2 == 0
end

# Parameterized test cases
let test_cases = [
  {input: 2, expected: true},
  {input: 3, expected: false},
  {input: 0, expected: true},
  {input: -2, expected: true},
  {input: -3, expected: false}
]

# Run parameterized tests
function test_parameterized() then
  for case in test_cases
    let result = is_even(case.input)
    assert(result == case.expected, "Test failed for input: " + str(case.input))
  end
  print "✓ test_parameterized passed"
end

test_parameterized()
print ""

# Test fixtures
print "=== Test Fixtures ==="

# Setup function
function setup() then
  let db = database.connect("test_db")
  db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
  return db
end

# Teardown function
function teardown(db) then
  db.execute("DROP TABLE IF EXISTS users")
  db.close()
end

# Test with fixtures
function test_with_fixtures() then
  let db = setup()
  
  try
    # Test code
    db.execute("INSERT INTO users (name) VALUES (?)", ["Alice"])
    let users = db.query("SELECT * FROM users")
    assert(len(users) == 1, "Insert failed")
    assert(users[0].name == "Alice", "Name mismatch")
    
    print "✓ test_with_fixtures passed"
  finally
    teardown(db)
  end
end

test_with_fixtures()
print ""

# Performance testing
print "=== Performance Testing ==="

# Performance test
function test_performance() then
  let start_time = millis()
  
  # Run many iterations
  for i in range(100000)
    add(i, i + 1)
  end
  
  let end_time = millis()
  let duration = end_time - start_time
  
  print "Duration:", duration, "ms"
  assert(duration < 1000, "Performance test failed")
  
  print "✓ test_performance passed"
end

test_performance()
print ""

# Test reporting
print "=== Test Reporting ==="

# Test suite
let tests = [
  {name: "test_add", fn: test_add},
  {name: "test_calculator", fn: test_calculator},
  {name: "test_api_endpoint", fn: test_api_endpoint},
  {name: "test_with_mock", fn: test_with_mock},
  {name: "test_parameterized", fn: test_parameterized},
  {name: "test_with_fixtures", fn: test_with_fixtures},
  {name: "test_performance", fn: test_performance}
]

# Run all tests
let passed = 0
let failed = 0
let errors = []

for test in tests
  try
    test.fn()
    passed = passed + 1
  catch error
    failed = failed + 1
    errors.push({name: test.name, error: error})
  end
end

# Print report
print "Test Results:"
print "Passed:", passed
print "Failed:", failed
print "Total:", passed + failed

if failed > 0 then
  print "\nFailed tests:"
  for error in errors
    print " -", error.name, ":", error.error
  end
end

print ""
print "=== Testing Example Complete ==="
