# Section 10 - Java 12-14 - Rapid Release Cycle

## 10.1 Switch Expressions (Preview)

Switch Expressions یکی از مهم‌ترین ویژگی‌های Java 12 بود که به صورت preview معرفی شد و در Java 14 به صورت نهایی درآمد. این ویژگی نحوه نوشتن switch statements را بهبود بخشید.

### مفاهیم کلیدی:

**1. Expression-based Switch:**
- Switch به عنوان expression عمل می‌کند
- می‌تواند مقدار return کند
- نیازی به break statements نیست

**2. Arrow Syntax:**
- استفاده از `->` به جای `:`
- کد تمیزتر و خوانا‌تر
- Multiple case labels

**3. Yield Statement:**
- برای return کردن مقادیر در switch blocks
- جایگزین break + return

### مثال عملی:

```java
public class SwitchExpressionsExample {
    
    // Traditional switch statement
    public static String getDayTypeTraditional(Day day) {
        String type;
        switch (day) {
            case MONDAY:
            case TUESDAY:
            case WEDNESDAY:
            case THURSDAY:
            case FRIDAY:
                type = "Working day";
                break;
            case SATURDAY:
            case SUNDAY:
                type = "Weekend";
                break;
            default:
                type = "Unknown";
                break;
        }
        return type;
    }
    
    // Switch expression (Java 12+)
    public static String getDayTypeExpression(Day day) {
        return switch (day) {
            case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "Working day";
            case SATURDAY, SUNDAY -> "Weekend";
            default -> "Unknown";
        };
    }
    
    // Switch expression with yield
    public static int getDayNumber(Day day) {
        return switch (day) {
            case MONDAY -> 1;
            case TUESDAY -> 2;
            case WEDNESDAY -> 3;
            case THURSDAY -> 4;
            case FRIDAY -> 5;
            case SATURDAY -> 6;
            case SUNDAY -> 7;
        };
    }
    
    // Complex switch expression
    public static String getGradeDescription(int score) {
        return switch (score / 10) {
            case 10 -> "Perfect!";
            case 9 -> "Excellent";
            case 8 -> "Very Good";
            case 7 -> "Good";
            case 6 -> "Satisfactory";
            case 5 -> "Pass";
            case 4, 3, 2, 1, 0 -> "Fail";
            default -> "Invalid score";
        };
    }
    
    // Switch expression with blocks
    public static String processNumber(int number) {
        return switch (number) {
            case 0 -> "Zero";
            case 1 -> "One";
            case 2 -> "Two";
            default -> {
                if (number > 0) {
                    yield "Positive number: " + number;
                } else {
                    yield "Negative number: " + number;
                }
            }
        };
    }
    
    public static void main(String[] args) {
        System.out.println("=== Switch Expressions Examples ===");
        
        // Test traditional vs expression
        Day today = Day.MONDAY;
        System.out.println("Traditional: " + getDayTypeTraditional(today));
        System.out.println("Expression: " + getDayTypeExpression(today));
        
        // Test day numbers
        for (Day day : Day.values()) {
            System.out.println(day + " -> " + getDayNumber(day));
        }
        
        // Test grade descriptions
        int[] scores = {95, 87, 76, 65, 45, 30};
        for (int score : scores) {
            System.out.println("Score " + score + ": " + getGradeDescription(score));
        }
        
        // Test number processing
        int[] numbers = {0, 1, 2, 5, -3, 100};
        for (int number : numbers) {
            System.out.println("Number " + number + ": " + processNumber(number));
        }
    }
}

enum Day {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}
```

### مزایای Switch Expressions:

```java
public class SwitchExpressionsAdvantages {
    
    // 1. No fall-through issues
    public static String getSeasonTraditional(int month) {
        String season;
        switch (month) {
            case 12:
            case 1:
            case 2:
                season = "Winter";
                break;
            case 3:
            case 4:
            case 5:
                season = "Spring";
                break;
            case 6:
            case 7:
            case 8:
                season = "Summer";
                break;
            case 9:
            case 10:
            case 11:
                season = "Autumn";
                break;
            default:
                season = "Invalid month";
                break;
        }
        return season;
    }
    
    // 2. Cleaner with switch expression
    public static String getSeasonExpression(int month) {
        return switch (month) {
            case 12, 1, 2 -> "Winter";
            case 3, 4, 5 -> "Spring";
            case 6, 7, 8 -> "Summer";
            case 9, 10, 11 -> "Autumn";
            default -> "Invalid month";
        };
    }
    
    // 3. Compile-time exhaustiveness checking
    public static String getTrafficLightColor(TrafficLight light) {
        return switch (light) {
            case RED -> "Stop";
            case YELLOW -> "Caution";
            case GREEN -> "Go";
            // Compiler ensures all cases are covered
        };
    }
    
    public static void main(String[] args) {
        System.out.println("=== Switch Expressions Advantages ===");
        
        // Test season methods
        for (int month = 1; month <= 12; month++) {
            System.out.println("Month " + month + ": " + getSeasonExpression(month));
        }
        
        // Test traffic light
        for (TrafficLight light : TrafficLight.values()) {
            System.out.println(light + ": " + getTrafficLightColor(light));
        }
    }
}

enum TrafficLight {
    RED, YELLOW, GREEN
}
```

### آنالوژی دنیای واقعی:
Switch Expressions مانند داشتن یک ماشین حساب پیشرفته است. به جای اینکه مجبور باشید هر بار دکمه "=" را فشار دهید (break)، ماشین حساب به صورت خودکار نتیجه را محاسبه و نمایش می‌دهد.

## 10.2 Text Blocks (Preview)

Text Blocks در Java 13 به صورت preview معرفی شد و در Java 15 به صورت نهایی درآمد. این ویژگی نوشتن رشته‌های چندخطی را بسیار ساده‌تر کرد.

### مفاهیم کلیدی:

**1. Triple Quotes:**
- استفاده از `"""` برای شروع و پایان
- Multiline strings بدون escape characters
- Automatic formatting

**2. Indentation Handling:**
- Incidental whitespace removal
- Preserving essential whitespace
- Consistent indentation

**3. Escape Sequences:**
- Support for traditional escape sequences
- New escape sequences for text blocks
- Line continuation

### مثال عملی:

```java
public class TextBlocksExample {
    
    public static void main(String[] args) {
        System.out.println("=== Text Blocks Examples ===");
        
        // 1. Basic text block
        String html = """
            <html>
                <body>
                    <h1>Hello World</h1>
                    <p>This is a text block example</p>
                </body>
            </html>
            """;
        System.out.println("HTML:");
        System.out.println(html);
        
        // 2. JSON example
        String json = """
            {
                "name": "احمد محمدی",
                "age": 25,
                "city": "تهران",
                "skills": ["Java", "Spring", "Microservices"]
            }
            """;
        System.out.println("\nJSON:");
        System.out.println(json);
        
        // 3. SQL query
        String sql = """
            SELECT u.id, u.name, u.email, p.title
            FROM users u
            LEFT JOIN posts p ON u.id = p.user_id
            WHERE u.active = true
            AND p.created_at > '2024-01-01'
            ORDER BY u.name, p.created_at DESC
            """;
        System.out.println("\nSQL Query:");
        System.out.println(sql);
        
        // 4. Configuration file
        String config = """
            # Application Configuration
            server.port=8080
            server.host=localhost
            
            # Database Configuration
            db.url=jdbc:mysql://localhost:3306/myapp
            db.username=admin
            db.password=secret
            
            # Logging Configuration
            logging.level.com.myapp=DEBUG
            logging.file=logs/application.log
            """;
        System.out.println("\nConfiguration:");
        System.out.println(config);
        
        // 5. Text block with variables
        String name = "فاطمه احمدی";
        int age = 30;
        String city = "اصفهان";
        
        String profile = """
            نام: %s
            سن: %d
            شهر: %s
            """.formatted(name, age, city);
        System.out.println("\nProfile:");
        System.out.println(profile);
        
        // 6. Text block with escape sequences
        String code = """
            public class Example {
                public static void main(String[] args) {
                    System.out.println("Hello \\"World\\"");
                    System.out.println("Line 1\\nLine 2");
                }
            }
            """;
        System.out.println("\nCode with escapes:");
        System.out.println(code);
    }
}
```

### مقایسه با String Concatenation:

```java
public class TextBlocksComparison {
    
    public static void main(String[] args) {
        System.out.println("=== Text Blocks vs String Concatenation ===");
        
        // Traditional string concatenation
        String traditionalHtml = "<html>\n" +
            "    <body>\n" +
            "        <h1>Hello World</h1>\n" +
            "        <p>This is a traditional string</p>\n" +
            "    </body>\n" +
            "</html>";
        
        // Text block
        String textBlockHtml = """
            <html>
                <body>
                    <h1>Hello World</h1>
                    <p>This is a text block</p>
                </body>
            </html>
            """;
        
        System.out.println("Traditional:");
        System.out.println(traditionalHtml);
        System.out.println("\nText Block:");
        System.out.println(textBlockHtml);
        
        // Complex example - Email template
        String recipient = "user@example.com";
        String subject = "Welcome to our service";
        
        // Traditional approach
        String traditionalEmail = "Dear " + recipient + ",\n\n" +
            "Thank you for signing up for our service!\n\n" +
            "Your account has been created successfully.\n" +
            "Please click the link below to activate your account:\n\n" +
            "https://example.com/activate?token=abc123\n\n" +
            "If you have any questions, please contact our support team.\n\n" +
            "Best regards,\n" +
            "The Team";
        
        // Text block approach
        String textBlockEmail = """
            Dear %s,
            
            Thank you for signing up for our service!
            
            Your account has been created successfully.
            Please click the link below to activate your account:
            
            https://example.com/activate?token=abc123
            
            If you have any questions, please contact our support team.
            
            Best regards,
            The Team
            """.formatted(recipient);
        
        System.out.println("\n=== Email Templates ===");
        System.out.println("Traditional:");
        System.out.println(traditionalEmail);
        System.out.println("\nText Block:");
        System.out.println(textBlockEmail);
    }
}
```

### آنالوژی دنیای واقعی:
Text Blocks مانند داشتن یک دفترچه یادداشت بزرگ برای نوشتن متن‌های طولانی است. به جای اینکه مجبور باشید هر خط را جداگانه بنویسید و از علامت‌های خاص استفاده کنید، می‌توانید کل متن را به صورت طبیعی بنویسید.

## 10.3 Pattern Matching for instanceof (Preview)

Pattern Matching for instanceof در Java 14 به صورت preview معرفی شد و در Java 16 به صورت نهایی درآمد. این ویژگی instanceof checks را ساده‌تر و قدرتمندتر کرد.

### مفاهیم کلیدی:

**1. Pattern Variables:**
- تعریف متغیر در همان instanceof check
- Scope محدود به if block
- Type safety

**2. Eliminates Casting:**
- نیازی به explicit casting نیست
- Compiler type checking
- Cleaner code

**3. Enhanced instanceof:**
- ترکیب instanceof و variable declaration
- Better readability
- Reduced boilerplate

### مثال عملی:

```java
public class PatternMatchingExample {
    
    public static void main(String[] args) {
        System.out.println("=== Pattern Matching for instanceof ===");
        
        // Test with different object types
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
    
    // Traditional approach
    public static void processObjectTraditional(Object obj) {
        if (obj instanceof String) {
            String str = (String) obj; // Explicit casting
            System.out.println("String length: " + str.length());
        } else if (obj instanceof Integer) {
            Integer num = (Integer) obj; // Explicit casting
            System.out.println("Integer value: " + num);
        } else if (obj instanceof Double) {
            Double dbl = (Double) obj; // Explicit casting
            System.out.println("Double value: " + dbl);
        } else if (obj instanceof int[]) {
            int[] arr = (int[]) obj; // Explicit casting
            System.out.println("Array length: " + arr.length);
        } else if (obj instanceof Person) {
            Person person = (Person) obj; // Explicit casting
            System.out.println("Person: " + person.getName());
        } else {
            System.out.println("Unknown type");
        }
    }
    
    // Pattern matching approach
    public static void processObject(Object obj) {
        if (obj instanceof String str) {
            System.out.println("String length: " + str.length());
        } else if (obj instanceof Integer num) {
            System.out.println("Integer value: " + num);
        } else if (obj instanceof Double dbl) {
            System.out.println("Double value: " + dbl);
        } else if (obj instanceof int[] arr) {
            System.out.println("Array length: " + arr.length);
        } else if (obj instanceof Person person) {
            System.out.println("Person: " + person.getName());
        } else {
            System.out.println("Unknown type");
        }
    }
    
    // Complex pattern matching
    public static void processShape(Object shape) {
        if (shape instanceof Circle circle) {
            System.out.println("Circle with radius: " + circle.getRadius());
            System.out.println("Area: " + circle.getArea());
        } else if (shape instanceof Rectangle rect) {
            System.out.println("Rectangle: " + rect.getWidth() + "x" + rect.getHeight());
            System.out.println("Area: " + rect.getArea());
        } else if (shape instanceof Triangle triangle) {
            System.out.println("Triangle with sides: " + triangle.getSide1() + 
                             ", " + triangle.getSide2() + ", " + triangle.getSide3());
        } else {
            System.out.println("Unknown shape");
        }
    }
    
    // Pattern matching with conditions
    public static void processNumber(Object obj) {
        if (obj instanceof Integer num && num > 0) {
            System.out.println("Positive integer: " + num);
        } else if (obj instanceof Integer num && num < 0) {
            System.out.println("Negative integer: " + num);
        } else if (obj instanceof Double dbl && dbl > 0) {
            System.out.println("Positive double: " + dbl);
        } else if (obj instanceof String str && str.length() > 5) {
            System.out.println("Long string: " + str);
        } else {
            System.out.println("Other: " + obj);
        }
    }
}

// Supporting classes
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

class Circle {
    private double radius;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    public double getRadius() { return radius; }
    public double getArea() { return Math.PI * radius * radius; }
}

class Rectangle {
    private double width, height;
    
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
    
    public double getWidth() { return width; }
    public double getHeight() { return height; }
    public double getArea() { return width * height; }
}

class Triangle {
    private double side1, side2, side3;
    
    public Triangle(double side1, double side2, double side3) {
        this.side1 = side1;
        this.side2 = side2;
        this.side3 = side3;
    }
    
    public double getSide1() { return side1; }
    public double getSide2() { return side2; }
    public double getSide3() { return side3; }
}
```

### مزایای Pattern Matching:

```java
public class PatternMatchingAdvantages {
    
    public static void main(String[] args) {
        System.out.println("=== Pattern Matching Advantages ===");
        
        // 1. Eliminates casting
        Object obj = "Hello World";
        
        // Traditional way
        if (obj instanceof String) {
            String str = (String) obj; // Casting required
            System.out.println("Length: " + str.length());
        }
        
        // Pattern matching way
        if (obj instanceof String str) {
            System.out.println("Length: " + str.length()); // No casting
        }
        
        // 2. Better readability
        processAnimal(new Dog("Rex"));
        processAnimal(new Cat("Whiskers"));
        processAnimal(new Bird("Tweety"));
    }
    
    public static void processAnimal(Object animal) {
        if (animal instanceof Dog dog) {
            System.out.println("Dog: " + dog.getName() + " barks");
        } else if (animal instanceof Cat cat) {
            System.out.println("Cat: " + cat.getName() + " meows");
        } else if (animal instanceof Bird bird) {
            System.out.println("Bird: " + bird.getName() + " chirps");
        }
    }
}

class Dog {
    private String name;
    public Dog(String name) { this.name = name; }
    public String getName() { return name; }
}

class Cat {
    private String name;
    public Cat(String name) { this.name = name; }
    public String getName() { return name; }
}

class Bird {
    private String name;
    public Bird(String name) { this.name = name; }
    public String getName() { return name; }
}
```

### آنالوژی دنیای واقعی:
Pattern Matching مانند داشتن یک سیستم تشخیص هوشمند است. به جای اینکه ابتدا بپرسید "آیا این یک ماشین است؟" و سپس "اگر ماشین است، آن را به عنوان ماشین استفاده کنید"، می‌توانید بگویید "اگر این یک ماشین است، آن را به عنوان ماشین استفاده کن".

## 10.4 Records (Preview)

Records در Java 14 به صورت preview معرفی شد و در Java 16 به صورت نهایی درآمد. این ویژگی راه ساده‌ای برای ایجاد immutable data classes فراهم می‌کند.

### مفاهیم کلیدی:

**1. Immutable Data Classes:**
- Automatic generation of constructor, getters, equals, hashCode, toString
- Final fields
- No setters

**2. Compact Syntax:**
- `record` keyword
- Header declaration
- Automatic implementations

**3. Enhanced Features:**
- Can implement interfaces
- Can have static methods
- Can have instance methods
- Can have nested classes

### مثال عملی:

```java
public class RecordsExample {
    
    public static void main(String[] args) {
        System.out.println("=== Records Examples ===");
        
        // 1. Basic record
        Person person = new Person("احمد", 25, "تهران");
        System.out.println("Person: " + person);
        System.out.println("Name: " + person.name());
        System.out.println("Age: " + person.age());
        System.out.println("City: " + person.city());
        
        // 2. Record with methods
        Point point1 = new Point(3, 4);
        Point point2 = new Point(3, 4);
        Point point3 = new Point(5, 6);
        
        System.out.println("\nPoint 1: " + point1);
        System.out.println("Distance from origin: " + point1.distanceFromOrigin());
        System.out.println("Point 1 equals Point 2: " + point1.equals(point2));
        System.out.println("Point 1 equals Point 3: " + point1.equals(point3));
        
        // 3. Record with validation
        try {
            Email email = new Email("user@example.com");
            System.out.println("\nValid email: " + email);
        } catch (IllegalArgumentException e) {
            System.out.println("Invalid email: " + e.getMessage());
        }
        
        // 4. Record with static methods
        Rectangle rect = Rectangle.create(10, 20);
        System.out.println("\nRectangle: " + rect);
        System.out.println("Area: " + rect.area());
        System.out.println("Perimeter: " + rect.perimeter());
        
        // 5. Record implementing interface
        Circle circle = new Circle(5.0);
        System.out.println("\nCircle: " + circle);
        System.out.println("Area: " + circle.area());
        System.out.println("Perimeter: " + circle.perimeter());
        
        // 6. Record with nested classes
        Student student = new Student("فاطمه", 20, "Computer Science");
        System.out.println("\nStudent: " + student);
        System.out.println("Is graduate: " + student.isGraduate());
    }
}

// Basic record
record Person(String name, int age, String city) {}

// Record with methods
record Point(int x, int y) {
    public double distanceFromOrigin() {
        return Math.sqrt(x * x + y * y);
    }
    
    public double distanceTo(Point other) {
        return Math.sqrt(Math.pow(x - other.x, 2) + Math.pow(y - other.y, 2));
    }
}

// Record with validation
record Email(String address) {
    public Email {
        if (address == null || !address.contains("@")) {
            throw new IllegalArgumentException("Invalid email address");
        }
    }
}

// Record with static methods
record Rectangle(double width, double height) {
    public static Rectangle create(double width, double height) {
        if (width <= 0 || height <= 0) {
            throw new IllegalArgumentException("Width and height must be positive");
        }
        return new Rectangle(width, height);
    }
    
    public double area() {
        return width * height;
    }
    
    public double perimeter() {
        return 2 * (width + height);
    }
}

// Record implementing interface
record Circle(double radius) implements Shape {
    public double area() {
        return Math.PI * radius * radius;
    }
    
    public double perimeter() {
        return 2 * Math.PI * radius;
    }
}

// Record with nested classes
record Student(String name, int age, String major) {
    public boolean isGraduate() {
        return age >= 22;
    }
    
    // Nested record
    public record Course(String name, int credits) {}
    
    // Nested class
    public static class Enrollment {
        private final Student student;
        private final Course course;
        
        public Enrollment(Student student, Course course) {
            this.student = student;
            this.course = course;
        }
        
        public Student getStudent() { return student; }
        public Course getCourse() { return course; }
    }
}

// Interface for shapes
interface Shape {
    double area();
    double perimeter();
}
```

### مقایسه با Traditional Classes:

```java
public class RecordsComparison {
    
    public static void main(String[] args) {
        System.out.println("=== Records vs Traditional Classes ===");
        
        // Traditional class
        TraditionalPerson traditionalPerson = new TraditionalPerson("احمد", 25, "تهران");
        
        // Record
        PersonRecord personRecord = new PersonRecord("احمد", 25, "تهران");
        
        System.out.println("Traditional: " + traditionalPerson);
        System.out.println("Record: " + personRecord);
        
        // Both have same functionality
        System.out.println("Traditional equals: " + traditionalPerson.equals(new TraditionalPerson("احمد", 25, "تهران")));
        System.out.println("Record equals: " + personRecord.equals(new PersonRecord("احمد", 25, "تهران")));
    }
}

// Traditional class
class TraditionalPerson {
    private final String name;
    private final int age;
    private final String city;
    
    public TraditionalPerson(String name, int age, String city) {
        this.name = name;
        this.age = age;
        this.city = city;
    }
    
    public String getName() { return name; }
    public int getAge() { return age; }
    public String getCity() { return city; }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        TraditionalPerson that = (TraditionalPerson) obj;
        return age == that.age && 
               Objects.equals(name, that.name) && 
               Objects.equals(city, that.city);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(name, age, city);
    }
    
    @Override
    public String toString() {
        return "TraditionalPerson{" +
               "name='" + name + '\'' +
               ", age=" + age +
               ", city='" + city + '\'' +
               '}';
    }
}

// Record equivalent
record PersonRecord(String name, int age, String city) {}
```

### آنالوژی دنیای واقعی:
Records مانند داشتن یک فرم استاندارد برای ثبت اطلاعات است. به جای اینکه مجبور باشید هر بار فرم را از ابتدا بنویسید، می‌توانید از فرم آماده استفاده کنید که تمام فیلدهای لازم و قوانین را دارد.

## 10.5 Sealed Classes (Preview)

Sealed Classes در Java 15 به صورت preview معرفی شد و در Java 17 به صورت نهایی درآمد. این ویژگی کنترل بهتری بر inheritance فراهم می‌کند.

### مفاهیم کلیدی:

**1. Restricted Inheritance:**
- تعریف کلاس‌هایی که فقط کلاس‌های مشخص می‌توانند از آن‌ها ارث ببرند
- کنترل کامل بر class hierarchy
- Compile-time checking

**2. Sealed Keyword:**
- `sealed` برای تعریف sealed class
- `permits` برای مشخص کردن subclasses مجاز
- `final` یا `sealed` یا `non-sealed` برای subclasses

**3. Pattern Matching Integration:**
- کار بهتر با pattern matching
- Exhaustive checking
- Type safety

### مثال عملی:

```java
public class SealedClassesExample {
    
    public static void main(String[] args) {
        System.out.println("=== Sealed Classes Examples ===");
        
        // Test different shapes
        Shape[] shapes = {
            new Circle(5.0),
            new Rectangle(10, 20),
            new Triangle(3, 4, 5),
            new Square(6)
        };
        
        for (Shape shape : shapes) {
            processShape(shape);
        }
        
        // Test different animals
        Animal[] animals = {
            new Dog("Rex"),
            new Cat("Whiskers"),
            new Bird("Tweety")
        };
        
        for (Animal animal : animals) {
            processAnimal(animal);
        }
    }
    
    // Pattern matching with sealed classes
    public static void processShape(Shape shape) {
        System.out.println("Processing shape: " + shape);
        
        // Exhaustive pattern matching
        String result = switch (shape) {
            case Circle c -> "Circle with radius " + c.radius() + ", area: " + c.area();
            case Rectangle r -> "Rectangle " + r.width() + "x" + r.height() + ", area: " + r.area();
            case Triangle t -> "Triangle with sides " + t.side1() + ", " + t.side2() + ", " + t.side3();
            case Square s -> "Square with side " + s.side() + ", area: " + s.area();
        };
        
        System.out.println("Result: " + result);
    }
    
    public static void processAnimal(Animal animal) {
        System.out.println("Processing animal: " + animal);
        
        String sound = switch (animal) {
            case Dog d -> d.name() + " barks";
            case Cat c -> c.name() + " meows";
            case Bird b -> b.name() + " chirps";
        };
        
        System.out.println("Sound: " + sound);
    }
}

// Sealed class hierarchy for shapes
sealed class Shape permits Circle, Rectangle, Triangle, Square {
    public abstract double area();
}

record Circle(double radius) extends Shape {
    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}

record Rectangle(double width, double height) extends Shape {
    @Override
    public double area() {
        return width * height;
    }
}

record Triangle(double side1, double side2, double side3) extends Shape {
    @Override
    public double area() {
        // Heron's formula
        double s = (side1 + side2 + side3) / 2;
        return Math.sqrt(s * (s - side1) * (s - side2) * (s - side3));
    }
}

record Square(double side) extends Shape {
    @Override
    public double area() {
        return side * side;
    }
}

// Sealed class hierarchy for animals
sealed class Animal permits Dog, Cat, Bird {
    public abstract String name();
}

record Dog(String name) extends Animal {}
record Cat(String name) extends Animal {}
record Bird(String name) extends Animal {}

// Complex sealed hierarchy
sealed class Expression permits Constant, Variable, Add, Multiply {
    public abstract double evaluate();
}

record Constant(double value) extends Expression {
    @Override
    public double evaluate() {
        return value;
    }
}

record Variable(String name) extends Expression {
    @Override
    public double evaluate() {
        throw new UnsupportedOperationException("Variable evaluation requires context");
    }
}

record Add(Expression left, Expression right) extends Expression {
    @Override
    public double evaluate() {
        return left.evaluate() + right.evaluate();
    }
}

record Multiply(Expression left, Expression right) extends Expression {
    @Override
    public double evaluate() {
        return left.evaluate() * right.evaluate();
    }
}
```

### مزایای Sealed Classes:

```java
public class SealedClassesAdvantages {
    
    public static void main(String[] args) {
        System.out.println("=== Sealed Classes Advantages ===");
        
        // 1. Exhaustive pattern matching
        Expression expr = new Add(new Constant(5), new Multiply(new Constant(3), new Constant(2)));
        System.out.println("Expression: " + expr);
        System.out.println("Result: " + evaluateExpression(expr));
        
        // 2. Type safety
        Shape shape = new Circle(5.0);
        // Compiler knows all possible types
        if (shape instanceof Circle circle) {
            System.out.println("Circle radius: " + circle.radius());
        }
    }
    
    public static double evaluateExpression(Expression expr) {
        return switch (expr) {
            case Constant c -> c.value();
            case Variable v -> throw new UnsupportedOperationException("Cannot evaluate variable");
            case Add a -> a.left().evaluate() + a.right().evaluate();
            case Multiply m -> m.left().evaluate() * m.right().evaluate();
        };
    }
}
```

### آنالوژی دنیای واقعی:
Sealed Classes مانند داشتن یک سیستم طبقه‌بندی محدود است. مثلاً در سیستم طبقه‌بندی حیوانات، فقط کلاس‌های مشخصی می‌توانند از "پستانداران" ارث ببرند: سگ، گربه، اسب، و غیره. نمی‌توانید کلاس جدیدی مثل "ماهی" را به عنوان زیرکلاس "پستانداران" تعریف کنید.

## 10.6 Helpful NullPointerExceptions

Helpful NullPointerExceptions در Java 14 معرفی شد و اطلاعات مفصل‌تری درباره NullPointerException ارائه می‌دهد.

### مفاهیم کلیدی:

**1. Detailed Error Messages:**
- نشان دادن دقیق کدام متغیر null است
- مسیر کامل تا null reference
- اطلاعات context بیشتر

**2. Automatic Detection:**
- نیازی به تنظیم خاص نیست
- به صورت خودکار فعال است
- Performance impact minimal

**3. Better Debugging:**
- سریع‌تر پیدا کردن مشکل
- کاهش زمان debugging
- بهبود developer experience

### مثال عملی:

```java
public class HelpfulNullPointerExample {
    
    public static void main(String[] args) {
        System.out.println("=== Helpful NullPointerExceptions ===");
        
        // Test different null pointer scenarios
        testNullPointerScenarios();
    }
    
    public static void testNullPointerScenarios() {
        try {
            // Scenario 1: Simple null reference
            String str = null;
            System.out.println(str.length()); // NullPointerException
        } catch (NullPointerException e) {
            System.out.println("Scenario 1 - Simple null:");
            System.out.println("Exception: " + e.getMessage());
            e.printStackTrace();
        }
        
        try {
            // Scenario 2: Null in method chain
            Person person = null;
            System.out.println(person.getName().toUpperCase()); // NullPointerException
        } catch (NullPointerException e) {
            System.out.println("\nScenario 2 - Method chain:");
            System.out.println("Exception: " + e.getMessage());
            e.printStackTrace();
        }
        
        try {
            // Scenario 3: Null in array access
            String[] names = {"احمد", null, "فاطمه"};
            System.out.println(names[1].length()); // NullPointerException
        } catch (NullPointerException e) {
            System.out.println("\nScenario 3 - Array access:");
            System.out.println("Exception: " + e.getMessage());
            e.printStackTrace();
        }
        
        try {
            // Scenario 4: Null in complex expression
            Person person = new Person("احمد", 25, null);
            System.out.println(person.getAddress().getCity().toUpperCase()); // NullPointerException
        } catch (NullPointerException e) {
            System.out.println("\nScenario 4 - Complex expression:");
            System.out.println("Exception: " + e.getMessage());
            e.printStackTrace();
        }
        
        try {
            // Scenario 5: Null in method parameter
            processName(null); // NullPointerException
        } catch (NullPointerException e) {
            System.out.println("\nScenario 5 - Method parameter:");
            System.out.println("Exception: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    public static void processName(String name) {
        if (name.length() > 0) { // NullPointerException if name is null
            System.out.println("Processing: " + name);
        }
    }
}

class Person {
    private String name;
    private int age;
    private Address address;
    
    public Person(String name, int age, Address address) {
        this.name = name;
        this.age = age;
        this.address = address;
    }
    
    public String getName() { return name; }
    public int getAge() { return age; }
    public Address getAddress() { return address; }
}

class Address {
    private String city;
    private String country;
    
    public Address(String city, String country) {
        this.city = city;
        this.country = country;
    }
    
    public String getCity() { return city; }
    public String getCountry() { return country; }
}
```

### مقایسه با Java قدیمی:

```java
public class NullPointerComparison {
    
    public static void main(String[] args) {
        System.out.println("=== NullPointerException Comparison ===");
        
        // Java 8 and earlier - less helpful
        try {
            String str = null;
            System.out.println(str.length());
        } catch (NullPointerException e) {
            System.out.println("Java 8 style exception:");
            System.out.println("Exception: " + e.getMessage());
            e.printStackTrace();
        }
        
        // Java 14+ - more helpful
        try {
            Person person = new Person("احمد", 25, null);
            System.out.println(person.getAddress().getCity().toUpperCase());
        } catch (NullPointerException e) {
            System.out.println("\nJava 14+ style exception:");
            System.out.println("Exception: " + e.getMessage());
            e.printStackTrace();
        }
    }
}

class Person {
    private String name;
    private int age;
    private Address address;
    
    public Person(String name, int age, Address address) {
        this.name = name;
        this.age = age;
        this.address = address;
    }
    
    public String getName() { return name; }
    public int getAge() { return age; }
    public Address getAddress() { return address; }
}

class Address {
    private String city;
    private String country;
    
    public Address(String city, String country) {
        this.city = city;
        this.country = country;
    }
    
    public String getCity() { return city; }
    public String getCountry() { return country; }
}
```

### آنالوژی دنیای واقعی:
Helpful NullPointerExceptions مانند داشتن یک سیستم هشدار هوشمند است. به جای اینکه فقط بگویید "مشکلی وجود دارد"، سیستم دقیقاً می‌گوید "مشکل در کجاست" و "چه چیزی باعث مشکل شده است".

## 10.7 Packaging Tool (jpackage)

jpackage در Java 14 معرفی شد و ابزاری برای بسته‌بندی Java applications به صورت native packages فراهم می‌کند.

### مفاهیم کلیدی:

**1. Native Packaging:**
- ایجاد executable files
- Platform-specific packages
- Self-contained applications

**2. Multiple Formats:**
- Windows: MSI, EXE
- macOS: DMG, PKG
- Linux: DEB, RPM

**3. JRE Bundling:**
- شامل کردن JRE در package
- No need for separate Java installation
- Smaller distribution size

### مثال عملی:

```java
public class JPackageExample {
    
    public static void main(String[] args) {
        System.out.println("=== JPackage Example Application ===");
        
        // Simple GUI application
        javax.swing.SwingUtilities.invokeLater(() -> {
            createAndShowGUI();
        });
    }
    
    private static void createAndShowGUI() {
        // Create main frame
        JFrame frame = new JFrame("JPackage Example");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 300);
        
        // Create main panel
        JPanel panel = new JPanel();
        panel.setLayout(new BorderLayout());
        
        // Create title label
        JLabel titleLabel = new JLabel("Java Application packaged with jpackage", JLabel.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 16));
        panel.add(titleLabel, BorderLayout.NORTH);
        
        // Create text area
        JTextArea textArea = new JTextArea(10, 30);
        textArea.setEditable(false);
        textArea.setText("This is a sample Java application that can be packaged using jpackage.\n\n" +
                        "Features:\n" +
                        "- Cross-platform packaging\n" +
                        "- Native executable creation\n" +
                        "- JRE bundling\n" +
                        "- Platform-specific installers\n\n" +
                        "To package this application, use:\n" +
                        "jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp");
        
        JScrollPane scrollPane = new JScrollPane(textArea);
        panel.add(scrollPane, BorderLayout.CENTER);
        
        // Create button panel
        JPanel buttonPanel = new JPanel();
        JButton infoButton = new JButton("Show Info");
        JButton exitButton = new JButton("Exit");
        
        infoButton.addActionListener(e -> {
            JOptionPane.showMessageDialog(frame, 
                "Application: JPackage Example\n" +
                "Version: 1.0\n" +
                "Java Version: " + System.getProperty("java.version") + "\n" +
                "OS: " + System.getProperty("os.name") + "\n" +
                "Architecture: " + System.getProperty("os.arch"),
                "Application Information", 
                JOptionPane.INFORMATION_MESSAGE);
        });
        
        exitButton.addActionListener(e -> System.exit(0));
        
        buttonPanel.add(infoButton);
        buttonPanel.add(exitButton);
        panel.add(buttonPanel, BorderLayout.SOUTH);
        
        // Add panel to frame
        frame.add(panel);
        
        // Center frame on screen
        frame.setLocationRelativeTo(null);
        
        // Show frame
        frame.setVisible(true);
    }
}
```

### دستورات jpackage:

```bash
# Basic packaging
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp

# Windows MSI
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --type msi

# Windows EXE
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --type exe

# macOS DMG
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --type dmg

# macOS PKG
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --type pkg

# Linux DEB
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --type deb

# Linux RPM
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --type rpm

# With custom JRE
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --runtime-image ./jre

# With application icon
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --icon app.ico

# With application version
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --app-version 1.0.0

# With vendor information
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --vendor "My Company"

# With description
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --description "My Java Application"

# With additional modules
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --add-modules java.desktop,java.logging

# With JVM options
jpackage --input . --main-jar app.jar --main-class JPackageExample --name MyApp --java-options "-Xmx512m -Dfile.encoding=UTF-8"
```

### آنالوژی دنیای واقعی:
jpackage مانند داشتن یک کارخانه بسته‌بندی هوشمند است. شما محصول خود (Java application) را به کارخانه می‌دهید و کارخانه آن را در بسته‌های مختلف (MSI, DMG, DEB, etc.) بسته‌بندی می‌کند تا برای هر سیستم عاملی مناسب باشد.