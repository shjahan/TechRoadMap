# Section 11 – Docker in Development

## 11.1 Development Workflow

Docker در محیط development به توسعه‌دهندگان امکان ایجاد محیط‌های یکسان و قابل تکرار را می‌دهد.

### مزایای Docker در Development:
- **Consistency**: محیط یکسان برای تمام توسعه‌دهندگان
- **Isolation**: جداسازی پروژه‌ها از یکدیگر
- **Portability**: قابلیت حمل بین سیستم‌های مختلف
- **Dependency Management**: مدیریت آسان وابستگی‌ها
- **Quick Setup**: راه‌اندازی سریع محیط development

### Workflow کلی:
```
1. Clone Repository
2. docker-compose up
3. Develop & Test
4. Commit Changes
5. Deploy
```

### مثال عملی:
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
      - ./public:/app/public
    environment:
      - NODE_ENV=development
      - DEBUG=true
    depends_on:
      - db
      - redis

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

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  postgres-dev-data:
```

## 11.2 Local Development Environment

راه‌اندازی محیط development محلی با Docker.

### ساختار پروژه:
```
my-project/
├── docker-compose.yml
├── docker-compose.dev.yml
├── Dockerfile
├── .env
├── src/
├── public/
└── README.md
```

### فایل‌های کلیدی:

#### **Dockerfile:**
```dockerfile
FROM node:16-alpine

WORKDIR /app

# کپی package.json
COPY package*.json ./

# نصب وابستگی‌ها
RUN npm ci

# کپی کد
COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

#### **docker-compose.dev.yml:**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src
      - ./public:/app/public
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DEBUG=true
      - DATABASE_URL=postgres://db:5432/myapp_dev
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
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

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

volumes:
  postgres-dev-data:
```

### دستورات Development:
```bash
# راه‌اندازی محیط development
docker-compose -f docker-compose.dev.yml up

# راه‌اندازی در پس‌زمینه
docker-compose -f docker-compose.dev.yml up -d

# مشاهده لاگ‌ها
docker-compose -f docker-compose.dev.yml logs -f

# توقف محیط
docker-compose -f docker-compose.dev.yml down
```

## 11.3 Code Volume Mounting

نصب کد برای توسعه real-time بدون rebuild کردن کانتینر.

### انواع Volume Mounting:

#### **1. Source Code Mounting:**
```yaml
services:
  web:
    build: .
    volumes:
      - ./src:/app/src
      - ./public:/app/public
      - /app/node_modules  # جلوگیری از override node_modules
```

#### **2. Configuration Mounting:**
```yaml
services:
  web:
    build: .
    volumes:
      - ./config:/app/config:ro
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
```

#### **3. Development Tools Mounting:**
```yaml
services:
  web:
    build: .
    volumes:
      - ./src:/app/src
      - ./tests:/app/tests
      - ./docs:/app/docs
```

### مثال عملی:
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - REACT_APP_API_URL=http://localhost:8000

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/src:/app/src
      - ./backend/tests:/app/tests
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://db:5432/myapp_dev
    depends_on:
      - db

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

## 11.4 Hot Reloading

Hot reloading برای تغییرات real-time در کد بدون restart کردن کانتینر.

### تنظیمات Hot Reloading:

#### **Node.js/Express:**
```yaml
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
```

#### **React:**
```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
      - /app/node_modules
    environment:
      - CHOKIDAR_USEPOLLING=true
      - WATCHPACK_POLLING=true
    command: npm start
```

#### **Vue.js:**
```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "8080:8080"
    volumes:
      - ./frontend/src:/app/src
      - /app/node_modules
    environment:
      - CHOKIDAR_USEPOLLING=true
    command: npm run serve
```

### مثال کامل:
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - CHOKIDAR_USEPOLLING=true
      - REACT_APP_API_URL=http://localhost:8000
    command: npm start

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/src:/app/src
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://db:5432/myapp_dev
    command: npm run dev
    depends_on:
      - db

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

## 11.5 Debugging Containers

عیب‌یابی کانتینرها برای حل مشکلات development.

### روش‌های Debugging:

#### **1. ورود به کانتینر:**
```bash
# ورود به کانتینر
docker exec -it container_name bash

# ورود به کانتینر با shell خاص
docker exec -it container_name sh

# اجرای دستور در کانتینر
docker exec -it container_name ls -la
```

#### **2. مشاهده لاگ‌ها:**
```bash
# لاگ‌های real-time
docker logs -f container_name

# آخرین N خط
docker logs --tail 100 container_name

# لاگ‌های از زمان خاص
docker logs --since "2023-01-01T00:00:00" container_name
```

#### **3. بررسی وضعیت کانتینر:**
```bash
# وضعیت کانتینرها
docker ps

# اطلاعات کامل کانتینر
docker inspect container_name

# آمار منابع
docker stats container_name
```

### مثال عملی:
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

### اسکریپت Debugging:
```bash
#!/bin/bash
# debug.sh

echo "=== Docker Development Debugging ==="

echo "1. Container Status:"
docker ps

echo "2. Container Logs:"
docker logs web

echo "3. Container Resources:"
docker stats --no-stream web

echo "4. Container Network:"
docker network ls
docker network inspect docker_default

echo "5. Container Volumes:"
docker volume ls

echo "6. Entering Container:"
docker exec -it web bash
```

## 11.6 Testing with Docker

تست کردن اپلیکیشن‌ها با Docker برای اطمینان از عملکرد صحیح.

### انواع تست‌ها:

#### **1. Unit Tests:**
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

#### **2. Integration Tests:**
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
      - DATABASE_URL=postgres://test-db:5432/myapp_test
    command: npm run test:integration
    depends_on:
      - test-db

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

#### **3. E2E Tests:**
```yaml
version: '3.8'
services:
  e2e:
    build: .
    volumes:
      - ./src:/app/src
      - ./tests:/app/tests
      - /app/node_modules
    environment:
      - NODE_ENV=test
      - BASE_URL=http://web:3000
    command: npm run test:e2e
    depends_on:
      - web
      - db

  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=test
      - DATABASE_URL=postgres://db:5432/myapp_test
    depends_on:
      - db

  db:
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

### اسکریپت تست:
```bash
#!/bin/bash
# test.sh

echo "Running tests with Docker..."

# Unit tests
echo "1. Running unit tests..."
docker-compose -f docker-compose.test.yml run --rm test npm test

# Integration tests
echo "2. Running integration tests..."
docker-compose -f docker-compose.test.yml run --rm test npm run test:integration

# E2E tests
echo "3. Running E2E tests..."
docker-compose -f docker-compose.test.yml run --rm e2e npm run test:e2e

# Cleanup
echo "4. Cleaning up..."
docker-compose -f docker-compose.test.yml down -v

echo "Tests completed!"
```

## 11.7 CI/CD Integration

ادغام Docker با CI/CD pipeline برای خودکارسازی فرآیند development.

### GitHub Actions:
```yaml
# .github/workflows/ci.yml
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
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Build and test
      run: |
        docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
        docker-compose -f docker-compose.test.yml down -v
    
    - name: Run tests
      run: |
        docker-compose -f docker-compose.test.yml run --rm test npm test
        docker-compose -f docker-compose.test.yml run --rm test npm run test:integration

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t my-app:${{ github.sha }} .
        docker build -t my-app:latest .
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push my-app:${{ github.sha }}
        docker push my-app:latest
```

### GitLab CI/CD:
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

services:
  - docker:dind

test:
  stage: test
  script:
    - docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
    - docker-compose -f docker-compose.test.yml down -v
  only:
    - merge_requests
    - main

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker build -t $CI_REGISTRY_IMAGE:latest .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main

deploy:
  stage: deploy
  script:
    - docker-compose -f docker-compose.prod.yml up -d
  only:
    - main
```

## 11.8 Development Tools

ابزارهای مفید برای development با Docker.

### ابزارهای کلیدی:

#### **1. Docker Desktop:**
- رابط گرافیکی
- مدیریت کانتینرها و ایمیج‌ها
- نظارت بر منابع
- تنظیمات پیشرفته

#### **2. Portainer:**
```yaml
version: '3.8'
services:
  portainer:
    image: portainer/portainer-ce
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer-data:/data
    restart: unless-stopped

volumes:
  portainer-data:
```

#### **3. Watchtower (Auto-update):**
```yaml
version: '3.8'
services:
  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=300
    restart: unless-stopped
```

#### **4. Development Database Admin:**
```yaml
version: '3.8'
services:
  pgadmin:
    image: dpage/pgadmin4
    ports:
      - "5050:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp_dev
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpassword
    volumes:
      - postgres-dev-data:/var/lib/postgresql/data

volumes:
  postgres-dev-data:
```

## 11.9 IDE Integration

ادغام Docker با IDEها برای development بهتر.

### VS Code:

#### **Extensions:**
- Docker
- Remote - Containers
- Docker Compose

#### **Settings:**
```json
{
  "docker.defaultRegistryPath": "localhost:5000",
  "docker.showStartPage": false,
  "docker.containers.sortBy": "CreatedTime",
  "docker.containers.sortOrder": "Desc"
}
```

#### **Dev Container:**
```json
{
  "name": "Node.js Development",
  "dockerComposeFile": "docker-compose.dev.yml",
  "service": "web",
  "workspaceFolder": "/app",
  "shutdownAction": "stopCompose"
}
```

### IntelliJ IDEA:

#### **Docker Plugin:**
- Docker integration
- Docker Compose support
- Container management
- Image management

#### **Run Configuration:**
```yaml
# Run Configuration
Type: Docker Compose
Compose file: docker-compose.dev.yml
Service: web
Command: npm run dev
```

## 11.10 Development Best Practices

بهترین روش‌های development با Docker.

### نکات مهم:

#### **1. استفاده از .dockerignore:**
```dockerignore
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.nyc_output
coverage
.nyc_output
.vscode
.idea
```

#### **2. بهینه‌سازی Dockerfile:**
```dockerfile
FROM node:16-alpine

WORKDIR /app

# کپی package.json اول
COPY package*.json ./

# نصب وابستگی‌ها
RUN npm ci --only=production

# کپی کد
COPY . .

# ایجاد کاربر غیر root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs

EXPOSE 3000

CMD ["npm", "start"]
```

#### **3. مدیریت Environment:**
```yaml
version: '3.8'
services:
  web:
    build: .
    environment:
      - NODE_ENV=${NODE_ENV:-development}
      - PORT=${PORT:-3000}
      - DATABASE_URL=${DATABASE_URL}
    env_file:
      - .env
```

#### **4. استفاده از Health Checks:**
```yaml
version: '3.8'
services:
  web:
    build: .
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

#### **5. مدیریت Volumeها:**
```yaml
version: '3.8'
services:
  web:
    build: .
    volumes:
      - ./src:/app/src
      - /app/node_modules
      - app-logs:/app/logs

volumes:
  app-logs:
```

### اسکریپت Development:
```bash
#!/bin/bash
# dev.sh

echo "Starting development environment..."

# بررسی وجود فایل‌های لازم
if [ ! -f "docker-compose.dev.yml" ]; then
  echo "Error: docker-compose.dev.yml not found"
  exit 1
fi

# راه‌اندازی محیط development
docker-compose -f docker-compose.dev.yml up --build

# Cleanup on exit
trap 'docker-compose -f docker-compose.dev.yml down' EXIT
```

این بخش شما را با تمام جنبه‌های استفاده از Docker در محیط development آشنا می‌کند.