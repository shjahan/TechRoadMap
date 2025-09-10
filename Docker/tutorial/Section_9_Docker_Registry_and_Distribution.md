# Section 9 – Docker Registry and Distribution

## 9.1 Docker Hub

Docker Hub مخزن عمومی ایمیج‌های Docker است که توسط Docker Inc. ارائه می‌شود. این پلتفرم امکان اشتراک‌گذاری و کشف ایمیج‌ها را فراهم می‌کند.

### ویژگی‌های Docker Hub:
- **Public Repositories**: مخازن عمومی رایگان
- **Private Repositories**: مخازن خصوصی (پولی)
- **Automated Builds**: ساخت خودکار از GitHub
- **Webhooks**: اعلان‌های خودکار
- **Vulnerability Scanning**: اسکن امنیتی

### دستورات کلیدی Docker Hub:

```bash
# ورود به Docker Hub
docker login

# آپلود ایمیج
docker push username/repository:tag

# دانلود ایمیج
docker pull username/repository:tag

# جستجوی ایمیج
docker search nginx

# خروج از Docker Hub
docker logout
```

### مثال عملی:

#### **آپلود ایمیج به Docker Hub:**
```bash
# ورود به Docker Hub
docker login

# ساخت ایمیج
docker build -t myusername/my-app:latest .

# تگ زدن ایمیج
docker tag my-app:latest myusername/my-app:latest

# آپلود ایمیج
docker push myusername/my-app:latest

# بررسی ایمیج آپلود شده
docker pull myusername/my-app:latest
```

#### **استفاده از ایمیج‌های Docker Hub:**
```bash
# دانلود ایمیج رسمی
docker pull nginx:alpine

# دانلود ایمیج از کاربر خاص
docker pull myusername/my-app:latest

# اجرای ایمیج
docker run -d -p 80:80 myusername/my-app:latest
```

### تنظیمات Docker Hub:

#### **1. ایجاد Repository:**
1. ورود به Docker Hub
2. کلیک روی "Create Repository"
3. انتخاب نام و توضیحات
4. انتخاب Public یا Private

#### **2. Automated Builds:**
1. اتصال GitHub account
2. انتخاب repository
3. تنظیم Dockerfile path
4. فعال‌سازی automated build

#### **3. Webhooks:**
1. تنظیم webhook URL
2. انتخاب events
3. تست webhook

## 9.2 Private Registries

Private Registryها برای ذخیره‌سازی ایمیج‌های خصوصی سازمان‌ها استفاده می‌شوند.

### راه‌اندازی Private Registry:

#### **1. Docker Registry:**
```bash
# اجرای Registry محلی
docker run -d \
  --name registry \
  -p 5000:5000 \
  -v registry-data:/var/lib/registry \
  registry:2

# بررسی Registry
curl http://localhost:5000/v2/_catalog
```

#### **2. Registry با Authentication:**
```bash
# ایجاد فایل htpasswd
docker run --rm --entrypoint htpasswd httpd:2 -Bbn testuser testpassword > auth/htpasswd

# اجرای Registry با authentication
docker run -d \
  --name registry \
  -p 5000:5000 \
  -v registry-data:/var/lib/registry \
  -v $(pwd)/auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
  registry:2
```

### مثال عملی:

#### **Docker Compose برای Private Registry:**
```yaml
version: '3.8'
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
    volumes:
      - registry-data:/var/lib/registry
      - ./auth:/auth
    networks:
      - registry-network

  registry-ui:
    image: joxit/docker-registry-ui:latest
    ports:
      - "8080:80"
    environment:
      REGISTRY_URL: http://registry:5000
    depends_on:
      - registry
    networks:
      - registry-network

networks:
  registry-network:
    driver: bridge

volumes:
  registry-data:
```

#### **استفاده از Private Registry:**
```bash
# ورود به Private Registry
docker login localhost:5000

# تگ زدن ایمیج برای Private Registry
docker tag my-app:latest localhost:5000/my-app:latest

# آپلود به Private Registry
docker push localhost:5000/my-app:latest

# دانلود از Private Registry
docker pull localhost:5000/my-app:latest
```

## 9.3 Registry Security

امنیت Registry برای محافظت از ایمیج‌های خصوصی ضروری است.

### اصول امنیت Registry:

#### **1. Authentication:**
```yaml
version: '3.8'
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
    volumes:
      - registry-data:/var/lib/registry
      - ./auth:/auth
```

#### **2. TLS/SSL:**
```yaml
version: '3.8'
services:
  registry:
    image: registry:2
    ports:
      - "443:5000"
    environment:
      REGISTRY_HTTP_TLS_CERTIFICATE: /certs/domain.crt
      REGISTRY_HTTP_TLS_KEY: /certs/domain.key
    volumes:
      - registry-data:/var/lib/registry
      - ./certs:/certs
```

#### **3. Network Security:**
```yaml
version: '3.8'
services:
  registry:
    image: registry:2
    ports:
      - "127.0.0.1:5000:5000"  # فقط localhost
    networks:
      - registry-network
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd

networks:
  registry-network:
    driver: bridge
    internal: true
```

### مثال عملی:

#### **Registry امن:**
```yaml
version: '3.8'
services:
  registry:
    image: registry:2
    ports:
      - "127.0.0.1:5000:5000"
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
      REGISTRY_HTTP_TLS_CERTIFICATE: /certs/domain.crt
      REGISTRY_HTTP_TLS_KEY: /certs/domain.key
    volumes:
      - registry-data:/var/lib/registry
      - ./auth:/auth
      - ./certs:/certs
    networks:
      - registry-network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - registry
    networks:
      - registry-network
    restart: unless-stopped

networks:
  registry-network:
    driver: bridge

volumes:
  registry-data:
```

## 9.4 Image Signing and Verification

امضای ایمیج‌ها برای اطمینان از اصالت و یکپارچگی ضروری است.

### Docker Content Trust:

#### **1. فعال‌سازی Content Trust:**
```bash
# فعال‌سازی برای تمام عملیات
export DOCKER_CONTENT_TRUST=1

# فعال‌سازی برای عملیات خاص
docker push --disable-content-trust=false my-app:latest
```

#### **2. ایجاد Key Pair:**
```bash
# ایجاد root key
docker trust key generate root

# ایجاد repository key
docker trust key generate my-app

# اضافه کردن key به repository
docker trust signer add --key my-app.pub my-app myusername/my-app
```

### مثال عملی:

#### **امضای ایمیج:**
```bash
# فعال‌سازی Content Trust
export DOCKER_CONTENT_TRUST=1

# ساخت ایمیج
docker build -t myusername/my-app:latest .

# امضای ایمیج
docker trust sign myusername/my-app:latest

# آپلود ایمیج امضا شده
docker push myusername/my-app:latest
```

#### **تأیید ایمیج:**
```bash
# فعال‌سازی Content Trust
export DOCKER_CONTENT_TRUST=1

# دانلود ایمیج (تأیید خودکار)
docker pull myusername/my-app:latest

# بررسی امضای ایمیج
docker trust inspect myusername/my-app:latest
```

## 9.5 Image Vulnerability Scanning

اسکن آسیب‌پذیری ایمیج‌ها برای شناسایی مشکلات امنیتی ضروری است.

### ابزارهای اسکن:

#### **1. Docker Scan:**
```bash
# اسکن ایمیج
docker scan my-app:latest

# اسکن با خروجی JSON
docker scan --json my-app:latest

# اسکن با فیلتر شدت
docker scan --severity high my-app:latest
```

#### **2. Trivy:**
```bash
# اسکن ایمیج
trivy image my-app:latest

# اسکن با خروجی JSON
trivy image --format json my-app:latest

# اسکن با فیلتر شدت
trivy image --severity HIGH,CRITICAL my-app:latest
```

#### **3. Clair:**
```bash
# اجرای Clair
docker run -d --name clair-db arminc/clair-db
docker run -d --name clair --link clair-db:postgres arminc/clair-local

# اسکن ایمیج
clair-scanner --ip clair my-app:latest
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
# vulnerability-scan.sh

echo "Starting vulnerability scan..."

# اسکن با Trivy
trivy image --severity HIGH,CRITICAL my-app:latest

# اسکن با Docker Scan
docker scan my-app:latest

# اسکن با Snyk
snyk container test my-app:latest

echo "Vulnerability scan completed!"
```

## 9.6 Registry Mirroring

Mirror کردن Registry برای بهبود عملکرد و کاهش مصرف پهنای باند ضروری است.

### تنظیمات Mirror:

#### **1. Docker Daemon Configuration:**
```json
{
  "registry-mirrors": [
    "https://mirror.example.com",
    "https://another-mirror.example.com"
  ]
}
```

#### **2. Registry Mirror:**
```yaml
version: '3.8'
services:
  registry-mirror:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_PROXY_REMOTEURL: https://registry-1.docker.io
      REGISTRY_PROXY_USERNAME: username
      REGISTRY_PROXY_PASSWORD: password
    volumes:
      - mirror-data:/var/lib/registry
```

### مثال عملی:

#### **Registry Mirror کامل:**
```yaml
version: '3.8'
services:
  registry-mirror:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_PROXY_REMOTEURL: https://registry-1.docker.io
      REGISTRY_PROXY_USERNAME: ${DOCKER_HUB_USERNAME}
      REGISTRY_PROXY_PASSWORD: ${DOCKER_HUB_PASSWORD}
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /var/lib/registry
    volumes:
      - mirror-data:/var/lib/registry
    networks:
      - mirror-network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - registry-mirror
    networks:
      - mirror-network
    restart: unless-stopped

networks:
  mirror-network:
    driver: bridge

volumes:
  mirror-data:
```

#### **فایل nginx.conf:**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream registry {
        server registry-mirror:5000;
    }
    
    server {
        listen 80;
        location / {
            proxy_pass http://registry;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## 9.7 Image Lifecycle Management

مدیریت چرخه حیات ایمیج‌ها برای بهینه‌سازی فضای ذخیره‌سازی ضروری است.

### استراتژی‌های Lifecycle:

#### **1. Tagging Strategy:**
```bash
# تگ‌های semantic versioning
docker tag my-app:latest my-app:1.0.0
docker tag my-app:latest my-app:1.0
docker tag my-app:latest my-app:1

# تگ‌های environment
docker tag my-app:latest my-app:dev
docker tag my-app:latest my-app:staging
docker tag my-app:latest my-app:prod
```

#### **2. Cleanup Strategy:**
```bash
# حذف ایمیج‌های قدیمی
docker image prune -a

# حذف ایمیج‌های بدون استفاده
docker image prune

# حذف ایمیج‌های با فیلتر
docker images --filter "dangling=true" -q | xargs docker rmi
```

### مثال عملی:

#### **اسکریپت Lifecycle Management:**
```bash
#!/bin/bash
# image-lifecycle.sh

echo "Starting image lifecycle management..."

# حذف ایمیج‌های dangling
docker images --filter "dangling=true" -q | xargs docker rmi

# حذف ایمیج‌های قدیمی (بیش از 7 روز)
docker images --filter "dangling=false" --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}" | \
  awk '$3 > 7 {print $1 ":" $2}' | \
  xargs docker rmi

# حذف ایمیج‌های بدون استفاده
docker image prune -f

# نمایش فضای استفاده شده
docker system df

echo "Image lifecycle management completed!"
```

#### **Docker Compose با Lifecycle:**
```yaml
version: '3.8'
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_STORAGE_DELETE_ENABLED: "true"
    volumes:
      - registry-data:/var/lib/registry
    networks:
      - registry-network

  cleanup:
    image: registry:2
    command: ["/bin/sh", "-c", "while true; do sleep 3600; docker image prune -f; done"]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - registry-network

networks:
  registry-network:
    driver: bridge

volumes:
  registry-data:
```

## 9.8 Registry Backup and Recovery

پشتیبان‌گیری و بازیابی Registry برای محافظت از ایمیج‌ها ضروری است.

### روش‌های پشتیبان‌گیری:

#### **1. Volume Backup:**
```bash
# پشتیبان‌گیری از volume
docker run --rm \
  -v registry-data:/data \
  -v $(pwd):/backup \
  ubuntu \
  tar czf /backup/registry-backup.tar.gz /data
```

#### **2. Registry Export:**
```bash
# export ایمیج‌ها
docker save $(docker images -q) > all-images.tar

# import ایمیج‌ها
docker load < all-images.tar
```

#### **3. Registry API Backup:**
```bash
# پشتیبان‌گیری از catalog
curl -X GET http://localhost:5000/v2/_catalog > catalog.json

# پشتیبان‌گیری از manifest
curl -X GET http://localhost:5000/v2/my-app/manifests/latest > manifest.json
```

### مثال عملی:

#### **اسکریپت پشتیبان‌گیری:**
```bash
#!/bin/bash
# registry-backup.sh

BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)

echo "Starting registry backup..."

# پشتیبان‌گیری از volume
docker run --rm \
  -v registry-data:/data \
  -v $BACKUP_DIR:/backup \
  ubuntu \
  tar czf /backup/registry-volume_$DATE.tar.gz /data

# پشتیبان‌گیری از catalog
curl -X GET http://localhost:5000/v2/_catalog > $BACKUP_DIR/catalog_$DATE.json

# پشتیبان‌گیری از ایمیج‌ها
docker images --format "{{.Repository}}:{{.Tag}}" | \
  xargs docker save > $BACKUP_DIR/images_$DATE.tar

echo "Registry backup completed: $DATE"
```

#### **اسکریپت بازیابی:**
```bash
#!/bin/bash
# registry-restore.sh

if [ -z "$1" ]; then
  echo "Usage: $0 <backup-date>"
  exit 1
fi

BACKUP_DATE=$1
BACKUP_DIR="/backup"

echo "Starting registry restore from $BACKUP_DATE..."

# بازیابی volume
docker run --rm \
  -v registry-data:/data \
  -v $BACKUP_DIR:/backup \
  ubuntu \
  tar xzf /backup/registry-volume_$BACKUP_DATE.tar.gz -C /

# بازیابی ایمیج‌ها
docker load < $BACKUP_DIR/images_$BACKUP_DATE.tar

echo "Registry restore completed!"
```

## 9.9 Multi-tenant Registries

Registryهای چندمستأجره برای سازمان‌های بزرگ ضروری است.

### ویژگی‌های Multi-tenant:

#### **1. Namespace Isolation:**
```yaml
version: '3.8'
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
    volumes:
      - registry-data:/var/lib/registry
      - ./auth:/auth
```

#### **2. Resource Quotas:**
```yaml
version: '3.8'
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /var/lib/registry
      REGISTRY_STORAGE_DELETE_ENABLED: "true"
    volumes:
      - registry-data:/var/lib/registry
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
```

### مثال عملی:

#### **Multi-tenant Registry:**
```yaml
version: '3.8'
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /var/lib/registry
      REGISTRY_STORAGE_DELETE_ENABLED: "true"
    volumes:
      - registry-data:/var/lib/registry
      - ./auth:/auth
    networks:
      - registry-network
    restart: unless-stopped

  registry-ui:
    image: joxit/docker-registry-ui:latest
    ports:
      - "8080:80"
    environment:
      REGISTRY_URL: http://registry:5000
      REGISTRY_TITLE: Multi-tenant Registry
    depends_on:
      - registry
    networks:
      - registry-network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - registry
    networks:
      - registry-network
    restart: unless-stopped

networks:
  registry-network:
    driver: bridge

volumes:
  registry-data:
```

## 9.10 Registry Performance Optimization

بهینه‌سازی عملکرد Registry برای بهبود سرعت و کاهش مصرف منابع ضروری است.

### تکنیک‌های بهینه‌سازی:

#### **1. Caching:**
```yaml
version: '3.8'
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /var/lib/registry
      REGISTRY_HTTP_HEADERS_X_CONTENT_TYPE_OPTIONS: nosniff
    volumes:
      - registry-data:/var/lib/registry
    networks:
      - registry-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - registry
    networks:
      - registry-network
```

#### **2. Load Balancing:**
```yaml
version: '3.8'
services:
  registry1:
    image: registry:2
    environment:
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /var/lib/registry
    volumes:
      - registry-data1:/var/lib/registry
    networks:
      - registry-network

  registry2:
    image: registry:2
    environment:
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /var/lib/registry
    volumes:
      - registry-data2:/var/lib/registry
    networks:
      - registry-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - registry1
      - registry2
    networks:
      - registry-network

networks:
  registry-network:
    driver: bridge

volumes:
  registry-data1:
  registry-data2:
```

### مثال عملی:

#### **Registry بهینه‌شده:**
```yaml
version: '3.8'
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /var/lib/registry
      REGISTRY_HTTP_HEADERS_X_CONTENT_TYPE_OPTIONS: nosniff
      REGISTRY_HTTP_HEADERS_X_FRAME_OPTIONS: DENY
      REGISTRY_HTTP_HEADERS_X_CONTENT_TYPE_OPTIONS: nosniff
    volumes:
      - registry-data:/var/lib/registry
    networks:
      - registry-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2.0'
        reservations:
          memory: 1G
          cpus: '1.0'

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - registry
    networks:
      - registry-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'

  monitoring:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - prometheus-data:/prometheus
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    networks:
      - registry-network
    restart: unless-stopped

networks:
  registry-network:
    driver: bridge

volumes:
  registry-data:
  prometheus-data:
```

#### **فایل nginx.conf بهینه‌شده:**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream registry {
        server registry:5000;
    }
    
    server {
        listen 80;
        listen 443 ssl;
        
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        
        location / {
            proxy_pass http://registry;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Caching
            proxy_cache_valid 200 1h;
            proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        }
    }
}
```

این بخش شما را با تمام جنبه‌های Docker Registry و Distribution آشنا می‌کند.