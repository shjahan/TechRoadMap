# Section 6 - Enterprise Patterns

## 6.1 Model-View-Controller (MVC)

The MVC pattern separates an application into three interconnected components: Model (data), View (user interface), and Controller (business logic).

### When to Use:
- When you want to separate concerns in your application
- When you need to support multiple views of the same data
- When you want to make your application more maintainable

### Real-World Analogy:
Think of a restaurant where the kitchen (Model) prepares food, the waiter (Controller) takes orders and coordinates, and the dining room (View) presents the food to customers.

### Implementation:
```java
// Model
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

// View
public class UserView {
    public void displayUser(User user) {
        System.out.println("User: " + user.getName());
        System.out.println("Email: " + user.getEmail());
    }
    
    public void displayMessage(String message) {
        System.out.println("Message: " + message);
    }
}

// Controller
public class UserController {
    private User model;
    private UserView view;
    
    public UserController(User model, UserView view) {
        this.model = model;
        this.view = view;
    }
    
    public void updateView() {
        view.displayUser(model);
    }
    
    public void setUserName(String name) {
        model.setName(name);
    }
    
    public void setUserEmail(String email) {
        model.setEmail(email);
    }
}
```

## 6.2 Model-View-Presenter (MVP)

The MVP pattern is similar to MVC but with a clearer separation between the View and the business logic through a Presenter.

### When to Use:
- When you want a clearer separation between View and business logic
- When you need to make the View more testable
- When you want to reduce coupling between components

### Implementation:
```java
// Model
public class Task {
    private String title;
    private boolean completed;
    
    public Task(String title) {
        this.title = title;
        this.completed = false;
    }
    
    // Getters and setters
    public String getTitle() { return title; }
    public boolean isCompleted() { return completed; }
    public void setCompleted(boolean completed) { this.completed = completed; }
}

// View interface
public interface TaskView {
    void displayTasks(List<Task> tasks);
    void showMessage(String message);
    String getNewTaskTitle();
}

// Presenter
public class TaskPresenter {
    private List<Task> tasks;
    private TaskView view;
    
    public TaskPresenter(TaskView view) {
        this.tasks = new ArrayList<>();
        this.view = view;
    }
    
    public void addTask() {
        String title = view.getNewTaskTitle();
        if (title != null && !title.trim().isEmpty()) {
            tasks.add(new Task(title));
            view.displayTasks(tasks);
            view.showMessage("Task added successfully");
        }
    }
    
    public void toggleTask(int index) {
        if (index >= 0 && index < tasks.size()) {
            Task task = tasks.get(index);
            task.setCompleted(!task.isCompleted());
            view.displayTasks(tasks);
        }
    }
}
```

## 6.3 Model-View-ViewModel (MVVM)

The MVVM pattern uses data binding to connect the View and ViewModel, making the View automatically update when the ViewModel changes.

### When to Use:
- When you want to use data binding
- When you need to support multiple views
- When you want to make the View more declarative

### Implementation:
```java
// Model
public class Product {
    private String name;
    private double price;
    private int quantity;
    
    public Product(String name, double price, int quantity) {
        this.name = name;
        this.price = price;
        this.quantity = quantity;
    }
    
    // Getters and setters
    public String getName() { return name; }
    public double getPrice() { return price; }
    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }
}

// ViewModel
public class ProductViewModel {
    private List<Product> products;
    private Product selectedProduct;
    
    public ProductViewModel() {
        this.products = new ArrayList<>();
        loadProducts();
    }
    
    private void loadProducts() {
        products.add(new Product("Laptop", 999.99, 10));
        products.add(new Product("Mouse", 29.99, 50));
        products.add(new Product("Keyboard", 79.99, 25));
    }
    
    public List<Product> getProducts() {
        return products;
    }
    
    public Product getSelectedProduct() {
        return selectedProduct;
    }
    
    public void setSelectedProduct(Product product) {
        this.selectedProduct = product;
    }
    
    public void updateQuantity(int newQuantity) {
        if (selectedProduct != null) {
            selectedProduct.setQuantity(newQuantity);
        }
    }
}
```

## 6.4 Service Layer Pattern

The Service Layer pattern encapsulates business logic and provides a uniform interface to the presentation layer.

### When to Use:
- When you want to encapsulate business logic
- When you need to provide a uniform interface
- When you want to separate business logic from presentation logic

### Implementation:
```java
// Service interface
public interface UserService {
    User createUser(String name, String email);
    User getUserById(Long id);
    List<User> getAllUsers();
    void updateUser(User user);
    void deleteUser(Long id);
}

// Service implementation
public class UserServiceImpl implements UserService {
    private UserRepository userRepository;
    private EmailService emailService;
    
    public UserServiceImpl(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }
    
    public User createUser(String name, String email) {
        // Business logic
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Name cannot be empty");
        }
        if (email == null || !email.contains("@")) {
            throw new IllegalArgumentException("Invalid email");
        }
        
        User user = new User(name, email);
        user = userRepository.save(user);
        
        // Send welcome email
        emailService.sendWelcomeEmail(user.getEmail());
        
        return user;
    }
    
    public User getUserById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new UserNotFoundException("User not found"));
    }
    
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }
    
    public void updateUser(User user) {
        userRepository.save(user);
    }
    
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
}
```

## 6.5 Data Access Object (DAO)

The DAO pattern provides an abstract interface to some type of database or persistence mechanism.

### When to Use:
- When you want to separate data access logic from business logic
- When you need to support multiple data sources
- When you want to make data access more testable

### Implementation:
```java
// DAO interface
public interface UserDAO {
    void save(User user);
    User findById(Long id);
    List<User> findAll();
    void update(User user);
    void delete(Long id);
}

// DAO implementation
public class UserDAOImpl implements UserDAO {
    private Map<Long, User> users;
    private Long nextId;
    
    public UserDAOImpl() {
        this.users = new HashMap<>();
        this.nextId = 1L;
    }
    
    public void save(User user) {
        if (user.getId() == null) {
            user.setId(nextId++);
        }
        users.put(user.getId(), user);
    }
    
    public User findById(Long id) {
        return users.get(id);
    }
    
    public List<User> findAll() {
        return new ArrayList<>(users.values());
    }
    
    public void update(User user) {
        if (users.containsKey(user.getId())) {
            users.put(user.getId(), user);
        }
    }
    
    public void delete(Long id) {
        users.remove(id);
    }
}
```

## 6.6 Repository Pattern

The Repository pattern encapsulates the logic needed to access data sources, centralizing common data access functionality.

### When to Use:
- When you want to centralize data access logic
- When you need to support multiple data sources
- When you want to make data access more testable

### Implementation:
```java
// Repository interface
public interface UserRepository {
    User save(User user);
    Optional<User> findById(Long id);
    List<User> findAll();
    List<User> findByName(String name);
    void deleteById(Long id);
}

// Repository implementation
public class UserRepositoryImpl implements UserRepository {
    private UserDAO userDAO;
    
    public UserRepositoryImpl(UserDAO userDAO) {
        this.userDAO = userDAO;
    }
    
    public User save(User user) {
        return userDAO.save(user);
    }
    
    public Optional<User> findById(Long id) {
        User user = userDAO.findById(id);
        return Optional.ofNullable(user);
    }
    
    public List<User> findAll() {
        return userDAO.findAll();
    }
    
    public List<User> findByName(String name) {
        return userDAO.findAll().stream()
                .filter(user -> user.getName().contains(name))
                .collect(Collectors.toList());
    }
    
    public void deleteById(Long id) {
        userDAO.delete(id);
    }
}
```

## 6.7 Unit of Work Pattern

The Unit of Work pattern maintains a list of objects affected by a business transaction and coordinates writing out changes.

### When to Use:
- When you need to coordinate multiple operations
- When you want to ensure data consistency
- When you need to support transactions

### Implementation:
```java
public class UnitOfWork {
    private List<Object> newObjects;
    private List<Object> dirtyObjects;
    private List<Object> removedObjects;
    
    public UnitOfWork() {
        this.newObjects = new ArrayList<>();
        this.dirtyObjects = new ArrayList<>();
        this.removedObjects = new ArrayList<>();
    }
    
    public void registerNew(Object obj) {
        newObjects.add(obj);
    }
    
    public void registerDirty(Object obj) {
        if (!newObjects.contains(obj) && !dirtyObjects.contains(obj)) {
            dirtyObjects.add(obj);
        }
    }
    
    public void registerRemoved(Object obj) {
        if (newObjects.remove(obj)) {
            return;
        }
        dirtyObjects.remove(obj);
        if (!removedObjects.contains(obj)) {
            removedObjects.add(obj);
        }
    }
    
    public void commit() {
        // Insert new objects
        for (Object obj : newObjects) {
            // Insert logic
        }
        
        // Update dirty objects
        for (Object obj : dirtyObjects) {
            // Update logic
        }
        
        // Delete removed objects
        for (Object obj : removedObjects) {
            // Delete logic
        }
        
        clear();
    }
    
    private void clear() {
        newObjects.clear();
        dirtyObjects.clear();
        removedObjects.clear();
    }
}
```

## 6.8 Specification Pattern

The Specification pattern encapsulates business rules that can be combined to build complex queries.

### When to Use:
- When you have complex business rules
- When you want to make business rules reusable
- When you need to combine multiple criteria

### Implementation:
```java
// Specification interface
public interface Specification<T> {
    boolean isSatisfiedBy(T candidate);
    Specification<T> and(Specification<T> other);
    Specification<T> or(Specification<T> other);
    Specification<T> not();
}

// Concrete specifications
public class UserNameSpecification implements Specification<User> {
    private String name;
    
    public UserNameSpecification(String name) {
        this.name = name;
    }
    
    public boolean isSatisfiedBy(User user) {
        return user.getName().contains(name);
    }
    
    public Specification<User> and(Specification<User> other) {
        return new AndSpecification<>(this, other);
    }
    
    public Specification<User> or(Specification<User> other) {
        return new OrSpecification<>(this, other);
    }
    
    public Specification<User> not() {
        return new NotSpecification<>(this);
    }
}

public class UserEmailSpecification implements Specification<User> {
    private String email;
    
    public UserEmailSpecification(String email) {
        this.email = email;
    }
    
    public boolean isSatisfiedBy(User user) {
        return user.getEmail().contains(email);
    }
    
    public Specification<User> and(Specification<User> other) {
        return new AndSpecification<>(this, other);
    }
    
    public Specification<User> or(Specification<User> other) {
        return new OrSpecification<>(this, other);
    }
    
    public Specification<User> not() {
        return new NotSpecification<>(this);
    }
}

// Composite specifications
public class AndSpecification<T> implements Specification<T> {
    private Specification<T> left;
    private Specification<T> right;
    
    public AndSpecification(Specification<T> left, Specification<T> right) {
        this.left = left;
        this.right = right;
    }
    
    public boolean isSatisfiedBy(T candidate) {
        return left.isSatisfiedBy(candidate) && right.isSatisfiedBy(candidate);
    }
    
    public Specification<T> and(Specification<T> other) {
        return new AndSpecification<>(this, other);
    }
    
    public Specification<T> or(Specification<T> other) {
        return new OrSpecification<>(this, other);
    }
    
    public Specification<T> not() {
        return new NotSpecification<>(this);
    }
}
```

## 6.9 Domain Model Pattern

The Domain Model pattern represents the business logic and data of the application in a way that closely mirrors the real-world domain.

### When to Use:
- When you have complex business logic
- When you want to model the real-world domain
- When you need to maintain business rules

### Implementation:
```java
// Domain model
public class Order {
    private Long id;
    private Customer customer;
    private List<OrderItem> items;
    private OrderStatus status;
    private Money totalAmount;
    
    public Order(Customer customer) {
        this.customer = customer;
        this.items = new ArrayList<>();
        this.status = OrderStatus.PENDING;
        this.totalAmount = Money.zero();
    }
    
    public void addItem(Product product, int quantity) {
        if (quantity <= 0) {
            throw new IllegalArgumentException("Quantity must be positive");
        }
        
        OrderItem item = new OrderItem(product, quantity);
        items.add(item);
        recalculateTotal();
    }
    
    public void removeItem(Product product) {
        items.removeIf(item -> item.getProduct().equals(product));
        recalculateTotal();
    }
    
    public void confirm() {
        if (status != OrderStatus.PENDING) {
            throw new IllegalStateException("Only pending orders can be confirmed");
        }
        
        if (items.isEmpty()) {
            throw new IllegalStateException("Cannot confirm empty order");
        }
        
        status = OrderStatus.CONFIRMED;
    }
    
    public void cancel() {
        if (status == OrderStatus.SHIPPED) {
            throw new IllegalStateException("Cannot cancel shipped order");
        }
        
        status = OrderStatus.CANCELLED;
    }
    
    private void recalculateTotal() {
        totalAmount = items.stream()
                .map(OrderItem::getSubtotal)
                .reduce(Money.zero(), Money::add);
    }
    
    // Getters
    public Long getId() { return id; }
    public Customer getCustomer() { return customer; }
    public List<OrderItem> getItems() { return items; }
    public OrderStatus getStatus() { return status; }
    public Money getTotalAmount() { return totalAmount; }
}
```

## 6.10 Table Module Pattern

The Table Module pattern organizes domain logic with one class per table in the database.

### When to Use:
- When you have simple domain logic
- When you want to organize logic by database tables
- When you need to work with record sets

### Implementation:
```java
public class UserTableModule {
    private List<User> users;
    
    public UserTableModule() {
        this.users = new ArrayList<>();
    }
    
    public void addUser(User user) {
        users.add(user);
    }
    
    public User findUserById(Long id) {
        return users.stream()
                .filter(user -> user.getId().equals(id))
                .findFirst()
                .orElse(null);
    }
    
    public List<User> findUsersByName(String name) {
        return users.stream()
                .filter(user -> user.getName().contains(name))
                .collect(Collectors.toList());
    }
    
    public void updateUser(User user) {
        for (int i = 0; i < users.size(); i++) {
            if (users.get(i).getId().equals(user.getId())) {
                users.set(i, user);
                break;
            }
        }
    }
    
    public void deleteUser(Long id) {
        users.removeIf(user -> user.getId().equals(id));
    }
    
    public List<User> getAllUsers() {
        return new ArrayList<>(users);
    }
}
```

This section covers the essential enterprise patterns that help structure large-scale applications with proper separation of concerns, data access, and business logic organization.