# Section 19 - Cloud & DevOps Integration

## 19.1 Containerization with Docker

Docker is a platform that enables developers to package applications and their dependencies into lightweight, portable containers.

### Core Concepts:

**1. Container Fundamentals:**
- Lightweight virtualization
- Process isolation
- Resource efficiency
- Portability across environments

**2. Docker Components:**
- Dockerfile (build instructions)
- Images (read-only templates)
- Containers (running instances)
- Docker Hub (registry)

**3. Benefits:**
- Consistent environments
- Easy deployment
- Scalability
- Resource optimization

### Example:

```dockerfile
# Dockerfile for Java Spring Boot Application
FROM openjdk:17-jdk-slim

WORKDIR /app

# Copy Maven files
COPY pom.xml .
COPY src ./src

# Install Maven and build application
RUN apt-get update && apt-get install -y maven
RUN mvn clean package -DskipTests

# Expose port
EXPOSE 8080

# Run application
CMD ["java", "-jar", "target/myapp.jar"]
```

```java
// Docker-compatible Spring Boot Application
@SpringBootApplication
public class CloudApplication {
    public static void main(String[] args) {
        SpringApplication.run(CloudApplication.class, args);
    }
}

@RestController
public class HealthController {
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        Map<String, String> status = new HashMap<>();
        status.put("status", "UP");
        status.put("timestamp", LocalDateTime.now().toString());
        return ResponseEntity.ok(status);
    }
}
```

### Real-world Analogy:
Docker containers are like shipping containers for software - standardized, portable, and can run anywhere.

## 19.2 Kubernetes for Java Applications

Kubernetes is an orchestration platform that manages containerized applications at scale.

### Core Concepts:

**1. Kubernetes Objects:**
- Pods (smallest deployable units)
- Services (network access)
- Deployments (replica management)
- ConfigMaps (configuration)

**2. Key Features:**
- Auto-scaling
- Load balancing
- Rolling updates
- Health checks

### Example:

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: java-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: java-app
  template:
    metadata:
      labels:
        app: java-app
    spec:
      containers:
      - name: java-app
        image: myapp:latest
        ports:
        - containerPort: 8080
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "production"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

```java
// Kubernetes-aware Spring Boot Application
@SpringBootApplication
public class KubernetesApp {
    public static void main(String[] args) {
        SpringApplication.run(KubernetesApp.class, args);
    }
}

@RestController
public class K8sController {
    @Value("${HOSTNAME:unknown}")
    private String hostname;
    
    @GetMapping("/info")
    public Map<String, String> info() {
        Map<String, String> info = new HashMap<>();
        info.put("hostname", hostname);
        info.put("timestamp", LocalDateTime.now().toString());
        return info;
    }
}
```

### Real-world Analogy:
Kubernetes is like a smart traffic management system that automatically routes traffic, scales services, and ensures everything runs smoothly.

## 19.3 Cloud-Native Development

Cloud-native development focuses on building applications designed to run in cloud environments.

### Core Concepts:

**1. Twelve-Factor App:**
- Codebase
- Dependencies
- Config
- Backing services
- Build, release, run
- Processes
- Port binding
- Concurrency
- Disposability
- Dev/prod parity
- Logs
- Admin processes

**2. Microservices Patterns:**
- Service discovery
- Circuit breakers
- Bulkhead isolation
- Timeout patterns

### Example:

```java
// Cloud-native Spring Boot Application
@SpringBootApplication
@EnableDiscoveryClient
@EnableCircuitBreaker
public class CloudNativeApp {
    public static void main(String[] args) {
        SpringApplication.run(CloudNativeApp.class, args);
    }
}

@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private RestTemplate restTemplate;
    
    @HystrixCommand(fallbackMethod = "getUserFallback")
    public User getUserWithProfile(Long userId) {
        User user = userRepository.findById(userId);
        Profile profile = restTemplate.getForObject(
            "http://profile-service/users/" + userId, Profile.class);
        user.setProfile(profile);
        return user;
    }
    
    public User getUserFallback(Long userId) {
        User user = userRepository.findById(userId);
        user.setProfile(new Profile("Default", "Profile"));
        return user;
    }
}
```

### Real-world Analogy:
Cloud-native development is like designing a city with modular, interconnected districts that can grow and adapt independently.

## 19.4 CI/CD Pipelines

Continuous Integration and Continuous Deployment automate the software delivery process.

### Core Concepts:

**1. CI/CD Pipeline Stages:**
- Source code management
- Build automation
- Testing
- Deployment
- Monitoring

**2. Popular Tools:**
- Jenkins
- GitLab CI
- GitHub Actions
- Azure DevOps

### Example:

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up JDK 17
      uses: actions/setup-java@v2
      with:
        java-version: '17'
        distribution: 'temurin'
    - name: Run tests
      run: mvn test
    - name: Generate test report
      uses: dorny/test-reporter@v1
      if: success() || failure()
      with:
        name: Maven Tests
        path: target/surefire-reports/*.xml
        reporter: java-junit

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up JDK 17
      uses: actions/setup-java@v2
      with:
        java-version: '17'
        distribution: 'temurin'
    - name: Build with Maven
      run: mvn clean package
    - name: Build Docker image
      run: docker build -t myapp:${{ github.sha }} .
    - name: Push to registry
      run: docker push myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to production
      run: kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
```

### Real-world Analogy:
CI/CD pipelines are like an automated assembly line that builds, tests, and ships products without human intervention.

## 19.5 Infrastructure as Code

Infrastructure as Code (IaC) manages and provisions infrastructure through code.

### Core Concepts:

**1. IaC Benefits:**
- Version control
- Reproducibility
- Automation
- Consistency

**2. Popular Tools:**
- Terraform
- Ansible
- CloudFormation
- Pulumi

### Example:

```hcl
# main.tf
provider "aws" {
  region = "us-west-2"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "java-app-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  
  tags = {
    Name = "java-app-public-subnet"
  }
}

resource "aws_eks_cluster" "java_app" {
  name     = "java-app-cluster"
  role_arn = aws_iam_role.eks_cluster.arn
  
  vpc_config {
    subnet_ids = [aws_subnet.public.id]
  }
}
```

### Real-world Analogy:
Infrastructure as Code is like having blueprints for a building that can be automatically constructed and modified.

## 19.6 Monitoring & Observability

Monitoring and observability ensure applications run smoothly in production.

### Core Concepts:

**1. Three Pillars of Observability:**
- Metrics (quantitative data)
- Logs (event records)
- Traces (request flows)

**2. Monitoring Tools:**
- Prometheus (metrics)
- Grafana (visualization)
- ELK Stack (logs)
- Jaeger (tracing)

### Example:

```java
// Micrometer metrics
@Component
public class MetricsService {
    
    private final MeterRegistry meterRegistry;
    private final Counter requestCounter;
    private final Timer requestTimer;
    
    public MetricsService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.requestCounter = Counter.builder("http_requests_total")
            .description("Total HTTP requests")
            .register(meterRegistry);
        this.requestTimer = Timer.builder("http_request_duration")
            .description("HTTP request duration")
            .register(meterRegistry);
    }
    
    public void recordRequest(String endpoint) {
        requestCounter.increment(Tags.of("endpoint", endpoint));
    }
    
    public Timer.Sample startTimer() {
        return Timer.start(meterRegistry);
    }
    
    public void recordTimer(Timer.Sample sample, String endpoint) {
        sample.stop(Timer.builder("http_request_duration")
            .tag("endpoint", endpoint)
            .register(meterRegistry));
    }
}

// Distributed tracing
@RestController
public class TracedController {
    
    @Autowired
    private Tracer tracer;
    
    @GetMapping("/api/users/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        Span span = tracer.nextSpan()
            .name("get-user")
            .tag("user.id", id.toString())
            .start();
        
        try (Tracer.SpanInScope ws = tracer.withSpanInScope(span)) {
            User user = userService.findById(id);
            return ResponseEntity.ok(user);
        } finally {
            span.end();
        }
    }
}
```

### Real-world Analogy:
Monitoring and observability are like having a comprehensive dashboard in a car that shows speed, fuel, engine status, and navigation.

## 19.7 Serverless Java

Serverless computing allows running Java applications without managing servers.

### Core Concepts:

**1. Serverless Benefits:**
- No server management
- Automatic scaling
- Pay-per-use pricing
- Event-driven execution

**2. Serverless Platforms:**
- AWS Lambda
- Azure Functions
- Google Cloud Functions
- Spring Cloud Function

### Example:

```java
// AWS Lambda Function
public class UserHandler implements RequestHandler<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent> {
    
    @Override
    public APIGatewayProxyResponseEvent handleRequest(APIGatewayProxyRequestEvent input, Context context) {
        String userId = input.getPathParameters().get("userId");
        
        User user = userService.findById(Long.parseLong(userId));
        
        APIGatewayProxyResponseEvent response = new APIGatewayProxyResponseEvent();
        response.setStatusCode(200);
        response.setBody(JsonUtils.toJson(user));
        
        return response;
    }
}

// Spring Cloud Function
@SpringBootApplication
public class ServerlessApp {
    public static void main(String[] args) {
        SpringApplication.run(ServerlessApp.class, args);
    }
    
    @Bean
    public Function<String, String> uppercase() {
        return value -> value.toUpperCase();
    }
    
    @Bean
    public Function<User, String> createUser() {
        return user -> {
            User savedUser = userService.save(user);
            return "User created with ID: " + savedUser.getId();
        };
    }
}
```

### Real-world Analogy:
Serverless computing is like using a taxi service - you don't need to own or maintain a car, just call when you need it and pay for the ride.