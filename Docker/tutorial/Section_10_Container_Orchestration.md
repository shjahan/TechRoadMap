# Section 10 – Container Orchestration

## 10.1 Orchestration Concepts

Container Orchestration مدیریت خودکار کانتینرها در محیط‌های توزیع‌شده است. این مفهوم شامل deployment، scaling، load balancing، health monitoring و service discovery می‌شود.

### مفاهیم کلیدی Orchestration:

#### **1. Service Discovery**
- کشف خودکار سرویس‌ها
- مدیریت DNS داخلی
- Load balancing خودکار

#### **2. Load Balancing**
- توزیع ترافیک بین کانتینرها
- Health check و failover
- Session affinity

#### **3. Scaling**
- Auto-scaling بر اساس metrics
- Manual scaling
- Resource-based scaling

#### **4. Health Monitoring**
- Health checks
- Automatic restart
- Circuit breaker pattern

### مزایای Orchestration:
- **Automation**: خودکارسازی عملیات
- **Scalability**: مقیاس‌پذیری آسان
- **Reliability**: قابلیت اطمینان بالا
- **Resource Optimization**: بهینه‌سازی منابع

### مثال عملی:

#### **Docker Swarm:**
```bash
# راه‌اندازی Swarm
docker swarm init

# اضافه کردن node
docker swarm join --token SWMTKN-1-xxx 192.168.1.100:2377

# ایجاد service
docker service create --name web --replicas 3 nginx
```

#### **Kubernetes:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
```

## 10.2 Docker Swarm

Docker Swarm ابزار اورکستراسیون داخلی Docker است که برای مدیریت clusterهای کانتینر استفاده می‌شود.

### ویژگی‌های Docker Swarm:
- **Built-in**: داخلی Docker
- **Simple**: ساده برای استفاده
- **Scalable**: مقیاس‌پذیری آسان
- **Secure**: امنیت بالا

### راه‌اندازی Docker Swarm:

#### **1. Initialize Swarm:**
```bash
# راه‌اندازی Swarm
docker swarm init

# راه‌اندازی با IP خاص
docker swarm init --advertise-addr 192.168.1.100
```

#### **2. Join Nodes:**
```bash
# دریافت token برای worker
docker swarm join-token worker

# اضافه کردن worker node
docker swarm join --token SWMTKN-1-xxx 192.168.1.100:2377

# دریافت token برای manager
docker swarm join-token manager
```

### مثال عملی:

#### **ایجاد Service:**
```bash
# ایجاد service ساده
docker service create --name web nginx

# ایجاد service با تنظیمات
docker service create \
  --name web \
  --replicas 3 \
  --publish 80:80 \
  --constraint 'node.role==worker' \
  nginx:alpine
```

#### **مدیریت Service:**
```bash
# مشاهده serviceها
docker service ls

# مشاهده جزئیات service
docker service inspect web

# مقیاس‌دهی service
docker service scale web=5

# حذف service
docker service rm web
```

#### **Docker Compose با Swarm:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    networks:
      - web-network

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role==manager
    networks:
      - web-network

networks:
  web-network:
    driver: overlay
```

## 10.3 Kubernetes Basics

Kubernetes پلتفرم اورکستراسیون پیشرفته‌ای است که برای مدیریت کانتینرها در محیط‌های production استفاده می‌شود.

### مفاهیم کلیدی Kubernetes:

#### **1. Pods**
- کوچکترین واحد deployable
- شامل یک یا چند کانتینر
- اشتراک شبکه و storage

#### **2. Services**
- endpoint ثابت برای pods
- Load balancing
- Service discovery

#### **3. Deployments**
- مدیریت replica sets
- Rolling updates
- Rollback

#### **4. Namespaces**
- جداسازی منابع
- Multi-tenancy
- Resource quotas

### مثال عملی:

#### **Pod ساده:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  containers:
  - name: nginx
    image: nginx:alpine
    ports:
    - containerPort: 80
```

#### **Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
```

#### **Service:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
```

## 10.4 Service Discovery

Service Discovery مکانیزمی برای کشف خودکار سرویس‌ها در محیط‌های توزیع‌شده است.

### انواع Service Discovery:

#### **1. DNS-based Discovery**
```yaml
# Kubernetes Service
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
```

#### **2. Environment Variables**
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: my-app:latest
    env:
    - name: DATABASE_URL
      value: "postgres://db-service:5432/mydb"
```

#### **3. Service Mesh**
```yaml
# Istio ServiceEntry
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: external-service
spec:
  hosts:
  - external-service.example.com
  ports:
  - number: 80
    name: http
    protocol: HTTP
```

### مثال عملی:

#### **Docker Swarm Service Discovery:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    networks:
      - app-network

  api:
    image: my-api:latest
    environment:
      - DATABASE_URL=postgres://db:5432/myapp
    networks:
      - app-network
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    networks:
      - app-network

networks:
  app-network:
    driver: overlay
```

#### **Kubernetes Service Discovery:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80

---
apiVersion: v1
kind: Service
metadata:
  name: api-service
spec:
  selector:
    app: api
  ports:
  - port: 3000
    targetPort: 3000

---
apiVersion: v1
kind: Service
metadata:
  name: db-service
spec:
  selector:
    app: db
  ports:
  - port: 5432
    targetPort: 5432
```

## 10.5 Load Balancing

Load Balancing توزیع ترافیک بین چندین کانتینر برای بهبود عملکرد و قابلیت اطمینان است.

### انواع Load Balancing:

#### **1. Round Robin**
```yaml
# Kubernetes Service
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
```

#### **2. Session Affinity**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
  sessionAffinity: ClientIP
```

#### **3. Custom Load Balancer**
```yaml
# Nginx Load Balancer
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  nginx.conf: |
    events {
        worker_connections 1024;
    }
    http {
        upstream backend {
            server web-service:80;
        }
        server {
            listen 80;
            location / {
                proxy_pass http://backend;
            }
        }
    }
```

### مثال عملی:

#### **Docker Swarm Load Balancing:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    networks:
      - web-network

networks:
  web-network:
    driver: overlay
```

#### **Kubernetes Load Balancing:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80

---
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
```

## 10.6 Health Checks

Health Checks برای نظارت بر وضعیت کانتینرها و سرویس‌ها ضروری است.

### انواع Health Checks:

#### **1. HTTP Health Check**
```yaml
# Kubernetes
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: nginx
    image: nginx:alpine
    ports:
    - containerPort: 80
    livenessProbe:
      httpGet:
        path: /health
        port: 80
      initialDelaySeconds: 30
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 5
```

#### **2. Command Health Check**
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: postgres
    image: postgres:13
    livenessProbe:
      exec:
        command:
        - pg_isready
        - -U
        - postgres
      initialDelaySeconds: 30
      periodSeconds: 10
```

#### **3. TCP Health Check**
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: redis
    image: redis:alpine
    ports:
    - containerPort: 6379
    livenessProbe:
      tcpSocket:
        port: 6379
      initialDelaySeconds: 30
      periodSeconds: 10
```

### مثال عملی:

#### **Docker Swarm Health Check:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
```

#### **Kubernetes Health Check:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
        livenessProbe:
          httpGet:
            path: /health
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
```

## 10.7 Rolling Updates

Rolling Updates برای به‌روزرسانی کانتینرها بدون downtime ضروری است.

### استراتژی‌های Rolling Update:

#### **1. Rolling Update (پیش‌فرض)**
```yaml
# Kubernetes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
```

#### **2. Blue-Green Deployment**
```yaml
# Blue-Green with Kubernetes
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
    version: blue
  ports:
  - port: 80
    targetPort: 80

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
      version: blue
  template:
    metadata:
      labels:
        app: web
        version: blue
    spec:
      containers:
      - name: nginx
        image: nginx:1.20
        ports:
        - containerPort: 80
```

### مثال عملی:

#### **Docker Swarm Rolling Update:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
        monitor: 60s
      rollback_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
```

#### **Kubernetes Rolling Update:**
```bash
# به‌روزرسانی image
kubectl set image deployment/web-deployment nginx=nginx:1.21

# مشاهده وضعیت update
kubectl rollout status deployment/web-deployment

# rollback
kubectl rollout undo deployment/web-deployment

# مشاهده history
kubectl rollout history deployment/web-deployment
```

## 10.8 Auto-scaling

Auto-scaling برای تنظیم خودکار تعداد کانتینرها بر اساس metrics ضروری است.

### انواع Auto-scaling:

#### **1. Horizontal Pod Autoscaler (HPA)**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-deployment
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

#### **2. Vertical Pod Autoscaler (VPA)**
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-deployment
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: nginx
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 1000m
        memory: 1Gi
```

### مثال عملی:

#### **Docker Swarm Auto-scaling:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

#### **Kubernetes Auto-scaling:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-deployment
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## 10.9 Resource Management

مدیریت منابع برای بهینه‌سازی استفاده از CPU، حافظه و storage ضروری است.

### انواع Resource Management:

#### **1. Resource Requests و Limits**
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: nginx
    image: nginx:alpine
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 500m
        memory: 512Mi
```

#### **2. Resource Quotas**
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
spec:
  hard:
    requests.cpu: "2"
    requests.memory: 4Gi
    limits.cpu: "4"
    limits.memory: 8Gi
    pods: "10"
```

#### **3. Limit Ranges**
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: mem-limit-range
spec:
  limits:
  - default:
      memory: 512Mi
    defaultRequest:
      memory: 256Mi
    type: Container
```

### مثال عملی:

#### **Docker Swarm Resource Management:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
      placement:
        constraints:
          - node.role==worker
```

#### **Kubernetes Resource Management:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
      nodeSelector:
        kubernetes.io/os: linux
```

## 10.10 Cluster Management

مدیریت cluster برای نظارت و نگهداری محیط‌های توزیع‌شده ضروری است.

### جنبه‌های Cluster Management:

#### **1. Node Management**
```bash
# Docker Swarm
docker node ls
docker node inspect node-id
docker node update --availability drain node-id

# Kubernetes
kubectl get nodes
kubectl describe node node-name
kubectl drain node-name
```

#### **2. Monitoring**
```yaml
# Prometheus monitoring
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
```

#### **3. Backup and Recovery**
```bash
# Kubernetes etcd backup
etcdctl snapshot save backup.db
etcdctl snapshot restore backup.db

# Docker Swarm backup
docker service ls
docker stack ls
```

### مثال عملی:

#### **Docker Swarm Cluster Management:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    deploy:
      replicas: 3
      placement:
        constraints:
          - node.role==worker
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    networks:
      - web-network

  monitoring:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - prometheus-data:/prometheus
    networks:
      - web-network

networks:
  web-network:
    driver: overlay

volumes:
  prometheus-data:
```

#### **Kubernetes Cluster Management:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi

---
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  selector:
    app: web
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-deployment
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

این بخش شما را با تمام جنبه‌های Container Orchestration آشنا می‌کند.