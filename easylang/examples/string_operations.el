# String Operations Example

# Create strings
let greeting = "Hello, World!"
let name = "Alice"
let sentence = "The quick brown fox jumps over the lazy dog"

# Basic operations
print "Greeting:", greeting
print "Name:", name
print ""

# Length
print "Length of greeting:", len(greeting)
print ""

# Case conversion
print "Uppercase:", greeting.upper()
print "Lowercase:", greeting.lower()
print "Title case:", sentence.title()
print ""

# Trim
let padded = "  Hello  "
print "Original:", padded
print "Trimmed:", padded.trim()
print "Left trimmed:", padded.trimLeft()
print "Right trimmed:", padded.trimRight()
print ""

# Split and join
let words = sentence.split(" ")
print "Words:", words
print "Joined:", words.join("-")
print ""

# Replace
let replaced = greeting.replace("World", "EasyLang")
print "Replaced:", replaced
print ""

# Search
let index = sentence.indexOf("fox")
print "Index of 'fox':", index
print "Contains 'fox':", sentence.includes("fox")
print "Starts with 'The':", sentence.startsWith("The")
print "Ends with 'dog':", sentence.endsWith("dog")
print ""

# Substring
let sub = sentence.substring(4, 19)
print "Substring:", sub
print ""

# Repeat
let repeated = "Ha".repeat(3)
print "Repeated:", repeated
print ""

# Padding
let padded_num = "42".padStart(5, "0")
print "Padded:", padded_num
print ""

# ASCII values
print "ASCII of 'A':", "A".charCodeAt(0)
print "Char from 65:", String.fromCharCode(65)
print ""

# Template literals
let age = 30
let intro = `My name is ${name} and I am ${age} years old.`
print "Template:", intro
