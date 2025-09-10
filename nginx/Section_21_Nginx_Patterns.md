# Section 21 - Nginx Patterns

## 21.1 Pattern Concepts

Nginx patterns are proven, reusable solutions to common problems in web server configuration, load balancing, caching, and security. These patterns provide templates and best practices for implementing specific functionality.

### Key Concepts:
- **Design Patterns**: Reusable solutions to common problems
- **Configuration Patterns**: Standardized ways to configure Nginx
- **Architecture Patterns**: High-level structural approaches
- **Security Patterns**: Proven security configurations
- **Performance Patterns**: Optimization techniques
- **Monitoring Patterns**: Observability and logging approaches

### Real-world Analogy:
Think of Nginx patterns like architectural blueprints:
- **Design Patterns** are like standard building designs (ranch, colonial, etc.)
- **Configuration Patterns** are like electrical and plumbing schematics
- **Security Patterns** are like security system layouts
- **Performance Patterns** are like HVAC and insulation designs

### Pattern Categories:
```
Load Balancing → Caching → Security → Performance → Monitoring → Deployment
      ↓            ↓         ↓          ↓           ↓          ↓
   Round Robin   Proxy    Rate Limit  Compression  Logging   Blue-Green
   Least Conn    FastCGI  Auth        Gzip        Metrics   Canary
   IP Hash       Redis    Headers     Buffering   Alerts    Rolling
```

## 21.2 Load Balancing Patterns

### 1. Round Robin Pattern:
```nginx
# Basic round robin load balancing
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. Weighted Round Robin Pattern:
```nginx
# Weighted round robin load balancing
upstream backend {
    server 192.168.1.10:8080 weight=3;
    server 192.168.1.11:8080 weight=2;
    server 192.168.1.12:8080 weight=1;
    server 192.168.1.13:8080 backup;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Least Connections Pattern:
```nginx
# Least connections load balancing
upstream backend {
    least_conn;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. IP Hash Pattern:
```nginx
# IP hash load balancing for session persistence
upstream backend {
    ip_hash;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5. Health Check Pattern:
```nginx
# Health check load balancing
upstream backend {
    server 192.168.1.10:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.12:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.13:8080 backup;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # Error handling
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 30s;
    }
}
```

## 21.3 Caching Patterns

### 1. Proxy Caching Pattern:
```nginx
# Proxy caching configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. FastCGI Caching Pattern:
```nginx
# FastCGI caching configuration
fastcgi_cache_path /var/cache/nginx/fastcgi levels=1:2 keys_zone=fastcgi_cache:10m max_size=1g inactive=60m;

server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    
    location ~ \.php$ {
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_cache fastcgi_cache;
        fastcgi_cache_valid 200 302 10m;
        fastcgi_cache_valid 404 1m;
        fastcgi_cache_key "$scheme$request_method$host$request_uri";
        
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

### 3. Browser Caching Pattern:
```nginx
# Browser caching for static files
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    
    # CSS and JS files
    location ~* \.(css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary "Accept-Encoding";
        access_log off;
    }
    
    # Images
    location ~* \.(jpg|jpeg|png|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # Fonts
    location ~* \.(woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Access-Control-Allow-Origin "*";
        access_log off;
    }
}
```

### 4. Cache Invalidation Pattern:
```nginx
# Cache invalidation pattern
map $request_method $purge_method {
    PURGE 1;
    default 0;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        
        # Cache invalidation
        proxy_cache_purge $purge_method;
        
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 21.4 Security Patterns

### 1. Rate Limiting Pattern:
```nginx
# Rate limiting pattern
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;

server {
    listen 80;
    server_name example.com;
    
    # Login endpoint with strict rate limiting
    location /login {
        limit_req zone=login burst=5 nodelay;
        # Login handling
    }
    
    # API endpoints with moderate rate limiting
    location /api/ {
        limit_req zone=api burst=50 nodelay;
        # API handling
    }
    
    # General endpoints with light rate limiting
    location / {
        limit_req zone=general burst=20 nodelay;
        # General handling
    }
}
```

### 2. Authentication Pattern:
```nginx
# Basic authentication pattern
server {
    listen 80;
    server_name example.com;
    
    # Public area
    location / {
        root /var/www/html;
    }
    
    # Protected area
    location /admin {
        auth_basic "Admin Area";
        auth_basic_user_file /etc/nginx/.htpasswd;
        
        root /var/www/admin;
    }
    
    # API with token authentication
    location /api/ {
        auth_request /auth;
        proxy_pass http://backend;
    }
    
    # Auth endpoint
    location = /auth {
        internal;
        proxy_pass http://auth_service/validate;
        proxy_pass_request_body off;
        proxy_set_header Content-Length "";
        proxy_set_header X-Original-URI $request_uri;
    }
}
```

### 3. Security Headers Pattern:
```nginx
# Security headers pattern
map $sent_http_content_type $csp_header {
    default "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';";
    "text/html" "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:;";
}

server {
    listen 80;
    server_name example.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy $csp_header always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
    
    location / {
        root /var/www/html;
    }
}
```

### 4. DDoS Protection Pattern:
```nginx
# DDoS protection pattern
limit_req_zone $binary_remote_addr zone=ddos:10m rate=1r/s;
limit_conn_zone $binary_remote_addr zone=conn_limit_per_ip:10m;

server {
    listen 80;
    server_name example.com;
    
    # DDoS protection
    limit_req zone=ddos burst=5 nodelay;
    limit_conn conn_limit_per_ip 10;
    
    # Block suspicious user agents
    if ($http_user_agent ~* (bot|crawler|spider|scraper)) {
        return 403;
    }
    
    # Block suspicious requests
    if ($request_uri ~* (\.\.|\.php|\.asp|\.jsp)) {
        return 403;
    }
    
    location / {
        root /var/www/html;
    }
}
```

## 21.5 Performance Patterns

### 1. Compression Pattern:
```nginx
# Compression pattern
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

server {
    listen 80;
    server_name example.com;
    
    location / {
        root /var/www/html;
    }
}
```

### 2. Connection Optimization Pattern:
```nginx
# Connection optimization pattern
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}

server {
    listen 80;
    server_name example.com;
    
    # Connection optimization
    keepalive_timeout 65;
    keepalive_requests 100;
    tcp_nopush on;
    tcp_nodelay on;
    sendfile on;
    
    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Buffer Optimization Pattern:
```nginx
# Buffer optimization pattern
server {
    listen 80;
    server_name example.com;
    
    # Client buffer optimization
    client_body_buffer_size 128k;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    client_max_body_size 10m;
    
    # Proxy buffer optimization
    proxy_buffering on;
    proxy_buffer_size 4k;
    proxy_buffers 8 4k;
    proxy_busy_buffers_size 8k;
    proxy_temp_file_write_size 8k;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Worker Optimization Pattern:
```nginx
# Worker optimization pattern
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
    accept_mutex off;
}

http {
    # Basic optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 100;
    
    server {
        listen 80;
        server_name example.com;
        root /var/www/html;
    }
}
```

## 21.6 Pattern Best Practices

### 1. Pattern Documentation:
```nginx
# =============================================================================
# Nginx Pattern: Load Balancing with Health Checks
# =============================================================================
# 
# Purpose: Distribute load across multiple backend servers with health monitoring
# Use Case: High availability web applications
# Benefits: Improved reliability, better resource utilization
# 
# =============================================================================
# Configuration
# =============================================================================

upstream backend {
    # Health check configuration
    server 192.168.1.10:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.12:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.13:8080 backup;
    
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
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # Error handling
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 30s;
    }
}
```

### 2. Pattern Testing:
```bash
#!/bin/bash
# Pattern testing script

echo "Testing Nginx Patterns"
echo "====================="

# Test load balancing pattern
echo "1. Testing load balancing pattern..."
for i in {1..10}; do
    curl -s http://localhost/ | grep -o "Server: [^<]*" || echo "No server header"
done

# Test caching pattern
echo "2. Testing caching pattern..."
curl -I http://localhost/ | grep -i "cache-control" || echo "No cache headers"

# Test rate limiting pattern
echo "3. Testing rate limiting pattern..."
for i in {1..10}; do
    curl -s -w "%{http_code}\n" -o /dev/null http://localhost/api/
done

# Test security headers pattern
echo "4. Testing security headers pattern..."
curl -I http://localhost/ | grep -i "x-frame-options" || echo "No security headers"
```

### 3. Pattern Monitoring:
```bash
#!/bin/bash
# Pattern monitoring script

echo "Monitoring Nginx Patterns"
echo "========================"

# Monitor load balancing
echo "1. Load Balancing Status:"
curl -s http://localhost/nginx_status | awk '{
    print "Active connections: " $3
    print "Server accepts handled requests: " $4 " " $5 " " $6
    print "Reading: " $7 " Writing: " $8 " Waiting: " $9
}'

# Monitor caching
echo "2. Cache Status:"
if [ -d /var/cache/nginx ]; then
    echo "Cache directory exists"
    du -sh /var/cache/nginx
else
    echo "Cache directory not found"
fi

# Monitor rate limiting
echo "3. Rate Limiting Status:"
tail -100 /var/log/nginx/access.log | grep -c " 429 " || echo "No rate limit hits"

# Monitor security
echo "4. Security Status:"
tail -100 /var/log/nginx/access.log | grep -c " 403 " || echo "No 403 errors"
```

## 21.7 Pattern Testing

### 1. Unit Testing:
```bash
#!/bin/bash
# Unit testing for patterns

echo "Nginx Pattern Unit Tests"
echo "======================="

# Test configuration syntax
echo "1. Testing configuration syntax..."
nginx -t || exit 1

# Test load balancing
echo "2. Testing load balancing..."
# Test with multiple requests
for i in {1..5}; do
    curl -s http://localhost/ > /dev/null
done

# Test caching
echo "3. Testing caching..."
# Test cache headers
curl -I http://localhost/ | grep -i "cache-control" || echo "No cache headers"

# Test rate limiting
echo "4. Testing rate limiting..."
# Test rate limit response
for i in {1..10}; do
    curl -s -w "%{http_code}\n" -o /dev/null http://localhost/api/
done
```

### 2. Integration Testing:
```bash
#!/bin/bash
# Integration testing for patterns

echo "Nginx Pattern Integration Tests"
echo "=============================="

# Test with real applications
echo "1. Testing with real applications..."
# Start test applications
docker run -d --name app1 -p 8001:80 nginx:alpine
docker run -d --name app2 -p 8002:80 nginx:alpine

# Wait for applications to start
sleep 5

# Test load balancing
echo "2. Testing load balancing integration..."
for i in {1..10}; do
    curl -s http://localhost/ | grep -o "Server: [^<]*" || echo "No server header"
done

# Test caching integration
echo "3. Testing caching integration..."
curl -I http://localhost/ | grep -i "cache-control" || echo "No cache headers"

# Cleanup
docker stop app1 app2
docker rm app1 app2
```

### 3. Performance Testing:
```bash
#!/bin/bash
# Performance testing for patterns

echo "Nginx Pattern Performance Tests"
echo "=============================="

# Load testing
echo "1. Load testing..."
ab -n 1000 -c 10 http://localhost/ || exit 1

# Stress testing
echo "2. Stress testing..."
wrk -t12 -c400 -d30s http://localhost/ || exit 1

# Response time testing
echo "3. Response time testing..."
RESPONSE_TIME=$(curl -w "%{time_total}" -o /dev/null -s http://localhost/)
if (( $(echo "$RESPONSE_TIME > 1.0" | bc -l) )); then
    echo "WARNING: High response time: ${RESPONSE_TIME}s"
fi
```

## 21.8 Pattern Performance

### 1. Performance Monitoring:
```bash
#!/bin/bash
# Performance monitoring for patterns

echo "Nginx Pattern Performance Monitoring"
echo "==================================="

# Monitor system resources
echo "1. System Resources:"
echo "   CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "   Memory Usage: $(free | grep Mem | awk '{printf "%.1f%%", $3/$2 * 100.0}')"
echo "   Load Average: $(uptime | awk '{print $10,$11,$12}')"

# Monitor Nginx performance
echo "2. Nginx Performance:"
if curl -s http://localhost/nginx_status > /dev/null 2>&1; then
    curl -s http://localhost/nginx_status | awk '{
        print "   Active connections: " $3
        print "   Server accepts handled requests: " $4 " " $5 " " $6
        print "   Reading: " $7 " Writing: " $8 " Waiting: " $9
    }'
else
    echo "   Nginx status endpoint not available"
fi

# Monitor pattern-specific metrics
echo "3. Pattern-specific Metrics:"
echo "   Load balancing distribution:"
for i in {1..10}; do
    curl -s http://localhost/ | grep -o "Server: [^<]*" || echo "No server header"
done
```

### 2. Performance Optimization:
```bash
#!/bin/bash
# Performance optimization for patterns

echo "Nginx Pattern Performance Optimization"
echo "====================================="

# Optimize worker processes
echo "1. Optimizing worker processes..."
CPU_CORES=$(nproc)
echo "   Detected CPU cores: $CPU_CORES"

# Update configuration
sed -i "s/worker_processes.*/worker_processes $CPU_CORES;/" /etc/nginx/nginx.conf
sed -i "s/worker_connections.*/worker_connections 1024;/" /etc/nginx/nginx.conf

# Test configuration
if nginx -t; then
    echo "   Configuration test passed. Reloading Nginx..."
    nginx -s reload
    echo "   Nginx reloaded successfully."
else
    echo "   Configuration test failed. Please check the configuration."
fi

# Optimize caching
echo "2. Optimizing caching..."
if [ -d /var/cache/nginx ]; then
    echo "   Cache directory exists"
    du -sh /var/cache/nginx
else
    echo "   Creating cache directory..."
    mkdir -p /var/cache/nginx
    chown nginx:nginx /var/cache/nginx
fi
```

## 21.9 Pattern Troubleshooting

### 1. Common Pattern Issues:
```bash
#!/bin/bash
# Pattern troubleshooting script

echo "Nginx Pattern Troubleshooting"
echo "============================"

# Check load balancing
echo "1. Load Balancing Issues:"
echo "   Checking upstream servers..."
netstat -tlnp | grep -E ":(8001|8002|8003)" || echo "   No upstream servers listening"

# Check caching
echo "2. Caching Issues:"
echo "   Checking cache directory..."
if [ -d /var/cache/nginx ]; then
    echo "   Cache directory exists"
    ls -la /var/cache/nginx
else
    echo "   Cache directory not found"
fi

# Check rate limiting
echo "3. Rate Limiting Issues:"
echo "   Checking rate limit zones..."
nginx -T | grep limit_req_zone || echo "   No rate limit zones configured"

# Check security
echo "4. Security Issues:"
echo "   Checking security headers..."
curl -I http://localhost/ | grep -i "x-frame-options" || echo "   No security headers found"
```

### 2. Pattern Debugging:
```bash
#!/bin/bash
# Pattern debugging script

echo "Nginx Pattern Debugging"
echo "======================"

# Enable debug logging
echo "1. Enabling debug logging..."
nginx -T | grep error_log || echo "   No error log configured"

# Check pattern-specific logs
echo "2. Checking pattern-specific logs..."
if [ -f /var/log/nginx/access.log ]; then
    echo "   Recent access logs:"
    tail -5 /var/log/nginx/access.log
else
    echo "   No access log found"
fi

# Check pattern configuration
echo "3. Checking pattern configuration..."
nginx -T | grep -E "(upstream|proxy_cache|limit_req)" || echo "   No pattern configuration found"
```

## 21.10 Pattern Documentation

### 1. Pattern Catalog:
```bash
#!/bin/bash
# Pattern catalog script

echo "Nginx Pattern Catalog"
echo "===================="

echo "1. Load Balancing Patterns:"
echo "   - Round Robin: Equal distribution"
echo "   - Weighted Round Robin: Custom weights"
echo "   - Least Connections: Based on active connections"
echo "   - IP Hash: Session persistence"
echo "   - Health Checks: Automatic failover"

echo ""
echo "2. Caching Patterns:"
echo "   - Proxy Caching: Backend response caching"
echo "   - FastCGI Caching: PHP response caching"
echo "   - Browser Caching: Static file caching"
echo "   - Cache Invalidation: Manual cache clearing"

echo ""
echo "3. Security Patterns:"
echo "   - Rate Limiting: Request throttling"
echo "   - Authentication: User verification"
echo "   - Security Headers: HTTP security"
echo "   - DDoS Protection: Attack mitigation"

echo ""
echo "4. Performance Patterns:"
echo "   - Compression: Response compression"
echo "   - Connection Optimization: Keep-alive tuning"
echo "   - Buffer Optimization: Memory management"
echo "   - Worker Optimization: Process tuning"
```

### 2. Pattern Implementation Guide:
```bash
#!/bin/bash
# Pattern implementation guide

echo "Nginx Pattern Implementation Guide"
echo "================================="

echo "1. Choose the right pattern for your use case"
echo "2. Copy the pattern configuration"
echo "3. Customize the configuration for your environment"
echo "4. Test the configuration with 'nginx -t'"
echo "5. Deploy the configuration"
echo "6. Monitor the pattern performance"
echo "7. Troubleshoot any issues"
echo "8. Document the implementation"
```