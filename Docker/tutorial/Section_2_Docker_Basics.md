# Section 2 – Docker Basics

## 2.1 Docker Images

ایمیج‌های Docker الگوهای فقط خواندنی هستند که برای ایجاد کانتینرها استفاده می‌شوند. هر ایمیج شامل کد اپلیکیشن، runtime، کتابخانه‌ها، وابستگی‌ها و تنظیمات مورد نیاز است.

### ویژگی‌های ایمیج‌ها:
- **Immutable**: غیرقابل تغییر پس از ایجاد
- **Layered**: ساخته شده از لایه‌های متعدد
- **Reusable**: قابل استفاده مجدد
- **Portable**: قابل حمل بین محیط‌های مختلف

### ساختار ایمیج:
```
Application Layer (Top)
├── Dependencies Layer
├── Runtime Layer
├── OS Libraries Layer
└── Base OS Layer (Bottom)
```

### دستورات کلیدی:
```bash
# لیست ایمیج‌های محلی
docker images

# دانلود ایمیج
docker pull nginx:latest

# حذف ایمیج
docker rmi nginx

# جستجوی ایمیج
docker search ubuntu

# مشاهده تاریخچه ایمیج
docker history nginx
```

### مثال عملی:
```bash
# دانلود و اجرای ایمیج nginx
docker pull nginx:1.21
docker run -d -p 8080:80 --name my-nginx nginx:1.21

# بررسی ایمیج‌های موجود
docker images
```

## 2.2 Docker Containers

کانتینرها نمونه‌های اجرایی ایمیج‌ها هستند که در محیط ایزوله اجرا می‌شوند. هر کانتینر شامل تمام فایل‌ها، وابستگی‌ها و تنظیمات مورد نیاز برای اجرای اپلیکیشن است.

### ویژگی‌های کانتینرها:
- **Isolated**: جدا از سایر کانتینرها
- **Ephemeral**: موقتی (قابل حذف)
- **Lightweight**: سبک و سریع
- **Portable**: قابل حمل

### چرخه حیات کانتینر:
```
Created → Running → Paused → Stopped → Removed
```

### دستورات کلیدی:
```bash
# ایجاد کانتینر جدید
docker create nginx

# اجرای کانتینر
docker start container_id

# اجرای کانتینر جدید
docker run -d nginx

# توقف کانتینر
docker stop container_id

# حذف کانتینر
docker rm container_id

# مشاهده کانتینرهای در حال اجرا
docker ps

# مشاهده تمام کانتینرها
docker ps -a
```

### مثال عملی:
```bash
# اجرای کانتینر nginx با نام و پورت
docker run -d --name web-server -p 80:80 nginx

# بررسی وضعیت کانتینر
docker ps

# مشاهده لاگ‌های کانتینر
docker logs web-server

# ورود به کانتینر
docker exec -it web-server bash
```

## 2.3 Dockerfile

Dockerfile فایل متنی است که شامل دستورالعمل‌های ساخت ایمیج سفارشی است. این فایل به Docker می‌گوید چگونه ایمیج مورد نظر را بسازد.

### ساختار Dockerfile:
```dockerfile
# Base image
FROM ubuntu:20.04

# Metadata
LABEL maintainer="developer@example.com"

# Environment variables
ENV NODE_ENV=production

# Working directory
WORKDIR /app

# Copy files
COPY package.json .
COPY src/ ./src/

# Install dependencies
RUN npm install

# Expose port
EXPOSE 3000

# Default command
CMD ["npm", "start"]
```

### دستورات کلیدی Dockerfile:

#### **FROM**
```dockerfile
FROM ubuntu:20.04
FROM node:16-alpine
FROM python:3.9-slim
```

#### **RUN**
```dockerfile
RUN apt-get update
RUN npm install
RUN pip install -r requirements.txt
```

#### **COPY و ADD**
```dockerfile
COPY package.json /app/
ADD https://example.com/file.tar.gz /tmp/
```

#### **WORKDIR**
```dockerfile
WORKDIR /app
WORKDIR /usr/src/app
```

#### **EXPOSE**
```dockerfile
EXPOSE 3000
EXPOSE 80 443
```

#### **CMD و ENTRYPOINT**
```dockerfile
CMD ["npm", "start"]
ENTRYPOINT ["python", "app.py"]
```

### مثال کامل:
```dockerfile
# Dockerfile برای اپلیکیشن Node.js
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

USER node

CMD ["npm", "start"]
```

### ساخت ایمیج:
```bash
# ساخت ایمیج
docker build -t my-app:latest .

# ساخت با تگ خاص
docker build -t my-app:v1.0.0 .

# ساخت با build context
docker build -f Dockerfile.prod -t my-app:prod .
```

## 2.4 Docker Hub

Docker Hub مخزن عمومی ایمیج‌های Docker است که توسط Docker Inc. ارائه می‌شود. این پلتفرم امکان اشتراک‌گذاری و کشف ایمیج‌ها را فراهم می‌کند.

### ویژگی‌های Docker Hub:
- **Public Repositories**: مخازن عمومی رایگان
- **Private Repositories**: مخازن خصوصی (پولی)
- **Automated Builds**: ساخت خودکار از GitHub
- **Webhooks**: اعلان‌های خودکار
- **Vulnerability Scanning**: اسکن امنیتی

### دستورات کلیدی:
```bash
# ورود به Docker Hub
docker login

# آپلود ایمیج
docker push username/repository:tag

# دانلود ایمیج
docker pull username/repository:tag

# جستجوی ایمیج
docker search nginx
```

### مثال عملی:
```bash
# ورود به حساب کاربری
docker login

# تگ زدن ایمیج
docker tag my-app:latest username/my-app:latest

# آپلود ایمیج
docker push username/my-app:latest

# دانلود ایمیج
docker pull username/my-app:latest
```

### تنظیمات Docker Hub:
1. ایجاد حساب کاربری
2. ایجاد Repository
3. تنظیم Automated Builds
4. تنظیم Webhooks

## 2.5 Docker Registry

Docker Registry سرویسی است که ایمیج‌های Docker را ذخیره و توزیع می‌کند. Docker Hub یک نمونه از Registry عمومی است.

### انواع Registry:
- **Public Registry**: Docker Hub
- **Private Registry**: داخلی سازمان
- **Cloud Registry**: AWS ECR, Google GCR, Azure ACR

### راه‌اندازی Private Registry:
```bash
# اجرای Registry محلی
docker run -d -p 5000:5000 --name registry registry:2

# آپلود ایمیج به Registry محلی
docker tag my-app:latest localhost:5000/my-app:latest
docker push localhost:5000/my-app:latest

# دانلود از Registry محلی
docker pull localhost:5000/my-app:latest
```

### تنظیمات Registry:
```yaml
# docker-compose.yml
version: '3'
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /var/lib/registry
    volumes:
      - registry-data:/var/lib/registry

volumes:
  registry-data:
```

## 2.6 Docker Commands Overview

دستورات Docker ابزارهای اصلی برای مدیریت کانتینرها و ایمیج‌ها هستند.

### دستورات ایمیج:
```bash
# مدیریت ایمیج‌ها
docker images                    # لیست ایمیج‌ها
docker pull <image>             # دانلود ایمیج
docker push <image>             # آپلود ایمیج
docker rmi <image>              # حذف ایمیج
docker build -t <name> .        # ساخت ایمیج
docker tag <source> <target>    # تگ زدن ایمیج
```

### دستورات کانتینر:
```bash
# مدیریت کانتینرها
docker ps                       # کانتینرهای در حال اجرا
docker ps -a                    # تمام کانتینرها
docker run <image>              # اجرای کانتینر
docker start <container>        # شروع کانتینر
docker stop <container>         # توقف کانتینر
docker rm <container>           # حذف کانتینر
docker exec -it <container> bash # ورود به کانتینر
```

### دستورات سیستم:
```bash
# مدیریت سیستم
docker info                     # اطلاعات Docker
docker version                  # نسخه Docker
docker system df                # استفاده از فضای دیسک
docker system prune             # پاکسازی سیستم
docker logs <container>         # مشاهده لاگ‌ها
```

### مثال‌های عملی:
```bash
# اجرای کانتینر با تنظیمات خاص
docker run -d \
  --name web-server \
  -p 8080:80 \
  -e ENV=production \
  -v /host/path:/container/path \
  nginx:latest

# مشاهده اطلاعات کانتینر
docker inspect web-server

# کپی فایل به/از کانتینر
docker cp file.txt web-server:/app/
docker cp web-server:/app/file.txt ./
```

## 2.7 Container Lifecycle

چرخه حیات کانتینر شامل مراحل مختلف از ایجاد تا حذف است.

### مراحل چرخه حیات:
1. **Created**: کانتینر ایجاد شده اما اجرا نشده
2. **Running**: کانتینر در حال اجرا
3. **Paused**: کانتینر متوقف موقت
4. **Stopped**: کانتینر متوقف شده
5. **Removed**: کانتینر حذف شده

### دستورات چرخه حیات:
```bash
# ایجاد کانتینر
docker create nginx

# شروع کانتینر
docker start container_id

# توقف کانتینر
docker stop container_id

# متوقف کردن موقت
docker pause container_id
docker unpause container_id

# راه‌اندازی مجدد
docker restart container_id

# حذف کانتینر
docker rm container_id
```

### مثال عملی:
```bash
# ایجاد و مدیریت کانتینر
docker create --name my-nginx nginx
docker start my-nginx
docker logs my-nginx
docker stop my-nginx
docker rm my-nginx
```

## 2.8 Image Layers and Caching

ایمیج‌های Docker از لایه‌های متعدد ساخته شده‌اند که امکان بهینه‌سازی و کش کردن را فراهم می‌کند.

### مفهوم لایه‌ها:
- هر دستور در Dockerfile یک لایه ایجاد می‌کند
- لایه‌های مشترک بین ایمیج‌ها استفاده مجدد می‌شوند
- تغییر در یک لایه فقط لایه‌های بالایی را بازسازی می‌کند

### مثال لایه‌ها:
```dockerfile
FROM ubuntu:20.04          # Layer 1: Base OS
RUN apt-get update         # Layer 2: Package list
RUN apt-get install nginx  # Layer 3: Nginx installation
COPY app.py /app/          # Layer 4: Application files
CMD ["python", "app.py"]   # Layer 5: Command
```

### بهینه‌سازی کش:
```dockerfile
# بهینه: وابستگی‌ها را ابتدا کپی کنید
COPY package.json .
RUN npm install
COPY . .

# غیربهینه: کپی تمام فایل‌ها در ابتدا
COPY . .
RUN npm install
```

### دستورات کش:
```bash
# مشاهده لایه‌های ایمیج
docker history nginx

# ساخت بدون کش
docker build --no-cache -t my-app .

# ساخت با کش خاص
docker build --cache-from my-app:latest -t my-app:new .
```

## 2.9 Container Networking Basics

شبکه‌بندی کانتینرها امکان ارتباط بین کانتینرها و دنیای خارج را فراهم می‌کند.

### انواع شبکه:
- **Bridge**: شبکه پیش‌فرض
- **Host**: استفاده از شبکه میزبان
- **None**: بدون شبکه
- **Overlay**: شبکه توزیع‌شده

### دستورات شبکه:
```bash
# مشاهده شبکه‌ها
docker network ls

# ایجاد شبکه
docker network create my-network

# اجرای کانتینر در شبکه
docker run --network my-network nginx

# اتصال کانتینر به شبکه
docker network connect my-network container_id
```

### مثال عملی:
```bash
# ایجاد شبکه
docker network create web-network

# اجرای کانتینرها در همان شبکه
docker run -d --name web --network web-network nginx
docker run -d --name db --network web-network postgres

# کانتینرها می‌توانند با نام یکدیگر ارتباط برقرار کنند
# web می‌تواند به db دسترسی داشته باشد
```

## 2.10 Container Storage Basics

ذخیره‌سازی کانتینرها شامل مدیریت داده‌های دائمی و موقتی است.

### انواع ذخیره‌سازی:
- **Bind Mounts**: اتصال مستقیم پوشه میزبان
- **Volumes**: مدیریت شده توسط Docker
- **tmpfs**: ذخیره‌سازی در حافظه

### دستورات ذخیره‌سازی:
```bash
# مشاهده volumeها
docker volume ls

# ایجاد volume
docker volume create my-volume

# اجرای کانتینر با volume
docker run -v my-volume:/data nginx

# اجرای کانتینر با bind mount
docker run -v /host/path:/container/path nginx
```

### مثال عملی:
```bash
# ایجاد volume برای دیتابیس
docker volume create db-data

# اجرای PostgreSQL با volume
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=password \
  -v db-data:/var/lib/postgresql/data \
  postgres:13

# پشتیبان‌گیری از volume
docker run --rm -v db-data:/data -v $(pwd):/backup ubuntu tar czf /backup/db-backup.tar.gz /data
```

این بخش پایه‌ای برای کار با Docker فراهم می‌کند و شما را برای یادگیری مفاهیم پیشرفته‌تر آماده می‌سازد.