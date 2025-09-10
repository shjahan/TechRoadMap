# Section 23 - Nginx with Cloud Platforms

## 23.1 Cloud Integration Concepts

Cloud integration with Nginx involves deploying and managing Nginx instances across various cloud platforms to leverage cloud-native features, scalability, and managed services.

### Key Concepts:
- **Cloud-Native Architecture**: Designing applications specifically for cloud environments
- **Managed Services**: Using cloud provider services instead of self-managed infrastructure
- **Auto-scaling**: Automatically adjusting resources based on demand
- **Multi-Cloud Strategy**: Using multiple cloud providers for redundancy and optimization
- **Cloud Security**: Implementing security best practices in cloud environments

### Real-world Analogy:
Think of cloud integration like moving from a traditional restaurant to a food court:
- **Traditional Setup**: You own the building, kitchen, and manage everything yourself
- **Cloud Setup**: You rent space in a food court with shared utilities, security, and management
- **Auto-scaling**: The food court automatically provides more tables during peak hours
- **Multi-cloud**: Having locations in different malls for redundancy

### Cloud Benefits:
- **Scalability**: Automatic resource scaling based on demand
- **Cost Optimization**: Pay only for what you use
- **High Availability**: Built-in redundancy and failover
- **Managed Services**: Less operational overhead
- **Global Reach**: Deploy across multiple regions

### Example Basic Cloud Configuration:
```nginx
# Basic cloud-optimized Nginx configuration
worker_processes auto;
worker_cpu_affinity auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    # Cloud-optimized settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    
    # Gzip compression for bandwidth optimization
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript;
    
    server {
        listen 80;
        server_name _;
        
        # Health check endpoint for load balancers
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
        
        location / {
            root /var/www/html;
            index index.html;
        }
    }
}
```

## 23.2 AWS Integration

Amazon Web Services (AWS) provides various services for deploying and managing Nginx in the cloud.

### AWS Services for Nginx:
- **EC2**: Virtual machines for running Nginx
- **Application Load Balancer (ALB)**: Managed load balancer
- **Elastic Container Service (ECS)**: Container orchestration
- **Elastic Kubernetes Service (EKS)**: Kubernetes management
- **CloudFront**: CDN service
- **Route 53**: DNS service
- **Certificate Manager**: SSL/TLS certificate management

### EC2 Deployment:
```bash
# Launch EC2 instance with Nginx
# User data script for EC2 launch
#!/bin/bash
yum update -y
yum install -y nginx
systemctl start nginx
systemctl enable nginx

# Configure Nginx
cat > /etc/nginx/conf.d/default.conf << 'EOF'
server {
    listen 80;
    server_name _;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
    }
    
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOF

systemctl reload nginx
```

### Application Load Balancer Configuration:
```nginx
# Nginx configuration behind ALB
server {
    listen 80;
    server_name _;
    
    # Trust ALB headers
    real_ip_header X-Forwarded-For;
    set_real_ip_from 10.0.0.0/8;
    set_real_ip_from 172.16.0.0/12;
    set_real_ip_from 192.168.0.0/16;
    
    # Log real client IP
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    
    access_log /var/log/nginx/access.log main;
    
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

### ECS Task Definition:
```json
{
  "family": "nginx-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "nginx",
      "image": "nginx:alpine",
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/nginx",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### CloudFront Integration:
```nginx
# Nginx configuration for CloudFront
server {
    listen 80;
    server_name _;
    
    # CloudFront headers
    add_header X-Cache $upstream_cache_status;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";
    
    # Cache control for static assets
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary Accept-Encoding;
    }
    
    # API endpoints with no cache
    location /api/ {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
        
        proxy_pass http://backend;
    }
}
```

## 23.3 Azure Integration

Microsoft Azure provides comprehensive cloud services for Nginx deployment and management.

### Azure Services for Nginx:
- **Virtual Machines**: Azure VMs for Nginx deployment
- **Azure Application Gateway**: Managed load balancer
- **Azure Container Instances (ACI)**: Serverless containers
- **Azure Kubernetes Service (AKS)**: Managed Kubernetes
- **Azure CDN**: Content delivery network
- **Azure DNS**: DNS management
- **Key Vault**: Certificate and secret management

### Azure VM Deployment:
```bash
# Azure CLI commands for Nginx deployment
# Create resource group
az group create --name nginx-rg --location eastus

# Create virtual machine
az vm create \
  --resource-group nginx-rg \
  --name nginx-vm \
  --image UbuntuLTS \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

# Install Nginx
az vm run-command invoke \
  --resource-group nginx-rg \
  --name nginx-vm \
  --command-id RunShellScript \
  --scripts "sudo apt update && sudo apt install -y nginx && sudo systemctl start nginx"
```

### Azure Application Gateway Configuration:
```nginx
# Nginx configuration behind Application Gateway
server {
    listen 80;
    server_name _;
    
    # Trust Application Gateway headers
    real_ip_header X-Forwarded-For;
    set_real_ip_from 10.0.0.0/8;
    set_real_ip_from 172.16.0.0/12;
    set_real_ip_from 192.168.0.0/16;
    
    # Health probe endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Main application
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

### Azure Container Instances:
```yaml
# aci-deployment.yaml
apiVersion: 2018-10-01
location: eastus
name: nginx-container
properties:
  containers:
  - name: nginx
    properties:
      image: nginx:alpine
      resources:
        requests:
          cpu: 1.0
          memoryInGb: 1.5
      ports:
      - port: 80
        protocol: TCP
  osType: Linux
  ipAddress:
    type: Public
    ports:
    - protocol: TCP
      port: 80
    dnsNameLabel: nginx-app
```

### Azure Key Vault Integration:
```nginx
# Nginx configuration with Azure Key Vault certificates
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # SSL configuration with Key Vault certificates
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-Frame-Options DENY always;
    
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

## 23.4 Google Cloud Integration

Google Cloud Platform (GCP) offers various services for Nginx deployment and management.

### GCP Services for Nginx:
- **Compute Engine**: Virtual machines for Nginx
- **Cloud Load Balancing**: Managed load balancer
- **Cloud Run**: Serverless containers
- **Google Kubernetes Engine (GKE)**: Managed Kubernetes
- **Cloud CDN**: Content delivery network
- **Cloud DNS**: DNS management
- **Certificate Manager**: SSL/TLS certificate management

### Compute Engine Deployment:
```bash
# Google Cloud CLI commands
# Create instance
gcloud compute instances create nginx-instance \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --machine-type=e2-medium \
    --zone=us-central1-a \
    --tags=http-server,https-server

# Install Nginx
gcloud compute ssh nginx-instance --zone=us-central1-a --command="
sudo apt update && 
sudo apt install -y nginx && 
sudo systemctl start nginx && 
sudo systemctl enable nginx
"
```

### Cloud Load Balancing Configuration:
```nginx
# Nginx configuration behind Cloud Load Balancer
server {
    listen 80;
    server_name _;
    
    # Trust Cloud Load Balancer headers
    real_ip_header X-Forwarded-For;
    set_real_ip_from 130.211.0.0/22;
    set_real_ip_from 35.191.0.0/16;
    
    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Main application
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

### Cloud Run Configuration:
```yaml
# cloud-run-service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: nginx-service
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cpu-throttling: "false"
    spec:
      containers:
      - image: nginx:alpine
        ports:
        - containerPort: 8080
        env:
        - name: PORT
          value: "8080"
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
```

### GKE Deployment:
```yaml
# nginx-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
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
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
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
  type: LoadBalancer
```

## 23.5 Cloud Best Practices

### 1. Security Best Practices:
```nginx
# Cloud security configuration
server {
    listen 80;
    server_name _;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        
        # Additional security measures
        add_header X-API-Version "1.0" always;
        
        proxy_pass http://backend;
    }
    
    # Block sensitive files
    location ~* \.(env|config|log|sql)$ {
        deny all;
    }
}
```

### 2. Performance Optimization:
```nginx
# Cloud performance optimization
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
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript;
    
    # Cache configuration
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;
    
    server {
        listen 80;
        server_name _;
        
        # Static file caching
        location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            access_log off;
        }
        
        # API caching
        location /api/ {
            proxy_cache my_cache;
            proxy_cache_valid 200 302 10m;
            proxy_cache_valid 404 1m;
            proxy_cache_key "$scheme$request_method$host$request_uri";
            
            proxy_pass http://backend;
        }
    }
}
```

### 3. Monitoring and Logging:
```nginx
# Cloud monitoring configuration
log_format cloud_logs '$remote_addr - $remote_user [$time_local] '
                      '"$request" $status $body_bytes_sent '
                      '"$http_referer" "$http_user_agent" '
                      'rt=$request_time uct="$upstream_connect_time" '
                      'uht="$upstream_header_time" urt="$upstream_response_time" '
                      'upstream_addr="$upstream_addr" '
                      'upstream_status="$upstream_status"';

server {
    listen 80;
    server_name _;
    
    access_log /var/log/nginx/access.log cloud_logs;
    error_log /var/log/nginx/error.log warn;
    
    # Health check for monitoring
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
    
    # Metrics endpoint
    location /metrics {
        access_log off;
        return 200 "nginx_up 1\n";
        add_header Content-Type text/plain;
    }
    
    location / {
        root /var/www/html;
        index index.html;
    }
}
```

## 23.6 Cloud Testing

### 1. Load Testing in Cloud:
```bash
# Load testing script for cloud environments
#!/bin/bash

CLOUD_ENDPOINT="https://your-app.cloudprovider.com"
CONCURRENT_USERS=100
TOTAL_REQUESTS=10000

echo "Starting cloud load test..."
echo "Endpoint: $CLOUD_ENDPOINT"
echo "Concurrent users: $CONCURRENT_USERS"
echo "Total requests: $TOTAL_REQUESTS"

# Test with Apache Bench
ab -n $TOTAL_REQUESTS -c $CONCURRENT_USERS $CLOUD_ENDPOINT/

# Test with wrk
wrk -t12 -c$CONCURRENT_USERS -d30s $CLOUD_ENDPOINT/

# Test with Artillery
artillery quick --count $CONCURRENT_USERS --num 100 $CLOUD_ENDPOINT/
```

### 2. Health Check Testing:
```bash
# Health check testing script
#!/bin/bash

ENDPOINTS=(
    "https://app1.cloudprovider.com/health"
    "https://app2.cloudprovider.com/health"
    "https://app3.cloudprovider.com/health"
)

for endpoint in "${ENDPOINTS[@]}"; do
    echo "Testing $endpoint"
    response=$(curl -s -o /dev/null -w "%{http_code}" $endpoint)
    if [ $response -eq 200 ]; then
        echo "✓ $endpoint is healthy"
    else
        echo "✗ $endpoint returned $response"
    fi
done
```

### 3. Performance Monitoring:
```bash
# Cloud performance monitoring
#!/bin/bash

echo "=== Cloud Performance Metrics ==="
echo "Date: $(date)"
echo ""

# Check response times
echo "Response Time Test:"
time curl -s https://your-app.cloudprovider.com/ > /dev/null

# Check SSL certificate
echo ""
echo "SSL Certificate Check:"
openssl s_client -connect your-app.cloudprovider.com:443 -servername your-app.cloudprovider.com < /dev/null 2>/dev/null | openssl x509 -noout -dates

# Check DNS resolution
echo ""
echo "DNS Resolution:"
nslookup your-app.cloudprovider.com
```

## 23.7 Cloud Performance

### 1. Auto-scaling Configuration:
```yaml
# Kubernetes HPA configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 2
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

### 2. CDN Configuration:
```nginx
# CDN-optimized configuration
server {
    listen 80;
    server_name _;
    
    # Cache control for CDN
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary Accept-Encoding;
        access_log off;
    }
    
    # API endpoints with no cache
    location /api/ {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        add_header Pragma "no-cache";
        add_header Expires "0";
        
        proxy_pass http://backend;
    }
    
    # Dynamic content with short cache
    location / {
        add_header Cache-Control "public, max-age=300";
        
        proxy_pass http://backend;
    }
}
```

### 3. Database Connection Pooling:
```nginx
# Database connection optimization
upstream database_backend {
    server db1.internal:5432 max_fails=3 fail_timeout=30s;
    server db2.internal:5432 max_fails=3 fail_timeout=30s;
    
    keepalive 32;
    keepalive_requests 100;
    keepalive_timeout 60s;
}

server {
    listen 80;
    server_name _;
    
    location /api/db/ {
        proxy_pass http://database_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # Connection optimization
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        
        # Timeouts
        proxy_connect_timeout 5s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
    }
}
```

## 23.8 Cloud Troubleshooting

### 1. Common Cloud Issues:

#### DNS Resolution Problems:
```bash
# Check DNS resolution
nslookup your-app.cloudprovider.com
dig your-app.cloudprovider.com

# Check DNS propagation
for i in {1..10}; do
    echo "Attempt $i:"
    nslookup your-app.cloudprovider.com
    sleep 5
done
```

#### Load Balancer Issues:
```bash
# Check load balancer health
curl -H "Host: your-app.cloudprovider.com" http://load-balancer-ip/health

# Check backend instances
curl -H "Host: your-app.cloudprovider.com" http://instance-ip/health
```

#### Certificate Issues:
```bash
# Check SSL certificate
openssl s_client -connect your-app.cloudprovider.com:443 -servername your-app.cloudprovider.com

# Check certificate expiration
echo | openssl s_client -connect your-app.cloudprovider.com:443 -servername your-app.cloudprovider.com 2>/dev/null | openssl x509 -noout -dates
```

### 2. Cloud Debugging Tools:
```bash
# Cloud debugging script
#!/bin/bash

echo "=== Cloud Debugging Information ==="
echo "Date: $(date)"
echo ""

# Check instance metadata
echo "Instance Metadata:"
curl -s http://169.254.169.254/latest/meta-data/instance-id 2>/dev/null || echo "Not available"

# Check network connectivity
echo ""
echo "Network Connectivity:"
ping -c 3 8.8.8.8

# Check DNS resolution
echo ""
echo "DNS Resolution:"
nslookup google.com

# Check Nginx status
echo ""
echo "Nginx Status:"
systemctl status nginx --no-pager

# Check logs
echo ""
echo "Recent Nginx Errors:"
tail -10 /var/log/nginx/error.log
```

## 23.9 Cloud Security

### 1. Network Security:
```nginx
# Cloud network security configuration
server {
    listen 80;
    server_name _;
    
    # Allow only specific IP ranges
    allow 10.0.0.0/8;
    allow 172.16.0.0/12;
    allow 192.168.0.0/16;
    deny all;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
    
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://backend;
    }
    
    location /login/ {
        limit_req zone=login burst=5 nodelay;
        proxy_pass http://backend;
    }
}
```

### 2. Secret Management:
```bash
# Cloud secret management
#!/bin/bash

# Retrieve secrets from cloud provider
DB_PASSWORD=$(aws ssm get-parameter --name "/app/database/password" --with-decryption --query "Parameter.Value" --output text)
API_KEY=$(aws ssm get-parameter --name "/app/api/key" --with-decryption --query "Parameter.Value" --output text)

# Update Nginx configuration with secrets
sed -i "s/DB_PASSWORD_PLACEHOLDER/$DB_PASSWORD/g" /etc/nginx/conf.d/app.conf
sed -i "s/API_KEY_PLACEHOLDER/$API_KEY/g" /etc/nginx/conf.d/app.conf

# Reload Nginx
nginx -s reload
```

### 3. WAF Integration:
```nginx
# WAF integration configuration
server {
    listen 80;
    server_name _;
    
    # WAF headers
    add_header X-WAF-Status $waf_status;
    add_header X-WAF-Action $waf_action;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Block common attack patterns
    location ~* \.(env|config|log|sql|bak|backup)$ {
        deny all;
    }
    
    # Block suspicious requests
    if ($request_uri ~* "(union|select|insert|delete|update|drop|create|alter)" ) {
        return 403;
    }
    
    location / {
        proxy_pass http://backend;
    }
}
```

## 23.10 Cloud Documentation

### 1. Infrastructure as Code:
```yaml
# Terraform configuration for cloud deployment
resource "aws_instance" "nginx" {
  ami           = "ami-0c02fb55956c7d3"
  instance_type = "t3.micro"
  
  vpc_security_group_ids = [aws_security_group.nginx.id]
  
  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y nginx
    systemctl start nginx
    systemctl enable nginx
  EOF
  
  tags = {
    Name = "nginx-server"
    Environment = "production"
  }
}

resource "aws_security_group" "nginx" {
  name_prefix = "nginx-"
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### 2. Monitoring Configuration:
```yaml
# CloudWatch monitoring configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-monitoring
data:
  nginx.conf: |
    server {
        listen 80;
        server_name _;
        
        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
        
        # Metrics endpoint
        location /metrics {
            access_log off;
            return 200 "nginx_up 1\n";
            add_header Content-Type text/plain;
        }
        
        location / {
            root /var/www/html;
            index index.html;
        }
    }
```

### 3. Deployment Pipeline:
```yaml
# CI/CD pipeline for cloud deployment
name: Deploy to Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2
    
    - name: Deploy to EC2
      run: |
        # Update Nginx configuration
        scp nginx.conf ec2-user@${{ secrets.EC2_HOST }}:/tmp/
        ssh ec2-user@${{ secrets.EC2_HOST }} "sudo cp /tmp/nginx.conf /etc/nginx/conf.d/ && sudo nginx -s reload"
    
    - name: Health Check
      run: |
        curl -f http://${{ secrets.EC2_HOST }}/health || exit 1
```