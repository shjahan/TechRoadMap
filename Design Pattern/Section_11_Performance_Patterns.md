# Section 11 - Performance Patterns

## 11.1 Caching Patterns

Caching patterns improve performance by storing frequently accessed data in fast storage to reduce computation and database access.

### When to Use:
- When you have expensive operations that are repeated
- When you need to reduce database load
- When you want to improve response times

### Real-World Analogy:
Think of a library's reference desk that keeps frequently asked questions and their answers readily available. Instead of looking up the same information repeatedly, the librarian can quickly provide the answer from memory.

### Basic Implementation:
```java
// Cache interface
public interface Cache<K, V> {
    V get(K key);
    void put(K key, V value);
    void remove(K key);
    void clear();
    boolean containsKey(K key);
}

// Simple in-memory cache
public class SimpleCache<K, V> implements Cache<K, V> {
    private Map<K, V> cache = new HashMap<>();
    private int maxSize;
    
    public SimpleCache(int maxSize) {
        this.maxSize = maxSize;
    }
    
    public V get(K key) {
        return cache.get(key);
    }
    
    public void put(K key, V value) {
        if (cache.size() >= maxSize) {
            // Remove oldest entry (simple implementation)
            K firstKey = cache.keySet().iterator().next();
            cache.remove(firstKey);
        }
        cache.put(key, value);
    }
    
    public void remove(K key) {
        cache.remove(key);
    }
    
    public void clear() {
        cache.clear();
    }
    
    public boolean containsKey(K key) {
        return cache.containsKey(key);
    }
}

// LRU Cache implementation
public class LRUCache<K, V> implements Cache<K, V> {
    private final int capacity;
    private Map<K, Node<K, V>> cache;
    private Node<K, V> head;
    private Node<K, V> tail;
    
    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new HashMap<>();
        this.head = new Node<>(null, null);
        this.tail = new Node<>(null, null);
        head.next = tail;
        tail.prev = head;
    }
    
    public V get(K key) {
        Node<K, V> node = cache.get(key);
        if (node != null) {
            moveToHead(node);
            return node.value;
        }
        return null;
    }
    
    public void put(K key, V value) {
        Node<K, V> node = cache.get(key);
        
        if (node != null) {
            node.value = value;
            moveToHead(node);
        } else {
            Node<K, V> newNode = new Node<>(key, value);
            cache.put(key, newNode);
            addToHead(newNode);
            
            if (cache.size() > capacity) {
                Node<K, V> tail = removeTail();
                cache.remove(tail.key);
            }
        }
    }
    
    private void addToHead(Node<K, V> node) {
        node.prev = head;
        node.next = head.next;
        head.next.prev = node;
        head.next = node;
    }
    
    private void removeNode(Node<K, V> node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    private void moveToHead(Node<K, V> node) {
        removeNode(node);
        addToHead(node);
    }
    
    private Node<K, V> removeTail() {
        Node<K, V> lastNode = tail.prev;
        removeNode(lastNode);
        return lastNode;
    }
    
    private static class Node<K, V> {
        K key;
        V value;
        Node<K, V> prev;
        Node<K, V> next;
        
        Node(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }
}
```

## 11.2 Lazy Loading Pattern

Lazy loading delays the initialization of objects until they are actually needed, improving startup time and memory usage.

### When to Use:
- When you have expensive objects that might not be used
- When you want to reduce memory usage
- When you need to improve startup performance

### Real-World Analogy:
Think of a smart phone that only loads apps when you actually open them, rather than keeping all apps in memory at once. This saves battery and memory.

### Basic Implementation:
```java
// Lazy loading interface
public interface LazyLoader<T> {
    T get();
    boolean isLoaded();
    void reset();
}

// Simple lazy loader
public class SimpleLazyLoader<T> implements LazyLoader<T> {
    private T value;
    private Supplier<T> supplier;
    private boolean loaded = false;
    
    public SimpleLazyLoader(Supplier<T> supplier) {
        this.supplier = supplier;
    }
    
    public T get() {
        if (!loaded) {
            value = supplier.get();
            loaded = true;
        }
        return value;
    }
    
    public boolean isLoaded() {
        return loaded;
    }
    
    public void reset() {
        value = null;
        loaded = false;
    }
}

// Thread-safe lazy loader
public class ThreadSafeLazyLoader<T> implements LazyLoader<T> {
    private volatile T value;
    private Supplier<T> supplier;
    private final Object lock = new Object();
    
    public ThreadSafeLazyLoader(Supplier<T> supplier) {
        this.supplier = supplier;
    }
    
    public T get() {
        if (value == null) {
            synchronized (lock) {
                if (value == null) {
                    value = supplier.get();
                }
            }
        }
        return value;
    }
    
    public boolean isLoaded() {
        return value != null;
    }
    
    public void reset() {
        synchronized (lock) {
            value = null;
        }
    }
}

// Lazy collection
public class LazyList<T> implements List<T> {
    private List<T> list;
    private Supplier<List<T>> supplier;
    private boolean loaded = false;
    
    public LazyList(Supplier<List<T>> supplier) {
        this.supplier = supplier;
    }
    
    private List<T> getList() {
        if (!loaded) {
            list = supplier.get();
            loaded = true;
        }
        return list;
    }
    
    public T get(int index) {
        return getList().get(index);
    }
    
    public int size() {
        return getList().size();
    }
    
    // Delegate other methods to the actual list
    public boolean add(T element) {
        return getList().add(element);
    }
    
    public boolean remove(Object element) {
        return getList().remove(element);
    }
    
    // ... implement other List methods
}
```

## 11.3 Eager Loading Pattern

Eager loading loads all related data at once, reducing the number of database queries and improving performance for scenarios where all data is needed.

### When to Use:
- When you know you'll need all related data
- When you want to reduce database round trips
- When you have a small, predictable dataset

### Real-World Analogy:
Think of a restaurant that prepares all the ingredients for a dish at once, rather than cooking each ingredient separately. This is more efficient when you know you'll need everything.

### Basic Implementation:
```java
// Eager loading service
public class EagerLoadingService {
    private UserRepository userRepository;
    private OrderRepository orderRepository;
    private ProductRepository productRepository;
    
    public EagerLoadingService(UserRepository userRepository,
                              OrderRepository orderRepository,
                              ProductRepository productRepository) {
        this.userRepository = userRepository;
        this.orderRepository = orderRepository;
        this.productRepository = productRepository;
    }
    
    public UserWithOrders loadUserWithOrders(String userId) {
        // Load user
        User user = userRepository.findById(userId);
        
        // Load all orders for the user
        List<Order> orders = orderRepository.findByUserId(userId);
        
        // Load all products for the orders
        Set<String> productIds = orders.stream()
            .flatMap(order -> order.getProductIds().stream())
            .collect(Collectors.toSet());
        
        Map<String, Product> products = productRepository.findByIds(productIds);
        
        // Attach products to orders
        orders.forEach(order -> {
            order.getProductIds().forEach(productId -> {
                Product product = products.get(productId);
                if (product != null) {
                    order.addProduct(product);
                }
            });
        });
        
        return new UserWithOrders(user, orders);
    }
}

// Data transfer object
public class UserWithOrders {
    private User user;
    private List<Order> orders;
    
    public UserWithOrders(User user, List<Order> orders) {
        this.user = user;
        this.orders = orders;
    }
    
    // Getters
    public User getUser() { return user; }
    public List<Order> getOrders() { return orders; }
}
```

## 11.4 Object Pool Pattern

The Object Pool pattern maintains a set of initialized objects ready to use, avoiding the overhead of creating and destroying objects.

### When to Use:
- When object creation is expensive
- When you need to limit the number of objects
- When you want to reuse objects

### Real-World Analogy:
Think of a car rental service that maintains a fleet of cars ready to rent. Instead of manufacturing a new car each time someone wants to rent one, they have cars available and ready to go.

### Basic Implementation:
```java
// Object pool interface
public interface ObjectPool<T> {
    T acquire();
    void release(T object);
    void shutdown();
}

// Generic object pool
public class GenericObjectPool<T> implements ObjectPool<T> {
    private Queue<T> availableObjects;
    private Set<T> usedObjects;
    private Supplier<T> objectFactory;
    private int maxSize;
    private int currentSize;
    
    public GenericObjectPool(Supplier<T> objectFactory, int maxSize) {
        this.objectFactory = objectFactory;
        this.maxSize = maxSize;
        this.availableObjects = new LinkedList<>();
        this.usedObjects = new HashSet<>();
    }
    
    public synchronized T acquire() {
        if (availableObjects.isEmpty()) {
            if (currentSize < maxSize) {
                T newObject = objectFactory.get();
                currentSize++;
                usedObjects.add(newObject);
                return newObject;
            } else {
                throw new RuntimeException("Pool exhausted");
            }
        }
        
        T object = availableObjects.poll();
        usedObjects.add(object);
        return object;
    }
    
    public synchronized void release(T object) {
        if (usedObjects.remove(object)) {
            availableObjects.offer(object);
        }
    }
    
    public synchronized void shutdown() {
        availableObjects.clear();
        usedObjects.clear();
        currentSize = 0;
    }
}

// Database connection pool
public class DatabaseConnectionPool implements ObjectPool<Connection> {
    private Queue<Connection> availableConnections;
    private Set<Connection> usedConnections;
    private String connectionString;
    private int maxSize;
    
    public DatabaseConnectionPool(String connectionString, int maxSize) {
        this.connectionString = connectionString;
        this.maxSize = maxSize;
        this.availableConnections = new LinkedList<>();
        this.usedConnections = new HashSet<>();
        initializePool();
    }
    
    private void initializePool() {
        for (int i = 0; i < maxSize; i++) {
            try {
                Connection connection = DriverManager.getConnection(connectionString);
                availableConnections.offer(connection);
            } catch (SQLException e) {
                throw new RuntimeException("Failed to create connection", e);
            }
        }
    }
    
    public synchronized Connection acquire() {
        if (availableConnections.isEmpty()) {
            throw new RuntimeException("No available connections");
        }
        
        Connection connection = availableConnections.poll();
        usedConnections.add(connection);
        return connection;
    }
    
    public synchronized void release(Connection connection) {
        if (usedConnections.remove(connection)) {
            availableConnections.offer(connection);
        }
    }
    
    public synchronized void shutdown() {
        // Close all connections
        availableConnections.forEach(this::closeConnection);
        usedConnections.forEach(this::closeConnection);
        availableConnections.clear();
        usedConnections.clear();
    }
    
    private void closeConnection(Connection connection) {
        try {
            connection.close();
        } catch (SQLException e) {
            // Log error
        }
    }
}
```

## 11.5 Resource Pool Pattern

The Resource Pool pattern manages a pool of resources to improve performance and resource utilization.

### When to Use:
- When you need to manage expensive resources
- When you want to limit resource usage
- When you need to improve resource utilization

### Real-World Analogy:
Think of a swimming pool with a limited number of lanes. The pool manager ensures that swimmers can use the lanes efficiently without overcrowding, and new swimmers wait for available lanes.

### Basic Implementation:
```java
// Resource pool interface
public interface ResourcePool<T> {
    T acquire() throws InterruptedException;
    T acquire(long timeout, TimeUnit unit) throws InterruptedException;
    void release(T resource);
    void shutdown();
}

// Thread pool implementation
public class ThreadPool implements ResourcePool<WorkerThread> {
    private Queue<WorkerThread> availableThreads;
    private Set<WorkerThread> usedThreads;
    private int maxSize;
    private boolean shutdown = false;
    
    public ThreadPool(int maxSize) {
        this.maxSize = maxSize;
        this.availableThreads = new LinkedList<>();
        this.usedThreads = new HashSet<>();
        initializePool();
    }
    
    private void initializePool() {
        for (int i = 0; i < maxSize; i++) {
            WorkerThread thread = new WorkerThread();
            availableThreads.offer(thread);
        }
    }
    
    public synchronized WorkerThread acquire() throws InterruptedException {
        while (availableThreads.isEmpty() && !shutdown) {
            wait();
        }
        
        if (shutdown) {
            throw new IllegalStateException("Pool is shutdown");
        }
        
        WorkerThread thread = availableThreads.poll();
        usedThreads.add(thread);
        return thread;
    }
    
    public synchronized WorkerThread acquire(long timeout, TimeUnit unit) throws InterruptedException {
        long endTime = System.currentTimeMillis() + unit.toMillis(timeout);
        
        while (availableThreads.isEmpty() && !shutdown) {
            long remainingTime = endTime - System.currentTimeMillis();
            if (remainingTime <= 0) {
                throw new InterruptedException("Timeout waiting for resource");
            }
            wait(remainingTime);
        }
        
        if (shutdown) {
            throw new IllegalStateException("Pool is shutdown");
        }
        
        WorkerThread thread = availableThreads.poll();
        usedThreads.add(thread);
        return thread;
    }
    
    public synchronized void release(WorkerThread thread) {
        if (usedThreads.remove(thread)) {
            availableThreads.offer(thread);
            notify();
        }
    }
    
    public synchronized void shutdown() {
        shutdown = true;
        notifyAll();
        
        // Wait for all threads to be released
        while (!usedThreads.isEmpty()) {
            try {
                wait();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
}

// Worker thread
public class WorkerThread {
    private Thread thread;
    private Runnable task;
    private boolean busy = false;
    
    public void execute(Runnable task) {
        this.task = task;
        this.busy = true;
        
        if (thread == null) {
            thread = new Thread(this::run);
            thread.start();
        }
    }
    
    private void run() {
        while (true) {
            if (task != null) {
                task.run();
                task = null;
                busy = false;
            }
            
            try {
                Thread.sleep(100); // Wait for next task
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    public boolean isBusy() {
        return busy;
    }
}
```

## 11.6 Connection Pool Pattern

The Connection Pool pattern manages database connections to improve performance and resource utilization.

### When to Use:
- When you need to manage database connections
- When you want to reduce connection overhead
- When you need to limit the number of connections

### Real-World Analogy:
Think of a taxi service that maintains a fleet of taxis ready to pick up passengers. Instead of calling a taxi company each time you need a ride, you can get a taxi from the pool of available ones.

### Basic Implementation:
```java
// Connection pool
public class ConnectionPool {
    private Queue<Connection> availableConnections;
    private Set<Connection> usedConnections;
    private String connectionString;
    private int maxSize;
    private int minSize;
    private long maxIdleTime;
    
    public ConnectionPool(String connectionString, int maxSize, int minSize, long maxIdleTime) {
        this.connectionString = connectionString;
        this.maxSize = maxSize;
        this.minSize = minSize;
        this.maxIdleTime = maxIdleTime;
        this.availableConnections = new LinkedList<>();
        this.usedConnections = new HashSet<>();
        
        initializePool();
        startIdleConnectionCleanup();
    }
    
    private void initializePool() {
        for (int i = 0; i < minSize; i++) {
            Connection connection = createConnection();
            availableConnections.offer(connection);
        }
    }
    
    public synchronized Connection getConnection() throws SQLException {
        if (availableConnections.isEmpty()) {
            if (usedConnections.size() < maxSize) {
                Connection connection = createConnection();
                usedConnections.add(connection);
                return connection;
            } else {
                throw new SQLException("No available connections");
            }
        }
        
        Connection connection = availableConnections.poll();
        usedConnections.add(connection);
        return connection;
    }
    
    public synchronized void releaseConnection(Connection connection) {
        if (usedConnections.remove(connection)) {
            if (isConnectionValid(connection)) {
                availableConnections.offer(connection);
            } else {
                closeConnection(connection);
            }
        }
    }
    
    private Connection createConnection() {
        try {
            Connection connection = DriverManager.getConnection(connectionString);
            connection.setAutoCommit(true);
            return connection;
        } catch (SQLException e) {
            throw new RuntimeException("Failed to create connection", e);
        }
    }
    
    private boolean isConnectionValid(Connection connection) {
        try {
            return connection.isValid(5); // 5 second timeout
        } catch (SQLException e) {
            return false;
        }
    }
    
    private void closeConnection(Connection connection) {
        try {
            connection.close();
        } catch (SQLException e) {
            // Log error
        }
    }
    
    private void startIdleConnectionCleanup() {
        Thread cleanupThread = new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(60000); // Check every minute
                    cleanupIdleConnections();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        cleanupThread.setDaemon(true);
        cleanupThread.start();
    }
    
    private synchronized void cleanupIdleConnections() {
        long currentTime = System.currentTimeMillis();
        Iterator<Connection> iterator = availableConnections.iterator();
        
        while (iterator.hasNext()) {
            Connection connection = iterator.next();
            if (currentTime - getLastUsedTime(connection) > maxIdleTime) {
                iterator.remove();
                closeConnection(connection);
            }
        }
    }
    
    private long getLastUsedTime(Connection connection) {
        // Implementation to track last used time
        return System.currentTimeMillis();
    }
}
```

## 11.7 Memoization Pattern

The Memoization pattern caches the results of expensive function calls to avoid redundant calculations.

### When to Use:
- When you have expensive pure functions
- When you have functions with repeated inputs
- When you want to optimize recursive functions

### Real-World Analogy:
Think of a math teacher who keeps a notebook of all the calculations they've done. When a student asks for the same calculation again, the teacher can quickly look it up instead of recalculating.

### Basic Implementation:
```java
// Memoization utility
public class Memoization {
    public static <T, R> Function<T, R> memoize(Function<T, R> function) {
        Map<T, R> cache = new ConcurrentHashMap<>();
        return input -> cache.computeIfAbsent(input, function);
    }
    
    public static <T, R> Function<T, R> memoizeWithExpiry(Function<T, R> function, long expiryMillis) {
        Map<T, CacheEntry<R>> cache = new ConcurrentHashMap<>();
        return input -> {
            CacheEntry<R> entry = cache.get(input);
            if (entry != null && !entry.isExpired(expiryMillis)) {
                return entry.getValue();
            }
            
            R result = function.apply(input);
            cache.put(input, new CacheEntry<>(result, System.currentTimeMillis()));
            return result;
        };
    }
}

// Cache entry for expiry
public class CacheEntry<T> {
    private T value;
    private long timestamp;
    
    public CacheEntry(T value, long timestamp) {
        this.value = value;
        this.timestamp = timestamp;
    }
    
    public T getValue() {
        return value;
    }
    
    public boolean isExpired(long expiryMillis) {
        return System.currentTimeMillis() - timestamp > expiryMillis;
    }
}

// Example usage
public class FibonacciCalculator {
    private Function<Integer, Long> memoizedFibonacci;
    
    public FibonacciCalculator() {
        this.memoizedFibonacci = Memoization.memoize(this::fibonacci);
    }
    
    public long calculate(int n) {
        return memoizedFibonacci.apply(n);
    }
    
    private long fibonacci(int n) {
        if (n <= 1) {
            return n;
        }
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

// Recursive memoization
public class RecursiveMemoization {
    public static <T, R> Function<T, R> memoizeRecursive(BiFunction<T, Function<T, R>, R> function) {
        Map<T, R> cache = new ConcurrentHashMap<>();
        return new Function<T, R>() {
            @Override
            public R apply(T input) {
                return cache.computeIfAbsent(input, key -> function.apply(key, this));
            }
        };
    }
}
```

## 11.8 Circuit Breaker Pattern

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

## 11.9 Bulkhead Pattern

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

## 11.10 Throttling Pattern

The Throttling pattern limits the rate of requests to prevent system overload.

### When to Use:
- When you need to limit request rates
- When you want to prevent system overload
- When you need to implement rate limiting

### Real-World Analogy:
Think of a traffic light that controls the flow of cars at an intersection. It ensures that only a certain number of cars can pass through at a time, preventing traffic jams.

### Basic Implementation:
```java
// Throttling interface
public interface Throttler {
    boolean allowRequest();
    void recordRequest();
}

// Token bucket throttler
public class TokenBucketThrottler implements Throttler {
    private final int capacity;
    private final int refillRate;
    private int tokens;
    private long lastRefillTime;
    private final Object lock = new Object();
    
    public TokenBucketThrottler(int capacity, int refillRate) {
        this.capacity = capacity;
        this.refillRate = refillRate;
        this.tokens = capacity;
        this.lastRefillTime = System.currentTimeMillis();
    }
    
    public boolean allowRequest() {
        synchronized (lock) {
            refillTokens();
            
            if (tokens > 0) {
                tokens--;
                return true;
            }
            return false;
        }
    }
    
    public void recordRequest() {
        // Token bucket automatically records requests
    }
    
    private void refillTokens() {
        long now = System.currentTimeMillis();
        long timePassed = now - lastRefillTime;
        
        if (timePassed > 0) {
            int tokensToAdd = (int) (timePassed * refillRate / 1000);
            tokens = Math.min(capacity, tokens + tokensToAdd);
            lastRefillTime = now;
        }
    }
}

// Sliding window throttler
public class SlidingWindowThrottler implements Throttler {
    private final int maxRequests;
    private final long windowSizeMillis;
    private final Queue<Long> requestTimes;
    private final Object lock = new Object();
    
    public SlidingWindowThrottler(int maxRequests, long windowSizeMillis) {
        this.maxRequests = maxRequests;
        this.windowSizeMillis = windowSizeMillis;
        this.requestTimes = new LinkedList<>();
    }
    
    public boolean allowRequest() {
        synchronized (lock) {
            long now = System.currentTimeMillis();
            
            // Remove old requests outside the window
            while (!requestTimes.isEmpty() && 
                   now - requestTimes.peek() > windowSizeMillis) {
                requestTimes.poll();
            }
            
            if (requestTimes.size() < maxRequests) {
                requestTimes.offer(now);
                return true;
            }
            
            return false;
        }
    }
    
    public void recordRequest() {
        // Sliding window automatically records requests
    }
}

// Rate limiter
public class RateLimiter {
    private final Throttler throttler;
    private final long retryAfterMillis;
    
    public RateLimiter(Throttler throttler, long retryAfterMillis) {
        this.throttler = throttler;
        this.retryAfterMillis = retryAfterMillis;
    }
    
    public boolean tryAcquire() {
        return throttler.allowRequest();
    }
    
    public void acquire() throws InterruptedException {
        while (!tryAcquire()) {
            Thread.sleep(retryAfterMillis);
        }
    }
    
    public boolean tryAcquire(long timeout, TimeUnit unit) throws InterruptedException {
        long endTime = System.currentTimeMillis() + unit.toMillis(timeout);
        
        while (System.currentTimeMillis() < endTime) {
            if (tryAcquire()) {
                return true;
            }
            Thread.sleep(Math.min(retryAfterMillis, endTime - System.currentTimeMillis()));
        }
        
        return false;
    }
}
```

This comprehensive coverage of performance patterns provides the foundation for building high-performance applications. Each pattern addresses specific performance challenges and offers different approaches to optimizing system performance.