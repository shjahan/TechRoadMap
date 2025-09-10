# Section 4 - Virtual Hosts

## 4.1 Virtual Host Concepts

Virtual Host (میزبان مجازی) قابلیتی است که به یک سرور فیزیکی اجازه می‌دهد چندین دامنه یا وب‌سایت را روی همان IP آدرس میزبانی کند.

### مفاهیم کلیدی:
- **Name-based Virtual Hosts**: بر اساس نام دامنه
- **IP-based Virtual Hosts**: بر اساس IP آدرس
- **Port-based Virtual Hosts**: بر اساس شماره پورت
- **Server Blocks**: بلوک‌های پیکربندی برای هر virtual host

### تشبیه دنیای واقعی:
Virtual Host مانند یک ساختمان چند طبقه است که:
- هر طبقه یک آپارتمان جداگانه دارد (دامنه)
- همه آپارتمان‌ها در همان آدرس هستند (IP)
- هر آپارتمان ساکنان و قوانین خاص خود را دارد (پیکربندی)

### مثال پایه:
```nginx
# Virtual host برای example.com
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}

# Virtual host برای api.example.com
server {
    listen 80;
    server_name api.example.com;
    root /var/www/api;
    index index.php;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

## 4.2 Server Blocks

Server Blocks بلوک‌های پیکربندی هستند که هر virtual host را تعریف می‌کنند:

### ساختار Server Block:
```nginx
server {
    # Basic configuration
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.html;
    
    # Location blocks
    location / {
        # Processing rules
    }
    
    location /api/ {
        # API handling
    }
}
```

### تنظیمات اساسی:
```nginx
server {
    # Port و protocol
    listen 80;
    listen 443 ssl http2;
    
    # نام دامنه
    server_name example.com www.example.com;
    
    # مسیر root
    root /var/www/example.com;
    
    # فایل‌های پیش‌فرض
    index index.html index.htm index.php;
    
    # Logging
    access_log /var/log/nginx/example.com.access.log;
    error_log /var/log/nginx/example.com.error.log;
}
```

### مثال کامل:
```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com;
    index index.html index.htm;
    
    # Security
    server_tokens off;
    
    # Logging
    access_log /var/log/nginx/example.com.access.log main;
    error_log /var/log/nginx/example.com.error.log;
    
    # Main location
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Static files
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # API endpoint
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 4.3 Name-based Virtual Hosts

Name-based Virtual Hosts بر اساس نام دامنه درخواست‌ها را به virtual host مناسب هدایت می‌کنند:

### مزایا:
- استفاده بهینه از IP آدرس
- مدیریت آسان‌تر
- هزینه کمتر
- انعطاف‌پذیری بیشتر

### مثال پایه:
```nginx
# Virtual host اول
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}

# Virtual host دوم
server {
    listen 80;
    server_name blog.example.com;
    root /var/www/blog;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}

# Virtual host سوم
server {
    listen 80;
    server_name api.example.com;
    root /var/www/api;
    index index.php;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### تنظیمات پیشرفته:
```nginx
# Wildcard subdomains
server {
    listen 80;
    server_name *.example.com;
    root /var/www/wildcard;
    
    # استفاده از متغیر برای subdomain
    location / {
        set $subdomain $1;
        try_files /$subdomain$uri /$subdomain$uri/ /default$uri =404;
    }
}

# Multiple domains
server {
    listen 80;
    server_name example.com www.example.com example.org www.example.org;
    root /var/www/shared;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Default Server:
```nginx
# Default server برای درخواست‌های نامشخص
server {
    listen 80 default_server;
    server_name _;
    return 444;  # Close connection
}

# یا redirect به HTTPS
server {
    listen 80 default_server;
    server_name _;
    return 301 https://$host$request_uri;
}
```

## 4.4 IP-based Virtual Hosts

IP-based Virtual Hosts بر اساس IP آدرس درخواست‌ها را هدایت می‌کنند:

### کاربردها:
- میزبانی چندین IP روی یک سرور
- جداسازی کامل بین سایت‌ها
- امنیت بیشتر
- کنترل دقیق‌تر ترافیک

### مثال پایه:
```nginx
# Virtual host برای IP اول
server {
    listen 192.168.1.10:80;
    server_name _;
    root /var/www/site1;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}

# Virtual host برای IP دوم
server {
    listen 192.168.1.11:80;
    server_name _;
    root /var/www/site2;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### تنظیمات پیشرفته:
```nginx
# Multiple IPs on same port
server {
    listen 192.168.1.10:80;
    listen 192.168.1.11:80;
    server_name _;
    root /var/www/shared;
    
    location / {
        try_files $uri $uri/ =404;
    }
}

# IP-based with SSL
server {
    listen 192.168.1.10:443 ssl;
    server_name _;
    root /var/www/secure;
    
    ssl_certificate /path/to/cert.crt;
    ssl_certificate_key /path/to/key.key;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### تشخیص IP در Location:
```nginx
server {
    listen 80;
    server_name _;
    root /var/www/html;
    
    # Location بر اساس IP
    location / {
        if ($remote_addr ~ "^192\.168\.1\.(10|11)$") {
            root /var/www/internal;
        }
        if ($remote_addr ~ "^10\.0\.0\.") {
            root /var/www/vpn;
        }
        
        try_files $uri $uri/ =404;
    }
}
```

## 4.5 Port-based Virtual Hosts

Port-based Virtual Hosts بر اساس شماره پورت درخواست‌ها را هدایت می‌کنند:

### کاربردها:
- سرویس‌های مختلف روی پورت‌های مختلف
- API های مختلف
- محیط‌های مختلف (dev, staging, production)
- سرویس‌های داخلی

### مثال پایه:
```nginx
# Virtual host برای پورت 80
server {
    listen 80;
    server_name example.com;
    root /var/www/production;
    
    location / {
        try_files $uri $uri/ =404;
    }
}

# Virtual host برای پورت 8080
server {
    listen 8080;
    server_name example.com;
    root /var/www/staging;
    
    location / {
        try_files $uri $uri/ =404;
    }
}

# Virtual host برای پورت 3000
server {
    listen 3000;
    server_name example.com;
    root /var/www/development;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### تنظیمات پیشرفته:
```nginx
# Multiple ports for same content
server {
    listen 80;
    listen 8080;
    listen 3000;
    server_name example.com;
    root /var/www/html;
    
    location / {
        try_files $uri $uri/ =404;
    }
}

# Port-based API routing
server {
    listen 8080;
    server_name api.example.com;
    
    location /v1/ {
        proxy_pass http://backend-v1;
    }
    
    location /v2/ {
        proxy_pass http://backend-v2;
    }
}

server {
    listen 8081;
    server_name api.example.com;
    
    location /admin/ {
        proxy_pass http://admin-backend;
    }
}
```

### Port Security:
```nginx
# محدود کردن دسترسی به پورت‌های خاص
server {
    listen 8080;
    server_name _;
    
    # فقط IP های داخلی
    allow 192.168.1.0/24;
    allow 10.0.0.0/8;
    deny all;
    
    root /var/www/internal;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

## 4.6 Virtual Host Best Practices

بهترین روش‌های مدیریت Virtual Hosts:

### 1. سازماندهی فایل‌ها:
```bash
# ساختار پیشنهادی
/etc/nginx/
├── sites-available/        # تمام سایت‌ها
│   ├── example.com
│   ├── blog.example.com
│   ├── api.example.com
│   └── admin.example.com
├── sites-enabled/          # سایت‌های فعال
│   ├── example.com -> ../sites-available/example.com
│   └── api.example.com -> ../sites-available/api.example.com
└── nginx.conf
```

### 2. استفاده از Include:
```nginx
# در nginx.conf
http {
    # تنظیمات کلی
    sendfile on;
    tcp_nopush on;
    
    # Include virtual hosts
    include /etc/nginx/sites-enabled/*;
}
```

### 3. Default Server:
```nginx
# Default server برای درخواست‌های نامشخص
server {
    listen 80 default_server;
    listen 443 ssl default_server;
    server_name _;
    
    # Redirect به صفحه اصلی یا نمایش خطا
    return 444;
}
```

### 4. Security Headers:
```nginx
# هدرهای امنیتی مشترک
map $host $security_headers {
    default "X-Frame-Options: SAMEORIGIN";
}

server {
    listen 80;
    server_name example.com;
    
    # اعمال هدرهای امنیتی
    add_header $security_headers always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### 5. Logging:
```nginx
# Logging مخصوص هر virtual host
server {
    listen 80;
    server_name example.com;
    
    # Access log
    access_log /var/log/nginx/example.com.access.log main;
    
    # Error log
    error_log /var/log/nginx/example.com.error.log;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
```

## 4.7 Virtual Host Testing

تست Virtual Hosts:

### 1. تست Configuration:
```bash
# تست syntax
nginx -t

# تست با نمایش کامل
nginx -T
```

### 2. تست DNS:
```bash
# تست DNS resolution
nslookup example.com
dig example.com

# تست از client
curl -H "Host: example.com" http://server-ip/
```

### 3. تست HTTP Headers:
```bash
# تست Host header
curl -H "Host: example.com" -I http://server-ip/

# تست multiple hosts
curl -H "Host: blog.example.com" -I http://server-ip/
curl -H "Host: api.example.com" -I http://server-ip/
```

### 4. تست Ports:
```bash
# تست پورت‌های مختلف
curl http://server-ip:80/
curl http://server-ip:8080/
curl http://server-ip:3000/
```

### 5. تست Load:
```bash
# تست load با ab
ab -n 1000 -c 10 -H "Host: example.com" http://server-ip/

# تست با wrk
wrk -t12 -c400 -d30s -H "Host: example.com" http://server-ip/
```

## 4.8 Virtual Host Performance

بهینه‌سازی عملکرد Virtual Hosts:

### 1. Worker Optimization:
```nginx
# تنظیمات worker
worker_processes auto;
worker_connections 1024;

events {
    use epoll;
    multi_accept on;
}
```

### 2. Caching:
```nginx
# Caching برای static files
server {
    listen 80;
    server_name example.com;
    root /var/www/example.com;
    
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
}
```

### 3. Gzip Compression:
```nginx
# فشرده‌سازی
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript;
```

### 4. Connection Optimization:
```nginx
# بهینه‌سازی اتصالات
http {
    keepalive_timeout 65;
    keepalive_requests 100;
    tcp_nopush on;
    tcp_nodelay on;
}
```

## 4.9 Virtual Host Troubleshooting

عیب‌یابی Virtual Hosts:

### 1. Common Issues:

#### Wrong Server Block:
```bash
# بررسی server blocks فعال
nginx -T | grep -A 10 "server {"

# بررسی default server
nginx -T | grep "default_server"
```

#### DNS Issues:
```bash
# تست DNS
nslookup example.com
dig example.com

# تست از client
curl -v http://example.com/
```

#### Port Conflicts:
```bash
# بررسی پورت‌های استفاده شده
netstat -tlnp | grep :80
lsof -i :80
```

### 2. Debugging Tools:

#### Error Logs:
```bash
# بررسی error logs
tail -f /var/log/nginx/error.log

# بررسی access logs
tail -f /var/log/nginx/access.log
```

#### Configuration Test:
```bash
# تست پیکربندی
nginx -t

# تست با debug
nginx -t -c /etc/nginx/nginx.conf
```

### 3. Common Solutions:

#### 404 Errors:
```nginx
# بررسی root directory
server {
    listen 80;
    server_name example.com;
    root /var/www/example.com;  # مسیر صحیح
    index index.html;
}
```

#### 502 Bad Gateway:
```nginx
# بررسی upstream configuration
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080 backup;
}
```

## 4.10 Virtual Host Security

امنیت Virtual Hosts:

### 1. Access Control:
```nginx
# محدود کردن دسترسی
server {
    listen 80;
    server_name internal.example.com;
    
    # فقط IP های داخلی
    allow 192.168.1.0/24;
    allow 10.0.0.0/8;
    deny all;
    
    root /var/www/internal;
}
```

### 2. SSL/TLS:
```nginx
# HTTPS configuration
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /path/to/cert.crt;
    ssl_certificate_key /path/to/key.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384;
    
    root /var/www/example.com;
}
```

### 3. Security Headers:
```nginx
# هدرهای امنیتی
server {
    listen 80;
    server_name example.com;
    
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

### 4. Rate Limiting:
```nginx
# محدودیت درخواست
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

server {
    listen 80;
    server_name api.example.com;
    
    location / {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://backend;
    }
}
```

### 5. Hidden Information:
```nginx
# مخفی کردن اطلاعات سرور
server_tokens off;

# حذف header های اضافی
more_clear_headers 'Server';
more_clear_headers 'X-Powered-By';
```