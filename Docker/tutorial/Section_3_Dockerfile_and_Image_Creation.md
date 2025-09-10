# Section 3 – Dockerfile and Image Creation

## 3.1 Dockerfile Syntax

Dockerfile فایل متنی است که شامل دستورالعمل‌های ساخت ایمیج Docker است. هر خط یک دستور است که با کلمات کلیدی شروع می‌شود.

### ساختار کلی Dockerfile:
```dockerfile
# Comment
INSTRUCTION arguments
```

### قوانین نوشتن:
- هر دستور در یک خط
- حساس به حروف کوچک/بزرگ
- دستورات به ترتیب اجرا می‌شوند
- کامنت‌ها با `#` شروع می‌شوند

### مثال پایه:
```dockerfile
# Base image
FROM ubuntu:20.04

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y python3

# Set default command
CMD ["python3", "app.py"]
```

### بهترین روش‌ها:
- استفاده از ایمیج‌های رسمی
- ترکیب دستورات RUN برای کاهش لایه‌ها
- استفاده از .dockerignore
- بهینه‌سازی ترتیب دستورات

## 3.2 Base Images Selection

انتخاب ایمیج پایه مناسب برای عملکرد و امنیت کانتینر بسیار مهم است.

### انواع ایمیج‌های پایه:

#### **Full Images (کامل)**
```dockerfile
FROM ubuntu:20.04
FROM centos:8
```
- شامل تمام ابزارهای سیستم
- حجم بالا
- مناسب برای development

#### **Minimal Images (حداقل)**
```dockerfile
FROM alpine:3.14
FROM scratch
```
- حجم کم
- امنیت بالا
- مناسب برای production

#### **Language-specific Images (مخصوص زبان)**
```dockerfile
FROM node:16-alpine
FROM python:3.9-slim
FROM openjdk:11-jre-slim
```
- بهینه‌سازی شده برای زبان خاص
- شامل runtime و ابزارهای لازم

### مقایسه حجم ایمیج‌ها:
```
ubuntu:20.04     ~72MB
alpine:3.14      ~5MB
node:16-alpine   ~110MB
python:3.9-slim  ~45MB
```

### مثال انتخاب مناسب:
```dockerfile
# برای اپلیکیشن Node.js
FROM node:16-alpine

# برای اپلیکیشن Python
FROM python:3.9-slim

# برای اپلیکیشن Go
FROM golang:1.17-alpine AS builder
FROM alpine:3.14
```

## 3.3 RUN, COPY, ADD Instructions

این دستورات برای اجرای دستورات، کپی فایل‌ها و اضافه کردن محتوا استفاده می‌شوند.

### دستور RUN:
```dockerfile
# اجرای دستورات در حین ساخت
RUN apt-get update
RUN apt-get install -y nginx
RUN npm install

# ترکیب دستورات (بهینه‌تر)
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### دستور COPY:
```dockerfile
# کپی فایل یا پوشه
COPY package.json /app/
COPY src/ /app/src/
COPY . /app/

# کپی با تغییر مالکیت
COPY --chown=node:node package.json /app/
```

### دستور ADD:
```dockerfile
# کپی فایل‌ها
ADD package.json /app/

# دانلود از URL
ADD https://example.com/file.tar.gz /tmp/

# استخراج فایل‌های فشرده
ADD archive.tar.gz /app/

# کپی با wildcard
ADD *.jar /app/libs/
```

### تفاوت COPY و ADD:
- **COPY**: فقط کپی فایل‌های محلی
- **ADD**: کپی + دانلود + استخراج

### مثال عملی:
```dockerfile
FROM node:16-alpine

WORKDIR /app

# کپی package.json اول (برای کش)
COPY package*.json ./
RUN npm ci --only=production

# کپی باقی فایل‌ها
COPY . .

EXPOSE 3000
CMD ["npm", "start"]
```

## 3.4 WORKDIR, ENV, ARG Instructions

این دستورات برای تنظیم محیط کاری، متغیرهای محیطی و آرگومان‌های ساخت استفاده می‌شوند.

### دستور WORKDIR:
```dockerfile
# تنظیم دایرکتوری کاری
WORKDIR /app
WORKDIR /usr/src/app

# ایجاد دایرکتوری‌های تو در تو
WORKDIR /app
WORKDIR src
# حالا در /app/src هستیم
```

### دستور ENV:
```dockerfile
# تنظیم متغیرهای محیطی
ENV NODE_ENV=production
ENV PORT=3000
ENV DATABASE_URL=postgres://localhost:5432/mydb

# استفاده از متغیرها
ENV NODE_ENV=production
ENV APP_HOME=/app
WORKDIR $APP_HOME
```

### دستور ARG:
```dockerfile
# تعریف آرگومان‌های ساخت
ARG NODE_VERSION=16
ARG BUILD_ENV=production

# استفاده از آرگومان‌ها
FROM node:${NODE_VERSION}-alpine
ENV NODE_ENV=${BUILD_ENV}
```

### مثال کامل:
```dockerfile
FROM node:16-alpine

# آرگومان‌های ساخت
ARG NODE_ENV=production
ARG PORT=3000

# متغیرهای محیطی
ENV NODE_ENV=${NODE_ENV}
ENV PORT=${PORT}
ENV APP_HOME=/app

# دایرکتوری کاری
WORKDIR $APP_HOME

# کپی و نصب وابستگی‌ها
COPY package*.json ./
RUN npm ci --only=production

# کپی کد اپلیکیشن
COPY . .

# اجرای اپلیکیشن
CMD ["npm", "start"]
```

## 3.5 EXPOSE, VOLUME Instructions

این دستورات برای تعریف پورت‌ها و حجم‌های ذخیره‌سازی استفاده می‌شوند.

### دستور EXPOSE:
```dockerfile
# تعریف پورت‌ها
EXPOSE 3000
EXPOSE 80 443
EXPOSE 8080/tcp
EXPOSE 8080/udp

# مثال کامل
FROM nginx:alpine
EXPOSE 80
EXPOSE 443
```

### دستور VOLUME:
```dockerfile
# تعریف volumeها
VOLUME ["/data"]
VOLUME ["/var/log"]
VOLUME ["/app/uploads"]

# مثال کامل
FROM postgres:13
VOLUME ["/var/lib/postgresql/data"]
```

### مثال عملی:
```dockerfile
FROM node:16-alpine

WORKDIR /app

# کپی و نصب وابستگی‌ها
COPY package*.json ./
RUN npm ci --only=production

# کپی کد اپلیکیشن
COPY . .

# تعریف پورت
EXPOSE 3000

# تعریف volume برای لاگ‌ها
VOLUME ["/app/logs"]

# تعریف volume برای داده‌های کاربر
VOLUME ["/app/uploads"]

CMD ["npm", "start"]
```

## 3.6 CMD vs ENTRYPOINT

این دستورات برای تعریف دستور پیش‌فرض کانتینر استفاده می‌شوند.

### دستور CMD:
```dockerfile
# فرم exec (پیشنهادی)
CMD ["npm", "start"]

# فرم shell
CMD npm start

# فقط یک CMD در Dockerfile
CMD ["node", "app.js"]
```

### دستور ENTRYPOINT:
```dockerfile
# فرم exec
ENTRYPOINT ["python", "app.py"]

# فرم shell
ENTRYPOINT python app.py

# ترکیب با CMD
ENTRYPOINT ["python", "app.py"]
CMD ["--help"]
```

### تفاوت‌های کلیدی:

#### **CMD:**
- قابل بازنویسی در docker run
- فقط آخرین CMD اجرا می‌شود
- مناسب برای دستورات پیش‌فرض

#### **ENTRYPOINT:**
- غیرقابل بازنویسی
- همیشه اجرا می‌شود
- مناسب برای executable

### مثال‌های عملی:

#### **استفاده از CMD:**
```dockerfile
FROM ubuntu:20.04
CMD ["echo", "Hello World"]
```
```bash
# قابل بازنویسی
docker run myimage echo "Hello Docker"
```

#### **استفاده از ENTRYPOINT:**
```dockerfile
FROM ubuntu:20.04
ENTRYPOINT ["echo"]
CMD ["Hello World"]
```
```bash
# ENTRYPOINT همیشه اجرا می‌شود
docker run myimage "Hello Docker"
```

#### **ترکیب ENTRYPOINT و CMD:**
```dockerfile
FROM node:16-alpine
ENTRYPOINT ["node"]
CMD ["app.js"]
```
```bash
# اجرای پیش‌فرض
docker run myimage
# خروجی: node app.js

# اجرای با آرگومان
docker run myimage server.js
# خروجی: node server.js
```

## 3.7 Multi-stage Builds

Multi-stage builds امکان استفاده از چندین مرحله ساخت در یک Dockerfile را فراهم می‌کند.

### مزایای Multi-stage:
- کاهش حجم ایمیج نهایی
- حذف ابزارهای build از ایمیج production
- بهبود امنیت
- بهینه‌سازی کش

### ساختار کلی:
```dockerfile
# Stage 1: Build
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### مثال کامل (React App):
```dockerfile
# Build stage
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### مثال Go Application:
```dockerfile
# Build stage
FROM golang:1.17-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Production stage
FROM alpine:3.14
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
CMD ["./main"]
```

## 3.8 Image Optimization

بهینه‌سازی ایمیج‌ها برای کاهش حجم، بهبود عملکرد و امنیت ضروری است.

### تکنیک‌های بهینه‌سازی:

#### **1. استفاده از ایمیج‌های کوچک:**
```dockerfile
# بد
FROM ubuntu:20.04

# خوب
FROM alpine:3.14
```

#### **2. ترکیب دستورات RUN:**
```dockerfile
# بد
RUN apt-get update
RUN apt-get install -y nginx
RUN apt-get clean

# خوب
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
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
```

#### **4. بهینه‌سازی ترتیب دستورات:**
```dockerfile
# کپی فایل‌های وابستگی اول
COPY package*.json ./
RUN npm ci --only=production

# سپس کپی کد اپلیکیشن
COPY . .
```

#### **5. استفاده از Multi-stage builds:**
```dockerfile
FROM node:16-alpine AS builder
# ... build steps

FROM node:16-alpine
COPY --from=builder /app/dist ./dist
```

### ابزارهای بهینه‌سازی:
```bash
# تحلیل ایمیج
docker history myimage

# اسکن امنیتی
docker scan myimage

# تحلیل لایه‌ها
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest myimage
```

## 3.9 Best Practices for Dockerfiles

رعایت بهترین روش‌ها برای ایجاد Dockerfileهای کارآمد و امن ضروری است.

### بهترین روش‌ها:

#### **1. استفاده از ایمیج‌های رسمی:**
```dockerfile
# خوب
FROM node:16-alpine
FROM python:3.9-slim

# بد
FROM ubuntu:20.04
RUN apt-get install -y nodejs
```

#### **2. تعیین نسخه مشخص:**
```dockerfile
# خوب
FROM node:16.14.0-alpine

# بد
FROM node:latest
```

#### **3. استفاده از کاربر غیر root:**
```dockerfile
FROM node:16-alpine
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs
```

#### **4. بهینه‌سازی کش:**
```dockerfile
# کپی فایل‌های وابستگی اول
COPY package*.json ./
RUN npm ci --only=production

# سپس کپی کد
COPY . .
```

#### **5. استفاده از .dockerignore:**
```dockerignore
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
```

#### **6. ترکیب دستورات RUN:**
```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
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

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی فایل‌های وابستگی
COPY package*.json ./

# نصب وابستگی‌ها
RUN npm ci --only=production && npm cache clean --force

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

## 3.10 Security Considerations

امنیت در Dockerfileها برای محافظت از اپلیکیشن‌ها و داده‌ها ضروری است.

### نکات امنیتی:

#### **1. استفاده از ایمیج‌های امن:**
```dockerfile
# خوب - ایمیج رسمی و به‌روز
FROM node:16-alpine

# بد - ایمیج قدیمی
FROM node:12
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
# حذف package manager cache
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

#### **4. استفاده از secrets:**
```dockerfile
# استفاده از build args برای secrets
ARG NPM_TOKEN
RUN echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc
```

#### **5. اسکن امنیتی:**
```bash
# اسکن ایمیج برای آسیب‌پذیری‌ها
docker scan myimage

# استفاده از Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image myimage
```

#### **6. محدود کردن capabilities:**
```dockerfile
# در docker run
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx
```

### مثال Dockerfile امن:
```dockerfile
FROM node:16.14.0-alpine

# به‌روزرسانی packages
RUN apk update && apk upgrade

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

این بخش شما را با تمام جنبه‌های ایجاد و بهینه‌سازی ایمیج‌های Docker آشنا می‌کند.