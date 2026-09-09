# Component Architecture Example

# React-like components
print "=== React-like Components ==="

# Functional component
function Greeting(props) then
  return gui.createDiv(
    gui.createH1("Hello, " + props.name + "!"),
    gui.createP("Welcome to our application.")
  )
end

# Class component
class Welcome extends Component then
  constructor(props) then
    super(props)
    this.state = {count: 0}
  end
  
  render() then
    return gui.createDiv(
      gui.createH1("Welcome, " + this.props.name + "!"),
      gui.createP("Count: " + this.state.count),
      gui.createButton("Increment", () -> {
        this.setState({count: this.state.count + 1})
      })
    )
  end
end

print "React-like components defined"
print ""

# Vue-like components
print "=== Vue-like Components ==="

# Vue component
let Counter = {
  template: """
    <div>
      <p>Count: {{ count }}</p>
      <button @click="increment">Increment</button>
    </div>
  """,
  data() {
    return {
      count: 0
    }
  },
  methods: {
    increment() {
      this.count++
    }
  }
}

# Vue component with props
let UserCard = {
  template: """
    <div class="user-card">
      <h2>{{ name }}</h2>
      <p>{{ email }}</p>
    </div>
  """,
  props: {
    name: String,
    email: String
  }
}

print "Vue-like components defined"
print ""

# Angular-like components
print "=== Angular-like Components ==="

# Angular component
@Component({
  selector: "app-counter",
  template: """
    <div>
      <p>Count: {{ count }}</p>
      <button (click)="increment()">Increment</button>
    </div>
  """
})
class CounterComponent {
  count = 0
  
  increment() {
    this.count++
  }
}

print "Angular-like components defined"
print ""

# Svelte-like components
print "=== Svelte-like Components ==="

# Svelte component
# <script>
#   let count = 0;
#   
#   function increment() {
#     count++
#   }
# </script>
# 
# <div>
#   <p>Count: {count}</p>
#   <button on:click={increment}>Increment</button>
# </div>

print "Svelte-like components defined"
print ""

# Web Components
print "=== Web Components ==="

# Custom element
class MyElement extends HTMLElement {
  constructor() {
    super()
    this.attachShadow({mode: "open"})
  }
  
  connectedCallback() {
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          border: 1px solid #ccc;
          padding: 16px;
        }
      </style>
      <div>
        <h2>My Element</h2>
        <p><slot></slot></p>
      </div>
    `
  }
}

customElements.define("my-element", MyElement)

print "Web Components defined"
print ""

# Composite pattern
print "=== Composite Pattern ==="

# Component interface
class Component then
  render() then
    throw "Must implement render method"
  end
end

# Leaf component
class Text extends Component then
  constructor(text) then
    super()
    this.text = text
  end
  
  render() then
    return gui.createText(this.text)
  end
end

# Composite component
class Container extends Component then
  constructor() then
    super()
    this.children = []
  end
  
  add(child) then
    this.children.push(child)
  end
  
  render() then
    let element = gui.createDiv()
    for child in this.children
      element.add(child.render())
    end
    return element
  end
end

# Use composite pattern
let container = new Container()
container.add(new Text("Hello"))
container.add(new Text("World"))

let element = container.render()
print "Composite pattern implemented"
print ""

# Decorator pattern
print "=== Decorator Pattern ==="

# Base component
class Button extends Component then
  constructor(text) then
    super()
    this.text = text
  end
  
  render() then
    return gui.createButton(this.text)
  end
end

# Decorator
class DisabledButton extends Button then
  constructor(button) then
    super(button.text)
    this.button = button
  end
  
  render() then
    let element = this.button.render()
    element.setAttribute("disabled", "true")
    return element
  end
end

# Another decorator
class LoadingButton extends Button then
  constructor(button) then
    super(button.text)
    this.button = button
  end
  
  render() then
    let element = this.button.render()
    element.add(gui.createSpinner())
    return element
  end
end

# Use decorators
let button = new Button("Click me")
let disabledButton = new DisabledButton(button)
let loadingButton = new LoadingButton(button)

print "Decorator pattern implemented"
print ""

# Observer pattern
print "=== Observer Pattern ==="

# Subject
class EventEmitter then
  constructor() {
    this.listeners = {}
  }
  
  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = []
    }
    this.listeners[event].push(callback)
  }
  
  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => callback(data))
    }
  }
}

# Observer
class Button extends Component {
  constructor(text) {
    super()
    this.text = text
    this.emitter = new EventEmitter()
  }
  
  onClick(callback) {
    this.emitter.on("click", callback)
  }
  
  render() {
    let element = gui.createButton(this.text)
    element.onClick(() => {
      this.emitter.emit("click")
    })
    return element
  }
}

# Use observer pattern
let button = new Button("Click me")
button.onClick(() -> {
  print "Button clicked!"
})

print "Observer pattern implemented"
print ""

# Render props
print "=== Render Props ==="

# Component with render prop
class MouseTracker extends Component {
  constructor(props) {
    super(props)
    this.state = {x: 0, y: 0}
  }
  
  handleMouseMove(event) {
    this.setState({
      x: event.clientX,
      y: event.clientY
    })
  }
  
  render() {
    return gui.createDiv(
      gui.createDiv("Mouse position: " + this.state.x + ", " + this.state.y),
      this.props.render(this.state)
    )
  }
}

# Use render prop
let tracker = new MouseTracker({
  render: (position) -> {
    return gui.createDiv("X: " + position.x + ", Y: " + position.y)
  }
})

print "Render props implemented"
print ""

# Higher-order components
print "=== Higher-Order Components ==="

# HOC
function withLogger(WrappedComponent) {
  return class extends Component {
    componentDidMount() {
      console.log("Component mounted:", WrappedComponent.name)
    }
    
    componentWillUnmount() {
      console.log("Component unmounted:", WrappedComponent.name)
    }
    
    render() {
      return <WrappedComponent {...this.props} />
    }
  }
}

# Use HOC
let LoggedButton = withLogger(Button)

print "Higher-order components implemented"
print ""

# Hooks
print "=== Hooks ==="

# useState hook
function useState(initialValue) {
  let value = initialValue
  let setValue = (newValue) -> {
    value = newValue
    reRender()
  }
  return [value, setValue]
}

# useEffect hook
function useEffect(callback, dependencies) {
  let prevDependencies = dependencies
  
  function checkDependencies() {
    if (JSON.stringify(prevDependencies) !== JSON.stringify(dependencies)) {
      callback()
      prevDependencies = dependencies
    }
  }
  
  // Run on mount and when dependencies change
  checkDependencies()
}

# Use hooks
function Counter() {
  let [count, setCount] = useState(0)
  
  useEffect(() -> {
    console.log("Count changed:", count)
  }, [count])
  
  return gui.createDiv(
    gui.createP("Count: " + count),
    gui.createButton("Increment", () -> setCount(count + 1))
  )
}

print "Hooks implemented"
print ""

print "=== Component Architecture Example Complete ==="
