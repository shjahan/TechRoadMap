# Section 12 – Service Mesh

## 12.1 Service Mesh Concepts

A service mesh is a dedicated infrastructure layer that handles service-to-service communication, providing observability, security, and traffic management.

### Key Concepts:

#### 1. **Data Plane**
Handles actual service-to-service communication.

#### 2. **Control Plane**
Manages and configures the data plane.

#### 3. **Sidecar Proxy**
Deployed alongside each service to handle communication.

### Service Mesh Benefits:

- **Traffic Management**: Load balancing, routing, and traffic splitting
- **Security**: mTLS, authentication, and authorization
- **Observability**: Metrics, logging, and tracing
- **Resilience**: Circuit breaking, retries, and timeouts

## 12.2 Istio Service Mesh

Istio is a popular service mesh implementation that provides traffic management, security, and observability.

### Istio Installation:

```yaml
# istio-installation.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: control-plane
spec:
  values:
    global:
      proxy:
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 128Mi
    pilot:
      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          cpu: 500m
          memory: 2048Mi
```

### Istio Gateway:

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
```

## 12.3 Linkerd Service Mesh

Linkerd is a lightweight service mesh that focuses on simplicity and performance.

### Linkerd Installation:

```bash
# Install Linkerd CLI
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh

# Install Linkerd control plane
linkerd install | kubectl apply -f -

# Install Linkerd data plane
linkerd inject k8s/ | kubectl apply -f -
```

### Linkerd Configuration:

```yaml
# linkerd-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: linkerd-config
  namespace: linkerd
data:
  config.yaml: |
    proxy:
      image:
        name: gcr.io/linkerd-io/proxy
        pullPolicy: IfNotPresent
      logLevel: info
      logFormat: plain
    controllerImage: gcr.io/linkerd-io/controller
    controllerLogLevel: info
    controllerLogFormat: plain
    webhookLogLevel: info
    webhookLogFormat: plain
    proxyInitImage: gcr.io/linkerd-io/proxy-init
    proxyInitImageVersion: v1.3.3
    debugImage: gcr.io/linkerd-io/debug
    debugImageVersion: v1.3.3
    grafana:
      enabled: true
      image:
        name: gcr.io/linkerd-io/grafana
        pullPolicy: IfNotPresent
    prometheus:
      enabled: true
      image:
        name: prom/prometheus
        pullPolicy: IfNotPresent
    tracing:
      enabled: true
      image:
        name: jaegertracing/all-in-one
        pullPolicy: IfNotPresent
```

## 12.4 Envoy Proxy

Envoy is a high-performance proxy that forms the data plane of many service meshes.

### Envoy Configuration:

```yaml
# envoy-config.yaml
static_resources:
  listeners:
  - name: listener_0
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 8080
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: ingress_http
          route_config:
            name: local_route
            virtual_hosts:
            - name: local_service
              domains: ["*"]
              routes:
              - match:
                  prefix: "/api/users"
                route:
                  cluster: user_service
              - match:
                  prefix: "/api/orders"
                route:
                  cluster: order_service
          http_filters:
          - name: envoy.filters.http.router
  clusters:
  - name: user_service
    connect_timeout: 0.25s
    type: LOGICAL_DNS
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: user_service
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: user-service
                port_value: 80
  - name: order_service
    connect_timeout: 0.25s
    type: LOGICAL_DNS
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: order_service
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: order-service
                port_value: 80
```

## 12.5 Traffic Management

Service mesh provides advanced traffic management capabilities.

### Traffic Splitting:

```yaml
# traffic-splitting.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: user-service
spec:
  hosts:
  - user-service
  http:
  - route:
    - destination:
        host: user-service
        port:
          number: 80
      weight: 90
    - destination:
        host: user-service-v2
        port:
          number: 80
      weight: 10
```

### Circuit Breaker:

```yaml
# circuit-breaker.yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: user-service
spec:
  host: user-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 10
      http:
        http1MaxPendingRequests: 10
        maxRequestsPerConnection: 2
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

## 12.6 Security Policies

Service mesh provides security policies for service-to-service communication.

### mTLS Policy:

```yaml
# mtls-policy.yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: microservices
spec:
  mtls:
    mode: STRICT
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: user-service-policy
  namespace: microservices
spec:
  selector:
    matchLabels:
      app: user-service
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/microservices/sa/order-service"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/users/*"]
```

## 12.7 Observability in Service Mesh

Service mesh provides comprehensive observability for microservices.

### Metrics Collection:

```yaml
# metrics-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'istio-mesh'
      kubernetes_sd_configs:
      - role: endpoints
        namespaces:
          names:
          - istio-system
      relabel_configs:
      - source_labels: [__meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: istio-telemetry;prometheus
```

### Distributed Tracing:

```yaml
# tracing-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: jaeger-config
data:
  jaeger.yaml: |
    sampling:
      type: const
      param: 1
    reporter:
      logSpans: true
      localAgentHostPort: jaeger-agent:6831
```

## 12.8 Service Mesh vs API Gateway

Service mesh and API gateway serve different purposes in microservices architecture.

### Comparison:

| Aspect | Service Mesh | API Gateway |
|--------|--------------|-------------|
| **Scope** | Service-to-service communication | External client communication |
| **Deployment** | Sidecar proxy | Centralized gateway |
| **Protocol** | Any protocol | HTTP/HTTPS |
| **Use Case** | Internal communication | External API management |

### When to Use:

- **Service Mesh**: For internal service communication, security, and observability
- **API Gateway**: For external API management, rate limiting, and authentication

This comprehensive guide covers all aspects of service mesh in microservices, providing both theoretical understanding and practical implementation examples.