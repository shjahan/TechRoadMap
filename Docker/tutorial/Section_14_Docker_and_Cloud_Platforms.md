# Section 14 – Docker and Cloud Platforms

## 14.1 AWS ECS

Amazon Elastic Container Service (ECS) سرویس مدیریت کانتینرهای AWS است.

### ویژگی‌های AWS ECS:
- **Managed Service**: سرویس مدیریت شده
- **Auto Scaling**: مقیاس‌دهی خودکار
- **Load Balancing**: توزیع بار
- **Service Discovery**: کشف سرویس‌ها
- **Security**: امنیت بالا

### راه‌اندازی ECS:
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### ECS Task Definition:
```json
{
  "family": "web-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "web",
      "image": "nginx:alpine",
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "NODE_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/web-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### ECS Service:
```json
{
  "serviceName": "web-service",
  "cluster": "my-cluster",
  "taskDefinition": "web-app:1",
  "desiredCount": 3,
  "launchType": "FARGATE",
  "networkConfiguration": {
    "awsvpcConfiguration": {
      "subnets": ["subnet-12345", "subnet-67890"],
      "securityGroups": ["sg-12345"],
      "assignPublicIp": "ENABLED"
    }
  },
  "loadBalancers": [
    {
      "targetGroupArn": "arn:aws:elasticloadbalancing:region:account:targetgroup/web-tg/12345",
      "containerName": "web",
      "containerPort": 80
    }
  ]
}
```

## 14.2 AWS Fargate

AWS Fargate سرویس serverless برای اجرای کانتینرها است.

### ویژگی‌های Fargate:
- **Serverless**: بدون مدیریت سرور
- **Pay-per-use**: پرداخت بر اساس استفاده
- **Auto Scaling**: مقیاس‌دهی خودکار
- **Security**: امنیت بالا

### Fargate Task Definition:
```json
{
  "family": "fargate-app",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "my-app:latest",
      "portMappings": [
        {
          "containerPort": 3000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "NODE_ENV",
          "value": "production"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/fargate-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Fargate Service:
```json
{
  "serviceName": "fargate-service",
  "cluster": "my-cluster",
  "taskDefinition": "fargate-app:1",
  "desiredCount": 2,
  "launchType": "FARGATE",
  "platformVersion": "LATEST",
  "networkConfiguration": {
    "awsvpcConfiguration": {
      "subnets": ["subnet-12345", "subnet-67890"],
      "securityGroups": ["sg-12345"],
      "assignPublicIp": "ENABLED"
    }
  }
}
```

## 14.3 Google Cloud Run

Google Cloud Run سرویس serverless برای اجرای کانتینرها است.

### ویژگی‌های Cloud Run:
- **Serverless**: بدون مدیریت سرور
- **Auto Scaling**: مقیاس‌دهی خودکار
- **Pay-per-use**: پرداخت بر اساس استفاده
- **Global**: دسترسی جهانی

### Cloud Run Service:
```yaml
# cloud-run.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: web-app
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        autoscaling.knative.dev/minScale: "1"
    spec:
      containerConcurrency: 100
      containers:
      - image: gcr.io/project-id/web-app:latest
        ports:
        - containerPort: 8080
        env:
        - name: NODE_ENV
          value: production
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
          requests:
            cpu: "0.5"
            memory: "256Mi"
```

### Cloud Run با Docker Compose:
```yaml
version: '3.8'
services:
  web:
    image: gcr.io/project-id/web-app:latest
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
      - PORT=8080
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## 14.4 Azure Container Instances

Azure Container Instances سرویس مدیریت کانتینرهای Azure است.

### ویژگی‌های ACI:
- **Serverless**: بدون مدیریت سرور
- **Pay-per-use**: پرداخت بر اساس استفاده
- **Quick Deployment**: استقرار سریع
- **Security**: امنیت بالا

### ACI Container Group:
```json
{
  "apiVersion": "2018-10-01",
  "name": "web-app",
  "type": "Microsoft.ContainerInstance/containerGroups",
  "location": "eastus",
  "properties": {
    "containers": [
      {
        "name": "web",
        "properties": {
          "image": "nginx:alpine",
          "ports": [
            {
              "port": 80,
              "protocol": "TCP"
            }
          ],
          "environmentVariables": [
            {
              "name": "NODE_ENV",
              "value": "production"
            }
          ],
          "resources": {
            "requests": {
              "cpu": 1,
              "memoryInGb": 1
            }
          }
        }
      }
    ],
    "osType": "Linux",
    "ipAddress": {
      "type": "Public",
      "ports": [
        {
          "port": 80,
          "protocol": "TCP"
        }
      ]
    }
  }
}
```

### ACI با Docker Compose:
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## 14.5 Cloud Migration Strategies

استراتژی‌های مهاجرت به cloud برای اپلیکیشن‌های Docker.

### استراتژی‌های مهاجرت:

#### **1. Lift and Shift:**
```yaml
# docker-compose.yml (On-premise)
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
```

```yaml
# docker-compose.yml (Cloud)
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
```

#### **2. Replatforming:**
```yaml
# docker-compose.yml (Cloud Native)
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
    configs:
      - source: nginx_config
        target: /etc/nginx/nginx.conf
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3

configs:
  nginx_config:
    file: ./nginx.conf
```

### Migration Script:
```bash
#!/bin/bash
# migrate-to-cloud.sh

echo "Starting cloud migration..."

# 1. Build and push images to cloud registry
echo "1. Building and pushing images..."
docker build -t gcr.io/project-id/web-app:latest .
docker push gcr.io/project-id/web-app:latest

# 2. Deploy to cloud
echo "2. Deploying to cloud..."
gcloud run deploy web-app \
  --image gcr.io/project-id/web-app:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# 3. Verify deployment
echo "3. Verifying deployment..."
gcloud run services list

echo "Migration completed!"
```

## 14.6 Hybrid Cloud Deployments

پیاده‌سازی Hybrid Cloud برای ترکیب on-premise و cloud.

### Hybrid Cloud Setup:
```yaml
# docker-compose.yml (Hybrid)
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
    deploy:
      placement:
        constraints:
          - node.labels.cloud == true

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    deploy:
      placement:
        constraints:
          - node.labels.location == on-premise

volumes:
  postgres-data:
```

### Hybrid Cloud با Kubernetes:
```yaml
# hybrid-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      nodeSelector:
        cloud: "true"
      containers:
      - name: web
        image: nginx:alpine
        ports:
        - containerPort: 80
        env:
        - name: NODE_ENV
          value: production
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: database
spec:
  replicas: 1
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      nodeSelector:
        location: "on-premise"
      containers:
      - name: postgres
        image: postgres:13
        env:
        - name: POSTGRES_PASSWORD
          value: password
```

## 14.7 Multi-Cloud Strategies

استراتژی‌های Multi-Cloud برای توزیع اپلیکیشن‌ها در چندین cloud.

### Multi-Cloud Setup:
```yaml
# docker-compose.yml (Multi-Cloud)
version: '3.8'
services:
  web-aws:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
      - CLOUD_PROVIDER=aws
    deploy:
      placement:
        constraints:
          - node.labels.cloud == aws

  web-gcp:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
      - CLOUD_PROVIDER=gcp
    deploy:
      placement:
        constraints:
          - node.labels.cloud == gcp

  web-azure:
    image: nginx:alpine
    ports:
      - "80:80"
    environment:
      - NODE_ENV=production
      - CLOUD_PROVIDER=azure
    deploy:
      placement:
        constraints:
          - node.labels.cloud == azure
```

### Multi-Cloud Load Balancer:
```yaml
version: '3.8'
services:
  load-balancer:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web-aws
      - web-gcp
      - web-azure

  web-aws:
    image: nginx:alpine
    environment:
      - NODE_ENV=production
      - CLOUD_PROVIDER=aws

  web-gcp:
    image: nginx:alpine
    environment:
      - NODE_ENV=production
      - CLOUD_PROVIDER=gcp

  web-azure:
    image: nginx:alpine
    environment:
      - NODE_ENV=production
      - CLOUD_PROVIDER=azure
```

## 14.8 Cloud Cost Optimization

بهینه‌سازی هزینه‌های cloud برای اپلیکیشن‌های Docker.

### Cost Optimization Strategies:

#### **1. Resource Optimization:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M
    environment:
      - NODE_ENV=production
```

#### **2. Auto Scaling:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      replicas: 1
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          cpus: '0.25'
          memory: 128M
    environment:
      - NODE_ENV=production
```

#### **3. Spot Instances:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      placement:
        preferences:
          - spread: node.labels.instance-type
    environment:
      - NODE_ENV=production
```

### Cost Monitoring:
```bash
#!/bin/bash
# cost-monitor.sh

echo "=== Cloud Cost Monitoring ==="

# AWS Cost
echo "1. AWS Costs:"
aws ce get-cost-and-usage \
  --time-period Start=2023-01-01,End=2023-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost

# GCP Cost
echo "2. GCP Costs:"
gcloud billing budgets list

# Azure Cost
echo "3. Azure Costs:"
az consumption usage list --start-date 2023-01-01 --end-date 2023-01-31
```

## 14.9 Cloud Security

امنیت در cloud برای اپلیکیشن‌های Docker.

### Security Best Practices:

#### **1. Image Security:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    user: "1000:1000"
    read_only: true
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true
    environment:
      - NODE_ENV=production
```

#### **2. Network Security:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    networks:
      - frontend
    environment:
      - NODE_ENV=production

  app:
    image: my-app:latest
    networks:
      - frontend
      - backend
    environment:
      - NODE_ENV=production

  db:
    image: postgres:13
    networks:
      - backend
    environment:
      POSTGRES_PASSWORD: password

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true
```

#### **3. Secrets Management:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    environment:
      - NODE_ENV=production
    secrets:
      - db_password
    configs:
      - source: nginx_config
        target: /etc/nginx/nginx.conf

secrets:
  db_password:
    external: true

configs:
  nginx_config:
    file: ./nginx.conf
```

## 14.10 Cloud Monitoring

نظارت بر اپلیکیشن‌های Docker در cloud.

### Cloud Monitoring Setup:

#### **1. AWS CloudWatch:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    logging:
      driver: awslogs
      options:
        awslogs-group: /ecs/web-app
        awslogs-region: us-east-1
        awslogs-stream-prefix: ecs
    environment:
      - NODE_ENV=production
```

#### **2. Google Cloud Logging:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    logging:
      driver: gcplogs
      options:
        gcp-project: my-project
        gcp-log-cmd: true
    environment:
      - NODE_ENV=production
```

#### **3. Azure Monitor:**
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    logging:
      driver: azure
      options:
        azure-log-type: application
    environment:
      - NODE_ENV=production
```

### Monitoring Script:
```bash
#!/bin/bash
# cloud-monitor.sh

echo "=== Cloud Monitoring ==="

# AWS Monitoring
echo "1. AWS CloudWatch Metrics:"
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --start-time 2023-01-01T00:00:00Z \
  --end-time 2023-01-01T23:59:59Z \
  --period 300 \
  --statistics Average

# GCP Monitoring
echo "2. GCP Monitoring:"
gcloud monitoring metrics list --filter="metric.type:run.googleapis.com/container/cpu/utilizations"

# Azure Monitoring
echo "3. Azure Monitor:"
az monitor metrics list --resource my-resource --metric "Percentage CPU"
```

این بخش شما را با تمام جنبه‌های استفاده از Docker در پلتفرم‌های cloud آشنا می‌کند.