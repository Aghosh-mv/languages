# File I/O Example

# Write to file
print "=== Writing to file ==="
let file = open("test.txt", "w")
file.write("Hello, World!\n")
file.write("This is a test file.\n")
file.write("Line 3: EasyLang is awesome!\n")
file.close()
print "File written successfully"
print ""

# Read from file
print "=== Reading from file ==="
let file = open("test.txt", "r")
let content = file.read()
print "Content:"
print content
file.close()
print ""

# Read line by line
print "=== Reading line by line ==="
let file = open("test.txt", "r")
let line = file.readline()
while line != null
  print "Line:", line
  line = file.readline()
end
file.close()
print ""

# Read all lines
print "=== Reading all lines ==="
let file = open("test.txt", "r")
let lines = file.readlines()
print "Lines:", lines
file.close()
print ""

# Append to file
print "=== Appending to file ==="
let file = open("test.txt", "a")
file.write("Line 4: Appended line\n")
file.write("Line 5: Another appended line\n")
file.close()
print "File appended successfully"
print ""

# Read updated file
print "=== Reading updated file ==="
let file = open("test.txt", "r")
let content = file.read()
print "Updated content:"
print content
file.close()
print ""

# File operations
print "=== File operations ==="
print "File exists:", exists("test.txt")
print "File size:", size("test.txt")
print "Is file:", isFile("test.txt")
print "Is directory:", isDirectory("test.txt")
print ""

# Delete file
print "=== Deleting file ==="
delete("test.txt")
print "File deleted:", not exists("test.txt")
print ""

# Directory operations
print "=== Directory operations ==="
createDirectory("test_dir")
print "Directory created:", exists("test_dir")
print "Is directory:", isDirectory("test_dir")
deleteDirectory("test_dir")
print "Directory deleted:", not exists("test_dir")
print ""

# List directory
print "=== Listing directory ==="
let files = listDirectory(".")
print "Files in current directory:", files
print ""

# Copy and move files
print "=== Copy and move ==="
let file = open("source.txt", "w")
file.write("This is the source file\n")
file.close()

copy("source.txt", "destination.txt")
print "File copied:", exists("destination.txt")

move("destination.txt", "moved.txt")
print "File moved:", exists("moved.txt") and not exists("destination.txt")

delete("source.txt")
delete("moved.txt")
print "Cleanup complete"
print ""

print "=== File I/O Complete ==="
