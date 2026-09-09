# Web Scraping Example

# Install requests library
# import requests
# from bs4 import BeautifulSoup

# Simple HTTP request
print "=== Simple HTTP Request ==="
let response = http.get("https://example.com")
print "Status:", response.status
print "Content length:", len(response.body)
print ""

# Parse HTML
print "=== Parse HTML ==="
let soup = html.parse(response.body)

# Find elements
let title = soup.find("title")
print "Title:", title.text

let h1 = soup.find("h1")
print "H1:", h1.text

let paragraphs = soup.find_all("p")
print "Paragraphs:"
for p in paragraphs
  print " -", p.text
end
print ""

# CSS selectors
print "=== CSS Selectors ==="
let links = soup.select("a")
print "Links:"
for link in links
  print " -", link.text, ":", link.get("href")
end
print ""

# Web scraping with beautifulsoup
print "=== Web Scraping ==="
let url = "https://news.ycombinator.com"
let response = http.get(url)
let soup = html.parse(response.body)

# Find all story links
let stories = soup.select(".titleline > a")
print "Top stories:"
for i in range(min(10, len(stories)))
  let story = stories[i]
  print (i + 1) + ".", story.text
  print "   Link:", story.get("href")
end
print ""

# Extract data
print "=== Extract Data ==="
let data = []
for story in stories
  let item = {
    title: story.text,
    url: story.get("href")
  }
  data.push(item)
end

# Save to JSON
let json = JSON.stringify(data, null, 2)
file.write("stories.json", json)
print "Data saved to stories.json"
print ""

# Pagination
print "=== Pagination ==="
let base_url = "https://example.com/page/"
let all_data = []

for page in range(1, 6)
  let url = base_url + str(page)
  let response = http.get(url)
  let soup = html.parse(response.body)
  
  # Extract data from page
  let items = soup.select(".item")
  for item in items
    all_data.push({
      title: item.select(".title").text,
      content: item.select(".content").text,
      page: page
    })
  end
  
  print "Scraped page", page, "-", len(items), "items"
  
  # Delay between requests
  delay(1000)
end

print "Total items:", len(all_data)
print ""

# Handle cookies
print "=== Handle Cookies ==="
let session = http.createSession()

# Login
let login_data = {
  username: "user",
  password: "pass"
}
let response = session.post("https://example.com/login", login_data)

# Access protected page
let response = session.get("https://example.com/protected")
print "Protected page status:", response.status
print ""

# Handle headers
print "=== Handle Headers ==="
let headers = {
  "User-Agent": "EasyLang Bot",
  "Accept": "text/html,application/xhtml+xml",
  "Accept-Language": "en-US,en;q=0.9"
}
let response = http.get("https://example.com", headers)
print "Response with custom headers:", response.status
print ""

# Handle proxies
print "=== Handle Proxies ==="
let proxies = {
  "http": "http://proxy.example.com:8080",
  "https": "http://proxy.example.com:8080"
}
let response = http.get("https://example.com", null, proxies)
print "Response with proxy:", response.status
print ""

# Handle SSL
print "=== Handle SSL ==="
let response = http.get("https://example.com", null, null, {verify: false})
print "Response with SSL verification disabled:", response.status
print ""

# File downloads
print "=== File Downloads ==="
let url = "https://example.com/file.pdf"
let response = http.get(url, null, null, {stream: true})
file.write("file.pdf", response.body)
print "File downloaded: file.pdf"
print ""

# File uploads
print "=== File Upload ==="
let file = file.read("upload.txt")
let response = http.post("https://example.com/upload", {
  file: file,
  description: "Upload file"
})
print "Upload status:", response.status
print ""

# Rate limiting
print "=== Rate Limiting ==="
let rate_limiter = http.createRateLimiter(10)  # 10 requests per second

for i in range(20)
  rate_limiter.wait()
  let response = http.get("https://example.com")
  print "Request", i + 1, "- Status:", response.status
end
print ""

# Caching
print "=== Caching ==="
let cache = http.createCache()

# Check cache
let cached = cache.get("https://example.com/data")
if cached != null then
  print "Using cached data"
else
  let response = http.get("https://example.com/data")
  cache.set("https://example.com/data", response.body, 3600)  # Cache for 1 hour
  print "Fetching fresh data"
end
print ""

# Error handling
print "=== Error Handling ==="
try
  let response = http.get("https://nonexistent.example.com")
  print "Response:", response.status
catch TimeoutError
  print "Request timed out"
catch ConnectionError
  print "Connection failed"
catch HTTPError as e
  print "HTTP error:", e.status, e.message
catch error
  print "Unknown error:", error
end
print ""

print "=== Web Scraping Example Complete ==="
