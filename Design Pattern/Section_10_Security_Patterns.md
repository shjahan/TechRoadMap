# Section 10 - Security Patterns

## 10.1 Authentication Patterns

Authentication patterns ensure that users are who they claim to be before granting access to system resources.

### When to Use:
- When you need to verify user identity
- When you want to control access to resources
- When you need to maintain user sessions

### Real-World Analogy:
Think of a high-security building where you need to show your ID card and go through a security checkpoint before being allowed to enter. The security guard verifies your identity and grants you access based on your credentials.

### Basic Implementation:
```java
// Authentication service interface
public interface AuthenticationService {
    AuthenticationResult authenticate(String username, String password);
    boolean isAuthenticated(String sessionId);
    void logout(String sessionId);
}

// Authentication result
public class AuthenticationResult {
    private boolean success;
    private String sessionId;
    private String errorMessage;
    private User user;
    
    public AuthenticationResult(boolean success, String sessionId, User user) {
        this.success = success;
        this.sessionId = sessionId;
        this.user = user;
    }
    
    // Getters and setters
    public boolean isSuccess() { return success; }
    public String getSessionId() { return sessionId; }
    public String getErrorMessage() { return errorMessage; }
    public User getUser() { return user; }
}

// Simple authentication service
public class SimpleAuthenticationService implements AuthenticationService {
    private UserRepository userRepository;
    private PasswordEncoder passwordEncoder;
    private SessionManager sessionManager;
    
    public SimpleAuthenticationService(UserRepository userRepository, 
                                     PasswordEncoder passwordEncoder,
                                     SessionManager sessionManager) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.sessionManager = sessionManager;
    }
    
    public AuthenticationResult authenticate(String username, String password) {
        try {
            User user = userRepository.findByUsername(username);
            if (user == null) {
                return new AuthenticationResult(false, null, null);
            }
            
            if (passwordEncoder.matches(password, user.getPasswordHash())) {
                String sessionId = sessionManager.createSession(user);
                return new AuthenticationResult(true, sessionId, user);
            } else {
                return new AuthenticationResult(false, null, null);
            }
        } catch (Exception e) {
            return new AuthenticationResult(false, null, null);
        }
    }
    
    public boolean isAuthenticated(String sessionId) {
        return sessionManager.isValidSession(sessionId);
    }
    
    public void logout(String sessionId) {
        sessionManager.invalidateSession(sessionId);
    }
}
```

## 10.2 Authorization Patterns

Authorization patterns control what authenticated users can access and what actions they can perform.

### When to Use:
- When you need to control access to resources
- When you want to implement role-based access control
- When you need to enforce business rules

### Real-World Analogy:
Think of a company's access control system where employees have different levels of access. A regular employee can access their own files, a manager can access their team's files, and an admin can access everything.

### Basic Implementation:
```java
// Authorization service interface
public interface AuthorizationService {
    boolean hasPermission(String userId, String resource, String action);
    boolean hasRole(String userId, String role);
    List<String> getUserPermissions(String userId);
}

// Role-based authorization
public class RoleBasedAuthorizationService implements AuthorizationService {
    private UserRoleRepository userRoleRepository;
    private RolePermissionRepository rolePermissionRepository;
    
    public RoleBasedAuthorizationService(UserRoleRepository userRoleRepository,
                                       RolePermissionRepository rolePermissionRepository) {
        this.userRoleRepository = userRoleRepository;
        this.rolePermissionRepository = rolePermissionRepository;
    }
    
    public boolean hasPermission(String userId, String resource, String action) {
        List<String> userRoles = userRoleRepository.getUserRoles(userId);
        
        for (String role : userRoles) {
            if (rolePermissionRepository.hasPermission(role, resource, action)) {
                return true;
            }
        }
        return false;
    }
    
    public boolean hasRole(String userId, String role) {
        List<String> userRoles = userRoleRepository.getUserRoles(userId);
        return userRoles.contains(role);
    }
    
    public List<String> getUserPermissions(String userId) {
        List<String> userRoles = userRoleRepository.getUserRoles(userId);
        List<String> permissions = new ArrayList<>();
        
        for (String role : userRoles) {
            permissions.addAll(rolePermissionRepository.getRolePermissions(role));
        }
        
        return permissions;
    }
}

// Permission-based authorization
public class PermissionBasedAuthorizationService implements AuthorizationService {
    private UserPermissionRepository userPermissionRepository;
    
    public PermissionBasedAuthorizationService(UserPermissionRepository userPermissionRepository) {
        this.userPermissionRepository = userPermissionRepository;
    }
    
    public boolean hasPermission(String userId, String resource, String action) {
        String permission = resource + ":" + action;
        return userPermissionRepository.hasPermission(userId, permission);
    }
    
    public boolean hasRole(String userId, String role) {
        // Not applicable for permission-based authorization
        return false;
    }
    
    public List<String> getUserPermissions(String userId) {
        return userPermissionRepository.getUserPermissions(userId);
    }
}
```

## 10.3 Session Management Patterns

Session management patterns handle user sessions, ensuring secure and efficient session handling.

### When to Use:
- When you need to maintain user state
- When you want to implement session security
- When you need to handle session timeouts

### Real-World Analogy:
Think of a hotel key card system. You get a key card when you check in, and it works for a certain period. If you lose it or it expires, you need to get a new one.

### Basic Implementation:
```java
// Session manager interface
public interface SessionManager {
    String createSession(User user);
    boolean isValidSession(String sessionId);
    User getSessionUser(String sessionId);
    void invalidateSession(String sessionId);
    void extendSession(String sessionId);
}

// Simple session manager
public class SimpleSessionManager implements SessionManager {
    private Map<String, Session> sessions = new HashMap<>();
    private long sessionTimeout = 30 * 60 * 1000; // 30 minutes
    
    public String createSession(User user) {
        String sessionId = generateSessionId();
        Session session = new Session(sessionId, user, System.currentTimeMillis());
        sessions.put(sessionId, session);
        return sessionId;
    }
    
    public boolean isValidSession(String sessionId) {
        Session session = sessions.get(sessionId);
        if (session == null) {
            return false;
        }
        
        if (System.currentTimeMillis() - session.getCreatedAt() > sessionTimeout) {
            sessions.remove(sessionId);
            return false;
        }
        
        return true;
    }
    
    public User getSessionUser(String sessionId) {
        Session session = sessions.get(sessionId);
        if (session != null && isValidSession(sessionId)) {
            return session.getUser();
        }
        return null;
    }
    
    public void invalidateSession(String sessionId) {
        sessions.remove(sessionId);
    }
    
    public void extendSession(String sessionId) {
        Session session = sessions.get(sessionId);
        if (session != null) {
            session.setLastAccessedAt(System.currentTimeMillis());
        }
    }
    
    private String generateSessionId() {
        return UUID.randomUUID().toString();
    }
}

// Session class
public class Session {
    private String sessionId;
    private User user;
    private long createdAt;
    private long lastAccessedAt;
    
    public Session(String sessionId, User user, long createdAt) {
        this.sessionId = sessionId;
        this.user = user;
        this.createdAt = createdAt;
        this.lastAccessedAt = createdAt;
    }
    
    // Getters and setters
    public String getSessionId() { return sessionId; }
    public User getUser() { return user; }
    public long getCreatedAt() { return createdAt; }
    public long getLastAccessedAt() { return lastAccessedAt; }
    public void setLastAccessedAt(long lastAccessedAt) { this.lastAccessedAt = lastAccessedAt; }
}
```

## 10.4 Input Validation Patterns

Input validation patterns ensure that user input is safe and meets application requirements.

### When to Use:
- When you need to prevent injection attacks
- When you want to ensure data integrity
- When you need to validate user input

### Real-World Analogy:
Think of a security checkpoint at an airport where every item is checked for prohibited materials. The security system validates each item to ensure it's safe before allowing it through.

### Basic Implementation:
```java
// Input validator interface
public interface InputValidator {
    ValidationResult validate(String input);
    boolean isValid(String input);
}

// Email validator
public class EmailValidator implements InputValidator {
    private static final String EMAIL_REGEX = "^[A-Za-z0-9+_.-]+@(.+)$";
    private Pattern pattern = Pattern.compile(EMAIL_REGEX);
    
    public ValidationResult validate(String input) {
        if (input == null || input.trim().isEmpty()) {
            return new ValidationResult(false, "Email cannot be empty");
        }
        
        if (pattern.matcher(input).matches()) {
            return new ValidationResult(true, null);
        } else {
            return new ValidationResult(false, "Invalid email format");
        }
    }
    
    public boolean isValid(String input) {
        return validate(input).isValid();
    }
}

// SQL injection validator
public class SqlInjectionValidator implements InputValidator {
    private static final String[] SQL_KEYWORDS = {
        "SELECT", "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER"
    };
    
    public ValidationResult validate(String input) {
        if (input == null) {
            return new ValidationResult(true, null);
        }
        
        String upperInput = input.toUpperCase();
        for (String keyword : SQL_KEYWORDS) {
            if (upperInput.contains(keyword)) {
                return new ValidationResult(false, "Potential SQL injection detected");
            }
        }
        
        return new ValidationResult(true, null);
    }
    
    public boolean isValid(String input) {
        return validate(input).isValid();
    }
}

// Composite validator
public class CompositeValidator implements InputValidator {
    private List<InputValidator> validators = new ArrayList<>();
    
    public void addValidator(InputValidator validator) {
        validators.add(validator);
    }
    
    public ValidationResult validate(String input) {
        for (InputValidator validator : validators) {
            ValidationResult result = validator.validate(input);
            if (!result.isValid()) {
                return result;
            }
        }
        return new ValidationResult(true, null);
    }
    
    public boolean isValid(String input) {
        return validate(input).isValid();
    }
}

// Validation result
public class ValidationResult {
    private boolean valid;
    private String errorMessage;
    
    public ValidationResult(boolean valid, String errorMessage) {
        this.valid = valid;
        this.errorMessage = errorMessage;
    }
    
    public boolean isValid() { return valid; }
    public String getErrorMessage() { return errorMessage; }
}
```

## 10.5 Output Encoding Patterns

Output encoding patterns prevent XSS attacks by properly encoding output data.

### When to Use:
- When you need to prevent XSS attacks
- When you want to ensure safe output
- When you need to handle special characters

### Real-World Analogy:
Think of a document that needs to be translated into a different language. The translator ensures that special characters and symbols are properly converted so they display correctly and don't cause issues.

### Basic Implementation:
```java
// Output encoder interface
public interface OutputEncoder {
    String encode(String input);
    String encodeForHtml(String input);
    String encodeForUrl(String input);
    String encodeForJavaScript(String input);
}

// HTML output encoder
public class HtmlOutputEncoder implements OutputEncoder {
    public String encode(String input) {
        return encodeForHtml(input);
    }
    
    public String encodeForHtml(String input) {
        if (input == null) {
            return null;
        }
        
        return input
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\"", "&quot;")
            .replace("'", "&#x27;")
            .replace("/", "&#x2F;");
    }
    
    public String encodeForUrl(String input) {
        if (input == null) {
            return null;
        }
        
        try {
            return URLEncoder.encode(input, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException("UTF-8 encoding not supported", e);
        }
    }
    
    public String encodeForJavaScript(String input) {
        if (input == null) {
            return null;
        }
        
        return input
            .replace("\\", "\\\\")
            .replace("\"", "\\\"")
            .replace("'", "\\'")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t");
    }
}

// Context-aware encoder
public class ContextAwareEncoder implements OutputEncoder {
    private Map<String, OutputEncoder> encoders = new HashMap<>();
    
    public ContextAwareEncoder() {
        encoders.put("html", new HtmlOutputEncoder());
        encoders.put("url", new HtmlOutputEncoder());
        encoders.put("javascript", new HtmlOutputEncoder());
    }
    
    public String encode(String input) {
        return encodeForHtml(input);
    }
    
    public String encodeForHtml(String input) {
        return encoders.get("html").encodeForHtml(input);
    }
    
    public String encodeForUrl(String input) {
        return encoders.get("url").encodeForUrl(input);
    }
    
    public String encodeForJavaScript(String input) {
        return encoders.get("javascript").encodeForJavaScript(input);
    }
    
    public String encodeForContext(String input, String context) {
        OutputEncoder encoder = encoders.get(context);
        if (encoder != null) {
            return encoder.encode(input);
        }
        return input;
    }
}
```

## 10.6 Error Handling Patterns

Error handling patterns ensure that security-sensitive information is not leaked through error messages.

### When to Use:
- When you need to prevent information disclosure
- When you want to provide user-friendly error messages
- When you need to log security events

### Real-World Analogy:
Think of a bank's error handling system. When there's a problem, customers get a generic message like "Transaction failed" rather than specific technical details that could help attackers.

### Basic Implementation:
```java
// Security error handler
public class SecurityErrorHandler {
    private Logger logger;
    private ErrorMessageProvider errorMessageProvider;
    
    public SecurityErrorHandler(Logger logger, ErrorMessageProvider errorMessageProvider) {
        this.logger = logger;
        this.errorMessageProvider = errorMessageProvider;
    }
    
    public ErrorResponse handleSecurityError(SecurityException e, HttpServletRequest request) {
        // Log the actual error for administrators
        logger.error("Security error occurred", e);
        
        // Log security event
        logSecurityEvent(e, request);
        
        // Return generic error message to user
        String userMessage = errorMessageProvider.getGenericErrorMessage();
        return new ErrorResponse("SECURITY_ERROR", userMessage);
    }
    
    public ErrorResponse handleAuthenticationError(AuthenticationException e, HttpServletRequest request) {
        logger.warn("Authentication failed for user: " + request.getParameter("username"));
        
        // Return generic authentication error
        return new ErrorResponse("AUTHENTICATION_ERROR", "Invalid credentials");
    }
    
    public ErrorResponse handleAuthorizationError(AuthorizationException e, HttpServletRequest request) {
        logger.warn("Authorization failed for user: " + getCurrentUser(request));
        
        // Return generic authorization error
        return new ErrorResponse("AUTHORIZATION_ERROR", "Access denied");
    }
    
    private void logSecurityEvent(SecurityException e, HttpServletRequest request) {
        SecurityEvent event = new SecurityEvent(
            e.getClass().getSimpleName(),
            getCurrentUser(request),
            request.getRemoteAddr(),
            System.currentTimeMillis()
        );
        
        logger.info("Security event: " + event);
    }
    
    private String getCurrentUser(HttpServletRequest request) {
        // Extract current user from request
        return "unknown";
    }
}

// Error response
public class ErrorResponse {
    private String errorCode;
    private String message;
    private long timestamp;
    
    public ErrorResponse(String errorCode, String message) {
        this.errorCode = errorCode;
        this.message = message;
        this.timestamp = System.currentTimeMillis();
    }
    
    // Getters
    public String getErrorCode() { return errorCode; }
    public String getMessage() { return message; }
    public long getTimestamp() { return timestamp; }
}
```

## 10.7 Logging and Auditing Patterns

Logging and auditing patterns track security events and user actions for compliance and security monitoring.

### When to Use:
- When you need to track security events
- When you want to maintain audit trails
- When you need to comply with regulations

### Real-World Analogy:
Think of a security camera system that records all activities in a building. The recordings provide evidence of what happened and help identify security breaches.

### Basic Implementation:
```java
// Security logger interface
public interface SecurityLogger {
    void logAuthentication(String userId, boolean success, String ipAddress);
    void logAuthorization(String userId, String resource, String action, boolean success);
    void logSecurityEvent(String eventType, String userId, String details);
    void logDataAccess(String userId, String resource, String action);
}

// Audit logger
public class AuditLogger implements SecurityLogger {
    private Logger logger;
    private AuditRepository auditRepository;
    
    public AuditLogger(Logger logger, AuditRepository auditRepository) {
        this.logger = logger;
        this.auditRepository = auditRepository;
    }
    
    public void logAuthentication(String userId, boolean success, String ipAddress) {
        AuditEntry entry = new AuditEntry(
            "AUTHENTICATION",
            userId,
            success ? "SUCCESS" : "FAILURE",
            "IP: " + ipAddress,
            System.currentTimeMillis()
        );
        
        logger.info("Authentication attempt: " + entry);
        auditRepository.save(entry);
    }
    
    public void logAuthorization(String userId, String resource, String action, boolean success) {
        AuditEntry entry = new AuditEntry(
            "AUTHORIZATION",
            userId,
            success ? "SUCCESS" : "FAILURE",
            "Resource: " + resource + ", Action: " + action,
            System.currentTimeMillis()
        );
        
        logger.info("Authorization attempt: " + entry);
        auditRepository.save(entry);
    }
    
    public void logSecurityEvent(String eventType, String userId, String details) {
        AuditEntry entry = new AuditEntry(
            eventType,
            userId,
            "EVENT",
            details,
            System.currentTimeMillis()
        );
        
        logger.warn("Security event: " + entry);
        auditRepository.save(entry);
    }
    
    public void logDataAccess(String userId, String resource, String action) {
        AuditEntry entry = new AuditEntry(
            "DATA_ACCESS",
            userId,
            "SUCCESS",
            "Resource: " + resource + ", Action: " + action,
            System.currentTimeMillis()
        );
        
        logger.info("Data access: " + entry);
        auditRepository.save(entry);
    }
}

// Audit entry
public class AuditEntry {
    private String eventType;
    private String userId;
    private String result;
    private String details;
    private long timestamp;
    
    public AuditEntry(String eventType, String userId, String result, String details, long timestamp) {
        this.eventType = eventType;
        this.userId = userId;
        this.result = result;
        this.details = details;
        this.timestamp = timestamp;
    }
    
    // Getters
    public String getEventType() { return eventType; }
    public String getUserId() { return userId; }
    public String getResult() { return result; }
    public String getDetails() { return details; }
    public long getTimestamp() { return timestamp; }
}
```

## 10.8 Encryption Patterns

Encryption patterns protect sensitive data by converting it into a form that cannot be easily understood by unauthorized users.

### When to Use:
- When you need to protect sensitive data
- When you want to ensure data confidentiality
- When you need to comply with data protection regulations

### Real-World Analogy:
Think of a secret code that only authorized people can understand. Even if someone intercepts the message, they can't read it without knowing the code.

### Basic Implementation:
```java
// Encryption service interface
public interface EncryptionService {
    String encrypt(String plaintext);
    String decrypt(String ciphertext);
    String hash(String input);
    boolean verifyHash(String input, String hash);
}

// AES encryption service
public class AesEncryptionService implements EncryptionService {
    private SecretKey secretKey;
    private Cipher cipher;
    
    public AesEncryptionService(String key) throws Exception {
        this.secretKey = new SecretKeySpec(key.getBytes(), "AES");
        this.cipher = Cipher.getInstance("AES");
    }
    
    public String encrypt(String plaintext) {
        try {
            cipher.init(Cipher.ENCRYPT_MODE, secretKey);
            byte[] encryptedBytes = cipher.doFinal(plaintext.getBytes());
            return Base64.getEncoder().encodeToString(encryptedBytes);
        } catch (Exception e) {
            throw new RuntimeException("Encryption failed", e);
        }
    }
    
    public String decrypt(String ciphertext) {
        try {
            cipher.init(Cipher.DECRYPT_MODE, secretKey);
            byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(ciphertext));
            return new String(decryptedBytes);
        } catch (Exception e) {
            throw new RuntimeException("Decryption failed", e);
        }
    }
    
    public String hash(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hashBytes = digest.digest(input.getBytes());
            return Base64.getEncoder().encodeToString(hashBytes);
        } catch (Exception e) {
            throw new RuntimeException("Hashing failed", e);
        }
    }
    
    public boolean verifyHash(String input, String hash) {
        String inputHash = hash(input);
        return inputHash.equals(hash);
    }
}

// Password hashing service
public class PasswordHashingService {
    private static final int SALT_LENGTH = 16;
    private static final int ITERATIONS = 10000;
    
    public String hashPassword(String password) {
        try {
            // Generate random salt
            byte[] salt = generateSalt();
            
            // Hash password with salt
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            digest.update(salt);
            byte[] hash = digest.digest(password.getBytes());
            
            // Combine salt and hash
            byte[] saltAndHash = new byte[salt.length + hash.length];
            System.arraycopy(salt, 0, saltAndHash, 0, salt.length);
            System.arraycopy(hash, 0, saltAndHash, salt.length, hash.length);
            
            return Base64.getEncoder().encodeToString(saltAndHash);
        } catch (Exception e) {
            throw new RuntimeException("Password hashing failed", e);
        }
    }
    
    public boolean verifyPassword(String password, String hashedPassword) {
        try {
            byte[] saltAndHash = Base64.getDecoder().decode(hashedPassword);
            byte[] salt = new byte[SALT_LENGTH];
            System.arraycopy(saltAndHash, 0, salt, 0, SALT_LENGTH);
            
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            digest.update(salt);
            byte[] hash = digest.digest(password.getBytes());
            
            byte[] storedHash = new byte[saltAndHash.length - SALT_LENGTH];
            System.arraycopy(saltAndHash, SALT_LENGTH, storedHash, 0, storedHash.length);
            
            return Arrays.equals(hash, storedHash);
        } catch (Exception e) {
            throw new RuntimeException("Password verification failed", e);
        }
    }
    
    private byte[] generateSalt() {
        byte[] salt = new byte[SALT_LENGTH];
        new SecureRandom().nextBytes(salt);
        return salt;
    }
}
```

## 10.9 Access Control Patterns

Access control patterns implement various access control models to protect resources.

### When to Use:
- When you need to implement access control
- When you want to enforce security policies
- When you need to manage user permissions

### Real-World Analogy:
Think of a building with different access levels. Some people can only access the lobby, others can access their office floor, and only security personnel can access the control room.

### Basic Implementation:
```java
// Access control interface
public interface AccessControl {
    boolean hasAccess(String userId, String resource, String action);
    void grantAccess(String userId, String resource, String action);
    void revokeAccess(String userId, String resource, String action);
}

// Role-based access control
public class RoleBasedAccessControl implements AccessControl {
    private Map<String, Set<String>> userRoles = new HashMap<>();
    private Map<String, Set<String>> rolePermissions = new HashMap<>();
    
    public boolean hasAccess(String userId, String resource, String action) {
        Set<String> userRoles = this.userRoles.get(userId);
        if (userRoles == null) {
            return false;
        }
        
        for (String role : userRoles) {
            Set<String> permissions = rolePermissions.get(role);
            if (permissions != null && permissions.contains(resource + ":" + action)) {
                return true;
            }
        }
        return false;
    }
    
    public void grantAccess(String userId, String resource, String action) {
        // Grant access by assigning role
        String role = resource + "_" + action;
        userRoles.computeIfAbsent(userId, k -> new HashSet<>()).add(role);
        rolePermissions.computeIfAbsent(role, k -> new HashSet<>()).add(resource + ":" + action);
    }
    
    public void revokeAccess(String userId, String resource, String action) {
        String role = resource + "_" + action;
        userRoles.getOrDefault(userId, new HashSet<>()).remove(role);
    }
}

// Attribute-based access control
public class AttributeBasedAccessControl implements AccessControl {
    private Map<String, Map<String, Object>> userAttributes = new HashMap<>();
    private Map<String, Map<String, Object>> resourceAttributes = new HashMap<>();
    private PolicyEngine policyEngine;
    
    public AttributeBasedAccessControl(PolicyEngine policyEngine) {
        this.policyEngine = policyEngine;
    }
    
    public boolean hasAccess(String userId, String resource, String action) {
        Map<String, Object> userAttrs = userAttributes.get(userId);
        Map<String, Object> resourceAttrs = resourceAttributes.get(resource);
        
        if (userAttrs == null || resourceAttrs == null) {
            return false;
        }
        
        return policyEngine.evaluate(userAttrs, resourceAttrs, action);
    }
    
    public void grantAccess(String userId, String resource, String action) {
        // Grant access by setting attributes
        userAttributes.computeIfAbsent(userId, k -> new HashMap<>())
            .put("canAccess", resource + ":" + action);
    }
    
    public void revokeAccess(String userId, String resource, String action) {
        Map<String, Object> attrs = userAttributes.get(userId);
        if (attrs != null) {
            attrs.remove("canAccess");
        }
    }
}
```

## 10.10 Security Monitoring Patterns

Security monitoring patterns detect and respond to security threats in real-time.

### When to Use:
- When you need to detect security threats
- When you want to implement real-time monitoring
- When you need to respond to security incidents

### Real-World Analogy:
Think of a security system that monitors a building 24/7. It detects unusual activities, sounds alarms when there's a breach, and can automatically lock doors or call security.

### Basic Implementation:
```java
// Security monitor interface
public interface SecurityMonitor {
    void monitorEvent(SecurityEvent event);
    void startMonitoring();
    void stopMonitoring();
}

// Real-time security monitor
public class RealTimeSecurityMonitor implements SecurityMonitor {
    private List<SecurityRule> rules = new ArrayList<>();
    private List<SecurityAlert> alerts = new ArrayList<>();
    private boolean monitoring = false;
    
    public void monitorEvent(SecurityEvent event) {
        for (SecurityRule rule : rules) {
            if (rule.matches(event)) {
                SecurityAlert alert = rule.createAlert(event);
                alerts.add(alert);
                handleAlert(alert);
            }
        }
    }
    
    public void startMonitoring() {
        monitoring = true;
        // Start monitoring thread
    }
    
    public void stopMonitoring() {
        monitoring = false;
    }
    
    private void handleAlert(SecurityAlert alert) {
        // Log alert
        System.out.println("Security alert: " + alert.getMessage());
        
        // Take action based on alert severity
        switch (alert.getSeverity()) {
            case LOW:
                logAlert(alert);
                break;
            case MEDIUM:
                logAlert(alert);
                notifySecurityTeam(alert);
                break;
            case HIGH:
                logAlert(alert);
                notifySecurityTeam(alert);
                blockUser(alert.getUserId());
                break;
            case CRITICAL:
                logAlert(alert);
                notifySecurityTeam(alert);
                blockUser(alert.getUserId());
                lockDownSystem();
                break;
        }
    }
    
    private void logAlert(SecurityAlert alert) {
        // Log to security log
    }
    
    private void notifySecurityTeam(SecurityAlert alert) {
        // Send notification to security team
    }
    
    private void blockUser(String userId) {
        // Block user account
    }
    
    private void lockDownSystem() {
        // Implement system lockdown
    }
}

// Security rule
public class SecurityRule {
    private String name;
    private Predicate<SecurityEvent> condition;
    private AlertSeverity severity;
    
    public SecurityRule(String name, Predicate<SecurityEvent> condition, AlertSeverity severity) {
        this.name = name;
        this.condition = condition;
        this.severity = severity;
    }
    
    public boolean matches(SecurityEvent event) {
        return condition.test(event);
    }
    
    public SecurityAlert createAlert(SecurityEvent event) {
        return new SecurityAlert(
            name,
            "Security rule triggered: " + name,
            severity,
            event.getUserId(),
            System.currentTimeMillis()
        );
    }
}

// Security alert
public class SecurityAlert {
    private String ruleName;
    private String message;
    private AlertSeverity severity;
    private String userId;
    private long timestamp;
    
    public SecurityAlert(String ruleName, String message, AlertSeverity severity, String userId, long timestamp) {
        this.ruleName = ruleName;
        this.message = message;
        this.severity = severity;
        this.userId = userId;
        this.timestamp = timestamp;
    }
    
    // Getters
    public String getRuleName() { return ruleName; }
    public String getMessage() { return message; }
    public AlertSeverity getSeverity() { return severity; }
    public String getUserId() { return userId; }
    public long getTimestamp() { return timestamp; }
}

// Alert severity enum
public enum AlertSeverity {
    LOW, MEDIUM, HIGH, CRITICAL
}
```

This comprehensive coverage of security patterns provides the foundation for building secure applications. Each pattern addresses specific security concerns and offers different approaches to protecting systems and data.