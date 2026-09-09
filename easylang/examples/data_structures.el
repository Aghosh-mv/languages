# Data Structures Example

# Arrays
print "=== Arrays ==="

# Create array
let arr = [1, 2, 3, 4, 5]

# Array operations
print "Array:", arr
print "Length:", len(arr)
print "First:", arr[0]
print "Last:", arr[len(arr) - 1]

# Array methods
arr.push(6)
print "After push:", arr

arr.pop()
print "After pop:", arr

arr.unshift(0)
print "After unshift:", arr

arr.shift()
print "After shift:", arr

arr.reverse()
print "After reverse:", arr

arr.sort()
print "After sort:", arr

print ""

# Linked List
print "=== Linked List ==="

class ListNode then
  constructor(value) then
    this.value = value
    this.next = null
  end
end

class LinkedList then
  constructor() then
    this.head = null
    this.size = 0
  end
  
  add(value) then
    let node = new ListNode(value)
    
    if this.head == null then
      this.head = node
    else
      let current = this.head
      while current.next != null
        current = current.next
      end
      current.next = node
    end
    
    this.size++
  end
  
  remove(value) then
    if this.head == null then
      return false
    end
    
    if this.head.value == value then
      this.head = this.head.next
      this.size--
      return true
    end
    
    let current = this.head
    while current.next != null
      if current.next.value == value then
        current.next = current.next.next
        this.size--
        return true
      end
      current = current.next
    end
    
    return false
  end
  
  find(value) then
    let current = this.head
    while current != null
      if current.value == value then
        return true
      end
      current = current.next
    end
    return false
  end
  
  toArray() then
    let result = []
    let current = this.head
    while current != null
      result.push(current.value)
      current = current.next
    end
    return result
  end
end

# Use linked list
let list = new LinkedList()
list.add(1)
list.add(2)
list.add(3)
print "List:", list.toArray()
print "Size:", list.size

list.remove(2)
print "After remove:", list.toArray()

print "Contains 3:", list.find(3)
print ""

# Stack
print "=== Stack ==="

class Stack then
  constructor() then
    this.items = []
  end
  
  push(item) then
    this.items.push(item)
  end
  
  pop() then
    return this.items.pop()
  end
  
  peek() then
    return this.items[this.items.length - 1]
  end
  
  isEmpty() then
    return this.items.length === 0
  end
  
  size() then
    return this.items.length
  end
end

# Use stack
let stack = new Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print "Stack size:", stack.size()
print "Top:", stack.peek()
print "Pop:", stack.pop()
print "Stack size:", stack.size()
print ""

# Queue
print "=== Queue ==="

class Queue then
  constructor() then
    this.items = []
  end
  
  enqueue(item) then
    this.items.push(item)
  end
  
  dequeue() then
    return this.items.shift()
  end
  
  front() then
    return this.items[0]
  end
  
  isEmpty() then
    return this.items.length === 0
  end
  
  size() then
    return this.items.length
  end
end

# Use queue
let queue = new Queue()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
print "Queue size:", queue.size()
print "Front:", queue.front()
print "Dequeue:", queue.dequeue()
print "Queue size:", queue.size()
print ""

# Hash Table
print "=== Hash Table ==="

class HashTable then
  constructor() then
    this.table = {}
  end
  
  set(key, value) then
    this.table[key] = value
  end
  
  get(key) then
    return this.table[key]
  end
  
  has(key) then
    return key in this.table
  end
  
  delete(key) then
    delete this.table[key]
  end
  
  keys() then
    return Object.keys(this.table)
  end
  
  values() then
    return Object.values(this.table)
  end
end

# Use hash table
let hashTable = new HashTable()
hashTable.set("name", "Alice")
hashTable.set("age", 30)
hashTable.set("city", "New York")

print "Name:", hashTable.get("name")
print "Has age:", hashTable.has("age")
print "Keys:", hashTable.keys()
print ""

# Binary Tree
print "=== Binary Tree ==="

class TreeNode then
  constructor(value) then
    this.value = value
    this.left = null
    this.right = null
  end
end

class BinarySearchTree then
  constructor() then
    this.root = null
  end
  
  insert(value) then
    let node = new TreeNode(value)
    
    if this.root == null then
      this.root = node
    else
      this.insertNode(this.root, node)
    end
  end
  
  insertNode(node, newNode) then
    if newNode.value < node.value then
      if node.left == null then
        node.left = newNode
      else
        this.insertNode(node.left, newNode)
      end
    else
      if node.right == null then
        node.right = newNode
      else
        this.insertNode(node.right, newNode)
      end
    end
  end
  
  search(value) then
    return this.searchNode(this.root, value)
  end
  
  searchNode(node, value) then
    if node == null then
      return false
    end
    
    if value < node.value then
      return this.searchNode(node.left, value)
    else if value > node.value then
      return this.searchNode(node.right, value)
    else
      return true
    end
  end
  
  inorder() then
    let result = []
    this.inorderNode(this.root, result)
    return result
  end
  
  inorderNode(node, result) then
    if node != null then
      this.inorderNode(node.left, result)
      result.push(node.value)
      this.inorderNode(node.right, result)
    end
  end
end

# Use binary search tree
let bst = new BinarySearchTree()
bst.insert(5)
bst.insert(3)
bst.insert(7)
bst.insert(1)
bst.insert(4)

print "Inorder traversal:", bst.inorder()
print "Search 3:", bst.search(3)
print "Search 6:", bst.search(6)
print ""

# Heap
print "=== Heap ==="

class MinHeap then
  constructor() then
    this.heap = []
  end
  
  insert(value) then
    this.heap.push(value)
    this.bubbleUp(this.heap.length - 1)
  end
  
  bubbleUp(index) then
    while index > 0
      let parent = Math.floor((index - 1) / 2)
      
      if this.heap[parent] <= this.heap[index] then
        break
      end
      
      [this.heap[parent], this.heap[index]] = [this.heap[index], this.heap[parent]]
      index = parent
    end
  end
  
  extractMin() then
    if this.heap.length == 0 then
      return null
    end
    
    let min = this.heap[0]
    let end = this.heap.pop()
    
    if this.heap.length > 0 then
      this.heap[0] = end
      this.sinkDown(0)
    end
    
    return min
  end
  
  sinkDown(index) then
    let length = this.heap.length
    
    while true
      let left = 2 * index + 1
      let right = 2 * index + 2
      let smallest = index
      
      if left < length and this.heap[left] < this.heap[smallest] then
        smallest = left
      end
      
      if right < length and this.heap[right] < this.heap[smallest] then
        smallest = right
      end
      
      if smallest == index then
        break
      end
      
      [this.heap[index], this.heap[smallest]] = [this.heap[smallest], this.heap[index]]
      index = smallest
    end
  end
  
  peek() then
    return this.heap[0]
  end
  
  size() then
    return this.heap.length
  end
end

# Use min heap
let heap = new MinHeap()
heap.insert(5)
heap.insert(3)
heap.insert(7)
heap.insert(1)
heap.insert(4)

print "Min heap:", heap.heap
print "Extract min:", heap.extractMin()
print "Min heap after extract:", heap.heap
print ""

# Graph
print "=== Graph ==="

class Graph then
  constructor() then
    this.adjacencyList = {}
  end
  
  addVertex(vertex) then
    if !this.adjacencyList[vertex] then
      this.adjacencyList[vertex] = []
    end
  end
  
  addEdge(vertex1, vertex2) then
    this.adjacencyList[vertex1].push(vertex2)
    this.adjacencyList[vertex2].push(vertex1)
  end
  
  removeEdge(vertex1, vertex2) then
    this.adjacencyList[vertex1] = this.adjacencyList[vertex1].filter(v => v !== vertex2)
    this.adjacencyList[vertex2] = this.adjacencyList[vertex2].filter(v => v !== vertex1)
  end
  
  dfs(start) then
    let result = []
    let visited = new Set()
    
    let dfsHelper = (vertex) -> {
      if (!vertex) return null
      visited.add(vertex)
      result.push(vertex)
      
      this.adjacencyList[vertex].forEach(neighbor => {
        if (!visited.has(neighbor)) {
          dfsHelper(neighbor)
        }
      })
    }
    
    dfsHelper(start)
    return result
  end
  
  bfs(start) then
    let queue = [start]
    let result = []
    let visited = new Set()
    visited.add(start)
    
    while queue.length
      let vertex = queue.shift()
      result.push(vertex)
      
      this.adjacencyList[vertex].forEach(neighbor => {
        if (!visited.has(neighbor)) {
          visited.add(neighbor)
          queue.push(neighbor)
        }
      })
    end
    
    return result
  end
end

# Use graph
let graph = new Graph()
graph.addVertex("A")
graph.addVertex("B")
graph.addVertex("C")
graph.addVertex("D")
graph.addVertex("E")

graph.addEdge("A", "B")
graph.addEdge("A", "C")
graph.addEdge("B", "D")
graph.addEdge("C", "E")

print "DFS from A:", graph.dfs("A")
print "BFS from A:", graph.bfs("A")
print ""

# Trie
print "=== Trie ==="

class TrieNode then
  constructor() then
    this.children = {}
    this.isEnd = false
  end
end

class Trie then
  constructor() then
    this.root = new TrieNode()
  end
  
  insert(word) then
    let node = this.root
    
    for char of word
      if !node.children[char] then
        node.children[char] = new TrieNode()
      end
      node = node.children[char]
    end
    
    node.isEnd = true
  end
  
  search(word) then
    let node = this.root
    
    for char of word
      if !node.children[char] then
        return false
      end
      node = node.children[char]
    end
    
    return node.isEnd
  end
  
  startsWith(prefix) then
    let node = this.root
    
    for char of prefix
      if !node.children[char] then
        return false
      end
      node = node.children[char]
    end
    
    return true
  end
end

# Use trie
let trie = new Trie()
trie.insert("apple")
trie.insert("app")
trie.insert("application")

print "Search 'apple':", trie.search("apple")
print "Search 'app':", trie.search("app")
print "Search 'ap':", trie.search("ap")
print "Starts with 'app':", trie.startsWith("app")
print ""

print "=== Data Structures Example Complete ==="
