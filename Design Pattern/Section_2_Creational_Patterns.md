# Section 2 - Creational Patterns

## 2.1 Singleton Pattern

The Singleton pattern ensures that a class has only one instance and provides global access to that instance. This is useful when you need exactly one object to coordinate actions across the system.

### When to Use:
- When you need exactly one instance of a class
- When you need global access to that instance
- When you want to control instantiation

### Real-World Analogy:
Think of a company's CEO - there's only one CEO at a time, and everyone in the company needs to access the same CEO for important decisions.

### Basic Implementation:
```java
public class DatabaseConnection {
    private static DatabaseConnection instance;
    private String connectionString;
    
    // Private constructor prevents instantiation
    private DatabaseConnection() {
        this.connectionString = "jdbc:mysql://localhost:3306/mydb";
    }
    
    // Public method to get the single instance
    public static DatabaseConnection getInstance() {
        if (instance == null) {
            instance = new DatabaseConnection();
        }
        return instance;
    }
    
    public void connect() {
        System.out.println("Connecting to: " + connectionString);
    }
}

// Usage
public class Application {
    public static void main(String[] args) {
        DatabaseConnection db1 = DatabaseConnection.getInstance();
        DatabaseConnection db2 = DatabaseConnection.getInstance();
        
        System.out.println(db1 == db2); // true - same instance
        db1.connect();
    }
}
```

### Thread-Safe Implementation:
```java
public class ThreadSafeDatabaseConnection {
    private static volatile ThreadSafeDatabaseConnection instance;
    
    private ThreadSafeDatabaseConnection() {}
    
    public static ThreadSafeDatabaseConnection getInstance() {
        if (instance == null) {
            synchronized (ThreadSafeDatabaseConnection.class) {
                if (instance == null) {
                    instance = new ThreadSafeDatabaseConnection();
                }
            }
        }
        return instance;
    }
}
```

### Enum Singleton (Recommended for Java):
```java
public enum DatabaseConnection {
    INSTANCE;
    
    private String connectionString;
    
    DatabaseConnection() {
        this.connectionString = "jdbc:mysql://localhost:3306/mydb";
    }
    
    public void connect() {
        System.out.println("Connecting to: " + connectionString);
    }
}

// Usage
DatabaseConnection.INSTANCE.connect();
```

### Pros and Cons:
**Pros:**
- Ensures single instance
- Global access point
- Lazy initialization possible

**Cons:**
- Global state can be problematic
- Hard to unit test
- Thread safety concerns
- Violates Single Responsibility Principle

## 2.2 Factory Method Pattern

The Factory Method pattern provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created. It's useful when you don't know beforehand the exact types and dependencies of objects your code should work with.

### When to Use:
- When you don't know the exact types of objects your code will work with
- When you want to provide an extension point for subclasses
- When you want to localize product creation logic

### Real-World Analogy:
Think of a car factory. The main factory (superclass) defines the process of building a car, but different factories (subclasses) can produce different types of cars (sedans, SUVs, trucks) following the same process.

### Basic Implementation:
```java
// Product interface
public interface Document {
    void open();
    void save();
    void close();
}

// Concrete products
public class PDFDocument implements Document {
    public void open() {
        System.out.println("Opening PDF document");
    }
    
    public void save() {
        System.out.println("Saving PDF document");
    }
    
    public void close() {
        System.out.println("Closing PDF document");
    }
}

public class WordDocument implements Document {
    public void open() {
        System.out.println("Opening Word document");
    }
    
    public void save() {
        System.out.println("Saving Word document");
    }
    
    public void close() {
        System.out.println("Closing Word document");
    }
}

// Creator abstract class
public abstract class DocumentFactory {
    // Factory method
    public abstract Document createDocument();
    
    // Template method using the factory method
    public void processDocument() {
        Document doc = createDocument();
        doc.open();
        doc.save();
        doc.close();
    }
}

// Concrete creators
public class PDFFactory extends DocumentFactory {
    public Document createDocument() {
        return new PDFDocument();
    }
}

public class WordFactory extends DocumentFactory {
    public Document createDocument() {
        return new WordDocument();
    }
}

// Usage
public class Application {
    public static void main(String[] args) {
        DocumentFactory pdfFactory = new PDFFactory();
        pdfFactory.processDocument();
        
        DocumentFactory wordFactory = new WordFactory();
        wordFactory.processDocument();
    }
}
```

### Parameterized Factory Method:
```java
public class DocumentFactory {
    public static Document createDocument(String type) {
        switch (type.toLowerCase()) {
            case "pdf":
                return new PDFDocument();
            case "word":
                return new WordDocument();
            case "excel":
                return new ExcelDocument();
            default:
                throw new IllegalArgumentException("Unknown document type: " + type);
        }
    }
}

// Usage
Document doc = DocumentFactory.createDocument("pdf");
```

### Pros and Cons:
**Pros:**
- Decouples client code from concrete classes
- Follows Open/Closed Principle
- Single Responsibility Principle

**Cons:**
- Can make code more complex
- Requires creating many subclasses

## 2.3 Abstract Factory Pattern

The Abstract Factory pattern provides an interface for creating families of related objects without specifying their concrete classes. It's useful when you need to create objects that are related or dependent on each other.

### When to Use:
- When you need to create families of related products
- When you want to ensure products from one family are used together
- When you want to provide a library of products

### Real-World Analogy:
Think of a furniture store. You have different styles (Modern, Victorian, Art Deco) and each style has a complete set of furniture (chair, table, sofa). An abstract factory would ensure all furniture in a room matches the same style.

### Implementation:
```java
// Abstract products
public interface Chair {
    void sit();
}

public interface Table {
    void place();
}

public interface Sofa {
    void relax();
}

// Concrete products - Modern style
public class ModernChair implements Chair {
    public void sit() {
        System.out.println("Sitting on a modern chair");
    }
}

public class ModernTable implements Table {
    public void place() {
        System.out.println("Placing items on a modern table");
    }
}

public class ModernSofa implements Sofa {
    public void relax() {
        System.out.println("Relaxing on a modern sofa");
    }
}

// Concrete products - Victorian style
public class VictorianChair implements Chair {
    public void sit() {
        System.out.println("Sitting on a Victorian chair");
    }
}

public class VictorianTable implements Table {
    public void place() {
        System.out.println("Placing items on a Victorian table");
    }
}

public class VictorianSofa implements Sofa {
    public void relax() {
        System.out.println("Relaxing on a Victorian sofa");
    }
}

// Abstract factory
public interface FurnitureFactory {
    Chair createChair();
    Table createTable();
    Sofa createSofa();
}

// Concrete factories
public class ModernFurnitureFactory implements FurnitureFactory {
    public Chair createChair() {
        return new ModernChair();
    }
    
    public Table createTable() {
        return new ModernTable();
    }
    
    public Sofa createSofa() {
        return new ModernSofa();
    }
}

public class VictorianFurnitureFactory implements FurnitureFactory {
    public Chair createChair() {
        return new VictorianChair();
    }
    
    public Table createTable() {
        return new VictorianTable();
    }
    
    public Sofa createSofa() {
        return new VictorianSofa();
    }
}

// Client code
public class Room {
    private Chair chair;
    private Table table;
    private Sofa sofa;
    
    public Room(FurnitureFactory factory) {
        this.chair = factory.createChair();
        this.table = factory.createTable();
        this.sofa = factory.createSofa();
    }
    
    public void useFurniture() {
        chair.sit();
        table.place();
        sofa.relax();
    }
}

// Usage
public class Application {
    public static void main(String[] args) {
        // Create a modern room
        FurnitureFactory modernFactory = new ModernFurnitureFactory();
        Room modernRoom = new Room(modernFactory);
        modernRoom.useFurniture();
        
        // Create a Victorian room
        FurnitureFactory victorianFactory = new VictorianFurnitureFactory();
        Room victorianRoom = new Room(victorianFactory);
        victorianRoom.useFurniture();
    }
}
```

### Pros and Cons:
**Pros:**
- Ensures products from one family are used together
- Isolates concrete classes from clients
- Easy to add new product families

**Cons:**
- Difficult to add new product types
- Can become complex with many products

## 2.4 Builder Pattern

The Builder pattern constructs complex objects step by step. It allows you to produce different types and representations of an object using the same construction code. It's particularly useful when you have objects with many optional parameters.

### When to Use:
- When you need to create complex objects with many optional parameters
- When you want to create different representations of the same object
- When you want to make the construction process more readable

### Real-World Analogy:
Think of building a house. You have a blueprint (builder) that defines the steps, but you can customize each step (foundation, walls, roof, etc.) to create different types of houses (mansion, cottage, apartment).

### Basic Implementation:
```java
// Product
public class Computer {
    private String cpu;
    private String memory;
    private String storage;
    private String graphicsCard;
    private String motherboard;
    
    // Private constructor
    private Computer(ComputerBuilder builder) {
        this.cpu = builder.cpu;
        this.memory = builder.memory;
        this.storage = builder.storage;
        this.graphicsCard = builder.graphicsCard;
        this.motherboard = builder.motherboard;
    }
    
    // Getters
    public String getCpu() { return cpu; }
    public String getMemory() { return memory; }
    public String getStorage() { return storage; }
    public String getGraphicsCard() { return graphicsCard; }
    public String getMotherboard() { return motherboard; }
    
    @Override
    public String toString() {
        return "Computer{" +
                "cpu='" + cpu + '\'' +
                ", memory='" + memory + '\'' +
                ", storage='" + storage + '\'' +
                ", graphicsCard='" + graphicsCard + '\'' +
                ", motherboard='" + motherboard + '\'' +
                '}';
    }
    
    // Builder class
    public static class ComputerBuilder {
        private String cpu;
        private String memory;
        private String storage;
        private String graphicsCard;
        private String motherboard;
        
        public ComputerBuilder setCpu(String cpu) {
            this.cpu = cpu;
            return this;
        }
        
        public ComputerBuilder setMemory(String memory) {
            this.memory = memory;
            return this;
        }
        
        public ComputerBuilder setStorage(String storage) {
            this.storage = storage;
            return this;
        }
        
        public ComputerBuilder setGraphicsCard(String graphicsCard) {
            this.graphicsCard = graphicsCard;
            return this;
        }
        
        public ComputerBuilder setMotherboard(String motherboard) {
            this.motherboard = motherboard;
            return this;
        }
        
        public Computer build() {
            return new Computer(this);
        }
    }
}

// Usage
public class Application {
    public static void main(String[] args) {
        Computer gamingPC = new Computer.ComputerBuilder()
                .setCpu("Intel i9")
                .setMemory("32GB DDR4")
                .setStorage("1TB SSD")
                .setGraphicsCard("RTX 4080")
                .setMotherboard("ASUS ROG")
                .build();
        
        Computer officePC = new Computer.ComputerBuilder()
                .setCpu("Intel i5")
                .setMemory("16GB DDR4")
                .setStorage("512GB SSD")
                .setMotherboard("MSI Pro")
                .build();
        
        System.out.println("Gaming PC: " + gamingPC);
        System.out.println("Office PC: " + officePC);
    }
}
```

### Fluent Builder with Validation:
```java
public class User {
    private String firstName;
    private String lastName;
    private String email;
    private int age;
    private String phone;
    
    private User(UserBuilder builder) {
        this.firstName = builder.firstName;
        this.lastName = builder.lastName;
        this.email = builder.email;
        this.age = builder.age;
        this.phone = builder.phone;
    }
    
    public static class UserBuilder {
        private String firstName;
        private String lastName;
        private String email;
        private int age;
        private String phone;
        
        public UserBuilder firstName(String firstName) {
            this.firstName = firstName;
            return this;
        }
        
        public UserBuilder lastName(String lastName) {
            this.lastName = lastName;
            return this;
        }
        
        public UserBuilder email(String email) {
            this.email = email;
            return this;
        }
        
        public UserBuilder age(int age) {
            this.age = age;
            return this;
        }
        
        public UserBuilder phone(String phone) {
            this.phone = phone;
            return this;
        }
        
        public User build() {
            validate();
            return new User(this);
        }
        
        private void validate() {
            if (firstName == null || firstName.trim().isEmpty()) {
                throw new IllegalArgumentException("First name is required");
            }
            if (lastName == null || lastName.trim().isEmpty()) {
                throw new IllegalArgumentException("Last name is required");
            }
            if (email == null || !email.contains("@")) {
                throw new IllegalArgumentException("Valid email is required");
            }
            if (age < 0 || age > 150) {
                throw new IllegalArgumentException("Age must be between 0 and 150");
            }
        }
    }
}
```

### Pros and Cons:
**Pros:**
- Makes object construction more readable
- Allows step-by-step construction
- Reuses construction code
- Provides validation during construction

**Cons:**
- Increases code complexity
- Requires creating builder classes

## 2.5 Prototype Pattern

The Prototype pattern creates objects by cloning an existing object (prototype) rather than creating new objects from scratch. This is useful when object creation is expensive or when you want to create objects that are similar to existing ones.

### When to Use:
- When object creation is expensive
- When you want to create objects similar to existing ones
- When you want to avoid subclassing

### Real-World Analogy:
Think of a photocopier. Instead of writing a document from scratch, you take an existing document and make copies of it, possibly modifying some details.

### Basic Implementation:
```java
// Prototype interface
public interface Cloneable {
    Cloneable clone();
}

// Concrete prototype
public class Document implements Cloneable {
    private String title;
    private String content;
    private String author;
    private Date createdDate;
    
    public Document(String title, String content, String author) {
        this.title = title;
        this.content = content;
        this.author = author;
        this.createdDate = new Date();
    }
    
    // Copy constructor for cloning
    public Document(Document document) {
        this.title = document.title;
        this.content = document.content;
        this.author = document.author;
        this.createdDate = new Date(); // New creation date
    }
    
    public Cloneable clone() {
        return new Document(this);
    }
    
    // Getters and setters
    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }
    
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    
    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }
    
    public Date getCreatedDate() { return createdDate; }
    
    @Override
    public String toString() {
        return "Document{" +
                "title='" + title + '\'' +
                ", content='" + content + '\'' +
                ", author='" + author + '\'' +
                ", createdDate=" + createdDate +
                '}';
    }
}

// Prototype manager
public class DocumentManager {
    private Map<String, Document> prototypes;
    
    public DocumentManager() {
        prototypes = new HashMap<>();
        initializePrototypes();
    }
    
    private void initializePrototypes() {
        Document reportTemplate = new Document(
            "Report Template",
            "This is a template for reports...",
            "System"
        );
        prototypes.put("report", reportTemplate);
        
        Document letterTemplate = new Document(
            "Letter Template",
            "Dear [Name],\n\nThis is a template for letters...",
            "System"
        );
        prototypes.put("letter", letterTemplate);
    }
    
    public Document createDocument(String type) {
        Document prototype = prototypes.get(type);
        if (prototype != null) {
            return (Document) prototype.clone();
        }
        throw new IllegalArgumentException("Unknown document type: " + type);
    }
}

// Usage
public class Application {
    public static void main(String[] args) {
        DocumentManager manager = new DocumentManager();
        
        // Create documents from prototypes
        Document report1 = manager.createDocument("report");
        report1.setTitle("Monthly Sales Report");
        report1.setAuthor("John Doe");
        
        Document report2 = manager.createDocument("report");
        report2.setTitle("Quarterly Report");
        report2.setAuthor("Jane Smith");
        
        Document letter = manager.createDocument("letter");
        letter.setTitle("Business Letter");
        letter.setAuthor("Manager");
        
        System.out.println("Report 1: " + report1);
        System.out.println("Report 2: " + report2);
        System.out.println("Letter: " + letter);
    }
}
```

### Deep vs Shallow Copy:
```java
public class Employee implements Cloneable {
    private String name;
    private String department;
    private Address address;
    
    public Employee(String name, String department, Address address) {
        this.name = name;
        this.department = department;
        this.address = address;
    }
    
    // Shallow copy
    public Employee shallowClone() {
        return new Employee(this.name, this.department, this.address);
    }
    
    // Deep copy
    public Employee deepClone() {
        Address clonedAddress = new Address(
            this.address.getStreet(),
            this.address.getCity(),
            this.address.getZipCode()
        );
        return new Employee(this.name, this.department, clonedAddress);
    }
}

public class Address {
    private String street;
    private String city;
    private String zipCode;
    
    public Address(String street, String city, String zipCode) {
        this.street = street;
        this.city = city;
        this.zipCode = zipCode;
    }
    
    // Getters and setters
    public String getStreet() { return street; }
    public void setStreet(String street) { this.street = street; }
    
    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }
    
    public String getZipCode() { return zipCode; }
    public void setZipCode(String zipCode) { this.zipCode = zipCode; }
}
```

### Pros and Cons:
**Pros:**
- Reduces object creation cost
- Hides complexity of creating new instances
- Allows adding/removing prototypes at runtime

**Cons:**
- Complex cloning of circular references
- Deep copying can be expensive
- Requires careful implementation of clone method

## 2.6 Object Pool Pattern

The Object Pool pattern maintains a set of initialized objects ready to use, rather than allocating and destroying them on demand. This is useful when object creation is expensive or when you need to limit the number of objects.

### When to Use:
- When object creation is expensive
- When you need to limit the number of objects
- When objects are frequently created and destroyed

### Real-World Analogy:
Think of a car rental service. Instead of manufacturing a new car every time someone wants to rent one, they maintain a pool of cars that can be rented and returned.

### Implementation:
```java
// Pooled object
public class DatabaseConnection {
    private String connectionId;
    private boolean inUse;
    private long lastUsed;
    
    public DatabaseConnection(String connectionId) {
        this.connectionId = connectionId;
        this.inUse = false;
        this.lastUsed = System.currentTimeMillis();
    }
    
    public void connect() {
        System.out.println("Connecting to database with ID: " + connectionId);
    }
    
    public void disconnect() {
        System.out.println("Disconnecting from database with ID: " + connectionId);
    }
    
    public void executeQuery(String query) {
        System.out.println("Executing query: " + query + " on connection: " + connectionId);
    }
    
    // Getters and setters
    public String getConnectionId() { return connectionId; }
    public boolean isInUse() { return inUse; }
    public void setInUse(boolean inUse) { this.inUse = inUse; }
    public long getLastUsed() { return lastUsed; }
    public void setLastUsed(long lastUsed) { this.lastUsed = lastUsed; }
}

// Object pool
public class DatabaseConnectionPool {
    private List<DatabaseConnection> availableConnections;
    private List<DatabaseConnection> usedConnections;
    private int maxSize;
    
    public DatabaseConnectionPool(int maxSize) {
        this.maxSize = maxSize;
        this.availableConnections = new ArrayList<>();
        this.usedConnections = new ArrayList<>();
        initializePool();
    }
    
    private void initializePool() {
        for (int i = 0; i < maxSize; i++) {
            DatabaseConnection connection = new DatabaseConnection("conn-" + i);
            availableConnections.add(connection);
        }
    }
    
    public synchronized DatabaseConnection getConnection() {
        if (availableConnections.isEmpty()) {
            throw new RuntimeException("No available connections in pool");
        }
        
        DatabaseConnection connection = availableConnections.remove(0);
        connection.setInUse(true);
        connection.setLastUsed(System.currentTimeMillis());
        usedConnections.add(connection);
        
        return connection;
    }
    
    public synchronized void releaseConnection(DatabaseConnection connection) {
        if (usedConnections.remove(connection)) {
            connection.setInUse(false);
            connection.setLastUsed(System.currentTimeMillis());
            availableConnections.add(connection);
        }
    }
    
    public synchronized void closeAllConnections() {
        for (DatabaseConnection connection : availableConnections) {
            connection.disconnect();
        }
        for (DatabaseConnection connection : usedConnections) {
            connection.disconnect();
        }
        availableConnections.clear();
        usedConnections.clear();
    }
    
    public int getAvailableConnectionsCount() {
        return availableConnections.size();
    }
    
    public int getUsedConnectionsCount() {
        return usedConnections.size();
    }
}

// Usage
public class Application {
    public static void main(String[] args) {
        DatabaseConnectionPool pool = new DatabaseConnectionPool(3);
        
        try {
            // Get connections from pool
            DatabaseConnection conn1 = pool.getConnection();
            DatabaseConnection conn2 = pool.getConnection();
            
            // Use connections
            conn1.connect();
            conn1.executeQuery("SELECT * FROM users");
            
            conn2.connect();
            conn2.executeQuery("SELECT * FROM orders");
            
            System.out.println("Available connections: " + pool.getAvailableConnectionsCount());
            System.out.println("Used connections: " + pool.getUsedConnectionsCount());
            
            // Release connections back to pool
            pool.releaseConnection(conn1);
            pool.releaseConnection(conn2);
            
            System.out.println("After release - Available connections: " + pool.getAvailableConnectionsCount());
            
        } finally {
            pool.closeAllConnections();
        }
    }
}
```

### Pros and Cons:
**Pros:**
- Reduces object creation overhead
- Controls resource usage
- Improves performance for expensive objects

**Cons:**
- Increases memory usage
- Objects may retain state between uses
- Complex pool management

## 2.7 Lazy Initialization Pattern

The Lazy Initialization pattern delays the creation of an object until it's actually needed. This can improve performance and reduce memory usage when objects are expensive to create or not always needed.

### When to Use:
- When object creation is expensive
- When objects are not always needed
- When you want to optimize memory usage

### Real-World Analogy:
Think of a library that doesn't load all books into memory at once, but only loads a book when someone actually wants to read it.

### Basic Implementation:
```java
public class LazyInitializedSingleton {
    private static LazyInitializedSingleton instance;
    
    private LazyInitializedSingleton() {
        System.out.println("Creating LazyInitializedSingleton instance");
    }
    
    public static LazyInitializedSingleton getInstance() {
        if (instance == null) {
            instance = new LazyInitializedSingleton();
        }
        return instance;
    }
    
    public void doSomething() {
        System.out.println("Doing something...");
    }
}

// Usage
public class Application {
    public static void main(String[] args) {
        System.out.println("Application started");
        
        // Instance is not created yet
        System.out.println("About to get instance...");
        
        LazyInitializedSingleton instance = LazyInitializedSingleton.getInstance();
        instance.doSomething();
        
        // Second call returns the same instance
        LazyInitializedSingleton instance2 = LazyInitializedSingleton.getInstance();
        System.out.println("Same instance? " + (instance == instance2));
    }
}
```

### Lazy Initialization with Holder Class:
```java
public class LazyInitializedService {
    private String data;
    
    private LazyInitializedService() {
        // Expensive initialization
        System.out.println("Initializing expensive service...");
        try {
            Thread.sleep(2000); // Simulate expensive operation
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        this.data = "Expensive data loaded";
    }
    
    public String getData() {
        return data;
    }
    
    // Lazy holder class
    private static class ServiceHolder {
        private static final LazyInitializedService INSTANCE = new LazyInitializedService();
    }
    
    public static LazyInitializedService getInstance() {
        return ServiceHolder.INSTANCE;
    }
}

// Usage
public class Application {
    public static void main(String[] args) {
        System.out.println("Application started");
        
        // Service is not initialized yet
        System.out.println("About to get service...");
        
        LazyInitializedService service = LazyInitializedService.getInstance();
        System.out.println("Data: " + service.getData());
    }
}
```

### Lazy Initialization for Collections:
```java
public class UserService {
    private List<User> users;
    
    public List<User> getUsers() {
        if (users == null) {
            users = loadUsersFromDatabase();
        }
        return users;
    }
    
    private List<User> loadUsersFromDatabase() {
        System.out.println("Loading users from database...");
        // Simulate database call
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        List<User> userList = new ArrayList<>();
        userList.add(new User("John", "john@example.com"));
        userList.add(new User("Jane", "jane@example.com"));
        return userList;
    }
    
    public void addUser(User user) {
        getUsers().add(user);
    }
    
    public void clearCache() {
        users = null;
    }
}

public class User {
    private String name;
    private String email;
    
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }
    
    // Getters and setters
    public String getName() { return name; }
    public String getEmail() { return email; }
}
```

### Pros and Cons:
**Pros:**
- Reduces startup time
- Saves memory when objects aren't needed
- Improves performance

**Cons:**
- Can cause unexpected delays when object is first accessed
- Thread safety concerns
- Makes code more complex

## 2.8 Dependency Injection Pattern

The Dependency Injection pattern is a design pattern that implements Inversion of Control (IoC) for resolving dependencies. Instead of objects creating their dependencies, dependencies are injected into the object.

### When to Use:
- When you want to decouple classes from their dependencies
- When you need to make code more testable
- When you want to follow the Dependency Inversion Principle

### Real-World Analogy:
Think of a car and its engine. Instead of the car manufacturing its own engine (tight coupling), the engine is built separately and then installed into the car (dependency injection).

### Constructor Injection:
```java
// Service interface
public interface EmailService {
    void sendEmail(String to, String subject, String body);
}

// Concrete implementation
public class SMTPEmailService implements EmailService {
    public void sendEmail(String to, String subject, String body) {
        System.out.println("Sending email via SMTP to: " + to);
        System.out.println("Subject: " + subject);
        System.out.println("Body: " + body);
    }
}

// Another implementation
public class SendGridEmailService implements EmailService {
    public void sendEmail(String to, String subject, String body) {
        System.out.println("Sending email via SendGrid to: " + to);
        System.out.println("Subject: " + subject);
        System.out.println("Body: " + body);
    }
}

// Service that depends on EmailService
public class UserService {
    private EmailService emailService;
    
    // Constructor injection
    public UserService(EmailService emailService) {
        this.emailService = emailService;
    }
    
    public void registerUser(String email, String name) {
        // Register user logic
        System.out.println("Registering user: " + name + " with email: " + email);
        
        // Send welcome email
        emailService.sendEmail(email, "Welcome!", "Welcome to our service, " + name + "!");
    }
}

// Usage
public class Application {
    public static void main(String[] args) {
        // Inject SMTP email service
        EmailService smtpService = new SMTPEmailService();
        UserService userService1 = new UserService(smtpService);
        userService1.registerUser("user1@example.com", "John Doe");
        
        // Inject SendGrid email service
        EmailService sendGridService = new SendGridEmailService();
        UserService userService2 = new UserService(sendGridService);
        userService2.registerUser("user2@example.com", "Jane Smith");
    }
}
```

### Setter Injection:
```java
public class OrderService {
    private PaymentService paymentService;
    private NotificationService notificationService;
    
    // Setter injection
    public void setPaymentService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
    
    public void setNotificationService(NotificationService notificationService) {
        this.notificationService = notificationService;
    }
    
    public void processOrder(Order order) {
        // Process payment
        if (paymentService != null) {
            paymentService.processPayment(order.getAmount());
        }
        
        // Send notification
        if (notificationService != null) {
            notificationService.sendNotification("Order processed successfully");
        }
    }
}

public interface PaymentService {
    void processPayment(double amount);
}

public interface NotificationService {
    void sendNotification(String message);
}
```

### Interface Injection:
```java
public interface ServiceLocator {
    <T> T getService(Class<T> serviceType);
}

public class SimpleServiceLocator implements ServiceLocator {
    private Map<Class<?>, Object> services = new HashMap<>();
    
    public <T> void registerService(Class<T> serviceType, T service) {
        services.put(serviceType, service);
    }
    
    @SuppressWarnings("unchecked")
    public <T> T getService(Class<T> serviceType) {
        return (T) services.get(serviceType);
    }
}

public class OrderProcessor {
    private ServiceLocator serviceLocator;
    
    public OrderProcessor(ServiceLocator serviceLocator) {
        this.serviceLocator = serviceLocator;
    }
    
    public void processOrder(Order order) {
        PaymentService paymentService = serviceLocator.getService(PaymentService.class);
        NotificationService notificationService = serviceLocator.getService(NotificationService.class);
        
        paymentService.processPayment(order.getAmount());
        notificationService.sendNotification("Order processed");
    }
}
```

### Pros and Cons:
**Pros:**
- Reduces coupling between classes
- Makes code more testable
- Follows SOLID principles
- Enables configuration changes without code changes

**Cons:**
- Can make code more complex
- Requires dependency injection framework or manual wiring
- Can make dependencies less obvious

## 2.9 Service Locator Pattern

The Service Locator pattern provides a centralized registry for services, allowing clients to locate services without knowing their concrete implementations. It's an alternative to dependency injection.

### When to Use:
- When you need a centralized way to access services
- When you want to decouple service consumers from service providers
- When you need dynamic service resolution

### Real-World Analogy:
Think of a phone directory service. Instead of knowing everyone's phone number directly, you call a directory service to get the number you need.

### Basic Implementation:
```java
// Service interface
public interface DatabaseService {
    void connect();
    void executeQuery(String query);
    void disconnect();
}

// Concrete service implementations
public class MySQLDatabaseService implements DatabaseService {
    public void connect() {
        System.out.println("Connecting to MySQL database");
    }
    
    public void executeQuery(String query) {
        System.out.println("Executing MySQL query: " + query);
    }
    
    public void disconnect() {
        System.out.println("Disconnecting from MySQL database");
    }
}

public class PostgreSQLDatabaseService implements DatabaseService {
    public void connect() {
        System.out.println("Connecting to PostgreSQL database");
    }
    
    public void executeQuery(String query) {
        System.out.println("Executing PostgreSQL query: " + query);
    }
    
    public void disconnect() {
        System.out.println("Disconnecting from PostgreSQL database");
    }
}

// Service locator
public class ServiceLocator {
    private static ServiceLocator instance;
    private Map<String, Object> services;
    
    private ServiceLocator() {
        services = new HashMap<>();
    }
    
    public static ServiceLocator getInstance() {
        if (instance == null) {
            instance = new ServiceLocator();
        }
        return instance;
    }
    
    public void registerService(String name, Object service) {
        services.put(name, service);
    }
    
    @SuppressWarnings("unchecked")
    public <T> T getService(String name, Class<T> serviceType) {
        Object service = services.get(name);
        if (service == null) {
            throw new RuntimeException("Service not found: " + name);
        }
        return (T) service;
    }
    
    public <T> T getService(Class<T> serviceType) {
        for (Object service : services.values()) {
            if (serviceType.isInstance(service)) {
                return serviceType.cast(service);
            }
        }
        throw new RuntimeException("Service not found for type: " + serviceType.getName());
    }
}

// Client code
public class UserRepository {
    private DatabaseService databaseService;
    
    public UserRepository() {
        // Get service from locator
        this.databaseService = ServiceLocator.getInstance().getService(DatabaseService.class);
    }
    
    public void saveUser(User user) {
        databaseService.connect();
        databaseService.executeQuery("INSERT INTO users VALUES ('" + user.getName() + "')");
        databaseService.disconnect();
    }
}

// Usage
public class Application {
    public static void main(String[] args) {
        ServiceLocator locator = ServiceLocator.getInstance();
        
        // Register services
        locator.registerService("mysql", new MySQLDatabaseService());
        locator.registerService("postgresql", new PostgreSQLDatabaseService());
        
        // Use service
        UserRepository userRepo = new UserRepository();
        userRepo.saveUser(new User("John Doe"));
        
        // Switch to different database
        locator.registerService("database", new PostgreSQLDatabaseService());
        UserRepository userRepo2 = new UserRepository();
        userRepo2.saveUser(new User("Jane Smith"));
    }
}
```

### Advanced Service Locator with Factory:
```java
public interface ServiceFactory<T> {
    T createService();
}

public class DatabaseServiceFactory implements ServiceFactory<DatabaseService> {
    private String databaseType;
    
    public DatabaseServiceFactory(String databaseType) {
        this.databaseType = databaseType;
    }
    
    public DatabaseService createService() {
        switch (databaseType.toLowerCase()) {
            case "mysql":
                return new MySQLDatabaseService();
            case "postgresql":
                return new PostgreSQLDatabaseService();
            default:
                throw new IllegalArgumentException("Unknown database type: " + databaseType);
        }
    }
}

public class AdvancedServiceLocator {
    private static AdvancedServiceLocator instance;
    private Map<Class<?>, ServiceFactory<?>> factories;
    private Map<Class<?>, Object> singletons;
    
    private AdvancedServiceLocator() {
        factories = new HashMap<>();
        singletons = new HashMap<>();
    }
    
    public static AdvancedServiceLocator getInstance() {
        if (instance == null) {
            instance = new AdvancedServiceLocator();
        }
        return instance;
    }
    
    public <T> void registerFactory(Class<T> serviceType, ServiceFactory<T> factory) {
        factories.put(serviceType, factory);
    }
    
    public <T> void registerSingleton(Class<T> serviceType, T service) {
        singletons.put(serviceType, service);
    }
    
    @SuppressWarnings("unchecked")
    public <T> T getService(Class<T> serviceType) {
        // Check if singleton exists
        if (singletons.containsKey(serviceType)) {
            return (T) singletons.get(serviceType);
        }
        
        // Create new instance using factory
        ServiceFactory<T> factory = (ServiceFactory<T>) factories.get(serviceType);
        if (factory != null) {
            T service = factory.createService();
            return service;
        }
        
        throw new RuntimeException("No service registered for type: " + serviceType.getName());
    }
}
```

### Pros and Cons:
**Pros:**
- Centralized service management
- Decouples service consumers from providers
- Enables dynamic service resolution
- Can support both singletons and factories

**Cons:**
- Creates hidden dependencies
- Makes testing more difficult
- Can become a bottleneck
- Less explicit than dependency injection

## 2.10 Registry Pattern

The Registry pattern provides a centralized way to store and retrieve objects by name or key. It's similar to a service locator but more general-purpose and can store any type of object.

### When to Use:
- When you need to store and retrieve objects by key
- When you want to share objects across different parts of an application
- When you need a simple object storage mechanism

### Real-World Analogy:
Think of a library catalog system. Books are stored in the library and can be retrieved by their catalog number or title.

### Basic Implementation:
```java
public class Registry {
    private static Registry instance;
    private Map<String, Object> registry;
    
    private Registry() {
        registry = new HashMap<>();
    }
    
    public static Registry getInstance() {
        if (instance == null) {
            instance = new Registry();
        }
        return instance;
    }
    
    public void register(String key, Object value) {
        registry.put(key, value);
    }
    
    @SuppressWarnings("unchecked")
    public <T> T get(String key, Class<T> type) {
        Object value = registry.get(key);
        if (value == null) {
            throw new RuntimeException("No object registered for key: " + key);
        }
        if (!type.isInstance(value)) {
            throw new RuntimeException("Object for key " + key + " is not of type " + type.getName());
        }
        return (T) value;
    }
    
    public Object get(String key) {
        return registry.get(key);
    }
    
    public boolean contains(String key) {
        return registry.containsKey(key);
    }
    
    public void unregister(String key) {
        registry.remove(key);
    }
    
    public void clear() {
        registry.clear();
    }
    
    public Set<String> getKeys() {
        return new HashSet<>(registry.keySet());
    }
}

// Usage
public class Application {
    public static void main(String[] args) {
        Registry registry = Registry.getInstance();
        
        // Register different types of objects
        registry.register("database", new MySQLDatabaseService());
        registry.register("email", new SMTPEmailService());
        registry.register("config", new ApplicationConfig());
        
        // Retrieve objects
        DatabaseService db = registry.get("database", DatabaseService.class);
        EmailService email = registry.get("email", EmailService.class);
        ApplicationConfig config = registry.get("config", ApplicationConfig.class);
        
        // Use the objects
        db.connect();
        email.sendEmail("test@example.com", "Test", "Test message");
        System.out.println("App name: " + config.getAppName());
    }
}

public class ApplicationConfig {
    private String appName;
    private String version;
    
    public ApplicationConfig() {
        this.appName = "My Application";
        this.version = "1.0.0";
    }
    
    public String getAppName() { return appName; }
    public String getVersion() { return version; }
}
```

### Typed Registry:
```java
public class TypedRegistry {
    private static TypedRegistry instance;
    private Map<Class<?>, Object> registry;
    
    private TypedRegistry() {
        registry = new HashMap<>();
    }
    
    public static TypedRegistry getInstance() {
        if (instance == null) {
            instance = new TypedRegistry();
        }
        return instance;
    }
    
    public <T> void register(Class<T> type, T instance) {
        registry.put(type, instance);
    }
    
    @SuppressWarnings("unchecked")
    public <T> T get(Class<T> type) {
        Object instance = registry.get(type);
        if (instance == null) {
            throw new RuntimeException("No instance registered for type: " + type.getName());
        }
        return (T) instance;
    }
    
    public <T> boolean contains(Class<T> type) {
        return registry.containsKey(type);
    }
    
    public <T> void unregister(Class<T> type) {
        registry.remove(type);
    }
}

// Usage
public class Application {
    public static void main(String[] args) {
        TypedRegistry registry = TypedRegistry.getInstance();
        
        // Register by type
        registry.register(DatabaseService.class, new MySQLDatabaseService());
        registry.register(EmailService.class, new SMTPEmailService());
        
        // Retrieve by type
        DatabaseService db = registry.get(DatabaseService.class);
        EmailService email = registry.get(EmailService.class);
        
        db.connect();
        email.sendEmail("test@example.com", "Test", "Test message");
    }
}
```

### Thread-Safe Registry:
```java
public class ThreadSafeRegistry {
    private static ThreadSafeRegistry instance;
    private final Map<String, Object> registry;
    private final ReadWriteLock lock;
    
    private ThreadSafeRegistry() {
        registry = new HashMap<>();
        lock = new ReentrantReadWriteLock();
    }
    
    public static ThreadSafeRegistry getInstance() {
        if (instance == null) {
            synchronized (ThreadSafeRegistry.class) {
                if (instance == null) {
                    instance = new ThreadSafeRegistry();
                }
            }
        }
        return instance;
    }
    
    public void register(String key, Object value) {
        lock.writeLock().lock();
        try {
            registry.put(key, value);
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    public Object get(String key) {
        lock.readLock().lock();
        try {
            return registry.get(key);
        } finally {
            lock.readLock().unlock();
        }
    }
    
    public boolean contains(String key) {
        lock.readLock().lock();
        try {
            return registry.containsKey(key);
        } finally {
            lock.readLock().unlock();
        }
    }
    
    public void unregister(String key) {
        lock.writeLock().lock();
        try {
            registry.remove(key);
        } finally {
            lock.writeLock().unlock();
        }
    }
}
```

### Pros and Cons:
**Pros:**
- Simple object storage and retrieval
- Centralized object management
- Can store any type of object
- Easy to implement

**Cons:**
- Can become a bottleneck
- Makes dependencies less explicit
- Can lead to tight coupling
- Thread safety concerns in multi-threaded environments

This comprehensive coverage of creational patterns provides the foundation for understanding how objects are created and managed in software systems. Each pattern addresses specific creation scenarios and offers different trade-offs in terms of flexibility, complexity, and performance.