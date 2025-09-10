# Section 10 - Performance Optimization

## 10.1 Performance Concepts

Performance optimization in Nginx involves improving response times, throughput, and resource utilization to deliver the best possible user experience while maintaining system stability.

### Key Performance Concepts:
- **Throughput**: Number of requests processed per second
- **Latency**: Time taken to process a single request
- **Concurrency**: Number of simultaneous connections handled
- **Resource Utilization**: Efficient use of CPU, memory, and I/O
- **Scalability**: Ability to handle increased load
- **Bottlenecks**: Points in the system that limit performance

### Real-world Analogy:
Performance optimization is like optimizing a restaurant's service that:
- Serves more customers per hour (throughput)
- Reduces waiting time for each customer (latency)
- Handles more customers simultaneously (concurrency)
- Uses kitchen staff and equipment efficiently (resource utilization)
- Can expand to serve more customers (scalability)
- Identifies and fixes slow processes (bottleneck elimination)

### Performance Metrics:
- **Requests per Second (RPS)**: How many requests can be handled
- **Response Time**: Time from request to response
- **CPU Usage**: Percentage of CPU utilization
- **Memory Usage**: Amount of RAM consumed
- **I/O Operations**: Disk and network activity
- **Connection Count**: Number of active connections

### Example Performance Monitoring:
```nginx
# Performance monitoring configuration
server {
    listen 80;
    server_name example.com;
    
    # Performance headers
    add_header X-Response-Time $request_time;
    add_header X-Upstream-Response-Time $upstream_response_time;
    add_header X-Connection-Count $connection_active;
    
    location / {
        root /var/www/html;
    }
}
```

## 10.2 Worker Processes

Worker processes are the core of Nginx's performance. Proper configuration of worker processes is crucial for optimal performance.

### Basic Worker Configuration:
```nginx
# Basic worker process configuration
user nginx;
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
    accept_mutex off;
}
```

### Advanced Worker Configuration:
```nginx
# Advanced worker process configuration
user nginx;
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;
worker_priority -5;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
    accept_mutex off;
    accept_mutex_delay 100ms;
    worker_aio_requests 32;
}
```

### CPU Affinity Configuration:
```nginx
# CPU affinity for specific CPU cores
worker_processes 4;
worker_cpu_affinity 0001 0010 0100 1000;

# For 8-core system
worker_processes 8;
worker_cpu_affinity 00000001 00000010 00000100 00001000 00010000 00100000 01000000 10000000;
```

### Worker Process Optimization:
```nginx
# Optimized worker configuration
user nginx;
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;
worker_priority -5;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
    accept_mutex off;
    
    # Performance optimizations
    worker_aio_requests 32;
    accept_mutex_delay 100ms;
    
    # Connection handling
    accept_mutex_off;
    worker_aio_requests 32;
}
```

### Worker Process Monitoring:
```bash
# Monitor worker processes
ps aux | grep nginx
top -p $(pgrep nginx)

# Check worker process status
curl http://localhost/nginx_status
```

## 10.3 Connection Handling

Connection handling optimization involves configuring how Nginx manages incoming connections and processes requests.

### Basic Connection Configuration:
```nginx
events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}
```

### Advanced Connection Configuration:
```nginx
events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
    accept_mutex off;
    
    # Connection handling optimizations
    worker_aio_requests 32;
    accept_mutex_delay 100ms;
    
    # Keep-alive optimizations
    keepalive_timeout 65;
    keepalive_requests 100;
}
```

### Connection Pooling:
```nginx
# Connection pooling configuration
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    
    # Connection pooling
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        
        # HTTP/1.1 for keep-alive
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

### Connection Limits:
```nginx
# Connection limits configuration
limit_conn_zone $binary_remote_addr zone=perip:10m;
limit_conn_zone $server_name zone=perserver:10m;

server {
    listen 80;
    server_name example.com;
    
    # Connection limits
    limit_conn perip 10;
    limit_conn perserver 100;
    
    location / {
        root /var/www/html;
    }
}
```

### Connection Monitoring:
```bash
# Monitor connections
ss -tuln | grep :80
netstat -an | grep :80 | wc -l

# Monitor connection states
ss -s
```

## 10.4 Memory Optimization

Memory optimization involves configuring Nginx to use memory efficiently and avoid memory-related performance issues.

### Basic Memory Configuration:
```nginx
# Basic memory configuration
worker_processes auto;
worker_rlimit_nofile 65535;

http {
    # Memory settings
    client_body_buffer_size 128k;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    client_max_body_size 10m;
}
```

### Advanced Memory Configuration:
```nginx
# Advanced memory configuration
worker_processes auto;
worker_rlimit_nofile 65535;

http {
    # Memory optimizations
    client_body_buffer_size 128k;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    client_max_body_size 10m;
    
    # Buffer optimizations
    proxy_buffering on;
    proxy_buffer_size 4k;
    proxy_buffers 8 4k;
    proxy_busy_buffers_size 8k;
    
    # FastCGI buffer optimizations
    fastcgi_buffering on;
    fastcgi_buffer_size 4k;
    fastcgi_buffers 8 4k;
    fastcgi_busy_buffers_size 8k;
}
```

### Memory Pool Configuration:
```nginx
# Memory pool configuration
http {
    # Memory pools
    client_body_temp_path /var/cache/nginx/client_temp;
    proxy_temp_path /var/cache/nginx/proxy_temp;
    fastcgi_temp_path /var/cache/nginx/fastcgi_temp;
    uwsgi_temp_path /var/cache/nginx/uwsgi_temp;
    scgi_temp_path /var/cache/nginx/scgi_temp;
}
```

### Memory Monitoring:
```bash
# Monitor memory usage
free -h
ps aux --sort=-%mem | head -10

# Monitor Nginx memory usage
ps aux | grep nginx
pmap $(pgrep nginx)
```

## 10.5 CPU Optimization

CPU optimization involves configuring Nginx to use CPU resources efficiently and avoid CPU bottlenecks.

### CPU Affinity Configuration:
```nginx
# CPU affinity configuration
worker_processes 4;
worker_cpu_affinity 0001 0010 0100 1000;

# For 8-core system
worker_processes 8;
worker_cpu_affinity 00000001 00000010 00000100 00001000 00010000 00100000 01000000 10000000;
```

### CPU Priority Configuration:
```nginx
# CPU priority configuration
worker_processes auto;
worker_priority -5;

# High priority for critical applications
worker_priority -10;
```

### CPU Optimization Settings:
```nginx
# CPU optimization settings
events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
    
    # CPU optimizations
    worker_aio_requests 32;
    accept_mutex_off;
}
```

### CPU Monitoring:
```bash
# Monitor CPU usage
top -p $(pgrep nginx)
htop -p $(pgrep nginx)

# Monitor CPU per core
mpstat -P ALL 1
```

## 10.6 Performance Best Practices

### 1. Configuration Optimization:
```nginx
# Optimized Nginx configuration
user nginx;
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
    accept_mutex_off;
}

http {
    # Basic optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 100;
    
    # Buffer optimizations
    client_body_buffer_size 128k;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript;
    
    server {
        listen 80;
        server_name example.com;
        
        location / {
            root /var/www/html;
        }
    }
}
```

### 2. Caching Strategy:
```nginx
# Comprehensive caching strategy
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

server {
    listen 80;
    server_name example.com;
    
    # Static content caching
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # API caching
    location /api/ {
        proxy_cache my_cache;
        proxy_cache_valid 200 1h;
        proxy_cache_valid 404 1m;
        proxy_pass http://backend;
    }
    
    # Dynamic content
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 10m;
        proxy_pass http://backend;
    }
}
```

### 3. Load Balancing Optimization:
```nginx
# Optimized load balancing
upstream backend {
    server 192.168.1.10:8080 weight=3 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 weight=3 max_fails=3 fail_timeout=30s;
    server 192.168.1.12:8080 weight=2 max_fails=3 fail_timeout=30s;
    
    # Connection pooling
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        
        # Connection optimization
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Buffer optimization
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }
}
```

### 4. SSL/TLS Optimization:
```nginx
# SSL/TLS optimization
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /path/to/cert.crt;
    ssl_certificate_key /path/to/key.key;
    
    # SSL optimizations
    ssl_session_cache shared:SSL:50m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;
    ssl_buffer_size 8k;
    
    # HTTP/2 optimizations
    http2_max_field_size 4k;
    http2_max_header_size 16k;
    http2_max_requests 1000;
    
    location / {
        root /var/www/html;
    }
}
```

## 10.7 Performance Testing

### 1. Load Testing:
```bash
# Basic load testing with Apache Bench
ab -n 1000 -c 10 http://example.com/

# Advanced load testing with wrk
wrk -t12 -c400 -d30s http://example.com/

# Load testing with specific headers
wrk -t12 -c400 -d30s -H "User-Agent: Mozilla/5.0" http://example.com/
```

### 2. Stress Testing:
```bash
# Stress testing
ab -n 10000 -c 100 http://example.com/

# Stress testing with different methods
wrk -t12 -c400 -d30s -s script.lua http://example.com/
```

### 3. Performance Benchmarking:
```bash
# Performance benchmarking script
#!/bin/bash

URL="http://example.com/"
CONCURRENT=10
REQUESTS=1000

echo "Starting performance test..."
echo "URL: $URL"
echo "Concurrent users: $CONCURRENT"
echo "Total requests: $REQUESTS"
echo ""

# Test with Apache Bench
echo "Apache Bench Results:"
ab -n $REQUESTS -c $CONCURRENT $URL

echo ""
echo "Wrk Results:"
wrk -t$CONCURRENT -c$CONCURRENT -d30s $URL
```

### 4. Performance Monitoring:
```bash
# Real-time performance monitoring
while true; do
    echo "=== $(date) ==="
    echo "Connections: $(ss -tuln | grep :80 | wc -l)"
    echo "Memory: $(free -h | grep Mem | awk '{print $3"/"$2}')"
    echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)"
    echo "Load: $(uptime | awk '{print $10,$11,$12}')"
    sleep 5
done
```

## 10.8 Performance Monitoring

### 1. Nginx Status Module:
```nginx
# Enable status module
server {
    listen 80;
    server_name localhost;
    
    location /nginx_status {
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        deny all;
    }
}
```

### 2. Performance Metrics:
```bash
# Monitor Nginx status
curl http://localhost/nginx_status

# Parse status output
curl -s http://localhost/nginx_status | awk '{
    print "Active connections: " $3
    print "Server accepts handled requests: " $4 " " $5 " " $6
    print "Reading: " $7 " Writing: " $8 " Waiting: " $9
}'
```

### 3. System Monitoring:
```bash
# System performance monitoring
#!/bin/bash

echo "=== System Performance ==="
echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "Memory Usage: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
echo "Load Average: $(uptime | awk '{print $10,$11,$12}')"
echo "Disk Usage: $(df -h / | awk 'NR==2{print $5}')"
echo ""

echo "=== Nginx Performance ==="
curl -s http://localhost/nginx_status | awk '{
    print "Active connections: " $3
    print "Server accepts handled requests: " $4 " " $5 " " $6
    print "Reading: " $7 " Writing: " $8 " Waiting: " $9
}'
```

### 4. Performance Logging:
```nginx
# Performance logging
log_format performance '$remote_addr - $remote_user [$time_local] '
                      '"$request" $status $body_bytes_sent '
                      '"$http_referer" "$http_user_agent" '
                      'rt=$request_time uct="$upstream_connect_time" '
                      'uht="$upstream_header_time" urt="$upstream_response_time" '
                      'upstream_addr="$upstream_addr" '
                      'upstream_status="$upstream_status"';

server {
    listen 80;
    server_name example.com;
    
    access_log /var/log/nginx/performance.log performance;
    
    location / {
        root /var/www/html;
    }
}
```

## 10.9 Performance Troubleshooting

### 1. Common Performance Issues:

#### High CPU Usage:
```bash
# Check CPU usage
top -p $(pgrep nginx)
htop -p $(pgrep nginx)

# Check for CPU-intensive operations
grep -i "cpu" /var/log/nginx/error.log
```

#### High Memory Usage:
```bash
# Check memory usage
free -h
ps aux --sort=-%mem | head -10

# Check Nginx memory usage
pmap $(pgrep nginx)
```

#### Slow Response Times:
```bash
# Check response times
curl -w "@curl-format.txt" -o /dev/null -s http://example.com/

# Check upstream response times
grep "upstream_response_time" /var/log/nginx/access.log | tail -10
```

### 2. Performance Debugging:
```nginx
# Enable performance debugging
error_log /var/log/nginx/performance_debug.log debug;

server {
    listen 80;
    server_name example.com;
    
    # Performance debug headers
    add_header X-Response-Time $request_time;
    add_header X-Upstream-Response-Time $upstream_response_time;
    add_header X-Connection-Count $connection_active;
    
    location / {
        root /var/www/html;
    }
}
```

### 3. Performance Optimization Scripts:
```bash
#!/bin/bash
# Performance optimization script

echo "Starting performance optimization..."

# Check current configuration
echo "Current worker processes: $(nginx -T 2>/dev/null | grep worker_processes | awk '{print $2}')"
echo "Current worker connections: $(nginx -T 2>/dev/null | grep worker_connections | awk '{print $2}')"

# Optimize worker processes
CPU_CORES=$(nproc)
echo "Detected CPU cores: $CPU_CORES"

# Update configuration
sed -i "s/worker_processes.*/worker_processes $CPU_CORES;/" /etc/nginx/nginx.conf
sed -i "s/worker_connections.*/worker_connections 1024;/" /etc/nginx/nginx.conf

# Test configuration
if nginx -t; then
    echo "Configuration test passed. Reloading Nginx..."
    nginx -s reload
    echo "Nginx reloaded successfully."
else
    echo "Configuration test failed. Please check the configuration."
fi
```

## 10.10 Performance Documentation

### 1. Performance Baseline:
```bash
#!/bin/bash
# Performance baseline script

echo "=== Performance Baseline ==="
echo "Date: $(date)"
echo ""

# System information
echo "=== System Information ==="
echo "CPU: $(lscpu | grep "Model name" | awk -F: '{print $2}' | xargs)"
echo "CPU Cores: $(nproc)"
echo "Memory: $(free -h | grep Mem | awk '{print $2}')"
echo "Disk: $(df -h / | awk 'NR==2{print $2}')"
echo ""

# Nginx configuration
echo "=== Nginx Configuration ==="
echo "Worker Processes: $(nginx -T 2>/dev/null | grep worker_processes | awk '{print $2}')"
echo "Worker Connections: $(nginx -T 2>/dev/null | grep worker_connections | awk '{print $2}')"
echo ""

# Performance test
echo "=== Performance Test ==="
ab -n 1000 -c 10 http://localhost/ | grep -E "(Requests per second|Time per request|Transfer rate)"
```

### 2. Performance Monitoring Dashboard:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Nginx Performance Dashboard</title>
    <meta http-equiv="refresh" content="5">
</head>
<body>
    <h1>Nginx Performance Dashboard</h1>
    <div id="status">
        <h2>Server Status</h2>
        <p>Active Connections: <span id="connections">-</span></p>
        <p>Server Accepts: <span id="accepts">-</span></p>
        <p>Handled Requests: <span id="handled">-</span></p>
        <p>Total Requests: <span id="requests">-</span></p>
        <p>Reading: <span id="reading">-</span></p>
        <p>Writing: <span id="writing">-</span></p>
        <p>Waiting: <span id="waiting">-</span></p>
    </div>
    
    <script>
        // Fetch status data
        fetch('/nginx_status')
            .then(response => response.text())
            .then(data => {
                const lines = data.split('\n');
                const active = lines[0].split(':')[1].trim();
                const server = lines[2].split(' ');
                document.getElementById('connections').textContent = active;
                document.getElementById('accepts').textContent = server[1];
                document.getElementById('handled').textContent = server[2];
                document.getElementById('requests').textContent = server[3];
                document.getElementById('reading').textContent = server[4];
                document.getElementById('writing').textContent = server[5];
                document.getElementById('waiting').textContent = server[6];
            });
    </script>
</body>
</html>
```

### 3. Performance Alerting:
```bash
#!/bin/bash
# Performance alerting script

THRESHOLD_CPU=80
THRESHOLD_MEMORY=80
THRESHOLD_RESPONSE_TIME=1.0

# Check CPU usage
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
if (( $(echo "$CPU_USAGE > $THRESHOLD_CPU" | bc -l) )); then
    echo "ALERT: High CPU usage: $CPU_USAGE%"
fi

# Check memory usage
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')
if (( $(echo "$MEMORY_USAGE > $THRESHOLD_MEMORY" | bc -l) )); then
    echo "ALERT: High memory usage: $MEMORY_USAGE%"
fi

# Check response time
RESPONSE_TIME=$(curl -w "%{time_total}" -o /dev/null -s http://localhost/)
if (( $(echo "$RESPONSE_TIME > $THRESHOLD_RESPONSE_TIME" | bc -l) )); then
    echo "ALERT: High response time: ${RESPONSE_TIME}s"
fi
```