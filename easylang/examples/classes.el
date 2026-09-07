# Classes Example

# Define a class
class Animal then
  let name = ""
  let sound = ""
  
  function init(name, sound) then
    this.name = name
    this.sound = sound
  end
  
  function speak() then
    print this.name + " says " + this.sound + "!"
  end
  
  function toString() then
    return "Animal(" + this.name + ")"
  end
end

# Create instances
let dog = new Animal("Dog", "Woof")
let cat = new Animal("Cat", "Meow")
let cow = new Animal("Cow", "Moo")

# Use the objects
dog.speak()  # Dog says Woof!
cat.speak()  # Cat says Meow!
cow.speak()  # Cow says Moo!

print ""

# Inheritance
class Dog extends Animal then
  let breed = ""
  
  function init(name, breed) then
    super.init(name, "Woof")
    this.breed = breed
  end
  
  function fetch() then
    print this.name + " fetches the ball!"
  end
end

let myDog = new Dog("Buddy", "Golden Retriever")
myDog.speak()  # Buddy says Woof!
myDog.fetch()  # Buddy fetches the ball!
print "Breed:", myDog.breed
print ""

# Encapsulation
class BankAccount then
  let balance = 0
  
  function init(initial_balance) then
    this.balance = initial_balance
  end
  
  function deposit(amount) then
    if amount > 0 then
      this.balance = this.balance + amount
      print "Deposited:", amount
    end
  end
  
  function withdraw(amount) then
    if amount > 0 and amount <= this.balance then
      this.balance = this.balance - amount
      print "Withdrew:", amount
    else
      print "Insufficient funds"
    end
  end
  
  function getBalance() then
    return this.balance
  end
end

let account = new BankAccount(1000)
print "Initial balance:", account.getBalance()

account.deposit(500)
print "After deposit:", account.getBalance()

account.withdraw(200)
print "After withdrawal:", account.getBalance()

account.withdraw(2000)  # Should print "Insufficient funds"
print "Final balance:", account.getBalance()
