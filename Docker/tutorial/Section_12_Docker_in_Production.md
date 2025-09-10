# Section 12 – Docker in Production

## 12.1 Production Readiness

آماده‌سازی Docker برای محیط production نیاز به ملاحظات خاصی دارد.

### نکات کلیدی Production:
- **Security**: امنیت بالا
- **Performance**: عملکرد بهینه
- **Reliability**: قابلیت اطمینان
- **Monitoring**: نظارت مستمر
- **Scalability**: مقیاس‌پذیری
- **Backup**: پشتیبان‌گیری

### چک‌لیست Production:
- [ ] ایمیج‌های امن و بهینه
- [ ] محدودیت‌های منابع
- [ ] Health checks
- [ ] Logging مناسب
- [ ] Monitoring و Alerting
- [ ] Backup strategy
- [ ] Security scanning
- [ ] Resource monitoring

### مثال Production Setup:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
    security_opt:
      - no-new-privileges:true
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## 12.2 Container Monitoring

نظارت بر کانتینرها برای اطمینان از عملکرد صحیح ضروری است.

### ابزارهای Monitoring:

#### **1. Prometheus + Grafana:**
```yaml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus

  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'

volumes:
  prometheus-data:
  grafana-data:
```

#### **2. cAdvisor:**
```yaml
version: '3.8'
services:
  cadvisor:
    image: gcr.io/cadvisor/cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    devices:
      - /dev/kmsg
    privileged: true
```

### فایل prometheus.yml:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'docker-containers'
    static_configs:
      - targets: ['docker-exporter:9323']
```

## 12.3 Log Management

مدیریت لاگ‌ها برای نظارت و عیب‌یابی ضروری است.

### ELK Stack:
```yaml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:7.15.0
    ports:
      - "5044:5044"
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:7.15.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    depends_on:
      - elasticsearch

  filebeat:
    image: docker.elastic.co/beats/filebeat:7.15.0
    user: root
    volumes:
      - ./filebeat.yml:/usr/share/filebeat/filebeat.yml:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    depends_on:
      - logstash

volumes:
  elasticsearch-data:
```

### فایل logstash.conf:
```ruby
input {
  beats {
    port => 5044
  }
}

filter {
  if [docker][container][name] {
    mutate {
      add_field => { "container_name" => "%{[docker][container][name]}" }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "docker-logs-%{+YYYY.MM.dd}"
  }
}
```

### فایل filebeat.yml:
```yaml
filebeat.inputs:
- type: container
  paths:
    - '/var/lib/docker/containers/*/*.log'
  processors:
    - add_docker_metadata:
        host: "unix:///var/run/docker.sock"

output.logstash:
  hosts: ["logstash:5044"]
```

## 12.4 Health Monitoring

نظارت بر سلامت کانتینرها و سرویس‌ها.

### Health Check Configuration:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    ports:
      - "80:80"

  app:
    image: my-app:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    depends_on:
      - db

  db:
    image: postgres:13
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

### Health Check Script:
```bash
#!/bin/bash
# health-check.sh

check_container_health() {
    local container_name=$1
    local health_status=$(docker inspect --format='{{.State.Health.Status}}' $container_name)
    
    if [ "$health_status" = "healthy" ]; then
        echo "✅ $container_name is healthy"
        return 0
    else
        echo "❌ $container_name is unhealthy"
        return 1
    fi
}

# Check all containers
containers=("web" "app" "db")
all_healthy=true

for container in "${containers[@]}"; do
    if ! check_container_health $container; then
        all_healthy=false
    fi
done

if [ "$all_healthy" = true ]; then
    echo "🎉 All containers are healthy"
    exit 0
else
    echo "⚠️ Some containers are unhealthy"
    exit 1
fi
```

## 12.5 Performance Optimization

بهینه‌سازی عملکرد کانتینرها در production.

### بهینه‌سازی منابع:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    ulimits:
      nproc: 65535
      nofile:
        soft: 20000
        hard: 40000
    sysctls:
      - net.core.somaxconn=65535
    ports:
      - "80:80"

  app:
    image: my-app:latest
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M
    environment:
      - NODE_ENV=production
      - NODE_OPTIONS=--max-old-space-size=1024
    depends_on:
      - db
```

### بهینه‌سازی شبکه:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    networks:
      - frontend
    ports:
      - "80:80"

  app:
    image: my-app:latest
    networks:
      - frontend
      - backend
    depends_on:
      - db

  db:
    image: postgres:13
    networks:
      - backend
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data

networks:
  frontend:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.enable_icc: "true"
      com.docker.network.bridge.enable_ip_masquerade: "true"
  backend:
    driver: bridge
    internal: true

volumes:
  postgres-data:
```

## 12.6 Resource Management

مدیریت منابع برای بهینه‌سازی استفاده از CPU، حافظه و I/O.

### Resource Limits:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    ulimits:
      nproc: 65535
      nofile:
        soft: 20000
        hard: 40000
    ports:
      - "80:80"

  app:
    image: my-app:latest
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M
    environment:
      - NODE_ENV=production
      - NODE_OPTIONS=--max-old-space-size=1024
    depends_on:
      - db

  db:
    image: postgres:13
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

### Resource Monitoring Script:
```bash
#!/bin/bash
# resource-monitor.sh

echo "=== Container Resource Usage ==="

# Get container stats
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}"

echo ""
echo "=== System Resources ==="

# CPU usage
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1

# Memory usage
echo "Memory Usage:"
free -h

# Disk usage
echo "Disk Usage:"
df -h

# Docker system info
echo "Docker System Info:"
docker system df
```

## 12.7 High Availability

پیاده‌سازی High Availability برای اطمینان از دسترسی مداوم.

### Load Balancer Setup:
```yaml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web1
      - web2
      - web3

  web1:
    image: my-app:latest
    environment:
      - NODE_ENV=production
      - INSTANCE_ID=1
    depends_on:
      - db

  web2:
    image: my-app:latest
    environment:
      - NODE_ENV=production
      - INSTANCE_ID=2
    depends_on:
      - db

  web3:
    image: my-app:latest
    environment:
      - NODE_ENV=production
      - INSTANCE_ID=3
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

### فایل nginx.conf:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream app {
        server web1:3000;
        server web2:3000;
        server web3:3000;
    }
    
    server {
        listen 80;
        location / {
            proxy_pass http://app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

## 12.8 Disaster Recovery

استراتژی Disaster Recovery برای بازیابی از خرابی‌ها.

### Backup Strategy:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    volumes:
      - web-data:/usr/share/nginx/html
    ports:
      - "80:80"

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backup:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./backups:/backups
    command: |
      sh -c '
      while true; do
        pg_dump -h db -U postgres myapp > /backups/backup-$(date +%Y%m%d-%H%M%S).sql
        find /backups -name "backup-*.sql" -mtime +7 -delete
        sleep 3600
      done
      '
    depends_on:
      - db

volumes:
  web-data:
  postgres-data:
```

### Backup Script:
```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d-%H%M%S)

echo "Starting backup process..."

# Database backup
echo "Backing up database..."
docker exec postgres pg_dump -U postgres myapp > $BACKUP_DIR/db-backup-$DATE.sql

# Application data backup
echo "Backing up application data..."
docker run --rm -v web-data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/app-data-$DATE.tar.gz /data

# Cleanup old backups (keep last 7 days)
echo "Cleaning up old backups..."
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed!"
```

## 12.9 Backup Strategies

استراتژی‌های مختلف پشتیبان‌گیری برای محافظت از داده‌ها.

### Automated Backup:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    volumes:
      - web-data:/usr/share/nginx/html
    ports:
      - "80:80"

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backup:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./backups:/backups
    command: |
      sh -c '
      while true; do
        pg_dump -h db -U postgres myapp > /backups/backup-$(date +%Y%m%d-%H%M%S).sql
        find /backups -name "backup-*.sql" -mtime +7 -delete
        sleep 3600
      done
      '
    depends_on:
      - db

volumes:
  web-data:
  postgres-data:
```

### Cloud Backup:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    volumes:
      - web-data:/usr/share/nginx/html
    ports:
      - "80:80"

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  cloud-backup:
    image: amazon/aws-cli
    environment:
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./backups:/backups
    command: |
      sh -c '
      while true; do
        pg_dump -h db -U postgres myapp > /backups/backup-$(date +%Y%m%d-%H%M%S).sql
        aws s3 cp /backups/backup-$(date +%Y%m%d-%H%M%S).sql s3://my-backup-bucket/
        find /backups -name "backup-*.sql" -mtime +1 -delete
        sleep 3600
      done
      '
    depends_on:
      - db

volumes:
  web-data:
  postgres-data:
```

## 12.10 Production Troubleshooting

عیب‌یابی مشکلات production برای حل سریع مسائل.

### ابزارهای عیب‌یابی:
```bash
#!/bin/bash
# troubleshoot.sh

echo "=== Docker Production Troubleshooting ==="

echo "1. Container Status:"
docker ps -a

echo "2. Container Logs:"
docker logs web
docker logs app
docker logs db

echo "3. Resource Usage:"
docker stats --no-stream

echo "4. Network Status:"
docker network ls
docker network inspect docker_default

echo "5. Volume Status:"
docker volume ls

echo "6. System Resources:"
free -h
df -h
top -bn1 | head -20

echo "7. Docker System Info:"
docker system df
docker system events --since 1h

echo "8. Container Health:"
docker inspect web | grep -A 10 "Health"
docker inspect app | grep -A 10 "Health"
docker inspect db | grep -A 10 "Health"
```

### Performance Analysis:
```bash
#!/bin/bash
# performance-analysis.sh

echo "=== Performance Analysis ==="

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

### Log Analysis:
```bash
#!/bin/bash
# log-analysis.sh

echo "=== Log Analysis ==="

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
```

این بخش شما را با تمام جنبه‌های استفاده از Docker در محیط production آشنا می‌کند.