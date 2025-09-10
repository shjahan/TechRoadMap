# Section 16 - Design Patterns & Architecture

## 16.1 Creational Patterns

Creational Patterns الگوهایی هستند که برای ایجاد objects استفاده می‌شوند.

### مفاهیم کلیدی:

**1. Singleton Pattern:**
- Ensure single instance
- Global access point
- Lazy initialization
- Thread safety

**2. Factory Pattern:**
- Object creation abstraction
- Centralized creation logic
- Type safety
- Extensibility

**3. Builder Pattern:**
- Complex object construction
- Step-by-step building
- Fluent interface
- Immutable objects

### مثال عملی:

```java
// Singleton Pattern
public class DatabaseConnection {
    private static volatile DatabaseConnection instance;
    
    private DatabaseConnection() {}
    
    public static DatabaseConnection getInstance() {
        if (instance == null) {
            synchronized (DatabaseConnection.class) {
                if (instance == null) {
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }
}

// Factory Pattern
public interface Shape {
    void draw();
}

public class Circle implements Shape {
    @Override
    public void draw() {
        System.out.println("Drawing Circle");
    }
}

public class Rectangle implements Shape {
    @Override
    public void draw() {
        System.out.println("Drawing Rectangle");
    }
}

public class ShapeFactory {
    public Shape createShape(String type) {
        return switch (type.toLowerCase()) {
            case "circle" -> new Circle();
            case "rectangle" -> new Rectangle();
            default -> throw new IllegalArgumentException("Unknown shape type");
        };
    }
}

// Builder Pattern
public class Computer {
    private String cpu;
    private String memory;
    private String storage;
    
    private Computer(Builder builder) {
        this.cpu = builder.cpu;
        this.memory = builder.memory;
        this.storage = builder.storage;
    }
    
    public static class Builder {
        private String cpu;
        private String memory;
        private String storage;
        
        public Builder setCpu(String cpu) {
            this.cpu = cpu;
            return this;
        }
        
        public Builder setMemory(String memory) {
            this.memory = memory;
            return this;
        }
        
        public Builder setStorage(String storage) {
            this.storage = storage;
            return this;
        }
        
        public Computer build() {
            return new Computer(this);
        }
    }
}
```

### آنالوژی دنیای واقعی:
Creational Patterns مانند داشتن یک کارخانه تولیدی است که:
- **Singleton:** مانند داشتن یک مدیر کل کارخانه
- **Factory:** مانند خط تولید که محصولات مختلف تولید می‌کند
- **Builder:** مانند خط مونتاژ که محصول را مرحله به مرحله می‌سازد

## 16.2 Structural Patterns

Structural Patterns الگوهایی هستند که برای ترکیب classes و objects استفاده می‌شوند.

### مفاهیم کلیدی:

**1. Adapter Pattern:**
- Interface compatibility
- Legacy system integration
- Wrapper classes
- Object adaptation

**2. Decorator Pattern:**
- Dynamic behavior addition
- Wrapper classes
- Composition over inheritance
- Flexible enhancement

**3. Facade Pattern:**
- Simplified interface
- Complex subsystem hiding
- Single entry point
- Reduced complexity

### مثال عملی:

```java
// Adapter Pattern
public interface MediaPlayer {
    void play(String audioType, String fileName);
}

public interface AdvancedMediaPlayer {
    void playVlc(String fileName);
    void playMp4(String fileName);
}

public class VlcPlayer implements AdvancedMediaPlayer {
    @Override
    public void playVlc(String fileName) {
        System.out.println("Playing vlc file: " + fileName);
    }
    
    @Override
    public void playMp4(String fileName) {
        // Do nothing
    }
}

public class MediaAdapter implements MediaPlayer {
    private AdvancedMediaPlayer advancedMusicPlayer;
    
    public MediaAdapter(String audioType) {
        if (audioType.equalsIgnoreCase("vlc")) {
            advancedMusicPlayer = new VlcPlayer();
        }
    }
    
    @Override
    public void play(String audioType, String fileName) {
        if (audioType.equalsIgnoreCase("vlc")) {
            advancedMusicPlayer.playVlc(fileName);
        }
    }
}

// Decorator Pattern
public interface Coffee {
    double getCost();
    String getDescription();
}

public class SimpleCoffee implements Coffee {
    @Override
    public double getCost() {
        return 10;
    }
    
    @Override
    public String getDescription() {
        return "Simple coffee";
    }
}

public abstract class CoffeeDecorator implements Coffee {
    protected Coffee coffee;
    
    public CoffeeDecorator(Coffee coffee) {
        this.coffee = coffee;
    }
    
    @Override
    public double getCost() {
        return coffee.getCost();
    }
    
    @Override
    public String getDescription() {
        return coffee.getDescription();
    }
}

public class MilkDecorator extends CoffeeDecorator {
    public MilkDecorator(Coffee coffee) {
        super(coffee);
    }
    
    @Override
    public double getCost() {
        return coffee.getCost() + 2;
    }
    
    @Override
    public String getDescription() {
        return coffee.getDescription() + ", milk";
    }
}

// Facade Pattern
public class ShapeMaker {
    private Shape circle;
    private Shape rectangle;
    private Shape square;
    
    public ShapeMaker() {
        circle = new Circle();
        rectangle = new Rectangle();
        square = new Square();
    }
    
    public void drawCircle() {
        circle.draw();
    }
    
    public void drawRectangle() {
        rectangle.draw();
    }
    
    public void drawSquare() {
        square.draw();
    }
}
```

### آنالوژی دنیای واقعی:
Structural Patterns مانند داشتن یک سیستم معماری هوشمند است که:
- **Adapter:** مانند مترجم که بین زبان‌های مختلف ترجمه می‌کند
- **Decorator:** مانند اضافه کردن تزئینات به یک ساختمان
- **Facade:** مانند نمای اصلی ساختمان که پیچیدگی‌های داخلی را مخفی می‌کند

## 16.3 Behavioral Patterns

Behavioral Patterns الگوهایی هستند که برای مدیریت algorithms و relationships بین objects استفاده می‌شوند.

### مفاهیم کلیدی:

**1. Observer Pattern:**
- One-to-many dependency
- Event notification
- Loose coupling
- Dynamic relationships

**2. Strategy Pattern:**
- Algorithm encapsulation
- Runtime algorithm selection
- Family of algorithms
- Context independence

**3. Command Pattern:**
- Request encapsulation
- Undo/redo functionality
- Queue operations
- Logging and auditing

### مثال عملی:

```java
// Observer Pattern
public interface Observer {
    void update(String message);
}

public interface Subject {
    void attach(Observer observer);
    void detach(Observer observer);
    void notifyObservers();
}

public class NewsAgency implements Subject {
    private List<Observer> observers = new ArrayList<>();
    private String news;
    
    @Override
    public void attach(Observer observer) {
        observers.add(observer);
    }
    
    @Override
    public void detach(Observer observer) {
        observers.remove(observer);
    }
    
    @Override
    public void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(news);
        }
    }
    
    public void setNews(String news) {
        this.news = news;
        notifyObservers();
    }
}

public class NewsChannel implements Observer {
    private String name;
    
    public NewsChannel(String name) {
        this.name = name;
    }
    
    @Override
    public void update(String message) {
        System.out.println(name + " received: " + message);
    }
}

// Strategy Pattern
public interface PaymentStrategy {
    void pay(double amount);
}

public class CreditCardPayment implements PaymentStrategy {
    private String cardNumber;
    
    public CreditCardPayment(String cardNumber) {
        this.cardNumber = cardNumber;
    }
    
    @Override
    public void pay(double amount) {
        System.out.println("Paid " + amount + " using credit card " + cardNumber);
    }
}

public class PayPalPayment implements PaymentStrategy {
    private String email;
    
    public PayPalPayment(String email) {
        this.email = email;
    }
    
    @Override
    public void pay(double amount) {
        System.out.println("Paid " + amount + " using PayPal " + email);
    }
}

public class PaymentContext {
    private PaymentStrategy strategy;
    
    public void setPaymentStrategy(PaymentStrategy strategy) {
        this.strategy = strategy;
    }
    
    public void executePayment(double amount) {
        strategy.pay(amount);
    }
}

// Command Pattern
public interface Command {
    void execute();
    void undo();
}

public class Light {
    private boolean on = false;
    
    public void turnOn() {
        on = true;
        System.out.println("Light is on");
    }
    
    public void turnOff() {
        on = false;
        System.out.println("Light is off");
    }
    
    public boolean isOn() {
        return on;
    }
}

public class LightOnCommand implements Command {
    private Light light;
    
    public LightOnCommand(Light light) {
        this.light = light;
    }
    
    @Override
    public void execute() {
        light.turnOn();
    }
    
    @Override
    public void undo() {
        light.turnOff();
    }
}

public class RemoteControl {
    private Command command;
    
    public void setCommand(Command command) {
        this.command = command;
    }
    
    public void pressButton() {
        command.execute();
    }
    
    public void pressUndo() {
        command.undo();
    }
}
```

### آنالوژی دنیای واقعی:
Behavioral Patterns مانند داشتن یک سیستم مدیریت هوشمند است که:
- **Observer:** مانند سیستم اطلاع‌رسانی که در صورت وقوع رویداد، همه را مطلع می‌کند
- **Strategy:** مانند داشتن چندین روش مختلف برای انجام یک کار
- **Command:** مانند داشتن یک سیستم کنترل از راه دور

## 16.4 Architectural Patterns

Architectural Patterns الگوهایی هستند که برای طراحی سیستم‌های بزرگ و پیچیده استفاده می‌شوند.

### مفاهیم کلیدی:

**1. MVC (Model-View-Controller):**
- Separation of concerns
- User interface separation
- Business logic isolation
- Data management

**2. MVP (Model-View-Presenter):**
- View logic separation
- Testability improvement
- Passive view
- Presenter mediation

**3. MVVM (Model-View-ViewModel):**
- Data binding
- View state management
- Command pattern
- Reactive programming

### مثال عملی:

```java
// MVC Pattern
public class User {
    private String name;
    private String email;
    
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }
    
    // Getters and setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}

public class UserController {
    private User model;
    private UserView view;
    
    public UserController(User model, UserView view) {
        this.model = model;
        this.view = view;
    }
    
    public void setUserName(String name) {
        model.setName(name);
    }
    
    public void setUserEmail(String email) {
        model.setEmail(email);
    }
    
    public void updateView() {
        view.printUserDetails(model.getName(), model.getEmail());
    }
}

public class UserView {
    public void printUserDetails(String name, String email) {
        System.out.println("User: " + name + ", Email: " + email);
    }
}

// MVP Pattern
public interface UserView {
    void setUserName(String name);
    void setUserEmail(String email);
    void showUserDetails();
}

public class UserPresenter {
    private User model;
    private UserView view;
    
    public UserPresenter(User model, UserView view) {
        this.model = model;
        this.view = view;
    }
    
    public void updateUser(String name, String email) {
        model.setName(name);
        model.setEmail(email);
        view.setUserName(model.getName());
        view.setUserEmail(model.getEmail());
    }
}

// MVVM Pattern
public class UserViewModel {
    private User model;
    private String name;
    private String email;
    
    public UserViewModel(User model) {
        this.model = model;
        this.name = model.getName();
        this.email = model.getEmail();
    }
    
    public String getName() { return name; }
    public void setName(String name) { 
        this.name = name;
        model.setName(name);
    }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { 
        this.email = email;
        model.setEmail(email);
    }
}
```

### آنالوژی دنیای واقعی:
Architectural Patterns مانند داشتن یک سیستم مدیریت ساختمان است که:
- **MVC:** مانند تقسیم ساختمان به بخش‌های مختلف (اداری، مسکونی، تجاری)
- **MVP:** مانند داشتن یک مدیر که بین بخش‌های مختلف هماهنگی ایجاد می‌کند
- **MVVM:** مانند داشتن یک سیستم هوشمند که همه بخش‌ها را به هم متصل می‌کند

## 16.5 Domain-Driven Design (DDD)

Domain-Driven Design یک رویکرد برای طراحی نرم‌افزار است که بر روی domain logic تمرکز می‌کند.

### مفاهیم کلیدی:

**1. Domain Model:**
- Business logic representation
- Entity identification
- Value objects
- Aggregate roots

**2. Bounded Context:**
- Domain boundary definition
- Context mapping
- Integration patterns
- Service boundaries

**3. Ubiquitous Language:**
- Common vocabulary
- Domain expert communication
- Code documentation
- Business alignment

### مثال عملی:

```java
// Domain Entity
public class Order {
    private OrderId id;
    private CustomerId customerId;
    private List<OrderItem> items;
    private OrderStatus status;
    private Money totalAmount;
    
    public Order(OrderId id, CustomerId customerId) {
        this.id = id;
        this.customerId = customerId;
        this.items = new ArrayList<>();
        this.status = OrderStatus.PENDING;
        this.totalAmount = Money.zero();
    }
    
    public void addItem(ProductId productId, Quantity quantity, Money unitPrice) {
        OrderItem item = new OrderItem(productId, quantity, unitPrice);
        items.add(item);
        recalculateTotal();
    }
    
    public void confirm() {
        if (status != OrderStatus.PENDING) {
            throw new IllegalStateException("Order cannot be confirmed");
        }
        status = OrderStatus.CONFIRMED;
    }
    
    private void recalculateTotal() {
        totalAmount = items.stream()
            .map(OrderItem::getTotalPrice)
            .reduce(Money.zero(), Money::add);
    }
}

// Value Object
public class Money {
    private final BigDecimal amount;
    private final Currency currency;
    
    public Money(BigDecimal amount, Currency currency) {
        this.amount = amount;
        this.currency = currency;
    }
    
    public static Money zero() {
        return new Money(BigDecimal.ZERO, Currency.getInstance("USD"));
    }
    
    public Money add(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("Cannot add different currencies");
        }
        return new Money(amount.add(other.amount), currency);
    }
    
    // Equals, hashCode, toString
}

// Domain Service
public class OrderService {
    private OrderRepository orderRepository;
    private InventoryService inventoryService;
    
    public Order createOrder(CustomerId customerId, List<OrderItem> items) {
        // Validate inventory
        for (OrderItem item : items) {
            if (!inventoryService.isAvailable(item.getProductId(), item.getQuantity())) {
                throw new InsufficientInventoryException("Product not available");
            }
        }
        
        Order order = new Order(OrderId.generate(), customerId);
        for (OrderItem item : items) {
            order.addItem(item.getProductId(), item.getQuantity(), item.getUnitPrice());
        }
        
        return orderRepository.save(order);
    }
}
```

### آنالوژی دنیای واقعی:
Domain-Driven Design مانند داشتن یک سیستم مدیریت شهری است که:
- **Domain Model:** مانند نقشه شهر که بخش‌های مختلف را نشان می‌دهد
- **Bounded Context:** مانند محدوده‌های مختلف شهری
- **Ubiquitous Language:** مانند زبان مشترک بین شهروندان

## 16.6 Clean Architecture Principles

Clean Architecture Principles مجموعه‌ای از اصول برای طراحی نرم‌افزار تمیز و قابل نگهداری است.

### مفاهیم کلیدی:

**1. Dependency Rule:**
- Dependencies point inward
- Inner layers don't know about outer layers
- Abstraction over concretion
- Interface segregation

**2. Layer Separation:**
- Entities (Business rules)
- Use cases (Application rules)
- Interface adapters
- Frameworks & drivers

**3. SOLID Principles:**
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

### مثال عملی:

```java
// Entity Layer
public class User {
    private UserId id;
    private String name;
    private Email email;
    
    public User(UserId id, String name, Email email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    public boolean isValid() {
        return name != null && !name.trim().isEmpty() && email.isValid();
    }
}

// Use Case Layer
public interface UserRepository {
    User findById(UserId id);
    void save(User user);
}

public class CreateUserUseCase {
    private UserRepository userRepository;
    
    public CreateUserUseCase(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public User execute(String name, String email) {
        User user = new User(UserId.generate(), name, new Email(email));
        if (user.isValid()) {
            userRepository.save(user);
            return user;
        }
        throw new InvalidUserException("Invalid user data");
    }
}

// Interface Adapter Layer
public class UserController {
    private CreateUserUseCase createUserUseCase;
    
    public UserController(CreateUserUseCase createUserUseCase) {
        this.createUserUseCase = createUserUseCase;
    }
    
    public ResponseEntity<User> createUser(CreateUserRequest request) {
        try {
            User user = createUserUseCase.execute(request.getName(), request.getEmail());
            return ResponseEntity.ok(user);
        } catch (InvalidUserException e) {
            return ResponseEntity.badRequest().build();
        }
    }
}

// Framework Layer
@Repository
public class JpaUserRepository implements UserRepository {
    @PersistenceContext
    private EntityManager entityManager;
    
    @Override
    public User findById(UserId id) {
        return entityManager.find(User.class, id);
    }
    
    @Override
    public void save(User user) {
        entityManager.persist(user);
    }
}
```

### آنالوژی دنیای واقعی:
Clean Architecture مانند داشتن یک سیستم مدیریت هوشمند است که:
- **Dependency Rule:** مانند جریان انرژی که از بیرون به داخل می‌رود
- **Layer Separation:** مانند طبقات مختلف یک ساختمان
- **SOLID Principles:** مانند قوانین مهندسی که از استحکام ساختمان اطمینان می‌دهند

## 16.7 SOLID Principles

SOLID Principles مجموعه‌ای از اصول برای طراحی نرم‌افزار تمیز و قابل نگهداری است.

### مفاهیم کلیدی:

**1. Single Responsibility Principle (SRP):**
- One class, one responsibility
- Cohesion
- Maintainability
- Testability

**2. Open/Closed Principle (OCP):**
- Open for extension
- Closed for modification
- Polymorphism
- Interface-based design

**3. Liskov Substitution Principle (LSP):**
- Substitutability
- Behavioral compatibility
- Contract adherence
- Inheritance safety

**4. Interface Segregation Principle (ISP):**
- Client-specific interfaces
- No forced dependencies
- Cohesive interfaces
- Minimal coupling

**5. Dependency Inversion Principle (DIP):**
- Depend on abstractions
- Not on concretions
- Inversion of control
- Loose coupling

### مثال عملی:

```java
// SRP - Single Responsibility
public class User {
    private String name;
    private String email;
    
    // User-related methods only
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}

public class UserValidator {
    public boolean isValid(User user) {
        return user.getName() != null && user.getEmail() != null;
    }
}

// OCP - Open/Closed
public interface Shape {
    double area();
}

public class Circle implements Shape {
    private double radius;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}

public class Rectangle implements Shape {
    private double width;
    private double height;
    
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
    
    @Override
    public double area() {
        return width * height;
    }
}

// LSP - Liskov Substitution
public class Bird {
    public void fly() {
        System.out.println("Flying");
    }
}

public class Eagle extends Bird {
    @Override
    public void fly() {
        System.out.println("Eagle flying high");
    }
}

public class Penguin extends Bird {
    @Override
    public void fly() {
        throw new UnsupportedOperationException("Penguins can't fly");
    }
}

// ISP - Interface Segregation
public interface Readable {
    String read();
}

public interface Writable {
    void write(String content);
}

public class FileReader implements Readable {
    @Override
    public String read() {
        return "File content";
    }
}

public class FileWriter implements Writable {
    @Override
    public void write(String content) {
        System.out.println("Writing: " + content);
    }
}

// DIP - Dependency Inversion
public interface NotificationService {
    void send(String message);
}

public class EmailService implements NotificationService {
    @Override
    public void send(String message) {
        System.out.println("Email: " + message);
    }
}

public class SMSService implements NotificationService {
    @Override
    public void send(String message) {
        System.out.println("SMS: " + message);
    }
}

public class NotificationManager {
    private NotificationService notificationService;
    
    public NotificationManager(NotificationService notificationService) {
        this.notificationService = notificationService;
    }
    
    public void sendNotification(String message) {
        notificationService.send(message);
    }
}
```

### آنالوژی دنیای واقعی:
SOLID Principles مانند داشتن یک سیستم مدیریت هوشمند است که:
- **SRP:** مانند تقسیم کارها بین کارگران مختلف
- **OCP:** مانند امکان اضافه کردن بخش‌های جدید بدون تغییر بخش‌های موجود
- **LSP:** مانند امکان جایگزینی کارگران با هم
- **ISP:** مانند داشتن قراردادهای کاری مشخص
- **DIP:** مانند وابستگی به قوانین کلی به جای جزئیات خاص