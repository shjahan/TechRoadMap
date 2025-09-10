# Section 5 – Docker Networking

## 5.1 Docker Network Types

Docker از انواع مختلف شبکه‌ها برای ارتباط کانتینرها استفاده می‌کند. هر نوع شبکه ویژگی‌ها و کاربردهای خاص خود را دارد.

### انواع شبکه‌های Docker:

#### **1. Bridge Network (پیش‌فرض)**
- شبکه مجازی داخلی
- کانتینرها می‌توانند با یکدیگر ارتباط برقرار کنند
- دسترسی به اینترنت از طریق NAT

#### **2. Host Network**
- استفاده مستقیم از شبکه میزبان
- عملکرد بهتر
- امنیت کمتر

#### **3. None Network**
- بدون شبکه
- کانتینر کاملاً ایزوله
- مناسب برای کانتینرهای خاص

#### **4. Overlay Network**
- شبکه توزیع‌شده
- مناسب برای Docker Swarm
- ارتباط بین nodeهای مختلف

#### **5. Macvlan Network**
- اختصاص IP واقعی به کانتینر
- کانتینر مستقیماً در شبکه فیزیکی
- عملکرد بالا

### دستورات مدیریت شبکه:

```bash
# مشاهده شبکه‌ها
docker network ls

# ایجاد شبکه جدید
docker network create my-network

# حذف شبکه
docker network rm my-network

# مشاهده جزئیات شبکه
docker network inspect my-network
```

### مثال‌های عملی:

#### **Bridge Network:**
```bash
# ایجاد شبکه bridge
docker network create --driver bridge my-bridge

# اجرای کانتینر در شبکه
docker run -d --name web --network my-bridge nginx
docker run -d --name db --network my-bridge postgres
```

#### **Host Network:**
```bash
# اجرای کانتینر با host network
docker run -d --name web --network host nginx
```

## 5.2 Bridge Networks

شبکه‌های Bridge رایج‌ترین نوع شبکه در Docker هستند و برای ارتباط کانتینرها با یکدیگر و اینترنت استفاده می‌شوند.

### ویژگی‌های Bridge Network:
- **Isolation**: جداسازی کانتینرها از شبکه میزبان
- **Communication**: امکان ارتباط بین کانتینرها
- **Internet Access**: دسترسی به اینترنت از طریق NAT
- **Port Mapping**: نقشه‌برداری پورت‌ها

### ایجاد Bridge Network:

```bash
# ایجاد شبکه bridge ساده
docker network create my-bridge

# ایجاد شبکه با تنظیمات خاص
docker network create \
  --driver bridge \
  --subnet=172.20.0.0/16 \
  --ip-range=172.20.240.0/20 \
  my-bridge
```

### مثال عملی:

#### **Web Application Stack:**
```bash
# ایجاد شبکه
docker network create web-stack

# اجرای دیتابیس
docker run -d \
  --name postgres \
  --network web-stack \
  -e POSTGRES_PASSWORD=password \
  postgres:13

# اجرای Redis
docker run -d \
  --name redis \
  --network web-stack \
  redis:alpine

# اجرای اپلیکیشن
docker run -d \
  --name web-app \
  --network web-stack \
  -p 3000:3000 \
  my-app:latest
```

### Docker Compose با Bridge Network:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    networks:
      - web-stack
    ports:
      - "80:80"
  db:
    image: postgres:13
    networks:
      - web-stack
    environment:
      POSTGRES_PASSWORD: password
  redis:
    image: redis:alpine
    networks:
      - web-stack

networks:
  web-stack:
    driver: bridge
```

## 5.3 Host Networks

شبکه Host به کانتینرها امکان استفاده مستقیم از شبکه میزبان را می‌دهد.

### ویژگی‌های Host Network:
- **Performance**: عملکرد بهتر (بدون NAT)
- **Simplicity**: سادگی در تنظیمات
- **Security**: امنیت کمتر
- **Port Conflicts**: امکان تداخل پورت

### استفاده از Host Network:

```bash
# اجرای کانتینر با host network
docker run -d --name web --network host nginx

# اجرای چندین کانتینر (ممکن است تداخل پورت داشته باشد)
docker run -d --name web1 --network host nginx
docker run -d --name web2 --network host nginx  # خطا: پورت 80 قبلاً استفاده شده
```

### مثال عملی:

#### **High-Performance Web Server:**
```bash
# اجرای nginx با host network
docker run -d \
  --name nginx \
  --network host \
  nginx:alpine

# دسترسی مستقیم: http://localhost:80
```

#### **Database Server:**
```bash
# اجرای PostgreSQL با host network
docker run -d \
  --name postgres \
  --network host \
  -e POSTGRES_PASSWORD=password \
  postgres:13

# اتصال مستقیم: localhost:5432
```

### Docker Compose با Host Network:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    network_mode: host
  db:
    image: postgres:13
    network_mode: host
    environment:
      POSTGRES_PASSWORD: password
```

## 5.4 Overlay Networks

شبکه‌های Overlay برای ارتباط کانتینرها در محیط‌های توزیع‌شده مانند Docker Swarm استفاده می‌شوند.

### ویژگی‌های Overlay Network:
- **Distributed**: توزیع‌شده بین چندین node
- **Encryption**: رمزنگاری ترافیک
- **Service Discovery**: کشف خودکار سرویس‌ها
- **Load Balancing**: توزیع بار

### ایجاد Overlay Network:

```bash
# ایجاد overlay network (نیاز به Swarm)
docker network create \
  --driver overlay \
  --attachable \
  my-overlay
```

### مثال عملی:

#### **Docker Swarm Stack:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    networks:
      - web-overlay
    deploy:
      replicas: 3
  db:
    image: postgres:13
    networks:
      - web-overlay
    environment:
      POSTGRES_PASSWORD: password

networks:
  web-overlay:
    driver: overlay
    attachable: true
```

### دستورات Swarm:
```bash
# راه‌اندازی Swarm
docker swarm init

# ایجاد overlay network
docker network create --driver overlay web-overlay

# اجرای stack
docker stack deploy -c docker-compose.yml my-stack
```

## 5.5 Macvlan Networks

شبکه‌های Macvlan به کانتینرها امکان اختصاص IP واقعی و ارتباط مستقیم با شبکه فیزیکی را می‌دهند.

### ویژگی‌های Macvlan Network:
- **Real IP**: IP واقعی برای کانتینر
- **High Performance**: عملکرد بالا
- **Direct Access**: دسترسی مستقیم به شبکه
- **Complex Setup**: تنظیمات پیچیده

### ایجاد Macvlan Network:

```bash
# ایجاد macvlan network
docker network create \
  --driver macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  my-macvlan
```

### مثال عملی:

#### **Container with Real IP:**
```bash
# اجرای کانتینر با IP واقعی
docker run -d \
  --name web \
  --network my-macvlan \
  --ip=192.168.1.100 \
  nginx:alpine

# دسترسی مستقیم: http://192.168.1.100
```

### Docker Compose با Macvlan:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    networks:
      my-macvlan:
        ipv4_address: 192.168.1.100

networks:
  my-macvlan:
    driver: macvlan
    driver_opts:
      parent: eth0
    ipam:
      config:
        - subnet: 192.168.1.0/24
          gateway: 192.168.1.1
```

## 5.6 Custom Networks

شبکه‌های سفارشی برای نیازهای خاص و کنترل دقیق‌تر بر تنظیمات شبکه استفاده می‌شوند.

### ایجاد Custom Network:

```bash
# ایجاد شبکه سفارشی با تنظیمات کامل
docker network create \
  --driver bridge \
  --subnet=172.20.0.0/16 \
  --ip-range=172.20.240.0/20 \
  --gateway=172.20.0.1 \
  --opt com.docker.network.bridge.name=my-bridge \
  --opt com.docker.network.bridge.enable_icc=true \
  --opt com.docker.network.bridge.enable_ip_masquerade=true \
  --opt com.docker.network.bridge.host_binding_ipv4=0.0.0.0 \
  --opt com.docker.network.driver.mtu=1500 \
  my-custom-network
```

### مثال عملی:

#### **Development Environment:**
```bash
# ایجاد شبکه development
docker network create \
  --driver bridge \
  --subnet=172.20.0.0/16 \
  --gateway=172.20.0.1 \
  dev-network

# اجرای سرویس‌ها
docker run -d --name frontend --network dev-network -p 3000:3000 react-app
docker run -d --name backend --network dev-network -p 8000:8000 node-api
docker run -d --name database --network dev-network -p 5432:5432 postgres:13
```

### Docker Compose با Custom Network:
```yaml
version: '3.8'
services:
  frontend:
    image: react-app:latest
    networks:
      - dev-network
    ports:
      - "3000:3000"
  backend:
    image: node-api:latest
    networks:
      - dev-network
    ports:
      - "8000:8000"
  database:
    image: postgres:13
    networks:
      - dev-network
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: password

networks:
  dev-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1
```

## 5.7 Network Security

امنیت شبکه‌ها برای محافظت از کانتینرها و داده‌ها ضروری است.

### اصول امنیت شبکه:

#### **1. Network Isolation:**
```bash
# ایجاد شبکه جداگانه برای هر سرویس
docker network create frontend-network
docker network create backend-network
docker network create database-network
```

#### **2. Firewall Rules:**
```bash
# محدود کردن دسترسی
docker run -d \
  --name web \
  --network frontend-network \
  nginx

# فقط کانتینرهای frontend-network می‌توانند به web دسترسی داشته باشند
```

#### **3. Encryption:**
```bash
# ایجاد overlay network با encryption
docker network create \
  --driver overlay \
  --opt encrypted \
  secure-overlay
```

### مثال عملی:

#### **Secure Multi-Tier Application:**
```yaml
version: '3.8'
services:
  frontend:
    image: nginx:alpine
    networks:
      - frontend-network
    ports:
      - "80:80"
  
  backend:
    image: node-api:latest
    networks:
      - frontend-network
      - backend-network
  
  database:
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
    internal: true  # بدون دسترسی به اینترنت
```

## 5.8 Service Discovery

کشف سرویس‌ها برای ارتباط خودکار بین کانتینرها ضروری است.

### روش‌های Service Discovery:

#### **1. DNS-based Discovery:**
```bash
# کانتینرها می‌توانند با نام یکدیگر ارتباط برقرار کنند
docker run -d --name web nginx
docker run -d --name app --link web:web-service my-app

# در کانتینر app: curl http://web-service
```

#### **2. Environment Variables:**
```bash
# ارسال اطلاعات سرویس از طریق متغیرهای محیطی
docker run -d \
  --name app \
  -e DATABASE_URL=postgres://db:5432/mydb \
  -e REDIS_URL=redis://redis:6379 \
  my-app
```

### مثال عملی:

#### **Microservices Communication:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    networks:
      - app-network
  
  api:
    image: node-api:latest
    networks:
      - app-network
    environment:
      - DATABASE_URL=postgres://db:5432/mydb
      - REDIS_URL=redis://redis:6379
  
  db:
    image: postgres:13
    networks:
      - app-network
    environment:
      POSTGRES_PASSWORD: password
  
  redis:
    image: redis:alpine
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

## 5.9 Load Balancing

توزیع بار برای مدیریت ترافیک و بهبود عملکرد ضروری است.

### روش‌های Load Balancing:

#### **1. Docker Swarm Load Balancing:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      replicas: 3
    networks:
      - web-network

networks:
  web-network:
    driver: overlay
```

#### **2. Nginx Load Balancer:**
```yaml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    networks:
      - web-network
  
  web1:
    image: my-app:latest
    networks:
      - web-network
  
  web2:
    image: my-app:latest
    networks:
      - web-network

networks:
  web-network:
    driver: bridge
```

### فایل nginx.conf:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server web1:3000;
        server web2:3000;
    }
    
    server {
        listen 80;
        location / {
            proxy_pass http://backend;
        }
    }
}
```

## 5.10 Network Troubleshooting

عیب‌یابی مشکلات شبکه برای حل مسائل ارتباطی ضروری است.

### دستورات عیب‌یابی:

#### **1. بررسی وضعیت شبکه:**
```bash
# مشاهده شبکه‌ها
docker network ls

# بررسی جزئیات شبکه
docker network inspect my-network

# مشاهده کانتینرهای متصل
docker network inspect my-network | grep -A 10 "Containers"
```

#### **2. تست اتصال:**
```bash
# تست ping بین کانتینرها
docker exec -it web ping db

# تست اتصال به پورت
docker exec -it web telnet db 5432

# تست DNS resolution
docker exec -it web nslookup db
```

#### **3. بررسی لاگ‌ها:**
```bash
# لاگ‌های Docker daemon
journalctl -u docker.service

# لاگ‌های کانتینر
docker logs web

# لاگ‌های شبکه
docker logs $(docker ps -q --filter name=web)
```

### مثال‌های عیب‌یابی:

#### **مشکل اتصال بین کانتینرها:**
```bash
# بررسی شبکه
docker network ls
docker network inspect my-network

# بررسی IP کانتینرها
docker inspect web | grep IPAddress
docker inspect db | grep IPAddress

# تست اتصال
docker exec -it web ping db
```

#### **مشکل دسترسی به اینترنت:**
```bash
# بررسی DNS
docker exec -it web nslookup google.com

# بررسی routing
docker exec -it web ip route

# بررسی iptables
sudo iptables -L
```

### اسکریپت عیب‌یابی:
```bash
#!/bin/bash
# network-troubleshoot.sh

echo "=== Docker Network Troubleshooting ==="

echo "1. Network List:"
docker network ls

echo "2. Container Networks:"
docker ps --format "table {{.Names}}\t{{.Networks}}"

echo "3. Network Details:"
docker network inspect bridge

echo "4. Container IPs:"
docker inspect $(docker ps -q) | grep -E '"Name"|"IPAddress"'

echo "5. Testing Connectivity:"
docker exec -it web ping -c 3 db
```

این بخش شما را با تمام جنبه‌های شبکه‌بندی Docker آشنا می‌کند.