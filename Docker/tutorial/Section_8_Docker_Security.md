# Section 8 – Docker Security

## 8.1 Container Security Fundamentals

امنیت کانتینرها برای محافظت از اپلیکیشن‌ها و داده‌ها ضروری است. درک اصول امنیت کانتینرها اولین قدم برای ایجاد محیط امن است.

### اصول امنیت کانتینر:

#### **1. Isolation (جداسازی)**
- کانتینرها باید از یکدیگر جدا باشند
- محدود کردن دسترسی به منابع سیستم
- استفاده از namespaceها و cgroups

#### **2. Least Privilege (حداقل دسترسی)**
- اجرای کانتینرها با کمترین دسترسی ممکن
- استفاده از کاربران غیر root
- محدود کردن capabilities

#### **3. Defense in Depth (دفاع چندلایه)**
- امنیت در تمام سطوح
- شبکه، ایمیج، runtime، host
- نظارت و logging

### مثال عملی:

#### **کانتینر امن:**
```dockerfile
FROM node:16-alpine

# ایجاد کاربر غیر root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# تنظیم متغیرهای محیطی
ENV NODE_ENV=production

# دایرکتوری کاری
WORKDIR /app

# کپی فایل‌ها
COPY package*.json ./
RUN npm ci --only=production

COPY . .

# تغییر مالکیت
RUN chown -R nextjs:nodejs /app
USER nextjs

# تعریف پورت
EXPOSE 3000

# دستور پیش‌فرض
CMD ["npm", "start"]
```

#### **اجرای امن:**
```bash
# اجرای کانتینر با محدودیت‌های امنیتی
docker run -d \
  --name secure-app \
  --user 1001:1001 \
  --read-only \
  --tmpfs /tmp \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --security-opt no-new-privileges:true \
  --memory=512m \
  --cpus="1.0" \
  my-app:latest
```

## 8.2 Image Security Scanning

اسکن امنیتی ایمیج‌ها برای شناسایی آسیب‌پذیری‌ها ضروری است.

### ابزارهای اسکن امنیتی:

#### **1. Docker Scan:**
```bash
# اسکن ایمیج
docker scan my-image:latest

# اسکن با خروجی JSON
docker scan --json my-image:latest

# اسکن با فیلتر
docker scan --severity high my-image:latest
```

#### **2. Trivy:**
```bash
# نصب Trivy
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh

# اسکن ایمیج
trivy image my-image:latest

# اسکن با خروجی JSON
trivy image --format json my-image:latest

# اسکن با فیلتر شدت
trivy image --severity HIGH,CRITICAL my-image:latest
```

#### **3. Clair:**
```bash
# اجرای Clair
docker run -d --name clair-db arminc/clair-db
docker run -d --name clair --link clair-db:postgres arminc/clair-local

# اسکن ایمیج
clair-scanner --ip clair my-image:latest
```

### مثال عملی:

#### **اسکن خودکار در CI/CD:**
```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build image
        run: docker build -t my-app:latest .
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'my-app:latest'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v1
        with:
          sarif_file: 'trivy-results.sarif'
```

#### **اسکن محلی:**
```bash
#!/bin/bash
# security-scan.sh

echo "Starting security scan..."

# اسکن با Trivy
trivy image --severity HIGH,CRITICAL my-app:latest

# اسکن با Docker Scan
docker scan my-app:latest

# اسکن با Snyk
snyk container test my-app:latest

echo "Security scan completed!"
```

## 8.3 Runtime Security

امنیت runtime برای محافظت از کانتینرها در حین اجرا ضروری است.

### اصول Runtime Security:

#### **1. Resource Limits:**
```bash
# محدودیت حافظه
docker run -m 512m my-app

# محدودیت CPU
docker run --cpus="1.0" my-app

# محدودیت I/O
docker run --device-read-bps /dev/sda:1mb my-app
```

#### **2. Capabilities:**
```bash
# حذف تمام capabilities
docker run --cap-drop=ALL my-app

# اضافه کردن capabilities مورد نیاز
docker run --cap-add=NET_BIND_SERVICE my-app
```

#### **3. Read-only Filesystem:**
```bash
# فایل سیستم فقط خواندنی
docker run --read-only my-app

# با tmpfs برای فایل‌های موقت
docker run --read-only --tmpfs /tmp my-app
```

### مثال عملی:

#### **کانتینر امن:**
```bash
# اجرای کانتینر با امنیت بالا
docker run -d \
  --name secure-app \
  --user 1001:1001 \
  --read-only \
  --tmpfs /tmp \
  --tmpfs /var/cache/nginx \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --security-opt no-new-privileges:true \
  --memory=512m \
  --cpus="1.0" \
  --device-read-bps /dev/sda:1mb \
  --device-write-bps /dev/sda:1mb \
  nginx:alpine
```

#### **Docker Compose امن:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.5'
```

## 8.4 Network Security

امنیت شبکه برای محافظت از ترافیک کانتینرها ضروری است.

### اصول Network Security:

#### **1. Network Isolation:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    networks:
      - frontend
  
  api:
    image: my-api:latest
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
    internal: true  # بدون دسترسی به اینترنت
```

#### **2. Firewall Rules:**
```bash
# محدود کردن دسترسی پورت
docker run -p 127.0.0.1:80:80 nginx

# استفاده از iptables
sudo iptables -A DOCKER -d 172.17.0.0/16 -j ACCEPT
sudo iptables -A DOCKER -d 172.17.0.0/16 -p tcp --dport 5432 -j DROP
```

#### **3. TLS/SSL:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./ssl:/etc/nginx/ssl:ro
    environment:
      - SSL_CERT=/etc/nginx/ssl/cert.pem
      - SSL_KEY=/etc/nginx/ssl/key.pem
```

### مثال عملی:

#### **شبکه امن:**
```yaml
version: '3.8'
services:
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    networks:
      - frontend
    volumes:
      - ./ssl:/etc/nginx/ssl:ro
  
  api:
    image: my-api:latest
    networks:
      - frontend
      - backend
    environment:
      - DATABASE_URL=postgres://db:5432/myapp
  
  db:
    image: postgres:13
    networks:
      - backend
    environment:
      POSTGRES_PASSWORD: password

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

## 8.5 Secrets Management

مدیریت secrets برای محافظت از اطلاعات حساس ضروری است.

### روش‌های مدیریت Secrets:

#### **1. Docker Secrets:**
```bash
# ایجاد secret
echo "mysecretpassword" | docker secret create db_password -

# استفاده از secret
docker service create \
  --name postgres \
  --secret db_password \
  postgres:13
```

#### **2. Environment Variables:**
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    external: true
```

#### **3. External Secret Management:**
```yaml
version: '3.8'
services:
  app:
    image: my-app:latest
    environment:
      - VAULT_ADDR=https://vault.example.com
      - VAULT_TOKEN=${VAULT_TOKEN}
    volumes:
      - ./vault-agent.hcl:/vault/config/vault-agent.hcl:ro
```

### مثال عملی:

#### **استفاده از Docker Secrets:**
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
      POSTGRES_USER_FILE: /run/secrets/db_user
    secrets:
      - db_password
      - db_user
    networks:
      - backend

  app:
    image: my-app:latest
    environment:
      DATABASE_URL: postgres://$(cat /run/secrets/db_user):$(cat /run/secrets/db_password)@db:5432/myapp
    secrets:
      - db_password
      - db_user
    networks:
      - frontend
      - backend

secrets:
  db_password:
    external: true
  db_user:
    external: true

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

#### **ایجاد Secrets:**
```bash
#!/bin/bash
# create-secrets.sh

echo "Creating secrets..."

# ایجاد secrets
echo "mysecretpassword" | docker secret create db_password -
echo "myuser" | docker secret create db_user -

# بررسی secrets
docker secret ls

echo "Secrets created successfully!"
```

## 8.6 User Namespaces

User Namespaces برای جداسازی کاربران کانتینرها از سیستم میزبان ضروری است.

### فعال‌سازی User Namespaces:

#### **1. تنظیم Docker Daemon:**
```json
{
  "userns-remap": "default"
}
```

#### **2. ایجاد کاربر mapping:**
```bash
# ایجاد فایل subuid
echo "1000:100000:65536" >> /etc/subuid
echo "1000:100000:65536" >> /etc/subgid

# راه‌اندازی مجدد Docker
sudo systemctl restart docker
```

### مثال عملی:

#### **کانتینر با User Namespace:**
```bash
# اجرای کانتینر با user namespace
docker run --user 1000:1000 nginx:alpine

# بررسی mapping
docker run --user 1000:1000 nginx:alpine id
```

#### **Docker Compose با User Namespace:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    user: "1000:1000"
    ports:
      - "80:80"
  
  app:
    image: my-app:latest
    user: "1000:1000"
    environment:
      - NODE_ENV=production
```

## 8.7 Capabilities and Privileges

مدیریت capabilities و privileges برای محدود کردن دسترسی کانتینرها ضروری است.

### انواع Capabilities:

#### **1. Capabilities مهم:**
- **NET_BIND_SERVICE**: اتصال به پورت‌های زیر 1024
- **SYS_ADMIN**: دسترسی‌های مدیریتی
- **DAC_OVERRIDE**: دور زدن permissionها
- **SETUID**: تغییر UID

#### **2. مدیریت Capabilities:**
```bash
# حذف تمام capabilities
docker run --cap-drop=ALL nginx

# اضافه کردن capabilities مورد نیاز
docker run --cap-add=NET_BIND_SERVICE nginx

# حذف capabilities خاص
docker run --cap-drop=SYS_ADMIN nginx
```

### مثال عملی:

#### **کانتینر با Capabilities محدود:**
```bash
# اجرای nginx با capabilities محدود
docker run -d \
  --name nginx \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --cap-add=SETGID \
  --cap-add=SETUID \
  nginx:alpine
```

#### **Docker Compose با Capabilities:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
      - SETGID
      - SETUID
    ports:
      - "80:80"
  
  app:
    image: my-app:latest
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    user: "1000:1000"
```

## 8.8 Security Best Practices

بهترین روش‌های امنیتی برای محافظت از کانتینرها ضروری است.

### بهترین روش‌ها:

#### **1. Image Security:**
```dockerfile
# استفاده از ایمیج‌های رسمی و به‌روز
FROM node:16-alpine

# اجرا با کاربر غیر root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs

# حذف package manager cache
RUN apk update && \
    apk add --no-cache nginx && \
    rm -rf /var/cache/apk/*

# استفاده از multi-stage build
FROM node:16-alpine AS builder
# ... build steps
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

#### **2. Runtime Security:**
```bash
# اجرای کانتینر با امنیت بالا
docker run -d \
  --name secure-app \
  --user 1001:1001 \
  --read-only \
  --tmpfs /tmp \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --security-opt no-new-privileges:true \
  --memory=512m \
  --cpus="1.0" \
  my-app:latest
```

#### **3. Network Security:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    networks:
      - frontend
    ports:
      - "127.0.0.1:80:80"  # فقط localhost
  
  api:
    image: my-api:latest
    networks:
      - frontend
      - backend
  
  db:
    image: postgres:13
    networks:
      - backend
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

secrets:
  db_password:
    external: true
```

### مثال عملی:

#### **Dockerfile امن:**
```dockerfile
FROM node:16-alpine

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

# تغییر مالکیت
RUN chown -R nextjs:nodejs /app
USER nextjs

# تعریف پورت
EXPOSE 3000

# دستور پیش‌فرض
CMD ["npm", "start"]
```

#### **Docker Compose امن:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    networks:
      - frontend
    ports:
      - "127.0.0.1:80:80"
  
  app:
    image: my-app:latest
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    networks:
      - frontend
      - backend
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://db:5432/myapp
    depends_on:
      - db
  
  db:
    image: postgres:13
    user: "999:999"
    read_only: true
    tmpfs:
      - /tmp
      - /var/lib/postgresql/data
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    networks:
      - backend
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true

secrets:
  db_password:
    external: true
```

## 8.9 Compliance and Auditing

رعایت استانداردهای امنیتی و حسابرسی برای سازمان‌ها ضروری است.

### استانداردهای امنیتی:

#### **1. CIS Docker Benchmark:**
```bash
# اجرای CIS benchmark
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/docker-bench-security
```

#### **2. NIST Cybersecurity Framework:**
- Identify: شناسایی دارایی‌ها
- Protect: محافظت از سیستم‌ها
- Detect: تشخیص تهدیدات
- Respond: پاسخ به حوادث
- Recover: بازیابی از حوادث

#### **3. ISO 27001:**
- مدیریت امنیت اطلاعات
- ارزیابی ریسک
- کنترل‌های امنیتی

### مثال عملی:

#### **اسکریپت Compliance:**
```bash
#!/bin/bash
# compliance-check.sh

echo "Starting compliance check..."

# بررسی CIS Docker Benchmark
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/docker-bench-security

# بررسی ایمیج‌ها
trivy image --severity HIGH,CRITICAL my-app:latest

# بررسی کانتینرها
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# بررسی شبکه‌ها
docker network ls

# بررسی volumeها
docker volume ls

echo "Compliance check completed!"
```

#### **Docker Compose با Compliance:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    networks:
      - frontend
    ports:
      - "127.0.0.1:80:80"
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
  
  monitoring:
    image: prom/prometheus
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    networks:
      - monitoring
    ports:
      - "127.0.0.1:9090:9090"
    volumes:
      - prometheus-data:/prometheus

networks:
  frontend:
    driver: bridge
  monitoring:
    driver: bridge

volumes:
  prometheus-data:
```

## 8.10 Security Monitoring

نظارت بر امنیت برای تشخیص تهدیدات و پاسخ به حوادث ضروری است.

### ابزارهای نظارت امنیتی:

#### **1. Falco:**
```yaml
version: '3.8'
services:
  falco:
    image: falcosecurity/falco:latest
    privileged: true
    volumes:
      - /var/run/docker.sock:/host/var/run/docker.sock
      - /dev:/host/dev
      - /proc:/host/proc:ro
      - /boot:/host/boot:ro
      - /lib/modules:/host/lib/modules:ro
      - /usr:/host/usr:ro
    environment:
      - FALCO_GRPC_ENABLED=true
      - FALCO_GRPC_BIND_ADDRESS=0.0.0.0:5060
    ports:
      - "5060:5060"
```

#### **2. OWASP ZAP:**
```yaml
version: '3.8'
services:
  zap:
    image: owasp/zap2docker-stable
    ports:
      - "8080:8080"
    environment:
      - ZAP_PROXY_PORT=8080
```

### مثال عملی:

#### **نظارت امنیتی کامل:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    networks:
      - frontend
    ports:
      - "127.0.0.1:80:80"
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
  
  falco:
    image: falcosecurity/falco:latest
    privileged: true
    volumes:
      - /var/run/docker.sock:/host/var/run/docker.sock
      - /dev:/host/dev
      - /proc:/host/proc:ro
      - /boot:/host/boot:ro
      - /lib/modules:/host/lib/modules:ro
      - /usr:/host/usr:ro
    environment:
      - FALCO_GRPC_ENABLED=true
      - FALCO_GRPC_BIND_ADDRESS=0.0.0.0:5060
    ports:
      - "127.0.0.1:5060:5060"
    networks:
      - monitoring
  
  prometheus:
    image: prom/prometheus
    user: "1001:1001"
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    security_opt:
      - no-new-privileges:true
    networks:
      - monitoring
    ports:
      - "127.0.0.1:9090:9090"
    volumes:
      - prometheus-data:/prometheus
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro

networks:
  frontend:
    driver: bridge
  monitoring:
    driver: bridge

volumes:
  prometheus-data:
```

#### **اسکریپت نظارت:**
```bash
#!/bin/bash
# security-monitor.sh

echo "Starting security monitoring..."

# بررسی وضعیت کانتینرها
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# بررسی لاگ‌های امنیتی
docker logs falco 2>&1 | grep -i "security\|threat\|attack"

# بررسی استفاده از منابع
docker stats --no-stream

# بررسی شبکه‌ها
docker network ls

# بررسی volumeها
docker volume ls

echo "Security monitoring completed!"
```

این بخش شما را با تمام جنبه‌های امنیت Docker آشنا می‌کند.