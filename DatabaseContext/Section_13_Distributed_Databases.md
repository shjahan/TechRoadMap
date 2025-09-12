# Section 13 – Distributed Databases

## 13.1 CAP Theorem

The CAP theorem states that in a distributed system, you can only guarantee two out of three properties: Consistency, Availability, and Partition tolerance.

### CAP Properties:
- **Consistency**: All nodes see the same data simultaneously
- **Availability**: System remains operational at all times
- **Partition Tolerance**: System continues despite network failures

### Real-World Analogy:
CAP theorem is like choosing between different communication methods:
- **Consistency** = Everyone gets the same message
- **Availability** = Message is always delivered
- **Partition Tolerance** = Works even when some people are unreachable

### Java Example - CAP Theorem Implementation:
```java
public class CAPTheoremExample {
    private List<Connection> nodes;
    private CAPMode mode;
    
    public enum CAPMode {
        CP, // Consistency + Partition Tolerance
        AP, // Availability + Partition Tolerance
        CA  // Consistency + Availability (not possible in distributed systems)
    }
    
    public CAPTheoremExample(List<Connection> nodes, CAPMode mode) {
        this.nodes = nodes;
        this.mode = mode;
    }
    
    // CP Mode: Prioritize Consistency and Partition Tolerance
    public void writeDataCP(String key, String value) throws SQLException {
        // Write to all available nodes
        for (Connection node : nodes) {
            if (isNodeAvailable(node)) {
                String sql = "INSERT INTO data_table (key, value) VALUES (?, ?)";
                try (PreparedStatement stmt = node.prepareStatement(sql)) {
                    stmt.setString(1, key);
                    stmt.setString(2, value);
                    stmt.executeUpdate();
                }
            }
        }
        System.out.println("Data written in CP mode");
    }
    
    // AP Mode: Prioritize Availability and Partition Tolerance
    public void writeDataAP(String key, String value) throws SQLException {
        // Write to any available node
        for (Connection node : nodes) {
            if (isNodeAvailable(node)) {
                String sql = "INSERT INTO data_table (key, value) VALUES (?, ?)";
                try (PreparedStatement stmt = node.prepareStatement(sql)) {
                    stmt.setString(1, key);
                    stmt.setString(2, value);
                    stmt.executeUpdate();
                    break; // Write to first available node
                }
            }
        }
        System.out.println("Data written in AP mode");
    }
    
    // Check if node is available
    private boolean isNodeAvailable(Connection node) {
        try {
            if (node.isClosed()) {
                return false;
            }
            
            try (Statement stmt = node.createStatement();
                 ResultSet rs = stmt.executeQuery("SELECT 1")) {
                return rs.next();
            }
        } catch (SQLException e) {
            return false;
        }
    }
    
    // Read data with consistency check
    public String readDataConsistent(String key) throws SQLException {
        Map<String, String> values = new HashMap<>();
        
        // Read from all available nodes
        for (Connection node : nodes) {
            if (isNodeAvailable(node)) {
                String sql = "SELECT value FROM data_table WHERE key = ?";
                try (PreparedStatement stmt = node.prepareStatement(sql)) {
                    stmt.setString(1, key);
                    
                    try (ResultSet rs = stmt.executeQuery()) {
                        if (rs.next()) {
                            values.put(node.getMetaData().getURL(), rs.getString("value"));
                        }
                    }
                }
            }
        }
        
        // Check for consistency
        if (values.size() > 1) {
            Set<String> uniqueValues = new HashSet<>(values.values());
            if (uniqueValues.size() > 1) {
                System.out.println("Inconsistent data detected across nodes");
                return null;
            }
        }
        
        return values.values().iterator().next();
    }
}
```

## 13.2 Consistency Models

Consistency models define the guarantees about data consistency in distributed systems, ranging from strong to eventual consistency.

### Consistency Levels:
- **Strong Consistency**: All nodes see the same data immediately
- **Eventual Consistency**: Data becomes consistent over time
- **Weak Consistency**: No guarantees about consistency
- **Bounded Staleness**: Data is consistent within a time bound
- **Monotonic Read**: Reads never return older data

### Real-World Analogy:
Consistency models are like different communication methods:
- **Strong Consistency** = Live video call (immediate, synchronized)
- **Eventual Consistency** = Email (eventually delivered)
- **Weak Consistency** = Post-it notes (no guarantees)
- **Bounded Staleness** = Scheduled updates (consistent within time frame)
- **Monotonic Read** = Never going backwards in time

### Java Example - Consistency Models:
```java
public class ConsistencyModels {
    private List<Connection> nodes;
    
    public ConsistencyModels(List<Connection> nodes) {
        this.nodes = nodes;
    }
    
    // Strong consistency: Read from all nodes and verify
    public String readStrongConsistent(String key) throws SQLException {
        Map<String, String> values = new HashMap<>();
        
        for (Connection node : nodes) {
            if (isNodeAvailable(node)) {
                String value = readFromNode(node, key);
                if (value != null) {
                    values.put(node.getMetaData().getURL(), value);
                }
            }
        }
        
        // Verify all values are the same
        if (values.size() > 1) {
            Set<String> uniqueValues = new HashSet<>(values.values());
            if (uniqueValues.size() > 1) {
                throw new SQLException("Strong consistency violation");
            }
        }
        
        return values.values().iterator().next();
    }
    
    // Eventual consistency: Read from any node
    public String readEventualConsistent(String key) throws SQLException {
        for (Connection node : nodes) {
            if (isNodeAvailable(node)) {
                String value = readFromNode(node, key);
                if (value != null) {
                    return value;
                }
            }
        }
        return null;
    }
    
    // Bounded staleness: Read with time constraint
    public String readBoundedStaleness(String key, long maxAgeMs) throws SQLException {
        for (Connection node : nodes) {
            if (isNodeAvailable(node)) {
                String value = readFromNodeWithTimestamp(node, key);
                if (value != null && isWithinTimeBound(value, maxAgeMs)) {
                    return value;
                }
            }
        }
        return null;
    }
    
    // Monotonic read: Track last read timestamp
    private long lastReadTimestamp = 0;
    
    public String readMonotonic(String key) throws SQLException {
        long currentTime = System.currentTimeMillis();
        
        for (Connection node : nodes) {
            if (isNodeAvailable(node)) {
                String value = readFromNodeWithTimestamp(node, key);
                if (value != null && currentTime > lastReadTimestamp) {
                    lastReadTimestamp = currentTime;
                    return value;
                }
            }
        }
        return null;
    }
    
    private String readFromNode(Connection node, String key) throws SQLException {
        String sql = "SELECT value FROM data_table WHERE key = ?";
        try (PreparedStatement stmt = node.prepareStatement(sql)) {
            stmt.setString(1, key);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getString("value");
                }
            }
        }
        return null;
    }
    
    private String readFromNodeWithTimestamp(Connection node, String key) throws SQLException {
        String sql = "SELECT value, timestamp FROM data_table WHERE key = ?";
        try (PreparedStatement stmt = node.prepareStatement(sql)) {
            stmt.setString(1, key);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getString("value");
                }
            }
        }
        return null;
    }
    
    private boolean isWithinTimeBound(String value, long maxAgeMs) {
        // Implementation would check if data is within time bound
        return true; // Simplified for example
    }
}
```

## 13.3 Distributed Transactions

Distributed transactions ensure ACID properties across multiple databases or services, maintaining data consistency in distributed systems.

### Distributed Transaction Types:
- **Two-Phase Commit (2PC)**: Coordinator manages transaction
- **Three-Phase Commit (3PC)**: Reduces blocking in 2PC
- **Saga Pattern**: Compensating transactions
- **TCC Pattern**: Try-Confirm-Cancel transactions
- **Event Sourcing**: Event-based transaction management

### Real-World Analogy:
Distributed transactions are like coordinating a group project:
- **2PC** = Project manager coordinates all team members
- **3PC** = More flexible coordination with backup plans
- **Saga** = Each team member can undo their work
- **TCC** = Try the work, confirm if good, cancel if bad
- **Event Sourcing** = Keep track of all changes

### Java Example - Distributed Transactions:
```java
public class DistributedTransactions {
    private List<Connection> connections;
    private TransactionCoordinator coordinator;
    
    public DistributedTransactions(List<Connection> connections) {
        this.connections = connections;
        this.coordinator = new TransactionCoordinator(connections);
    }
    
    // Two-Phase Commit
    public void executeTwoPhaseCommit() throws SQLException {
        System.out.println("Starting Two-Phase Commit");
        
        // Phase 1: Prepare
        boolean allPrepared = coordinator.prepareAll();
        if (!allPrepared) {
            coordinator.abortAll();
            throw new SQLException("Prepare phase failed");
        }
        
        // Phase 2: Commit
        coordinator.commitAll();
        System.out.println("Two-Phase Commit completed");
    }
    
    // Three-Phase Commit
    public void executeThreePhaseCommit() throws SQLException {
        System.out.println("Starting Three-Phase Commit");
        
        // Phase 1: Can Commit
        boolean allCanCommit = coordinator.canCommitAll();
        if (!allCanCommit) {
            coordinator.abortAll();
            throw new SQLException("Can commit phase failed");
        }
        
        // Phase 2: Pre Commit
        coordinator.preCommitAll();
        
        // Phase 3: Do Commit
        coordinator.doCommitAll();
        System.out.println("Three-Phase Commit completed");
    }
    
    // Saga Pattern
    public void executeSaga() throws SQLException {
        System.out.println("Starting Saga Pattern");
        
        List<SagaStep> steps = new ArrayList<>();
        steps.add(new SagaStep(connections.get(0), "INSERT INTO table1 VALUES (1, 'data1')"));
        steps.add(new SagaStep(connections.get(1), "INSERT INTO table2 VALUES (2, 'data2')"));
        steps.add(new SagaStep(connections.get(2), "INSERT INTO table3 VALUES (3, 'data3')"));
        
        try {
            // Execute steps
            for (SagaStep step : steps) {
                step.execute();
            }
            System.out.println("Saga completed successfully");
        } catch (SQLException e) {
            // Compensate (undo) completed steps
            System.out.println("Saga failed, compensating...");
            for (int i = steps.size() - 1; i >= 0; i--) {
                try {
                    steps.get(i).compensate();
                } catch (SQLException ex) {
                    System.err.println("Compensation failed for step " + i);
                }
            }
            throw e;
        }
    }
    
    // Transaction Coordinator
    private static class TransactionCoordinator {
        private List<Connection> connections;
        
        public TransactionCoordinator(List<Connection> connections) {
            this.connections = connections;
        }
        
        public boolean prepareAll() throws SQLException {
            for (Connection conn : connections) {
                conn.setAutoCommit(false);
                // Simulate prepare phase
                if (!isNodeHealthy(conn)) {
                    return false;
                }
            }
            return true;
        }
        
        public void commitAll() throws SQLException {
            for (Connection conn : connections) {
                conn.commit();
            }
        }
        
        public void abortAll() throws SQLException {
            for (Connection conn : connections) {
                conn.rollback();
            }
        }
        
        public boolean canCommitAll() throws SQLException {
            return prepareAll();
        }
        
        public void preCommitAll() throws SQLException {
            // Pre-commit phase
            System.out.println("Pre-commit phase completed");
        }
        
        public void doCommitAll() throws SQLException {
            commitAll();
        }
        
        private boolean isNodeHealthy(Connection conn) {
            try {
                return !conn.isClosed();
            } catch (SQLException e) {
                return false;
            }
        }
    }
    
    // Saga Step
    private static class SagaStep {
        private Connection connection;
        private String sql;
        private String compensateSql;
        
        public SagaStep(Connection connection, String sql) {
            this.connection = connection;
            this.sql = sql;
            this.compensateSql = generateCompensateSql(sql);
        }
        
        public void execute() throws SQLException {
            try (Statement stmt = connection.createStatement()) {
                stmt.execute(sql);
            }
        }
        
        public void compensate() throws SQLException {
            try (Statement stmt = connection.createStatement()) {
                stmt.execute(compensateSql);
            }
        }
        
        private String generateCompensateSql(String sql) {
            // Generate compensation SQL (simplified)
            if (sql.startsWith("INSERT")) {
                return sql.replace("INSERT", "DELETE");
            }
            return sql;
        }
    }
}
```

## 13.4 Consensus Algorithms

Consensus algorithms ensure that all nodes in a distributed system agree on a single value, even in the presence of failures.

### Consensus Algorithm Types:
- **Raft**: Leader-based consensus algorithm
- **Paxos**: Classic consensus algorithm
- **PBFT**: Practical Byzantine Fault Tolerance
- **POW**: Proof of Work (used in blockchain)
- **POS**: Proof of Stake (used in blockchain)

### Real-World Analogy:
Consensus algorithms are like democratic voting:
- **Raft** = Elected leader makes decisions
- **Paxos** = Complex voting process
- **PBFT** = Voting with some corrupt voters
- **POW** = Proof of work (mining)
- **POS** = Proof of stake (wealth-based voting)

### Java Example - Consensus Algorithms:
```java
public class ConsensusAlgorithms {
    private List<Node> nodes;
    private Node leader;
    
    public ConsensusAlgorithms(List<Node> nodes) {
        this.nodes = nodes;
        this.leader = null;
    }
    
    // Raft Algorithm
    public void raftConsensus() {
        System.out.println("Starting Raft Consensus");
        
        // Elect leader
        leader = electLeader();
        if (leader == null) {
            System.out.println("No leader elected");
            return;
        }
        
        System.out.println("Leader elected: " + leader.getId());
        
        // Leader handles requests
        leader.handleRequests();
        
        // Check for leader failure
        if (!leader.isHealthy()) {
            System.out.println("Leader failed, starting new election");
            raftConsensus();
        }
    }
    
    // Paxos Algorithm
    public void paxosConsensus(Object value) {
        System.out.println("Starting Paxos Consensus for value: " + value);
        
        // Phase 1: Prepare
        int proposalNumber = generateProposalNumber();
        boolean majorityPrepared = preparePhase(proposalNumber);
        
        if (!majorityPrepared) {
            System.out.println("Prepare phase failed");
            return;
        }
        
        // Phase 2: Accept
        boolean majorityAccepted = acceptPhase(proposalNumber, value);
        
        if (majorityAccepted) {
            System.out.println("Consensus reached on value: " + value);
        } else {
            System.out.println("Accept phase failed");
        }
    }
    
    // PBFT Algorithm
    public void pbftConsensus(Object value) {
        System.out.println("Starting PBFT Consensus for value: " + value);
        
        int totalNodes = nodes.size();
        int maxFaultyNodes = (totalNodes - 1) / 3;
        
        // Pre-prepare phase
        if (leader != null && leader.isHealthy()) {
            leader.broadcastPrePrepare(value);
        }
        
        // Prepare phase
        int prepareCount = 0;
        for (Node node : nodes) {
            if (node.hasPrepared(value)) {
                prepareCount++;
            }
        }
        
        if (prepareCount >= 2 * maxFaultyNodes + 1) {
            System.out.println("Prepare phase successful");
            
            // Commit phase
            int commitCount = 0;
            for (Node node : nodes) {
                if (node.hasCommitted(value)) {
                    commitCount++;
                }
            }
            
            if (commitCount >= 2 * maxFaultyNodes + 1) {
                System.out.println("Consensus reached on value: " + value);
            }
        }
    }
    
    private Node electLeader() {
        // Simple leader election (in practice, more complex)
        for (Node node : nodes) {
            if (node.isHealthy() && node.requestVote()) {
                return node;
            }
        }
        return null;
    }
    
    private int generateProposalNumber() {
        return (int) (System.currentTimeMillis() % Integer.MAX_VALUE);
    }
    
    private boolean preparePhase(int proposalNumber) {
        int preparedCount = 0;
        for (Node node : nodes) {
            if (node.prepare(proposalNumber)) {
                preparedCount++;
            }
        }
        return preparedCount > nodes.size() / 2;
    }
    
    private boolean acceptPhase(int proposalNumber, Object value) {
        int acceptedCount = 0;
        for (Node node : nodes) {
            if (node.accept(proposalNumber, value)) {
                acceptedCount++;
            }
        }
        return acceptedCount > nodes.size() / 2;
    }
    
    // Node class
    private static class Node {
        private String id;
        private boolean healthy;
        private Object preparedValue;
        private Object committedValue;
        
        public Node(String id) {
            this.id = id;
            this.healthy = true;
        }
        
        public String getId() { return id; }
        public boolean isHealthy() { return healthy; }
        
        public boolean requestVote() {
            // Simulate vote request
            return Math.random() > 0.3; // 70% chance of voting
        }
        
        public void handleRequests() {
            System.out.println("Node " + id + " handling requests");
        }
        
        public void broadcastPrePrepare(Object value) {
            System.out.println("Node " + id + " broadcasting pre-prepare for: " + value);
        }
        
        public boolean hasPrepared(Object value) {
            return preparedValue != null && preparedValue.equals(value);
        }
        
        public boolean hasCommitted(Object value) {
            return committedValue != null && committedValue.equals(value);
        }
        
        public boolean prepare(int proposalNumber) {
            // Simulate prepare
            return Math.random() > 0.2; // 80% chance of preparing
        }
        
        public boolean accept(int proposalNumber, Object value) {
            // Simulate accept
            preparedValue = value;
            return Math.random() > 0.2; // 80% chance of accepting
        }
    }
}
```

## 13.5 Vector Clocks

Vector clocks are a mechanism for tracking causality in distributed systems, allowing nodes to determine the order of events.

### Vector Clock Properties:
- **Causality**: Track cause-and-effect relationships
- **Partial Ordering**: Determine event ordering
- **Concurrent Events**: Identify simultaneous events
- **Conflict Detection**: Detect conflicting updates
- **Event Ordering**: Maintain event sequence

### Real-World Analogy:
Vector clocks are like timestamps with context:
- **Causality** = Knowing what caused what
- **Partial Ordering** = Some events can be ordered, others can't
- **Concurrent Events** = Events happening at the same time
- **Conflict Detection** = Finding conflicting information
- **Event Ordering** = Keeping track of sequence

### Java Example - Vector Clocks:
```java
import java.util.Map;
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;

public class VectorClocks {
    private Map<String, Integer> clock;
    private String nodeId;
    
    public VectorClocks(String nodeId) {
        this.nodeId = nodeId;
        this.clock = new HashMap<>();
        this.clock.put(nodeId, 0);
    }
    
    // Increment local clock
    public void increment() {
        clock.put(nodeId, clock.get(nodeId) + 1);
    }
    
    // Update clock with received event
    public void update(VectorClocks other) {
        for (Map.Entry<String, Integer> entry : other.clock.entrySet()) {
            String node = entry.getKey();
            int time = entry.getValue();
            
            clock.put(node, Math.max(clock.getOrDefault(node, 0), time));
        }
        increment();
    }
    
    // Compare vector clocks
    public ClockComparison compare(VectorClocks other) {
        boolean thisGreater = true;
        boolean otherGreater = true;
        
        Set<String> allNodes = new HashSet<>(clock.keySet());
        allNodes.addAll(other.clock.keySet());
        
        for (String node : allNodes) {
            int thisTime = clock.getOrDefault(node, 0);
            int otherTime = other.clock.getOrDefault(node, 0);
            
            if (thisTime > otherTime) {
                otherGreater = false;
            } else if (thisTime < otherTime) {
                thisGreater = false;
            }
        }
        
        if (thisGreater && !otherGreater) {
            return ClockComparison.BEFORE;
        } else if (otherGreater && !thisGreater) {
            return ClockComparison.AFTER;
        } else if (thisGreater && otherGreater) {
            return ClockComparison.EQUAL;
        } else {
            return ClockComparison.CONCURRENT;
        }
    }
    
    // Check if this event happened before another
    public boolean happenedBefore(VectorClocks other) {
        return compare(other) == ClockComparison.BEFORE;
    }
    
    // Check if events are concurrent
    public boolean isConcurrent(VectorClocks other) {
        return compare(other) == ClockComparison.CONCURRENT;
    }
    
    // Merge clocks (for conflict resolution)
    public VectorClocks merge(VectorClocks other) {
        VectorClocks merged = new VectorClocks(nodeId);
        
        Set<String> allNodes = new HashSet<>(clock.keySet());
        allNodes.addAll(other.clock.keySet());
        
        for (String node : allNodes) {
            int thisTime = clock.getOrDefault(node, 0);
            int otherTime = other.clock.getOrDefault(node, 0);
            merged.clock.put(node, Math.max(thisTime, otherTime));
        }
        
        return merged;
    }
    
    // Get clock as string
    public String toString() {
        return clock.toString();
    }
    
    // Clock comparison result
    public enum ClockComparison {
        BEFORE,    // This happened before other
        AFTER,     // This happened after other
        EQUAL,     // This and other are the same
        CONCURRENT // This and other are concurrent
    }
    
    // Example usage
    public static void main(String[] args) {
        VectorClocks node1 = new VectorClocks("node1");
        VectorClocks node2 = new VectorClocks("node2");
        VectorClocks node3 = new VectorClocks("node3");
        
        // Node 1 sends message to Node 2
        node1.increment();
        node2.update(node1);
        
        // Node 2 sends message to Node 3
        node2.increment();
        node3.update(node2);
        
        // Node 1 sends another message to Node 3
        node1.increment();
        node3.update(node1);
        
        System.out.println("Node 1 clock: " + node1);
        System.out.println("Node 2 clock: " + node2);
        System.out.println("Node 3 clock: " + node3);
        
        // Compare clocks
        System.out.println("Node 1 vs Node 2: " + node1.compare(node2));
        System.out.println("Node 2 vs Node 3: " + node2.compare(node3));
        System.out.println("Node 1 vs Node 3: " + node1.compare(node3));
    }
}
```

## 13.6 Conflict Resolution

Conflict resolution handles conflicting updates in distributed systems, ensuring data consistency and integrity.

### Conflict Resolution Strategies:
- **Last Writer Wins**: Use timestamp to resolve conflicts
- **First Writer Wins**: Reject conflicting updates
- **Merge**: Combine conflicting values
- **Custom Logic**: Application-specific resolution
- **User Resolution**: Let users decide conflicts

### Real-World Analogy:
Conflict resolution is like resolving disputes:
- **Last Writer Wins** = Most recent decision wins
- **First Writer Wins** = First decision is final
- **Merge** = Combine different decisions
- **Custom Logic** = Use specific rules
- **User Resolution** = Let people decide

### Java Example - Conflict Resolution:
```java
public class ConflictResolution {
    private Map<String, DataVersion> dataStore = new HashMap<>();
    
    // Data version with metadata
    private static class DataVersion {
        private String value;
        private long timestamp;
        private String nodeId;
        private int version;
        
        public DataVersion(String value, long timestamp, String nodeId, int version) {
            this.value = value;
            this.timestamp = timestamp;
            this.nodeId = nodeId;
            this.version = version;
        }
        
        // Getters
        public String getValue() { return value; }
        public long getTimestamp() { return timestamp; }
        public String getNodeId() { return nodeId; }
        public int getVersion() { return version; }
    }
    
    // Last Writer Wins
    public void updateLastWriterWins(String key, String value, String nodeId) {
        DataVersion current = dataStore.get(key);
        long currentTime = System.currentTimeMillis();
        
        if (current == null || currentTime > current.getTimestamp()) {
            dataStore.put(key, new DataVersion(value, currentTime, nodeId, 
                current != null ? current.getVersion() + 1 : 1));
            System.out.println("Data updated (Last Writer Wins): " + key + " = " + value);
        } else {
            System.out.println("Update rejected (Last Writer Wins): " + key);
        }
    }
    
    // First Writer Wins
    public void updateFirstWriterWins(String key, String value, String nodeId) {
        DataVersion current = dataStore.get(key);
        
        if (current == null) {
            dataStore.put(key, new DataVersion(value, System.currentTimeMillis(), nodeId, 1));
            System.out.println("Data updated (First Writer Wins): " + key + " = " + value);
        } else {
            System.out.println("Update rejected (First Writer Wins): " + key);
        }
    }
    
    // Merge conflicts
    public void updateMerge(String key, String value, String nodeId) {
        DataVersion current = dataStore.get(key);
        
        if (current == null) {
            dataStore.put(key, new DataVersion(value, System.currentTimeMillis(), nodeId, 1));
        } else {
            // Merge values
            String mergedValue = mergeValues(current.getValue(), value);
            dataStore.put(key, new DataVersion(mergedValue, System.currentTimeMillis(), 
                nodeId, current.getVersion() + 1));
            System.out.println("Data merged: " + key + " = " + mergedValue);
        }
    }
    
    // Custom conflict resolution
    public void updateCustom(String key, String value, String nodeId) {
        DataVersion current = dataStore.get(key);
        
        if (current == null) {
            dataStore.put(key, new DataVersion(value, System.currentTimeMillis(), nodeId, 1));
        } else {
            // Custom resolution logic
            String resolvedValue = resolveConflict(current, value, nodeId);
            dataStore.put(key, new DataVersion(resolvedValue, System.currentTimeMillis(), 
                nodeId, current.getVersion() + 1));
            System.out.println("Data resolved (Custom): " + key + " = " + resolvedValue);
        }
    }
    
    // User resolution
    public void updateUserResolution(String key, String value, String nodeId) {
        DataVersion current = dataStore.get(key);
        
        if (current == null) {
            dataStore.put(key, new DataVersion(value, System.currentTimeMillis(), nodeId, 1));
        } else {
            // Present conflict to user
            System.out.println("Conflict detected for key: " + key);
            System.out.println("Current value: " + current.getValue());
            System.out.println("New value: " + value);
            System.out.println("Please resolve conflict...");
            
            // In real implementation, this would be handled by UI
            String resolvedValue = resolveUserConflict(current.getValue(), value);
            dataStore.put(key, new DataVersion(resolvedValue, System.currentTimeMillis(), 
                nodeId, current.getVersion() + 1));
        }
    }
    
    private String mergeValues(String current, String newValue) {
        // Simple merge: combine values
        return current + " + " + newValue;
    }
    
    private String resolveConflict(DataVersion current, String newValue, String nodeId) {
        // Custom resolution: prefer longer values
        if (newValue.length() > current.getValue().length()) {
            return newValue;
        } else {
            return current.getValue();
        }
    }
    
    private String resolveUserConflict(String current, String newValue) {
        // In real implementation, this would be handled by UI
        // For example, return the new value
        return newValue;
    }
    
    // Get data
    public String getData(String key) {
        DataVersion version = dataStore.get(key);
        return version != null ? version.getValue() : null;
    }
    
    // Get data with metadata
    public DataVersion getDataVersion(String key) {
        return dataStore.get(key);
    }
}
```

## 13.7 Eventual Consistency

Eventual consistency guarantees that if no new updates are made to a given data item, all reads will eventually return the last updated value.

### Eventual Consistency Properties:
- **Convergence**: All replicas eventually converge
- **Monotonic Read**: Reads never return older data
- **Monotonic Write**: Writes are applied in order
- **Read Your Writes**: Reads see your own writes
- **Causal Consistency**: Causally related events are ordered

### Real-World Analogy:
Eventual consistency is like spreading news:
- **Convergence** = Everyone eventually hears the news
- **Monotonic Read** = You never hear older news
- **Monotonic Write** = News is spread in order
- **Read Your Writes** = You see your own news first
- **Causal Consistency** = Related news is spread in order

### Java Example - Eventual Consistency:
```java
public class EventualConsistency {
    private Map<String, List<DataVersion>> replicas = new HashMap<>();
    private Map<String, Long> lastReadTimestamp = new HashMap<>();
    
    // Data version with timestamp
    private static class DataVersion {
        private String value;
        private long timestamp;
        private String nodeId;
        
        public DataVersion(String value, long timestamp, String nodeId) {
            this.value = value;
            this.timestamp = timestamp;
            this.nodeId = nodeId;
        }
        
        // Getters
        public String getValue() { return value; }
        public long getTimestamp() { return timestamp; }
        public String getNodeId() { return nodeId; }
    }
    
    // Write data to all replicas
    public void write(String key, String value, String nodeId) {
        long timestamp = System.currentTimeMillis();
        DataVersion version = new DataVersion(value, timestamp, nodeId);
        
        // Write to all replicas
        for (String replicaId : replicas.keySet()) {
            replicas.get(replicaId).add(version);
        }
        
        System.out.println("Data written: " + key + " = " + value + " at " + timestamp);
    }
    
    // Read data with eventual consistency
    public String read(String key, String nodeId) {
        List<DataVersion> versions = replicas.get(nodeId);
        if (versions == null || versions.isEmpty()) {
            return null;
        }
        
        // Get latest version
        DataVersion latest = versions.stream()
            .max((v1, v2) -> Long.compare(v1.getTimestamp(), v2.getTimestamp()))
            .orElse(null);
        
        if (latest != null) {
            // Update last read timestamp for monotonic read
            lastReadTimestamp.put(nodeId, latest.getTimestamp());
            return latest.getValue();
        }
        
        return null;
    }
    
    // Monotonic read: never return older data
    public String readMonotonic(String key, String nodeId) {
        List<DataVersion> versions = replicas.get(nodeId);
        if (versions == null || versions.isEmpty()) {
            return null;
        }
        
        long lastRead = lastReadTimestamp.getOrDefault(nodeId, 0L);
        
        // Get latest version after last read
        DataVersion latest = versions.stream()
            .filter(v -> v.getTimestamp() > lastRead)
            .max((v1, v2) -> Long.compare(v1.getTimestamp(), v2.getTimestamp()))
            .orElse(null);
        
        if (latest != null) {
            lastReadTimestamp.put(nodeId, latest.getTimestamp());
            return latest.getValue();
        }
        
        return null;
    }
    
    // Check convergence across replicas
    public boolean isConverged(String key) {
        Set<String> values = new HashSet<>();
        
        for (String replicaId : replicas.keySet()) {
            List<DataVersion> versions = replicas.get(replicaId);
            if (versions != null && !versions.isEmpty()) {
                DataVersion latest = versions.stream()
                    .max((v1, v2) -> Long.compare(v1.getTimestamp(), v2.getTimestamp()))
                    .orElse(null);
                
                if (latest != null) {
                    values.add(latest.getValue());
                }
            }
        }
        
        return values.size() <= 1;
    }
    
    // Synchronize replicas (eventual consistency)
    public void synchronizeReplicas() {
        System.out.println("Synchronizing replicas...");
        
        for (String replicaId : replicas.keySet()) {
            List<DataVersion> versions = replicas.get(replicaId);
            
            // Get latest version from this replica
            DataVersion latest = versions.stream()
                .max((v1, v2) -> Long.compare(v1.getTimestamp(), v2.getTimestamp()))
                .orElse(null);
            
            if (latest != null) {
                // Propagate to other replicas
                for (String otherReplicaId : replicas.keySet()) {
                    if (!otherReplicaId.equals(replicaId)) {
                        List<DataVersion> otherVersions = replicas.get(otherReplicaId);
                        if (!otherVersions.contains(latest)) {
                            otherVersions.add(latest);
                        }
                    }
                }
            }
        }
        
        System.out.println("Replicas synchronized");
    }
    
    // Initialize replicas
    public void initializeReplicas(String... replicaIds) {
        for (String replicaId : replicaIds) {
            replicas.put(replicaId, new ArrayList<>());
        }
    }
}
```

## 13.8 CRDTs (Conflict-free Replicated Data Types)

CRDTs are data structures that can be replicated across multiple nodes and updated independently without coordination, automatically resolving conflicts.

### CRDT Types:
- **G-Counter**: Grow-only counter
- **PN-Counter**: Positive-negative counter
- **G-Set**: Grow-only set
- **2P-Set**: Two-phase set
- **OR-Set**: Observed-removed set
- **LWW-Register**: Last-writer-wins register

### Real-World Analogy:
CRDTs are like collaborative documents:
- **G-Counter** = Vote counter (only increases)
- **PN-Counter** = Score counter (increases and decreases)
- **G-Set** = List of attendees (only additions)
- **2P-Set** = List with additions and deletions
- **OR-Set** = List with observed removals
- **LWW-Register** = Last edit wins

### Java Example - CRDTs:
```java
import java.util.Map;
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;
import java.util.List;
import java.util.ArrayList;

public class CRDTs {
    
    // G-Counter (Grow-only counter)
    public static class GCounter {
        private Map<String, Integer> counts = new HashMap<>();
        private String nodeId;
        
        public GCounter(String nodeId) {
            this.nodeId = nodeId;
            counts.put(nodeId, 0);
        }
        
        public void increment() {
            counts.put(nodeId, counts.get(nodeId) + 1);
        }
        
        public int getValue() {
            return counts.values().stream().mapToInt(Integer::intValue).sum();
        }
        
        public void merge(GCounter other) {
            for (Map.Entry<String, Integer> entry : other.counts.entrySet()) {
                String node = entry.getKey();
                int count = entry.getValue();
                counts.put(node, Math.max(counts.getOrDefault(node, 0), count));
            }
        }
    }
    
    // PN-Counter (Positive-negative counter)
    public static class PNCounter {
        private Map<String, Integer> positive = new HashMap<>();
        private Map<String, Integer> negative = new HashMap<>();
        private String nodeId;
        
        public PNCounter(String nodeId) {
            this.nodeId = nodeId;
            positive.put(nodeId, 0);
            negative.put(nodeId, 0);
        }
        
        public void increment() {
            positive.put(nodeId, positive.get(nodeId) + 1);
        }
        
        public void decrement() {
            negative.put(nodeId, negative.get(nodeId) + 1);
        }
        
        public int getValue() {
            int posSum = positive.values().stream().mapToInt(Integer::intValue).sum();
            int negSum = negative.values().stream().mapToInt(Integer::intValue).sum();
            return posSum - negSum;
        }
        
        public void merge(PNCounter other) {
            for (Map.Entry<String, Integer> entry : other.positive.entrySet()) {
                String node = entry.getKey();
                int count = entry.getValue();
                positive.put(node, Math.max(positive.getOrDefault(node, 0), count));
            }
            
            for (Map.Entry<String, Integer> entry : other.negative.entrySet()) {
                String node = entry.getKey();
                int count = entry.getValue();
                negative.put(node, Math.max(negative.getOrDefault(node, 0), count));
            }
        }
    }
    
    // G-Set (Grow-only set)
    public static class GSet {
        private Set<String> elements = new HashSet<>();
        
        public void add(String element) {
            elements.add(element);
        }
        
        public boolean contains(String element) {
            return elements.contains(element);
        }
        
        public Set<String> getElements() {
            return new HashSet<>(elements);
        }
        
        public void merge(GSet other) {
            elements.addAll(other.elements);
        }
    }
    
    // OR-Set (Observed-removed set)
    public static class ORSet {
        private Map<String, Set<String>> added = new HashMap<>();
        private Map<String, Set<String>> removed = new HashMap<>();
        private String nodeId;
        
        public ORSet(String nodeId) {
            this.nodeId = nodeId;
        }
        
        public void add(String element) {
            String tag = nodeId + ":" + System.currentTimeMillis();
            added.computeIfAbsent(element, k -> new HashSet<>()).add(tag);
        }
        
        public void remove(String element) {
            if (added.containsKey(element)) {
                removed.computeIfAbsent(element, k -> new HashSet<>()).addAll(added.get(element));
            }
        }
        
        public boolean contains(String element) {
            if (!added.containsKey(element)) {
                return false;
            }
            
            Set<String> addedTags = added.get(element);
            Set<String> removedTags = removed.getOrDefault(element, new HashSet<>());
            
            return !addedTags.isEmpty() && !removedTags.containsAll(addedTags);
        }
        
        public Set<String> getElements() {
            Set<String> result = new HashSet<>();
            for (String element : added.keySet()) {
                if (contains(element)) {
                    result.add(element);
                }
            }
            return result;
        }
        
        public void merge(ORSet other) {
            for (Map.Entry<String, Set<String>> entry : other.added.entrySet()) {
                String element = entry.getKey();
                Set<String> tags = entry.getValue();
                added.computeIfAbsent(element, k -> new HashSet<>()).addAll(tags);
            }
            
            for (Map.Entry<String, Set<String>> entry : other.removed.entrySet()) {
                String element = entry.getKey();
                Set<String> tags = entry.getValue();
                removed.computeIfAbsent(element, k -> new HashSet<>()).addAll(tags);
            }
        }
    }
    
    // LWW-Register (Last-writer-wins register)
    public static class LWWRegister {
        private String value;
        private long timestamp;
        private String nodeId;
        
        public LWWRegister(String nodeId) {
            this.nodeId = nodeId;
            this.value = null;
            this.timestamp = 0;
        }
        
        public void set(String value) {
            this.value = value;
            this.timestamp = System.currentTimeMillis();
        }
        
        public String get() {
            return value;
        }
        
        public void merge(LWWRegister other) {
            if (other.timestamp > this.timestamp) {
                this.value = other.value;
                this.timestamp = other.timestamp;
                this.nodeId = other.nodeId;
            }
        }
    }
    
    // Example usage
    public static void main(String[] args) {
        // G-Counter example
        GCounter counter1 = new GCounter("node1");
        GCounter counter2 = new GCounter("node2");
        
        counter1.increment();
        counter1.increment();
        counter2.increment();
        
        counter1.merge(counter2);
        System.out.println("G-Counter value: " + counter1.getValue());
        
        // G-Set example
        GSet set1 = new GSet();
        GSet set2 = new GSet();
        
        set1.add("apple");
        set1.add("banana");
        set2.add("banana");
        set2.add("cherry");
        
        set1.merge(set2);
        System.out.println("G-Set elements: " + set1.getElements());
        
        // OR-Set example
        ORSet orSet1 = new ORSet("node1");
        ORSet orSet2 = new ORSet("node2");
        
        orSet1.add("apple");
        orSet1.add("banana");
        orSet2.add("banana");
        orSet2.add("cherry");
        
        orSet1.remove("banana");
        orSet1.merge(orSet2);
        System.out.println("OR-Set elements: " + orSet1.getElements());
    }
}
```