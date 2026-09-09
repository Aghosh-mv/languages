# Deployment Example

# Docker deployment
print "=== Docker Deployment ==="

# Generate Dockerfile
let dockerfile = """
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
"""

file.write("Dockerfile", dockerfile)
print "Dockerfile generated"
print ""

# Generate docker-compose.yml
let docker-compose = """
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydb
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
"""

file.write("docker-compose.yml", docker-compose)
print "docker-compose.yml generated"
print ""

# Kubernetes deployment
print "=== Kubernetes Deployment ==="

# Generate deployment.yaml
let deployment = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:latest
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: my-secrets
              key: database-url
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
"""

file.write("kubernetes/deployment.yaml", deployment)
print "Kubernetes deployment.yaml generated"
print ""

# Generate service.yaml
let service = """
apiVersion: v1
kind: Service
metadata:
  name: my-app-service
spec:
  selector:
    app: my-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
"""

file.write("kubernetes/service.yaml", service)
print "Kubernetes service.yaml generated"
print ""

# CI/CD pipeline
print "=== CI/CD Pipeline ==="

# Generate GitHub Actions workflow
let github_actions = """
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Run linting
      run: |
        flake8 .
        black --check .
    
    - name: Run type checking
      run: |
        mypy .

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1
    
    - name: Login to DockerHub
      uses: docker/login-action@v1
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    
    - name: Build and push
      uses: docker/build-push-action@v2
      with:
        context: .
        push: true
        tags: my-app:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f kubernetes/
        kubectl rollout restart deployment/my-app
"""

file.write(".github/workflows/ci-cd.yml", github_actions)
print "GitHub Actions workflow generated"
print ""

# Terraform infrastructure
print "=== Terraform Infrastructure ==="

# Generate main.tf
let terraform = """
provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "web-server"
  }
}

resource "aws_s3_bucket" "data" {
  bucket = "my-app-data-bucket"

  tags = {
    Name        = "Data bucket"
    Environment = "Production"
  }
}

resource "aws_db_instance" "database" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "13.4"
  instance_class       = "db.t3.micro"
  name                 = "mydb"
  username             = "admin"
  password             = var.database_password
  skip_final_snapshot  = true
}
"""

file.write("terraform/main.tf", terraform)
print "Terraform configuration generated"
print ""

# Ansible playbook
print "=== Ansible Playbook ==="

# Generate playbook
let ansible = """
---
- hosts: web servers
  become: yes
  vars:
    app_name: my-app
    app_version: "1.0.0"
  
  tasks:
  - name: Update apt cache
    apt:
      update_cache: yes
      cache_valid_time: 3600

  - name: Install dependencies
    apt:
      name:
        - python3
        - python3-pip
        - nginx
      state: present

  - name: Copy application code
    copy:
      src: /path/to/app
      dest: /opt/{{ app_name }}
      owner: www-data
      group: www-data

  - name: Install Python dependencies
    pip:
      requirements: /opt/{{ app_name }}/requirements.txt

  - name: Configure nginx
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/sites-available/{{ app_name }}
    notify: Restart nginx

  - name: Enable nginx site
    file:
      src: /etc/nginx/sites-available/{{ app_name }}
      dest: /etc/nginx/sites-enabled/{{ app_name }}
      state: link
    notify: Restart nginx

  handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted
"""

file.write("ansible/playbook.yml", ansible)
print "Ansible playbook generated"
print ""

# Monitoring and logging
print "=== Monitoring and Logging ==="

# Generate Prometheus config
let prometheus = """
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'my-app'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 5s
"""

file.write("monitoring/prometheus.yml", prometheus)
print "Prometheus configuration generated"
print ""

# Generate Grafana dashboard
let grafana = """
{
  "dashboard": {
    "title": "My App Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
"""

file.write("monitoring/grafana-dashboard.json", grafana)
print "Grafana dashboard generated"
print ""

# ELK stack
let elasticsearch = """
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0
  },
  "mappings": {
    "properties": {
      "timestamp": {"type": "date"},
      "level": {"type": "keyword"},
      "message": {"type": "text"},
      "service": {"type": "keyword"}
    }
  }
}
"""

file.write("monitoring/elasticsearch.json", elasticsearch)
print "Elasticsearch configuration generated"
print ""

print "=== Deployment Example Complete ==="
