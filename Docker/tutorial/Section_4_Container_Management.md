# Section 4 – Container Management

## 4.1 Container Lifecycle Management

مدیریت چرخه حیات کانتینرها شامل کنترل مراحل مختلف از ایجاد تا حذف کانتینر است.

### مراحل چرخه حیات:
1. **Created**: کانتینر ایجاد شده اما اجرا نشده
2. **Running**: کانتینر در حال اجرا
3. **Paused**: کانتینر متوقف موقت
4. **Stopped**: کانتینر متوقف شده
5. **Removed**: کانتینر حذف شده

### دستورات مدیریت چرخه حیات:

#### **ایجاد کانتینر:**
```bash
# ایجاد کانتینر جدید
docker create nginx

# ایجاد با نام و تنظیمات
docker create --name web-server -p 80:80 nginx

# ایجاد با متغیرهای محیطی
docker create -e NODE_ENV=production node:16
```

#### **شروع کانتینر:**
```bash
# شروع کانتینر
docker start container_id

# شروع با نام
docker start web-server

# شروع در پس‌زمینه
docker start -d web-server
```

#### **توقف کانتینر:**
```bash
# توقف نرم (SIGTERM)
docker stop container_id

# توقف فوری (SIGKILL)
docker kill container_id

# توقف با timeout
docker stop -t 30 container_id
```

#### **راه‌اندازی مجدد:**
```bash
# راه‌اندازی مجدد
docker restart container_id

# راه‌اندازی مجدد با timeout
docker restart -t 30 container_id
```

### مثال عملی:
```bash
# ایجاد و مدیریت کانتینر
docker create --name my-nginx nginx:alpine
docker start my-nginx
docker ps
docker stop my-nginx
docker start my-nginx
docker restart my-nginx
docker rm my-nginx
```

## 4.2 Container Resource Limits

محدود کردن منابع کانتینرها برای کنترل مصرف CPU، حافظه و I/O ضروری است.

### محدودیت‌های حافظه:
```bash
# محدودیت حافظه (512MB)
docker run -m 512m nginx

# محدودیت حافظه با swap
docker run -m 512m --memory-swap 1g nginx

# محدودیت حافظه بدون swap
docker run -m 512m --memory-swap 512m nginx
```

### محدودیت‌های CPU:
```bash
# محدودیت CPU (0.5 core)
docker run --cpus="0.5" nginx

# محدودیت CPU با cpuset
docker run --cpuset-cpus="0,1" nginx

# محدودیت CPU با cpu-shares
docker run --cpu-shares=512 nginx
```

### محدودیت‌های I/O:
```bash
# محدودیت read/write
docker run --device-read-bps /dev/sda:1mb nginx
docker run --device-write-bps /dev/sda:1mb nginx

# محدودیت IOPS
docker run --device-read-iops /dev/sda:100 nginx
```

### مثال کامل:
```bash
# کانتینر با محدودیت‌های کامل
docker run -d \
  --name web-server \
  -m 1g \
  --memory-swap 1g \
  --cpus="1.0" \
  --cpuset-cpus="0,1" \
  --device-read-bps /dev/sda:10mb \
  --device-write-bps /dev/sda:10mb \
  nginx:alpine
```

### Docker Compose با محدودیت‌ها:
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

## 4.3 Container Environment Variables

متغیرهای محیطی برای پیکربندی کانتینرها و انتقال اطلاعات استفاده می‌شوند.

### تنظیم متغیرهای محیطی:

#### **در docker run:**
```bash
# متغیر ساده
docker run -e NODE_ENV=production nginx

# چندین متغیر
docker run -e NODE_ENV=production -e PORT=3000 nginx

# از فایل
docker run --env-file .env nginx

# از متغیر سیستم
docker run -e NODE_ENV=$NODE_ENV nginx
```

#### **در Dockerfile:**
```dockerfile
# تعریف متغیر
ENV NODE_ENV=production
ENV PORT=3000

# استفاده از متغیر
ENV APP_HOME=/app
WORKDIR $APP_HOME
```

### مثال عملی:
```bash
# اجرای کانتینر با متغیرهای محیطی
docker run -d \
  --name web-app \
  -e NODE_ENV=production \
  -e PORT=3000 \
  -e DATABASE_URL=postgres://localhost:5432/mydb \
  -p 3000:3000 \
  my-app:latest
```

### فایل .env:
```env
NODE_ENV=production
PORT=3000
DATABASE_URL=postgres://localhost:5432/mydb
REDIS_URL=redis://localhost:6379
```

### Docker Compose با متغیرهای محیطی:
```yaml
version: '3.8'
services:
  web:
    image: my-app:latest
    environment:
      - NODE_ENV=production
      - PORT=3000
    env_file:
      - .env
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
```

## 4.4 Container Port Mapping

نقشه‌برداری پورت‌ها برای دسترسی به سرویس‌های داخل کانتینر از خارج ضروری است.

### انواع Port Mapping:

#### **Port Binding:**
```bash
# پورت ساده
docker run -p 8080:80 nginx

# پورت با IP خاص
docker run -p 127.0.0.1:8080:80 nginx

# پورت تصادفی
docker run -P nginx
```

#### **Port Ranges:**
```bash
# محدوده پورت
docker run -p 8080-8090:80-90 nginx

# چندین پورت
docker run -p 80:80 -p 443:443 nginx
```

### مثال‌های عملی:

#### **Web Server:**
```bash
# nginx روی پورت 8080
docker run -d --name web -p 8080:80 nginx

# دسترسی: http://localhost:8080
```

#### **Database:**
```bash
# PostgreSQL روی پورت 5432
docker run -d --name db -p 5432:5432 postgres:13

# اتصال: localhost:5432
```

#### **Application:**
```bash
# Node.js app روی پورت 3000
docker run -d --name app -p 3000:3000 my-app:latest

# دسترسی: http://localhost:3000
```

### Docker Compose با Port Mapping:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
  app:
    image: my-app:latest
    ports:
      - "3000:3000"
  db:
    image: postgres:13
    ports:
      - "5432:5432"
```

## 4.5 Container Volume Mounting

نصب حجم‌ها برای اشتراک داده بین کانتینر و میزبان ضروری است.

### انواع Volume Mounting:

#### **Bind Mounts:**
```bash
# نصب پوشه میزبان
docker run -v /host/path:/container/path nginx

# نصب فایل
docker run -v /host/file.txt:/container/file.txt nginx

# نصب با دسترسی فقط خواندنی
docker run -v /host/path:/container/path:ro nginx
```

#### **Named Volumes:**
```bash
# ایجاد volume
docker volume create my-volume

# استفاده از volume
docker run -v my-volume:/data nginx

# مشاهده volumeها
docker volume ls
```

### مثال‌های عملی:

#### **Web Application:**
```bash
# نصب کد اپلیکیشن
docker run -d \
  --name web-app \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/public:/app/public \
  -p 3000:3000 \
  my-app:latest
```

#### **Database:**
```bash
# نصب داده‌های دیتابیس
docker run -d \
  --name postgres \
  -v postgres-data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=password \
  postgres:13
```

#### **Log Files:**
```bash
# نصب لاگ‌ها
docker run -d \
  --name web-server \
  -v /var/log/nginx:/var/log/nginx \
  -p 80:80 \
  nginx:alpine
```

### Docker Compose با Volumes:
```yaml
version: '3.8'
services:
  web:
    image: my-app:latest
    volumes:
      - ./src:/app/src
      - ./public:/app/public
      - app-logs:/app/logs
  db:
    image: postgres:13
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: password

volumes:
  postgres-data:
  app-logs:
```

## 4.6 Container Logging

مدیریت لاگ‌های کانتینرها برای نظارت و عیب‌یابی ضروری است.

### انواع Logging:

#### **مشاهده لاگ‌ها:**
```bash
# لاگ‌های کانتینر
docker logs container_id

# لاگ‌های با timestamp
docker logs -t container_id

# لاگ‌های real-time
docker logs -f container_id

# آخرین N خط
docker logs --tail 100 container_id

# لاگ‌های از زمان خاص
docker logs --since "2023-01-01T00:00:00" container_id
```

#### **Log Drivers:**
```bash
# JSON File (پیش‌فرض)
docker run --log-driver json-file nginx

# Syslog
docker run --log-driver syslog nginx

# Journald
docker run --log-driver journald nginx

# Fluentd
docker run --log-driver fluentd nginx
```

### مثال‌های عملی:

#### **Web Server Logs:**
```bash
# اجرای nginx با logging
docker run -d \
  --name web \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  nginx

# مشاهده لاگ‌ها
docker logs web
```

#### **Application Logs:**
```bash
# اجرای اپلیکیشن با logging
docker run -d \
  --name app \
  --log-driver json-file \
  --log-opt max-size=50m \
  --log-opt max-file=5 \
  my-app:latest

# مشاهده لاگ‌های real-time
docker logs -f app
```

### Docker Compose با Logging:
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
  app:
    image: my-app:latest
    logging:
      driver: fluentd
      options:
        fluentd-address: localhost:24224
        tag: docker.app
```

## 4.7 Container Health Checks

بررسی سلامت کانتینرها برای اطمینان از عملکرد صحیح ضروری است.

### انواع Health Checks:

#### **در Dockerfile:**
```dockerfile
# Health check با CMD
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Health check با script
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD /app/health-check.sh
```

#### **در docker run:**
```bash
# Health check با curl
docker run --health-cmd="curl -f http://localhost:3000/health || exit 1" \
  --health-interval=30s \
  --health-timeout=3s \
  --health-start-period=5s \
  --health-retries=3 \
  my-app:latest
```

### مثال‌های عملی:

#### **Web Application:**
```dockerfile
FROM node:16-alpine
COPY . .
RUN npm install
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
CMD ["npm", "start"]
```

#### **Database:**
```dockerfile
FROM postgres:13
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD pg_isready -U postgres || exit 1
```

### Docker Compose با Health Checks:
```yaml
version: '3.8'
services:
  web:
    image: my-app:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 3s
      start_period: 5s
      retries: 3
  db:
    image: postgres:13
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 3s
      start_period: 5s
      retries: 3
```

## 4.8 Container Restart Policies

سیاست‌های راه‌اندازی مجدد برای مدیریت خودکار کانتینرها ضروری است.

### انواع Restart Policies:

#### **no (پیش‌فرض):**
```bash
# کانتینر راه‌اندازی مجدد نمی‌شود
docker run --restart=no nginx
```

#### **on-failure:**
```bash
# راه‌اندازی مجدد فقط در صورت خطا
docker run --restart=on-failure nginx

# با تعداد تلاش محدود
docker run --restart=on-failure:5 nginx
```

#### **always:**
```bash
# همیشه راه‌اندازی مجدد
docker run --restart=always nginx
```

#### **unless-stopped:**
```bash
# راه‌اندازی مجدد مگر اینکه دستی متوقف شود
docker run --restart=unless-stopped nginx
```

### مثال‌های عملی:

#### **Web Server:**
```bash
# nginx با restart policy
docker run -d \
  --name web \
  --restart=always \
  -p 80:80 \
  nginx:alpine
```

#### **Database:**
```bash
# PostgreSQL با restart policy
docker run -d \
  --name postgres \
  --restart=unless-stopped \
  -e POSTGRES_PASSWORD=password \
  postgres:13
```

### Docker Compose با Restart Policies:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
  db:
    image: postgres:13
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD: password
  app:
    image: my-app:latest
    restart: on-failure:3
    depends_on:
      - db
```

## 4.9 Container Monitoring

نظارت بر کانتینرها برای اطمینان از عملکرد صحیح و تشخیص مشکلات ضروری است.

### دستورات نظارت:

#### **مشاهده وضعیت کانتینرها:**
```bash
# کانتینرهای در حال اجرا
docker ps

# تمام کانتینرها
docker ps -a

# با فرمت خاص
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

#### **مشاهده آمار منابع:**
```bash
# آمار real-time
docker stats

# آمار کانتینر خاص
docker stats container_id

# آمار بدون streaming
docker stats --no-stream
```

#### **مشاهده اطلاعات کانتینر:**
```bash
# اطلاعات کامل کانتینر
docker inspect container_id

# اطلاعات خاص
docker inspect --format='{{.State.Status}}' container_id
```

### مثال‌های عملی:

#### **نظارت بر Web Server:**
```bash
# اجرای nginx
docker run -d --name web nginx

# مشاهده آمار
docker stats web

# بررسی وضعیت
docker ps --filter name=web
```

#### **نظارت بر Database:**
```bash
# اجرای PostgreSQL
docker run -d --name postgres postgres:13

# مشاهده آمار
docker stats postgres

# بررسی لاگ‌ها
docker logs postgres
```

### Docker Compose با Monitoring:
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
  monitoring:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

## 4.10 Container Cleanup

پاکسازی کانتینرها و منابع برای مدیریت فضای دیسک ضروری است.

### دستورات پاکسازی:

#### **حذف کانتینرها:**
```bash
# حذف کانتینر متوقف شده
docker rm container_id

# حذف تمام کانتینرهای متوقف شده
docker container prune

# حذف کانتینر با فیلتر
docker rm $(docker ps -aq --filter status=exited)
```

#### **حذف ایمیج‌ها:**
```bash
# حذف ایمیج
docker rmi image_id

# حذف ایمیج‌های بدون استفاده
docker image prune

# حذف ایمیج‌های dangling
docker image prune -f
```

#### **حذف حجم‌ها:**
```bash
# حذف volume
docker volume rm volume_name

# حذف volumeهای بدون استفاده
docker volume prune
```

#### **پاکسازی کامل:**
```bash
# پاکسازی تمام منابع بدون استفاده
docker system prune

# پاکسازی با volumeها
docker system prune -a --volumes
```

### مثال‌های عملی:

#### **پاکسازی روزانه:**
```bash
# حذف کانتینرهای متوقف شده
docker container prune -f

# حذف ایمیج‌های بدون استفاده
docker image prune -f

# حذف volumeهای بدون استفاده
docker volume prune -f
```

#### **پاکسازی کامل:**
```bash
# پاکسازی تمام منابع
docker system prune -a --volumes -f

# مشاهده فضای استفاده شده
docker system df
```

### اسکریپت پاکسازی:
```bash
#!/bin/bash
# cleanup.sh

echo "Cleaning up Docker resources..."

# حذف کانتینرهای متوقف شده
docker container prune -f

# حذف ایمیج‌های بدون استفاده
docker image prune -f

# حذف volumeهای بدون استفاده
docker volume prune -f

# نمایش فضای استفاده شده
docker system df

echo "Cleanup completed!"
```

این بخش شما را با تمام جنبه‌های مدیریت کانتینرها آشنا می‌کند.