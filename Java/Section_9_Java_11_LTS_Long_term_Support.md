# Section 9 - Java 11 - LTS & Long-term Support

## 9.1 HTTP Client (Standard)

Java 11 introduced the HTTP Client as a standard feature, replacing the legacy HttpURLConnection with a modern, fluent API that supports HTTP/2 and WebSocket.

### مفاهیم کلیدی:

**1. Modern HTTP API:**
- Fluent API design
- Built-in support for HTTP/2
- Asynchronous and synchronous operations
- WebSocket support

**2. Key Components:**
- `HttpClient` - Main client interface
- `HttpRequest` - Request builder
- `HttpResponse` - Response handler
- `BodyHandlers` - Response body processors

### مثال عملی:

```java
import java.net.http.*;
import java.net.URI;
import java.time.Duration;
import java.util.concurrent.CompletableFuture;

public class HttpClientExample {
    public static void main(String[] args) throws Exception {
        // 1. Basic HTTP GET request
        System.out.println("=== Basic HTTP GET ===");
        demonstrateBasicGet();
        
        // 2. HTTP POST with JSON
        System.out.println("\n=== HTTP POST with JSON ===");
        demonstratePostWithJson();
        
        // 3. Asynchronous requests
        System.out.println("\n=== Asynchronous Requests ===");
        demonstrateAsyncRequests();
        
        // 4. HTTP/2 support
        System.out.println("\n=== HTTP/2 Support ===");
        demonstrateHttp2();
    }
    
    public static void demonstrateBasicGet() throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://httpbin.org/get"))
            .timeout(Duration.ofSeconds(10))
            .header("User-Agent", "Java 11 HTTP Client")
            .GET()
            .build();
        
        HttpResponse<String> response = client.send(request, 
            HttpResponse.BodyHandlers.ofString());
        
        System.out.println("Status Code: " + response.statusCode());
        System.out.println("Headers: " + response.headers().map());
        System.out.println("Body: " + response.body());
    }
    
    public static void demonstratePostWithJson() throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        
        String jsonData = """
            {
                "name": "احمد محمدی",
                "age": 30,
                "city": "تهران"
            }
            """;
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://httpbin.org/post"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(jsonData))
            .build();
        
        HttpResponse<String> response = client.send(request, 
            HttpResponse.BodyHandlers.ofString());
        
        System.out.println("Status Code: " + response.statusCode());
        System.out.println("Response: " + response.body());
    }
    
    public static void demonstrateAsyncRequests() throws Exception {
        HttpClient client = HttpClient.newHttpClient();
        
        // Create multiple async requests
        CompletableFuture<HttpResponse<String>> future1 = client.sendAsync(
            HttpRequest.newBuilder()
                .uri(URI.create("https://httpbin.org/delay/1"))
                .GET()
                .build(),
            HttpResponse.BodyHandlers.ofString()
        );
        
        CompletableFuture<HttpResponse<String>> future2 = client.sendAsync(
            HttpRequest.newBuilder()
                .uri(URI.create("https://httpbin.org/delay/2"))
                .GET()
                .build(),
            HttpResponse.BodyHandlers.ofString()
        );
        
        // Wait for all requests to complete
        CompletableFuture<Void> allFutures = CompletableFuture.allOf(future1, future2);
        allFutures.get(); // Wait for completion
        
        System.out.println("Request 1 completed: " + future1.get().statusCode());
        System.out.println("Request 2 completed: " + future2.get().statusCode());
    }
    
    public static void demonstrateHttp2() throws Exception {
        HttpClient client = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_2)
            .build();
        
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://httpbin.org/get"))
            .GET()
            .build();
        
        HttpResponse<String> response = client.send(request, 
            HttpResponse.BodyHandlers.ofString());
        
        System.out.println("HTTP Version: " + response.version());
        System.out.println("Status Code: " + response.statusCode());
    }
}
```

### آنالوژی دنیای واقعی:
HTTP Client مانند داشتن یک پستچی حرفه‌ای است که می‌تواند نامه‌ها را به صورت همزمان و با سرعت بالا ارسال کند، از پروتکل‌های جدید پشتیبانی می‌کند و می‌تواند پاسخ‌ها را به صورت خودکار پردازش کند.

## 9.2 Local Variable Syntax for Lambda Parameters

Java 11 introduced the ability to use `var` keyword in lambda parameters, making lambda expressions more concise and consistent with local variable declarations.

### مفاهیم کلیدی:

**1. var in Lambda Parameters:**
- Type inference for lambda parameters
- Consistent with local variable syntax
- Reduces verbosity in complex generic types

**2. Benefits:**
- Cleaner code
- Better readability
- Consistent syntax

### مثال عملی:

```java
import java.util.*;
import java.util.function.*;
import java.util.stream.Collectors;

public class LocalVariableLambdaExample {
    public static void main(String[] args) {
        // 1. Basic var in lambda parameters
        System.out.println("=== Basic var in Lambda ===");
        demonstrateBasicVarLambda();
        
        // 2. Complex generic types
        System.out.println("\n=== Complex Generic Types ===");
        demonstrateComplexGenerics();
        
        // 3. Method references with var
        System.out.println("\n=== Method References ===");
        demonstrateMethodReferences();
        
        // 4. Stream operations
        System.out.println("\n=== Stream Operations ===");
        demonstrateStreamOperations();
    }
    
    public static void demonstrateBasicVarLambda() {
        List<String> names = Arrays.asList("احمد", "فاطمه", "علی", "زهرا");
        
        // Traditional lambda
        names.forEach(name -> System.out.println("Hello " + name));
        
        // With var keyword
        names.forEach(var name -> System.out.println("سلام " + name));
        
        // Multiple parameters
        Map<String, Integer> ages = Map.of("احمد", 25, "فاطمه", 30, "علی", 28);
        ages.forEach((var name, var age) -> 
            System.out.println(name + " is " + age + " years old"));
    }
    
    public static void demonstrateComplexGenerics() {
        List<Map<String, List<Integer>>> complexData = Arrays.asList(
            Map.of("scores", Arrays.asList(85, 90, 78)),
            Map.of("grades", Arrays.asList(92, 88, 95))
        );
        
        // Without var - very verbose
        complexData.forEach(map -> 
            map.forEach((key, value) -> 
                value.forEach(score -> 
                    System.out.println(key + ": " + score))));
        
        // With var - much cleaner
        complexData.forEach(var map -> 
            map.forEach((var key, var value) -> 
                value.forEach(var score -> 
                    System.out.println(key + ": " + score))));
    }
    
    public static void demonstrateMethodReferences() {
        List<String> words = Arrays.asList("Java", "Programming", "Language");
        
        // Traditional method reference
        words.stream()
            .map(String::toUpperCase)
            .forEach(System.out::println);
        
        // With var in lambda
        words.stream()
            .map(var word -> word.toUpperCase())
            .forEach(var result -> System.out.println(result));
    }
    
    public static void demonstrateStreamOperations() {
        List<Person> people = Arrays.asList(
            new Person("احمد", 25, "تهران"),
            new Person("فاطمه", 30, "اصفهان"),
            new Person("علی", 28, "شیراز")
        );
        
        // Complex stream operation with var
        Map<String, List<Person>> groupedByCity = people.stream()
            .filter(var person -> person.getAge() > 25)
            .collect(Collectors.groupingBy(var person -> person.getCity()));
        
        groupedByCity.forEach((var city, var peopleInCity) -> {
            System.out.println("شهر: " + city);
            peopleInCity.forEach(var person -> 
                System.out.println("  " + person.getName() + " - " + person.getAge()));
        });
    }
}

class Person {
    private String name;
    private int age;
    private String city;
    
    public Person(String name, int age, String city) {
        this.name = name;
        this.age = age;
        this.city = city;
    }
    
    public String getName() { return name; }
    public int getAge() { return age; }
    public String getCity() { return city; }
}
```

### آنالوژی دنیای واقعی:
استفاده از `var` در lambda parameters مانند استفاده از ضمیر "آن" در زبان فارسی است. به جای گفتن "کتابی که روی میز است"، می‌گوییم "آن کتاب". این کار کد را کوتاه‌تر و خوانا‌تر می‌کند.

## 9.3 Epsilon Garbage Collector

Epsilon GC is a no-op garbage collector that only handles memory allocation but never reclaims memory. It's designed for testing and performance analysis.

### مفاهیم کلیدی:

**1. No-Op Garbage Collector:**
- Allocates memory but never frees it
- Predictable performance
- No GC pauses
- Useful for testing and benchmarking

**2. Use Cases:**
- Performance testing
- Memory allocation testing
- Short-lived applications
- Testing memory leaks

### مثال عملی:

```java
public class EpsilonGCExample {
    private static final int MEGABYTE = 1024 * 1024;
    
    public static void main(String[] args) {
        System.out.println("=== Epsilon GC Example ===");
        System.out.println("Run with: -XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC");
        
        // 1. Memory allocation test
        demonstrateMemoryAllocation();
        
        // 2. Performance comparison
        demonstratePerformanceComparison();
        
        // 3. OutOfMemoryError demonstration
        demonstrateOutOfMemory();
    }
    
    public static void demonstrateMemoryAllocation() {
        System.out.println("\n=== Memory Allocation Test ===");
        
        Runtime runtime = Runtime.getRuntime();
        long maxMemory = runtime.maxMemory() / MEGABYTE;
        System.out.println("Max Memory: " + maxMemory + " MB");
        
        // Allocate memory in chunks
        List<byte[]> memoryChunks = new ArrayList<>();
        int chunkSize = 10 * MEGABYTE; // 10 MB chunks
        
        try {
            for (int i = 0; i < 50; i++) {
                byte[] chunk = new byte[chunkSize];
                memoryChunks.add(chunk);
                
                long usedMemory = (runtime.totalMemory() - runtime.freeMemory()) / MEGABYTE;
                System.out.println("Allocated chunk " + (i + 1) + ", Used memory: " + usedMemory + " MB");
                
                // Small delay to observe memory usage
                Thread.sleep(100);
            }
        } catch (OutOfMemoryError e) {
            System.out.println("OutOfMemoryError occurred: " + e.getMessage());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public static void demonstratePerformanceComparison() {
        System.out.println("\n=== Performance Comparison ===");
        
        int iterations = 1000000;
        
        // Test with Epsilon GC (no GC pauses)
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < iterations; i++) {
            String temp = "Test string " + i;
            // String will be allocated but never collected
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Epsilon GC time: " + (endTime - startTime) + " ms");
        
        // Note: This is just for demonstration
        // Real performance comparison would require running with different GC settings
    }
    
    public static void demonstrateOutOfMemory() {
        System.out.println("\n=== OutOfMemoryError Demonstration ===");
        
        List<byte[]> memoryChunks = new ArrayList<>();
        int chunkSize = 100 * MEGABYTE; // 100 MB chunks
        
        try {
            while (true) {
                byte[] chunk = new byte[chunkSize];
                memoryChunks.add(chunk);
                System.out.println("Allocated chunk " + memoryChunks.size() + 
                    " (" + (memoryChunks.size() * chunkSize / MEGABYTE) + " MB)");
            }
        } catch (OutOfMemoryError e) {
            System.out.println("OutOfMemoryError: " + e.getMessage());
            System.out.println("Total chunks allocated: " + memoryChunks.size());
        }
    }
}
```

### آنالوژی دنیای واقعی:
Epsilon GC مانند یک انبار است که فقط کالاها را می‌پذیرد اما هیچ‌وقت آن‌ها را تحویل نمی‌دهد. این برای تست کردن ظرفیت انبار مفید است، اما برای استفاده عملی مناسب نیست.

## 9.4 ZGC (Z Garbage Collector)

ZGC is a low-latency garbage collector designed for applications that require very short pause times, even with large heaps.

### مفاهیم کلیدی:

**1. Ultra-Low Latency:**
- Pause times under 10ms
- Scalable to multi-terabyte heaps
- Concurrent collection
- No stop-the-world phases

**2. Key Features:**
- Colored pointers
- Load barriers
- Concurrent marking and relocation
- Generational collection

### مثال عملی:

```java
public class ZGCExample {
    private static final int MEGABYTE = 1024 * 1024;
    
    public static void main(String[] args) {
        System.out.println("=== ZGC Example ===");
        System.out.println("Run with: -XX:+UnlockExperimentalVMOptions -XX:+UseZGC");
        
        // 1. Large heap allocation
        demonstrateLargeHeapAllocation();
        
        // 2. Concurrent operations
        demonstrateConcurrentOperations();
        
        // 3. Memory pressure test
        demonstrateMemoryPressure();
    }
    
    public static void demonstrateLargeHeapAllocation() {
        System.out.println("\n=== Large Heap Allocation ===");
        
        Runtime runtime = Runtime.getRuntime();
        long maxMemory = runtime.maxMemory() / MEGABYTE;
        System.out.println("Max Memory: " + maxMemory + " MB");
        
        // Allocate large objects
        List<byte[]> largeObjects = new ArrayList<>();
        int objectSize = 50 * MEGABYTE; // 50 MB per object
        
        for (int i = 0; i < 10; i++) {
            byte[] largeObject = new byte[objectSize];
            largeObjects.add(largeObject);
            
            long usedMemory = (runtime.totalMemory() - runtime.freeMemory()) / MEGABYTE;
            System.out.println("Allocated object " + (i + 1) + ", Used memory: " + usedMemory + " MB");
        }
    }
    
    public static void demonstrateConcurrentOperations() {
        System.out.println("\n=== Concurrent Operations ===");
        
        // Create multiple threads that allocate and deallocate memory
        List<Thread> threads = new ArrayList<>();
        
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            Thread thread = new Thread(() -> {
                List<byte[]> threadObjects = new ArrayList<>();
                
                for (int j = 0; j < 100; j++) {
                    // Allocate memory
                    byte[] object = new byte[1024 * 1024]; // 1 MB
                    threadObjects.add(object);
                    
                    // Simulate work
                    try {
                        Thread.sleep(10);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }
                    
                    // Periodically clear some objects
                    if (j % 20 == 0) {
                        threadObjects.clear();
                    }
                }
                
                System.out.println("Thread " + threadId + " completed");
            });
            
            threads.add(thread);
            thread.start();
        }
        
        // Wait for all threads to complete
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("All threads completed");
    }
    
    public static void demonstrateMemoryPressure() {
        System.out.println("\n=== Memory Pressure Test ===");
        
        List<byte[]> pressureObjects = new ArrayList<>();
        int objectSize = 10 * MEGABYTE; // 10 MB per object
        
        try {
            for (int i = 0; i < 100; i++) {
                byte[] object = new byte[objectSize];
                pressureObjects.add(object);
                
                if (i % 10 == 0) {
                    long usedMemory = (Runtime.getRuntime().totalMemory() - 
                        Runtime.getRuntime().freeMemory()) / MEGABYTE;
                    System.out.println("Pressure test - Object " + i + 
                        ", Used memory: " + usedMemory + " MB");
                }
                
                // Simulate some work
                Thread.sleep(50);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } catch (OutOfMemoryError e) {
            System.out.println("OutOfMemoryError during pressure test: " + e.getMessage());
        }
    }
}
```

### آنالوژی دنیای واقعی:
ZGC مانند یک سیستم تحویل کالا است که در حین کار کردن، کالاهای قدیمی را به صورت خودکار و بدون توقف کار، از انبار خارج می‌کند. این کار باعث می‌شود که کارخانه همیشه در حال کار باشد و هیچ‌وقت متوقف نشود.

## 9.5 Flight Recorder

Java Flight Recorder (JFR) is a profiling and event collection framework built into the JDK that provides low-overhead data collection about the JVM and application.

### مفاهیم کلیدی:

**1. Low-Overhead Profiling:**
- Minimal performance impact
- Continuous monitoring
- Rich event data
- Built into JVM

**2. Event Types:**
- JVM events (GC, compilation, class loading)
- Application events (custom events)
- System events (CPU, memory, I/O)
- Security events

### مثال عملی:

```java
import jdk.jfr.*;
import java.time.Duration;
import java.util.concurrent.TimeUnit;

@Name("com.example.BusinessEvent")
@Label("Business Event")
@Description("Custom business event for monitoring")
public class FlightRecorderExample {
    
    public static void main(String[] args) throws Exception {
        System.out.println("=== Flight Recorder Example ===");
        
        // 1. Enable JFR programmatically
        enableJFR();
        
        // 2. Record custom events
        demonstrateCustomEvents();
        
        // 3. Record method execution
        demonstrateMethodRecording();
        
        // 4. Record business operations
        demonstrateBusinessRecording();
    }
    
    public static void enableJFR() throws Exception {
        System.out.println("\n=== Enabling JFR ===");
        
        // Start JFR recording
        Recording recording = new Recording();
        recording.setName("MyApplication");
        recording.setDuration(Duration.ofMinutes(1));
        
        // Configure recording settings
        recording.setSettings(Map.of(
            "jdk.GCHeapSummary#enabled", "true",
            "jdk.CPULoad#enabled", "true",
            "jdk.MemoryUsage#enabled", "true"
        ));
        
        recording.start();
        System.out.println("JFR recording started");
        
        // Stop recording after some time
        Thread.sleep(5000);
        recording.stop();
        
        // Save recording to file
        recording.dump(Path.of("my-recording.jfr"));
        System.out.println("Recording saved to my-recording.jfr");
        
        recording.close();
    }
    
    public static void demonstrateCustomEvents() {
        System.out.println("\n=== Custom Events ===");
        
        // Record custom business events
        for (int i = 0; i < 10; i++) {
            BusinessEvent event = new BusinessEvent();
            event.userId = "user" + i;
            event.operation = "login";
            event.duration = Duration.ofMillis(100 + i * 10);
            event.commit();
            
            System.out.println("Recorded event for user" + i);
        }
    }
    
    public static void demonstrateMethodRecording() {
        System.out.println("\n=== Method Recording ===");
        
        // Record method execution times
        for (int i = 0; i < 5; i++) {
            long startTime = System.currentTimeMillis();
            
            // Simulate some work
            performWork();
            
            long endTime = System.currentTimeMillis();
            long duration = endTime - startTime;
            
            System.out.println("Method execution took: " + duration + " ms");
        }
    }
    
    public static void demonstrateBusinessRecording() {
        System.out.println("\n=== Business Recording ===");
        
        // Simulate business operations
        processOrder("order-001", 150.0);
        processOrder("order-002", 75.5);
        processOrder("order-003", 200.0);
    }
    
    @Name("com.example.WorkEvent")
    @Label("Work Event")
    @Description("Event for work operations")
    static class WorkEvent extends Event {
        @Label("Work Type")
        String workType;
        
        @Label("Duration")
        Duration duration;
    }
    
    public static void performWork() {
        WorkEvent event = new WorkEvent();
        event.begin();
        
        try {
            // Simulate work
            Thread.sleep(100);
            event.workType = "data-processing";
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            event.duration = Duration.ofMillis(100);
            event.commit();
        }
    }
    
    @Name("com.example.OrderEvent")
    @Label("Order Processing Event")
    @Description("Event for order processing operations")
    static class OrderEvent extends Event {
        @Label("Order ID")
        String orderId;
        
        @Label("Order Amount")
        double amount;
        
        @Label("Processing Time")
        Duration processingTime;
    }
    
    public static void processOrder(String orderId, double amount) {
        OrderEvent event = new OrderEvent();
        event.begin();
        
        try {
            // Simulate order processing
            Thread.sleep(50);
            event.orderId = orderId;
            event.amount = amount;
            
            System.out.println("Processing order: " + orderId + " for $" + amount);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            event.processingTime = Duration.ofMillis(50);
            event.commit();
        }
    }
}

// Custom event class
@Name("com.example.BusinessEvent")
@Label("Business Event")
@Description("Custom business event for monitoring")
class BusinessEvent extends Event {
    @Label("User ID")
    String userId;
    
    @Label("Operation")
    String operation;
    
    @Label("Duration")
    Duration duration;
}
```

### آنالوژی دنیای واقعی:
Flight Recorder مانند داشتن یک دوربین امنیتی است که تمام فعالیت‌های مهم را ضبط می‌کند. این دوربین بدون اینکه کار را مختل کند، تمام جزئیات را ثبت می‌کند و بعداً می‌توانید آن‌ها را بررسی کنید.

## 9.6 Nest-based Access Control

Nest-based access control allows classes in the same nest to access each other's private members, improving encapsulation while maintaining security.

### مفاهیم کلیدی:

**1. Nest Concept:**
- Group of classes that share private access
- Nest host and nest members
- Compile-time and runtime access control
- Better encapsulation

**2. Benefits:**
- Cleaner code organization
- Better encapsulation
- Reduced boilerplate code
- Maintained security

### مثال عملی:

```java
public class NestBasedAccessExample {
    public static void main(String[] args) {
        System.out.println("=== Nest-based Access Control ===");
        
        // 1. Basic nest access
        demonstrateBasicNestAccess();
        
        // 2. Inner class access
        demonstrateInnerClassAccess();
        
        // 3. Static nested class access
        demonstrateStaticNestedAccess();
    }
    
    public static void demonstrateBasicNestAccess() {
        System.out.println("\n=== Basic Nest Access ===");
        
        OuterClass outer = new OuterClass();
        outer.demonstrateNestAccess();
    }
    
    public static void demonstrateInnerClassAccess() {
        System.out.println("\n=== Inner Class Access ===");
        
        OuterClass outer = new OuterClass();
        OuterClass.InnerClass inner = outer.new InnerClass();
        inner.accessOuterPrivate();
    }
    
    public static void demonstrateStaticNestedAccess() {
        System.out.println("\n=== Static Nested Access ===");
        
        OuterClass.StaticNestedClass staticNested = new OuterClass.StaticNestedClass();
        staticNested.accessOuterPrivate();
    }
}

class OuterClass {
    private String privateField = "Private field in outer class";
    private static String privateStaticField = "Private static field";
    
    public void demonstrateNestAccess() {
        System.out.println("Outer class accessing its own private field: " + privateField);
    }
    
    // Inner class - part of the same nest
    class InnerClass {
        private String innerPrivateField = "Private field in inner class";
        
        public void accessOuterPrivate() {
            // Can access outer class private members
            System.out.println("Inner class accessing outer private field: " + privateField);
            System.out.println("Inner class accessing outer private static field: " + privateStaticField);
        }
        
        public void demonstrateInnerPrivate() {
            System.out.println("Inner class accessing its own private field: " + innerPrivateField);
        }
    }
    
    // Static nested class - part of the same nest
    static class StaticNestedClass {
        private String staticNestedPrivateField = "Private field in static nested class";
        
        public void accessOuterPrivate() {
            // Can access outer class private static members
            System.out.println("Static nested class accessing outer private static field: " + privateStaticField);
        }
        
        public void demonstrateStaticNestedPrivate() {
            System.out.println("Static nested class accessing its own private field: " + staticNestedPrivateField);
        }
    }
    
    // Method to demonstrate access from outer to inner
    public void accessInnerPrivate() {
        InnerClass inner = new InnerClass();
        // This would not work - cannot access inner class private members
        // System.out.println(inner.innerPrivateField); // Compilation error
    }
}

// Example of different nest
class DifferentNest {
    private String differentNestField = "Field in different nest";
    
    public void demonstrateDifferentNest() {
        System.out.println("Different nest field: " + differentNestField);
    }
}

// This class cannot access OuterClass private members
class UnrelatedClass {
    public void demonstrateNoAccess() {
        OuterClass outer = new OuterClass();
        // This would not work - not in the same nest
        // System.out.println(outer.privateField); // Compilation error
    }
}
```

### آنالوژی دنیای واقعی:
Nest-based access control مانند داشتن کلیدهای مختلف برای اتاق‌های مختلف در یک خانه است. اعضای خانواده (کلاس‌های درون nest) می‌توانند به اتاق‌های خصوصی یکدیگر دسترسی داشته باشند، اما مهمانان (کلاس‌های خارج از nest) نمی‌توانند.

## 9.7 Dynamic Class-File Constants

Dynamic class-file constants (CONSTANT_Dynamic) allow for more flexible constant creation at runtime, enabling better performance and more dynamic behavior.

### مفاهیم کلیدی:

**1. Dynamic Constants:**
- Runtime constant creation
- Better performance than reflection
- More flexible than static constants
- JVM optimization

**2. Use Cases:**
- Dynamic method handles
- Runtime constant creation
- Performance optimization
- Flexible constant management

### مثال عملی:

```java
import java.lang.invoke.*;
import java.lang.reflect.Method;
import java.util.function.Function;

public class DynamicClassFileConstantsExample {
    public static void main(String[] args) throws Throwable {
        System.out.println("=== Dynamic Class-File Constants ===");
        
        // 1. Basic dynamic constant
        demonstrateBasicDynamicConstant();
        
        // 2. Dynamic method handles
        demonstrateDynamicMethodHandles();
        
        // 3. Performance comparison
        demonstratePerformanceComparison();
    }
    
    public static void demonstrateBasicDynamicConstant() throws Throwable {
        System.out.println("\n=== Basic Dynamic Constant ===");
        
        // Create a dynamic constant
        CallSite callSite = MethodHandles.constant(String.class, "Hello Dynamic World!");
        String result = (String) callSite.getTarget().invoke();
        
        System.out.println("Dynamic constant result: " + result);
    }
    
    public static void demonstrateDynamicMethodHandles() throws Throwable {
        System.out.println("\n=== Dynamic Method Handles ===");
        
        // Create dynamic method handle for String.length()
        MethodHandles.Lookup lookup = MethodHandles.lookup();
        MethodHandle lengthMethod = lookup.findVirtual(String.class, "length", 
            MethodType.methodType(int.class));
        
        // Create dynamic constant
        String testString = "Dynamic Method Handle";
        CallSite callSite = MethodHandles.constant(String.class, testString);
        
        // Invoke method on dynamic constant
        String dynamicString = (String) callSite.getTarget().invoke();
        int length = (int) lengthMethod.invoke(dynamicString);
        
        System.out.println("Dynamic string: " + dynamicString);
        System.out.println("Length: " + length);
    }
    
    public static void demonstratePerformanceComparison() throws Throwable {
        System.out.println("\n=== Performance Comparison ===");
        
        int iterations = 1000000;
        
        // Test with dynamic constants
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < iterations; i++) {
            CallSite callSite = MethodHandles.constant(String.class, "Test " + i);
            String result = (String) callSite.getTarget().invoke();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Dynamic constants time: " + (endTime - startTime) + " ms");
        
        // Test with regular string creation
        startTime = System.currentTimeMillis();
        
        for (int i = 0; i < iterations; i++) {
            String result = "Test " + i;
        }
        
        endTime = System.currentTimeMillis();
        System.out.println("Regular string creation time: " + (endTime - startTime) + " ms");
    }
}

// Example class for dynamic constant creation
class DynamicConstantFactory {
    private static final MethodHandles.Lookup LOOKUP = MethodHandles.lookup();
    
    public static CallSite createDynamicConstant(String value) throws Throwable {
        return MethodHandles.constant(String.class, value);
    }
    
    public static CallSite createDynamicNumber(int value) throws Throwable {
        return MethodHandles.constant(Integer.class, value);
    }
    
    public static CallSite createDynamicBoolean(boolean value) throws Throwable {
        return MethodHandles.constant(Boolean.class, value);
    }
    
    // Example of dynamic constant with method
    public static CallSite createDynamicMethod(String methodName) throws Throwable {
        MethodHandle method = LOOKUP.findStatic(DynamicConstantFactory.class, 
            methodName, MethodType.methodType(String.class));
        return MethodHandles.constant(MethodHandle.class, method);
    }
    
    public static String getCurrentTime() {
        return "Current time: " + System.currentTimeMillis();
    }
    
    public static String getSystemInfo() {
        return "Java version: " + System.getProperty("java.version");
    }
}
```

### آنالوژی دنیای واقعی:
Dynamic class-file constants مانند داشتن یک کارخانه هوشمند است که می‌تواند در زمان اجرا، محصولات مختلف را بر اساس نیاز تولید کند. این کارخانه می‌تواند سریع‌تر و کارآمدتر از روش‌های سنتی عمل کند.

### خلاصه Java 11:

Java 11 به عنوان یک نسخه LTS، ویژگی‌های مهمی را معرفی کرد که شامل HTTP Client مدرن، بهبودهای GC، Flight Recorder، و بهبودهای امنیتی می‌شود. این نسخه پایه‌ای محکم برای توسعه‌های آینده جاوا فراهم کرد.