# Section 17 - Nginx with Kubernetes

## 17.1 Kubernetes Integration Concepts

Kubernetes integration with Nginx involves using Nginx as an Ingress Controller to manage external access to services, handle load balancing, and provide advanced routing capabilities in a Kubernetes cluster.

### Key Concepts:
- **Ingress Controller**: Nginx as a Kubernetes Ingress Controller
- **Ingress Resources**: Kubernetes objects that define routing rules
- **Service Discovery**: Automatic discovery of services in the cluster
- **Load Balancing**: Built-in load balancing across pods
- **SSL Termination**: Handling SSL/TLS at the ingress level

### Real-world Analogy:
Think of Kubernetes with Nginx like a smart traffic management system:
- **Kubernetes Cluster** is a city with multiple districts (namespaces)
- **Nginx Ingress Controller** is the central traffic control system
- **Services** are different destinations in the city
- **Pods** are individual vehicles carrying passengers (requests)

### Architecture Overview:
```
Client Request → Nginx Ingress Controller → Kubernetes Service → Pod → Response
                     ↓
                Ingress Rules, SSL Termination, Load Balancing
```

### Example Basic Configuration:
```yaml
# nginx-ingress-controller.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-ingress-controller
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx-ingress-controller
  template:
    metadata:
      labels:
        app: nginx-ingress-controller
    spec:
      containers:
      - name: nginx-ingress-controller
        image: nginx/nginx-ingress:latest
        ports:
        - containerPort: 80
        - containerPort: 443
        env:
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
```

## 17.2 Ingress Controller

### Nginx Ingress Controller Setup:
```yaml
# nginx-ingress-controller.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-ingress-controller
  namespace: ingress-nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx-ingress-controller
  template:
    metadata:
      labels:
        app: nginx-ingress-controller
    spec:
      containers:
      - name: nginx-ingress-controller
        image: nginx/nginx-ingress:latest
        ports:
        - containerPort: 80
        - containerPort: 443
        env:
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 10254
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /healthz
            port: 10254
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-ingress-controller
  namespace: ingress-nginx
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
  - port: 443
    targetPort: 443
    protocol: TCP
    name: https
  selector:
    app: nginx-ingress-controller
```

### Ingress Controller Configuration:
```yaml
# nginx-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: ingress-nginx
data:
  worker-processes: "auto"
  worker-connections: "1024"
  keepalive-timeout: "65"
  client-max-body-size: "10m"
  proxy-connect-timeout: "30"
  proxy-send-timeout: "30"
  proxy-read-timeout: "30"
  proxy-buffer-size: "4k"
  proxy-buffers: "8 4k"
  gzip: "on"
  gzip-types: "text/plain text/css application/json application/javascript"
```

## 17.3 Service Configuration

### Basic Service Configuration:
```yaml
# app-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: default
spec:
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
  type: ClusterIP
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-app:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Advanced Service Configuration:
```yaml
# advanced-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: default
  labels:
    app: my-app
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  selector:
    app: my-app
  ports:
  - name: http
    port: 80
    targetPort: 8080
    protocol: TCP
  - name: https
    port: 443
    targetPort: 8443
    protocol: TCP
  type: LoadBalancer
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 3600
```

## 17.4 Load Balancing

### Ingress Load Balancing:
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: default
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/load-balance: "round_robin"
spec:
  tls:
  - hosts:
    - example.com
    secretName: tls-secret
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

### Advanced Load Balancing:
```yaml
# advanced-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: advanced-ingress
  namespace: default
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/load-balance: "least_conn"
    nginx.ingress.kubernetes.io/upstream-hash-by: "$binary_remote_addr"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
spec:
  tls:
  - hosts:
    - example.com
    secretName: tls-secret
  rules:
  - host: example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /admin
        pathType: Prefix
        backend:
          service:
            name: admin-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

## 17.5 Kubernetes Best Practices

### 1. Resource Management:
```yaml
# resource-management.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-ingress-controller
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx-ingress-controller
  template:
    metadata:
      labels:
        app: nginx-ingress-controller
    spec:
      containers:
      - name: nginx-ingress-controller
        image: nginx/nginx-ingress:latest
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 10254
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /healthz
            port: 10254
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 2. Security Best Practices:
```yaml
# security-practices.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-ingress-controller
  namespace: ingress-nginx
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: nginx-ingress-controller
rules:
- apiGroups: [""]
  resources: ["configmaps", "endpoints", "nodes", "pods", "secrets"]
  verbs: ["list", "watch"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get"]
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["extensions", "networking.k8s.io"]
  resources: ["ingresses"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["events"]
  verbs: ["create", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: nginx-ingress-controller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: nginx-ingress-controller
subjects:
- kind: ServiceAccount
  name: nginx-ingress-controller
  namespace: ingress-nginx
```

### 3. Monitoring and Logging:
```yaml
# monitoring.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
  namespace: ingress-nginx
data:
  enable-metrics: "true"
  metrics-port: "10254"
  enable-prometheus: "true"
  prometheus-port: "10254"
  enable-stats: "true"
  stats-port: "10254"
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-ingress-controller-metrics
  namespace: ingress-nginx
  labels:
    app: nginx-ingress-controller
spec:
  ports:
  - name: metrics
    port: 10254
    targetPort: 10254
  selector:
    app: nginx-ingress-controller
```

## 17.6 Kubernetes Testing

### 1. Ingress Testing:
```bash
# Test ingress configuration
kubectl get ingress
kubectl describe ingress app-ingress

# Test ingress endpoints
curl -H "Host: example.com" http://ingress-ip/
curl -H "Host: example.com" http://ingress-ip/api/
```

### 2. Service Testing:
```bash
# Test service endpoints
kubectl get services
kubectl describe service app-service

# Test service connectivity
kubectl exec -it pod-name -- curl http://app-service/
```

### 3. Load Testing:
```bash
# Load testing with kubectl
kubectl run load-test --image=williamyeh/wrk --rm -it --restart=Never -- -t12 -c400 -d30s http://app-service/

# Load testing with ab
kubectl run ab-test --image=httpd:alpine --rm -it --restart=Never -- ab -n 1000 -c 10 http://app-service/
```

## 17.7 Kubernetes Performance

### 1. Horizontal Pod Autoscaling:
```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-ingress-controller-hpa
  namespace: ingress-nginx
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-ingress-controller
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

### 2. Resource Optimization:
```yaml
# resource-optimization.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-ingress-controller
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx-ingress-controller
  template:
    metadata:
      labels:
        app: nginx-ingress-controller
    spec:
      containers:
      - name: nginx-ingress-controller
        image: nginx/nginx-ingress:latest
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        livenessProbe:
          httpGet:
            path: /healthz
            port: 10254
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /healthz
            port: 10254
          initialDelaySeconds: 5
          periodSeconds: 5
```

## 17.8 Kubernetes Troubleshooting

### 1. Common Issues:
```bash
# Check pod status
kubectl get pods -n ingress-nginx
kubectl describe pod nginx-ingress-controller-pod

# Check service status
kubectl get services -n ingress-nginx
kubectl describe service nginx-ingress-controller

# Check ingress status
kubectl get ingress
kubectl describe ingress app-ingress
```

### 2. Debugging Tools:
```bash
# Check logs
kubectl logs -n ingress-nginx nginx-ingress-controller-pod

# Check events
kubectl get events -n ingress-nginx

# Check configuration
kubectl get configmap nginx-config -n ingress-nginx -o yaml
```

### 3. Network Troubleshooting:
```bash
# Check network connectivity
kubectl exec -it nginx-ingress-controller-pod -- nslookup app-service
kubectl exec -it nginx-ingress-controller-pod -- curl http://app-service/

# Check DNS resolution
kubectl exec -it nginx-ingress-controller-pod -- nslookup kubernetes.default
```

## 17.9 Kubernetes Security

### 1. Network Policies:
```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: nginx-ingress-network-policy
  namespace: ingress-nginx
spec:
  podSelector:
    matchLabels:
      app: nginx-ingress-controller
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: default
    ports:
    - protocol: TCP
      port: 80
    - protocol: TCP
      port: 443
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: default
    ports:
    - protocol: TCP
      port: 80
    - protocol: TCP
      port: 443
```

### 2. RBAC Security:
```yaml
# rbac-security.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-ingress-controller
  namespace: ingress-nginx
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: nginx-ingress-controller
rules:
- apiGroups: [""]
  resources: ["configmaps", "endpoints", "nodes", "pods", "secrets"]
  verbs: ["list", "watch"]
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get"]
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["extensions", "networking.k8s.io"]
  resources: ["ingresses"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["events"]
  verbs: ["create", "patch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: nginx-ingress-controller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: nginx-ingress-controller
subjects:
- kind: ServiceAccount
  name: nginx-ingress-controller
  namespace: ingress-nginx
```

## 17.10 Kubernetes Documentation

### 1. Ingress Documentation:
```yaml
# ingress-documentation.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: default
  annotations:
    # Basic annotations
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    
    # Load balancing
    nginx.ingress.kubernetes.io/load-balance: "round_robin"
    nginx.ingress.kubernetes.io/upstream-hash-by: "$binary_remote_addr"
    
    # Timeouts
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "30"
    
    # Body size
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    
    # Rate limiting
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    
    # CORS
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://example.com"
    nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS"
    nginx.ingress.kubernetes.io/cors-allow-headers: "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization"
spec:
  tls:
  - hosts:
    - example.com
    secretName: tls-secret
  rules:
  - host: example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /admin
        pathType: Prefix
        backend:
          service:
            name: admin-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

### 2. Deployment Documentation:
```bash
#!/bin/bash
# Kubernetes deployment script

echo "Starting Kubernetes deployment..."

# Apply namespace
kubectl apply -f namespace.yaml

# Apply RBAC
kubectl apply -f rbac.yaml

# Apply ConfigMap
kubectl apply -f configmap.yaml

# Apply Deployment
kubectl apply -f deployment.yaml

# Apply Service
kubectl apply -f service.yaml

# Apply Ingress
kubectl apply -f ingress.yaml

# Wait for deployment
kubectl rollout status deployment/nginx-ingress-controller -n ingress-nginx

echo "Deployment completed successfully!"
```