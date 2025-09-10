# Section 13 - Nginx with Node.js

## 13.1 Node.js Integration Concepts

Node.js integration with Nginx involves using Nginx as a reverse proxy to handle static content and load balance Node.js applications, while Node.js handles dynamic content and API requests.

### Key Concepts:
- **Reverse Proxy**: Nginx forwards requests to Node.js applications
- **Load Balancing**: Distributing requests across multiple Node.js instances
- **Static File Serving**: Nginx serves static assets directly
- **Process Management**: Managing Node.js processes and clusters
- **WebSocket Support**: Handling real-time connections

### Real-world Analogy:
Think of Nginx with Node.js like a restaurant with specialized staff:
- **Nginx** is the host who greets customers and serves drinks (static content)
- **Node.js** is the specialized chef who prepares custom orders (dynamic content)
- **Load Balancer** is the manager who assigns customers to available chefs
- **WebSocket** is the direct communication line between customer and chef

### Architecture Overview:
```
Client Request → Nginx → Load Balancer → Node.js Cluster → Response
                     ↓
                Static Files (CSS, JS, Images)
```

### Example Basic Configuration:
```nginx
upstream nodejs_backend {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
}

server {
    listen 80;
    server_name example.com;
    root /var/www/html;

    # Serve static files directly
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Proxy to Node.js
    location / {
        proxy_pass http://nodejs_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 13.2 Proxy Configuration

### Basic Proxy Setup:
```nginx
server {
    listen 80;
    server_name api.example.com;
    root /var/www/api;

    # Proxy all requests to Node.js
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Advanced Proxy Configuration:
```nginx
upstream nodejs_app {
    server 127.0.0.1:3000 weight=3;
    server 127.0.0.1:3001 weight=2;
    server 127.0.0.1:3002 weight=1;
    
    # Health checks
    server 127.0.0.1:3003 backup;
}

server {
    listen 80;
    server_name api.example.com;

    # API endpoints
    location /api/ {
        proxy_pass http://nodejs_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        proxy_busy_buffers_size 8k;
        
        # Headers
        proxy_set_header Connection "";
        proxy_http_version 1.1;
    }

    # WebSocket support
    location /socket.io/ {
        proxy_pass http://nodejs_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket timeouts
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }
}
```

### WebSocket Configuration:
```nginx
# WebSocket proxy configuration
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

server {
    listen 80;
    server_name chat.example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket specific timeouts
        proxy_read_timeout 86400;
        proxy_send_timeout 86400;
    }
}
```

## 13.3 Load Balancing

### Round Robin Load Balancing:
```nginx
upstream nodejs_cluster {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
    server 127.0.0.1:3003;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://nodejs_cluster;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Weighted Load Balancing:
```nginx
upstream nodejs_cluster {
    # Primary servers with higher weight
    server 127.0.0.1:3000 weight=3;
    server 127.0.0.1:3001 weight=3;
    
    # Secondary servers with lower weight
    server 127.0.0.1:3002 weight=1;
    server 127.0.0.1:3003 weight=1;
    
    # Backup server
    server 127.0.0.1:3004 backup;
}
```

### Least Connections Load Balancing:
```nginx
upstream nodejs_cluster {
    least_conn;
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
    server 127.0.0.1:3003;
}
```

### IP Hash Load Balancing:
```nginx
upstream nodejs_cluster {
    ip_hash;
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
    server 127.0.0.1:3003;
}
```

### Health Checks and Failover:
```nginx
upstream nodejs_cluster {
    server 127.0.0.1:3000 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3001 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3002 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:3003 backup;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://nodejs_cluster;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # Error handling
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
        proxy_next_upstream_timeout 30s;
    }
}
```

## 13.4 Node.js Best Practices

### 1. Process Management:
```javascript
// cluster.js - Node.js cluster setup
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
    console.log(`Master ${process.pid} is running`);
    
    // Fork workers
    for (let i = 0; i < numCPUs; i++) {
        cluster.fork();
    }
    
    cluster.on('exit', (worker, code, signal) => {
        console.log(`Worker ${worker.process.pid} died`);
        cluster.fork(); // Restart worker
    });
} else {
    // Worker process
    require('./app.js');
    console.log(`Worker ${process.pid} started`);
}
```

### 2. Graceful Shutdown:
```javascript
// app.js - Graceful shutdown handling
const express = require('express');
const app = express();

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down gracefully');
    server.close(() => {
        console.log('Process terminated');
        process.exit(0);
    });
});

process.on('SIGINT', () => {
    console.log('SIGINT received, shutting down gracefully');
    server.close(() => {
        console.log('Process terminated');
        process.exit(0);
    });
});
```

### 3. Error Handling:
```javascript
// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

// Unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
    process.exit(1);
});
```

### 4. Nginx Configuration for Best Practices:
```nginx
# Optimized Nginx configuration for Node.js
upstream nodejs_cluster {
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
    server 127.0.0.1:3003;
}

server {
    listen 80;
    server_name api.example.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    # API endpoints
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://nodejs_cluster;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Connection optimization
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        
        # Error handling
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
    }
    
    # Static files
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
}
```

## 13.5 Node.js Testing

### 1. Unit Testing:
```javascript
// test/app.test.js
const request = require('supertest');
const app = require('../app');

describe('API Tests', () => {
    test('GET /api/health should return 200', async () => {
        const response = await request(app).get('/api/health');
        expect(response.status).toBe(200);
        expect(response.body.status).toBe('OK');
    });
    
    test('POST /api/users should create user', async () => {
        const userData = { name: 'John Doe', email: 'john@example.com' };
        const response = await request(app)
            .post('/api/users')
            .send(userData);
        expect(response.status).toBe(201);
        expect(response.body.name).toBe('John Doe');
    });
});
```

### 2. Load Testing:
```bash
# Load testing with Apache Bench
ab -n 1000 -c 10 http://api.example.com/api/health

# Load testing with wrk
wrk -t12 -c400 -d30s http://api.example.com/api/health

# Load testing with Artillery
artillery quick --count 100 --num 10 http://api.example.com/api/health
```

### 3. Integration Testing:
```javascript
// test/integration.test.js
const request = require('supertest');
const app = require('../app');

describe('Integration Tests', () => {
    test('Complete user flow', async () => {
        // Create user
        const createResponse = await request(app)
            .post('/api/users')
            .send({ name: 'Jane Doe', email: 'jane@example.com' });
        expect(createResponse.status).toBe(201);
        
        const userId = createResponse.body.id;
        
        // Get user
        const getResponse = await request(app).get(`/api/users/${userId}`);
        expect(getResponse.status).toBe(200);
        expect(getResponse.body.name).toBe('Jane Doe');
        
        // Update user
        const updateResponse = await request(app)
            .put(`/api/users/${userId}`)
            .send({ name: 'Jane Smith' });
        expect(updateResponse.status).toBe(200);
        
        // Delete user
        const deleteResponse = await request(app).delete(`/api/users/${userId}`);
        expect(deleteResponse.status).toBe(204);
    });
});
```

### 4. Nginx Testing:
```bash
# Test Nginx configuration
nginx -t

# Test with curl
curl -H "Host: api.example.com" http://localhost/api/health

# Test load balancing
for i in {1..10}; do
    curl -H "Host: api.example.com" http://localhost/api/health
    echo
done
```

## 13.6 Node.js Performance

### 1. Node.js Cluster Optimization:
```javascript
// cluster-optimized.js
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
    // Create workers based on CPU cores
    for (let i = 0; i < numCPUs; i++) {
        cluster.fork();
    }
    
    cluster.on('exit', (worker, code, signal) => {
        console.log(`Worker ${worker.process.pid} died`);
        cluster.fork();
    });
} else {
    // Worker process
    const express = require('express');
    const app = express();
    
    // Performance optimizations
    app.use(express.json({ limit: '10mb' }));
    app.use(express.urlencoded({ extended: true, limit: '10mb' }));
    
    // Routes
    app.get('/api/health', (req, res) => {
        res.json({ status: 'OK', pid: process.pid });
    });
    
    const server = app.listen(3000, () => {
        console.log(`Worker ${process.pid} listening on port 3000`);
    });
}
```

### 2. Nginx Performance Configuration:
```nginx
# High-performance Nginx configuration
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    # Basic optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 100;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript;
    
    # Upstream configuration
    upstream nodejs_cluster {
        least_conn;
        server 127.0.0.1:3000;
        server 127.0.0.1:3001;
        server 127.0.0.1:3002;
        server 127.0.0.1:3003;
        
        keepalive 32;
    }
    
    server {
        listen 80;
        server_name api.example.com;
        
        # Proxy configuration
        location / {
            proxy_pass http://nodejs_cluster;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            
            # Connection optimization
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            
            # Buffering
            proxy_buffering on;
            proxy_buffer_size 4k;
            proxy_buffers 8 4k;
        }
    }
}
```

### 3. Caching Strategy:
```nginx
# Caching configuration for Node.js
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m;

server {
    listen 80;
    server_name api.example.com;
    
    # Cache API responses
    location /api/ {
        proxy_cache api_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        
        proxy_pass http://nodejs_cluster;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # No cache for dynamic content
    location /api/auth/ {
        proxy_pass http://nodejs_cluster;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Memory Optimization:
```javascript
// Memory optimization in Node.js
const express = require('express');
const app = express();

// Limit request size
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Memory monitoring
setInterval(() => {
    const used = process.memoryUsage();
    console.log('Memory usage:', {
        rss: Math.round(used.rss / 1024 / 1024) + ' MB',
        heapTotal: Math.round(used.heapTotal / 1024 / 1024) + ' MB',
        heapUsed: Math.round(used.heapUsed / 1024 / 1024) + ' MB',
        external: Math.round(used.external / 1024 / 1024) + ' MB'
    });
}, 30000);

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM received, shutting down gracefully');
    process.exit(0);
});
```

## 13.7 Node.js Troubleshooting

### 1. Common Issues:

#### High Memory Usage:
```bash
# Check Node.js memory usage
ps aux | grep node
pm2 monit

# Monitor memory in real-time
watch -n 1 'ps aux --sort=-%mem | head -10'
```

#### Process Crashes:
```bash
# Check PM2 logs
pm2 logs

# Check system logs
journalctl -u nodejs-app

# Check for memory leaks
node --inspect app.js
```

#### Connection Issues:
```bash
# Check if Node.js is listening
netstat -tlnp | grep :3000
lsof -i :3000

# Test connection
curl http://localhost:3000/api/health
```

### 2. Debugging Tools:
```javascript
// Debug configuration
const debug = require('debug')('app');
const app = express();

// Debug middleware
app.use((req, res, next) => {
    debug(`${req.method} ${req.url}`);
    next();
});

// Error handling
app.use((err, req, res, next) => {
    debug('Error:', err);
    res.status(500).json({ error: 'Internal Server Error' });
});
```

### 3. Performance Monitoring:
```javascript
// Performance monitoring
const startTime = Date.now();

app.use((req, res, next) => {
    const start = Date.now();
    
    res.on('finish', () => {
        const duration = Date.now() - start;
        console.log(`${req.method} ${req.url} - ${res.statusCode} - ${duration}ms`);
    });
    
    next();
});

// Memory monitoring
setInterval(() => {
    const used = process.memoryUsage();
    if (used.heapUsed > 100 * 1024 * 1024) { // 100MB
        console.warn('High memory usage detected:', used.heapUsed / 1024 / 1024, 'MB');
    }
}, 30000);
```

## 13.8 Node.js Security

### 1. Input Validation:
```javascript
// Input validation middleware
const { body, validationResult } = require('express-validator');

app.post('/api/users', [
    body('email').isEmail().normalizeEmail(),
    body('password').isLength({ min: 8 }).matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/),
    body('name').trim().isLength({ min: 2, max: 50 })
], (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
    }
    // Process valid data
});
```

### 2. Rate Limiting:
```javascript
// Rate limiting with express-rate-limit
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limit each IP to 100 requests per windowMs
    message: 'Too many requests from this IP'
});

app.use('/api/', limiter);
```

### 3. Nginx Security Configuration:
```nginx
# Security configuration for Node.js
server {
    listen 80;
    server_name api.example.com;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    
    # API endpoints
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        
        proxy_pass http://nodejs_cluster;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Login endpoint with stricter rate limiting
    location /api/auth/login {
        limit_req zone=login burst=5 nodelay;
        
        proxy_pass http://nodejs_cluster;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Block common attack patterns
    location ~* \.(env|config|log)$ {
        deny all;
    }
}
```

### 4. Authentication and Authorization:
```javascript
// JWT authentication middleware
const jwt = require('jsonwebtoken');

const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) {
        return res.status(401).json({ error: 'Access token required' });
    }
    
    jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
            return res.status(403).json({ error: 'Invalid token' });
        }
        req.user = user;
        next();
    });
};

// Protected routes
app.get('/api/protected', authenticateToken, (req, res) => {
    res.json({ message: 'Protected data', user: req.user });
});
```

## 13.9 Node.js Documentation

### 1. API Documentation:
```javascript
// API documentation with Swagger
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const options = {
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'Node.js API',
            version: '1.0.0',
            description: 'API documentation for Node.js application'
        },
        servers: [
            {
                url: 'http://api.example.com',
                description: 'Production server'
            }
        ]
    },
    apis: ['./routes/*.js']
};

const specs = swaggerJsdoc(options);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));
```

### 2. Configuration Documentation:
```nginx
# =============================================================================
# Node.js Integration Configuration
# =============================================================================
# 
# This configuration provides:
# - Load balancing across Node.js instances
# - WebSocket support for real-time applications
# - Static file serving optimization
# - Security headers and rate limiting
# 
# Dependencies:
# - Node.js 16+ with PM2 or similar process manager
# - Express.js or similar web framework
# - WebSocket support (Socket.io recommended)
# 
# =============================================================================

upstream nodejs_cluster {
    least_conn;
    server 127.0.0.1:3000;
    server 127.0.0.1:3001;
    server 127.0.0.1:3002;
    server 127.0.0.1:3003;
    
    keepalive 32;
}

server {
    listen 80;
    server_name api.example.com;
    
    # Security and performance configuration
    # ... (configuration details)
}
```

### 3. Deployment Documentation:
```bash
#!/bin/bash
# Node.js deployment script

echo "Starting Node.js deployment..."

# Install dependencies
npm install --production

# Build application (if needed)
npm run build

# Start with PM2
pm2 start ecosystem.config.js

# Reload Nginx
nginx -s reload

echo "Deployment completed successfully!"
```

## 13.10 Node.js Monitoring

### 1. Application Monitoring:
```javascript
// Application monitoring with Prometheus
const promClient = require('prom-client');

// Create metrics
const httpRequestDuration = new promClient.Histogram({
    name: 'http_request_duration_seconds',
    help: 'Duration of HTTP requests in seconds',
    labelNames: ['method', 'route', 'status_code']
});

const httpRequestTotal = new promClient.Counter({
    name: 'http_requests_total',
    help: 'Total number of HTTP requests',
    labelNames: ['method', 'route', 'status_code']
});

// Middleware to collect metrics
app.use((req, res, next) => {
    const start = Date.now();
    
    res.on('finish', () => {
        const duration = (Date.now() - start) / 1000;
        httpRequestDuration
            .labels(req.method, req.route?.path || req.path, res.statusCode)
            .observe(duration);
        httpRequestTotal
            .labels(req.method, req.route?.path || req.path, res.statusCode)
            .inc();
    });
    
    next();
});

// Metrics endpoint
app.get('/metrics', (req, res) => {
    res.set('Content-Type', promClient.register.contentType);
    res.end(promClient.register.metrics());
});
```

### 2. Nginx Monitoring:
```nginx
# Nginx monitoring configuration
server {
    listen 80;
    server_name monitor.example.com;
    
    # Nginx status
    location /nginx_status {
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        deny all;
    }
    
    # Node.js health check
    location /health {
        proxy_pass http://nodejs_cluster;
        proxy_set_header Host $host;
        access_log off;
    }
}
```

### 3. Logging Configuration:
```javascript
// Structured logging with Winston
const winston = require('winston');

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
    ),
    defaultMeta: { service: 'nodejs-api' },
    transports: [
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' })
    ]
});

// Use logger in application
app.use((req, res, next) => {
    logger.info('Request received', {
        method: req.method,
        url: req.url,
        ip: req.ip,
        userAgent: req.get('User-Agent')
    });
    next();
});
```

### 4. Alerting Script:
```bash
#!/bin/bash
# Node.js monitoring and alerting

THRESHOLD_MEMORY=80
THRESHOLD_RESPONSE_TIME=2.0
ALERT_EMAIL="admin@example.com"

# Check Node.js memory usage
MEMORY_USAGE=$(ps aux --sort=-%mem | grep node | head -1 | awk '{print $4}')
if (( $(echo "$MEMORY_USAGE > $THRESHOLD_MEMORY" | bc -l) )); then
    echo "ALERT: High Node.js memory usage: $MEMORY_USAGE%" | mail -s "Node.js Memory Alert" $ALERT_EMAIL
fi

# Check response time
RESPONSE_TIME=$(curl -w "%{time_total}" -o /dev/null -s http://api.example.com/api/health)
if (( $(echo "$RESPONSE_TIME > $THRESHOLD_RESPONSE_TIME" | bc -l) )); then
    echo "ALERT: High Node.js response time: ${RESPONSE_TIME}s" | mail -s "Node.js Performance Alert" $ALERT_EMAIL
fi

# Check if Node.js is running
if ! pgrep -f "node.*app.js" > /dev/null; then
    echo "ALERT: Node.js application is not running" | mail -s "Node.js Down Alert" $ALERT_EMAIL
fi
```