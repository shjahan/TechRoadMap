# Section 6 - Reverse Proxy

## 6.1 Reverse Proxy Concepts

A reverse proxy is a server that sits between clients and backend servers, forwarding client requests to the appropriate backend server and returning the response to the client. Unlike a forward proxy that represents clients, a reverse proxy represents servers.

### Key Concepts:
- **Client-facing**: Acts as the public interface for backend services
- **Request Forwarding**: Routes client requests to appropriate backend servers
- **Response Handling**: Returns backend responses to clients
- **Load Distribution**: Can distribute requests across multiple backends
- **Security Layer**: Provides an additional security boundary

### Real-world Analogy:
A reverse proxy is like a receptionist in a large office building who:
- Greets visitors (clients) at the front desk
- Determines which department (backend server) can help
- Routes visitors to the appropriate office
- Handles all communication between visitors and departments
- Provides a single point of contact for the entire building

### Forward Proxy vs Reverse Proxy:
```
Forward Proxy:  Client → Proxy → Internet
Reverse Proxy:  Internet → Proxy → Backend Servers
```

### Example Basic Setup:
```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://192.168.1.10:8080;
    }
}
```

### Benefits:
- **Security**: Hides backend server details
- **Load Balancing**: Distributes traffic across multiple servers
- **SSL Termination**: Handles SSL/TLS encryption
- **Caching**: Can cache responses to improve performance
- **Compression**: Can compress responses
- **Authentication**: Can handle authentication centrally

## 6.2 Proxy Configuration

Proxy configuration defines how Nginx forwards requests to backend servers and handles responses.

### Basic Proxy Configuration:
```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://192.168.1.10:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Advanced Proxy Configuration:
```nginx
upstream backend {
    server 192.168.1.10:8080 weight=3;
    server 192.168.1.11:8080 weight=2;
    server 192.168.1.12:8080 weight=1;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        
        # Headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        proxy_busy_buffers_size 8k;
        
        # Error handling
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 10s;
    }
}
```

### Proxy Pass Variations:
```nginx
# Exact path matching
location /api/ {
    proxy_pass http://backend/;  # Note the trailing slash
}

# Path preservation
location /api/ {
    proxy_pass http://backend;   # No trailing slash
}

# URL rewriting
location /old/ {
    proxy_pass http://backend/new/;
}

# Different backends for different paths
location /api/v1/ {
    proxy_pass http://backend-v1;
}

location /api/v2/ {
    proxy_pass http://backend-v2;
}
```

## 6.3 Proxy Headers

Proxy headers provide information about the original request and the proxy chain to backend servers.

### Essential Headers:
```nginx
location / {
    proxy_pass http://backend;
    
    # Host header - tells backend which virtual host was requested
    proxy_set_header Host $host;
    
    # Real IP - original client IP address
    proxy_set_header X-Real-IP $remote_addr;
    
    # Forwarded For - chain of proxy IPs
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    
    # Forwarded Proto - original protocol (http/https)
    proxy_set_header X-Forwarded-Proto $scheme;
    
    # Forwarded Host - original host header
    proxy_set_header X-Forwarded-Host $host;
    
    # Forwarded Port - original port
    proxy_set_header X-Forwarded-Port $server_port;
}
```

### Custom Headers:
```nginx
location / {
    proxy_pass http://backend;
    
    # Custom headers
    proxy_set_header X-Custom-Header "nginx-proxy";
    proxy_set_header X-Request-ID $request_id;
    proxy_set_header X-Forwarded-Server $hostname;
    
    # Remove headers
    proxy_set_header Accept-Encoding "";
    proxy_set_header Connection "";
}
```

### Header Processing:
```nginx
# Conditional headers based on client
map $http_user_agent $is_mobile {
    default 0;
    ~*mobile 1;
}

location / {
    proxy_pass http://backend;
    
    # Add mobile header if client is mobile
    proxy_set_header X-Is-Mobile $is_mobile;
    
    # Add client info
    proxy_set_header X-Client-IP $remote_addr;
    proxy_set_header X-User-Agent $http_user_agent;
}
```

### Header Security:
```nginx
# Remove sensitive headers
location / {
    proxy_pass http://backend;
    
    # Remove internal headers
    proxy_hide_header X-Powered-By;
    proxy_hide_header Server;
    
    # Set security headers
    add_header X-Proxy-Server "nginx" always;
    add_header X-Proxy-Version "1.20.2" always;
}
```

## 6.4 Proxy Buffering

Proxy buffering controls how Nginx handles data between clients and backend servers, affecting performance and memory usage.

### Basic Buffering Configuration:
```nginx
location / {
    proxy_pass http://backend;
    
    # Enable buffering
    proxy_buffering on;
    
    # Buffer sizes
    proxy_buffer_size 4k;
    proxy_buffers 8 4k;
    proxy_busy_buffers_size 8k;
    
    # Temporary file buffering
    proxy_temp_file_write_size 8k;
    proxy_max_temp_file_size 1024m;
}
```

### Advanced Buffering:
```nginx
location / {
    proxy_pass http://backend;
    
    # Buffering settings
    proxy_buffering on;
    proxy_request_buffering on;
    
    # Buffer sizes based on content type
    location ~* \.(json|xml)$ {
        proxy_buffering on;
        proxy_buffer_size 8k;
        proxy_buffers 16 8k;
        proxy_busy_buffers_size 16k;
    }
    
    # Large file handling
    location ~* \.(mp4|avi|zip)$ {
        proxy_buffering off;
        proxy_request_buffering off;
        proxy_max_temp_file_size 0;
    }
}
```

### Buffering for Different Content Types:
```nginx
# JSON API responses
location /api/ {
    proxy_pass http://backend;
    proxy_buffering on;
    proxy_buffer_size 4k;
    proxy_buffers 8 4k;
    proxy_busy_buffers_size 8k;
}

# Large file downloads
location /downloads/ {
    proxy_pass http://backend;
    proxy_buffering off;
    proxy_request_buffering off;
    proxy_max_temp_file_size 0;
}

# Streaming content
location /stream/ {
    proxy_pass http://backend;
    proxy_buffering off;
    proxy_cache off;
    proxy_read_timeout 24h;
}
```

### Memory Optimization:
```nginx
# Optimize memory usage
location / {
    proxy_pass http://backend;
    
    # Smaller buffers for memory efficiency
    proxy_buffer_size 1k;
    proxy_buffers 4 1k;
    proxy_busy_buffers_size 2k;
    
    # Limit temporary file size
    proxy_max_temp_file_size 100m;
}
```

## 6.5 Proxy Caching

Proxy caching stores backend responses to improve performance and reduce backend load.

### Basic Caching Setup:
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
        proxy_pass http://backend;
        
        # Caching configuration
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_background_update on;
    }
}
```

### Advanced Caching Configuration:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:100m max_size=10g inactive=24h;

# Cache key configuration
proxy_cache_key "$scheme$request_method$host$request_uri";

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
        proxy_pass http://backend;
        
        # Caching
        proxy_cache api_cache;
        proxy_cache_valid 200 302 1h;
        proxy_cache_valid 404 1m;
        proxy_cache_bypass $no_cache;
        proxy_no_cache $no_cache;
        
        # Cache headers
        add_header X-Cache-Status $upstream_cache_status;
        add_header X-Cache-Key $proxy_cache_key;
    }
}
```

### Cache Invalidation:
```nginx
# Cache invalidation endpoint
location /admin/cache/purge {
    allow 192.168.1.0/24;
    deny all;
    
    proxy_cache_purge api_cache $arg_key;
    return 200 "Cache purged for key: $arg_key\n";
}

# Conditional cache invalidation
location /api/ {
    proxy_pass http://backend;
    proxy_cache api_cache;
    
    # Invalidate cache on POST/PUT/DELETE
    if ($request_method ~ ^(POST|PUT|DELETE)$) {
        proxy_cache_bypass 1;
        proxy_no_cache 1;
    }
}
```

### Cache Performance Optimization:
```nginx
# Optimized caching for different content types
location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
    proxy_pass http://backend;
    proxy_cache api_cache;
    proxy_cache_valid 200 1y;
    proxy_cache_valid 404 1m;
    expires 1y;
    add_header Cache-Control "public, immutable";
}

location /api/static/ {
    proxy_pass http://backend;
    proxy_cache api_cache;
    proxy_cache_valid 200 1h;
    proxy_cache_lock on;
    proxy_cache_lock_timeout 5s;
}
```

## 6.6 Reverse Proxy Best Practices

### 1. Security Headers:
```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        
        # Hide backend information
        proxy_hide_header X-Powered-By;
        proxy_hide_header Server;
    }
}
```

### 2. Error Handling:
```nginx
upstream backend {
    server 192.168.1.10:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.12:8080 backup;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        
        # Error handling
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 10s;
        
        # Custom error pages
        error_page 502 503 504 /50x.html;
    }
    
    location = /50x.html {
        root /var/www/error;
        internal;
    }
}
```

### 3. Logging and Monitoring:
```nginx
# Custom log format for reverse proxy
log_format proxy_combined '$remote_addr - $remote_user [$time_local] '
                         '"$request" $status $body_bytes_sent '
                         '"$http_referer" "$http_user_agent" '
                         'upstream_addr="$upstream_addr" '
                         'upstream_status="$upstream_status" '
                         'upstream_response_time="$upstream_response_time" '
                         'request_time="$request_time"';

server {
    listen 80;
    server_name example.com;
    access_log /var/log/nginx/proxy_access.log proxy_combined;
    
    location / {
        proxy_pass http://backend;
    }
}
```

### 4. Performance Optimization:
```nginx
server {
    listen 80;
    server_name example.com;
    
    # Global optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    
    location / {
        proxy_pass http://backend;
        
        # Connection optimization
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Buffering optimization
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        
        # Timeout optimization
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
    }
}
```

## 6.7 Reverse Proxy Testing

### 1. Basic Connectivity Test:
```bash
# Test proxy connectivity
curl -I http://example.com/

# Test with verbose output
curl -v http://example.com/

# Test specific endpoints
curl http://example.com/api/health
```

### 2. Header Testing:
```bash
# Test forwarded headers
curl -H "X-Forwarded-For: 192.168.1.100" http://example.com/

# Test custom headers
curl -H "X-Custom-Header: test" http://example.com/

# Check response headers
curl -I http://example.com/ | grep -i "x-"
```

### 3. Load Testing:
```bash
# Load test with Apache Bench
ab -n 1000 -c 10 http://example.com/

# Load test with wrk
wrk -t12 -c400 -d30s http://example.com/

# Load test with specific headers
wrk -t12 -c400 -d30s -H "X-Forwarded-For: 192.168.1.100" http://example.com/
```

### 4. Failover Testing:
```bash
# Test backend failover
# Stop one backend server
sudo systemctl stop backend-service

# Test that proxy continues working
curl http://example.com/

# Check logs for failover
tail -f /var/log/nginx/error.log
```

## 6.8 Reverse Proxy Performance

### 1. Connection Optimization:
```nginx
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    
    # Keep-alive connections
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

### 2. Buffering Optimization:
```nginx
# Optimize buffering for different content types
location /api/ {
    proxy_pass http://backend;
    
    # JSON responses - smaller buffers
    proxy_buffering on;
    proxy_buffer_size 2k;
    proxy_buffers 4 2k;
    proxy_busy_buffers_size 4k;
}

location /downloads/ {
    proxy_pass http://backend;
    
    # Large files - disable buffering
    proxy_buffering off;
    proxy_request_buffering off;
    proxy_max_temp_file_size 0;
}
```

### 3. Caching Strategy:
```nginx
# Multi-level caching
proxy_cache_path /var/cache/nginx/level1 levels=1:2 keys_zone=level1:10m max_size=1g;
proxy_cache_path /var/cache/nginx/level2 levels=1:2 keys_zone=level2:100m max_size=10g;

# Fast cache for frequently accessed content
location /api/hot/ {
    proxy_pass http://backend;
    proxy_cache level1;
    proxy_cache_valid 200 5m;
}

# Slower cache for less frequent content
location /api/cold/ {
    proxy_pass http://backend;
    proxy_cache level2;
    proxy_cache_valid 200 1h;
}
```

## 6.9 Reverse Proxy Troubleshooting

### 1. Common Issues:

#### 502 Bad Gateway:
```bash
# Check backend server status
curl http://192.168.1.10:8080/health

# Check Nginx error logs
tail -f /var/log/nginx/error.log

# Check upstream configuration
nginx -T | grep -A 10 "upstream"
```

#### 504 Gateway Timeout:
```nginx
# Increase timeout values
location / {
    proxy_pass http://backend;
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
```

#### Headers Not Forwarded:
```nginx
# Ensure headers are properly set
location / {
    proxy_pass http://backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 2. Debugging Tools:
```nginx
# Enable debug logging
error_log /var/log/nginx/debug.log debug;

# Add debug headers
add_header X-Upstream-Addr $upstream_addr;
add_header X-Upstream-Status $upstream_status;
add_header X-Upstream-Response-Time $upstream_response_time;
add_header X-Request-ID $request_id;
```

### 3. Monitoring Commands:
```bash
# Monitor proxy performance
curl -w "@curl-format.txt" -o /dev/null -s http://example.com/

# Check upstream status
curl http://example.com/upstream_status

# Monitor error logs
tail -f /var/log/nginx/error.log | grep proxy
```

## 6.10 Reverse Proxy Security

### 1. Access Control:
```nginx
# Restrict access to proxy
server {
    listen 80;
    server_name internal.example.com;
    
    # Only allow specific IPs
    allow 192.168.1.0/24;
    allow 10.0.0.0/8;
    deny all;
    
    location / {
        proxy_pass http://backend;
    }
}
```

### 2. Rate Limiting:
```nginx
# Rate limiting for reverse proxy
limit_req_zone $binary_remote_addr zone=proxy:10m rate=10r/s;

server {
    listen 80;
    server_name example.com;
    
    location / {
        limit_req zone=proxy burst=20 nodelay;
        proxy_pass http://backend;
    }
}
```

### 3. SSL Termination:
```nginx
# SSL termination at reverse proxy
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}

server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /path/to/cert.crt;
    ssl_certificate_key /path/to/key.key;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 4. Security Headers:
```nginx
# Comprehensive security headers
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        add_header Content-Security-Policy "default-src 'self'" always;
    }
}
```

### 5. DDoS Protection:
```nginx
# DDoS protection for reverse proxy
limit_req_zone $binary_remote_addr zone=ddos:10m rate=1r/s;
limit_conn_zone $binary_remote_addr zone=conn_limit_per_ip:10m;

server {
    listen 80;
    server_name example.com;
    
    location / {
        limit_req zone=ddos burst=5 nodelay;
        limit_conn conn_limit_per_ip 10;
        proxy_pass http://backend;
    }
}
```