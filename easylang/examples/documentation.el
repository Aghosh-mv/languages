# Documentation Example

# Generate documentation
print "=== Generating Documentation ==="

# Function documentation
function add(a, b) then
  # Add two numbers
  # 
  # Args:
  #   a: First number
  #   b: Second number
  # 
  # Returns:
  #   Sum of a and b
  # 
  # Example:
  #   add(2, 3)  # Returns 5
  
  return a + b
end

# Class documentation
class Calculator then
  # A simple calculator class
  # 
  # This class provides basic arithmetic operations.
  # 
  # Example:
  #   calc = new Calculator()
  #   calc.add(2, 3)  # Returns 5
  
  function add(a, b) then
    # Add two numbers
    # 
    # Args:
    #   a: First number
    #   b: Second number
    # 
    # Returns:
    #   Sum of a and b
    
    return a + b
  end
  
  function subtract(a, b) then
    # Subtract two numbers
    # 
    # Args:
    #   a: First number
    #   b: Second number
    # 
    # Returns:
    #   Difference of a and b
    
    return a - b
  end
end

# Module documentation
module MathUtils then
  # Mathematical utility functions
  # 
  # This module provides various mathematical functions.
  
  function factorial(n) then
    # Calculate factorial of a number
    # 
    # Args:
    #   n: Number to calculate factorial for
    # 
    # Returns:
    #   Factorial of n
    # 
    # Raises:
    #   ValueError: If n is negative
    # 
    # Example:
    #   factorial(5)  # Returns 120
    
    if n < 0 then
      throw "Factorial not defined for negative numbers"
    end
    
    if n == 0 then
      return 1
    end
    
    return n * factorial(n - 1)
  end
  
  function fibonacci(n) then
    # Calculate nth Fibonacci number
    # 
    # Args:
    #   n: Position in Fibonacci sequence
    # 
    # Returns:
    #   nth Fibonacci number
    # 
    # Example:
    #   fibonacci(10)  # Returns 55
    
    if n <= 0 then
      return 0
    end
    
    if n == 1 then
      return 1
    end
    
    return fibonacci(n - 1) + fibonacci(n - 2)
  end
end

# Generate API documentation
print "=== API Documentation ==="
let docs = documentation.generate(add)
print "Function:", docs.name
print "Description:", docs.description
print "Args:", docs.args
print "Returns:", docs.returns
print "Example:", docs.example
print ""

# Generate class documentation
print "=== Class Documentation ==="
let docs = documentation.generate(Calculator)
print "Class:", docs.name
print "Description:", docs.description
print "Methods:", docs.methods
print ""

# Generate module documentation
print "=== Module Documentation ==="
let docs = documentation.generate(MathUtils)
print "Module:", docs.name
print "Description:", docs.description
print "Functions:", docs.functions
print ""

# Generate markdown documentation
print "=== Markdown Documentation ==="
let markdown = documentation.toMarkdown(MathUtils)
print markdown
print ""

# Generate HTML documentation
print "=== HTML Documentation ==="
let html = documentation.toHTML(MathUtils)
file.write("docs/index.html", html)
print "HTML documentation generated: docs/index.html"
print ""

# Generate PDF documentation
print "=== PDF Documentation ==="
let pdf = documentation.toPDF(MathUtils)
file.write("docs/manual.pdf", pdf)
print "PDF documentation generated: docs/manual.pdf"
print ""

# Generate REST API documentation
print "=== REST API Documentation ==="
let api_docs = documentation.generateRESTAPI([
  {
    method: "GET",
    path: "/api/users",
    description: "Get all users",
    params: [],
    response: "Array of user objects"
  },
  {
    method: "GET",
    path: "/api/users/:id",
    description: "Get user by ID",
    params: [{name: "id", type: "integer", description: "User ID"}],
    response: "User object"
  },
  {
    method: "POST",
    path: "/api/users",
    description: "Create new user",
    params: [
      {name: "name", type: "string", description: "User name"},
      {name: "email", type: "string", description: "User email"}
    ],
    response: "Created user object"
  }
])

print "API Documentation:"
print api_docs
print ""

# Generate OpenAPI specification
print "=== OpenAPI Specification ==="
let openapi = documentation.generateOpenAPI(
  "My API",
  "1.0.0",
  "API for managing users",
  [
    {
      method: "GET",
      path: "/api/users",
      description: "Get all users",
      responses: {
        200: "Successful operation"
      }
    }
  ]
)

file.write("docs/openapi.json", JSON.stringify(openapi, null, 2))
print "OpenAPI specification generated: docs/openapi.json"
print ""

# Generate Swagger UI
print "=== Swagger UI ==="
let swagger_html = documentation.generateSwaggerUI("docs/openapi.json")
file.write("docs/swagger.html", swagger_html)
print "Swagger UI generated: docs/swagger.html"
print ""

# Documentation testing
print "=== Documentation Testing ==="

# Test code examples
function test_documentation_examples() then
  let examples = documentation.extractExamples(MathUtils)
  
  for example in examples
    try
      # Execute example
      let result = eval(example.code)
      
      # Check if result matches expected
      assert(result == example.expected, "Example failed: " + example.description)
      
      print "✓", example.description
    catch error
      print "✗", example.description, ":", error
    end
  end
end

test_documentation_examples()
print ""

# Documentation coverage
print "=== Documentation Coverage ==="

# Check documentation coverage
let coverage = documentation.checkCoverage(MathUtils)
print "Total functions:", coverage.total
print "Documented functions:", coverage.documented
print "Coverage percentage:", coverage.percentage, "%"

if coverage.percentage < 100 then
  print "\nUndocumented functions:"
  for func in coverage.undocumented
    print " -", func.name
  end
end

print ""
print "=== Documentation Example Complete ==="
