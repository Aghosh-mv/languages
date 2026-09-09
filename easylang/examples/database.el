# Database Example

# Connect to database
print "=== Database Connection ==="
let db = database.connect("sqlite", "mydb.db")
print "Connected to database"
print ""

# Create table
print "=== Create Table ==="
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, age INTEGER)")
print "Table created"
print ""

# Insert data
print "=== Insert Data ==="
db.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ["Alice", "alice@example.com", 30])
db.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ["Bob", "bob@example.com", 25])
db.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ["Charlie", "charlie@example.com", 35])
print "Data inserted"
print ""

# Query data
print "=== Query Data ==="
let users = db.query("SELECT * FROM users")
for user in users
  print "ID:", user.id, "Name:", user.name, "Email:", user.email, "Age:", user.age
end
print ""

# Query with condition
print "=== Query with Condition ==="
let adults = db.query("SELECT * FROM users WHERE age >= ?", [18])
print "Adults:"
for user in adults
  print " ", user.name, "- Age:", user.age
end
print ""

# Update data
print "=== Update Data ==="
db.execute("UPDATE users SET age = ? WHERE name = ?", [31, "Alice"])
print "Data updated"
print ""

# Verify update
print "=== Verify Update ==="
let alice = db.query("SELECT * FROM users WHERE name = ?", ["Alice"])
print "Alice's new age:", alice[0].age
print ""

# Delete data
print "=== Delete Data ==="
db.execute("DELETE FROM users WHERE name = ?", ["Charlie"])
print "Data deleted"
print ""

# Verify deletion
print "=== Verify Deletion ==="
let users = db.query("SELECT * FROM users")
print "Remaining users:"
for user in users
  print " ", user.name
end
print ""

# Transactions
print "=== Transactions ==="
db.beginTransaction()
try
  db.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ["David", "david@example.com", 28])
  db.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ["Eve", "eve@example.com", 22])
  db.commit()
  print "Transaction committed"
catch error
  db.rollback()
  print "Transaction rolled back:", error
end
print ""

# Stored procedures
print "=== Stored Procedures ==="
db.execute("CREATE PROCEDURE get_users_by_age(IN min_age INTEGER) BEGIN SELECT * FROM users WHERE age >= min_age; END")
let users = db.call("get_users_by_age", [25])
print "Users over 25:"
for user in users
  print " ", user.name, "- Age:", user.age
end
print ""

# Close connection
print "=== Close Connection ==="
db.close()
print "Database connection closed"
print ""

print "=== Database Example Complete ==="
