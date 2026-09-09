# Algorithms Example

# Sorting algorithms
print "=== Sorting Algorithms ==="

# Bubble sort
function bubbleSort(arr) then
  let n = len(arr)
  for i in range(n)
    for j in range(0, n-i-1)
      if arr[j] > arr[j+1] then
        let temp = arr[j]
        arr[j] = arr[j+1]
        arr[j+1] = temp
      end
    end
  end
  return arr
end

# Quick sort
function quickSort(arr) then
  if len(arr) <= 1 then
    return arr
  end
  
  let pivot = arr[0]
  let left = []
  let right = []
  
  for i in range(1, len(arr))
    if arr[i] < pivot then
      left.push(arr[i])
    else
      right.push(arr[i])
    end
  end
  
  return [...quickSort(left), pivot, ...quickSort(right)]
end

# Merge sort
function mergeSort(arr) then
  if len(arr) <= 1 then
    return arr
  end
  
  let mid = Math.floor(len(arr) / 2)
  let left = mergeSort(arr.slice(0, mid))
  let right = mergeSort(arr.slice(mid))
  
  return merge(left, right)
end

function merge(left, right) then
  let result = []
  let i = 0
  let j = 0
  
  while i < len(left) and j < len(right)
    if left[i] < right[j] then
      result.push(left[i])
      i++
    else
      result.push(right[j])
      j++
    end
  end
  
  return [...result, ...left.slice(i), ...right.slice(j)]
end

# Test sorting algorithms
let arr = [5, 3, 8, 4, 2, 7, 1, 6]
print "Bubble sort:", bubbleSort([...arr])
print "Quick sort:", quickSort([...arr])
print "Merge sort:", mergeSort([...arr])
print ""

# Search algorithms
print "=== Search Algorithms ==="

# Linear search
function linearSearch(arr, target) then
  for i in range(len(arr))
    if arr[i] == target then
      return i
    end
  end
  return -1
end

# Binary search
function binarySearch(arr, target) then
  let left = 0
  let right = len(arr) - 1
  
  while left <= right
    let mid = Math.floor((left + right) / 2)
    
    if arr[mid] == target then
      return mid
    else if arr[mid] < target then
      left = mid + 1
    else
      right = mid - 1
    end
  end
  
  return -1
end

# Test search algorithms
let arr = [1, 2, 3, 4, 5, 6, 7, 8]
print "Linear search for 5:", linearSearch(arr, 5)
print "Binary search for 5:", binarySearch(arr, 5)
print ""

# Graph algorithms
print "=== Graph Algorithms ==="

# BFS
function bfs(graph, start) then
  let visited = new Set()
  let queue = [start]
  let result = []
  
  while queue.length > 0
    let node = queue.shift()
    
    if !visited.has(node) then
      visited.add(node)
      result.push(node)
      
      for neighbor in graph[node]
        if !visited.has(neighbor) then
          queue.push(neighbor)
        end
      end
    end
  end
  
  return result
end

# DFS
function dfs(graph, start) then
  let visited = new Set()
  let result = []
  
  function dfsHelper(node) then
    if !visited.has(node) then
      visited.add(node)
      result.push(node)
      
      for neighbor in graph[node]
        dfsHelper(neighbor)
      end
    end
  end
  
  dfsHelper(start)
  return result
end

# Test graph algorithms
let graph = {
  A: ["B", "C"],
  B: ["A", "D", "E"],
  C: ["A", "F"],
  D: ["B"],
  E: ["B", "F"],
  F: ["C", "E"]
}

print "BFS from A:", bfs(graph, "A")
print "DFS from A:", dfs(graph, "A")
print ""

# Dynamic programming
print "=== Dynamic Programming ==="

# Fibonacci with memoization
function fibonacci(n, memo = {}) then
  if n <= 1 then
    return n
  end
  
  if memo[n] != null then
    return memo[n]
  end
  
  memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
  return memo[n]
end

# Knapsack problem
function knapsack(weights, values, capacity) then
  let n = len(weights)
  let dp = Array(n + 1).fill(null).map(() -> Array(capacity + 1).fill(0))
  
  for i in range(1, n + 1)
    for w in range(1, capacity + 1)
      if weights[i-1] <= w then
        dp[i][w] = Math.max(
          values[i-1] + dp[i-1][w-weights[i-1]],
          dp[i-1][w]
        )
      else
        dp[i][w] = dp[i-1][w]
      end
    end
  end
  
  return dp[n][capacity]
end

# Test dynamic programming
print "Fibonacci(10):", fibonacci(10)
print "Knapsack:", knapsack([2, 3, 4, 5], [3, 4, 5, 6], 8)
print ""

# Tree algorithms
print "=== Tree Algorithms ==="

class TreeNode then
  constructor(value) then
    this.value = value
    this.left = null
    this.right = null
  end
end

# In-order traversal
function inOrder(node) then
  if node == null then
    return []
  end
  
  return [...inOrder(node.left), node.value, ...inOrder(node.right)]
end

# Pre-order traversal
function preOrder(node) then
  if node == null then
    return []
  end
  
  return [node.value, ...preOrder(node.left), ...preOrder(node.right)]
end

# Post-order traversal
function postOrder(node) then
  if node == null then
    return []
  end
  
  return [...postOrder(node.left), ...postOrder(node.right), node.value]
end

# Test tree algorithms
let root = new TreeNode(1)
root.left = new TreeNode(2)
root.right = new TreeNode(3)
root.left.left = new TreeNode(4)
root.left.right = new TreeNode(5)

print "In-order:", inOrder(root)
print "Pre-order:", preOrder(root)
print "Post-order:", postOrder(root)
print ""

# String algorithms
print "=== String Algorithms ==="

# KMP algorithm
function kmpSearch(text, pattern) then
  let n = len(text)
  let m = len(pattern)
  let lps = Array(m).fill(0)
  
  # Build LPS array
  let len = 0
  let i = 1
  while i < m
    if pattern[i] == pattern[len] then
      len++
      lps[i] = len
      i++
    else
      if len != 0 then
        len = lps[len-1]
      else
        lps[i] = 0
        i++
      end
    end
  end
  
  # Search pattern
  let result = []
  i = 0
  let j = 0
  while i < n
    if pattern[j] == text[i] then
      i++
      j++
    end
    
    if j == m then
      result.push(i-j)
      j = lps[j-1]
    else if i < n and pattern[j] != text[i] then
      if j != 0 then
        j = lps[j-1]
      else
        i++
      end
    end
  end
  
  return result
end

# Test string algorithms
print "KMP search:", kmpSearch("ABABDABACDABABCABAB", "ABABCABAB")
print ""

# Mathematical algorithms
print "=== Mathematical Algorithms ==="

# GCD
function gcd(a, b) then
  while b != 0
    let temp = b
    b = a % b
    a = temp
  end
  return a
end

# LCM
function lcm(a, b) then
  return (a * b) / gcd(a, b)
end

# Prime check
function isPrime(n) then
  if n <= 1 then
    return false
  end
  
  for i in range(2, Math.sqrt(n) + 1)
    if n % i == 0 then
      return false
    end
  end
  
  return true
end

# Test mathematical algorithms
print "GCD of 12 and 18:", gcd(12, 18)
print "LCM of 12 and 18:", lcm(12, 18)
print "Is 17 prime:", isPrime(17)
print ""

# Cryptographic algorithms
print "=== Cryptographic Algorithms ==="

# Hash function
function hash(str) then
  let hash = 0
  for i in range(len(str))
    let char = str.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash  # Convert to 32bit integer
  end
  return hash
end

# Test cryptographic algorithms
print "Hash of 'hello':", hash("hello")
print ""

print "=== Algorithms Example Complete ==="
