# Section 19 – Legacy System Migration

## 19.1 Monolith to Microservices Migration

Migrating from a monolith to microservices requires careful planning and execution.

### Migration Strategy:

```java
// Migration Strategy Service
@Service
public class MonolithMigrationService {
    @Autowired
    private MigrationPlanRepository migrationPlanRepository;
    @Autowired
    private ServiceExtractionService serviceExtractionService;
    
    public MigrationPlan createMigrationPlan(MonolithApplication monolith) {
        MigrationPlan plan = MigrationPlan.builder()
            .monolithId(monolith.getId())
            .strategy(MigrationStrategy.STRANGLER_FIG)
            .phases(createMigrationPhases(monolith))
            .timeline(estimateMigrationTimeline(monolith))
            .build();
        
        return migrationPlanRepository.save(plan);
    }
    
    private List<MigrationPhase> createMigrationPhases(MonolithApplication monolith) {
        List<MigrationPhase> phases = new ArrayList<>();
        
        // Phase 1: Analysis
        phases.add(MigrationPhase.builder()
            .name("Analysis")
            .duration(Duration.ofWeeks(2))
            .tasks(Arrays.asList("Code Analysis", "Dependency Mapping", "Service Identification"))
            .build());
        
        // Phase 2: Service Extraction
        phases.add(MigrationPhase.builder()
            .name("Service Extraction")
            .duration(Duration.ofWeeks(8))
            .tasks(Arrays.asList("Extract Services", "Create APIs", "Data Migration"))
            .build());
        
        // Phase 3: Integration
        phases.add(MigrationPhase.builder()
            .name("Integration")
            .duration(Duration.ofWeeks(4))
            .tasks(Arrays.asList("Service Integration", "Testing", "Deployment"))
            .build());
        
        return phases;
    }
}
```

### Service Extraction:

```java
// Service Extraction Service
@Service
public class ServiceExtractionService {
    @Autowired
    private CodeAnalysisService codeAnalysisService;
    @Autowired
    private ServiceTemplateService serviceTemplateService;
    
    public ExtractedService extractService(MonolithApplication monolith, String serviceName) {
        // Analyze code to identify service boundaries
        ServiceBoundary boundary = codeAnalysisService.identifyServiceBoundary(monolith, serviceName);
        
        // Extract service code
        ServiceCode serviceCode = extractServiceCode(monolith, boundary);
        
        // Create service template
        ServiceTemplate template = serviceTemplateService.createTemplate(serviceName, serviceCode);
        
        // Generate service
        ExtractedService service = generateService(template);
        
        return service;
    }
    
    private ServiceCode extractServiceCode(MonolithApplication monolith, ServiceBoundary boundary) {
        ServiceCode serviceCode = new ServiceCode();
        
        // Extract classes
        for (String className : boundary.getClassNames()) {
            ClassCode classCode = monolith.getClassCode(className);
            serviceCode.addClass(classCode);
        }
        
        // Extract dependencies
        for (String dependency : boundary.getDependencies()) {
            serviceCode.addDependency(dependency);
        }
        
        return serviceCode;
    }
}
```

## 19.2 Strangler Fig Pattern Implementation

The Strangler Fig pattern gradually replaces a monolith with microservices.

### Strangler Fig Service:

```java
// Strangler Fig Service
@Service
public class StranglerFigService {
    @Autowired
    private MonolithClient monolithClient;
    @Autowired
    private MicroserviceClient microserviceClient;
    @Autowired
    private FeatureToggleService featureToggleService;
    
    public ResponseEntity<?> handleRequest(HttpServletRequest request) {
        String path = request.getRequestURI();
        String method = request.getMethod();
        
        // Check if feature is enabled for microservice
        if (featureToggleService.isEnabled("microservice", path)) {
            return microserviceClient.handleRequest(request);
        } else {
            return monolithClient.handleRequest(request);
        }
    }
    
    public void migrateFeature(String featureName, String path) {
        // Enable feature toggle for microservice
        featureToggleService.enable("microservice", path);
        
        // Monitor traffic
        monitorTraffic(featureName, path);
        
        // Gradually increase traffic to microservice
        graduallyIncreaseTraffic(featureName, path);
    }
    
    private void monitorTraffic(String featureName, String path) {
        // Monitor traffic patterns
        TrafficMetrics metrics = collectTrafficMetrics(featureName, path);
        
        // Check for errors
        if (metrics.getErrorRate() > 0.05) {
            // Rollback to monolith
            featureToggleService.disable("microservice", path);
        }
    }
}
```

### Feature Toggle Service:

```java
// Feature Toggle Service
@Service
public class FeatureToggleService {
    @Autowired
    private FeatureToggleRepository featureToggleRepository;
    
    public boolean isEnabled(String service, String path) {
        FeatureToggle toggle = featureToggleRepository.findByServiceAndPath(service, path);
        return toggle != null && toggle.isEnabled();
    }
    
    public void enable(String service, String path) {
        FeatureToggle toggle = featureToggleRepository.findByServiceAndPath(service, path);
        if (toggle == null) {
            toggle = new FeatureToggle(service, path, true);
        } else {
            toggle.setEnabled(true);
        }
        featureToggleRepository.save(toggle);
    }
    
    public void disable(String service, String path) {
        FeatureToggle toggle = featureToggleRepository.findByServiceAndPath(service, path);
        if (toggle != null) {
            toggle.setEnabled(false);
            featureToggleRepository.save(toggle);
        }
    }
}
```

## 19.3 Database Migration Strategies

Database migration strategies handle data movement from monolith to microservices.

### Database Migration Service:

```java
// Database Migration Service
@Service
public class DatabaseMigrationService {
    @Autowired
    private MonolithDatabase monolithDatabase;
    @Autowired
    private MicroserviceDatabase microserviceDatabase;
    @Autowired
    private DataSyncService dataSyncService;
    
    public void migrateDatabase(String serviceName, String tableName) {
        // Create new database for microservice
        microserviceDatabase.createDatabase(serviceName);
        
        // Copy data from monolith
        copyDataFromMonolith(serviceName, tableName);
        
        // Set up data synchronization
        setupDataSynchronization(serviceName, tableName);
        
        // Switch traffic to microservice
        switchTrafficToMicroservice(serviceName, tableName);
    }
    
    private void copyDataFromMonolith(String serviceName, String tableName) {
        // Get data from monolith
        List<Map<String, Object>> data = monolithDatabase.getData(tableName);
        
        // Transform data for microservice
        List<Map<String, Object>> transformedData = transformData(data, serviceName);
        
        // Insert data into microservice database
        microserviceDatabase.insertData(serviceName, tableName, transformedData);
    }
    
    private void setupDataSynchronization(String serviceName, String tableName) {
        // Set up real-time synchronization
        dataSyncService.setupSync(monolithDatabase, microserviceDatabase, tableName);
        
        // Set up batch synchronization
        dataSyncService.setupBatchSync(monolithDatabase, microserviceDatabase, tableName);
    }
}
```

### Data Synchronization:

```java
// Data Synchronization Service
@Service
public class DataSyncService {
    @Autowired
    private MessageQueueService messageQueueService;
    
    public void setupSync(Database source, Database target, String tableName) {
        // Set up change data capture
        ChangeDataCapture cdc = new ChangeDataCapture(source, tableName);
        
        // Listen for changes
        cdc.onChange(change -> {
            // Transform change
            DataChange transformedChange = transformChange(change, target);
            
            // Apply change to target
            applyChange(target, transformedChange);
        });
    }
    
    public void setupBatchSync(Database source, Database target, String tableName) {
        // Schedule batch sync
        @Scheduled(fixedRate = 300000) // Every 5 minutes
        public void syncData() {
            // Get changes since last sync
            List<DataChange> changes = source.getChangesSince(lastSyncTime);
            
            // Apply changes to target
            for (DataChange change : changes) {
                applyChange(target, change);
            }
            
            // Update last sync time
            lastSyncTime = Instant.now();
        }
    }
}
```

## 19.4 API Wrapping Techniques

API wrapping techniques provide a bridge between monolith and microservices.

### API Wrapper Service:

```java
// API Wrapper Service
@RestController
@RequestMapping("/api/legacy")
public class LegacyApiWrapper {
    @Autowired
    private MonolithClient monolithClient;
    @Autowired
    private MicroserviceClient microserviceClient;
    @Autowired
    private FeatureToggleService featureToggleService;
    
    @GetMapping("/users/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        // Check if microservice is available
        if (featureToggleService.isEnabled("user-service", "/users/" + id)) {
            try {
                return microserviceClient.getUser(id);
            } catch (Exception e) {
                // Fallback to monolith
                return monolithClient.getUser(id);
            }
        } else {
            return monolithClient.getUser(id);
        }
    }
    
    @PostMapping("/users")
    public ResponseEntity<User> createUser(@RequestBody UserRequest request) {
        // Check if microservice is available
        if (featureToggleService.isEnabled("user-service", "/users")) {
            try {
                return microserviceClient.createUser(request);
            } catch (Exception e) {
                // Fallback to monolith
                return monolithClient.createUser(request);
            }
        } else {
            return monolithClient.createUser(request);
        }
    }
}
```

### API Gateway Wrapper:

```java
// API Gateway Wrapper
@Configuration
public class ApiGatewayWrapperConfig {
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("user-service", r -> r.path("/api/users/**")
                .filters(f -> f
                    .rewritePath("/api/users/(?<path>.*)", "/${path}")
                    .circuitBreaker(config -> config
                        .setName("user-service-cb")
                        .setFallbackUri("forward:/fallback/user-service")))
                .uri("lb://user-service"))
            .route("legacy-monolith", r -> r.path("/api/legacy/**")
                .filters(f -> f
                    .rewritePath("/api/legacy/(?<path>.*)", "/${path}"))
                .uri("http://monolith:8080"))
            .build();
    }
}
```

## 19.5 Gradual Migration Approaches

Gradual migration approaches minimize risk by migrating incrementally.

### Gradual Migration Service:

```java
// Gradual Migration Service
@Service
public class GradualMigrationService {
    @Autowired
    private MigrationPlanRepository migrationPlanRepository;
    @Autowired
    private TrafficSplitService trafficSplitService;
    
    public void executeGradualMigration(String serviceName, MigrationPlan plan) {
        // Phase 1: Deploy microservice alongside monolith
        deployMicroservice(serviceName);
        
        // Phase 2: Start with 5% traffic
        trafficSplitService.setTrafficSplit(serviceName, 5, 95);
        
        // Phase 3: Gradually increase traffic
        graduallyIncreaseTraffic(serviceName, plan);
        
        // Phase 4: Complete migration
        completeMigration(serviceName);
    }
    
    private void graduallyIncreaseTraffic(String serviceName, MigrationPlan plan) {
        int[] trafficPercentages = {5, 10, 25, 50, 75, 90, 100};
        
        for (int percentage : trafficPercentages) {
            // Set traffic split
            trafficSplitService.setTrafficSplit(serviceName, percentage, 100 - percentage);
            
            // Monitor for issues
            monitorTraffic(serviceName, percentage);
            
            // Wait for stability
            waitForStability(serviceName, percentage);
        }
    }
    
    private void monitorTraffic(String serviceName, int percentage) {
        // Monitor error rates
        double errorRate = getErrorRate(serviceName);
        if (errorRate > 0.05) {
            // Rollback traffic
            trafficSplitService.setTrafficSplit(serviceName, 0, 100);
            throw new MigrationException("Error rate too high: " + errorRate);
        }
        
        // Monitor response times
        double avgResponseTime = getAverageResponseTime(serviceName);
        if (avgResponseTime > 2000) {
            // Rollback traffic
            trafficSplitService.setTrafficSplit(serviceName, 0, 100);
            throw new MigrationException("Response time too high: " + avgResponseTime);
        }
    }
}
```

## 19.6 Risk Assessment and Mitigation

Risk assessment and mitigation strategies help manage migration risks.

### Risk Assessment Service:

```java
// Risk Assessment Service
@Service
public class RiskAssessmentService {
    @Autowired
    private RiskRepository riskRepository;
    
    public RiskAssessment assessMigrationRisks(MonolithApplication monolith) {
        RiskAssessment assessment = new RiskAssessment();
        
        // Assess technical risks
        List<Risk> technicalRisks = assessTechnicalRisks(monolith);
        assessment.addRisks(technicalRisks);
        
        // Assess business risks
        List<Risk> businessRisks = assessBusinessRisks(monolith);
        assessment.addRisks(businessRisks);
        
        // Assess operational risks
        List<Risk> operationalRisks = assessOperationalRisks(monolith);
        assessment.addRisks(operationalRisks);
        
        return assessment;
    }
    
    private List<Risk> assessTechnicalRisks(MonolithApplication monolith) {
        List<Risk> risks = new ArrayList<>();
        
        // Assess complexity
        if (monolith.getComplexity() > 0.8) {
            risks.add(Risk.builder()
                .type(RiskType.TECHNICAL)
                .name("High Complexity")
                .description("Monolith has high complexity")
                .probability(0.7)
                .impact(0.8)
                .mitigation("Break down into smaller services")
                .build());
        }
        
        // Assess dependencies
        if (monolith.getDependencyCount() > 100) {
            risks.add(Risk.builder()
                .type(RiskType.TECHNICAL)
                .name("High Dependencies")
                .description("Monolith has many dependencies")
                .probability(0.6)
                .impact(0.7)
                .mitigation("Identify and decouple dependencies")
                .build());
        }
        
        return risks;
    }
}
```

## 19.7 Change Management

Change management ensures smooth migration with minimal disruption.

### Change Management Service:

```java
// Change Management Service
@Service
public class ChangeManagementService {
    @Autowired
    private ChangeRequestRepository changeRequestRepository;
    @Autowired
    private ApprovalService approvalService;
    
    public ChangeRequest createChangeRequest(ChangeRequest request) {
        request.setStatus(ChangeRequestStatus.PENDING);
        request.setCreatedAt(Instant.now());
        
        // Validate request
        validateChangeRequest(request);
        
        // Submit for approval
        approvalService.submitForApproval(request);
        
        return changeRequestRepository.save(request);
    }
    
    public void approveChangeRequest(Long requestId, String approver) {
        ChangeRequest request = changeRequestRepository.findById(requestId);
        request.setStatus(ChangeRequestStatus.APPROVED);
        request.setApprovedBy(approver);
        request.setApprovedAt(Instant.now());
        
        changeRequestRepository.save(request);
    }
    
    public void implementChangeRequest(Long requestId) {
        ChangeRequest request = changeRequestRepository.findById(requestId);
        
        // Implement change
        implementChange(request);
        
        // Update status
        request.setStatus(ChangeRequestStatus.IMPLEMENTED);
        request.setImplementedAt(Instant.now());
        
        changeRequestRepository.save(request);
    }
}
```

## 19.8 Rollback Strategies

Rollback strategies ensure quick recovery from migration issues.

### Rollback Service:

```java
// Rollback Service
@Service
public class RollbackService {
    @Autowired
    private DeploymentService deploymentService;
    @Autowired
    private TrafficSplitService trafficSplitService;
    @Autowired
    private DatabaseRollbackService databaseRollbackService;
    
    public void rollbackMigration(String serviceName, RollbackReason reason) {
        log.warn("Rolling back migration for service: {} due to: {}", serviceName, reason);
        
        // Rollback traffic to monolith
        trafficSplitService.setTrafficSplit(serviceName, 0, 100);
        
        // Rollback database changes
        databaseRollbackService.rollback(serviceName);
        
        // Rollback deployment
        deploymentService.rollback(serviceName);
        
        // Notify stakeholders
        notifyStakeholders(serviceName, reason);
    }
    
    public void rollbackToPreviousVersion(String serviceName) {
        // Get previous version
        String previousVersion = deploymentService.getPreviousVersion(serviceName);
        
        // Deploy previous version
        deploymentService.deploy(serviceName, previousVersion);
        
        // Verify rollback
        verifyRollback(serviceName);
    }
    
    private void verifyRollback(String serviceName) {
        // Check service health
        boolean isHealthy = checkServiceHealth(serviceName);
        if (!isHealthy) {
            throw new RollbackException("Service is not healthy after rollback");
        }
        
        // Check traffic flow
        boolean isTrafficFlowing = checkTrafficFlow(serviceName);
        if (!isTrafficFlowing) {
            throw new RollbackException("Traffic is not flowing after rollback");
        }
    }
}
```

This comprehensive guide covers all aspects of legacy system migration, providing both theoretical understanding and practical implementation examples.