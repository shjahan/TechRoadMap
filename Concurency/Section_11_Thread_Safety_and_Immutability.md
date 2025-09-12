# Section 11 – Thread Safety and Immutability

## 11.1 Thread-Safe Design Principles

Thread-safe design principles provide guidelines for creating code that can be safely used by multiple threads without causing data corruption or race conditions.

### Key Principles
- **Immutable Objects**: Objects that cannot be modified after creation
- **Thread Confinement**: Restricting access to specific threads
- **Synchronization**: Using locks and atomic operations
- **Defensive Copying**: Creating copies to prevent shared state

### Real-World Analogy
Think of a shared workspace where everyone has their own locked drawer (thread confinement) and uses only read-only documents (immutable objects) to prevent conflicts.

### Java Example
```java
public class ThreadSafeDesignExample {
    // Thread-safe counter using synchronization
    public static class ThreadSafeCounter {
        private int count = 0;
        private final Object lock = new Object();
        
        public void increment() {
            synchronized (lock) {
                count++;
            }
        }
        
        public int getCount() {
            synchronized (lock) {
                return count;
            }
        }
    }
    
    // Thread-safe counter using atomic operations
    public static class AtomicCounter {
        private final AtomicInteger count = new AtomicInteger(0);
        
        public void increment() {
            count.incrementAndGet();
        }
        
        public int getCount() {
            return count.get();
        }
    }
    
    // Thread-safe list using defensive copying
    public static class ThreadSafeList<T> {
        private final List<T> list = new ArrayList<>();
        private final Object lock = new Object();
        
        public void add(T item) {
            synchronized (lock) {
                list.add(item);
            }
        }
        
        public List<T> getSnapshot() {
            synchronized (lock) {
                return new ArrayList<>(list); // Defensive copy
            }
        }
    }
    
    public static void demonstrateThreadSafeDesign() {
        ThreadSafeCounter counter = new ThreadSafeCounter();
        AtomicCounter atomicCounter = new AtomicCounter();
        ThreadSafeList<String> list = new ThreadSafeList<>();
        
        // Test thread-safe counter
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    counter.increment();
                    atomicCounter.increment();
                }
            });
            threads[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("Thread-safe counter: " + counter.getCount());
        System.out.println("Atomic counter: " + atomicCounter.getCount());
    }
}
```

## 11.2 Immutable Objects

Immutable objects are objects whose state cannot be modified after creation, providing natural thread safety.

### Key Characteristics
- **No Mutators**: No methods that change state
- **Final Fields**: All fields are final
- **Deep Immutability**: All referenced objects are also immutable
- **Thread Safety**: Can be safely shared between threads

### Real-World Analogy
Think of a stone tablet with text carved into it. Once carved, the text cannot be changed, and anyone can read it safely without worrying about modifications.

### Java Example
```java
public class ImmutableObjectsExample {
    // Immutable person class
    public static final class ImmutablePerson {
        private final String name;
        private final int age;
        private final List<String> hobbies;
        
        public ImmutablePerson(String name, int age, List<String> hobbies) {
            this.name = name;
            this.age = age;
            this.hobbies = Collections.unmodifiableList(new ArrayList<>(hobbies));
        }
        
        public String getName() { return name; }
        public int getAge() { return age; }
        public List<String> getHobbies() { return hobbies; }
        
        @Override
        public String toString() {
            return "Person{name='" + name + "', age=" + age + ", hobbies=" + hobbies + "}";
        }
    }
    
    // Immutable point class
    public static final class ImmutablePoint {
        private final double x;
        private final double y;
        
        public ImmutablePoint(double x, double y) {
            this.x = x;
            this.y = y;
        }
        
        public double getX() { return x; }
        public double getY() { return y; }
        
        public ImmutablePoint move(double dx, double dy) {
            return new ImmutablePoint(x + dx, y + dy);
        }
        
        public double distance(ImmutablePoint other) {
            double dx = x - other.x;
            double dy = y - other.y;
            return Math.sqrt(dx * dx + dy * dy);
        }
        
        @Override
        public String toString() {
            return "Point{x=" + x + ", y=" + y + "}";
        }
    }
    
    // Immutable collection wrapper
    public static final class ImmutableCollection<T> {
        private final Collection<T> items;
        
        public ImmutableCollection(Collection<T> items) {
            this.items = Collections.unmodifiableCollection(new ArrayList<>(items));
        }
        
        public Collection<T> getItems() { return items; }
        
        public ImmutableCollection<T> add(T item) {
            List<T> newItems = new ArrayList<>(items);
            newItems.add(item);
            return new ImmutableCollection<>(newItems);
        }
        
        public ImmutableCollection<T> remove(T item) {
            List<T> newItems = new ArrayList<>(items);
            newItems.remove(item);
            return new ImmutableCollection<>(newItems);
        }
        
        @Override
        public String toString() {
            return "ImmutableCollection" + items;
        }
    }
    
    public static void demonstrateImmutableObjects() {
        // Create immutable person
        List<String> hobbies = Arrays.asList("Reading", "Swimming", "Cooking");
        ImmutablePerson person = new ImmutablePerson("John", 30, hobbies);
        System.out.println("Person: " + person);
        
        // Create immutable point
        ImmutablePoint point1 = new ImmutablePoint(0, 0);
        ImmutablePoint point2 = point1.move(3, 4);
        System.out.println("Point1: " + point1);
        System.out.println("Point2: " + point2);
        System.out.println("Distance: " + point1.distance(point2));
        
        // Create immutable collection
        List<String> items = Arrays.asList("A", "B", "C");
        ImmutableCollection<String> collection = new ImmutableCollection<>(items);
        System.out.println("Original: " + collection);
        
        ImmutableCollection<String> newCollection = collection.add("D");
        System.out.println("After add: " + newCollection);
        System.out.println("Original unchanged: " + collection);
    }
}
```

## 11.3 Defensive Copying

Defensive copying creates copies of mutable objects to prevent external modifications from affecting the internal state of an object.

### Key Concepts
- **Copy on Input**: Create copies when receiving mutable objects
- **Copy on Output**: Create copies when returning mutable objects
- **Deep Copying**: Copy nested objects as well
- **Performance Trade-off**: Copying has overhead but ensures safety

### Real-World Analogy
Think of a museum that makes copies of valuable documents before displaying them, so visitors can't damage the originals.

### Java Example
```java
public class DefensiveCopyingExample {
    // Class with defensive copying
    public static class DefensivePerson {
        private final String name;
        private final int age;
        private final List<String> hobbies;
        private final Date birthDate;
        
        public DefensivePerson(String name, int age, List<String> hobbies, Date birthDate) {
            this.name = name;
            this.age = age;
            // Defensive copy on input
            this.hobbies = new ArrayList<>(hobbies);
            this.birthDate = new Date(birthDate.getTime());
        }
        
        public String getName() { return name; }
        public int getAge() { return age; }
        
        // Defensive copy on output
        public List<String> getHobbies() {
            return new ArrayList<>(hobbies);
        }
        
        public Date getBirthDate() {
            return new Date(birthDate.getTime());
        }
        
        public void addHobby(String hobby) {
            hobbies.add(hobby);
        }
        
        @Override
        public String toString() {
            return "Person{name='" + name + "', age=" + age + ", hobbies=" + hobbies + ", birthDate=" + birthDate + "}";
        }
    }
    
    // Class without defensive copying (vulnerable)
    public static class VulnerablePerson {
        private final String name;
        private final int age;
        private final List<String> hobbies;
        private final Date birthDate;
        
        public VulnerablePerson(String name, int age, List<String> hobbies, Date birthDate) {
            this.name = name;
            this.age = age;
            this.hobbies = hobbies; // No defensive copy
            this.birthDate = birthDate; // No defensive copy
        }
        
        public String getName() { return name; }
        public int getAge() { return age; }
        public List<String> getHobbies() { return hobbies; } // No defensive copy
        public Date getBirthDate() { return birthDate; } // No defensive copy
        
        @Override
        public String toString() {
            return "Person{name='" + name + "', age=" + age + ", hobbies=" + hobbies + ", birthDate=" + birthDate + "}";
        }
    }
    
    public static void demonstrateDefensiveCopying() {
        // Test defensive copying
        List<String> hobbies = new ArrayList<>(Arrays.asList("Reading", "Swimming"));
        Date birthDate = new Date();
        
        DefensivePerson defensivePerson = new DefensivePerson("John", 30, hobbies, birthDate);
        System.out.println("Original person: " + defensivePerson);
        
        // Try to modify the original collections
        hobbies.add("Cooking");
        birthDate.setTime(birthDate.getTime() + 1000);
        
        System.out.println("After modifying original collections: " + defensivePerson);
        
        // Test vulnerable person
        List<String> vulnerableHobbies = new ArrayList<>(Arrays.asList("Reading", "Swimming"));
        Date vulnerableBirthDate = new Date();
        
        VulnerablePerson vulnerablePerson = new VulnerablePerson("Jane", 25, vulnerableHobbies, vulnerableBirthDate);
        System.out.println("\nOriginal vulnerable person: " + vulnerablePerson);
        
        // Modify the original collections
        vulnerableHobbies.add("Cooking");
        vulnerableBirthDate.setTime(vulnerableBirthDate.getTime() + 1000);
        
        System.out.println("After modifying original collections: " + vulnerablePerson);
    }
}
```

## 11.4 Thread Confinement

Thread confinement restricts access to objects to a specific thread, eliminating the need for synchronization.

### Key Concepts
- **Stack Confinement**: Objects exist only on the stack
- **Thread Local**: Thread-specific storage
- **Single Thread**: Objects used by only one thread
- **No Sharing**: Objects are not shared between threads

### Real-World Analogy
Think of a personal workspace where only you have access to your tools and materials, so there's no need to coordinate with others.

### Java Example
```java
public class ThreadConfinementExample {
    // Stack confinement example
    public static void demonstrateStackConfinement() {
        List<String> localList = new ArrayList<>(); // Stack confined
        
        localList.add("Item 1");
        localList.add("Item 2");
        localList.add("Item 3");
        
        processList(localList);
        
        System.out.println("Stack confined list: " + localList);
    }
    
    private static void processList(List<String> list) {
        // List is only accessible within this method
        list.add("Processed item");
    }
    
    // Thread local storage
    public static class ThreadLocalStorage {
        private static final ThreadLocal<String> threadName = new ThreadLocal<>();
        private static final ThreadLocal<Integer> threadId = new ThreadLocal<>();
        
        public static void setThreadInfo(String name, int id) {
            threadName.set(name);
            threadId.set(id);
        }
        
        public static String getThreadName() {
            return threadName.get();
        }
        
        public static Integer getThreadId() {
            return threadId.get();
        }
        
        public static void clear() {
            threadName.remove();
            threadId.remove();
        }
    }
    
    // Thread-specific worker
    public static class ThreadSpecificWorker extends Thread {
        private final String workerName;
        private final List<String> workItems;
        
        public ThreadSpecificWorker(String workerName, List<String> workItems) {
            this.workerName = workerName;
            this.workItems = new ArrayList<>(workItems); // Thread confined
        }
        
        @Override
        public void run() {
            // Set thread local storage
            ThreadLocalStorage.setThreadInfo(workerName, (int) Thread.currentThread().getId());
            
            // Process work items (thread confined)
            for (String item : workItems) {
                System.out.println(ThreadLocalStorage.getThreadName() + " processing: " + item);
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
            
            // Clear thread local storage
            ThreadLocalStorage.clear();
        }
    }
    
    public static void demonstrateThreadConfinement() {
        // Stack confinement
        demonstrateStackConfinement();
        
        // Thread local storage
        ThreadLocalStorage.setThreadInfo("Main Thread", 1);
        System.out.println("Main thread name: " + ThreadLocalStorage.getThreadName());
        System.out.println("Main thread ID: " + ThreadLocalStorage.getThreadId());
        
        // Thread-specific workers
        List<String> workItems1 = Arrays.asList("Task 1", "Task 2", "Task 3");
        List<String> workItems2 = Arrays.asList("Task 4", "Task 5", "Task 6");
        
        ThreadSpecificWorker worker1 = new ThreadSpecificWorker("Worker 1", workItems1);
        ThreadSpecificWorker worker2 = new ThreadSpecificWorker("Worker 2", workItems2);
        
        worker1.start();
        worker2.start();
        
        try {
            worker1.join();
            worker2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 11.5 Stack Confinement

Stack confinement is a form of thread confinement where objects are only accessible within the method that creates them.

### Key Concepts
- **Local Variables**: Objects exist only on the stack
- **Method Scope**: Objects are only accessible within the method
- **No Sharing**: Objects cannot be shared between threads
- **Automatic Cleanup**: Objects are automatically cleaned up when method returns

### Real-World Analogy
Think of a temporary workspace that you set up for a specific task. Once the task is complete, you clean up and the workspace is gone.

### Java Example
```java
public class StackConfinementExample {
    // Stack confined counter
    public static void demonstrateStackConfinement() {
        int counter = 0; // Stack confined
        
        for (int i = 0; i < 10; i++) {
            counter++;
            System.out.println("Counter: " + counter);
        }
        
        // Counter is only accessible within this method
        processCounter(counter);
    }
    
    private static void processCounter(int counter) {
        // Counter is passed by value, so it's still stack confined
        System.out.println("Processing counter: " + counter);
    }
    
    // Stack confined collection
    public static void demonstrateStackConfinedCollection() {
        List<String> items = new ArrayList<>(); // Stack confined
        
        items.add("Item 1");
        items.add("Item 2");
        items.add("Item 3");
        
        // Process items
        for (String item : items) {
            System.out.println("Processing: " + item);
        }
        
        // Items are only accessible within this method
        modifyItems(items);
    }
    
    private static void modifyItems(List<String> items) {
        // Items are passed by reference, but still stack confined
        items.add("Item 4");
        System.out.println("Modified items: " + items);
    }
    
    // Stack confined object
    public static void demonstrateStackConfinedObject() {
        Person person = new Person("John", 30); // Stack confined
        
        person.setAge(31);
        person.setName("John Doe");
        
        System.out.println("Person: " + person);
        
        // Person is only accessible within this method
        processPerson(person);
    }
    
    private static void processPerson(Person person) {
        // Person is passed by reference, but still stack confined
        person.setAge(32);
        System.out.println("Processed person: " + person);
    }
    
    // Simple person class for demonstration
    public static class Person {
        private String name;
        private int age;
        
        public Person(String name, int age) {
            this.name = name;
            this.age = age;
        }
        
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public int getAge() { return age; }
        public void setAge(int age) { this.age = age; }
        
        @Override
        public String toString() {
            return "Person{name='" + name + "', age=" + age + "}";
        }
    }
    
    public static void main(String[] args) {
        demonstrateStackConfinement();
        System.out.println();
        demonstrateStackConfinedCollection();
        System.out.println();
        demonstrateStackConfinedObject();
    }
}
```

## 11.6 ThreadLocal Usage

ThreadLocal provides thread-specific storage, allowing each thread to have its own copy of a variable.

### Key Concepts
- **Thread-Specific**: Each thread has its own copy
- **No Synchronization**: No need for locks or synchronization
- **Memory Management**: Automatic cleanup when thread terminates
- **Performance**: Fast access to thread-local data

### Real-World Analogy
Think of a personal locker where each person has their own space to store their belongings, and no one else can access it.

### Java Example
```java
public class ThreadLocalUsageExample {
    // ThreadLocal for user context
    private static final ThreadLocal<UserContext> userContext = new ThreadLocal<>();
    
    // User context class
    public static class UserContext {
        private final String userId;
        private final String userName;
        private final String sessionId;
        
        public UserContext(String userId, String userName, String sessionId) {
            this.userId = userId;
            this.userName = userName;
            this.sessionId = sessionId;
        }
        
        public String getUserId() { return userId; }
        public String getUserName() { return userName; }
        public String getSessionId() { return sessionId; }
        
        @Override
        public String toString() {
            return "UserContext{userId='" + userId + "', userName='" + userName + "', sessionId='" + sessionId + "'}";
        }
    }
    
    // Service that uses ThreadLocal
    public static class UserService {
        public void setUserContext(UserContext context) {
            userContext.set(context);
        }
        
        public UserContext getCurrentUser() {
            return userContext.get();
        }
        
        public void clearUserContext() {
            userContext.remove();
        }
        
        public void processRequest(String request) {
            UserContext currentUser = getCurrentUser();
            if (currentUser != null) {
                System.out.println("Processing request '" + request + "' for user: " + currentUser.getUserName());
            } else {
                System.out.println("Processing request '" + request + "' for anonymous user");
            }
        }
    }
    
    // ThreadLocal for request ID
    private static final ThreadLocal<String> requestId = new ThreadLocal<>();
    
    // Request processor
    public static class RequestProcessor {
        public void processRequest(String request) {
            // Set request ID for this thread
            requestId.set("REQ-" + System.currentTimeMillis());
            
            System.out.println("Processing request: " + request + " with ID: " + requestId.get());
            
            // Simulate processing
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            System.out.println("Completed request: " + request + " with ID: " + requestId.get());
            
            // Clean up
            requestId.remove();
        }
    }
    
    // ThreadLocal for counter
    private static final ThreadLocal<Integer> threadCounter = new ThreadLocal<Integer>() {
        @Override
        protected Integer initialValue() {
            return 0;
        }
    };
    
    // Counter service
    public static class CounterService {
        public void increment() {
            threadCounter.set(threadCounter.get() + 1);
        }
        
        public int getCount() {
            return threadCounter.get();
        }
        
        public void reset() {
            threadCounter.set(0);
        }
    }
    
    public static void demonstrateThreadLocalUsage() {
        UserService userService = new UserService();
        RequestProcessor requestProcessor = new RequestProcessor();
        CounterService counterService = new CounterService();
        
        // Test user context
        System.out.println("=== User Context Test ===");
        UserContext user1 = new UserContext("user1", "John Doe", "session1");
        UserContext user2 = new UserContext("user2", "Jane Smith", "session2");
        
        userService.setUserContext(user1);
        userService.processRequest("Get profile");
        
        userService.setUserContext(user2);
        userService.processRequest("Update settings");
        
        userService.clearUserContext();
        userService.processRequest("Public data");
        
        // Test request processing
        System.out.println("\n=== Request Processing Test ===");
        Thread requestThread1 = new Thread(() -> requestProcessor.processRequest("Request 1"));
        Thread requestThread2 = new Thread(() -> requestProcessor.processRequest("Request 2"));
        
        requestThread1.start();
        requestThread2.start();
        
        try {
            requestThread1.join();
            requestThread2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Test counter
        System.out.println("\n=== Counter Test ===");
        Thread counterThread1 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                counterService.increment();
                System.out.println("Thread 1 counter: " + counterService.getCount());
            }
        });
        
        Thread counterThread2 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                counterService.increment();
                System.out.println("Thread 2 counter: " + counterService.getCount());
            }
        });
        
        counterThread1.start();
        counterThread2.start();
        
        try {
            counterThread1.join();
            counterThread2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 11.7 Final Fields and Immutability

Final fields provide a way to ensure that certain fields cannot be modified after object construction, contributing to immutability.

### Key Concepts
- **Final Fields**: Fields that cannot be modified after construction
- **Immutable References**: References that cannot be reassigned
- **Thread Safety**: Final fields are thread-safe after construction
- **Memory Visibility**: Final fields are visible to other threads

### Real-World Analogy
Think of a contract that's signed and sealed. Once signed, the terms cannot be changed, and everyone can rely on the terms being the same.

### Java Example
```java
public class FinalFieldsImmutabilityExample {
    // Immutable class using final fields
    public static final class ImmutablePoint {
        private final double x;
        private final double y;
        
        public ImmutablePoint(double x, double y) {
            this.x = x;
            this.y = y;
        }
        
        public double getX() { return x; }
        public double getY() { return y; }
        
        public ImmutablePoint move(double dx, double dy) {
            return new ImmutablePoint(x + dx, y + dy);
        }
        
        @Override
        public String toString() {
            return "Point{x=" + x + ", y=" + y + "}";
        }
    }
    
    // Immutable person class
    public static final class ImmutablePerson {
        private final String name;
        private final int age;
        private final List<String> hobbies;
        
        public ImmutablePerson(String name, int age, List<String> hobbies) {
            this.name = name;
            this.age = age;
            this.hobbies = Collections.unmodifiableList(new ArrayList<>(hobbies));
        }
        
        public String getName() { return name; }
        public int getAge() { return age; }
        public List<String> getHobbies() { return hobbies; }
        
        @Override
        public String toString() {
            return "Person{name='" + name + "', age=" + age + ", hobbies=" + hobbies + "}";
        }
    }
    
    // Immutable configuration class
    public static final class ImmutableConfig {
        private final String databaseUrl;
        private final int maxConnections;
        private final boolean debugMode;
        private final Map<String, String> properties;
        
        public ImmutableConfig(String databaseUrl, int maxConnections, boolean debugMode, Map<String, String> properties) {
            this.databaseUrl = databaseUrl;
            this.maxConnections = maxConnections;
            this.debugMode = debugMode;
            this.properties = Collections.unmodifiableMap(new HashMap<>(properties));
        }
        
        public String getDatabaseUrl() { return databaseUrl; }
        public int getMaxConnections() { return maxConnections; }
        public boolean isDebugMode() { return debugMode; }
        public Map<String, String> getProperties() { return properties; }
        
        @Override
        public String toString() {
            return "Config{databaseUrl='" + databaseUrl + "', maxConnections=" + maxConnections + 
                   ", debugMode=" + debugMode + ", properties=" + properties + "}";
        }
    }
    
    // Thread-safe counter using final fields
    public static final class ThreadSafeCounter {
        private final AtomicInteger count;
        private final String name;
        
        public ThreadSafeCounter(String name) {
            this.name = name;
            this.count = new AtomicInteger(0);
        }
        
        public void increment() {
            count.incrementAndGet();
        }
        
        public int getCount() {
            return count.get();
        }
        
        public String getName() { return name; }
        
        @Override
        public String toString() {
            return "Counter{name='" + name + "', count=" + count.get() + "}";
        }
    }
    
    public static void demonstrateFinalFieldsImmutability() {
        // Immutable point
        ImmutablePoint point1 = new ImmutablePoint(0, 0);
        ImmutablePoint point2 = point1.move(3, 4);
        System.out.println("Point1: " + point1);
        System.out.println("Point2: " + point2);
        
        // Immutable person
        List<String> hobbies = Arrays.asList("Reading", "Swimming", "Cooking");
        ImmutablePerson person = new ImmutablePerson("John", 30, hobbies);
        System.out.println("Person: " + person);
        
        // Immutable configuration
        Map<String, String> properties = new HashMap<>();
        properties.put("timeout", "30");
        properties.put("retries", "3");
        ImmutableConfig config = new ImmutableConfig("jdbc:mysql://localhost:3306/mydb", 10, true, properties);
        System.out.println("Config: " + config);
        
        // Thread-safe counter
        ThreadSafeCounter counter = new ThreadSafeCounter("TestCounter");
        counter.increment();
        counter.increment();
        System.out.println("Counter: " + counter);
    }
}
```

## 11.8 Safe Publication

Safe publication ensures that objects are properly initialized and visible to other threads when they are published.

### Key Concepts
- **Publication**: Making an object visible to other threads
- **Initialization**: Ensuring object is fully constructed
- **Visibility**: Ensuring changes are visible to other threads
- **Happens-Before**: Establishing ordering relationships

### Real-World Analogy
Think of a press release that's only sent out after all the details are finalized and verified, ensuring everyone gets the complete and accurate information.

### Java Example
```java
public class SafePublicationExample {
    // Unsafe publication
    public static class UnsafePublication {
        private String data;
        private boolean initialized = false;
        
        public void setData(String data) {
            this.data = data;
            this.initialized = true;
        }
        
        public String getData() {
            if (initialized) {
                return data;
            }
            return null;
        }
    }
    
    // Safe publication using volatile
    public static class SafePublicationVolatile {
        private volatile String data;
        private volatile boolean initialized = false;
        
        public void setData(String data) {
            this.data = data;
            this.initialized = true;
        }
        
        public String getData() {
            if (initialized) {
                return data;
            }
            return null;
        }
    }
    
    // Safe publication using synchronized
    public static class SafePublicationSynchronized {
        private String data;
        private boolean initialized = false;
        private final Object lock = new Object();
        
        public void setData(String data) {
            synchronized (lock) {
                this.data = data;
                this.initialized = true;
            }
        }
        
        public String getData() {
            synchronized (lock) {
                if (initialized) {
                    return data;
                }
                return null;
            }
        }
    }
    
    // Safe publication using final fields
    public static class SafePublicationFinal {
        private final String data;
        private final boolean initialized;
        
        public SafePublicationFinal(String data) {
            this.data = data;
            this.initialized = true;
        }
        
        public String getData() {
            if (initialized) {
                return data;
            }
            return null;
        }
    }
    
    // Safe publication using static initializer
    public static class SafePublicationStatic {
        private static final String data;
        
        static {
            data = "Initialized data";
        }
        
        public static String getData() {
            return data;
        }
    }
    
    // Safe publication using atomic reference
    public static class SafePublicationAtomic {
        private final AtomicReference<String> data = new AtomicReference<>();
        
        public void setData(String data) {
            this.data.set(data);
        }
        
        public String getData() {
            return data.get();
        }
    }
    
    public static void demonstrateSafePublication() {
        // Test unsafe publication
        System.out.println("=== Unsafe Publication Test ===");
        UnsafePublication unsafe = new UnsafePublication();
        
        Thread writer = new Thread(() -> {
            unsafe.setData("Hello World");
        });
        
        Thread reader = new Thread(() -> {
            String data = unsafe.getData();
            System.out.println("Unsafe data: " + data);
        });
        
        writer.start();
        reader.start();
        
        try {
            writer.join();
            reader.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Test safe publication with volatile
        System.out.println("\n=== Safe Publication with Volatile Test ===");
        SafePublicationVolatile safeVolatile = new SafePublicationVolatile();
        
        Thread writer2 = new Thread(() -> {
            safeVolatile.setData("Hello World");
        });
        
        Thread reader2 = new Thread(() -> {
            String data = safeVolatile.getData();
            System.out.println("Safe volatile data: " + data);
        });
        
        writer2.start();
        reader2.start();
        
        try {
            writer2.join();
            reader2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Test safe publication with final fields
        System.out.println("\n=== Safe Publication with Final Fields Test ===");
        SafePublicationFinal safeFinal = new SafePublicationFinal("Hello World");
        System.out.println("Safe final data: " + safeFinal.getData());
        
        // Test safe publication with static initializer
        System.out.println("\n=== Safe Publication with Static Initializer Test ===");
        System.out.println("Safe static data: " + SafePublicationStatic.getData());
    }
}
```

This comprehensive explanation covers all aspects of thread safety and immutability, providing both theoretical understanding and practical Java examples to illustrate each concept.