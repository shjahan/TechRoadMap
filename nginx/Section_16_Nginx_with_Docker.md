# Section 16 - Nginx with Docker

## 16.1 Docker Integration Concepts

Docker integration with Nginx involves containerizing Nginx and using it as a reverse proxy for containerized applications, managing container networking, and orchestrating multi-container deployments.

### Key Concepts:
- **Containerization**: Running Nginx in Docker containers
- **Container Networking**: Communication between containers
- **Volume Management**: Persistent data and configuration
- **Multi-container Orchestration**: Managing multiple services
- **Container Registry**: Storing and distributing container images

### Real-world Analogy:
Think of Docker with Nginx like a shipping container system:
- **Docker Containers** are standardized shipping containers
- **Nginx** is the port authority that directs traffic
- **Docker Network** is the transportation system between containers
- **Docker Compose** is the logistics coordinator

### Architecture Overview:
```
Client Request → Nginx Container → Docker Network → Application Container → Response
                     ↓
                Volume Mounts (Config, Logs)
```

### Example Basic Configuration:
```dockerfile
# Dockerfile for Nginx
FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/
COPY ssl/ /etc/nginx/ssl/

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

## 16.2 Container Configuration

### Basic Nginx Container:
```dockerfile
# Dockerfile
FROM nginx:alpine

# Copy configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Create directories
RUN mkdir -p /var/log/nginx /var/cache/nginx

# Set permissions
RUN chown -R nginx:nginx /var/log/nginx /var/cache/nginx

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

### Multi-stage Build:
```dockerfile
# Multi-stage Dockerfile
FROM nginx:alpine AS base

# Install dependencies
RUN apk add --no-cache curl

# Copy configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

FROM base AS production
COPY ssl/ /etc/nginx/ssl/
EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
```

### Nginx Configuration for Containers:
```nginx
# nginx.conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    
    # Include additional configurations
    include /etc/nginx/conf.d/*.conf;
}
```

## 16.3 Docker Compose

### Basic Docker Compose:
```yaml
# docker-compose.yml
version: '3.8'

services:
  nginx:
    build: .
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./conf.d:/etc/nginx/conf.d
      - ./ssl:/etc/nginx/ssl
      - nginx_logs:/var/log/nginx
    depends_on:
      - app1
      - app2
    networks:
      - app-network

  app1:
    image: node:alpine
    command: node app.js
    volumes:
      - ./app1:/app
    networks:
      - app-network

  app2:
    image: python:alpine
    command: python app.py
    volumes:
      - ./app2:/app
    networks:
      - app-network

volumes:
  nginx_logs:

networks:
  app-network:
    driver: bridge
```

### Advanced Docker Compose:
```yaml
# docker-compose.yml
version: '3.8'

services:
  nginx:
    build: 
      context: .
      dockerfile: Dockerfile
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./conf.d:/etc/nginx/conf.d:ro
      - ./ssl:/etc/nginx/ssl:ro
      - nginx_logs:/var/log/nginx
    environment:
      - NGINX_ENVSUBST_TEMPLATE_DIR=/etc/nginx/templates
      - NGINX_ENVSUBST_OUTPUT_DIR=/etc/nginx/conf.d
    depends_on:
      - app1
      - app2
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  app1:
    image: node:alpine
    command: node app.js
    volumes:
      - ./app1:/app
    environment:
      - NODE_ENV=production
    networks:
      - app-network
    restart: unless-stopped

  app2:
    image: python:alpine
    command: python app.py
    volumes:
      - ./app2:/app
    environment:
      - PYTHON_ENV=production
    networks:
      - app-network
    restart: unless-stopped

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped

volumes:
  nginx_logs:
  redis_data:

networks:
  app-network:
    driver: bridge
```

## 16.4 Container Orchestration

### Docker Swarm:
```yaml
# docker-stack.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./conf.d:/etc/nginx/conf.d:ro
    deploy:
      replicas: 2
      placement:
        constraints:
          - node.role == manager
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M
    networks:
      - app-network

  app:
    image: myapp:latest
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
    networks:
      - app-network

networks:
  app-network:
    driver: overlay
```

### Kubernetes Deployment:
```yaml
# nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
        - containerPort: 443
        volumeMounts:
        - name: nginx-config
          mountPath: /etc/nginx/nginx.conf
          subPath: nginx.conf
        - name: nginx-conf-d
          mountPath: /etc/nginx/conf.d
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      volumes:
      - name: nginx-config
        configMap:
          name: nginx-config
      - name: nginx-conf-d
        configMap:
          name: nginx-conf-d
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
  - port: 443
    targetPort: 443
  type: LoadBalancer
```

## 16.5 Docker Best Practices

### 1. Security Best Practices:
```dockerfile
# Security-focused Dockerfile
FROM nginx:alpine

# Create non-root user
RUN addgroup -g 1001 -S nginx && \
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx

# Remove unnecessary packages
RUN apk del apk-tools

# Copy configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Set proper permissions
RUN chown -R nginx:nginx /var/log/nginx /var/cache/nginx /etc/nginx

# Switch to non-root user
USER nginx

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

### 2. Performance Optimization:
```dockerfile
# Performance-optimized Dockerfile
FROM nginx:alpine

# Install performance tools
RUN apk add --no-cache curl

# Copy configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Optimize for container environment
RUN echo "worker_processes auto;" > /etc/nginx/nginx.conf && \
    echo "events { worker_connections 1024; }" >> /etc/nginx/nginx.conf && \
    echo "http { include /etc/nginx/mime.types; default_type application/octet-stream; }" >> /etc/nginx/nginx.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

### 3. Health Checks:
```dockerfile
# Health check configuration
FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

## 16.6 Docker Testing

### 1. Container Testing:
```bash
# Build and test container
docker build -t my-nginx .
docker run -d --name test-nginx -p 80:80 my-nginx

# Test container
curl http://localhost/health
docker logs test-nginx

# Cleanup
docker stop test-nginx
docker rm test-nginx
```

### 2. Integration Testing:
```bash
# Test with docker-compose
docker-compose up -d
docker-compose ps
docker-compose logs nginx

# Test endpoints
curl http://localhost/api/health
curl http://localhost/api/users

# Cleanup
docker-compose down
```

### 3. Load Testing:
```bash
# Load testing with Docker
docker run --rm -it --network host williamyeh/wrk -t12 -c400 -d30s http://localhost/

# Load testing with ab
docker run --rm -it --network host httpd:alpine ab -n 1000 -c 10 http://localhost/
```

## 16.7 Docker Performance

### 1. Resource Optimization:
```yaml
# docker-compose.yml with resource limits
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
    networks:
      - app-network
```

### 2. Network Optimization:
```yaml
# Optimized networking
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    networks:
      - app-network
    sysctls:
      - net.core.somaxconn=65535
      - net.ipv4.tcp_max_syn_backlog=65535

networks:
  app-network:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.enable_icc: "true"
      com.docker.network.bridge.enable_ip_masquerade: "true"
```

## 16.8 Docker Troubleshooting

### 1. Common Issues:
```bash
# Check container status
docker ps -a
docker logs nginx-container

# Check container resources
docker stats nginx-container

# Check network connectivity
docker exec nginx-container ping app-container
```

### 2. Debugging Tools:
```bash
# Debug container
docker exec -it nginx-container sh
docker exec -it nginx-container nginx -t

# Check container configuration
docker inspect nginx-container
docker exec nginx-container cat /etc/nginx/nginx.conf
```

## 16.9 Docker Security

### 1. Container Security:
```dockerfile
# Security-focused Dockerfile
FROM nginx:alpine

# Update packages
RUN apk update && apk upgrade

# Remove unnecessary packages
RUN apk del apk-tools

# Create non-root user
RUN addgroup -g 1001 -S nginx && \
    adduser -S -D -H -u 1001 -h /var/cache/nginx -s /sbin/nologin -G nginx -g nginx nginx

# Copy configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Set proper permissions
RUN chown -R nginx:nginx /var/log/nginx /var/cache/nginx /etc/nginx

# Switch to non-root user
USER nginx

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

### 2. Network Security:
```yaml
# Secure networking
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    networks:
      - app-network
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
      - /var/cache/nginx
      - /var/run

networks:
  app-network:
    driver: bridge
    internal: true
```

## 16.10 Docker Documentation

### 1. Container Documentation:
```dockerfile
# Well-documented Dockerfile
FROM nginx:alpine

# Metadata
LABEL maintainer="admin@example.com"
LABEL version="1.0"
LABEL description="Nginx container for microservices"

# Environment variables
ENV NGINX_VERSION=1.20.2
ENV NGINX_USER=nginx
ENV NGINX_GROUP=nginx

# Install dependencies
RUN apk add --no-cache curl

# Copy configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/ /etc/nginx/conf.d/

# Create directories
RUN mkdir -p /var/log/nginx /var/cache/nginx

# Set permissions
RUN chown -R nginx:nginx /var/log/nginx /var/cache/nginx

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

### 2. Deployment Documentation:
```bash
#!/bin/bash
# Docker deployment script

echo "Starting Docker deployment..."

# Build images
docker build -t nginx:latest .

# Start services
docker-compose up -d

# Wait for services to be ready
sleep 10

# Health check
curl -f http://localhost/health || exit 1

echo "Deployment completed successfully!"
```