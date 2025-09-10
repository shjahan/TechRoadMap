# Section 13 – Microservices with Docker

## 13.1 Microservices Architecture

معماری میکروسرویس‌ها با Docker امکان ایجاد سیستم‌های توزیع‌شده و مقیاس‌پذیر را فراهم می‌کند.

### اصول معماری میکروسرویس‌ها:
- **Single Responsibility**: هر سرویس یک مسئولیت دارد
- **Decentralized**: غیرمتمرکز و مستقل
- **Fault Tolerant**: مقاوم در برابر خطا
- **Scalable**: مقیاس‌پذیر
- **Technology Agnostic**: مستقل از تکنولوژی

### مزایای میکروسرویس‌ها با Docker:
- **Isolation**: جداسازی کامل سرویس‌ها
- **Scalability**: مقیاس‌دهی مستقل
- **Deployment**: استقرار مستقل
- **Technology Diversity**: تنوع تکنولوژی
- **Team Autonomy**: استقلال تیم‌ها

### مثال معماری میکروسرویس:
```yaml
version: '3.8'
services:
  # API Gateway
  gateway:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - user-service
      - order-service
      - product-service

  # User Service
  user-service:
    image: user-service:latest
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://user-db:5432/users
      - REDIS_URL=redis://redis:6379
    depends_on:
      - user-db
      - redis

  # Order Service
  order-service:
    image: order-service:latest
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://order-db:5432/orders
      - REDIS_URL=redis://redis:6379
    depends_on:
      - order-db
      - redis

  # Product Service
  product-service:
    image: product-service:latest
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://product-db:5432/products
      - REDIS_URL=redis://redis:6379
    depends_on:
      - product-db
      - redis

  # Databases
  user-db:
    image: postgres:13
    environment:
      POSTGRES_DB: users
      POSTGRES_PASSWORD: password
    volumes:
      - user-data:/var/lib/postgresql/data

  order-db:
    image: postgres:13
    environment:
      POSTGRES_DB: orders
      POSTGRES_PASSWORD: password
    volumes:
      - order-data:/var/lib/postgresql/data

  product-db:
    image: postgres:13
    environment:
      POSTGRES_DB: products
      POSTGRES_PASSWORD: password
    volumes:
      - product-data:/var/lib/postgresql/data

  # Cache
  redis:
    image: redis:alpine

volumes:
  user-data:
  order-data:
  product-data:
```

## 13.2 Service Decomposition

تجزیه سرویس‌ها برای ایجاد میکروسرویس‌های مؤثر.

### اصول تجزیه سرویس‌ها:

#### **1. Domain-Driven Design (DDD):**
```yaml
version: '3.8'
services:
  # User Domain
  user-service:
    image: user-service:latest
    environment:
      - SERVICE_NAME=user-service
      - PORT=3001
    networks:
      - user-network

  # Order Domain
  order-service:
    image: order-service:latest
    environment:
      - SERVICE_NAME=order-service
      - PORT=3002
    networks:
      - order-network

  # Product Domain
  product-service:
    image: product-service:latest
    environment:
      - SERVICE_NAME=product-service
      - PORT=3003
    networks:
      - product-network

networks:
  user-network:
    driver: bridge
  order-network:
    driver: bridge
  product-network:
    driver: bridge
```

#### **2. Database per Service:**
```yaml
version: '3.8'
services:
  user-service:
    image: user-service:latest
    environment:
      - DATABASE_URL=postgres://user-db:5432/users
    depends_on:
      - user-db

  user-db:
    image: postgres:13
    environment:
      POSTGRES_DB: users
      POSTGRES_PASSWORD: password
    volumes:
      - user-data:/var/lib/postgresql/data

  order-service:
    image: order-service:latest
    environment:
      - DATABASE_URL=postgres://order-db:5432/orders
    depends_on:
      - order-db

  order-db:
    image: postgres:13
    environment:
      POSTGRES_DB: orders
      POSTGRES_PASSWORD: password
    volumes:
      - order-data:/var/lib/postgresql/data

volumes:
  user-data:
  order-data:
```

### مثال تجزیه سرویس E-commerce:
```yaml
version: '3.8'
services:
  # Frontend
  frontend:
    image: frontend:latest
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://gateway:80
    depends_on:
      - gateway

  # API Gateway
  gateway:
    image: gateway:latest
    ports:
      - "80:80"
    depends_on:
      - user-service
      - product-service
      - order-service
      - payment-service

  # User Management
  user-service:
    image: user-service:latest
    environment:
      - DATABASE_URL=postgres://user-db:5432/users
      - REDIS_URL=redis://redis:6379
    depends_on:
      - user-db
      - redis

  # Product Catalog
  product-service:
    image: product-service:latest
    environment:
      - DATABASE_URL=postgres://product-db:5432/products
      - REDIS_URL=redis://redis:6379
    depends_on:
      - product-db
      - redis

  # Order Management
  order-service:
    image: order-service:latest
    environment:
      - DATABASE_URL=postgres://order-db:5432/orders
      - REDIS_URL=redis://redis:6379
    depends_on:
      - order-db
      - redis

  # Payment Processing
  payment-service:
    image: payment-service:latest
    environment:
      - DATABASE_URL=postgres://payment-db:5432/payments
      - REDIS_URL=redis://redis:6379
    depends_on:
      - payment-db
      - redis

  # Databases
  user-db:
    image: postgres:13
    environment:
      POSTGRES_DB: users
      POSTGRES_PASSWORD: password
    volumes:
      - user-data:/var/lib/postgresql/data

  product-db:
    image: postgres:13
    environment:
      POSTGRES_DB: products
      POSTGRES_PASSWORD: password
    volumes:
      - product-data:/var/lib/postgresql/data

  order-db:
    image: postgres:13
    environment:
      POSTGRES_DB: orders
      POSTGRES_PASSWORD: password
    volumes:
      - order-data:/var/lib/postgresql/data

  payment-db:
    image: postgres:13
    environment:
      POSTGRES_DB: payments
      POSTGRES_PASSWORD: password
    volumes:
      - payment-data:/var/lib/postgresql/data

  # Cache
  redis:
    image: redis:alpine

volumes:
  user-data:
  product-data:
  order-data:
  payment-data:
```

## 13.3 Service Communication

ارتباط بین سرویس‌ها در معماری میکروسرویس‌ها.

### انواع ارتباط:

#### **1. Synchronous Communication (HTTP/REST):**
```yaml
version: '3.8'
services:
  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
    networks:
      - microservices

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
      - USER_SERVICE_URL=http://user-service:3001
    networks:
      - microservices
    depends_on:
      - user-service

networks:
  microservices:
    driver: bridge
```

#### **2. Asynchronous Communication (Message Queue):**
```yaml
version: '3.8'
services:
  user-service:
    image: user-service:latest
    environment:
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - rabbitmq

  order-service:
    image: order-service:latest
    environment:
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - rabbitmq

  notification-service:
    image: notification-service:latest
    environment:
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - rabbitmq

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin
```

### مثال ارتباط سرویس‌ها:
```yaml
version: '3.8'
services:
  # API Gateway
  gateway:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - user-service
      - order-service

  # User Service
  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
      - DATABASE_URL=postgres://user-db:5432/users
      - RABBITMQ_URL=amqp://rabbitmq:5672
    networks:
      - microservices
    depends_on:
      - user-db
      - rabbitmq

  # Order Service
  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
      - DATABASE_URL=postgres://order-db:5432/orders
      - USER_SERVICE_URL=http://user-service:3001
      - RABBITMQ_URL=amqp://rabbitmq:5672
    networks:
      - microservices
    depends_on:
      - order-db
      - user-service
      - rabbitmq

  # Notification Service
  notification-service:
    image: notification-service:latest
    environment:
      - PORT=3003
      - RABBITMQ_URL=amqp://rabbitmq:5672
    networks:
      - microservices
    depends_on:
      - rabbitmq

  # Databases
  user-db:
    image: postgres:13
    environment:
      POSTGRES_DB: users
      POSTGRES_PASSWORD: password
    volumes:
      - user-data:/var/lib/postgresql/data

  order-db:
    image: postgres:13
    environment:
      POSTGRES_DB: orders
      POSTGRES_PASSWORD: password
    volumes:
      - order-data:/var/lib/postgresql/data

  # Message Queue
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin

networks:
  microservices:
    driver: bridge

volumes:
  user-data:
  order-data:
```

## 13.4 API Gateway Patterns

الگوهای API Gateway برای مدیریت ترافیک و routing.

### API Gateway با Nginx:
```yaml
version: '3.8'
services:
  gateway:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - user-service
      - order-service
      - product-service

  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
    networks:
      - microservices

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
    networks:
      - microservices

  product-service:
    image: product-service:latest
    environment:
      - PORT=3003
    networks:
      - microservices

networks:
  microservices:
    driver: bridge
```

### فایل nginx.conf:
```nginx
events {
    worker_connections 1024;
}

http {
    upstream user-service {
        server user-service:3001;
    }
    
    upstream order-service {
        server order-service:3002;
    }
    
    upstream product-service {
        server product-service:3003;
    }
    
    server {
        listen 80;
        
        # User Service Routes
        location /api/users {
            proxy_pass http://user-service;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Order Service Routes
        location /api/orders {
            proxy_pass http://order-service;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Product Service Routes
        location /api/products {
            proxy_pass http://product-service;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### API Gateway با Kong:
```yaml
version: '3.8'
services:
  kong:
    image: kong:latest
    ports:
      - "8000:8000"
      - "8001:8001"
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: /kong/declarative/kong.yml
    volumes:
      - ./kong.yml:/kong/declarative/kong.yml:ro
    depends_on:
      - user-service
      - order-service

  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
    networks:
      - microservices

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
    networks:
      - microservices

networks:
  microservices:
    driver: bridge
```

## 13.5 Service Discovery

کشف سرویس‌ها برای ارتباط خودکار بین میکروسرویس‌ها.

### Service Discovery با Consul:
```yaml
version: '3.8'
services:
  consul:
    image: consul:latest
    ports:
      - "8500:8500"
    command: agent -server -bootstrap-expect=1 -ui -client=0.0.0.0

  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
      - CONSUL_URL=http://consul:8500
    depends_on:
      - consul

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
      - CONSUL_URL=http://consul:8500
    depends_on:
      - consul

  product-service:
    image: product-service:latest
    environment:
      - PORT=3003
      - CONSUL_URL=http://consul:8500
    depends_on:
      - consul
```

### Service Discovery با Eureka:
```yaml
version: '3.8'
services:
  eureka:
    image: steeltoeoss/eureka-server
    ports:
      - "8761:8761"
    environment:
      - EUREKA_CLIENT_REGISTER_WITH_EUREKA=false
      - EUREKA_CLIENT_FETCH_REGISTRY=false

  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
      - EUREKA_URL=http://eureka:8761
    depends_on:
      - eureka

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
      - EUREKA_URL=http://eureka:8761
    depends_on:
      - eureka
```

## 13.6 Circuit Breaker Pattern

الگوی Circuit Breaker برای مدیریت خطاها و بهبود قابلیت اطمینان.

### Circuit Breaker با Hystrix:
```yaml
version: '3.8'
services:
  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
      - HYSTRIX_ENABLED=true
      - HYSTRIX_TIMEOUT=5000
    networks:
      - microservices

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
      - USER_SERVICE_URL=http://user-service:3001
      - HYSTRIX_ENABLED=true
      - HYSTRIX_TIMEOUT=5000
    networks:
      - microservices
    depends_on:
      - user-service

networks:
  microservices:
    driver: bridge
```

### Circuit Breaker با Istio:
```yaml
version: '3.8'
services:
  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
    networks:
      - microservices

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
      - USER_SERVICE_URL=http://user-service:3001
    networks:
      - microservices
    depends_on:
      - user-service

networks:
  microservices:
    driver: bridge
```

## 13.7 Bulkhead Pattern

الگوی Bulkhead برای جداسازی منابع و جلوگیری از انتشار خطا.

### Bulkhead با Resource Isolation:
```yaml
version: '3.8'
services:
  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    networks:
      - user-network

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    networks:
      - order-network

  product-service:
    image: product-service:latest
    environment:
      - PORT=3003
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
    networks:
      - product-network

networks:
  user-network:
    driver: bridge
  order-network:
    driver: bridge
  product-network:
    driver: bridge
```

## 13.8 Saga Pattern

الگوی Saga برای مدیریت تراکنش‌های توزیع‌شده.

### Saga با Event Sourcing:
```yaml
version: '3.8'
services:
  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - rabbitmq

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - rabbitmq

  payment-service:
    image: payment-service:latest
    environment:
      - PORT=3003
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - rabbitmq

  saga-orchestrator:
    image: saga-orchestrator:latest
    environment:
      - PORT=3004
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - rabbitmq

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin
```

## 13.9 Event-Driven Architecture

معماری Event-Driven برای ارتباط غیرهمزمان بین سرویس‌ها.

### Event-Driven با Apache Kafka:
```yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
      - KAFKA_URL=kafka:9092
    depends_on:
      - kafka

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
      - KAFKA_URL=kafka:9092
    depends_on:
      - kafka

  notification-service:
    image: notification-service:latest
    environment:
      - PORT=3003
      - KAFKA_URL=kafka:9092
    depends_on:
      - kafka
```

### Event-Driven با RabbitMQ:
```yaml
version: '3.8'
services:
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin

  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - rabbitmq

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - rabbitmq

  notification-service:
    image: notification-service:latest
    environment:
      - PORT=3003
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - rabbitmq
```

## 13.10 Microservices Testing

تست کردن میکروسرویس‌ها برای اطمینان از عملکرد صحیح.

### Contract Testing:
```yaml
version: '3.8'
services:
  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
    networks:
      - microservices

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
      - USER_SERVICE_URL=http://user-service:3001
    networks:
      - microservices
    depends_on:
      - user-service

  contract-tests:
    image: contract-tests:latest
    environment:
      - USER_SERVICE_URL=http://user-service:3001
      - ORDER_SERVICE_URL=http://order-service:3002
    networks:
      - microservices
    depends_on:
      - user-service
      - order-service

networks:
  microservices:
    driver: bridge
```

### Integration Testing:
```yaml
version: '3.8'
services:
  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
      - DATABASE_URL=postgres://user-db:5432/users_test
    depends_on:
      - user-db

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
      - DATABASE_URL=postgres://order-db:5432/orders_test
      - USER_SERVICE_URL=http://user-service:3001
    depends_on:
      - order-db
      - user-service

  user-db:
    image: postgres:13
    environment:
      POSTGRES_DB: users_test
      POSTGRES_PASSWORD: password

  order-db:
    image: postgres:13
    environment:
      POSTGRES_DB: orders_test
      POSTGRES_PASSWORD: password

  integration-tests:
    image: integration-tests:latest
    environment:
      - USER_SERVICE_URL=http://user-service:3001
      - ORDER_SERVICE_URL=http://order-service:3002
    depends_on:
      - user-service
      - order-service
```

### Load Testing:
```yaml
version: '3.8'
services:
  user-service:
    image: user-service:latest
    environment:
      - PORT=3001
    networks:
      - microservices

  order-service:
    image: order-service:latest
    environment:
      - PORT=3002
      - USER_SERVICE_URL=http://user-service:3001
    networks:
      - microservices
    depends_on:
      - user-service

  load-tests:
    image: load-tests:latest
    environment:
      - USER_SERVICE_URL=http://user-service:3001
      - ORDER_SERVICE_URL=http://order-service:3002
    networks:
      - microservices
    depends_on:
      - user-service
      - order-service

networks:
  microservices:
    driver: bridge
```

این بخش شما را با تمام جنبه‌های پیاده‌سازی میکروسرویس‌ها با Docker آشنا می‌کند.