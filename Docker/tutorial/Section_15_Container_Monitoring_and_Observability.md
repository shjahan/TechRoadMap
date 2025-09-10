# Section 15 – Container Monitoring and Observability

## 15.1 Container Metrics

نظارت بر metrics کانتینرها برای درک عملکرد و استفاده از منابع.

### انواع Metrics:

#### **1. Resource Metrics:**
- **CPU Usage**: استفاده از CPU
- **Memory Usage**: استفاده از حافظه
- **Disk I/O**: ورودی/خروجی دیسک
- **Network I/O**: ورودی/خروجی شبکه

#### **2. Application Metrics:**
- **Request Rate**: نرخ درخواست‌ها
- **Response Time**: زمان پاسخ
- **Error Rate**: نرخ خطا
- **Throughput**: توان عملیاتی

### Prometheus + cAdvisor:
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
```

### فایل prometheus.yml:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'docker-containers'
    static_configs:
      - targets: ['docker-exporter:9323']
```

## 15.2 Log Aggregation

جمع‌آوری و تجمیع لاگ‌ها از کانتینرها.

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
  
  if [fields][log_type] == "application" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" }
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

## 15.3 Distributed Tracing

ردیابی توزیع‌شده برای درک جریان درخواست‌ها در میکروسرویس‌ها.

### Jaeger Tracing:
```yaml
version: '3.8'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "14268:14268"
    environment:
      - COLLECTOR_OTLP_ENABLED=true

  web:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - JAEGER_AGENT_HOST=jaeger
      - JAEGER_AGENT_PORT=14268
      - JAEGER_SERVICE_NAME=web-service
    depends_on:
      - jaeger

  app:
    image: my-app:latest
    environment:
      - JAEGER_AGENT_HOST=jaeger
      - JAEGER_AGENT_PORT=14268
      - JAEGER_SERVICE_NAME=app-service
    depends_on:
      - jaeger
```

### Zipkin Tracing:
```yaml
version: '3.8'
services:
  zipkin:
    image: openzipkin/zipkin:latest
    ports:
      - "9411:9411"
    environment:
      - STORAGE_TYPE=mem

  web:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - ZIPKIN_URL=http://zipkin:9411
    depends_on:
      - zipkin

  app:
    image: my-app:latest
    environment:
      - ZIPKIN_URL=http://zipkin:9411
    depends_on:
      - zipkin
```

## 15.4 APM Tools

ابزارهای Application Performance Monitoring.

### New Relic:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - NEW_RELIC_LICENSE_KEY=${NEW_RELIC_LICENSE_KEY}
      - NEW_RELIC_APP_NAME=web-app
    depends_on:
      - app

  app:
    image: my-app:latest
    environment:
      - NEW_RELIC_LICENSE_KEY=${NEW_RELIC_LICENSE_KEY}
      - NEW_RELIC_APP_NAME=app-service
```

### Datadog:
```yaml
version: '3.8'
services:
  datadog-agent:
    image: datadog/agent:latest
    environment:
      - DD_API_KEY=${DD_API_KEY}
      - DD_SITE=datadoghq.com
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup/:/host/sys/fs/cgroup:ro
    ports:
      - "8126:8126"

  web:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - DD_TRACE_ENABLED=true
      - DD_SERVICE=web-app
    depends_on:
      - datadog-agent

  app:
    image: my-app:latest
    environment:
      - DD_TRACE_ENABLED=true
      - DD_SERVICE=app-service
    depends_on:
      - datadog-agent
```

## 15.5 Prometheus and Grafana

نظارت کامل با Prometheus و Grafana.

### Prometheus + Grafana Setup:
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

volumes:
  prometheus-data:
  grafana-data:
```

### Grafana Dashboard:
```json
{
  "dashboard": {
    "title": "Docker Monitoring",
    "panels": [
      {
        "title": "Container CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(container_cpu_usage_seconds_total[5m])",
            "legendFormat": "{{container_name}}"
          }
        ]
      },
      {
        "title": "Container Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "container_memory_usage_bytes",
            "legendFormat": "{{container_name}}"
          }
        ]
      }
    ]
  }
}
```

## 15.6 ELK Stack

جمع‌آوری، پردازش و تجسم لاگ‌ها با ELK Stack.

### ELK Stack Setup:
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

### Logstash Configuration:
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
  
  if [fields][log_type] == "application" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:message}" }
    }
  }
  
  if [fields][log_type] == "nginx" {
    grok {
      match => { "message" => "%{NGINXACCESS}" }
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

## 15.7 Jaeger Tracing

ردیابی توزیع‌شده با Jaeger.

### Jaeger Setup:
```yaml
version: '3.8'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "14268:14268"
    environment:
      - COLLECTOR_OTLP_ENABLED=true

  web:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - JAEGER_AGENT_HOST=jaeger
      - JAEGER_AGENT_PORT=14268
      - JAEGER_SERVICE_NAME=web-service
    depends_on:
      - jaeger

  app:
    image: my-app:latest
    environment:
      - JAEGER_AGENT_HOST=jaeger
      - JAEGER_AGENT_PORT=14268
      - JAEGER_SERVICE_NAME=app-service
    depends_on:
      - jaeger
```

### Jaeger Configuration:
```yaml
# jaeger-config.yaml
collector:
  otlp:
    grpc:
      endpoint: 0.0.0.0:4317
    http:
      endpoint: 0.0.0.0:4318

query:
  base-path: /jaeger

agent:
  collector:
    host-port: jaeger:14250
```

## 15.8 Container Health Monitoring

نظارت بر سلامت کانتینرها.

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

### Health Monitoring Script:
```bash
#!/bin/bash
# health-monitor.sh

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

## 15.9 Alerting Strategies

استراتژی‌های هشدار برای مشکلات کانتینرها.

### Prometheus Alerting:
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

### Alert Rules:
```yaml
# alert_rules.yml
groups:
- name: container_alerts
  rules:
  - alert: HighCPUUsage
    expr: rate(container_cpu_usage_seconds_total[5m]) > 0.8
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage detected"
      description: "Container {{ $labels.container_name }} has high CPU usage"

  - alert: HighMemoryUsage
    expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.8
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High memory usage detected"
      description: "Container {{ $labels.container_name }} has high memory usage"

  - alert: ContainerDown
    expr: up == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Container is down"
      description: "Container {{ $labels.container_name }} is down"
```

### Alertmanager:
```yaml
version: '3.8'
services:
  alertmanager:
    image: prom/alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
```

## 15.10 Performance Analysis

تحلیل عملکرد کانتینرها.

### Performance Monitoring:
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

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
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

volumes:
  prometheus-data:
  grafana-data:
```

### Performance Analysis Script:
```bash
#!/bin/bash
# performance-analysis.sh

echo "=== Container Performance Analysis ==="

echo "1. Container Resource Usage:"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}"

echo ""
echo "2. System Resources:"
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1

echo "Memory Usage:"
free -h

echo "Disk Usage:"
df -h

echo ""
echo "3. Container Health:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "4. Network Performance:"
netstat -tuln
ss -tuln

echo ""
echo "5. Docker Performance:"
docker system df
docker system events --since 1h | head -20
```

این بخش شما را با تمام جنبه‌های نظارت و observability کانتینرها آشنا می‌کند.