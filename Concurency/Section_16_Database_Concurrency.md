# Section 16 – Database Concurrency

## 16.1 ACID Properties

ACID properties ensure reliable database transactions in concurrent environments.

### Key Concepts
- **Atomicity**: All operations in a transaction succeed or all fail
- **Consistency**: Database remains in a valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist

### Real-World Analogy
Think of a bank transfer where money is either completely transferred from one account to another or not at all, with all accounts remaining balanced and the transaction permanently recorded.

### Java Example
```java
public class ACIDPropertiesExample {
    // Database connection simulation
    public static class DatabaseConnection {
        private final AtomicBoolean inTransaction = new AtomicBoolean(false);
        private final AtomicInteger balance = new AtomicInteger(1000);
        
        public void beginTransaction() {
            inTransaction.set(true);
        }
        
        public void commit() {
            inTransaction.set(false);
        }
        
        public void rollback() {
            inTransaction.set(false);
        }
        
        public boolean isInTransaction() {
            return inTransaction.get();
        }
        
        public int getBalance() {
            return balance.get();
        }
        
        public void setBalance(int newBalance) {
            balance.set(newBalance);
        }
    }
    
    // Transaction manager
    public static class TransactionManager {
        private final DatabaseConnection connection;
        
        public TransactionManager(DatabaseConnection connection) {
            this.connection = connection;
        }
        
        public boolean transferMoney(int fromAccount, int toAccount, int amount) {
            connection.beginTransaction();
            
            try {
                // Atomicity: All operations succeed or all fail
                if (connection.getBalance() < amount) {
                    connection.rollback();
                    return false;
                }
                
                // Consistency: Maintain valid state
                int newBalance = connection.getBalance() - amount;
                connection.setBalance(newBalance);
                
                // Simulate transfer to another account
                Thread.sleep(100);
                
                connection.commit();
                return true;
                
            } catch (Exception e) {
                connection.rollback();
                return false;
            }
        }
    }
    
    // Isolation levels simulation
    public static class IsolationLevels {
        public enum IsolationLevel {
            READ_UNCOMMITTED,
            READ_COMMITTED,
            REPEATABLE_READ,
            SERIALIZABLE
        }
        
        private final IsolationLevel level;
        private final Map<String, Integer> data = new ConcurrentHashMap<>();
        private final Map<String, Integer> uncommittedData = new ConcurrentHashMap<>();
        
        public IsolationLevels(IsolationLevel level) {
            this.level = level;
            data.put("account1", 1000);
            data.put("account2", 500);
        }
        
        public Integer read(String key) {
            switch (level) {
                case READ_UNCOMMITTED:
                    return uncommittedData.getOrDefault(key, data.get(key));
                case READ_COMMITTED:
                case REPEATABLE_READ:
                case SERIALIZABLE:
                    return data.get(key);
                default:
                    return data.get(key);
            }
        }
        
        public void write(String key, Integer value) {
            uncommittedData.put(key, value);
        }
        
        public void commit() {
            data.putAll(uncommittedData);
            uncommittedData.clear();
        }
        
        public void rollback() {
            uncommittedData.clear();
        }
    }
}
```

## 16.2 Transaction Isolation Levels

Transaction isolation levels control how transactions interact with each other and what data they can see.

### Key Concepts
- **Read Uncommitted**: Can read uncommitted changes
- **Read Committed**: Can only read committed changes
- **Repeatable Read**: Consistent reads within transaction
- **Serializable**: Highest isolation level

### Real-World Analogy
Think of different levels of privacy in a shared office space, from everyone seeing everything (read uncommitted) to complete privacy (serializable).

### Java Example
```java
public class TransactionIsolationLevelsExample {
    // Transaction isolation levels
    public enum IsolationLevel {
        READ_UNCOMMITTED,
        READ_COMMITTED,
        REPEATABLE_READ,
        SERIALIZABLE
    }
    
    // Database simulation
    public static class DatabaseSimulation {
        private final Map<String, Integer> committedData = new ConcurrentHashMap<>();
        private final Map<String, Integer> uncommittedData = new ConcurrentHashMap<>();
        private final Map<String, Integer> transactionData = new ConcurrentHashMap<>();
        private final IsolationLevel isolationLevel;
        
        public DatabaseSimulation(IsolationLevel isolationLevel) {
            this.isolationLevel = isolationLevel;
            committedData.put("account1", 1000);
            committedData.put("account2", 500);
        }
        
        public Integer read(String key, String transactionId) {
            switch (isolationLevel) {
                case READ_UNCOMMITTED:
                    // Can read uncommitted changes
                    return uncommittedData.getOrDefault(key, committedData.get(key));
                    
                case READ_COMMITTED:
                    // Can only read committed changes
                    return committedData.get(key);
                    
                case REPEATABLE_READ:
                    // Consistent reads within transaction
                    if (transactionData.containsKey(transactionId + ":" + key)) {
                        return transactionData.get(transactionId + ":" + key);
                    }
                    Integer value = committedData.get(key);
                    transactionData.put(transactionId + ":" + key, value);
                    return value;
                    
                case SERIALIZABLE:
                    // Highest isolation level
                    return committedData.get(key);
                    
                default:
                    return committedData.get(key);
            }
        }
        
        public void write(String key, Integer value, String transactionId) {
            uncommittedData.put(key, value);
            if (isolationLevel == IsolationLevel.REPEATABLE_READ) {
                transactionData.put(transactionId + ":" + key, value);
            }
        }
        
        public void commit(String transactionId) {
            committedData.putAll(uncommittedData);
            uncommittedData.clear();
            transactionData.entrySet().removeIf(entry -> entry.getKey().startsWith(transactionId + ":"));
        }
        
        public void rollback(String transactionId) {
            uncommittedData.clear();
            transactionData.entrySet().removeIf(entry -> entry.getKey().startsWith(transactionId + ":"));
        }
    }
    
    // Transaction simulation
    public static class TransactionSimulation {
        private final DatabaseSimulation database;
        private final String transactionId;
        
        public TransactionSimulation(DatabaseSimulation database, String transactionId) {
            this.database = database;
            this.transactionId = transactionId;
        }
        
        public Integer read(String key) {
            return database.read(key, transactionId);
        }
        
        public void write(String key, Integer value) {
            database.write(key, value, transactionId);
        }
        
        public void commit() {
            database.commit(transactionId);
        }
        
        public void rollback() {
            database.rollback(transactionId);
        }
    }
    
    // Demonstrate isolation levels
    public static void demonstrateIsolationLevels() {
        for (IsolationLevel level : IsolationLevel.values()) {
            System.out.println("\n=== " + level + " ===");
            
            DatabaseSimulation database = new DatabaseSimulation(level);
            TransactionSimulation transaction1 = new TransactionSimulation(database, "T1");
            TransactionSimulation transaction2 = new TransactionSimulation(database, "T2");
            
            // Transaction 1 reads, then writes
            System.out.println("T1 reads account1: " + transaction1.read("account1"));
            transaction1.write("account1", 800);
            
            // Transaction 2 reads before T1 commits
            System.out.println("T2 reads account1: " + transaction2.read("account1"));
            
            // Transaction 1 commits
            transaction1.commit();
            
            // Transaction 2 reads after T1 commits
            System.out.println("T2 reads account1 after T1 commit: " + transaction2.read("account1"));
        }
    }
}
```

## 16.3 Locking in Databases

Database locking prevents concurrent access to the same data, ensuring data consistency.

### Key Concepts
- **Shared Locks**: Multiple readers can hold
- **Exclusive Locks**: Only one writer can hold
- **Lock Granularity**: Row, page, or table level
- **Deadlock Prevention**: Avoiding circular waits

### Real-World Analogy
Think of a library where books can be read by multiple people simultaneously (shared lock) but only one person can write in them at a time (exclusive lock).

### Java Example
```java
public class DatabaseLockingExample {
    // Lock types
    public enum LockType {
        SHARED,
        EXCLUSIVE
    }
    
    // Lock manager
    public static class LockManager {
        private final Map<String, Set<String>> sharedLocks = new ConcurrentHashMap<>();
        private final Map<String, String> exclusiveLocks = new ConcurrentHashMap<>();
        private final Map<String, Set<String>> waitingLocks = new ConcurrentHashMap<>();
        
        public boolean acquireLock(String resource, String transactionId, LockType lockType) {
            synchronized (this) {
                if (lockType == LockType.SHARED) {
                    return acquireSharedLock(resource, transactionId);
                } else {
                    return acquireExclusiveLock(resource, transactionId);
                }
            }
        }
        
        private boolean acquireSharedLock(String resource, String transactionId) {
            // Check if exclusive lock exists
            if (exclusiveLocks.containsKey(resource)) {
                addToWaitingList(resource, transactionId);
                return false;
            }
            
            // Acquire shared lock
            sharedLocks.computeIfAbsent(resource, k -> ConcurrentHashMap.newKeySet()).add(transactionId);
            return true;
        }
        
        private boolean acquireExclusiveLock(String resource, String transactionId) {
            // Check if any locks exist
            if (exclusiveLocks.containsKey(resource) || 
                sharedLocks.containsKey(resource) && !sharedLocks.get(resource).isEmpty()) {
                addToWaitingList(resource, transactionId);
                return false;
            }
            
            // Acquire exclusive lock
            exclusiveLocks.put(resource, transactionId);
            return true;
        }
        
        private void addToWaitingList(String resource, String transactionId) {
            waitingLocks.computeIfAbsent(resource, k -> ConcurrentHashMap.newKeySet()).add(transactionId);
        }
        
        public void releaseLock(String resource, String transactionId) {
            synchronized (this) {
                // Release shared lock
                if (sharedLocks.containsKey(resource)) {
                    sharedLocks.get(resource).remove(transactionId);
                    if (sharedLocks.get(resource).isEmpty()) {
                        sharedLocks.remove(resource);
                    }
                }
                
                // Release exclusive lock
                if (exclusiveLocks.containsKey(resource) && 
                    exclusiveLocks.get(resource).equals(transactionId)) {
                    exclusiveLocks.remove(resource);
                }
                
                // Process waiting locks
                processWaitingLocks(resource);
            }
        }
        
        private void processWaitingLocks(String resource) {
            Set<String> waiting = waitingLocks.get(resource);
            if (waiting != null && !waiting.isEmpty()) {
                String nextTransaction = waiting.iterator().next();
                waiting.remove(nextTransaction);
                
                if (waiting.isEmpty()) {
                    waitingLocks.remove(resource);
                }
            }
        }
        
        public boolean isLocked(String resource) {
            return exclusiveLocks.containsKey(resource) || 
                   (sharedLocks.containsKey(resource) && !sharedLocks.get(resource).isEmpty());
        }
    }
    
    // Transaction with locking
    public static class LockingTransaction {
        private final LockManager lockManager;
        private final String transactionId;
        private final Map<String, Integer> data = new ConcurrentHashMap<>();
        
        public LockingTransaction(LockManager lockManager, String transactionId) {
            this.lockManager = lockManager;
            this.transactionId = transactionId;
        }
        
        public boolean read(String resource) {
            if (lockManager.acquireLock(resource, transactionId, LockType.SHARED)) {
                System.out.println("Transaction " + transactionId + " acquired shared lock on " + resource);
                return true;
            }
            return false;
        }
        
        public boolean write(String resource, Integer value) {
            if (lockManager.acquireLock(resource, transactionId, LockType.EXCLUSIVE)) {
                data.put(resource, value);
                System.out.println("Transaction " + transactionId + " acquired exclusive lock on " + resource);
                return true;
            }
            return false;
        }
        
        public void commit() {
            // Release all locks
            for (String resource : data.keySet()) {
                lockManager.releaseLock(resource, transactionId);
            }
            System.out.println("Transaction " + transactionId + " committed");
        }
        
        public void rollback() {
            data.clear();
            System.out.println("Transaction " + transactionId + " rolled back");
        }
    }
}
```

## 16.4 Optimistic vs Pessimistic Locking

Optimistic and pessimistic locking are two approaches to handling concurrent access to data.

### Key Concepts
- **Optimistic Locking**: Assume no conflicts, detect them if they occur
- **Pessimistic Locking**: Assume conflicts will occur, prevent them
- **Version Control**: Using version numbers for optimistic locking
- **Performance Trade-offs**: Different performance characteristics

### Real-World Analogy
**Optimistic**: Like a shared document where everyone can edit simultaneously, and conflicts are resolved when they occur
**Pessimistic**: Like a document that only one person can edit at a time, with others waiting in line

### Java Example
```java
public class OptimisticPessimisticLockingExample {
    // Optimistic locking with version control
    public static class OptimisticLocking {
        private final Map<String, VersionedData> data = new ConcurrentHashMap<>();
        
        public static class VersionedData {
            private final String value;
            private final int version;
            
            public VersionedData(String value, int version) {
                this.value = value;
                this.version = version;
            }
            
            public String getValue() { return value; }
            public int getVersion() { return version; }
        }
        
        public boolean update(String key, String newValue, int expectedVersion) {
            VersionedData current = data.get(key);
            if (current != null && current.getVersion() == expectedVersion) {
                data.put(key, new VersionedData(newValue, expectedVersion + 1));
                return true;
            }
            return false;
        }
        
        public VersionedData read(String key) {
            return data.get(key);
        }
        
        public void put(String key, String value) {
            data.put(key, new VersionedData(value, 0));
        }
    }
    
    // Pessimistic locking
    public static class PessimisticLocking {
        private final Map<String, String> data = new ConcurrentHashMap<>();
        private final Map<String, ReentrantLock> locks = new ConcurrentHashMap<>();
        
        public String read(String key) {
            ReentrantLock lock = locks.computeIfAbsent(key, k -> new ReentrantLock());
            lock.lock();
            try {
                return data.get(key);
            } finally {
                lock.unlock();
            }
        }
        
        public void write(String key, String value) {
            ReentrantLock lock = locks.computeIfAbsent(key, k -> new ReentrantLock());
            lock.lock();
            try {
                data.put(key, value);
            } finally {
                lock.unlock();
            }
        }
    }
    
    // Transaction simulation
    public static class TransactionSimulation {
        private final OptimisticLocking optimisticDB;
        private final PessimisticLocking pessimisticDB;
        
        public TransactionSimulation(OptimisticLocking optimisticDB, PessimisticLocking pessimisticDB) {
            this.optimisticDB = optimisticDB;
            this.pessimisticDB = pessimisticDB;
        }
        
        public boolean optimisticUpdate(String key, String newValue) {
            OptimisticLocking.VersionedData current = optimisticDB.read(key);
            if (current != null) {
                return optimisticDB.update(key, newValue, current.getVersion());
            }
            return false;
        }
        
        public void pessimisticUpdate(String key, String newValue) {
            pessimisticDB.write(key, newValue);
        }
        
        public String optimisticRead(String key) {
            OptimisticLocking.VersionedData data = optimisticDB.read(key);
            return data != null ? data.getValue() : null;
        }
        
        public String pessimisticRead(String key) {
            return pessimisticDB.read(key);
        }
    }
}
```

## 16.5 MVCC (Multi-Version Concurrency Control)

MVCC allows multiple versions of data to coexist, enabling readers to see consistent snapshots without blocking writers.

### Key Concepts
- **Versioning**: Multiple versions of each record
- **Snapshot Isolation**: Readers see consistent snapshots
- **Garbage Collection**: Cleanup of old versions
- **Write Conflicts**: Detection and resolution

### Real-World Analogy
Think of a document with version history where readers can see any previous version while writers create new versions, and old versions are eventually archived.

### Java Example
```java
public class MVCCExample {
    // MVCC record
    public static class MVCCRecord {
        private final String key;
        private final String value;
        private final long transactionId;
        private final long commitTime;
        private final boolean isDeleted;
        
        public MVCCRecord(String key, String value, long transactionId, long commitTime, boolean isDeleted) {
            this.key = key;
            this.value = value;
            this.transactionId = transactionId;
            this.commitTime = commitTime;
            this.isDeleted = isDeleted;
        }
        
        public String getKey() { return key; }
        public String getValue() { return value; }
        public long getTransactionId() { return transactionId; }
        public long getCommitTime() { return commitTime; }
        public boolean isDeleted() { return isDeleted; }
    }
    
    // MVCC database
    public static class MVCCDatabase {
        private final Map<String, List<MVCCRecord>> records = new ConcurrentHashMap<>();
        private final AtomicLong transactionIdCounter = new AtomicLong(0);
        private final AtomicLong commitTimeCounter = new AtomicLong(0);
        
        public long beginTransaction() {
            return transactionIdCounter.incrementAndGet();
        }
        
        public void commitTransaction(long transactionId) {
            long commitTime = commitTimeCounter.incrementAndGet();
            // Update commit times for all records in this transaction
            for (List<MVCCRecord> recordList : records.values()) {
                for (MVCCRecord record : recordList) {
                    if (record.getTransactionId() == transactionId) {
                        // Update commit time
                    }
                }
            }
        }
        
        public void write(String key, String value, long transactionId) {
            long commitTime = commitTimeCounter.get();
            MVCCRecord record = new MVCCRecord(key, value, transactionId, commitTime, false);
            
            records.computeIfAbsent(key, k -> new ArrayList<>()).add(record);
        }
        
        public void delete(String key, long transactionId) {
            long commitTime = commitTimeCounter.get();
            MVCCRecord record = new MVCCRecord(key, null, transactionId, commitTime, true);
            
            records.computeIfAbsent(key, k -> new ArrayList<>()).add(record);
        }
        
        public String read(String key, long transactionId) {
            List<MVCCRecord> recordList = records.get(key);
            if (recordList == null) {
                return null;
            }
            
            // Find the most recent committed version visible to this transaction
            MVCCRecord visibleRecord = null;
            for (MVCCRecord record : recordList) {
                if (record.getTransactionId() <= transactionId && 
                    record.getCommitTime() <= transactionId) {
                    if (visibleRecord == null || record.getCommitTime() > visibleRecord.getCommitTime()) {
                        visibleRecord = record;
                    }
                }
            }
            
            if (visibleRecord != null && !visibleRecord.isDeleted()) {
                return visibleRecord.getValue();
            }
            
            return null;
        }
        
        public void garbageCollect(long beforeTransactionId) {
            for (List<MVCCRecord> recordList : records.values()) {
                recordList.removeIf(record -> 
                    record.getTransactionId() < beforeTransactionId && 
                    record.getCommitTime() < beforeTransactionId);
            }
        }
    }
    
    // Transaction manager
    public static class MVCCTransactionManager {
        private final MVCCDatabase database;
        
        public MVCCTransactionManager(MVCCDatabase database) {
            this.database = database;
        }
        
        public long beginTransaction() {
            return database.beginTransaction();
        }
        
        public void commitTransaction(long transactionId) {
            database.commitTransaction(transactionId);
        }
        
        public void write(String key, String value, long transactionId) {
            database.write(key, value, transactionId);
        }
        
        public void delete(String key, long transactionId) {
            database.delete(key, transactionId);
        }
        
        public String read(String key, long transactionId) {
            return database.read(key, transactionId);
        }
    }
}
```

## 16.6 Deadlock Detection and Prevention

Deadlock detection and prevention are crucial for maintaining database performance and availability.

### Key Concepts
- **Deadlock Detection**: Identifying circular waits
- **Deadlock Prevention**: Avoiding conditions that lead to deadlocks
- **Timeout Mechanisms**: Breaking deadlocks with timeouts
- **Lock Ordering**: Consistent lock acquisition order

### Real-World Analogy
Think of a traffic intersection where cars are waiting for each other in a circle. Deadlock detection is like having a traffic controller who can identify and resolve these situations.

### Java Example
```java
public class DeadlockDetectionPreventionExample {
    // Deadlock detector
    public static class DeadlockDetector {
        private final Map<String, Set<String>> waitForGraph = new ConcurrentHashMap<>();
        private final Map<String, String> resourceOwners = new ConcurrentHashMap<>();
        private final Map<String, Set<String>> waitingTransactions = new ConcurrentHashMap<>();
        
        public boolean detectDeadlock() {
            // Build wait-for graph
            for (Map.Entry<String, Set<String>> entry : waitingTransactions.entrySet()) {
                String transaction = entry.getKey();
                Set<String> waitingFor = entry.getValue();
                
                for (String resource : waitingFor) {
                    String owner = resourceOwners.get(resource);
                    if (owner != null) {
                        waitForGraph.computeIfAbsent(transaction, k -> ConcurrentHashMap.newKeySet()).add(owner);
                    }
                }
            }
            
            // Check for cycles using DFS
            Set<String> visited = new HashSet<>();
            Set<String> recursionStack = new HashSet<>();
            
            for (String transaction : waitForGraph.keySet()) {
                if (!visited.contains(transaction)) {
                    if (hasCycle(transaction, visited, recursionStack)) {
                        return true;
                    }
                }
            }
            
            return false;
        }
        
        private boolean hasCycle(String transaction, Set<String> visited, Set<String> recursionStack) {
            visited.add(transaction);
            recursionStack.add(transaction);
            
            Set<String> neighbors = waitForGraph.get(transaction);
            if (neighbors != null) {
                for (String neighbor : neighbors) {
                    if (!visited.contains(neighbor)) {
                        if (hasCycle(neighbor, visited, recursionStack)) {
                            return true;
                        }
                    } else if (recursionStack.contains(neighbor)) {
                        return true;
                    }
                }
            }
            
            recursionStack.remove(transaction);
            return false;
        }
        
        public void addWait(String transaction, String resource) {
            waitingTransactions.computeIfAbsent(transaction, k -> ConcurrentHashMap.newKeySet()).add(resource);
        }
        
        public void removeWait(String transaction, String resource) {
            Set<String> waiting = waitingTransactions.get(transaction);
            if (waiting != null) {
                waiting.remove(resource);
                if (waiting.isEmpty()) {
                    waitingTransactions.remove(transaction);
                }
            }
        }
        
        public void setOwner(String resource, String transaction) {
            resourceOwners.put(resource, transaction);
        }
        
        public void removeOwner(String resource) {
            resourceOwners.remove(resource);
        }
    }
    
    // Deadlock prevention with timeout
    public static class DeadlockPrevention {
        private final Map<String, Long> transactionStartTimes = new ConcurrentHashMap<>();
        private final long timeoutMs;
        
        public DeadlockPrevention(long timeoutMs) {
            this.timeoutMs = timeoutMs;
        }
        
        public void startTransaction(String transactionId) {
            transactionStartTimes.put(transactionId, System.currentTimeMillis());
        }
        
        public boolean isTransactionTimedOut(String transactionId) {
            Long startTime = transactionStartTimes.get(transactionId);
            if (startTime != null) {
                return System.currentTimeMillis() - startTime > timeoutMs;
            }
            return false;
        }
        
        public void endTransaction(String transactionId) {
            transactionStartTimes.remove(transactionId);
        }
    }
    
    // Lock ordering for deadlock prevention
    public static class LockOrdering {
        private final Map<String, Integer> resourceOrder = new ConcurrentHashMap<>();
        private final AtomicInteger orderCounter = new AtomicInteger(0);
        
        public void addResource(String resource) {
            resourceOrder.put(resource, orderCounter.incrementAndGet());
        }
        
        public boolean canAcquireLock(String transactionId, String resource) {
            // Check if transaction already holds locks with higher order
            // This is a simplified implementation
            return true;
        }
        
        public int getResourceOrder(String resource) {
            return resourceOrder.getOrDefault(resource, 0);
        }
    }
}
```

## 16.7 Distributed Transactions

Distributed transactions ensure ACID properties across multiple databases or systems.

### Key Concepts
- **Two-Phase Commit**: Coordinating commits across systems
- **Three-Phase Commit**: Improved version of 2PC
- **Saga Pattern**: Alternative to distributed transactions
- **Compensation**: Undoing changes in case of failure

### Real-World Analogy
Think of a complex business deal involving multiple parties where everyone must agree before the deal is finalized, and if anyone backs out, all changes must be undone.

### Java Example
```java
public class DistributedTransactionsExample {
    // Distributed transaction coordinator
    public static class DistributedTransactionCoordinator {
        private final List<TransactionParticipant> participants = new ArrayList<>();
        
        public void addParticipant(TransactionParticipant participant) {
            participants.add(participant);
        }
        
        public boolean executeTransaction() {
            // Phase 1: Prepare
            List<TransactionParticipant> preparedParticipants = new ArrayList<>();
            
            for (TransactionParticipant participant : participants) {
                if (participant.prepare()) {
                    preparedParticipants.add(participant);
                } else {
                    // Abort all prepared participants
                    for (TransactionParticipant prepared : preparedParticipants) {
                        prepared.abort();
                    }
                    return false;
                }
            }
            
            // Phase 2: Commit
            for (TransactionParticipant participant : preparedParticipants) {
                participant.commit();
            }
            
            return true;
        }
    }
    
    // Transaction participant
    public static class TransactionParticipant {
        private final String participantId;
        private final AtomicBoolean prepared = new AtomicBoolean(false);
        private final AtomicBoolean committed = new AtomicBoolean(false);
        
        public TransactionParticipant(String participantId) {
            this.participantId = participantId;
        }
        
        public boolean prepare() {
            try {
                // Simulate preparation work
                Thread.sleep(100);
                prepared.set(true);
                System.out.println("Participant " + participantId + " prepared");
                return true;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return false;
            }
        }
        
        public void commit() {
            if (prepared.get()) {
                committed.set(true);
                System.out.println("Participant " + participantId + " committed");
            }
        }
        
        public void abort() {
            prepared.set(false);
            System.out.println("Participant " + participantId + " aborted");
        }
        
        public boolean isPrepared() { return prepared.get(); }
        public boolean isCommitted() { return committed.get(); }
    }
    
    // Saga pattern implementation
    public static class SagaPattern {
        private final List<SagaStep> steps = new ArrayList<>();
        
        public void addStep(SagaStep step) {
            steps.add(step);
        }
        
        public boolean executeSaga() {
            List<SagaStep> executedSteps = new ArrayList<>();
            
            try {
                // Execute steps in order
                for (SagaStep step : steps) {
                    if (step.execute()) {
                        executedSteps.add(step);
                    } else {
                        // Compensate executed steps
                        for (int i = executedSteps.size() - 1; i >= 0; i--) {
                            executedSteps.get(i).compensate();
                        }
                        return false;
                    }
                }
                return true;
            } catch (Exception e) {
                // Compensate executed steps
                for (int i = executedSteps.size() - 1; i >= 0; i--) {
                    executedSteps.get(i).compensate();
                }
                return false;
            }
        }
    }
    
    // Saga step
    public static class SagaStep {
        private final String stepId;
        private final Runnable action;
        private final Runnable compensation;
        
        public SagaStep(String stepId, Runnable action, Runnable compensation) {
            this.stepId = stepId;
            this.action = action;
            this.compensation = compensation;
        }
        
        public boolean execute() {
            try {
                action.run();
                System.out.println("Saga step " + stepId + " executed");
                return true;
            } catch (Exception e) {
                System.out.println("Saga step " + stepId + " failed: " + e.getMessage());
                return false;
            }
        }
        
        public void compensate() {
            try {
                compensation.run();
                System.out.println("Saga step " + stepId + " compensated");
            } catch (Exception e) {
                System.out.println("Saga step " + stepId + " compensation failed: " + e.getMessage());
            }
        }
    }
}
```

## 16.8 CAP Theorem and Consistency

The CAP theorem states that a distributed system cannot simultaneously guarantee Consistency, Availability, and Partition tolerance.

### Key Concepts
- **Consistency**: All nodes see the same data
- **Availability**: System remains operational
- **Partition Tolerance**: System continues despite network failures
- **Trade-offs**: Choosing between different guarantees

### Real-World Analogy
Think of a global company where you can't have all three: perfect communication between all offices (consistency), all offices always being open (availability), and the system working even when some offices lose internet connection (partition tolerance).

### Java Example
```java
public class CAPTheoremExample {
    // Consistency-focused system
    public static class ConsistencyFocusedSystem {
        private final Map<String, String> data = new ConcurrentHashMap<>();
        private final AtomicInteger version = new AtomicInteger(0);
        
        public synchronized void write(String key, String value) {
            data.put(key, value);
            version.incrementAndGet();
        }
        
        public synchronized String read(String key) {
            return data.get(key);
        }
        
        public synchronized int getVersion() {
            return version.get();
        }
    }
    
    // Availability-focused system
    public static class AvailabilityFocusedSystem {
        private final Map<String, String> data = new ConcurrentHashMap<>();
        private final AtomicInteger version = new AtomicInteger(0);
        
        public void write(String key, String value) {
            data.put(key, value);
            version.incrementAndGet();
        }
        
        public String read(String key) {
            return data.get(key);
        }
        
        public int getVersion() {
            return version.get();
        }
    }
    
    // Partition-tolerant system
    public static class PartitionTolerantSystem {
        private final Map<String, String> data = new ConcurrentHashMap<>();
        private final AtomicInteger version = new AtomicInteger(0);
        private final AtomicBoolean isPartitioned = new AtomicBoolean(false);
        
        public void write(String key, String value) {
            if (!isPartitioned.get()) {
                data.put(key, value);
                version.incrementAndGet();
            }
        }
        
        public String read(String key) {
            return data.get(key);
        }
        
        public void setPartitioned(boolean partitioned) {
            isPartitioned.set(partitioned);
        }
        
        public boolean isPartitioned() {
            return isPartitioned.get();
        }
    }
    
    // Eventual consistency system
    public static class EventualConsistencySystem {
        private final Map<String, String> data = new ConcurrentHashMap<>();
        private final AtomicInteger version = new AtomicInteger(0);
        private final Queue<String> pendingUpdates = new ConcurrentLinkedQueue<>();
        
        public void write(String key, String value) {
            data.put(key, value);
            version.incrementAndGet();
            pendingUpdates.offer(key + ":" + value);
        }
        
        public String read(String key) {
            return data.get(key);
        }
        
        public void processPendingUpdates() {
            while (!pendingUpdates.isEmpty()) {
                String update = pendingUpdates.poll();
                if (update != null) {
                    String[] parts = update.split(":");
                    if (parts.length == 2) {
                        data.put(parts[0], parts[1]);
                    }
                }
            }
        }
    }
}
```

This comprehensive explanation covers all aspects of database concurrency, providing both theoretical understanding and practical Java examples to illustrate each concept.