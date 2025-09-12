# Section 9 – Monitoring & Observability

## 9.1 Distributed Tracing

Distributed tracing tracks requests as they flow through multiple microservices, providing visibility into the entire request path and performance bottlenecks.

### OpenTelemetry Implementation:

```java
// OpenTelemetry Configuration
@Configuration
public class TracingConfig {
    @Bean
    public Tracer tracer() {
        return OpenTelemetry.getGlobalTracer("user-service");
    }
    
    @Bean
    public SdkTracerProvider sdkTracerProvider() {
        return SdkTracerProvider.builder()
            .addSpanProcessor(BatchSpanProcessor.builder(
                OtlpGrpcSpanExporter.builder()
                    .setEndpoint("http://jaeger:14250")
                    .build())
                .build())
            .setResource(Resource.getDefault()
                .merge(Resource.create(Attributes.of(
                    ResourceAttributes.SERVICE_NAME, "user-service",
                    ResourceAttributes.SERVICE_VERSION, "1.0.0"))))
            .build();
    }
}

// Tracing Service
@Service
public class TracingService {
    @Autowired
    private Tracer tracer;
    
    public <T> T trace(String operationName, Supplier<T> operation) {
        Span span = tracer.spanBuilder(operationName).startSpan();
        try (Scope scope = span.makeCurrent()) {
            return operation.get();
        } catch (Exception e) {
            span.recordException(e);
            span.setStatus(StatusCode.ERROR, e.getMessage());
            throw e;
        } finally {
            span.end();
        }
    }
    
    public void addSpanAttribute(String key, String value) {
        Span.current().setAttribute(key, value);
    }
    
    public void addSpanEvent(String eventName, Map<String, String> attributes) {
        Span.current().addEvent(eventName, Attributes.of(
            attributes.entrySet().stream()
                .map(entry -> AttributeKey.stringKey(entry.getKey()), entry -> entry.getValue())
                .toArray(AttributeKeyValue[]::new)
        ));
    }
}

// Traced Service
@Service
public class UserService {
    @Autowired
    private TracingService tracingService;
    @Autowired
    private UserRepository userRepository;
    
    public User getUser(Long id) {
        return tracingService.trace("getUser", () -> {
            tracingService.addSpanAttribute("user.id", id.toString());
            
            User user = userRepository.findById(id);
            if (user == null) {
                tracingService.addSpanEvent("user.not.found", Map.of("user.id", id.toString()));
                throw new UserNotFoundException("User not found: " + id);
            }
            
            tracingService.addSpanEvent("user.found", Map.of("user.id", id.toString()));
            return user;
        });
    }
    
    public User createUser(UserRequest request) {
        return tracingService.trace("createUser", () -> {
            tracingService.addSpanAttribute("user.email", request.getEmail());
            
            User user = new User(request);
            User savedUser = userRepository.save(user);
            
            tracingService.addSpanEvent("user.created", Map.of(
                "user.id", savedUser.getId().toString(),
                "user.email", savedUser.getEmail()
            ));
            
            return savedUser;
        });
    }
}
```

### Zipkin Integration:

```java
// Zipkin Configuration
@Configuration
public class ZipkinConfig {
    @Bean
    public Sender sender() {
        return OkHttpSender.create("http://zipkin:9411/api/v2/spans");
    }
    
    @Bean
    public AsyncReporter<Span> spanReporter() {
        return AsyncReporter.create(sender());
    }
    
    @Bean
    public Tracing tracing() {
        return Tracing.newBuilder()
            .localServiceName("user-service")
            .spanReporter(spanReporter())
            .sampler(Sampler.create(1.0f))
            .build();
    }
}

// Zipkin Traced Service
@Service
public class OrderService {
    @Autowired
    private Tracing tracing;
    @Autowired
    private UserServiceClient userServiceClient;
    
    public Order createOrder(OrderRequest request) {
        Tracer tracer = tracing.tracer();
        Span span = tracer.nextSpan()
            .name("createOrder")
            .tag("order.userId", request.getUserId().toString())
            .start();
        
        try (Tracer.SpanInScope ws = tracer.withSpanInScope(span)) {
            // Get user information
            User user = userServiceClient.getUser(request.getUserId());
            
            // Create order
            Order order = new Order(request, user);
            
            span.tag("order.id", order.getId().toString());
            span.tag("order.total", order.getTotalAmount().toString());
            
            return order;
        } finally {
            span.end();
        }
    }
}
```

## 9.2 Centralized Logging

Centralized logging aggregates logs from all microservices into a single location for analysis and monitoring.

### ELK Stack Integration:

```java
// Logback Configuration
@Configuration
public class LoggingConfig {
    @Bean
    public LoggerContext loggerContext() {
        LoggerContext context = (LoggerContext) LoggerFactory.getILoggerFactory();
        
        // Configure console appender
        ConsoleAppender<ILoggingEvent> consoleAppender = new ConsoleAppender<>();
        consoleAppender.setContext(context);
        consoleAppender.setName("CONSOLE");
        consoleAppender.setEncoder(new PatternLayoutEncoder());
        consoleAppender.start();
        
        // Configure file appender
        RollingFileAppender<ILoggingEvent> fileAppender = new RollingFileAppender<>();
        fileAppender.setContext(context);
        fileAppender.setName("FILE");
        fileAppender.setFile("logs/user-service.log");
        fileAppender.setEncoder(new PatternLayoutEncoder());
        fileAppender.setRollingPolicy(new TimeBasedRollingPolicy());
        fileAppender.start();
        
        // Configure root logger
        Logger rootLogger = context.getLogger(Logger.ROOT_LOGGER_NAME);
        rootLogger.addAppender(consoleAppender);
        rootLogger.addAppender(fileAppender);
        
        return context;
    }
}

// Structured Logging Service
@Service
public class StructuredLoggingService {
    private static final Logger logger = LoggerFactory.getLogger(StructuredLoggingService.class);
    
    public void logUserAction(String action, Long userId, Map<String, Object> context) {
        Map<String, Object> logData = new HashMap<>();
        logData.put("timestamp", Instant.now().toString());
        logData.put("service", "user-service");
        logData.put("action", action);
        logData.put("userId", userId);
        logData.putAll(context);
        
        logger.info("User action: {}", logData);
    }
    
    public void logError(String error, Exception exception, Map<String, Object> context) {
        Map<String, Object> logData = new HashMap<>();
        logData.put("timestamp", Instant.now().toString());
        logData.put("service", "user-service");
        logData.put("error", error);
        logData.put("exception", exception.getMessage());
        logData.put("stackTrace", getStackTrace(exception));
        logData.putAll(context);
        
        logger.error("Error occurred: {}", logData);
    }
    
    private String getStackTrace(Exception exception) {
        StringWriter sw = new StringWriter();
        PrintWriter pw = new PrintWriter(sw);
        exception.printStackTrace(pw);
        return sw.toString();
    }
}

// Logging Controller
@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private StructuredLoggingService loggingService;
    @Autowired
    private UserService userService;
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        try {
            User user = userService.getUser(id);
            
            loggingService.logUserAction("GET_USER", id, Map.of(
                "success", true,
                "userEmail", user.getEmail()
            ));
            
            return ResponseEntity.ok(user);
        } catch (UserNotFoundException e) {
            loggingService.logError("User not found", e, Map.of(
                "userId", id,
                "action", "GET_USER"
            ));
            
            return ResponseEntity.notFound().build();
        } catch (Exception e) {
            loggingService.logError("Unexpected error", e, Map.of(
                "userId", id,
                "action", "GET_USER"
            ));
            
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}
```

### Fluentd Integration:

```java
// Fluentd Configuration
@Configuration
public class FluentdConfig {
    @Bean
    public FluentdAppender fluentdAppender() {
        FluentdAppender appender = new FluentdAppender();
        appender.setRemoteHost("fluentd");
        appender.setRemotePort(24224);
        appender.setTag("user-service");
        appender.setLabel("app");
        appender.start();
        return appender;
    }
}

// Fluentd Logging Service
@Service
public class FluentdLoggingService {
    private static final Logger logger = LoggerFactory.getLogger(FluentdLoggingService.class);
    
    public void logBusinessEvent(String eventType, Map<String, Object> data) {
        Map<String, Object> logData = new HashMap<>();
        logData.put("eventType", eventType);
        logData.put("timestamp", Instant.now().toString());
        logData.put("service", "user-service");
        logData.putAll(data);
        
        logger.info("Business event: {}", logData);
    }
    
    public void logPerformanceMetric(String metricName, double value, Map<String, String> tags) {
        Map<String, Object> logData = new HashMap<>();
        logData.put("metricName", metricName);
        logData.put("value", value);
        logData.put("timestamp", Instant.now().toString());
        logData.put("service", "user-service");
        logData.putAll(tags);
        
        logger.info("Performance metric: {}", logData);
    }
}
```

## 9.3 Metrics Collection and Analysis

Metrics collection provides quantitative data about system performance and behavior.

### Micrometer Integration:

```java
// Micrometer Configuration
@Configuration
public class MetricsConfig {
    @Bean
    public MeterRegistry meterRegistry() {
        return new PrometheusMeterRegistry(PrometheusConfig.DEFAULT);
    }
    
    @Bean
    public TimedAspect timedAspect(MeterRegistry meterRegistry) {
        return new TimedAspect(meterRegistry);
    }
    
    @Bean
    public CountedAspect countedAspect(MeterRegistry meterRegistry) {
        return new CountedAspect(meterRegistry);
    }
}

// Metrics Service
@Service
public class MetricsService {
    private final MeterRegistry meterRegistry;
    private final Counter userCreatedCounter;
    private final Counter userUpdatedCounter;
    private final Counter userDeletedCounter;
    private final Timer userServiceTimer;
    private final Gauge activeUsersGauge;
    
    public MetricsService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.userCreatedCounter = Counter.builder("user.created")
            .description("Number of users created")
            .register(meterRegistry);
        this.userUpdatedCounter = Counter.builder("user.updated")
            .description("Number of users updated")
            .register(meterRegistry);
        this.userDeletedCounter = Counter.builder("user.deleted")
            .description("Number of users deleted")
            .register(meterRegistry);
        this.userServiceTimer = Timer.builder("user.service.duration")
            .description("User service operation duration")
            .register(meterRegistry);
        this.activeUsersGauge = Gauge.builder("user.active")
            .description("Number of active users")
            .register(meterRegistry, this, MetricsService::getActiveUsersCount);
    }
    
    public void incrementUserCreated() {
        userCreatedCounter.increment();
    }
    
    public void incrementUserUpdated() {
        userUpdatedCounter.increment();
    }
    
    public void incrementUserDeleted() {
        userDeletedCounter.increment();
    }
    
    public Timer.Sample startTimer() {
        return Timer.start(meterRegistry);
    }
    
    public void recordTimer(Timer.Sample sample) {
        sample.stop(userServiceTimer);
    }
    
    public void recordCustomMetric(String name, double value, String... tags) {
        Gauge.builder(name)
            .description("Custom metric")
            .tags(tags)
            .register(meterRegistry, () -> value);
    }
    
    private double getActiveUsersCount() {
        // Return actual active users count
        return 1000; // This would be calculated from actual data
    }
}

// Metrics Controller
@RestController
@RequestMapping("/api/metrics")
public class MetricsController {
    @Autowired
    private MeterRegistry meterRegistry;
    
    @GetMapping(produces = "text/plain")
    public String metrics() {
        return ((PrometheusMeterRegistry) meterRegistry).scrape();
    }
}
```

### Custom Metrics:

```java
// Custom Metrics Service
@Service
public class CustomMetricsService {
    private final MeterRegistry meterRegistry;
    private final Counter businessEventCounter;
    private final Timer businessOperationTimer;
    private final DistributionSummary businessDataSummary;
    
    public CustomMetricsService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.businessEventCounter = Counter.builder("business.events")
            .description("Number of business events")
            .tag("service", "user-service")
            .register(meterRegistry);
        this.businessOperationTimer = Timer.builder("business.operations")
            .description("Business operation duration")
            .tag("service", "user-service")
            .register(meterRegistry);
        this.businessDataSummary = DistributionSummary.builder("business.data.size")
            .description("Business data size distribution")
            .tag("service", "user-service")
            .register(meterRegistry);
    }
    
    public void recordBusinessEvent(String eventType, String status) {
        businessEventCounter.increment(
            Tags.of(
                "eventType", eventType,
                "status", status
            )
        );
    }
    
    public void recordBusinessOperation(String operation, Runnable operationCode) {
        Timer.Sample sample = Timer.start(meterRegistry);
        try {
            operationCode.run();
        } finally {
            sample.stop(Timer.builder("business.operations")
                .tag("operation", operation)
                .register(meterRegistry));
        }
    }
    
    public void recordDataSize(String dataType, int size) {
        businessDataSummary.record(size, Tags.of("dataType", dataType));
    }
}
```

## 9.4 Health Checks and Readiness Probes

Health checks ensure that services are running and ready to handle requests.

### Spring Boot Actuator Health Checks:

```java
// Health Check Configuration
@Configuration
public class HealthCheckConfig {
    @Bean
    public HealthIndicator databaseHealthIndicator() {
        return new DatabaseHealthIndicator();
    }
    
    @Bean
    public HealthIndicator externalServiceHealthIndicator() {
        return new ExternalServiceHealthIndicator();
    }
    
    @Bean
    public HealthIndicator customHealthIndicator() {
        return new CustomHealthIndicator();
    }
}

// Database Health Indicator
@Component
public class DatabaseHealthIndicator implements HealthIndicator {
    @Autowired
    private UserRepository userRepository;
    
    @Override
    public Health health() {
        try {
            // Check database connectivity
            userRepository.count();
            
            return Health.up()
                .withDetail("database", "Available")
                .withDetail("responseTime", "10ms")
                .withDetail("timestamp", Instant.now().toString())
                .build();
        } catch (Exception e) {
            return Health.down()
                .withDetail("database", "Unavailable")
                .withDetail("error", e.getMessage())
                .withDetail("timestamp", Instant.now().toString())
                .build();
        }
    }
}

// External Service Health Indicator
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
                    .withDetail("status", response.getStatusCode().toString())
                    .build();
            } else {
                return Health.down()
                    .withDetail("external-service", "Unavailable")
                    .withDetail("status", response.getStatusCode().toString())
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

// Custom Health Indicator
@Component
public class CustomHealthIndicator implements HealthIndicator {
    @Autowired
    private UserService userService;
    
    @Override
    public Health health() {
        try {
            // Check business logic health
            boolean isHealthy = userService.isHealthy();
            
            if (isHealthy) {
                return Health.up()
                    .withDetail("business-logic", "Healthy")
                    .withDetail("timestamp", Instant.now().toString())
                    .build();
            } else {
                return Health.down()
                    .withDetail("business-logic", "Unhealthy")
                    .withDetail("timestamp", Instant.now().toString())
                    .build();
            }
        } catch (Exception e) {
            return Health.down()
                .withDetail("business-logic", "Error")
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
```

### Kubernetes Health Checks:

```yaml
# Kubernetes Health Check Configuration
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
        livenessProbe:
          httpGet:
            path: /actuator/health/liveness
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /actuator/health/startup
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 30
```

## 9.5 Alerting and Incident Response

Alerting and incident response ensure that issues are detected and resolved quickly.

### Alerting Service:

```java
// Alerting Service
@Service
public class AlertingService {
    @Autowired
    private AlertRepository alertRepository;
    @Autowired
    private NotificationService notificationService;
    
    public void createAlert(AlertType type, String message, Map<String, Object> context) {
        Alert alert = Alert.builder()
            .type(type)
            .message(message)
            .context(context)
            .timestamp(Instant.now())
            .status(AlertStatus.ACTIVE)
            .build();
        
        alertRepository.save(alert);
        
        // Send notification
        notificationService.sendAlert(alert);
    }
    
    public void resolveAlert(Long alertId, String resolution) {
        Alert alert = alertRepository.findById(alertId)
            .orElseThrow(() -> new AlertNotFoundException("Alert not found: " + alertId));
        
        alert.setStatus(AlertStatus.RESOLVED);
        alert.setResolution(resolution);
        alert.setResolvedAt(Instant.now());
        
        alertRepository.save(alert);
    }
    
    public List<Alert> getActiveAlerts() {
        return alertRepository.findByStatus(AlertStatus.ACTIVE);
    }
}

// Alert Rules Engine
@Component
public class AlertRulesEngine {
    @Autowired
    private AlertingService alertingService;
    @Autowired
    private MetricsService metricsService;
    
    @Scheduled(fixedRate = 60000) // Check every minute
    public void checkAlertRules() {
        // Check error rate
        checkErrorRate();
        
        // Check response time
        checkResponseTime();
        
        // Check memory usage
        checkMemoryUsage();
        
        // Check disk usage
        checkDiskUsage();
    }
    
    private void checkErrorRate() {
        double errorRate = metricsService.getErrorRate();
        if (errorRate > 0.05) { // 5% error rate threshold
            alertingService.createAlert(
                AlertType.ERROR_RATE_HIGH,
                "Error rate is above threshold: " + errorRate,
                Map.of("errorRate", errorRate, "threshold", 0.05)
            );
        }
    }
    
    private void checkResponseTime() {
        double avgResponseTime = metricsService.getAverageResponseTime();
        if (avgResponseTime > 2000) { // 2 second threshold
            alertingService.createAlert(
                AlertType.RESPONSE_TIME_HIGH,
                "Average response time is above threshold: " + avgResponseTime + "ms",
                Map.of("avgResponseTime", avgResponseTime, "threshold", 2000)
            );
        }
    }
    
    private void checkMemoryUsage() {
        double memoryUsage = metricsService.getMemoryUsage();
        if (memoryUsage > 0.8) { // 80% memory usage threshold
            alertingService.createAlert(
                AlertType.MEMORY_USAGE_HIGH,
                "Memory usage is above threshold: " + (memoryUsage * 100) + "%",
                Map.of("memoryUsage", memoryUsage, "threshold", 0.8)
            );
        }
    }
    
    private void checkDiskUsage() {
        double diskUsage = metricsService.getDiskUsage();
        if (diskUsage > 0.9) { // 90% disk usage threshold
            alertingService.createAlert(
                AlertType.DISK_USAGE_HIGH,
                "Disk usage is above threshold: " + (diskUsage * 100) + "%",
                Map.of("diskUsage", diskUsage, "threshold", 0.9)
            );
        }
    }
}
```

### Incident Response Service:

```java
// Incident Response Service
@Service
public class IncidentResponseService {
    @Autowired
    private IncidentRepository incidentRepository;
    @Autowired
    private NotificationService notificationService;
    @Autowired
    private EscalationService escalationService;
    
    public Incident createIncident(Alert alert) {
        Incident incident = Incident.builder()
            .title(alert.getMessage())
            .description(alert.getMessage())
            .severity(determineSeverity(alert))
            .status(IncidentStatus.OPEN)
            .createdAt(Instant.now())
            .alertId(alert.getId())
            .build();
        
        incidentRepository.save(incident);
        
        // Notify on-call team
        notificationService.notifyOnCallTeam(incident);
        
        // Start escalation timer
        escalationService.startEscalationTimer(incident);
        
        return incident;
    }
    
    public void updateIncidentStatus(Long incidentId, IncidentStatus status, String comment) {
        Incident incident = incidentRepository.findById(incidentId)
            .orElseThrow(() -> new IncidentNotFoundException("Incident not found: " + incidentId));
        
        incident.setStatus(status);
        incident.setUpdatedAt(Instant.now());
        
        if (comment != null) {
            incident.addComment(comment);
        }
        
        incidentRepository.save(incident);
        
        // Notify stakeholders
        notificationService.notifyIncidentUpdate(incident);
    }
    
    private IncidentSeverity determineSeverity(Alert alert) {
        switch (alert.getType()) {
            case ERROR_RATE_HIGH:
            case RESPONSE_TIME_HIGH:
                return IncidentSeverity.HIGH;
            case MEMORY_USAGE_HIGH:
            case DISK_USAGE_HIGH:
                return IncidentSeverity.MEDIUM;
            default:
                return IncidentSeverity.LOW;
        }
    }
}
```

## 9.6 Performance Monitoring

Performance monitoring tracks system performance metrics and identifies bottlenecks.

### Performance Metrics Service:

```java
// Performance Metrics Service
@Service
public class PerformanceMetricsService {
    private final MeterRegistry meterRegistry;
    private final Timer requestTimer;
    private final Counter requestCounter;
    private final Gauge activeConnectionsGauge;
    
    public PerformanceMetricsService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.requestTimer = Timer.builder("http.requests")
            .description("HTTP request duration")
            .register(meterRegistry);
        this.requestCounter = Counter.builder("http.requests")
            .description("HTTP request count")
            .register(meterRegistry);
        this.activeConnectionsGauge = Gauge.builder("http.active.connections")
            .description("Active HTTP connections")
            .register(meterRegistry, this, PerformanceMetricsService::getActiveConnections);
    }
    
    public void recordRequest(String method, String path, int statusCode, long duration) {
        requestTimer.record(duration, TimeUnit.MILLISECONDS);
        requestCounter.increment(
            Tags.of(
                "method", method,
                "path", path,
                "status", String.valueOf(statusCode)
            )
        );
    }
    
    public void recordDatabaseOperation(String operation, long duration) {
        Timer.builder("database.operations")
            .description("Database operation duration")
            .tag("operation", operation)
            .register(meterRegistry)
            .record(duration, TimeUnit.MILLISECONDS);
    }
    
    public void recordCacheOperation(String operation, boolean hit) {
        Counter.builder("cache.operations")
            .description("Cache operation count")
            .tag("operation", operation)
            .tag("hit", String.valueOf(hit))
            .register(meterRegistry)
            .increment();
    }
    
    private double getActiveConnections() {
        // Return actual active connections count
        return 50; // This would be calculated from actual data
    }
}

// Performance Monitoring Filter
@Component
public class PerformanceMonitoringFilter implements Filter {
    @Autowired
    private PerformanceMetricsService performanceMetricsService;
    
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) 
            throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        long startTime = System.currentTimeMillis();
        
        try {
            chain.doFilter(request, response);
        } finally {
            long duration = System.currentTimeMillis() - startTime;
            
            performanceMetricsService.recordRequest(
                httpRequest.getMethod(),
                httpRequest.getRequestURI(),
                httpResponse.getStatus(),
                duration
            );
        }
    }
}
```

## 9.7 Business Metrics and KPIs

Business metrics track key performance indicators that are important to the business.

### Business Metrics Service:

```java
// Business Metrics Service
@Service
public class BusinessMetricsService {
    private final MeterRegistry meterRegistry;
    private final Counter userRegistrationCounter;
    private final Counter userLoginCounter;
    private final Counter orderCreationCounter;
    private final Gauge activeUsersGauge;
    
    public BusinessMetricsService(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.userRegistrationCounter = Counter.builder("business.user.registrations")
            .description("Number of user registrations")
            .register(meterRegistry);
        this.userLoginCounter = Counter.builder("business.user.logins")
            .description("Number of user logins")
            .register(meterRegistry);
        this.orderCreationCounter = Counter.builder("business.orders.created")
            .description("Number of orders created")
            .register(meterRegistry);
        this.activeUsersGauge = Gauge.builder("business.users.active")
            .description("Number of active users")
            .register(meterRegistry, this, BusinessMetricsService::getActiveUsersCount);
    }
    
    public void recordUserRegistration(String source) {
        userRegistrationCounter.increment(
            Tags.of("source", source)
        );
    }
    
    public void recordUserLogin(String userId, String method) {
        userLoginCounter.increment(
            Tags.of(
                "method", method,
                "userType", getUserType(userId)
            )
        );
    }
    
    public void recordOrderCreation(String userId, BigDecimal amount) {
        orderCreationCounter.increment(
            Tags.of(
                "userType", getUserType(userId),
                "amountRange", getAmountRange(amount)
            )
        );
    }
    
    public void recordBusinessEvent(String eventType, Map<String, String> tags) {
        Counter.builder("business.events")
            .description("Business events")
            .tag("eventType", eventType)
            .tags(tags)
            .register(meterRegistry)
            .increment();
    }
    
    private String getUserType(String userId) {
        // Determine user type based on user ID
        return "premium"; // This would be calculated from actual data
    }
    
    private String getAmountRange(BigDecimal amount) {
        if (amount.compareTo(new BigDecimal("100")) < 0) {
            return "low";
        } else if (amount.compareTo(new BigDecimal("500")) < 0) {
            return "medium";
        } else {
            return "high";
        }
    }
    
    private double getActiveUsersCount() {
        // Return actual active users count
        return 1000; // This would be calculated from actual data
    }
}
```

## 9.8 Observability Tools and Platforms

Observability tools provide comprehensive monitoring, logging, and tracing capabilities.

### Prometheus Integration:

```java
// Prometheus Configuration
@Configuration
public class PrometheusConfig {
    @Bean
    public PrometheusMeterRegistry prometheusMeterRegistry() {
        return new PrometheusMeterRegistry(PrometheusConfig.DEFAULT);
    }
    
    @Bean
    public PrometheusScrapeEndpoint prometheusScrapeEndpoint() {
        return new PrometheusScrapeEndpoint(prometheusMeterRegistry());
    }
}

// Prometheus Metrics Controller
@RestController
@RequestMapping("/actuator/prometheus")
public class PrometheusController {
    @Autowired
    private PrometheusMeterRegistry prometheusMeterRegistry;
    
    @GetMapping(produces = "text/plain")
    public String metrics() {
        return prometheusMeterRegistry.scrape();
    }
}
```

### Grafana Dashboard Configuration:

```json
{
  "dashboard": {
    "title": "Microservices Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{path}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "5xx errors"
          }
        ]
      }
    ]
  }
}
```

This comprehensive guide covers all aspects of monitoring and observability in microservices, providing both theoretical understanding and practical implementation examples. Each concept is explained with real-world scenarios and Java code examples to make the concepts clear and actionable.