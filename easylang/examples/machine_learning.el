# Machine Learning Example

# Import ML libraries
# import tensorflow as tf
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler

# Simple linear regression
print "=== Linear Regression ==="

# Generate sample data
let x = []
let y = []
for i in range(100)
  x.push(i)
  y.push(i * 2 + 5 + random(-5, 5))
end

# Split data
let x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# Create model
let model = ml.LinearRegression()

# Train model
model.fit(x_train, y_train)

# Make predictions
let predictions = model.predict(x_test)

# Evaluate model
let score = model.score(x_test, y_test)
print "R-squared score:", score
print ""

# Multiple linear regression
print "=== Multiple Linear Regression ==="

# Generate sample data
let features = []
let targets = []
for i in range(100)
  let f1 = random(0, 10)
  let f2 = random(0, 10)
  let f3 = random(0, 10)
  features.push([f1, f2, f3])
  targets.push(f1 * 2 + f2 * 3 + f3 * 4 + random(-5, 5))
end

# Split data
let x_train, x_test, y_train, y_test = train_test_split(features, targets, test_size=0.2)

# Create model
let model = ml.LinearRegression()

# Train model
model.fit(x_train, y_train)

# Make predictions
let predictions = model.predict(x_test)

# Evaluate model
let score = model.score(x_test, y_test)
print "R-squared score:", score
print ""

# Polynomial regression
print "=== Polynomial Regression ==="

# Generate sample data
let x = []
let y = []
for i in range(100)
  let xi = i / 10.0
  x.push(xi)
  y.push(xi * xi + random(-2, 2))
end

# Split data
let x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# Create model
let model = ml.PolynomialRegression(degree=2)

# Train model
model.fit(x_train, y_train)

# Make predictions
let predictions = model.predict(x_test)

# Evaluate model
let score = model.score(x_test, y_test)
print "R-squared score:", score
print ""

# Logistic regression
print "=== Logistic Regression ==="

# Generate sample data
let features = []
let targets = []
for i in range(100)
  let f1 = random(0, 10)
  let f2 = random(0, 10)
  features.push([f1, f2])
  targets.push(f1 + f2 > 10 ? 1 : 0)
end

# Split data
let x_train, x_test, y_train, y_test = train_test_split(features, targets, test_size=0.2)

# Create model
let model = ml.LogisticRegression()

# Train model
model.fit(x_train, y_train)

# Make predictions
let predictions = model.predict(x_test)

# Evaluate model
let accuracy = model.accuracy(y_test, predictions)
print "Accuracy:", accuracy
print ""

# Decision tree
print "=== Decision Tree ==="

# Generate sample data
let features = []
let targets = []
for i in range(100)
  let f1 = random(0, 10)
  let f2 = random(0, 10)
  features.push([f1, f2])
  targets.push(f1 > 5 ? 1 : 0)
end

# Split data
let x_train, x_test, y_train, y_test = train_test_split(features, targets, test_size=0.2)

# Create model
let model = ml.DecisionTree()

# Train model
model.fit(x_train, y_train)

# Make predictions
let predictions = model.predict(x_test)

# Evaluate model
let accuracy = model.accuracy(y_test, predictions)
print "Accuracy:", accuracy
print ""

# Random forest
print "=== Random Forest ==="

# Generate sample data
let features = []
let targets = []
for i in range(100)
  let f1 = random(0, 10)
  let f2 = random(0, 10)
  features.push([f1, f2])
  targets.push(f1 + f2 > 10 ? 1 : 0)
end

# Split data
let x_train, x_test, y_train, y_test = train_test_split(features, targets, test_size=0.2)

# Create model
let model = ml.RandomForest(n_estimators=100)

# Train model
model.fit(x_train, y_train)

# Make predictions
let predictions = model.predict(x_test)

# Evaluate model
let accuracy = model.accuracy(y_test, predictions)
print "Accuracy:", accuracy
print ""

# Support vector machine
print "=== Support Vector Machine ==="

# Generate sample data
let features = []
let targets = []
for i in range(100)
  let f1 = random(0, 10)
  let f2 = random(0, 10)
  features.push([f1, f2])
  targets.push(f1 + f2 > 10 ? 1 : 0)
end

# Split data
let x_train, x_test, y_train, y_test = train_test_split(features, targets, test_size=0.2)

# Create model
let model = ml.SVM()

# Train model
model.fit(x_train, y_train)

# Make predictions
let predictions = model.predict(x_test)

# Evaluate model
let accuracy = model.accuracy(y_test, predictions)
print "Accuracy:", accuracy
print ""

# Neural network
print "=== Neural Network ==="

# Generate sample data
let features = []
let targets = []
for i in range(100)
  let f1 = random(0, 10)
  let f2 = random(0, 10)
  features.push([f1, f2])
  targets.push(f1 + f2 > 10 ? 1 : 0)
end

# Split data
let x_train, x_test, y_train, y_test = train_test_split(features, targets, test_size=0.2)

# Create model
let model = ml.NeuralNetwork([
  {type: "dense", units: 64, activation: "relu"},
  {type: "dense", units: 32, activation: "relu"},
  {type: "dense", units: 1, activation: "sigmoid"}
])

# Compile model
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Train model
model.fit(x_train, y_train, epochs=10, batch_size=32)

# Make predictions
let predictions = model.predict(x_test)

# Evaluate model
let loss, accuracy = model.evaluate(x_test, y_test)
print "Loss:", loss
print "Accuracy:", accuracy
print ""

# K-means clustering
print "=== K-Means Clustering ==="

# Generate sample data
let features = []
for i in range(100)
  let cluster = i % 3
  let f1 = cluster * 10 + random(-2, 2)
  let f2 = cluster * 10 + random(-2, 2)
  features.push([f1, f2])
end

# Create model
let model = ml.KMeans(n_clusters=3)

# Train model
model.fit(features)

# Get cluster assignments
let labels = model.labels

# Get centroids
let centroids = model.centroids

print "Cluster labels:", labels.slice(0, 10), "..."
print "Centroids:", centroids
print ""

# Principal component analysis
print "=== Principal Component Analysis ==="

# Generate sample data
let features = []
for i in range(100)
  let f1 = random(0, 10)
  let f2 = random(0, 10)
  let f3 = f1 + f2 + random(-1, 1)
  features.push([f1, f2, f3])
end

# Create model
let model = ml.PCA(n_components=2)

# Fit and transform
let transformed = model.fit_transform(features)

print "Original shape:", [len(features), len(features[0])]
print "Transformed shape:", [len(transformed), len(transformed[0])]
print ""

# Save and load model
print "=== Save and Load Model ==="

# Save model
model.save("model.pkl")

# Load model
let loaded_model = ml.load("model.pkl")
print "Model loaded successfully"
print ""

print "=== Machine Learning Example Complete ==="
