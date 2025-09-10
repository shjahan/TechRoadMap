# Section 7 – Docker Compose

## 7.1 Docker Compose Overview

Docker Compose ابزاری برای تعریف و اجرای اپلیکیشن‌های چندکانتینری Docker است. با استفاده از فایل YAML، می‌توانید سرویس‌ها، شبکه‌ها و volumeهای مورد نیاز را تعریف کنید.

### ویژگی‌های کلیدی:
- **Multi-container Applications**: مدیریت اپلیکیشن‌های چندکانتینری
- **YAML Configuration**: تنظیمات ساده و خوانا
- **Service Dependencies**: مدیریت وابستگی‌ها
- **Environment Management**: مدیریت محیط‌های مختلف
- **Scaling**: مقیاس‌دهی آسان سرویس‌ها

### مزایای Docker Compose:
- **Simplicity**: سادگی در تعریف و اجرا
- **Reproducibility**: قابلیت تکرار در محیط‌های مختلف
- **Development**: مناسب برای محیط development
- **Testing**: آسان برای تست‌های integration

### مثال پایه:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
```

### نصب Docker Compose:
```bash
# نصب Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# بررسی نصب
docker-compose --version
```

## 7.2 Compose File Syntax

فایل Docker Compose از syntax YAML استفاده می‌کند و شامل بخش‌های مختلفی است.

### ساختار کلی فایل:
```yaml
version: '3.8'  # نسخه Compose

services:        # تعریف سرویس‌ها
  service1:
    # تنظیمات سرویس
  service2:
    # تنظیمات سرویس

networks:        # تعریف شبکه‌ها
  network1:
    # تنظیمات شبکه

volumes:         # تعریف volumeها
  volume1:
    # تنظیمات volume
```

### نسخه‌های Compose:
- **1.x**: نسخه قدیمی (deprecated)
- **2.x**: نسخه فعلی (پیشنهادی)
- **3.x**: نسخه جدید (Docker Swarm)

### مثال کامل:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

networks:
  app-network:
    driver: bridge

volumes:
  postgres-data:
```

## 7.3 Service Definition

تعریف سرویس‌ها بخش اصلی فایل Docker Compose است.

### فیلدهای کلیدی سرویس:

#### **image:**
```yaml
services:
  web:
    image: nginx:alpine
    # یا
    image: my-app:latest
```

#### **build:**
```yaml
services:
  web:
    build: .
    # یا
    build:
      context: .
      dockerfile: Dockerfile.prod
      args:
        - NODE_ENV=production
```

#### **ports:**
```yaml
services:
  web:
    ports:
      - "80:80"
      - "443:443"
    # یا
    ports:
      - "3000-3005:3000-3005"
```

#### **environment:**
```yaml
services:
  web:
    environment:
      - NODE_ENV=production
      - PORT=3000
    # یا
    environment:
      NODE_ENV: production
      PORT: 3000
```

### مثال کامل سرویس:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db:5432/myapp
    volumes:
      - ./src:/app/src
      - app-logs:/app/logs
    depends_on:
      - db
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 7.4 Network Configuration

تنظیمات شبکه در Docker Compose برای ارتباط بین سرویس‌ها ضروری است.

### انواع شبکه‌ها:

#### **Default Network:**
```yaml
version: '3.8'
services:
  web:
    image: nginx
  db:
    image: postgres
# سرویس‌ها در همان شبکه پیش‌فرض قرار می‌گیرند
```

#### **Custom Network:**
```yaml
version: '3.8'
services:
  web:
    image: nginx
    networks:
      - frontend
  db:
    image: postgres
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

#### **External Network:**
```yaml
version: '3.8'
services:
  web:
    image: nginx
    networks:
      - existing-network

networks:
  existing-network:
    external: true
```

### مثال عملی:
```yaml
version: '3.8'
services:
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    networks:
      - frontend-network

  backend:
    image: node-api:latest
    networks:
      - frontend-network
      - backend-network
    environment:
      - DATABASE_URL=postgres://db:5432/myapp

  db:
    image: postgres:13
    networks:
      - backend-network
    environment:
      POSTGRES_PASSWORD: password

networks:
  frontend-network:
    driver: bridge
  backend-network:
    driver: bridge
    internal: true
```

## 7.5 Volume Configuration

تنظیمات volume برای مدیریت داده‌های دائمی ضروری است.

### انواع Volumeها:

#### **Named Volumes:**
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

#### **Bind Mounts:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./html:/usr/share/nginx/html:ro
```

#### **External Volumes:**
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
    external: true
```

### مثال عملی:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./html:/usr/share/nginx/html:ro
      - nginx-logs:/var/log/nginx

  app:
    image: my-app:latest
    volumes:
      - app-data:/app/data
      - ./src:/app/src
    environment:
      - DATABASE_URL=postgres://db:5432/myapp

  db:
    image: postgres:13
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: password

volumes:
  postgres-data:
  app-data:
  nginx-logs:
```

## 7.6 Environment Variables

مدیریت متغیرهای محیطی برای پیکربندی سرویس‌ها ضروری است.

### روش‌های تعریف متغیرهای محیطی:

#### **1. در فایل Compose:**
```yaml
version: '3.8'
services:
  web:
    image: my-app:latest
    environment:
      - NODE_ENV=production
      - PORT=3000
      - DATABASE_URL=postgres://db:5432/myapp
```

#### **2. از فایل .env:**
```yaml
version: '3.8'
services:
  web:
    image: my-app:latest
    env_file:
      - .env
      - .env.production
```

#### **3. از متغیرهای سیستم:**
```yaml
version: '3.8'
services:
  web:
    image: my-app:latest
    environment:
      - NODE_ENV=${NODE_ENV}
      - PORT=${PORT:-3000}
```

### فایل .env:
```env
NODE_ENV=production
PORT=3000
DATABASE_URL=postgres://db:5432/myapp
REDIS_URL=redis://redis:6379
```

### مثال عملی:
```yaml
version: '3.8'
services:
  web:
    image: my-app:latest
    ports:
      - "${PORT:-3000}:3000"
    environment:
      - NODE_ENV=${NODE_ENV:-development}
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    env_file:
      - .env
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-myapp}
      POSTGRES_USER: ${POSTGRES_USER:-user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    environment:
      REDIS_PASSWORD: ${REDIS_PASSWORD}

volumes:
  postgres-data:
```

## 7.7 Service Dependencies

مدیریت وابستگی‌ها برای اجرای صحیح سرویس‌ها ضروری است.

### انواع وابستگی‌ها:

#### **depends_on:**
```yaml
version: '3.8'
services:
  web:
    image: nginx
    depends_on:
      - app
  app:
    image: my-app:latest
    depends_on:
      - db
  db:
    image: postgres:13
```

#### **condition:**
```yaml
version: '3.8'
services:
  web:
    image: nginx
    depends_on:
      app:
        condition: service_healthy
  app:
    image: my-app:latest
    depends_on:
      db:
        condition: service_started
  db:
    image: postgres:13
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### مثال عملی:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      app:
        condition: service_healthy
    networks:
      - frontend

  app:
    image: my-app:latest
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    environment:
      - DATABASE_URL=postgres://db:5432/myapp
      - REDIS_URL=redis://redis:6379
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:alpine
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

volumes:
  postgres-data:
```

## 7.8 Scaling Services

مقیاس‌دهی سرویس‌ها برای مدیریت بار و بهبود عملکرد ضروری است.

### روش‌های مقیاس‌دهی:

#### **1. با دستور scale:**
```bash
# مقیاس‌دهی سرویس
docker-compose up --scale web=3

# مقیاس‌دهی چندین سرویس
docker-compose up --scale web=3 --scale worker=2
```

#### **2. در فایل Compose:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      replicas: 3
    ports:
      - "80:80"
```

#### **3. با Docker Swarm:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    ports:
      - "80:80"
```

### مثال عملی:

#### **Load Balanced Web Application:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app

  app:
    image: my-app:latest
    environment:
      - NODE_ENV=production
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

#### **فایل nginx.conf:**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server app:3000;
    }
    
    server {
        listen 80;
        location / {
            proxy_pass http://app;
        }
    }
}
```

#### **اجرای مقیاس‌دهی:**
```bash
# مقیاس‌دهی اپلیکیشن
docker-compose up --scale app=3

# مقیاس‌دهی با load balancer
docker-compose up --scale app=3 --scale web=1
```

## 7.9 Compose Override Files

فایل‌های override برای تنظیمات مختلف محیط‌ها استفاده می‌شوند.

### انواع فایل‌های Override:

#### **1. docker-compose.override.yml (پیش‌فرض):**
```yaml
# docker-compose.override.yml
version: '3.8'
services:
  web:
    ports:
      - "8080:80"  # override پورت
    environment:
      - DEBUG=true
```

#### **2. فایل‌های محیط خاص:**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  web:
    environment:
      - NODE_ENV=production
    restart: always
  db:
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```

#### **3. فایل‌های توسعه:**
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  web:
    volumes:
      - ./src:/app/src
    environment:
      - NODE_ENV=development
      - DEBUG=true
```

### استفاده از فایل‌های Override:

```bash
# استفاده از فایل override پیش‌فرض
docker-compose up

# استفاده از فایل خاص
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

# استفاده از چندین فایل
docker-compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.debug.yml up
```

### مثال عملی:

#### **فایل اصلی (docker-compose.yml):**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
```

#### **فایل Development (docker-compose.dev.yml):**
```yaml
version: '3.8'
services:
  web:
    ports:
      - "3000:80"
    environment:
      - NODE_ENV=development
      - DEBUG=true
    volumes:
      - ./nginx.dev.conf:/etc/nginx/nginx.conf:ro
  db:
    environment:
      POSTGRES_PASSWORD: devpassword
    ports:
      - "5432:5432"
```

#### **فایل Production (docker-compose.prod.yml):**
```yaml
version: '3.8'
services:
  web:
    restart: always
    environment:
      - NODE_ENV=production
  db:
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

## 7.10 Production Considerations

ملاحظات production برای استقرار امن و پایدار ضروری است.

### نکات مهم Production:

#### **1. Security:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    user: "1000:1000"  # اجرا با کاربر غیر root
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
    security_opt:
      - no-new-privileges:true
```

#### **2. Resource Limits:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

#### **3. Health Checks:**
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

#### **4. Logging:**
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

### مثال کامل Production:

#### **docker-compose.prod.yml:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
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

  app:
    image: my-app:latest
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db:5432/myapp
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: json-file
      options:
        max-size: "50m"
        max-file: "5"
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./postgres.conf:/etc/postgresql/postgresql.conf:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: json-file
      options:
        max-size: "100m"
        max-file: "3"
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M

networks:
  default:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

volumes:
  postgres-data:
```

### اسکریپت Production:
```bash
#!/bin/bash
# deploy.sh

echo "Deploying to production..."

# بررسی متغیرهای محیطی
if [ -z "$POSTGRES_PASSWORD" ]; then
  echo "Error: POSTGRES_PASSWORD is not set"
  exit 1
fi

# اجرای production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# بررسی وضعیت
docker-compose ps

echo "Deployment completed!"
```

این بخش شما را با تمام جنبه‌های Docker Compose آشنا می‌کند.