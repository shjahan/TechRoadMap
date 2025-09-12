# Section 8 – Database Security

## 8.1 Authentication and Authorization

Authentication verifies user identity, while authorization controls what authenticated users can access. Together, they form the foundation of database security.

### Authentication Methods:
- **Username/Password**: Traditional login credentials
- **Multi-Factor Authentication (MFA)**: Additional security layers
- **Certificate-Based**: Digital certificates for authentication
- **Single Sign-On (SSO)**: Centralized authentication system
- **Biometric**: Fingerprint, facial recognition, etc.

### Authorization Levels:
- **Database Level**: Access to entire database
- **Schema Level**: Access to specific schemas
- **Table Level**: Access to specific tables
- **Column Level**: Access to specific columns
- **Row Level**: Access to specific rows

### Real-World Analogy:
Authentication and authorization are like a secure building:
- **Authentication** = ID card verification at the entrance
- **Authorization** = Different access levels (lobby, office, executive floor)
- **MFA** = Additional security checks (fingerprint, PIN)
- **SSO** = One card works for all company buildings

### Java Example - Authentication and Authorization:
```java
import java.sql.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class DatabaseSecurity {
    private Connection connection;
    
    public DatabaseSecurity(Connection connection) {
        this.connection = connection;
    }
    
    // Authenticate user with password hashing
    public boolean authenticateUser(String username, String password) throws SQLException {
        String sql = "SELECT password_hash, salt FROM users WHERE username = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, username);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    String storedHash = rs.getString("password_hash");
                    String salt = rs.getString("salt");
                    String hashedPassword = hashPassword(password, salt);
                    
                    return storedHash.equals(hashedPassword);
                }
            }
        }
        return false;
    }
    
    // Hash password with salt
    private String hashPassword(String password, String salt) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        md.update(salt.getBytes());
        byte[] hashedPassword = md.digest(password.getBytes());
        
        StringBuilder sb = new StringBuilder();
        for (byte b : hashedPassword) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
    
    // Check user authorization for specific table
    public boolean checkTableAccess(String username, String tableName, String operation) throws SQLException {
        String sql = """
            SELECT COUNT(*) as access_count
            FROM user_permissions up
            JOIN permissions p ON up.permission_id = p.id
            WHERE up.username = ? 
            AND p.table_name = ? 
            AND p.operation = ?
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, username);
            stmt.setString(2, tableName);
            stmt.setString(3, operation);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("access_count") > 0;
                }
            }
        }
        return false;
    }
    
    // Create user with encrypted password
    public void createUser(String username, String password, String role) throws SQLException, NoSuchAlgorithmException {
        String salt = generateSalt();
        String hashedPassword = hashPassword(password, salt);
        
        String sql = "INSERT INTO users (username, password_hash, salt, role) VALUES (?, ?, ?, ?)";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, username);
            stmt.setString(2, hashedPassword);
            stmt.setString(3, salt);
            stmt.setString(4, role);
            stmt.executeUpdate();
            
            System.out.println("User created successfully: " + username);
        }
    }
    
    private String generateSalt() {
        return String.valueOf(System.currentTimeMillis());
    }
}
```

## 8.2 Role-Based Access Control (RBAC)

RBAC assigns permissions to roles rather than individual users, making security management more scalable and maintainable.

### RBAC Components:
- **Users**: Individuals who access the system
- **Roles**: Collections of permissions
- **Permissions**: Specific actions on resources
- **Resources**: Database objects (tables, columns, etc.)

### Real-World Analogy:
RBAC is like a company's organizational structure:
- **Users** = Employees
- **Roles** = Job titles (Manager, Developer, Analyst)
- **Permissions** = What each role can do
- **Resources** = Company assets and systems

### Java Example - RBAC Implementation:
```java
public class RBACManager {
    private Connection connection;
    
    public RBACManager(Connection connection) {
        this.connection = connection;
    }
    
    // Create role
    public void createRole(String roleName, String description) throws SQLException {
        String sql = "INSERT INTO roles (role_name, description) VALUES (?, ?)";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, roleName);
            stmt.setString(2, description);
            stmt.executeUpdate();
            
            System.out.println("Role created: " + roleName);
        }
    }
    
    // Assign role to user
    public void assignRoleToUser(String username, String roleName) throws SQLException {
        String sql = "INSERT INTO user_roles (username, role_name) VALUES (?, ?)";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, username);
            stmt.setString(2, roleName);
            stmt.executeUpdate();
            
            System.out.println("Role " + roleName + " assigned to user " + username);
        }
    }
    
    // Grant permission to role
    public void grantPermissionToRole(String roleName, String tableName, String operation) throws SQLException {
        String sql = "INSERT INTO role_permissions (role_name, table_name, operation) VALUES (?, ?, ?)";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, roleName);
            stmt.setString(2, tableName);
            stmt.setString(3, operation);
            stmt.executeUpdate();
            
            System.out.println("Permission granted: " + roleName + " can " + operation + " on " + tableName);
        }
    }
    
    // Check if user has permission through role
    public boolean hasPermission(String username, String tableName, String operation) throws SQLException {
        String sql = """
            SELECT COUNT(*) as permission_count
            FROM user_roles ur
            JOIN role_permissions rp ON ur.role_name = rp.role_name
            WHERE ur.username = ? 
            AND rp.table_name = ? 
            AND rp.operation = ?
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, username);
            stmt.setString(2, tableName);
            stmt.setString(3, operation);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("permission_count") > 0;
                }
            }
        }
        return false;
    }
    
    // Get user's roles
    public List<String> getUserRoles(String username) throws SQLException {
        List<String> roles = new ArrayList<>();
        String sql = "SELECT role_name FROM user_roles WHERE username = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, username);
            
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    roles.add(rs.getString("role_name"));
                }
            }
        }
        return roles;
    }
}
```

## 8.3 Data Encryption (At Rest and In Transit)

Data encryption protects sensitive information by converting it into an unreadable format that can only be decrypted with the proper key.

### Encryption Types:
- **Symmetric Encryption**: Same key for encryption and decryption
- **Asymmetric Encryption**: Different keys for encryption and decryption
- **Hashing**: One-way encryption (cannot be decrypted)
- **Transparent Data Encryption (TDE)**: Automatic encryption of data files

### Real-World Analogy:
Data encryption is like a secure safe:
- **Symmetric Encryption** = Same key to lock and unlock
- **Asymmetric Encryption** = Different keys for locking and unlocking
- **Hashing** = One-way lock (cannot be opened)
- **TDE** = Automatic safe for all valuables

### Java Example - Data Encryption:
```java
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.util.Base64;

public class DataEncryption {
    private SecretKey secretKey;
    
    public DataEncryption() throws Exception {
        generateSecretKey();
    }
    
    // Generate secret key
    private void generateSecretKey() throws Exception {
        KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
        keyGenerator.init(256);
        secretKey = keyGenerator.generateKey();
    }
    
    // Encrypt sensitive data
    public String encryptData(String plainText) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        
        byte[] encryptedBytes = cipher.doFinal(plainText.getBytes());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }
    
    // Decrypt sensitive data
    public String decryptData(String encryptedText) throws Exception {
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.DECRYPT_MODE, secretKey);
        
        byte[] encryptedBytes = Base64.getDecoder().decode(encryptedText);
        byte[] decryptedBytes = cipher.doFinal(encryptedBytes);
        return new String(decryptedBytes);
    }
    
    // Store encrypted data in database
    public void storeEncryptedData(String tableName, String columnName, String value) throws Exception {
        String encryptedValue = encryptData(value);
        
        String sql = "INSERT INTO " + tableName + " (" + columnName + ") VALUES (?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, encryptedValue);
            stmt.executeUpdate();
        }
    }
    
    // Retrieve and decrypt data from database
    public String retrieveDecryptedData(String tableName, String columnName, String condition) throws Exception {
        String sql = "SELECT " + columnName + " FROM " + tableName + " WHERE " + condition;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                String encryptedValue = rs.getString(columnName);
                return decryptData(encryptedValue);
            }
        }
        return null;
    }
    
    // Hash password (one-way encryption)
    public String hashPassword(String password) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] hashedPassword = md.digest(password.getBytes());
        
        StringBuilder sb = new StringBuilder();
        for (byte b : hashedPassword) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
```

## 8.4 Database Auditing

Database auditing tracks and logs all database activities to ensure compliance, security, and accountability.

### Audit Types:
- **Login Auditing**: Track user logins and logouts
- **Data Access Auditing**: Monitor data reads and writes
- **Schema Auditing**: Track DDL operations
- **Privilege Auditing**: Monitor permission changes
- **Failed Access Auditing**: Log unsuccessful access attempts

### Real-World Analogy:
Database auditing is like a security camera system:
- **Login Auditing** = Recording who enters the building
- **Data Access Auditing** = Recording what people do inside
- **Schema Auditing** = Recording building modifications
- **Privilege Auditing** = Recording key assignments
- **Failed Access Auditing** = Recording break-in attempts

### Java Example - Database Auditing:
```java
public class DatabaseAuditing {
    private Connection connection;
    
    public DatabaseAuditing(Connection connection) {
        this.connection = connection;
    }
    
    // Enable database auditing
    public void enableAuditing() throws SQLException {
        String[] auditCommands = {
            "SET GLOBAL general_log = 'ON'",
            "SET GLOBAL general_log_file = '/var/log/mysql/audit.log'",
            "SET GLOBAL log_output = 'FILE'"
        };
        
        for (String command : auditCommands) {
            try (Statement stmt = connection.createStatement()) {
                stmt.execute(command);
            }
        }
        
        System.out.println("Database auditing enabled");
    }
    
    // Log user activity
    public void logUserActivity(String username, String action, String tableName, String details) throws SQLException {
        String sql = """
            INSERT INTO audit_log (username, action, table_name, details, timestamp)
            VALUES (?, ?, ?, ?, NOW())
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, username);
            stmt.setString(2, action);
            stmt.setString(3, tableName);
            stmt.setString(4, details);
            stmt.executeUpdate();
        }
    }
    
    // Query audit log
    public void queryAuditLog(String username, String startDate, String endDate) throws SQLException {
        String sql = """
            SELECT username, action, table_name, details, timestamp
            FROM audit_log
            WHERE username = ? 
            AND timestamp BETWEEN ? AND ?
            ORDER BY timestamp DESC
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, username);
            stmt.setString(2, startDate);
            stmt.setString(3, endDate);
            
            try (ResultSet rs = stmt.executeQuery()) {
                System.out.println("Audit Log for " + username + ":");
                while (rs.next()) {
                    System.out.printf("Time: %s, Action: %s, Table: %s, Details: %s%n",
                        rs.getTimestamp("timestamp"),
                        rs.getString("action"),
                        rs.getString("table_name"),
                        rs.getString("details"));
                }
            }
        }
    }
    
    // Monitor failed login attempts
    public void monitorFailedLogins() throws SQLException {
        String sql = """
            SELECT username, COUNT(*) as failed_attempts
            FROM audit_log
            WHERE action = 'LOGIN_FAILED'
            AND timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR)
            GROUP BY username
            HAVING failed_attempts > 5
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Suspicious login activity:");
            while (rs.next()) {
                System.out.printf("User: %s, Failed attempts: %d%n",
                    rs.getString("username"),
                    rs.getInt("failed_attempts"));
            }
        }
    }
}
```

## 8.5 SQL Injection Prevention

SQL injection is a security vulnerability where malicious SQL code is inserted into input fields, potentially allowing unauthorized database access.

### SQL Injection Types:
- **Union-based**: Using UNION to extract data
- **Boolean-based**: Using boolean conditions to infer data
- **Time-based**: Using time delays to infer data
- **Error-based**: Using error messages to extract data

### Prevention Methods:
- **Prepared Statements**: Use parameterized queries
- **Input Validation**: Validate and sanitize input
- **Least Privilege**: Limit database user permissions
- **Input Escaping**: Escape special characters
- **Stored Procedures**: Use database procedures

### Real-World Analogy:
SQL injection is like a con artist tricking a security guard:
- **Malicious Input** = Fake credentials
- **Prepared Statements** = Proper ID verification
- **Input Validation** = Background checks
- **Least Privilege** = Limited access areas

### Java Example - SQL Injection Prevention:
```java
public class SQLInjectionPrevention {
    private Connection connection;
    
    public SQLInjectionPrevention(Connection connection) {
        this.connection = connection;
    }
    
    // VULNERABLE - Don't do this
    public void vulnerableQuery(String username) throws SQLException {
        String sql = "SELECT * FROM users WHERE username = '" + username + "'";
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            // This is vulnerable to SQL injection
            while (rs.next()) {
                System.out.println("User: " + rs.getString("username"));
            }
        }
    }
    
    // SECURE - Use prepared statements
    public void secureQuery(String username) throws SQLException {
        String sql = "SELECT * FROM users WHERE username = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, username);
            
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    System.out.println("User: " + rs.getString("username"));
                }
            }
        }
    }
    
    // Input validation
    public boolean isValidUsername(String username) {
        // Check for SQL injection patterns
        String[] dangerousPatterns = {
            "'", "\"", ";", "--", "/*", "*/", "xp_", "sp_", "exec", "execute"
        };
        
        for (String pattern : dangerousPatterns) {
            if (username.toLowerCase().contains(pattern.toLowerCase())) {
                return false;
            }
        }
        
        // Check length
        if (username.length() > 50) {
            return false;
        }
        
        // Check for alphanumeric characters only
        return username.matches("^[a-zA-Z0-9_]+$");
    }
    
    // Sanitize input
    public String sanitizeInput(String input) {
        if (input == null) {
            return null;
        }
        
        // Remove or escape dangerous characters
        return input.replace("'", "''")
                   .replace("\"", "\"\"")
                   .replace(";", "")
                   .replace("--", "")
                   .replace("/*", "")
                   .replace("*/", "");
    }
    
    // Use stored procedures
    public void secureStoredProcedure(String username) throws SQLException {
        String sql = "CALL GetUserByUsername(?)";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, username);
            
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    System.out.println("User: " + rs.getString("username"));
                }
            }
        }
    }
}
```

## 8.6 Data Masking and Anonymization

Data masking and anonymization protect sensitive data by replacing it with realistic but fake data, allowing safe testing and development.

### Masking Techniques:
- **Static Masking**: Replace data with fixed values
- **Dynamic Masking**: Replace data at query time
- **Tokenization**: Replace with tokens that can be reversed
- **Encryption**: Encrypt sensitive data
- **Hashing**: One-way transformation

### Real-World Analogy:
Data masking is like using a disguise:
- **Static Masking** = Wearing a permanent mask
- **Dynamic Masking** = Wearing a mask only when needed
- **Tokenization** = Using a code name
- **Encryption** = Using a secret language
- **Hashing** = Creating a fingerprint

### Java Example - Data Masking:
```java
public class DataMasking {
    private Connection connection;
    
    public DataMasking(Connection connection) {
        this.connection = connection;
    }
    
    // Static masking - replace with fixed values
    public void staticMasking() throws SQLException {
        String sql = """
            UPDATE students 
            SET email = 'masked@example.com',
                phone = '***-***-****',
                ssn = '***-**-****'
            WHERE student_id > 0
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.executeUpdate(sql);
            System.out.println("Static masking applied");
        }
    }
    
    // Dynamic masking - mask at query time
    public void dynamicMasking(String username) throws SQLException {
        String sql = "SELECT student_id, first_name, last_name, email FROM students WHERE student_id = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, username);
            
            try (ResultSet rs = stmt.executeQuery()) {
                while (rs.next()) {
                    String email = maskEmail(rs.getString("email"));
                    System.out.printf("ID: %s, Name: %s %s, Email: %s%n",
                        rs.getString("student_id"),
                        rs.getString("first_name"),
                        rs.getString("last_name"),
                        email);
                }
            }
        }
    }
    
    // Mask email address
    private String maskEmail(String email) {
        if (email == null || !email.contains("@")) {
            return email;
        }
        
        String[] parts = email.split("@");
        String username = parts[0];
        String domain = parts[1];
        
        if (username.length() <= 2) {
            return "**@" + domain;
        }
        
        String maskedUsername = username.charAt(0) + "*".repeat(username.length() - 2) + username.charAt(username.length() - 1);
        return maskedUsername + "@" + domain;
    }
    
    // Tokenization - replace with tokens
    public String tokenizeData(String data) {
        if (data == null) {
            return null;
        }
        
        // Generate token based on data hash
        String token = "TOKEN_" + Math.abs(data.hashCode());
        return token;
    }
    
    // Anonymize data
    public void anonymizeData() throws SQLException {
        String sql = """
            UPDATE students 
            SET first_name = CONCAT('User', student_id),
                last_name = 'Anonymous',
                email = CONCAT('user', student_id, '@anonymous.com'),
                phone = '***-***-****'
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.executeUpdate(sql);
            System.out.println("Data anonymized");
        }
    }
}
```

## 8.7 Compliance and Regulations

Database compliance ensures adherence to various regulations and standards that protect data privacy and security.

### Key Regulations:
- **GDPR**: General Data Protection Regulation (EU)
- **CCPA**: California Consumer Privacy Act
- **HIPAA**: Health Insurance Portability and Accountability Act
- **SOX**: Sarbanes-Oxley Act
- **PCI DSS**: Payment Card Industry Data Security Standard

### Real-World Analogy:
Compliance is like following building codes:
- **GDPR** = Privacy protection requirements
- **CCPA** = Consumer rights protection
- **HIPAA** = Medical information protection
- **SOX** = Financial reporting standards
- **PCI DSS** = Payment security standards

### Java Example - Compliance Implementation:
```java
public class ComplianceManager {
    private Connection connection;
    
    public ComplianceManager(Connection connection) {
        this.connection = connection;
    }
    
    // GDPR compliance - data subject rights
    public void handleDataSubjectRequest(String requestType, String userId) throws SQLException {
        switch (requestType) {
            case "ACCESS":
                provideDataAccess(userId);
                break;
            case "RECTIFICATION":
                enableDataRectification(userId);
                break;
            case "ERASURE":
                handleDataErasure(userId);
                break;
            case "PORTABILITY":
                provideDataPortability(userId);
                break;
            default:
                System.out.println("Unknown request type: " + requestType);
        }
    }
    
    // Provide data access (GDPR Article 15)
    private void provideDataAccess(String userId) throws SQLException {
        String sql = "SELECT * FROM user_data WHERE user_id = ?";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, userId);
            
            try (ResultSet rs = stmt.executeQuery()) {
                System.out.println("Data Access Report for User " + userId + ":");
                while (rs.next()) {
                    System.out.printf("Data: %s, Collected: %s, Purpose: %s%n",
                        rs.getString("data_type"),
                        rs.getTimestamp("collected_at"),
                        rs.getString("purpose"));
                }
            }
        }
    }
    
    // Handle data erasure (GDPR Article 17)
    private void handleDataErasure(String userId) throws SQLException {
        // Check if data can be erased (no legal obligation to retain)
        if (canEraseData(userId)) {
            String sql = "DELETE FROM user_data WHERE user_id = ?";
            
            try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                stmt.setString(1, userId);
                int rowsAffected = stmt.executeUpdate();
                System.out.println("Data erased for user " + userId + ": " + rowsAffected + " records");
            }
        } else {
            System.out.println("Data cannot be erased due to legal obligations");
        }
    }
    
    // Check if data can be erased
    private boolean canEraseData(String userId) throws SQLException {
        String sql = "SELECT COUNT(*) as count FROM user_data WHERE user_id = ? AND legal_obligation = 1";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, userId);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("count") == 0;
                }
            }
        }
        return true;
    }
    
    // HIPAA compliance - audit access to health data
    public void auditHealthDataAccess(String userId, String dataType) throws SQLException {
        String sql = """
            INSERT INTO health_data_audit (user_id, data_type, access_time, accessor)
            VALUES (?, ?, NOW(), USER())
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, userId);
            stmt.setString(2, dataType);
            stmt.executeUpdate();
            
            System.out.println("Health data access audited for user " + userId);
        }
    }
    
    // PCI DSS compliance - mask credit card data
    public String maskCreditCard(String cardNumber) {
        if (cardNumber == null || cardNumber.length() < 4) {
            return cardNumber;
        }
        
        String lastFour = cardNumber.substring(cardNumber.length() - 4);
        return "****-****-****-" + lastFour;
    }
}
```

## 8.8 Security Best Practices

Security best practices provide guidelines for implementing comprehensive database security measures.

### Best Practices:
- **Principle of Least Privilege**: Grant minimum necessary permissions
- **Defense in Depth**: Multiple layers of security
- **Regular Updates**: Keep systems and software current
- **Monitoring**: Continuous security monitoring
- **Incident Response**: Plan for security incidents
- **Training**: Educate users on security practices

### Real-World Analogy:
Security best practices are like home security:
- **Least Privilege** = Only give keys to necessary people
- **Defense in Depth** = Multiple security layers (locks, alarms, cameras)
- **Regular Updates** = Maintain security systems
- **Monitoring** = Security cameras and alarms
- **Incident Response** = Emergency procedures
- **Training** = Teach family about security

### Java Example - Security Best Practices:
```java
public class SecurityBestPractices {
    private Connection connection;
    
    public SecurityBestPractices(Connection connection) {
        this.connection = connection;
    }
    
    // Implement least privilege
    public void implementLeastPrivilege() throws SQLException {
        // Create limited privilege user
        String createUserSql = "CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'secure_password'";
        String grantPrivilegesSql = "GRANT SELECT, INSERT, UPDATE ON university_db.students TO 'app_user'@'localhost'";
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(createUserSql);
            stmt.execute(grantPrivilegesSql);
            System.out.println("Limited privilege user created");
        }
    }
    
    // Regular security audit
    public void performSecurityAudit() throws SQLException {
        System.out.println("Security Audit Report:");
        
        // Check for weak passwords
        checkWeakPasswords();
        
        // Check for excessive privileges
        checkExcessivePrivileges();
        
        // Check for inactive users
        checkInactiveUsers();
        
        // Check for failed login attempts
        checkFailedLogins();
    }
    
    private void checkWeakPasswords() throws SQLException {
        String sql = """
            SELECT username FROM users 
            WHERE password_hash IN (
                SELECT password_hash FROM users 
                GROUP BY password_hash 
                HAVING COUNT(*) > 1
            )
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Users with weak passwords:");
            while (rs.next()) {
                System.out.println("- " + rs.getString("username"));
            }
        }
    }
    
    private void checkExcessivePrivileges() throws SQLException {
        String sql = """
            SELECT user, host, db, select_priv, insert_priv, update_priv, delete_priv
            FROM mysql.user
            WHERE select_priv = 'Y' AND insert_priv = 'Y' AND update_priv = 'Y' AND delete_priv = 'Y'
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Users with excessive privileges:");
            while (rs.next()) {
                System.out.printf("- %s@%s on %s%n",
                    rs.getString("user"),
                    rs.getString("host"),
                    rs.getString("db"));
            }
        }
    }
    
    private void checkInactiveUsers() throws SQLException {
        String sql = """
            SELECT username FROM users 
            WHERE last_login < DATE_SUB(NOW(), INTERVAL 90 DAY)
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Inactive users (90+ days):");
            while (rs.next()) {
                System.out.println("- " + rs.getString("username"));
            }
        }
    }
    
    private void checkFailedLogins() throws SQLException {
        String sql = """
            SELECT username, COUNT(*) as failed_attempts
            FROM audit_log
            WHERE action = 'LOGIN_FAILED'
            AND timestamp > DATE_SUB(NOW(), INTERVAL 24 HOUR)
            GROUP BY username
            HAVING failed_attempts > 3
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("Users with multiple failed logins:");
            while (rs.next()) {
                System.out.printf("- %s: %d attempts%n",
                    rs.getString("username"),
                    rs.getInt("failed_attempts"));
            }
        }
    }
}
```