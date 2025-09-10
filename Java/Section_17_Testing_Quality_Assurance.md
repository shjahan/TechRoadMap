# Section 17 - Testing & Quality Assurance

## 17.1 Unit Testing with JUnit

Unit Testing with JUnit یکی از مهم‌ترین جنبه‌های Quality Assurance در Java است.

### مفاهیم کلیدی:

**1. JUnit Framework:**
- Test annotations
- Assertions
- Test lifecycle
- Test runners

**2. Test Structure:**
- Arrange-Act-Assert (AAA)
- Test methods
- Setup and teardown
- Test data

**3. Best Practices:**
- Test isolation
- Descriptive names
- Single responsibility
- Fast execution

### مثال عملی:

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorTest {
    private Calculator calculator;
    
    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }
    
    @Test
    @DisplayName("Addition should return correct result")
    void testAddition() {
        // Arrange
        int a = 5;
        int b = 3;
        int expected = 8;
        
        // Act
        int result = calculator.add(a, b);
        
        // Assert
        assertEquals(expected, result);
    }
    
    @Test
    @DisplayName("Division by zero should throw exception")
    void testDivisionByZero() {
        // Arrange
        int a = 10;
        int b = 0;
        
        // Act & Assert
        assertThrows(ArithmeticException.class, () -> {
            calculator.divide(a, b);
        });
    }
    
    @Test
    @DisplayName("Multiple test cases for subtraction")
    @ParameterizedTest
    @ValueSource(ints = {5, 10, 15, 20})
    void testSubtraction(int value) {
        // Arrange
        int expected = value - 2;
        
        // Act
        int result = calculator.subtract(value, 2);
        
        // Assert
        assertEquals(expected, result);
    }
    
    @AfterEach
    void tearDown() {
        calculator = null;
    }
}

class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    public int subtract(int a, int b) {
        return a - b;
    }
    
    public int divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Division by zero");
        }
        return a / b;
    }
}
```

### آنالوژی دنیای واقعی:
Unit Testing مانند داشتن یک سیستم کنترل کیفیت در کارخانه است که:
- **Test Cases:** مانند آزمایش‌های مختلف برای هر محصول
- **Assertions:** مانند استانداردهای کیفیت که باید رعایت شوند
- **Setup/Teardown:** مانند آماده‌سازی و تمیز کردن محیط آزمایش

## 17.2 Integration Testing

Integration Testing تست‌هایی هستند که چندین component را با هم تست می‌کنند.

### مفاهیم کلیدی:

**1. Integration Test Types:**
- Component integration
- System integration
- End-to-end testing
- API testing

**2. Test Environment:**
- Test databases
- Mock services
- Test containers
- Configuration management

**3. Test Data:**
- Test fixtures
- Data setup
- Data cleanup
- Test isolation

### مثال عملی:

```java
@SpringBootTest
@TestPropertySource(properties = {
    "spring.datasource.url=jdbc:h2:mem:testdb",
    "spring.jpa.hibernate.ddl-auto=create-drop"
})
class UserServiceIntegrationTest {
    @Autowired
    private UserService userService;
    
    @Autowired
    private UserRepository userRepository;
    
    @Test
    @Transactional
    void testCreateUser() {
        // Arrange
        String name = "احمد محمدی";
        String email = "ahmad@example.com";
        
        // Act
        User user = userService.createUser(name, email);
        
        // Assert
        assertNotNull(user.getId());
        assertEquals(name, user.getName());
        assertEquals(email, user.getEmail());
        
        // Verify database
        User savedUser = userRepository.findById(user.getId()).orElse(null);
        assertNotNull(savedUser);
        assertEquals(name, savedUser.getName());
    }
    
    @Test
    @Transactional
    void testFindUserById() {
        // Arrange
        User user = new User("فاطمه احمدی", "fateme@example.com");
        user = userRepository.save(user);
        
        // Act
        User foundUser = userService.findById(user.getId());
        
        // Assert
        assertNotNull(foundUser);
        assertEquals(user.getId(), foundUser.getId());
        assertEquals(user.getName(), foundUser.getName());
    }
}
```

### آنالوژی دنیای واقعی:
Integration Testing مانند تست کردن سیستم‌های مختلف یک کارخانه با هم است.

## 17.3 Mocking Frameworks (Mockito)

Mocking Frameworks ابزارهایی برای ایجاد mock objects در تست‌ها هستند.

### مفاهیم کلیدی:

**1. Mock Objects:**
- Fake implementations
- Behavior verification
- Interaction testing
- Isolation

**2. Mockito Features:**
- Mock creation
- Stubbing
- Verification
- Argument matchers

**3. Best Practices:**
- Mock external dependencies
- Verify interactions
- Use realistic data
- Keep mocks simple

### مثال عملی:

```java
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.mockito.Mockito.*;

public class UserServiceTest {
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private EmailService emailService;
    
    private UserService userService;
    
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        userService = new UserService(userRepository, emailService);
    }
    
    @Test
    void testCreateUser() {
        // Arrange
        String name = "احمد محمدی";
        String email = "ahmad@example.com";
        User user = new User(name, email);
        
        when(userRepository.save(any(User.class))).thenReturn(user);
        
        // Act
        User result = userService.createUser(name, email);
        
        // Assert
        assertNotNull(result);
        assertEquals(name, result.getName());
        assertEquals(email, result.getEmail());
        
        // Verify interactions
        verify(userRepository).save(any(User.class));
        verify(emailService).sendWelcomeEmail(email);
    }
    
    @Test
    void testFindUserById() {
        // Arrange
        Long userId = 1L;
        User user = new User("احمد محمدی", "ahmad@example.com");
        when(userRepository.findById(userId)).thenReturn(Optional.of(user));
        
        // Act
        User result = userService.findById(userId);
        
        // Assert
        assertNotNull(result);
        assertEquals(userId, result.getId());
        verify(userRepository).findById(userId);
    }
    
    @Test
    void testCreateUserWithDuplicateEmail() {
        // Arrange
        String name = "احمد محمدی";
        String email = "ahmad@example.com";
        
        when(userRepository.findByEmail(email)).thenReturn(Optional.of(new User()));
        
        // Act & Assert
        assertThrows(DuplicateEmailException.class, () -> {
            userService.createUser(name, email);
        });
        
        verify(userRepository).findByEmail(email);
        verify(userRepository, never()).save(any(User.class));
    }
}
```

### آنالوژی دنیای واقعی:
Mocking Frameworks مانند داشتن یک سیستم شبیه‌سازی هوشمند است.

## 17.4 Test-Driven Development (TDD)

Test-Driven Development یک روش توسعه نرم‌افزار است که تست‌ها قبل از کد نوشته می‌شوند.

### مفاهیم کلیدی:

**1. TDD Cycle:**
- Red (Write failing test)
- Green (Write minimal code)
- Refactor (Improve code)

**2. Benefits:**
- Better design
- Higher quality
- Faster feedback
- Documentation

**3. Best Practices:**
- Write tests first
- Keep tests simple
- Refactor regularly
- Maintain test suite

### مثال عملی:

```java
// Step 1: Red - Write failing test
public class BankAccountTest {
    @Test
    void testDeposit() {
        BankAccount account = new BankAccount();
        account.deposit(100);
        assertEquals(100, account.getBalance());
    }
}

// Step 2: Green - Write minimal code
public class BankAccount {
    private double balance;
    
    public void deposit(double amount) {
        balance += amount;
    }
    
    public double getBalance() {
        return balance;
    }
}

// Step 3: Refactor - Improve code
public class BankAccount {
    private double balance;
    
    public void deposit(double amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        balance += amount;
    }
    
    public double getBalance() {
        return balance;
    }
}
```

### آنالوژی دنیای واقعی:
TDD مانند داشتن یک نقشه قبل از شروع سفر است.

## 17.5 Behavior-Driven Development (BDD)

Behavior-Driven Development یک روش توسعه است که بر روی behavior تمرکز می‌کند.

### مفاهیم کلیدی:

**1. BDD Structure:**
- Given (Preconditions)
- When (Action)
- Then (Expected result)

**2. BDD Tools:**
- Cucumber
- JBehave
- SpecFlow
- Gherkin syntax

**3. Benefits:**
- Business alignment
- Better communication
- Living documentation
- User-focused

### مثال عملی:

```java
// Feature file
@Given("a bank account with balance {double}")
public void aBankAccountWithBalance(double balance) {
    account = new BankAccount(balance);
}

@When("I deposit {double}")
public void iDeposit(double amount) {
    account.deposit(amount);
}

@Then("the balance should be {double}")
public void theBalanceShouldBe(double expectedBalance) {
    assertEquals(expectedBalance, account.getBalance());
}

@Given("a bank account with balance {double}")
public void aBankAccountWithBalance(double balance) {
    account = new BankAccount(balance);
}

@When("I withdraw {double}")
public void iWithdraw(double amount) {
    account.withdraw(amount);
}

@Then("the balance should be {double}")
public void theBalanceShouldBe(double expectedBalance) {
    assertEquals(expectedBalance, account.getBalance());
}
```

### آنالوژی دنیای واقعی:
BDD مانند داشتن یک قرارداد کاری است که همه طرف‌ها آن را می‌فهمند.

## 17.6 Performance Testing

Performance Testing تست‌هایی هستند که عملکرد سیستم را بررسی می‌کنند.

### مفاهیم کلیدی:

**1. Performance Metrics:**
- Response time
- Throughput
- Resource usage
- Scalability

**2. Test Types:**
- Load testing
- Stress testing
- Volume testing
- Spike testing

**3. Tools:**
- JMeter
- Gatling
- LoadRunner
- Custom tools

### مثال عملی:

```java
@Test
@Timeout(value = 5, unit = TimeUnit.SECONDS)
void testPerformance() {
    long startTime = System.currentTimeMillis();
    
    // Perform operation
    for (int i = 0; i < 1000000; i++) {
        calculator.add(i, i + 1);
    }
    
    long endTime = System.currentTimeMillis();
    long duration = endTime - startTime;
    
    assertTrue(duration < 1000, "Operation took too long: " + duration + "ms");
}
```

### آنالوژی دنیای واقعی:
Performance Testing مانند تست کردن سرعت و کارایی یک ماشین است.

## 17.7 Code Quality & Static Analysis

Code Quality & Static Analysis ابزارهایی برای بررسی کیفیت کد هستند.

### مفاهیم کلیدی:

**1. Code Quality Metrics:**
- Cyclomatic complexity
- Code coverage
- Duplication
- Maintainability

**2. Static Analysis Tools:**
- SonarQube
- SpotBugs
- PMD
- Checkstyle

**3. Best Practices:**
- Regular analysis
- Quality gates
- Continuous monitoring
- Team standards

### مثال عملی:

```java
// Good quality code
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
    
    public UserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }
    
    public User createUser(String name, String email) {
        validateUserData(name, email);
        User user = new User(name, email);
        User savedUser = userRepository.save(user);
        emailService.sendWelcomeEmail(email);
        return savedUser;
    }
    
    private void validateUserData(String name, String email) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Name cannot be empty");
        }
        if (email == null || !email.contains("@")) {
            throw new IllegalArgumentException("Invalid email format");
        }
    }
}
```

### آنالوژی دنیای واقعی:
Code Quality & Static Analysis مانند داشتن یک سیستم کنترل کیفیت خودکار است.