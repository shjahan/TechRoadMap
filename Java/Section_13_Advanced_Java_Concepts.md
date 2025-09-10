# Section 13 - Advanced Java Concepts

## 13.1 JVM Internals & Bytecode

JVM Internals & Bytecode یکی از مهم‌ترین مفاهیم پیشرفته جاوا است که درک عمیق‌تری از نحوه کارکرد Java فراهم می‌کند.

### مفاهیم کلیدی:

**1. JVM Architecture:**
- Class Loader Subsystem
- Runtime Data Areas
- Execution Engine
- Native Method Interface

**2. Bytecode:**
- Intermediate representation
- Platform-independent
- JIT compilation

**3. Memory Management:**
- Heap memory
- Stack memory
- Method area
- PC registers

### مثال عملی:

```java
public class JVMInternalsExample {
    private static final int CONSTANT_VALUE = 42;
    private String instanceField = "Hello";
    
    public static void main(String[] args) {
        JVMInternalsExample example = new JVMInternalsExample();
        example.demonstrateJVMConcepts();
    }
    
    public void demonstrateJVMConcepts() {
        // Local variables (stored in stack)
        int localVar = 10;
        String localString = "World";
        
        // Object creation (stored in heap)
        Object obj = new Object();
        
        // Method calls
        int result = calculateSum(localVar, CONSTANT_VALUE);
        
        System.out.println("Result: " + result);
        System.out.println("Instance field: " + instanceField);
    }
    
    public int calculateSum(int a, int b) {
        return a + b;
    }
}
```

### Bytecode Analysis:

```java
// Compile with: javac -g JVMInternalsExample.java
// View bytecode with: javap -c JVMInternalsExample

// Example bytecode for calculateSum method:
// 0: iload_1        // Load first parameter
// 1: iload_2        // Load second parameter
// 2: iadd           // Add them
// 3: ireturn        // Return result
```

### آنالوژی دنیای واقعی:
JVM مانند یک کارخانه تولیدی است که:
- **Class Loader:** مانند سیستم تامین مواد اولیه
- **Runtime Data Areas:** مانند انبارهای مختلف برای ذخیره مواد
- **Execution Engine:** مانند ماشین‌آلات تولید
- **Bytecode:** مانند دستورالعمل‌های تولید

## 13.2 Memory Management & Garbage Collection Tuning

Memory Management & Garbage Collection Tuning یکی از مهم‌ترین جنبه‌های بهینه‌سازی Java applications است.

### مفاهیم کلیدی:

**1. Heap Memory:**
- Young Generation (Eden, Survivor spaces)
- Old Generation (Tenured space)
- Metaspace (Class metadata)

**2. Garbage Collectors:**
- Serial GC
- Parallel GC
- G1 GC
- ZGC
- Shenandoah GC

**3. Tuning Parameters:**
- Heap size settings
- GC algorithm selection
- Tuning parameters

### مثال عملی:

```java
public class MemoryManagementExample {
    private static final int MEGABYTE = 1024 * 1024;
    
    public static void main(String[] args) {
        System.out.println("=== Memory Management Example ===");
        
        // Display memory information
        displayMemoryInfo();
        
        // Demonstrate memory allocation
        demonstrateMemoryAllocation();
        
        // Demonstrate garbage collection
        demonstrateGarbageCollection();
    }
    
    public static void displayMemoryInfo() {
        Runtime runtime = Runtime.getRuntime();
        
        long totalMemory = runtime.totalMemory() / MEGABYTE;
        long freeMemory = runtime.freeMemory() / MEGABYTE;
        long usedMemory = totalMemory - freeMemory;
        long maxMemory = runtime.maxMemory() / MEGABYTE;
        
        System.out.println("Total Memory: " + totalMemory + " MB");
        System.out.println("Free Memory: " + freeMemory + " MB");
        System.out.println("Used Memory: " + usedMemory + " MB");
        System.out.println("Max Memory: " + maxMemory + " MB");
    }
    
    public static void demonstrateMemoryAllocation() {
        System.out.println("\n=== Memory Allocation ===");
        
        // Create large objects
        for (int i = 0; i < 1000; i++) {
            String largeString = new String("Large string " + i + " " + 
                "x".repeat(1000));
            // Object will be eligible for GC after this iteration
        }
        
        System.out.println("1000 objects created");
        displayMemoryInfo();
    }
    
    public static void demonstrateGarbageCollection() {
        System.out.println("\n=== Garbage Collection ===");
        
        // Create objects
        for (int i = 0; i < 10000; i++) {
            new String("Object " + i);
        }
        
        System.out.println("Before GC:");
        displayMemoryInfo();
        
        // Suggest garbage collection
        System.gc();
        
        // Wait a bit for GC to complete
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        System.out.println("After GC:");
        displayMemoryInfo();
    }
}
```

### GC Tuning Examples:

```bash
# Basic GC tuning
java -Xms512m -Xmx2g -XX:+UseG1GC MyApplication

# G1 GC tuning
java -Xms1g -Xmx4g -XX:+UseG1GC -XX:MaxGCPauseMillis=200 MyApplication

# ZGC tuning
java -Xms2g -Xmx8g -XX:+UnlockExperimentalVMOptions -XX:+UseZGC MyApplication

# GC logging
java -Xms1g -Xmx2g -XX:+UseG1GC -Xlog:gc*:gc.log MyApplication
```

### آنالوژی دنیای واقعی:
Memory Management مانند مدیریت یک انبار بزرگ است:
- **Heap:** مانند انبار اصلی که کالاها (objects) در آن ذخیره می‌شوند
- **Garbage Collection:** مانند سیستم نظافت که کالاهای غیرضروری را حذف می‌کند
- **Tuning:** مانند بهینه‌سازی سیستم انبارداری برای کارایی بهتر

## 13.3 Performance Optimization Techniques

Performance Optimization Techniques مجموعه‌ای از روش‌ها برای بهبود عملکرد Java applications است.

### مفاهیم کلیدی:

**1. Code Optimization:**
- Algorithm optimization
- Data structure selection
- Loop optimization
- Method inlining

**2. Memory Optimization:**
- Object pooling
- String optimization
- Collection optimization
- Memory leak prevention

**3. JVM Optimization:**
- JIT compilation
- HotSpot optimization
- Profiling
- Benchmarking

### مثال عملی:

```java
public class PerformanceOptimizationExample {
    private static final int ITERATIONS = 1000000;
    
    public static void main(String[] args) {
        System.out.println("=== Performance Optimization Examples ===");
        
        // 1. String concatenation optimization
        demonstrateStringOptimization();
        
        // 2. Collection optimization
        demonstrateCollectionOptimization();
        
        // 3. Loop optimization
        demonstrateLoopOptimization();
        
        // 4. Algorithm optimization
        demonstrateAlgorithmOptimization();
    }
    
    public static void demonstrateStringOptimization() {
        System.out.println("\n=== String Optimization ===");
        
        // Bad: String concatenation in loop
        long startTime = System.currentTimeMillis();
        String badResult = "";
        for (int i = 0; i < 10000; i++) {
            badResult += "item" + i; // Creates many temporary objects
        }
        long endTime = System.currentTimeMillis();
        System.out.println("Bad approach time: " + (endTime - startTime) + " ms");
        
        // Good: StringBuilder
        startTime = System.currentTimeMillis();
        StringBuilder goodResult = new StringBuilder();
        for (int i = 0; i < 10000; i++) {
            goodResult.append("item").append(i);
        }
        endTime = System.currentTimeMillis();
        System.out.println("Good approach time: " + (endTime - startTime) + " ms");
    }
    
    public static void demonstrateCollectionOptimization() {
        System.out.println("\n=== Collection Optimization ===");
        
        // Bad: Default capacity
        long startTime = System.currentTimeMillis();
        java.util.List<String> badList = new java.util.ArrayList<>();
        for (int i = 0; i < 100000; i++) {
            badList.add("item" + i);
        }
        long endTime = System.currentTimeMillis();
        System.out.println("Bad list time: " + (endTime - startTime) + " ms");
        
        // Good: Pre-allocate capacity
        startTime = System.currentTimeMillis();
        java.util.List<String> goodList = new java.util.ArrayList<>(100000);
        for (int i = 0; i < 100000; i++) {
            goodList.add("item" + i);
        }
        endTime = System.currentTimeMillis();
        System.out.println("Good list time: " + (endTime - startTime) + " ms");
    }
    
    public static void demonstrateLoopOptimization() {
        System.out.println("\n=== Loop Optimization ===");
        
        int[] array = new int[1000000];
        for (int i = 0; i < array.length; i++) {
            array[i] = i;
        }
        
        // Bad: Method call in loop condition
        long startTime = System.currentTimeMillis();
        int sum1 = 0;
        for (int i = 0; i < array.length; i++) { // array.length called each iteration
            sum1 += array[i];
        }
        long endTime = System.currentTimeMillis();
        System.out.println("Bad loop time: " + (endTime - startTime) + " ms");
        
        // Good: Cache array length
        startTime = System.currentTimeMillis();
        int sum2 = 0;
        int length = array.length; // Cache length
        for (int i = 0; i < length; i++) {
            sum2 += array[i];
        }
        endTime = System.currentTimeMillis();
        System.out.println("Good loop time: " + (endTime - startTime) + " ms");
    }
    
    public static void demonstrateAlgorithmOptimization() {
        System.out.println("\n=== Algorithm Optimization ===");
        
        int[] numbers = {5, 2, 8, 1, 9, 3, 7, 4, 6};
        
        // Bad: O(n²) bubble sort
        long startTime = System.currentTimeMillis();
        int[] badArray = numbers.clone();
        bubbleSort(badArray);
        long endTime = System.currentTimeMillis();
        System.out.println("Bubble sort time: " + (endTime - startTime) + " ms");
        
        // Good: O(n log n) quick sort
        startTime = System.currentTimeMillis();
        int[] goodArray = numbers.clone();
        java.util.Arrays.sort(goodArray);
        endTime = System.currentTimeMillis();
        System.out.println("Quick sort time: " + (endTime - startTime) + " ms");
    }
    
    public static void bubbleSort(int[] array) {
        int n = array.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (array[j] > array[j + 1]) {
                    int temp = array[j];
                    array[j] = array[j + 1];
                    array[j + 1] = temp;
                }
            }
        }
    }
}
```

### آنالوژی دنیای واقعی:
Performance Optimization مانند بهینه‌سازی یک کارخانه تولیدی است:
- **Code Optimization:** مانند بهبود فرآیندهای تولید
- **Memory Optimization:** مانند بهینه‌سازی سیستم انبارداری
- **JVM Optimization:** مانند تنظیم ماشین‌آلات برای کارایی بهتر

## 13.4 JIT Compilation & HotSpot

JIT Compilation & HotSpot یکی از مهم‌ترین جنبه‌های عملکرد Java است که کد را در runtime بهینه‌سازی می‌کند.

### مفاهیم کلیدی:

**1. JIT Compilation:**
- Just-In-Time compilation
- Bytecode to native code
- Runtime optimization

**2. HotSpot JVM:**
- Adaptive optimization
- Method profiling
- Inline caching

**3. Optimization Levels:**
- C1 compiler (client)
- C2 compiler (server)
- Tiered compilation

### مثال عملی:

```java
public class JITCompilationExample {
    private static final int ITERATIONS = 1000000;
    
    public static void main(String[] args) {
        System.out.println("=== JIT Compilation Example ===");
        
        // Warm up JIT
        warmUpJIT();
        
        // Measure performance after JIT optimization
        measurePerformance();
    }
    
    public static void warmUpJIT() {
        System.out.println("Warming up JIT...");
        
        // Execute method multiple times to trigger JIT compilation
        for (int i = 0; i < 10000; i++) {
            performCalculation(i);
        }
        
        System.out.println("JIT warm-up completed");
    }
    
    public static void measurePerformance() {
        System.out.println("\nMeasuring performance...");
        
        long startTime = System.nanoTime();
        
        for (int i = 0; i < ITERATIONS; i++) {
            performCalculation(i);
        }
        
        long endTime = System.nanoTime();
        long duration = endTime - startTime;
        
        System.out.println("Total time: " + duration + " ns");
        System.out.println("Average time per iteration: " + (duration / ITERATIONS) + " ns");
    }
    
    public static int performCalculation(int value) {
        // Simple calculation that can be optimized by JIT
        return value * value + value * 2 + 1;
    }
}
```

### JIT Tuning Examples:

```bash
# Enable JIT compilation logging
java -XX:+PrintCompilation MyApplication

# Enable detailed JIT logging
java -XX:+PrintCompilation -XX:+PrintInlining MyApplication

# Set compilation threshold
java -XX:CompileThreshold=1000 MyApplication

# Enable tiered compilation
java -XX:+TieredCompilation MyApplication
```

### آنالوژی دنیای واقعی:
JIT Compilation مانند داشتن یک مترجم هوشمند است که:
- **Bytecode:** مانند دستورالعمل‌های عمومی
- **JIT Compilation:** مانند ترجمه به زبان محلی برای کارایی بهتر
- **HotSpot:** مانند شناسایی بخش‌های مهم و بهینه‌سازی آن‌ها

## 13.5 Class Loading & Reflection

Class Loading & Reflection یکی از مهم‌ترین جنبه‌های Java است که امکان dynamic loading و introspection را فراهم می‌کند.

### مفاهیم کلیدی:

**1. Class Loading:**
- Bootstrap ClassLoader
- Extension ClassLoader
- Application ClassLoader
- Custom ClassLoaders

**2. Reflection:**
- Runtime class inspection
- Dynamic method invocation
- Field access
- Constructor invocation

**3. Class Loading Process:**
- Loading
- Linking
- Initialization

### مثال عملی:

```java
import java.lang.reflect.*;
import java.net.URL;
import java.net.URLClassLoader;

public class ClassLoadingReflectionExample {
    public static void main(String[] args) {
        System.out.println("=== Class Loading & Reflection Example ===");
        
        // 1. Demonstrate class loading
        demonstrateClassLoading();
        
        // 2. Demonstrate reflection
        demonstrateReflection();
        
        // 3. Demonstrate custom class loader
        demonstrateCustomClassLoader();
    }
    
    public static void demonstrateClassLoading() {
        System.out.println("\n=== Class Loading ===");
        
        // Get class loader hierarchy
        ClassLoader classLoader = ClassLoadingReflectionExample.class.getClassLoader();
        
        System.out.println("Current class loader: " + classLoader);
        System.out.println("Parent class loader: " + classLoader.getParent());
        System.out.println("Grandparent class loader: " + classLoader.getParent().getParent());
        
        // Load a class
        try {
            Class<?> clazz = Class.forName("java.lang.String");
            System.out.println("Loaded class: " + clazz.getName());
            System.out.println("Class loader: " + clazz.getClassLoader());
        } catch (ClassNotFoundException e) {
            System.err.println("Class not found: " + e.getMessage());
        }
    }
    
    public static void demonstrateReflection() {
        System.out.println("\n=== Reflection ===");
        
        try {
            // Get class information
            Class<?> clazz = Person.class;
            System.out.println("Class name: " + clazz.getName());
            System.out.println("Simple name: " + clazz.getSimpleName());
            System.out.println("Package: " + clazz.getPackage());
            
            // Get constructors
            System.out.println("\nConstructors:");
            Constructor<?>[] constructors = clazz.getConstructors();
            for (Constructor<?> constructor : constructors) {
                System.out.println("  " + constructor);
            }
            
            // Get fields
            System.out.println("\nFields:");
            Field[] fields = clazz.getDeclaredFields();
            for (Field field : fields) {
                System.out.println("  " + field.getName() + " - " + field.getType());
            }
            
            // Get methods
            System.out.println("\nMethods:");
            Method[] methods = clazz.getDeclaredMethods();
            for (Method method : methods) {
                System.out.println("  " + method.getName() + " - " + method.getReturnType());
            }
            
            // Create instance using reflection
            System.out.println("\nCreating instance using reflection:");
            Constructor<?> constructor = clazz.getConstructor(String.class, int.class);
            Object instance = constructor.newInstance("احمد", 25);
            System.out.println("Created instance: " + instance);
            
            // Invoke method using reflection
            Method getNameMethod = clazz.getMethod("getName");
            String name = (String) getNameMethod.invoke(instance);
            System.out.println("Name via reflection: " + name);
            
            // Access field using reflection
            Field nameField = clazz.getDeclaredField("name");
            nameField.setAccessible(true);
            String fieldValue = (String) nameField.get(instance);
            System.out.println("Name field via reflection: " + fieldValue);
            
        } catch (Exception e) {
            System.err.println("Reflection error: " + e.getMessage());
        }
    }
    
    public static void demonstrateCustomClassLoader() {
        System.out.println("\n=== Custom Class Loader ===");
        
        try {
            // Create custom class loader
            URL[] urls = {new URL("file:///tmp/")};
            URLClassLoader customLoader = new URLClassLoader(urls);
            
            System.out.println("Custom class loader created: " + customLoader);
            System.out.println("Parent: " + customLoader.getParent());
            
            // Load class with custom loader
            Class<?> clazz = customLoader.loadClass("java.lang.String");
            System.out.println("Loaded class with custom loader: " + clazz.getName());
            
            customLoader.close();
            
        } catch (Exception e) {
            System.err.println("Custom class loader error: " + e.getMessage());
        }
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
    
    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + "}";
    }
}
```

### آنالوژی دنیای واقعی:
Class Loading & Reflection مانند داشتن یک سیستم کتابخانه هوشمند است:
- **Class Loading:** مانند سیستم قفسه‌بندی و بازیابی کتاب‌ها
- **Reflection:** مانند داشتن یک فهرست کامل از محتویات کتاب‌ها
- **Custom ClassLoader:** مانند داشتن یک سیستم قفسه‌بندی اختصاصی

## 13.6 Instrumentation & Profiling

Instrumentation & Profiling ابزارهای مهمی برای monitoring و بهینه‌سازی Java applications هستند.

### مفاهیم کلیدی:

**1. Java Instrumentation:**
- Bytecode manipulation
- Runtime monitoring
- Performance measurement
- Memory profiling

**2. Profiling Tools:**
- JProfiler
- VisualVM
- JConsole
- Flight Recorder

**3. Monitoring:**
- JVM metrics
- Application metrics
- Performance counters
- Memory usage

### مثال عملی:

```java
import java.lang.instrument.Instrumentation;
import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.lang.management.MemoryUsage;
import java.lang.management.ThreadMXBean;
import java.lang.management.GarbageCollectorMXBean;
import java.util.List;

public class InstrumentationProfilingExample {
    private static Instrumentation instrumentation;
    
    public static void main(String[] args) {
        System.out.println("=== Instrumentation & Profiling Example ===");
        
        // 1. Demonstrate JVM monitoring
        demonstrateJVMMonitoring();
        
        // 2. Demonstrate memory profiling
        demonstrateMemoryProfiling();
        
        // 3. Demonstrate thread profiling
        demonstrateThreadProfiling();
        
        // 4. Demonstrate GC monitoring
        demonstrateGCMonitoring();
    }
    
    public static void demonstrateJVMMonitoring() {
        System.out.println("\n=== JVM Monitoring ===");
        
        // Get JVM name and version
        String jvmName = ManagementFactory.getRuntimeMXBean().getVmName();
        String jvmVersion = ManagementFactory.getRuntimeMXBean().getVmVersion();
        System.out.println("JVM Name: " + jvmName);
        System.out.println("JVM Version: " + jvmVersion);
        
        // Get uptime
        long uptime = ManagementFactory.getRuntimeMXBean().getUptime();
        System.out.println("Uptime: " + uptime + " ms");
        
        // Get available processors
        int processors = Runtime.getRuntime().availableProcessors();
        System.out.println("Available Processors: " + processors);
    }
    
    public static void demonstrateMemoryProfiling() {
        System.out.println("\n=== Memory Profiling ===");
        
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        
        // Heap memory usage
        MemoryUsage heapUsage = memoryBean.getHeapMemoryUsage();
        System.out.println("Heap Memory:");
        System.out.println("  Used: " + heapUsage.getUsed() / 1024 / 1024 + " MB");
        System.out.println("  Committed: " + heapUsage.getCommitted() / 1024 / 1024 + " MB");
        System.out.println("  Max: " + heapUsage.getMax() / 1024 / 1024 + " MB");
        
        // Non-heap memory usage
        MemoryUsage nonHeapUsage = memoryBean.getNonHeapMemoryUsage();
        System.out.println("Non-Heap Memory:");
        System.out.println("  Used: " + nonHeapUsage.getUsed() / 1024 / 1024 + " MB");
        System.out.println("  Committed: " + nonHeapUsage.getCommitted() / 1024 / 1024 + " MB");
        System.out.println("  Max: " + nonHeapUsage.getMax() / 1024 / 1024 + " MB");
    }
    
    public static void demonstrateThreadProfiling() {
        System.out.println("\n=== Thread Profiling ===");
        
        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        
        // Thread count
        int threadCount = threadBean.getThreadCount();
        int peakThreadCount = threadBean.getPeakThreadCount();
        System.out.println("Current Thread Count: " + threadCount);
        System.out.println("Peak Thread Count: " + peakThreadCount);
        
        // Thread IDs
        long[] threadIds = threadBean.getAllThreadIds();
        System.out.println("Thread IDs: " + java.util.Arrays.toString(threadIds));
        
        // Thread info
        for (long threadId : threadIds) {
            java.lang.management.ThreadInfo threadInfo = threadBean.getThreadInfo(threadId);
            if (threadInfo != null) {
                System.out.println("Thread " + threadId + ": " + threadInfo.getThreadName() + 
                                 " - " + threadInfo.getThreadState());
            }
        }
    }
    
    public static void demonstrateGCMonitoring() {
        System.out.println("\n=== GC Monitoring ===");
        
        List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
        
        for (GarbageCollectorMXBean gcBean : gcBeans) {
            System.out.println("GC Name: " + gcBean.getName());
            System.out.println("  Collections: " + gcBean.getCollectionCount());
            System.out.println("  Time: " + gcBean.getCollectionTime() + " ms");
        }
    }
}
```

### Profiling Tools Examples:

```bash
# JConsole
jconsole

# VisualVM
jvisualvm

# Flight Recorder
java -XX:+FlightRecorder -XX:StartFlightRecording=duration=60s,filename=recording.jfr MyApplication

# JProfiler (commercial)
# Requires JProfiler installation
```

### آنالوژی دنیای واقعی:
Instrumentation & Profiling مانند داشتن یک سیستم نظارت هوشمند است:
- **Instrumentation:** مانند نصب سنسورهای مختلف در کارخانه
- **Profiling:** مانند تحلیل داده‌های جمع‌آوری شده
- **Monitoring:** مانند داشتن یک داشبورد کنترل برای نظارت بر عملکرد