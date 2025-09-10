# Section 4 - Behavioral Patterns

## 4.1 Observer Pattern

The Observer pattern defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

### When to Use:
- When changes to one object require changing multiple dependent objects
- When an object should notify other objects without knowing who they are
- When you need to broadcast changes to multiple subscribers

### Real-World Analogy:
Think of a news agency and its subscribers. When news breaks, all subscribers are automatically notified without the agency knowing who they are.

### Implementation:
```java
// Subject interface
public interface Subject {
    void registerObserver(Observer observer);
    void removeObserver(Observer observer);
    void notifyObservers();
}

// Observer interface
public interface Observer {
    void update(String message);
}

// Concrete subject
public class NewsAgency implements Subject {
    private List<Observer> observers;
    private String news;
    
    public NewsAgency() {
        observers = new ArrayList<>();
    }
    
    public void registerObserver(Observer observer) {
        observers.add(observer);
    }
    
    public void removeObserver(Observer observer) {
        observers.remove(observer);
    }
    
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

// Concrete observers
public class NewsChannel implements Observer {
    private String name;
    
    public NewsChannel(String name) {
        this.name = name;
    }
    
    public void update(String news) {
        System.out.println(name + " received news: " + news);
    }
}
```

## 4.2 Strategy Pattern

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.

### When to Use:
- When you have multiple ways to perform a task
- When you want to switch algorithms at runtime
- When you want to avoid conditional statements for algorithm selection

### Real-World Analogy:
Think of different payment methods (credit card, PayPal, bank transfer) - each is a different strategy for paying, but the payment process remains the same.

### Implementation:
```java
// Strategy interface
public interface PaymentStrategy {
    void pay(int amount);
}

// Concrete strategies
public class CreditCardPayment implements PaymentStrategy {
    public void pay(int amount) {
        System.out.println("Paid " + amount + " using Credit Card");
    }
}

public class PayPalPayment implements PaymentStrategy {
    public void pay(int amount) {
        System.out.println("Paid " + amount + " using PayPal");
    }
}

public class BankTransferPayment implements PaymentStrategy {
    public void pay(int amount) {
        System.out.println("Paid " + amount + " using Bank Transfer");
    }
}

// Context
public class PaymentProcessor {
    private PaymentStrategy paymentStrategy;
    
    public void setPaymentStrategy(PaymentStrategy paymentStrategy) {
        this.paymentStrategy = paymentStrategy;
    }
    
    public void processPayment(int amount) {
        paymentStrategy.pay(amount);
    }
}
```

## 4.3 Command Pattern

The Command pattern encapsulates a request as an object, allowing you to parameterize clients with different requests, queue or log requests, and support undoable operations.

### When to Use:
- When you want to parameterize objects with operations
- When you want to queue, log, or support undo operations
- When you want to support macro operations

### Real-World Analogy:
Think of a remote control with buttons. Each button press is a command that can be stored, queued, or undone.

### Implementation:
```java
// Command interface
public interface Command {
    void execute();
    void undo();
}

// Concrete commands
public class LightOnCommand implements Command {
    private Light light;
    
    public LightOnCommand(Light light) {
        this.light = light;
    }
    
    public void execute() {
        light.turnOn();
    }
    
    public void undo() {
        light.turnOff();
    }
}

public class LightOffCommand implements Command {
    private Light light;
    
    public LightOffCommand(Light light) {
        this.light = light;
    }
    
    public void execute() {
        light.turnOff();
    }
    
    public void undo() {
        light.turnOn();
    }
}

// Receiver
public class Light {
    public void turnOn() {
        System.out.println("Light is ON");
    }
    
    public void turnOff() {
        System.out.println("Light is OFF");
    }
}

// Invoker
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

## 4.4 State Pattern

The State pattern allows an object to alter its behavior when its internal state changes.

### When to Use:
- When an object's behavior depends on its state
- When you have many conditional statements based on object state
- When you want to make state transitions explicit

### Real-World Analogy:
Think of a traffic light that changes its behavior (red, yellow, green) based on its current state.

### Implementation:
```java
// State interface
public interface State {
    void handle(Context context);
}

// Concrete states
public class RedState implements State {
    public void handle(Context context) {
        System.out.println("Red light - Stop!");
        context.setState(new GreenState());
    }
}

public class GreenState implements State {
    public void handle(Context context) {
        System.out.println("Green light - Go!");
        context.setState(new YellowState());
    }
}

public class YellowState implements State {
    public void handle(Context context) {
        System.out.println("Yellow light - Slow down!");
        context.setState(new RedState());
    }
}

// Context
public class TrafficLight {
    private State state;
    
    public TrafficLight() {
        this.state = new RedState();
    }
    
    public void setState(State state) {
        this.state = state;
    }
    
    public void change() {
        state.handle(this);
    }
}
```

## 4.5 Template Method Pattern

The Template Method pattern defines the skeleton of an algorithm in a method, deferring some steps to subclasses.

### When to Use:
- When you have an algorithm with invariant steps
- When you want to control the algorithm's structure
- When you want to avoid code duplication

### Real-World Analogy:
Think of a recipe template. The basic steps (prepare ingredients, cook, serve) are the same, but the specific details vary for each dish.

### Implementation:
```java
// Abstract class with template method
public abstract class DataProcessor {
    // Template method
    public final void processData(String data) {
        String processedData = preprocess(data);
        String result = process(processedData);
        postprocess(result);
    }
    
    // Concrete steps
    protected String preprocess(String data) {
        System.out.println("Preprocessing data...");
        return data.trim().toLowerCase();
    }
    
    // Abstract step
    protected abstract String process(String data);
    
    // Concrete step
    protected void postprocess(String result) {
        System.out.println("Postprocessing result: " + result);
    }
}

// Concrete implementations
public class TextProcessor extends DataProcessor {
    protected String process(String data) {
        System.out.println("Processing text data...");
        return data.replaceAll("\\s+", " ");
    }
}

public class NumberProcessor extends DataProcessor {
    protected String process(String data) {
        System.out.println("Processing number data...");
        return data.replaceAll("[^0-9]", "");
    }
}
```

## 4.6 Visitor Pattern

The Visitor pattern represents an operation to be performed on elements of an object structure without changing the classes of the elements.

### When to Use:
- When you have many unrelated operations on object structure
- When you want to add new operations without changing existing classes
- When the object structure is stable but operations change frequently

### Real-World Analogy:
Think of a tax inspector visiting different types of businesses. Each business type has different tax calculations, but the inspector can visit all of them using the same process.

### Implementation:
```java
// Element interface
public interface Element {
    void accept(Visitor visitor);
}

// Concrete elements
public class Book implements Element {
    private String title;
    private double price;
    
    public Book(String title, double price) {
        this.title = title;
        this.price = price;
    }
    
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
    
    public double getPrice() { return price; }
    public String getTitle() { return title; }
}

public class Fruit implements Element {
    private String name;
    private double weight;
    private double pricePerKg;
    
    public Fruit(String name, double weight, double pricePerKg) {
        this.name = name;
        this.weight = weight;
        this.pricePerKg = pricePerKg;
    }
    
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
    
    public double getWeight() { return weight; }
    public double getPricePerKg() { return pricePerKg; }
    public String getName() { return name; }
}

// Visitor interface
public interface Visitor {
    void visit(Book book);
    void visit(Fruit fruit);
}

// Concrete visitor
public class ShoppingCartVisitor implements Visitor {
    private double totalCost = 0;
    
    public void visit(Book book) {
        totalCost += book.getPrice();
        System.out.println("Book: " + book.getTitle() + " - $" + book.getPrice());
    }
    
    public void visit(Fruit fruit) {
        double cost = fruit.getWeight() * fruit.getPricePerKg();
        totalCost += cost;
        System.out.println("Fruit: " + fruit.getName() + " - $" + cost);
    }
    
    public double getTotalCost() {
        return totalCost;
    }
}
```

## 4.7 Iterator Pattern

The Iterator pattern provides a way to access elements of an aggregate object sequentially without exposing its underlying representation.

### When to Use:
- When you want to access elements of a collection without exposing its structure
- When you want to support multiple traversals of the same collection
- When you want to provide a uniform interface for different collection types

### Real-World Analogy:
Think of a TV remote control that lets you navigate through channels without knowing how the channel list is stored internally.

### Implementation:
```java
// Iterator interface
public interface Iterator<T> {
    boolean hasNext();
    T next();
}

// Aggregate interface
public interface Container<T> {
    Iterator<T> getIterator();
}

// Concrete aggregate
public class NameRepository implements Container<String> {
    private String[] names = {"Robert", "John", "Julie", "Lora"};
    
    public Iterator<String> getIterator() {
        return new NameIterator();
    }
    
    // Concrete iterator
    private class NameIterator implements Iterator<String> {
        int index;
        
        public boolean hasNext() {
            return index < names.length;
        }
        
        public String next() {
            if (hasNext()) {
                return names[index++];
            }
            return null;
        }
    }
}
```

## 4.8 Mediator Pattern

The Mediator pattern defines how a set of objects interact by encapsulating their communication in a mediator object.

### When to Use:
- When communication between objects is complex
- When you want to reduce coupling between objects
- When you want to centralize communication logic

### Real-World Analogy:
Think of an air traffic control tower that coordinates communication between aircraft without them talking directly to each other.

### Implementation:
```java
// Mediator interface
public interface ChatMediator {
    void sendMessage(String message, User user);
    void addUser(User user);
}

// Concrete mediator
public class ChatRoom implements ChatMediator {
    private List<User> users;
    
    public ChatRoom() {
        users = new ArrayList<>();
    }
    
    public void addUser(User user) {
        users.add(user);
    }
    
    public void sendMessage(String message, User user) {
        for (User u : users) {
            if (u != user) {
                u.receive(message);
            }
        }
    }
}

// Colleague
public abstract class User {
    protected ChatMediator mediator;
    protected String name;
    
    public User(ChatMediator mediator, String name) {
        this.mediator = mediator;
        this.name = name;
    }
    
    public abstract void send(String message);
    public abstract void receive(String message);
}

// Concrete colleague
public class ChatUser extends User {
    public ChatUser(ChatMediator mediator, String name) {
        super(mediator, name);
    }
    
    public void send(String message) {
        System.out.println(name + " sends: " + message);
        mediator.sendMessage(message, this);
    }
    
    public void receive(String message) {
        System.out.println(name + " receives: " + message);
    }
}
```

## 4.9 Memento Pattern

The Memento pattern captures and externalizes an object's internal state so that the object can be restored to this state later.

### When to Use:
- When you need to save and restore object state
- When you want to implement undo functionality
- When you want to provide checkpoints in long operations

### Real-World Analogy:
Think of a video game save system that allows you to save your progress and restore it later.

### Implementation:
```java
// Memento
public class Memento {
    private String state;
    
    public Memento(String state) {
        this.state = state;
    }
    
    public String getState() {
        return state;
    }
}

// Originator
public class TextEditor {
    private String content;
    
    public void setContent(String content) {
        this.content = content;
    }
    
    public String getContent() {
        return content;
    }
    
    public Memento save() {
        return new Memento(content);
    }
    
    public void restore(Memento memento) {
        content = memento.getState();
    }
}

// Caretaker
public class TextEditorHistory {
    private List<Memento> history;
    
    public TextEditorHistory() {
        history = new ArrayList<>();
    }
    
    public void save(Memento memento) {
        history.add(memento);
    }
    
    public Memento undo() {
        if (!history.isEmpty()) {
            return history.remove(history.size() - 1);
        }
        return null;
    }
}
```

## 4.10 Chain of Responsibility Pattern

The Chain of Responsibility pattern passes requests along a chain of handlers, where each handler decides whether to process the request or pass it to the next handler.

### When to Use:
- When you want to decouple the sender and receiver of a request
- When you want to give multiple objects a chance to handle a request
- When you want to specify handlers dynamically

### Real-World Analogy:
Think of a customer service system where requests are passed through different levels (front desk, supervisor, manager) until someone can handle it.

### Implementation:
```java
// Handler interface
public abstract class Handler {
    protected Handler nextHandler;
    
    public void setNext(Handler nextHandler) {
        this.nextHandler = nextHandler;
    }
    
    public abstract void handleRequest(Request request);
}

// Concrete handlers
public class FrontDeskHandler extends Handler {
    public void handleRequest(Request request) {
        if (request.getType().equals("simple")) {
            System.out.println("Front desk handles: " + request.getDescription());
        } else if (nextHandler != null) {
            nextHandler.handleRequest(request);
        }
    }
}

public class SupervisorHandler extends Handler {
    public void handleRequest(Request request) {
        if (request.getType().equals("complex")) {
            System.out.println("Supervisor handles: " + request.getDescription());
        } else if (nextHandler != null) {
            nextHandler.handleRequest(request);
        }
    }
}

public class ManagerHandler extends Handler {
    public void handleRequest(Request request) {
        if (request.getType().equals("urgent")) {
            System.out.println("Manager handles: " + request.getDescription());
        } else if (nextHandler != null) {
            nextHandler.handleRequest(request);
        }
    }
}

// Request class
public class Request {
    private String type;
    private String description;
    
    public Request(String type, String description) {
        this.type = type;
        this.description = description;
    }
    
    public String getType() { return type; }
    public String getDescription() { return description; }
}
```

This section covers the essential behavioral patterns that define how objects interact and communicate with each other, making systems more flexible and maintainable.