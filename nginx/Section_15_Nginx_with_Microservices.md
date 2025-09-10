# Section 15 - Nginx with Microservices

## 15.1 Microservices Integration Concepts

Microservices integration with Nginx involves using Nginx as an API Gateway to route requests to different microservices, handle load balancing, and provide cross-cutting concerns like authentication, rate limiting, and monitoring.

### Key Concepts:
- **API Gateway**: Single entry point for all client requests
- **Service Discovery**: Finding and connecting to microservices
- **Load Balancing**: Distributing requests across service instances
- **Circuit Breaker**: Handling service failures gracefully
- **Service Mesh**: Advanced networking and communication patterns

### Real-world Analogy:
Think of Nginx with microservices like a hotel concierge system:
- **Nginx** is the main concierge desk that receives all guest requests
- **Microservices** are specialized departments (housekeeping, restaurant, spa, etc.)
- **Service Discovery** is the internal directory that knows which department handles what
- **Load Balancing** is assigning guests to available staff members

### Architecture Overview:
```
Client Request → Nginx API Gateway → Service Discovery → Microservice → Response
                     ↓
                Authentication, Rate Limiting, Monitoring
```

### Example Basic Configuration:
```nginx
upstream user_service {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

upstream order_service {
    server 127.0.0.1:8003;
    server 127.0.0.1:8004;
}

server {
    listen 80;
    server_name api.example.com;

    # User service
    location /api/users/ {
        proxy_pass http://user_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Order service
    location /api/orders/ {
        proxy_pass http://order_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 15.2 API Gateway Configuration

### Basic API Gateway Setup:
```nginx
# API Gateway configuration
upstream auth_service {
    server 127.0.0.1:8001;
}

upstream user_service {
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

upstream order_service {
    server 127.0.0.1:8004;
    server 127.0.0.1:8005;
}

upstream payment_service {
    server 127.0.0.1:8006;
    server 127.0.0.1:8007;
}

server {
    listen 80;
    server_name api.example.com;

    # Authentication service
    location /api/auth/ {
        proxy_pass http://auth_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # User service
    location /api/users/ {
        proxy_pass http://user_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Order service
    location /api/orders/ {
        proxy_pass http://order_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Payment service
    location /api/payments/ {
        proxy_pass http://payment_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Advanced API Gateway with Rate Limiting:
```nginx
# Rate limiting zones
limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/m;
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;
limit_req_zone $binary_remote_addr zone=payment:10m rate=10r/s;

server {
    listen 80;
    server_name api.example.com;

    # Authentication with strict rate limiting
    location /api/auth/ {
        limit_req zone=auth burst=5 nodelay;
        
        proxy_pass http://auth_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # General API with moderate rate limiting
    location /api/ {
        limit_req zone=api burst=50 nodelay;
        
        # Route to appropriate service based on path
        location ~ ^/api/users/(.*)$ {
            proxy_pass http://user_service/$1;
        }
        
        location ~ ^/api/orders/(.*)$ {
            proxy_pass http://order_service/$1;
        }
    }

    # Payment with strict rate limiting
    location /api/payments/ {
        limit_req zone=payment burst=10 nodelay;
        
        proxy_pass http://payment_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 15.3 Service Discovery

### Consul Integration:
```nginx
# Consul service discovery
upstream user_service {
    server 127.0.0.1:8002;
    server 127.0.1:8002;
    server 127.0.0.2:8002;
}

# Health check endpoint
location /health {
    access_log off;
    return 200 "healthy\n";
    add_header Content-Type text/plain;
}
```

### DNS-based Service Discovery:
```nginx
# DNS-based service discovery
upstream user_service {
    server user-service.internal:8002;
    server user-service.internal:8003;
    server user-service.internal:8004;
}

upstream order_service {
    server order-service.internal:8002;
    server order-service.internal:8003;
}
```

### Service Mesh Integration:
```nginx
# Service mesh configuration
upstream user_service {
    server istio-proxy:8002;
}

upstream order_service {
    server istio-proxy:8003;
}
```

## 15.4 Load Balancing

### Round Robin Load Balancing:
```nginx
upstream microservice_cluster {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
    server 127.0.0.1:8004;
}
```

### Weighted Load Balancing:
```nginx
upstream microservice_cluster {
    server 127.0.0.1:8001 weight=3;
    server 127.0.0.1:8002 weight=2;
    server 127.0.0.1:8003 weight=1;
    server 127.0.0.1:8004 backup;
}
```

### Least Connections:
```nginx
upstream microservice_cluster {
    least_conn;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
    server 127.0.0.1:8004;
}
```

### Health Checks:
```nginx
upstream microservice_cluster {
    server 127.0.0.1:8001 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8002 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8003 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8004 backup;
}
```

## 15.5 Microservices Best Practices

### 1. Circuit Breaker Pattern:
```nginx
# Circuit breaker implementation
upstream user_service {
    server 127.0.0.1:8001 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8002 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8003 backup;
}

server {
    listen 80;
    server_name api.example.com;

    location /api/users/ {
        proxy_pass http://user_service;
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 30s;
    }
}
```

### 2. Request Tracing:
```nginx
# Request tracing headers
server {
    listen 80;
    server_name api.example.com;

    location /api/ {
        proxy_pass http://microservice_cluster;
        proxy_set_header X-Request-ID $request_id;
        proxy_set_header X-Trace-ID $request_id;
        proxy_set_header X-Span-ID $request_id;
    }
}
```

### 3. Security Headers:
```nginx
# Security headers for microservices
server {
    listen 80;
    server_name api.example.com;

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location /api/ {
        proxy_pass http://microservice_cluster;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 15.6 Microservices Testing

### 1. Load Testing:
```bash
# Load testing microservices
ab -n 1000 -c 10 http://api.example.com/api/users/
ab -n 1000 -c 10 http://api.example.com/api/orders/
```

### 2. Integration Testing:
```bash
# Test service communication
curl -X GET http://api.example.com/api/users/1
curl -X POST http://api.example.com/api/orders/ -d '{"user_id": 1, "items": []}'
```

### 3. Health Check Testing:
```bash
# Test health endpoints
curl http://api.example.com/health
curl http://user-service:8002/health
curl http://order-service:8003/health
```

## 15.7 Microservices Performance

### 1. Connection Pooling:
```nginx
upstream microservice_cluster {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
    
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}
```

### 2. Caching:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=microservice_cache:10m max_size=1g inactive=60m;

server {
    listen 80;
    server_name api.example.com;

    location /api/ {
        proxy_cache microservice_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        
        proxy_pass http://microservice_cluster;
    }
}
```

## 15.8 Microservices Troubleshooting

### 1. Service Discovery Issues:
```bash
# Check service registration
consul catalog services
consul catalog nodes

# Check DNS resolution
nslookup user-service.internal
dig user-service.internal
```

### 2. Load Balancing Issues:
```bash
# Check upstream health
curl http://api.example.com/nginx_status

# Check individual services
curl http://user-service:8002/health
curl http://order-service:8003/health
```

## 15.9 Microservices Security

### 1. Authentication:
```nginx
# JWT authentication
location /api/ {
    auth_request /auth;
    proxy_pass http://microservice_cluster;
}

location = /auth {
    internal;
    proxy_pass http://auth_service/validate;
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header X-Original-URI $request_uri;
}
```

### 2. Rate Limiting:
```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=100r/s;

server {
    listen 80;
    server_name api.example.com;

    location /api/ {
        limit_req zone=api burst=50 nodelay;
        proxy_pass http://microservice_cluster;
    }
}
```

## 15.10 Microservices Documentation

### 1. API Documentation:
```yaml
# OpenAPI specification
openapi: 3.0.0
info:
  title: Microservices API
  version: 1.0.0
  description: API Gateway for microservices architecture

paths:
  /api/users:
    get:
      summary: Get users
      responses:
        '200':
          description: List of users
  /api/orders:
    post:
      summary: Create order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
```

### 2. Service Discovery Documentation:
```bash
# Service discovery configuration
# Consul configuration
consul agent -server -bootstrap-expect=3 -data-dir=/tmp/consul -node=agent-one -bind=172.20.20.10

# Service registration
curl -X PUT http://localhost:8500/v1/agent/service/register -d '{
  "ID": "user-service-1",
  "Name": "user-service",
  "Tags": ["api", "users"],
  "Address": "127.0.0.1",
  "Port": 8002,
  "Check": {
    "HTTP": "http://127.0.0.1:8002/health",
    "Interval": "10s"
  }
}'
```