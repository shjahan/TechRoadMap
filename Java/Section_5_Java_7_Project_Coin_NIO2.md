# Section 5 - Java 7 - Project Coin & NIO.2

## 5.1 Try-with-resources Statement

Try-with-resources statement یکی از مهم‌ترین ویژگی‌های Java 7 است که مدیریت منابع (resources) را به صورت خودکار انجام می‌دهد.

### مفاهیم کلیدی:

**1. Automatic Resource Management:**
- منابع به صورت خودکار بسته می‌شوند
- نیازی به finally block نیست
- جلوگیری از resource leaks

**2. AutoCloseable Interface:**
- تمام منابع باید این interface را implement کنند
- close() method به صورت خودکار فراخوانی می‌شود

### مثال عملی:

```java
import java.io.*;
import java.sql.*;

public class TryWithResourcesExample {
    
    // Before Java 7 - Manual resource management
    public static void readFileOldWay(String filename) {
        FileReader reader = null;
        try {
            reader = new FileReader(filename);
            int character;
            while ((character = reader.read()) != -1) {
                System.out.print((char) character);
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    System.err.println("Error closing file: " + e.getMessage());
                }
            }
        }
    }
    
    // Java 7+ - Try-with-resources
    public static void readFileNewWay(String filename) {
        try (FileReader reader = new FileReader(filename)) {
            int character;
            while ((character = reader.read()) != -1) {
                System.out.print((char) character);
            }
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }
        // FileReader automatically closed
    }
    
    // Multiple resources
    public static void copyFile(String source, String destination) {
        try (FileInputStream fis = new FileInputStream(source);
             FileOutputStream fos = new FileOutputStream(destination)) {
            
            byte[] buffer = new byte[1024];
            int length;
            while ((length = fis.read(buffer)) > 0) {
                fos.write(buffer, 0, length);
            }
            System.out.println("File copied successfully");
        } catch (IOException e) {
            System.err.println("Error copying file: " + e.getMessage());
        }
    }
    
    // Custom resource
    public static void useCustomResource() {
        try (CustomResource resource = new CustomResource()) {
            resource.doSomething();
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
    
    public static void main(String[] args) {
        // Example usage
        readFileNewWay("sample.txt");
        copyFile("source.txt", "destination.txt");
        useCustomResource();
    }
}

// Custom resource implementing AutoCloseable
class CustomResource implements AutoCloseable {
    public void doSomething() {
        System.out.println("Using custom resource");
    }
    
    @Override
    public void close() throws Exception {
        System.out.println("Custom resource closed");
    }
}
```

### آنالوژی دنیای واقعی:
Try-with-resources مانند استفاده از کلید خودکار در ماشین است. وقتی ماشین را روشن می‌کنید، کلید به صورت خودکار در جای خود قرار می‌گیرد و وقتی ماشین را خاموش می‌کنید، کلید به صورت خودکار خارج می‌شود.

## 5.2 Diamond Operator (<>) for Generics

Diamond operator راه ساده‌تری برای استفاده از generics فراهم می‌کند.

### مفاهیم کلیدی:

**1. Type Inference:**
- کامپایلر نوع را از context تشخیص می‌دهد
- کد کوتاه‌تر و خوانا‌تر می‌شود
- کمتر prone to errors

### مثال عملی:

```java
import java.util.*;

public class DiamondOperatorExample {
    public static void main(String[] args) {
        // Before Java 7 - Verbose
        Map<String, List<String>> oldMap = new HashMap<String, List<String>>();
        List<String> oldList = new ArrayList<String>();
        
        // Java 7+ - Diamond operator
        Map<String, List<String>> newMap = new HashMap<>();
        List<String> newList = new ArrayList<>();
        
        // Generic method with diamond
        List<String> result = createList("Java", "Python", "C++");
        System.out.println("Created list: " + result);
        
        // Nested generics
        Map<String, Map<String, Integer>> nestedMap = new HashMap<>();
        nestedMap.put("category1", new HashMap<>());
        nestedMap.get("category1").put("item1", 100);
        
        System.out.println("Nested map: " + nestedMap);
    }
    
    public static <T> List<T> createList(T... items) {
        List<T> list = new ArrayList<>();
        for (T item : items) {
            list.add(item);
        }
        return list;
    }
}
```

### آنالوژی دنیای واقعی:
Diamond operator مانند استفاده از "همان" به جای تکرار نام کامل است. به جای گفتن "من همان کتابی را می‌خواهم که قبلاً داشتم"، می‌گویید "همان کتاب را می‌خواهم".

## 5.3 String Switch Statements

Java 7 امکان استفاده از String در switch statements را فراهم کرد.

### مفاهیم کلیدی:

**1. String-based Switching:**
- مقایسه String با equals() و hashCode()
- Performance optimization
- Cleaner code structure

### مثال عملی:

```java
public class StringSwitchExample {
    
    public static String getDayType(String day) {
        switch (day.toLowerCase()) {
            case "monday":
            case "tuesday":
            case "wednesday":
            case "thursday":
            case "friday":
                return "Weekday";
            case "saturday":
            case "sunday":
                return "Weekend";
            default:
                return "Unknown";
        }
    }
    
    public static String getSeason(String month) {
        switch (month.toLowerCase()) {
            case "december":
            case "january":
            case "february":
                return "Winter";
            case "march":
            case "april":
            case "may":
                return "Spring";
            case "june":
            case "july":
            case "august":
                return "Summer";
            case "september":
            case "october":
            case "november":
                return "Autumn";
            default:
                return "Invalid month";
        }
    }
    
    public static void main(String[] args) {
        System.out.println("Monday is a: " + getDayType("Monday"));
        System.out.println("Saturday is a: " + getDayType("Saturday"));
        System.out.println("December is: " + getSeason("December"));
        System.out.println("June is: " + getSeason("June"));
    }
}
```

### آنالوژی دنیای واقعی:
String switch مانند داشتن یک کلید هوشمند است که می‌تواند با کلمات مختلف کار کند. به جای داشتن کلیدهای مختلف برای هر در، یک کلید دارید که با گفتن نام در، آن را باز می‌کند.

## 5.4 Binary Literals & Underscores in Numerics

Java 7 امکان استفاده از binary literals و underscores در اعداد را فراهم کرد.

### مفاهیم کلیدی:

**1. Binary Literals:**
- نمایش اعداد در مبنای 2
- استفاده از prefix `0b` یا `0B`
- مفید برای bit manipulation

**2. Underscores in Numerics:**
- بهبود خوانایی اعداد بزرگ
- فقط در بین ارقام قابل استفاده
- کامپایلر آن‌ها را نادیده می‌گیرد

### مثال عملی:

```java
public class BinaryLiteralsExample {
    public static void main(String[] args) {
        // Binary literals
        int binary = 0b1010; // 10 in decimal
        int binaryWithUnderscore = 0b1010_1010; // 170 in decimal
        
        System.out.println("Binary 1010: " + binary);
        System.out.println("Binary 1010_1010: " + binaryWithUnderscore);
        
        // Underscores in different bases
        int decimal = 1_000_000;
        int hex = 0xFF_EC_DE_5E;
        int octal = 07_7_7;
        
        System.out.println("Decimal with underscores: " + decimal);
        System.out.println("Hex with underscores: " + hex);
        System.out.println("Octal with underscores: " + octal);
        
        // Bit manipulation examples
        int flags = 0b0000_0000_0000_0000_0000_0000_0000_0000;
        
        // Set bit 5
        flags |= 0b0000_0000_0000_0000_0000_0000_0001_0000;
        System.out.println("After setting bit 5: " + Integer.toBinaryString(flags));
        
        // Set bit 10
        flags |= 0b0000_0000_0000_0000_0000_0100_0000_0000;
        System.out.println("After setting bit 10: " + Integer.toBinaryString(flags));
        
        // Check if bit 5 is set
        boolean bit5Set = (flags & 0b0000_0000_0000_0000_0000_0000_0001_0000) != 0;
        System.out.println("Bit 5 is set: " + bit5Set);
        
        // Long literals with underscores
        long creditCardNumber = 1234_5678_9012_3456L;
        long socialSecurityNumber = 999_99_9999L;
        
        System.out.println("Credit card: " + creditCardNumber);
        System.out.println("SSN: " + socialSecurityNumber);
    }
}
```

### آنالوژی دنیای واقعی:
Binary literals مانند استفاده از کدهای دودویی در سیستم‌های امنیتی است. هر بیت نشان‌دهنده یک وضعیت (روشن/خاموش) است. Underscores مانند استفاده از کاما در اعداد بزرگ برای خوانایی بهتر است.

## 5.5 Multi-catch Exception Handling

Java 7 امکان catch کردن چندین exception در یک catch block را فراهم کرد.

### مفاهیم کلیدی:

**1. Multiple Exception Types:**
- استفاده از `|` برای جدا کردن exception types
- کاهش code duplication
- Cleaner exception handling

### مثال عملی:

```java
import java.io.*;
import java.sql.*;
import java.net.*;

public class MultiCatchExample {
    
    public static void processFile(String filename) {
        try {
            FileInputStream fis = new FileInputStream(filename);
            // Process file
            fis.close();
        } catch (FileNotFoundException | SecurityException e) {
            System.err.println("File access error: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("IO error: " + e.getMessage());
        }
    }
    
    public static void connectToDatabase(String url, String user, String password) {
        try {
            Connection conn = DriverManager.getConnection(url, user, password);
            // Database operations
            conn.close();
        } catch (SQLException | ClassNotFoundException e) {
            System.err.println("Database error: " + e.getMessage());
        }
    }
    
    public static void makeHttpRequest(String url) {
        try {
            URL requestUrl = new URL(url);
            // Make HTTP request
        } catch (MalformedURLException | SecurityException e) {
            System.err.println("URL error: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Network error: " + e.getMessage());
        }
    }
    
    public static void demonstrateMultiCatch() {
        try {
            // Simulate different exceptions
            throw new FileNotFoundException("File not found");
        } catch (FileNotFoundException | IOException | RuntimeException e) {
            System.err.println("Caught exception: " + e.getClass().getSimpleName());
            System.err.println("Message: " + e.getMessage());
        }
    }
    
    public static void main(String[] args) {
        processFile("nonexistent.txt");
        connectToDatabase("jdbc:mysql://localhost/test", "user", "pass");
        makeHttpRequest("http://example.com");
        demonstrateMultiCatch();
    }
}
```

### آنالوژی دنیای واقعی:
Multi-catch مانند داشتن یک سیستم امنیتی است که می‌تواند چندین نوع تهدید را همزمان تشخیص دهد. به جای داشتن سنسورهای جداگانه برای هر نوع تهدید، یک سیستم دارید که همه را پوشش می‌دهد.

## 5.6 NIO.2 File System API

NIO.2 API جدیدی برای کار با فایل‌ها و دایرکتوری‌ها فراهم کرد.

### مفاهیم کلیدی:

**1. Path Interface:**
- جایگزین File class
- Cross-platform path handling
- More flexible and powerful

**2. Files Utility Class:**
- Static methods for file operations
- Better error handling
- Stream-based operations

### مثال عملی:

```java
import java.nio.file.*;
import java.nio.file.attribute.*;
import java.io.IOException;
import java.util.stream.Stream;

public class NIO2Example {
    
    public static void demonstratePathOperations() {
        // Creating paths
        Path path1 = Paths.get("C:", "Users", "John", "Documents");
        Path path2 = Paths.get("file.txt");
        Path absolutePath = path1.resolve(path2);
        
        System.out.println("Path 1: " + path1);
        System.out.println("Path 2: " + path2);
        System.out.println("Absolute path: " + absolutePath);
        
        // Path operations
        System.out.println("File name: " + absolutePath.getFileName());
        System.out.println("Parent: " + absolutePath.getParent());
        System.out.println("Root: " + absolutePath.getRoot());
    }
    
    public static void demonstrateFileOperations() {
        try {
            // Create directory
            Path dir = Paths.get("test_directory");
            Files.createDirectories(dir);
            System.out.println("Directory created: " + dir);
            
            // Create file
            Path file = dir.resolve("test.txt");
            Files.write(file, "Hello NIO.2!".getBytes());
            System.out.println("File created: " + file);
            
            // Read file
            byte[] content = Files.readAllBytes(file);
            System.out.println("File content: " + new String(content));
            
            // Copy file
            Path copyFile = dir.resolve("test_copy.txt");
            Files.copy(file, copyFile, StandardCopyOption.REPLACE_EXISTING);
            System.out.println("File copied to: " + copyFile);
            
            // List directory contents
            try (Stream<Path> paths = Files.list(dir)) {
                System.out.println("Directory contents:");
                paths.forEach(System.out::println);
            }
            
            // Delete files
            Files.delete(file);
            Files.delete(copyFile);
            Files.delete(dir);
            System.out.println("Files deleted");
            
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
    
    public static void demonstrateFileAttributes() {
        try {
            Path file = Paths.get("sample.txt");
            Files.write(file, "Sample content".getBytes());
            
            // Basic file attributes
            BasicFileAttributes attrs = Files.readAttributes(file, BasicFileAttributes.class);
            System.out.println("File size: " + attrs.size());
            System.out.println("Creation time: " + attrs.creationTime());
            System.out.println("Last modified: " + attrs.lastModifiedTime());
            System.out.println("Is directory: " + attrs.isDirectory());
            System.out.println("Is regular file: " + attrs.isRegularFile());
            
            // File permissions
            PosixFileAttributes posixAttrs = Files.readAttributes(file, PosixFileAttributes.class);
            System.out.println("Permissions: " + posixAttrs.permissions());
            System.out.println("Owner: " + posixAttrs.owner());
            System.out.println("Group: " + posixAttrs.group());
            
            Files.delete(file);
            
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
    
    public static void main(String[] args) {
        demonstratePathOperations();
        demonstrateFileOperations();
        demonstrateFileAttributes();
    }
}
```

### آنالوژی دنیای واقعی:
NIO.2 مانند داشتن یک سیستم مدیریت فایل پیشرفته است. به جای استفاده از ابزارهای ساده، ابزارهای قدرتمند و انعطاف‌پذیری دارید که می‌توانند با فایل‌ها و پوشه‌ها به صورت هوشمند کار کنند.

## 5.7 Fork/Join Framework

Fork/Join Framework برای parallel processing و divide-and-conquer algorithms طراحی شده است.

### مفاهیم کلیدی:

**1. Work Stealing:**
- Threads می‌توانند کارهای دیگر threads را بدزدند
- Better load balancing
- Efficient utilization of CPU cores

**2. RecursiveTask and RecursiveAction:**
- RecursiveTask: returns a result
- RecursiveAction: performs action without returning result

### مثال عملی:

```java
import java.util.concurrent.*;

public class ForkJoinExample {
    
    // RecursiveTask for calculating sum
    static class SumTask extends RecursiveTask<Long> {
        private final int[] array;
        private final int start;
        private final int end;
        private static final int THRESHOLD = 1000;
        
        public SumTask(int[] array, int start, int end) {
            this.array = array;
            this.start = start;
            this.end = end;
        }
        
        @Override
        protected Long compute() {
            if (end - start <= THRESHOLD) {
                // Base case: compute directly
                long sum = 0;
                for (int i = start; i < end; i++) {
                    sum += array[i];
                }
                return sum;
            } else {
                // Divide: split the task
                int mid = (start + end) / 2;
                SumTask leftTask = new SumTask(array, start, mid);
                SumTask rightTask = new SumTask(array, mid, end);
                
                // Fork: start left task asynchronously
                leftTask.fork();
                
                // Compute right task and wait for left
                long rightResult = rightTask.compute();
                long leftResult = leftTask.join();
                
                // Combine results
                return leftResult + rightResult;
            }
        }
    }
    
    // RecursiveAction for parallel array processing
    static class ArrayProcessor extends RecursiveAction {
        private final int[] array;
        private final int start;
        private final int end;
        private static final int THRESHOLD = 1000;
        
        public ArrayProcessor(int[] array, int start, int end) {
            this.array = array;
            this.start = start;
            this.end = end;
        }
        
        @Override
        protected void compute() {
            if (end - start <= THRESHOLD) {
                // Base case: process directly
                for (int i = start; i < end; i++) {
                    array[i] = array[i] * array[i]; // Square each element
                }
            } else {
                // Divide: split the task
                int mid = (start + end) / 2;
                ArrayProcessor leftTask = new ArrayProcessor(array, start, mid);
                ArrayProcessor rightTask = new ArrayProcessor(array, mid, end);
                
                // Fork both tasks
                invokeAll(leftTask, rightTask);
            }
        }
    }
    
    public static void main(String[] args) {
        // Create test array
        int[] array = new int[10000];
        for (int i = 0; i < array.length; i++) {
            array[i] = i + 1;
        }
        
        // Fork/Join pool
        ForkJoinPool pool = new ForkJoinPool();
        
        // Sum calculation
        System.out.println("=== Sum Calculation ===");
        long startTime = System.currentTimeMillis();
        
        SumTask sumTask = new SumTask(array, 0, array.length);
        long result = pool.invoke(sumTask);
        
        long endTime = System.currentTimeMillis();
        System.out.println("Sum: " + result);
        System.out.println("Time taken: " + (endTime - startTime) + " ms");
        
        // Array processing
        System.out.println("\n=== Array Processing ===");
        startTime = System.currentTimeMillis();
        
        ArrayProcessor processor = new ArrayProcessor(array, 0, array.length);
        pool.invoke(processor);
        
        endTime = System.currentTimeMillis();
        System.out.println("Array processed in: " + (endTime - startTime) + " ms");
        System.out.println("First 10 elements: ");
        for (int i = 0; i < 10; i++) {
            System.out.print(array[i] + " ");
        }
        System.out.println();
        
        pool.shutdown();
    }
}
```

### آنالوژی دنیای واقعی:
Fork/Join Framework مانند تقسیم کار در یک تیم بزرگ است. کار بزرگ به کارهای کوچک‌تر تقسیم می‌شود و هر عضو تیم روی بخشی کار می‌کند. اگر کسی زودتر کارش تمام شد، می‌تواند به دیگران کمک کند.