# Multithreading Example

# Create threads
print "=== Creating Threads ==="

# Thread function
function worker(id, iterations) then
  for i in range(iterations)
    print "Thread", id, "- Iteration", i
    delay(100)
  end
  print "Thread", id, "- Complete"
end

# Create multiple threads
let thread1 = threading.create(worker, [1, 5])
let thread2 = threading.create(worker, [2, 5])
let thread3 = threading.create(worker, [3, 5])

# Wait for threads to complete
thread1.join()
thread2.join()
thread3.join()

print "All threads complete"
print ""

# Thread synchronization
print "=== Thread Synchronization ==="

# Shared resource
let counter = 0
let lock = threading.Lock()

# Thread function with synchronization
function synchronized_worker(id, iterations) then
  for i in range(iterations)
    lock.acquire()
    counter = counter + 1
    print "Thread", id, "- Counter:", counter
    lock.release()
    delay(100)
  end
end

# Create threads
let threads = []
for i in range(5)
  let thread = threading.create(synchronized_worker, [i, 3])
  threads.push(thread)
end

# Wait for all threads
for thread in threads
  thread.join()
end

print "Final counter:", counter
print ""

# Thread pool
print "=== Thread Pool ==="

# Create thread pool
let pool = threading.ThreadPool(4)

# Submit tasks
let futures = []
for i in range(10)
  let future = pool.submit(worker, [i, 2])
  futures.push(future)
end

# Wait for all futures
for future in futures
  future.get()
end

# Shutdown pool
pool.shutdown()
print "Thread pool complete"
print ""

# Producer-consumer pattern
print "=== Producer-Consumer Pattern ==="

# Shared queue
let queue = []
let queue_lock = threading.Lock()
let queue_condition = threading.Condition(queue_lock)

# Producer function
function producer(items) then
  for item in items
    queue_lock.acquire()
    queue.push(item)
    print "Produced:", item
    queue_condition.notify()
    queue_lock.release()
    delay(50)
  end
end

# Consumer function
function consumer(count) then
  for i in range(count)
    queue_lock.acquire()
    while len(queue) == 0
      queue_condition.wait()
    end
    let item = queue.shift()
    print "Consumed:", item
    queue_lock.release()
    delay(100)
  end
end

# Create producer and consumer threads
let producer_thread = threading.create(producer, [["A", "B", "C", "D", "E"]])
let consumer_thread = threading.create(consumer, [5])

# Wait for completion
producer_thread.join()
consumer_thread.join()
print "Producer-consumer complete"
print ""

# Thread-local storage
print "=== Thread-Local Storage ==="

# Thread-local variable
let local_data = threading.local()

# Thread function using local storage
function local_worker(id) then
  local_data.value = id * 10
  print "Thread", id, "- Local value:", local_data.value
  delay(100)
  print "Thread", id, "- Local value again:", local_data.value
end

# Create threads
let threads = []
for i in range(3)
  let thread = threading.create(local_worker, [i])
  threads.push(thread)
end

# Wait for completion
for thread in threads
  thread.join()
end
print "Thread-local storage complete"
print ""

# Async/await with threads
print "=== Async/Await ==="

# Async function
async function async_task(id) then
  print "Starting async task", id
  await threading.sleep(100)
  print "Async task", id, "complete"
  return id * 2
end

# Run multiple async tasks
let tasks = []
for i in range(5)
  let task = async_task(i)
  tasks.push(task)
end

# Wait for all tasks
let results = await Promise.all(tasks)
print "Async results:", results
print ""

# Thread communication with queues
print "=== Thread Communication ==="

# Create communication queue
let comm_queue = threading.Queue()

# Sender function
function sender(count) then
  for i in range(count)
    comm_queue.put("Message " + str(i))
    print "Sent: Message", i
    delay(50)
  end
  comm_queue.put("DONE")
end

# Receiver function
function receiver() then
  while true
    let message = comm_queue.get()
    if message == "DONE" then
      break
    end
    print "Received:", message
    delay(100)
  end
end

# Create threads
let sender_thread = threading.create(sender, [5])
let receiver_thread = threading.create(receiver)

# Wait for completion
sender_thread.join()
receiver_thread.join()
print "Thread communication complete"
print ""

print "=== Multithreading Example Complete ==="
