# Testing Frameworks Example

# Jest-like testing
print "=== Jest-like Testing ==="

# Test suite
describe("Calculator", () => {
  let calculator
  
  beforeEach(() => {
    calculator = new Calculator()
  })
  
  afterEach(() => {
    calculator = null
  })
  
  test("should add two numbers", () => {
    expect(calculator.add(2, 3)).toBe(5)
  })
  
  test("should subtract two numbers", () => {
    expect(calculator.subtract(5, 3)).toBe(2)
  })
  
  test("should multiply two numbers", () => {
    expect(calculator.multiply(2, 3)).toBe(6)
  })
  
  test("should divide two numbers", () => {
    expect(calculator.divide(6, 3)).toBe(2)
  })
  
  test("should throw error on division by zero", () => {
    expect(() -> calculator.divide(1, 0)).toThrow("Division by zero")
  })
  
  describe("with negative numbers", () => {
    test("should add negative numbers", () => {
      expect(calculator.add(-2, -3)).toBe(-5)
    })
    
    test("should subtract negative numbers", () => {
      expect(calculator.subtract(-2, -3)).toBe(1)
    })
  })
})
print ""

# Mocha-like testing
print "=== Mocha-like Testing ==="

describe("Array", () => {
  describe("#indexOf()", () => {
    test("should return -1 when the value is not present", () => {
      assert.equal([1, 2, 3].indexOf(4), -1)
    })
    
    test("should return the index when the value is present", () => {
      assert.equal([1, 2, 3].indexOf(2), 1)
    })
  })
})
print ""

# Jasmine-like testing
print "=== Jasmine-like Testing ==="

describe("Pet", () => {
  let pet
  
  beforeEach(() => {
    pet = new Pet("Fido")
  })
  
  it("should be created with a name", () => {
    expect(pet.name).toBe("Fido")
  })
  
  it("should be able to eat", () => {
    pet.eat()
    expect(pet.hunger).toBeLessThan(100)
  })
  
  it("should be able to play", () => {
    pet.play()
    expect(pet.happiness).toBeGreaterThan(0)
  })
  
  describe("when hungry", () => {
    beforeEach(() => {
      pet.hunger = 100
    })
    
    it("should be hungry", () => {
      expect(pet.isHungry()).toBe(true)
    })
    
    it("should eat when fed", () => {
      pet.feed()
      expect(pet.hunger).toBeLessThan(100)
    })
  })
})
print ""

# Cypress-like testing
print "=== Cypress-like Testing ==="

describe("Login", () => {
  beforeEach(() => {
    cy.visit("/login")
  })
  
  test("should login successfully", () => {
    cy.get("[data-testid=email]").type("user@example.com")
    cy.get("[data-testid=password]").type("password")
    cy.get("[data-testid=submit]").click()
    
    cy.url().should("include", "/dashboard")
    cy.get("[data-testid=welcome]").should("contain", "Welcome")
  })
  
  test("should show error for invalid credentials", () => {
    cy.get("[data-testid=email]").type("wrong@example.com")
    cy.get("[data-testid=password]").type("wrongpassword")
    cy.get("[data-testid=submit]").click()
    
    cy.get("[data-testid=error]").should("contain", "Invalid credentials")
  })
  
  test("should validate required fields", () => {
    cy.get("[data-testid=submit]").click()
    
    cy.get("[data-testid=email-error]").should("contain", "Email is required")
    cy.get("[data-testid=password-error]").should("contain", "Password is required")
  })
})
print ""

# Puppeteer-like testing
print "=== Puppeteer-like Testing ==="

describe("Homepage", () => {
  let browser
  let page
  
  beforeEach(async () => {
    browser = await puppeteer.launch()
    page = await browser.newPage()
    await page.goto("https://example.com")
  })
  
  afterEach(async () => {
    await browser.close()
  })
  
  test("should display the title", async () => {
    let title = await page.title()
    expect(title).toBe("Example Domain")
  })
  
  test("should have a heading", async () => {
    let heading = await page.$eval("h1", el => el.textContent)
    expect(heading).toBe("Example Domain")
  })
  
  test("should click a link", async () => {
    await page.click("a")
    await page.waitForNavigation()
    expect(page.url()).toContain("example.com")
  })
})
print ""

# Playwright-like testing
print "=== Playwright-like Testing ==="

describe("Search", () => {
  let browser
  let page
  
  beforeAll(async () => {
    browser = await chromium.launch()
    page = await browser.newPage()
  })
  
  afterAll(async () => {
    await browser.close()
  })
  
  test("should search for results", async () => {
    await page.goto("https://example.com")
    await page.fill("[data-testid=search]", "test query")
    await page.click("[data-testid=search-button]")
    
    await page.waitForSelector("[data-testid=results]")
    let results = await page.$$("[data-testid=result-item]")
    expect(results.length).toBeGreaterThan(0)
  })
  
  test("should display search suggestions", async () => {
    await page.goto("https://example.com")
    await page.type("[data-testid=search]", "test", {delay: 100})
    
    await page.waitForSelector("[data-testid=suggestions]")
    let suggestions = await page.$$("[data-testid=suggestion]")
    expect(suggestions.length).toBeGreaterThan(0)
  })
})
print ""

# Vitest-like testing
print "=== Vitest-like Testing ==="

import {describe, it, expect, vi} from "vitest"

describe("UserService", () => {
  let userService
  
  beforeEach(() => {
    userService = new UserService()
  })
  
  it("should create a user", async () => {
    let user = await userService.create({name: "Alice"})
    expect(user).toHaveProperty("id")
    expect(user.name).toBe("Alice")
  })
  
  it("should find a user by id", async () => {
    let user = await userService.create({name: "Alice"})
    let found = await userService.findById(user.id)
    expect(found).toEqual(user)
  })
  
  it("should update a user", async () => {
    let user = await userService.create({name: "Alice"})
    let updated = await userService.update(user.id, {name: "Bob"})
    expect(updated.name).toBe("Bob")
  })
  
  it("should delete a user", async () => {
    let user = await userService.create({name: "Alice"})
    await userService.delete(user.id)
    let found = await userService.findById(user.id)
    expect(found).toBeNull()
  })
})
print ""

# React Testing Library-like testing
print "=== React Testing Library-like Testing ==="

describe("Counter", () => {
  test("renders with initial count", () => {
    render(<Counter initialCount={0} />)
    expect(screen.getByText("Count: 0")).toBeInTheDocument()
  })
  
  test("increments count", () => {
    render(<Counter initialCount={0} />)
    fireEvent.click(screen.getByText("Increment"))
    expect(screen.getByText("Count: 1")).toBeInTheDocument()
  })
  
  test("decrements count", () => {
    render(<Counter initialCount={0} />)
    fireEvent.click(screen.getByText("Decrement"))
    expect(screen.getByText("Count: -1")).toBeInTheDocument()
  })
  
  test("resets count", () => {
    render(<Counter initialCount={5} />)
    fireEvent.click(screen.getByText("Reset"))
    expect(screen.getByText("Count: 0")).toBeInTheDocument()
  })
})
print ""

# Snapshot testing
print "=== Snapshot Testing ==="

test("renders correctly", () => {
  let tree = renderer.create(<App />).toJSON()
  expect(tree).toMatchSnapshot()
})

test("renders with props", () => {
  let tree = renderer.create(<App title="Test" />).toJSON()
  expect(tree).toMatchSnapshot()
})
print ""

# Mocking
print "=== Mocking ==="

# Mock function
let mockFn = vi.fn()
mockFn("hello")
expect(mockFn).toHaveBeenCalledWith("hello")
expect(mockFn).toHaveBeenCalledTimes(1)

# Mock module
vi.mock("./api", () => ({
  fetchData: vi.fn().mockResolvedValue({data: "mocked"})
}))

# Spy on method
let spy = vi.spyOn(console, "log")
console.log("test")
expect(spy).toHaveBeenCalledWith("test")
spy.mockRestore()
print ""

# Code coverage
print "=== Code Coverage ==="

# Run tests with coverage
# npx vitest --coverage

# Coverage report
# {
#   "total": {
#     "statements": 85.7,
#     "branches": 80.0,
#     "functions": 90.0,
#     "lines": 85.7
#   },
#   "files": {
#     "src/calculator.js": {
#       "statements": 100,
#       "branches": 100,
#       "functions": 100,
#       "lines": 100
#     }
#   }
# }

print "Code coverage example"
print ""

print "=== Testing Frameworks Example Complete ==="
