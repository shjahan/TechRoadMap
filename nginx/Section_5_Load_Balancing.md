# Section 5 - Load Balancing

## 5.1 Load Balancing Concepts

Load balancing is the process of distributing incoming network traffic across multiple servers to ensure no single server becomes overwhelmed. This improves application availability, reliability, and performance.

### Key Concepts:
- **Load Distribution**: Spreading traffic evenly across multiple servers
- **High Availability**: Ensuring service continues even if some servers fail
- **Scalability**: Ability to handle increased traffic by adding more servers
- **Health Monitoring**: Checking server status and removing failed servers

### Real-world Analogy:
Load balancing is like a smart traffic controller at a busy intersection who directs cars to different lanes based on:
- Which lane has the least traffic
- Which lane is moving fastest
- Which lane is currently available

### Example Scenario:
```nginx
# Basic load balancing setup
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
    }
}
```

### Benefits:
- **Improved Performance**: Distributes load to prevent bottlenecks
- **High Availability**: Service continues if individual servers fail
- **Scalability**: Easy to add or remove servers
- **Maintenance**: Can take servers offline for updates without downtime

## 5.2 Upstream Configuration

Upstream configuration defines the group of backend servers that will receive traffic from the load balancer.

### Basic Upstream Block:
```nginx
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}
```

### Advanced Upstream Configuration:
```nginx
upstream backend {
    # Server definitions with parameters
    server 192.168.1.10:8080 weight=3 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 weight=2 max_fails=3 fail_timeout=30s;
    server 192.168.1.12:8080 weight=1 max_fails=3 fail_timeout=30s;
    
    # Backup server
    server 192.168.1.13:8080 backup;
    
    # Keep-alive connections
    keepalive 32;
    
    # Load balancing method
    least_conn;
}
```

### Server Parameters:
- **weight**: Server weight (default: 1)
- **max_fails**: Maximum number of failed attempts
- **fail_timeout**: Time to consider server failed
- **backup**: Use only when other servers are unavailable
- **down**: Mark server as permanently unavailable

### Example with Health Checks:
```nginx
upstream api_servers {
    server 192.168.1.10:8080 weight=3 max_fails=2 fail_timeout=10s;
    server 192.168.1.11:8080 weight=3 max_fails=2 fail_timeout=10s;
    server 192.168.1.12:8080 weight=2 max_fails=2 fail_timeout=10s;
    server 192.168.1.13:8080 backup;
    
    # Health check endpoint
    health_check uri=/health;
}
```

## 5.3 Load Balancing Methods

Nginx supports several load balancing algorithms to distribute traffic across backend servers.

### 1. Round Robin (Default):
```nginx
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
    # Uses round-robin by default
}
```

### 2. Weighted Round Robin:
```nginx
upstream backend {
    server 192.168.1.10:8080 weight=3;  # Gets 3 requests
    server 192.168.1.11:8080 weight=2;  # Gets 2 requests
    server 192.168.1.12:8080 weight=1;  # Gets 1 request
}
```

### 3. Least Connections:
```nginx
upstream backend {
    least_conn;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}
```

### 4. IP Hash (Session Persistence):
```nginx
upstream backend {
    ip_hash;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}
```

### 5. Generic Hash:
```nginx
upstream backend {
    hash $request_uri consistent;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}
```

### Method Comparison:
| Method | Use Case | Pros | Cons |
|--------|----------|------|------|
| Round Robin | General purpose | Simple, fair distribution | Doesn't consider server load |
| Weighted Round Robin | Servers with different capacities | Considers server capacity | Still doesn't consider current load |
| Least Connections | Long-running connections | Considers current load | More complex to implement |
| IP Hash | Session persistence | Maintains user sessions | Can create uneven distribution |
| Generic Hash | Cache-friendly | Consistent hashing | Requires careful key selection |

## 5.4 Health Checks

Health checks monitor backend server status and automatically remove failed servers from the load balancing pool.

### Basic Health Check:
```nginx
upstream backend {
    server 192.168.1.10:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.12:8080 max_fails=3 fail_timeout=30s;
}
```

### Advanced Health Check with Custom Endpoint:
```nginx
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
    
    # Health check configuration
    health_check uri=/health interval=10s fails=3 passes=2;
}

# Health check endpoint
location /health {
    access_log off;
    return 200 "healthy\n";
    add_header Content-Type text/plain;
}
```

### Health Check Parameters:
- **uri**: Health check endpoint
- **interval**: Check interval (default: 5s)
- **fails**: Number of failed checks before marking server down
- **passes**: Number of successful checks before marking server up
- **match**: Custom response matching

### Custom Health Check Response:
```nginx
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
    
    health_check uri=/health match=server_ok;
}

match server_ok {
    status 200;
    header Content-Type = text/plain;
    body ~ "OK";
}
```

### Monitoring Health Status:
```nginx
# Status endpoint for monitoring
location /upstream_status {
    access_log off;
    return 200 "$upstream_addr\n";
    add_header Content-Type text/plain;
}
```

## 5.5 Session Persistence

Session persistence ensures that requests from the same client are always routed to the same backend server.

### IP Hash Method:
```nginx
upstream backend {
    ip_hash;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}
```

### Sticky Sessions with Cookies:
```nginx
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
    
    sticky cookie srv_id expires=1h domain=.example.com path=/;
}
```

### Sticky Sessions with Route:
```nginx
upstream backend {
    server 192.168.1.10:8080 route=a;
    server 192.168.1.11:8080 route=b;
    server 192.168.1.12:8080 route=c;
    
    sticky route $route_cookie;
}
```

### Custom Session Persistence:
```nginx
# Using custom header for session persistence
map $http_x_session_id $backend_pool {
    default backend;
    ~^session1 backend1;
    ~^session2 backend2;
}

upstream backend1 {
    server 192.168.1.10:8080;
}

upstream backend2 {
    server 192.168.1.11:8080;
}

upstream backend {
    server 192.168.1.12:8080;
}

server {
    listen 80;
    location / {
        proxy_pass http://$backend_pool;
    }
}
```

### Session Persistence Considerations:
- **Scalability**: IP hash can create uneven distribution
- **Failover**: Sticky sessions can cause issues during server failures
- **Load Distribution**: May not distribute load evenly
- **Client IP Changes**: IP hash fails with dynamic IPs

## 5.6 Load Balancing Best Practices

### 1. Server Configuration:
```nginx
upstream backend {
    # Use multiple servers for redundancy
    server 192.168.1.10:8080 weight=3 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 weight=3 max_fails=3 fail_timeout=30s;
    server 192.168.1.12:8080 weight=2 max_fails=3 fail_timeout=30s;
    
    # Backup server
    server 192.168.1.13:8080 backup;
    
    # Keep-alive connections
    keepalive 32;
    
    # Load balancing method
    least_conn;
}
```

### 2. Health Monitoring:
```nginx
# Health check endpoint
location /health {
    access_log off;
    return 200 "healthy\n";
    add_header Content-Type text/plain;
}

# Upstream status monitoring
location /upstream_status {
    access_log off;
    return 200 "$upstream_addr\n";
    add_header Content-Type text/plain;
}
```

### 3. Error Handling:
```nginx
upstream backend {
    server 192.168.1.10:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.12:8080 backup;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 10s;
    }
}
```

### 4. Logging and Monitoring:
```nginx
# Custom log format for load balancing
log_format lb_combined '$remote_addr - $remote_user [$time_local] '
                      '"$request" $status $body_bytes_sent '
                      '"$http_referer" "$http_user_agent" '
                      'upstream_addr="$upstream_addr" '
                      'upstream_status="$upstream_status" '
                      'upstream_response_time="$upstream_response_time"';

server {
    listen 80;
    access_log /var/log/nginx/lb_access.log lb_combined;
    
    location / {
        proxy_pass http://backend;
    }
}
```

## 5.7 Load Balancing Testing

### 1. Basic Load Test:
```bash
# Test with Apache Bench
ab -n 1000 -c 10 http://example.com/

# Test with wrk
wrk -t12 -c400 -d30s http://example.com/
```

### 2. Health Check Testing:
```bash
# Test health check endpoint
curl -I http://example.com/health

# Test upstream status
curl http://example.com/upstream_status
```

### 3. Failover Testing:
```bash
# Stop one backend server
sudo systemctl stop backend-service

# Test that traffic continues
curl http://example.com/

# Check logs for failover
tail -f /var/log/nginx/error.log
```

### 4. Session Persistence Testing:
```bash
# Test IP hash persistence
for i in {1..10}; do
    curl -H "X-Forwarded-For: 192.168.1.100" http://example.com/
done

# Test cookie-based persistence
curl -c cookies.txt http://example.com/
curl -b cookies.txt http://example.com/
```

## 5.8 Load Balancing Performance

### 1. Connection Optimization:
```nginx
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
    
    # Keep-alive connections
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}
```

### 2. Buffer Optimization:
```nginx
server {
    listen 80;
    location / {
        proxy_pass http://backend;
        
        # Buffer optimization
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        proxy_busy_buffers_size 8k;
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
    }
}
```

### 3. Caching:
```nginx
# Proxy cache for load balancing
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=lb_cache:10m max_size=1g inactive=60m;

upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}

server {
    listen 80;
    location / {
        proxy_cache lb_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_pass http://backend;
    }
}
```

## 5.9 Load Balancing Troubleshooting

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

#### Uneven Load Distribution:
```nginx
# Check server weights
upstream backend {
    server 192.168.1.10:8080 weight=3;
    server 192.168.1.11:8080 weight=1;  # This might be too low
}
```

#### Session Persistence Issues:
```bash
# Test IP hash consistency
for i in {1..5}; do
    curl -H "X-Forwarded-For: 192.168.1.100" http://example.com/
done
```

### 2. Debugging Tools:
```nginx
# Enable debug logging
error_log /var/log/nginx/debug.log debug;

# Add debug headers
add_header X-Upstream-Addr $upstream_addr;
add_header X-Upstream-Status $upstream_status;
add_header X-Upstream-Response-Time $upstream_response_time;
```

### 3. Monitoring Commands:
```bash
# Check upstream status
curl http://example.com/upstream_status

# Monitor error logs
tail -f /var/log/nginx/error.log | grep upstream

# Check server health
for server in 192.168.1.10 192.168.1.11 192.168.1.12; do
    echo "Testing $server:8080"
    curl -I http://$server:8080/health
done
```

## 5.10 Load Balancing Security

### 1. Access Control:
```nginx
# Restrict access to load balancer
server {
    listen 80;
    server_name _;
    
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
# Rate limiting for load balancer
limit_req_zone $binary_remote_addr zone=lb:10m rate=10r/s;

upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}

server {
    listen 80;
    location / {
        limit_req zone=lb burst=20 nodelay;
        proxy_pass http://backend;
    }
}
```

### 3. SSL Termination:
```nginx
# SSL termination at load balancer
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
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
# Security headers for load balancer
server {
    listen 80;
    location / {
        proxy_pass http://backend;
        
        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
    }
}
```

### 5. DDoS Protection:
```nginx
# DDoS protection
limit_req_zone $binary_remote_addr zone=ddos:10m rate=1r/s;
limit_conn_zone $binary_remote_addr zone=conn_limit_per_ip:10m;

upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    server 192.168.1.12:8080;
}

server {
    listen 80;
    location / {
        limit_req zone=ddos burst=5 nodelay;
        limit_conn conn_limit_per_ip 10;
        proxy_pass http://backend;
    }
}
```