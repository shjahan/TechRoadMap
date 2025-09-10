# Section 1 – Docker Fundamentals

## 1.1 What is Docker

Docker یک پلتفرم کانتینری‌سازی است که به شما امکان بسته‌بندی، توزیع و اجرای اپلیکیشن‌ها را در محیط‌های ایزوله به نام کانتینر می‌دهد. Docker از تکنولوژی‌های مجازی‌سازی سطح سیستم عامل استفاده می‌کند تا اپلیکیشن‌ها را همراه با تمام وابستگی‌هایشان در یک واحد قابل حمل قرار دهد.

### مفاهیم کلیدی:
- **کانتینر**: یک واحد نرم‌افزاری سبک که شامل کد، runtime، کتابخانه‌ها و تنظیمات است
- **ایمیج**: یک الگوی فقط خواندنی که برای ایجاد کانتینرها استفاده می‌شود
- **Dockerfile**: فایل متنی که دستورالعمل‌های ساخت ایمیج را شامل می‌شود

### مثال عملی:
```bash
# ایجاد یک کانتینر ساده از ایمیج nginx
docker run -d -p 8080:80 nginx
```

### آنالوژی دنیای واقعی:
کانتینرها مانند جعبه‌های حمل و نقل استاندارد هستند که می‌توانند هر نوع محتوایی را حمل کنند و در هر کشتی (سرور) قابل استفاده هستند.

## 1.2 Docker vs Virtual Machines

تفاوت اصلی بین Docker و ماشین‌های مجازی در نحوه استفاده از منابع سیستم است.

### ماشین‌های مجازی (VMs):
- هر VM یک سیستم عامل کامل دارد
- نیاز به Hypervisor دارد
- مصرف منابع بالا (CPU، RAM، Storage)
- راه‌اندازی کند

### کانتینرهای Docker:
- از هسته سیستم عامل میزبان استفاده می‌کنند
- سبک‌تر و سریع‌تر
- مصرف منابع کمتر
- راه‌اندازی سریع

### مقایسه منابع:
```
VM: Host OS → Hypervisor → Guest OS → App
Docker: Host OS → Docker Engine → App
```

### مثال عملی:
```bash
# راه‌اندازی کانتینر (چند ثانیه)
docker run nginx

# راه‌اندازی VM (چند دقیقه)
# نیاز به نصب کامل سیستم عامل
```

## 1.3 Docker History and Evolution

Docker در سال 2013 توسط Solomon Hykes در شرکت dotCloud معرفی شد و انقلابی در دنیای کانتینری‌سازی ایجاد کرد.

### تاریخچه کلیدی:
- **2013**: معرفی Docker
- **2014**: انتشار Docker 1.0
- **2015**: معرفی Docker Compose
- **2016**: Docker Swarm برای orchestration
- **2017**: Docker for Mac/Windows
- **2018**: Docker Enterprise Edition
- **2020**: Docker Desktop و BuildKit

### تأثیر بر صنعت:
- استانداردسازی کانتینری‌سازی
- تسهیل DevOps و CI/CD
- انقلاب در میکروسرویس‌ها
- تغییر پارادایم deployment

## 1.4 Containerization Benefits

کانتینری‌سازی مزایای متعددی برای توسعه و استقرار نرم‌افزار دارد.

### مزایای اصلی:

#### 1. **Portability (قابلیت حمل)**
```bash
# همان ایمیج در محیط‌های مختلف
docker run myapp  # در development
docker run myapp  # در production
```

#### 2. **Consistency (سازگاری)**
- محیط یکسان در تمام مراحل
- حذف مشکل "در سیستم من کار می‌کند"

#### 3. **Scalability (مقیاس‌پذیری)**
```bash
# مقیاس‌دهی آسان
docker-compose up --scale web=5
```

#### 4. **Resource Efficiency (بهره‌وری منابع)**
- استفاده بهینه از CPU و RAM
- راه‌اندازی سریع

#### 5. **Isolation (جداسازی)**
- اپلیکیشن‌های مستقل
- امنیت بهتر

### مثال عملی:
```yaml
# docker-compose.yml
version: '3'
services:
  web:
    image: nginx
    ports:
      - "80:80"
  database:
    image: postgres
    environment:
      POSTGRES_DB: myapp
```

## 1.5 Docker Architecture

معماری Docker شامل چندین کامپوننت اصلی است که با هم کار می‌کنند.

### کامپوننت‌های اصلی:

#### 1. **Docker Client**
- رابط خط فرمان
- ارسال دستورات به Docker daemon

#### 2. **Docker Daemon (dockerd)**
- سرویس پس‌زمینه
- مدیریت کانتینرها و ایمیج‌ها

#### 3. **Docker Registry**
- مخزن ایمیج‌ها
- Docker Hub (عمومی) یا Private Registry

#### 4. **Docker Objects**
- Images (ایمیج‌ها)
- Containers (کانتینرها)
- Networks (شبکه‌ها)
- Volumes (حجم‌ها)

### نمودار معماری:
```
Client → Docker Daemon → Registry
         ↓
    Containers ← Images
```

### مثال عملی:
```bash
# Client command
docker pull nginx

# Daemon process
# 1. دریافت درخواست از Client
# 2. دانلود ایمیج از Registry
# 3. ذخیره ایمیج محلی
```

## 1.6 Docker Installation and Setup

نصب Docker در سیستم‌های مختلف متفاوت است اما روند کلی مشابه است.

### نصب در Windows:
1. دانلود Docker Desktop
2. نصب و راه‌اندازی
3. فعال‌سازی WSL2 (اختیاری)

### نصب در Linux:
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# CentOS/RHEL
sudo yum install docker-ce
```

### نصب در macOS:
1. دانلود Docker Desktop for Mac
2. نصب از فایل .dmg
3. راه‌اندازی از Applications

### بررسی نصب:
```bash
# بررسی نسخه Docker
docker --version

# بررسی وضعیت سرویس
docker info

# تست با Hello World
docker run hello-world
```

### تنظیمات اولیه:
```bash
# اضافه کردن کاربر به گروه docker
sudo usermod -aG docker $USER

# راه‌اندازی سرویس
sudo systemctl start docker
sudo systemctl enable docker
```

## 1.7 Docker Concepts and Terminology

درک اصطلاحات Docker برای کار مؤثر با آن ضروری است.

### اصطلاحات کلیدی:

#### **Image (ایمیج)**
- الگوی فقط خواندنی
- شامل کد، runtime، کتابخانه‌ها
- پایه ایجاد کانتینرها

#### **Container (کانتینر)**
- نمونه اجرایی ایمیج
- قابل اجرا، متوقف، حذف
- ایزوله از سایر کانتینرها

#### **Dockerfile**
- فایل متنی با دستورالعمل‌ها
- برای ساخت ایمیج سفارشی
- شامل دستورات RUN، COPY، CMD

#### **Registry**
- مخزن ایمیج‌ها
- Docker Hub (عمومی)
- Private Registry (خصوصی)

#### **Volume**
- ذخیره‌سازی دائمی
- اشتراک داده بین کانتینر و میزبان
- پشتیبان‌گیری و بازیابی

### مثال عملی:
```dockerfile
# Dockerfile
FROM ubuntu:20.04
RUN apt-get update
COPY app.py /app/
CMD ["python", "/app/app.py"]
```

## 1.8 Docker Ecosystem

اکوسیستم Docker شامل ابزارها و تکنولوژی‌های متعددی است.

### ابزارهای اصلی:

#### **Docker Compose**
- مدیریت چندین کانتینر
- فایل YAML برای تنظیمات
- مناسب برای development

#### **Docker Swarm**
- اورکستراسیون کانتینرها
- مدیریت cluster
- Load balancing

#### **Kubernetes**
- پلتفرم اورکستراسیون پیشرفته
- Auto-scaling
- Service discovery

#### **Docker Registry**
- Docker Hub
- Amazon ECR
- Google Container Registry
- Azure Container Registry

### ابزارهای کمکی:
- **Portainer**: رابط گرافیکی
- **Docker Desktop**: محیط توسعه
- **Docker Machine**: مدیریت ماشین‌ها
- **Docker Buildx**: ساخت چندپلتفرمه

### مثال استفاده:
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
```

این بخش پایه‌ای برای درک Docker فراهم می‌کند و شما را برای یادگیری مفاهیم پیشرفته‌تر آماده می‌سازد.