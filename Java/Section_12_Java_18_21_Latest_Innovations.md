# Section 12 - Java 18-21 - Latest Innovations

## 12.1 Pattern Matching for Switch (Preview)

Pattern Matching for Switch در Java 17 به صورت preview معرفی شد و در Java 21 به صورت نهایی درآمد. این ویژگی switch statements را با pattern matching ترکیب می‌کند.

### مفاهیم کلیدی:

**1. Type Patterns:**
- استفاده از pattern matching در switch
- Type checking و variable binding
- Exhaustive checking

**2. Guarded Patterns:**
- اضافه کردن conditions به patterns
- More precise matching
- Better control flow

### مثال عملی:

```java
public class PatternMatchingSwitch {
    public static void main(String[] args) {
        Object[] objects = {
            "Hello World",
            42,
            3.14,
            new int[]{1, 2, 3},
            new Person("احمد", 25),
            null
        };
        
        for (Object obj : objects) {
            processObject(obj);
        }
    }
    
    public static void processObject(Object obj) {
        String result = switch (obj) {
            case String s when s.length() > 5 -> "Long string: " + s;
            case String s -> "Short string: " + s;
            case Integer i when i > 0 -> "Positive integer: " + i;
            case Integer i -> "Non-positive integer: " + i;
            case Double d -> "Double: " + d;
            case int[] arr when arr.length > 0 -> "Non-empty array: " + arr.length + " elements";
            case int[] arr -> "Empty array";
            case Person p when p.getAge() >= 18 -> "Adult: " + p.getName();
            case Person p -> "Minor: " + p.getName();
            case null -> "Null object";
            default -> "Unknown type: " + obj.getClass().getSimpleName();
        };
        
        System.out.println("Result: " + result);
    }
}

class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public String getName() { return name; }
    public int getAge() { return age; }
}
```

### آنالوژی دنیای واقعی:
Pattern Matching for Switch مانند داشتن یک سیستم تشخیص هوشمند است که می‌تواند بر اساس نوع و ویژگی‌های مختلف، تصمیم‌گیری کند.

## 12.2 Virtual Threads (Preview)

Virtual Threads در Java 19 به صورت preview معرفی شد و در Java 21 به صورت نهایی درآمد. این ویژگی امکان ایجاد میلیون‌ها thread با overhead کم را فراهم می‌کند.

### مفاهیم کلیدی:

**1. Lightweight Threads:**
- Threads با overhead بسیار کم
- میلیون‌ها thread همزمان
- Managed by JVM

**2. Structured Concurrency:**
- Better thread management
- Scoped execution
- Improved error handling

### مثال عملی:

```java
import java.util.concurrent.*;

public class VirtualThreadsExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Virtual Threads Example ===");
        
        // Create virtual thread
        Thread virtualThread = Thread.ofVirtual().start(() -> {
            System.out.println("Virtual thread: " + Thread.currentThread());
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            System.out.println("Virtual thread completed");
        });
        
        // Wait for completion
        virtualThread.join();
        
        // Create multiple virtual threads
        System.out.println("\n=== Multiple Virtual Threads ===");
        ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
        
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Task " + taskId + " running on: " + Thread.currentThread());
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                System.out.println("Task " + taskId + " completed");
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
}
```

### آنالوژی دنیای واقعی:
Virtual Threads مانند داشتن یک سیستم مدیریت هوشمند است که می‌تواند میلیون‌ها کارگر مجازی را همزمان مدیریت کند.

## 12.3 Foreign Function & Memory API (Preview)

Foreign Function & Memory API در Java 17 به صورت preview معرفی شد و امکان تعامل با native code را فراهم می‌کند.

### مفاهیم کلیدی:

**1. Native Code Integration:**
- تعامل با C libraries
- Memory management
- Type safety

**2. Performance Benefits:**
- Direct memory access
- Zero-copy operations
- Low-level control

### مثال عملی:

```java
import jdk.incubator.foreign.*;

public class ForeignFunctionAPI {
    public static void main(String[] args) {
        // Example of using Foreign Function API
        // Note: This is a preview feature and requires special flags
        
        System.out.println("Foreign Function & Memory API is a preview feature");
        System.out.println("It allows interaction with native code");
        System.out.println("Requires --enable-preview flag to compile and run");
    }
}
```

### آنالوژی دنیای واقعی:
Foreign Function API مانند داشتن یک مترجم حرفه‌ای است که می‌تواند با زبان‌های مختلف صحبت کند.

## 12.4 Vector API (Preview)

Vector API در Java 17 به صورت preview معرفی شد و امکان استفاده از SIMD instructions را فراهم می‌کند.

### مفاهیم کلیدی:

**1. SIMD Operations:**
- Single Instruction, Multiple Data
- Parallel processing
- Performance optimization

**2. Vector Operations:**
- Element-wise operations
- Vectorized loops
- Hardware acceleration

### مثال عملی:

```java
import jdk.incubator.vector.*;

public class VectorAPI {
    public static void main(String[] args) {
        // Example of using Vector API
        // Note: This is a preview feature and requires special flags
        
        System.out.println("Vector API is a preview feature");
        System.out.println("It allows SIMD operations for better performance");
        System.out.println("Requires --enable-preview flag to compile and run");
    }
}
```

### آنالوژی دنیای واقعی:
Vector API مانند داشتن یک کارخانه تولیدی است که می‌تواند چندین محصول را همزمان تولید کند.

## 12.5 Scoped Values (Preview)

Scoped Values در Java 20 به صورت preview معرفی شد و راه بهتری برای انتقال داده‌ها بین threads فراهم می‌کند.

### مفاهیم کلیدی:

**1. Scoped Data:**
- انتقال داده‌ها در scope محدود
- Thread-safe
- Better than ThreadLocal

**2. Structured Concurrency:**
- Better thread management
- Scoped execution
- Improved error handling

### مثال عملی:

```java
import jdk.incubator.concurrent.*;

public class ScopedValuesExample {
    // Scoped value
    private static final ScopedValue<String> USER_NAME = ScopedValue.newInstance();
    
    public static void main(String[] args) {
        System.out.println("=== Scoped Values Example ===");
        
        // Set scoped value
        ScopedValue.runWhere(USER_NAME, "احمد محمدی", () -> {
            processUser();
        });
    }
    
    public static void processUser() {
        String userName = USER_NAME.get();
        System.out.println("Processing user: " + userName);
        
        // Nested scope
        ScopedValue.runWhere(USER_NAME, "فاطمه احمدی", () -> {
            processUser();
        });
    }
}
```

### آنالوژی دنیای واقعی:
Scoped Values مانند داشتن یک سیستم مدیریت اطلاعات هوشمند است که می‌تواند داده‌ها را در محدوده‌های مشخص مدیریت کند.

## 12.6 String Templates (Preview)

String Templates در Java 21 به صورت preview معرفی شد و راه بهتری برای string interpolation فراهم می‌کند.

### مفاهیم کلیدی:

**1. String Interpolation:**
- جایگزینی متغیرها در strings
- Type safety
- Better performance

**2. Template Processing:**
- Custom template processors
- Validation
- Security

### مثال عملی:

```java
import java.util.*;

public class StringTemplatesExample {
    public static void main(String[] args) {
        System.out.println("=== String Templates Example ===");
        
        String name = "احمد محمدی";
        int age = 25;
        String city = "تهران";
        
        // String template (preview feature)
        // Note: This requires --enable-preview flag
        
        System.out.println("String Templates is a preview feature");
        System.out.println("It allows string interpolation with type safety");
        System.out.println("Requires --enable-preview flag to compile and run");
        
        // Traditional string formatting
        String message = String.format("نام: %s, سن: %d, شهر: %s", name, age, city);
        System.out.println("Traditional: " + message);
    }
}
```

### آنالوژی دنیای واقعی:
String Templates مانند داشتن یک سیستم چاپ هوشمند است که می‌تواند متغیرها را به صورت خودکار در متن جایگزین کند.

## 12.7 Unnamed Classes & Instance Main Methods

Unnamed Classes & Instance Main Methods در Java 21 معرفی شد و راه ساده‌تری برای نوشتن برنامه‌های کوچک فراهم می‌کند.

### مفاهیم کلیدی:

**1. Unnamed Classes:**
- نیازی به تعریف کلاس نیست
- کد مستقیم در فایل
- ساده‌تر برای beginners

**2. Instance Main Methods:**
- متد main بدون static
- دسترسی به instance variables
- ساده‌تر برای OOP

### مثال عملی:

```java
// Unnamed class example
// This can be written directly in a .java file without class declaration

public class UnnamedClassesExample {
    // Instance variables
    private String name = "احمد محمدی";
    private int age = 25;
    
    // Instance main method
    public void main(String[] args) {
        System.out.println("=== Unnamed Classes & Instance Main Methods ===");
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
        
        // Can access instance variables
        greet();
    }
    
    public void greet() {
        System.out.println("Hello, " + name + "!");
    }
}
```

### آنالوژی دنیای واقعی:
Unnamed Classes مانند داشتن یک دفترچه یادداشت ساده است که می‌توانید مستقیماً در آن بنویسید بدون نیاز به قالب‌های پیچیده.