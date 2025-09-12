# Section 5 - Thread Safety

## 5.1 Thread Safety Fundamentals

Thread safety is the property of a program that ensures it behaves correctly when accessed by multiple threads simultaneously. A thread-safe program guarantees that shared data is accessed in a way that prevents race conditions and data corruption.

### What Makes Code Thread-Safe?

#### 1. **No Race Conditions**
- Multiple threads can access shared data safely
- No data corruption or inconsistent states
- Predictable behavior regardless of thread scheduling

#### 2. **Atomic Operations**
- Operations complete entirely or not at all
- No partial execution visible to other threads
- All-or-nothing behavior

#### 3. **Proper Synchronization**
- Critical sections are protected
- Shared resources are accessed safely
- Threads coordinate their access

### Thread Safety Levels:

#### 1. **Not Thread-Safe**
```java
public class NotThreadSafeExample {
    private int counter = 0;
    
    public void increment() {
        counter++; // Not thread-safe
    }
    
    public int getCounter() {
        return counter; // Not thread-safe
    }
    
    public static void main(String[] args) throws InterruptedException {
        NotThreadSafeExample example = new NotThreadSafeExample();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    example.increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Counter: " + example.getCounter()); // Unpredictable result
    }
}
```

#### 2. **Thread-Safe with Synchronization**
```java
public class ThreadSafeWithSynchronization {
    private int counter = 0;
    private final Object lock = new Object();
    
    public void increment() {
        synchronized (lock) {
            counter++; // Thread-safe
        }
    }
    
    public int getCounter() {
        synchronized (lock) {
            return counter; // Thread-safe
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadSafeWithSynchronization example = new ThreadSafeWithSynchronization();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    example.increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Counter: " + example.getCounter()); // Always 10000
    }
}
```

#### 3. **Thread-Safe with Atomic Operations**
```java
import java.util.concurrent.atomic.AtomicInteger;

public class ThreadSafeWithAtomic {
    private final AtomicInteger counter = new AtomicInteger(0);
    
    public void increment() {
        counter.incrementAndGet(); // Thread-safe
    }
    
    public int getCounter() {
        return counter.get(); // Thread-safe
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadSafeWithAtomic example = new ThreadSafeWithAtomic();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    example.increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Counter: " + example.getCounter()); // Always 10000
    }
}
```

### Real-World Analogy:
Think of thread safety like a bank account:
- **Not Thread-Safe**: Like having multiple people withdraw money simultaneously without any control
- **Thread-Safe**: Like having a teller who ensures only one person can access the account at a time
- **Atomic Operations**: Like having a machine that processes transactions completely or not at all

## 5.2 Immutable Objects

Immutable objects are objects whose state cannot be modified after creation. They are inherently thread-safe because they cannot be changed by any thread.

### Characteristics of Immutable Objects:

#### 1. **Final Fields**
- All fields are declared final
- Cannot be reassigned after construction
- State is fixed at creation time

#### 2. **No Mutator Methods**
- No methods that modify the object's state
- Only accessor methods (getters)
- No side effects

#### 3. **Proper Construction**
- All fields initialized in constructor
- No this reference escape during construction
- Defensive copying if needed

### Immutable Object Example:

```java
public class ImmutablePerson {
    private final String name;
    private final int age;
    private final List<String> hobbies;
    
    public ImmutablePerson(String name, int age, List<String> hobbies) {
        this.name = name;
        this.age = age;
        // Defensive copying to prevent external modification
        this.hobbies = Collections.unmodifiableList(new ArrayList<>(hobbies));
    }
    
    public String getName() {
        return name;
    }
    
    public int getAge() {
        return age;
    }
    
    public List<String> getHobbies() {
        return hobbies; // Safe to return - unmodifiable
    }
    
    // No mutator methods - object cannot be modified
    
    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + ", hobbies=" + hobbies + "}";
    }
    
    public static void main(String[] args) {
        List<String> hobbies = new ArrayList<>();
        hobbies.add("Reading");
        hobbies.add("Swimming");
        
        ImmutablePerson person = new ImmutablePerson("John", 30, hobbies);
        System.out.println(person);
        
        // Try to modify the original list
        hobbies.add("Cooking");
        System.out.println("Original list: " + hobbies);
        System.out.println("Person hobbies: " + person.getHobbies()); // Unchanged
        
        // Try to modify the returned list
        try {
            person.getHobbies().add("Dancing"); // This will throw UnsupportedOperationException
        } catch (UnsupportedOperationException e) {
            System.out.println("Cannot modify hobbies list: " + e.getMessage());
        }
    }
}
```

### Immutable Collections:

```java
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class ImmutableCollectionsExample {
    public static void main(String[] args) {
        // Create immutable collections
        List<String> immutableList = List.of("apple", "banana", "cherry");
        Set<String> immutableSet = Set.of("red", "green", "blue");
        Map<String, Integer> immutableMap = Map.of("one", 1, "two", 2, "three", 3);
        
        // Try to modify (will throw UnsupportedOperationException)
        try {
            immutableList.add("date");
        } catch (UnsupportedOperationException e) {
            System.out.println("Cannot modify immutable list: " + e.getMessage());
        }
        
        try {
            immutableSet.remove("red");
        } catch (UnsupportedOperationException e) {
            System.out.println("Cannot modify immutable set: " + e.getMessage());
        }
        
        try {
            immutableMap.put("four", 4);
        } catch (UnsupportedOperationException e) {
            System.out.println("Cannot modify immutable map: " + e.getMessage());
        }
        
        // Safe to access from multiple threads
        System.out.println("List: " + immutableList);
        System.out.println("Set: " + immutableSet);
        System.out.println("Map: " + immutableMap);
    }
}
```

### Builder Pattern for Immutable Objects:

```java
public class ImmutableConfig {
    private final String host;
    private final int port;
    private final boolean sslEnabled;
    private final int timeout;
    
    private ImmutableConfig(Builder builder) {
        this.host = builder.host;
        this.port = builder.port;
        this.sslEnabled = builder.sslEnabled;
        this.timeout = builder.timeout;
    }
    
    public String getHost() { return host; }
    public int getPort() { return port; }
    public boolean isSslEnabled() { return sslEnabled; }
    public int getTimeout() { return timeout; }
    
    public static class Builder {
        private String host = "localhost";
        private int port = 8080;
        private boolean sslEnabled = false;
        private int timeout = 5000;
        
        public Builder host(String host) {
            this.host = host;
            return this;
        }
        
        public Builder port(int port) {
            this.port = port;
            return this;
        }
        
        public Builder sslEnabled(boolean sslEnabled) {
            this.sslEnabled = sslEnabled;
            return this;
        }
        
        public Builder timeout(int timeout) {
            this.timeout = timeout;
            return this;
        }
        
        public ImmutableConfig build() {
            return new ImmutableConfig(this);
        }
    }
    
    public static void main(String[] args) {
        ImmutableConfig config = new ImmutableConfig.Builder()
            .host("example.com")
            .port(443)
            .sslEnabled(true)
            .timeout(10000)
            .build();
        
        System.out.println("Config: " + config);
    }
}
```

## 5.3 Thread-Safe Data Structures

Thread-safe data structures are collections that can be safely accessed by multiple threads without external synchronization. Java provides several thread-safe collections in the `java.util.concurrent` package.

### Concurrent Collections:

#### 1. **ConcurrentHashMap**
```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

public class ConcurrentHashMapExample {
    private final ConcurrentMap<String, Integer> map = new ConcurrentHashMap<>();
    
    public void put(String key, Integer value) {
        map.put(key, value);
    }
    
    public Integer get(String key) {
        return map.get(key);
    }
    
    public void increment(String key) {
        map.compute(key, (k, v) -> v == null ? 1 : v + 1);
    }
    
    public static void main(String[] args) throws InterruptedException {
        ConcurrentHashMapExample example = new ConcurrentHashMapExample();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    example.increment("counter");
                    example.put("thread" + threadId, threadId);
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Counter value: " + example.get("counter"));
        System.out.println("Map size: " + example.map.size());
    }
}
```

#### 2. **ConcurrentLinkedQueue**
```java
import java.util.concurrent.ConcurrentLinkedQueue;

public class ConcurrentLinkedQueueExample {
    private final ConcurrentLinkedQueue<String> queue = new ConcurrentLinkedQueue<>();
    
    public void add(String item) {
        queue.offer(item);
    }
    
    public String poll() {
        return queue.poll();
    }
    
    public int size() {
        return queue.size();
    }
    
    public static void main(String[] args) throws InterruptedException {
        ConcurrentLinkedQueueExample example = new ConcurrentLinkedQueueExample();
        
        // Producer threads
        Thread[] producers = new Thread[3];
        for (int i = 0; i < 3; i++) {
            final int producerId = i;
            producers[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    example.add("Producer" + producerId + "-Item" + j);
                }
            });
            producers[i].start();
        }
        
        // Consumer threads
        Thread[] consumers = new Thread[2];
        for (int i = 0; i < 2; i++) {
            consumers[i] = new Thread(() -> {
                String item;
                while ((item = example.poll()) != null) {
                    System.out.println("Consumed: " + item);
                }
            });
            consumers[i].start();
        }
        
        for (Thread producer : producers) {
            producer.join();
        }
        
        for (Thread consumer : consumers) {
            consumer.join();
        }
    }
}
```

#### 3. **CopyOnWriteArrayList**
```java
import java.util.concurrent.CopyOnWriteArrayList;

public class CopyOnWriteArrayListExample {
    private final CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
    
    public void add(String item) {
        list.add(item);
    }
    
    public void remove(String item) {
        list.remove(item);
    }
    
    public void iterate() {
        // Safe to iterate without synchronization
        for (String item : list) {
            System.out.println("Item: " + item);
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        CopyOnWriteArrayListExample example = new CopyOnWriteArrayListExample();
        
        // Add some items
        example.add("item1");
        example.add("item2");
        example.add("item3");
        
        // Reader thread
        Thread reader = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                example.iterate();
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Writer thread
        Thread writer = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                example.add("newItem" + i);
                try {
                    Thread.sleep(150);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        reader.start();
        writer.start();
        
        reader.join();
        writer.join();
    }
}
```

### Blocking Queues:

#### 1. **ArrayBlockingQueue**
```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class ArrayBlockingQueueExample {
    private final BlockingQueue<String> queue = new ArrayBlockingQueue<>(5);
    
    public void produce(String item) throws InterruptedException {
        queue.put(item); // Blocks if queue is full
        System.out.println("Produced: " + item);
    }
    
    public String consume() throws InterruptedException {
        String item = queue.take(); // Blocks if queue is empty
        System.out.println("Consumed: " + item);
        return item;
    }
    
    public static void main(String[] args) throws InterruptedException {
        ArrayBlockingQueueExample example = new ArrayBlockingQueueExample();
        
        // Producer thread
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    example.produce("Item" + i);
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Consumer thread
        Thread consumer = new Thread(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    example.consume();
                    Thread.sleep(150);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        producer.start();
        consumer.start();
        
        producer.join();
        consumer.join();
    }
}
```

#### 2. **LinkedBlockingQueue**
```java
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class LinkedBlockingQueueExample {
    private final BlockingQueue<Integer> queue = new LinkedBlockingQueue<>();
    
    public void produce(int item) throws InterruptedException {
        queue.put(item);
        System.out.println("Produced: " + item);
    }
    
    public Integer consume() throws InterruptedException {
        Integer item = queue.take();
        System.out.println("Consumed: " + item);
        return item;
    }
    
    public static void main(String[] args) throws InterruptedException {
        LinkedBlockingQueueExample example = new LinkedBlockingQueueExample();
        
        // Multiple producers
        Thread[] producers = new Thread[3];
        for (int i = 0; i < 3; i++) {
            final int producerId = i;
            producers[i] = new Thread(() -> {
                try {
                    for (int j = 0; j < 5; j++) {
                        example.produce(producerId * 10 + j);
                        Thread.sleep(100);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            producers[i].start();
        }
        
        // Multiple consumers
        Thread[] consumers = new Thread[2];
        for (int i = 0; i < 2; i++) {
            consumers[i] = new Thread(() -> {
                try {
                    for (int j = 0; j < 7; j++) {
                        example.consume();
                        Thread.sleep(150);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            consumers[i].start();
        }
        
        for (Thread producer : producers) {
            producer.join();
        }
        
        for (Thread consumer : consumers) {
            consumer.join();
        }
    }
}
```

## 5.4 Thread Confinement

Thread confinement is a technique where data is restricted to a single thread, eliminating the need for synchronization. It's one of the most effective ways to achieve thread safety.

### Types of Thread Confinement:

#### 1. **Stack Confinement**
```java
public class StackConfinementExample {
    public void processData() {
        // Local variables are stack-confined
        int localCounter = 0;
        String localData = "Hello";
        
        // These variables are only accessible within this method
        // and by the thread that calls this method
        for (int i = 0; i < 1000; i++) {
            localCounter++;
            localData = localData + i;
        }
        
        System.out.println("Local counter: " + localCounter);
        System.out.println("Local data: " + localData);
    }
    
    public static void main(String[] args) throws InterruptedException {
        StackConfinementExample example = new StackConfinementExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(example::processData);
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### 2. **ThreadLocal Confinement**
```java
public class ThreadLocalConfinementExample {
    private static final ThreadLocal<Integer> threadLocalCounter = new ThreadLocal<Integer>() {
        @Override
        protected Integer initialValue() {
            return 0;
        }
    };
    
    private static final ThreadLocal<String> threadLocalData = new ThreadLocal<String>() {
        @Override
        protected String initialValue() {
            return "Thread-" + Thread.currentThread().getName();
        }
    };
    
    public void increment() {
        int current = threadLocalCounter.get();
        threadLocalCounter.set(current + 1);
    }
    
    public void setData(String data) {
        threadLocalData.set(data);
    }
    
    public int getCounter() {
        return threadLocalCounter.get();
    }
    
    public String getData() {
        return threadLocalData.get();
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadLocalConfinementExample example = new ThreadLocalConfinementExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    example.increment();
                }
                example.setData("Data from thread " + threadId);
                
                System.out.println("Thread " + threadId + 
                                 " counter: " + example.getCounter() + 
                                 ", data: " + example.getData());
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### 3. **Object Confinement**
```java
public class ObjectConfinementExample {
    private static class ConfinedObject {
        private int value = 0;
        private String data = "";
        
        public void increment() {
            value++;
        }
        
        public void setData(String newData) {
            data = newData;
        }
        
        public int getValue() {
            return value;
        }
        
        public String getData() {
            return data;
        }
    }
    
    public void processWithConfinedObject() {
        // Object is confined to this method's scope
        ConfinedObject obj = new ConfinedObject();
        
        for (int i = 0; i < 1000; i++) {
            obj.increment();
        }
        
        obj.setData("Processed by " + Thread.currentThread().getName());
        
        System.out.println("Thread " + Thread.currentThread().getName() + 
                         " - Value: " + obj.getValue() + 
                         ", Data: " + obj.getData());
    }
    
    public static void main(String[] args) throws InterruptedException {
        ObjectConfinementExample example = new ObjectConfinementExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(example::processWithConfinedObject);
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

## 5.5 Stack Confinement

Stack confinement is a specific type of thread confinement where variables are stored on the thread's stack and are only accessible to that thread.

### Stack Confinement Examples:

#### 1. **Local Variables**
```java
public class LocalVariableExample {
    public void processData() {
        // Local variables are stack-confined
        int localSum = 0;
        String localResult = "";
        
        for (int i = 0; i < 1000; i++) {
            localSum += i;
            localResult += i + " ";
        }
        
        System.out.println("Thread " + Thread.currentThread().getName() + 
                         " - Sum: " + localSum);
    }
    
    public static void main(String[] args) throws InterruptedException {
        LocalVariableExample example = new LocalVariableExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(example::processData);
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### 2. **Method Parameters**
```java
public class MethodParameterExample {
    public void processParameter(int value, String data) {
        // Parameters are stack-confined
        int processedValue = value * 2;
        String processedData = data.toUpperCase();
        
        System.out.println("Thread " + Thread.currentThread().getName() + 
                         " - Processed value: " + processedValue + 
                         ", Processed data: " + processedData);
    }
    
    public static void main(String[] args) throws InterruptedException {
        MethodParameterExample example = new MethodParameterExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                example.processParameter(threadId * 10, "data" + threadId);
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### 3. **Local Objects**
```java
public class LocalObjectExample {
    public void processWithLocalObject() {
        // Local object is stack-confined
        StringBuilder localBuilder = new StringBuilder();
        List<Integer> localList = new ArrayList<>();
        
        for (int i = 0; i < 100; i++) {
            localBuilder.append(i).append(" ");
            localList.add(i);
        }
        
        System.out.println("Thread " + Thread.currentThread().getName() + 
                         " - Builder length: " + localBuilder.length() + 
                         ", List size: " + localList.size());
    }
    
    public static void main(String[] args) throws InterruptedException {
        LocalObjectExample example = new LocalObjectExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(example::processWithLocalObject);
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

## 5.6 ThreadLocal Storage

ThreadLocal storage provides thread-local variables. Each thread has its own independent copy of the variable, eliminating the need for synchronization.

### ThreadLocal Basics:

#### 1. **Simple ThreadLocal**
```java
public class SimpleThreadLocalExample {
    private static final ThreadLocal<Integer> threadLocalValue = new ThreadLocal<Integer>() {
        @Override
        protected Integer initialValue() {
            return 0;
        }
    };
    
    public void increment() {
        int current = threadLocalValue.get();
        threadLocalValue.set(current + 1);
    }
    
    public int getValue() {
        return threadLocalValue.get();
    }
    
    public static void main(String[] args) throws InterruptedException {
        SimpleThreadLocalExample example = new SimpleThreadLocalExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    example.increment();
                }
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " final value: " + example.getValue());
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### 2. **ThreadLocal with Custom Initial Value**
```java
public class CustomThreadLocalExample {
    private static final ThreadLocal<String> threadLocalName = new ThreadLocal<String>() {
        @Override
        protected String initialValue() {
            return "Thread-" + Thread.currentThread().getName();
        }
    };
    
    private static final ThreadLocal<Long> threadLocalStartTime = new ThreadLocal<Long>() {
        @Override
        protected Long initialValue() {
            return System.currentTimeMillis();
        }
    };
    
    public void setThreadName(String name) {
        threadLocalName.set(name);
    }
    
    public String getThreadName() {
        return threadLocalName.get();
    }
    
    public long getElapsedTime() {
        return System.currentTimeMillis() - threadLocalStartTime.get();
    }
    
    public static void main(String[] args) throws InterruptedException {
        CustomThreadLocalExample example = new CustomThreadLocalExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                example.setThreadName("CustomThread-" + threadId);
                
                try {
                    Thread.sleep(1000 + threadId * 100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                System.out.println("Thread " + threadId + 
                                 " - Name: " + example.getThreadName() + 
                                 ", Elapsed: " + example.getElapsedTime() + "ms");
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### 3. **ThreadLocal with Cleanup**
```java
public class ThreadLocalCleanupExample {
    private static final ThreadLocal<StringBuilder> threadLocalBuilder = new ThreadLocal<StringBuilder>() {
        @Override
        protected StringBuilder initialValue() {
            return new StringBuilder();
        }
    };
    
    public void append(String text) {
        threadLocalBuilder.get().append(text);
    }
    
    public String getResult() {
        return threadLocalBuilder.get().toString();
    }
    
    public void cleanup() {
        threadLocalBuilder.remove(); // Clean up to prevent memory leaks
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadLocalCleanupExample example = new ThreadLocalCleanupExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                try {
                    for (int j = 0; j < 10; j++) {
                        example.append("Thread" + threadId + "-" + j + " ");
                    }
                    
                    System.out.println("Thread " + threadId + 
                                     " result: " + example.getResult());
                } finally {
                    example.cleanup(); // Always clean up
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

## 5.7 Volatile Variables

Volatile variables ensure that reads and writes to the variable are visible to all threads. They provide a weaker form of synchronization than locks but are useful for simple flags and counters.

### Volatile Keyword:

#### 1. **Basic Volatile Usage**
```java
public class VolatileExample {
    private volatile boolean flag = false;
    private int value = 0;
    
    public void writer() {
        value = 42;
        flag = true; // Volatile write
    }
    
    public void reader() {
        if (flag) { // Volatile read
            System.out.println("Value: " + value); // Will always see 42
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        VolatileExample example = new VolatileExample();
        
        Thread writer = new Thread(example::writer);
        Thread reader = new Thread(example::reader);
        
        reader.start();
        writer.start();
        
        writer.join();
        reader.join();
    }
}
```

#### 2. **Volatile vs Non-Volatile**
```java
public class VolatileComparisonExample {
    private boolean nonVolatileFlag = false;
    private volatile boolean volatileFlag = false;
    private int value = 0;
    
    public void setNonVolatile() {
        value = 42;
        nonVolatileFlag = true; // Non-volatile write
    }
    
    public void setVolatile() {
        value = 42;
        volatileFlag = true; // Volatile write
    }
    
    public void checkNonVolatile() {
        if (nonVolatileFlag) {
            System.out.println("Non-volatile value: " + value); // May not see 42
        }
    }
    
    public void checkVolatile() {
        if (volatileFlag) {
            System.out.println("Volatile value: " + value); // Will always see 42
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        VolatileComparisonExample example = new VolatileComparisonExample();
        
        // Test non-volatile
        Thread writer1 = new Thread(example::setNonVolatile);
        Thread reader1 = new Thread(example::checkNonVolatile);
        
        reader1.start();
        writer1.start();
        
        writer1.join();
        reader1.join();
        
        // Test volatile
        Thread writer2 = new Thread(example::setVolatile);
        Thread reader2 = new Thread(example::checkVolatile);
        
        reader2.start();
        writer2.start();
        
        writer2.join();
        reader2.join();
    }
}
```

#### 3. **Volatile Counter (Incorrect Usage)**
```java
public class VolatileCounterExample {
    private volatile int counter = 0;
    
    public void increment() {
        counter++; // This is NOT thread-safe!
    }
    
    public int getCounter() {
        return counter;
    }
    
    public static void main(String[] args) throws InterruptedException {
        VolatileCounterExample example = new VolatileCounterExample();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    example.increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Counter: " + example.getCounter()); // May not be 10000
    }
}
```

## 5.8 Final Fields

Final fields are immutable once initialized and provide thread safety guarantees. They are particularly useful for creating immutable objects.

### Final Field Thread Safety:

#### 1. **Final Fields in Immutable Objects**
```java
public class FinalFieldExample {
    private final int value;
    private final String name;
    private final List<String> items;
    
    public FinalFieldExample(int value, String name, List<String> items) {
        this.value = value;
        this.name = name;
        // Defensive copying for mutable collections
        this.items = Collections.unmodifiableList(new ArrayList<>(items));
    }
    
    public int getValue() {
        return value;
    }
    
    public String getName() {
        return name;
    }
    
    public List<String> getItems() {
        return items; // Safe to return - unmodifiable
    }
    
    public static void main(String[] args) throws InterruptedException {
        List<String> items = new ArrayList<>();
        items.add("item1");
        items.add("item2");
        
        FinalFieldExample example = new FinalFieldExample(42, "Test", items);
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                // Safe to access final fields from multiple threads
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " - Value: " + example.getValue() + 
                                 ", Name: " + example.getName() + 
                                 ", Items: " + example.getItems());
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### 2. **Final Fields with Lazy Initialization**
```java
public class LazyInitializationExample {
    private final String expensiveValue;
    
    public LazyInitializationExample() {
        // Expensive computation in constructor
        this.expensiveValue = computeExpensiveValue();
    }
    
    private String computeExpensiveValue() {
        // Simulate expensive computation
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 1000; i++) {
            sb.append(i).append(" ");
        }
        return sb.toString();
    }
    
    public String getExpensiveValue() {
        return expensiveValue; // Safe to access from multiple threads
    }
    
    public static void main(String[] args) throws InterruptedException {
        LazyInitializationExample example = new LazyInitializationExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " - Value length: " + example.getExpensiveValue().length());
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

## 5.9 Safe Publication

Safe publication ensures that an object is properly initialized and visible to other threads. It's crucial for sharing objects between threads safely.

### Safe Publication Patterns:

#### 1. **Static Initialization**
```java
public class StaticInitializationExample {
    private static final String STATIC_VALUE = "Hello World";
    private static final int STATIC_NUMBER = 42;
    
    public static String getStaticValue() {
        return STATIC_VALUE; // Safe - static final
    }
    
    public static int getStaticNumber() {
        return STATIC_NUMBER; // Safe - static final
    }
    
    public static void main(String[] args) throws InterruptedException {
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " - Value: " + getStaticValue() + 
                                 ", Number: " + getStaticNumber());
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### 2. **Volatile Reference**
```java
public class VolatileReferenceExample {
    private volatile String volatileValue = null;
    
    public void setValue(String value) {
        this.volatileValue = value; // Safe publication
    }
    
    public String getValue() {
        return volatileValue; // Safe read
    }
    
    public static void main(String[] args) throws InterruptedException {
        VolatileReferenceExample example = new VolatileReferenceExample();
        
        // Writer thread
        Thread writer = new Thread(() -> {
            example.setValue("Published value");
        });
        
        // Reader threads
        Thread[] readers = new Thread[5];
        for (int i = 0; i < 5; i++) {
            readers[i] = new Thread(() -> {
                String value = example.getValue();
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " - Value: " + value);
            });
        }
        
        writer.start();
        for (Thread reader : readers) {
            reader.start();
        }
        
        writer.join();
        for (Thread reader : readers) {
            reader.join();
        }
    }
}
```

#### 3. **Synchronized Publication**
```java
public class SynchronizedPublicationExample {
    private String value = null;
    private final Object lock = new Object();
    
    public void setValue(String value) {
        synchronized (lock) {
            this.value = value; // Safe publication
        }
    }
    
    public String getValue() {
        synchronized (lock) {
            return value; // Safe read
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        SynchronizedPublicationExample example = new SynchronizedPublicationExample();
        
        // Writer thread
        Thread writer = new Thread(() -> {
            example.setValue("Synchronized value");
        });
        
        // Reader threads
        Thread[] readers = new Thread[5];
        for (int i = 0; i < 5; i++) {
            readers[i] = new Thread(() -> {
                String value = example.getValue();
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " - Value: " + value);
            });
        }
        
        writer.start();
        for (Thread reader : readers) {
            reader.start();
        }
        
        writer.join();
        for (Thread reader : readers) {
            reader.join();
        }
    }
}
```

## 5.10 Thread Safety Patterns

Thread safety patterns are common design patterns that help achieve thread safety in multithreaded applications.

### Common Thread Safety Patterns:

#### 1. **Monitor Pattern**
```java
public class MonitorPatternExample {
    private final Object lock = new Object();
    private int value = 0;
    private boolean ready = false;
    
    public void setValue(int value) {
        synchronized (lock) {
            this.value = value;
            this.ready = true;
            lock.notifyAll(); // Notify waiting threads
        }
    }
    
    public int getValue() throws InterruptedException {
        synchronized (lock) {
            while (!ready) {
                lock.wait(); // Wait until value is ready
            }
            return value;
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        MonitorPatternExample example = new MonitorPatternExample();
        
        // Reader threads
        Thread[] readers = new Thread[3];
        for (int i = 0; i < 3; i++) {
            readers[i] = new Thread(() -> {
                try {
                    int value = example.getValue();
                    System.out.println("Thread " + Thread.currentThread().getName() + 
                                     " got value: " + value);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            readers[i].start();
        }
        
        // Writer thread
        Thread writer = new Thread(() -> {
            try {
                Thread.sleep(1000); // Simulate work
                example.setValue(42);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        writer.start();
        
        for (Thread reader : readers) {
            reader.join();
        }
        writer.join();
    }
}
```

#### 2. **Thread-Safe Singleton Pattern**
```java
public class ThreadSafeSingletonExample {
    private static volatile ThreadSafeSingletonExample instance;
    
    private ThreadSafeSingletonExample() {
        // Private constructor
    }
    
    public static ThreadSafeSingletonExample getInstance() {
        if (instance == null) {
            synchronized (ThreadSafeSingletonExample.class) {
                if (instance == null) {
                    instance = new ThreadSafeSingletonExample();
                }
            }
        }
        return instance;
    }
    
    public void doSomething() {
        System.out.println("Singleton instance: " + this);
    }
    
    public static void main(String[] args) throws InterruptedException {
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                ThreadSafeSingletonExample instance = getInstance();
                instance.doSomething();
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### 3. **Thread-Safe Builder Pattern**
```java
public class ThreadSafeBuilderExample {
    private final String name;
    private final int age;
    private final String email;
    
    private ThreadSafeBuilderExample(Builder builder) {
        this.name = builder.name;
        this.age = builder.age;
        this.email = builder.email;
    }
    
    public String getName() { return name; }
    public int getAge() { return age; }
    public String getEmail() { return email; }
    
    public static class Builder {
        private String name;
        private int age;
        private String email;
        
        public Builder name(String name) {
            this.name = name;
            return this;
        }
        
        public Builder age(int age) {
            this.age = age;
            return this;
        }
        
        public Builder email(String email) {
            this.email = email;
            return this;
        }
        
        public ThreadSafeBuilderExample build() {
            return new ThreadSafeBuilderExample(this);
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                ThreadSafeBuilderExample person = new ThreadSafeBuilderExample.Builder()
                    .name("Person" + threadId)
                    .age(20 + threadId)
                    .email("person" + threadId + "@example.com")
                    .build();
                
                System.out.println("Thread " + threadId + 
                                 " - Name: " + person.getName() + 
                                 ", Age: " + person.getAge() + 
                                 ", Email: " + person.getEmail());
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

### Real-World Analogy:
Think of thread safety like different types of security systems:
- **Immutable Objects**: Like a museum display - once set up, it can't be changed
- **Thread-Safe Collections**: Like a bank vault with proper access controls
- **Thread Confinement**: Like having your own private office
- **ThreadLocal Storage**: Like having your own personal locker
- **Volatile Variables**: Like a public announcement board that everyone can see
- **Final Fields**: Like a contract that can't be modified once signed
- **Safe Publication**: Like properly announcing news to everyone at the same time

Each pattern provides a different level of protection and is suitable for different scenarios, just like different security systems protect different types of valuables.