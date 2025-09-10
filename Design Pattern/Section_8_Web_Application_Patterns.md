# Section 8 - Web Application Patterns

## 8.1 Front Controller Pattern

The Front Controller pattern provides a centralized entry point for handling web requests, ensuring consistent request processing and reducing code duplication.

### When to Use:
- When you need centralized request handling
- When you want to implement cross-cutting concerns (authentication, logging)
- When you need consistent error handling across the application

### Real-World Analogy:
Think of a hotel's front desk - all guests go through the same entry point where they're greeted, their requests are processed, and they're directed to the appropriate department.

### Basic Implementation:
```java
// Front controller interface
public interface FrontController {
    void handleRequest(HttpServletRequest request, HttpServletResponse response);
}

// Simple front controller
public class SimpleFrontController implements FrontController {
    private Map<String, Controller> controllers = new HashMap<>();
    private List<Filter> filters = new ArrayList<>();
    
    public void handleRequest(HttpServletRequest request, HttpServletResponse response) {
        try {
            // Apply pre-processing filters
            for (Filter filter : filters) {
                if (!filter.doFilter(request, response)) {
                    return; // Filter stopped processing
                }
            }
            
            // Route to appropriate controller
            String path = request.getRequestURI();
            Controller controller = controllers.get(path);
            
            if (controller != null) {
                controller.handle(request, response);
            } else {
                response.setStatus(HttpServletResponse.SC_NOT_FOUND);
            }
            
        } catch (Exception e) {
            handleError(request, response, e);
        }
    }
    
    public void addController(String path, Controller controller) {
        controllers.put(path, controller);
    }
    
    public void addFilter(Filter filter) {
        filters.add(filter);
    }
    
    private void handleError(HttpServletRequest request, HttpServletResponse response, Exception e) {
        response.setStatus(HttpServletResponse.SC_INTERNAL_SERVER_ERROR);
        // Log error and send error response
    }
}

// Controller interface
public interface Controller {
    void handle(HttpServletRequest request, HttpServletResponse response) throws Exception;
}

// Example controller
public class UserController implements Controller {
    public void handle(HttpServletRequest request, HttpServletResponse response) throws Exception {
        String method = request.getMethod();
        
        switch (method) {
            case "GET":
                handleGet(request, response);
                break;
            case "POST":
                handlePost(request, response);
                break;
            default:
                response.setStatus(HttpServletResponse.SC_METHOD_NOT_ALLOWED);
        }
    }
    
    private void handleGet(HttpServletRequest request, HttpServletResponse response) throws Exception {
        // Handle GET request
        String userId = request.getParameter("id");
        // Process and send response
    }
    
    private void handlePost(HttpServletRequest request, HttpServletResponse response) throws Exception {
        // Handle POST request
        // Process form data and send response
    }
}
```

## 8.2 Page Controller Pattern

The Page Controller pattern assigns each page or action to a specific controller, providing a more granular approach to request handling.

### When to Use:
- When you need fine-grained control over individual pages
- When different pages have different processing requirements
- When you want to maintain separation of concerns

### Real-World Analogy:
Think of a restaurant where each dish has its own specialized chef. The pasta chef handles all pasta orders, the grill chef handles all grilled items, and the dessert chef handles all desserts.

### Basic Implementation:
```java
// Page controller interface
public interface PageController {
    void process(HttpServletRequest request, HttpServletResponse response);
    String getViewName();
}

// User list page controller
public class UserListController implements PageController {
    private UserService userService;
    
    public UserListController(UserService userService) {
        this.userService = userService;
    }
    
    public void process(HttpServletRequest request, HttpServletResponse response) {
        try {
            List<User> users = userService.getAllUsers();
            request.setAttribute("users", users);
            request.setAttribute("pageTitle", "User List");
        } catch (Exception e) {
            request.setAttribute("error", "Failed to load users");
        }
    }
    
    public String getViewName() {
        return "userList";
    }
}

// User detail page controller
public class UserDetailController implements PageController {
    private UserService userService;
    
    public UserDetailController(UserService userService) {
        this.userService = userService;
    }
    
    public void process(HttpServletRequest request, HttpServletResponse response) {
        try {
            String userId = request.getParameter("id");
            User user = userService.getUserById(userId);
            request.setAttribute("user", user);
            request.setAttribute("pageTitle", "User Details");
        } catch (Exception e) {
            request.setAttribute("error", "User not found");
        }
    }
    
    public String getViewName() {
        return "userDetail";
    }
}

// Page controller factory
public class PageControllerFactory {
    private Map<String, PageController> controllers = new HashMap<>();
    
    public PageControllerFactory() {
        UserService userService = new UserService();
        controllers.put("/users", new UserListController(userService));
        controllers.put("/user/detail", new UserDetailController(userService));
    }
    
    public PageController getController(String path) {
        return controllers.get(path);
    }
}
```

## 8.3 Application Controller Pattern

The Application Controller pattern centralizes application flow control, managing navigation and business logic coordination.

### When to Use:
- When you need centralized application flow control
- When you want to manage complex navigation logic
- When you need to coordinate between multiple controllers

### Real-World Analogy:
Think of an air traffic control system that coordinates the flow of aircraft, ensuring they follow the correct routes and don't collide, while managing the overall traffic flow.

### Basic Implementation:
```java
// Application controller interface
public interface ApplicationController {
    String handleRequest(HttpServletRequest request, HttpServletResponse response);
}

// Simple application controller
public class SimpleApplicationController implements ApplicationController {
    private Map<String, Command> commands = new HashMap<>();
    private Map<String, String> views = new HashMap<>();
    
    public String handleRequest(HttpServletRequest request, HttpServletResponse response) {
        String action = request.getParameter("action");
        Command command = commands.get(action);
        
        if (command != null) {
            String result = command.execute(request, response);
            return views.get(result);
        }
        
        return "error";
    }
    
    public void addCommand(String action, Command command) {
        commands.put(action, command);
    }
    
    public void addView(String result, String viewName) {
        views.put(result, viewName);
    }
}

// Command interface
public interface Command {
    String execute(HttpServletRequest request, HttpServletResponse response);
}

// Example command
public class CreateUserCommand implements Command {
    private UserService userService;
    
    public CreateUserCommand(UserService userService) {
        this.userService = userService;
    }
    
    public String execute(HttpServletRequest request, HttpServletResponse response) {
        try {
            String name = request.getParameter("name");
            String email = request.getParameter("email");
            
            User user = new User(name, email);
            userService.createUser(user);
            
            return "success";
        } catch (Exception e) {
            request.setAttribute("error", e.getMessage());
            return "error";
        }
    }
}
```

## 8.4 Intercepting Filter Pattern

The Intercepting Filter pattern provides a way to add cross-cutting concerns to web requests without modifying individual controllers.

### When to Use:
- When you need to add common functionality to multiple requests
- When you want to implement cross-cutting concerns
- When you need to modify request/response processing

### Real-World Analogy:
Think of airport security checkpoints. Every passenger goes through the same security procedures (filters) before boarding their flight, regardless of their destination or airline.

### Basic Implementation:
```java
// Filter interface
public interface Filter {
    boolean doFilter(HttpServletRequest request, HttpServletResponse response);
}

// Authentication filter
public class AuthenticationFilter implements Filter {
    public boolean doFilter(HttpServletRequest request, HttpServletResponse response) {
        String sessionId = request.getSession().getId();
        if (isAuthenticated(sessionId)) {
            return true;
        } else {
            response.sendRedirect("/login");
            return false;
        }
    }
    
    private boolean isAuthenticated(String sessionId) {
        // Check if user is authenticated
        return true; // Simplified
    }
}

// Logging filter
public class LoggingFilter implements Filter {
    public boolean doFilter(HttpServletRequest request, HttpServletResponse response) {
        long startTime = System.currentTimeMillis();
        
        // Log request
        System.out.println("Request: " + request.getMethod() + " " + request.getRequestURI());
        
        // Continue processing
        boolean result = true;
        
        // Log response time
        long endTime = System.currentTimeMillis();
        System.out.println("Response time: " + (endTime - startTime) + "ms");
        
        return result;
    }
}

// Filter chain
public class FilterChain {
    private List<Filter> filters = new ArrayList<>();
    private int index = 0;
    
    public void addFilter(Filter filter) {
        filters.add(filter);
    }
    
    public boolean doFilter(HttpServletRequest request, HttpServletResponse response) {
        if (index < filters.size()) {
            Filter filter = filters.get(index++);
            return filter.doFilter(request, response) && doFilter(request, response);
        }
        return true;
    }
}
```

## 8.5 Context Object Pattern

The Context Object pattern encapsulates request-specific information in a single object, making it easier to pass data between different layers.

### When to Use:
- When you need to pass multiple related parameters
- When you want to reduce method parameter lists
- When you need to maintain request state

### Real-World Analogy:
Think of a patient's medical chart that contains all relevant information about their condition, history, and treatment - doctors can access this single source of truth instead of asking for individual pieces of information.

### Basic Implementation:
```java
// Context object interface
public interface RequestContext {
    String getParameter(String name);
    void setAttribute(String name, Object value);
    Object getAttribute(String name);
    String getSessionId();
    String getUserId();
}

// Simple request context
public class SimpleRequestContext implements RequestContext {
    private Map<String, String> parameters = new HashMap<>();
    private Map<String, Object> attributes = new HashMap<>();
    private String sessionId;
    private String userId;
    
    public SimpleRequestContext(HttpServletRequest request) {
        // Extract parameters
        request.getParameterMap().forEach((key, values) -> {
            if (values.length > 0) {
                parameters.put(key, values[0]);
            }
        });
        
        // Extract session information
        this.sessionId = request.getSession().getId();
        this.userId = (String) request.getSession().getAttribute("userId");
    }
    
    public String getParameter(String name) {
        return parameters.get(name);
    }
    
    public void setAttribute(String name, Object value) {
        attributes.put(name, value);
    }
    
    public Object getAttribute(String name) {
        return attributes.get(name);
    }
    
    public String getSessionId() { return sessionId; }
    public String getUserId() { return userId; }
}

// Usage in controller
public class UserController {
    public void handleRequest(RequestContext context) {
        String action = context.getParameter("action");
        
        switch (action) {
            case "create":
                createUser(context);
                break;
            case "update":
                updateUser(context);
                break;
            default:
                listUsers(context);
        }
    }
    
    private void createUser(RequestContext context) {
        String name = context.getParameter("name");
        String email = context.getParameter("email");
        
        User user = new User(name, email);
        // Process user creation
        context.setAttribute("user", user);
        context.setAttribute("message", "User created successfully");
    }
}
```

## 8.6 Frontend Controller Pattern

The Frontend Controller pattern provides a single entry point for frontend applications, handling routing and state management.

### When to Use:
- When building single-page applications
- When you need centralized frontend routing
- When you want to manage application state

### Real-World Analogy:
Think of a smart home hub that controls all your devices. You interact with one central interface that routes your commands to the appropriate devices and manages the overall state of your home.

### Basic Implementation:
```javascript
// Frontend controller
class FrontendController {
    constructor() {
        this.routes = new Map();
        this.state = {};
        this.init();
    }
    
    init() {
        // Set up event listeners
        window.addEventListener('popstate', () => this.handleRoute());
        document.addEventListener('click', (e) => this.handleClick(e));
        
        // Initial route
        this.handleRoute();
    }
    
    addRoute(path, handler) {
        this.routes.set(path, handler);
    }
    
    navigate(path) {
        history.pushState({}, '', path);
        this.handleRoute();
    }
    
    handleRoute() {
        const path = window.location.pathname;
        const handler = this.routes.get(path);
        
        if (handler) {
            handler(this.state);
        } else {
            this.show404();
        }
    }
    
    handleClick(e) {
        if (e.target.matches('[data-route]')) {
            e.preventDefault();
            const route = e.target.getAttribute('data-route');
            this.navigate(route);
        }
    }
    
    setState(newState) {
        this.state = { ...this.state, ...newState };
        this.notifyStateChange();
    }
    
    notifyStateChange() {
        // Notify components of state change
        document.dispatchEvent(new CustomEvent('stateChange', { detail: this.state }));
    }
}

// Usage
const controller = new FrontendController();

controller.addRoute('/', (state) => {
    document.getElementById('content').innerHTML = '<h1>Home</h1>';
});

controller.addRoute('/users', (state) => {
    document.getElementById('content').innerHTML = '<h1>Users</h1>';
});
```

## 8.7 Model-View-Controller (MVC) Web

The MVC pattern separates web applications into three interconnected components: Model (data), View (presentation), and Controller (logic).

### When to Use:
- When you need clear separation of concerns
- When you want to make applications more maintainable
- When you need to support multiple views of the same data

### Real-World Analogy:
Think of a restaurant: the Model is the kitchen (data and business logic), the View is the dining room (presentation), and the Controller is the waiter (coordinates between kitchen and dining room).

### Basic Implementation:
```java
// Model - represents data and business logic
public class User {
    private String id;
    private String name;
    private String email;
    
    // Constructors, getters, setters
    public User(String id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    // Getters and setters
    public String getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}

// Model - data access
public class UserRepository {
    private List<User> users = new ArrayList<>();
    
    public void save(User user) {
        users.add(user);
    }
    
    public User findById(String id) {
        return users.stream()
            .filter(user -> user.getId().equals(id))
            .findFirst()
            .orElse(null);
    }
    
    public List<User> findAll() {
        return new ArrayList<>(users);
    }
}

// Controller - handles requests and coordinates
public class UserController {
    private UserRepository userRepository;
    
    public UserController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
    
    public String listUsers(HttpServletRequest request) {
        List<User> users = userRepository.findAll();
        request.setAttribute("users", users);
        return "userList";
    }
    
    public String createUser(HttpServletRequest request) {
        String name = request.getParameter("name");
        String email = request.getParameter("email");
        
        User user = new User(UUID.randomUUID().toString(), name, email);
        userRepository.save(user);
        
        return "redirect:/users";
    }
}

// View - JSP template
// userList.jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>User List</title>
</head>
<body>
    <h1>Users</h1>
    <table>
        <tr>
            <th>Name</th>
            <th>Email</th>
        </tr>
        <c:forEach var="user" items="${users}">
            <tr>
                <td>${user.name}</td>
                <td>${user.email}</td>
            </tr>
        </c:forEach>
    </table>
</body>
</html>
```

## 8.8 RESTful API Patterns

RESTful API patterns provide a standardized way to design web APIs using HTTP methods and resource-based URLs.

### When to Use:
- When building web APIs
- When you need stateless communication
- When you want to follow REST principles

### Real-World Analogy:
Think of a library catalog system where you can search for books (GET), add new books (POST), update book information (PUT), and remove books (DELETE) using standardized procedures.

### Basic Implementation:
```java
// RESTful controller
@RestController
@RequestMapping("/api/users")
public class UserRestController {
    private UserService userService;
    
    public UserRestController(UserService userService) {
        this.userService = userService;
    }
    
    // GET /api/users - List all users
    @GetMapping
    public ResponseEntity<List<User>> getAllUsers() {
        List<User> users = userService.getAllUsers();
        return ResponseEntity.ok(users);
    }
    
    // GET /api/users/{id} - Get user by ID
    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable String id) {
        User user = userService.getUserById(id);
        if (user != null) {
            return ResponseEntity.ok(user);
        } else {
            return ResponseEntity.notFound().build();
        }
    }
    
    // POST /api/users - Create new user
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        User createdUser = userService.createUser(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdUser);
    }
    
    // PUT /api/users/{id} - Update user
    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(@PathVariable String id, @RequestBody User user) {
        User updatedUser = userService.updateUser(id, user);
        if (updatedUser != null) {
            return ResponseEntity.ok(updatedUser);
        } else {
            return ResponseEntity.notFound().build();
        }
    }
    
    // DELETE /api/users/{id} - Delete user
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable String id) {
        boolean deleted = userService.deleteUser(id);
        if (deleted) {
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}
```

## 8.9 Microservices Patterns

Microservices patterns help break down monolithic applications into smaller, independent services.

### When to Use:
- When you need to scale different parts of your system independently
- When you want to use different technologies for different services
- When you need to improve fault isolation

### Real-World Analogy:
Think of a shopping mall where each store is independent but they all work together to provide a complete shopping experience. Each store can have its own hours, staff, and inventory management.

### Basic Implementation:
```java
// User service
@RestController
@RequestMapping("/users")
public class UserService {
    private UserRepository userRepository;
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable String id) {
        User user = userRepository.findById(id);
        return ResponseEntity.ok(user);
    }
}

// Order service
@RestController
@RequestMapping("/orders")
public class OrderService {
    private OrderRepository orderRepository;
    private UserServiceClient userServiceClient;
    
    @PostMapping
    public ResponseEntity<Order> createOrder(@RequestBody OrderRequest request) {
        // Validate user exists
        User user = userServiceClient.getUser(request.getUserId());
        if (user == null) {
            return ResponseEntity.badRequest().build();
        }
        
        Order order = new Order(request);
        order = orderRepository.save(order);
        return ResponseEntity.ok(order);
    }
}

// Service client
@Component
public class UserServiceClient {
    private RestTemplate restTemplate;
    private String userServiceUrl;
    
    public User getUser(String userId) {
        try {
            ResponseEntity<User> response = restTemplate.getForEntity(
                userServiceUrl + "/users/" + userId, User.class);
            return response.getBody();
        } catch (Exception e) {
            return null;
        }
    }
}
```

## 8.10 Single Page Application (SPA) Patterns

SPA patterns provide a way to build web applications that load a single HTML page and dynamically update content.

### When to Use:
- When you want to provide a desktop-like experience
- When you need to reduce server round trips
- When you want to improve user experience

### Real-World Analogy:
Think of a smart TV interface where you can navigate between different apps and content without changing the channel or reloading the screen.

### Basic Implementation:
```javascript
// SPA router
class SPARouter {
    constructor() {
        this.routes = new Map();
        this.currentRoute = null;
        this.init();
    }
    
    init() {
        window.addEventListener('popstate', () => this.handleRoute());
        document.addEventListener('click', (e) => this.handleClick(e));
        this.handleRoute();
    }
    
    addRoute(path, component) {
        this.routes.set(path, component);
    }
    
    navigate(path) {
        history.pushState({}, '', path);
        this.handleRoute();
    }
    
    handleRoute() {
        const path = window.location.pathname;
        const component = this.routes.get(path);
        
        if (component) {
            this.render(component);
        } else {
            this.render(this.routes.get('/404'));
        }
    }
    
    handleClick(e) {
        if (e.target.matches('[data-route]')) {
            e.preventDefault();
            const route = e.target.getAttribute('data-route');
            this.navigate(route);
        }
    }
    
    render(component) {
        const container = document.getElementById('app');
        container.innerHTML = component.render();
        component.afterRender();
    }
}

// Component base class
class Component {
    constructor(props = {}) {
        this.props = props;
        this.state = {};
    }
    
    setState(newState) {
        this.state = { ...this.state, ...newState };
        this.render();
    }
    
    render() {
        throw new Error('render() must be implemented');
    }
    
    afterRender() {
        // Override in subclasses
    }
}

// Example component
class UserListComponent extends Component {
    constructor(props) {
        super(props);
        this.state = { users: [] };
    }
    
    async afterRender() {
        try {
            const response = await fetch('/api/users');
            const users = await response.json();
            this.setState({ users });
        } catch (error) {
            console.error('Error loading users:', error);
        }
    }
    
    render() {
        return `
            <div>
                <h1>Users</h1>
                <ul>
                    ${this.state.users.map(user => `
                        <li>${user.name} - ${user.email}</li>
                    `).join('')}
                </ul>
            </div>
        `;
    }
}

// Usage
const router = new SPARouter();
router.addRoute('/', new UserListComponent());
router.addRoute('/404', new Component({ render: () => '<h1>Page Not Found</h1>' }));
```

This comprehensive coverage of web application patterns provides the foundation for building robust, scalable web applications. Each pattern addresses specific web development challenges and offers different trade-offs in terms of complexity, maintainability, and performance.