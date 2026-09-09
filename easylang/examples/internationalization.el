# Internationalization (i18n) Example

# Load language files
print "=== Loading Languages ==="
let i18n = i18n.create({
  defaultLocale: "en",
  fallbackLocale: "en",
  messages: {
    en: {
      greeting: "Hello, {name}!",
      farewell: "Goodbye, {name}!",
      items: "You have {count} item(s)",
      plural: {
        one: "You have # item",
        other: "You have # items"
      }
    },
    es: {
      greeting: "¡Hola, {name}!",
      farewell: "¡Adiós, {name}!",
      items: "Tienes {count} artículo(s)",
      plural: {
        one: "Tienes # artículo",
        other: "Tienes # artículos"
      }
    },
    fr: {
      greeting: "Bonjour, {name}!",
      farewell: "Au revoir, {name}!",
      items: "Vous avez {count} article(s)",
      plural: {
        one: "Vous avez # article",
        other: "Vous avez # articles"
      }
    }
  }
})

print "Languages loaded"
print ""

# Basic translation
print "=== Basic Translation ==="

# Set locale
i18n.setLocale("en")
print "Locale:", i18n.getLocale()

# Translate
print "Greeting:", i18n.translate("greeting", {name: "World"})
print ""

# Change locale
i18n.setLocale("es")
print "Locale:", i18n.getLocale())
print "Greeting:", i18n.translate("greeting", {name: "Mundo"})
print ""

# Change locale
i18n.setLocale("fr")
print "Locale:", i18n.getLocale())
print "Greeting:", i18n.translate("greeting", {name: "Monde"})
print ""

# Pluralization
print "=== Pluralization ==="

i18n.setLocale("en")
print "0 items:", i18n.translate("plural", {count: 0})
print "1 item:", i18n.translate("plural", {count: 1})
print "5 items:", i18n.translate("plural", {count: 5})
print ""

# Date formatting
print "=== Date Formatting ==="

let date = new Date()

i18n.setLocale("en")
print "English date:", i18n.formatDate(date, {dateStyle: "full"})

i18n.setLocale("es")
print "Spanish date:", i18n.formatDate(date, {dateStyle: "full"})

i18n.setLocale("fr")
print "French date:", i18n.formatDate(date, {dateStyle: "full"})
print ""

# Number formatting
print "=== Number Formatting ==="

let number = 1234567.89

i18n.setLocale("en")
print "English number:", i18n.formatNumber(number, {style: "decimal"})

i18n.setLocale("de")
print "German number:", i18n.formatNumber(number, {style: "decimal"})

i18n.setLocale("fr")
print "French number:", i18n.formatNumber(number, {style: "decimal"})
print ""

# Currency formatting
print "=== Currency Formatting ==="

let price = 1234.56

i18n.setLocale("en")
print "USD:", i18n.formatCurrency(price, {currency: "USD"})

i18n.setLocale("de")
print "EUR:", i18n.formatCurrency(price, {currency: "EUR"})

i18n.setLocale("ja")
print "JPY:", i18n.formatCurrency(price, {currency: "JPY"})
print ""

# Time formatting
print "=== Time Formatting ==="

let time = new Date()

i18n.setLocale("en")
print "English time:", i18n.formatTime(time, {timeStyle: "medium"})

i18n.setLocale("de")
print "German time:", i18n.formatTime(time, {timeStyle: "medium"})

i18n.setLocale("ja")
print "Japanese time:", i18n.formatTime(time, {timeStyle: "medium"})
print ""

# Relative time
print "=== Relative Time ==="

let pastDate = new Date(Date.now() - 3600000)  # 1 hour ago
let futureDate = new Date(Date.now() + 86400000)  # 1 day from now

i18n.setLocale("en")
print "1 hour ago:", i18n.formatRelativeTime(pastDate)
print "1 day from now:", i18n.formatRelativeTime(futureDate)

i18n.setLocale("es")
print "1 hour ago:", i18n.formatRelativeTime(pastDate)
print "1 day from now:", i18n.formatRelativeTime(futureDate)
print ""

# RTL support
print "=== RTL Support ==="

i18n.setLocale("ar")  # Arabic
print "Locale:", i18n.getLocale()
print "RTL:", i18n.isRTL()
print "Greeting:", i18n.translate("greeting", {name: "عالم"})
print ""

# Language detection
print "=== Language Detection ==="

# Detect from browser
let browserLang = i18n.detectLanguage()
print "Browser language:", browserLang

# Detect from URL
let urlLang = i18n.detectLanguageFromURL("https://example.com/es/page")
print "URL language:", urlLang

# Detect from header
let headerLang = i18n.detectLanguageFromHeader("en-US,en;q=0.9")
print "Header language:", headerLang
print ""

# Loading translations
print "=== Loading Translations ==="

# Load from file
i18n.loadMessages("locales/en.json")
i18n.loadMessages("locales/es.json")
i18n.loadMessages("locales/fr.json")

# Load from API
async function loadTranslations(locale) then
  let response = await http.get("https://api.example.com/translations/" + locale)
  i18n.setMessages(locale, response.body)
end

# Load all translations
async function loadAllTranslations() then
  let locales = ["en", "es", "fr", "de", "ja"]
  let promises = locales.map(locale -> loadTranslations(locale))
  await Promise.all(promises)
  print "All translations loaded"
end

loadAllTranslations()
print ""

# Fallback handling
print "=== Fallback Handling ==="

i18n.setLocale("unknown")
print "Locale:", i18n.getLocale()
print "Fallback:", i18n.getFallbackLocale())
print "Greeting:", i18n.translate("greeting", {name: "World"})
print ""

# Missing translation handling
print "=== Missing Translation ==="

i18n.setLocale("en")
print "Missing key:", i18n.translate("missing_key")
print "With fallback:", i18n.translate("missing_key", {fallback: "Default value"})
print ""

# Namespace support
print "=== Namespace Support ==="

i18n.setMessages("en", {
  common: {
    greeting: "Hello!",
    farewell: "Goodbye!"
  },
  auth: {
    login: "Login",
    logout: "Logout"
  }
})

i18n.setLocale("en")
print "Common greeting:", i18n.translate("common:greeting")
print "Auth login:", i18n.translate("auth:login")
print ""

# Interpolation
print "=== Interpolation ==="

i18n.setLocale("en")
i18n.setMessages("en", {
  greeting: "Hello, {name}!",
  items: "You have {count} item(s)",
  nested: {
    message: "Nested message: {value}"
  }
})

print "Simple:", i18n.translate("greeting", {name: "World"})
print "With count:", i18n.translate("items", {count: 5})
print "Nested:", i18n.translate("nested:message", {value: "test"})
print ""

# Formatting functions
print "=== Formatting Functions ==="

i18n.setLocale("en")
i18n.setMessages("en", {
  greeting: "Hello, {name | uppercase}!",
  date: "Today is {date | date:medium}",
  number: "Price: {price | currency:USD}"
})

print "Uppercase:", i18n.translate("greeting", {name: "world"})
print "Date:", i18n.translate("date", {date: new Date()})
print "Currency:", i18n.translate("number", {price: 1234.56})
print ""

# Loading states
print "=== Loading States ==="

i18n.on("loading", (locale) -> {
  print "Loading translations for:", locale
})

i18n.on("loaded", (locale) -> {
  print "Translations loaded for:", locale
})

i18n.on("error", (error) -> {
  print "Error loading translations:", error
})

print "Event handlers set up"
print ""

print "=== Internationalization Example Complete ==="
