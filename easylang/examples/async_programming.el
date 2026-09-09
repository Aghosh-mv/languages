# Async Programming Example

# Async function
async function fetchData(url) then
  print "Fetching data from:", url
  
  # Simulate network request
  delay(1000)
  
  return {status: "success", data: "Hello World"}
end

# Await async function
async function main() then
  print "Starting async operations..."
  
  # Fetch data
  let result = await fetchData("https://api.example.com/data")
  print "Result:", result
  
  # Fetch multiple URLs in parallel
  let urls = [
    "https://api.example.com/users",
    "https://api.example.com/posts",
    "https://api.example.com/comments"
  ]
  
  let promises = urls.map((url) -> fetchData(url))
  let results = await Promise.all(promises)
  
  print "All results:", results
  
  print "Async operations complete"
end

# Run async main
main()

print "Program continues while async operations run"
