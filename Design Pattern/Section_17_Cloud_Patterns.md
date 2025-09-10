# Section 17 - Cloud Patterns

## 17.1 Cloud-Native Patterns

Cloud-native patterns are architectural approaches designed specifically for cloud environments, leveraging cloud services and capabilities to build scalable, resilient applications.

### When to Use:
- When building applications specifically for cloud platforms
- When you need to leverage cloud-native services
- When you want to maximize cloud benefits

### Real-World Analogy:
Think of designing a house specifically for a particular climate. Instead of adapting a generic house design, you design it from the ground up to take advantage of the local weather patterns, materials, and energy sources.

### Basic Implementation:
```java
// Cloud-native configuration
@Configuration
@EnableConfigurationProperties(CloudConfig.class)
public class CloudNativeConfig {
    
    @Bean
    public CloudService cloudService(CloudConfig config) {
        return new CloudService(config);
    }
}

// Cloud service abstraction
public class CloudService {
    private CloudConfig config;
    private CloudStorage storage;
    private CloudDatabase database;
    private CloudMessaging messaging;
    
    public CloudService(CloudConfig config) {
        this.config = config;
        this.storage = new CloudStorage(config.getStorageConfig());
        this.database = new CloudDatabase(config.getDatabaseConfig());
        this.messaging = new CloudMessaging(config.getMessagingConfig());
    }
    
    public void deployApplication(Application app) {
        // Deploy to cloud platform
        storage.uploadApplication(app);
        database.initializeSchema(app.getSchema());
        messaging.setupQueues(app.getQueues());
    }
}
```

## 17.2 Serverless Patterns

Serverless patterns focus on building applications using serverless computing models where you don't manage servers directly.

### When to Use:
- When you have event-driven workloads
- When you want to pay only for actual usage
- When you need automatic scaling

### Real-World Analogy:
Think of a taxi service where you only pay for the ride you take. You don't need to own a car, maintain it, or pay for it when you're not using it. The service provider handles all the infrastructure.

### Basic Implementation:
```java
// Serverless function
@FunctionName("processOrder")
public class OrderProcessor {
    
    @EventHubTrigger(name = "trigger", eventHubName = "orders", 
                    connection = "EventHubConnectionString")
    public void processOrder(OrderEvent event, ExecutionContext context) {
        try {
            // Process order
            Order order = parseOrder(event);
            validateOrder(order);
            saveOrder(order);
            sendNotification(order);
            
            context.getLogger().info("Order processed: " + order.getId());
        } catch (Exception e) {
            context.getLogger().severe("Error processing order: " + e.getMessage());
            throw e;
        }
    }
}

// Serverless configuration
@Configuration
public class ServerlessConfig {
    
    @Bean
    public Function<OrderEvent, ProcessedOrder> orderProcessor() {
        return event -> {
            // Process order logic
            return new ProcessedOrder(event.getOrderId(), "PROCESSED");
        };
    }
}
```

## 17.3 Container Patterns

Container patterns involve packaging applications and their dependencies into lightweight, portable containers.

### When to Use:
- When you need consistent deployment across environments
- When you want to isolate applications
- When you need efficient resource utilization

### Real-World Analogy:
Think of shipping containers that can carry any type of cargo. They're standardized, portable, and can be moved between different ships, trucks, and cranes without modification.

### Basic Implementation:
```dockerfile
# Dockerfile
FROM openjdk:11-jre-slim

WORKDIR /app
COPY target/myapp.jar app.jar

EXPOSE 8080

ENV JAVA_OPTS="-Xmx512m -Xms256m"

ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

```java
// Container-aware application
@SpringBootApplication
public class ContainerizedApplication {
    
    @Value("${server.port:8080}")
    private int port;
    
    @Value("${spring.datasource.url}")
    private String databaseUrl;
    
    public static void main(String[] args) {
        SpringApplication.run(ContainerizedApplication.class, args);
    }
    
    @Bean
    public HealthIndicator containerHealthIndicator() {
        return new HealthIndicator() {
            @Override
            public Health health() {
                return Health.up()
                    .withDetail("port", port)
                    .withDetail("database", databaseUrl)
                    .build();
            }
        };
    }
}
```

## 17.4 Multi-Tenant Patterns

Multi-tenant patterns allow a single application instance to serve multiple customers (tenants) while keeping their data isolated.

### When to Use:
- When building SaaS applications
- When you need to serve multiple customers efficiently
- When you want to share resources while maintaining isolation

### Real-World Analogy:
Think of an apartment building where multiple families live in separate units but share common infrastructure like elevators, heating, and water systems. Each family has their own space, but they all benefit from shared resources.

### Basic Implementation:
```java
// Tenant context
public class TenantContext {
    private static final ThreadLocal<String> currentTenant = new ThreadLocal<>();
    
    public static void setCurrentTenant(String tenantId) {
        currentTenant.set(tenantId);
    }
    
    public static String getCurrentTenant() {
        return currentTenant.get();
    }
    
    public static void clear() {
        currentTenant.remove();
    }
}

// Multi-tenant service
@Service
public class MultiTenantService {
    
    @Autowired
    private TenantRepository tenantRepository;
    
    public List<Order> getOrders() {
        String tenantId = TenantContext.getCurrentTenant();
        return tenantRepository.findOrdersByTenant(tenantId);
    }
    
    public void createOrder(Order order) {
        String tenantId = TenantContext.getCurrentTenant();
        order.setTenantId(tenantId);
        tenantRepository.save(order);
    }
}

// Tenant-aware repository
@Repository
public class TenantRepository {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    public List<Order> findOrdersByTenant(String tenantId) {
        return entityManager.createQuery(
            "SELECT o FROM Order o WHERE o.tenantId = :tenantId", Order.class)
            .setParameter("tenantId", tenantId)
            .getResultList();
    }
}
```

## 17.5 Data Lake Patterns

Data lake patterns provide centralized storage for structured and unstructured data at any scale.

### When to Use:
- When you need to store large amounts of diverse data
- When you want to perform analytics on raw data
- When you need flexible data processing

### Real-World Analogy:
Think of a large warehouse where you can store any type of item - boxes, furniture, electronics, documents - without needing to organize them first. You can later sort and process them as needed.

### Basic Implementation:
```java
// Data lake service
@Service
public class DataLakeService {
    
    @Autowired
    private S3Client s3Client;
    
    private static final String DATA_LAKE_BUCKET = "my-data-lake";
    
    public void storeData(String key, Object data) {
        try {
            String jsonData = objectMapper.writeValueAsString(data);
            s3Client.putObject(PutObjectRequest.builder()
                .bucket(DATA_LAKE_BUCKET)
                .key(key)
                .build(), RequestBody.fromString(jsonData));
        } catch (Exception e) {
            throw new DataLakeException("Failed to store data", e);
        }
    }
    
    public <T> T retrieveData(String key, Class<T> type) {
        try {
            GetObjectResponse response = s3Client.getObject(GetObjectRequest.builder()
                .bucket(DATA_LAKE_BUCKET)
                .key(key)
                .build());
            
            return objectMapper.readValue(response, type);
        } catch (Exception e) {
            throw new DataLakeException("Failed to retrieve data", e);
        }
    }
}

// Data processing pipeline
@Component
public class DataProcessingPipeline {
    
    @Autowired
    private DataLakeService dataLakeService;
    
    @Scheduled(fixedRate = 60000) // Every minute
    public void processRawData() {
        // Get raw data from data lake
        List<RawData> rawData = dataLakeService.retrieveData("raw/", RawData.class);
        
        // Process and transform data
        List<ProcessedData> processedData = rawData.stream()
            .map(this::transformData)
            .collect(Collectors.toList());
        
        // Store processed data
        dataLakeService.storeData("processed/", processedData);
    }
    
    private ProcessedData transformData(RawData raw) {
        // Transformation logic
        return new ProcessedData(raw.getId(), raw.getValue() * 2);
    }
}
```

## 17.6 Edge Computing Patterns

Edge computing patterns bring computation and data storage closer to the location where it's needed.

### When to Use:
- When you need low latency processing
- When you have limited bandwidth
- When you need real-time decision making

### Real-World Analogy:
Think of a local branch office that can handle most customer requests without needing to contact the main headquarters. This reduces response time and saves on communication costs.

### Basic Implementation:
```java
// Edge computing service
@Service
public class EdgeComputingService {
    
    @Autowired
    private CloudService cloudService;
    
    @Autowired
    private LocalCache localCache;
    
    public ProcessingResult processData(DataRequest request) {
        // Try to process locally first
        if (canProcessLocally(request)) {
            return processLocally(request);
        }
        
        // Fall back to cloud processing
        return cloudService.processData(request);
    }
    
    private boolean canProcessLocally(DataRequest request) {
        return localCache.hasData(request.getDataId()) && 
               request.getPriority() == Priority.LOW;
    }
    
    private ProcessingResult processLocally(DataRequest request) {
        Data data = localCache.getData(request.getDataId());
        return new ProcessingResult(data.getValue() * 2);
    }
}

// Edge device manager
@Component
public class EdgeDeviceManager {
    
    private Map<String, EdgeDevice> devices = new HashMap<>();
    
    public void registerDevice(EdgeDevice device) {
        devices.put(device.getId(), device);
    }
    
    public void distributeWorkload(Workload workload) {
        EdgeDevice bestDevice = findBestDevice(workload);
        bestDevice.processWorkload(workload);
    }
    
    private EdgeDevice findBestDevice(Workload workload) {
        return devices.values().stream()
            .filter(device -> device.canHandle(workload))
            .min(Comparator.comparing(EdgeDevice::getLoad))
            .orElseThrow(() -> new NoSuitableDeviceException());
    }
}
```

## 17.7 Hybrid Cloud Patterns

Hybrid cloud patterns combine on-premises infrastructure with public cloud services.

### When to Use:
- When you need to maintain some data on-premises
- When you want to gradually migrate to cloud
- When you need to comply with data residency requirements

### Real-World Analogy:
Think of a company that has its main office downtown but also uses co-working spaces in different locations. They can work from either location depending on their needs, and they can move between them as required.

### Basic Implementation:
```java
// Hybrid cloud service
@Service
public class HybridCloudService {
    
    @Autowired
    private OnPremisesService onPremisesService;
    
    @Autowired
    private CloudService cloudService;
    
    public DataResult processData(DataRequest request) {
        if (shouldUseOnPremises(request)) {
            return onPremisesService.processData(request);
        } else {
            return cloudService.processData(request);
        }
    }
    
    private boolean shouldUseOnPremises(DataRequest request) {
        return request.isSensitive() || 
               request.getDataSize() < 1000 || 
               !cloudService.isAvailable();
    }
}

// Data synchronization service
@Component
public class DataSynchronizationService {
    
    @Scheduled(fixedRate = 300000) // Every 5 minutes
    public void synchronizeData() {
        // Sync data from on-premises to cloud
        List<Data> onPremisesData = onPremisesService.getNewData();
        cloudService.syncData(onPremisesData);
        
        // Sync data from cloud to on-premises
        List<Data> cloudData = cloudService.getNewData();
        onPremisesService.syncData(cloudData);
    }
}
```

## 17.8 Cloud Migration Patterns

Cloud migration patterns provide strategies for moving applications and data from on-premises to cloud environments.

### When to Use:
- When you want to move to cloud infrastructure
- When you need to modernize legacy applications
- When you want to reduce operational overhead

### Real-World Analogy:
Think of moving from a house you own to a luxury apartment. You need to decide what to take with you, what to replace, and how to adapt your lifestyle to the new environment.

### Basic Implementation:
```java
// Migration strategy interface
public interface MigrationStrategy {
    void migrate(Application app);
    MigrationResult getResult();
}

// Lift and shift strategy
@Component
public class LiftAndShiftStrategy implements MigrationStrategy {
    
    @Override
    public void migrate(Application app) {
        // Move application as-is to cloud
        CloudInfrastructure infra = new CloudInfrastructure();
        infra.deployApplication(app);
    }
    
    @Override
    public MigrationResult getResult() {
        return new MigrationResult("LIFT_AND_SHIFT", "COMPLETED");
    }
}

// Replatforming strategy
@Component
public class ReplatformingStrategy implements MigrationStrategy {
    
    @Override
    public void migrate(Application app) {
        // Modify application for cloud platform
        CloudOptimizedApp optimizedApp = optimizeForCloud(app);
        CloudInfrastructure infra = new CloudInfrastructure();
        infra.deployApplication(optimizedApp);
    }
    
    private CloudOptimizedApp optimizeForCloud(Application app) {
        // Add cloud-specific optimizations
        return new CloudOptimizedApp(app);
    }
}

// Migration orchestrator
@Service
public class MigrationOrchestrator {
    
    @Autowired
    private List<MigrationStrategy> strategies;
    
    public void migrateApplication(Application app, MigrationType type) {
        MigrationStrategy strategy = selectStrategy(type);
        strategy.migrate(app);
    }
    
    private MigrationStrategy selectStrategy(MigrationType type) {
        return strategies.stream()
            .filter(strategy -> strategy.supports(type))
            .findFirst()
            .orElseThrow(() -> new UnsupportedMigrationTypeException());
    }
}
```

## 17.9 Cost Optimization Patterns

Cost optimization patterns help minimize cloud spending while maintaining performance and functionality.

### When to Use:
- When you want to reduce cloud costs
- When you need to optimize resource utilization
- When you want to implement cost controls

### Real-World Analogy:
Think of managing a household budget. You track your expenses, identify areas where you can save money, and make adjustments to stay within your budget while maintaining your quality of life.

### Basic Implementation:
```java
// Cost optimization service
@Service
public class CostOptimizationService {
    
    @Autowired
    private CloudCostAnalyzer costAnalyzer;
    
    @Autowired
    private ResourceOptimizer resourceOptimizer;
    
    @Scheduled(cron = "0 0 2 * * ?") // Daily at 2 AM
    public void optimizeCosts() {
        CostAnalysis analysis = costAnalyzer.analyzeCosts();
        
        if (analysis.getWastePercentage() > 20) {
            List<OptimizationRecommendation> recommendations = 
                resourceOptimizer.generateRecommendations(analysis);
            
            applyRecommendations(recommendations);
        }
    }
    
    private void applyRecommendations(List<OptimizationRecommendation> recommendations) {
        recommendations.forEach(rec -> {
            switch (rec.getType()) {
                case SCALE_DOWN:
                    scaleDownResources(rec.getResourceId());
                    break;
                case SCHEDULE_SHUTDOWN:
                    scheduleShutdown(rec.getResourceId(), rec.getSchedule());
                    break;
                case MIGRATE_TO_CHEAPER_TIER:
                    migrateToCheaperTier(rec.getResourceId());
                    break;
            }
        });
    }
}

// Cost monitoring
@Component
public class CostMonitor {
    
    @EventListener
    public void handleResourceCreation(ResourceCreatedEvent event) {
        if (getCurrentCost() > getBudgetLimit()) {
            throw new BudgetExceededException("Cannot create resource: budget exceeded");
        }
    }
    
    private double getCurrentCost() {
        // Calculate current monthly cost
        return costCalculator.calculateMonthlyCost();
    }
    
    private double getBudgetLimit() {
        return budgetService.getMonthlyLimit();
    }
}
```

## 17.10 Security Patterns in Cloud

Security patterns in cloud environments address unique security challenges and leverage cloud security services.

### When to Use:
- When you need to secure cloud applications
- When you want to leverage cloud security services
- When you need to comply with cloud security standards

### Real-World Analogy:
Think of a high-security building with multiple layers of protection - key cards for entry, security cameras, biometric scanners, and security personnel. Each layer provides additional security, and they work together to protect the building.

### Basic Implementation:
```java
// Cloud security service
@Service
public class CloudSecurityService {
    
    @Autowired
    private CloudIdentityProvider identityProvider;
    
    @Autowired
    private CloudEncryptionService encryptionService;
    
    @Autowired
    private CloudAuditService auditService;
    
    public SecurityContext authenticateUser(String token) {
        try {
            UserIdentity user = identityProvider.validateToken(token);
            auditService.logAuthentication(user.getId(), "SUCCESS");
            return new SecurityContext(user);
        } catch (InvalidTokenException e) {
            auditService.logAuthentication("unknown", "FAILURE");
            throw new AuthenticationException("Invalid token", e);
        }
    }
    
    public String encryptSensitiveData(String data) {
        return encryptionService.encrypt(data, getCurrentEncryptionKey());
    }
    
    public String decryptSensitiveData(String encryptedData) {
        return encryptionService.decrypt(encryptedData, getCurrentEncryptionKey());
    }
}

// Cloud security configuration
@Configuration
@EnableWebSecurity
public class CloudSecurityConfig extends WebSecurityConfigurerAdapter {
    
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
                .antMatchers("/public/**").permitAll()
                .antMatchers("/api/**").authenticated()
                .and()
            .oauth2Login()
                .and()
            .oauth2ResourceServer()
                .jwt()
                .and()
            .addFilterBefore(new CloudSecurityFilter(), UsernamePasswordAuthenticationFilter.class);
    }
}

// Cloud security filter
public class CloudSecurityFilter extends OncePerRequestFilter {
    
    @Override
    protected void doFilterInternal(HttpServletRequest request, 
                                  HttpServletResponse response, 
                                  FilterChain filterChain) throws ServletException, IOException {
        
        String token = extractToken(request);
        if (token != null) {
            try {
                SecurityContext context = cloudSecurityService.authenticateUser(token);
                SecurityContextHolder.setContext(context);
            } catch (AuthenticationException e) {
                response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                return;
            }
        }
        
        filterChain.doFilter(request, response);
    }
    
    private String extractToken(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (bearerToken != null && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }
}
```

This comprehensive coverage of cloud patterns provides the foundation for building cloud-native applications. Each pattern addresses specific cloud computing challenges and offers different approaches to leveraging cloud services effectively.