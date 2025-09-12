# Section 17 – Technology Stack & Frameworks

## 17.1 Spring Boot for Microservices

Spring Boot is a popular framework for building microservices in Java.

### Spring Boot Configuration:

```java
// Spring Boot Application
@SpringBootApplication
@EnableDiscoveryClient
@EnableCircuitBreaker
public class UserServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(UserServiceApplication.class, args);
    }
}

// Configuration
@Configuration
public class UserServiceConfig {
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
    
    @Bean
    public UserServiceClient userServiceClient() {
        return new UserServiceClient(restTemplate());
    }
}
```

### Spring Boot Service:

```java
// Spring Boot Service
@Service
@Transactional
public class UserService {
    @Autowired
    private UserRepository userRepository;
    @Autowired
    private EventPublisher eventPublisher;
    
    public User createUser(UserRequest request) {
        User user = new User(request);
        User savedUser = userRepository.save(user);
        
        eventPublisher.publishUserCreated(savedUser);
        
        return savedUser;
    }
    
    public User getUser(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found: " + id));
    }
}
```

## 17.2 Spring Cloud Ecosystem

Spring Cloud provides tools for building microservices.

### Service Discovery:

```java
// Eureka Client
@SpringBootApplication
@EnableEurekaClient
public class UserServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(UserServiceApplication.class, args);
    }
}

// Service Discovery
@Service
public class ServiceDiscoveryService {
    @Autowired
    private DiscoveryClient discoveryClient;
    
    public List<ServiceInstance> getServiceInstances(String serviceName) {
        return discoveryClient.getInstances(serviceName);
    }
    
    public String getServiceUrl(String serviceName) {
        List<ServiceInstance> instances = getServiceInstances(serviceName);
        if (instances.isEmpty()) {
            throw new ServiceNotFoundException("Service not found: " + serviceName);
        }
        
        ServiceInstance instance = instances.get(0);
        return "http://" + instance.getHost() + ":" + instance.getPort();
    }
}
```

### Circuit Breaker:

```java
// Circuit Breaker
@Service
public class UserServiceClient {
    @Autowired
    private RestTemplate restTemplate;
    
    @HystrixCommand(fallbackMethod = "getUserFallback")
    public User getUser(Long id) {
        String url = "http://user-service/api/users/" + id;
        return restTemplate.getForObject(url, User.class);
    }
    
    public User getUserFallback(Long id) {
        return User.builder()
            .id(id)
            .name("Unknown User")
            .email("unknown@example.com")
            .build();
    }
}
```

### API Gateway:

```java
// API Gateway
@SpringBootApplication
@EnableZuulProxy
public class ApiGatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(ApiGatewayApplication.class, args);
    }
}

// Gateway Configuration
@Configuration
public class GatewayConfig {
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("user-service", r -> r.path("/api/users/**")
                .uri("lb://user-service"))
            .route("order-service", r -> r.path("/api/orders/**")
                .uri("lb://order-service"))
            .build();
    }
}
```

## 17.3 .NET Core Microservices

.NET Core provides a cross-platform framework for building microservices.

### .NET Core Service:

```csharp
// .NET Core Service
[ApiController]
[Route("api/[controller]")]
public class UserController : ControllerBase
{
    private readonly IUserService _userService;
    
    public UserController(IUserService userService)
    {
        _userService = userService;
    }
    
    [HttpGet("{id}")]
    public async Task<ActionResult<User>> GetUser(int id)
    {
        var user = await _userService.GetUserAsync(id);
        if (user == null)
        {
            return NotFound();
        }
        return Ok(user);
    }
    
    [HttpPost]
    public async Task<ActionResult<User>> CreateUser([FromBody] UserRequest request)
    {
        var user = await _userService.CreateUserAsync(request);
        return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
    }
}
```

### .NET Core Configuration:

```csharp
// Startup Configuration
public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.AddControllers();
        services.AddDbContext<UserDbContext>(options =>
            options.UseSqlServer(Configuration.GetConnectionString("DefaultConnection")));
        services.AddScoped<IUserService, UserService>();
        services.AddScoped<IUserRepository, UserRepository>();
    }
    
    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        if (env.IsDevelopment())
        {
            app.UseDeveloperExceptionPage();
        }
        
        app.UseRouting();
        app.UseEndpoints(endpoints =>
        {
            endpoints.MapControllers();
        });
    }
}
```

## 17.4 Node.js Microservices

Node.js provides a lightweight runtime for building microservices.

### Node.js Service:

```javascript
// Node.js Service
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// User Schema
const userSchema = new mongoose.Schema({
    email: { type: String, required: true, unique: true },
    name: { type: String, required: true },
    status: { type: String, enum: ['ACTIVE', 'INACTIVE'], default: 'ACTIVE' }
});

const User = mongoose.model('User', userSchema);

// Routes
app.get('/api/users/:id', async (req, res) => {
    try {
        const user = await User.findById(req.params.id);
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }
        res.json(user);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/users', async (req, res) => {
    try {
        const user = new User(req.body);
        await user.save();
        res.status(201).json(user);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

## 17.5 Go Microservices

Go provides a simple and efficient language for building microservices.

### Go Service:

```go
// Go Service
package main

import (
    "encoding/json"
    "log"
    "net/http"
    "strconv"
    
    "github.com/gorilla/mux"
    "github.com/gorilla/handlers"
)

type User struct {
    ID     int    `json:"id"`
    Email  string `json:"email"`
    Name   string `json:"name"`
    Status string `json:"status"`
}

type UserService struct {
    users []User
}

func (s *UserService) GetUser(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    id, _ := strconv.Atoi(vars["id"])
    
    for _, user := range s.users {
        if user.ID == id {
            json.NewEncoder(w).Encode(user)
            return
        }
    }
    
    http.NotFound(w, r)
}

func (s *UserService) CreateUser(w http.ResponseWriter, r *http.Request) {
    var user User
    json.NewDecoder(r.Body).Decode(&user)
    
    user.ID = len(s.users) + 1
    s.users = append(s.users, user)
    
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}

func main() {
    service := &UserService{}
    
    r := mux.NewRouter()
    r.HandleFunc("/api/users/{id}", service.GetUser).Methods("GET")
    r.HandleFunc("/api/users", service.CreateUser).Methods("POST")
    
    log.Println("Server starting on port 8080")
    log.Fatal(http.ListenAndServe(":8080", handlers.CORS()(r)))
}
```

## 17.6 Python Microservices

Python provides a flexible language for building microservices.

### Python Service:

```python
# Python Service
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default='ACTIVE')

# User Schema
class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    name = fields.Str()
    status = fields.Str()

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Routes
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(email=data['email'], name=data['name'])
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## 17.7 Microservices Frameworks Comparison

Different frameworks have different strengths and weaknesses.

### Framework Comparison:

| Framework | Language | Strengths | Weaknesses |
|-----------|----------|-----------|------------|
| Spring Boot | Java | Mature, extensive ecosystem | Verbose, memory intensive |
| .NET Core | C# | Cross-platform, performance | Windows-centric history |
| Node.js | JavaScript | Fast development, large community | Single-threaded, callback hell |
| Go | Go | Simple, fast, concurrent | Limited ecosystem |
| Python | Python | Easy to learn, extensive libraries | Performance limitations |

### Technology Selection Criteria:

```java
// Technology Selection Service
@Service
public class TechnologySelectionService {
    
    public TechnologyRecommendation selectTechnology(ProjectRequirements requirements) {
        TechnologyRecommendation recommendation = new TechnologyRecommendation();
        
        // Evaluate based on requirements
        if (requirements.isHighPerformance()) {
            recommendation.addTechnology("Go", 0.9);
            recommendation.addTechnology(".NET Core", 0.8);
        }
        
        if (requirements.isRapidDevelopment()) {
            recommendation.addTechnology("Node.js", 0.9);
            recommendation.addTechnology("Python", 0.8);
        }
        
        if (requirements.isEnterprise()) {
            recommendation.addTechnology("Spring Boot", 0.9);
            recommendation.addTechnology(".NET Core", 0.8);
        }
        
        if (requirements.isMicroservices()) {
            recommendation.addTechnology("Spring Boot", 0.9);
            recommendation.addTechnology("Go", 0.8);
        }
        
        return recommendation;
    }
}
```

## 17.8 Technology Selection Criteria

Technology selection should be based on specific project requirements.

### Selection Criteria:

#### 1. **Performance Requirements**
- Go: High performance, low latency
- .NET Core: Good performance, cross-platform
- Spring Boot: Good performance, enterprise features
- Node.js: Good for I/O intensive applications
- Python: Lower performance, but easy to develop

#### 2. **Development Speed**
- Node.js: Fast development, large ecosystem
- Python: Easy to learn, rapid prototyping
- Spring Boot: Mature, but verbose
- Go: Simple syntax, but limited libraries
- .NET Core: Good balance of features and simplicity

#### 3. **Team Expertise**
- Choose technologies the team knows
- Consider learning curve for new technologies
- Evaluate training requirements

#### 4. **Ecosystem and Libraries**
- Spring Boot: Extensive ecosystem
- Node.js: Large npm ecosystem
- Python: Extensive scientific libraries
- Go: Growing ecosystem
- .NET Core: Microsoft ecosystem

#### 5. **Scalability and Maintenance**
- Go: Excellent for microservices
- Spring Boot: Enterprise-grade scalability
- .NET Core: Good scalability
- Node.js: Good for I/O intensive applications
- Python: Limited scalability

This comprehensive guide covers all aspects of technology stack and frameworks for microservices, providing both theoretical understanding and practical implementation examples.