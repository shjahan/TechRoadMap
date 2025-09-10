# Section 3 - Structural Patterns

## 3.1 Adapter Pattern

The Adapter pattern allows incompatible interfaces to work together by wrapping an existing class with a new interface.

### When to Use:
- When you need to use an existing class with an incompatible interface
- When you want to integrate third-party libraries
- When you need to create a reusable class that cooperates with unrelated classes

### Real-World Analogy:
Think of a power adapter that allows you to use a device with a different plug type in a foreign country.

### Implementation:
```java
// Target interface
public interface MediaPlayer {
    void play(String audioType, String fileName);
}

// Adaptee
public class AdvancedMediaPlayer {
    public void playVlc(String fileName) {
        System.out.println("Playing vlc file: " + fileName);
    }
    
    public void playMp4(String fileName) {
        System.out.println("Playing mp4 file: " + fileName);
    }
}

// Adapter
public class MediaAdapter implements MediaPlayer {
    private AdvancedMediaPlayer advancedMusicPlayer;
    
    public MediaAdapter(String audioType) {
        if (audioType.equalsIgnoreCase("vlc")) {
            advancedMusicPlayer = new AdvancedMediaPlayer();
        }
    }
    
    public void play(String audioType, String fileName) {
        if (audioType.equalsIgnoreCase("vlc")) {
            advancedMusicPlayer.playVlc(fileName);
        }
    }
}

// Client
public class AudioPlayer implements MediaPlayer {
    private MediaAdapter mediaAdapter;
    
    public void play(String audioType, String fileName) {
        if (audioType.equalsIgnoreCase("mp3")) {
            System.out.println("Playing mp3 file: " + fileName);
        } else if (audioType.equalsIgnoreCase("vlc")) {
            mediaAdapter = new MediaAdapter(audioType);
            mediaAdapter.play(audioType, fileName);
        }
    }
}
```

## 3.2 Bridge Pattern

The Bridge pattern decouples an abstraction from its implementation so that both can vary independently.

### When to Use:
- When you want to avoid permanent binding between abstraction and implementation
- When you want to share an implementation among multiple objects
- When you need to extend both abstractions and implementations independently

### Real-World Analogy:
Think of a remote control (abstraction) and a TV (implementation). The remote control can work with different types of TVs without being tied to a specific TV model.

### Implementation:
```java
// Implementation interface
public interface DrawingAPI {
    void drawCircle(double x, double y, double radius);
}

// Concrete implementations
public class DrawingAPI1 implements DrawingAPI {
    public void drawCircle(double x, double y, double radius) {
        System.out.printf("API1.circle at %f:%f radius %f%n", x, y, radius);
    }
}

public class DrawingAPI2 implements DrawingAPI {
    public void drawCircle(double x, double y, double radius) {
        System.out.printf("API2.circle at %f:%f radius %f%n", x, y, radius);
    }
}

// Abstraction
public abstract class Shape {
    protected DrawingAPI drawingAPI;
    
    protected Shape(DrawingAPI drawingAPI) {
        this.drawingAPI = drawingAPI;
    }
    
    public abstract void draw();
}

// Refined abstraction
public class CircleShape extends Shape {
    private double x, y, radius;
    
    public CircleShape(double x, double y, double radius, DrawingAPI drawingAPI) {
        super(drawingAPI);
        this.x = x;
        this.y = y;
        this.radius = radius;
    }
    
    public void draw() {
        drawingAPI.drawCircle(x, y, radius);
    }
}
```

## 3.3 Composite Pattern

The Composite pattern composes objects into tree structures to represent part-whole hierarchies.

### When to Use:
- When you want to represent part-whole hierarchies
- When you want clients to treat individual objects and compositions uniformly
- When you have a tree structure of objects

### Real-World Analogy:
Think of a file system where files and folders can be treated uniformly - both can be opened, moved, or deleted.

### Implementation:
```java
// Component interface
public interface FileSystemComponent {
    void display(String indent);
    int getSize();
}

// Leaf
public class File implements FileSystemComponent {
    private String name;
    private int size;
    
    public File(String name, int size) {
        this.name = name;
        this.size = size;
    }
    
    public void display(String indent) {
        System.out.println(indent + "File: " + name + " (" + size + " bytes)");
    }
    
    public int getSize() {
        return size;
    }
}

// Composite
public class Directory implements FileSystemComponent {
    private String name;
    private List<FileSystemComponent> children;
    
    public Directory(String name) {
        this.name = name;
        this.children = new ArrayList<>();
    }
    
    public void add(FileSystemComponent component) {
        children.add(component);
    }
    
    public void display(String indent) {
        System.out.println(indent + "Directory: " + name);
        for (FileSystemComponent child : children) {
            child.display(indent + "  ");
        }
    }
    
    public int getSize() {
        int totalSize = 0;
        for (FileSystemComponent child : children) {
            totalSize += child.getSize();
        }
        return totalSize;
    }
}
```

## 3.4 Decorator Pattern

The Decorator pattern attaches additional responsibilities to an object dynamically without altering its structure.

### When to Use:
- When you want to add responsibilities to objects dynamically
- When you want to add features without subclassing
- When you need to add or remove features at runtime

### Real-World Analogy:
Think of adding toppings to a pizza. You start with a base pizza and can add cheese, pepperoni, mushrooms, etc., each adding to the cost and description.

### Implementation:
```java
// Component interface
public interface Coffee {
    double getCost();
    String getDescription();
}

// Concrete component
public class SimpleCoffee implements Coffee {
    public double getCost() {
        return 2.0;
    }
    
    public String getDescription() {
        return "Simple coffee";
    }
}

// Base decorator
public abstract class CoffeeDecorator implements Coffee {
    protected Coffee coffee;
    
    public CoffeeDecorator(Coffee coffee) {
        this.coffee = coffee;
    }
    
    public double getCost() {
        return coffee.getCost();
    }
    
    public String getDescription() {
        return coffee.getDescription();
    }
}

// Concrete decorators
public class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }
    
    public double getCost() {
        return coffee.getCost() + 0.5;
    }
    
    public String getDescription() {
        return coffee.getDescription() + ", milk";
    }
}

public class SugarDecorator extends CoffeeDecorator {
    public SugarDecorator(Coffee coffee) {
        super(coffee);
    }
    
    public double getCost() {
        return coffee.getCost() + 0.2;
    }
    
    public String getDescription() {
        return coffee.getDescription() + ", sugar";
    }
}
```

## 3.5 Facade Pattern

The Facade pattern provides a simplified interface to a complex subsystem.

### When to Use:
- When you want to provide a simple interface to a complex subsystem
- When you want to decouple clients from subsystem components
- When you want to layer your subsystems

### Real-World Analogy:
Think of a home theater system. Instead of turning on the TV, DVD player, sound system, and lights separately, you have one remote that controls everything with a single button.

### Implementation:
```java
// Subsystem classes
public class CPU {
    public void freeze() {
        System.out.println("CPU freeze");
    }
    
    public void jump(long position) {
        System.out.println("CPU jump to position: " + position);
    }
    
    public void execute() {
        System.out.println("CPU execute");
    }
}

public class Memory {
    public void load(long position, byte[] data) {
        System.out.println("Memory load at position: " + position);
    }
}

public class HardDrive {
    public byte[] read(long lba, int size) {
        System.out.println("Hard drive read LBA: " + lba + ", size: " + size);
        return new byte[size];
    }
}

// Facade
public class ComputerFacade {
    private CPU processor;
    private Memory ram;
    private HardDrive hd;
    
    public ComputerFacade() {
        this.processor = new CPU();
        this.ram = new Memory();
        this.hd = new HardDrive();
    }
    
    public void start() {
        processor.freeze();
        ram.load(0, hd.read(0, 1024));
        processor.jump(0);
        processor.execute();
    }
}
```

## 3.6 Flyweight Pattern

The Flyweight pattern uses sharing to support large numbers of fine-grained objects efficiently.

### When to Use:
- When you have a large number of similar objects
- When storage costs are high due to object quantity
- When most object state can be made extrinsic

### Real-World Analogy:
Think of a word processor where each character doesn't need to store its font, size, and color separately - these properties can be shared among many characters.

### Implementation:
```java
// Flyweight interface
public interface Shape {
    void draw(int x, int y);
}

// Concrete flyweight
public class Circle implements Shape {
    private String color;
    
    public Circle(String color) {
        this.color = color;
    }
    
    public void draw(int x, int y) {
        System.out.println("Drawing " + color + " circle at (" + x + ", " + y + ")");
    }
}

// Flyweight factory
public class ShapeFactory {
    private static Map<String, Shape> shapes = new HashMap<>();
    
    public static Shape getCircle(String color) {
        Circle circle = (Circle) shapes.get(color);
        
        if (circle == null) {
            circle = new Circle(color);
            shapes.put(color, circle);
            System.out.println("Creating circle of color: " + color);
        }
        
        return circle;
    }
}
```

## 3.7 Proxy Pattern

The Proxy pattern provides a placeholder or surrogate for another object to control access to it.

### When to Use:
- When you want to control access to an object
- When you want to add functionality before/after the original object
- When you want to create a representative of a complex object

### Real-World Analogy:
Think of a credit card as a proxy for cash. It represents money but provides additional features like spending limits and transaction logging.

### Implementation:
```java
// Subject interface
public interface Image {
    void display();
}

// Real subject
public class RealImage implements Image {
    private String filename;
    
    public RealImage(String filename) {
        this.filename = filename;
        loadFromDisk();
    }
    
    private void loadFromDisk() {
        System.out.println("Loading " + filename);
    }
    
    public void display() {
        System.out.println("Displaying " + filename);
    }
}

// Proxy
public class ProxyImage implements Image {
    private RealImage realImage;
    private String filename;
    
    public ProxyImage(String filename) {
        this.filename = filename;
    }
    
    public void display() {
        if (realImage == null) {
            realImage = new RealImage(filename);
        }
        realImage.display();
    }
}
```

## 3.8 Module Pattern

The Module pattern provides a way to create private and public encapsulation for classes.

### When to Use:
- When you want to create private and public encapsulation
- When you want to organize code into logical units
- When you want to avoid global namespace pollution

### Implementation:
```java
public class UserModule {
    // Private variables
    private String name;
    private String email;
    
    // Private methods
    private boolean isValidEmail(String email) {
        return email != null && email.contains("@");
    }
    
    // Public methods
    public void setName(String name) {
        this.name = name;
    }
    
    public String getName() {
        return name;
    }
    
    public void setEmail(String email) {
        if (isValidEmail(email)) {
            this.email = email;
        } else {
            throw new IllegalArgumentException("Invalid email");
        }
    }
    
    public String getEmail() {
        return email;
    }
}
```

## 3.9 Mixin Pattern

The Mixin pattern allows classes to inherit functionality from multiple sources.

### When to Use:
- When you want to add functionality to classes without inheritance
- When you want to share common functionality across unrelated classes
- When you want to avoid deep inheritance hierarchies

### Implementation:
```java
// Mixin interfaces
public interface Flyable {
    default void fly() {
        System.out.println("Flying...");
    }
}

public interface Swimmable {
    default void swim() {
        System.out.println("Swimming...");
    }
}

// Classes using mixins
public class Duck implements Flyable, Swimmable {
    public void quack() {
        System.out.println("Quack!");
    }
}

public class Airplane implements Flyable {
    public void takeOff() {
        System.out.println("Taking off...");
    }
}
```

## 3.10 Facade Pattern Variations

### Multi-Facade Pattern
```java
public class DatabaseFacade {
    private UserService userService;
    private OrderService orderService;
    
    public DatabaseFacade() {
        this.userService = new UserService();
        this.orderService = new OrderService();
    }
    
    public void createUserWithOrder(String username, String product) {
        User user = userService.createUser(username);
        orderService.createOrder(user.getId(), product);
    }
}
```

### Facade with Builder
```java
public class ComplexSystemFacade {
    private SystemA systemA;
    private SystemB systemB;
    private SystemC systemC;
    
    public ComplexSystemFacade() {
        this.systemA = new SystemA();
        this.systemB = new SystemB();
        this.systemC = new SystemC();
    }
    
    public void performComplexOperation() {
        systemA.operationA();
        systemB.operationB();
        systemC.operationC();
    }
}
```

This section covers the essential structural patterns that help organize classes and objects into larger structures while keeping them flexible and efficient.