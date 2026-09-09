# Design Patterns Example

# Singleton pattern
print "=== Singleton Pattern ==="

class Database then
  static instance = null
  
  static getInstance() then
    if Database.instance == null then
      Database.instance = new Database()
    end
    return Database.instance
  end
  
  constructor() then
    if Database.instance != null then
      throw "Database is a singleton"
    end
    this.connection = this.connect()
  end
  
  connect() then
    print "Connecting to database..."
    return "connected"
  end
  
  query(sql) then
    print "Executing query:", sql
    return []
  end
end

# Use singleton
let db1 = Database.getInstance()
let db2 = Database.getInstance()
print "Same instance:", db1 === db2
print ""

# Factory pattern
print "=== Factory Pattern ==="

class Animal then
  speak() then
    throw "Must implement speak method"
  end
end

class Dog extends Animal then
  speak() then
    return "Woof!"
  end
end

class Cat extends Animal then
  speak() then
    return "Meow!"
  end
end

class AnimalFactory then
  static create(type) then
    switch(type)
      when "dog":
        return new Dog()
      when "cat":
        return new Cat()
      default:
        throw "Unknown animal type"
    end
  end
end

# Use factory
let dog = AnimalFactory.create("dog")
let cat = AnimalFactory.create("cat")
print "Dog says:", dog.speak()
print "Cat says:", cat.speak()
print ""

# Builder pattern
print "=== Builder Pattern ==="

class Computer then
  constructor() then
    this.cpu = null
    this.ram = null
    this.storage = null
    this.gpu = null
  end
end

class ComputerBuilder then
  constructor() then
    this.computer = new Computer()
  end
  
  setCPU(cpu) then
    this.computer.cpu = cpu
    return this
  end
  
  setRAM(ram) then
    this.computer.ram = ram
    return this
  end
  
  setStorage(storage) then
    this.computer.storage = storage
    return this
  end
  
  setGPU(gpu) then
    this.computer.gpu = gpu
    return this
  end
  
  build() then
    return this.computer
  end
end

# Use builder
let computer = new ComputerBuilder()
  .setCPU("Intel i7")
  .setRAM("16GB")
  .setStorage("512GB SSD")
  .setGPU("NVIDIA RTX 3080")
  .build()

print "Computer built with:", computer.cpu, computer.ram, computer.storage, computer.gpu
print ""

# Observer pattern
print "=== Observer Pattern ==="

class EventEmitter then
  constructor() then
    this.listeners = {}
  end
  
  on(event, callback) then
    if this.listeners[event] == null then
      this.listeners[event] = []
    end
    this.listeners[event].push(callback)
  end
  
  emit(event, data) then
    if this.listeners[event] != null then
      for callback in this.listeners[event]
        callback(data)
      end
    end
  end
end

class Button then
  constructor(text) then
    this.text = text
    this.emitter = new EventEmitter()
  end
  
  onClick(callback) then
    this.emitter.on("click", callback)
  end
  
  click() then
    this.emitter.emit("click", {button: this})
  end
end

# Use observer
let button = new Button("Click me")
button.onClick((data) -> {
  print "Button clicked!"
})
button.click()
print ""

# Strategy pattern
print "=== Strategy Pattern ==="

class SortStrategy then
  sort(data) then
    throw "Must implement sort method"
  end
end

class BubbleSort extends SortStrategy then
  sort(data) then
    print "Sorting with bubble sort"
    return data.sort()
  end
end

class QuickSort extends SortStrategy then
  sort(data) then
    print "Sorting with quick sort"
    return data.sort()
  end
end

class Sorter then
  constructor(strategy) then
    this.strategy = strategy
  end
  
  setStrategy(strategy) then
    this.strategy = strategy
  end
  
  sort(data) then
    return this.strategy.sort(data)
  end
end

# Use strategy
let sorter = new Sorter(new BubbleSort())
let sorted = sorter.sort([3, 1, 4, 1, 5, 9, 2, 6])

sorter.setStrategy(new QuickSort())
sorted = sorter.sort([3, 1, 4, 1, 5, 9, 2, 6])
print ""

# Decorator pattern
print "=== Decorator Pattern ==="

class Coffee then
  cost() then
    return 5
  end
  
  description() then
    return "Simple coffee"
  end
end

class MilkDecorator then
  constructor(coffee) then
    this.coffee = coffee
  end
  
  cost() then
    return this.coffee.cost() + 2
  end
  
  description() then
    return this.coffee.description() + ", milk"
  end
end

class SugarDecorator then
  constructor(coffee) then
    this.coffee = coffee
  end
  
  cost() then
    return this.coffee.cost() + 1
  end
  
  description() then
    return this.coffee.description() + ", sugar"
  end
end

# Use decorator
let coffee = new Coffee()
print coffee.description(), ":", coffee.cost()

coffee = new MilkDecorator(coffee)
print coffee.description(), ":", coffee.cost()

coffee = new SugarDecorator(coffee)
print coffee.description(), ":", coffee.cost()
print ""

# Proxy pattern
print "=== Proxy Pattern ==="

class RealImage then
  constructor(filename) then
    this.filename = filename
    this.loadFromDisk()
  end
  
  loadFromDisk() then
    print "Loading image:", this.filename
  end
  
  display() then
    print "Displaying image:", this.filename
  end
end

class ImageProxy then
  constructor(filename) then
    this.filename = filename
    this.realImage = null
  end
  
  display() then
    if this.realImage == null then
      this.realImage = new RealImage(this.filename)
    end
    this.realImage.display()
  end
end

# Use proxy
let image = new ImageProxy("photo.jpg")
print "Image created (not loaded yet)"
image.display()  # Loads and displays
image.display()  # Just displays
print ""

# Command pattern
print "=== Command Pattern ==="

class Command then
  execute() then
    throw "Must implement execute method"
  end
  
  undo() then
    throw "Must implement undo method"
  end
end

class Light then
  on() then
    print "Light on"
  end
  
  off() then
    print "Light off"
  end
end

class LightOnCommand extends Command then
  constructor(light) then
    super()
    this.light = light
  end
  
  execute() then
    this.light.on()
  end
  
  undo() then
    this.light.off()
  end
end

class LightOffCommand extends Command then
  constructor(light) then
    super()
    this.light = light
  end
  
  execute() then
    this.light.off()
  end
  
  undo() then
    this.light.on()
  end
end

class RemoteControl then
  constructor() then
    this.commands = []
  end
  
  setCommand(command) then
    this.commands.push(command)
  end
  
  pressButton() then
    let command = this.commands.pop()
    command.execute()
  end
  
  pressUndo() then
    let command = this.commands.pop()
    command.undo()
  end
end

# Use command
let light = new Light()
let remote = new RemoteControl()

remote.setCommand(new LightOnCommand(light))
remote.setCommand(new LightOffCommand(light))

remote.pressButton()  # Light off
remote.pressUndo()    # Light on
print ""

# Adapter pattern
print "=== Adapter Pattern ==="

class EuropeanSocket then
  voltage() then
    return 230
  end
  
  live() then
    return 1
  end
  
  neutral() then
    return -1
  end
end

class AmericanSocket then
  voltage() then
    return 120
  end
  
  live() then
    return 1
  end
  
  neutral() then
    return -1
  end
end

class Adapter then
  constructor(socket) then
    this.socket = socket
  end
  
  voltage() then
    return this.socket.voltage()
  end
  
  live() then
    return this.socket.live()
  end
  
  neutral() then
    return this.socket.neutral()
  end
end

# Use adapter
let europeanSocket = new EuropeanSocket()
let adapter = new Adapter(europeanSocket)

print "Voltage:", adapter.voltage()
print ""

# Facade pattern
print "=== Facade Pattern ==="

class CPU then
  freeze() then
    print "Freezing CPU"
  end
  
  jump(address) then
    print "Jumping to address:", address
  end
  
  execute() then
    print "Executing instructions"
  end
end

class Memory then
  load(address, data) then
    print "Loading data to address:", address
  end
end

class HardDrive then
  read(sector, size) then
    print "Reading from sector:", sector
    return "data"
  end
end

class ComputerFacade then
  constructor() then
    this.cpu = new CPU()
    this.memory = new Memory()
    this.hardDrive = new HardDrive()
  end
  
  start() then
    this.cpu.freeze()
    this.memory.load(0, this.hardDrive.read(0, 1024))
    this.cpu.jump(0)
    this.cpu.execute()
  end
end

# Use facade
let computer = new ComputerFacade()
computer.start()
print ""

print "=== Design Patterns Example Complete ==="
