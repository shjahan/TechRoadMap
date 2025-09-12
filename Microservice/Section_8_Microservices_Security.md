# Section 8 – Microservices Security

## 8.1 Security Challenges in Microservices

Microservices introduce unique security challenges due to their distributed nature, multiple entry points, and complex communication patterns.

### Key Security Challenges:

#### 1. **Distributed Attack Surface**
Multiple services create more potential attack vectors.

#### 2. **Service-to-Service Communication**
Securing communication between services is complex.

#### 3. **Data Security**
Data is distributed across multiple services and databases.

#### 4. **Identity and Access Management**
Managing identities across multiple services.

#### 5. **Network Security**
Securing network communication between services.

### Security Threat Model:

```java
// Security Threat Analysis
@Component
public class SecurityThreatAnalyzer {
    
    public SecurityThreats analyzeThreats(ServiceArchitecture architecture) {
        SecurityThreats threats = new SecurityThreats();
        
        // Analyze each service
        for (Service service : architecture.getServices()) {
            threats.addThreats(analyzeServiceThreats(service));
        }
        
        // Analyze communication patterns
        threats.addThreats(analyzeCommunicationThreats(architecture));
        
        // Analyze data flow
        threats.addThreats(analyzeDataFlowThreats(architecture));
        
        return threats;
    }
    
    private List<SecurityThreat> analyzeServiceThreats(Service service) {
        List<SecurityThreat> threats = new ArrayList<>();
        
        // API endpoints threats
        threats.add(new SecurityThreat("API_ENDPOINT_EXPOSURE", 
            "Service exposes API endpoints that could be attacked"));
        
        // Database threats
        threats.add(new SecurityThreat("DATABASE_ACCESS", 
            "Service has direct database access"));
        
        // External dependencies
        threats.add(new SecurityThreat("EXTERNAL_DEPENDENCIES", 
            "Service depends on external services"));
        
        return threats;
    }
}
```

## 8.2 Zero Trust Architecture

Zero Trust Architecture assumes that no entity, whether inside or outside the network, should be trusted by default.

### Zero Trust Principles:

#### 1. **Never Trust, Always Verify**
Every request must be authenticated and authorized.

#### 2. **Least Privilege Access**
Users and services get only the minimum access they need.

#### 3. **Assume Breach**
Design security as if the network is already compromised.

### Implementation:

```java
// Zero Trust Security Service
@Service
public class ZeroTrustSecurityService {
    @Autowired
    private AuthenticationService authenticationService;
    @Autowired
    private AuthorizationService authorizationService;
    @Autowired
    private AuditService auditService;
    
    public SecurityContext authenticateAndAuthorize(HttpServletRequest request) {
        // Step 1: Authenticate
        Authentication authentication = authenticationService.authenticate(request);
        if (authentication == null) {
            throw new AuthenticationException("Authentication failed");
        }
        
        // Step 2: Authorize
        AuthorizationResult authorization = authorizationService.authorize(authentication, request);
        if (!authorization.isAuthorized()) {
            throw new AuthorizationException("Authorization failed");
        }
        
        // Step 3: Audit
        auditService.logAccess(authentication, request, authorization);
        
        return SecurityContext.builder()
            .authentication(authentication)
            .authorization(authorization)
            .timestamp(Instant.now())
            .build();
    }
}

// Zero Trust Filter
@Component
public class ZeroTrustFilter implements Filter {
    @Autowired
    private ZeroTrustSecurityService securityService;
    
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) 
            throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        try {
            // Apply zero trust security
            SecurityContext securityContext = securityService.authenticateAndAuthorize(httpRequest);
            
            // Add security context to request
            httpRequest.setAttribute("securityContext", securityContext);
            
            // Continue with request
            chain.doFilter(request, response);
            
        } catch (AuthenticationException e) {
            httpResponse.setStatus(HttpStatus.UNAUTHORIZED.value());
            httpResponse.getWriter().write("Authentication failed");
        } catch (AuthorizationException e) {
            httpResponse.setStatus(HttpStatus.FORBIDDEN.value());
            httpResponse.getWriter().write("Authorization failed");
        }
    }
}
```

## 8.3 Service-to-Service Authentication

Service-to-service authentication ensures that only authorized services can communicate with each other.

### JWT-based Service Authentication:

```java
// Service Authentication Service
@Service
public class ServiceAuthenticationService {
    @Autowired
    private JwtTokenProvider jwtTokenProvider;
    @Autowired
    private ServiceRegistry serviceRegistry;
    
    public String generateServiceToken(String serviceId, String targetService) {
        ServiceClaims claims = ServiceClaims.builder()
            .serviceId(serviceId)
            .targetService(targetService)
            .issuedAt(Instant.now())
            .expiresAt(Instant.now().plus(Duration.ofHours(1)))
            .build();
        
        return jwtTokenProvider.generateServiceToken(claims);
    }
    
    public boolean validateServiceToken(String token, String expectedService) {
        try {
            ServiceClaims claims = jwtTokenProvider.validateServiceToken(token);
            return expectedService.equals(claims.getTargetService()) && 
                   isServiceAuthorized(claims.getServiceId(), expectedService);
        } catch (Exception e) {
            return false;
        }
    }
    
    private boolean isServiceAuthorized(String serviceId, String targetService) {
        // Check if service is authorized to access target service
        return serviceRegistry.isServiceAuthorized(serviceId, targetService);
    }
}

// Service Token Provider
@Component
public class JwtTokenProvider {
    private final String secret;
    private final int expiration;
    
    public JwtTokenProvider(@Value("${jwt.secret}") String secret, 
                           @Value("${jwt.expiration}") int expiration) {
        this.secret = secret;
        this.expiration = expiration;
    }
    
    public String generateServiceToken(ServiceClaims claims) {
        Map<String, Object> tokenClaims = new HashMap<>();
        tokenClaims.put("serviceId", claims.getServiceId());
        tokenClaims.put("targetService", claims.getTargetService());
        tokenClaims.put("issuedAt", claims.getIssuedAt().toEpochMilli());
        tokenClaims.put("expiresAt", claims.getExpiresAt().toEpochMilli());
        
        return Jwts.builder()
            .setClaims(tokenClaims)
            .setSubject(claims.getServiceId())
            .setIssuedAt(Date.from(claims.getIssuedAt()))
            .setExpiration(Date.from(claims.getExpiresAt()))
            .signWith(SignatureAlgorithm.HS512, secret)
            .compact();
    }
    
    public ServiceClaims validateServiceToken(String token) {
        Claims claims = Jwts.parser()
            .setSigningKey(secret)
            .parseClaimsJws(token)
            .getBody();
        
        return ServiceClaims.builder()
            .serviceId(claims.getSubject())
            .targetService(claims.get("targetService", String.class))
            .issuedAt(Instant.ofEpochMilli(claims.getIssuedAt().getTime()))
            .expiresAt(Instant.ofEpochMilli(claims.getExpiration().getTime()))
            .build();
    }
}
```

### Mutual TLS (mTLS) Authentication:

```java
// mTLS Configuration
@Configuration
public class MTLSConfig {
    @Bean
    public RestTemplate mTLSRestTemplate() throws Exception {
        // Load client certificate
        KeyStore keyStore = KeyStore.getInstance("PKCS12");
        keyStore.load(new FileInputStream("client.p12"), "password".toCharArray());
        
        // Load trust store
        KeyStore trustStore = KeyStore.getInstance("PKCS12");
        trustStore.load(new FileInputStream("truststore.p12"), "password".toCharArray());
        
        // Create SSL context
        SSLContext sslContext = SSLContextBuilder.create()
            .loadKeyMaterial(keyStore, "password".toCharArray())
            .loadTrustMaterial(trustStore, null)
            .build();
        
        // Create HTTP client
        CloseableHttpClient httpClient = HttpClients.custom()
            .setSSLContext(sslContext)
            .build();
        
        // Create REST template
        HttpComponentsClientHttpRequestFactory factory = new HttpComponentsClientHttpRequestFactory(httpClient);
        return new RestTemplate(factory);
    }
}

// mTLS Service Client
@Service
public class MTLSServiceClient {
    @Autowired
    private RestTemplate mTLSRestTemplate;
    
    public User getUser(Long id) {
        String url = "https://user-service/api/users/" + id;
        
        try {
            ResponseEntity<User> response = mTLSRestTemplate.getForEntity(url, User.class);
            return response.getBody();
        } catch (Exception e) {
            throw new ServiceCommunicationException("Failed to get user", e);
        }
    }
}
```

## 8.4 JWT and OAuth 2.0

JWT and OAuth 2.0 provide secure authentication and authorization for microservices.

### JWT Implementation:

```java
// JWT Configuration
@Configuration
public class JWTConfig {
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
        claims.put("userId", getUserId(userDetails));
        
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
    
    public List<GrantedAuthority> getAuthoritiesFromToken(String token) {
        Claims claims = Jwts.parser()
            .setSigningKey(secret)
            .parseClaimsJws(token)
            .getBody();
        
        @SuppressWarnings("unchecked")
        List<String> authorities = claims.get("authorities", List.class);
        
        return authorities.stream()
            .map(SimpleGrantedAuthority::new)
            .collect(Collectors.toList());
    }
}
```

### OAuth 2.0 Implementation:

```java
// OAuth 2.0 Authorization Server
@Configuration
@EnableAuthorizationServer
public class AuthorizationServerConfig extends AuthorizationServerConfigurerAdapter {
    @Autowired
    private AuthenticationManager authenticationManager;
    
    @Override
    public void configure(ClientDetailsServiceConfigurer clients) throws Exception {
        clients.inMemory()
            .withClient("web-app")
            .secret("web-secret")
            .authorizedGrantTypes("authorization_code", "refresh_token")
            .scopes("read", "write")
            .redirectUris("http://localhost:3000/callback")
            .accessTokenValiditySeconds(3600)
            .refreshTokenValiditySeconds(7200)
            .and()
            .withClient("mobile-app")
            .secret("mobile-secret")
            .authorizedGrantTypes("password", "refresh_token")
            .scopes("read", "write")
            .accessTokenValiditySeconds(3600)
            .refreshTokenValiditySeconds(7200);
    }
    
    @Override
    public void configure(AuthorizationServerEndpointsConfigurer endpoints) throws Exception {
        endpoints.authenticationManager(authenticationManager);
    }
}

// OAuth 2.0 Resource Server
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

## 8.5 API Security Best Practices

API security best practices ensure that microservices APIs are protected against common attacks.

### Input Validation:

```java
// Input Validation Service
@Service
public class InputValidationService {
    
    public void validateUserRequest(UserRequest request) {
        if (request == null) {
            throw new ValidationException("Request cannot be null");
        }
        
        if (request.getEmail() == null || !isValidEmail(request.getEmail())) {
            throw new ValidationException("Invalid email format");
        }
        
        if (request.getName() == null || request.getName().trim().isEmpty()) {
            throw new ValidationException("Name is required");
        }
        
        if (request.getPassword() == null || !isValidPassword(request.getPassword())) {
            throw new ValidationException("Password does not meet requirements");
        }
    }
    
    private boolean isValidEmail(String email) {
        return email.matches("^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$");
    }
    
    private boolean isValidPassword(String password) {
        // Password must be at least 8 characters, contain uppercase, lowercase, number, and special character
        return password.length() >= 8 && 
               password.matches(".*[A-Z].*") && 
               password.matches(".*[a-z].*") && 
               password.matches(".*[0-9].*") && 
               password.matches(".*[!@#$%^&*()_+\\-=\\[\\]{};':\"\\\\|,.<>\\/?].*");
    }
}

// Validation Controller
@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private InputValidationService validationService;
    @Autowired
    private UserService userService;
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody @Valid UserRequest request) {
        // Validate input
        validationService.validateUserRequest(request);
        
        // Create user
        User user = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }
}
```

### Rate Limiting:

```java
// Rate Limiting Service
@Service
public class RateLimitingService {
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

// Rate Limiting Filter
@Component
public class RateLimitingFilter implements Filter {
    @Autowired
    private RateLimitingService rateLimitingService;
    
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) 
            throws IOException, ServletException {
        
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        String clientId = getClientId(httpRequest);
        
        if (rateLimitingService.isAllowed(clientId, 100, Duration.ofMinutes(1))) {
            chain.doFilter(request, response);
        } else {
            httpResponse.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
            httpResponse.getWriter().write("Rate limit exceeded");
        }
    }
    
    private String getClientId(HttpServletRequest request) {
        String clientId = request.getHeader("X-Client-Id");
        if (clientId == null) {
            clientId = request.getRemoteAddr();
        }
        return clientId;
    }
}
```

## 8.6 Network Security and Segmentation

Network security and segmentation protect microservices by isolating them in secure network segments.

### Network Segmentation:

```java
// Network Security Configuration
@Configuration
public class NetworkSecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeRequests()
                .antMatchers("/api/public/**").permitAll()
                .antMatchers("/api/internal/**").hasIpAddress("10.0.0.0/8")
                .antMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            .and()
            .csrf().disable()
            .headers()
                .frameOptions().deny()
                .contentTypeOptions().and()
                .httpStrictTransportSecurity(hstsConfig -> hstsConfig
                    .maxAgeInSeconds(31536000)
                    .includeSubdomains(true))
            .and()
            .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS);
        
        return http.build();
    }
}

// Network Security Service
@Service
public class NetworkSecurityService {
    
    public boolean isInternalRequest(HttpServletRequest request) {
        String clientIp = getClientIp(request);
        return isInternalIp(clientIp);
    }
    
    public boolean isAdminRequest(HttpServletRequest request) {
        String clientIp = getClientIp(request);
        return isAdminIp(clientIp);
    }
    
    private String getClientIp(HttpServletRequest request) {
        String xForwardedFor = request.getHeader("X-Forwarded-For");
        if (xForwardedFor != null && !xForwardedFor.isEmpty()) {
            return xForwardedFor.split(",")[0].trim();
        }
        return request.getRemoteAddr();
    }
    
    private boolean isInternalIp(String ip) {
        try {
            InetAddress address = InetAddress.getByName(ip);
            return address.isSiteLocalAddress() || address.isLoopbackAddress();
        } catch (UnknownHostException e) {
            return false;
        }
    }
    
    private boolean isAdminIp(String ip) {
        // Check if IP is in admin network range
        return ip.startsWith("192.168.1.") || ip.startsWith("10.0.1.");
    }
}
```

### Service Mesh Security:

```yaml
# Istio Security Policy
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: microservices
spec:
  mtls:
    mode: STRICT
---
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: user-service-policy
  namespace: microservices
spec:
  selector:
    matchLabels:
      app: user-service
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/microservices/sa/order-service"]
    - source:
        principals: ["cluster.local/ns/microservices/sa/admin-service"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/users/*"]
```

## 8.7 Secrets Management

Secrets management ensures that sensitive information like passwords, API keys, and certificates are stored and accessed securely.

### HashiCorp Vault Integration:

```java
// Vault Configuration
@Configuration
public class VaultConfig {
    @Value("${vault.host}")
    private String vaultHost;
    
    @Value("${vault.token}")
    private String vaultToken;
    
    @Bean
    public VaultTemplate vaultTemplate() {
        VaultEndpoint vaultEndpoint = new VaultEndpoint();
        vaultEndpoint.setHost(vaultHost);
        vaultEndpoint.setPort(8200);
        vaultEndpoint.setScheme("https");
        
        ClientAuthentication clientAuthentication = new TokenAuthentication(vaultToken);
        
        return new VaultTemplate(vaultEndpoint, clientAuthentication);
    }
}

// Secrets Service
@Service
public class SecretsService {
    @Autowired
    private VaultTemplate vaultTemplate;
    
    public String getDatabasePassword(String serviceName) {
        VaultResponseSupport<Map<String, Object>> response = vaultTemplate.read(
            "secret/data/" + serviceName + "/database", Map.class);
        
        if (response != null && response.getData() != null) {
            Map<String, Object> data = response.getData();
            return (String) data.get("password");
        }
        
        throw new SecretNotFoundException("Database password not found for service: " + serviceName);
    }
    
    public String getApiKey(String serviceName, String keyName) {
        VaultResponseSupport<Map<String, Object>> response = vaultTemplate.read(
            "secret/data/" + serviceName + "/api-keys", Map.class);
        
        if (response != null && response.getData() != null) {
            Map<String, Object> data = response.getData();
            return (String) data.get(keyName);
        }
        
        throw new SecretNotFoundException("API key not found: " + keyName);
    }
    
    public void rotateSecret(String serviceName, String secretName, String newValue) {
        Map<String, Object> secretData = new HashMap<>();
        secretData.put(secretName, newValue);
        
        vaultTemplate.write("secret/data/" + serviceName + "/" + secretName, secretData);
    }
}
```

### Kubernetes Secrets:

```java
// Kubernetes Secrets Service
@Service
public class KubernetesSecretsService {
    @Autowired
    private KubernetesClient kubernetesClient;
    
    public String getSecret(String namespace, String secretName, String key) {
        Secret secret = kubernetesClient.secrets()
            .inNamespace(namespace)
            .withName(secretName)
            .get();
        
        if (secret != null && secret.getData() != null) {
            String encodedValue = secret.getData().get(key);
            if (encodedValue != null) {
                return new String(Base64.getDecoder().decode(encodedValue));
            }
        }
        
        throw new SecretNotFoundException("Secret not found: " + secretName + "/" + key);
    }
    
    public void createSecret(String namespace, String secretName, Map<String, String> data) {
        Map<String, String> encodedData = data.entrySet().stream()
            .collect(Collectors.toMap(
                Map.Entry::getKey,
                entry -> Base64.getEncoder().encodeToString(entry.getValue().getBytes())
            ));
        
        Secret secret = new SecretBuilder()
            .withNewMetadata()
                .withName(secretName)
                .withNamespace(namespace)
            .endMetadata()
            .withData(encodedData)
            .build();
        
        kubernetesClient.secrets()
            .inNamespace(namespace)
            .createOrReplace(secret);
    }
}
```

## 8.8 Security Monitoring and Auditing

Security monitoring and auditing help detect and respond to security threats in microservices.

### Security Event Monitoring:

```java
// Security Event Monitor
@Component
public class SecurityEventMonitor {
    @Autowired
    private SecurityEventRepository securityEventRepository;
    @Autowired
    private AlertService alertService;
    
    public void monitorAuthenticationAttempt(String username, boolean success, String ipAddress) {
        SecurityEvent event = SecurityEvent.builder()
            .eventType("AUTHENTICATION_ATTEMPT")
            .username(username)
            .success(success)
            .ipAddress(ipAddress)
            .timestamp(Instant.now())
            .build();
        
        securityEventRepository.save(event);
        
        // Check for suspicious patterns
        if (isSuspiciousActivity(username, ipAddress)) {
            alertService.sendSecurityAlert("Suspicious authentication activity detected", event);
        }
    }
    
    public void monitorAuthorizationAttempt(String username, String resource, boolean success) {
        SecurityEvent event = SecurityEvent.builder()
            .eventType("AUTHORIZATION_ATTEMPT")
            .username(username)
            .resource(resource)
            .success(success)
            .timestamp(Instant.now())
            .build();
        
        securityEventRepository.save(event);
        
        // Check for privilege escalation attempts
        if (!success && isPrivilegeEscalationAttempt(username, resource)) {
            alertService.sendSecurityAlert("Privilege escalation attempt detected", event);
        }
    }
    
    private boolean isSuspiciousActivity(String username, String ipAddress) {
        // Check for multiple failed attempts
        long failedAttempts = securityEventRepository.countFailedAttempts(username, ipAddress, 
            Instant.now().minus(Duration.ofMinutes(15)));
        
        return failedAttempts > 5;
    }
    
    private boolean isPrivilegeEscalationAttempt(String username, String resource) {
        // Check if user is trying to access admin resources
        return resource.startsWith("/api/admin/");
    }
}

// Security Audit Service
@Service
public class SecurityAuditService {
    @Autowired
    private SecurityEventRepository securityEventRepository;
    
    public SecurityAuditReport generateAuditReport(Instant from, Instant to) {
        List<SecurityEvent> events = securityEventRepository.findByTimestampBetween(from, to);
        
        SecurityAuditReport report = SecurityAuditReport.builder()
            .from(from)
            .to(to)
            .totalEvents(events.size())
            .authenticationEvents(events.stream()
                .filter(e -> "AUTHENTICATION_ATTEMPT".equals(e.getEventType()))
                .count())
            .authorizationEvents(events.stream()
                .filter(e -> "AUTHORIZATION_ATTEMPT".equals(e.getEventType()))
                .count())
            .failedAttempts(events.stream()
                .filter(e -> !e.isSuccess())
                .count())
            .build();
        
        return report;
    }
}
```

### Security Metrics:

```java
// Security Metrics
@Component
public class SecurityMetrics {
    private final MeterRegistry meterRegistry;
    private final Counter authenticationAttempts;
    private final Counter authenticationFailures;
    private final Counter authorizationAttempts;
    private final Counter authorizationFailures;
    
    public SecurityMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.authenticationAttempts = Counter.builder("security.authentication.attempts")
            .description("Number of authentication attempts")
            .register(meterRegistry);
        this.authenticationFailures = Counter.builder("security.authentication.failures")
            .description("Number of authentication failures")
            .register(meterRegistry);
        this.authorizationAttempts = Counter.builder("security.authorization.attempts")
            .description("Number of authorization attempts")
            .register(meterRegistry);
        this.authorizationFailures = Counter.builder("security.authorization.failures")
            .description("Number of authorization failures")
            .register(meterRegistry);
    }
    
    public void recordAuthenticationAttempt(boolean success) {
        authenticationAttempts.increment();
        if (!success) {
            authenticationFailures.increment();
        }
    }
    
    public void recordAuthorizationAttempt(boolean success) {
        authorizationAttempts.increment();
        if (!success) {
            authorizationFailures.increment();
        }
    }
}
```

This comprehensive guide covers all aspects of microservices security, providing both theoretical understanding and practical implementation examples. Each concept is explained with real-world scenarios and Java code examples to make the concepts clear and actionable.