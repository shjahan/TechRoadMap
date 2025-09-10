# Section 6 - Java 8 - The Lambda Revolution

## 6.1 Lambda Expressions

Lambda expressions یکی از مهم‌ترین ویژگی‌های Java 8 است که برنامه‌نویسی functional را به Java آورد.

### مفاهیم کلیدی:

**1. Functional Programming:**
- توابع به عنوان first-class citizens
- Concise syntax
- Better code readability

**2. Syntax:**
- `(parameters) -> expression`
- `(parameters) -> { statements }`
- Type inference

### مثال عملی:

```java
import java.util.*;
import java.util.function.*;

public class LambdaExpressionsExample {
    
    public static void main(String[] args) {
        // 1. Basic lambda expressions
        System.out.println("=== Basic Lambda Expressions ===");
        
        // Runnable lambda
        Runnable runnable = () -> System.out.println("Hello Lambda!");
        runnable.run();
        
        // Comparator lambda
        List<String> names = Arrays.asList("احمد", "فاطمه", "علی", "زهرا");
        names.sort((a, b) -> a.compareTo(b));
        System.out.println("Sorted names: " + names);
        
        // 2. Functional interfaces
        System.out.println("\n=== Functional Interfaces ===");
        
        // Predicate
        Predicate<String> isLong = s -> s.length() > 3;
        System.out.println("Is 'Java' long? " + isLong.test("Java"));
        
        // Function
        Function<String, Integer> getLength = s -> s.length();
        System.out.println("Length of 'Hello': " + getLength.apply("Hello"));
        
        // Consumer
        Consumer<String> printer = s -> System.out.println("Printing: " + s);
        printer.accept("Lambda World");
        
        // Supplier
        Supplier<Double> randomValue = () -> Math.random();
        System.out.println("Random value: " + randomValue.get());
        
        // 3. Method references
        System.out.println("\n=== Method References ===");
        
        // Static method reference
        Function<String, Integer> parseInt = Integer::parseInt;
        System.out.println("Parsed: " + parseInt.apply("123"));
        
        // Instance method reference
        List<String> words = Arrays.asList("hello", "world", "java");
        words.forEach(System.out::println);
        
        // Constructor reference
        Supplier<List<String>> listSupplier = ArrayList::new;
        List<String> newList = listSupplier.get();
        newList.add("New item");
        System.out.println("New list: " + newList);
    }
}
```

### آنالوژی دنیای واقعی:
Lambda expressions مانند داشتن یک دستیار شخصی است که می‌تواند کارهای ساده را به صورت خودکار انجام دهد. به جای نوشتن دستورالعمل‌های طولانی، فقط می‌گویید "این کار را انجام بده" و دستیار می‌داند چه کار کند.

## 6.2 Stream API & Functional Programming

Stream API راه قدرتمندی برای پردازش collections به صورت functional فراهم می‌کند.

### مفاهیم کلیدی:

**1. Stream Operations:**
- Intermediate operations (filter, map, sorted)
- Terminal operations (collect, forEach, reduce)
- Lazy evaluation

**2. Pipeline Processing:**
- Chain operations together
- Efficient processing
- Parallel streams

### مثال عملی:

```java
import java.util.*;
import java.util.stream.*;

public class StreamAPIExample {
    
    public static void main(String[] args) {
        List<Person> people = Arrays.asList(
            new Person("احمد", 25, "تهران"),
            new Person("فاطمه", 30, "اصفهان"),
            new Person("علی", 22, "تهران"),
            new Person("زهرا", 28, "شیراز"),
            new Person("محمد", 35, "تهران")
        );
        
        // 1. Basic stream operations
        System.out.println("=== Basic Stream Operations ===");
        
        // Filter and map
        List<String> names = people.stream()
            .filter(p -> p.getAge() > 25)
            .map(Person::getName)
            .collect(Collectors.toList());
        System.out.println("Names of people over 25: " + names);
        
        // 2. Intermediate operations
        System.out.println("\n=== Intermediate Operations ===");
        
        // Filter, map, and sorted
        List<String> sortedNames = people.stream()
            .filter(p -> p.getCity().equals("تهران"))
            .map(Person::getName)
            .sorted()
            .collect(Collectors.toList());
        System.out.println("Tehran residents (sorted): " + sortedNames);
        
        // 3. Terminal operations
        System.out.println("\n=== Terminal Operations ===");
        
        // Count
        long count = people.stream()
            .filter(p -> p.getAge() > 25)
            .count();
        System.out.println("People over 25: " + count);
        
        // Average age
        double averageAge = people.stream()
            .mapToInt(Person::getAge)
            .average()
            .orElse(0.0);
        System.out.println("Average age: " + averageAge);
        
        // Group by city
        Map<String, List<Person>> byCity = people.stream()
            .collect(Collectors.groupingBy(Person::getCity));
        System.out.println("Grouped by city: " + byCity);
        
        // 4. Parallel streams
        System.out.println("\n=== Parallel Streams ===");
        
        long startTime = System.currentTimeMillis();
        List<String> parallelResult = people.parallelStream()
            .filter(p -> p.getAge() > 20)
            .map(Person::getName)
            .collect(Collectors.toList());
        long endTime = System.currentTimeMillis();
        
        System.out.println("Parallel processing time: " + (endTime - startTime) + " ms");
        System.out.println("Result: " + parallelResult);
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
    
    // Getters
    public String getName() { return name; }
    public int getAge() { return age; }
    public String getCity() { return city; }
    
    @Override
    public String toString() {
        return name + " (" + age + ", " + city + ")";
    }
}
```

### آنالوژی دنیای واقعی:
Stream API مانند داشتن یک خط تولید هوشمند است. مواد اولیه (data) از یک طرف وارد می‌شود، در هر مرحله پردازش می‌شود (filter, map, sort)، و در نهایت محصول نهایی (result) از طرف دیگر خارج می‌شود.

## 6.3 Method References

Method references راه ساده‌تری برای ارجاع به متدها فراهم می‌کند.

### مفاهیم کلیدی:

**1. Types of Method References:**
- Static method reference: `Class::staticMethod`
- Instance method reference: `instance::method`
- Constructor reference: `Class::new`

### مثال عملی:

```java
import java.util.*;
import java.util.function.*;

public class MethodReferencesExample {
    
    public static void main(String[] args) {
        List<String> names = Arrays.asList("احمد", "فاطمه", "علی", "زهرا");
        
        // 1. Static method reference
        System.out.println("=== Static Method Reference ===");
        
        // Using lambda
        names.stream()
            .map(s -> Integer.parseInt(s))
            .forEach(System.out::println);
        
        // Using method reference
        names.stream()
            .map(Integer::parseInt)
            .forEach(System.out::println);
        
        // 2. Instance method reference
        System.out.println("\n=== Instance Method Reference ===");
        
        String prefix = "Mr. ";
        names.stream()
            .map(prefix::concat)
            .forEach(System.out::println);
        
        // 3. Constructor reference
        System.out.println("\n=== Constructor Reference ===");
        
        List<String> words = Arrays.asList("hello", "world", "java");
        List<StringBuilder> builders = words.stream()
            .map(StringBuilder::new)
            .collect(Collectors.toList());
        
        builders.forEach(System.out::println);
        
        // 4. Complex method reference
        System.out.println("\n=== Complex Method Reference ===");
        
        List<Person> people = Arrays.asList(
            new Person("احمد", 25),
            new Person("فاطمه", 30),
            new Person("علی", 22)
        );
        
        // Sort by age using method reference
        people.sort(Comparator.comparing(Person::getAge));
        people.forEach(System.out::println);
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
        return name + " (" + age + ")";
    }
}
```

### آنالوژی دنیای واقعی:
Method references مانند داشتن یک دفترچه تلفن هوشمند است. به جای نوشتن کامل شماره تلفن، فقط نام شخص را می‌نویسید و سیستم خودکار شماره را پیدا می‌کند.

## 6.4 Optional Class

Optional class راه ایمنی برای handling null values فراهم می‌کند.

### مفاهیم کلیدی:

**1. Null Safety:**
- جلوگیری از NullPointerException
- Explicit null handling
- Better code documentation

**2. Optional Methods:**
- `of()`, `ofNullable()`, `empty()`
- `isPresent()`, `ifPresent()`
- `orElse()`, `orElseGet()`, `orElseThrow()`

### مثال عملی:

```java
import java.util.*;
import java.util.Optional;

public class OptionalExample {
    
    public static void main(String[] args) {
        // 1. Creating Optional
        System.out.println("=== Creating Optional ===");
        
        Optional<String> empty = Optional.empty();
        Optional<String> present = Optional.of("Hello");
        Optional<String> nullable = Optional.ofNullable(null);
        
        System.out.println("Empty: " + empty.isPresent());
        System.out.println("Present: " + present.isPresent());
        System.out.println("Nullable: " + nullable.isPresent());
        
        // 2. Working with Optional
        System.out.println("\n=== Working with Optional ===");
        
        Optional<String> name = Optional.of("احمد");
        
        // Check if present
        if (name.isPresent()) {
            System.out.println("Name: " + name.get());
        }
        
        // If present
        name.ifPresent(n -> System.out.println("Name is: " + n));
        
        // Or else
        String result = name.orElse("Unknown");
        System.out.println("Result: " + result);
        
        // 3. Optional chaining
        System.out.println("\n=== Optional Chaining ===");
        
        Optional<String> optionalName = Optional.of("احمد محمدی");
        
        Optional<String> upperCase = optionalName
            .filter(n -> n.length() > 5)
            .map(String::toUpperCase);
        
        upperCase.ifPresent(System.out::println);
        
        // 4. Practical example
        System.out.println("\n=== Practical Example ===");
        
        User user = findUserById(1);
        String email = user
            .flatMap(User::getEmail)
            .orElse("No email provided");
        
        System.out.println("User email: " + email);
        
        // 5. Optional with collections
        System.out.println("\n=== Optional with Collections ===");
        
        List<String> names = Arrays.asList("احمد", "فاطمه", "علی");
        Optional<String> first = names.stream()
            .filter(n -> n.startsWith("ا"))
            .findFirst();
        
        first.ifPresent(System.out::println);
    }
    
    public static Optional<User> findUserById(int id) {
        // Simulate database lookup
        if (id == 1) {
            return Optional.of(new User("احمد", Optional.of("ahmad@example.com")));
        }
        return Optional.empty();
    }
}

class User {
    private String name;
    private Optional<String> email;
    
    public User(String name, Optional<String> email) {
        this.name = name;
        this.email = email;
    }
    
    public String getName() { return name; }
    public Optional<String> getEmail() { return email; }
}
```

### آنالوژی دنیای واقعی:
Optional مانند داشتن یک جعبه است که ممکن است خالی باشد یا چیزی در آن باشد. قبل از باز کردن جعبه، باید بررسی کنید که آیا چیزی در آن است یا نه. این کار از تعجب‌های ناخوشایند جلوگیری می‌کند.

## 6.5 Default Methods in Interfaces

Default methods امکان اضافه کردن implementation به interfaces را فراهم می‌کند.

### مفاهیم کلیدی:

**1. Backward Compatibility:**
- اضافه کردن متدهای جدید بدون breaking existing code
- Multiple inheritance of behavior
- Diamond problem resolution

### مثال عملی:

```java
public class DefaultMethodsExample {
    
    public static void main(String[] args) {
        // 1. Basic default methods
        System.out.println("=== Basic Default Methods ===");
        
        Calculator calculator = new BasicCalculator();
        System.out.println("Add: " + calculator.add(5, 3));
        System.out.println("Subtract: " + calculator.subtract(5, 3));
        System.out.println("Multiply: " + calculator.multiply(5, 3));
        System.out.println("Divide: " + calculator.divide(5, 3));
        
        // 2. Overriding default methods
        System.out.println("\n=== Overriding Default Methods ===");
        
        AdvancedCalculator advanced = new AdvancedCalculator();
        System.out.println("Power: " + advanced.power(2, 3));
        System.out.println("Square root: " + advanced.squareRoot(16));
        
        // 3. Multiple interfaces
        System.out.println("\n=== Multiple Interfaces ===");
        
        MultiFunction multi = new MultiFunction();
        multi.log("Hello World");
        multi.print("Hello World");
    }
}

// Basic interface with default methods
interface Calculator {
    int add(int a, int b);
    int subtract(int a, int b);
    
    // Default methods
    default int multiply(int a, int b) {
        return a * b;
    }
    
    default int divide(int a, int b) {
        if (b == 0) {
            throw new IllegalArgumentException("Division by zero");
        }
        return a / b;
    }
}

// Advanced interface extending basic
interface AdvancedCalculator extends Calculator {
    double power(double base, double exponent);
    
    default double squareRoot(double number) {
        return Math.sqrt(number);
    }
}

// Implementation
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
}

// Multiple interfaces
interface Logger {
    default void log(String message) {
        System.out.println("LOG: " + message);
    }
}

interface Printer {
    default void print(String message) {
        System.out.println("PRINT: " + message);
    }
}

class MultiFunction implements Logger, Printer {
    // Can use both default methods
}
```

### آنالوژی دنیای واقعی:
Default methods مانند داشتن یک قرارداد پایه‌ای است که می‌تواند در طول زمان بهبود یابد. اگر قرارداد جدیدی اضافه شود، نیازی به تغییر تمام طرف‌های قرارداد نیست - فقط کسانی که می‌خواهند از ویژگی جدید استفاده کنند، آن را پیاده‌سازی می‌کنند.

## 6.6 Date & Time API (java.time)

Java 8 API جدیدی برای کار با تاریخ و زمان معرفی کرد.

### مفاهیم کلیدی:

**1. Immutable Classes:**
- Thread-safe
- No side effects
- Better performance

**2. Main Classes:**
- `LocalDate`, `LocalTime`, `LocalDateTime`
- `ZonedDateTime`, `OffsetDateTime`
- `Duration`, `Period`

### مثال عملی:

```java
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

public class DateTimeAPIExample {
    
    public static void main(String[] args) {
        // 1. Basic date and time
        System.out.println("=== Basic Date and Time ===");
        
        LocalDate today = LocalDate.now();
        LocalTime now = LocalTime.now();
        LocalDateTime dateTime = LocalDateTime.now();
        
        System.out.println("Today: " + today);
        System.out.println("Now: " + now);
        System.out.println("DateTime: " + dateTime);
        
        // 2. Creating specific dates
        System.out.println("\n=== Creating Specific Dates ===");
        
        LocalDate specificDate = LocalDate.of(2024, 1, 15);
        LocalTime specificTime = LocalTime.of(14, 30, 0);
        LocalDateTime specificDateTime = LocalDateTime.of(specificDate, specificTime);
        
        System.out.println("Specific date: " + specificDate);
        System.out.println("Specific time: " + specificTime);
        System.out.println("Specific datetime: " + specificDateTime);
        
        // 3. Date arithmetic
        System.out.println("\n=== Date Arithmetic ===");
        
        LocalDate tomorrow = today.plusDays(1);
        LocalDate nextWeek = today.plusWeeks(1);
        LocalDate nextMonth = today.plusMonths(1);
        LocalDate nextYear = today.plusYears(1);
        
        System.out.println("Tomorrow: " + tomorrow);
        System.out.println("Next week: " + nextWeek);
        System.out.println("Next month: " + nextMonth);
        System.out.println("Next year: " + nextYear);
        
        // 4. Duration and Period
        System.out.println("\n=== Duration and Period ===");
        
        LocalDateTime start = LocalDateTime.of(2024, 1, 1, 10, 0);
        LocalDateTime end = LocalDateTime.of(2024, 1, 1, 15, 30);
        
        Duration duration = Duration.between(start, end);
        System.out.println("Duration: " + duration);
        System.out.println("Hours: " + duration.toHours());
        System.out.println("Minutes: " + duration.toMinutes());
        
        Period period = Period.between(LocalDate.of(2020, 1, 1), LocalDate.of(2024, 1, 1));
        System.out.println("Period: " + period);
        System.out.println("Years: " + period.getYears());
        
        // 5. Formatting
        System.out.println("\n=== Formatting ===");
        
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        String formatted = dateTime.format(formatter);
        System.out.println("Formatted: " + formatted);
        
        // 6. Parsing
        System.out.println("\n=== Parsing ===");
        
        String dateString = "2024-01-15";
        LocalDate parsedDate = LocalDate.parse(dateString);
        System.out.println("Parsed date: " + parsedDate);
        
        // 7. Time zones
        System.out.println("\n=== Time Zones ===");
        
        ZonedDateTime utc = ZonedDateTime.now(ZoneOffset.UTC);
        ZonedDateTime tehran = ZonedDateTime.now(ZoneId.of("Asia/Tehran"));
        
        System.out.println("UTC: " + utc);
        System.out.println("Tehran: " + tehran);
        
        // 8. ChronoUnit
        System.out.println("\n=== ChronoUnit ===");
        
        long daysBetween = ChronoUnit.DAYS.between(specificDate, today);
        long hoursBetween = ChronoUnit.HOURS.between(start, end);
        
        System.out.println("Days between: " + daysBetween);
        System.out.println("Hours between: " + hoursBetween);
    }
}
```

### آنالوژی دنیای واقعی:
Date & Time API مانند داشتن یک تقویم هوشمند است که می‌تواند با تاریخ‌ها و زمان‌ها به صورت دقیق و ایمن کار کند. می‌توانید تاریخ‌ها را اضافه کنید، تفاوت بین آن‌ها را محاسبه کنید، و آن‌ها را به فرمت‌های مختلف تبدیل کنید.

## 6.7 CompletableFuture

CompletableFuture راه قدرتمندی برای asynchronous programming فراهم می‌کند.

### مفاهیم کلیدی:

**1. Asynchronous Execution:**
- Non-blocking operations
- Better resource utilization
- Responsive applications

**2. Composition:**
- Chain operations
- Combine results
- Handle errors

### مثال عملی:

```java
import java.util.concurrent.*;
import java.util.function.*;

public class CompletableFutureExample {
    
    public static void main(String[] args) throws Exception {
        // 1. Basic CompletableFuture
        System.out.println("=== Basic CompletableFuture ===");
        
        CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "Hello World";
        });
        
        String result = future.get();
        System.out.println("Result: " + result);
        
        // 2. Chaining operations
        System.out.println("\n=== Chaining Operations ===");
        
        CompletableFuture<String> chained = CompletableFuture
            .supplyAsync(() -> "Hello")
            .thenApply(s -> s + " World")
            .thenApply(String::toUpperCase);
        
        System.out.println("Chained result: " + chained.get());
        
        // 3. Combining futures
        System.out.println("\n=== Combining Futures ===");
        
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello");
        CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World");
        
        CompletableFuture<String> combined = future1.thenCombine(future2, (s1, s2) -> s1 + " " + s2);
        System.out.println("Combined: " + combined.get());
        
        // 4. Error handling
        System.out.println("\n=== Error Handling ===");
        
        CompletableFuture<String> errorFuture = CompletableFuture
            .supplyAsync(() -> {
                if (Math.random() > 0.5) {
                    throw new RuntimeException("Random error");
                }
                return "Success";
            })
            .handle((result, throwable) -> {
                if (throwable != null) {
                    return "Error handled: " + throwable.getMessage();
                }
                return result;
            });
        
        System.out.println("Error handling: " + errorFuture.get());
        
        // 5. Multiple futures
        System.out.println("\n=== Multiple Futures ===");
        
        CompletableFuture<String> f1 = CompletableFuture.supplyAsync(() -> "Task 1");
        CompletableFuture<String> f2 = CompletableFuture.supplyAsync(() -> "Task 2");
        CompletableFuture<String> f3 = CompletableFuture.supplyAsync(() -> "Task 3");
        
        CompletableFuture<Void> allOf = CompletableFuture.allOf(f1, f2, f3);
        allOf.thenRun(() -> {
            System.out.println("All tasks completed");
            System.out.println("Results: " + f1.join() + ", " + f2.join() + ", " + f3.join());
        });
        
        allOf.get();
    }
}
```

### آنالوژی دنیای واقعی:
CompletableFuture مانند داشتن چندین کارگر است که همزمان روی کارهای مختلف کار می‌کنند. وقتی یکی از کارها تمام شد، می‌تواند نتیجه را به کارگر بعدی بدهد یا منتظر بماند تا کارگران دیگر کارشان تمام شود.

## 6.8 Nashorn JavaScript Engine

Nashorn JavaScript engine امکان اجرای JavaScript در JVM را فراهم می‌کند.

### مفاهیم کلیدی:

**1. JavaScript in Java:**
- Execute JavaScript code
- Interact with Java objects
- Performance improvements

### مثال عملی:

```java
import javax.script.*;
import java.io.*;

public class NashornExample {
    
    public static void main(String[] args) throws Exception {
        // 1. Basic JavaScript execution
        System.out.println("=== Basic JavaScript Execution ===");
        
        ScriptEngineManager manager = new ScriptEngineManager();
        ScriptEngine engine = manager.getEngineByName("nashorn");
        
        // Execute JavaScript
        engine.eval("print('Hello from JavaScript!')");
        
        // 2. JavaScript variables
        System.out.println("\n=== JavaScript Variables ===");
        
        engine.eval("var name = 'احمد'; var age = 25;");
        engine.eval("print('Name: ' + name + ', Age: ' + age)");
        
        // 3. JavaScript functions
        System.out.println("\n=== JavaScript Functions ===");
        
        engine.eval("function greet(name) { return 'Hello, ' + name + '!'; }");
        Object result = engine.eval("greet('فاطمه')");
        System.out.println("Function result: " + result);
        
        // 4. Java-JavaScript interaction
        System.out.println("\n=== Java-JavaScript Interaction ===");
        
        // Pass Java object to JavaScript
        engine.put("javaObject", new JavaObject("احمد", 25));
        engine.eval("print('Java object name: ' + javaObject.getName())");
        
        // 5. JavaScript to Java
        System.out.println("\n=== JavaScript to Java ===");
        
        engine.eval("var javaList = new java.util.ArrayList();");
        engine.eval("javaList.add('Item 1');");
        engine.eval("javaList.add('Item 2');");
        engine.eval("print('List size: ' + javaList.size())");
        
        // 6. File execution
        System.out.println("\n=== File Execution ===");
        
        // Create JavaScript file
        try (PrintWriter writer = new PrintWriter("script.js")) {
            writer.println("function calculate(a, b) {");
            writer.println("    return a + b;");
            writer.println("}");
            writer.println("print('Result: ' + calculate(5, 3));");
        }
        
        // Execute JavaScript file
        engine.eval(new FileReader("script.js"));
        
        // Clean up
        new File("script.js").delete();
    }
}

class JavaObject {
    private String name;
    private int age;
    
    public JavaObject(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public String getName() { return name; }
    public int getAge() { return age; }
}
```

### آنالوژی دنیای واقعی:
Nashorn مانند داشتن یک مترجم است که می‌تواند بین زبان‌های مختلف ترجمه کند. می‌توانید کد JavaScript بنویسید و آن را در محیط Java اجرا کنید، یا از Java objects در JavaScript استفاده کنید.