# Section 3 - Java 5 (J2SE 5.0) - The Generics Revolution

## 3.1 Generics & Type Safety

Generics یکی از مهم‌ترین ویژگی‌های Java 5 است که type safety را در compile time فراهم می‌کند. این ویژگی به شما امکان می‌دهد تا کلاس‌ها، interfaces و متدها را با پارامترهای نوع تعریف کنید.

### مفاهیم کلیدی:

**1. Type Parameters:**
- استفاده از angle brackets `<>` برای تعریف نوع
- Single letter type parameters (T, E, K, V)
- Bounded type parameters

**2. Type Safety:**
- جلوگیری از ClassCastException در runtime
- Compile-time type checking
- Better code documentation

### مثال عملی:

```java
// Generic Class
public class Box<T> {
    private T content;
    
    public void setContent(T content) {
        this.content = content;
    }
    
    public T getContent() {
        return content;
    }
}

// Generic Interface
public interface Comparable<T> {
    int compareTo(T other);
}

// Generic Method
public static <T> void printArray(T[] array) {
    for (T element : array) {
        System.out.println(element);
    }
}

// Usage
public class GenericsExample {
    public static void main(String[] args) {
        // Type-safe usage
        Box<String> stringBox = new Box<>();
        stringBox.setContent("Hello World");
        String content = stringBox.getContent(); // No casting needed
        
        Box<Integer> intBox = new Box<>();
        intBox.setContent(42);
        Integer number = intBox.getContent(); // Type safety guaranteed
        
        // Generic method usage
        String[] words = {"Java", "Generics", "Type Safety"};
        printArray(words);
        
        Integer[] numbers = {1, 2, 3, 4, 5};
        printArray(numbers);
    }
}
```

### آنالوژی دنیای واقعی:
Generics مانند برچسب‌گذاری جعبه‌ها است. اگر جعبه‌ای را با برچسب "کتاب" برچسب‌گذاری کنید، فقط کتاب‌ها را می‌توانید در آن قرار دهید و هنگام باز کردن، مطمئن هستید که کتاب دریافت خواهید کرد.

## 3.2 Enhanced for Loop (for-each)

Enhanced for loop که به for-each loop نیز معروف است، راه ساده‌تری برای iterate کردن بر روی collections و arrays فراهم می‌کند.

### ویژگی‌های کلیدی:

**1. Syntax ساده:**
- `for (Type variable : collection)`
- No index management needed
- Automatic iteration

**2. Type Safety:**
- Compile-time type checking
- No casting required
- Prevents IndexOutOfBoundsException

### مثال عملی:

```java
import java.util.*;

public class EnhancedForLoopExample {
    public static void main(String[] args) {
        // 1. Array iteration
        System.out.println("=== Array Iteration ===");
        int[] numbers = {1, 2, 3, 4, 5};
        
        // Traditional for loop
        System.out.println("Traditional for loop:");
        for (int i = 0; i < numbers.length; i++) {
            System.out.println("Index " + i + ": " + numbers[i]);
        }
        
        // Enhanced for loop
        System.out.println("\nEnhanced for loop:");
        for (int number : numbers) {
            System.out.println("Number: " + number);
        }
        
        // 2. Collection iteration
        System.out.println("\n=== Collection Iteration ===");
        List<String> fruits = Arrays.asList("سیب", "موز", "پرتقال", "انگور");
        
        // Enhanced for loop with collections
        for (String fruit : fruits) {
            System.out.println("میوه: " + fruit);
        }
        
        // 3. Set iteration
        System.out.println("\n=== Set Iteration ===");
        Set<String> colors = new HashSet<>();
        colors.add("قرمز");
        colors.add("سبز");
        colors.add("آبی");
        
        for (String color : colors) {
            System.out.println("رنگ: " + color);
        }
        
        // 4. Map iteration
        System.out.println("\n=== Map Iteration ===");
        Map<String, Integer> studentGrades = new HashMap<>();
        studentGrades.put("احمد", 18);
        studentGrades.put("فاطمه", 19);
        studentGrades.put("علی", 17);
        
        for (Map.Entry<String, Integer> entry : studentGrades.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
    }
}
```

### مزایای Enhanced for Loop:

```java
public class EnhancedForLoopAdvantages {
    public static void main(String[] args) {
        List<String> items = Arrays.asList("آیتم1", "آیتم2", "آیتم3");
        
        // 1. Cleaner code
        System.out.println("=== Cleaner Code ===");
        for (String item : items) {
            System.out.println(item);
        }
        
        // 2. No index management
        System.out.println("\n=== No Index Management ===");
        // No need to worry about array bounds
        for (String item : items) {
            if (item.startsWith("آیتم")) {
                System.out.println("Found: " + item);
            }
        }
        
        // 3. Type safety
        System.out.println("\n=== Type Safety ===");
        List<Object> mixedList = Arrays.asList("String", 42, true);
        for (Object obj : mixedList) {
            if (obj instanceof String) {
                String str = (String) obj; // Safe casting
                System.out.println("String: " + str);
            }
        }
    }
}
```

### آنالوژی دنیای واقعی:
Enhanced for loop مانند راه رفتن در یک صف است. شما نیازی به شمارش افراد یا نگرانی در مورد ایندکس ندارید - فقط از ابتدا تا انتها راه می‌روید و هر شخص را می‌بینید.

## 3.3 Autoboxing & Unboxing

Autoboxing و Unboxing ویژگی‌هایی هستند که به صورت خودکار بین primitive types و wrapper classes تبدیل انجام می‌دهند.

### مفاهیم کلیدی:

**1. Autoboxing:**
- تبدیل خودکار primitive type به wrapper class
- `int` → `Integer`
- `double` → `Double`

**2. Unboxing:**
- تبدیل خودکار wrapper class به primitive type
- `Integer` → `int`
- `Double` → `double`

### مثال عملی:

```java
import java.util.*;

public class AutoboxingUnboxingExample {
    public static void main(String[] args) {
        // 1. Autoboxing examples
        System.out.println("=== Autoboxing Examples ===");
        
        // Automatic conversion from int to Integer
        Integer intObj = 42; // Autoboxing
        System.out.println("Integer object: " + intObj);
        
        // Automatic conversion from double to Double
        Double doubleObj = 3.14; // Autoboxing
        System.out.println("Double object: " + doubleObj);
        
        // 2. Unboxing examples
        System.out.println("\n=== Unboxing Examples ===");
        
        Integer intWrapper = 100;
        int primitiveInt = intWrapper; // Unboxing
        System.out.println("Primitive int: " + primitiveInt);
        
        Double doubleWrapper = 2.718;
        double primitiveDouble = doubleWrapper; // Unboxing
        System.out.println("Primitive double: " + primitiveDouble);
        
        // 3. Collections with autoboxing
        System.out.println("\n=== Collections with Autoboxing ===");
        
        List<Integer> numbers = new ArrayList<>();
        numbers.add(1);    // Autoboxing: int -> Integer
        numbers.add(2);    // Autoboxing: int -> Integer
        numbers.add(3);    // Autoboxing: int -> Integer
        
        for (int num : numbers) { // Unboxing: Integer -> int
            System.out.println("Number: " + num);
        }
        
        // 4. Method calls
        System.out.println("\n=== Method Calls ===");
        
        // Autoboxing in method calls
        printInteger(42); // int -> Integer
        printDouble(3.14); // double -> Double
        
        // Unboxing in method calls
        Integer intVal = 100;
        printPrimitiveInt(intVal); // Integer -> int
    }
    
    public static void printInteger(Integer value) {
        System.out.println("Integer value: " + value);
    }
    
    public static void printDouble(Double value) {
        System.out.println("Double value: " + value);
    }
    
    public static void printPrimitiveInt(int value) {
        System.out.println("Primitive int: " + value);
    }
}
```

### مزایا و نکات مهم:

```java
public class AutoboxingBestPractices {
    public static void main(String[] args) {
        // 1. Performance considerations
        System.out.println("=== Performance Considerations ===");
        
        long startTime = System.currentTimeMillis();
        
        // Using autoboxing (creates objects)
        for (int i = 0; i < 1000000; i++) {
            Integer obj = i; // Creates new Integer object each time
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Autoboxing time: " + (endTime - startTime) + " ms");
        
        // Using primitives (no objects created)
        startTime = System.currentTimeMillis();
        
        for (int i = 0; i < 1000000; i++) {
            int primitive = i; // No object creation
        }
        
        endTime = System.currentTimeMillis();
        System.out.println("Primitive time: " + (endTime - startTime) + " ms");
        
        // 2. Null pointer exceptions
        System.out.println("\n=== Null Pointer Exceptions ===");
        
        Integer nullInteger = null;
        try {
            int value = nullInteger; // NullPointerException during unboxing
        } catch (NullPointerException e) {
            System.out.println("NullPointerException: " + e.getMessage());
        }
        
        // 3. Comparison gotchas
        System.out.println("\n=== Comparison Gotchas ===");
        
        Integer a = 127;
        Integer b = 127;
        System.out.println("a == b (127): " + (a == b)); // true (cached)
        
        Integer c = 128;
        Integer d = 128;
        System.out.println("c == d (128): " + (c == d)); // false (not cached)
        
        // Always use .equals() for wrapper classes
        System.out.println("c.equals(d): " + c.equals(d)); // true
    }
}
```

### آنالوژی دنیای واقعی:
Autoboxing و Unboxing مانند تبدیل خودکار بین پول نقد و چک است. وقتی می‌خواهید پول نقد را در کیف پول قرار دهید، به صورت خودکار به چک تبدیل می‌شود (autoboxing). وقتی می‌خواهید از چک استفاده کنید، به صورت خودکار به پول نقد تبدیل می‌شود (unboxing).

## 3.4 Enumerations (Enums)

Enums در Java 5 معرفی شدند و راه قدرتمندی برای تعریف مجموعه‌ای از مقادیر ثابت فراهم می‌کنند.

### مفاهیم کلیدی:

**1. Type Safety:**
- Compile-time checking
- No invalid values
- Better than constants

**2. Rich Features:**
- Methods and fields
- Constructors
- Implement interfaces

### مثال عملی:

```java
// Basic enum
public enum Day {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}

// Enum with methods and fields
public enum Planet {
    MERCURY(3.303e+23, 2.4397e6),
    VENUS(4.869e+24, 6.0518e6),
    EARTH(5.976e+24, 6.37814e6),
    MARS(6.421e+23, 3.3972e6),
    JUPITER(1.9e+27, 7.1492e7),
    SATURN(5.688e+26, 6.0268e7),
    URANUS(8.686e+25, 2.5559e7),
    NEPTUNE(1.024e+26, 2.4746e7);
    
    private final double mass;   // in kilograms
    private final double radius; // in meters
    
    Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }
    
    public double getMass() { return mass; }
    public double getRadius() { return radius; }
    
    // Universal gravitational constant (m3 kg-1 s-2)
    public static final double G = 6.67300E-11;
    
    public double surfaceGravity() {
        return G * mass / (radius * radius);
    }
    
    public double surfaceWeight(double otherMass) {
        return otherMass * surfaceGravity();
    }
}

// Enum with abstract methods
public enum Operation {
    PLUS("+") {
        public double apply(double x, double y) { return x + y; }
    },
    MINUS("-") {
        public double apply(double x, double y) { return x - y; }
    },
    TIMES("*") {
        public double apply(double x, double y) { return x * y; }
    },
    DIVIDE("/") {
        public double apply(double x, double y) { return x / y; }
    };
    
    private final String symbol;
    
    Operation(String symbol) {
        this.symbol = symbol;
    }
    
    public abstract double apply(double x, double y);
    
    @Override
    public String toString() {
        return symbol;
    }
}

// Usage example
public class EnumExample {
    public static void main(String[] args) {
        // 1. Basic enum usage
        System.out.println("=== Basic Enum Usage ===");
        Day today = Day.MONDAY;
        System.out.println("Today is: " + today);
        
        // Switch statement with enum
        switch (today) {
            case MONDAY:
                System.out.println("Start of work week");
                break;
            case FRIDAY:
                System.out.println("TGIF!");
                break;
            case SATURDAY:
            case SUNDAY:
                System.out.println("Weekend!");
                break;
            default:
                System.out.println("Midweek");
        }
        
        // 2. Enum with methods
        System.out.println("\n=== Enum with Methods ===");
        Planet earth = Planet.EARTH;
        double earthWeight = 175; // pounds
        double mass = earthWeight / earth.surfaceGravity();
        
        for (Planet p : Planet.values()) {
            System.out.printf("Weight on %s is %f%n", p, p.surfaceWeight(mass));
        }
        
        // 3. Enum with abstract methods
        System.out.println("\n=== Enum with Abstract Methods ===");
        double x = 2.0;
        double y = 4.0;
        
        for (Operation op : Operation.values()) {
            System.out.printf("%f %s %f = %f%n", x, op, y, op.apply(x, y));
        }
        
        // 4. Enum methods
        System.out.println("\n=== Enum Methods ===");
        System.out.println("All days: " + Arrays.toString(Day.values()));
        System.out.println("Monday ordinal: " + Day.MONDAY.ordinal());
        System.out.println("Day from string: " + Day.valueOf("TUESDAY"));
    }
}
```

### آنالوژی دنیای واقعی:
Enums مانند تعریف رنگ‌های ترافیک هستند. فقط سه رنگ معتبر وجود دارد: قرمز، زرد، و سبز. نمی‌توانید رنگ "آبی" را برای چراغ راهنمایی تعریف کنید، و هر رنگ معنای خاصی دارد.

## 3.5 Varargs (Variable Arguments)

Varargs امکان ارسال تعداد متغیری از آرگومان‌ها به یک متد را فراهم می‌کند.

### مفاهیم کلیدی:

**1. Syntax:**
- `Type... parameterName`
- Must be the last parameter
- Treated as array

**2. Benefits:**
- Flexible method calls
- Cleaner code
- No need for array creation

### مثال عملی:

```java
public class VarargsExample {
    
    // Basic varargs method
    public static void printNumbers(int... numbers) {
        System.out.println("Number of arguments: " + numbers.length);
        for (int num : numbers) {
            System.out.print(num + " ");
        }
        System.out.println();
    }
    
    // Varargs with other parameters
    public static void printMessage(String message, String... names) {
        System.out.print(message + ": ");
        for (String name : names) {
            System.out.print(name + " ");
        }
        System.out.println();
    }
    
    // Generic varargs method
    public static <T> void printArray(T... items) {
        for (T item : items) {
            System.out.print(item + " ");
        }
        System.out.println();
    }
    
    // Varargs with overloaded methods
    public static void method(String s) {
        System.out.println("Single string: " + s);
    }
    
    public static void method(String s, String... strings) {
        System.out.println("String with varargs: " + s);
        for (String str : strings) {
            System.out.print(str + " ");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        // 1. Basic varargs usage
        System.out.println("=== Basic Varargs Usage ===");
        printNumbers(1, 2, 3, 4, 5);
        printNumbers(10, 20);
        printNumbers(); // No arguments
        
        // 2. Varargs with other parameters
        System.out.println("\n=== Varargs with Other Parameters ===");
        printMessage("Hello", "احمد", "فاطمه", "علی");
        printMessage("Welcome", "Java", "Programming");
        printMessage("Hi"); // No varargs
        
        // 3. Generic varargs
        System.out.println("\n=== Generic Varargs ===");
        printArray("Java", "Python", "C++");
        printArray(1, 2, 3, 4, 5);
        printArray(3.14, 2.718, 1.414);
        
        // 4. Method overloading with varargs
        System.out.println("\n=== Method Overloading ===");
        method("Single");
        method("First", "Second", "Third");
        
        // 5. Array as varargs
        System.out.println("\n=== Array as Varargs ===");
        int[] numbers = {10, 20, 30, 40};
        printNumbers(numbers); // Array passed as varargs
        
        // 6. Null handling
        System.out.println("\n=== Null Handling ===");
        printMessage("Test", (String[]) null); // Explicit null
    }
}
```

### نکات مهم Varargs:

```java
public class VarargsBestPractices {
    
    // Good: Varargs as last parameter
    public static void goodMethod(String prefix, int... numbers) {
        System.out.print(prefix + ": ");
        for (int num : numbers) {
            System.out.print(num + " ");
        }
        System.out.println();
    }
    
    // Bad: Varargs not as last parameter (won't compile)
    // public static void badMethod(int... numbers, String suffix) {
    //     // This won't compile
    // }
    
    // Performance consideration
    public static void performanceTest() {
        long startTime = System.currentTimeMillis();
        
        // Using varargs (creates array each time)
        for (int i = 0; i < 1000000; i++) {
            printNumbers(1, 2, 3, 4, 5);
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Varargs time: " + (endTime - startTime) + " ms");
        
        // Using array (no array creation)
        int[] numbers = {1, 2, 3, 4, 5};
        startTime = System.currentTimeMillis();
        
        for (int i = 0; i < 1000000; i++) {
            printNumbers(numbers);
        }
        
        endTime = System.currentTimeMillis();
        System.out.println("Array time: " + (endTime - startTime) + " ms");
    }
    
    public static void printNumbers(int... numbers) {
        // Method implementation
    }
    
    public static void main(String[] args) {
        goodMethod("Numbers", 1, 2, 3, 4, 5);
        performanceTest();
    }
}
```

### آنالوژی دنیای واقعی:
Varargs مانند سفارش غذا در رستوران است. می‌توانید بگویید "یک پیتزا" یا "یک پیتزا با پنیر اضافی و قارچ" یا "یک پیتزا با تمام مواد اضافی". متد رستوران (پیتزا) می‌تواند هر تعداد مواد اضافی را بپذیرد.

## 3.6 Annotations Introduction

Annotations در Java 5 معرفی شدند و راه قدرتمندی برای اضافه کردن metadata به کد فراهم می‌کنند.

### مفاهیم کلیدی:

**1. Built-in Annotations:**
- `@Override`
- `@Deprecated`
- `@SuppressWarnings`

**2. Custom Annotations:**
- `@interface` keyword
- Retention policies
- Target elements

### مثال عملی:

```java
import java.lang.annotation.*;
import java.lang.reflect.Method;

// Custom annotation
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@interface TestMethod {
    String description() default "Test method";
    int priority() default 0;
}

// Custom annotation with multiple targets
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE, ElementType.METHOD, ElementType.FIELD})
@interface Author {
    String name();
    String date();
    String version() default "1.0";
}

// Using annotations
@Author(name = "احمد محمدی", date = "2024-01-01", version = "2.0")
public class AnnotationExample {
    
    @Author(name = "احمد محمدی", date = "2024-01-01")
    private String field;
    
    @Override
    public String toString() {
        return "AnnotationExample";
    }
    
    @Deprecated
    public void oldMethod() {
        System.out.println("This method is deprecated");
    }
    
    @SuppressWarnings("unchecked")
    public void suppressWarnings() {
        // This would normally generate a warning
        java.util.List list = new java.util.ArrayList();
        list.add("item");
    }
    
    @TestMethod(description = "Test addition method", priority = 1)
    public int add(int a, int b) {
        return a + b;
    }
    
    @TestMethod(description = "Test multiplication method", priority = 2)
    public int multiply(int a, int b) {
        return a * b;
    }
    
    // Method to process annotations
    public static void processAnnotations() {
        Class<?> clazz = AnnotationExample.class;
        
        // Process class-level annotations
        if (clazz.isAnnotationPresent(Author.class)) {
            Author author = clazz.getAnnotation(Author.class);
            System.out.println("Class Author: " + author.name());
            System.out.println("Date: " + author.date());
            System.out.println("Version: " + author.version());
        }
        
        // Process method-level annotations
        Method[] methods = clazz.getDeclaredMethods();
        for (Method method : methods) {
            if (method.isAnnotationPresent(TestMethod.class)) {
                TestMethod testMethod = method.getAnnotation(TestMethod.class);
                System.out.println("Method: " + method.getName());
                System.out.println("Description: " + testMethod.description());
                System.out.println("Priority: " + testMethod.priority());
            }
        }
    }
    
    public static void main(String[] args) {
        System.out.println("=== Annotation Examples ===");
        
        // 1. Built-in annotations
        AnnotationExample example = new AnnotationExample();
        example.oldMethod(); // Deprecated method
        
        // 2. Custom annotations
        processAnnotations();
        
        // 3. Runtime annotation processing
        System.out.println("\n=== Runtime Processing ===");
        try {
            Method method = AnnotationExample.class.getMethod("add", int.class, int.class);
            if (method.isAnnotationPresent(TestMethod.class)) {
                TestMethod annotation = method.getAnnotation(TestMethod.class);
                System.out.println("Found test method: " + annotation.description());
            }
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        }
    }
}
```

### آنالوژی دنیای واقعی:
Annotations مانند برچسب‌های روی بسته‌ها هستند. برچسب "شکننده" روی بسته به شما می‌گوید که باید مراقب باشید. برچسب "اولویت بالا" به شما می‌گوید که باید زودتر تحویل دهید. در کد، annotations اطلاعات مهمی درباره کد به کامپایلر و runtime می‌دهند.

## 3.7 Concurrency Utilities (java.util.concurrent)

Java 5 مجموعه‌ای از utilities قدرتمند برای برنامه‌نویسی concurrent معرفی کرد.

### مفاهیم کلیدی:

**1. Executor Framework:**
- Thread pool management
- Task execution
- Lifecycle management

**2. Concurrent Collections:**
- Thread-safe collections
- High-performance alternatives
- Atomic operations

**3. Synchronization Utilities:**
- Locks, Semaphores
- CountDownLatch, CyclicBarrier
- Atomic variables

### مثال عملی:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

public class ConcurrencyUtilitiesExample {
    
    // Atomic counter
    private static final AtomicInteger counter = new AtomicInteger(0);
    
    // Reentrant lock
    private static final ReentrantLock lock = new ReentrantLock();
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Concurrency Utilities Examples ===");
        
        // 1. Executor Framework
        demonstrateExecutorFramework();
        
        // 2. Concurrent Collections
        demonstrateConcurrentCollections();
        
        // 3. Synchronization Utilities
        demonstrateSynchronizationUtilities();
        
        // 4. Atomic Variables
        demonstrateAtomicVariables();
    }
    
    public static void demonstrateExecutorFramework() throws InterruptedException {
        System.out.println("\n=== Executor Framework ===");
        
        // Create thread pool
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Submit tasks
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Task " + taskId + " executed by " + 
                    Thread.currentThread().getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Shutdown executor
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
    }
    
    public static void demonstrateConcurrentCollections() {
        System.out.println("\n=== Concurrent Collections ===");
        
        // ConcurrentHashMap
        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
        
        // Multiple threads adding to map
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        for (int i = 0; i < 10; i++) {
            final int value = i;
            executor.submit(() -> {
                map.put("key" + value, value);
                System.out.println("Added: key" + value + " = " + value);
            });
        }
        
        executor.shutdown();
        
        // ConcurrentLinkedQueue
        ConcurrentLinkedQueue<String> queue = new ConcurrentLinkedQueue<>();
        queue.offer("First");
        queue.offer("Second");
        queue.offer("Third");
        
        System.out.println("Queue size: " + queue.size());
        System.out.println("Polled: " + queue.poll());
        System.out.println("Queue size after poll: " + queue.size());
    }
    
    public static void demonstrateSynchronizationUtilities() throws InterruptedException {
        System.out.println("\n=== Synchronization Utilities ===");
        
        // CountDownLatch
        CountDownLatch latch = new CountDownLatch(3);
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        for (int i = 0; i < 3; i++) {
            final int workerId = i;
            executor.submit(() -> {
                System.out.println("Worker " + workerId + " starting");
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                System.out.println("Worker " + workerId + " finished");
                latch.countDown();
            });
        }
        
        System.out.println("Waiting for all workers to finish...");
        latch.await();
        System.out.println("All workers finished!");
        
        executor.shutdown();
        
        // Semaphore
        Semaphore semaphore = new Semaphore(2); // Allow 2 concurrent access
        
        System.out.println("\n=== Semaphore Example ===");
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            new Thread(() -> {
                try {
                    semaphore.acquire();
                    System.out.println("Task " + taskId + " acquired semaphore");
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    semaphore.release();
                    System.out.println("Task " + taskId + " released semaphore");
                }
            }).start();
        }
    }
    
    public static void demonstrateAtomicVariables() {
        System.out.println("\n=== Atomic Variables ===");
        
        // Multiple threads incrementing counter
        ExecutorService executor = Executors.newFixedThreadPool(5);
        
        for (int i = 0; i < 10; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    counter.incrementAndGet();
                }
            });
        }
        
        executor.shutdown();
        
        try {
            executor.awaitTermination(5, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        System.out.println("Final counter value: " + counter.get());
        
        // Atomic operations
        AtomicInteger atomicInt = new AtomicInteger(10);
        
        System.out.println("Initial value: " + atomicInt.get());
        System.out.println("Increment and get: " + atomicInt.incrementAndGet());
        System.out.println("Add and get: " + atomicInt.addAndGet(5));
        System.out.println("Compare and set: " + atomicInt.compareAndSet(16, 20));
        System.out.println("Final value: " + atomicInt.get());
    }
}
```

### آنالوژی دنیای واقعی:
Concurrency Utilities مانند مدیریت یک رستوران شلوغ است. Executor Framework مانند مدیر رستوران است که کارگران (threads) را مدیریت می‌کند. Concurrent Collections مانند صندوق‌های امن هستند که چندین نفر می‌توانند همزمان از آن‌ها استفاده کنند. Synchronization Utilities مانند سیستم نوبت‌دهی هستند که اطمینان می‌دهند همه مشتریان به ترتیب سرویس شوند.