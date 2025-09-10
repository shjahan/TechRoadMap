# Section 3 - Nginx Configuration

## 3.1 Configuration Concepts

پیکربندی Nginx بر اساس یک سیستم سلسله‌مراتبی و اعلانی است که به شما امکان کنترل دقیق رفتار سرور را می‌دهد.

### مفاهیم کلیدی:
- **Contexts**: بخش‌های مختلف پیکربندی که قوانین خاص خود را دارند
- **Directives**: دستورات پیکربندی که رفتار Nginx را تعریف می‌کنند
- **Variables**: متغیرهایی که در runtime مقداردهی می‌شوند
- **Inheritance**: قوانین ارث‌بری تنظیمات از سطوح بالاتر

### ساختار سلسله‌مراتبی:
```
Main Context (Global)
├── Events Context
├── HTTP Context
│   ├── Server Context (Virtual Hosts)
│   │   ├── Location Context
│   │   └── Location Context
│   └── Upstream Context
└── Mail Context (Optional)
```

### مثال پایه:
```nginx
# Main context
user nginx;
worker_processes auto;

# Events context
events {
    worker_connections 1024;
}

# HTTP context
http {
    # Global settings
    sendfile on;
    
    # Server context
    server {
        listen 80;
        server_name example.com;
        
        # Location context
        location / {
            root /var/www/html;
        }
    }
}
```

## 3.2 Configuration Files

فایل‌های پیکربندی Nginx در مکان‌های مختلف قرار دارند:

### فایل اصلی:
```bash
# فایل پیکربندی اصلی
/etc/nginx/nginx.conf

# فایل‌های پیکربندی اضافی
/etc/nginx/conf.d/*.conf
/etc/nginx/sites-available/*
/etc/nginx/sites-enabled/*
```

### ساختار فایل اصلی:
```nginx
# /etc/nginx/nginx.conf
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
    types_hash_max_size 2048;
    
    # MIME types
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    
    # Include additional configurations
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### فایل‌های جداگانه:
```nginx
# /etc/nginx/sites-available/example.com
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

## 3.3 Configuration Directives

Directive ها دستورات پیکربندی هستند که رفتار Nginx را تعریف می‌کنند:

### انواع Directives:

#### 1. Simple Directives:
```nginx
# Directives ساده
user nginx;
worker_processes 4;
error_log /var/log/nginx/error.log;
```

#### 2. Block Directives:
```nginx
# Directives بلوکی
events {
    worker_connections 1024;
    use epoll;
}

http {
    sendfile on;
    tcp_nopush on;
}
```

#### 3. Context-specific Directives:
```nginx
# Directives مخصوص context
server {
    listen 80;
    server_name example.com;
    
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

### Directives مهم:

#### Worker Configuration:
```nginx
# تنظیمات worker processes
worker_processes auto;                    # تعداد worker processes
worker_cpu_affinity 0001 0010 0100 1000; # CPU affinity
worker_rlimit_nofile 65535;              # حداکثر فایل‌های باز
```

#### Event Configuration:
```nginx
events {
    worker_connections 1024;    # اتصالات همزمان
    use epoll;                  # روش event
    multi_accept on;            # پذیرش چندگانه
    accept_mutex off;           # mutex برای accept
}
```

#### HTTP Configuration:
```nginx
http {
    sendfile on;                # استفاده از sendfile
    tcp_nopush on;              # TCP_NOPUSH
    tcp_nodelay on;             # TCP_NODELAY
    keepalive_timeout 65;       # timeout برای keep-alive
    client_max_body_size 10M;   # حداکثر اندازه body
}
```

## 3.4 Configuration Contexts

Context ها بخش‌های مختلف پیکربندی هستند که قوانین خاص خود را دارند:

### 1. Main Context:
```nginx
# تنظیمات کلی
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;
```

### 2. Events Context:
```nginx
# تنظیمات event handling
events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
    accept_mutex off;
}
```

### 3. HTTP Context:
```nginx
# تنظیمات HTTP
http {
    # Global HTTP settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    
    # Server blocks
    server {
        listen 80;
        server_name example.com;
    }
    
    # Upstream blocks
    upstream backend {
        server 192.168.1.10:8080;
    }
}
```

### 4. Server Context:
```nginx
# Virtual host configuration
server {
    listen 80;
    server_name example.com www.example.com;
    
    # Location blocks
    location / {
        root /var/www/html;
    }
    
    location /api/ {
        proxy_pass http://backend;
    }
}
```

### 5. Location Context:
```nginx
# URL matching and processing
location / {
    root /var/www/html;
    index index.html;
    try_files $uri $uri/ =404;
}

location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 6. Upstream Context:
```nginx
# Load balancing configuration
upstream backend {
    server 192.168.1.10:8080 weight=3;
    server 192.168.1.11:8080 weight=2;
    server 192.168.1.12:8080 weight=1;
    
    keepalive 32;
}
```

## 3.5 Configuration Best Practices

بهترین روش‌های پیکربندی Nginx:

### 1. سازماندهی فایل‌ها:
```bash
# ساختار پیشنهادی
/etc/nginx/
├── nginx.conf              # فایل اصلی
├── conf.d/                 # تنظیمات اضافی
│   ├── security.conf       # تنظیمات امنیتی
│   ├── gzip.conf          # تنظیمات فشرده‌سازی
│   └── rate-limiting.conf  # تنظیمات محدودیت
├── sites-available/        # سایت‌های موجود
│   ├── example.com
│   └── api.example.com
└── sites-enabled/          # سایت‌های فعال
    ├── example.com -> ../sites-available/example.com
    └── api.example.com -> ../sites-available/api.example.com
```

### 2. استفاده از Include:
```nginx
# در nginx.conf
http {
    # تنظیمات پایه
    sendfile on;
    tcp_nopush on;
    
    # Include فایل‌های اضافی
    include /etc/nginx/conf.d/security.conf;
    include /etc/nginx/conf.d/gzip.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### 3. متغیرها و Template ها:
```nginx
# استفاده از متغیرها
map $http_user_agent $is_mobile {
    default 0;
    ~*mobile 1;
}

server {
    listen 80;
    server_name example.com;
    
    # استفاده از متغیر
    if ($is_mobile) {
        root /var/www/mobile;
    }
    else {
        root /var/www/desktop;
    }
}
```

### 4. Error Handling:
```nginx
# صفحه‌های خطای سفارشی
server {
    listen 80;
    server_name example.com;
    
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    
    location = /404.html {
        root /var/www/error;
        internal;
    }
    
    location = /50x.html {
        root /var/www/error;
        internal;
    }
}
```

## 3.6 Configuration Testing

تست پیکربندی Nginx:

### 1. تست Syntax:
```bash
# تست syntax پیکربندی
nginx -t

# تست با نمایش کامل پیکربندی
nginx -T
```

### 2. تست Reload:
```bash
# reload پیکربندی بدون restart
nginx -s reload

# graceful restart
nginx -s quit
nginx
```

### 3. تست Performance:
```bash
# تست عملکرد با ab
ab -n 1000 -c 10 http://example.com/

# تست با wrk
wrk -t12 -c400 -d30s http://example.com/
```

### 4. تست Security:
```bash
# تست SSL
openssl s_client -connect example.com:443

# تست headers
curl -I https://example.com/
```

### 5. تست Configuration:
```nginx
# تست پیکربندی با logging
error_log /var/log/nginx/debug.log debug;

# تست با stub_status
location /nginx_status {
    stub_status on;
    access_log off;
    allow 127.0.0.1;
    deny all;
}
```

## 3.7 Configuration Performance

بهینه‌سازی عملکرد پیکربندی:

### 1. Worker Optimization:
```nginx
# بهینه‌سازی worker processes
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}
```

### 2. Network Optimization:
```nginx
# بهینه‌سازی شبکه
http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 100;
}
```

### 3. Buffer Optimization:
```nginx
# بهینه‌سازی buffer ها
http {
    client_body_buffer_size 128k;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    client_max_body_size 10m;
}
```

### 4. Caching Optimization:
```nginx
# بهینه‌سازی caching
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m;

location / {
    proxy_cache my_cache;
    proxy_cache_valid 200 302 10m;
    proxy_cache_valid 404 1m;
    proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
}
```

## 3.8 Configuration Troubleshooting

عیب‌یابی پیکربندی Nginx:

### 1. Common Issues:

#### Syntax Errors:
```bash
# خطای syntax
nginx -t
# nginx: [emerg] unexpected "}" in /etc/nginx/nginx.conf:45
```

#### Permission Issues:
```bash
# مشکل دسترسی
chown -R nginx:nginx /var/log/nginx
chmod 755 /var/log/nginx
```

#### Port Conflicts:
```bash
# بررسی پورت‌های استفاده شده
netstat -tlnp | grep :80
lsof -i :80
```

### 2. Debugging Tools:

#### Error Logs:
```nginx
# فعال‌سازی debug logging
error_log /var/log/nginx/error.log debug;
```

#### Access Logs:
```nginx
# logging تفصیلی
log_format detailed '$remote_addr - $remote_user [$time_local] '
                   '"$request" $status $body_bytes_sent '
                   '"$http_referer" "$http_user_agent" '
                   'rt=$request_time uct="$upstream_connect_time" '
                   'uht="$upstream_header_time" urt="$upstream_response_time"';
```

#### Status Module:
```nginx
# فعال‌سازی status module
location /nginx_status {
    stub_status on;
    access_log off;
    allow 127.0.0.1;
    deny all;
}
```

### 3. Common Solutions:

#### 502 Bad Gateway:
```nginx
# بررسی upstream servers
upstream backend {
    server 192.168.1.10:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 backup;
}
```

#### 404 Not Found:
```nginx
# بررسی root directory
server {
    listen 80;
    server_name example.com;
    root /var/www/html;  # مسیر صحیح
    index index.html;
}
```

## 3.9 Configuration Security

امنیت پیکربندی Nginx:

### 1. Hide Server Information:
```nginx
# مخفی کردن اطلاعات سرور
server_tokens off;

# حذف header های اضافی
more_clear_headers 'Server';
more_clear_headers 'X-Powered-By';
```

### 2. Security Headers:
```nginx
# هدرهای امنیتی
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

### 3. Access Control:
```nginx
# کنترل دسترسی
location /admin {
    allow 192.168.1.0/24;
    deny all;
    auth_basic "Admin Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

### 4. Rate Limiting:
```nginx
# محدودیت درخواست
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

location /api/ {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://backend;
}

location /login {
    limit_req zone=login burst=5 nodelay;
    # login handling
}
```

### 5. SSL/TLS Security:
```nginx
# تنظیمات SSL امن
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

## 3.10 Configuration Documentation

مستندسازی پیکربندی Nginx:

### 1. Comments:
```nginx
# Main configuration file
# This file contains the basic configuration for Nginx

# User and group for worker processes
user nginx;

# Number of worker processes (auto = number of CPU cores)
worker_processes auto;

# Error log file
error_log /var/log/nginx/error.log;

# Process ID file
pid /run/nginx.pid;

# Events context - configuration for connection processing
events {
    # Maximum number of simultaneous connections per worker
    worker_connections 1024;
    
    # Use epoll event method (Linux)
    use epoll;
    
    # Accept multiple connections at once
    multi_accept on;
}
```

### 2. Configuration Templates:
```nginx
# Template for basic server configuration
# Copy this template and modify as needed

server {
    # Listen on port 80
    listen 80;
    
    # Server name (domain)
    server_name example.com www.example.com;
    
    # Document root
    root /var/www/html;
    
    # Default index files
    index index.html index.htm;
    
    # Basic location block
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
}
```

### 3. Documentation Standards:
```nginx
# =============================================================================
# Nginx Configuration Documentation
# =============================================================================
# 
# File: /etc/nginx/sites-available/example.com
# Purpose: Virtual host configuration for example.com
# Author: System Administrator
# Last Modified: 2024-01-15
# 
# =============================================================================
# Configuration Overview
# =============================================================================
# 
# This configuration provides:
# - HTTP to HTTPS redirect
# - Static file serving with caching
# - API proxy to backend services
# - Security headers
# - Rate limiting
# 
# =============================================================================
# Dependencies
# =============================================================================
# 
# Required modules:
# - http_ssl_module
# - http_realip_module
# - http_secure_link_module
# 
# =============================================================================
```

### 4. Version Control:
```bash
# استفاده از Git برای مدیریت پیکربندی
git init /etc/nginx
git add .
git commit -m "Initial Nginx configuration"

# ایجاد branch برای تغییرات
git checkout -b feature/ssl-configuration
# تغییرات...
git commit -m "Add SSL configuration"
git checkout main
git merge feature/ssl-configuration
```