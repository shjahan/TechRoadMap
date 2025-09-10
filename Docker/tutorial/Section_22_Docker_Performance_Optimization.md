# Section 22 – Docker Performance Optimization

## 22.1 Container Performance Tuning

بهینه‌سازی عملکرد کانتینرها برای بهبود کارایی.

### اصول بهینه‌سازی:

#### **1. محدود کردن منابع:**
```yaml
# docker-compose.yml
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
    ulimits:
      nproc: 65535
      nofile:
        soft: 20000
        hard: 40000
```

#### **2. بهینه‌سازی CPU:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      resources:
        limits:
          cpus: '2.0'
        reservations:
          cpus: '1.0'
    cpuset: "0,1"  # استفاده از CPU cores خاص
```

#### **3. بهینه‌سازی حافظه:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
    environment:
      - NODE_OPTIONS=--max-old-space-size=1024
```

### مثال بهینه‌سازی کامل:
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
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M
    ulimits:
      nproc: 65535
      nofile:
        soft: 20000
        hard: 40000
    sysctls:
      - net.core.somaxconn=65535
      - net.ipv4.tcp_max_syn_backlog=65535
    ports:
      - "80:80"
```

## 22.2 Image Size Optimization

بهینه‌سازی اندازه ایمیج‌ها برای بهبود عملکرد.

### تکنیک‌های بهینه‌سازی:

#### **1. استفاده از ایمیج‌های کوچک:**
```dockerfile
# خوب
FROM alpine:3.14
FROM node:16-alpine
FROM python:3.9-slim

# بد
FROM ubuntu:20.04
FROM node:16
FROM python:3.9
```

#### **2. Multi-stage Build:**
```dockerfile
# Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Production stage
FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

#### **3. حذف فایل‌های غیرضروری:**
```dockerfile
FROM node:16-alpine

WORKDIR /app

# کپی فایل‌های وابستگی
COPY package*.json ./

# نصب وابستگی‌ها
RUN npm ci --only=production && \
    npm cache clean --force && \
    rm -rf /tmp/* /var/cache/apk/*

# کپی کد اپلیکیشن
COPY . .

# حذف فایل‌های غیرضروری
RUN rm -rf tests/ docs/ *.md

EXPOSE 3000
CMD ["npm", "start"]
```

#### **4. استفاده از .dockerignore:**
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
tests/
docs/
*.md
```

### مثال بهینه‌سازی کامل:
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
    rm -rf /tmp/* /var/cache/apk/*

# کپی کد اپلیکیشن
COPY . .

# حذف فایل‌های غیرضروری
RUN rm -rf tests/ docs/ *.md

# تغییر مالکیت
RUN chown -R nextjs:nodejs /app
USER nextjs

# تعریف پورت
EXPOSE 3000

# دستور پیش‌فرض
CMD ["npm", "start"]
```

## 22.3 Build Performance

بهینه‌سازی عملکرد build برای کاهش زمان ساخت.

### تکنیک‌های بهینه‌سازی Build:

#### **1. بهینه‌سازی ترتیب دستورات:**
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

#### **2. استفاده از BuildKit:**
```bash
# فعال‌سازی BuildKit
export DOCKER_BUILDKIT=1

# ساخت با BuildKit
docker build -t my-app:latest .
```

#### **3. Cache Mounts:**
```dockerfile
# syntax=docker/dockerfile:1
FROM node:16-alpine

WORKDIR /app

# Cache mount برای npm
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

# Cache mount برای apt
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y curl

COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

#### **4. Parallel Builds:**
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.web
    ports:
      - "3000:3000"

  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"

  worker:
    build:
      context: .
      dockerfile: Dockerfile.worker
```

### Build Optimization Script:
```bash
#!/bin/bash
# build-optimize.sh

echo "=== Docker Build Optimization ==="

echo "1. Enabling BuildKit..."
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

echo "2. Building with cache..."
docker build \
  --cache-from my-app:latest \
  --cache-to my-app:build \
  -t my-app:latest .

echo "3. Building with parallel jobs..."
docker build \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  -t my-app:latest .

echo "4. Building with multi-stage..."
docker build \
  --target production \
  -t my-app:latest .

echo "Build optimization completed!"
```

## 22.4 Runtime Performance

بهینه‌سازی عملکرد runtime کانتینرها.

### تکنیک‌های بهینه‌سازی Runtime:

#### **1. بهینه‌سازی JVM:**
```yaml
version: '3.8'
services:
  app:
    image: openjdk:11-jre-slim
    environment:
      - JAVA_OPTS=-Xms512m -Xmx1024m -XX:+UseG1GC -XX:MaxGCPauseMillis=200
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

#### **2. بهینه‌سازی Node.js:**
```yaml
version: '3.8'
services:
  app:
    image: node:16-alpine
    environment:
      - NODE_ENV=production
      - NODE_OPTIONS=--max-old-space-size=1024
      - UV_THREADPOOL_SIZE=4
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

#### **3. بهینه‌سازی Python:**
```yaml
version: '3.8'
services:
  app:
    image: python:3.9-slim
    environment:
      - PYTHONUNBUFFERED=1
      - PYTHONDONTWRITEBYTECODE=1
      - PYTHONHASHSEED=random
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

### Runtime Optimization Script:
```bash
#!/bin/bash
# runtime-optimize.sh

echo "=== Docker Runtime Optimization ==="

echo "1. Setting CPU limits..."
docker run -d --cpus="2.0" nginx

echo "2. Setting memory limits..."
docker run -d --memory="1g" nginx

echo "3. Setting ulimits..."
docker run -d --ulimit nofile=65535:65535 nginx

echo "4. Setting sysctls..."
docker run -d --sysctl net.core.somaxconn=65535 nginx

echo "5. Setting security options..."
docker run -d --security-opt no-new-privileges nginx

echo "Runtime optimization completed!"
```

## 22.5 Network Performance

بهینه‌سازی عملکرد شبکه در Docker.

### تکنیک‌های بهینه‌سازی شبکه:

#### **1. بهینه‌سازی Bridge Network:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    networks:
      - web-network
    ports:
      - "80:80"

networks:
  web-network:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.enable_icc: "true"
      com.docker.network.bridge.enable_ip_masquerade: "true"
      com.docker.network.bridge.host_binding_ipv4: "0.0.0.0"
      com.docker.network.driver.mtu: "1500"
```

#### **2. استفاده از Host Network:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    network_mode: host
```

#### **3. بهینه‌سازی TCP:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    sysctls:
      - net.core.somaxconn=65535
      - net.ipv4.tcp_max_syn_backlog=65535
      - net.ipv4.tcp_keepalive_time=600
      - net.ipv4.tcp_keepalive_intvl=60
      - net.ipv4.tcp_keepalive_probes=3
    ports:
      - "80:80"
```

### Network Optimization Script:
```bash
#!/bin/bash
# network-optimize.sh

echo "=== Docker Network Optimization ==="

echo "1. Creating optimized network..."
docker network create \
  --driver bridge \
  --opt com.docker.network.bridge.enable_icc=true \
  --opt com.docker.network.bridge.enable_ip_masquerade=true \
  --opt com.docker.network.driver.mtu=1500 \
  web-network

echo "2. Setting TCP parameters..."
echo 'net.core.somaxconn = 65535' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_max_syn_backlog = 65535' >> /etc/sysctl.conf
echo 'net.ipv4.tcp_keepalive_time = 600' >> /etc/sysctl.conf
sysctl -p

echo "3. Testing network performance..."
docker run --rm --network web-network nginx:alpine \
  sh -c "time wget -q -O /dev/null http://web:80"

echo "Network optimization completed!"
```

## 22.6 Storage Performance

بهینه‌سازی عملکرد storage در Docker.

### تکنیک‌های بهینه‌سازی Storage:

#### **1. استفاده از SSD:**
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    volumes:
      - /ssd/postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: password
```

#### **2. بهینه‌سازی Volume:**
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: password
    command: |
      postgres
      -c shared_buffers=256MB
      -c effective_cache_size=1GB
      -c maintenance_work_mem=64MB
      -c checkpoint_completion_target=0.9
      -c wal_buffers=16MB
      -c default_statistics_target=100

volumes:
  postgres-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /ssd/postgres-data
```

#### **3. استفاده از tmpfs:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    tmpfs:
      - /tmp
      - /var/cache/nginx
    ports:
      - "80:80"
```

### Storage Optimization Script:
```bash
#!/bin/bash
# storage-optimize.sh

echo "=== Docker Storage Optimization ==="

echo "1. Creating optimized volume..."
docker volume create \
  --driver local \
  --opt type=tmpfs \
  --opt device=tmpfs \
  --opt o=size=1g \
  tmp-volume

echo "2. Setting up SSD mount..."
sudo mkdir -p /ssd/docker-data
sudo mount -t tmpfs -o size=10G tmpfs /ssd/docker-data

echo "3. Moving Docker data to SSD..."
sudo systemctl stop docker
sudo mv /var/lib/docker /ssd/docker-data/
sudo ln -s /ssd/docker-data/docker /var/lib/docker
sudo systemctl start docker

echo "4. Testing storage performance..."
docker run --rm -v tmp-volume:/data alpine \
  sh -c "dd if=/dev/zero of=/data/test bs=1M count=100"

echo "Storage optimization completed!"
```

## 22.7 Memory Optimization

بهینه‌سازی استفاده از حافظه در کانتینرها.

### تکنیک‌های بهینه‌سازی حافظه:

#### **1. محدود کردن حافظه:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    environment:
      - NGINX_WORKER_PROCESSES=2
      - NGINX_WORKER_CONNECTIONS=1024
```

#### **2. بهینه‌سازی JVM:**
```yaml
version: '3.8'
services:
  app:
    image: openjdk:11-jre-slim
    environment:
      - JAVA_OPTS=-Xms256m -Xmx512m -XX:+UseG1GC -XX:MaxGCPauseMillis=200
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

#### **3. بهینه‌سازی Node.js:**
```yaml
version: '3.8'
services:
  app:
    image: node:16-alpine
    environment:
      - NODE_ENV=production
      - NODE_OPTIONS=--max-old-space-size=512
      - UV_THREADPOOL_SIZE=2
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
```

### Memory Optimization Script:
```bash
#!/bin/bash
# memory-optimize.sh

echo "=== Docker Memory Optimization ==="

echo "1. Setting memory limits..."
docker run -d --memory="512m" --memory-swap="1g" nginx

echo "2. Setting memory reservation..."
docker run -d --memory-reservation="256m" nginx

echo "3. Setting OOM killer..."
docker run -d --oom-kill-disable nginx

echo "4. Monitoring memory usage..."
docker stats --no-stream

echo "5. Setting swap limits..."
docker run -d --memory="512m" --memory-swap="1g" nginx

echo "Memory optimization completed!"
```

## 22.8 CPU Optimization

بهینه‌سازی استفاده از CPU در کانتینرها.

### تکنیک‌های بهینه‌سازی CPU:

#### **1. محدود کردن CPU:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      resources:
        limits:
          cpus: '2.0'
        reservations:
          cpus: '1.0'
    cpuset: "0,1"  # استفاده از CPU cores خاص
```

#### **2. بهینه‌سازی Thread Pool:**
```yaml
version: '3.8'
services:
  app:
    image: node:16-alpine
    environment:
      - UV_THREADPOOL_SIZE=4
      - NODE_ENV=production
    deploy:
      resources:
        limits:
          cpus: '2.0'
        reservations:
          cpus: '1.0'
```

#### **3. بهینه‌سازی Java:**
```yaml
version: '3.8'
services:
  app:
    image: openjdk:11-jre-slim
    environment:
      - JAVA_OPTS=-XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:+UseStringDeduplication
    deploy:
      resources:
        limits:
          cpus: '2.0'
        reservations:
          cpus: '1.0'
```

### CPU Optimization Script:
```bash
#!/bin/bash
# cpu-optimize.sh

echo "=== Docker CPU Optimization ==="

echo "1. Setting CPU limits..."
docker run -d --cpus="2.0" nginx

echo "2. Setting CPU shares..."
docker run -d --cpu-shares=512 nginx

echo "3. Setting CPU period and quota..."
docker run -d --cpu-period=100000 --cpu-quota=200000 nginx

echo "4. Setting CPU affinity..."
docker run -d --cpuset-cpus="0,1" nginx

echo "5. Monitoring CPU usage..."
docker stats --no-stream

echo "CPU optimization completed!"
```

## 22.9 I/O Optimization

بهینه‌سازی I/O در کانتینرها.

### تکنیک‌های بهینه‌سازی I/O:

#### **1. بهینه‌سازی Database:**
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: password
    command: |
      postgres
      -c shared_buffers=256MB
      -c effective_cache_size=1GB
      -c maintenance_work_mem=64MB
      -c checkpoint_completion_target=0.9
      -c wal_buffers=16MB
      -c default_statistics_target=100
      -c random_page_cost=1.1
      -c effective_io_concurrency=200

volumes:
  postgres-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /ssd/postgres-data
```

#### **2. بهینه‌سازی Nginx:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
```

### فایل nginx.conf:
```nginx
events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
    open_file_cache max=1000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;
}
```

### I/O Optimization Script:
```bash
#!/bin/bash
# io-optimize.sh

echo "=== Docker I/O Optimization ==="

echo "1. Setting I/O limits..."
docker run -d --device-read-bps /dev/sda:1mb --device-write-bps /dev/sda:1mb nginx

echo "2. Setting I/O weight..."
docker run -d --blkio-weight=500 nginx

echo "3. Setting I/O device weight..."
docker run -d --blkio-weight-device /dev/sda:500 nginx

echo "4. Monitoring I/O usage..."
docker stats --no-stream

echo "5. Setting I/O scheduler..."
echo mq-deadline > /sys/block/sda/queue/scheduler

echo "I/O optimization completed!"
```

## 22.10 Benchmarking and Testing

تست و benchmark عملکرد کانتینرها.

### ابزارهای Benchmarking:

#### **1. Apache Bench:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"

  ab:
    image: httpd:alpine
    command: ab -n 1000 -c 10 http://web:80/
    depends_on:
      - web
```

#### **2. wrk:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"

  wrk:
    image: williamyeh/wrk
    command: wrk -t12 -c400 -d30s http://web:80/
    depends_on:
      - web
```

#### **3. Custom Benchmark:**
```bash
#!/bin/bash
# benchmark.sh

echo "=== Docker Performance Benchmark ==="

echo "1. Starting test containers..."
docker-compose up -d

echo "2. Waiting for containers to start..."
sleep 10

echo "3. Running CPU benchmark..."
docker run --rm --cpus="1.0" nginx:alpine \
  sh -c "time dd if=/dev/zero of=/dev/null bs=1M count=1000"

echo "4. Running memory benchmark..."
docker run --rm --memory="512m" nginx:alpine \
  sh -c "time dd if=/dev/zero of=/tmp/test bs=1M count=500"

echo "5. Running network benchmark..."
docker run --rm nginx:alpine \
  sh -c "time wget -q -O /dev/null http://web:80"

echo "6. Running I/O benchmark..."
docker run --rm -v /tmp:/data nginx:alpine \
  sh -c "time dd if=/dev/zero of=/data/test bs=1M count=100"

echo "7. Cleaning up..."
docker-compose down

echo "Benchmark completed!"
```

### Performance Monitoring:
```bash
#!/bin/bash
# performance-monitor.sh

echo "=== Docker Performance Monitoring ==="

echo "1. Container Performance:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}"

echo "2. System Performance:"
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1

echo "Memory Usage:"
free -h

echo "Disk Usage:"
df -h

echo "3. Network Performance:"
netstat -tuln
ss -tuln

echo "4. Docker Performance:"
docker system df
docker system events --since 1h | head -20

echo "Performance monitoring completed!"
```

این بخش شما را با تمام جنبه‌های بهینه‌سازی عملکرد Docker آشنا می‌کند.