# Section 10 – Testing Strategies

## 10.1 Unit Testing for Microservices

Unit testing focuses on testing individual components in isolation, ensuring that each unit of code works correctly.

### Unit Test Structure:

```java
// User Service Unit Test
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository userRepository;
    @Mock
    private EmailService emailService;
    @Mock
    private EventPublisher eventPublisher;
    
    @InjectMocks
    private UserService userService;
    
    @Test
    void shouldCreateUserSuccessfully() {
        // Given
        UserRequest request = UserRequest.builder()
            .email("test@example.com")
            .name("Test User")
            .password("password123")
            .build();
        
        User savedUser = User.builder()
            .id(1L)
            .email("test@example.com")
            .name("Test User")
            .status(UserStatus.ACTIVE)
            .build();
        
        when(userRepository.save(any(User.class))).thenReturn(savedUser);
        
        // When
        User result = userService.createUser(request);
        
        // Then
        assertThat(result).isNotNull();
        assertThat(result.getEmail()).isEqualTo("test@example.com");
        assertThat(result.getName()).isEqualTo("Test User");
        assertThat(result.getStatus()).isEqualTo(UserStatus.ACTIVE);
        
        verify(userRepository).save(any(User.class));
        verify(emailService).sendWelcomeEmail("test@example.com", "Test User");
        verify(eventPublisher).publishUserCreated(any(UserCreatedEvent.class));
    }
    
    @Test
    void shouldThrowExceptionWhenUserAlreadyExists() {
        // Given
        UserRequest request = UserRequest.builder()
            .email("existing@example.com")
            .name("Existing User")
            .password("password123")
            .build();
        
        when(userRepository.findByEmail("existing@example.com"))
            .thenReturn(Optional.of(new User()));
        
        // When & Then
        assertThatThrownBy(() -> userService.createUser(request))
            .isInstanceOf(UserAlreadyExistsException.class)
            .hasMessage("User with email existing@example.com already exists");
        
        verify(userRepository, never()).save(any(User.class));
        verify(emailService, never()).sendWelcomeEmail(anyString(), anyString());
    }
    
    @Test
    void shouldUpdateUserSuccessfully() {
        // Given
        Long userId = 1L;
        UserUpdateRequest request = UserUpdateRequest.builder()
            .name("Updated Name")
            .email("updated@example.com")
            .build();
        
        User existingUser = User.builder()
            .id(userId)
            .email("old@example.com")
            .name("Old Name")
            .status(UserStatus.ACTIVE)
            .build();
        
        when(userRepository.findById(userId)).thenReturn(Optional.of(existingUser));
        when(userRepository.save(any(User.class))).thenReturn(existingUser);
        
        // When
        User result = userService.updateUser(userId, request);
        
        // Then
        assertThat(result.getName()).isEqualTo("Updated Name");
        assertThat(result.getEmail()).isEqualTo("updated@example.com");
        
        verify(userRepository).findById(userId);
        verify(userRepository).save(existingUser);
        verify(eventPublisher).publishUserUpdated(any(UserUpdatedEvent.class));
    }
}
```

### Test Data Builders:

```java
// Test Data Builder
public class UserTestDataBuilder {
    private Long id = 1L;
    private String email = "test@example.com";
    private String name = "Test User";
    private String password = "password123";
    private UserStatus status = UserStatus.ACTIVE;
    private Instant createdAt = Instant.now();
    
    public static UserTestDataBuilder aUser() {
        return new UserTestDataBuilder();
    }
    
    public UserTestDataBuilder withId(Long id) {
        this.id = id;
        return this;
    }
    
    public UserTestDataBuilder withEmail(String email) {
        this.email = email;
        return this;
    }
    
    public UserTestDataBuilder withName(String name) {
        this.name = name;
        return this;
    }
    
    public UserTestDataBuilder withPassword(String password) {
        this.password = password;
        return this;
    }
    
    public UserTestDataBuilder withStatus(UserStatus status) {
        this.status = status;
        return this;
    }
    
    public User build() {
        return User.builder()
            .id(id)
            .email(email)
            .name(name)
            .password(password)
            .status(status)
            .createdAt(createdAt)
            .build();
    }
}

// Using Test Data Builder
@Test
void shouldCreateUserWithBuilder() {
    // Given
    User user = UserTestDataBuilder.aUser()
        .withEmail("builder@example.com")
        .withName("Builder User")
        .withStatus(UserStatus.ACTIVE)
        .build();
    
    when(userRepository.save(any(User.class))).thenReturn(user);
    
    // When
    User result = userService.createUser(user);
    
    // Then
    assertThat(result).isNotNull();
    assertThat(result.getEmail()).isEqualTo("builder@example.com");
}
```

## 10.2 Integration Testing

Integration testing verifies that different components work together correctly.

### Spring Boot Integration Test:

```java
// Integration Test
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(properties = {
    "spring.datasource.url=jdbc:h2:mem:testdb",
    "spring.jpa.hibernate.ddl-auto=create-drop"
})
class UserServiceIntegrationTest {
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Autowired
    private UserRepository userRepository;
    
    @LocalServerPort
    private int port;
    
    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }
    
    @Test
    void shouldCreateUserThroughApi() {
        // Given
        UserRequest request = UserRequest.builder()
            .email("integration@example.com")
            .name("Integration User")
            .password("password123")
            .build();
        
        // When
        ResponseEntity<User> response = restTemplate.postForEntity(
            "/api/users", request, User.class);
        
        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody()).isNotNull();
        assertThat(response.getBody().getEmail()).isEqualTo("integration@example.com");
        
        // Verify in database
        List<User> users = userRepository.findAll();
        assertThat(users).hasSize(1);
        assertThat(users.get(0).getEmail()).isEqualTo("integration@example.com");
    }
    
    @Test
    void shouldGetUserThroughApi() {
        // Given
        User user = User.builder()
            .email("get@example.com")
            .name("Get User")
            .status(UserStatus.ACTIVE)
            .build();
        userRepository.save(user);
        
        // When
        ResponseEntity<User> response = restTemplate.getForEntity(
            "/api/users/" + user.getId(), User.class);
        
        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody()).isNotNull();
        assertThat(response.getBody().getEmail()).isEqualTo("get@example.com");
    }
    
    @Test
    void shouldReturn404WhenUserNotFound() {
        // When
        ResponseEntity<String> response = restTemplate.getForEntity(
            "/api/users/999", String.class);
        
        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }
}
```

### Database Integration Test:

```java
// Database Integration Test
@DataJpaTest
class UserRepositoryIntegrationTest {
    @Autowired
    private TestEntityManager entityManager;
    
    @Autowired
    private UserRepository userRepository;
    
    @Test
    void shouldFindUserByEmail() {
        // Given
        User user = User.builder()
            .email("find@example.com")
            .name("Find User")
            .status(UserStatus.ACTIVE)
            .build();
        entityManager.persistAndFlush(user);
        
        // When
        Optional<User> result = userRepository.findByEmail("find@example.com");
        
        // Then
        assertThat(result).isPresent();
        assertThat(result.get().getEmail()).isEqualTo("find@example.com");
    }
    
    @Test
    void shouldFindActiveUsers() {
        // Given
        User activeUser = User.builder()
            .email("active@example.com")
            .name("Active User")
            .status(UserStatus.ACTIVE)
            .build();
        User inactiveUser = User.builder()
            .email("inactive@example.com")
            .name("Inactive User")
            .status(UserStatus.INACTIVE)
            .build();
        
        entityManager.persistAndFlush(activeUser);
        entityManager.persistAndFlush(inactiveUser);
        
        // When
        List<User> activeUsers = userRepository.findByStatus(UserStatus.ACTIVE);
        
        // Then
        assertThat(activeUsers).hasSize(1);
        assertThat(activeUsers.get(0).getEmail()).isEqualTo("active@example.com");
    }
}
```

## 10.3 Contract Testing

Contract testing ensures that services can communicate with each other correctly by testing the contracts between them.

### Pact Contract Testing:

```java
// Consumer Contract Test
@ExtendWith(PactConsumerTestExt.class)
@PactTestFor(providerName = "user-service")
class UserServiceContractTest {
    
    @Pact(consumer = "order-service")
    public RequestResponsePact getUserPact(PactDslWithProvider builder) {
        return builder
            .given("user exists")
            .uponReceiving("a request for user")
            .path("/api/users/1")
            .method("GET")
            .willRespondWith()
            .status(200)
            .headers(Map.of("Content-Type", "application/json"))
            .body(new PactDslJsonBody()
                .numberType("id", 1L)
                .stringType("email", "test@example.com")
                .stringType("name", "Test User")
                .stringType("status", "ACTIVE"))
            .toPact();
    }
    
    @Test
    @PactTestFor(pactMethod = "getUserPact")
    void shouldGetUser(MockServer mockServer) {
        // Given
        String userServiceUrl = mockServer.getUrl();
        UserServiceClient userServiceClient = new UserServiceClient(userServiceUrl);
        
        // When
        User user = userServiceClient.getUser(1L);
        
        // Then
        assertThat(user).isNotNull();
        assertThat(user.getId()).isEqualTo(1L);
        assertThat(user.getEmail()).isEqualTo("test@example.com");
        assertThat(user.getName()).isEqualTo("Test User");
        assertThat(user.getStatus()).isEqualTo(UserStatus.ACTIVE);
    }
}
```

### Provider Contract Test:

```java
// Provider Contract Test
@ExtendWith(PactVerificationInvocationContextProvider.class)
@PactTestFor(providerName = "user-service")
class UserServiceProviderContractTest {
    
    @TestTemplate
    @ExtendWith(PactVerificationInvocationContextProvider.class)
    void pactVerificationTestTemplate(PactVerificationContext context) {
        context.verifyInteraction();
    }
    
    @BeforeEach
    void before(PactVerificationContext context) {
        context.setTarget(new HttpTestTarget("localhost", 8080));
    }
    
    @State("user exists")
    void userExists() {
        // Setup test data
        User user = User.builder()
            .id(1L)
            .email("test@example.com")
            .name("Test User")
            .status(UserStatus.ACTIVE)
            .build();
        
        // Mock repository or service
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
    }
}
```

## 10.4 End-to-End Testing

End-to-end testing verifies that the entire system works correctly from the user's perspective.

### Selenium E2E Test:

```java
// E2E Test with Selenium
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class UserManagementE2ETest {
    @Autowired
    private TestRestTemplate restTemplate;
    
    @LocalServerPort
    private int port;
    
    private WebDriver driver;
    
    @BeforeEach
    void setUp() {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless");
        driver = new ChromeDriver(options);
    }
    
    @AfterEach
    void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
    
    @Test
    void shouldCreateUserThroughWebInterface() {
        // Given
        driver.get("http://localhost:" + port + "/users/create");
        
        // When
        driver.findElement(By.id("email")).sendKeys("e2e@example.com");
        driver.findElement(By.id("name")).sendKeys("E2E User");
        driver.findElement(By.id("password")).sendKeys("password123");
        driver.findElement(By.id("submit")).click();
        
        // Then
        WebElement successMessage = driver.findElement(By.id("success-message"));
        assertThat(successMessage.getText()).contains("User created successfully");
        
        // Verify user was created
        ResponseEntity<User> response = restTemplate.getForEntity(
            "/api/users?email=e2e@example.com", User.class);
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
    }
    
    @Test
    void shouldLoginUserThroughWebInterface() {
        // Given
        User user = User.builder()
            .email("login@example.com")
            .name("Login User")
            .password(encodePassword("password123"))
            .status(UserStatus.ACTIVE)
            .build();
        restTemplate.postForEntity("/api/users", user, User.class);
        
        driver.get("http://localhost:" + port + "/login");
        
        // When
        driver.findElement(By.id("email")).sendKeys("login@example.com");
        driver.findElement(By.id("password")).sendKeys("password123");
        driver.findElement(By.id("login")).click();
        
        // Then
        WebElement welcomeMessage = driver.findElement(By.id("welcome-message"));
        assertThat(welcomeMessage.getText()).contains("Welcome, Login User");
    }
}
```

### API E2E Test:

```java
// API E2E Test
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class UserServiceE2ETest {
    @Autowired
    private TestRestTemplate restTemplate;
    
    @LocalServerPort
    private int port;
    
    @Test
    void shouldCompleteUserLifecycle() {
        // Create user
        UserRequest createRequest = UserRequest.builder()
            .email("lifecycle@example.com")
            .name("Lifecycle User")
            .password("password123")
            .build();
        
        ResponseEntity<User> createResponse = restTemplate.postForEntity(
            "/api/users", createRequest, User.class);
        
        assertThat(createResponse.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        User createdUser = createResponse.getBody();
        assertThat(createdUser).isNotNull();
        assertThat(createdUser.getEmail()).isEqualTo("lifecycle@example.com");
        
        // Get user
        ResponseEntity<User> getResponse = restTemplate.getForEntity(
            "/api/users/" + createdUser.getId(), User.class);
        
        assertThat(getResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        User retrievedUser = getResponse.getBody();
        assertThat(retrievedUser).isNotNull();
        assertThat(retrievedUser.getEmail()).isEqualTo("lifecycle@example.com");
        
        // Update user
        UserUpdateRequest updateRequest = UserUpdateRequest.builder()
            .name("Updated Lifecycle User")
            .email("updated@example.com")
            .build();
        
        ResponseEntity<User> updateResponse = restTemplate.exchange(
            "/api/users/" + createdUser.getId(),
            HttpMethod.PUT,
            new HttpEntity<>(updateRequest),
            User.class
        );
        
        assertThat(updateResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        User updatedUser = updateResponse.getBody();
        assertThat(updatedUser).isNotNull();
        assertThat(updatedUser.getName()).isEqualTo("Updated Lifecycle User");
        
        // Delete user
        ResponseEntity<Void> deleteResponse = restTemplate.exchange(
            "/api/users/" + createdUser.getId(),
            HttpMethod.DELETE,
            null,
            Void.class
        );
        
        assertThat(deleteResponse.getStatusCode()).isEqualTo(HttpStatus.NO_CONTENT);
        
        // Verify user is deleted
        ResponseEntity<User> getDeletedResponse = restTemplate.getForEntity(
            "/api/users/" + createdUser.getId(), User.class);
        
        assertThat(getDeletedResponse.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }
}
```

## 10.5 Chaos Engineering

Chaos engineering tests the system's resilience by intentionally introducing failures.

### Chaos Monkey Implementation:

```java
// Chaos Monkey Service
@Service
public class ChaosMonkeyService {
    @Value("${chaos.monkey.enabled:false}")
    private boolean chaosMonkeyEnabled;
    
    @Value("${chaos.monkey.latency.probability:0.1}")
    private double latencyProbability;
    
    @Value("${chaos.monkey.exception.probability:0.05}")
    private double exceptionProbability;
    
    @Value("${chaos.monkey.latency.range:100-1000}")
    private String latencyRange;
    
    public void maybeIntroduceLatency() {
        if (chaosMonkeyEnabled && Math.random() < latencyProbability) {
            int minLatency = Integer.parseInt(latencyRange.split("-")[0]);
            int maxLatency = Integer.parseInt(latencyRange.split("-")[1]);
            int latency = minLatency + (int) (Math.random() * (maxLatency - minLatency));
            
            try {
                Thread.sleep(latency);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    public void maybeThrowException() {
        if (chaosMonkeyEnabled && Math.random() < exceptionProbability) {
            throw new ChaosMonkeyException("Chaos monkey introduced exception");
        }
    }
}

// Chaos Monkey Aspect
@Aspect
@Component
public class ChaosMonkeyAspect {
    @Autowired
    private ChaosMonkeyService chaosMonkeyService;
    
    @Around("@annotation(ChaosMonkey)")
    public Object introduceChaos(ProceedingJoinPoint joinPoint) throws Throwable {
        chaosMonkeyService.maybeIntroduceLatency();
        chaosMonkeyService.maybeThrowException();
        
        return joinPoint.proceed();
    }
}

// Chaos Monkey Annotation
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface ChaosMonkey {
}

// Using Chaos Monkey
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
    
    @ChaosMonkey
    public User getUser(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found: " + id));
    }
}
```

### Chaos Engineering Test:

```java
// Chaos Engineering Test
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class ChaosEngineeringTest {
    @Autowired
    private TestRestTemplate restTemplate;
    
    @LocalServerPort
    private int port;
    
    @Test
    void shouldHandleServiceFailure() {
        // Given
        UserRequest request = UserRequest.builder()
            .email("chaos@example.com")
            .name("Chaos User")
            .password("password123")
            .build();
        
        // When - Make multiple requests to trigger chaos
        List<CompletableFuture<ResponseEntity<User>>> futures = new ArrayList<>();
        
        for (int i = 0; i < 100; i++) {
            futures.add(CompletableFuture.supplyAsync(() -> 
                restTemplate.postForEntity("/api/users", request, User.class)));
        }
        
        // Then - Verify some requests succeed despite chaos
        List<ResponseEntity<User>> responses = futures.stream()
            .map(CompletableFuture::join)
            .collect(Collectors.toList());
        
        long successCount = responses.stream()
            .mapToLong(response -> response.getStatusCode().is2xxSuccessful() ? 1 : 0)
            .sum();
        
        assertThat(successCount).isGreaterThan(0);
    }
}
```

## 10.6 Load Testing and Performance Testing

Load testing verifies that the system can handle expected load levels.

### JMeter Load Test:

```java
// JMeter Load Test Configuration
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class LoadTest {
    @Autowired
    private TestRestTemplate restTemplate;
    
    @LocalServerPort
    private int port;
    
    @Test
    void shouldHandleConcurrentUsers() throws InterruptedException {
        int numberOfUsers = 100;
        int requestsPerUser = 10;
        ExecutorService executor = Executors.newFixedThreadPool(numberOfUsers);
        CountDownLatch latch = new CountDownLatch(numberOfUsers);
        List<CompletableFuture<TestResult>> futures = new ArrayList<>();
        
        for (int i = 0; i < numberOfUsers; i++) {
            final int userIndex = i;
            CompletableFuture<TestResult> future = CompletableFuture.supplyAsync(() -> {
                try {
                    return simulateUserLoad(userIndex, requestsPerUser);
                } finally {
                    latch.countDown();
                }
            }, executor);
            futures.add(future);
        }
        
        // Wait for all users to complete
        latch.await(60, TimeUnit.SECONDS);
        
        // Analyze results
        List<TestResult> results = futures.stream()
            .map(CompletableFuture::join)
            .collect(Collectors.toList());
        
        analyzeLoadTestResults(results);
    }
    
    private TestResult simulateUserLoad(int userIndex, int requestsPerUser) {
        TestResult result = new TestResult();
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < requestsPerUser; i++) {
            try {
                UserRequest request = UserRequest.builder()
                    .email("loadtest" + userIndex + "_" + i + "@example.com")
                    .name("Load Test User " + userIndex + "_" + i)
                    .password("password123")
                    .build();
                
                long requestStart = System.currentTimeMillis();
                ResponseEntity<User> response = restTemplate.postForEntity(
                    "/api/users", request, User.class);
                long requestEnd = System.currentTimeMillis();
                
                result.addRequest(requestEnd - requestStart, response.getStatusCode().is2xxSuccessful());
                
            } catch (Exception e) {
                result.addError(e.getMessage());
            }
        }
        
        result.setTotalTime(System.currentTimeMillis() - startTime);
        return result;
    }
    
    private void analyzeLoadTestResults(List<TestResult> results) {
        long totalRequests = results.stream()
            .mapToLong(TestResult::getRequestCount)
            .sum();
        
        long successfulRequests = results.stream()
            .mapToLong(TestResult::getSuccessfulRequestCount)
            .sum();
        
        double successRate = (double) successfulRequests / totalRequests;
        double averageResponseTime = results.stream()
            .mapToDouble(TestResult::getAverageResponseTime)
            .average()
            .orElse(0.0);
        
        assertThat(successRate).isGreaterThan(0.95); // 95% success rate
        assertThat(averageResponseTime).isLessThan(1000); // Less than 1 second
    }
}
```

### Performance Test:

```java
// Performance Test
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class PerformanceTest {
    @Autowired
    private TestRestTemplate restTemplate;
    
    @LocalServerPort
    private int port;
    
    @Test
    void shouldMeetPerformanceRequirements() {
        // Test response time
        testResponseTime();
        
        // Test throughput
        testThroughput();
        
        // Test memory usage
        testMemoryUsage();
    }
    
    private void testResponseTime() {
        UserRequest request = UserRequest.builder()
            .email("perf@example.com")
            .name("Performance User")
            .password("password123")
            .build();
        
        long startTime = System.currentTimeMillis();
        ResponseEntity<User> response = restTemplate.postForEntity(
            "/api/users", request, User.class);
        long endTime = System.currentTimeMillis();
        
        long responseTime = endTime - startTime;
        assertThat(responseTime).isLessThan(500); // Less than 500ms
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
    }
    
    private void testThroughput() {
        int numberOfRequests = 1000;
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < numberOfRequests; i++) {
            UserRequest request = UserRequest.builder()
                .email("throughput" + i + "@example.com")
                .name("Throughput User " + i)
                .password("password123")
                .build();
            
            restTemplate.postForEntity("/api/users", request, User.class);
        }
        
        long endTime = System.currentTimeMillis();
        long totalTime = endTime - startTime;
        double throughput = (double) numberOfRequests / (totalTime / 1000.0);
        
        assertThat(throughput).isGreaterThan(100); // More than 100 requests per second
    }
    
    private void testMemoryUsage() {
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        long initialMemory = memoryBean.getHeapMemoryUsage().getUsed();
        
        // Perform memory-intensive operations
        for (int i = 0; i < 1000; i++) {
            UserRequest request = UserRequest.builder()
                .email("memory" + i + "@example.com")
                .name("Memory User " + i)
                .password("password123")
                .build();
            
            restTemplate.postForEntity("/api/users", request, User.class);
        }
        
        long finalMemory = memoryBean.getHeapMemoryUsage().getUsed();
        long memoryIncrease = finalMemory - initialMemory;
        
        // Memory increase should be reasonable (less than 100MB)
        assertThat(memoryIncrease).isLessThan(100 * 1024 * 1024);
    }
}
```

## 10.7 Security Testing

Security testing ensures that the system is protected against security threats.

### Security Test:

```java
// Security Test
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class SecurityTest {
    @Autowired
    private TestRestTemplate restTemplate;
    
    @LocalServerPort
    private int port;
    
    @Test
    void shouldPreventSQLInjection() {
        // Given
        String maliciousEmail = "test@example.com'; DROP TABLE users; --";
        UserRequest request = UserRequest.builder()
            .email(maliciousEmail)
            .name("Test User")
            .password("password123")
            .build();
        
        // When
        ResponseEntity<String> response = restTemplate.postForEntity(
            "/api/users", request, String.class);
        
        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.BAD_REQUEST);
    }
    
    @Test
    void shouldPreventXSS() {
        // Given
        String maliciousName = "<script>alert('XSS')</script>";
        UserRequest request = UserRequest.builder()
            .email("xss@example.com")
            .name(maliciousName)
            .password("password123")
            .build();
        
        // When
        ResponseEntity<User> response = restTemplate.postForEntity(
            "/api/users", request, User.class);
        
        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        assertThat(response.getBody().getName()).doesNotContain("<script>");
    }
    
    @Test
    void shouldRequireAuthentication() {
        // When
        ResponseEntity<String> response = restTemplate.getForEntity(
            "/api/users/1", String.class);
        
        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.UNAUTHORIZED);
    }
    
    @Test
    void shouldRateLimitRequests() {
        // When - Make many requests quickly
        for (int i = 0; i < 1000; i++) {
            UserRequest request = UserRequest.builder()
                .email("ratelimit" + i + "@example.com")
                .name("Rate Limit User " + i)
                .password("password123")
                .build();
            
            ResponseEntity<String> response = restTemplate.postForEntity(
                "/api/users", request, String.class);
            
            if (response.getStatusCode() == HttpStatus.TOO_MANY_REQUESTS) {
                break;
            }
        }
        
        // Then - Should eventually get rate limited
        UserRequest request = UserRequest.builder()
            .email("ratelimit@example.com")
            .name("Rate Limit User")
            .password("password123")
            .build();
        
        ResponseEntity<String> response = restTemplate.postForEntity(
            "/api/users", request, String.class);
        
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.TOO_MANY_REQUESTS);
    }
}
```

## 10.8 Test Data Management

Test data management ensures that tests have consistent and reliable data.

### Test Data Factory:

```java
// Test Data Factory
@Component
public class TestDataFactory {
    private final AtomicLong userIdCounter = new AtomicLong(1);
    private final AtomicLong orderIdCounter = new AtomicLong(1);
    
    public User createUser() {
        return User.builder()
            .id(userIdCounter.getAndIncrement())
            .email("user" + userIdCounter.get() + "@example.com")
            .name("Test User " + userIdCounter.get())
            .password("password123")
            .status(UserStatus.ACTIVE)
            .createdAt(Instant.now())
            .build();
    }
    
    public User createUserWithEmail(String email) {
        return User.builder()
            .id(userIdCounter.getAndIncrement())
            .email(email)
            .name("Test User " + userIdCounter.get())
            .password("password123")
            .status(UserStatus.ACTIVE)
            .createdAt(Instant.now())
            .build();
    }
    
    public Order createOrder(Long userId) {
        return Order.builder()
            .id(orderIdCounter.getAndIncrement())
            .userId(userId)
            .totalAmount(new BigDecimal("100.00"))
            .status(OrderStatus.PENDING)
            .createdAt(Instant.now())
            .build();
    }
    
    public List<User> createUsers(int count) {
        return IntStream.range(0, count)
            .mapToObj(i -> createUser())
            .collect(Collectors.toList());
    }
}

// Test Data Setup
@SpringBootTest
class TestDataManagementTest {
    @Autowired
    private TestDataFactory testDataFactory;
    
    @Autowired
    private UserRepository userRepository;
    
    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }
    
    @Test
    void shouldCreateTestData() {
        // Given
        User user = testDataFactory.createUser();
        
        // When
        User savedUser = userRepository.save(user);
        
        // Then
        assertThat(savedUser).isNotNull();
        assertThat(savedUser.getId()).isNotNull();
    }
    
    @Test
    void shouldCreateMultipleTestData() {
        // Given
        List<User> users = testDataFactory.createUsers(10);
        
        // When
        List<User> savedUsers = userRepository.saveAll(users);
        
        // Then
        assertThat(savedUsers).hasSize(10);
        assertThat(savedUsers).allMatch(user -> user.getId() != null);
    }
}
```

This comprehensive guide covers all aspects of testing strategies in microservices, providing both theoretical understanding and practical implementation examples. Each concept is explained with real-world scenarios and Java code examples to make the concepts clear and actionable.