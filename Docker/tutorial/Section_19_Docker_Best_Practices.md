# Section 19 – Docker Best Practices

## 19.1 Image Best Practices

بهترین روش‌های ایجاد و مدیریت ایمیج‌های Docker.

### اصول کلی:

#### **1. استفاده از ایمیج‌های رسمی:**
```dockerfile
# خوب
FROM node:16-alpine
FROM python:3.9-slim
FROM postgres:13

# بد
FROM ubuntu:20.04
RUN apt-get install -y nodejs
```

#### **2. تعیین نسخه مشخص:**
```dockerfile
# خوب
FROM node:16.14.0-alpine
FROM python:3.9.7-slim

# بد
FROM node:latest
FROM python:latest
```

#### **3. استفاده از ایمیج‌های کوچک:**
```dockerfile
# خوب
FROM alpine:3.14
FROM node:16-alpine

# بد
FROM ubuntu:20.04
FROM node:16
```

### بهینه‌سازی Dockerfile:

#### **1. ترکیب دستورات RUN:**
```dockerfile
# خوب
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# بد
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get clean
```

#### **2. بهینه‌سازی ترتیب دستورات:**
```dockerfile
# خوب
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]

# بد
FROM node:16-alpine
WORKDIR /app
COPY . .
RUN npm ci --only=production
EXPOSE 3000
CMD ["npm", "start"]
```

#### **3. استفاده از .dockerignore:**
```dockerignore
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.nyc_output
coverage
.vscode
.idea
```

### مثال Dockerfile بهینه:
```dockerfile
FROM node:16.14.0-alpine

# ایجاد کاربر غیر root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# تنظیم متغیرهای محیطی
ENV NODE_ENV=production
ENV PORT=3000

# دایرکتوری کاری
WORKDIR /app

# کپی فایل‌های وابستگی
COPY package*.json ./

# نصب وابستگی‌ها
RUN npm ci --only=production && \
    npm cache clean --force && \
    rm -rf /tmp/*

# کپی کد اپلیکیشن
COPY . .

# تغییر مالکیت فایل‌ها
RUN chown -R nextjs:nodejs /app
USER nextjs

# تعریف پورت
EXPOSE 3000

# دستور پیش‌فرض
CMD ["npm", "start"]
```

## 19.2 Container Best Practices

بهترین روش‌های اجرای کانتینرها.

### اصول کلی:

#### **1. اجرا با کاربر غیر root:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    image: nginx:alpine
    user: "1000:1000"
    ports:
      - "80:80"
```

#### **2. محدود کردن منابع:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

#### **3. استفاده از Health Checks:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

#### **4. تنظیم Restart Policy:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
```

### مثال Container Configuration:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
    security_opt:
      - no-new-privileges:true
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    ports:
      - "80:80"
```

## 19.3 Security Best Practices

بهترین روش‌های امنیتی در Docker.

### اصول امنیتی:

#### **1. استفاده از ایمیج‌های امن:**
```dockerfile
# خوب
FROM node:16-alpine
FROM python:3.9-slim

# بد
FROM node:12
FROM python:3.7
```

#### **2. اجرا با کاربر غیر root:**
```dockerfile
FROM node:16-alpine
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs
```

#### **3. حذف ابزارهای غیرضروری:**
```dockerfile
FROM node:16-alpine
RUN apk update && apk upgrade && \
    apk add --no-cache curl && \
    apk del curl && \
    rm -rf /var/cache/apk/*
```

#### **4. استفاده از Secrets:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    secrets:
      - db_password
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

#### **5. محدود کردن Capabilities:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### مثال Security Configuration:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    secrets:
      - ssl_cert
      - ssl_key
    environment:
      - NODE_ENV=production
    ports:
      - "80:80"
      - "443:443"

secrets:
  ssl_cert:
    file: ./ssl/cert.pem
  ssl_key:
    file: ./ssl/key.pem
```

## 19.4 Performance Best Practices

بهترین روش‌های بهینه‌سازی عملکرد.

### بهینه‌سازی عملکرد:

#### **1. بهینه‌سازی ایمیج:**
```dockerfile
# Multi-stage build
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

#### **2. بهینه‌سازی کش:**
```dockerfile
# کپی فایل‌های وابستگی اول
COPY package*.json ./
RUN npm ci --only=production

# سپس کپی کد
COPY . .
```

#### **3. محدود کردن منابع:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

#### **4. بهینه‌سازی شبکه:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    networks:
      - frontend
    ports:
      - "80:80"

  app:
    image: my-app:latest
    networks:
      - frontend
      - backend

  db:
    image: postgres:13
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

### مثال Performance Configuration:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    networks:
      - frontend
    ports:
      - "80:80"
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    ulimits:
      nproc: 65535
      nofile:
        soft: 20000
        hard: 40000

  app:
    image: my-app:latest
    networks:
      - frontend
      - backend
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M
    environment:
      - NODE_ENV=production
      - NODE_OPTIONS=--max-old-space-size=1024

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

## 19.5 Development Best Practices

بهترین روش‌های development با Docker.

### اصول Development:

#### **1. استفاده از Volume Mounting:**
```yaml
version: '3.8'
services:
  web:
    build: .
    volumes:
      - ./src:/app/src
      - /app/node_modules
    environment:
      - NODE_ENV=development
```

#### **2. Hot Reloading:**
```yaml
version: '3.8'
services:
  web:
    build: .
    volumes:
      - ./src:/app/src
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - CHOKIDAR_USEPOLLING=true
    command: npm run dev
```

#### **3. Development Tools:**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
      - "9229:9229"  # Debug port
    volumes:
      - ./src:/app/src
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=*
    command: npm run dev:debug
```

#### **4. Testing Environment:**
```yaml
version: '3.8'
services:
  test:
    build: .
    volumes:
      - ./src:/app/src
      - ./tests:/app/tests
      - /app/node_modules
    environment:
      - NODE_ENV=test
    command: npm test

  test-db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp_test
      POSTGRES_USER: test
      POSTGRES_PASSWORD: testpassword
    volumes:
      - postgres-test-data:/var/lib/postgresql/data

volumes:
  postgres-test-data:
```

## 19.6 Production Best Practices

بهترین روش‌های production با Docker.

### اصول Production:

#### **1. Health Checks:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

#### **2. Logging:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

#### **3. Monitoring:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    labels:
      - "prometheus.scrape=true"
      - "prometheus.port=80"
      - "prometheus.path=/metrics"
```

#### **4. Backup:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    volumes:
      - web-data:/usr/share/nginx/html

  backup:
    image: postgres:13
    volumes:
      - web-data:/data
      - ./backups:/backups
    command: |
      sh -c '
      while true; do
        tar czf /backups/backup-$(date +%Y%m%d-%H%M%S).tar.gz /data
        find /backups -name "backup-*.tar.gz" -mtime +7 -delete
        sleep 3600
      done
      '

volumes:
  web-data:
```

### مثال Production Configuration:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
    security_opt:
      - no-new-privileges:true
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    ports:
      - "80:80"
      - "443:443"
    labels:
      - "prometheus.scrape=true"
      - "prometheus.port=80"
      - "prometheus.path=/metrics"
```

## 19.7 Monitoring Best Practices

بهترین روش‌های نظارت بر Docker.

### اصول Monitoring:

#### **1. Metrics Collection:**
```yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  prometheus-data:
  grafana-data:
```

#### **2. Log Aggregation:**
```yaml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.0
    environment:
      - discovery.type=single-node
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data

  kibana:
    image: docker.elastic.co/kibana/kibana:7.15.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

volumes:
  elasticsearch-data:
```

#### **3. Alerting:**
```yaml
version: '3.8'
services:
  alertmanager:
    image: prom/alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
```

## 19.8 Backup Best Practices

بهترین روش‌های پشتیبان‌گیری از Docker.

### اصول Backup:

#### **1. Database Backup:**
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data

  backup:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./backups:/backups
    command: |
      sh -c '
      while true; do
        pg_dump -h db -U postgres myapp > /backups/backup-$(date +%Y%m%d-%H%M%S).sql
        find /backups -name "backup-*.sql" -mtime +7 -delete
        sleep 3600
      done
      '

volumes:
  postgres-data:
```

#### **2. Volume Backup:**
```bash
#!/bin/bash
# backup-volumes.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d-%H%M%S)

echo "Starting volume backup..."

# Database volume backup
docker run --rm -v postgres-data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/postgres-$DATE.tar.gz /data

# Application volume backup
docker run --rm -v app-data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/app-$DATE.tar.gz /data

# Cleanup old backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Volume backup completed!"
```

## 19.9 Documentation Best Practices

بهترین روش‌های مستندسازی Docker.

### اصول Documentation:

#### **1. README.md:**
```markdown
# My Docker Application

## Quick Start

```bash
# Clone repository
git clone https://github.com/user/my-app.git
cd my-app

# Build and run
docker-compose up --build
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| NODE_ENV | Environment | production |
| PORT | Port number | 3000 |
| DATABASE_URL | Database URL | postgres://localhost:5432/myapp |

## Development

```bash
# Run in development mode
docker-compose -f docker-compose.dev.yml up
```

## Production

```bash
# Run in production mode
docker-compose -f docker-compose.prod.yml up -d
```
```

#### **2. Dockerfile Comments:**
```dockerfile
# Use official Node.js runtime as base image
FROM node:16-alpine

# Create app directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs

# Expose port
EXPOSE 3000

# Start application
CMD ["npm", "start"]
```

## 19.10 Team Collaboration Best Practices

بهترین روش‌های همکاری تیمی با Docker.

### اصول Collaboration:

#### **1. Standardized Development Environment:**
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev

  db:
    image: postgres:13
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: myapp_dev
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpassword
    volumes:
      - postgres-dev-data:/var/lib/postgresql/data

volumes:
  postgres-dev-data:
```

#### **2. Code Review Guidelines:**
```markdown
# Docker Code Review Checklist

## Dockerfile
- [ ] Uses official base image
- [ ] Specifies exact version
- [ ] Runs as non-root user
- [ ] Optimizes layer caching
- [ ] Includes health check
- [ ] Removes unnecessary files

## docker-compose.yml
- [ ] Uses specific image versions
- [ ] Sets resource limits
- [ ] Configures health checks
- [ ] Uses secrets for sensitive data
- [ ] Includes proper networking
```

#### **3. CI/CD Pipeline:**
```yaml
# .github/workflows/ci-cd.yml
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
    - uses: actions/checkout@v3
    - name: Run tests
      run: docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
    - name: Cleanup
      run: docker-compose -f docker-compose.test.yml down -v

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Build image
      run: docker build -t my-app:latest .
    - name: Push image
      run: docker push my-app:latest
```

این بخش شما را با تمام بهترین روش‌های Docker آشنا می‌کند.