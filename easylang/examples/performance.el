# Performance Optimization Example

# Profiling
print "=== Profiling ==="

# Profile a function
function fibonacci(n) then
  if n <= 1 then
    return n
  end
  return fibonacci(n - 1) + fibonacci(n - 2)
end

# Profile the function
let profile = profiler.profile(() -> fibonacci(30))
print "Function:", profile.name
print "Time:", profile.time, "ms"
print "Memory:", profile.memory, "bytes"
print "Calls:", profile.calls
print ""

# Benchmark
print "=== Benchmark ==="

# Benchmark a function
let benchmark = benchmark.run("fibonacci", () -> fibonacci(30), iterations=100)
print "Benchmark:", benchmark.name
print "Average time:", benchmark.average_time, "ms"
print "Min time:", benchmark.min_time, "ms"
print "Max time:", benchmark.max_time, "ms"
print "Standard deviation:", benchmark.std_dev, "ms"
print ""

# Memory optimization
print "=== Memory Optimization ==="

# Object pooling
let pool = pool.create({
  initial_size: 100,
  max_size: 1000,
  factory: () -> ({data: null})
})

# Acquire objects from pool
let obj1 = pool.acquire()
let obj2 = pool.acquire()

# Use objects
obj1.data = "Hello"
obj2.data = "World"

# Return objects to pool
pool.release(obj1)
pool.release(obj2)

print "Pool size:", pool.size
print "Pool available:", pool.available
print ""

# Lazy loading
print "=== Lazy Loading ==="

# Lazy load a module
let lazy_module = lazy.load("expensive_module")

# Module is not loaded until accessed
print "Module loaded:", lazy_module.loaded

# Access module to trigger loading
let result = lazy_module.compute()
print "Module loaded:", lazy_module.loaded
print "Result:", result
print ""

# Caching
print "=== Caching ==="

# Simple cache
let cache = cache.create({
  max_size: 1000,
  ttl: 3600  # 1 hour
})

# Cache a function
let cached_fib = cache.memoize(fibonacci)

# Call function (will be cached)
let result1 = cached_fib(30)
print "First call result:", result1

# Call again (will use cache)
let result2 = cached_fib(30)
print "Second call result:", result2

# Check cache stats
print "Cache hits:", cache.hits
print "Cache misses:", cache.misses
print ""

# Memoization
print "=== Memoization ==="

# Memoize a function
let memoized_fib = memoize(fibonacci)

# Call function
let result = memoized_fib(30)
print "Result:", result

# Check memoization stats
print "Cache size:", memoized_fib.cache.size
print ""

# Concurrency
print "=== Concurrency ==="

# Async/await
async function fetchData(url) then
  let response = await http.get(url)
  return response.body
end

# Parallel execution
async function fetchMultiple(urls) then
  let promises = urls.map(url -> fetchData(url))
  let results = await Promise.all(promises)
  return results
end

# Execute parallel tasks
let urls = [
  "https://api.example.com/data1",
  "https://api.example.com/data2",
  "https://api.example.com/data3"
]

let results = fetchMultiple(urls)
print "Fetched", len(results), "results"
print ""

# Thread pool
print "=== Thread Pool ==="

# Create thread pool
let pool = threadPool.create({
  min_threads: 4,
  max_threads: 16,
  queue_size: 100
})

# Submit tasks
let futures = []
for i in range(10)
  let future = pool.submit(() -> {
    # Simulate work
    delay(100)
    return i * 2
  })
  futures.push(future)
end

# Wait for results
let results = futures.map(f -> f.get())
print "Results:", results

# Shutdown pool
pool.shutdown()
print ""

# Data structures
print "=== Optimized Data Structures ==="

# Bloom filter
let bloom = bloomFilter.create({
  expected_items: 1000,
  false_positive_rate: 0.01
})

# Add items
bloom.add("item1")
bloom.add("item2")
bloom.add("item3")

# Check membership
print "Contains item1:", bloom.contains("item1")
print "Contains item4:", bloom.contains("item4")
print ""

# Skip list
let skipList = skipList.create()

# Add items
skipList.insert(1, "one")
skipList.insert(2, "two")
skipList.insert(3, "three")

# Search
let result = skipList.search(2)
print "Found:", result
print ""

# Trie
let trie = trie.create()

# Add words
trie.insert("hello")
trie.insert("world")
trie.insert("help")

# Search
print "Contains hello:", trie.contains("hello")
print "Contains hell:", trie.contains("hell")
print "Starts with hel:", trie.startsWith("hel")
print ""

# Algorithms
print "=== Optimized Algorithms ==="

# Quick sort
let arr = [5, 3, 8, 4, 2, 7, 1, 6]
let sorted = algorithms.quickSort(arr)
print "Quick sort:", sorted

# Binary search
let index = algorithms.binarySearch(sorted, 4)
print "Binary search for 4:", index

# Dynamic programming
let fib = algorithms.dynamicProgramming(fibonacci, 30)
print "Dynamic programming fibonacci:", fib
print ""

# I/O optimization
print "=== I/O Optimization ==="

# Buffered I/O
let reader = io.bufferedReader("large_file.txt")
let line = reader.readline()
while line != null
  # Process line
  line = reader.readline()
end
reader.close()

# Memory mapped files
let mmap = io.memoryMapped("large_file.txt")
let data = mmap.read(0, 1024)
mmap.close()

print "I/O optimization complete"
print ""

# Network optimization
print "=== Network Optimization ==="

# Connection pooling
let pool = http.createConnectionPool({
  max_connections: 100,
  timeout: 30000
})

# Use connection pool
let connection = pool.get()
let response = connection.get("https://api.example.com")
pool.release(connection)

# HTTP/2
let client = http.createClient({
  http2: true,
  compression: true
})

let response = client.get("https://api.example.com")
print "HTTP/2 response:", response.status
print ""

print "=== Performance Optimization Example Complete ==="
