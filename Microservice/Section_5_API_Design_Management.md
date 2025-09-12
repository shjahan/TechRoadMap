# Section 5 – API Design & Management

## 5.1 RESTful API Design for Microservices

RESTful API design is crucial for microservices as it provides a standard way for services to communicate. REST (Representational State Transfer) is an architectural style that uses HTTP methods and status codes to create, read, update, and delete resources.

### REST Principles:

#### 1. **Resource-Based URLs**
URLs should represent resources, not actions.

```java
// Good: Resource-based URLs
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        // Get user by ID
    }
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody UserRequest request) {
        // Create new user
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(@PathVariable Long id, @RequestBody UserRequest request) {
        // Update user
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        // Delete user
    }
}

// Bad: Action-based URLs
@RestController
public class UserController {
    @PostMapping("/api/getUser")
    public ResponseEntity<User> getUser(@RequestBody GetUserRequest request) {
        // Bad: Action in URL
    }
    
    @PostMapping("/api/createUser")
    public ResponseEntity<User> createUser(@RequestBody UserRequest request) {
        // Bad: Action in URL
    }
}
```

#### 2. **HTTP Methods**
Use appropriate HTTP methods for different operations.

```java
// HTTP Methods for CRUD operations
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    // GET - Read operations
    @GetMapping
    public ResponseEntity<List<Order>> getAllOrders() {
        return ResponseEntity.ok(orderService.getAllOrders());
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Order> getOrder(@PathVariable Long id) {
        return ResponseEntity.ok(orderService.getOrderById(id));
    }
    
    // POST - Create operations
    @PostMapping
    public ResponseEntity<Order> createOrder(@RequestBody OrderRequest request) {
        Order order = orderService.createOrder(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(order);
    }
    
    // PUT - Update operations (full update)
    @PutMapping("/{id}")
    public ResponseEntity<Order> updateOrder(@PathVariable Long id, @RequestBody OrderRequest request) {
        Order order = orderService.updateOrder(id, request);
        return ResponseEntity.ok(order);
    }
    
    // PATCH - Partial update operations
    @PatchMapping("/{id}/status")
    public ResponseEntity<Order> updateOrderStatus(@PathVariable Long id, @RequestBody StatusUpdateRequest request) {
        Order order = orderService.updateOrderStatus(id, request.getStatus());
        return ResponseEntity.ok(order);
    }
    
    // DELETE - Delete operations
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteOrder(@PathVariable Long id) {
        orderService.deleteOrder(id);
        return ResponseEntity.noContent().build();
    }
}
```

#### 3. **HTTP Status Codes**
Use appropriate HTTP status codes to indicate the result of operations.

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        try {
            User user = userService.findById(id);
            return ResponseEntity.ok(user);
        } catch (UserNotFoundException e) {
            return ResponseEntity.notFound().build();
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody UserRequest request) {
        try {
            User user = userService.createUser(request);
            return ResponseEntity.status(HttpStatus.CREATED).body(user);
        } catch (ValidationException e) {
            return ResponseEntity.badRequest().build();
        } catch (DuplicateUserException e) {
            return ResponseEntity.status(HttpStatus.CONFLICT).build();
        }
    }
}
```

### API Versioning Strategies:

#### 1. **URL Path Versioning**

```java
// Version 1 API
@RestController
@RequestMapping("/api/v1/users")
public class UserControllerV1 {
    @GetMapping("/{id}")
    public ResponseEntity<UserV1> getUser(@PathVariable Long id) {
        // V1 implementation
    }
}

// Version 2 API
@RestController
@RequestMapping("/api/v2/users")
public class UserControllerV2 {
    @GetMapping("/{id}")
    public ResponseEntity<UserV2> getUser(@PathVariable Long id) {
        // V2 implementation
    }
}
```

#### 2. **Header Versioning**

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping(value = "/{id}", headers = "API-Version=1")
    public ResponseEntity<UserV1> getUserV1(@PathVariable Long id) {
        // V1 implementation
    }
    
    @GetMapping(value = "/{id}", headers = "API-Version=2")
    public ResponseEntity<UserV2> getUserV2(@PathVariable Long id) {
        // V2 implementation
    }
}
```

#### 3. **Content Negotiation Versioning**

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping(value = "/{id}", produces = "application/vnd.company.user.v1+json")
    public ResponseEntity<UserV1> getUserV1(@PathVariable Long id) {
        // V1 implementation
    }
    
    @GetMapping(value = "/{id}", produces = "application/vnd.company.user.v2+json")
    public ResponseEntity<UserV2> getUserV2(@PathVariable Long id) {
        // V2 implementation
    }
}
```

## 5.2 GraphQL in Microservices

GraphQL provides a single endpoint for querying multiple microservices, allowing clients to request exactly the data they need.

### GraphQL Schema Definition:

```graphql
# GraphQL Schema
type User {
    id: ID!
    email: String!
    name: String!
    orders: [Order!]!
}

type Order {
    id: ID!
    userId: ID!
    totalAmount: Float!
    status: OrderStatus!
    items: [OrderItem!]!
}

type OrderItem {
    id: ID!
    productId: ID!
    quantity: Int!
    price: Float!
}

enum OrderStatus {
    PENDING
    CONFIRMED
    SHIPPED
    DELIVERED
    CANCELLED
}

type Query {
    user(id: ID!): User
    users: [User!]!
    order(id: ID!): Order
    orders(userId: ID): [Order!]!
}
```

### GraphQL Resolver Implementation:

```java
// GraphQL Resolver
@Component
public class UserResolver implements GraphQLQueryResolver {
    @Autowired
    private UserService userService;
    @Autowired
    private OrderService orderService;
    
    public User user(String id) {
        return userService.findById(Long.parseLong(id));
    }
    
    public List<User> users() {
        return userService.findAll();
    }
    
    public List<Order> orders(User user) {
        return orderService.findByUserId(user.getId());
    }
}

// Order Resolver
@Component
public class OrderResolver implements GraphQLQueryResolver {
    @Autowired
    private OrderService orderService;
    @Autowired
    private ProductService productService;
    
    public Order order(String id) {
        return orderService.findById(Long.parseLong(id));
    }
    
    public List<Order> orders(String userId) {
        if (userId != null) {
            return orderService.findByUserId(Long.parseLong(userId));
        }
        return orderService.findAll();
    }
    
    public List<OrderItem> items(Order order) {
        return order.getItems();
    }
}
```

### GraphQL Configuration:

```java
// GraphQL Configuration
@Configuration
public class GraphQLConfig {
    @Bean
    public GraphQLSchema graphQLSchema() {
        return GraphQLSchema.newSchema()
            .query(GraphQLObjectType.newObject()
                .name("Query")
                .field(GraphQLFieldDefinition.newFieldDefinition()
                    .name("user")
                    .type(UserType.getType())
                    .argument(GraphQLArgument.newArgument()
                        .name("id")
                        .type(Scalars.GraphQLID))
                    .dataFetcher(environment -> {
                        String id = environment.getArgument("id");
                        return userService.findById(Long.parseLong(id));
                    }))
                .build())
            .build();
    }
}
```

## 5.3 gRPC and Protocol Buffers

gRPC is a high-performance RPC framework that uses Protocol Buffers for serialization and HTTP/2 for transport.

### Protocol Buffer Definition:

```protobuf
// user.proto
syntax = "proto3";

package com.example.user;

option java_package = "com.example.user";
option java_outer_classname = "UserProto";

service UserService {
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
    rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
    rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);
    rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);
}

message GetUserRequest {
    int64 id = 1;
}

message GetUserResponse {
    int64 id = 1;
    string email = 2;
    string name = 3;
    UserStatus status = 4;
}

message CreateUserRequest {
    string email = 1;
    string name = 2;
    string password = 3;
}

message CreateUserResponse {
    int64 id = 1;
    string email = 2;
    string name = 3;
    UserStatus status = 4;
}

message UpdateUserRequest {
    int64 id = 1;
    string email = 2;
    string name = 3;
}

message UpdateUserResponse {
    int64 id = 1;
    string email = 2;
    string name = 3;
    UserStatus status = 4;
}

message DeleteUserRequest {
    int64 id = 1;
}

message DeleteUserResponse {
    bool success = 1;
}

enum UserStatus {
    ACTIVE = 0;
    INACTIVE = 1;
    SUSPENDED = 2;
}
```

### gRPC Service Implementation:

```java
// gRPC Service Implementation
@Service
public class UserServiceImpl extends UserServiceGrpc.UserServiceImplBase {
    @Autowired
    private UserRepository userRepository;
    
    @Override
    public void getUser(GetUserRequest request, StreamObserver<GetUserResponse> responseObserver) {
        try {
            User user = userRepository.findById(request.getId());
            
            GetUserResponse response = GetUserResponse.newBuilder()
                .setId(user.getId())
                .setEmail(user.getEmail())
                .setName(user.getName())
                .setStatus(translateStatus(user.getStatus()))
                .build();
            
            responseObserver.onNext(response);
            responseObserver.onCompleted();
        } catch (Exception e) {
            responseObserver.onError(Status.NOT_FOUND
                .withDescription("User not found")
                .asRuntimeException());
        }
    }
    
    @Override
    public void createUser(CreateUserRequest request, StreamObserver<CreateUserResponse> responseObserver) {
        try {
            User user = new User();
            user.setEmail(request.getEmail());
            user.setName(request.getName());
            user.setPassword(encodePassword(request.getPassword()));
            user.setStatus(UserStatus.ACTIVE);
            
            User savedUser = userRepository.save(user);
            
            CreateUserResponse response = CreateUserResponse.newBuilder()
                .setId(savedUser.getId())
                .setEmail(savedUser.getEmail())
                .setName(savedUser.getName())
                .setStatus(translateStatus(savedUser.getStatus()))
                .build();
            
            responseObserver.onNext(response);
            responseObserver.onCompleted();
        } catch (Exception e) {
            responseObserver.onError(Status.INTERNAL
                .withDescription("Failed to create user")
                .asRuntimeException());
        }
    }
    
    private UserStatusProto translateStatus(UserStatus status) {
        switch (status) {
            case ACTIVE:
                return UserStatusProto.ACTIVE;
            case INACTIVE:
                return UserStatusProto.INACTIVE;
            case SUSPENDED:
                return UserStatusProto.SUSPENDED;
            default:
                return UserStatusProto.ACTIVE;
        }
    }
}
```

### gRPC Client Implementation:

```java
// gRPC Client
@Component
public class UserServiceGrpcClient {
    private final UserServiceGrpc.UserServiceBlockingStub userServiceStub;
    
    public UserServiceGrpcClient() {
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 9090)
            .usePlaintext()
            .build();
        this.userServiceStub = UserServiceGrpc.newBlockingStub(channel);
    }
    
    public User getUser(Long id) {
        GetUserRequest request = GetUserRequest.newBuilder()
            .setId(id)
            .build();
        
        try {
            GetUserResponse response = userServiceStub.getUser(request);
            return User.builder()
                .id(response.getId())
                .email(response.getEmail())
                .name(response.getName())
                .status(translateStatus(response.getStatus()))
                .build();
        } catch (StatusRuntimeException e) {
            if (e.getStatus().getCode() == Status.Code.NOT_FOUND) {
                throw new UserNotFoundException("User not found: " + id);
            }
            throw new UserServiceException("Failed to get user", e);
        }
    }
    
    public User createUser(UserRequest request) {
        CreateUserRequest grpcRequest = CreateUserRequest.newBuilder()
            .setEmail(request.getEmail())
            .setName(request.getName())
            .setPassword(request.getPassword())
            .build();
        
        try {
            CreateUserResponse response = userServiceStub.createUser(grpcRequest);
            return User.builder()
                .id(response.getId())
                .email(response.getEmail())
                .name(response.getName())
                .status(translateStatus(response.getStatus()))
                .build();
        } catch (StatusRuntimeException e) {
            throw new UserServiceException("Failed to create user", e);
        }
    }
}
```

## 5.4 API Versioning Strategies

API versioning is essential for maintaining backward compatibility while evolving APIs.

### 1. **URL Path Versioning**

```java
// Version 1 API
@RestController
@RequestMapping("/api/v1/users")
public class UserControllerV1 {
    @GetMapping("/{id}")
    public ResponseEntity<UserV1> getUser(@PathVariable Long id) {
        User user = userService.findById(id);
        UserV1 userV1 = convertToV1(user);
        return ResponseEntity.ok(userV1);
    }
}

// Version 2 API
@RestController
@RequestMapping("/api/v2/users")
public class UserControllerV2 {
    @GetMapping("/{id}")
    public ResponseEntity<UserV2> getUser(@PathVariable Long id) {
        User user = userService.findById(id);
        UserV2 userV2 = convertToV2(user);
        return ResponseEntity.ok(userV2);
    }
}
```

### 2. **Header Versioning**

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping(value = "/{id}", headers = "API-Version=1")
    public ResponseEntity<UserV1> getUserV1(@PathVariable Long id) {
        User user = userService.findById(id);
        UserV1 userV1 = convertToV1(user);
        return ResponseEntity.ok(userV1);
    }
    
    @GetMapping(value = "/{id}", headers = "API-Version=2")
    public ResponseEntity<UserV2> getUserV2(@PathVariable Long id) {
        User user = userService.findById(id);
        UserV2 userV2 = convertToV2(user);
        return ResponseEntity.ok(userV2);
    }
}
```

### 3. **Content Negotiation Versioning**

```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping(value = "/{id}", produces = "application/vnd.company.user.v1+json")
    public ResponseEntity<UserV1> getUserV1(@PathVariable Long id) {
        User user = userService.findById(id);
        UserV1 userV1 = convertToV1(user);
        return ResponseEntity.ok(userV1);
    }
    
    @GetMapping(value = "/{id}", produces = "application/vnd.company.user.v2+json")
    public ResponseEntity<UserV2> getUserV2(@PathVariable Long id) {
        User user = userService.findById(id);
        UserV2 userV2 = convertToV2(user);
        return ResponseEntity.ok(userV2);
    }
}
```

## 5.5 API Documentation Standards

API documentation is crucial for microservices to ensure proper integration and usage.

### OpenAPI/Swagger Documentation:

```java
// OpenAPI Configuration
@Configuration
@EnableSwagger2
public class SwaggerConfig {
    @Bean
    public Docket api() {
        return new Docket(DocumentationType.SWAGGER_2)
            .select()
            .apis(RequestHandlerSelectors.basePackage("com.example.controller"))
            .paths(PathSelectors.any())
            .build()
            .apiInfo(apiInfo());
    }
    
    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
            .title("User Service API")
            .description("API for managing users")
            .version("1.0.0")
            .contact(new Contact("API Team", "https://example.com", "api@example.com"))
            .license("MIT License")
            .licenseUrl("https://opensource.org/licenses/MIT")
            .build();
    }
}

// API Documentation Annotations
@RestController
@RequestMapping("/api/users")
@Api(tags = "User Management")
public class UserController {
    @GetMapping("/{id}")
    @ApiOperation(value = "Get user by ID", response = User.class)
    @ApiResponses(value = {
        @ApiResponse(code = 200, message = "User found"),
        @ApiResponse(code = 404, message = "User not found"),
        @ApiResponse(code = 500, message = "Internal server error")
    })
    public ResponseEntity<User> getUser(
            @ApiParam(value = "User ID", required = true) @PathVariable Long id) {
        // Implementation
    }
    
    @PostMapping
    @ApiOperation(value = "Create new user", response = User.class)
    @ApiResponses(value = {
        @ApiResponse(code = 201, message = "User created successfully"),
        @ApiResponse(code = 400, message = "Invalid input"),
        @ApiResponse(code = 409, message = "User already exists")
    })
    public ResponseEntity<User> createUser(
            @ApiParam(value = "User details", required = true) @RequestBody UserRequest request) {
        // Implementation
    }
}
```

## 5.6 API Gateway Configuration

API Gateway provides a single entry point for all client requests to microservices.

### Spring Cloud Gateway Configuration:

```java
// Gateway Configuration
@Configuration
public class GatewayConfig {
    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("user-service", r -> r.path("/api/users/**")
                .filters(f -> f
                    .addRequestHeader("X-User-Service", "true")
                    .addResponseHeader("X-Response-Time", "true")
                    .circuitBreaker(config -> config
                        .setName("user-service-cb")
                        .setFallbackUri("forward:/fallback/user-service")))
                .uri("lb://user-service"))
            .route("order-service", r -> r.path("/api/orders/**")
                .filters(f -> f
                    .addRequestHeader("X-Order-Service", "true")
                    .addResponseHeader("X-Response-Time", "true")
                    .circuitBreaker(config -> config
                        .setName("order-service-cb")
                        .setFallbackUri("forward:/fallback/order-service")))
                .uri("lb://order-service"))
            .build();
    }
}

// Fallback Controller
@RestController
public class FallbackController {
    @GetMapping("/fallback/user-service")
    public ResponseEntity<ErrorResponse> userServiceFallback() {
        ErrorResponse error = ErrorResponse.builder()
            .error("USER_SERVICE_UNAVAILABLE")
            .message("User service is temporarily unavailable")
            .timestamp(Instant.now().toString())
            .build();
        return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(error);
    }
}
```

## 5.7 Rate Limiting and Throttling

Rate limiting controls the number of requests a client can make within a specific time period.

### Redis-based Rate Limiting:

```java
// Rate Limiting Configuration
@Configuration
public class RateLimitConfig {
    @Bean
    public RedisRateLimiter redisRateLimiter() {
        return new RedisRateLimiter(10, 20); // 10 requests per second, burst of 20
    }
}

// Rate Limiting Filter
@Component
public class RateLimitFilter implements GatewayFilter {
    @Autowired
    private RedisRateLimiter redisRateLimiter;
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        String key = getClientId(exchange.getRequest());
        
        return redisRateLimiter.isAllowed(key, 10, 20)
            .flatMap(response -> {
                if (response.isAllowed()) {
                    return chain.filter(exchange);
                } else {
                    exchange.getResponse().setStatusCode(HttpStatus.TOO_MANY_REQUESTS);
                    return exchange.getResponse().setComplete();
                }
            });
    }
    
    private String getClientId(ServerHttpRequest request) {
        String clientId = request.getHeaders().getFirst("X-Client-Id");
        if (clientId == null) {
            clientId = request.getRemoteAddress().getAddress().getHostAddress();
        }
        return clientId;
    }
}
```

### Custom Rate Limiting:

```java
// Custom Rate Limiter
@Component
public class CustomRateLimiter {
    private final Map<String, RateLimitInfo> rateLimits = new ConcurrentHashMap<>();
    
    public boolean isAllowed(String clientId, int maxRequests, Duration window) {
        RateLimitInfo info = rateLimits.computeIfAbsent(clientId, k -> new RateLimitInfo());
        
        Instant now = Instant.now();
        if (info.getWindowStart().isBefore(now.minus(window))) {
            info.reset(now);
        }
        
        if (info.getRequestCount() < maxRequests) {
            info.increment();
            return true;
        }
        
        return false;
    }
    
    private static class RateLimitInfo {
        private int requestCount = 0;
        private Instant windowStart = Instant.now();
        
        public void increment() {
            requestCount++;
        }
        
        public void reset(Instant now) {
            requestCount = 0;
            windowStart = now;
        }
        
        public int getRequestCount() {
            return requestCount;
        }
        
        public Instant getWindowStart() {
            return windowStart;
        }
    }
}
```

## 5.8 API Security and Authentication

API security is crucial for protecting microservices from unauthorized access.

### JWT Authentication:

```java
// JWT Configuration
@Configuration
public class JwtConfig {
    @Value("${jwt.secret}")
    private String secret;
    
    @Value("${jwt.expiration}")
    private int expiration;
    
    @Bean
    public JwtTokenProvider jwtTokenProvider() {
        return new JwtTokenProvider(secret, expiration);
    }
}

// JWT Token Provider
@Component
public class JwtTokenProvider {
    private final String secret;
    private final int expiration;
    
    public JwtTokenProvider(String secret, int expiration) {
        this.secret = secret;
        this.expiration = expiration;
    }
    
    public String generateToken(UserDetails userDetails) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("sub", userDetails.getUsername());
        claims.put("authorities", userDetails.getAuthorities());
        
        return createToken(claims, userDetails.getUsername());
    }
    
    private String createToken(Map<String, Object> claims, String subject) {
        return Jwts.builder()
            .setClaims(claims)
            .setSubject(subject)
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + expiration * 1000))
            .signWith(SignatureAlgorithm.HS512, secret)
            .compact();
    }
    
    public boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(secret).parseClaimsJws(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }
    
    public String getUsernameFromToken(String token) {
        return Jwts.parser()
            .setSigningKey(secret)
            .parseClaimsJws(token)
            .getBody()
            .getSubject();
    }
}
```

### OAuth 2.0 Implementation:

```java
// OAuth 2.0 Configuration
@Configuration
@EnableAuthorizationServer
public class AuthorizationServerConfig extends AuthorizationServerConfigurerAdapter {
    @Autowired
    private AuthenticationManager authenticationManager;
    
    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.inMemory()
            .withClient("client-app")
            .secret("client-secret")
            .authorizedGrantTypes("authorization_code", "refresh_token", "password")
            .scopes("read", "write")
            .redirectUris("http://localhost:3000/callback")
            .accessTokenValiditySeconds(3600)
            .refreshTokenValiditySeconds(7200);
    }
    
    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) throws Exception {
        endpoints.authenticationManager(authenticationManager);
    }
}

// Resource Server Configuration
@Configuration
@EnableResourceServer
public class ResourceServerConfig extends ResourceServerConfigurerAdapter {
    @Override
    public void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
            .antMatchers("/api/public/**").permitAll()
            .antMatchers("/api/users/**").hasRole("USER")
            .antMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated();
    }
}
```

This comprehensive guide covers all aspects of API design and management in microservices, providing both theoretical understanding and practical implementation examples. Each concept is explained with real-world scenarios and Java code examples to make the concepts clear and actionable.