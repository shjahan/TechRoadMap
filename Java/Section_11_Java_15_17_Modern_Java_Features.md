# Section 11 - Java 15-17 - Modern Java Features

## 11.1 Text Blocks (Final)

Text Blocks در Java 15 به صورت نهایی درآمد و راه ساده‌ای برای نوشتن رشته‌های چندخطی فراهم می‌کند.

### مفاهیم کلیدی:

**1. Triple Quotes:**
- استفاده از `"""` برای شروع و پایان
- Multiline strings بدون escape characters
- Automatic formatting

**2. Indentation Handling:**
- Incidental whitespace removal
- Preserving essential whitespace
- Consistent indentation

### مثال عملی:

```java
public class TextBlocksFinal {
    public static void main(String[] args) {
        // HTML example
        String html = """
            <html>
                <body>
                    <h1>Hello World</h1>
                    <p>This is a text block</p>
                </body>
            </html>
            """;
        
        // JSON example
        String json = """
            {
                "name": "احمد محمدی",
                "age": 25,
                "city": "تهران"
            }
            """;
        
        System.out.println(html);
        System.out.println(json);
    }
}
```

### آنالوژی دنیای واقعی:
Text Blocks مانند داشتن یک دفترچه یادداشت بزرگ برای نوشتن متن‌های طولانی است.

## 11.2 Records (Final)

Records در Java 16 به صورت نهایی درآمد و راه ساده‌ای برای ایجاد immutable data classes فراهم می‌کند.

### مفاهیم کلیدی:

**1. Immutable Data Classes:**
- Automatic generation of constructor, getters, equals, hashCode, toString
- Final fields
- No setters

**2. Compact Syntax:**
- `record` keyword
- Header declaration
- Automatic implementations

### مثال عملی:

```java
// Basic record
record Person(String name, int age, String city) {}

// Record with methods
record Point(int x, int y) {
    public double distanceFromOrigin() {
        return Math.sqrt(x * x + y * y);
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

public class RecordsFinal {
    public static void main(String[] args) {
        Person person = new Person("احمد", 25, "تهران");
        System.out.println("Person: " + person);
        System.out.println("Name: " + person.name());
        
        Point point = new Point(3, 4);
        System.out.println("Distance: " + point.distanceFromOrigin());
    }
}
```

### آنالوژی دنیای واقعی:
Records مانند داشتن یک فرم استاندارد برای ثبت اطلاعات است.

## 11.3 Sealed Classes (Final)

Sealed Classes در Java 17 به صورت نهایی درآمد و کنترل بهتری بر inheritance فراهم می‌کند.

### مفاهیم کلیدی:

**1. Restricted Inheritance:**
- تعریف کلاس‌هایی که فقط کلاس‌های مشخص می‌توانند از آن‌ها ارث ببرند
- کنترل کامل بر class hierarchy
- Compile-time checking

**2. Sealed Keyword:**
- `sealed` برای تعریف sealed class
- `permits` برای مشخص کردن subclasses مجاز
- `final` یا `sealed` یا `non-sealed` برای subclasses

### مثال عملی:

```java
// Sealed class hierarchy
sealed class Shape permits Circle, Rectangle, Triangle {
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
        double s = (side1 + side2 + side3) / 2;
        return Math.sqrt(s * (s - side1) * (s - side2) * (s - side3));
    }
}

public class SealedClassesFinal {
    public static void main(String[] args) {
        Shape[] shapes = {
            new Circle(5.0),
            new Rectangle(10, 20),
            new Triangle(3, 4, 5)
        };
        
        for (Shape shape : shapes) {
            processShape(shape);
        }
    }
    
    public static void processShape(Shape shape) {
        String result = switch (shape) {
            case Circle c -> "Circle with radius " + c.radius() + ", area: " + c.area();
            case Rectangle r -> "Rectangle " + r.width() + "x" + r.height() + ", area: " + r.area();
            case Triangle t -> "Triangle with sides " + t.side1() + ", " + t.side2() + ", " + t.side3();
        };
        
        System.out.println("Result: " + result);
    }
}
```

### آنالوژی دنیای واقعی:
Sealed Classes مانند داشتن یک سیستم طبقه‌بندی محدود است.

## 11.4 Pattern Matching for instanceof (Final)

Pattern Matching for instanceof در Java 16 به صورت نهایی درآمد و instanceof checks را ساده‌تر کرد.

### مفاهیم کلیدی:

**1. Pattern Variables:**
- تعریف متغیر در همان instanceof check
- Scope محدود به if block
- Type safety

**2. Eliminates Casting:**
- نیازی به explicit casting نیست
- Compiler type checking
- Cleaner code

### مثال عملی:

```java
public class PatternMatchingFinal {
    public static void main(String[] args) {
        Object[] objects = {
            "Hello World",
            42,
            3.14,
            new int[]{1, 2, 3}
        };
        
        for (Object obj : objects) {
            processObject(obj);
        }
    }
    
    public static void processObject(Object obj) {
        if (obj instanceof String str) {
            System.out.println("String length: " + str.length());
        } else if (obj instanceof Integer num) {
            System.out.println("Integer value: " + num);
        } else if (obj instanceof Double dbl) {
            System.out.println("Double value: " + dbl);
        } else if (obj instanceof int[] arr) {
            System.out.println("Array length: " + arr.length);
        } else {
            System.out.println("Unknown type");
        }
    }
}
```

### آنالوژی دنیای واقعی:
Pattern Matching مانند داشتن یک سیستم تشخیص هوشمند است.

## 11.5 Switch Expressions (Final)

Switch Expressions در Java 14 به صورت نهایی درآمد و نحوه نوشتن switch statements را بهبود بخشید.

### مفاهیم کلیدی:

**1. Expression-based Switch:**
- Switch به عنوان expression عمل می‌کند
- می‌تواند مقدار return کند
- نیازی به break statements نیست

**2. Arrow Syntax:**
- استفاده از `->` به جای `:`
- کد تمیزتر و خوانا‌تر
- Multiple case labels

### مثال عملی:

```java
public class SwitchExpressionsFinal {
    public static void main(String[] args) {
        Day today = Day.MONDAY;
        
        // Switch expression
        String dayType = switch (today) {
            case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "Working day";
            case SATURDAY, SUNDAY -> "Weekend";
        };
        
        System.out.println("Today is: " + today);
        System.out.println("Day type: " + dayType);
        
        // Switch expression with yield
        int dayNumber = switch (today) {
            case MONDAY -> 1;
            case TUESDAY -> 2;
            case WEDNESDAY -> 3;
            case THURSDAY -> 4;
            case FRIDAY -> 5;
            case SATURDAY -> 6;
            case SUNDAY -> 7;
        };
        
        System.out.println("Day number: " + dayNumber);
    }
}

enum Day {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}
```

### آنالوژی دنیای واقعی:
Switch Expressions مانند داشتن یک ماشین حساب پیشرفته است.

## 11.6 Foreign Function & Memory API (Preview)

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

## 11.7 Vector API (Preview)

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