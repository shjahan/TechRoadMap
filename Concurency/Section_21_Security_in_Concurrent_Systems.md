# Section 21 – Security in Concurrent Systems

## 21.1 Thread Safety and Security

Thread safety in concurrent systems is crucial for maintaining security, as race conditions and data races can lead to security vulnerabilities and data breaches.

### Key Concepts
- **Race Conditions**: When multiple threads access shared resources without proper synchronization
- **Data Races**: Concurrent access to shared data without proper protection
- **Atomic Operations**: Operations that complete without interruption
- **Memory Barriers**: Ensuring proper ordering of memory operations

### Real-World Analogy
Think of a bank vault with multiple security guards. If the guards don't coordinate properly, they might accidentally leave the vault unlocked or allow unauthorized access. Thread safety is like having proper protocols that ensure only authorized access and prevent security breaches.

### Java Example
```java
// Secure counter with proper synchronization
public class SecureCounter {
    private final AtomicInteger count = new AtomicInteger(0);
    private final Object lock = new Object();
    private volatile boolean isLocked = false;
    
    public void increment() {
        // Use atomic operation for thread safety
        count.incrementAndGet();
    }
    
    public int getCount() {
        return count.get();
    }
    
    // Secure method with additional validation
    public boolean secureIncrement(int maxValue) {
        synchronized (lock) {
            if (isLocked) {
                throw new SecurityException("Counter is locked");
            }
            
            int currentValue = count.get();
            if (currentValue >= maxValue) {
                return false; // Prevent overflow
            }
            
            count.incrementAndGet();
            return true;
        }
    }
    
    public void lock() {
        synchronized (lock) {
            isLocked = true;
        }
    }
    
    public void unlock() {
        synchronized (lock) {
            isLocked = false;
        }
    }
}

// Secure user session management
public class SecureSessionManager {
    private final Map<String, UserSession> sessions = new ConcurrentHashMap<>();
    private final Map<String, Long> sessionTimestamps = new ConcurrentHashMap<>();
    private final long sessionTimeout = 30 * 60 * 1000; // 30 minutes
    
    public String createSession(User user) {
        String sessionId = generateSecureSessionId();
        UserSession session = new UserSession(user, sessionId);
        
        // Store session securely
        sessions.put(sessionId, session);
        sessionTimestamps.put(sessionId, System.currentTimeMillis());
        
        return sessionId;
    }
    
    public UserSession getSession(String sessionId) {
        // Check if session exists and is not expired
        if (!sessions.containsKey(sessionId)) {
            throw new SecurityException("Invalid session");
        }
        
        Long timestamp = sessionTimestamps.get(sessionId);
        if (timestamp == null || System.currentTimeMillis() - timestamp > sessionTimeout) {
            // Session expired, remove it
            sessions.remove(sessionId);
            sessionTimestamps.remove(sessionId);
            throw new SecurityException("Session expired");
        }
        
        // Update last access time
        sessionTimestamps.put(sessionId, System.currentTimeMillis());
        
        return sessions.get(sessionId);
    }
    
    private String generateSecureSessionId() {
        // Use cryptographically secure random number generator
        SecureRandom random = new SecureRandom();
        byte[] bytes = new byte[32];
        random.nextBytes(bytes);
        return Base64.getEncoder().encodeToString(bytes);
    }
}
```

## 21.2 Race Conditions in Security

Race conditions in security-critical code can lead to serious vulnerabilities, including privilege escalation and data corruption.

### Key Concepts
- **Time-of-Check-Time-of-Use**: Vulnerabilities where state changes between check and use
- **Double-Free**: Memory corruption from freeing the same memory twice
- **Use-After-Free**: Accessing memory after it has been freed
- **Integer Overflow**: Arithmetic operations that exceed maximum values

### Real-World Analogy
Think of a security checkpoint where guards check IDs and then allow entry. If there's a race condition, someone might change their ID between the check and entry, or multiple people might pass through with the same valid ID.

### Java Example
```java
// Vulnerable authentication system (demonstrates race condition)
public class VulnerableAuthSystem {
    private final Map<String, String> userPasswords = new ConcurrentHashMap<>();
    private final Map<String, Integer> loginAttempts = new ConcurrentHashMap<>();
    private final int maxAttempts = 3;
    
    // VULNERABLE: Race condition in password reset
    public boolean resetPassword(String username, String newPassword) {
        // Check if user exists
        if (!userPasswords.containsKey(username)) {
            return false;
        }
        
        // Check login attempts (vulnerable to race condition)
        Integer attempts = loginAttempts.get(username);
        if (attempts != null && attempts >= maxAttempts) {
            return false; // Account locked
        }
        
        // Simulate some processing time
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Update password (race condition here!)
        userPasswords.put(username, hashPassword(newPassword));
        loginAttempts.remove(username); // Reset attempts
        
        return true;
    }
    
    // SECURE: Fixed version with proper synchronization
    public boolean resetPasswordSecure(String username, String newPassword) {
        synchronized (this) {
            // Check if user exists
            if (!userPasswords.containsKey(username)) {
                return false;
            }
            
            // Check login attempts atomically
            Integer attempts = loginAttempts.get(username);
            if (attempts != null && attempts >= maxAttempts) {
                return false; // Account locked
            }
            
            // Update password atomically
            userPasswords.put(username, hashPassword(newPassword));
            loginAttempts.remove(username); // Reset attempts
            
            return true;
        }
    }
    
    // Secure login with rate limiting
    public boolean login(String username, String password) {
        synchronized (this) {
            // Check login attempts first
            Integer attempts = loginAttempts.get(username);
            if (attempts != null && attempts >= maxAttempts) {
                return false; // Account locked
            }
            
            // Verify password
            String storedPassword = userPasswords.get(username);
            if (storedPassword == null || !verifyPassword(password, storedPassword)) {
                // Increment failed attempts
                loginAttempts.merge(username, 1, Integer::sum);
                return false;
            }
            
            // Successful login, reset attempts
            loginAttempts.remove(username);
            return true;
        }
    }
    
    private String hashPassword(String password) {
        // Use secure password hashing
        return BCrypt.hashpw(password, BCrypt.gensalt());
    }
    
    private boolean verifyPassword(String password, String hash) {
        return BCrypt.checkpw(password, hash);
    }
}
```

## 21.3 Side-Channel Attacks

Side-channel attacks exploit information leaked through timing, power consumption, or other physical characteristics of a system.

### Key Concepts
- **Timing Attacks**: Exploiting differences in execution time
- **Power Analysis**: Analyzing power consumption patterns
- **Cache Attacks**: Exploiting cache behavior to extract information
- **Electromagnetic Attacks**: Analyzing electromagnetic emissions

### Real-World Analogy
Think of a safe with a combination lock. Even if you can't see the combination, you might be able to determine it by listening to the clicks, feeling the resistance, or timing how long it takes to turn each number. Side-channel attacks work similarly by observing unintended information leaks.

### Java Example
```java
// Vulnerable string comparison (timing attack)
public class VulnerableStringComparison {
    // VULNERABLE: Timing attack possible
    public boolean comparePasswords(String input, String stored) {
        if (input.length() != stored.length()) {
            return false;
        }
        
        for (int i = 0; i < input.length(); i++) {
            if (input.charAt(i) != stored.charAt(i)) {
                return false; // Early return reveals position of first difference
            }
        }
        
        return true;
    }
    
    // SECURE: Constant-time comparison
    public boolean comparePasswordsSecure(String input, String stored) {
        if (input.length() != stored.length()) {
            return false;
        }
        
        int result = 0;
        for (int i = 0; i < input.length(); i++) {
            result |= input.charAt(i) ^ stored.charAt(i);
        }
        
        return result == 0;
    }
}

// Secure random number generation
public class SecureRandomGenerator {
    private final SecureRandom secureRandom;
    
    public SecureRandomGenerator() {
        try {
            // Use cryptographically secure random number generator
            this.secureRandom = SecureRandom.getInstanceStrong();
        } catch (NoSuchAlgorithmException e) {
            throw new SecurityException("Secure random not available", e);
        }
    }
    
    public byte[] generateRandomBytes(int length) {
        byte[] bytes = new byte[length];
        secureRandom.nextBytes(bytes);
        return bytes;
    }
    
    public String generateSecureToken(int length) {
        byte[] bytes = generateRandomBytes(length);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }
    
    // Generate secure session ID
    public String generateSessionId() {
        return generateSecureToken(32);
    }
}

// Protection against cache attacks
public class CacheAttackProtection {
    private final Map<String, String> sensitiveData = new ConcurrentHashMap<>();
    private final SecureRandom random = new SecureRandom();
    
    public void storeSensitiveData(String key, String data) {
        // Add random padding to prevent cache-based attacks
        String paddedData = addRandomPadding(data);
        sensitiveData.put(key, paddedData);
    }
    
    public String retrieveSensitiveData(String key) {
        String paddedData = sensitiveData.get(key);
        if (paddedData == null) {
            return null;
        }
        
        // Remove padding
        return removePadding(paddedData);
    }
    
    private String addRandomPadding(String data) {
        // Add random padding to make data access patterns unpredictable
        int paddingLength = random.nextInt(100) + 50; // 50-149 bytes
        byte[] padding = new byte[paddingLength];
        random.nextBytes(padding);
        
        return data + Base64.getEncoder().encodeToString(padding);
    }
    
    private String removePadding(String paddedData) {
        // Remove padding (simplified - in practice, you'd need to track padding length)
        int dataLength = paddedData.length() - 100; // Assume average padding
        return paddedData.substring(0, Math.max(0, dataLength));
    }
}
```

## 21.4 Timing Attacks

Timing attacks exploit differences in execution time to extract sensitive information, particularly in cryptographic operations.

### Key Concepts
- **Constant-Time Algorithms**: Algorithms that take the same time regardless of input
- **Timing Analysis**: Measuring execution time to infer information
- **Countermeasures**: Techniques to prevent timing attacks
- **Statistical Analysis**: Using multiple measurements to improve accuracy

### Real-World Analogy
Think of a combination lock where each number takes a different amount of time to turn. An attacker could time how long it takes to turn each number and use this information to determine the combination. Timing attacks work similarly by measuring how long operations take.

### Java Example
```java
// Timing attack demonstration and protection
public class TimingAttackProtection {
    private final Map<String, String> userTokens = new ConcurrentHashMap<>();
    private final SecureRandom random = new SecureRandom();
    
    // VULNERABLE: Timing attack possible
    public boolean verifyTokenVulnerable(String username, String token) {
        String storedToken = userTokens.get(username);
        if (storedToken == null) {
            return false; // Early return - different timing
        }
        
        return storedToken.equals(token); // Timing depends on token similarity
    }
    
    // SECURE: Constant-time verification
    public boolean verifyTokenSecure(String username, String token) {
        String storedToken = userTokens.get(username);
        if (storedToken == null) {
            // Simulate processing time even for non-existent users
            simulateProcessingTime();
            return false;
        }
        
        // Constant-time comparison
        return constantTimeEquals(storedToken, token);
    }
    
    private boolean constantTimeEquals(String a, String b) {
        if (a.length() != b.length()) {
            // Still need to simulate processing time
            simulateProcessingTime();
            return false;
        }
        
        int result = 0;
        for (int i = 0; i < a.length(); i++) {
            result |= a.charAt(i) ^ b.charAt(i);
        }
        
        // Simulate processing time regardless of result
        simulateProcessingTime();
        
        return result == 0;
    }
    
    private void simulateProcessingTime() {
        // Add random delay to prevent timing attacks
        try {
            Thread.sleep(random.nextInt(10) + 5); // 5-14ms delay
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Secure password verification
    public boolean verifyPasswordSecure(String password, String hash) {
        // Use constant-time comparison
        String computedHash = BCrypt.hashpw(password, hash);
        return constantTimeEquals(computedHash, hash);
    }
    
    // Secure HMAC verification
    public boolean verifyHMAC(byte[] data, byte[] signature, byte[] key) {
        try {
            Mac mac = Mac.getInstance("HmacSHA256");
            SecretKeySpec keySpec = new SecretKeySpec(key, "HmacSHA256");
            mac.init(keySpec);
            
            byte[] computedSignature = mac.doFinal(data);
            
            // Constant-time comparison
            return constantTimeEquals(computedSignature, signature);
            
        } catch (Exception e) {
            throw new SecurityException("HMAC verification failed", e);
        }
    }
    
    private boolean constantTimeEquals(byte[] a, byte[] b) {
        if (a.length != b.length) {
            simulateProcessingTime();
            return false;
        }
        
        int result = 0;
        for (int i = 0; i < a.length; i++) {
            result |= a[i] ^ b[i];
        }
        
        simulateProcessingTime();
        return result == 0;
    }
}
```

## 21.5 Cache Attacks

Cache attacks exploit shared caches to extract sensitive information from other processes or virtual machines.

### Key Concepts
- **Cache Side-Channels**: Using cache behavior to infer information
- **Flush+Reload**: Flushing cache lines and monitoring reloads
- **Prime+Probe**: Priming cache sets and probing for changes
- **Spectre/Meltdown**: CPU vulnerabilities exploiting speculative execution

### Real-World Analogy
Think of a shared library where different people can see which books are checked out. Even if you can't read the books directly, you can infer information about what someone is reading by observing which books are missing from the shelves.

### Java Example
```java
// Cache attack protection
public class CacheAttackProtection {
    private final Map<String, byte[]> sensitiveData = new ConcurrentHashMap<>();
    private final SecureRandom random = new SecureRandom();
    
    // Protection against cache-based attacks
    public void storeSensitiveData(String key, byte[] data) {
        // Add random padding to prevent cache-based attacks
        byte[] paddedData = addRandomPadding(data);
        sensitiveData.put(key, paddedData);
    }
    
    public byte[] retrieveSensitiveData(String key) {
        byte[] paddedData = sensitiveData.get(key);
        if (paddedData == null) {
            return null;
        }
        
        // Remove padding
        return removePadding(paddedData);
    }
    
    private byte[] addRandomPadding(byte[] data) {
        // Add random padding to make data access patterns unpredictable
        int paddingLength = random.nextInt(1000) + 500; // 500-1499 bytes
        byte[] padding = new byte[paddingLength];
        random.nextBytes(padding);
        
        // Combine data and padding
        byte[] result = new byte[data.length + padding.length];
        System.arraycopy(data, 0, result, 0, data.length);
        System.arraycopy(padding, 0, result, data.length, padding.length);
        
        return result;
    }
    
    private byte[] removePadding(byte[] paddedData) {
        // Remove padding (simplified - in practice, you'd need to track padding length)
        int dataLength = paddedData.length - 1000; // Assume average padding
        if (dataLength <= 0) {
            return new byte[0];
        }
        
        byte[] result = new byte[dataLength];
        System.arraycopy(paddedData, 0, result, 0, dataLength);
        return result;
    }
    
    // Secure memory access
    public void secureMemoryAccess(byte[] data) {
        // Access memory in a way that doesn't reveal access patterns
        for (int i = 0; i < data.length; i++) {
            // Access all elements to prevent cache-based attacks
            byte value = data[i];
            // Perform some operation to prevent optimization
            if (value == 0) {
                // Do nothing, but prevent compiler optimization
            }
        }
    }
    
    // Protection against Spectre/Meltdown
    public void protectAgainstSpeculativeExecution() {
        // Use memory barriers to prevent speculative execution
        // This is a simplified example - real protection requires hardware support
        System.gc(); // Force garbage collection
        Thread.yield(); // Yield to other threads
    }
}
```

## 21.6 Spectre and Meltdown

Spectre and Meltdown are CPU vulnerabilities that exploit speculative execution to access sensitive data.

### Key Concepts
- **Speculative Execution**: CPU feature that executes instructions before knowing if they're needed
- **Branch Prediction**: CPU mechanism for predicting which code path to take
- **Cache Flushing**: Technique to clear sensitive data from cache
- **Mitigation Techniques**: Software and hardware countermeasures

### Real-World Analogy
Think of a security guard who sometimes opens doors before checking if the person has permission, then closes them if they don't. Even though the door is closed, the person might have seen what's inside. Spectre and Meltdown work similarly by exploiting the CPU's speculative execution.

### Java Example
```java
// Spectre/Meltdown protection
public class SpectreMeltdownProtection {
    private final Map<String, byte[]> sensitiveData = new ConcurrentHashMap<>();
    private final SecureRandom random = new SecureRandom();
    
    // Protection against speculative execution attacks
    public void storeSensitiveData(String key, byte[] data) {
        // Encrypt sensitive data
        byte[] encryptedData = encryptData(data);
        sensitiveData.put(key, encryptedData);
    }
    
    public byte[] retrieveSensitiveData(String key) {
        byte[] encryptedData = sensitiveData.get(key);
        if (encryptedData == null) {
            return null;
        }
        
        // Decrypt data
        return decryptData(encryptedData);
    }
    
    private byte[] encryptData(byte[] data) {
        try {
            // Use AES encryption
            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
            SecretKey key = generateSecretKey();
            cipher.init(Cipher.ENCRYPT_MODE, key);
            
            byte[] encryptedData = cipher.doFinal(data);
            
            // Combine IV and encrypted data
            byte[] iv = cipher.getIV();
            byte[] result = new byte[iv.length + encryptedData.length];
            System.arraycopy(iv, 0, result, 0, iv.length);
            System.arraycopy(encryptedData, 0, result, iv.length, encryptedData.length);
            
            return result;
            
        } catch (Exception e) {
            throw new SecurityException("Encryption failed", e);
        }
    }
    
    private byte[] decryptData(byte[] encryptedData) {
        try {
            // Extract IV and encrypted data
            byte[] iv = new byte[12]; // GCM IV is typically 12 bytes
            byte[] data = new byte[encryptedData.length - iv.length];
            System.arraycopy(encryptedData, 0, iv, 0, iv.length);
            System.arraycopy(encryptedData, iv.length, data, 0, data.length);
            
            // Decrypt data
            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
            SecretKey key = generateSecretKey();
            GCMParameterSpec spec = new GCMParameterSpec(128, iv);
            cipher.init(Cipher.DECRYPT_MODE, key, spec);
            
            return cipher.doFinal(data);
            
        } catch (Exception e) {
            throw new SecurityException("Decryption failed", e);
        }
    }
    
    private SecretKey generateSecretKey() {
        // Generate secret key (in practice, this should be stored securely)
        byte[] keyBytes = new byte[32]; // 256 bits
        random.nextBytes(keyBytes);
        return new SecretKeySpec(keyBytes, "AES");
    }
    
    // Protection against cache-based attacks
    public void protectCacheAccess() {
        // Clear sensitive data from cache
        System.gc(); // Force garbage collection
        System.runFinalization(); // Run finalizers
        
        // Add random delay to prevent timing attacks
        try {
            Thread.sleep(random.nextInt(10) + 5);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Secure memory access
    public void secureMemoryAccess(byte[] data) {
        // Access memory in a way that doesn't reveal access patterns
        for (int i = 0; i < data.length; i++) {
            // Access all elements to prevent cache-based attacks
            byte value = data[i];
            // Perform some operation to prevent optimization
            if (value == 0) {
                // Do nothing, but prevent compiler optimization
            }
        }
    }
}
```

## 21.7 Secure Coding Practices

Secure coding practices help prevent vulnerabilities in concurrent systems by following established security guidelines.

### Key Concepts
- **Input Validation**: Validating all inputs to prevent injection attacks
- **Output Encoding**: Encoding outputs to prevent XSS attacks
- **Error Handling**: Proper error handling without information leakage
- **Resource Management**: Proper cleanup of resources

### Real-World Analogy
Think of building a secure house. You need strong locks (input validation), secure windows (output encoding), proper alarm systems (error handling), and regular maintenance (resource management). Each security measure works together to protect the entire system.

### Java Example
```java
// Secure coding practices
public class SecureCodingPractices {
    private final Map<String, User> users = new ConcurrentHashMap<>();
    private final Map<String, String> sessions = new ConcurrentHashMap<>();
    private final SecureRandom random = new SecureRandom();
    
    // Input validation
    public boolean validateInput(String input) {
        if (input == null || input.isEmpty()) {
            return false;
        }
        
        // Check for malicious patterns
        if (input.contains("<script>") || input.contains("javascript:")) {
            return false;
        }
        
        // Check length
        if (input.length() > 1000) {
            return false;
        }
        
        // Check for SQL injection patterns
        if (input.matches(".*('|(\\-\\-)|(;)|(\\|\\|)).*")) {
            return false;
        }
        
        return true;
    }
    
    // Output encoding
    public String encodeOutput(String input) {
        if (input == null) {
            return "";
        }
        
        // HTML encoding
        return input.replace("&", "&amp;")
                   .replace("<", "&lt;")
                   .replace(">", "&gt;")
                   .replace("\"", "&quot;")
                   .replace("'", "&#x27;");
    }
    
    // Secure error handling
    public void handleError(Exception e, String operation) {
        // Log error securely
        System.err.println("Error in " + operation + ": " + e.getMessage());
        
        // Don't expose sensitive information
        // Don't log stack traces in production
        if (System.getProperty("debug") != null) {
            e.printStackTrace();
        }
        
        // Return generic error message to user
        throw new SecurityException("Operation failed");
    }
    
    // Secure resource management
    public void secureResourceManagement() {
        try (FileInputStream fis = new FileInputStream("config.properties");
             BufferedReader reader = new BufferedReader(new InputStreamReader(fis))) {
            
            // Process file
            String line;
            while ((line = reader.readLine()) != null) {
                processLine(line);
            }
            
        } catch (IOException e) {
            handleError(e, "file processing");
        }
    }
    
    // Secure session management
    public String createSecureSession(User user) {
        // Generate secure session ID
        String sessionId = generateSecureSessionId();
        
        // Store session securely
        sessions.put(sessionId, user.getId());
        
        // Set session timeout
        scheduleSessionTimeout(sessionId);
        
        return sessionId;
    }
    
    public User getSessionUser(String sessionId) {
        if (!validateSessionId(sessionId)) {
            throw new SecurityException("Invalid session ID");
        }
        
        String userId = sessions.get(sessionId);
        if (userId == null) {
            throw new SecurityException("Session not found");
        }
        
        User user = users.get(userId);
        if (user == null) {
            throw new SecurityException("User not found");
        }
        
        return user;
    }
    
    private String generateSecureSessionId() {
        byte[] bytes = new byte[32];
        random.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }
    
    private boolean validateSessionId(String sessionId) {
        if (sessionId == null || sessionId.isEmpty()) {
            return false;
        }
        
        // Check format
        if (!sessionId.matches("^[A-Za-z0-9_-]+$")) {
            return false;
        }
        
        // Check length
        if (sessionId.length() < 32 || sessionId.length() > 64) {
            return false;
        }
        
        return true;
    }
    
    private void scheduleSessionTimeout(String sessionId) {
        // Schedule session timeout (simplified)
        new Timer().schedule(new TimerTask() {
            @Override
            public void run() {
                sessions.remove(sessionId);
            }
        }, 30 * 60 * 1000); // 30 minutes
    }
    
    private void processLine(String line) {
        // Process configuration line
        if (line.startsWith("#") || line.trim().isEmpty()) {
            return; // Skip comments and empty lines
        }
        
        String[] parts = line.split("=", 2);
        if (parts.length == 2) {
            String key = parts[0].trim();
            String value = parts[1].trim();
            
            // Validate key and value
            if (validateInput(key) && validateInput(value)) {
                // Process configuration
                System.out.println("Config: " + key + " = " + value);
            }
        }
    }
}
```

## 21.8 Security Testing

Security testing ensures that concurrent systems are protected against various security threats and vulnerabilities.

### Key Concepts
- **Penetration Testing**: Simulating attacks to find vulnerabilities
- **Vulnerability Scanning**: Automated scanning for known vulnerabilities
- **Code Review**: Manual review of code for security issues
- **Security Auditing**: Comprehensive security assessment

### Real-World Analogy
Think of testing a bank's security by hiring ethical hackers to try to break in. They might try different approaches like social engineering, technical exploits, or physical security weaknesses. Security testing works similarly by systematically testing all possible attack vectors.

### Java Example
```java
// Security testing framework
public class SecurityTestingFramework {
    private final Map<String, String> testResults = new ConcurrentHashMap<>();
    private final List<SecurityTest> securityTests = new ArrayList<>();
    
    public SecurityTestingFramework() {
        initializeSecurityTests();
    }
    
    public void runSecurityTests() {
        System.out.println("Starting security tests...");
        
        for (SecurityTest test : securityTests) {
            try {
                boolean result = test.run();
                testResults.put(test.getName(), result ? "PASS" : "FAIL");
                System.out.println(test.getName() + ": " + (result ? "PASS" : "FAIL"));
            } catch (Exception e) {
                testResults.put(test.getName(), "ERROR: " + e.getMessage());
                System.out.println(test.getName() + ": ERROR - " + e.getMessage());
            }
        }
        
        printTestSummary();
    }
    
    private void initializeSecurityTests() {
        securityTests.add(new InputValidationTest());
        securityTests.add(new AuthenticationTest());
        securityTests.add(new AuthorizationTest());
        securityTests.add(new SessionManagementTest());
        securityTests.add(new DataProtectionTest());
        securityTests.add(new ErrorHandlingTest());
    }
    
    private void printTestSummary() {
        System.out.println("\nSecurity Test Summary:");
        System.out.println("=====================");
        
        int passCount = 0;
        int failCount = 0;
        int errorCount = 0;
        
        for (Map.Entry<String, String> entry : testResults.entrySet()) {
            String result = entry.getValue();
            if (result.equals("PASS")) {
                passCount++;
            } else if (result.equals("FAIL")) {
                failCount++;
            } else {
                errorCount++;
            }
            
            System.out.println(entry.getKey() + ": " + result);
        }
        
        System.out.println("\nTotal: " + (passCount + failCount + errorCount));
        System.out.println("Passed: " + passCount);
        System.out.println("Failed: " + failCount);
        System.out.println("Errors: " + errorCount);
    }
    
    // Security test interface
    public interface SecurityTest {
        String getName();
        boolean run() throws Exception;
    }
    
    // Input validation test
    public static class InputValidationTest implements SecurityTest {
        @Override
        public String getName() {
            return "Input Validation Test";
        }
        
        @Override
        public boolean run() throws Exception {
            // Test various malicious inputs
            String[] maliciousInputs = {
                "<script>alert('XSS')</script>",
                "'; DROP TABLE users; --",
                "../../../etc/passwd",
                "javascript:alert('XSS')",
                "<img src=x onerror=alert('XSS')>"
            };
            
            for (String input : maliciousInputs) {
                if (validateInput(input)) {
                    return false; // Should reject malicious input
                }
            }
            
            return true;
        }
        
        private boolean validateInput(String input) {
            // Simplified validation - in practice, use proper validation
            return input != null && !input.contains("<script>") && !input.contains("javascript:");
        }
    }
    
    // Authentication test
    public static class AuthenticationTest implements SecurityTest {
        @Override
        public String getName() {
            return "Authentication Test";
        }
        
        @Override
        public boolean run() throws Exception {
            // Test authentication mechanisms
            String username = "testuser";
            String password = "testpass";
            
            // Test valid login
            if (!authenticate(username, password)) {
                return false;
            }
            
            // Test invalid login
            if (authenticate(username, "wrongpass")) {
                return false;
            }
            
            // Test brute force protection
            for (int i = 0; i < 5; i++) {
                authenticate(username, "wrongpass");
            }
            
            // Should be locked after multiple failed attempts
            if (authenticate(username, password)) {
                return false; // Should be locked
            }
            
            return true;
        }
        
        private boolean authenticate(String username, String password) {
            // Simplified authentication - in practice, use proper authentication
            return "testuser".equals(username) && "testpass".equals(password);
        }
    }
    
    // Authorization test
    public static class AuthorizationTest implements SecurityTest {
        @Override
        public String getName() {
            return "Authorization Test";
        }
        
        @Override
        public boolean run() throws Exception {
            // Test authorization mechanisms
            String userRole = "user";
            String adminRole = "admin";
            
            // Test user access
            if (!hasAccess(userRole, "userResource")) {
                return false;
            }
            
            // Test admin access
            if (!hasAccess(adminRole, "adminResource")) {
                return false;
            }
            
            // Test unauthorized access
            if (hasAccess(userRole, "adminResource")) {
                return false; // User should not have admin access
            }
            
            return true;
        }
        
        private boolean hasAccess(String role, String resource) {
            // Simplified authorization - in practice, use proper authorization
            if ("admin".equals(role)) {
                return true; // Admin has access to everything
            } else if ("user".equals(role)) {
                return "userResource".equals(resource);
            }
            return false;
        }
    }
}
```

This comprehensive explanation covers all aspects of security in concurrent systems, providing both theoretical understanding and practical examples to illustrate each concept.