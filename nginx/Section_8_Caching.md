# Section 8 - Caching

## 8.1 Caching Concepts

Caching is the process of storing frequently accessed data in a fast storage layer to improve performance and reduce load on backend servers. In Nginx, caching can be implemented at multiple levels.

### Key Concepts:
- **Cache Hit**: Requested data is found in cache
- **Cache Miss**: Requested data is not in cache, must be fetched from backend
- **Cache Invalidation**: Process of removing or updating cached data
- **Cache Expiration**: Automatic removal of cached data after a certain time
- **Cache Warming**: Pre-loading cache with frequently accessed data

### Real-world Analogy:
Caching is like a library's reference desk that:
- Keeps copies of frequently requested books (cached data) on hand
- Quickly provides books without going to the main shelves (cache hit)
- Fetches books from the main shelves when not available (cache miss)
- Updates the reference collection when new editions arrive (cache invalidation)
- Removes old books that are no longer needed (cache expiration)

### Types of Caching in Nginx:
1. **Proxy Caching**: Caching responses from backend servers
2. **FastCGI Caching**: Caching responses from FastCGI applications
3. **Browser Caching**: Instructing browsers to cache static content
4. **Memory Caching**: Caching data in memory for fast access

### Benefits of Caching:
- **Improved Performance**: Faster response times
- **Reduced Backend Load**: Less pressure on origin servers
- **Better User Experience**: Faster page loads
- **Cost Savings**: Reduced bandwidth and server costs
- **Scalability**: Better handling of traffic spikes

### Example Basic Caching:
```nginx
# Basic proxy cache configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_pass http://backend;
    }
}
```

## 8.2 Proxy Caching

Proxy caching stores responses from backend servers to serve them directly to clients without hitting the backend again.

### Basic Proxy Cache Setup:
```nginx
# Define cache zone
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_pass http://backend;
    }
}
```

### Advanced Proxy Cache Configuration:
```nginx
# Advanced cache configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:100m max_size=10g inactive=24h;

# Cache key configuration
proxy_cache_key "$scheme$request_method$host$request_uri$is_args$args";

# Cache bypass conditions
map $request_method $no_cache {
    default 0;
    POST 1;
    PUT 1;
    DELETE 1;
}

server {
    listen 80;
    server_name api.example.com;
    
    location /api/ {
        proxy_cache api_cache;
        proxy_cache_valid 200 302 1h;
        proxy_cache_valid 404 1m;
        proxy_cache_bypass $no_cache;
        proxy_no_cache $no_cache;
        
        # Cache headers
        add_header X-Cache-Status $upstream_cache_status;
        add_header X-Cache-Key $proxy_cache_key;
        
        proxy_pass http://backend;
    }
}
```

### Cache Zones Configuration:
```nginx
# Multiple cache zones for different content types
proxy_cache_path /var/cache/nginx/static levels=1:2 keys_zone=static_cache:50m max_size=5g inactive=7d;
proxy_cache_path /var/cache/nginx/api levels=1:2 keys_zone=api_cache:100m max_size=10g inactive=1d;
proxy_cache_path /var/cache/nginx/images levels=1:2 keys_zone=image_cache:200m max_size=20g inactive=30d;

server {
    listen 80;
    server_name example.com;
    
    # Static content caching
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        proxy_cache static_cache;
        proxy_cache_valid 200 1y;
        proxy_cache_valid 404 1m;
        proxy_pass http://backend;
    }
    
    # API caching
    location /api/ {
        proxy_cache api_cache;
        proxy_cache_valid 200 1h;
        proxy_cache_valid 404 1m;
        proxy_pass http://backend;
    }
    
    # Image caching
    location /images/ {
        proxy_cache image_cache;
        proxy_cache_valid 200 30d;
        proxy_cache_valid 404 1m;
        proxy_pass http://backend;
    }
}
```

### Cache Performance Optimization:
```nginx
# Optimized cache configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=optimized_cache:500m max_size=50g inactive=7d;

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache optimized_cache;
        proxy_cache_valid 200 302 1h;
        proxy_cache_valid 404 1m;
        
        # Performance optimizations
        proxy_cache_lock on;
        proxy_cache_lock_timeout 5s;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_background_update on;
        
        # Cache headers
        add_header X-Cache-Status $upstream_cache_status;
        add_header X-Cache-Key $proxy_cache_key;
        add_header X-Cache-Date $upstream_http_date;
        
        proxy_pass http://backend;
    }
}
```

## 8.3 FastCGI Caching

FastCGI caching is used to cache responses from FastCGI applications like PHP-FPM, providing significant performance improvements for dynamic content.

### Basic FastCGI Cache Setup:
```nginx
# Define FastCGI cache zone
fastcgi_cache_path /var/cache/nginx/fastcgi levels=1:2 keys_zone=fastcgi_cache:10m max_size=1g inactive=60m;

server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.php;
    
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
        
        # FastCGI caching
        fastcgi_cache fastcgi_cache;
        fastcgi_cache_valid 200 302 10m;
        fastcgi_cache_valid 404 1m;
    }
}
```

### Advanced FastCGI Cache Configuration:
```nginx
# Advanced FastCGI cache configuration
fastcgi_cache_path /var/cache/nginx/fastcgi levels=1:2 keys_zone=php_cache:100m max_size=10g inactive=24h;

# Cache bypass conditions
map $request_method $no_cache {
    default 0;
    POST 1;
    PUT 1;
    DELETE 1;
}

map $cookie_logged_in $bypass_cache {
    default 0;
    "1" 1;
}

server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.php;
    
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
        
        # FastCGI caching
        fastcgi_cache php_cache;
        fastcgi_cache_valid 200 302 1h;
        fastcgi_cache_valid 404 1m;
        fastcgi_cache_bypass $no_cache $bypass_cache;
        fastcgi_no_cache $no_cache $bypass_cache;
        
        # Cache headers
        add_header X-FastCGI-Cache $upstream_cache_status;
        add_header X-Cache-Key $fastcgi_cache_key;
    }
}
```

### FastCGI Cache for Different Applications:
```nginx
# Multiple FastCGI cache zones
fastcgi_cache_path /var/cache/nginx/wordpress levels=1:2 keys_zone=wp_cache:50m max_size=5g inactive=1d;
fastcgi_cache_path /var/cache/nginx/drupal levels=1:2 keys_zone=drupal_cache:100m max_size=10g inactive=2d;

# WordPress caching
server {
    listen 80;
    server_name blog.example.com;
    root /var/www/wordpress;
    index index.php;
    
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
        
        fastcgi_cache wp_cache;
        fastcgi_cache_valid 200 302 1h;
        fastcgi_cache_valid 404 1m;
    }
}

# Drupal caching
server {
    listen 80;
    server_name cms.example.com;
    root /var/www/drupal;
    index index.php;
    
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
        
        fastcgi_cache drupal_cache;
        fastcgi_cache_valid 200 302 2h;
        fastcgi_cache_valid 404 1m;
    }
}
```

## 8.4 Cache Configuration

Cache configuration involves setting up cache zones, defining cache policies, and optimizing cache performance.

### Cache Zone Configuration:
```nginx
# Multiple cache zones with different configurations
proxy_cache_path /var/cache/nginx/static levels=1:2 keys_zone=static:50m max_size=5g inactive=7d;
proxy_cache_path /var/cache/nginx/api levels=1:2 keys_zone=api:100m max_size=10g inactive=1d;
proxy_cache_path /var/cache/nginx/dynamic levels=1:2 keys_zone=dynamic:200m max_size=20g inactive=1h;

# Cache zone parameters:
# levels: Directory structure (1:2 = 2 levels deep)
# keys_zone: Zone name and memory size
# max_size: Maximum disk space
# inactive: Time before inactive cache is removed
```

### Cache Policies:
```nginx
# Different cache policies for different content types
server {
    listen 80;
    server_name example.com;
    
    # Static content - long cache
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        proxy_cache static;
        proxy_cache_valid 200 1y;
        proxy_cache_valid 404 1m;
        expires 1y;
        add_header Cache-Control "public, immutable";
        proxy_pass http://backend;
    }
    
    # API responses - medium cache
    location /api/ {
        proxy_cache api;
        proxy_cache_valid 200 1h;
        proxy_cache_valid 404 1m;
        proxy_cache_bypass $http_pragma $http_authorization;
        proxy_pass http://backend;
    }
    
    # Dynamic content - short cache
    location / {
        proxy_cache dynamic;
        proxy_cache_valid 200 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_use_stale error timeout updating;
        proxy_pass http://backend;
    }
}
```

### Cache Key Configuration:
```nginx
# Custom cache key configuration
proxy_cache_key "$scheme$request_method$host$request_uri$is_args$args$http_accept_encoding";

# Cache key with user-specific content
map $cookie_user_id $cache_key_suffix {
    default "";
    ~.+ "-user-$cookie_user_id";
}

proxy_cache_key "$scheme$request_method$host$request_uri$cache_key_suffix";

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache dynamic;
        proxy_cache_valid 200 1h;
        proxy_pass http://backend;
    }
}
```

### Cache Headers and Status:
```nginx
# Cache status headers
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache dynamic;
        proxy_cache_valid 200 1h;
        
        # Cache status headers
        add_header X-Cache-Status $upstream_cache_status;
        add_header X-Cache-Key $proxy_cache_key;
        add_header X-Cache-Date $upstream_http_date;
        add_header X-Cache-Expires $upstream_http_expires;
        
        proxy_pass http://backend;
    }
}
```

## 8.5 Cache Invalidation

Cache invalidation is the process of removing or updating cached data when the original data changes.

### Manual Cache Invalidation:
```nginx
# Cache invalidation endpoint
location /admin/cache/purge {
    allow 192.168.1.0/24;
    deny all;
    
    # Purge specific cache key
    proxy_cache_purge dynamic $arg_key;
    return 200 "Cache purged for key: $arg_key\n";
}

# Purge cache by pattern
location /admin/cache/purge-pattern {
    allow 192.168.1.0/24;
    deny all;
    
    # Purge cache by pattern
    proxy_cache_purge dynamic $arg_pattern;
    return 200 "Cache purged for pattern: $arg_pattern\n";
}
```

### Automatic Cache Invalidation:
```nginx
# Cache invalidation based on request method
map $request_method $purge_cache {
    default 0;
    POST 1;
    PUT 1;
    DELETE 1;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache dynamic;
        proxy_cache_valid 200 1h;
        
        # Invalidate cache on data modification
        if ($purge_cache) {
            proxy_cache_bypass 1;
            proxy_no_cache 1;
        }
        
        proxy_pass http://backend;
    }
}
```

### Cache Invalidation with Headers:
```nginx
# Cache invalidation using custom headers
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache dynamic;
        proxy_cache_valid 200 1h;
        
        # Bypass cache if purge header is present
        proxy_cache_bypass $http_x_purge_cache;
        proxy_no_cache $http_x_purge_cache;
        
        proxy_pass http://backend;
    }
}

# Usage example:
# curl -H "X-Purge-Cache: 1" http://example.com/api/data
```

### Cache Invalidation Scripts:
```bash
#!/bin/bash
# Cache invalidation script

CACHE_DIR="/var/cache/nginx"
NGINX_PID="/var/run/nginx.pid"

# Function to purge cache by pattern
purge_cache_pattern() {
    local pattern=$1
    echo "Purging cache for pattern: $pattern"
    
    # Find and remove matching cache files
    find $CACHE_DIR -name "*$pattern*" -type f -delete
    
    # Reload Nginx to clear memory cache
    kill -USR1 $(cat $NGINX_PID)
    
    echo "Cache purged successfully"
}

# Function to purge all cache
purge_all_cache() {
    echo "Purging all cache..."
    
    # Remove all cache files
    rm -rf $CACHE_DIR/*
    
    # Reload Nginx
    kill -USR1 $(cat $NGINX_PID)
    
    echo "All cache purged successfully"
}

# Main script
case $1 in
    "pattern")
        purge_cache_pattern $2
        ;;
    "all")
        purge_all_cache
        ;;
    *)
        echo "Usage: $0 {pattern|all} [pattern]"
        exit 1
        ;;
esac
```

## 8.6 Caching Best Practices

### 1. Cache Strategy:
```nginx
# Layered caching strategy
proxy_cache_path /var/cache/nginx/l1 levels=1:2 keys_zone=l1_cache:10m max_size=1g inactive=1h;
proxy_cache_path /var/cache/nginx/l2 levels=1:2 keys_zone=l2_cache:100m max_size=10g inactive=1d;

# Level 1: Fast cache for hot content
location /api/hot/ {
    proxy_cache l1_cache;
    proxy_cache_valid 200 5m;
    proxy_pass http://backend;
}

# Level 2: Slower cache for warm content
location /api/warm/ {
    proxy_cache l2_cache;
    proxy_cache_valid 200 1h;
    proxy_pass http://backend;
}
```

### 2. Cache Monitoring:
```nginx
# Cache monitoring endpoint
location /cache-status {
    allow 127.0.0.1;
    deny all;
    
    return 200 "Cache Status:\nHit: $upstream_cache_status\nKey: $proxy_cache_key\n";
    add_header Content-Type text/plain;
}

# Cache statistics
location /cache-stats {
    allow 192.168.1.0/24;
    deny all;
    
    return 200 "Cache Statistics:\nZone: dynamic\nStatus: $upstream_cache_status\n";
    add_header Content-Type text/plain;
}
```

### 3. Cache Security:
```nginx
# Secure cache configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=secure_cache:100m max_size=10g inactive=1d;

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache secure_cache;
        proxy_cache_valid 200 1h;
        
        # Security headers
        add_header X-Cache-Status $upstream_cache_status;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        
        proxy_pass http://backend;
    }
}
```

### 4. Cache Performance:
```nginx
# Performance-optimized cache configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=perf_cache:500m max_size=50g inactive=7d;

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache perf_cache;
        proxy_cache_valid 200 1h;
        
        # Performance optimizations
        proxy_cache_lock on;
        proxy_cache_lock_timeout 5s;
        proxy_cache_use_stale error timeout updating;
        proxy_cache_background_update on;
        
        proxy_pass http://backend;
    }
}
```

## 8.7 Caching Testing

### 1. Cache Hit/Miss Testing:
```bash
# Test cache hits
curl -I http://example.com/api/data

# Check cache status header
curl -I http://example.com/api/data | grep X-Cache-Status

# Test cache miss (after purging)
curl -H "X-Purge-Cache: 1" http://example.com/api/data
curl -I http://example.com/api/data | grep X-Cache-Status
```

### 2. Cache Performance Testing:
```bash
# Load test with cache
ab -n 1000 -c 10 http://example.com/api/data

# Load test without cache
ab -n 1000 -c 10 -H "X-Purge-Cache: 1" http://example.com/api/data

# Compare response times
wrk -t12 -c400 -d30s http://example.com/api/data
```

### 3. Cache Validation Testing:
```bash
# Test cache expiration
curl -I http://example.com/api/data
sleep 60
curl -I http://example.com/api/data

# Test cache invalidation
curl -X POST http://example.com/api/data
curl -I http://example.com/api/data
```

## 8.8 Caching Performance

### 1. Cache Optimization:
```nginx
# Optimized cache configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=opt_cache:1g max_size=100g inactive=7d;

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache opt_cache;
        proxy_cache_valid 200 1h;
        
        # Performance optimizations
        proxy_cache_lock on;
        proxy_cache_lock_timeout 5s;
        proxy_cache_use_stale error timeout updating;
        proxy_cache_background_update on;
        
        # Buffer optimization
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        
        proxy_pass http://backend;
    }
}
```

### 2. Memory Optimization:
```nginx
# Memory-optimized cache configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=mem_cache:100m max_size=10g inactive=1d;

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache mem_cache;
        proxy_cache_valid 200 1h;
        
        # Memory optimizations
        proxy_cache_min_uses 2;
        proxy_cache_revalidate on;
        
        proxy_pass http://backend;
    }
}
```

### 3. Disk Optimization:
```nginx
# Disk-optimized cache configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=disk_cache:500m max_size=50g inactive=7d;

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache disk_cache;
        proxy_cache_valid 200 1h;
        
        # Disk optimizations
        proxy_temp_file_write_size 8k;
        proxy_max_temp_file_size 1024m;
        
        proxy_pass http://backend;
    }
}
```

## 8.9 Caching Troubleshooting

### 1. Common Cache Issues:

#### Cache Not Working:
```bash
# Check cache configuration
nginx -t

# Check cache directory permissions
ls -la /var/cache/nginx/

# Check cache zone configuration
nginx -T | grep -A 10 "proxy_cache_path"
```

#### Cache Not Invalidating:
```bash
# Check cache invalidation configuration
nginx -T | grep -A 5 "proxy_cache_purge"

# Test cache invalidation
curl -H "X-Purge-Cache: 1" http://example.com/api/data

# Check cache status
curl -I http://example.com/api/data | grep X-Cache-Status
```

#### Cache Performance Issues:
```bash
# Check cache hit ratio
grep "HIT\|MISS" /var/log/nginx/access.log | sort | uniq -c

# Check cache size
du -sh /var/cache/nginx/

# Check cache file count
find /var/cache/nginx/ -type f | wc -l
```

### 2. Cache Debugging:
```nginx
# Enable cache debugging
error_log /var/log/nginx/cache_debug.log debug;

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache dynamic;
        proxy_cache_valid 200 1h;
        
        # Debug headers
        add_header X-Cache-Status $upstream_cache_status;
        add_header X-Cache-Key $proxy_cache_key;
        add_header X-Cache-Date $upstream_http_date;
        
        proxy_pass http://backend;
    }
}
```

### 3. Cache Monitoring:
```bash
# Monitor cache performance
tail -f /var/log/nginx/access.log | grep -E "(HIT|MISS|EXPIRED|UPDATING)"

# Check cache statistics
curl http://example.com/cache-status

# Monitor cache size
watch -n 5 'du -sh /var/cache/nginx/'
```

## 8.10 Caching Security

### 1. Cache Access Control:
```nginx
# Secure cache configuration
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=secure_cache:100m max_size=10g inactive=1d;

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache secure_cache;
        proxy_cache_valid 200 1h;
        
        # Access control
        allow 192.168.1.0/24;
        deny all;
        
        proxy_pass http://backend;
    }
}
```

### 2. Cache Encryption:
```bash
# Encrypt cache directory
sudo chmod 700 /var/cache/nginx/
sudo chown nginx:nginx /var/cache/nginx/

# Set up encrypted cache
sudo mount -t tmpfs -o size=1g tmpfs /var/cache/nginx/
```

### 3. Cache Validation:
```nginx
# Cache validation
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_cache dynamic;
        proxy_cache_valid 200 1h;
        
        # Cache validation
        proxy_cache_revalidate on;
        proxy_cache_use_stale error timeout updating;
        
        # Security headers
        add_header X-Cache-Status $upstream_cache_status;
        add_header X-Frame-Options "SAMEORIGIN" always;
        
        proxy_pass http://backend;
    }
}
```

### 4. Cache Audit:
```bash
#!/bin/bash
# Cache security audit script

CACHE_DIR="/var/cache/nginx"
LOG_FILE="/var/log/nginx/cache_audit.log"

echo "Starting cache security audit..." >> $LOG_FILE

# Check cache directory permissions
PERMS=$(stat -c %a $CACHE_DIR)
if [ "$PERMS" != "700" ]; then
    echo "WARNING: Cache directory permissions are $PERMS, should be 700" >> $LOG_FILE
fi

# Check cache directory ownership
OWNER=$(stat -c %U:%G $CACHE_DIR)
if [ "$OWNER" != "nginx:nginx" ]; then
    echo "WARNING: Cache directory ownership is $OWNER, should be nginx:nginx" >> $LOG_FILE
fi

# Check for suspicious cache files
SUSPICIOUS=$(find $CACHE_DIR -name "*.php" -o -name "*.sh" -o -name "*.exe")
if [ -n "$SUSPICIOUS" ]; then
    echo "WARNING: Suspicious files found in cache: $SUSPICIOUS" >> $LOG_FILE
fi

echo "Cache security audit completed" >> $LOG_FILE
```