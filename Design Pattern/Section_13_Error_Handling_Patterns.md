# Section 13 - Error Handling Patterns

## 13.1 Exception Handling Patterns

Exception handling patterns provide structured approaches to managing errors and exceptions in applications.

### When to Use:
- When you need to handle errors gracefully
- When you want to provide meaningful error messages
- When you need to log and monitor errors

### Real-World Analogy:
Think of a fire safety system in a building. When a fire is detected, the system doesn't just let it burn - it triggers alarms, notifies authorities, and activates sprinklers to contain the damage.

### Basic Implementation:
```java
// Exception hierarchy
public class ApplicationException extends Exception {
    private String errorCode;
    private Map<String, Object> context;
    
    public ApplicationException(String message, String errorCode) {
        super(message);
        this.errorCode = errorCode;
        this.context = new HashMap<>();
    }
    
    public ApplicationException(String message, String errorCode, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
        this.context = new HashMap<>();
    }
    
    public String getErrorCode() { return errorCode; }
    public Map<String, Object> getContext() { return context; }
    
    public ApplicationException addContext(String key, Object value) {
        context.put(key, value);
        return this;
    }
}

// Specific exception types
public class ValidationException extends ApplicationException {
    public ValidationException(String message) {
        super(message, "VALIDATION_ERROR");
    }
}

public class BusinessException extends ApplicationException {
    public BusinessException(String message) {
        super(message, "BUSINESS_ERROR");
    }
}

public class TechnicalException extends ApplicationException {
    public TechnicalException(String message, Throwable cause) {
        super(message, "TECHNICAL_ERROR", cause);
    }
}

// Exception handler
public class ExceptionHandler {
    private Logger logger;
    private ErrorReporter errorReporter;
    
    public ExceptionHandler(Logger logger, ErrorReporter errorReporter) {
        this.logger = logger;
        this.errorReporter = errorReporter;
    }
    
    public <T> T handle(Supplier<T> operation, T defaultValue) {
        try {
            return operation.get();
        } catch (ApplicationException e) {
            handleApplicationException(e);
            return defaultValue;
        } catch (Exception e) {
            handleUnexpectedException(e);
            return defaultValue;
        }
    }
    
    public void handle(Runnable operation) {
        try {
            operation.run();
        } catch (ApplicationException e) {
            handleApplicationException(e);
        } catch (Exception e) {
            handleUnexpectedException(e);
        }
    }
    
    private void handleApplicationException(ApplicationException e) {
        logger.error("Application error: " + e.getMessage(), e);
        errorReporter.reportError(e);
    }
    
    private void handleUnexpectedException(Exception e) {
        logger.error("Unexpected error: " + e.getMessage(), e);
        errorReporter.reportError(new TechnicalException("Unexpected error", e));
    }
}
```

## 13.2 Error Recovery Patterns

Error recovery patterns provide mechanisms to recover from errors and continue system operation.

### When to Use:
- When you need to recover from transient errors
- When you want to implement automatic retry logic
- When you need to maintain system availability

### Real-World Analogy:
Think of a car's automatic transmission that can shift gears when it encounters resistance. If it can't shift to a higher gear, it tries a lower gear to maintain forward motion.

### Basic Implementation:
```java
// Error recovery strategy interface
public interface ErrorRecoveryStrategy {
    boolean canRecover(Throwable error);
    void recover(Throwable error) throws Exception;
}

// Retry strategy
public class RetryStrategy implements ErrorRecoveryStrategy {
    private int maxRetries;
    private long delayMillis;
    private Class<? extends Exception>[] retryableExceptions;
    
    @SafeVarargs
    public RetryStrategy(int maxRetries, long delayMillis, Class<? extends Exception>... retryableExceptions) {
        this.maxRetries = maxRetries;
        this.delayMillis = delayMillis;
        this.retryableExceptions = retryableExceptions;
    }
    
    public boolean canRecover(Throwable error) {
        if (retryableExceptions.length == 0) {
            return true;
        }
        
        for (Class<? extends Exception> exceptionClass : retryableExceptions) {
            if (exceptionClass.isInstance(error)) {
                return true;
            }
        }
        return false;
    }
    
    public void recover(Throwable error) throws Exception {
        // Retry logic is handled by the caller
        throw new RuntimeException("Retry needed", error);
    }
}

// Fallback strategy
public class FallbackStrategy implements ErrorRecoveryStrategy {
    private Supplier<Object> fallbackSupplier;
    
    public FallbackStrategy(Supplier<Object> fallbackSupplier) {
        this.fallbackSupplier = fallbackSupplier;
    }
    
    public boolean canRecover(Throwable error) {
        return true;
    }
    
    public void recover(Throwable error) throws Exception {
        // Fallback logic is handled by the caller
        throw new RuntimeException("Fallback needed", error);
    }
}

// Error recovery manager
public class ErrorRecoveryManager {
    private List<ErrorRecoveryStrategy> strategies;
    private Logger logger;
    
    public ErrorRecoveryManager(Logger logger) {
        this.strategies = new ArrayList<>();
        this.logger = logger;
    }
    
    public void addStrategy(ErrorRecoveryStrategy strategy) {
        strategies.add(strategy);
    }
    
    public <T> T executeWithRecovery(Supplier<T> operation, T defaultValue) {
        for (ErrorRecoveryStrategy strategy : strategies) {
            try {
                return operation.get();
            } catch (Exception e) {
                if (strategy.canRecover(e)) {
                    logger.warn("Attempting recovery for error: " + e.getMessage());
                    try {
                        strategy.recover(e);
                        return operation.get(); // Retry
                    } catch (Exception recoveryError) {
                        logger.error("Recovery failed: " + recoveryError.getMessage());
                        continue; // Try next strategy
                    }
                }
            }
        }
        
        logger.error("All recovery strategies failed, using default value");
        return defaultValue;
    }
}
```

## 13.3 Circuit Breaker Pattern

The Circuit Breaker pattern prevents cascading failures by stopping calls to failing services.

### When to Use:
- When you have external service dependencies
- When you want to prevent cascading failures
- When you need to provide fallback behavior

### Real-World Analogy:
Think of an electrical circuit breaker in your home. When there's too much current (indicating a problem), the breaker trips to prevent damage to the electrical system.

### Basic Implementation:
```java
// Circuit breaker interface
public interface CircuitBreaker {
    <T> T execute(Supplier<T> operation) throws Exception;
    void reset();
    CircuitState getState();
}

// Circuit breaker states
public enum CircuitState {
    CLOSED,    // Normal operation
    OPEN,      // Circuit is open, calls fail fast
    HALF_OPEN  // Testing if service is back
}

// Simple circuit breaker
public class SimpleCircuitBreaker implements CircuitBreaker {
    private int failureThreshold;
    private long timeoutMillis;
    private int failureCount;
    private long lastFailureTime;
    private CircuitState state;
    
    public SimpleCircuitBreaker(int failureThreshold, long timeoutMillis) {
        this.failureThreshold = failureThreshold;
        this.timeoutMillis = timeoutMillis;
        this.state = CircuitState.CLOSED;
    }
    
    public <T> T execute(Supplier<T> operation) throws Exception {
        if (state == CircuitState.OPEN) {
            if (System.currentTimeMillis() - lastFailureTime > timeoutMillis) {
                state = CircuitState.HALF_OPEN;
            } else {
                throw new CircuitBreakerOpenException("Circuit breaker is open");
            }
        }
        
        try {
            T result = operation.get();
            onSuccess();
            return result;
        } catch (Exception e) {
            onFailure();
            throw e;
        }
    }
    
    private void onSuccess() {
        failureCount = 0;
        state = CircuitState.CLOSED;
    }
    
    private void onFailure() {
        failureCount++;
        lastFailureTime = System.currentTimeMillis();
        
        if (failureCount >= failureThreshold) {
            state = CircuitState.OPEN;
        }
    }
    
    public void reset() {
        failureCount = 0;
        state = CircuitState.CLOSED;
    }
    
    public CircuitState getState() {
        return state;
    }
}

// Circuit breaker with fallback
public class CircuitBreakerWithFallback<T> {
    private CircuitBreaker circuitBreaker;
    private Supplier<T> fallback;
    
    public CircuitBreakerWithFallback(CircuitBreaker circuitBreaker, Supplier<T> fallback) {
        this.circuitBreaker = circuitBreaker;
        this.fallback = fallback;
    }
    
    public T execute(Supplier<T> operation) {
        try {
            return circuitBreaker.execute(operation);
        } catch (Exception e) {
            return fallback.get();
        }
    }
}
```

## 13.4 Retry Pattern

The Retry pattern automatically retries failed operations, often with exponential backoff.

### When to Use:
- When you have transient failures
- When you want to improve system reliability
- When you need to handle temporary service unavailability

### Real-World Analogy:
Think of a persistent salesperson who doesn't give up after the first "no." They try different approaches, wait a bit, and try again, increasing their chances of success.

### Basic Implementation:
```java
// Retry configuration
public class RetryConfig {
    private int maxAttempts;
    private long initialDelayMillis;
    private long maxDelayMillis;
    private double backoffMultiplier;
    private Class<? extends Exception>[] retryableExceptions;
    
    @SafeVarargs
    public RetryConfig(int maxAttempts, long initialDelayMillis, long maxDelayMillis, 
                      double backoffMultiplier, Class<? extends Exception>... retryableExceptions) {
        this.maxAttempts = maxAttempts;
        this.initialDelayMillis = initialDelayMillis;
        this.maxDelayMillis = maxDelayMillis;
        this.backoffMultiplier = backoffMultiplier;
        this.retryableExceptions = retryableExceptions;
    }
    
    // Getters
    public int getMaxAttempts() { return maxAttempts; }
    public long getInitialDelayMillis() { return initialDelayMillis; }
    public long getMaxDelayMillis() { return maxDelayMillis; }
    public double getBackoffMultiplier() { return backoffMultiplier; }
    public Class<? extends Exception>[] getRetryableExceptions() { return retryableExceptions; }
}

// Retry executor
public class RetryExecutor {
    private RetryConfig config;
    private Logger logger;
    
    public RetryExecutor(RetryConfig config, Logger logger) {
        this.config = config;
        this.logger = logger;
    }
    
    public <T> T execute(Supplier<T> operation) throws Exception {
        Exception lastException = null;
        long delay = config.getInitialDelayMillis();
        
        for (int attempt = 1; attempt <= config.getMaxAttempts(); attempt++) {
            try {
                return operation.get();
            } catch (Exception e) {
                lastException = e;
                
                if (!isRetryable(e) || attempt == config.getMaxAttempts()) {
                    throw e;
                }
                
                logger.warn("Attempt " + attempt + " failed, retrying in " + delay + "ms", e);
                Thread.sleep(delay);
                delay = Math.min(delay * (long) config.getBackoffMultiplier(), config.getMaxDelayMillis());
            }
        }
        
        throw lastException;
    }
    
    private boolean isRetryable(Exception e) {
        if (config.getRetryableExceptions().length == 0) {
            return true;
        }
        
        for (Class<? extends Exception> exceptionClass : config.getRetryableExceptions()) {
            if (exceptionClass.isInstance(e)) {
                return true;
            }
        }
        return false;
    }
}

// Usage example
public class UserService {
    private RetryExecutor retryExecutor;
    private UserRepository userRepository;
    
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
        this.retryExecutor = new RetryExecutor(
            new RetryConfig(3, 1000, 10000, 2.0, SQLException.class),
            LoggerFactory.getLogger(UserService.class)
        );
    }
    
    public User findById(String id) throws Exception {
        return retryExecutor.execute(() -> userRepository.findById(id));
    }
}
```

## 13.5 Timeout Pattern

The Timeout pattern limits the time allowed for operations to complete, preventing indefinite waits.

### When to Use:
- When you have operations that might hang
- When you want to prevent resource exhaustion
- When you need to provide responsive user experience

### Real-World Analogy:
Think of a parking meter that gives you a limited time to park. If you exceed the time limit, you get a ticket, preventing you from occupying the space indefinitely.

### Basic Implementation:
```java
// Timeout executor
public class TimeoutExecutor {
    private long timeoutMillis;
    private ExecutorService executor;
    
    public TimeoutExecutor(long timeoutMillis) {
        this.timeoutMillis = timeoutMillis;
        this.executor = Executors.newCachedThreadPool();
    }
    
    public <T> T execute(Supplier<T> operation) throws TimeoutException, Exception {
        Future<T> future = executor.submit(operation::get);
        
        try {
            return future.get(timeoutMillis, TimeUnit.MILLISECONDS);
        } catch (java.util.concurrent.TimeoutException e) {
            future.cancel(true);
            throw new TimeoutException("Operation timed out after " + timeoutMillis + "ms");
        }
    }
    
    public void execute(Runnable operation) throws TimeoutException, Exception {
        Future<?> future = executor.submit(operation);
        
        try {
            future.get(timeoutMillis, TimeUnit.MILLISECONDS);
        } catch (java.util.concurrent.TimeoutException e) {
            future.cancel(true);
            throw new TimeoutException("Operation timed out after " + timeoutMillis + "ms");
        }
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}

// Timeout decorator
public class TimeoutDecorator<T> {
    private T target;
    private long timeoutMillis;
    
    public TimeoutDecorator(T target, long timeoutMillis) {
        this.target = target;
        this.timeoutMillis = timeoutMillis;
    }
    
    public <R> R execute(Function<T, R> operation) throws TimeoutException, Exception {
        TimeoutExecutor executor = new TimeoutExecutor(timeoutMillis);
        return executor.execute(() -> operation.apply(target));
    }
}

// Usage example
public class UserService {
    private UserRepository userRepository;
    private TimeoutExecutor timeoutExecutor;
    
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
        this.timeoutExecutor = new TimeoutExecutor(5000); // 5 second timeout
    }
    
    public User findById(String id) throws TimeoutException, Exception {
        return timeoutExecutor.execute(() -> userRepository.findById(id));
    }
}
```

## 13.6 Bulkhead Pattern

The Bulkhead pattern isolates critical resources to prevent cascading failures.

### When to Use:
- When you want to prevent cascading failures
- When you need to isolate critical resources
- When you want to improve system resilience

### Real-World Analogy:
Think of a ship with watertight compartments. If one compartment floods, the water doesn't spread to other compartments, keeping the ship afloat.

### Basic Implementation:
```java
// Bulkhead configuration
public class BulkheadConfig {
    private int maxConcurrentCalls;
    private long maxWaitTime;
    private int maxQueueSize;
    
    public BulkheadConfig(int maxConcurrentCalls, long maxWaitTime, int maxQueueSize) {
        this.maxConcurrentCalls = maxConcurrentCalls;
        this.maxWaitTime = maxWaitTime;
        this.maxQueueSize = maxQueueSize;
    }
    
    // Getters
    public int getMaxConcurrentCalls() { return maxConcurrentCalls; }
    public long getMaxWaitTime() { return maxWaitTime; }
    public int getMaxQueueSize() { return maxQueueSize; }
}

// Bulkhead implementation
public class Bulkhead {
    private final Semaphore semaphore;
    private final BlockingQueue<Runnable> queue;
    private final ExecutorService executor;
    private final BulkheadConfig config;
    
    public Bulkhead(BulkheadConfig config) {
        this.config = config;
        this.semaphore = new Semaphore(config.getMaxConcurrentCalls());
        this.queue = new ArrayBlockingQueue<>(config.getMaxQueueSize());
        this.executor = Executors.newCachedThreadPool();
        
        startQueueProcessor();
    }
    
    public <T> CompletableFuture<T> execute(Supplier<T> operation) {
        CompletableFuture<T> future = new CompletableFuture<>();
        
        try {
            if (semaphore.tryAcquire(config.getMaxWaitTime(), TimeUnit.MILLISECONDS)) {
                executor.submit(() -> {
                    try {
                        T result = operation.get();
                        future.complete(result);
                    } catch (Exception e) {
                        future.completeExceptionally(e);
                    } finally {
                        semaphore.release();
                    }
                });
            } else {
                future.completeExceptionally(new BulkheadException("Bulkhead is full"));
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            future.completeExceptionally(e);
        }
        
        return future;
    }
    
    private void startQueueProcessor() {
        Thread processor = new Thread(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                try {
                    Runnable task = queue.poll(100, TimeUnit.MILLISECONDS);
                    if (task != null) {
                        executor.submit(task);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        processor.setDaemon(true);
        processor.start();
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}

// Bulkhead exception
public class BulkheadException extends RuntimeException {
    public BulkheadException(String message) {
        super(message);
    }
}
```

## 13.7 Graceful Degradation Pattern

The Graceful Degradation pattern allows systems to continue operating with reduced functionality when components fail.

### When to Use:
- When you need to maintain system availability
- When you want to provide partial functionality
- When you need to handle component failures gracefully

### Real-World Analogy:
Think of a car that can still drive even if the air conditioning fails. The core functionality (driving) is maintained, but some features are unavailable.

### Basic Implementation:
```java
// Service interface
public interface Service {
    boolean isAvailable();
    Object execute(Object request) throws Exception;
}

// Primary service
public class PrimaryService implements Service {
    private boolean available = true;
    
    public boolean isAvailable() {
        return available;
    }
    
    public Object execute(Object request) throws Exception {
        if (!available) {
            throw new ServiceUnavailableException("Primary service is unavailable");
        }
        // Execute primary service logic
        return "Primary result for: " + request;
    }
    
    public void setAvailable(boolean available) {
        this.available = available;
    }
}

// Fallback service
public class FallbackService implements Service {
    public boolean isAvailable() {
        return true; // Fallback is always available
    }
    
    public Object execute(Object request) throws Exception {
        // Execute fallback logic with reduced functionality
        return "Fallback result for: " + request;
    }
}

// Graceful degradation manager
public class GracefulDegradationManager {
    private List<Service> services;
    private Logger logger;
    
    public GracefulDegradationManager(Logger logger) {
        this.services = new ArrayList<>();
        this.logger = logger;
    }
    
    public void addService(Service service) {
        services.add(service);
    }
    
    public Object execute(Object request) throws Exception {
        for (Service service : services) {
            if (service.isAvailable()) {
                try {
                    return service.execute(request);
                } catch (Exception e) {
                    logger.warn("Service failed, trying next service: " + e.getMessage());
                    continue;
                }
            }
        }
        
        throw new ServiceUnavailableException("All services are unavailable");
    }
}

// Usage example
public class UserService {
    private GracefulDegradationManager degradationManager;
    
    public UserService() {
        degradationManager = new GracefulDegradationManager(LoggerFactory.getLogger(UserService.class));
        degradationManager.addService(new PrimaryService());
        degradationManager.addService(new FallbackService());
    }
    
    public String getUserData(String userId) throws Exception {
        return (String) degradationManager.execute(userId);
    }
}
```

## 13.8 Fail-Safe Pattern

The Fail-Safe pattern ensures that system failures don't cause data loss or corruption.

### When to Use:
- When you need to protect critical data
- When you want to ensure system safety
- When you need to handle unexpected failures

### Real-World Analogy:
Think of a safety valve on a pressure cooker. If the pressure gets too high, the valve opens to release pressure, preventing the cooker from exploding.

### Basic Implementation:
```java
// Fail-safe operation
public class FailSafeOperation {
    private Logger logger;
    private ErrorHandler errorHandler;
    
    public FailSafeOperation(Logger logger, ErrorHandler errorHandler) {
        this.logger = logger;
        this.errorHandler = errorHandler;
    }
    
    public <T> T execute(Supplier<T> operation, T safeValue) {
        try {
            return operation.get();
        } catch (Exception e) {
            logger.error("Operation failed, using safe value", e);
            errorHandler.handle(e);
            return safeValue;
        }
    }
    
    public void execute(Runnable operation, Runnable safeOperation) {
        try {
            operation.run();
        } catch (Exception e) {
            logger.error("Operation failed, executing safe operation", e);
            errorHandler.handle(e);
            safeOperation.run();
        }
    }
}

// Data protection
public class DataProtection {
    private Logger logger;
    private BackupService backupService;
    
    public DataProtection(Logger logger, BackupService backupService) {
        this.logger = logger;
        this.backupService = backupService;
    }
    
    public <T> T executeWithProtection(Supplier<T> operation, T defaultValue) {
        try {
            T result = operation.get();
            backupService.createBackup(result);
            return result;
        } catch (Exception e) {
            logger.error("Operation failed, attempting recovery", e);
            T recoveredValue = backupService.recover();
            return recoveredValue != null ? recoveredValue : defaultValue;
        }
    }
    
    public void executeWithProtection(Runnable operation, Runnable recoveryOperation) {
        try {
            operation.run();
        } catch (Exception e) {
            logger.error("Operation failed, attempting recovery", e);
            recoveryOperation.run();
        }
    }
}

// Usage example
public class UserService {
    private FailSafeOperation failSafeOperation;
    private DataProtection dataProtection;
    
    public UserService() {
        Logger logger = LoggerFactory.getLogger(UserService.class);
        this.failSafeOperation = new FailSafeOperation(logger, new ErrorHandler());
        this.dataProtection = new DataProtection(logger, new BackupService());
    }
    
    public User findById(String id) {
        return failSafeOperation.execute(
            () -> userRepository.findById(id),
            new User("unknown", "Unknown User", "unknown@example.com")
        );
    }
    
    public void saveUser(User user) {
        dataProtection.executeWithProtection(
            () -> userRepository.save(user),
            () -> logger.warn("Failed to save user, data may be lost")
        );
    }
}
```

## 13.9 Fail-Fast Pattern

The Fail-Fast pattern detects errors early and stops execution immediately to prevent further damage.

### When to Use:
- When you need to detect errors early
- When you want to prevent cascading failures
- When you need to provide quick feedback

### Real-World Analogy:
Think of a smoke detector that sounds an alarm as soon as it detects smoke, allowing you to take immediate action before the fire spreads.

### Basic Implementation:
```java
// Fail-fast validator
public class FailFastValidator {
    private List<ValidationRule> rules;
    
    public FailFastValidator() {
        this.rules = new ArrayList<>();
    }
    
    public void addRule(ValidationRule rule) {
        rules.add(rule);
    }
    
    public void validate(Object object) throws ValidationException {
        for (ValidationRule rule : rules) {
            if (!rule.isValid(object)) {
                throw new ValidationException("Validation failed: " + rule.getErrorMessage());
            }
        }
    }
}

// Validation rule interface
public interface ValidationRule {
    boolean isValid(Object object);
    String getErrorMessage();
}

// Specific validation rules
public class NotNullRule implements ValidationRule {
    public boolean isValid(Object object) {
        return object != null;
    }
    
    public String getErrorMessage() {
        return "Object cannot be null";
    }
}

public class NotEmptyRule implements ValidationRule {
    public boolean isValid(Object object) {
        if (object instanceof String) {
            return !((String) object).trim().isEmpty();
        }
        return true;
    }
    
    public String getErrorMessage() {
        return "String cannot be empty";
    }
}

// Fail-fast service
public class FailFastService {
    private FailFastValidator validator;
    private Logger logger;
    
    public FailFastService(Logger logger) {
        this.validator = new FailFastValidator();
        this.logger = logger;
        
        // Add common validation rules
        validator.addRule(new NotNullRule());
        validator.addRule(new NotEmptyRule());
    }
    
    public <T> T execute(Supplier<T> operation, Object input) throws ValidationException {
        validator.validate(input);
        
        try {
            return operation.get();
        } catch (Exception e) {
            logger.error("Operation failed, stopping execution", e);
            throw new RuntimeException("Operation failed", e);
        }
    }
}

// Usage example
public class UserService {
    private FailFastService failFastService;
    
    public UserService() {
        this.failFastService = new FailFastService(LoggerFactory.getLogger(UserService.class));
    }
    
    public User createUser(String name, String email) throws ValidationException {
        return failFastService.execute(
            () -> {
                User user = new User(UUID.randomUUID().toString(), name, email);
                userRepository.save(user);
                return user;
            },
            name // Validate input
        );
    }
}
```

## 13.10 Error Propagation Pattern

The Error Propagation pattern ensures that errors are properly propagated through the system while maintaining context.

### When to Use:
- When you need to maintain error context
- When you want to provide detailed error information
- When you need to handle errors at different levels

### Real-World Analogy:
Think of a chain of command in an organization. When an error occurs at a lower level, it's reported up the chain with additional context at each level, ensuring that the right people are informed and can take appropriate action.

### Basic Implementation:
```java
// Error context
public class ErrorContext {
    private String operation;
    private Map<String, Object> parameters;
    private String userId;
    private long timestamp;
    private String correlationId;
    
    public ErrorContext(String operation) {
        this.operation = operation;
        this.parameters = new HashMap<>();
        this.timestamp = System.currentTimeMillis();
        this.correlationId = UUID.randomUUID().toString();
    }
    
    // Getters and setters
    public String getOperation() { return operation; }
    public Map<String, Object> getParameters() { return parameters; }
    public String getUserId() { return userId; }
    public void setUserId(String userId) { this.userId = userId; }
    public long getTimestamp() { return timestamp; }
    public String getCorrelationId() { return correlationId; }
    
    public ErrorContext addParameter(String key, Object value) {
        parameters.put(key, value);
        return this;
    }
}

// Error propagator
public class ErrorPropagator {
    private Logger logger;
    private ErrorReporter errorReporter;
    
    public ErrorPropagator(Logger logger, ErrorReporter errorReporter) {
        this.logger = logger;
        this.errorReporter = errorReporter;
    }
    
    public <T> T propagate(Supplier<T> operation, ErrorContext context) throws Exception {
        try {
            return operation.get();
        } catch (Exception e) {
            enrichError(e, context);
            propagateError(e, context);
            throw e;
        }
    }
    
    public void propagate(Runnable operation, ErrorContext context) throws Exception {
        try {
            operation.run();
        } catch (Exception e) {
            enrichError(e, context);
            propagateError(e, context);
            throw e;
        }
    }
    
    private void enrichError(Exception e, ErrorContext context) {
        if (e instanceof ApplicationException) {
            ApplicationException appException = (ApplicationException) e;
            appException.addContext("operation", context.getOperation());
            appException.addContext("correlationId", context.getCorrelationId());
            appException.addContext("userId", context.getUserId());
            appException.addContext("timestamp", context.getTimestamp());
        }
    }
    
    private void propagateError(Exception e, ErrorContext context) {
        logger.error("Error in operation: " + context.getOperation(), e);
        errorReporter.reportError(e, context);
    }
}

// Usage example
public class UserService {
    private ErrorPropagator errorPropagator;
    private UserRepository userRepository;
    
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
        this.errorPropagator = new ErrorPropagator(
            LoggerFactory.getLogger(UserService.class),
            new ErrorReporter()
        );
    }
    
    public User findById(String id) throws Exception {
        ErrorContext context = new ErrorContext("findUserById")
            .addParameter("userId", id);
        
        return errorPropagator.propagate(
            () -> userRepository.findById(id),
            context
        );
    }
    
    public User createUser(String name, String email) throws Exception {
        ErrorContext context = new ErrorContext("createUser")
            .addParameter("name", name)
            .addParameter("email", email);
        
        return errorPropagator.propagate(
            () -> {
                User user = new User(UUID.randomUUID().toString(), name, email);
                userRepository.save(user);
                return user;
            },
            context
        );
    }
}
```

This comprehensive coverage of error handling patterns provides the foundation for building robust, fault-tolerant applications. Each pattern addresses specific error handling challenges and offers different approaches to managing errors and failures.