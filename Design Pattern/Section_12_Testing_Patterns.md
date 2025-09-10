# Section 12 - Testing Patterns

## 12.1 Test Doubles (Mock, Stub, Fake)

Test doubles are objects that replace real dependencies in tests, allowing you to control and verify interactions.

### When to Use:
- When you need to isolate the unit under test
- When you want to control external dependencies
- When you need to verify interactions

### Real-World Analogy:
Think of a movie stunt double. The real actor is replaced with a stunt double for dangerous scenes, allowing the movie to be made safely while maintaining the illusion of the real actor performing the action.

### Basic Implementation:
```java
// Stub - provides predetermined responses
public class UserServiceStub implements UserService {
    private Map<String, User> users = new HashMap<>();
    
    public void addUser(User user) {
        users.put(user.getId(), user);
    }
    
    public User findById(String id) {
        return users.get(id);
    }
    
    public List<User> findAll() {
        return new ArrayList<>(users.values());
    }
}

// Mock - verifies interactions
public class UserServiceMock implements UserService {
    private List<String> calledMethods = new ArrayList<>();
    private Map<String, User> users = new HashMap<>();
    
    public User findById(String id) {
        calledMethods.add("findById(" + id + ")");
        return users.get(id);
    }
    
    public List<User> findAll() {
        calledMethods.add("findAll()");
        return new ArrayList<>(users.values());
    }
    
    public boolean wasCalled(String methodName) {
        return calledMethods.stream().anyMatch(method -> method.startsWith(methodName));
    }
    
    public int getCallCount(String methodName) {
        return (int) calledMethods.stream()
            .filter(method -> method.startsWith(methodName))
            .count();
    }
}

// Fake - simplified implementation
public class InMemoryUserRepository implements UserRepository {
    private Map<String, User> users = new HashMap<>();
    
    public void save(User user) {
        users.put(user.getId(), user);
    }
    
    public User findById(String id) {
        return users.get(id);
    }
    
    public List<User> findAll() {
        return new ArrayList<>(users.values());
    }
    
    public void delete(String id) {
        users.remove(id);
    }
}

// Test using doubles
public class UserServiceTest {
    @Test
    public void testCreateUser() {
        // Arrange
        UserServiceMock userServiceMock = new UserServiceMock();
        UserController controller = new UserController(userServiceMock);
        User user = new User("1", "John Doe", "john@example.com");
        
        // Act
        controller.createUser(user);
        
        // Assert
        assertTrue(userServiceMock.wasCalled("save"));
        assertEquals(1, userServiceMock.getCallCount("save"));
    }
}
```

## 12.2 Test Data Builder Pattern

The Test Data Builder pattern creates test objects with a fluent interface, making tests more readable and maintainable.

### When to Use:
- When you need to create complex test objects
- When you want to make tests more readable
- When you need to create objects with many optional parameters

### Real-World Analogy:
Think of a custom car builder. You can specify the engine, color, interior, and other features step by step, and the builder creates the car exactly as you want it.

### Basic Implementation:
```java
// Test data builder
public class UserBuilder {
    private String id = "default-id";
    private String name = "Default Name";
    private String email = "default@example.com";
    private int age = 25;
    private String phone = "123-456-7890";
    private boolean active = true;
    
    public UserBuilder withId(String id) {
        this.id = id;
        return this;
    }
    
    public UserBuilder withName(String name) {
        this.name = name;
        return this;
    }
    
    public UserBuilder withEmail(String email) {
        this.email = email;
        return this;
    }
    
    public UserBuilder withAge(int age) {
        this.age = age;
        return this;
    }
    
    public UserBuilder withPhone(String phone) {
        this.phone = phone;
        return this;
    }
    
    public UserBuilder withActive(boolean active) {
        this.active = active;
        return this;
    }
    
    public User build() {
        return new User(id, name, email, age, phone, active);
    }
    
    // Static factory methods for common scenarios
    public static UserBuilder aUser() {
        return new UserBuilder();
    }
    
    public static UserBuilder anActiveUser() {
        return new UserBuilder().withActive(true);
    }
    
    public static UserBuilder anInactiveUser() {
        return new UserBuilder().withActive(false);
    }
}

// Usage in tests
public class UserServiceTest {
    @Test
    public void testCreateUser() {
        // Arrange
        User user = UserBuilder.aUser()
            .withName("John Doe")
            .withEmail("john@example.com")
            .withAge(30)
            .build();
        
        UserService userService = new UserService();
        
        // Act
        User createdUser = userService.createUser(user);
        
        // Assert
        assertEquals("John Doe", createdUser.getName());
        assertEquals("john@example.com", createdUser.getEmail());
    }
    
    @Test
    public void testCreateInactiveUser() {
        // Arrange
        User user = UserBuilder.anInactiveUser()
            .withName("Jane Doe")
            .withEmail("jane@example.com")
            .build();
        
        UserService userService = new UserService();
        
        // Act
        User createdUser = userService.createUser(user);
        
        // Assert
        assertFalse(createdUser.isActive());
    }
}
```

## 12.3 Object Mother Pattern

The Object Mother pattern provides factory methods for creating test objects with predefined data.

### When to Use:
- When you need to create objects with complex default data
- When you want to centralize test object creation
- When you need to create objects for different test scenarios

### Real-World Analogy:
Think of a toy factory that has different production lines for different types of toys. Each line knows how to create a specific type of toy with all the right parts and features.

### Basic Implementation:
```java
// Object Mother for User
public class UserMother {
    public static User createValidUser() {
        return new User("1", "John Doe", "john@example.com", 30, "123-456-7890", true);
    }
    
    public static User createInvalidUser() {
        return new User("2", "", "invalid-email", -1, "", false);
    }
    
    public static User createAdminUser() {
        return new User("3", "Admin User", "admin@example.com", 35, "987-654-3210", true);
    }
    
    public static User createInactiveUser() {
        return new User("4", "Inactive User", "inactive@example.com", 25, "555-555-5555", false);
    }
    
    public static User createUserWithAge(int age) {
        return new User("5", "Age User", "age@example.com", age, "111-222-3333", true);
    }
    
    public static List<User> createUserList() {
        return Arrays.asList(
            createValidUser(),
            createAdminUser(),
            createInactiveUser()
        );
    }
}

// Object Mother for Order
public class OrderMother {
    public static Order createValidOrder() {
        return new Order("1", "CUSTOMER_1", Arrays.asList("ITEM_1", "ITEM_2"), 100.0, OrderStatus.PENDING);
    }
    
    public static Order createCompletedOrder() {
        return new Order("2", "CUSTOMER_2", Arrays.asList("ITEM_3"), 50.0, OrderStatus.COMPLETED);
    }
    
    public static Order createCancelledOrder() {
        return new Order("3", "CUSTOMER_3", Arrays.asList("ITEM_4"), 75.0, OrderStatus.CANCELLED);
    }
    
    public static Order createOrderWithItems(List<String> items) {
        return new Order("4", "CUSTOMER_4", items, 200.0, OrderStatus.PENDING);
    }
}

// Usage in tests
public class UserServiceTest {
    @Test
    public void testCreateValidUser() {
        // Arrange
        User user = UserMother.createValidUser();
        UserService userService = new UserService();
        
        // Act
        User createdUser = userService.createUser(user);
        
        // Assert
        assertNotNull(createdUser);
        assertEquals("John Doe", createdUser.getName());
    }
    
    @Test
    public void testCreateInvalidUser() {
        // Arrange
        User user = UserMother.createInvalidUser();
        UserService userService = new UserService();
        
        // Act & Assert
        assertThrows(ValidationException.class, () -> userService.createUser(user));
    }
}
```

## 12.4 Test Fixture Pattern

The Test Fixture pattern provides a consistent environment for tests by setting up and tearing down test data.

### When to Use:
- When you need consistent test setup
- When you want to share test data across tests
- When you need to clean up after tests

### Real-World Analogy:
Think of a laboratory setup where each experiment requires the same equipment and conditions. The lab technician sets up the equipment before each experiment and cleans up afterward.

### Basic Implementation:
```java
// Test fixture base class
public abstract class TestFixture {
    protected UserService userService;
    protected UserRepository userRepository;
    protected List<User> testUsers;
    
    @BeforeEach
    public void setUp() {
        // Set up test environment
        userRepository = new InMemoryUserRepository();
        userService = new UserService(userRepository);
        testUsers = new ArrayList<>();
        
        // Create test data
        createTestData();
    }
    
    @AfterEach
    public void tearDown() {
        // Clean up test data
        testUsers.clear();
        userRepository = null;
        userService = null;
    }
    
    protected abstract void createTestData();
    
    protected void addTestUser(User user) {
        testUsers.add(user);
        userRepository.save(user);
    }
}

// Specific test fixture
public class UserServiceTestFixture extends TestFixture {
    @Override
    protected void createTestData() {
        // Create test users
        addTestUser(new User("1", "John Doe", "john@example.com", 30, "123-456-7890", true));
        addTestUser(new User("2", "Jane Smith", "jane@example.com", 25, "987-654-3210", true));
        addTestUser(new User("3", "Bob Johnson", "bob@example.com", 35, "555-555-5555", false));
    }
    
    public User getActiveUser() {
        return testUsers.get(0);
    }
    
    public User getInactiveUser() {
        return testUsers.get(2);
    }
    
    public List<User> getAllUsers() {
        return new ArrayList<>(testUsers);
    }
}

// Test using fixture
public class UserServiceTest extends UserServiceTestFixture {
    @Test
    public void testFindActiveUsers() {
        // Act
        List<User> activeUsers = userService.findActiveUsers();
        
        // Assert
        assertEquals(2, activeUsers.size());
        assertTrue(activeUsers.stream().allMatch(User::isActive));
    }
    
    @Test
    public void testFindUserById() {
        // Arrange
        User expectedUser = getActiveUser();
        
        // Act
        User actualUser = userService.findById(expectedUser.getId());
        
        // Assert
        assertNotNull(actualUser);
        assertEquals(expectedUser.getName(), actualUser.getName());
    }
}
```

## 12.5 Page Object Pattern

The Page Object pattern encapsulates web page elements and actions, making tests more maintainable and readable.

### When to Use:
- When you're testing web applications
- When you want to encapsulate page logic
- When you need to make tests more maintainable

### Real-World Analogy:
Think of a remote control for your TV. Instead of manually pressing buttons on the TV, you use the remote control which knows how to interact with the TV and provides a simple interface.

### Basic Implementation:
```java
// Base page object
public abstract class BasePage {
    protected WebDriver driver;
    protected WebDriverWait wait;
    
    public BasePage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }
    
    protected void click(By locator) {
        wait.until(ExpectedConditions.elementToBeClickable(locator));
        driver.findElement(locator).click();
    }
    
    protected void type(By locator, String text) {
        wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
        WebElement element = driver.findElement(locator);
        element.clear();
        element.sendKeys(text);
    }
    
    protected String getText(By locator) {
        wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
        return driver.findElement(locator).getText();
    }
    
    protected boolean isElementPresent(By locator) {
        try {
            driver.findElement(locator);
            return true;
        } catch (NoSuchElementException e) {
            return false;
        }
    }
}

// Login page object
public class LoginPage extends BasePage {
    private static final By USERNAME_FIELD = By.id("username");
    private static final By PASSWORD_FIELD = By.id("password");
    private static final By LOGIN_BUTTON = By.id("login-button");
    private static final By ERROR_MESSAGE = By.className("error-message");
    
    public LoginPage(WebDriver driver) {
        super(driver);
    }
    
    public LoginPage enterUsername(String username) {
        type(USERNAME_FIELD, username);
        return this;
    }
    
    public LoginPage enterPassword(String password) {
        type(PASSWORD_FIELD, password);
        return this;
    }
    
    public HomePage clickLogin() {
        click(LOGIN_BUTTON);
        return new HomePage(driver);
    }
    
    public LoginPage clickLoginExpectingError() {
        click(LOGIN_BUTTON);
        return this;
    }
    
    public String getErrorMessage() {
        return getText(ERROR_MESSAGE);
    }
    
    public boolean isErrorMessageDisplayed() {
        return isElementPresent(ERROR_MESSAGE);
    }
}

// Home page object
public class HomePage extends BasePage {
    private static final By WELCOME_MESSAGE = By.id("welcome-message");
    private static final By USER_MENU = By.id("user-menu");
    private static final By LOGOUT_BUTTON = By.id("logout-button");
    
    public HomePage(WebDriver driver) {
        super(driver);
    }
    
    public String getWelcomeMessage() {
        return getText(WELCOME_MESSAGE);
    }
    
    public HomePage clickUserMenu() {
        click(USER_MENU);
        return this;
    }
    
    public LoginPage clickLogout() {
        click(LOGOUT_BUTTON);
        return new LoginPage(driver);
    }
}

// Test using page objects
public class LoginTest {
    private WebDriver driver;
    private LoginPage loginPage;
    
    @BeforeEach
    public void setUp() {
        driver = new ChromeDriver();
        loginPage = new LoginPage(driver);
    }
    
    @AfterEach
    public void tearDown() {
        driver.quit();
    }
    
    @Test
    public void testSuccessfulLogin() {
        // Act
        HomePage homePage = loginPage
            .enterUsername("testuser")
            .enterPassword("testpass")
            .clickLogin();
        
        // Assert
        assertEquals("Welcome, testuser!", homePage.getWelcomeMessage());
    }
    
    @Test
    public void testFailedLogin() {
        // Act
        loginPage
            .enterUsername("testuser")
            .enterPassword("wrongpass")
            .clickLoginExpectingError();
        
        // Assert
        assertTrue(loginPage.isErrorMessageDisplayed());
        assertEquals("Invalid username or password", loginPage.getErrorMessage());
    }
}
```

## 12.6 Test Strategy Pattern

The Test Strategy pattern allows you to choose different testing approaches based on the context.

### When to Use:
- When you need different testing approaches
- When you want to make tests configurable
- When you need to support multiple test environments

### Real-World Analogy:
Think of a GPS navigation system that can choose different routes based on your preferences - fastest route, scenic route, or avoiding tolls. The system adapts its strategy based on your needs.

### Basic Implementation:
```java
// Test strategy interface
public interface TestStrategy {
    void setup();
    void execute();
    void cleanup();
    boolean isApplicable(TestContext context);
}

// Unit test strategy
public class UnitTestStrategy implements TestStrategy {
    private TestContext context;
    
    public void setup() {
        // Set up unit test environment
        context.setTestType("UNIT");
        context.setMockingEnabled(true);
    }
    
    public void execute() {
        // Execute unit tests
        System.out.println("Executing unit tests...");
    }
    
    public void cleanup() {
        // Clean up unit test environment
        context.setMockingEnabled(false);
    }
    
    public boolean isApplicable(TestContext context) {
        return context.getTestType() == null || "UNIT".equals(context.getTestType());
    }
}

// Integration test strategy
public class IntegrationTestStrategy implements TestStrategy {
    private TestContext context;
    
    public void setup() {
        // Set up integration test environment
        context.setTestType("INTEGRATION");
        context.setDatabaseEnabled(true);
    }
    
    public void execute() {
        // Execute integration tests
        System.out.println("Executing integration tests...");
    }
    
    public void cleanup() {
        // Clean up integration test environment
        context.setDatabaseEnabled(false);
    }
    
    public boolean isApplicable(TestContext context) {
        return "INTEGRATION".equals(context.getTestType());
    }
}

// Test context
public class TestContext {
    private String testType;
    private boolean mockingEnabled;
    private boolean databaseEnabled;
    
    // Getters and setters
    public String getTestType() { return testType; }
    public void setTestType(String testType) { this.testType = testType; }
    public boolean isMockingEnabled() { return mockingEnabled; }
    public void setMockingEnabled(boolean mockingEnabled) { this.mockingEnabled = mockingEnabled; }
    public boolean isDatabaseEnabled() { return databaseEnabled; }
    public void setDatabaseEnabled(boolean databaseEnabled) { this.databaseEnabled = databaseEnabled; }
}

// Test strategy selector
public class TestStrategySelector {
    private List<TestStrategy> strategies;
    
    public TestStrategySelector() {
        this.strategies = Arrays.asList(
            new UnitTestStrategy(),
            new IntegrationTestStrategy()
        );
    }
    
    public TestStrategy selectStrategy(TestContext context) {
        return strategies.stream()
            .filter(strategy -> strategy.isApplicable(context))
            .findFirst()
            .orElseThrow(() -> new IllegalArgumentException("No applicable strategy found"));
    }
}
```

## 12.7 Test Template Pattern

The Test Template pattern provides a common structure for tests, reducing duplication and ensuring consistency.

### When to Use:
- When you have similar test structures
- When you want to reduce test duplication
- When you need to ensure test consistency

### Real-World Analogy:
Think of a recipe template that provides the basic structure for cooking different dishes. The template includes common steps like preparation, cooking, and serving, while allowing for specific variations.

### Basic Implementation:
```java
// Test template base class
public abstract class TestTemplate {
    protected TestContext context;
    
    public final void runTest() {
        setup();
        try {
            executeTest();
        } finally {
            cleanup();
        }
    }
    
    protected void setup() {
        context = new TestContext();
        initializeTestData();
        configureTestEnvironment();
    }
    
    protected abstract void executeTest();
    
    protected void cleanup() {
        if (context != null) {
            context.cleanup();
        }
    }
    
    protected abstract void initializeTestData();
    
    protected abstract void configureTestEnvironment();
}

// Specific test template
public class UserServiceTestTemplate extends TestTemplate {
    private UserService userService;
    private UserRepository userRepository;
    
    @Override
    protected void initializeTestData() {
        userRepository = new InMemoryUserRepository();
        userService = new UserService(userRepository);
    }
    
    @Override
    protected void configureTestEnvironment() {
        context.setTestType("UNIT");
        context.setMockingEnabled(true);
    }
    
    @Override
    protected void executeTest() {
        // This will be implemented by concrete test classes
        performTest();
    }
    
    protected abstract void performTest();
}

// Concrete test implementation
public class CreateUserTest extends UserServiceTestTemplate {
    @Override
    protected void performTest() {
        // Arrange
        User user = new User("1", "John Doe", "john@example.com", 30, "123-456-7890", true);
        
        // Act
        User createdUser = userService.createUser(user);
        
        // Assert
        assertNotNull(createdUser);
        assertEquals("John Doe", createdUser.getName());
        assertEquals("john@example.com", createdUser.getEmail());
    }
}

// Another concrete test implementation
public class UpdateUserTest extends UserServiceTestTemplate {
    @Override
    protected void performTest() {
        // Arrange
        User user = new User("1", "John Doe", "john@example.com", 30, "123-456-7890", true);
        userService.createUser(user);
        
        // Act
        user.setName("Jane Doe");
        User updatedUser = userService.updateUser(user);
        
        // Assert
        assertEquals("Jane Doe", updatedUser.getName());
    }
}
```

## 12.8 Test Observer Pattern

The Test Observer pattern allows tests to observe and react to test events, enabling better test reporting and debugging.

### When to Use:
- When you need to monitor test execution
- When you want to implement test reporting
- When you need to debug test failures

### Real-World Analogy:
Think of a security camera system that monitors a building. The cameras observe events and can trigger alarms or record footage when something happens.

### Basic Implementation:
```java
// Test observer interface
public interface TestObserver {
    void onTestStarted(TestEvent event);
    void onTestCompleted(TestEvent event);
    void onTestFailed(TestEvent event);
    void onTestSkipped(TestEvent event);
}

// Test event
public class TestEvent {
    private String testName;
    private long startTime;
    private long endTime;
    private Throwable error;
    private Map<String, Object> metadata;
    
    public TestEvent(String testName) {
        this.testName = testName;
        this.startTime = System.currentTimeMillis();
        this.metadata = new HashMap<>();
    }
    
    // Getters and setters
    public String getTestName() { return testName; }
    public long getStartTime() { return startTime; }
    public long getEndTime() { return endTime; }
    public void setEndTime(long endTime) { this.endTime = endTime; }
    public Throwable getError() { return error; }
    public void setError(Throwable error) { this.error = error; }
    public Map<String, Object> getMetadata() { return metadata; }
}

// Test logger observer
public class TestLoggerObserver implements TestObserver {
    private Logger logger = LoggerFactory.getLogger(TestLoggerObserver.class);
    
    public void onTestStarted(TestEvent event) {
        logger.info("Test started: " + event.getTestName());
    }
    
    public void onTestCompleted(TestEvent event) {
        long duration = event.getEndTime() - event.getStartTime();
        logger.info("Test completed: " + event.getTestName() + " (duration: " + duration + "ms)");
    }
    
    public void onTestFailed(TestEvent event) {
        logger.error("Test failed: " + event.getTestName(), event.getError());
    }
    
    public void onTestSkipped(TestEvent event) {
        logger.warn("Test skipped: " + event.getTestName());
    }
}

// Test reporter observer
public class TestReporterObserver implements TestObserver {
    private List<TestEvent> testEvents = new ArrayList<>();
    
    public void onTestStarted(TestEvent event) {
        // Record test start
    }
    
    public void onTestCompleted(TestEvent event) {
        event.setEndTime(System.currentTimeMillis());
        testEvents.add(event);
    }
    
    public void onTestFailed(TestEvent event) {
        event.setEndTime(System.currentTimeMillis());
        testEvents.add(event);
    }
    
    public void onTestSkipped(TestEvent event) {
        event.setEndTime(System.currentTimeMillis());
        testEvents.add(event);
    }
    
    public TestReport generateReport() {
        return new TestReport(testEvents);
    }
}

// Test runner with observers
public class TestRunner {
    private List<TestObserver> observers = new ArrayList<>();
    
    public void addObserver(TestObserver observer) {
        observers.add(observer);
    }
    
    public void removeObserver(TestObserver observer) {
        observers.remove(observer);
    }
    
    public void runTest(TestTemplate test) {
        TestEvent event = new TestEvent(test.getClass().getSimpleName());
        
        try {
            notifyObservers(observer -> observer.onTestStarted(event));
            test.runTest();
            notifyObservers(observer -> observer.onTestCompleted(event));
        } catch (Exception e) {
            event.setError(e);
            notifyObservers(observer -> observer.onTestFailed(event));
        }
    }
    
    private void notifyObservers(Consumer<TestObserver> notification) {
        observers.forEach(notification);
    }
}
```

## 12.9 Test Command Pattern

The Test Command pattern encapsulates test operations as objects, allowing you to parameterize, queue, and log test operations.

### When to Use:
- When you need to parameterize test operations
- When you want to queue test operations
- When you need to support undo/redo functionality

### Real-World Analogy:
Think of a remote control that can store commands. You can program the remote to execute a series of commands, and it will execute them in sequence, allowing you to automate complex operations.

### Basic Implementation:
```java
// Test command interface
public interface TestCommand {
    void execute();
    void undo();
    String getDescription();
}

// Create user command
public class CreateUserCommand implements TestCommand {
    private UserService userService;
    private User user;
    private User createdUser;
    
    public CreateUserCommand(UserService userService, User user) {
        this.userService = userService;
        this.user = user;
    }
    
    public void execute() {
        createdUser = userService.createUser(user);
    }
    
    public void undo() {
        if (createdUser != null) {
            userService.deleteUser(createdUser.getId());
        }
    }
    
    public String getDescription() {
        return "Create user: " + user.getName();
    }
}

// Update user command
public class UpdateUserCommand implements TestCommand {
    private UserService userService;
    private User originalUser;
    private User updatedUser;
    private User previousUser;
    
    public UpdateUserCommand(UserService userService, User updatedUser) {
        this.userService = userService;
        this.updatedUser = updatedUser;
    }
    
    public void execute() {
        originalUser = userService.findById(updatedUser.getId());
        previousUser = new User(originalUser); // Create copy
        userService.updateUser(updatedUser);
    }
    
    public void undo() {
        if (previousUser != null) {
            userService.updateUser(previousUser);
        }
    }
    
    public String getDescription() {
        return "Update user: " + updatedUser.getName();
    }
}

// Test command invoker
public class TestCommandInvoker {
    private List<TestCommand> commandHistory = new ArrayList<>();
    private int currentIndex = -1;
    
    public void executeCommand(TestCommand command) {
        command.execute();
        commandHistory.add(command);
        currentIndex++;
    }
    
    public void undo() {
        if (currentIndex >= 0) {
            TestCommand command = commandHistory.get(currentIndex);
            command.undo();
            currentIndex--;
        }
    }
    
    public void redo() {
        if (currentIndex < commandHistory.size() - 1) {
            currentIndex++;
            TestCommand command = commandHistory.get(currentIndex);
            command.execute();
        }
    }
    
    public List<String> getCommandHistory() {
        return commandHistory.stream()
            .map(TestCommand::getDescription)
            .collect(Collectors.toList());
    }
}

// Usage in tests
public class UserServiceTest {
    private TestCommandInvoker commandInvoker;
    private UserService userService;
    
    @BeforeEach
    public void setUp() {
        commandInvoker = new TestCommandInvoker();
        userService = new UserService(new InMemoryUserRepository());
    }
    
    @Test
    public void testCreateAndUpdateUser() {
        // Arrange
        User user = new User("1", "John Doe", "john@example.com", 30, "123-456-7890", true);
        
        // Act
        commandInvoker.executeCommand(new CreateUserCommand(userService, user));
        
        User updatedUser = new User("1", "Jane Doe", "jane@example.com", 25, "987-654-3210", true);
        commandInvoker.executeCommand(new UpdateUserCommand(userService, updatedUser));
        
        // Assert
        User result = userService.findById("1");
        assertEquals("Jane Doe", result.getName());
        assertEquals("jane@example.com", result.getEmail());
    }
}
```

## 12.10 Test Factory Pattern

The Test Factory pattern creates test objects and test scenarios, providing a centralized way to generate test data.

### When to Use:
- When you need to create complex test scenarios
- When you want to centralize test object creation
- When you need to generate test data dynamically

### Real-World Analogy:
Think of a toy factory that can produce different types of toys based on specifications. The factory knows how to create each type of toy and can produce them on demand.

### Basic Implementation:
```java
// Test factory interface
public interface TestFactory<T> {
    T create();
    T createWithDefaults();
    T createWithCustomizations(Map<String, Object> customizations);
}

// User test factory
public class UserTestFactory implements TestFactory<User> {
    private Random random = new Random();
    
    public User create() {
        return createWithDefaults();
    }
    
    public User createWithDefaults() {
        return new User(
            generateId(),
            generateName(),
            generateEmail(),
            generateAge(),
            generatePhone(),
            true
        );
    }
    
    public User createWithCustomizations(Map<String, Object> customizations) {
        User user = createWithDefaults();
        
        if (customizations.containsKey("name")) {
            user.setName((String) customizations.get("name"));
        }
        if (customizations.containsKey("email")) {
            user.setEmail((String) customizations.get("email"));
        }
        if (customizations.containsKey("age")) {
            user.setAge((Integer) customizations.get("age"));
        }
        if (customizations.containsKey("active")) {
            user.setActive((Boolean) customizations.get("active"));
        }
        
        return user;
    }
    
    private String generateId() {
        return "user_" + random.nextInt(1000);
    }
    
    private String generateName() {
        String[] firstNames = {"John", "Jane", "Bob", "Alice", "Charlie"};
        String[] lastNames = {"Doe", "Smith", "Johnson", "Brown", "Wilson"};
        return firstNames[random.nextInt(firstNames.length)] + " " + 
               lastNames[random.nextInt(lastNames.length)];
    }
    
    private String generateEmail() {
        return "user" + random.nextInt(1000) + "@example.com";
    }
    
    private int generateAge() {
        return 18 + random.nextInt(50);
    }
    
    private String generatePhone() {
        return String.format("%03d-%03d-%04d", 
            random.nextInt(1000), random.nextInt(1000), random.nextInt(10000));
    }
}

// Test scenario factory
public class TestScenarioFactory {
    private UserTestFactory userFactory;
    
    public TestScenarioFactory() {
        this.userFactory = new UserTestFactory();
    }
    
    public TestScenario createValidUserScenario() {
        return new TestScenario()
            .addStep("Create valid user", () -> userFactory.create())
            .addStep("Verify user creation", user -> {
                assertNotNull(user);
                assertTrue(user.isActive());
            });
    }
    
    public TestScenario createInvalidUserScenario() {
        return new TestScenario()
            .addStep("Create invalid user", () -> {
                Map<String, Object> customizations = new HashMap<>();
                customizations.put("name", "");
                customizations.put("email", "invalid-email");
                return userFactory.createWithCustomizations(customizations);
            })
            .addStep("Verify validation failure", user -> {
                assertThrows(ValidationException.class, () -> {
                    // Attempt to save invalid user
                });
            });
    }
    
    public TestScenario createUserWithAgeScenario(int age) {
        return new TestScenario()
            .addStep("Create user with age " + age, () -> {
                Map<String, Object> customizations = new HashMap<>();
                customizations.put("age", age);
                return userFactory.createWithCustomizations(customizations);
            })
            .addStep("Verify age", user -> {
                assertEquals(age, user.getAge());
            });
    }
}

// Test scenario
public class TestScenario {
    private List<TestStep> steps = new ArrayList<>();
    
    public TestScenario addStep(String description, TestStep step) {
        steps.add(step);
        return this;
    }
    
    public void execute() {
        for (TestStep step : steps) {
            step.execute();
        }
    }
}

// Test step interface
public interface TestStep {
    void execute();
}

// Usage in tests
public class UserServiceTest {
    private TestScenarioFactory scenarioFactory;
    private UserService userService;
    
    @BeforeEach
    public void setUp() {
        scenarioFactory = new TestScenarioFactory();
        userService = new UserService(new InMemoryUserRepository());
    }
    
    @Test
    public void testValidUserScenario() {
        TestScenario scenario = scenarioFactory.createValidUserScenario();
        scenario.execute();
    }
    
    @Test
    public void testInvalidUserScenario() {
        TestScenario scenario = scenarioFactory.createInvalidUserScenario();
        scenario.execute();
    }
}
```

This comprehensive coverage of testing patterns provides the foundation for building robust, maintainable test suites. Each pattern addresses specific testing challenges and offers different approaches to organizing and executing tests.