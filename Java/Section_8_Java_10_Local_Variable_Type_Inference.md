# Section 8 - Java 10 - Local Variable Type Inference

## 8.1 var Keyword & Type Inference

Java 10 کلمه کلیدی `var` را معرفی کرد که امکان type inference برای local variables فراهم می‌کند.

### مفاهیم کلیدی:

**1. Type Inference:**
- کامپایلر نوع را از context تشخیص می‌دهد
- کد کوتاه‌تر و خوانا‌تر می‌شود
- فقط برای local variables قابل استفاده است

**2. Limitations:**
- نمی‌توان برای fields، method parameters، یا return types استفاده کرد
- باید initializer داشته باشد
- نمی‌توان null assign کرد

### مثال عملی:

```java
import java.util.*;
import java.util.stream.*;

public class VarKeywordExample {
    
    public static void main(String[] args) {
        // 1. Basic var usage
        System.out.println("=== Basic var Usage ===");
        
        var name = "احمد محمدی";
        var age = 25;
        var salary = 50000.50;
        var isEmployed = true;
        
        System.out.println("Name: " + name + " (" + name.getClass().getSimpleName() + ")");
        System.out.println("Age: " + age + " (" + age.getClass().getSimpleName() + ")");
        System.out.println("Salary: " + salary + " (" + salary.getClass().getSimpleName() + ")");
        System.out.println("Employed: " + isEmployed + " (" + isEmployed.getClass().getSimpleName() + ")");
        
        // 2. Collections with var
        System.out.println("\n=== Collections with var ===");
        
        var numbers = Arrays.asList(1, 2, 3, 4, 5);
        var names = new ArrayList<String>();
        names.add("احمد");
        names.add("فاطمه");
        names.add("علی");
        
        System.out.println("Numbers: " + numbers);
        System.out.println("Names: " + names);
        
        // 3. Maps with var
        System.out.println("\n=== Maps with var ===");
        
        var studentGrades = new HashMap<String, Integer>();
        studentGrades.put("احمد", 18);
        studentGrades.put("فاطمه", 19);
        studentGrades.put("علی", 17);
        
        System.out.println("Student grades: " + studentGrades);
        
        // 4. Streams with var
        System.out.println("\n=== Streams with var ===");
        
        var numbersList = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        var evenNumbers = numbersList.stream()
            .filter(n -> n % 2 == 0)
            .map(n -> n * n)
            .collect(Collectors.toList());
        
        System.out.println("Even numbers squared: " + evenNumbers);
        
        // 5. Complex types with var
        System.out.println("\n=== Complex Types with var ===");
        
        var person = new Person("احمد", 25, "تهران");
        var personList = Arrays.asList(
            new Person("احمد", 25, "تهران"),
            new Person("فاطمه", 30, "اصفهان"),
            new Person("علی", 22, "تهران")
        );
        
        System.out.println("Person: " + person);
        System.out.println("Person list: " + personList);
        
        // 6. Method calls with var
        System.out.println("\n=== Method Calls with var ===");
        
        var result = calculateSum(10, 20);
        var message = createMessage("احمد", 25);
        
        System.out.println("Sum result: " + result);
        System.out.println("Message: " + message);
        
        // 7. Loops with var
        System.out.println("\n=== Loops with var ===");
        
        for (var i = 0; i < 5; i++) {
            System.out.println("Loop iteration: " + i);
        }
        
        for (var person2 : personList) {
            System.out.println("Person in loop: " + person2);
        }
        
        // 8. Try-with-resources with var
        System.out.println("\n=== Try-with-resources with var ===");
        
        try (var scanner = new Scanner("Hello World")) {
            while (scanner.hasNext()) {
                var word = scanner.next();
                System.out.println("Word: " + word);
            }
        }
        
        // 9. Lambda expressions with var
        System.out.println("\n=== Lambda Expressions with var ===");
        
        var numbers2 = Arrays.asList(1, 2, 3, 4, 5);
        var doubledNumbers = numbers2.stream()
            .map((var n) -> n * 2)
            .collect(Collectors.toList());
        
        System.out.println("Doubled numbers: " + doubledNumbers);
        
        // 10. Generic types with var
        System.out.println("\n=== Generic Types with var ===");
        
        var stringList = new ArrayList<String>();
        stringList.add("Java");
        stringList.add("Python");
        stringList.add("C++");
        
        var integerList = new ArrayList<Integer>();
        integerList.add(1);
        integerList.add(2);
        integerList.add(3);
        
        System.out.println("String list: " + stringList);
        System.out.println("Integer list: " + integerList);
    }
    
    public static int calculateSum(int a, int b) {
        return a + b;
    }
    
    public static String createMessage(String name, int age) {
        return "Hello " + name + ", you are " + age + " years old";
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
    
    @Override
    public String toString() {
        return name + " (" + age + ", " + city + ")";
    }
}
```

### آنالوژی دنیای واقعی:
var keyword مانند داشتن یک دستیار هوشمند است که می‌تواند نوع اشیاء را از context تشخیص دهد. به جای گفتن "یک لیست از اعداد صحیح"، می‌گویید "یک لیست" و دستیار می‌داند که چه نوع لیستی است.

## 8.2 Application Class-Data Sharing

Application Class-Data Sharing (AppCDS) امکان اشتراک‌گذاری class data بین multiple JVM instances را فراهم می‌کند.

### مفاهیم کلیدی:

**1. Class Data Sharing:**
- کاهش startup time
- کاهش memory footprint
- بهتر برای applications با classpath بزرگ

**2. CDS Archive:**
- فایل‌های .jsa برای storing class data
- Shared across JVM instances
- Platform-specific

### مثال عملی:

```java
import java.util.*;
import java.util.concurrent.*;

public class AppCDSExample {
    
    public static void main(String[] args) {
        System.out.println("=== Application Class-Data Sharing Example ===");
        
        // 1. Basic class loading demonstration
        System.out.println("=== Basic Class Loading ===");
        
        var startTime = System.currentTimeMillis();
        
        // Load various classes
        var list = new ArrayList<String>();
        var map = new HashMap<String, Integer>();
        var set = new HashSet<String>();
        var queue = new ConcurrentLinkedQueue<String>();
        
        var endTime = System.currentTimeMillis();
        System.out.println("Class loading time: " + (endTime - startTime) + " ms");
        
        // 2. Memory usage demonstration
        System.out.println("\n=== Memory Usage ===");
        
        var runtime = Runtime.getRuntime();
        var totalMemory = runtime.totalMemory();
        var freeMemory = runtime.freeMemory();
        var usedMemory = totalMemory - freeMemory;
        
        System.out.println("Total memory: " + totalMemory / 1024 / 1024 + " MB");
        System.out.println("Free memory: " + freeMemory / 1024 / 1024 + " MB");
        System.out.println("Used memory: " + usedMemory / 1024 / 1024 + " MB");
        
        // 3. Class loading performance
        System.out.println("\n=== Class Loading Performance ===");
        
        var classNames = Arrays.asList(
            "java.util.ArrayList",
            "java.util.HashMap",
            "java.util.HashSet",
            "java.util.concurrent.ConcurrentLinkedQueue",
            "java.util.concurrent.Executors",
            "java.util.stream.Stream",
            "java.util.Optional",
            "java.util.function.Predicate"
        );
        
        startTime = System.currentTimeMillis();
        
        for (var className : classNames) {
            try {
                Class.forName(className);
            } catch (ClassNotFoundException e) {
                System.err.println("Class not found: " + className);
            }
        }
        
        endTime = System.currentTimeMillis();
        System.out.println("Class loading time for " + classNames.size() + " classes: " + 
            (endTime - startTime) + " ms");
        
        // 4. Application-specific classes
        System.out.println("\n=== Application-Specific Classes ===");
        
        var calculator = new Calculator();
        var result = calculator.calculate(10, 5, Calculator.Operation.ADD);
        System.out.println("Calculation result: " + result);
        
        var processor = new DataProcessor();
        var processedData = processor.process("Hello World");
        System.out.println("Processed data: " + processedData);
        
        // 5. Thread pool demonstration
        System.out.println("\n=== Thread Pool Demonstration ===");
        
        var executor = Executors.newFixedThreadPool(4);
        var futures = new ArrayList<Future<String>>();
        
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            var future = executor.submit(() -> {
                Thread.sleep(1000);
                return "Task " + taskId + " completed";
            });
            futures.add(future);
        }
        
        for (var future : futures) {
            try {
                System.out.println(future.get());
            } catch (InterruptedException | ExecutionException e) {
                System.err.println("Task failed: " + e.getMessage());
            }
        }
        
        executor.shutdown();
        
        // 6. Stream processing demonstration
        System.out.println("\n=== Stream Processing ===");
        
        var numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        var evenSquares = numbers.stream()
            .filter(n -> n % 2 == 0)
            .map(n -> n * n)
            .collect(Collectors.toList());
        
        System.out.println("Even squares: " + evenSquares);
        
        // 7. Optional usage
        System.out.println("\n=== Optional Usage ===");
        
        var optionalValue = Optional.of("Hello World");
        optionalValue.ifPresent(value -> System.out.println("Optional value: " + value));
        
        var emptyOptional = Optional.empty();
        var defaultValue = emptyOptional.orElse("Default value");
        System.out.println("Default value: " + defaultValue);
    }
}

// Application-specific classes
class Calculator {
    public enum Operation {
        ADD, SUBTRACT, MULTIPLY, DIVIDE
    }
    
    public double calculate(double a, double b, Operation operation) {
        return switch (operation) {
            case ADD -> a + b;
            case SUBTRACT -> a - b;
            case MULTIPLY -> a * b;
            case DIVIDE -> b != 0 ? a / b : Double.NaN;
        };
    }
}

class DataProcessor {
    public String process(String data) {
        return data.toUpperCase().trim();
    }
}
```

### آنالوژی دنیای واقعی:
AppCDS مانند داشتن یک کتابخانه مشترک است که چندین نفر می‌توانند از آن استفاده کنند. به جای اینکه هر نفر کتاب‌های خود را داشته باشد، همه از همان کتابخانه استفاده می‌کنند که باعث صرفه‌جویی در فضا و زمان می‌شود.

## 8.3 Garbage Collector Interface

Java 10 یک interface مشترک برای garbage collectors معرفی کرد.

### مفاهیم کلیدی:

**1. Unified GC Interface:**
- Interface مشترک برای تمام GCs
- آسان‌تر برای اضافه کردن GCs جدید
- Better abstraction

**2. GC Selection:**
- انتخاب GC بر اساس application requirements
- Performance tuning
- Memory management

### مثال عملی:

```java
import java.util.*;
import java.util.concurrent.*;

public class GCInterfaceExample {
    
    public static void main(String[] args) {
        System.out.println("=== Garbage Collector Interface Example ===");
        
        // 1. Memory allocation demonstration
        System.out.println("=== Memory Allocation ===");
        
        var startTime = System.currentTimeMillis();
        var memoryBefore = getUsedMemory();
        
        // Allocate memory
        var largeList = new ArrayList<String>();
        for (int i = 0; i < 100000; i++) {
            largeList.add("String " + i);
        }
        
        var memoryAfter = getUsedMemory();
        var endTime = System.currentTimeMillis();
        
        System.out.println("Memory before: " + memoryBefore + " MB");
        System.out.println("Memory after: " + memoryAfter + " MB");
        System.out.println("Memory allocated: " + (memoryAfter - memoryBefore) + " MB");
        System.out.println("Allocation time: " + (endTime - startTime) + " ms");
        
        // 2. GC triggering demonstration
        System.out.println("\n=== GC Triggering ===");
        
        // Clear references to allow GC
        largeList = null;
        
        // Suggest garbage collection
        System.gc();
        
        // Wait a bit for GC to complete
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        var memoryAfterGC = getUsedMemory();
        System.out.println("Memory after GC: " + memoryAfterGC + " MB");
        System.out.println("Memory freed: " + (memoryAfter - memoryAfterGC) + " MB");
        
        // 3. Object creation and destruction
        System.out.println("\n=== Object Creation and Destruction ===");
        
        var objectList = new ArrayList<Object>();
        
        for (int i = 0; i < 1000; i++) {
            var obj = new TestObject("Object " + i, i);
            objectList.add(obj);
        }
        
        System.out.println("Created " + objectList.size() + " objects");
        
        // Clear half of the objects
        for (int i = 0; i < objectList.size() / 2; i++) {
            objectList.set(i, null);
        }
        
        System.gc();
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        System.out.println("Cleared half of the objects");
        
        // 4. Memory pressure demonstration
        System.out.println("\n=== Memory Pressure ===");
        
        var pressureList = new ArrayList<byte[]>();
        
        try {
            while (true) {
                var buffer = new byte[1024 * 1024]; // 1MB buffer
                pressureList.add(buffer);
                
                if (pressureList.size() % 100 == 0) {
                    System.out.println("Allocated " + pressureList.size() + " MB");
                }
            }
        } catch (OutOfMemoryError e) {
            System.out.println("Out of memory after allocating " + pressureList.size() + " MB");
        }
        
        // 5. GC monitoring
        System.out.println("\n=== GC Monitoring ===");
        
        var gcMonitor = new GCMonitor();
        gcMonitor.start();
        
        // Create some objects
        var tempList = new ArrayList<String>();
        for (int i = 0; i < 10000; i++) {
            tempList.add("Temp string " + i);
        }
        
        // Clear and trigger GC
        tempList = null;
        System.gc();
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        gcMonitor.stop();
        
        // 6. Different object types
        System.out.println("\n=== Different Object Types ===");
        
        var stringList = new ArrayList<String>();
        var integerList = new ArrayList<Integer>();
        var doubleList = new ArrayList<Double>();
        var booleanList = new ArrayList<Boolean>();
        
        for (int i = 0; i < 1000; i++) {
            stringList.add("String " + i);
            integerList.add(i);
            doubleList.add(i * 1.0);
            booleanList.add(i % 2 == 0);
        }
        
        System.out.println("Created collections of different types");
        System.out.println("String list size: " + stringList.size());
        System.out.println("Integer list size: " + integerList.size());
        System.out.println("Double list size: " + doubleList.size());
        System.out.println("Boolean list size: " + booleanList.size());
        
        // 7. Finalization demonstration
        System.out.println("\n=== Finalization ===");
        
        for (int i = 0; i < 10; i++) {
            var finalizableObject = new FinalizableObject("Object " + i);
            finalizableObject = null;
        }
        
        System.gc();
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    private static long getUsedMemory() {
        var runtime = Runtime.getRuntime();
        return (runtime.totalMemory() - runtime.freeMemory()) / 1024 / 1024;
    }
}

// Test object class
class TestObject {
    private String name;
    private int value;
    
    public TestObject(String name, int value) {
        this.name = name;
        this.value = value;
    }
    
    @Override
    protected void finalize() throws Throwable {
        System.out.println("Finalizing: " + name);
        super.finalize();
    }
}

// Finalizable object class
class FinalizableObject {
    private String name;
    
    public FinalizableObject(String name) {
        this.name = name;
    }
    
    @Override
    protected void finalize() throws Throwable {
        System.out.println("Finalizing: " + name);
        super.finalize();
    }
}

// GC monitor class
class GCMonitor {
    private volatile boolean running = false;
    private Thread monitorThread;
    
    public void start() {
        running = true;
        monitorThread = new Thread(() -> {
            while (running) {
                var runtime = Runtime.getRuntime();
                var usedMemory = (runtime.totalMemory() - runtime.freeMemory()) / 1024 / 1024;
                System.out.println("Memory usage: " + usedMemory + " MB");
                
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        monitorThread.start();
    }
    
    public void stop() {
        running = false;
        if (monitorThread != null) {
            monitorThread.interrupt();
        }
    }
}
```

### آنالوژی دنیای واقعی:
GC Interface مانند داشتن یک سیستم مدیریت زباله هوشمند است که می‌تواند روش‌های مختلف جمع‌آوری زباله را انتخاب کند. بسته به نوع زباله و شرایط محیطی، بهترین روش را انتخاب می‌کند.

## 8.4 Root Certificates

Java 10 root certificates جدیدی را به Java platform اضافه کرد.

### مفاهیم کلیدی:

**1. Security Updates:**
- اضافه کردن root certificates جدید
- بهبود امنیت SSL/TLS
- پشتیبانی از CA های جدید

### مثال عملی:

```java
import javax.net.ssl.*;
import java.security.cert.*;
import java.security.*;
import java.io.*;
import java.net.*;

public class RootCertificatesExample {
    
    public static void main(String[] args) {
        System.out.println("=== Root Certificates Example ===");
        
        // 1. List available root certificates
        System.out.println("=== Available Root Certificates ===");
        
        try {
            var trustStore = KeyStore.getInstance("JKS");
            var trustStoreFile = new File(System.getProperty("java.home") + 
                "/lib/security/cacerts");
            var trustStorePassword = "changeit";
            
            trustStore.load(new FileInputStream(trustStoreFile), 
                trustStorePassword.toCharArray());
            
            var aliases = trustStore.aliases();
            var count = 0;
            
            while (aliases.hasMoreElements()) {
                var alias = aliases.nextElement();
                var certificate = trustStore.getCertificate(alias);
                
                if (certificate instanceof X509Certificate) {
                    var x509Cert = (X509Certificate) certificate;
                    System.out.println("Alias: " + alias);
                    System.out.println("Subject: " + x509Cert.getSubjectDN());
                    System.out.println("Issuer: " + x509Cert.getIssuerDN());
                    System.out.println("Valid from: " + x509Cert.getNotBefore());
                    System.out.println("Valid until: " + x509Cert.getNotAfter());
                    System.out.println("---");
                    count++;
                }
            }
            
            System.out.println("Total root certificates: " + count);
            
        } catch (Exception e) {
            System.err.println("Error listing certificates: " + e.getMessage());
        }
        
        // 2. SSL connection demonstration
        System.out.println("\n=== SSL Connection ===");
        
        try {
            var url = new URL("https://www.google.com");
            var connection = (HttpsURLConnection) url.openConnection();
            
            // Set SSL context
            var sslContext = SSLContext.getInstance("TLS");
            sslContext.init(null, null, null);
            connection.setSSLSocketFactory(sslContext.getSocketFactory());
            
            // Set hostname verifier
            connection.setHostnameVerifier((hostname, session) -> true);
            
            // Connect
            connection.connect();
            
            System.out.println("Response code: " + connection.getResponseCode());
            System.out.println("Cipher suite: " + connection.getCipherSuite());
            System.out.println("Server certificates: " + 
                connection.getServerCertificates().length);
            
            connection.disconnect();
            
        } catch (Exception e) {
            System.err.println("Error connecting to HTTPS: " + e.getMessage());
        }
        
        // 3. Certificate validation
        System.out.println("\n=== Certificate Validation ===");
        
        try {
            var url = new URL("https://www.github.com");
            var connection = (HttpsURLConnection) url.openConnection();
            
            connection.connect();
            
            var certificates = connection.getServerCertificates();
            System.out.println("Server certificates count: " + certificates.length);
            
            for (int i = 0; i < certificates.length; i++) {
                var cert = (X509Certificate) certificates[i];
                System.out.println("Certificate " + (i + 1) + ":");
                System.out.println("  Subject: " + cert.getSubjectDN());
                System.out.println("  Issuer: " + cert.getIssuerDN());
                System.out.println("  Valid from: " + cert.getNotBefore());
                System.out.println("  Valid until: " + cert.getNotAfter());
                System.out.println("  Signature algorithm: " + cert.getSigAlgName());
            }
            
            connection.disconnect();
            
        } catch (Exception e) {
            System.err.println("Error validating certificates: " + e.getMessage());
        }
        
        // 4. Custom trust store
        System.out.println("\n=== Custom Trust Store ===");
        
        try {
            var customTrustStore = KeyStore.getInstance("JKS");
            customTrustStore.load(null, null);
            
            // Add a custom certificate (example)
            var customCert = createCustomCertificate();
            customTrustStore.setCertificateEntry("custom", customCert);
            
            System.out.println("Custom trust store created with " + 
                customTrustStore.size() + " certificates");
            
        } catch (Exception e) {
            System.err.println("Error creating custom trust store: " + e.getMessage());
        }
        
        // 5. SSL context configuration
        System.out.println("\n=== SSL Context Configuration ===");
        
        try {
            var sslContext = SSLContext.getInstance("TLS");
            sslContext.init(null, null, null);
            
            var supportedProtocols = sslContext.getSupportedSSLParameters().getProtocols();
            System.out.println("Supported protocols: " + Arrays.toString(supportedProtocols));
            
            var supportedCipherSuites = sslContext.getSupportedSSLParameters().getCipherSuites();
            System.out.println("Supported cipher suites count: " + supportedCipherSuites.length);
            
        } catch (Exception e) {
            System.err.println("Error configuring SSL context: " + e.getMessage());
        }
    }
    
    private static X509Certificate createCustomCertificate() {
        // This is a simplified example - in practice, you would load a real certificate
        try {
            var certFactory = CertificateFactory.getInstance("X.509");
            var certData = "-----BEGIN CERTIFICATE-----\n" +
                "MIICdTCCAd4CAQAwDQYJKoZIhvcNAQEFBQAwEzERMA8GA1UEAxMIY2F0ZXN0\n" +
                "-----END CERTIFICATE-----";
            var certStream = new ByteArrayInputStream(certData.getBytes());
            return (X509Certificate) certFactory.generateCertificate(certStream);
        } catch (Exception e) {
            throw new RuntimeException("Error creating custom certificate", e);
        }
    }
}
```

### آنالوژی دنیای واقعی:
Root certificates مانند داشتن یک دفترچه تلفن معتبر برای شناسایی افراد است. وقتی کسی خود را معرفی می‌کند، می‌توانید از این دفترچه استفاده کنید تا مطمئن شوید که او واقعاً همان کسی است که می‌گوید.

## 8.5 Thread-Local Handshakes

Thread-Local Handshakes امکان اجرای operations روی threads بدون stopping آن‌ها فراهم می‌کند.

### مفاهیم کلیدی:

**1. Safe Points:**
- نقاطی که thread می‌تواند safely stop شود
- بدون affecting application performance
- Better debugging and profiling

**2. Thread Operations:**
- اجرای operations روی specific threads
- بدون stopping entire application
- Better control over thread execution

### مثال عملی:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ThreadLocalHandshakesExample {
    
    private static final AtomicInteger threadCounter = new AtomicInteger(0);
    private static final ExecutorService executor = Executors.newFixedThreadPool(4);
    
    public static void main(String[] args) throws Exception {
        System.out.println("=== Thread-Local Handshakes Example ===");
        
        // 1. Basic thread creation and management
        System.out.println("=== Basic Thread Management ===");
        
        var threads = new ArrayList<Thread>();
        
        for (int i = 0; i < 5; i++) {
            var thread = new Thread(() -> {
                var threadId = threadCounter.incrementAndGet();
                System.out.println("Thread " + threadId + " started");
                
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                System.out.println("Thread " + threadId + " completed");
            });
            
            threads.add(thread);
            thread.start();
        }
        
        // Wait for all threads to complete
        for (var thread : threads) {
            thread.join();
        }
        
        // 2. Thread pool demonstration
        System.out.println("\n=== Thread Pool Demonstration ===");
        
        var futures = new ArrayList<Future<String>>();
        
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            var future = executor.submit(() -> {
                var threadName = Thread.currentThread().getName();
                System.out.println("Task " + taskId + " executed by " + threadName);
                
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                return "Task " + taskId + " completed by " + threadName;
            });
            
            futures.add(future);
        }
        
        // Wait for all tasks to complete
        for (var future : futures) {
            try {
                var result = future.get();
                System.out.println("Result: " + result);
            } catch (InterruptedException | ExecutionException e) {
                System.err.println("Task failed: " + e.getMessage());
            }
        }
        
        // 3. Thread monitoring
        System.out.println("\n=== Thread Monitoring ===");
        
        var monitor = new ThreadMonitor();
        monitor.start();
        
        // Create some threads
        var monitoredThreads = new ArrayList<Thread>();
        
        for (int i = 0; i < 3; i++) {
            var thread = new Thread(() -> {
                var threadName = Thread.currentThread().getName();
                System.out.println("Monitored thread " + threadName + " started");
                
                try {
                    Thread.sleep(3000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                System.out.println("Monitored thread " + threadName + " completed");
            });
            
            monitoredThreads.add(thread);
            thread.start();
        }
        
        // Wait for monitored threads
        for (var thread : monitoredThreads) {
            thread.join();
        }
        
        monitor.stop();
        
        // 4. Thread interruption
        System.out.println("\n=== Thread Interruption ===");
        
        var interruptibleThread = new Thread(() -> {
            var threadName = Thread.currentThread().getName();
            System.out.println("Interruptible thread " + threadName + " started");
            
            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                System.out.println("Thread " + threadName + " was interrupted");
                Thread.currentThread().interrupt();
            }
            
            System.out.println("Interruptible thread " + threadName + " completed");
        });
        
        interruptibleThread.start();
        
        // Interrupt after 2 seconds
        Thread.sleep(2000);
        interruptibleThread.interrupt();
        interruptibleThread.join();
        
        // 5. Thread synchronization
        System.out.println("\n=== Thread Synchronization ===");
        
        var sharedCounter = new AtomicInteger(0);
        var syncThreads = new ArrayList<Thread>();
        
        for (int i = 0; i < 5; i++) {
            var thread = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    sharedCounter.incrementAndGet();
                }
            });
            
            syncThreads.add(thread);
            thread.start();
        }
        
        // Wait for all sync threads
        for (var thread : syncThreads) {
            thread.join();
        }
        
        System.out.println("Final counter value: " + sharedCounter.get());
        
        // 6. Thread group demonstration
        System.out.println("\n=== Thread Group Demonstration ===");
        
        var threadGroup = new ThreadGroup("TestGroup");
        var groupThreads = new ArrayList<Thread>();
        
        for (int i = 0; i < 3; i++) {
            var thread = new Thread(threadGroup, () -> {
                var threadName = Thread.currentThread().getName();
                System.out.println("Group thread " + threadName + " started");
                
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                System.out.println("Group thread " + threadName + " completed");
            });
            
            groupThreads.add(thread);
            thread.start();
        }
        
        // Wait for group threads
        for (var thread : groupThreads) {
            thread.join();
        }
        
        System.out.println("Thread group active count: " + threadGroup.activeCount());
        
        // 7. Thread local variables
        System.out.println("\n=== Thread Local Variables ===");
        
        var threadLocal = new ThreadLocal<String>();
        var localThreads = new ArrayList<Thread>();
        
        for (int i = 0; i < 3; i++) {
            final int threadId = i;
            var thread = new Thread(() -> {
                threadLocal.set("Thread " + threadId + " value");
                System.out.println("Thread " + threadId + " set value: " + threadLocal.get());
                
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                System.out.println("Thread " + threadId + " final value: " + threadLocal.get());
            });
            
            localThreads.add(thread);
            thread.start();
        }
        
        // Wait for local threads
        for (var thread : localThreads) {
            thread.join();
        }
        
        // Cleanup
        executor.shutdown();
    }
}

// Thread monitor class
class ThreadMonitor {
    private volatile boolean running = false;
    private Thread monitorThread;
    
    public void start() {
        running = true;
        monitorThread = new Thread(() -> {
            while (running) {
                var threadCount = Thread.activeCount();
                System.out.println("Active threads: " + threadCount);
                
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        monitorThread.start();
    }
    
    public void stop() {
        running = false;
        if (monitorThread != null) {
            monitorThread.interrupt();
        }
    }
}
```

### آنالوژی دنیای واقعی:
Thread-Local Handshakes مانند داشتن یک سیستم ارتباطی هوشمند است که می‌تواند با کارگران مختلف در یک کارخانه صحبت کند بدون اینکه کار را متوقف کند. می‌تواند دستورالعمل‌های جدید بدهد یا وضعیت آن‌ها را بررسی کند.