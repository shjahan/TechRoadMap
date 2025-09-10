# Section 2 - Web Server Concepts

## 2.1 Web Server Concepts

A web server is software that receives HTTP/HTTPS requests and sends appropriate responses. Web servers act as the main entry point for all web traffic.

### Key Concepts:
- **Request**: Message sent by browser to server
- **Response**: Response sent by server back to browser
- **HTTP Protocol**: Communication language between browser and server
- **Port**: Number of the port server listens on (usually 80 for HTTP and 443 for HTTPS)

### Real-world Analogy:
A web server is like a librarian in a library who:
- Receives requests for books
- Finds the appropriate book and delivers it
- Returns an error message if the book is not available

### Example:
```bash
# Simple HTTP request
GET /index.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0...

# Server response
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1024

<!DOCTYPE html>
<html>...</html>
```

## 2.2 HTTP Protocol

HTTP (HyperText Transfer Protocol) is the standard communication protocol for data transfer on the web.

### HTTP Versions:
- **HTTP/1.0**: Initial version with many limitations
- **HTTP/1.1**: Improved with Keep-Alive and pipelining
- **HTTP/2**: Performance improvements with multiplexing and compression
- **HTTP/3**: Based on QUIC with improved security and speed

### HTTP Request Structure:
```http
GET /api/users HTTP/1.1
Host: api.example.com
Accept: application/json
Authorization: Bearer token123
User-Agent: MyApp/1.0
```

### HTTP Response Structure:
```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 156
Cache-Control: max-age=3600

{
  "users": [
    {"id": 1, "name": "John"},
    {"id": 2, "name": "Jane"}
  ]
}
```

### HTTP Status Codes:
- **2xx**: Success (200 OK, 201 Created)
- **3xx**: Redirection (301 Moved Permanently, 302 Found)
- **4xx**: Client Error (400 Bad Request, 404 Not Found)
- **5xx**: Server Error (500 Internal Server Error, 502 Bad Gateway)

## 2.3 HTTPS Protocol

HTTPS is the secure version of HTTP that uses SSL/TLS for encryption.

### HTTPS Benefits:
- **Encryption**: Data is protected during transmission
- **Authentication**: Server identity is verified
- **Integrity**: Data cannot be modified
- **Trust**: Users feel more secure

### Handshake Process:
```bash
1. Client Hello: Client sends its capabilities
2. Server Hello: Server sends certificate and public key
3. Key Exchange: Shared keys are generated
4. Finished: Secure connection is established
```

### Example HTTPS Configuration in Nginx:
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

## 2.4 Web Server Types

Different types of web servers based on architecture and usage:

### 1. Thread-based Servers:
```c
// Apache HTTP Server
// Each request gets a separate thread
for (int i = 0; i < max_threads; i++) {
    pthread_create(&threads[i], NULL, handle_request, NULL);
}
```

### 2. Event-driven Servers:
```c
// Nginx
// One thread handles all requests
while (true) {
    events = epoll_wait(epfd, events, MAX_EVENTS, -1);
    for (i = 0; i < events; i++) {
        handle_event(events[i]);
    }
}
```

### 3. Process-based Servers:
```c
// Apache Prefork MPM
// Each request gets a separate process
pid_t pid = fork();
if (pid == 0) {
    handle_request();
    exit(0);
}
```

### Performance Comparison:
| Server Type | Memory | CPU | Concurrency | Complexity |
|-------------|--------|-----|-------------|------------|
| Thread-based | High | Medium | Limited | Medium |
| Event-driven | Low | Low | High | High |
| Process-based | Very High | High | Very Limited | Low |

## 2.5 Web Server Benefits

Benefits of using web servers:

### 1. High Performance:
```nginx
# Nginx optimization
worker_processes auto;
worker_connections 1024;
use epoll;
multi_accept on;
```

### 2. Scalability:
```nginx
# Load balancing
upstream backend {
    server 192.168.1.10:8080 weight=3;
    server 192.168.1.11:8080 weight=2;
    server 192.168.1.12:8080 weight=1;
}
```

### 3. Security:
```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
```

### 4. Reliability:
```nginx
# Health checks
upstream backend {
    server 192.168.1.10:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 backup;
}
```

## 2.6 Web Server Challenges

Challenges in managing web servers:

### 1. Configuration Complexity:
```nginx
# Complex configuration for microservices
location /api/v1/users {
    proxy_pass http://user-service;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_connect_timeout 30s;
    proxy_send_timeout 30s;
    proxy_read_timeout 30s;
}
```

### 2. Memory Management:
```bash
# Memory monitoring
free -h
ps aux --sort=-%mem | head -10
```

### 3. Security:
```nginx
# DDoS protection
limit_req_zone $binary_remote_addr zone=ddos:10m rate=1r/s;
limit_req zone=ddos burst=5 nodelay;
```

### 4. Monitoring:
```nginx
# Logging
log_format detailed '$remote_addr - $remote_user [$time_local] '
                   '"$request" $status $body_bytes_sent '
                   '"$http_referer" "$http_user_agent" '
                   'rt=$request_time uct="$upstream_connect_time" '
                   'uht="$upstream_header_time" urt="$upstream_response_time"';
```

## 2.7 Web Server Best Practices

Best practices for managing web servers:

### 1. Performance Optimization:
```nginx
# Gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript;

# Browser caching
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}
```

### 2. Security:
```nginx
# Hide server version
server_tokens off;

# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

### 3. Monitoring:
```nginx
# Status page
location /nginx_status {
    stub_status on;
    access_log off;
    allow 127.0.0.1;
    deny all;
}
```

### 4. Logging:
```nginx
# Structured logging
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

## 2.8 Web Server Testing

Methods for testing web servers:

### 1. Load Testing:
```bash
# Using Apache Bench
ab -n 1000 -c 10 http://example.com/

# Using wrk
wrk -t12 -c400 -d30s http://example.com/
```

### 2. Stress Testing:
```bash
# Testing with high requests
ab -n 10000 -c 100 http://example.com/
```

### 3. Configuration Testing:
```bash
# Test Nginx configuration
nginx -t

# Test configuration with details
nginx -T
```

### 4. Security Testing:
```bash
# Security testing with nmap
nmap -sV -sC example.com

# SSL testing
openssl s_client -connect example.com:443
```

## 2.9 Web Server Performance

Optimizing web server performance:

### 1. Worker Settings:
```nginx
# Number of worker processes
worker_processes auto;

# Maximum connections
worker_connections 1024;

# CPU affinity
worker_cpu_affinity 0001 0010 0100 1000;
```

### 2. Network Optimization:
```nginx
# TCP optimizations
tcp_nopush on;
tcp_nodelay on;
sendfile on;
```

### 3. Caching:
```nginx
# Proxy caching
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m;

location / {
    proxy_cache my_cache;
    proxy_cache_valid 200 302 10m;
    proxy_cache_valid 404 1m;
}
```

### 4. Compression:
```nginx
# Gzip compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_comp_level 6;
gzip_types text/plain text/css application/json application/javascript;
```

## 2.10 Web Server Security

Web server security:

### 1. Rate Limiting:
```nginx
# Request limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

### 2. Access Control:
```nginx
# Access control
location /admin {
    allow 192.168.1.0/24;
    deny all;
    auth_basic "Admin Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

### 3. SSL/TLS:
```nginx
# SSL settings
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
ssl_prefer_server_ciphers off;
```

### 4. Security Headers:
```nginx
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```