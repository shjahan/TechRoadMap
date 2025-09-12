# Section 4 – Service Discovery & Registration

## 4.1 Service Discovery Concepts

Service discovery is the process of automatically detecting and locating services in a distributed system. It enables services to find and communicate with each other without hardcoded endpoints.

### Key Concepts:

#### 1. **Service Registry**
A centralized database that maintains a list of available services and their locations.

#### 2. **Service Registration**
The process of services registering themselves with the service registry.

#### 3. **Service Discovery**
The process of services finding other services through the registry.

#### 4. **Health Checks**
Mechanisms to verify that services are running and healthy.

### Service Registry Implementation:

```java
// Service Registry Interface
public interface ServiceRegistry {
    void register(ServiceInstance serviceInstance);
    void deregister(String serviceId);
    List<ServiceInstance> getInstances(String serviceName);
    ServiceInstance getInstance(String serviceName, String instanceId);
}

// Service Instance
public class ServiceInstance {
    private String serviceId;
    private String serviceName;
    private String host;
    private int port;
    private boolean secure;
    private Map<String, String> metadata;
    private Instant registrationTime;
    private Instant lastHeartbeat;
    
    // Constructors, getters, setters
}

// Service Registry Implementation
@Component
public class InMemoryServiceRegistry implements ServiceRegistry {
    private final Map<String, ServiceInstance> services = new ConcurrentHashMap<>();
    private final Map<String, List<ServiceInstance>> serviceInstances = new ConcurrentHashMap<>();
    
    @Override
    public void register(ServiceInstance serviceInstance) {
        services.put(serviceInstance.getServiceId(), serviceInstance);
        serviceInstances.computeIfAbsent(serviceInstance.getServiceName(), k -> new ArrayList<>())
            .add(serviceInstance);
        
        log.info("Service registered: {} at {}:{}", 
            serviceInstance.getServiceName(), 
            serviceInstance.getHost(), 
            serviceInstance.getPort());
    }
    
    @Override
    public void deregister(String serviceId) {
        ServiceInstance instance = services.remove(serviceId);
        if (instance != null) {
            serviceInstances.get(instance.getServiceName()).remove(instance);
            log.info("Service deregistered: {}", serviceId);
        }
    }
    
    @Override
    public List<ServiceInstance> getInstances(String serviceName) {
        return serviceInstances.getOrDefault(serviceName, Collections.emptyList());
    }
}
```

## 4.2 Client-Side Service Discovery

In client-side service discovery, the client is responsible for querying the service registry and load balancing requests.

### Implementation:

```java
// Service Discovery Client
@Component
public class ServiceDiscoveryClient {
    @Autowired
    private ServiceRegistry serviceRegistry;
    @Autowired
    private LoadBalancer loadBalancer;
    
    public ServiceInstance getServiceInstance(String serviceName) {
        List<ServiceInstance> instances = serviceRegistry.getInstances(serviceName);
        
        if (instances.isEmpty()) {
            throw new ServiceNotFoundException("No instances found for service: " + serviceName);
        }
        
        return loadBalancer.choose(instances);
    }
    
    public String getServiceUrl(String serviceName, String path) {
        ServiceInstance instance = getServiceInstance(serviceName);
        String protocol = instance.isSecure() ? "https" : "http";
        return String.format("%s://%s:%d%s", protocol, instance.getHost(), instance.getPort(), path);
    }
}

// Load Balancer
@Component
public class RoundRobinLoadBalancer implements LoadBalancer {
    private final AtomicInteger counter = new AtomicInteger(0);
    
    @Override
    public ServiceInstance choose(List<ServiceInstance> instances) {
        if (instances.isEmpty()) {
            return null;
        }
        
        int index = counter.getAndIncrement() % instances.size();
        return instances.get(index);
    }
}

// Service Client with Discovery
@Component
public class UserServiceClient {
    @Autowired
    private ServiceDiscoveryClient serviceDiscoveryClient;
    @Autowired
    private RestTemplate restTemplate;
    
    public User getUser(Long id) {
        String url = serviceDiscoveryClient.getServiceUrl("user-service", "/api/users/" + id);
        
        try {
            ResponseEntity<User> response = restTemplate.getForEntity(url, User.class);
            return response.getBody();
        } catch (Exception e) {
            throw new UserServiceException("Failed to get user", e);
        }
    }
}
```

## 4.3 Server-Side Service Discovery

In server-side service discovery, a load balancer or proxy handles service discovery and routing.

### Implementation with Spring Cloud Gateway:

```java
// Gateway Configuration
@Configuration
public class GatewayConfig {
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("user-service", r -> r.path("/api/users/**")
                .uri("lb://user-service"))
            .route("order-service", r -> r.path("/api/orders/**")
                .uri("lb://order-service"))
            .route("product-service", r -> r.path("/api/products/**")
                .uri("lb://product-service"))
            .build();
    }
}

// Service Discovery Configuration
@Configuration
@EnableDiscoveryClient
public class DiscoveryConfig {
    @Bean
    public DiscoveryClientRouteDefinitionLocator discoveryClientRouteDefinitionLocator(
            DiscoveryClient discoveryClient) {
        return new DiscoveryClientRouteDefinitionLocator(discoveryClient);
    }
}
```

### Load Balancer Configuration:

```java
// Load Balancer Configuration
@Configuration
public class LoadBalancerConfig {
    @Bean
    @LoadBalanced
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
    
    @Bean
    public LoadBalancerClientFilter loadBalancerClientFilter(LoadBalancerClient client) {
        return new LoadBalancerClientFilter(client);
    }
}

// Service Client with Load Balancing
@Component
public class UserServiceClient {
    @Autowired
    @LoadBalanced
    private RestTemplate restTemplate;
    
    public User getUser(Long id) {
        String url = "http://user-service/api/users/" + id;
        
        try {
            ResponseEntity<User> response = restTemplate.getForEntity(url, User.class);
            return response.getBody();
        } catch (Exception e) {
            throw new UserServiceException("Failed to get user", e);
        }
    }
}
```

## 4.4 Service Registry Patterns

### Eureka Server Implementation:

```java
// Eureka Server
@SpringBootApplication
@EnableEurekaServer
public class EurekaServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServerApplication.class, args);
    }
}

// Eureka Server Configuration
@Configuration
public class EurekaServerConfig {
    @Bean
    public EurekaInstanceConfigBean eurekaInstanceConfigBean() {
        EurekaInstanceConfigBean config = new EurekaInstanceConfigBean();
        config.setInstanceId("eureka-server");
        config.setAppname("eureka-server");
        return config;
    }
}
```

### Eureka Client Implementation:

```java
// Eureka Client
@SpringBootApplication
@EnableEurekaClient
public class UserServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(UserServiceApplication.class, args);
    }
}

// Eureka Client Configuration
@Configuration
public class EurekaClientConfig {
    @Bean
    public EurekaInstanceConfigBean eurekaInstanceConfigBean() {
        EurekaInstanceConfigBean config = new EurekaInstanceConfigBean();
        config.setInstanceId("user-service-" + System.currentTimeMillis());
        config.setAppname("user-service");
        config.setHostname("localhost");
        config.setPort(8080);
        config.setSecurePort(8443);
        return config;
    }
}
```

### Consul Service Registry:

```java
// Consul Configuration
@Configuration
public class ConsulConfig {
    @Bean
    public ConsulClient consulClient() {
        return new ConsulClient("localhost", 8500);
    }
}

// Consul Service Registration
@Component
public class ConsulServiceRegistration {
    @Autowired
    private ConsulClient consulClient;
    
    @PostConstruct
    public void registerService() {
        NewService newService = new NewService();
        newService.setId("user-service-1");
        newService.setName("user-service");
        newService.setAddress("localhost");
        newService.setPort(8080);
        
        NewService.Check check = new NewService.Check();
        check.setHttp("http://localhost:8080/health");
        check.setInterval("10s");
        newService.setCheck(check);
        
        consulClient.agentServiceRegister(newService);
    }
    
    @PreDestroy
    public void deregisterService() {
        consulClient.agentServiceDeregister("user-service-1");
    }
}
```

## 4.5 Health Checks and Monitoring

Health checks are essential for service discovery to ensure only healthy services are used.

### Health Check Implementation:

```java
// Health Check Controller
@RestController
@RequestMapping("/health")
public class HealthController {
    @Autowired
    private UserService userService;
    @Autowired
    private UserRepository userRepository;
    
    @GetMapping
    public ResponseEntity<HealthStatus> getHealth() {
        HealthStatus status = checkHealth();
        
        if (status.isHealthy()) {
            return ResponseEntity.ok(status);
        } else {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(status);
        }
    }
    
    private HealthStatus checkHealth() {
        HealthStatus status = new HealthStatus();
        
        // Check database connectivity
        try {
            userRepository.count();
            status.addCheck("database", "UP", "Database connection successful");
        } catch (Exception e) {
            status.addCheck("database", "DOWN", "Database connection failed: " + e.getMessage());
        }
        
        // Check external service dependencies
        try {
            // Check if external services are reachable
            status.addCheck("external-services", "UP", "External services reachable");
        } catch (Exception e) {
            status.addCheck("external-services", "DOWN", "External services unreachable: " + e.getMessage());
        }
        
        return status;
    }
}

// Health Status Model
public class HealthStatus {
    private boolean healthy;
    private Map<String, CheckResult> checks = new HashMap<>();
    private Instant timestamp;
    
    public void addCheck(String name, String status, String message) {
        checks.put(name, new CheckResult(status, message));
        this.healthy = checks.values().stream().allMatch(check -> "UP".equals(check.getStatus()));
    }
    
    // Getters and setters
}

// Check Result Model
public class CheckResult {
    private String status;
    private String message;
    
    // Constructors, getters, setters
}
```

### Actuator Health Checks:

```java
// Custom Health Indicator
@Component
public class DatabaseHealthIndicator implements HealthIndicator {
    @Autowired
    private UserRepository userRepository;
    
    @Override
    public Health health() {
        try {
            userRepository.count();
            return Health.up()
                .withDetail("database", "Available")
                .withDetail("responseTime", "10ms")
                .build();
        } catch (Exception e) {
            return Health.down()
                .withDetail("database", "Unavailable")
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}

// Custom Health Indicator for External Services
@Component
public class ExternalServiceHealthIndicator implements HealthIndicator {
    @Autowired
    private RestTemplate restTemplate;
    
    @Override
    public Health health() {
        try {
            ResponseEntity<String> response = restTemplate.getForEntity(
                "http://external-service/health", String.class);
            
            if (response.getStatusCode().is2xxSuccessful()) {
                return Health.up()
                    .withDetail("external-service", "Available")
                    .build();
            } else {
                return Health.down()
                    .withDetail("external-service", "Unavailable")
                    .withDetail("status", response.getStatusCode())
                    .build();
            }
        } catch (Exception e) {
            return Health.down()
                .withDetail("external-service", "Unavailable")
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
```

## 4.6 Load Balancing in Service Discovery

Load balancing distributes requests across multiple service instances to improve performance and reliability.

### Round Robin Load Balancing:

```java
// Round Robin Load Balancer
@Component
public class RoundRobinLoadBalancer implements LoadBalancer {
    private final AtomicInteger counter = new AtomicInteger(0);
    
    @Override
    public ServiceInstance choose(List<ServiceInstance> instances) {
        if (instances.isEmpty()) {
            return null;
        }
        
        int index = counter.getAndIncrement() % instances.size();
        return instances.get(index);
    }
}
```

### Weighted Round Robin Load Balancing:

```java
// Weighted Round Robin Load Balancer
@Component
public class WeightedRoundRobinLoadBalancer implements LoadBalancer {
    private final AtomicInteger counter = new AtomicInteger(0);
    
    @Override
    public ServiceInstance choose(List<ServiceInstance> instances) {
        if (instances.isEmpty()) {
            return null;
        }
        
        // Calculate total weight
        int totalWeight = instances.stream()
            .mapToInt(instance -> getWeight(instance))
            .sum();
        
        if (totalWeight == 0) {
            return instances.get(counter.getAndIncrement() % instances.size());
        }
        
        // Select instance based on weight
        int randomWeight = counter.getAndIncrement() % totalWeight;
        int currentWeight = 0;
        
        for (ServiceInstance instance : instances) {
            currentWeight += getWeight(instance);
            if (randomWeight < currentWeight) {
                return instance;
            }
        }
        
        return instances.get(instances.size() - 1);
    }
    
    private int getWeight(ServiceInstance instance) {
        String weightStr = instance.getMetadata().get("weight");
        return weightStr != null ? Integer.parseInt(weightStr) : 1;
    }
}
```

### Least Connections Load Balancing:

```java
// Least Connections Load Balancer
@Component
public class LeastConnectionsLoadBalancer implements LoadBalancer {
    private final Map<String, AtomicInteger> connectionCounts = new ConcurrentHashMap<>();
    
    @Override
    public ServiceInstance choose(List<ServiceInstance> instances) {
        if (instances.isEmpty()) {
            return null;
        }
        
        return instances.stream()
            .min(Comparator.comparing(instance -> 
                connectionCounts.getOrDefault(instance.getServiceId(), new AtomicInteger(0)).get()))
            .orElse(instances.get(0));
    }
    
    public void incrementConnections(String serviceId) {
        connectionCounts.computeIfAbsent(serviceId, k -> new AtomicInteger(0)).incrementAndGet();
    }
    
    public void decrementConnections(String serviceId) {
        connectionCounts.computeIfAbsent(serviceId, k -> new AtomicInteger(0)).decrementAndGet();
    }
}
```

## 4.7 Service Mesh Integration

Service mesh provides service-to-service communication, service discovery, load balancing, and other cross-cutting concerns.

### Istio Service Mesh:

```yaml
# Istio Service Configuration
apiVersion: v1
kind: Service
metadata:
  name: user-service
  labels:
    app: user-service
spec:
  ports:
  - port: 8080
    name: http
  selector:
    app: user-service
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
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
```

### Service Mesh Configuration:

```yaml
# Istio Virtual Service
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: user-service
spec:
  http:
  - match:
    - uri:
        prefix: /api/users
    route:
    - destination:
        host: user-service
        port:
          number: 8080
    timeout: 30s
    retries:
      attempts: 3
      perTryTimeout: 10s
```

## 4.8 DNS-Based Service Discovery

DNS-based service discovery uses DNS records to locate services, providing a simple and standard approach.

### DNS Service Discovery:

```java
// DNS Service Discovery
@Component
public class DnsServiceDiscovery {
    @Autowired
    private DnsResolver dnsResolver;
    
    public List<ServiceInstance> discoverServices(String serviceName) {
        try {
            InetAddress[] addresses = InetAddress.getAllByName(serviceName);
            
            return Arrays.stream(addresses)
                .map(address -> ServiceInstance.builder()
                    .serviceId(serviceName + "-" + address.getHostAddress())
                    .serviceName(serviceName)
                    .host(address.getHostAddress())
                    .port(8080) // Default port
                    .build())
                .collect(Collectors.toList());
        } catch (UnknownHostException e) {
            log.error("Failed to resolve service: {}", serviceName, e);
            return Collections.emptyList();
        }
    }
}

// DNS Resolver
@Component
public class DnsResolver {
    public InetAddress[] resolve(String hostname) throws UnknownHostException {
        return InetAddress.getAllByName(hostname);
    }
}
```

### Consul DNS Integration:

```java
// Consul DNS Service Discovery
@Component
public class ConsulDnsServiceDiscovery {
    @Autowired
    private ConsulClient consulClient;
    
    public List<ServiceInstance> discoverServices(String serviceName) {
        try {
            Response<List<HealthService>> response = consulClient.getHealthServices(
                serviceName, true, QueryParams.DEFAULT);
            
            return response.getValue().stream()
                .map(healthService -> {
                    HealthService.Service service = healthService.getService();
                    return ServiceInstance.builder()
                        .serviceId(service.getId())
                        .serviceName(service.getService())
                        .host(service.getAddress())
                        .port(service.getPort())
                        .build();
                })
                .collect(Collectors.toList());
        } catch (Exception e) {
            log.error("Failed to discover services: {}", serviceName, e);
            return Collections.emptyList();
        }
    }
}
```

This comprehensive guide covers all aspects of service discovery and registration in microservices, providing both theoretical understanding and practical implementation examples. Each concept is explained with real-world scenarios and Java code examples to make the concepts clear and actionable.