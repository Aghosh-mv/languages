# Security Example

# Input validation
print "=== Input Validation ==="

# Validate email
function validateEmail(email) then
  let pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
  return regex.match(email, pattern)
end

print "Valid email:", validateEmail("user@example.com")
print "Invalid email:", validateEmail("invalid-email")
print ""

# Validate password
function validatePassword(password) then
  let errors = []
  
  if len(password) < 8 then
    errors.push("Password must be at least 8 characters")
  end
  
  if not regex.match(password, "[A-Z]") then
    errors.push("Password must contain at least one uppercase letter")
  end
  
  if not regex.match(password, "[a-z]") then
    errors.push("Password must contain at least one lowercase letter")
  end
  
  if not regex.match(password, "[0-9]") then
    errors.push("Password must contain at least one digit")
  end
  
  if not regex.match(password, "[!@#$%^&*]") then
    errors.push("Password must contain at least one special character")
  end
  
  return {valid: len(errors) == 0, errors: errors}
end

let result = validatePassword("MyP@ssw0rd")
print "Password valid:", result.valid
print "Errors:", result.errors
print ""

# SQL injection prevention
print "=== SQL Injection Prevention ==="

# Parameterized queries
function getUserSafe(userId) then
  let query = "SELECT * FROM users WHERE id = ?"
  let params = [userId]
  return db.query(query, params)
end

# User input sanitization
function sanitizeInput(input) then
  # Remove potentially dangerous characters
  let sanitized = input.replace(/[<>\"';&]/g, "")
  return sanitized
end

let userInput = "'; DROP TABLE users; --"
let sanitized = sanitizeInput(userInput)
print "Original:", userInput
print "Sanitized:", sanitized
print ""

# XSS prevention
print "=== XSS Prevention ==="

# HTML encoding
function encodeHTML(str) then
  return str.replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;")
end

let userInput = "<script>alert('XSS')</script>"
let encoded = encodeHTML(userInput)
print "Original:", userInput
print "Encoded:", encoded
print ""

# CSRF protection
print "=== CSRF Protection ==="

# Generate CSRF token
function generateCSRFToken() then
  return crypto.randomString(32)
end

# Validate CSRF token
function validateCSRFToken(token, sessionToken) then
  return token == sessionToken
end

let token = generateCSRFToken()
print "CSRF token:", token
print "Token valid:", validateCSRFToken(token, token)
print ""

# Authentication
print "=== Authentication ==="

# Hash password
function hashPassword(password) then
  let salt = crypto.generateSalt()
  let hash = crypto.pbkdf2(password, salt, 100000, 64)
  return {salt: salt, hash: hash}
end

# Verify password
function verifyPassword(password, stored) then
  let hash = crypto.pbkdf2(password, stored.salt, 100000, 64)
  return hash == stored.hash
end

let stored = hashPassword("mypassword")
print "Password hashed"
print "Password verified:", verifyPassword("mypassword", stored)
print "Wrong password:", verifyPassword("wrongpassword", stored)
print ""

# JWT tokens
print "=== JWT Tokens ==="

# Generate JWT
function generateJWT(payload, secret) then
  let header = {alg: "HS256", typ: "JWT"}
  let headerEncoded = base64Encode(JSON.stringify(header))
  let payloadEncoded = base64Encode(JSON.stringify(payload))
  let signature = crypto.hmac_sha256(secret, headerEncoded + "." + payloadEncoded)
  return headerEncoded + "." + payloadEncoded + "." + signature
end

# Verify JWT
function verifyJWT(token, secret) then
  let parts = token.split(".")
  if len(parts) != 3 then
    return false
  end
  
  let header = JSON.parse(base64Decode(parts[0]))
  let payload = JSON.parse(base64Decode(parts[1]))
  let signature = crypto.hmac_sha256(secret, parts[0] + "." + parts[1])
  
  return parts[2] == signature
end

let jwt = generateJWT({user_id: 123, exp: Date.now() + 3600000}, "secret_key")
print "JWT generated:", jwt
print "JWT valid:", verifyJWT(jwt, "secret_key")
print ""

# Encryption
print "=== Encryption ==="

# Encrypt data
function encrypt(data, key) then
  let iv = crypto.randomBytes(16)
  let encrypted = crypto.aes_encrypt(data, key, iv)
  return {iv: iv, data: encrypted}
end

# Decrypt data
function decrypt(encrypted, key) then
  let decrypted = crypto.aes_decrypt(encrypted.data, key, encrypted.iv)
  return decrypted
end

let original = "Sensitive data"
let key = crypto.generateKey(256)
let encrypted = encrypt(original, key)
let decrypted = decrypt(encrypted, key)
print "Original:", original
print "Encrypted:", encrypted
print "Decrypted:", decrypted
print ""

# Secure communication
print "=== Secure Communication ==="

# HTTPS
let context = ssl.createContext()
context.loadCertificate("cert.pem")
context.loadKey("key.pem")

let secureSocket = ssl.wrap(socket, context)
secureSocket.send("Hello Secure!")
let response = secureSocket.receive()
secureSocket.close()

print "Secure communication established"
print ""

# Rate limiting
print "=== Rate Limiting ==="

# Create rate limiter
let rateLimiter = rateLimit.create({
  window: 60000,  # 1 minute
  max_requests: 100
})

# Check rate limit
function checkRateLimit(ip) then
  if rateLimiter.isAllowed(ip) then
    return true
  else
    print "Rate limit exceeded for IP:", ip
    return false
  end
end

# Test rate limiting
for i in range(10)
  print "Request", i + 1, "allowed:", checkRateLimit("192.168.1.1")
end
print ""

# Input sanitization
print "=== Input Sanitization ==="

# Sanitize for SQL
function sanitizeForSQL(input) then
  return input.replace(/'/g, "''")
end

# Sanitize for HTML
function sanitizeForHTML(input) then
  return encodeHTML(input)
end

# Sanitize for JavaScript
function sanitizeForJS(input) then
  return input.replace(/\\/g, "\\\\")
              .replace(/'/g, "\\'")
              .replace(/"/g, '\\"')
              .replace(/\n/g, "\\n")
              .replace(/\r/g, "\\r")
end

let userInput = "O'Brien's \"data\""
print "Original:", userInput
print "SQL safe:", sanitizeForSQL(userInput)
print "HTML safe:", sanitizeForHTML(userInput)
print "JS safe:", sanitizeForJS(userInput)
print ""

# Security headers
print "=== Security Headers ==="

# Set security headers
function setSecurityHeaders(response) then
  response.setHeader("X-Content-Type-Options", "nosniff")
  response.setHeader("X-Frame-Options", "DENY")
  response.setHeader("X-XSS-Protection", "1; mode=block")
  response.setHeader("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
  response.setHeader("Content-Security-Policy", "default-src 'self'")
  response.setHeader("Referrer-Policy", "strict-origin-when-cross-origin")
  response.setHeader("Permissions-Policy", "geolocation=(), microphone=()")
end

print "Security headers configured"
print ""

print "=== Security Example Complete ==="
