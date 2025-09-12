# Section 11 – Deployment & DevOps

## 11.1 Containerization with Docker

Containerization packages applications and their dependencies into lightweight, portable containers that can run consistently across different environments.

### Dockerfile for Microservices:

```dockerfile
# Multi-stage Dockerfile for Java Spring Boot application
FROM openjdk:11-jdk-slim as builder

# Set working directory
WORKDIR /app

# Copy Maven files
COPY pom.xml .
COPY .mvn .mvn
COPY mvnw .

# Download dependencies
RUN ./mvnw dependency:go-offline -B

# Copy source code
COPY src src

# Build application
RUN ./mvnw clean package -DskipTests

# Runtime stage
FROM openjdk:11-jre-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy application from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Change ownership to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run application
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Docker Compose for Development:

```yaml
# docker-compose.yml
version: '3.8'

services:
  user-service:
    build: ./user-service
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=docker
      - DATABASE_URL=jdbc:mysql://mysql:3306/user_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - mysql
      - redis
    networks:
      - microservices-network

  order-service:
    build: ./order-service
    ports:
      - "8081:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=docker
      - DATABASE_URL=jdbc:postgresql://postgres:5432/order_db
      - USER_SERVICE_URL=http://user-service:8080
    depends_on:
      - postgres
      - user-service
    networks:
      - microservices-network

  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=user_db
      - MYSQL_USER=user
      - MYSQL_PASSWORD=password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - microservices-network

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=order_db
      - POSTGRES_USER=order
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - microservices-network

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - microservices-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - user-service
      - order-service
    networks:
      - microservices-network

volumes:
  mysql_data:
  postgres_data:
  redis_data:

networks:
  microservices-network:
    driver: bridge
```

### Docker Build Script:

```bash
#!/bin/bash
# build.sh

set -e

# Build all microservices
echo "Building microservices..."

# Build user service
echo "Building user service..."
cd user-service
docker build -t user-service:latest .
cd ..

# Build order service
echo "Building order service..."
cd order-service
docker build -t order-service:latest .
cd ..

# Build product service
echo "Building product service..."
cd product-service
docker build -t product-service:latest .
cd ..

echo "All microservices built successfully!"
```

## 11.2 Container Orchestration with Kubernetes

Kubernetes provides container orchestration, managing the deployment, scaling, and networking of containerized applications.

### Kubernetes Deployment:

```yaml
# user-service-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
  labels:
    app: user-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: user-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "kubernetes"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: user-service-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: user-service-config
              key: redis-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        startupProbe:
          httpGet:
            path: /actuator/health/startup
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 30
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: user-service-config
data:
  redis-url: "redis://redis-service:6379"
  logging-level: "INFO"
---
apiVersion: v1
kind: Secret
metadata:
  name: user-service-secrets
type: Opaque
data:
  database-url: "amRiYzpteXNxbDovL215c3FsLXNlcnZpY2U6MzMwNi91c2VyX2Ri" # base64 encoded
```

### Kubernetes Service Mesh:

```yaml
# istio-gateway.yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: microservices-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: microservices-vs
spec:
  hosts:
  - "*"
  gateways:
  - microservices-gateway
  http:
  - match:
    - uri:
        prefix: /api/users
    route:
    - destination:
        host: user-service
        port:
          number: 80
  - match:
    - uri:
        prefix: /api/orders
    route:
    - destination:
        host: order-service
        port:
          number: 80
---
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT
```

## 11.3 CI/CD Pipelines for Microservices

CI/CD pipelines automate the build, test, and deployment of microservices.

### Jenkins Pipeline:

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry.com'
        KUBERNETES_NAMESPACE = 'microservices'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'mvn clean compile'
            }
        }
        
        stage('Test') {
            steps {
                sh 'mvn test'
            }
            post {
                always {
                    publishTestResults testResultsPattern: 'target/surefire-reports/*.xml'
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                sh 'mvn org.owasp:dependency-check-maven:check'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    def image = docker.build("${DOCKER_REGISTRY}/${env.JOB_NAME}:${env.BUILD_NUMBER}")
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-registry-credentials') {
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                sh "kubectl set image deployment/user-service user-service=${DOCKER_REGISTRY}/${env.JOB_NAME}:${env.BUILD_NUMBER} -n ${KUBERNETES_NAMESPACE}"
                sh "kubectl rollout status deployment/user-service -n ${KUBERNETES_NAMESPACE}"
            }
        }
        
        stage('Integration Tests') {
            steps {
                sh 'mvn verify -Pintegration-tests'
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                sh "kubectl set image deployment/user-service user-service=${DOCKER_REGISTRY}/${env.JOB_NAME}:${env.BUILD_NUMBER} -n production"
                sh "kubectl rollout status deployment/user-service -n production"
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            emailext (
                subject: "Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Build failed. Check the console output for details.",
                to: "team@example.com"
            )
        }
    }
}
```

### GitHub Actions Pipeline:

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  DOCKER_REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up JDK 11
      uses: actions/setup-java@v3
      with:
        java-version: '11'
        distribution: 'temurin'
    
    - name: Cache Maven dependencies
      uses: actions/cache@v3
      with:
        path: ~/.m2
        key: ${{ runner.os }}-m2-${{ hashFiles('**/pom.xml') }}
    
    - name: Run tests
      run: mvn test
    
    - name: Run security scan
      run: mvn org.owasp:dependency-check-maven:check
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: target/surefire-reports/

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Log in to Container Registry
      uses: docker/login-action@v2
      with:
        registry: ${{ env.DOCKER_REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          ${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBE_CONFIG }}
    
    - name: Deploy to staging
      run: |
        kubectl set image deployment/user-service user-service=${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} -n staging
        kubectl rollout status deployment/user-service -n staging

  deploy-production:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBE_CONFIG }}
    
    - name: Deploy to production
      run: |
        kubectl set image deployment/user-service user-service=${{ env.DOCKER_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} -n production
        kubectl rollout status deployment/user-service -n production
```

## 11.4 Blue-Green Deployment

Blue-Green deployment maintains two identical production environments, allowing for zero-downtime deployments.

### Blue-Green Deployment Script:

```bash
#!/bin/bash
# blue-green-deploy.sh

set -e

SERVICE_NAME="user-service"
NAMESPACE="production"
NEW_VERSION=$1
CURRENT_VERSION=$(kubectl get deployment $SERVICE_NAME -n $NAMESPACE -o jsonpath='{.spec.template.spec.containers[0].image}' | cut -d: -f2)

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: $0 <new-version>"
    exit 1
fi

echo "Current version: $CURRENT_VERSION"
echo "New version: $NEW_VERSION"

# Deploy new version to green environment
echo "Deploying new version to green environment..."
kubectl set image deployment/$SERVICE_NAME-green user-service=your-registry.com/$SERVICE_NAME:$NEW_VERSION -n $NAMESPACE
kubectl rollout status deployment/$SERVICE_NAME-green -n $NAMESPACE

# Run health checks
echo "Running health checks..."
kubectl get pods -l app=$SERVICE_NAME-green -n $NAMESPACE
kubectl get service $SERVICE_NAME-green -n $NAMESPACE

# Test new version
echo "Testing new version..."
GREEN_SERVICE_IP=$(kubectl get service $SERVICE_NAME-green -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
if [ -z "$GREEN_SERVICE_IP" ]; then
    GREEN_SERVICE_IP=$(kubectl get service $SERVICE_NAME-green -n $NAMESPACE -o jsonpath='{.spec.clusterIP}')
fi

# Health check
curl -f http://$GREEN_SERVICE_IP:8080/actuator/health || {
    echo "Health check failed for green environment"
    exit 1
}

# Switch traffic to green
echo "Switching traffic to green environment..."
kubectl patch service $SERVICE_NAME -n $NAMESPACE -p '{"spec":{"selector":{"version":"green"}}}'

# Wait for traffic to switch
sleep 30

# Verify traffic is flowing to green
echo "Verifying traffic is flowing to green environment..."
kubectl get pods -l app=$SERVICE_NAME-green -n $NAMESPACE

# Scale down blue environment
echo "Scaling down blue environment..."
kubectl scale deployment $SERVICE_NAME-blue --replicas=0 -n $NAMESPACE

echo "Blue-Green deployment completed successfully!"
```

### Kubernetes Blue-Green Deployment:

```yaml
# blue-green-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service-blue
  labels:
    app: user-service
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
      version: blue
  template:
    metadata:
      labels:
        app: user-service
        version: blue
    spec:
      containers:
      - name: user-service
        image: user-service:blue
        ports:
        - containerPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service-green
  labels:
    app: user-service
    version: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
      version: green
  template:
    metadata:
      labels:
        app: user-service
        version: green
    spec:
      containers:
      - name: user-service
        image: user-service:green
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
    version: blue  # This will be changed during deployment
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

## 11.5 Canary Deployment

Canary deployment gradually rolls out changes to a small subset of users before making them available to everyone.

### Canary Deployment Script:

```bash
#!/bin/bash
# canary-deploy.sh

set -e

SERVICE_NAME="user-service"
NAMESPACE="production"
NEW_VERSION=$1
CANARY_PERCENTAGE=${2:-10}

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: $0 <new-version> [canary-percentage]"
    exit 1
fi

echo "Deploying canary version: $NEW_VERSION with $CANARY_PERCENTAGE% traffic"

# Deploy canary version
echo "Deploying canary version..."
kubectl set image deployment/$SERVICE_NAME-canary user-service=your-registry.com/$SERVICE_NAME:$NEW_VERSION -n $NAMESPACE
kubectl rollout status deployment/$SERVICE_NAME-canary -n $NAMESPACE

# Configure traffic splitting
echo "Configuring traffic splitting..."
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: $SERVICE_NAME
spec:
  hosts:
  - $SERVICE_NAME
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: $SERVICE_NAME-canary
        port:
          number: 80
  - route:
    - destination:
        host: $SERVICE_NAME
        port:
          number: 80
      weight: $((100 - CANARY_PERCENTAGE))
    - destination:
        host: $SERVICE_NAME-canary
        port:
          number: 80
      weight: $CANARY_PERCENTAGE
EOF

# Monitor canary deployment
echo "Monitoring canary deployment..."
kubectl get pods -l app=$SERVICE_NAME -n $NAMESPACE

# Wait for monitoring period
echo "Waiting for monitoring period (5 minutes)..."
sleep 300

# Check metrics
echo "Checking canary metrics..."
kubectl get pods -l app=$SERVICE_NAME-canary -n $NAMESPACE

# Ask for confirmation to proceed
read -p "Do you want to promote the canary deployment? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Promoting canary deployment..."
    kubectl set image deployment/$SERVICE_NAME user-service=your-registry.com/$SERVICE_NAME:$NEW_VERSION -n $NAMESPACE
    kubectl rollout status deployment/$SERVICE_NAME -n $NAMESPACE
    
    # Remove canary deployment
    kubectl delete deployment $SERVICE_NAME-canary -n $NAMESPACE
    echo "Canary deployment promoted successfully!"
else
    echo "Rolling back canary deployment..."
    kubectl delete deployment $SERVICE_NAME-canary -n $NAMESPACE
    echo "Canary deployment rolled back!"
fi
```

## 11.6 Rolling Updates

Rolling updates gradually replace instances of the old version with the new version, ensuring zero downtime.

### Rolling Update Configuration:

```yaml
# rolling-update-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: user-service:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Rolling Update Script:

```bash
#!/bin/bash
# rolling-update.sh

set -e

SERVICE_NAME="user-service"
NAMESPACE="production"
NEW_VERSION=$1

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: $0 <new-version>"
    exit 1
fi

echo "Starting rolling update to version: $NEW_VERSION"

# Update deployment
echo "Updating deployment..."
kubectl set image deployment/$SERVICE_NAME user-service=your-registry.com/$SERVICE_NAME:$NEW_VERSION -n $NAMESPACE

# Monitor rollout
echo "Monitoring rollout..."
kubectl rollout status deployment/$SERVICE_NAME -n $NAMESPACE

# Verify deployment
echo "Verifying deployment..."
kubectl get pods -l app=$SERVICE_NAME -n $NAMESPACE

# Check service health
echo "Checking service health..."
kubectl get service $SERVICE_NAME -n $NAMESPACE

echo "Rolling update completed successfully!"
```

## 11.7 Infrastructure as Code

Infrastructure as Code (IaC) manages and provisions infrastructure through code, ensuring consistency and reproducibility.

### Terraform Configuration:

```hcl
# main.tf
provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "microservices_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "microservices-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "microservices_igw" {
  vpc_id = aws_vpc.microservices_vpc.id

  tags = {
    Name = "microservices-igw"
  }
}

# Public Subnets
resource "aws_subnet" "public_subnets" {
  count             = 2
  vpc_id            = aws_vpc.microservices_vpc.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index + 1}"
  }
}

# Private Subnets
resource "aws_subnet" "private_subnets" {
  count             = 2
  vpc_id            = aws_vpc.microservices_vpc.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "private-subnet-${count.index + 1}"
  }
}

# EKS Cluster
resource "aws_eks_cluster" "microservices_cluster" {
  name     = "microservices-cluster"
  role_arn = aws_iam_role.eks_cluster_role.arn
  version  = "1.24"

  vpc_config {
    subnet_ids = aws_subnet.private_subnets[*].id
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
  ]

  tags = {
    Name = "microservices-cluster"
  }
}

# EKS Node Group
resource "aws_eks_node_group" "microservices_nodes" {
  cluster_name    = aws_eks_cluster.microservices_cluster.name
  node_group_name = "microservices-nodes"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = aws_subnet.private_subnets[*].id

  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 1
  }

  instance_types = ["t3.medium"]

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.eks_container_registry_policy,
  ]

  tags = {
    Name = "microservices-nodes"
  }
}

# RDS Database
resource "aws_db_instance" "user_database" {
  identifier = "user-database"
  engine     = "mysql"
  engine_version = "8.0"
  instance_class = "db.t3.micro"
  allocated_storage = 20
  storage_type = "gp2"

  db_name  = "user_db"
  username = "admin"
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.microservices_db_subnet_group.name

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  skip_final_snapshot = true

  tags = {
    Name = "user-database"
  }
}
```

### Ansible Playbook:

```yaml
# deploy-microservices.yml
---
- name: Deploy Microservices to Kubernetes
  hosts: localhost
  gather_facts: no
  vars:
    namespace: "microservices"
    image_tag: "latest"
    
  tasks:
    - name: Create namespace
      kubernetes.core.k8s:
        name: "{{ namespace }}"
        api_version: v1
        kind: Namespace
        state: present

    - name: Deploy user service
      kubernetes.core.k8s:
        state: present
        definition:
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: user-service
            namespace: "{{ namespace }}"
          spec:
            replicas: 3
            selector:
              matchLabels:
                app: user-service
            template:
              metadata:
                labels:
                  app: user-service
              spec:
                containers:
                - name: user-service
                  image: "user-service:{{ image_tag }}"
                  ports:
                  - containerPort: 8080
                  env:
                  - name: SPRING_PROFILES_ACTIVE
                    value: "kubernetes"
                  resources:
                    requests:
                      memory: "256Mi"
                      cpu: "250m"
                    limits:
                      memory: "512Mi"
                      cpu: "500m"

    - name: Deploy user service
      kubernetes.core.k8s:
        state: present
        definition:
          apiVersion: v1
          kind: Service
          metadata:
            name: user-service
            namespace: "{{ namespace }}"
          spec:
            selector:
              app: user-service
            ports:
            - port: 80
              targetPort: 8080
            type: ClusterIP

    - name: Deploy order service
      kubernetes.core.k8s:
        state: present
        definition:
          apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: order-service
            namespace: "{{ namespace }}"
          spec:
            replicas: 3
            selector:
              matchLabels:
                app: order-service
            template:
              metadata:
                labels:
                  app: order-service
              spec:
                containers:
                - name: order-service
                  image: "order-service:{{ image_tag }}"
                  ports:
                  - containerPort: 8080
                  env:
                  - name: SPRING_PROFILES_ACTIVE
                    value: "kubernetes"
                  - name: USER_SERVICE_URL
                    value: "http://user-service:80"
                  resources:
                    requests:
                      memory: "256Mi"
                      cpu: "250m"
                    limits:
                      memory: "512Mi"
                      cpu: "500m"

    - name: Deploy order service
      kubernetes.core.k8s:
        state: present
        definition:
          apiVersion: v1
          kind: Service
          metadata:
            name: order-service
            namespace: "{{ namespace }}"
          spec:
            selector:
              app: order-service
            ports:
            - port: 80
              targetPort: 8080
            type: ClusterIP
```

## 11.8 GitOps for Microservices

GitOps uses Git as the single source of truth for infrastructure and application deployment.

### ArgoCD Application:

```yaml
# argocd-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: microservices-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/microservices-k8s
    targetRevision: HEAD
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: microservices
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### GitOps Workflow:

```yaml
# .github/workflows/gitops.yml
name: GitOps

on:
  push:
    branches: [ main ]
    paths: [ 'k8s/**' ]

jobs:
  update-apps:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Update image tags
      run: |
        # Update image tags in Kubernetes manifests
        find k8s -name "*.yaml" -exec sed -i "s|image: user-service:.*|image: user-service:${{ github.sha }}|g" {} \;
        find k8s -name "*.yaml" -exec sed -i "s|image: order-service:.*|image: order-service:${{ github.sha }}|g" {} \;
    
    - name: Commit changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add k8s/
        git commit -m "Update image tags to ${{ github.sha }}" || exit 0
        git push
```

This comprehensive guide covers all aspects of deployment and DevOps in microservices, providing both theoretical understanding and practical implementation examples. Each concept is explained with real-world scenarios and code examples to make the concepts clear and actionable.