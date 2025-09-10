# Section 18 – Docker Troubleshooting

## 18.1 Common Issues and Solutions

مشکلات رایج Docker و راه‌حل‌های آنها.

### مشکلات رایج:

#### **1. Container Won't Start:**
```bash
# بررسی وضعیت کانتینر
docker ps -a

# مشاهده لاگ‌های کانتینر
docker logs container_name

# بررسی اطلاعات کانتینر
docker inspect container_name

# راه‌اندازی مجدد کانتینر
docker restart container_name
```

#### **2. Out of Memory:**
```bash
# بررسی استفاده از حافظه
docker stats

# بررسی حافظه سیستم
free -h

# پاکسازی حافظه
docker system prune -a

# محدود کردن حافظه کانتینر
docker run -m 512m nginx
```

#### **3. Port Already in Use:**
```bash
# بررسی پورت‌های استفاده شده
netstat -tuln | grep :80

# یا
ss -tuln | grep :80

# توقف کانتینر استفاده کننده از پورت
docker stop container_name

# استفاده از پورت متفاوت
docker run -p 8080:80 nginx
```

#### **4. Permission Denied:**
```bash
# بررسی مجوزهای فایل
ls -la

# تغییر مالکیت فایل
sudo chown -R $USER:$USER .

# اجرای با sudo
sudo docker run nginx
```

### اسکریپت عیب‌یابی:
```bash
#!/bin/bash
# troubleshoot.sh

echo "=== Docker Troubleshooting ==="

echo "1. Docker Version:"
docker --version

echo "2. Docker Info:"
docker info

echo "3. Container Status:"
docker ps -a

echo "4. Image Status:"
docker images

echo "5. Network Status:"
docker network ls

echo "6. Volume Status:"
docker volume ls

echo "7. System Resources:"
free -h
df -h

echo "8. Docker System Usage:"
docker system df

echo "9. Recent Events:"
docker system events --since 1h | tail -20
```

## 18.2 Container Debugging

عیب‌یابی کانتینرها برای حل مشکلات.

### روش‌های Debugging:

#### **1. ورود به کانتینر:**
```bash
# ورود به کانتینر در حال اجرا
docker exec -it container_name bash

# ورود به کانتینر متوقف شده
docker run -it --rm image_name bash

# اجرای دستور در کانتینر
docker exec container_name ls -la
```

#### **2. بررسی لاگ‌ها:**
```bash
# لاگ‌های real-time
docker logs -f container_name

# آخرین N خط
docker logs --tail 100 container_name

# لاگ‌های از زمان خاص
docker logs --since "2023-01-01T00:00:00" container_name

# لاگ‌های با timestamp
docker logs -t container_name
```

#### **3. بررسی منابع:**
```bash
# آمار real-time
docker stats

# آمار کانتینر خاص
docker stats container_name

# آمار بدون streaming
docker stats --no-stream
```

### Debugging Script:
```bash
#!/bin/bash
# debug-container.sh

CONTAINER_NAME=$1

if [ -z "$CONTAINER_NAME" ]; then
    echo "Usage: $0 <container_name>"
    exit 1
fi

echo "=== Debugging Container: $CONTAINER_NAME ==="

echo "1. Container Status:"
docker ps -a | grep $CONTAINER_NAME

echo "2. Container Logs:"
docker logs $CONTAINER_NAME

echo "3. Container Resources:"
docker stats --no-stream $CONTAINER_NAME

echo "4. Container Configuration:"
docker inspect $CONTAINER_NAME

echo "5. Container Processes:"
docker top $CONTAINER_NAME

echo "6. Container Network:"
docker network ls
docker network inspect $(docker inspect $CONTAINER_NAME --format='{{.NetworkSettings.Networks}}')

echo "7. Container Volumes:"
docker inspect $CONTAINER_NAME --format='{{.Mounts}}'
```

## 18.3 Network Troubleshooting

عیب‌یابی مشکلات شبکه در Docker.

### مشکلات شبکه:

#### **1. کانتینرها نمی‌توانند با یکدیگر ارتباط برقرار کنند:**
```bash
# بررسی شبکه‌ها
docker network ls

# بررسی جزئیات شبکه
docker network inspect network_name

# بررسی IP کانتینرها
docker inspect container_name | grep IPAddress

# تست اتصال
docker exec container1 ping container2
```

#### **2. کانتینر نمی‌تواند به اینترنت دسترسی داشته باشد:**
```bash
# بررسی DNS
docker exec container_name nslookup google.com

# بررسی routing
docker exec container_name ip route

# بررسی iptables
sudo iptables -L
```

#### **3. پورت در دسترس نیست:**
```bash
# بررسی پورت‌های باز
netstat -tuln | grep :80

# بررسی firewall
sudo ufw status

# تست اتصال
telnet localhost 80
```

### Network Troubleshooting Script:
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

echo "6. DNS Resolution:"
docker exec -it web nslookup db

echo "7. Port Status:"
netstat -tuln | grep :80

echo "8. Firewall Status:"
sudo ufw status
```

## 18.4 Storage Issues

عیب‌یابی مشکلات storage در Docker.

### مشکلات Storage:

#### **1. فضای دیسک تمام شده:**
```bash
# بررسی فضای دیسک
df -h

# بررسی استفاده Docker
docker system df

# پاکسازی Docker
docker system prune -a

# پاکسازی volumeها
docker volume prune
```

#### **2. Volume mount نشده:**
```bash
# بررسی volumeها
docker volume ls

# بررسی mount points
docker inspect container_name | grep Mounts

# ایجاد volume
docker volume create my-volume

# استفاده از volume
docker run -v my-volume:/data nginx
```

#### **3. Permission denied در volume:**
```bash
# بررسی مجوزهای volume
ls -la /var/lib/docker/volumes/

# تغییر مالکیت
sudo chown -R $USER:$USER /var/lib/docker/volumes/
```

### Storage Troubleshooting Script:
```bash
#!/bin/bash
# storage-troubleshoot.sh

echo "=== Docker Storage Troubleshooting ==="

echo "1. Disk Usage:"
df -h

echo "2. Docker System Usage:"
docker system df

echo "3. Volume List:"
docker volume ls

echo "4. Volume Details:"
docker volume inspect $(docker volume ls -q)

echo "5. Container Mounts:"
docker inspect $(docker ps -q) | grep -A 10 "Mounts"

echo "6. Docker Root Directory:"
docker info | grep "Docker Root Dir"

echo "7. Available Space:"
df -h $(docker info | grep "Docker Root Dir" | cut -d: -f2 | tr -d ' ')
```

## 18.5 Performance Issues

عیب‌یابی مشکلات عملکرد در Docker.

### مشکلات عملکرد:

#### **1. CPU Usage بالا:**
```bash
# بررسی استفاده از CPU
docker stats

# بررسی processes
docker top container_name

# محدود کردن CPU
docker run --cpus="0.5" nginx
```

#### **2. Memory Usage بالا:**
```bash
# بررسی استفاده از حافظه
docker stats

# بررسی memory limits
docker inspect container_name | grep -i memory

# محدود کردن حافظه
docker run -m 512m nginx
```

#### **3. I/O Performance:**
```bash
# بررسی I/O
iostat -x 1

# بررسی disk usage
iotop

# بهینه‌سازی I/O
docker run --device-read-bps /dev/sda:1mb nginx
```

### Performance Analysis Script:
```bash
#!/bin/bash
# performance-analysis.sh

echo "=== Docker Performance Analysis ==="

echo "1. Container Performance:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}"

echo "2. System Performance:"
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1

echo "Memory Usage:"
free -h

echo "Disk Usage:"
df -h

echo "3. Network Performance:"
netstat -tuln
ss -tuln

echo "4. Docker Performance:"
docker system df
docker system events --since 1h | head -20
```

## 18.6 Security Issues

عیب‌یابی مشکلات امنیتی در Docker.

### مشکلات امنیتی:

#### **1. Container با root اجرا می‌شود:**
```bash
# بررسی user کانتینر
docker exec container_name whoami

# اجرای با user غیر root
docker run --user 1000:1000 nginx
```

#### **2. Privileged container:**
```bash
# بررسی privileged status
docker inspect container_name | grep Privileged

# اجرای بدون privileged
docker run --privileged=false nginx
```

#### **3. Security vulnerabilities:**
```bash
# اسکن امنیتی
docker scan image_name

# استفاده از Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image image_name
```

### Security Troubleshooting Script:
```bash
#!/bin/bash
# security-troubleshoot.sh

echo "=== Docker Security Troubleshooting ==="

echo "1. Container Users:"
docker exec $(docker ps -q) whoami

echo "2. Privileged Containers:"
docker ps --format "table {{.Names}}\t{{.Command}}" | grep privileged

echo "3. Security Scan:"
docker scan $(docker images -q | head -1)

echo "4. Container Capabilities:"
docker inspect $(docker ps -q) | grep -A 10 "CapAdd\|CapDrop"

echo "5. Security Options:"
docker inspect $(docker ps -q) | grep -A 10 "SecurityOpt"

echo "6. Read-only Containers:"
docker inspect $(docker ps -q) | grep -A 5 "ReadonlyRootfs"
```

## 18.7 Registry Issues

عیب‌یابی مشکلات registry در Docker.

### مشکلات Registry:

#### **1. Authentication failed:**
```bash
# ورود به registry
docker login registry.example.com

# بررسی credentials
cat ~/.docker/config.json

# حذف credentials
docker logout registry.example.com
```

#### **2. Push failed:**
```bash
# بررسی اتصال
ping registry.example.com

# بررسی SSL
openssl s_client -connect registry.example.com:443

# تست push
docker push registry.example.com/image:tag
```

#### **3. Pull failed:**
```bash
# بررسی image وجود دارد
docker search image_name

# بررسی tags
curl -X GET https://registry.example.com/v2/image_name/tags/list

# تست pull
docker pull registry.example.com/image:tag
```

### Registry Troubleshooting Script:
```bash
#!/bin/bash
# registry-troubleshoot.sh

REGISTRY=$1

if [ -z "$REGISTRY" ]; then
    echo "Usage: $0 <registry_url>"
    exit 1
fi

echo "=== Docker Registry Troubleshooting: $REGISTRY ==="

echo "1. Registry Connectivity:"
ping -c 3 $REGISTRY

echo "2. Registry SSL:"
openssl s_client -connect $REGISTRY:443 -servername $REGISTRY

echo "3. Registry API:"
curl -X GET https://$REGISTRY/v2/

echo "4. Authentication:"
docker login $REGISTRY

echo "5. Image List:"
curl -X GET https://$REGISTRY/v2/_catalog

echo "6. Test Push:"
docker tag nginx:alpine $REGISTRY/test:latest
docker push $REGISTRY/test:latest
```

## 18.8 Orchestration Issues

عیب‌یابی مشکلات orchestration در Docker.

### مشکلات Orchestration:

#### **1. Service won't start:**
```bash
# بررسی service status
docker service ls

# بررسی service logs
docker service logs service_name

# بررسی service details
docker service inspect service_name
```

#### **2. Load balancing issues:**
```bash
# بررسی load balancer
docker service inspect service_name | grep -A 10 "Endpoint"

# بررسی health checks
docker service inspect service_name | grep -A 10 "HealthCheck"

# تست load balancing
curl http://localhost:80
```

#### **3. Scaling issues:**
```bash
# بررسی replicas
docker service inspect service_name | grep Replicas

# scale کردن service
docker service scale service_name=3

# بررسی node resources
docker node ls
docker node inspect node_id
```

### Orchestration Troubleshooting Script:
```bash
#!/bin/bash
# orchestration-troubleshoot.sh

echo "=== Docker Orchestration Troubleshooting ==="

echo "1. Swarm Status:"
docker node ls

echo "2. Service Status:"
docker service ls

echo "3. Service Details:"
docker service inspect $(docker service ls -q)

echo "4. Service Logs:"
docker service logs $(docker service ls -q)

echo "5. Node Resources:"
docker node inspect $(docker node ls -q) | grep -A 10 "Resources"

echo "6. Network Status:"
docker network ls
docker network inspect $(docker network ls -q)
```

## 18.9 Log Analysis

تحلیل لاگ‌ها برای عیب‌یابی.

### تحلیل لاگ‌ها:

#### **1. Application Logs:**
```bash
# لاگ‌های application
docker logs container_name | grep -i error
docker logs container_name | grep -i warning

# لاگ‌های real-time
docker logs -f container_name | grep -i error
```

#### **2. System Logs:**
```bash
# لاگ‌های Docker daemon
journalctl -u docker.service

# لاگ‌های سیستم
journalctl --since "1 hour ago"

# لاگ‌های kernel
dmesg | tail -20
```

#### **3. Log Aggregation:**
```bash
# استفاده از ELK Stack
curl -X GET "localhost:9200/docker-logs-*/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "message": "error"
    }
  }
}'
```

### Log Analysis Script:
```bash
#!/bin/bash
# log-analysis.sh

echo "=== Docker Log Analysis ==="

echo "1. Application Logs:"
docker logs app --tail 100 | grep -i error
docker logs app --tail 100 | grep -i warning

echo "2. Database Logs:"
docker logs db --tail 100 | grep -i error
docker logs db --tail 100 | grep -i warning

echo "3. Web Server Logs:"
docker logs web --tail 100 | grep -i error
docker logs web --tail 100 | grep -i warning

echo "4. System Logs:"
journalctl -u docker.service --since "1 hour ago" | tail -20

echo "5. Recent Events:"
docker system events --since 1h | tail -20
```

## 18.10 Diagnostic Tools

ابزارهای تشخیصی برای عیب‌یابی Docker.

### ابزارهای تشخیصی:

#### **1. Docker Built-in Tools:**
```bash
# Docker system info
docker system info

# Docker system events
docker system events

# Docker system df
docker system df

# Docker system prune
docker system prune
```

#### **2. Third-party Tools:**
```bash
# Dive - تحلیل ایمیج
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest image_name

# Trivy - اسکن امنیتی
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image image_name

# Portainer - مدیریت Docker
docker run -d -p 9000:9000 --name portainer \
  -v /var/run/docker.sock:/var/run/docker.sock \
  portainer/portainer
```

#### **3. Custom Diagnostic Script:**
```bash
#!/bin/bash
# docker-diagnostics.sh

echo "=== Docker Comprehensive Diagnostics ==="

echo "1. Docker Version:"
docker --version
docker-compose --version

echo "2. Docker Info:"
docker info

echo "3. System Resources:"
free -h
df -h
top -bn1 | head -20

echo "4. Container Status:"
docker ps -a

echo "5. Image Status:"
docker images

echo "6. Network Status:"
docker network ls
docker network inspect bridge

echo "7. Volume Status:"
docker volume ls

echo "8. Service Status:"
docker service ls 2>/dev/null || echo "No services found"

echo "9. Recent Events:"
docker system events --since 1h | tail -20

echo "10. System Usage:"
docker system df

echo "11. Container Resources:"
docker stats --no-stream

echo "12. Log Analysis:"
docker logs $(docker ps -q) --tail 10 2>/dev/null || echo "No running containers"

echo "=== Diagnostics Complete ==="
```

این بخش شما را با تمام جنبه‌های عیب‌یابی Docker آشنا می‌کند.