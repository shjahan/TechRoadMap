# Section 7 – Transaction Management

## 7.1 ACID Properties

ACID properties are the four fundamental characteristics that ensure reliable database transactions. They guarantee that database operations are processed reliably even in the event of system failures.

### ACID Components:
- **Atomicity**: All operations in a transaction succeed or all fail
- **Consistency**: Database remains in a valid state before and after transaction
- **Isolation**: Concurrent transactions don't interfere with each other
- **Durability**: Committed changes persist even after system failure

### Real-World Analogy:
ACID properties are like a bank transfer:
- **Atomicity** = Either the entire transfer completes or nothing happens
- **Consistency** = Account balances remain valid (no negative balances)
- **Isolation** = Multiple transfers don't interfere with each other
- **Durability** = Once confirmed, the transfer is permanent

### Java Example - ACID Implementation:
```java
import java.sql.*;

public class ACIDExample {
    private Connection connection;
    
    public ACIDExample(Connection connection) {
        this.connection = connection;
    }
    
    // Atomic transaction - transfer money between accounts
    public void transferMoney(int fromAccount, int toAccount, double amount) throws SQLException {
        try {
            // Start transaction (Atomicity)
            connection.setAutoCommit(false);
            
            // Check sufficient funds (Consistency)
            double fromBalance = getAccountBalance(fromAccount);
            if (fromBalance < amount) {
                throw new SQLException("Insufficient funds");
            }
            
            // Debit from source account
            updateAccountBalance(fromAccount, fromBalance - amount);
            
            // Credit to destination account
            double toBalance = getAccountBalance(toAccount);
            updateAccountBalance(toAccount, toBalance + amount);
            
            // Commit transaction (Durability)
            connection.commit();
            System.out.println("Transfer completed successfully");
            
        } catch (SQLException e) {
            // Rollback on any error (Atomicity)
            connection.rollback();
            System.err.println("Transfer failed: " + e.getMessage());
            throw e;
        } finally {
            // Restore auto-commit
            connection.setAutoCommit(true);
        }
    }
    
    private double getAccountBalance(int accountId) throws SQLException {
        String sql = "SELECT balance FROM accounts WHERE account_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, accountId);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getDouble("balance");
                }
                throw new SQLException("Account not found");
            }
        }
    }
    
    private void updateAccountBalance(int accountId, double newBalance) throws SQLException {
        String sql = "UPDATE accounts SET balance = ? WHERE account_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setDouble(1, newBalance);
            stmt.setInt(2, accountId);
            int rowsAffected = stmt.executeUpdate();
            if (rowsAffected == 0) {
                throw new SQLException("Account update failed");
            }
        }
    }
}
```

## 7.2 Transaction States

A transaction progresses through several states during its lifetime, from initiation to completion or failure.

### Transaction States:
- **Active**: Transaction is executing
- **Partially Committed**: All operations completed, but not yet committed
- **Committed**: Transaction successfully completed
- **Failed**: Transaction cannot proceed further
- **Aborted**: Transaction rolled back due to failure

### Real-World Analogy:
Transaction states are like the stages of a contract:
- **Active** = Contract is being negotiated
- **Partially Committed** = Terms agreed, waiting for signatures
- **Committed** = Contract fully executed and binding
- **Failed** = Negotiations broke down
- **Aborted** = Contract cancelled and voided

### Java Example - Transaction State Management:
```java
public class TransactionStateManager {
    private Connection connection;
    
    public TransactionStateManager(Connection connection) {
        this.connection = connection;
    }
    
    // Demonstrate transaction states
    public void demonstrateTransactionStates() throws SQLException {
        System.out.println("Transaction State Demonstration:");
        
        // Active state
        System.out.println("1. Active State - Starting transaction");
        connection.setAutoCommit(false);
        
        try {
            // Partially committed state
            System.out.println("2. Partially Committed - Executing operations");
            String sql = "INSERT INTO students (first_name, last_name, email) VALUES (?, ?, ?)";
            try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                stmt.setString(1, "John");
                stmt.setString(2, "Doe");
                stmt.setString(3, "john.doe@example.com");
                stmt.executeUpdate();
            }
            
            // Committed state
            System.out.println("3. Committed - Transaction completed");
            connection.commit();
            
        } catch (SQLException e) {
            // Failed/Aborted state
            System.out.println("4. Failed/Aborted - Transaction rolled back");
            connection.rollback();
            throw e;
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Check transaction state
    public boolean isTransactionActive() throws SQLException {
        return !connection.getAutoCommit();
    }
    
    // Get transaction isolation level
    public int getTransactionIsolation() throws SQLException {
        return connection.getTransactionIsolation();
    }
    
    // Set transaction isolation level
    public void setTransactionIsolation(int level) throws SQLException {
        connection.setTransactionIsolation(level);
        System.out.println("Transaction isolation level set to: " + level);
    }
}
```

## 7.3 Concurrency Control

Concurrency control manages simultaneous access to database resources by multiple transactions to ensure data consistency and integrity.

### Concurrency Problems:
- **Lost Update**: Two transactions modify the same data simultaneously
- **Dirty Read**: Reading uncommitted data from another transaction
- **Non-repeatable Read**: Different values read in the same transaction
- **Phantom Read**: New rows appear in subsequent reads

### Real-World Analogy:
Concurrency control is like managing a shared workspace:
- **Lost Update** = Two people editing the same document simultaneously
- **Dirty Read** = Reading a document while someone is still editing it
- **Non-repeatable Read** = Document content changes between reads
- **Phantom Read** = New documents appear in the workspace

### Java Example - Concurrency Control:
```java
public class ConcurrencyControl {
    private Connection connection;
    
    public ConcurrencyControl(Connection connection) {
        this.connection = connection;
    }
    
    // Demonstrate lost update problem
    public void demonstrateLostUpdate() throws SQLException {
        System.out.println("Lost Update Problem Demonstration:");
        
        // Transaction 1: Read and update
        connection.setAutoCommit(false);
        try {
            // Read current value
            int currentValue = readValue("counter");
            System.out.println("Transaction 1 reads: " + currentValue);
            
            // Simulate processing time
            Thread.sleep(1000);
            
            // Update value
            updateValue("counter", currentValue + 1);
            connection.commit();
            System.out.println("Transaction 1 commits: " + (currentValue + 1));
            
        } catch (Exception e) {
            connection.rollback();
            System.err.println("Transaction 1 failed: " + e.getMessage());
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Prevent lost update using locking
    public void preventLostUpdate() throws SQLException {
        System.out.println("Lost Update Prevention with Locking:");
        
        connection.setAutoCommit(false);
        try {
            // Read with lock
            int currentValue = readValueWithLock("counter");
            System.out.println("Transaction reads with lock: " + currentValue);
            
            // Simulate processing time
            Thread.sleep(1000);
            
            // Update value
            updateValue("counter", currentValue + 1);
            connection.commit();
            System.out.println("Transaction commits: " + (currentValue + 1));
            
        } catch (Exception e) {
            connection.rollback();
            System.err.println("Transaction failed: " + e.getMessage());
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    private int readValue(String key) throws SQLException {
        String sql = "SELECT value FROM test_table WHERE key = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, key);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("value");
                }
                return 0;
            }
        }
    }
    
    private int readValueWithLock(String key) throws SQLException {
        String sql = "SELECT value FROM test_table WHERE key = ? FOR UPDATE";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, key);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("value");
                }
                return 0;
            }
        }
    }
    
    private void updateValue(String key, int newValue) throws SQLException {
        String sql = "UPDATE test_table SET value = ? WHERE key = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, newValue);
            stmt.setString(2, key);
            stmt.executeUpdate();
        }
    }
}
```

## 7.4 Locking Mechanisms

Locking mechanisms prevent concurrent transactions from interfering with each other by controlling access to database resources.

### Lock Types:
- **Shared Lock (S)**: Allows reading but not writing
- **Exclusive Lock (X)**: Allows both reading and writing
- **Intent Lock (I)**: Indicates intention to acquire locks on child resources
- **Update Lock (U)**: Allows reading and potential upgrading to exclusive lock

### Lock Granularity:
- **Row-level**: Lock individual rows
- **Page-level**: Lock database pages
- **Table-level**: Lock entire tables
- **Database-level**: Lock entire database

### Real-World Analogy:
Locking mechanisms are like library book management:
- **Shared Lock** = Multiple people can read the same book
- **Exclusive Lock** = Only one person can write in the book
- **Intent Lock** = Reserving a section of the library
- **Update Lock** = Checking out a book for potential editing

### Java Example - Locking Mechanisms:
```java
public class LockingMechanisms {
    private Connection connection;
    
    public LockingMechanisms(Connection connection) {
        this.connection = connection;
    }
    
    // Demonstrate shared lock
    public void demonstrateSharedLock() throws SQLException {
        System.out.println("Shared Lock Demonstration:");
        
        connection.setAutoCommit(false);
        try {
            // Acquire shared lock
            String sql = "SELECT * FROM students WHERE student_id = ? LOCK IN SHARE MODE";
            try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                stmt.setInt(1, 1);
                try (ResultSet rs = stmt.executeQuery()) {
                    while (rs.next()) {
                        System.out.println("Reading student: " + rs.getString("first_name"));
                    }
                }
            }
            
            // Hold lock for demonstration
            Thread.sleep(2000);
            connection.commit();
            
        } catch (Exception e) {
            connection.rollback();
            System.err.println("Shared lock failed: " + e.getMessage());
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Demonstrate exclusive lock
    public void demonstrateExclusiveLock() throws SQLException {
        System.out.println("Exclusive Lock Demonstration:");
        
        connection.setAutoCommit(false);
        try {
            // Acquire exclusive lock
            String sql = "SELECT * FROM students WHERE student_id = ? FOR UPDATE";
            try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                stmt.setInt(1, 1);
                try (ResultSet rs = stmt.executeQuery()) {
                    while (rs.next()) {
                        System.out.println("Updating student: " + rs.getString("first_name"));
                    }
                }
            }
            
            // Update the locked row
            String updateSql = "UPDATE students SET email = ? WHERE student_id = ?";
            try (PreparedStatement stmt = connection.prepareStatement(updateSql)) {
                stmt.setString(1, "updated@example.com");
                stmt.setInt(2, 1);
                stmt.executeUpdate();
            }
            
            connection.commit();
            System.out.println("Exclusive lock transaction completed");
            
        } catch (Exception e) {
            connection.rollback();
            System.err.println("Exclusive lock failed: " + e.getMessage());
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Demonstrate deadlock detection
    public void demonstrateDeadlock() throws SQLException {
        System.out.println("Deadlock Demonstration:");
        
        // This would typically be run in separate threads
        // to demonstrate deadlock scenarios
        connection.setAutoCommit(false);
        try {
            // Transaction 1: Lock student 1, then student 2
            String sql1 = "SELECT * FROM students WHERE student_id = ? FOR UPDATE";
            try (PreparedStatement stmt = connection.prepareStatement(sql1)) {
                stmt.setInt(1, 1);
                stmt.executeQuery();
                System.out.println("Locked student 1");
            }
            
            // Simulate delay
            Thread.sleep(100);
            
            String sql2 = "SELECT * FROM students WHERE student_id = ? FOR UPDATE";
            try (PreparedStatement stmt = connection.prepareStatement(sql2)) {
                stmt.setInt(1, 2);
                stmt.executeQuery();
                System.out.println("Locked student 2");
            }
            
            connection.commit();
            
        } catch (Exception e) {
            if (e.getMessage().contains("Deadlock")) {
                System.out.println("Deadlock detected and resolved");
            }
            connection.rollback();
        } finally {
            connection.setAutoCommit(true);
        }
    }
}
```

## 7.5 Deadlock Detection and Prevention

Deadlock occurs when two or more transactions are waiting for each other to release locks, creating a circular wait condition.

### Deadlock Conditions:
- **Mutual Exclusion**: Resources cannot be shared
- **Hold and Wait**: Transactions hold resources while waiting for others
- **No Preemption**: Resources cannot be forcibly taken
- **Circular Wait**: Circular chain of waiting transactions

### Prevention Strategies:
- **Lock Ordering**: Always acquire locks in the same order
- **Timeout**: Set maximum wait time for locks
- **Deadlock Detection**: Periodically check for circular waits
- **Resource Preemption**: Force release of locks when deadlock detected

### Real-World Analogy:
Deadlock is like a traffic jam at a four-way intersection:
- **Mutual Exclusion** = Only one car can occupy the intersection
- **Hold and Wait** = Cars wait while occupying part of the intersection
- **No Preemption** = Cars cannot be forcibly moved
- **Circular Wait** = Cars waiting for each other in a circle

### Java Example - Deadlock Prevention:
```java
public class DeadlockPrevention {
    private Connection connection;
    
    public DeadlockPrevention(Connection connection) {
        this.connection = connection;
    }
    
    // Prevent deadlock using lock ordering
    public void preventDeadlockWithOrdering(int studentId1, int studentId2) throws SQLException {
        System.out.println("Deadlock Prevention with Lock Ordering:");
        
        // Always lock in ascending order of ID
        int firstId = Math.min(studentId1, studentId2);
        int secondId = Math.max(studentId1, studentId2);
        
        connection.setAutoCommit(false);
        try {
            // Lock first student
            lockStudent(firstId);
            System.out.println("Locked student " + firstId);
            
            // Lock second student
            lockStudent(secondId);
            System.out.println("Locked student " + secondId);
            
            // Perform operations
            updateStudentEmail(firstId, "first@example.com");
            updateStudentEmail(secondId, "second@example.com");
            
            connection.commit();
            System.out.println("Transaction completed successfully");
            
        } catch (Exception e) {
            connection.rollback();
            System.err.println("Transaction failed: " + e.getMessage());
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Prevent deadlock using timeout
    public void preventDeadlockWithTimeout(int studentId) throws SQLException {
        System.out.println("Deadlock Prevention with Timeout:");
        
        // Set lock timeout
        try (Statement stmt = connection.createStatement()) {
            stmt.execute("SET innodb_lock_wait_timeout = 5"); // 5 seconds
        }
        
        connection.setAutoCommit(false);
        try {
            lockStudent(studentId);
            System.out.println("Locked student " + studentId);
            
            // Simulate processing
            Thread.sleep(3000);
            
            updateStudentEmail(studentId, "timeout@example.com");
            connection.commit();
            
        } catch (Exception e) {
            if (e.getMessage().contains("timeout")) {
                System.out.println("Lock timeout occurred");
            }
            connection.rollback();
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    private void lockStudent(int studentId) throws SQLException {
        String sql = "SELECT * FROM students WHERE student_id = ? FOR UPDATE";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, studentId);
            stmt.executeQuery();
        }
    }
    
    private void updateStudentEmail(int studentId, String email) throws SQLException {
        String sql = "UPDATE students SET email = ? WHERE student_id = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, email);
            stmt.setInt(2, studentId);
            stmt.executeUpdate();
        }
    }
}
```

## 7.6 Isolation Levels

Isolation levels control the degree to which one transaction is isolated from other concurrent transactions, balancing consistency with performance.

### Isolation Levels:
- **READ UNCOMMITTED**: Lowest isolation, allows dirty reads
- **READ COMMITTED**: Prevents dirty reads, allows non-repeatable reads
- **REPEATABLE READ**: Prevents dirty and non-repeatable reads, allows phantom reads
- **SERIALIZABLE**: Highest isolation, prevents all concurrency problems

### Real-World Analogy:
Isolation levels are like privacy settings in a shared workspace:
- **READ UNCOMMITTED** = See everything, even work in progress
- **READ COMMITTED** = See only completed work
- **REPEATABLE READ** = See consistent snapshots
- **SERIALIZABLE** = Complete privacy, no interference

### Java Example - Isolation Levels:
```java
public class IsolationLevels {
    private Connection connection;
    
    public IsolationLevels(Connection connection) {
        this.connection = connection;
    }
    
    // Demonstrate READ UNCOMMITTED
    public void demonstrateReadUncommitted() throws SQLException {
        System.out.println("READ UNCOMMITTED Demonstration:");
        
        connection.setTransactionIsolation(Connection.TRANSACTION_READ_UNCOMMITTED);
        connection.setAutoCommit(false);
        
        try {
            // Read data that might be uncommitted
            String sql = "SELECT * FROM students WHERE student_id = ?";
            try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                stmt.setInt(1, 1);
                try (ResultSet rs = stmt.executeQuery()) {
                    while (rs.next()) {
                        System.out.println("Read (possibly uncommitted): " + rs.getString("email"));
                    }
                }
            }
            
        } catch (Exception e) {
            System.err.println("READ UNCOMMITTED failed: " + e.getMessage());
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Demonstrate READ COMMITTED
    public void demonstrateReadCommitted() throws SQLException {
        System.out.println("READ COMMITTED Demonstration:");
        
        connection.setTransactionIsolation(Connection.TRANSACTION_READ_COMMITTED);
        connection.setAutoCommit(false);
        
        try {
            // Read committed data only
            String sql = "SELECT * FROM students WHERE student_id = ?";
            try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                stmt.setInt(1, 1);
                try (ResultSet rs = stmt.executeQuery()) {
                    while (rs.next()) {
                        System.out.println("Read (committed): " + rs.getString("email"));
                    }
                }
            }
            
        } catch (Exception e) {
            System.err.println("READ COMMITTED failed: " + e.getMessage());
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Demonstrate REPEATABLE READ
    public void demonstrateRepeatableRead() throws SQLException {
        System.out.println("REPEATABLE READ Demonstration:");
        
        connection.setTransactionIsolation(Connection.TRANSACTION_REPEATABLE_READ);
        connection.setAutoCommit(false);
        
        try {
            // First read
            String sql = "SELECT * FROM students WHERE student_id = ?";
            try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                stmt.setInt(1, 1);
                try (ResultSet rs = stmt.executeQuery()) {
                    while (rs.next()) {
                        System.out.println("First read: " + rs.getString("email"));
                    }
                }
            }
            
            // Second read (should be same as first)
            try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                stmt.setInt(1, 1);
                try (ResultSet rs = stmt.executeQuery()) {
                    while (rs.next()) {
                        System.out.println("Second read: " + rs.getString("email"));
                    }
                }
            }
            
        } catch (Exception e) {
            System.err.println("REPEATABLE READ failed: " + e.getMessage());
        } finally {
            connection.setAutoCommit(true);
        }
    }
    
    // Demonstrate SERIALIZABLE
    public void demonstrateSerializable() throws SQLException {
        System.out.println("SERIALIZABLE Demonstration:");
        
        connection.setTransactionIsolation(Connection.TRANSACTION_SERIALIZABLE);
        connection.setAutoCommit(false);
        
        try {
            // Read with serializable isolation
            String sql = "SELECT * FROM students WHERE gpa > ?";
            try (PreparedStatement stmt = connection.prepareStatement(sql)) {
                stmt.setDouble(1, 3.0);
                try (ResultSet rs = stmt.executeQuery()) {
                    while (rs.next()) {
                        System.out.println("Serializable read: " + rs.getString("first_name"));
                    }
                }
            }
            
        } catch (Exception e) {
            System.err.println("SERIALIZABLE failed: " + e.getMessage());
        } finally {
            connection.setAutoCommit(true);
        }
    }
}
```

## 7.7 Two-Phase Commit (2PC)

Two-Phase Commit is a distributed transaction protocol that ensures atomicity across multiple database systems or resources.

### 2PC Phases:
- **Phase 1 (Prepare)**: Coordinator asks all participants to prepare
- **Phase 2 (Commit/Rollback)**: Coordinator decides to commit or rollback based on responses

### Real-World Analogy:
2PC is like organizing a group meeting:
- **Phase 1** = Ask everyone if they can attend
- **Phase 2** = If everyone can attend, confirm the meeting; otherwise, cancel

### Java Example - Two-Phase Commit:
```java
public class TwoPhaseCommit {
    private List<Connection> connections;
    
    public TwoPhaseCommit(List<Connection> connections) {
        this.connections = connections;
    }
    
    // Execute distributed transaction using 2PC
    public void executeDistributedTransaction() throws SQLException {
        System.out.println("Two-Phase Commit Demonstration:");
        
        // Phase 1: Prepare
        System.out.println("Phase 1: Preparing all participants");
        boolean allPrepared = true;
        
        for (Connection conn : connections) {
            try {
                conn.setAutoCommit(false);
                // Simulate prepare phase
                prepareTransaction(conn);
                System.out.println("Participant prepared successfully");
            } catch (SQLException e) {
                System.err.println("Participant failed to prepare: " + e.getMessage());
                allPrepared = false;
                break;
            }
        }
        
        // Phase 2: Commit or Rollback
        if (allPrepared) {
            System.out.println("Phase 2: All participants prepared, committing");
            for (Connection conn : connections) {
                try {
                    conn.commit();
                    System.out.println("Participant committed successfully");
                } catch (SQLException e) {
                    System.err.println("Participant commit failed: " + e.getMessage());
                }
            }
        } else {
            System.out.println("Phase 2: Some participants failed, rolling back");
            for (Connection conn : connections) {
                try {
                    conn.rollback();
                    System.out.println("Participant rolled back");
                } catch (SQLException e) {
                    System.err.println("Participant rollback failed: " + e.getMessage());
                }
            }
        }
        
        // Restore auto-commit
        for (Connection conn : connections) {
            conn.setAutoCommit(true);
        }
    }
    
    private void prepareTransaction(Connection conn) throws SQLException {
        // Simulate transaction preparation
        String sql = "INSERT INTO test_table (value) VALUES (?)";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, "prepared");
            stmt.executeUpdate();
        }
    }
}
```

## 7.8 Three-Phase Commit (3PC)

Three-Phase Commit is an improvement over 2PC that reduces the risk of blocking by adding a pre-commit phase.

### 3PC Phases:
- **Phase 1 (CanCommit)**: Coordinator asks if participants can commit
- **Phase 2 (PreCommit)**: Coordinator sends pre-commit message
- **Phase 3 (DoCommit)**: Coordinator sends final commit message

### Real-World Analogy:
3PC is like a three-step confirmation process:
- **Phase 1** = "Can you attend the meeting?"
- **Phase 2** = "Meeting is confirmed, please prepare"
- **Phase 3** = "Meeting is starting now"

### Java Example - Three-Phase Commit:
```java
public class ThreePhaseCommit {
    private List<Connection> connections;
    
    public ThreePhaseCommit(List<Connection> connections) {
        this.connections = connections;
    }
    
    // Execute distributed transaction using 3PC
    public void executeDistributedTransaction() throws SQLException {
        System.out.println("Three-Phase Commit Demonstration:");
        
        // Phase 1: CanCommit
        System.out.println("Phase 1: Checking if all participants can commit");
        boolean allCanCommit = true;
        
        for (Connection conn : connections) {
            try {
                conn.setAutoCommit(false);
                canCommit(conn);
                System.out.println("Participant can commit");
            } catch (SQLException e) {
                System.err.println("Participant cannot commit: " + e.getMessage());
                allCanCommit = false;
                break;
            }
        }
        
        if (!allCanCommit) {
            System.out.println("Phase 1 failed, aborting transaction");
            abortTransaction();
            return;
        }
        
        // Phase 2: PreCommit
        System.out.println("Phase 2: Sending pre-commit to all participants");
        for (Connection conn : connections) {
            try {
                preCommit(conn);
                System.out.println("Participant pre-committed");
            } catch (SQLException e) {
                System.err.println("Participant pre-commit failed: " + e.getMessage());
                abortTransaction();
                return;
            }
        }
        
        // Phase 3: DoCommit
        System.out.println("Phase 3: Final commit");
        for (Connection conn : connections) {
            try {
                doCommit(conn);
                System.out.println("Participant committed");
            } catch (SQLException e) {
                System.err.println("Participant commit failed: " + e.getMessage());
            }
        }
        
        // Restore auto-commit
        for (Connection conn : connections) {
            conn.setAutoCommit(true);
        }
    }
    
    private void canCommit(Connection conn) throws SQLException {
        // Simulate can commit check
        String sql = "SELECT COUNT(*) FROM test_table";
        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            // Check if commit is possible
        }
    }
    
    private void preCommit(Connection conn) throws SQLException {
        // Simulate pre-commit
        String sql = "INSERT INTO test_table (value) VALUES (?)";
        try (PreparedStatement stmt = conn.prepareStatement(sql)) {
            stmt.setString(1, "pre-committed");
            stmt.executeUpdate();
        }
    }
    
    private void doCommit(Connection conn) throws SQLException {
        conn.commit();
    }
    
    private void abortTransaction() throws SQLException {
        for (Connection conn : connections) {
            try {
                conn.rollback();
                System.out.println("Participant aborted");
            } catch (SQLException e) {
                System.err.println("Participant abort failed: " + e.getMessage());
            }
        }
    }
}
```