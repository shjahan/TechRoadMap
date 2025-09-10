# Section 19 - Nginx Best Practices

## 19.1 Best Practice Concepts

Nginx best practices are proven methodologies and configurations that ensure optimal performance, security, reliability, and maintainability of Nginx deployments.

### Key Concepts:
- **Performance Optimization**: Maximizing throughput and minimizing latency
- **Security Hardening**: Protecting against vulnerabilities and attacks
- **Reliability**: Ensuring high availability and fault tolerance
- **Maintainability**: Making configurations easy to understand and modify
- **Scalability**: Designing for growth and increased load
- **Monitoring**: Implementing comprehensive observability
- **Documentation**: Maintaining clear and up-to-date documentation

### Real-world Analogy:
Think of Nginx best practices like building a house:
- **Performance** is like having a strong foundation and efficient utilities
- **Security** is like having good locks, alarms, and security systems
- **Reliability** is like having backup systems and redundancy
- **Maintainability** is like having accessible wiring and plumbing
- **Scalability** is like designing for future additions
- **Monitoring** is like having sensors and alarms throughout the house

### Best Practice Framework:
```
Security → Performance → Reliability → Maintainability → Scalability → Monitoring
    ↓           ↓           ↓            ↓              ↓           ↓
 Hardening   Optimization  Redundancy  Documentation  Load Balancing  Observability
```

## 19.2 Configuration Best Practices

### 1. Configuration Organization:
```nginx
# Main nginx.conf structure
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Events context
events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

# HTTP context
http {
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    
    # Include additional configurations
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### 2. Modular Configuration:
```bash
# Configuration directory structure
/etc/nginx/
├── nginx.conf              # Main configuration
├── conf.d/                 # Additional configurations
│   ├── security.conf       # Security settings
│   ├── gzip.conf          # Compression settings
│   ├── rate-limiting.conf  # Rate limiting
│   └── monitoring.conf     # Monitoring settings
├── sites-available/        # Available sites
│   ├── example.com
│   └── api.example.com
└── sites-enabled/          # Active sites
    ├── example.com -> ../sites-available/example.com
    └── api.example.com -> ../sites-available/api.example.com
```

### 3. Configuration Templates:
```nginx
# Template for basic server configuration
server {
    listen 80;
    server_name example.com www.example.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Root directory
    root /var/www/html;
    index index.html index.htm;
    
    # Main location
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Static files
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # Security
    location ~ /\. {
        deny all;
    }
}
```

### 4. Environment-specific Configurations:
```nginx
# Development configuration
server {
    listen 80;
    server_name dev.example.com;
    
    # Development-specific settings
    access_log /var/log/nginx/dev.access.log;
    error_log /var/log/nginx/dev.error.log debug;
    
    # Allow all origins in development
    add_header Access-Control-Allow-Origin "*" always;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Production configuration
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # Production-specific settings
    access_log /var/log/nginx/prod.access.log;
    error_log /var/log/nginx/prod.error.log warn;
    
    # SSL configuration
    ssl_certificate /path/to/cert.crt;
    ssl_certificate_key /path/to/key.key;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 19.3 Security Best Practices

### 1. Security Headers:
```nginx
# Comprehensive security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
```

### 2. Rate Limiting:
```nginx
# Rate limiting zones
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;

# Apply rate limiting
location /login {
    limit_req zone=login burst=5 nodelay;
    # Login handling
}

location /api/ {
    limit_req zone=api burst=50 nodelay;
    # API handling
}

location / {
    limit_req zone=general burst=20 nodelay;
    # General handling
}
```

### 3. Access Control:
```nginx
# IP-based access control
location /admin {
    allow 192.168.1.0/24;
    allow 10.0.0.0/8;
    deny all;
    
    # Admin handling
}

# User agent blocking
map $http_user_agent $blocked_agent {
    default 0;
    ~*malicious 1;
    ~*bot 1;
}

server {
    listen 80;
    server_name example.com;
    
    if ($blocked_agent) {
        return 403;
    }
    
    # Server configuration
}
```

### 4. SSL/TLS Security:
```nginx
# Secure SSL configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /path/to/trusted-ca.crt;
```

## 19.4 Performance Best Practices

### 1. Worker Optimization:
```nginx
# Optimized worker configuration
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

### 2. Caching Strategy:
```nginx
# Proxy caching
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

server {
    listen 80;
    server_name example.com;
    
    # Cache API responses
    location /api/ {
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        
        proxy_pass http://backend;
    }
    
    # No cache for dynamic content
    location /api/auth/ {
        proxy_pass http://backend;
    }
}
```

### 3. Compression:
```nginx
# Gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_comp_level 6;
gzip_types
    text/plain
    text/css
    text/xml
    text/javascript
    application/json
    application/javascript
    application/xml+rss
    application/atom+xml
    image/svg+xml;
```

### 4. Connection Optimization:
```nginx
# Connection optimization
keepalive_timeout 65;
keepalive_requests 100;
tcp_nopush on;
tcp_nodelay on;
sendfile on;

# Upstream connection pooling
upstream backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}
```

## 19.5 Monitoring Best Practices

### 1. Comprehensive Logging:
```nginx
# Detailed logging format
log_format detailed '$remote_addr - $remote_user [$time_local] '
                   '"$request" $status $body_bytes_sent '
                   '"$http_referer" "$http_user_agent" '
                   'rt=$request_time uct="$upstream_connect_time" '
                   'uht="$upstream_header_time" urt="$upstream_response_time" '
                   'upstream_addr="$upstream_addr" '
                   'upstream_status="$upstream_status"';

# JSON logging format
log_format json_combined escape=json
    '{'
        '"time_local":"$time_local",'
        '"remote_addr":"$remote_addr",'
        '"remote_user":"$remote_user",'
        '"request":"$request",'
        '"status": "$status",'
        '"body_bytes_sent":"$body_bytes_sent",'
        '"request_time":"$request_time",'
        '"http_referrer":"$http_referer",'
        '"http_user_agent":"$http_user_agent"'
    '}';
```

### 2. Health Checks:
```nginx
# Health check endpoint
location /health {
    access_log off;
    return 200 "healthy\n";
    add_header Content-Type text/plain;
}

# Nginx status
location /nginx_status {
    stub_status on;
    access_log off;
    allow 127.0.0.1;
    deny all;
}
```

### 3. Metrics Collection:
```nginx
# Prometheus metrics
location /metrics {
    access_log off;
    allow 127.0.0.1;
    deny all;
    stub_status on;
}
```

### 4. Alerting Configuration:
```bash
#!/bin/bash
# Monitoring and alerting script

# Check Nginx status
if ! systemctl is-active --quiet nginx; then
    echo "ALERT: Nginx is not running" | mail -s "Nginx Down Alert" admin@example.com
fi

# Check response time
RESPONSE_TIME=$(curl -w "%{time_total}" -o /dev/null -s http://localhost/health)
if (( $(echo "$RESPONSE_TIME > 2.0" | bc -l) )); then
    echo "ALERT: High response time: ${RESPONSE_TIME}s" | mail -s "Nginx Performance Alert" admin@example.com
fi

# Check error rate
ERROR_RATE=$(tail -100 /var/log/nginx/access.log | grep -c " 5[0-9][0-9] ")
if [ $ERROR_RATE -gt 10 ]; then
    echo "ALERT: High error rate: $ERROR_RATE errors in last 100 requests" | mail -s "Nginx Error Alert" admin@example.com
fi
```

## 19.6 Best Practice Examples

### 1. Production-Ready Configuration:
```nginx
# Production-ready nginx.conf
user nginx;
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;
error_log /var/log/nginx/error.log warn;
pid /run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
    accept_mutex off;
}

http {
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 100;
    types_hash_max_size 2048;
    
    # MIME types
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    
    # Upstream servers
    upstream backend {
        server 127.0.0.1:8000 weight=3;
        server 127.0.0.1:8001 weight=2;
        server 127.0.0.1:8002 weight=1;
        
        keepalive 32;
        keepalive_requests 100;
        keepalive_timeout 60s;
    }
    
    # Include additional configurations
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### 2. High-Availability Configuration:
```nginx
# High-availability server configuration
server {
    listen 80;
    server_name example.com www.example.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Rate limiting
    limit_req zone=api burst=50 nodelay;
    
    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # API endpoints
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # Error handling
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 30s;
    }
    
    # Static files
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # Security
    location ~ /\. {
        deny all;
    }
}
```

## 19.7 Best Practice Testing

### 1. Configuration Testing:
```bash
#!/bin/bash
# Configuration testing script

echo "Testing Nginx configuration..."

# Test syntax
nginx -t || exit 1

# Test with specific configuration
nginx -t -c /etc/nginx/nginx.conf || exit 1

# Test with different user
nginx -t -u nginx || exit 1

echo "Configuration tests passed!"
```

### 2. Performance Testing:
```bash
#!/bin/bash
# Performance testing script

echo "Starting performance tests..."

# Load testing
ab -n 1000 -c 10 http://localhost/ || exit 1

# Stress testing
wrk -t12 -c400 -d30s http://localhost/ || exit 1

# Response time testing
RESPONSE_TIME=$(curl -w "%{time_total}" -o /dev/null -s http://localhost/)
if (( $(echo "$RESPONSE_TIME > 1.0" | bc -l) )); then
    echo "WARNING: High response time: ${RESPONSE_TIME}s"
fi

echo "Performance tests completed!"
```

### 3. Security Testing:
```bash
#!/bin/bash
# Security testing script

echo "Starting security tests..."

# SSL testing
openssl s_client -connect localhost:443 -servername example.com || exit 1

# Header testing
curl -I http://localhost/ | grep -i "x-frame-options" || echo "WARNING: Missing security headers"

# Rate limiting testing
for i in {1..10}; do
    curl -s http://localhost/api/ > /dev/null
done

echo "Security tests completed!"
```

## 19.8 Best Practice Performance

### 1. Performance Monitoring:
```bash
#!/bin/bash
# Performance monitoring script

echo "=== Nginx Performance Metrics ==="
echo "Date: $(date)"
echo ""

# Nginx status
echo "Nginx Status:"
curl -s http://localhost/nginx_status || echo "Status endpoint not available"

# System metrics
echo ""
echo "System Metrics:"
echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "Memory Usage: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
echo "Load Average: $(uptime | awk '{print $10,$11,$12}')"

# Nginx metrics
echo ""
echo "Nginx Metrics:"
echo "Active Connections: $(curl -s http://localhost/nginx_status | awk 'NR==1{print $3}')"
echo "Requests per Second: $(curl -s http://localhost/nginx_status | awk 'NR==3{print $2}')"
```

### 2. Performance Optimization:
```bash
#!/bin/bash
# Performance optimization script

echo "Optimizing Nginx performance..."

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

## 19.9 Best Practice Troubleshooting

### 1. Common Issues and Solutions:
```bash
#!/bin/bash
# Troubleshooting script

echo "Nginx Troubleshooting Guide"
echo "=========================="

# Check if Nginx is running
if systemctl is-active --quiet nginx; then
    echo "✓ Nginx is running"
else
    echo "✗ Nginx is not running"
    echo "  Solution: sudo systemctl start nginx"
fi

# Check configuration
if nginx -t > /dev/null 2>&1; then
    echo "✓ Configuration is valid"
else
    echo "✗ Configuration has errors"
    echo "  Solution: nginx -t (check output for errors)"
fi

# Check ports
if netstat -tlnp | grep -q ":80 "; then
    echo "✓ Port 80 is listening"
else
    echo "✗ Port 80 is not listening"
    echo "  Solution: Check Nginx configuration and restart"
fi

# Check logs
echo ""
echo "Recent error logs:"
tail -5 /var/log/nginx/error.log

echo ""
echo "Recent access logs:"
tail -5 /var/log/nginx/access.log
```

### 2. Debugging Tools:
```bash
#!/bin/bash
# Debugging tools script

echo "Nginx Debugging Tools"
echo "===================="

# Configuration debugging
echo "1. Configuration debugging:"
nginx -T 2>&1 | grep -i error || echo "No configuration errors found"

# Network debugging
echo ""
echo "2. Network debugging:"
echo "Listening ports:"
netstat -tlnp | grep nginx

echo "Active connections:"
ss -tuln | grep :80

# Process debugging
echo ""
echo "3. Process debugging:"
echo "Nginx processes:"
ps aux | grep nginx

echo "Memory usage:"
ps aux --sort=-%mem | grep nginx | head -5

# Performance debugging
echo ""
echo "4. Performance debugging:"
echo "Response time test:"
time curl -s http://localhost/ > /dev/null
```

## 19.10 Best Practice Documentation

### 1. Configuration Documentation:
```nginx
# =============================================================================
# Nginx Configuration Documentation
# =============================================================================
# 
# File: /etc/nginx/nginx.conf
# Purpose: Main Nginx configuration file
# Author: System Administrator
# Last Modified: 2024-01-15
# Version: 1.0
# 
# =============================================================================
# Configuration Overview
# =============================================================================
# 
# This configuration provides:
# - High-performance web server
# - Reverse proxy capabilities
# - Load balancing
# - SSL/TLS termination
# - Security headers
# - Rate limiting
# - Monitoring and logging
# 
# =============================================================================
# Dependencies
# =============================================================================
# 
# Required modules:
# - http_ssl_module
# - http_realip_module
# - http_secure_link_module
# - http_stub_status_module
# 
# =============================================================================
# Performance Tuning
# =============================================================================
# 
# Worker processes: Set to auto (number of CPU cores)
# Worker connections: 1024 per worker
# Keep-alive timeout: 65 seconds
# Keep-alive requests: 100 per connection
# 
# =============================================================================
# Security Features
# =============================================================================
# 
# - Rate limiting for API endpoints
# - Security headers for all responses
# - SSL/TLS configuration
# - Access control for admin areas
# - Request size limits
# 
# =============================================================================

user nginx;
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;
error_log /var/log/nginx/error.log warn;
pid /run/nginx.pid;

# Events context - configuration for connection processing
events {
    worker_connections 1024;    # Maximum connections per worker
    use epoll;                  # Event method (Linux)
    multi_accept on;            # Accept multiple connections at once
    accept_mutex off;           # Disable accept mutex for better performance
}

# HTTP context - main configuration
http {
    # Basic settings
    sendfile on;                # Use sendfile for efficient file serving
    tcp_nopush on;              # Optimize TCP packets
    tcp_nodelay on;             # Disable Nagle's algorithm
    keepalive_timeout 65;       # Keep-alive timeout
    keepalive_requests 100;     # Requests per keep-alive connection
    types_hash_max_size 2048;   # Maximum size of types hash table
    
    # MIME types
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Logging format
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript;
    
    # Rate limiting zones
    limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    
    # Upstream servers
    upstream backend {
        server 127.0.0.1:8000 weight=3;
        server 127.0.0.1:8001 weight=2;
        server 127.0.0.1:8002 weight=1;
        
        keepalive 32;
        keepalive_requests 100;
        keepalive_timeout 60s;
    }
    
    # Include additional configurations
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### 2. Deployment Documentation:
```bash
#!/bin/bash
# Nginx deployment documentation

echo "Nginx Deployment Guide"
echo "====================="

echo "1. Prerequisites:"
echo "   - Ubuntu 20.04+ or CentOS 8+"
echo "   - Root or sudo access"
echo "   - Internet connection"

echo ""
echo "2. Installation:"
echo "   # Ubuntu/Debian"
echo "   sudo apt update"
echo "   sudo apt install nginx"

echo "   # CentOS/RHEL"
echo "   sudo yum install nginx"

echo ""
echo "3. Configuration:"
echo "   sudo cp nginx.conf /etc/nginx/nginx.conf"
echo "   sudo nginx -t"
echo "   sudo systemctl reload nginx"

echo ""
echo "4. Verification:"
echo "   curl http://localhost/"
echo "   systemctl status nginx"

echo ""
echo "5. Monitoring:"
echo "   tail -f /var/log/nginx/access.log"
echo "   tail -f /var/log/nginx/error.log"
```

### 3. Maintenance Documentation:
```bash
#!/bin/bash
# Nginx maintenance documentation

echo "Nginx Maintenance Guide"
echo "======================"

echo "Daily tasks:"
echo "- Check error logs: tail -f /var/log/nginx/error.log"
echo "- Monitor access logs: tail -f /var/log/nginx/access.log"
echo "- Check Nginx status: systemctl status nginx"

echo ""
echo "Weekly tasks:"
echo "- Review log files for errors"
echo "- Check disk space: df -h /var/log/nginx"
echo "- Update Nginx if needed: apt update && apt upgrade nginx"

echo ""
echo "Monthly tasks:"
echo "- Rotate log files: logrotate -f /etc/logrotate.d/nginx"
echo "- Review configuration: nginx -T"
echo "- Check security updates"

echo ""
echo "Troubleshooting:"
echo "- Configuration test: nginx -t"
echo "- Check ports: netstat -tlnp | grep nginx"
echo "- Check processes: ps aux | grep nginx"
echo "- Check memory: free -h"
```