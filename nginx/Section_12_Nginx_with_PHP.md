# Section 12 - Nginx with PHP

## 12.1 PHP Integration Concepts

PHP integration with Nginx involves configuring Nginx to work as a reverse proxy for PHP applications, typically using FastCGI protocol for communication between Nginx and PHP processes.

### Key Concepts:
- **FastCGI Protocol**: Communication protocol between web server and application server
- **PHP-FPM**: FastCGI Process Manager for PHP
- **Process Management**: How PHP processes are spawned and managed
- **Request Handling**: How HTTP requests are processed through the stack

### Real-world Analogy:
Think of Nginx with PHP like a restaurant with a kitchen:
- **Nginx** is the waiter who takes orders and serves customers
- **PHP-FPM** is the kitchen staff who prepares the food (processes requests)
- **FastCGI** is the communication system between waiter and kitchen
- **PHP processes** are the individual chefs working on different orders

### Architecture Overview:
```
Client Request → Nginx → FastCGI → PHP-FPM → PHP Process → Response
```

### Example Basic Configuration:
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.php index.html;

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

## 12.2 FastCGI Configuration

FastCGI (Fast Common Gateway Interface) is a protocol for interfacing interactive programs with web servers. It's more efficient than traditional CGI because it keeps processes alive between requests.

### FastCGI Benefits:
- **Persistent Processes**: PHP processes stay alive between requests
- **Better Performance**: No process creation overhead
- **Resource Efficiency**: Shared memory and connection pooling
- **Scalability**: Can handle multiple concurrent requests

### Basic FastCGI Configuration:
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.php;

    location ~ \.php$ {
        # FastCGI configuration
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

### Advanced FastCGI Configuration:
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.php;

    location ~ \.php$ {
        # FastCGI settings
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        
        # FastCGI parameters
        fastcgi_connect_timeout 60s;
        fastcgi_send_timeout 60s;
        fastcgi_read_timeout 60s;
        fastcgi_buffer_size 4k;
        fastcgi_buffers 8 4k;
        fastcgi_busy_buffers_size 8k;
        fastcgi_temp_file_write_size 8k;
        
        # Security
        fastcgi_hide_header X-Powered-By;
        
        include fastcgi_params;
    }
}
```

### FastCGI Parameters:
```nginx
# Common FastCGI parameters
fastcgi_param QUERY_STRING $query_string;
fastcgi_param REQUEST_METHOD $request_method;
fastcgi_param CONTENT_TYPE $content_type;
fastcgi_param CONTENT_LENGTH $content_length;
fastcgi_param SCRIPT_NAME $fastcgi_script_name;
fastcgi_param REQUEST_URI $request_uri;
fastcgi_param DOCUMENT_URI $document_uri;
fastcgi_param DOCUMENT_ROOT $document_root;
fastcgi_param SERVER_PROTOCOL $server_protocol;
fastcgi_param HTTPS $https if_not_empty;
fastcgi_param GATEWAY_INTERFACE CGI/1.1;
fastcgi_param SERVER_SOFTWARE nginx/$nginx_version;
fastcgi_param REMOTE_ADDR $remote_addr;
fastcgi_param REMOTE_PORT $remote_port;
fastcgi_param SERVER_ADDR $server_addr;
fastcgi_param SERVER_PORT $server_port;
fastcgi_param SERVER_NAME $server_name;
```

## 12.3 PHP-FPM Integration

PHP-FPM (FastCGI Process Manager) is an alternative PHP FastCGI implementation with additional features useful for heavy-loaded sites.

### PHP-FPM Features:
- **Process Management**: Automatic process spawning and recycling
- **Pool Configuration**: Multiple pools for different applications
- **Status Page**: Built-in monitoring capabilities
- **Slow Log**: Logging of slow requests
- **Advanced Logging**: Detailed request logging

### PHP-FPM Pool Configuration:
```ini
; /etc/php/8.1/fpm/pool.d/www.conf
[www]
user = www-data
group = www-data
listen = /var/run/php/php8.1-fpm.sock
listen.owner = www-data
listen.group = www-data
listen.mode = 0660

pm = dynamic
pm.max_children = 50
pm.start_servers = 5
pm.min_spare_servers = 5
pm.max_spare_servers = 35
pm.max_requests = 1000

; Slow log
slowlog = /var/log/php8.1-fpm-slow.log
request_slowlog_timeout = 10s

; Status page
pm.status_path = /fpm-status
ping.path = /fpm-ping
```

### Nginx Configuration for PHP-FPM:
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.php;

    # PHP processing
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    # PHP-FPM status page
    location ~ ^/(fpm-status|fpm-ping)$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
        allow 127.0.0.1;
        deny all;
    }
}
```

### Multiple PHP-FPM Pools:
```ini
; Pool for main website
[www]
user = www-data
group = www-data
listen = /var/run/php/php8.1-fpm-www.sock
pm = dynamic
pm.max_children = 20

; Pool for API
[api]
user = www-data
group = www-data
listen = /var/run/php/php8.1-fpm-api.sock
pm = dynamic
pm.max_children = 10
```

```nginx
# Nginx configuration for multiple pools
server {
    listen 80;
    server_name example.com;
    root /var/www/html;

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm-www.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}

server {
    listen 80;
    server_name api.example.com;
    root /var/www/api;

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm-api.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

## 12.4 PHP Best Practices

### 1. Security Configuration:
```nginx
# Hide PHP version
fastcgi_hide_header X-Powered-By;

# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;

# Prevent access to sensitive files
location ~ /\. {
    deny all;
}

location ~ \.(htaccess|htpasswd|ini|log|sh|sql|conf)$ {
    deny all;
}
```

### 2. Performance Optimization:
```nginx
# Enable gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

# Browser caching for static files
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}

# PHP file caching
location ~ \.php$ {
    fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    fastcgi_cache my_cache;
    fastcgi_cache_valid 200 302 10m;
    fastcgi_cache_valid 404 1m;
    fastcgi_cache_key "$scheme$request_method$host$request_uri";
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
}
```

### 3. Error Handling:
```nginx
# Custom error pages
error_page 404 /404.html;
error_page 500 502 503 504 /50x.html;

# PHP error handling
location ~ \.php$ {
    fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    fastcgi_intercept_errors on;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
}
```

### 4. Request Size Limits:
```nginx
# Client body size
client_max_body_size 10M;

# PHP upload limits
location ~ \.php$ {
    fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_param PHP_VALUE "upload_max_filesize=10M \n post_max_size=10M";
    include fastcgi_params;
}
```

## 12.5 PHP Testing

### 1. Basic PHP Test:
```php
<?php
// test.php
phpinfo();
?>
```

### 2. Performance Testing:
```bash
# Test PHP response time
curl -w "@curl-format.txt" -o /dev/null -s http://example.com/test.php

# Load testing with ab
ab -n 1000 -c 10 http://example.com/test.php

# Load testing with wrk
wrk -t12 -c400 -d30s http://example.com/test.php
```

### 3. PHP-FPM Status Testing:
```bash
# Check PHP-FPM status
curl http://example.com/fpm-status

# Check PHP-FPM ping
curl http://example.com/fpm-ping
```

### 4. Error Testing:
```php
<?php
// error-test.php
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Test different error types
echo "Testing PHP errors...\n";

// Notice
echo $undefined_variable;

// Warning
include 'nonexistent_file.php';

// Fatal error
function test() {
    test(); // Recursive call
}
test();
?>
```

## 12.6 PHP Performance

### 1. PHP-FPM Pool Optimization:
```ini
; Optimized PHP-FPM configuration
[www]
pm = dynamic
pm.max_children = 50
pm.start_servers = 10
pm.min_spare_servers = 5
pm.max_spare_servers = 20
pm.max_requests = 1000

; Process recycling
pm.process_idle_timeout = 10s
pm.max_requests = 1000
```

### 2. Nginx Caching for PHP:
```nginx
# FastCGI cache configuration
fastcgi_cache_path /var/cache/nginx levels=1:2 keys_zone=php_cache:10m max_size=1g inactive=60m;

server {
    listen 80;
    server_name example.com;
    root /var/www/html;

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_cache php_cache;
        fastcgi_cache_valid 200 302 10m;
        fastcgi_cache_valid 404 1m;
        fastcgi_cache_key "$scheme$request_method$host$request_uri";
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

### 3. OpCache Configuration:
```ini
; PHP OpCache settings
opcache.enable=1
opcache.memory_consumption=128
opcache.interned_strings_buffer=8
opcache.max_accelerated_files=4000
opcache.revalidate_freq=2
opcache.fast_shutdown=1
opcache.enable_cli=1
```

### 4. Memory Optimization:
```nginx
# Buffer optimization
fastcgi_buffer_size 4k;
fastcgi_buffers 8 4k;
fastcgi_busy_buffers_size 8k;
fastcgi_temp_file_write_size 8k;

# Connection optimization
fastcgi_connect_timeout 60s;
fastcgi_send_timeout 60s;
fastcgi_read_timeout 60s;
```

## 12.7 PHP Troubleshooting

### 1. Common Issues:

#### 502 Bad Gateway:
```bash
# Check PHP-FPM status
systemctl status php8.1-fpm

# Check PHP-FPM logs
tail -f /var/log/php8.1-fpm.log

# Check socket permissions
ls -la /var/run/php/php8.1-fpm.sock
```

#### 504 Gateway Timeout:
```nginx
# Increase timeout values
fastcgi_connect_timeout 300s;
fastcgi_send_timeout 300s;
fastcgi_read_timeout 300s;
```

#### Memory Issues:
```bash
# Check PHP memory usage
ps aux | grep php-fpm

# Check PHP-FPM pool status
curl http://example.com/fpm-status
```

### 2. Debugging Tools:
```nginx
# Enable debug logging
error_log /var/log/nginx/debug.log debug;

# PHP error logging
location ~ \.php$ {
    fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_param PHP_VALUE "log_errors=On \n error_log=/var/log/php_errors.log";
    include fastcgi_params;
}
```

### 3. Performance Monitoring:
```bash
# Monitor PHP-FPM processes
watch -n 1 'ps aux | grep php-fpm | wc -l'

# Monitor memory usage
watch -n 1 'ps aux --sort=-%mem | head -10'

# Monitor slow requests
tail -f /var/log/php8.1-fpm-slow.log
```

## 12.8 PHP Security

### 1. File Upload Security:
```nginx
# Secure file upload handling
location ~ \.php$ {
    # Prevent execution of uploaded files
    if ($uri ~* ^/uploads/.*\.php$) {
        return 403;
    }
    
    fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
}
```

### 2. Path Traversal Protection:
```nginx
# Prevent path traversal attacks
location ~ \.php$ {
    # Validate script path
    if ($fastcgi_script_name ~* \.\./) {
        return 403;
    }
    
    fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
}
```

### 3. Rate Limiting:
```nginx
# Rate limiting for PHP endpoints
limit_req_zone $binary_remote_addr zone=php:10m rate=10r/s;

location ~ \.php$ {
    limit_req zone=php burst=20 nodelay;
    
    fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
}
```

### 4. Security Headers:
```nginx
# Security headers for PHP applications
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Hide server information
fastcgi_hide_header X-Powered-By;
server_tokens off;
```

## 12.9 PHP Documentation

### 1. Configuration Documentation:
```nginx
# =============================================================================
# PHP Integration Configuration
# =============================================================================
# 
# This configuration provides:
# - FastCGI communication with PHP-FPM
# - Security headers and protections
# - Performance optimizations
# - Error handling and logging
# 
# Dependencies:
# - PHP 8.1 or higher
# - PHP-FPM service
# - FastCGI module for Nginx
# 
# =============================================================================

server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.php index.html;

    # PHP processing with security
    location ~ \.php$ {
        # FastCGI configuration
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        
        # Security settings
        fastcgi_hide_header X-Powered-By;
        
        # Performance settings
        fastcgi_cache my_cache;
        fastcgi_cache_valid 200 302 10m;
        
        include fastcgi_params;
    }
}
```

### 2. Monitoring Documentation:
```bash
#!/bin/bash
# PHP-FPM monitoring script

echo "=== PHP-FPM Status ==="
curl -s http://localhost/fpm-status | grep -E "(pool|process manager|start time|accepted conn|listen queue|max children|active processes|total processes)"

echo ""
echo "=== PHP-FPM Ping ==="
curl -s http://localhost/fpm-ping

echo ""
echo "=== PHP-FPM Processes ==="
ps aux | grep php-fpm | wc -l

echo ""
echo "=== Memory Usage ==="
ps aux --sort=-%mem | grep php-fpm | head -5
```

## 12.10 PHP Monitoring

### 1. PHP-FPM Status Page:
```nginx
# PHP-FPM status monitoring
location ~ ^/(fpm-status|fpm-ping)$ {
    fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    include fastcgi_params;
    
    # Restrict access
    allow 127.0.0.1;
    allow 192.168.1.0/24;
    deny all;
}
```

### 2. Logging Configuration:
```nginx
# Detailed logging for PHP requests
log_format php_requests '$remote_addr - $remote_user [$time_local] '
                       '"$request" $status $body_bytes_sent '
                       '"$http_referer" "$http_user_agent" '
                       'rt=$request_time uct="$upstream_connect_time" '
                       'uht="$upstream_header_time" urt="$upstream_response_time" '
                       'upstream_addr="$upstream_addr" '
                       'upstream_status="$upstream_status"';

server {
    listen 80;
    server_name example.com;
    
    access_log /var/log/nginx/php_requests.log php_requests;
    
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

### 3. Performance Monitoring:
```bash
#!/bin/bash
# PHP performance monitoring

echo "=== PHP Performance Metrics ==="
echo "Date: $(date)"
echo ""

# PHP-FPM status
echo "PHP-FPM Status:"
curl -s http://localhost/fpm-status | grep -E "(active processes|total processes|max children)"

# Memory usage
echo ""
echo "Memory Usage:"
ps aux --sort=-%mem | grep php-fpm | head -5

# Response time
echo ""
echo "Response Time Test:"
time curl -s http://localhost/test.php > /dev/null

# Error rate
echo ""
echo "Error Rate (last 100 requests):"
tail -100 /var/log/nginx/access.log | grep -c " 5[0-9][0-9] "
```

### 4. Alerting Script:
```bash
#!/bin/bash
# PHP monitoring and alerting

THRESHOLD_MEMORY=80
THRESHOLD_RESPONSE_TIME=2.0
ALERT_EMAIL="admin@example.com"

# Check memory usage
MEMORY_USAGE=$(ps aux --sort=-%mem | grep php-fpm | head -1 | awk '{print $4}')
if (( $(echo "$MEMORY_USAGE > $THRESHOLD_MEMORY" | bc -l) )); then
    echo "ALERT: High PHP memory usage: $MEMORY_USAGE%" | mail -s "PHP Memory Alert" $ALERT_EMAIL
fi

# Check response time
RESPONSE_TIME=$(time curl -s http://localhost/test.php > /dev/null 2>&1 | grep real | awk '{print $2}' | cut -d'm' -f1)
if (( $(echo "$RESPONSE_TIME > $THRESHOLD_RESPONSE_TIME" | bc -l) )); then
    echo "ALERT: High PHP response time: ${RESPONSE_TIME}s" | mail -s "PHP Performance Alert" $ALERT_EMAIL
fi
```