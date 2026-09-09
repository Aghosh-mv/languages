# State Management Example

# Simple state management
print "=== Simple State Management ==="

# Create store
let store = createStore({
  state: {
    count: 0,
    user: null,
    items: []
  },
  mutations: {
    increment(state) then
      state.count = state.count + 1
    end,
    decrement(state) then
      state.count = state.count - 1
    end,
    setUser(state, user) then
      state.user = user
    end,
    addItem(state, item) then
      state.items.push(item)
    end
  },
  actions: {
    incrementAsync({commit}) then
      setTimeout(() -> {
        commit("increment")
      }, 1000)
    end,
    fetchUser({commit}, userId) then
      return http.get("/api/users/" + userId).then(response => {
        commit("setUser", response.body)
      })
    end
  },
  getters: {
    doubleCount(state) then
      return state.count * 2
    end,
    currentUser(state) then
      return state.user
    end
  }
})

# Use store
store.commit("increment")
print "Count:", store.state.count
print "Double count:", store.getters.doubleCount

store.commit("addItem", {id: 1, name: "Item 1"})
print "Items:", store.state.items
print ""

# Redux-like state management
print "=== Redux-like State Management ==="

# Create reducer
function counterReducer(state = {count: 0}, action) then
  switch(action.type)
    when "INCREMENT":
      return {...state, count: state.count + 1}
    when "DECREMENT":
      return {...state, count: state.count - 1}
    when "SET":
      return {...state, count: action.payload}
    default:
      return state
  end
end

# Create store
let reduxStore = createStore(counterReducer)

# Subscribe to changes
reduxStore.subscribe(() -> {
  print "State changed:", reduxStore.getState()
})

# Dispatch actions
reduxStore.dispatch({type: "INCREMENT"})
reduxStore.dispatch({type: "INCREMENT"})
reduxStore.dispatch({type: "SET", payload: 10})
print ""

# MobX-like state management
print "=== MobX-like State Management ==="

# Create observable state
let observableState = observable({
  count: 0,
  get doubleCount() {
    return this.count * 2
  }
})

# Create actions
let actions = action({
  increment() {
    observableState.count = observableState.count + 1
  },
  decrement() {
    observableState.count = observableState.count - 1
  }
})

# Create reaction
let disposer = reaction(
  () => observableState.count,
  (count) => {
    print "Count changed to:", count
  }
)

# Use actions
actions.increment()
actions.increment()
actions.decrement()
print ""

# Context API
print "=== Context API ==="

# Create context
let UserContext = createContext({
  user: null,
  updateUser: () -> {}
})

# Provider component
function UserProvider({children}) then
  let [user, setUser] = useState(null)
  
  let updateUser = (newUser) -> {
    setUser(newUser)
  }
  
  return UserContext.Provider({value: {user, updateUser}}, children)
end

# Consumer component
function UserInfo() then
  return UserContext.Consumer(({user, updateUser}) -> {
    if user then
      return gui.createDiv("Hello, " + user.name)
    else
      return gui.createButton("Login", () -> {
        updateUser({name: "Alice"})
      })
    end
  })
end

print "Context API set up"
print ""

# Signals
print "=== Signals ==="

# Create signal
let count = signal(0)
let doubled = computed(() => count.value * 2)

# Create effect
effect(() => {
  print "Count:", count.value, "Doubled:", doubled.value
})

# Update signal
count.value = 1
count.value = 2
count.value = 3
print ""

# Recoil-like state management
print "=== Recoil-like State Management ==="

# Create atoms
let countAtom = atom({
  key: "count",
  default: 0
})

let doubledAtom = selector({
  key: "doubled",
  get: ({get}) -> {
    return get(countAtom) * 2
  }
})

# Use atoms
function Counter() then
  let [count, setCount] = useRecoilState(countAtom)
  let doubled = useRecoilValue(doubledAtom)
  
  return gui.createDiv(
    gui.createDiv("Count: " + count),
    gui.createDiv("Doubled: " + doubled),
    gui.createButton("Increment", () -> setCount(count + 1))
  )
end

print "Recoil-like state management set up"
print ""

# Zustand-like state management
print "=== Zustand-like State Management ==="

# Create store
let useStore = createStore((set) -> ({
  count: 0,
  increment: () -> set((state) -> ({count: state.count + 1})),
  decrement: () -> set((state) -> ({count: state.count - 1}))
}))

# Use store
function Counter() then
  let count = useStore((state) => state.count)
  let increment = useStore((state) => state.increment)
  
  return gui.createButton("Count: " + count, increment)
end

print "Zustand-like state management set up"
print ""

# Jotai-like state management
print "=== Jotai-like State Management ==="

# Create atoms
let countAtom = atom(0)
let doubledAtom = atom((get) -> get(countAtom) * 2)

# Use atoms
function Counter() then
  let [count, setCount] = useAtom(countAtom)
  let [doubled] = useAtom(doubledAtom)
  
  return gui.createDiv(
    gui.createDiv("Count: " + count),
    gui.createDiv("Doubled: " + doubled),
    gui.createButton("Increment", () -> setCount(count + 1))
  )
end

print "Jotai-like state management set up"
print ""

# XState-like state management
print "=== XState-like State Management ==="

# Create state machine
let counterMachine = createMachine({
  id: "counter",
  initial: "idle",
  context: {
    count: 0
  },
  states: {
    idle: {
      on: {
        INCREMENT: {
          target: "idle",
          actions: assign({
            count: (context) -> context.count + 1
          })
        },
        DECREMENT: {
          target: "idle",
          actions: assign({
            count: (context) -> context.count - 1
          })
        }
      }
    }
  }
})

# Use state machine
let service = interpret(counterMachine)
service.start()

service.send("INCREMENT")
service.send("INCREMENT")
service.send("DECREMENT")

print "State:", service.state.context.count
print ""

# Immutable state updates
print "=== Immutable State Updates ==="

# Immutable update functions
function update(state, path, value) then
  let keys = path.split(".")
  let result = {...state}
  let current = result
  
  for i in range(len(keys) - 1)
    current[keys[i]] = {...current[keys[i]]}
    current = current[keys[i]]
  end
  
  current[keys[len(keys) - 1]] = value
  return result
end

# Test immutable update
let state = {
  user: {
    name: "Alice",
    address: {
      city: "New York"
    }
  }
}

let newState = update(state, "user.address.city", "San Francisco")
print "Original:", state.user.address.city
print "Updated:", newState.user.address.city
print ""

print "=== State Management Example Complete ==="
