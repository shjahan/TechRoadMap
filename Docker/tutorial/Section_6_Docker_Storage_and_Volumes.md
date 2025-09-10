# Section 6 – Docker Storage and Volumes

## 6.1 Docker Storage Drivers

Storage Driverها مسئول مدیریت نحوه ذخیره‌سازی داده‌ها در Docker هستند. هر driver ویژگی‌ها و محدودیت‌های خاص خود را دارد.

### انواع Storage Drivers:

#### **1. Overlay2 (پیش‌فرض)**
- بهترین عملکرد
- پشتیبانی از copy-on-write
- مناسب برای اکثر موارد

#### **2. Device Mapper**
- مناسب برای production
- پشتیبانی از thin provisioning
- پیچیدگی بیشتر

#### **3. Btrfs**
- پشتیبانی از snapshot
- مناسب برای development
- نیاز به filesystem خاص

#### **4. ZFS**
- پشتیبانی از compression
- مناسب برای enterprise
- نیاز به ZFS filesystem

### بررسی Storage Driver:

```bash
# مشاهده storage driver
docker info | grep "Storage Driver"

# مشاهده جزئیات storage
docker system df

# مشاهده اطلاعات storage driver
docker info | grep -A 10 "Storage Driver"
```

### تغییر Storage Driver:

```bash
# در /etc/docker/daemon.json
{
  "storage-driver": "overlay2"
}

# راه‌اندازی مجدد Docker
sudo systemctl restart docker
```

### مثال عملی:

#### **بررسی Storage Driver:**
```bash
# بررسی driver فعلی
docker info | grep "Storage Driver"
# خروجی: Storage Driver: overlay2

# مشاهده استفاده از فضای دیسک
docker system df
# خروجی:
# TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
# Images          5         5         1.2GB     0B (0%)
# Containers      3         3         0B        0B (0%)
# Local Volumes   2         2         100MB     0B (0%)
# Build Cache     0         0         0B        0B (0%)
```

## 6.2 Bind Mounts

Bind Mounts امکان اتصال مستقیم پوشه یا فایل میزبان به کانتینر را فراهم می‌کند.

### ویژگی‌های Bind Mounts:
- **Direct Access**: دسترسی مستقیم به فایل‌های میزبان
- **Real-time Sync**: همگام‌سازی لحظه‌ای
- **Development Friendly**: مناسب برای development
- **Security Risk**: ریسک امنیتی بالاتر

### استفاده از Bind Mounts:

```bash
# نصب پوشه
docker run -v /host/path:/container/path nginx

# نصب فایل
docker run -v /host/file.txt:/container/file.txt nginx

# نصب با دسترسی فقط خواندنی
docker run -v /host/path:/container/path:ro nginx
```

### مثال‌های عملی:

#### **Development Environment:**
```bash
# نصب کد source
docker run -d \
  --name dev-app \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/public:/app/public \
  -p 3000:3000 \
  my-app:latest
```

#### **Configuration Files:**
```bash
# نصب فایل تنظیمات
docker run -d \
  --name nginx \
  -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
  -p 80:80 \
  nginx:alpine
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

### Docker Compose با Bind Mounts:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./html:/usr/share/nginx/html:ro
    ports:
      - "80:80"
  
  app:
    image: my-app:latest
    volumes:
      - ./src:/app/src
      - ./public:/app/public
    ports:
      - "3000:3000"
```

## 6.3 Named Volumes

Named Volumes توسط Docker مدیریت می‌شوند و برای ذخیره‌سازی دائمی داده‌ها استفاده می‌شوند.

### ویژگی‌های Named Volumes:
- **Managed by Docker**: مدیریت شده توسط Docker
- **Portable**: قابل حمل بین کانتینرها
- **Secure**: امن‌تر از Bind Mounts
- **Backup Friendly**: مناسب برای پشتیبان‌گیری

### استفاده از Named Volumes:

```bash
# ایجاد volume
docker volume create my-volume

# استفاده از volume
docker run -v my-volume:/data nginx

# مشاهده volumeها
docker volume ls

# مشاهده جزئیات volume
docker volume inspect my-volume
```

### مثال‌های عملی:

#### **Database Storage:**
```bash
# ایجاد volume برای دیتابیس
docker volume create postgres-data

# اجرای PostgreSQL با volume
docker run -d \
  --name postgres \
  -v postgres-data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=password \
  postgres:13
```

#### **Application Data:**
```bash
# ایجاد volume برای داده‌های اپلیکیشن
docker volume create app-data

# اجرای اپلیکیشن با volume
docker run -d \
  --name my-app \
  -v app-data:/app/data \
  my-app:latest
```

### Docker Compose با Named Volumes:
```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: password
  
  app:
    image: my-app:latest
    volumes:
      - app-data:/app/data
    depends_on:
      - db

volumes:
  postgres-data:
  app-data:
```

## 6.4 Volume Drivers

Volume Driverها امکان استفاده از سیستم‌های ذخیره‌سازی مختلف را فراهم می‌کنند.

### انواع Volume Drivers:

#### **1. Local Driver (پیش‌فرض)**
```bash
# ایجاد volume با local driver
docker volume create --driver local my-volume
```

#### **2. NFS Driver**
```bash
# ایجاد volume با NFS
docker volume create \
  --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.100,rw \
  --opt device=:/path/to/nfs \
  nfs-volume
```

#### **3. CIFS Driver**
```bash
# ایجاد volume با CIFS
docker volume create \
  --driver local \
  --opt type=cifs \
  --opt device=//server/share \
  --opt o=username=user,password=pass \
  cifs-volume
```

### مثال‌های عملی:

#### **NFS Volume:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    volumes:
      - nfs-volume:/usr/share/nginx/html

volumes:
  nfs-volume:
    driver: local
    driver_opts:
      type: nfs
      o: addr=192.168.1.100,rw
      device: ":/path/to/nfs"
```

#### **CIFS Volume:**
```yaml
version: '3.8'
services:
  app:
    image: my-app:latest
    volumes:
      - cifs-volume:/app/data

volumes:
  cifs-volume:
    driver: local
    driver_opts:
      type: cifs
      device: "//server/share"
      o: "username=user,password=pass"
```

## 6.5 Data Persistence

حفظ داده‌ها برای اطمینان از عدم از دست رفتن اطلاعات ضروری است.

### روش‌های حفظ داده‌ها:

#### **1. Named Volumes:**
```bash
# ایجاد volume برای داده‌های مهم
docker volume create important-data

# استفاده از volume
docker run -v important-data:/data my-app
```

#### **2. Bind Mounts:**
```bash
# نصب پوشه مهم
docker run -v /important/data:/data my-app
```

#### **3. Backup Strategy:**
```bash
# پشتیبان‌گیری از volume
docker run --rm \
  -v important-data:/data \
  -v $(pwd):/backup \
  ubuntu \
  tar czf /backup/backup.tar.gz /data
```

### مثال عملی:

#### **Database Backup:**
```bash
# پشتیبان‌گیری از PostgreSQL
docker run --rm \
  -v postgres-data:/var/lib/postgresql/data \
  -v $(pwd):/backup \
  postgres:13 \
  pg_dump -U postgres mydb > /backup/db-backup.sql
```

#### **Application Data Backup:**
```bash
# پشتیبان‌گیری از داده‌های اپلیکیشن
docker run --rm \
  -v app-data:/data \
  -v $(pwd):/backup \
  ubuntu \
  tar czf /backup/app-data-backup.tar.gz /data
```

### اسکریپت پشتیبان‌گیری:
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)

# پشتیبان‌گیری از PostgreSQL
docker run --rm \
  -v postgres-data:/var/lib/postgresql/data \
  -v $BACKUP_DIR:/backup \
  postgres:13 \
  pg_dump -U postgres mydb > /backup/postgres_$DATE.sql

# پشتیبان‌گیری از داده‌های اپلیکیشن
docker run --rm \
  -v app-data:/data \
  -v $BACKUP_DIR:/backup \
  ubuntu \
  tar czf /backup/app-data_$DATE.tar.gz /data

echo "Backup completed: $DATE"
```

## 6.6 Backup and Restore

استراتژی‌های پشتیبان‌گیری و بازیابی برای محافظت از داده‌ها ضروری است.

### روش‌های پشتیبان‌گیری:

#### **1. Volume Backup:**
```bash
# پشتیبان‌گیری از volume
docker run --rm \
  -v my-volume:/data \
  -v $(pwd):/backup \
  ubuntu \
  tar czf /backup/volume-backup.tar.gz /data
```

#### **2. Container Backup:**
```bash
# پشتیبان‌گیری از کانتینر
docker commit container_id backup-image:latest
docker save backup-image:latest > backup-image.tar
```

#### **3. Full System Backup:**
```bash
# پشتیبان‌گیری کامل
docker system df
docker save $(docker images -q) > all-images.tar
```

### روش‌های بازیابی:

#### **1. Volume Restore:**
```bash
# بازیابی volume
docker run --rm \
  -v my-volume:/data \
  -v $(pwd):/backup \
  ubuntu \
  tar xzf /backup/volume-backup.tar.gz -C /
```

#### **2. Container Restore:**
```bash
# بازیابی کانتینر
docker load < backup-image.tar
docker run -d backup-image:latest
```

### مثال عملی:

#### **Database Backup and Restore:**
```bash
# پشتیبان‌گیری
docker run --rm \
  -v postgres-data:/var/lib/postgresql/data \
  -v $(pwd):/backup \
  postgres:13 \
  pg_dump -U postgres mydb > /backup/db-backup.sql

# بازیابی
docker run --rm \
  -v postgres-data:/var/lib/postgresql/data \
  -v $(pwd):/backup \
  postgres:13 \
  psql -U postgres mydb < /backup/db-backup.sql
```

### اسکریپت کامل Backup/Restore:
```bash
#!/bin/bash
# backup-restore.sh

case $1 in
  backup)
    echo "Starting backup..."
    docker run --rm \
      -v postgres-data:/var/lib/postgresql/data \
      -v $(pwd):/backup \
      postgres:13 \
      pg_dump -U postgres mydb > /backup/db-backup-$(date +%Y%m%d_%H%M%S).sql
    echo "Backup completed"
    ;;
  restore)
    if [ -z "$2" ]; then
      echo "Usage: $0 restore <backup-file>"
      exit 1
    fi
    echo "Starting restore from $2..."
    docker run --rm \
      -v postgres-data:/var/lib/postgresql/data \
      -v $(pwd):/backup \
      postgres:13 \
      psql -U postgres mydb < /backup/$2
    echo "Restore completed"
    ;;
  *)
    echo "Usage: $0 {backup|restore <file>}"
    exit 1
    ;;
esac
```

## 6.7 Storage Optimization

بهینه‌سازی ذخیره‌سازی برای کاهش مصرف فضای دیسک و بهبود عملکرد ضروری است.

### تکنیک‌های بهینه‌سازی:

#### **1. Image Optimization:**
```dockerfile
# استفاده از ایمیج‌های کوچک
FROM alpine:3.14

# ترکیب دستورات RUN
RUN apk update && \
    apk add --no-cache nginx && \
    rm -rf /var/cache/apk/*
```

#### **2. Volume Optimization:**
```bash
# استفاده از volumeهای مشترک
docker volume create shared-data
docker run -v shared-data:/data1 app1
docker run -v shared-data:/data2 app2
```

#### **3. Cleanup:**
```bash
# پاکسازی منابع بدون استفاده
docker system prune -a --volumes

# پاکسازی ایمیج‌های بدون استفاده
docker image prune -a

# پاکسازی volumeهای بدون استفاده
docker volume prune
```

### مثال عملی:

#### **Multi-stage Build:**
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
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### **Volume Sharing:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    volumes:
      - shared-data:/usr/share/nginx/html
  
  app:
    image: my-app:latest
    volumes:
      - shared-data:/app/public

volumes:
  shared-data:
```

## 6.8 Volume Security

امنیت volumeها برای محافظت از داده‌های حساس ضروری است.

### اصول امنیت Volume:

#### **1. Access Control:**
```bash
# محدود کردن دسترسی به volume
docker run -v my-volume:/data:ro nginx

# استفاده از کاربر غیر root
docker run --user 1000:1000 -v my-volume:/data nginx
```

#### **2. Encryption:**
```bash
# ایجاد volume با encryption
docker volume create \
  --driver local \
  --opt type=tmpfs \
  --opt device=tmpfs \
  --opt o=size=1g,noexec,nosuid,nodev \
  secure-volume
```

#### **3. Backup Security:**
```bash
# پشتیبان‌گیری با encryption
docker run --rm \
  -v my-volume:/data \
  -v $(pwd):/backup \
  ubuntu \
  tar czf /backup/backup.tar.gz /data && \
  gpg --symmetric --cipher-algo AES256 /backup/backup.tar.gz
```

### مثال عملی:

#### **Secure Database Volume:**
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:13
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: password
    user: "999:999"  # postgres user

volumes:
  postgres-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /secure/postgres-data
```

## 6.9 Distributed Storage

ذخیره‌سازی توزیع‌شده برای محیط‌های کلان‌مقیاس ضروری است.

### راه‌حل‌های Distributed Storage:

#### **1. NFS:**
```yaml
version: '3.8'
services:
  app:
    image: my-app:latest
    volumes:
      - nfs-volume:/data

volumes:
  nfs-volume:
    driver: local
    driver_opts:
      type: nfs
      o: addr=192.168.1.100,rw
      device: ":/path/to/nfs"
```

#### **2. Ceph:**
```yaml
version: '3.8'
services:
  app:
    image: my-app:latest
    volumes:
      - ceph-volume:/data

volumes:
  ceph-volume:
    driver: rexray/ceph
    driver_opts:
      cephfs: true
      cephfsRoot: /data
```

#### **3. GlusterFS:**
```yaml
version: '3.8'
services:
  app:
    image: my-app:latest
    volumes:
      - gluster-volume:/data

volumes:
  gluster-volume:
    driver: local
    driver_opts:
      type: glusterfs
      device: "192.168.1.100:/gv0"
```

### مثال عملی:

#### **Multi-Node Storage:**
```yaml
version: '3.8'
services:
  web1:
    image: nginx:alpine
    volumes:
      - shared-storage:/usr/share/nginx/html
    deploy:
      placement:
        constraints:
          - node.hostname == node1
  
  web2:
    image: nginx:alpine
    volumes:
      - shared-storage:/usr/share/nginx/html
    deploy:
      placement:
        constraints:
          - node.hostname == node2

volumes:
  shared-storage:
    driver: local
    driver_opts:
      type: nfs
      o: addr=192.168.1.100,rw
      device: ":/shared"
```

## 6.10 Storage Monitoring

نظارت بر ذخیره‌سازی برای مدیریت منابع و تشخیص مشکلات ضروری است.

### دستورات نظارت:

#### **1. بررسی استفاده از فضای دیسک:**
```bash
# مشاهده استفاده از فضای دیسک
docker system df

# مشاهده جزئیات
docker system df -v
```

#### **2. بررسی Volumeها:**
```bash
# لیست volumeها
docker volume ls

# جزئیات volume
docker volume inspect my-volume

# استفاده از volume
docker run --rm -v my-volume:/data ubuntu du -sh /data
```

#### **3. نظارت بر I/O:**
```bash
# نظارت بر I/O کانتینر
docker stats container_id

# نظارت بر I/O volume
docker run --rm -v my-volume:/data ubuntu iostat -x 1
```

### مثال عملی:

#### **Storage Monitoring Script:**
```bash
#!/bin/bash
# storage-monitor.sh

echo "=== Docker Storage Monitoring ==="

echo "1. System Storage Usage:"
docker system df

echo "2. Volume Usage:"
for volume in $(docker volume ls -q); do
  echo "Volume: $volume"
  docker run --rm -v $volume:/data ubuntu du -sh /data 2>/dev/null || echo "  Cannot access volume"
done

echo "3. Container Storage:"
docker ps --format "table {{.Names}}\t{{.Size}}"

echo "4. Image Storage:"
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

### Docker Compose با Monitoring:
```yaml
version: '3.8'
services:
  app:
    image: my-app:latest
    volumes:
      - app-data:/data
  
  monitoring:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"

volumes:
  app-data:
  prometheus-data:
```

این بخش شما را با تمام جنبه‌های ذخیره‌سازی و مدیریت volumeها در Docker آشنا می‌کند.