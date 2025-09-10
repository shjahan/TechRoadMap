# Section 18 - Security & Best Practices

## 18.1 Java Security Model

The Java Security Model is a comprehensive framework that provides multiple layers of security to protect Java applications from various threats and vulnerabilities.

### Core Concepts:

**1. Security Architecture:**
- Sandbox model for applets and untrusted code
- Class loader security
- Bytecode verification
- Access control mechanisms

**2. Security Manager:**
- Controls access to system resources
- Defines security policies
- Enforces permission checks
- Can be enabled/disabled per application

**3. Security Policies:**
- Define what permissions are granted to code
- Based on code source and signers
- Stored in policy files
- Applied at runtime

### Example:

```java
import java.security.*;

public class SecurityModelExample {
    public static void main(String[] args) {
        // Check if security manager is enabled
        SecurityManager sm = System.getSecurityManager();
        if (sm != null) {
            System.out.println("Security Manager is enabled");
        } else {
            System.out.println("Security Manager is disabled");
        }
        
        // Demonstrate permission checking
        try {
            // This will throw SecurityException if not allowed
            System.setProperty("java.security.policy", "my.policy");
            System.out.println("Property set successfully");
        } catch (SecurityException e) {
            System.out.println("Security exception: " + e.getMessage());
        }
        
        // Check current permissions
        checkPermissions();
    }
    
    public static void checkPermissions() {
        AccessController.doPrivileged(new PrivilegedAction<Void>() {
            public Void run() {
                // Check file read permission
                try {
                    FilePermission filePermission = new FilePermission("test.txt", "read");
                    AccessController.checkPermission(filePermission);
                    System.out.println("File read permission granted");
                } catch (AccessControlException e) {
                    System.out.println("File read permission denied: " + e.getMessage());
                }
                
                // Check network permission
                try {
                    SocketPermission socketPermission = new SocketPermission("www.google.com:80", "connect");
                    AccessController.checkPermission(socketPermission);
                    System.out.println("Network permission granted");
                } catch (AccessControlException e) {
                    System.out.println("Network permission denied: " + e.getMessage());
                }
                
                return null;
            }
        });
    }
}
```

### Real-world Analogy:
Java Security Model is like a multi-layered security system in a high-security building:
- **Sandbox:** Like a restricted area where visitors can only access certain rooms
- **Security Manager:** Like security guards who check credentials at each checkpoint
- **Policies:** Like the building's security rules that define who can access what

## 18.2 Authentication & Authorization

Authentication and Authorization are fundamental security concepts that control who can access what in a Java application.

### Core Concepts:

**1. Authentication:**
- Verifying user identity
- Login mechanisms
- Password management
- Multi-factor authentication

**2. Authorization:**
- Controlling access to resources
- Role-based access control (RBAC)
- Permission-based access control
- Resource-level security

**3. Security Frameworks:**
- Spring Security
- Apache Shiro
- Java Authentication and Authorization Service (JAAS)
- OAuth 2.0 / OpenID Connect

### Example:

```java
// Spring Security Configuration
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(authz -> authz
                .requestMatchers("/public/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .requestMatchers("/user/**").hasAnyRole("USER", "ADMIN")
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .loginPage("/login")
                .defaultSuccessUrl("/dashboard")
                .failureUrl("/login?error=true")
            )
            .logout(logout -> logout
                .logoutUrl("/logout")
                .logoutSuccessUrl("/login?logout=true")
            )
            .sessionManagement(session -> session
                .maximumSessions(1)
                .maxSessionsPreventsLogin(false)
            );
        
        return http.build();
    }
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}

// User Service with Authentication
@Service
public class UserService {
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    public User authenticate(String username, String password) {
        User user = userRepository.findByUsername(username);
        if (user != null && passwordEncoder.matches(password, user.getPassword())) {
            return user;
        }
        throw new AuthenticationException("Invalid credentials");
    }
    
    public boolean hasPermission(User user, String resource, String action) {
        // Check if user has permission to perform action on resource
        return user.getRoles().stream()
            .anyMatch(role -> role.hasPermission(resource, action));
    }
}

// JWT Token Service
@Service
public class JwtTokenService {
    
    private static final String SECRET_KEY = "mySecretKey";
    private static final int EXPIRATION_TIME = 86400000; // 24 hours
    
    public String generateToken(UserDetails userDetails) {
        Map<String, Object> claims = new HashMap<>();
        claims.put("roles", userDetails.getAuthorities());
        
        return Jwts.builder()
            .setClaims(claims)
            .setSubject(userDetails.getUsername())
            .setIssuedAt(new Date(System.currentTimeMillis()))
            .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
            .signWith(SignatureAlgorithm.HS512, SECRET_KEY)
            .compact();
    }
    
    public boolean validateToken(String token, UserDetails userDetails) {
        try {
            String username = extractUsername(token);
            return username.equals(userDetails.getUsername()) && !isTokenExpired(token);
        } catch (Exception e) {
            return false;
        }
    }
    
    private String extractUsername(String token) {
        return Jwts.parser()
            .setSigningKey(SECRET_KEY)
            .parseClaimsJws(token)
            .getBody()
            .getSubject();
    }
    
    private boolean isTokenExpired(String token) {
        Date expiration = Jwts.parser()
            .setSigningKey(SECRET_KEY)
            .parseClaimsJws(token)
            .getBody()
            .getExpiration();
        return expiration.before(new Date());
    }
}
```

### Real-world Analogy:
Authentication and Authorization are like a hotel's security system:
- **Authentication:** Like checking in at the front desk with your ID and reservation
- **Authorization:** Like your room key that only works for your floor and room
- **Roles:** Like different types of access (guest, staff, manager) with different permissions

## 18.3 Cryptography & Encryption

Cryptography provides the mathematical foundation for secure communication and data protection in Java applications.

### Core Concepts:

**1. Symmetric Encryption:**
- Same key for encryption and decryption
- Fast and efficient
- Examples: AES, DES, 3DES
- Used for bulk data encryption

**2. Asymmetric Encryption:**
- Public/private key pairs
- More secure but slower
- Examples: RSA, ECC
- Used for key exchange and digital signatures

**3. Hash Functions:**
- One-way functions
- Fixed-length output
- Examples: SHA-256, MD5
- Used for password hashing and data integrity

### Example:

```java
import javax.crypto.*;
import javax.crypto.spec.SecretKeySpec;
import java.security.*;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

public class CryptographyExample {
    
    // Symmetric Encryption (AES)
    public static String encryptAES(String plainText, String secretKey) throws Exception {
        SecretKeySpec key = new SecretKeySpec(secretKey.getBytes(), "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        
        byte[] encryptedBytes = cipher.doFinal(plainText.getBytes());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }
    
    public static String decryptAES(String encryptedText, String secretKey) throws Exception {
        SecretKeySpec key = new SecretKeySpec(secretKey.getBytes(), "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.DECRYPT_MODE, key);
        
        byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(encryptedText));
        return new String(decryptedBytes);
    }
    
    // Asymmetric Encryption (RSA)
    public static KeyPair generateRSAKeyPair() throws Exception {
        KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA");
        keyPairGenerator.initialize(2048);
        return keyPairGenerator.generateKeyPair();
    }
    
    public static String encryptRSA(String plainText, PublicKey publicKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        
        byte[] encryptedBytes = cipher.doFinal(plainText.getBytes());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }
    
    public static String decryptRSA(String encryptedText, PrivateKey privateKey) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.DECRYPT_MODE, privateKey);
        
        byte[] decryptedBytes = cipher.doFinal(Base64.getDecoder().decode(encryptedText));
        return new String(decryptedBytes);
    }
    
    // Digital Signature
    public static String signData(String data, PrivateKey privateKey) throws Exception {
        Signature signature = Signature.getInstance("SHA256withRSA");
        signature.initSign(privateKey);
        signature.update(data.getBytes());
        
        byte[] signatureBytes = signature.sign();
        return Base64.getEncoder().encodeToString(signatureBytes);
    }
    
    public static boolean verifySignature(String data, String signature, PublicKey publicKey) throws Exception {
        Signature sig = Signature.getInstance("SHA256withRSA");
        sig.initVerify(publicKey);
        sig.update(data.getBytes());
        
        return sig.verify(Base64.getDecoder().decode(signature));
    }
    
    // Password Hashing
    public static String hashPassword(String password, String salt) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        md.update(salt.getBytes());
        byte[] hashedBytes = md.digest(password.getBytes());
        return Base64.getEncoder().encodeToString(hashedBytes);
    }
    
    public static boolean verifyPassword(String password, String hashedPassword, String salt) throws Exception {
        String hashedInput = hashPassword(password, salt);
        return hashedInput.equals(hashedPassword);
    }
    
    public static void main(String[] args) throws Exception {
        // Symmetric Encryption Example
        String secretKey = "MySecretKey12345"; // 16 characters for AES-128
        String plainText = "Hello, World!";
        
        String encryptedText = encryptAES(plainText, secretKey);
        String decryptedText = decryptAES(encryptedText, secretKey);
        
        System.out.println("Original: " + plainText);
        System.out.println("Encrypted: " + encryptedText);
        System.out.println("Decrypted: " + decryptedText);
        
        // Asymmetric Encryption Example
        KeyPair keyPair = generateRSAKeyPair();
        PublicKey publicKey = keyPair.getPublic();
        PrivateKey privateKey = keyPair.getPrivate();
        
        String rsaEncrypted = encryptRSA(plainText, publicKey);
        String rsaDecrypted = decryptRSA(rsaEncrypted, privateKey);
        
        System.out.println("\nRSA Encrypted: " + rsaEncrypted);
        System.out.println("RSA Decrypted: " + rsaDecrypted);
        
        // Digital Signature Example
        String signature = signData(plainText, privateKey);
        boolean isValid = verifySignature(plainText, signature, publicKey);
        
        System.out.println("\nSignature: " + signature);
        System.out.println("Signature Valid: " + isValid);
        
        // Password Hashing Example
        String password = "myPassword123";
        String salt = "randomSalt123";
        String hashedPassword = hashPassword(password, salt);
        boolean passwordValid = verifyPassword(password, hashedPassword, salt);
        
        System.out.println("\nHashed Password: " + hashedPassword);
        System.out.println("Password Valid: " + passwordValid);
    }
}
```

### Real-world Analogy:
Cryptography is like a sophisticated postal system:
- **Symmetric Encryption:** Like using the same key for both locking and unlocking a safe
- **Asymmetric Encryption:** Like having a public mailbox (anyone can drop mail) but only you have the key to open it
- **Digital Signatures:** Like a wax seal on a letter that proves it came from the sender
- **Hashing:** Like creating a unique fingerprint for a document that can't be reversed

## 18.4 Secure Coding Practices

Secure coding practices are essential guidelines that help developers write code that is resistant to security vulnerabilities and attacks.

### Core Concepts:

**1. Input Validation:**
- Validate all user inputs
- Sanitize data before processing
- Use whitelist validation when possible
- Prevent injection attacks

**2. Output Encoding:**
- Encode output to prevent XSS
- Use appropriate encoding for context
- Escape special characters
- Validate output format

**3. Error Handling:**
- Don't expose sensitive information
- Log errors securely
- Use generic error messages
- Implement proper exception handling

### Example:

```java
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import org.owasp.esapi.ESAPI;

public class SecureCodingExample {
    
    // Input Validation
    public static boolean isValidEmail(String email) {
        if (email == null || email.isEmpty()) {
            return false;
        }
        
        // Use regex for email validation
        String emailRegex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$";
        Pattern pattern = Pattern.compile(emailRegex);
        Matcher matcher = pattern.matcher(email);
        
        return matcher.matches();
    }
    
    public static boolean isValidUsername(String username) {
        if (username == null || username.length() < 3 || username.length() > 20) {
            return false;
        }
        
        // Only allow alphanumeric characters and underscores
        String usernameRegex = "^[a-zA-Z0-9_]+$";
        Pattern pattern = Pattern.compile(usernameRegex);
        Matcher matcher = pattern.matcher(username);
        
        return matcher.matches();
    }
    
    // SQL Injection Prevention
    public static String sanitizeSqlInput(String input) {
        if (input == null) {
            return null;
        }
        
        // Remove or escape dangerous characters
        return input.replace("'", "''")
                   .replace(";", "")
                   .replace("--", "")
                   .replace("/*", "")
                   .replace("*/", "");
    }
    
    // XSS Prevention
    public static String sanitizeHtmlInput(String input) {
        if (input == null) {
            return null;
        }
        
        // Escape HTML special characters
        return input.replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;")
                   .replace("\"", "&quot;")
                   .replace("'", "&#x27;")
                   .replace("/", "&#x2F;");
    }
    
    // Secure Password Requirements
    public static boolean isSecurePassword(String password) {
        if (password == null || password.length() < 8) {
            return false;
        }
        
        // Check for at least one uppercase letter
        boolean hasUpperCase = password.chars().anyMatch(Character::isUpperCase);
        
        // Check for at least one lowercase letter
        boolean hasLowerCase = password.chars().anyMatch(Character::isLowerCase);
        
        // Check for at least one digit
        boolean hasDigit = password.chars().anyMatch(Character::isDigit);
        
        // Check for at least one special character
        boolean hasSpecialChar = password.chars().anyMatch(ch -> 
            "!@#$%^&*()_+-=[]{}|;:,.<>?".indexOf(ch) >= 0);
        
        return hasUpperCase && hasLowerCase && hasDigit && hasSpecialChar;
    }
    
    // Secure File Upload
    public static boolean isAllowedFileType(String fileName) {
        if (fileName == null) {
            return false;
        }
        
        String extension = fileName.substring(fileName.lastIndexOf(".") + 1).toLowerCase();
        String[] allowedExtensions = {"jpg", "jpeg", "png", "gif", "pdf", "doc", "docx"};
        
        for (String allowedExt : allowedExtensions) {
            if (extension.equals(allowedExt)) {
                return true;
            }
        }
        
        return false;
    }
    
    // Secure Error Handling
    public static class SecureException extends Exception {
        private final String userMessage;
        private final String logMessage;
        
        public SecureException(String userMessage, String logMessage) {
            super(userMessage);
            this.userMessage = userMessage;
            this.logMessage = logMessage;
        }
        
        public String getUserMessage() {
            return userMessage;
        }
        
        public String getLogMessage() {
            return logMessage;
        }
    }
    
    // Secure Logging
    public static void logSecurely(String message, String userId) {
        // Remove sensitive information from logs
        String sanitizedMessage = message.replaceAll("(?i)(password|pwd|pass|secret|key|token)", "***");
        
        // Log with timestamp and user context
        System.out.println("[" + new java.util.Date() + "] User: " + userId + " - " + sanitizedMessage);
    }
    
    public static void main(String[] args) {
        // Test input validation
        System.out.println("Email validation:");
        System.out.println("test@example.com: " + isValidEmail("test@example.com"));
        System.out.println("invalid-email: " + isValidEmail("invalid-email"));
        
        System.out.println("\nUsername validation:");
        System.out.println("user123: " + isValidUsername("user123"));
        System.out.println("user@123: " + isValidUsername("user@123"));
        
        // Test password security
        System.out.println("\nPassword security:");
        System.out.println("Password123!: " + isSecurePassword("Password123!"));
        System.out.println("weak: " + isSecurePassword("weak"));
        
        // Test file upload security
        System.out.println("\nFile upload security:");
        System.out.println("document.pdf: " + isAllowedFileType("document.pdf"));
        System.out.println("script.exe: " + isAllowedFileType("script.exe"));
        
        // Test secure error handling
        try {
            throw new SecureException("An error occurred", "Detailed error information for logging");
        } catch (SecureException e) {
            System.out.println("\nUser message: " + e.getUserMessage());
            System.out.println("Log message: " + e.getLogMessage());
        }
    }
}
```

### Real-world Analogy:
Secure coding practices are like building a secure house:
- **Input Validation:** Like checking IDs at the door before letting people in
- **Output Encoding:** Like putting protective covers on electrical outlets
- **Error Handling:** Like having a security system that alerts without revealing the layout
- **Password Security:** Like having strong locks and multiple security layers

## 18.5 OWASP Guidelines

The Open Web Application Security Project (OWASP) provides comprehensive guidelines for web application security, including the famous OWASP Top 10 list of security risks.

### Core Concepts:

**1. OWASP Top 10 (2021):**
- A01:2021 – Broken Access Control
- A02:2021 – Cryptographic Failures
- A03:2021 – Injection
- A04:2021 – Insecure Design
- A05:2021 – Security Misconfiguration
- A06:2021 – Vulnerable and Outdated Components
- A07:2021 – Identification and Authentication Failures
- A08:2021 – Software and Data Integrity Failures
- A09:2021 – Security Logging and Monitoring Failures
- A10:2021 – Server-Side Request Forgery (SSRF)

**2. Security Testing:**
- Static Application Security Testing (SAST)
- Dynamic Application Security Testing (DAST)
- Interactive Application Security Testing (IAST)
- Software Composition Analysis (SCA)

**3. Security Frameworks:**
- OWASP Application Security Verification Standard (ASVS)
- OWASP Software Assurance Maturity Model (SAMM)
- OWASP Testing Guide

### Example:

```java
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import javax.validation.Valid;
import java.util.List;
import java.util.ArrayList;

// A01:2021 – Broken Access Control Prevention
@RestController
@RequestMapping("/api/users")
public class SecureUserController {
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id, 
                                      @RequestHeader("Authorization") String token) {
        // Verify user has permission to access this resource
        if (!hasPermission(token, "USER_READ", id)) {
            return ResponseEntity.status(403).build();
        }
        
        User user = userService.findById(id);
        if (user == null) {
            return ResponseEntity.notFound().build();
        }
        
        return ResponseEntity.ok(user);
    }
    
    private boolean hasPermission(String token, String action, Long resourceId) {
        // Implement proper authorization logic
        return true; // Simplified for example
    }
}

// A02:2021 – Cryptographic Failures Prevention
@Service
public class SecurePasswordService {
    
    private final PasswordEncoder passwordEncoder = new BCryptPasswordEncoder(12);
    
    public String hashPassword(String password) {
        // Use strong hashing algorithm with salt
        return passwordEncoder.encode(password);
    }
    
    public boolean verifyPassword(String password, String hashedPassword) {
        return passwordEncoder.matches(password, hashedPassword);
    }
}

// A03:2021 – Injection Prevention
@Repository
public class SecureUserRepository {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    public List<User> findUsersByName(String name) {
        // Use parameterized queries to prevent SQL injection
        String jpql = "SELECT u FROM User u WHERE u.name = :name";
        return entityManager.createQuery(jpql, User.class)
                          .setParameter("name", name)
                          .getResultList();
    }
    
    public List<User> findUsersByEmail(String email) {
        // Use Criteria API for dynamic queries
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<User> query = cb.createQuery(User.class);
        Root<User> user = query.from(User.class);
        
        query.select(user).where(cb.equal(user.get("email"), email));
        
        return entityManager.createQuery(query).getResultList();
    }
}

// A05:2021 – Security Misconfiguration Prevention
@Configuration
@EnableWebSecurity
public class SecurityConfiguration {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .headers(headers -> headers
                .frameOptions().deny()
                .contentTypeOptions().and()
                .httpStrictTransportSecurity(hstsConfig -> hstsConfig
                    .maxAgeInSeconds(31536000)
                    .includeSubdomains(true)
                )
            )
            .csrf(csrf -> csrf
                .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
            )
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                .maximumSessions(1)
                .maxSessionsPreventsLogin(false)
            );
        
        return http.build();
    }
}

// A07:2021 – Identification and Authentication Failures Prevention
@Service
public class SecureAuthenticationService {
    
    private final int MAX_LOGIN_ATTEMPTS = 5;
    private final long LOCKOUT_DURATION = 30 * 60 * 1000; // 30 minutes
    
    public boolean authenticate(String username, String password) {
        User user = userRepository.findByUsername(username);
        
        if (user == null) {
            return false;
        }
        
        // Check if account is locked
        if (isAccountLocked(user)) {
            throw new AccountLockedException("Account is temporarily locked");
        }
        
        // Verify password
        if (passwordEncoder.matches(password, user.getPassword())) {
            // Reset failed attempts on successful login
            user.setFailedLoginAttempts(0);
            user.setLastLoginAttempt(null);
            userRepository.save(user);
            return true;
        } else {
            // Increment failed attempts
            user.setFailedLoginAttempts(user.getFailedLoginAttempts() + 1);
            user.setLastLoginAttempt(System.currentTimeMillis());
            userRepository.save(user);
            return false;
        }
    }
    
    private boolean isAccountLocked(User user) {
        if (user.getFailedLoginAttempts() >= MAX_LOGIN_ATTEMPTS) {
            long timeSinceLastAttempt = System.currentTimeMillis() - user.getLastLoginAttempt();
            return timeSinceLastAttempt < LOCKOUT_DURATION;
        }
        return false;
    }
}

// A09:2021 – Security Logging and Monitoring Failures Prevention
@Component
public class SecurityLogger {
    
    private final Logger logger = LoggerFactory.getLogger(SecurityLogger.class);
    
    public void logSecurityEvent(String event, String userId, String details) {
        // Log security events with proper context
        logger.warn("SECURITY_EVENT: {} - User: {} - Details: {} - Timestamp: {}", 
                   event, userId, details, System.currentTimeMillis());
    }
    
    public void logAuthenticationFailure(String username, String ipAddress) {
        logger.warn("AUTHENTICATION_FAILURE: Username: {} - IP: {} - Timestamp: {}", 
                   username, ipAddress, System.currentTimeMillis());
    }
    
    public void logAuthorizationFailure(String userId, String resource, String action) {
        logger.warn("AUTHORIZATION_FAILURE: User: {} - Resource: {} - Action: {} - Timestamp: {}", 
                   userId, resource, action, System.currentTimeMillis());
    }
}
```

### Real-world Analogy:
OWASP guidelines are like a comprehensive security manual for building a fortress:
- **Top 10 Risks:** Like the 10 most common ways enemies try to breach the fortress
- **Prevention Measures:** Like specific defensive strategies for each attack method
- **Testing:** Like regular security drills to ensure defenses are working
- **Monitoring:** Like having guards and cameras to detect and respond to threats

## 18.6 Security Testing

Security testing is the process of identifying vulnerabilities and security weaknesses in Java applications through various testing methodologies.

### Core Concepts:

**1. Types of Security Testing:**
- Static Application Security Testing (SAST)
- Dynamic Application Security Testing (DAST)
- Interactive Application Security Testing (IAST)
- Penetration Testing
- Vulnerability Assessment

**2. Security Testing Tools:**
- OWASP ZAP
- Burp Suite
- SonarQube
- Checkmarx
- Veracode

**3. Testing Methodologies:**
- Black Box Testing
- White Box Testing
- Gray Box Testing
- Automated Testing
- Manual Testing

### Example:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
public class SecurityTestingExample {
    
    private MockMvc mockMvc;
    
    @BeforeEach
    void setUp(WebApplicationContext webApplicationContext) {
        this.mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext).build();
    }
    
    // Test for SQL Injection
    @Test
    public void testSqlInjectionPrevention() throws Exception {
        String maliciousInput = "'; DROP TABLE users; --";
        
        mockMvc.perform(get("/api/users/search")
                .param("name", maliciousInput))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray());
    }
    
    // Test for XSS Prevention
    @Test
    public void testXssPrevention() throws Exception {
        String maliciousScript = "<script>alert('XSS')</script>";
        
        mockMvc.perform(post("/api/users")
                .contentType("application/json")
                .content("{\"name\":\"" + maliciousScript + "\",\"email\":\"test@example.com\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value(not(containsString("<script>"))));
    }
    
    // Test for Authentication Bypass
    @Test
    public void testAuthenticationRequired() throws Exception {
        mockMvc.perform(get("/api/admin/users"))
                .andExpect(status().isUnauthorized());
    }
    
    // Test for Authorization
    @Test
    public void testAuthorization() throws Exception {
        String validToken = "valid-jwt-token";
        
        mockMvc.perform(get("/api/admin/users")
                .header("Authorization", "Bearer " + validToken))
                .andExpect(status().isOk());
    }
    
    // Test for CSRF Protection
    @Test
    public void testCsrfProtection() throws Exception {
        mockMvc.perform(post("/api/users")
                .contentType("application/json")
                .content("{\"name\":\"test\",\"email\":\"test@example.com\"}"))
                .andExpect(status().isForbidden());
    }
    
    // Test for Input Validation
    @Test
    public void testInputValidation() throws Exception {
        mockMvc.perform(post("/api/users")
                .contentType("application/json")
                .content("{\"name\":\"\",\"email\":\"invalid-email\"}"))
                .andExpect(status().isBadRequest());
    }
    
    // Test for Rate Limiting
    @Test
    public void testRateLimiting() throws Exception {
        for (int i = 0; i < 100; i++) {
            mockMvc.perform(get("/api/public/data"));
        }
        
        mockMvc.perform(get("/api/public/data"))
                .andExpect(status().isTooManyRequests());
    }
}

// Security Test Utilities
public class SecurityTestUtils {
    
    public static String generateJwtToken(String username, List<String> roles) {
        // Generate JWT token for testing
        return "test-jwt-token";
    }
    
    public static String encodeHtml(String input) {
        return input.replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;")
                   .replace("\"", "&quot;")
                   .replace("'", "&#x27;");
    }
    
    public static boolean isSqlInjectionSafe(String input) {
        String[] dangerousPatterns = {
            "';", "--", "/*", "*/", "xp_", "sp_", "exec", "execute"
        };
        
        String lowerInput = input.toLowerCase();
        for (String pattern : dangerousPatterns) {
            if (lowerInput.contains(pattern)) {
                return false;
            }
        }
        return true;
    }
}
```

### Real-world Analogy:
Security testing is like conducting a security audit of a building:
- **SAST:** Like checking the blueprints for security flaws before construction
- **DAST:** Like testing the actual building's security systems
- **Penetration Testing:** Like hiring ethical hackers to try to break in
- **Vulnerability Assessment:** Like having security experts inspect every corner

## 18.7 Compliance & Regulations

Compliance and regulations ensure that Java applications meet legal and industry requirements for data protection, privacy, and security.

### Core Concepts:

**1. Major Regulations:**
- GDPR (General Data Protection Regulation)
- CCPA (California Consumer Privacy Act)
- HIPAA (Health Insurance Portability and Accountability Act)
- SOX (Sarbanes-Oxley Act)
- PCI DSS (Payment Card Industry Data Security Standard)

**2. Compliance Requirements:**
- Data Protection
- Privacy by Design
- Right to be Forgotten
- Data Portability
- Consent Management
- Audit Trails

**3. Implementation Strategies:**
- Data Classification
- Access Controls
- Encryption
- Monitoring
- Documentation

### Example:

```java
import java.time.LocalDateTime;
import java.util.List;
import java.util.ArrayList;
import javax.persistence.*;
import javax.validation.constraints.NotNull;

// GDPR Compliance Example
@Entity
@Table(name = "user_data")
public class UserData {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Column(name = "user_id")
    private Long userId;
    
    @NotNull
    @Column(name = "data_type")
    @Enumerated(EnumType.STRING)
    private DataType dataType;
    
    @NotNull
    @Column(name = "sensitive_data")
    private String sensitiveData;
    
    @Column(name = "encryption_key_id")
    private String encryptionKeyId;
    
    @NotNull
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @Column(name = "deleted_at")
    private LocalDateTime deletedAt;
    
    @Column(name = "retention_until")
    private LocalDateTime retentionUntil;
    
    // Getters and setters
}

enum DataType {
    PERSONAL_IDENTIFIABLE_INFORMATION,
    FINANCIAL_DATA,
    HEALTH_DATA,
    BIOMETRIC_DATA,
    LOCATION_DATA
}

// GDPR Service
@Service
public class GDPRComplianceService {
    
    @Autowired
    private UserDataRepository userDataRepository;
    
    @Autowired
    private EncryptionService encryptionService;
    
    @Autowired
    private AuditService auditService;
    
    // Right to be Forgotten (Article 17)
    public void deleteUserData(Long userId) {
        List<UserData> userDataList = userDataRepository.findByUserId(userId);
        
        for (UserData userData : userDataList) {
            // Soft delete for audit purposes
            userData.setDeletedAt(LocalDateTime.now());
            userDataRepository.save(userData);
            
            // Log the deletion
            auditService.logDataDeletion(userId, userData.getDataType());
        }
    }
    
    // Data Portability (Article 20)
    public String exportUserData(Long userId) {
        List<UserData> userDataList = userDataRepository.findByUserId(userId);
        
        StringBuilder exportData = new StringBuilder();
        exportData.append("{\n");
        exportData.append("  \"userId\": ").append(userId).append(",\n");
        exportData.append("  \"exportDate\": \"").append(LocalDateTime.now()).append("\",\n");
        exportData.append("  \"data\": [\n");
        
        for (int i = 0; i < userDataList.size(); i++) {
            UserData userData = userDataList.get(i);
            exportData.append("    {\n");
            exportData.append("      \"type\": \"").append(userData.getDataType()).append("\",\n");
            exportData.append("      \"data\": \"").append(decryptData(userData)).append("\",\n");
            exportData.append("      \"createdAt\": \"").append(userData.getCreatedAt()).append("\"\n");
            exportData.append("    }");
            
            if (i < userDataList.size() - 1) {
                exportData.append(",");
            }
            exportData.append("\n");
        }
        
        exportData.append("  ]\n");
        exportData.append("}\n");
        
        return exportData.toString();
    }
    
    // Consent Management
    public void recordConsent(Long userId, String purpose, boolean granted) {
        ConsentRecord consent = new ConsentRecord();
        consent.setUserId(userId);
        consent.setPurpose(purpose);
        consent.setGranted(granted);
        consent.setTimestamp(LocalDateTime.now());
        consent.setIpAddress(getCurrentIpAddress());
        
        consentRepository.save(consent);
        
        auditService.logConsentChange(userId, purpose, granted);
    }
    
    // Data Minimization
    public void minimizeData(Long userId, List<DataType> allowedTypes) {
        List<UserData> userDataList = userDataRepository.findByUserId(userId);
        
        for (UserData userData : userDataList) {
            if (!allowedTypes.contains(userData.getDataType())) {
                userData.setDeletedAt(LocalDateTime.now());
                userDataRepository.save(userData);
            }
        }
    }
    
    // Data Retention
    public void enforceDataRetention() {
        LocalDateTime cutoffDate = LocalDateTime.now().minusYears(7); // 7-year retention
        
        List<UserData> expiredData = userDataRepository.findByRetentionUntilBefore(cutoffDate);
        
        for (UserData userData : expiredData) {
            userData.setDeletedAt(LocalDateTime.now());
            userDataRepository.save(userData);
            
            auditService.logDataRetentionDeletion(userData.getUserId(), userData.getDataType());
        }
    }
    
    private String decryptData(UserData userData) {
        return encryptionService.decrypt(userData.getSensitiveData(), userData.getEncryptionKeyId());
    }
    
    private String getCurrentIpAddress() {
        // Implementation to get current IP address
        return "127.0.0.1";
    }
}

// PCI DSS Compliance Example
@Entity
@Table(name = "payment_data")
public class PaymentData {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @NotNull
    @Column(name = "user_id")
    private Long userId;
    
    @NotNull
    @Column(name = "encrypted_card_number")
    private String encryptedCardNumber;
    
    @NotNull
    @Column(name = "encrypted_cvv")
    private String encryptedCvv;
    
    @NotNull
    @Column(name = "expiry_month")
    private Integer expiryMonth;
    
    @NotNull
    @Column(name = "expiry_year")
    private Integer expiryYear;
    
    @NotNull
    @Column(name = "cardholder_name")
    private String cardholderName;
    
    @NotNull
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    // Getters and setters
}

@Service
public class PCIDSSComplianceService {
    
    @Autowired
    private PaymentDataRepository paymentDataRepository;
    
    @Autowired
    private EncryptionService encryptionService;
    
    // Store payment data securely
    public void storePaymentData(Long userId, String cardNumber, String cvv, 
                                Integer expiryMonth, Integer expiryYear, String cardholderName) {
        PaymentData paymentData = new PaymentData();
        paymentData.setUserId(userId);
        paymentData.setEncryptedCardNumber(encryptionService.encrypt(cardNumber));
        paymentData.setEncryptedCvv(encryptionService.encrypt(cvv));
        paymentData.setExpiryMonth(expiryMonth);
        paymentData.setExpiryYear(expiryYear);
        paymentData.setCardholderName(cardholderName);
        paymentData.setCreatedAt(LocalDateTime.now());
        
        paymentDataRepository.save(paymentData);
        
        // Log the storage
        auditService.logPaymentDataStorage(userId);
    }
    
    // Mask card number for display
    public String getMaskedCardNumber(Long paymentDataId) {
        PaymentData paymentData = paymentDataRepository.findById(paymentDataId).orElse(null);
        if (paymentData == null) {
            return null;
        }
        
        String decryptedCardNumber = encryptionService.decrypt(paymentData.getEncryptedCardNumber());
        return maskCardNumber(decryptedCardNumber);
    }
    
    private String maskCardNumber(String cardNumber) {
        if (cardNumber.length() < 4) {
            return "****";
        }
        
        String lastFour = cardNumber.substring(cardNumber.length() - 4);
        return "****-****-****-" + lastFour;
    }
}
```

### Real-world Analogy:
Compliance and regulations are like building codes for software:
- **GDPR:** Like privacy regulations for buildings (who can see what, when data must be deleted)
- **PCI DSS:** Like security standards for banks (how to protect financial data)
- **HIPAA:** Like medical privacy laws (how to protect health information)
- **Audit Trails:** Like security cameras that record who did what and when