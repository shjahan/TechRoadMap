# Section 1 - Java Fundamentals & Core Concepts

## 1.1 Java Language Basics

Java Language Basics شامل مفاهیم اساسی و پایه‌ای زبان جاوا است که هر برنامه‌نویس جاوا باید با آن‌ها آشنا باشد.

### مفاهیم کلیدی:

**1. Syntax و Structure:**
- هر برنامه جاوا باید در یک کلاس قرار گیرد
- متد `main` نقطه شروع اجرای برنامه است
- هر statement باید با `;` خاتمه یابد
- Java case-sensitive است

**2. Data Types:**
- **Primitive Types:** int, double, boolean, char, byte, short, long, float
- **Reference Types:** String, Arrays, Objects

**3. Variables:**
- **Declaration:** تعریف متغیر
- **Initialization:** مقداردهی اولیه
- **Scope:** محدوده دسترسی

### مثال عملی:

```java
public class JavaBasics {
    public static void main(String[] args) {
        // Primitive data types
        int age = 25;
        double salary = 50000.50;
        boolean isEmployed = true;
        char grade = 'A';
        
        // Reference data types
        String name = "احمد محمدی";
        int[] numbers = {1, 2, 3, 4, 5};
        
        // Variable scope
        if (age > 18) {
            String message = "شما بالغ هستید";
            System.out.println(message);
        }
        
        // Output
        System.out.println("نام: " + name);
        System.out.println("سن: " + age);
        System.out.println("حقوق: " + salary);
    }
}
```

### آنالوژی دنیای واقعی:
فکر کنید Java Language Basics مانند یادگیری الفبای فارسی است. قبل از اینکه بتوانید شعر بنویسید، باید حروف، کلمات و قواعد دستوری را یاد بگیرید.

## 1.2 Object-Oriented Programming Principles

برنامه‌نویسی شی‌گرا (OOP) یکی از مهم‌ترین پارادایم‌های برنامه‌نویسی است که Java بر اساس آن طراحی شده است.

### چهار اصل اصلی OOP:

**1. Encapsulation (کپسوله‌سازی):**
- مخفی کردن جزئیات پیاده‌سازی
- استفاده از access modifiers (private, protected, public)
- Getter و Setter methods

**2. Inheritance (وراثت):**
- کلاس‌ها می‌توانند از کلاس‌های دیگر ارث ببرند
- استفاده از کلمه کلیدی `extends`
- Code reusability

**3. Polymorphism (چندریختی):**
- یک interface، چندین implementation
- Method overriding و overloading
- Runtime polymorphism

**4. Abstraction (انتزاع):**
- مخفی کردن پیچیدگی‌ها
- Abstract classes و interfaces
- Focus on what object does, not how

### مثال عملی:

```java
// 1. Encapsulation
class BankAccount {
    private double balance; // private field
    
    // Getter method
    public double getBalance() {
        return balance;
    }
    
    // Setter method
    public void setBalance(double balance) {
        if (balance >= 0) {
            this.balance = balance;
        }
    }
    
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }
}

// 2. Inheritance
class SavingsAccount extends BankAccount {
    private double interestRate;
    
    public SavingsAccount(double interestRate) {
        this.interestRate = interestRate;
    }
    
    public void addInterest() {
        double interest = getBalance() * interestRate / 100;
        deposit(interest);
    }
}

// 3. Polymorphism
interface Shape {
    double calculateArea();
}

class Circle implements Shape {
    private double radius;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}

class Rectangle implements Shape {
    private double width, height;
    
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
    
    @Override
    public double calculateArea() {
        return width * height;
    }
}

// 4. Abstraction
abstract class Vehicle {
    protected String brand;
    protected int year;
    
    public Vehicle(String brand, int year) {
        this.brand = brand;
        this.year = year;
    }
    
    // Abstract method - must be implemented by subclasses
    public abstract void start();
    
    // Concrete method
    public void displayInfo() {
        System.out.println("برند: " + brand + ", سال: " + year);
    }
}

class Car extends Vehicle {
    public Car(String brand, int year) {
        super(brand, year);
    }
    
    @Override
    public void start() {
        System.out.println("ماشین روشن شد");
    }
}

// Usage example
public class OOPExample {
    public static void main(String[] args) {
        // Encapsulation
        BankAccount account = new BankAccount();
        account.setBalance(1000);
        System.out.println("موجودی: " + account.getBalance());
        
        // Inheritance
        SavingsAccount savings = new SavingsAccount(5.0);
        savings.setBalance(1000);
        savings.addInterest();
        System.out.println("موجودی پس از سود: " + savings.getBalance());
        
        // Polymorphism
        Shape[] shapes = {
            new Circle(5),
            new Rectangle(4, 6)
        };
        
        for (Shape shape : shapes) {
            System.out.println("مساحت: " + shape.calculateArea());
        }
        
        // Abstraction
        Vehicle car = new Car("تویوتا", 2023);
        car.displayInfo();
        car.start();
    }
}
```

### آنالوژی دنیای واقعی:
OOP مانند طراحی یک ساختمان است:
- **Encapsulation:** دیوارها و درها که جزئیات داخلی را مخفی می‌کنند
- **Inheritance:** آپارتمان‌ها که از طرح کلی ساختمان ارث می‌برند
- **Polymorphism:** درهای مختلف (چوبی، فلزی) که همه یک کار می‌کنند
- **Abstraction:** نقشه ساختمان که جزئیات پیاده‌سازی را نشان نمی‌دهد

## 1.3 Java Collections Framework

Java Collections Framework مجموعه‌ای از interfaces و classes است که برای ذخیره و مدیریت گروهی از objects استفاده می‌شود.

### سلسله مراتب Collections:

**1. Collection Interface:**
- ریشه تمام collection interfaces
- شامل methods اساسی مانند add, remove, size, isEmpty

**2. List Interface:**
- Ordered collection
- Duplicate elements allowed
- Index-based access
- Implementations: ArrayList, LinkedList, Vector

**3. Set Interface:**
- No duplicate elements
- No guaranteed order
- Implementations: HashSet, LinkedHashSet, TreeSet

**4. Map Interface:**
- Key-value pairs
- No duplicate keys
- Implementations: HashMap, LinkedHashMap, TreeMap

**5. Queue Interface:**
- FIFO (First In, First Out)
- Implementations: LinkedList, PriorityQueue, ArrayDeque

### مثال عملی:

```java
import java.util.*;

public class CollectionsExample {
    public static void main(String[] args) {
        // 1. List Examples
        System.out.println("=== List Examples ===");
        
        // ArrayList
        List<String> arrayList = new ArrayList<>();
        arrayList.add("سیب");
        arrayList.add("موز");
        arrayList.add("پرتقال");
        arrayList.add("سیب"); // Duplicate allowed
        
        System.out.println("ArrayList: " + arrayList);
        System.out.println("اندازه: " + arrayList.size());
        System.out.println("عنصر در ایندکس 1: " + arrayList.get(1));
        
        // LinkedList
        List<Integer> linkedList = new LinkedList<>();
        linkedList.add(10);
        linkedList.add(20);
        linkedList.add(30);
        System.out.println("LinkedList: " + linkedList);
        
        // 2. Set Examples
        System.out.println("\n=== Set Examples ===");
        
        // HashSet
        Set<String> hashSet = new HashSet<>();
        hashSet.add("قرمز");
        hashSet.add("سبز");
        hashSet.add("آبی");
        hashSet.add("قرمز"); // Duplicate ignored
        
        System.out.println("HashSet: " + hashSet);
        System.out.println("حاوی 'سبز': " + hashSet.contains("سبز"));
        
        // TreeSet (Sorted)
        Set<Integer> treeSet = new TreeSet<>();
        treeSet.add(50);
        treeSet.add(10);
        treeSet.add(30);
        treeSet.add(20);
        System.out.println("TreeSet (مرتب): " + treeSet);
        
        // 3. Map Examples
        System.out.println("\n=== Map Examples ===");
        
        // HashMap
        Map<String, Integer> studentGrades = new HashMap<>();
        studentGrades.put("احمد", 18);
        studentGrades.put("فاطمه", 19);
        studentGrades.put("علی", 17);
        studentGrades.put("زهرا", 20);
        
        System.out.println("نمرات دانشجویان: " + studentGrades);
        System.out.println("نمره احمد: " + studentGrades.get("احمد"));
        
        // Iterating through map
        System.out.println("همه نمرات:");
        for (Map.Entry<String, Integer> entry : studentGrades.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
        
        // 4. Queue Examples
        System.out.println("\n=== Queue Examples ===");
        
        // LinkedList as Queue
        Queue<String> queue = new LinkedList<>();
        queue.offer("اولین");
        queue.offer("دومین");
        queue.offer("سومین");
        
        System.out.println("Queue: " + queue);
        System.out.println("اولین عنصر: " + queue.peek());
        System.out.println("حذف: " + queue.poll());
        System.out.println("Queue بعد از حذف: " + queue);
        
        // PriorityQueue
        Queue<Integer> priorityQueue = new PriorityQueue<>();
        priorityQueue.offer(30);
        priorityQueue.offer(10);
        priorityQueue.offer(50);
        priorityQueue.offer(20);
        
        System.out.println("PriorityQueue: " + priorityQueue);
        while (!priorityQueue.isEmpty()) {
            System.out.println("حذف: " + priorityQueue.poll());
        }
    }
}
```

### عملیات رایج Collections:

```java
import java.util.*;

public class CommonOperations {
    public static void main(String[] args) {
        List<String> fruits = new ArrayList<>();
        fruits.add("سیب");
        fruits.add("موز");
        fruits.add("پرتقال");
        fruits.add("انگور");
        
        // 1. Iteration
        System.out.println("=== Iteration Methods ===");
        
        // Traditional for loop
        System.out.println("For loop:");
        for (int i = 0; i < fruits.size(); i++) {
            System.out.println(fruits.get(i));
        }
        
        // Enhanced for loop
        System.out.println("\nEnhanced for loop:");
        for (String fruit : fruits) {
            System.out.println(fruit);
        }
        
        // Iterator
        System.out.println("\nIterator:");
        Iterator<String> iterator = fruits.iterator();
        while (iterator.hasNext()) {
            System.out.println(iterator.next());
        }
        
        // 2. Searching
        System.out.println("\n=== Searching ===");
        System.out.println("حاوی 'موز': " + fruits.contains("موز"));
        System.out.println("ایندکس 'پرتقال': " + fruits.indexOf("پرتقال"));
        
        // 3. Sorting
        System.out.println("\n=== Sorting ===");
        List<Integer> numbers = Arrays.asList(5, 2, 8, 1, 9);
        System.out.println("قبل از مرتب‌سازی: " + numbers);
        Collections.sort(numbers);
        System.out.println("بعد از مرتب‌سازی: " + numbers);
        
        // 4. Filtering and Transformation
        System.out.println("\n=== Filtering ===");
        List<String> filteredFruits = new ArrayList<>();
        for (String fruit : fruits) {
            if (fruit.length() > 3) {
                filteredFruits.add(fruit);
            }
        }
        System.out.println("میوه‌های با بیش از 3 حرف: " + filteredFruits);
    }
}
```

### آنالوژی دنیای واقعی:
Collections Framework مانند انواع مختلف ظروف آشپزخانه است:
- **List:** مانند لیست خرید که ترتیب مهم است و می‌توان آیتم‌های تکراری داشت
- **Set:** مانند مجموعه کلیدهای منزل که هیچ تکراری ندارد
- **Map:** مانند دفترچه تلفن که هر نام یک شماره دارد
- **Queue:** مانند صف بانک که اولین نفر، اولین خدمت را دریافت می‌کند

## 1.4 Exception Handling & Error Management

مدیریت خطا (Exception Handling) یکی از مهم‌ترین جنبه‌های برنامه‌نویسی است که Java آن را به صورت قدرتمند پشتیبانی می‌کند.

### انواع Exception:

**1. Checked Exceptions:**
- باید در compile time handle شوند
- Compiler آن‌ها را بررسی می‌کند
- مثال: IOException, SQLException

**2. Unchecked Exceptions (Runtime Exceptions):**
- در runtime رخ می‌دهند
- Compiler آن‌ها را بررسی نمی‌کند
- مثال: NullPointerException, ArrayIndexOutOfBoundsException

**3. Errors:**
- مشکلات جدی سیستم
- معمولاً قابل recovery نیستند
- مثال: OutOfMemoryError, StackOverflowError

### ساختار Exception Handling:

```java
try {
    // کد پرخطر
} catch (ExceptionType e) {
    // مدیریت خطا
} finally {
    // کد همیشه اجرا می‌شود
}
```

### مثال عملی:

```java
import java.io.*;
import java.util.*;

public class ExceptionHandlingExample {
    public static void main(String[] args) {
        // 1. Basic Exception Handling
        System.out.println("=== Basic Exception Handling ===");
        
        try {
            int result = divide(10, 0);
            System.out.println("نتیجه: " + result);
        } catch (ArithmeticException e) {
            System.out.println("خطا: " + e.getMessage());
        } finally {
            System.out.println("Finally block اجرا شد");
        }
        
        // 2. Multiple Exception Handling
        System.out.println("\n=== Multiple Exception Handling ===");
        
        try {
            int[] numbers = {1, 2, 3};
            System.out.println("عنصر: " + numbers[5]); // ArrayIndexOutOfBoundsException
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("خطای ایندکس آرایه: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("خطای عمومی: " + e.getMessage());
        }
        
        // 3. Custom Exception
        System.out.println("\n=== Custom Exception ===");
        
        try {
            validateAge(15);
        } catch (InvalidAgeException e) {
            System.out.println("خطای سن: " + e.getMessage());
        }
        
        // 4. Try-with-resources
        System.out.println("\n=== Try-with-resources ===");
        
        try (FileWriter writer = new FileWriter("test.txt")) {
            writer.write("سلام دنیا!");
            System.out.println("فایل با موفقیت نوشته شد");
        } catch (IOException e) {
            System.out.println("خطا در نوشتن فایل: " + e.getMessage());
        }
        
        // 5. Exception Propagation
        System.out.println("\n=== Exception Propagation ===");
        
        try {
            methodA();
        } catch (Exception e) {
            System.out.println("خطا در methodA: " + e.getMessage());
        }
    }
    
    // Method that throws exception
    public static int divide(int a, int b) throws ArithmeticException {
        if (b == 0) {
            throw new ArithmeticException("تقسیم بر صفر امکان‌پذیر نیست");
        }
        return a / b;
    }
    
    // Method with multiple exceptions
    public static void methodA() throws Exception {
        try {
            methodB();
        } catch (Exception e) {
            System.out.println("مدیریت خطا در methodA");
            throw e; // Re-throw exception
        }
    }
    
    public static void methodB() throws Exception {
        throw new Exception("خطا در methodB");
    }
    
    // Custom Exception Example
    public static void validateAge(int age) throws InvalidAgeException {
        if (age < 18) {
            throw new InvalidAgeException("سن باید حداقل 18 سال باشد");
        }
        System.out.println("سن معتبر است: " + age);
    }
}

// Custom Exception Class
class InvalidAgeException extends Exception {
    public InvalidAgeException(String message) {
        super(message);
    }
}
```

### Best Practices برای Exception Handling:

```java
public class ExceptionBestPractices {
    
    // 1. Specific Exception Handling
    public void readFile(String filename) {
        try {
            FileReader file = new FileReader(filename);
            // Process file
        } catch (FileNotFoundException e) {
            System.err.println("فایل پیدا نشد: " + filename);
        } catch (IOException e) {
            System.err.println("خطا در خواندن فایل: " + e.getMessage());
        }
    }
    
    // 2. Logging Exceptions
    public void processData(String data) {
        try {
            // Process data
            int result = Integer.parseInt(data);
            System.out.println("نتیجه: " + result);
        } catch (NumberFormatException e) {
            // Log the exception
            System.err.println("خطا در تبدیل داده: " + data);
            e.printStackTrace();
        }
    }
    
    // 3. Resource Management
    public void writeToFile(String filename, String content) {
        try (FileWriter writer = new FileWriter(filename);
             BufferedWriter bufferedWriter = new BufferedWriter(writer)) {
            
            bufferedWriter.write(content);
            bufferedWriter.flush();
            
        } catch (IOException e) {
            System.err.println("خطا در نوشتن فایل: " + e.getMessage());
        }
    }
    
    // 4. Exception Wrapping
    public void connectToDatabase() throws DatabaseException {
        try {
            // Database connection code
            throw new SQLException("خطای اتصال به دیتابیس");
        } catch (SQLException e) {
            throw new DatabaseException("خطا در اتصال به دیتابیس", e);
        }
    }
}

// Custom Exception for wrapping
class DatabaseException extends Exception {
    public DatabaseException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

### آنالوژی دنیای واقعی:
Exception Handling مانند سیستم امنیتی یک ساختمان است:
- **Try Block:** مانند ورود به ساختمان
- **Catch Block:** مانند سیستم هشدار که در صورت مشکل فعال می‌شود
- **Finally Block:** مانند خروج اضطراری که همیشه در دسترس است
- **Custom Exceptions:** مانند قوانین خاص ساختمان که باید رعایت شوند

## 1.5 Input/Output (I/O) Operations

عملیات ورودی/خروجی (I/O) برای خواندن و نوشتن داده‌ها از منابع مختلف استفاده می‌شود.

### انواع I/O Streams:

**1. Byte Streams:**
- برای داده‌های باینری
- FileInputStream, FileOutputStream
- BufferedInputStream, BufferedOutputStream

**2. Character Streams:**
- برای داده‌های متنی
- FileReader, FileWriter
- BufferedReader, BufferedWriter

**3. Object Streams:**
- برای serialization
- ObjectInputStream, ObjectOutputStream

### مثال عملی:

```java
import java.io.*;
import java.util.*;

public class IOOperationsExample {
    public static void main(String[] args) {
        // 1. File Reading and Writing
        System.out.println("=== File Operations ===");
        
        // Write to file
        writeToFile("sample.txt", "سلام دنیا!\nاین یک فایل نمونه است.");
        
        // Read from file
        readFromFile("sample.txt");
        
        // 2. Buffered I/O
        System.out.println("\n=== Buffered I/O ===");
        
        writeWithBuffering("buffered.txt", "داده‌های بافر شده");
        readWithBuffering("buffered.txt");
        
        // 3. Object Serialization
        System.out.println("\n=== Object Serialization ===");
        
        Person person = new Person("احمد", 25, "تهران");
        serializeObject(person, "person.ser");
        
        Person deserializedPerson = deserializeObject("person.ser");
        if (deserializedPerson != null) {
            System.out.println("شخص deserialize شده: " + deserializedPerson);
        }
        
        // 4. Console Input
        System.out.println("\n=== Console Input ===");
        readFromConsole();
    }
    
    // File Writing
    public static void writeToFile(String filename, String content) {
        try (FileWriter writer = new FileWriter(filename)) {
            writer.write(content);
            System.out.println("فایل " + filename + " با موفقیت نوشته شد");
        } catch (IOException e) {
            System.err.println("خطا در نوشتن فایل: " + e.getMessage());
        }
    }
    
    // File Reading
    public static void readFromFile(String filename) {
        try (FileReader reader = new FileReader(filename)) {
            int character;
            System.out.println("محتوای فایل " + filename + ":");
            while ((character = reader.read()) != -1) {
                System.out.print((char) character);
            }
            System.out.println();
        } catch (IOException e) {
            System.err.println("خطا در خواندن فایل: " + e.getMessage());
        }
    }
    
    // Buffered Writing
    public static void writeWithBuffering(String filename, String content) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            writer.write(content);
            writer.newLine();
            writer.write("خط دوم");
            System.out.println("فایل بافر شده نوشته شد");
        } catch (IOException e) {
            System.err.println("خطا در نوشتن بافر: " + e.getMessage());
        }
    }
    
    // Buffered Reading
    public static void readWithBuffering(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            System.out.println("خواندن بافر شده:");
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.err.println("خطا در خواندن بافر: " + e.getMessage());
        }
    }
    
    // Object Serialization
    public static void serializeObject(Person person, String filename) {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(filename))) {
            oos.writeObject(person);
            System.out.println("Object serialize شد");
        } catch (IOException e) {
            System.err.println("خطا در serialization: " + e.getMessage());
        }
    }
    
    // Object Deserialization
    public static Person deserializeObject(String filename) {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(filename))) {
            return (Person) ois.readObject();
        } catch (IOException | ClassNotFoundException e) {
            System.err.println("خطا در deserialization: " + e.getMessage());
            return null;
        }
    }
    
    // Console Input
    public static void readFromConsole() {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("نام خود را وارد کنید: ");
        String name = scanner.nextLine();
        
        System.out.print("سن خود را وارد کنید: ");
        int age = scanner.nextInt();
        
        System.out.println("سلام " + name + "! شما " + age + " سال دارید.");
        
        scanner.close();
    }
}

// Serializable Person class
class Person implements Serializable {
    private static final long serialVersionUID = 1L;
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
        return "Person{name='" + name + "', age=" + age + ", city='" + city + "'}";
    }
    
    // Getters and Setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }
}
```

### Advanced I/O Operations:

```java
import java.io.*;
import java.nio.file.*;
import java.util.stream.Stream;

public class AdvancedIOExample {
    public static void main(String[] args) {
        // 1. NIO.2 File Operations
        System.out.println("=== NIO.2 File Operations ===");
        
        try {
            // Create directory
            Path dir = Paths.get("test_directory");
            Files.createDirectories(dir);
            System.out.println("پوشه ایجاد شد: " + dir);
            
            // Create file
            Path file = dir.resolve("test.txt");
            Files.write(file, "محتوای فایل تست".getBytes());
            System.out.println("فایل ایجاد شد: " + file);
            
            // Read file
            String content = new String(Files.readAllBytes(file));
            System.out.println("محتوای فایل: " + content);
            
            // List directory contents
            System.out.println("محتوای پوشه:");
            try (Stream<Path> paths = Files.list(dir)) {
                paths.forEach(System.out::println);
            }
            
        } catch (IOException e) {
            System.err.println("خطا در عملیات NIO: " + e.getMessage());
        }
        
        // 2. File Properties
        System.out.println("\n=== File Properties ===");
        
        try {
            Path file = Paths.get("sample.txt");
            if (Files.exists(file)) {
                System.out.println("اندازه فایل: " + Files.size(file) + " بایت");
                System.out.println("آیا فایل است: " + Files.isRegularFile(file));
                System.out.println("آیا قابل خواندن است: " + Files.isReadable(file));
                System.out.println("آیا قابل نوشتن است: " + Files.isWritable(file));
            }
        } catch (IOException e) {
            System.err.println("خطا در بررسی خصوصیات فایل: " + e.getMessage());
        }
    }
}
```

### آنالوژی دنیای واقعی:
I/O Operations مانند سیستم پست است:
- **File Reading:** مانند دریافت نامه از صندوق پستی
- **File Writing:** مانند ارسال نامه از صندوق پستی
- **Buffering:** مانند استفاده از سبد برای حمل چندین نامه
- **Serialization:** مانند بسته‌بندی اشیاء برای ارسال
- **Streams:** مانند لوله‌های آب که داده‌ها از آن‌ها جریان می‌یابند

## 1.6 Memory Management & Garbage Collection

مدیریت حافظه و Garbage Collection یکی از مهم‌ترین جنبه‌های Java است که به صورت خودکار انجام می‌شود.

### مفاهیم کلیدی Memory Management:

**1. Heap Memory:**
- محل ذخیره objects
- به صورت خودکار مدیریت می‌شود
- Garbage Collection در اینجا عمل می‌کند

**2. Stack Memory:**
- محل ذخیره local variables و method calls
- LIFO (Last In, First Out)
- به صورت خودکار آزاد می‌شود

**3. Method Area:**
- محل ذخیره class information
- Static variables
- Constant pool

### انواع Garbage Collectors:

**1. Serial GC:**
- برای single-threaded applications
- مناسب برای applications کوچک

**2. Parallel GC:**
- برای multi-threaded applications
- Default در Java 8

**3. G1 GC:**
- برای applications با heap بزرگ
- Low-latency garbage collection

**4. ZGC:**
- برای applications با heap بسیار بزرگ
- Ultra-low latency

### مثال عملی:

```java
public class MemoryManagementExample {
    private static final int MEGABYTE = 1024 * 1024;
    
    public static void main(String[] args) {
        // 1. Memory Information
        System.out.println("=== Memory Information ===");
        displayMemoryInfo();
        
        // 2. Object Creation and Garbage Collection
        System.out.println("\n=== Object Creation ===");
        createObjects();
        
        // 3. Memory Leak Example
        System.out.println("\n=== Memory Leak Prevention ===");
        demonstrateMemoryLeakPrevention();
        
        // 4. Garbage Collection Triggers
        System.out.println("\n=== Garbage Collection ===");
        triggerGarbageCollection();
        
        // 5. Finalizer Example
        System.out.println("\n=== Finalizer Example ===");
        demonstrateFinalizer();
    }
    
    public static void displayMemoryInfo() {
        Runtime runtime = Runtime.getRuntime();
        
        long totalMemory = runtime.totalMemory() / MEGABYTE;
        long freeMemory = runtime.freeMemory() / MEGABYTE;
        long usedMemory = totalMemory - freeMemory;
        long maxMemory = runtime.maxMemory() / MEGABYTE;
        
        System.out.println("حافظه کل: " + totalMemory + " MB");
        System.out.println("حافظه آزاد: " + freeMemory + " MB");
        System.out.println("حافظه استفاده شده: " + usedMemory + " MB");
        System.out.println("حداکثر حافظه: " + maxMemory + " MB");
    }
    
    public static void createObjects() {
        // Create large objects
        for (int i = 0; i < 1000; i++) {
            String largeString = new String("Large string " + i + " " + 
                "x".repeat(1000));
            // Object will be eligible for GC after this iteration
        }
        
        System.out.println("1000 object ایجاد شد");
        displayMemoryInfo();
        
        // Force garbage collection
        System.gc();
        System.out.println("Garbage Collection اجرا شد");
        displayMemoryInfo();
    }
    
    public static void demonstrateMemoryLeakPrevention() {
        // Good practice: Use try-with-resources
        try (Resource resource = new Resource()) {
            resource.doSomething();
        } // Resource automatically closed
        
        // Bad practice: Manual resource management (can cause leaks)
        Resource resource = new Resource();
        try {
            resource.doSomething();
        } finally {
            resource.close(); // Must remember to close
        }
    }
    
    public static void triggerGarbageCollection() {
        // Create objects
        for (int i = 0; i < 10000; i++) {
            new String("Object " + i);
        }
        
        System.out.println("قبل از GC:");
        displayMemoryInfo();
        
        // Suggest garbage collection
        System.gc();
        
        // Wait a bit for GC to complete
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        System.out.println("بعد از GC:");
        displayMemoryInfo();
    }
    
    public static void demonstrateFinalizer() {
        // Create object with finalizer
        FinalizerExample obj = new FinalizerExample("Test Object");
        obj = null; // Make object eligible for GC
        
        // Force garbage collection
        System.gc();
        
        // Wait for finalizer to run
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

// Resource class for demonstration
class Resource implements AutoCloseable {
    private boolean closed = false;
    
    public void doSomething() {
        if (closed) {
            throw new IllegalStateException("Resource is closed");
        }
        System.out.println("Resource در حال استفاده");
    }
    
    @Override
    public void close() {
        if (!closed) {
            closed = true;
            System.out.println("Resource بسته شد");
        }
    }
}

// Class with finalizer
class FinalizerExample {
    private String name;
    
    public FinalizerExample(String name) {
        this.name = name;
        System.out.println("Object ایجاد شد: " + name);
    }
    
    @Override
    protected void finalize() throws Throwable {
        try {
            System.out.println("Finalizer اجرا شد برای: " + name);
        } finally {
            super.finalize();
        }
    }
}
```

### Memory Optimization Techniques:

```java
public class MemoryOptimization {
    
    // 1. Object Pooling
    private static final ObjectPool<StringBuilder> stringBuilderPool = 
        new ObjectPool<>(StringBuilder::new);
    
    public static void main(String[] args) {
        // 1. String Optimization
        System.out.println("=== String Optimization ===");
        demonstrateStringOptimization();
        
        // 2. Collection Optimization
        System.out.println("\n=== Collection Optimization ===");
        demonstrateCollectionOptimization();
        
        // 3. Object Pooling
        System.out.println("\n=== Object Pooling ===");
        demonstrateObjectPooling();
    }
    
    public static void demonstrateStringOptimization() {
        // Bad: String concatenation in loop
        String badResult = "";
        for (int i = 0; i < 1000; i++) {
            badResult += "item" + i; // Creates many temporary objects
        }
        
        // Good: StringBuilder
        StringBuilder goodResult = new StringBuilder();
        for (int i = 0; i < 1000; i++) {
            goodResult.append("item").append(i);
        }
        
        System.out.println("String concatenation completed");
    }
    
    public static void demonstrateCollectionOptimization() {
        // Bad: Default capacity
        List<String> badList = new ArrayList<>();
        
        // Good: Pre-allocate capacity
        List<String> goodList = new ArrayList<>(1000);
        
        // Good: Use appropriate collection type
        Set<String> uniqueItems = new HashSet<>(1000);
        
        System.out.println("Collection optimization completed");
    }
    
    public static void demonstrateObjectPooling() {
        // Get StringBuilder from pool
        StringBuilder sb = stringBuilderPool.get();
        try {
            sb.append("Hello World");
            System.out.println(sb.toString());
        } finally {
            // Return to pool
            stringBuilderPool.returnObject(sb);
        }
    }
}

// Simple Object Pool implementation
class ObjectPool<T> {
    private final Queue<T> pool = new LinkedList<>();
    private final Supplier<T> factory;
    
    public ObjectPool(Supplier<T> factory) {
        this.factory = factory;
    }
    
    public T get() {
        T obj = pool.poll();
        if (obj == null) {
            obj = factory.get();
        }
        return obj;
    }
    
    public void returnObject(T obj) {
        if (obj != null) {
            pool.offer(obj);
        }
    }
}
```

### آنالوژی دنیای واقعی:
Memory Management مانند مدیریت فضای پارکینگ است:
- **Heap:** مانند پارکینگ بزرگ که ماشین‌ها (objects) در آن پارک می‌شوند
- **Stack:** مانند صف ورودی که ماشین‌ها به ترتیب وارد می‌شوند
- **Garbage Collection:** مانند کارگران نظافت که ماشین‌های خالی را شناسایی و حذف می‌کنند
- **Memory Leaks:** مانند ماشین‌هایی که پارک شده‌اند اما کلید آن‌ها گم شده است