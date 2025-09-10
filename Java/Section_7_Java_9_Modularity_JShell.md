# Section 7 - Java 9 - Modularity & JShell

## 7.1 Java Platform Module System (JPMS)

Java Platform Module System (JPMS) یکی از مهم‌ترین ویژگی‌های Java 9 است که modularity را به Java platform آورد.

### مفاهیم کلیدی:

**1. Module System:**
- Encapsulation at module level
- Explicit dependencies
- Better security and performance

**2. Module Descriptor:**
- `module-info.java` file
- Exports and requires clauses
- Service provider mechanism

### مثال عملی:

```java
// module-info.java
module com.example.calculator {
    requires java.base;
    exports com.example.calculator;
    provides com.example.calculator.CalculatorService 
        with com.example.calculator.BasicCalculatorService;
}

// CalculatorService.java
package com.example.calculator;

public interface CalculatorService {
    double add(double a, double b);
    double subtract(double a, double b);
    double multiply(double a, double b);
    double divide(double a, double b);
}

// BasicCalculatorService.java
package com.example.calculator;

public class BasicCalculatorService implements CalculatorService {
    @Override
    public double add(double a, double b) {
        return a + b;
    }
    
    @Override
    public double subtract(double a, double b) {
        return a - b;
    }
    
    @Override
    public double multiply(double a, double b) {
        return a * b;
    }
    
    @Override
    public double divide(double a, double b) {
        if (b == 0) {
            throw new IllegalArgumentException("Division by zero");
        }
        return a / b;
    }
}

// CalculatorApp.java
package com.example.calculator;

import java.util.ServiceLoader;

public class CalculatorApp {
    public static void main(String[] args) {
        // Use service loader to find implementations
        ServiceLoader<CalculatorService> services = 
            ServiceLoader.load(CalculatorService.class);
        
        CalculatorService calculator = services.findFirst()
            .orElseThrow(() -> new RuntimeException("No calculator service found"));
        
        System.out.println("Addition: " + calculator.add(5, 3));
        System.out.println("Subtraction: " + calculator.subtract(5, 3));
        System.out.println("Multiplication: " + calculator.multiply(5, 3));
        System.out.println("Division: " + calculator.divide(5, 3));
    }
}
```

### آنالوژی دنیای واقعی:
JPMS مانند داشتن یک ساختمان با آپارتمان‌های جداگانه است. هر آپارتمان (module) دارای درها و پنجره‌های خاص خود است که می‌تواند به آپارتمان‌های دیگر دسترسی داشته باشد یا نداشته باشد. این کار امنیت و سازماندهی را بهبود می‌بخشد.

## 7.2 JShell - Interactive Java REPL

JShell یک interactive Java REPL (Read-Eval-Print Loop) است که امکان تست سریع کد Java را فراهم می‌کند.

### مفاهیم کلیدی:

**1. Interactive Development:**
- Execute Java code immediately
- No need for compilation
- Quick prototyping

**2. JShell Commands:**
- `/help` - Show help
- `/list` - List all snippets
- `/vars` - Show variables
- `/methods` - Show methods

### مثال عملی:

```java
// JShell examples
// Start JShell: jshell

// 1. Basic expressions
jshell> 2 + 3
$1 ==> 5

jshell> "Hello" + " World"
$2 ==> "Hello World"

// 2. Variables
jshell> int x = 10
x ==> 10

jshell> String name = "احمد"
name ==> "احمد"

// 3. Methods
jshell> int add(int a, int b) { return a + b; }
|  created method add(int,int)

jshell> add(5, 3)
$3 ==> 8

// 4. Classes
jshell> class Person {
...>     private String name;
...>     private int age;
...>     
...>     public Person(String name, int age) {
...>         this.name = name;
...>         this.age = age;
...>     }
...>     
...>     public String getName() { return name; }
...>     public int getAge() { return age; }
...> }
|  created class Person

jshell> Person person = new Person("فاطمه", 25)
person ==> Person@2f92e0f4

jshell> person.getName()
$4 ==> "فاطمه"

// 5. Imports
jshell> import java.util.*
jshell> List<String> list = new ArrayList<>()
list ==> []

jshell> list.add("Java")
$5 ==> true

jshell> list
$5 ==> [Java]

// 6. JShell commands
jshell> /list
   1 : 2 + 3
   2 : "Hello" + " World"
   3 : int x = 10
   4 : String name = "احمد"
   5 : int add(int a, int b) { return a + b; }
   6 : class Person {
       private String name;
       private int age;
       
       public Person(String name, int age) {
           this.name = name;
           this.age = age;
       }
       
       public String getName() { return name; }
       public int getAge() { return age; }
   }
   7 : Person person = new Person("فاطمه", 25)
   8 : person.getName()
   9 : import java.util.*
  10 : List<String> list = new ArrayList<>()
  11 : list.add("Java")

jshell> /vars
|    int x = 10
|    String name = "احمد"
|    Person person = Person@2f92e0f4
|    List<String> list = [Java]

jshell> /methods
|    int add(int,int)

// 7. Error handling
jshell> int result = 10 / 0
|  Exception java.lang.ArithmeticException: / by zero
|        at (#12:1)

jshell> /edit add
// Edit the method in external editor

// 8. Save and load
jshell> /save mysession.jsh
jshell> /open mysession.jsh
```

### آنالوژی دنیای واقعی:
JShell مانند داشتن یک دفترچه یادداشت هوشمند است که می‌توانید ایده‌های خود را فوراً تست کنید. به جای نوشتن یک برنامه کامل، می‌توانید قطعات کوچک کد را بنویسید و نتیجه را فوراً ببینید.

## 7.3 Collection Factory Methods

Java 9 متدهای factory جدیدی برای ایجاد collections معرفی کرد.

### مفاهیم کلیدی:

**1. Immutable Collections:**
- Cannot be modified after creation
- Thread-safe
- Better performance

**2. Factory Methods:**
- `List.of()`, `Set.of()`, `Map.of()`
- Varargs support
- Null safety

### مثال عملی:

```java
import java.util.*;

public class CollectionFactoryMethodsExample {
    
    public static void main(String[] args) {
        // 1. List factory methods
        System.out.println("=== List Factory Methods ===");
        
        // Empty list
        List<String> emptyList = List.of();
        System.out.println("Empty list: " + emptyList);
        
        // List with elements
        List<String> names = List.of("احمد", "فاطمه", "علی", "زهرا");
        System.out.println("Names: " + names);
        
        // 2. Set factory methods
        System.out.println("\n=== Set Factory Methods ===");
        
        // Empty set
        Set<String> emptySet = Set.of();
        System.out.println("Empty set: " + emptySet);
        
        // Set with elements
        Set<String> colors = Set.of("قرمز", "سبز", "آبی");
        System.out.println("Colors: " + colors);
        
        // 3. Map factory methods
        System.out.println("\n=== Map Factory Methods ===");
        
        // Empty map
        Map<String, Integer> emptyMap = Map.of();
        System.out.println("Empty map: " + emptyMap);
        
        // Map with key-value pairs
        Map<String, Integer> ages = Map.of(
            "احمد", 25,
            "فاطمه", 30,
            "علی", 22
        );
        System.out.println("Ages: " + ages);
        
        // 4. Map with more than 10 entries
        System.out.println("\n=== Map with Many Entries ===");
        
        Map<String, String> countries = Map.ofEntries(
            Map.entry("IR", "Iran"),
            Map.entry("US", "United States"),
            Map.entry("UK", "United Kingdom"),
            Map.entry("DE", "Germany"),
            Map.entry("FR", "France")
        );
        System.out.println("Countries: " + countries);
        
        // 5. Immutability demonstration
        System.out.println("\n=== Immutability ===");
        
        try {
            names.add("محمد"); // This will throw UnsupportedOperationException
        } catch (UnsupportedOperationException e) {
            System.out.println("Cannot modify immutable list: " + e.getMessage());
        }
        
        try {
            colors.remove("قرمز"); // This will throw UnsupportedOperationException
        } catch (UnsupportedOperationException e) {
            System.out.println("Cannot modify immutable set: " + e.getMessage());
        }
        
        // 6. Performance comparison
        System.out.println("\n=== Performance Comparison ===");
        
        // Traditional way
        long startTime = System.currentTimeMillis();
        List<String> traditionalList = new ArrayList<>();
        traditionalList.add("Item 1");
        traditionalList.add("Item 2");
        traditionalList.add("Item 3");
        List<String> unmodifiableList = Collections.unmodifiableList(traditionalList);
        long endTime = System.currentTimeMillis();
        System.out.println("Traditional way time: " + (endTime - startTime) + " ms");
        
        // Factory method way
        startTime = System.currentTimeMillis();
        List<String> factoryList = List.of("Item 1", "Item 2", "Item 3");
        endTime = System.currentTimeMillis();
        System.out.println("Factory method time: " + (endTime - startTime) + " ms");
        
        // 7. Null safety
        System.out.println("\n=== Null Safety ===");
        
        try {
            List<String> listWithNull = List.of("Item 1", null, "Item 3");
        } catch (NullPointerException e) {
            System.out.println("Null not allowed: " + e.getMessage());
        }
        
        // 8. Duplicate handling
        System.out.println("\n=== Duplicate Handling ===");
        
        try {
            Set<String> setWithDuplicates = Set.of("Item 1", "Item 2", "Item 1");
        } catch (IllegalArgumentException e) {
            System.out.println("Duplicates not allowed in Set: " + e.getMessage());
        }
    }
}
```

### آنالوژی دنیای واقعی:
Collection factory methods مانند داشتن یک کارخانه هوشمند است که می‌تواند محصولات مختلف را به سرعت و با کیفیت بالا تولید کند. به جای ساختن دستی هر محصول، فقط مواد اولیه را می‌دهید و محصول نهایی را دریافت می‌کنید.

## 7.4 Process API Improvements

Java 9 API جدیدی برای مدیریت processes معرفی کرد.

### مفاهیم کلیدی:

**1. Process Information:**
- Process ID, command, arguments
- Start time, CPU time
- User and group information

**2. Process Control:**
- Start processes
- Wait for completion
- Handle input/output

### مثال عملی:

```java
import java.io.*;
import java.time.*;
import java.util.*;

public class ProcessAPIExample {
    
    public static void main(String[] args) throws Exception {
        // 1. Current process information
        System.out.println("=== Current Process Information ===");
        
        ProcessHandle currentProcess = ProcessHandle.current();
        System.out.println("PID: " + currentProcess.pid());
        System.out.println("Is alive: " + currentProcess.isAlive());
        System.out.println("Parent: " + currentProcess.parent().orElse(null));
        
        // 2. Process info
        System.out.println("\n=== Process Info ===");
        
        ProcessHandle.Info info = currentProcess.info();
        System.out.println("Command: " + info.command().orElse("Unknown"));
        System.out.println("Arguments: " + Arrays.toString(info.arguments().orElse(new String[0])));
        System.out.println("Start time: " + info.startInstant().orElse(null));
        System.out.println("Total CPU time: " + info.totalCpuDuration().orElse(null));
        System.out.println("User: " + info.user().orElse("Unknown"));
        
        // 3. All processes
        System.out.println("\n=== All Processes ===");
        
        ProcessHandle.allProcesses()
            .limit(10)
            .forEach(process -> {
                System.out.println("PID: " + process.pid() + 
                    ", Command: " + process.info().command().orElse("Unknown"));
            });
        
        // 4. Start a new process
        System.out.println("\n=== Starting New Process ===");
        
        ProcessBuilder pb = new ProcessBuilder("java", "-version");
        Process process = pb.start();
        
        // Read output
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println("Output: " + line);
            }
        }
        
        // Wait for process to complete
        int exitCode = process.waitFor();
        System.out.println("Exit code: " + exitCode);
        
        // 5. Process monitoring
        System.out.println("\n=== Process Monitoring ===");
        
        ProcessHandle processHandle = process.toHandle();
        System.out.println("Process PID: " + processHandle.pid());
        System.out.println("Is alive: " + processHandle.isAlive());
        
        // 6. Process tree
        System.out.println("\n=== Process Tree ===");
        
        ProcessHandle current = ProcessHandle.current();
        printProcessTree(current, 0);
        
        // 7. Process completion
        System.out.println("\n=== Process Completion ===");
        
        ProcessBuilder longRunning = new ProcessBuilder("ping", "google.com");
        Process longProcess = longRunning.start();
        
        // Add completion handler
        longProcess.toHandle().onExit().thenAccept(completedProcess -> {
            System.out.println("Process completed with exit code: " + 
                completedProcess.exitValue());
        });
        
        // Wait a bit then destroy
        Thread.sleep(2000);
        longProcess.destroy();
        System.out.println("Process destroyed");
    }
    
    private static void printProcessTree(ProcessHandle process, int depth) {
        String indent = "  ".repeat(depth);
        System.out.println(indent + "PID: " + process.pid() + 
            ", Command: " + process.info().command().orElse("Unknown"));
        
        process.children().forEach(child -> printProcessTree(child, depth + 1));
    }
}
```

### آنالوژی دنیای واقعی:
Process API مانند داشتن یک مدیر سیستم هوشمند است که می‌تواند تمام برنامه‌های در حال اجرا را ببیند، اطلاعات آن‌ها را بررسی کند، و در صورت نیاز آن‌ها را کنترل کند.

## 7.5 HTTP/2 Client

Java 9 یک HTTP/2 client جدید معرفی کرد.

### مفاهیم کلیدی:

**1. HTTP/2 Support:**
- Multiplexing
- Server push
- Header compression

**2. Asynchronous API:**
- Non-blocking operations
- CompletableFuture support
- Better performance

### مثال عملی:

```java
import java.net.http.*;
import java.net.URI;
import java.time.Duration;
import java.util.concurrent.CompletableFuture;

public class HTTP2ClientExample {
    
    public static void main(String[] args) throws Exception {
        // 1. Basic HTTP request
        System.out.println("=== Basic HTTP Request ===");
        
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://httpbin.org/get"))
            .timeout(Duration.ofSeconds(10))
            .build();
        
        HttpResponse<String> response = client.send(request, 
            HttpResponse.BodyHandlers.ofString());
        
        System.out.println("Status: " + response.statusCode());
        System.out.println("Headers: " + response.headers().map());
        System.out.println("Body: " + response.body());
        
        // 2. Asynchronous request
        System.out.println("\n=== Asynchronous Request ===");
        
        CompletableFuture<HttpResponse<String>> future = client.sendAsync(request,
            HttpResponse.BodyHandlers.ofString());
        
        future.thenAccept(response2 -> {
            System.out.println("Async Status: " + response2.statusCode());
            System.out.println("Async Body: " + response2.body());
        });
        
        // Wait for completion
        future.get();
        
        // 3. POST request
        System.out.println("\n=== POST Request ===");
        
        String jsonBody = "{\"name\":\"احمد\",\"age\":25}";
        HttpRequest postRequest = HttpRequest.newBuilder()
            .uri(URI.create("https://httpbin.org/post"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
            .build();
        
        HttpResponse<String> postResponse = client.send(postRequest,
            HttpResponse.BodyHandlers.ofString());
        
        System.out.println("POST Status: " + postResponse.statusCode());
        System.out.println("POST Body: " + postResponse.body());
        
        // 4. Custom headers
        System.out.println("\n=== Custom Headers ===");
        
        HttpRequest customRequest = HttpRequest.newBuilder()
            .uri(URI.create("https://httpbin.org/headers"))
            .header("User-Agent", "Java HTTP/2 Client")
            .header("Authorization", "Bearer token123")
            .header("Custom-Header", "Custom-Value")
            .build();
        
        HttpResponse<String> customResponse = client.send(customRequest,
            HttpResponse.BodyHandlers.ofString());
        
        System.out.println("Custom Headers Response: " + customResponse.body());
        
        // 5. Error handling
        System.out.println("\n=== Error Handling ===");
        
        try {
            HttpRequest errorRequest = HttpRequest.newBuilder()
                .uri(URI.create("https://httpbin.org/status/404"))
                .build();
            
            HttpResponse<String> errorResponse = client.send(errorRequest,
                HttpResponse.BodyHandlers.ofString());
            
            System.out.println("Error Status: " + errorResponse.statusCode());
            
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
        
        // 6. Multiple requests
        System.out.println("\n=== Multiple Requests ===");
        
        String[] urls = {
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/2",
            "https://httpbin.org/delay/3"
        };
        
        CompletableFuture<String>[] futures = new CompletableFuture[urls.length];
        
        for (int i = 0; i < urls.length; i++) {
            final int index = i;
            HttpRequest multiRequest = HttpRequest.newBuilder()
                .uri(URI.create(urls[index]))
                .build();
            
            futures[i] = client.sendAsync(multiRequest,
                HttpResponse.BodyHandlers.ofString())
                .thenApply(response3 -> "Request " + index + " completed");
        }
        
        CompletableFuture.allOf(futures).thenRun(() -> {
            for (CompletableFuture<String> future2 : futures) {
                System.out.println(future2.join());
            }
        }).get();
    }
}
```

### آنالوژی دنیای واقعی:
HTTP/2 Client مانند داشتن یک پستچی هوشمند است که می‌تواند چندین نامه را همزمان حمل کند، از مسیرهای مختلف استفاده کند، و نامه‌ها را به صورت موثرتر تحویل دهد.

## 7.6 Private Methods in Interfaces

Java 9 امکان تعریف private methods در interfaces را فراهم کرد.

### مفاهیم کلیدی:

**1. Code Reuse:**
- Avoid code duplication
- Better organization
- Cleaner interfaces

**2. Private Methods:**
- Cannot be called from outside
- Can be used by default methods
- Helper methods

### مثال عملی:

```java
public class PrivateMethodsInInterfacesExample {
    
    public static void main(String[] args) {
        // 1. Basic interface with private methods
        System.out.println("=== Basic Interface with Private Methods ===");
        
        Calculator calculator = new BasicCalculator();
        System.out.println("Add: " + calculator.add(5, 3));
        System.out.println("Subtract: " + calculator.subtract(5, 3));
        System.out.println("Multiply: " + calculator.multiply(5, 3));
        System.out.println("Divide: " + calculator.divide(5, 3));
        
        // 2. Advanced interface with private methods
        System.out.println("\n=== Advanced Interface with Private Methods ===");
        
        AdvancedCalculator advanced = new AdvancedCalculator();
        System.out.println("Power: " + advanced.power(2, 3));
        System.out.println("Square root: " + advanced.squareRoot(16));
        System.out.println("Logarithm: " + advanced.logarithm(10, 100));
        
        // 3. Interface with multiple private methods
        System.out.println("\n=== Interface with Multiple Private Methods ===");
        
        DataProcessor processor = new DataProcessor();
        System.out.println("Process: " + processor.process("Hello World"));
        System.out.println("Validate: " + processor.validate("test@example.com"));
    }
}

// Basic interface with private methods
interface Calculator {
    int add(int a, int b);
    int subtract(int a, int b);
    
    // Default methods using private methods
    default int multiply(int a, int b) {
        return performOperation(a, b, (x, y) -> x * y);
    }
    
    default int divide(int a, int b) {
        if (b == 0) {
            throw new IllegalArgumentException("Division by zero");
        }
        return performOperation(a, b, (x, y) -> x / y);
    }
    
    // Private method for common operation
    private int performOperation(int a, int b, Operation operation) {
        validateInputs(a, b);
        return operation.calculate(a, b);
    }
    
    // Private method for validation
    private void validateInputs(int a, int b) {
        if (a < 0 || b < 0) {
            throw new IllegalArgumentException("Negative numbers not allowed");
        }
    }
    
    // Functional interface for operations
    @FunctionalInterface
    interface Operation {
        int calculate(int a, int b);
    }
}

// Advanced interface with multiple private methods
interface AdvancedCalculator extends Calculator {
    double power(double base, double exponent);
    double squareRoot(double number);
    double logarithm(double base, double number);
    
    // Default method using private methods
    default double complexCalculation(double a, double b, double c) {
        double result1 = performPower(a, b);
        double result2 = performSquareRoot(c);
        return performLogarithm(result1, result2);
    }
    
    // Private methods for complex calculations
    private double performPower(double base, double exponent) {
        validateDoubleInputs(base, exponent);
        return Math.pow(base, exponent);
    }
    
    private double performSquareRoot(double number) {
        validateDoubleInputs(number, 0);
        return Math.sqrt(number);
    }
    
    private double performLogarithm(double base, double number) {
        validateDoubleInputs(base, number);
        return Math.log(number) / Math.log(base);
    }
    
    private void validateDoubleInputs(double a, double b) {
        if (a < 0 || b < 0) {
            throw new IllegalArgumentException("Negative numbers not allowed");
        }
    }
}

// Interface with multiple private methods
interface DataProcessor {
    String process(String data);
    boolean validate(String data);
    
    // Default method using multiple private methods
    default String processAndValidate(String data) {
        if (validate(data)) {
            return process(data);
        } else {
            throw new IllegalArgumentException("Invalid data");
        }
    }
    
    // Private methods for data processing
    private String cleanData(String data) {
        return data.trim().toLowerCase();
    }
    
    private String formatData(String data) {
        return data.substring(0, 1).toUpperCase() + data.substring(1);
    }
    
    private boolean isValidEmail(String email) {
        return email.contains("@") && email.contains(".");
    }
    
    private boolean isValidLength(String data) {
        return data.length() > 0 && data.length() < 100;
    }
}

// Implementations
class BasicCalculator implements Calculator {
    @Override
    public int add(int a, int b) {
        return a + b;
    }
    
    @Override
    public int subtract(int a, int b) {
        return a - b;
    }
}

class AdvancedCalculator implements AdvancedCalculator {
    @Override
    public int add(int a, int b) {
        return a + b;
    }
    
    @Override
    public int subtract(int a, int b) {
        return a - b;
    }
    
    @Override
    public double power(double base, double exponent) {
        return Math.pow(base, exponent);
    }
    
    @Override
    public double squareRoot(double number) {
        return Math.sqrt(number);
    }
    
    @Override
    public double logarithm(double base, double number) {
        return Math.log(number) / Math.log(base);
    }
}

class DataProcessor implements DataProcessor {
    @Override
    public String process(String data) {
        String cleaned = cleanData(data);
        return formatData(cleaned);
    }
    
    @Override
    public boolean validate(String data) {
        return isValidEmail(data) && isValidLength(data);
    }
}
```

### آنالوژی دنیای واقعی:
Private methods در interfaces مانند داشتن یک آشپزخانه خصوصی در یک رستوران است. مشتریان نمی‌توانند مستقیماً به آشپزخانه دسترسی داشته باشند، اما آشپزها می‌توانند از ابزارها و روش‌های خصوصی برای تهیه غذا استفاده کنند.

## 7.7 Reactive Streams

Java 9 Reactive Streams API را معرفی کرد که برای asynchronous stream processing طراحی شده است.

### مفاهیم کلیدی:

**1. Reactive Programming:**
- Asynchronous data processing
- Backpressure handling
- Non-blocking operations

**2. Main Interfaces:**
- `Publisher` - produces data
- `Subscriber` - consumes data
- `Subscription` - controls flow

### مثال عملی:

```java
import java.util.concurrent.*;
import java.util.concurrent.Flow.*;

public class ReactiveStreamsExample {
    
    public static void main(String[] args) throws Exception {
        // 1. Basic reactive stream
        System.out.println("=== Basic Reactive Stream ===");
        
        Publisher<String> publisher = new StringPublisher();
        Subscriber<String> subscriber = new StringSubscriber();
        
        publisher.subscribe(subscriber);
        
        // 2. Custom publisher
        System.out.println("\n=== Custom Publisher ===");
        
        NumberPublisher numberPublisher = new NumberPublisher();
        NumberSubscriber numberSubscriber = new NumberSubscriber();
        
        numberPublisher.subscribe(numberSubscriber);
        
        // 3. Backpressure handling
        System.out.println("\n=== Backpressure Handling ===");
        
        SlowPublisher slowPublisher = new SlowPublisher();
        SlowSubscriber slowSubscriber = new SlowSubscriber();
        
        slowPublisher.subscribe(slowSubscriber);
        
        // Wait for completion
        Thread.sleep(5000);
    }
}

// Basic string publisher
class StringPublisher implements Publisher<String> {
    private final String[] data = {"Hello", "World", "Java", "Reactive", "Streams"};
    
    @Override
    public void subscribe(Subscriber<? super String> subscriber) {
        subscriber.onSubscribe(new StringSubscription(subscriber, data));
    }
}

// String subscription
class StringSubscription implements Subscription {
    private final Subscriber<? super String> subscriber;
    private final String[] data;
    private int index = 0;
    private boolean cancelled = false;
    
    public StringSubscription(Subscriber<? super String> subscriber, String[] data) {
        this.subscriber = subscriber;
        this.data = data;
    }
    
    @Override
    public void request(long n) {
        if (cancelled) return;
        
        for (int i = 0; i < n && index < data.length; i++) {
            subscriber.onNext(data[index++]);
        }
        
        if (index >= data.length) {
            subscriber.onComplete();
        }
    }
    
    @Override
    public void cancel() {
        cancelled = true;
    }
}

// String subscriber
class StringSubscriber implements Subscriber<String> {
    private Subscription subscription;
    
    @Override
    public void onSubscribe(Subscription subscription) {
        this.subscription = subscription;
        subscription.request(1);
    }
    
    @Override
    public void onNext(String item) {
        System.out.println("Received: " + item);
        subscription.request(1);
    }
    
    @Override
    public void onError(Throwable throwable) {
        System.err.println("Error: " + throwable.getMessage());
    }
    
    @Override
    public void onComplete() {
        System.out.println("Stream completed");
    }
}

// Number publisher
class NumberPublisher implements Publisher<Integer> {
    @Override
    public void subscribe(Subscriber<? super Integer> subscriber) {
        subscriber.onSubscribe(new NumberSubscription(subscriber));
    }
}

// Number subscription
class NumberSubscription implements Subscription {
    private final Subscriber<? super Integer> subscriber;
    private int count = 0;
    private boolean cancelled = false;
    
    public NumberSubscription(Subscriber<? super Integer> subscriber) {
        this.subscriber = subscriber;
    }
    
    @Override
    public void request(long n) {
        if (cancelled) return;
        
        for (int i = 0; i < n && count < 10; i++) {
            subscriber.onNext(count++);
        }
        
        if (count >= 10) {
            subscriber.onComplete();
        }
    }
    
    @Override
    public void cancel() {
        cancelled = true;
    }
}

// Number subscriber
class NumberSubscriber implements Subscriber<Integer> {
    private Subscription subscription;
    
    @Override
    public void onSubscribe(Subscription subscription) {
        this.subscription = subscription;
        subscription.request(5); // Request 5 items at once
    }
    
    @Override
    public void onNext(Integer item) {
        System.out.println("Number: " + item);
    }
    
    @Override
    public void onError(Throwable throwable) {
        System.err.println("Error: " + throwable.getMessage());
    }
    
    @Override
    public void onComplete() {
        System.out.println("Number stream completed");
    }
}

// Slow publisher for backpressure demonstration
class SlowPublisher implements Publisher<String> {
    @Override
    public void subscribe(Subscriber<? super String> subscriber) {
        subscriber.onSubscribe(new SlowSubscription(subscriber));
    }
}

// Slow subscription
class SlowSubscription implements Subscription {
    private final Subscriber<? super String> subscriber;
    private int count = 0;
    private boolean cancelled = false;
    private final ScheduledExecutorService executor = Executors.newScheduledThreadPool(1);
    
    public SlowSubscription(Subscriber<? super String> subscriber) {
        this.subscriber = subscriber;
    }
    
    @Override
    public void request(long n) {
        if (cancelled) return;
        
        for (int i = 0; i < n && count < 20; i++) {
            final int currentCount = count++;
            executor.schedule(() -> {
                if (!cancelled) {
                    subscriber.onNext("Item " + currentCount);
                }
            }, 100, TimeUnit.MILLISECONDS);
        }
        
        if (count >= 20) {
            executor.schedule(() -> {
                if (!cancelled) {
                    subscriber.onComplete();
                }
            }, 2000, TimeUnit.MILLISECONDS);
        }
    }
    
    @Override
    public void cancel() {
        cancelled = true;
        executor.shutdown();
    }
}

// Slow subscriber
class SlowSubscriber implements Subscriber<String> {
    private Subscription subscription;
    
    @Override
    public void onSubscribe(Subscription subscription) {
        this.subscription = subscription;
        subscription.request(1); // Request one item at a time
    }
    
    @Override
    public void onNext(String item) {
        System.out.println("Slow received: " + item);
        try {
            Thread.sleep(200); // Process slowly
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        subscription.request(1); // Request next item
    }
    
    @Override
    public void onError(Throwable throwable) {
        System.err.println("Slow error: " + throwable.getMessage());
    }
    
    @Override
    public void onComplete() {
        System.out.println("Slow stream completed");
    }
}
```

### آنالوژی دنیای واقعی:
Reactive Streams مانند داشتن یک سیستم آبیاری هوشمند است که می‌تواند جریان آب را کنترل کند. اگر باغبان (subscriber) نمی‌تواند آب بیشتری دریافت کند، سیستم (publisher) جریان را کاهش می‌دهد تا از سرریز جلوگیری کند.