# Networking Example

# HTTP requests
print "=== HTTP Requests ==="
let response = http.get("https://api.example.com/data")
print "Status:", response.status
print "Body:", response.body
print ""

# POST request
print "=== POST Request ==="
let data = {name: "Alice", age: 30}
let response = http.post("https://api.example.com/users", data)
print "Status:", response.status
print "Body:", response.body
print ""

# WebSocket
print "=== WebSocket ==="
let ws = websocket.connect("wss://echo.websocket.org")
ws.send("Hello WebSocket!")
let message = ws.receive()
print "Received:", message
ws.close()
print ""

# TCP socket
print "=== TCP Socket ==="
let socket = tcp.connect("example.com", 80)
socket.send("GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
let response = socket.receive()
print "Response:", response
socket.close()
print ""

# UDP socket
print "=== UDP Socket ==="
let socket = udp.create()
socket.send("Hello UDP", "example.com", 12345)
let message = socket.receive()
print "Received:", message
socket.close()
print ""

# DNS lookup
print "=== DNS Lookup ==="
let ip = dns.lookup("example.com")
print "IP address:", ip
print ""

# URL parsing
print "=== URL Parsing ==="
let url = "https://example.com:8080/path?query=value#fragment"
let parsed = url.parse()
print "Protocol:", parsed.protocol
print "Host:", parsed.host
print "Port:", parsed.port
print "Path:", parsed.path
print "Query:", parsed.query
print "Fragment:", parsed.fragment
print ""

# SSL/TLS
print "=== SSL/TLS ==="
let context = ssl.createContext()
context.loadCertificate("cert.pem")
context.loadKey("key.pem")
let secure_socket = ssl.wrap(socket, context)
secure_socket.send("Hello Secure!")
let response = secure_socket.receive()
print "Secure response:", response
secure_socket.close()
print ""

# HTTP Server
print "=== HTTP Server ==="
let server = http.createServer()
server.on("request", (req, res) => {
  print "Request:", req.method, req.url
  res.send("Hello World!")
})
server.listen(8080)
print "Server listening on port 8080"
print ""

# WebSocket Server
print "=== WebSocket Server ==="
let wss = websocket.createServer()
wss.on("connection", (ws) => {
  ws.send("Welcome!")
  ws.on("message", (message) => {
    print "Received:", message
    ws.send("Echo: " + message)
  })
})
wss.listen(8081)
print "WebSocket server listening on port 8081"
print ""

print "=== Networking Complete ==="
