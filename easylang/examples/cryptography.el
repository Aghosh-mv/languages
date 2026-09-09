# Cryptography Example

# Hash functions
print "=== Hash Functions ==="
let message = "Hello, World!"

# MD5
let md5_hash = crypto.md5(message)
print "MD5:", md5_hash

# SHA-1
let sha1_hash = crypto.sha1(message)
print "SHA-1:", sha1_hash

# SHA-256
let sha256_hash = crypto.sha256(message)
print "SHA-256:", sha256_hash

# SHA-512
let sha512_hash = crypto.sha512(message)
print "SHA-512:", sha512_hash
print ""

# HMAC
print "=== HMAC ==="
let key = "secret_key"
let message = "Hello, World!"

# HMAC-MD5
let hmac_md5 = crypto.hmac_md5(key, message)
print "HMAC-MD5:", hmac_md5

# HMAC-SHA256
let hmac_sha256 = crypto.hmac_sha256(key, message)
print "HMAC-SHA256:", hmac_sha256

# HMAC-SHA512
let hmac_sha512 = crypto.hmac_sha512(key, message)
print "HMAC-SHA512:", hmac_sha512
print ""

# Symmetric encryption
print "=== Symmetric Encryption ==="
let message = "Hello, World!"
let key = crypto.generateKey(256)

# AES encryption
let aes_encrypted = crypto.aes_encrypt(message, key)
let aes_decrypted = crypto.aes_decrypt(aes_encrypted, key)
print "AES Encrypted:", aes_encrypted
print "AES Decrypted:", aes_decrypted

# DES encryption (not recommended for production)
let des_encrypted = crypto.des_encrypt(message, key)
let des_decrypted = crypto.des_decrypt(des_encrypted, key)
print "DES Encrypted:", des_encrypted
print "DES Decrypted:", des_decrypted

# 3DES encryption
let triple_des_encrypted = crypto.triple_des_encrypt(message, key)
let triple_des_decrypted = crypto.triple_des_decrypt(triple_des_encrypted, key)
print "3DES Encrypted:", triple_des_encrypted
print "3DES Decrypted:", triple_des_decrypted
print ""

# Asymmetric encryption
print "=== Asymmetric Encryption ==="

# Generate RSA key pair
let key_pair = crypto.generate_rsa_keypair(2048)
let public_key = key_pair.public
let private_key = key_pair.private

# RSA encryption
let message = "Hello, World!"
let rsa_encrypted = crypto.rsa_encrypt(message, public_key)
let rsa_decrypted = crypto.rsa_decrypt(rsa_encrypted, private_key)
print "RSA Encrypted:", rsa_encrypted
print "RSA Decrypted:", rsa_decrypted

# RSA signing
let signature = crypto.rsa_sign(message, private_key)
let verified = crypto.rsa_verify(message, signature, public_key)
print "RSA Signature:", signature
print "RSA Verified:", verified
print ""

# Digital signatures
print "=== Digital Signatures ==="

# Generate ECDSA key pair
let key_pair = crypto.generate_ecdsa_keypair()
let public_key = key_pair.public
let private_key = key_pair.private

# Sign message
let message = "Hello, World!"
let signature = crypto.ecdsa_sign(message, private_key)

# Verify signature
let verified = crypto.ecdsa_verify(message, signature, public_key)
print "ECDSA Signature:", signature
print "ECDSA Verified:", verified
print ""

# Key exchange
print "=== Key Exchange ==="

# Diffie-Hellman key exchange
let alice_private, alice_public = crypto.diffie_hellman_generate()
let bob_private, bob_public = crypto.diffie_hellman_generate()

# Compute shared secret
let alice_secret = crypto.diffie_hellman_compute(alice_private, bob_public)
let bob_secret = crypto.diffie_hellman_compute(bob_private, alice_public)

print "Alice's secret:", alice_secret
print "Bob's secret:", bob_secret
print "Secrets match:", alice_secret == bob_secret
print ""

# Elliptic curve Diffie-Hellman
let alice_private, alice_public = crypto.ecdh_generate()
let bob_private, bob_public = crypto.ecdh_generate()

# Compute shared secret
let alice_secret = crypto.ecdh_compute(alice_private, bob_public)
let bob_secret = crypto.ecdh_compute(bob_private, alice_public)

print "Alice's secret:", alice_secret
print "Bob's secret:", bob_secret
print "Secrets match:", alice_secret == bob_secret
print ""

# Password hashing
print "=== Password Hashing ==="
let password = "my_secret_password"

# PBKDF2
let salt = crypto.generateSalt()
let hash = crypto.pbkdf2(password, salt, 100000, 64)
print "PBKDF2 Hash:", hash

# bcrypt
let bcrypt_hash = crypto.bcrypt(password)
print "bcrypt Hash:", bcrypt_hash

# Verify password
let verified = crypto.bcrypt_verify(password, bcrypt_hash)
print "Password Verified:", verified
print ""

# Random number generation
print "=== Random Number Generation ==="

# Generate random bytes
let random_bytes = crypto.randomBytes(32)
print "Random bytes:", random_bytes

# Generate random integer
let random_int = crypto.randomInt(0, 100)
print "Random integer:", random_int

# Generate random string
let random_string = crypto.randomString(16)
print "Random string:", random_string
print ""

# Encoding/Decoding
print "=== Encoding/Decoding ==="
let message = "Hello, World!"

# Base64
let base64_encoded = crypto.base64_encode(message)
let base64_decoded = crypto.base64_decode(base64_encoded)
print "Base64 Encoded:", base64_encoded
print "Base64 Decoded:", base64_decoded

# Hex
let hex_encoded = crypto.hex_encode(message)
let hex_decoded = crypto.hex_decode(hex_encoded)
print "Hex Encoded:", hex_encoded
print "Hex Decoded:", hex_decoded

# URL encoding
let url_encoded = crypto.url_encode("Hello World!")
let url_decoded = crypto.url_decode(url_encoded)
print "URL Encoded:", url_encoded
print "URL Decoded:", url_decoded
print ""

# X.509 certificates
print "=== X.509 Certificates ==="

# Generate self-signed certificate
let certificate = crypto.generate_self_signed_certificate(
  "CN=localhost",
  365
)
print "Certificate generated"

# Parse certificate
let parsed = crypto.parse_certificate(certificate)
print "Subject:", parsed.subject
print "Issuer:", parsed.issuer
print "Valid from:", parsed.valid_from
print "Valid to:", parsed.valid_to
print ""

# SSL/TLS
print "=== SSL/TLS ==="

# Create SSL context
let context = ssl.createContext()
context.loadCertificate("cert.pem")
context.loadKey("key.pem")

# Wrap socket
let secure_socket = ssl.wrap(socket, context)

# Send data
secure_socket.send("Hello Secure!")

# Receive data
let response = secure_socket.receive()
print "Secure response:", response

# Close connection
secure_socket.close()
print ""

print "=== Cryptography Example Complete ==="
