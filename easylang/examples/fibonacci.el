# Fibonacci in EasyLang - natural and easy!

let n = 10
let a = 0
let b = 1
let i = 0

while i < n do
  print a
  let temp = a + b
  set a to b
  set b to temp
  set i to i + 1
end
