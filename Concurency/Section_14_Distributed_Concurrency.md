# Section 14 – Distributed Concurrency

## 14.1 Distributed Locks

Distributed locks provide synchronization across multiple machines in a distributed system, ensuring that only one process can access a shared resource at a time.

### Key Concepts
- **Consensus**: Agreement among distributed processes
- **Fault Tolerance**: Handling node failures
- **Performance**: Minimizing lock overhead
- **Deadlock Prevention**: Avoiding distributed deadlocks

### Real-World Analogy
Think of a shared office building where only one person can use the conference room at a time, and they need to coordinate with the building's management system to reserve it.

### Java Example
```java
public class DistributedLocksExample {
    // Simple distributed lock interface
    public interface DistributedLock {
        boolean tryLock(String resource, long timeoutMs);
        void unlock(String resource);
        boolean isLocked(String resource);
    }
    
    // Redis-based distributed lock
    public static class RedisDistributedLock implements DistributedLock {
        private final Jedis jedis;
        private final String lockPrefix = "lock:";
        private final int defaultTimeout = 30; // seconds
        
        public RedisDistributedLock(String host, int port) {
            this.jedis = new Jedis(host, port);
        }
        
        @Override
        public boolean tryLock(String resource, long timeoutMs) {
            String lockKey = lockPrefix + resource;
            String lockValue = Thread.currentThread().getName() + ":" + System.currentTimeMillis();
            
            // Try to acquire lock with expiration
            String result = jedis.set(lockKey, lockValue, "NX", "EX", defaultTimeout);
            return "OK".equals(result);
        }
        
        @Override
        public void unlock(String resource) {
            String lockKey = lockPrefix + resource;
            jedis.del(lockKey);
        }
        
        @Override
        public boolean isLocked(String resource) {
            String lockKey = lockPrefix + resource;
            return jedis.exists(lockKey);
        }
    }
    
    // ZooKeeper-based distributed lock
    public static class ZooKeeperDistributedLock implements DistributedLock {
        private final ZooKeeper zooKeeper;
        private final String lockPrefix = "/locks/";
        private final Map<String, String> lockPaths = new ConcurrentHashMap<>();
        
        public ZooKeeperDistributedLock(String connectString) throws Exception {
            this.zooKeeper = new ZooKeeper(connectString, 3000, null);
        }
        
        @Override
        public boolean tryLock(String resource, long timeoutMs) {
            try {
                String lockPath = lockPrefix + resource;
                String createdPath = zooKeeper.create(lockPath, 
                    Thread.currentThread().getName().getBytes(), 
                    ZooDefs.Ids.OPEN_ACL_UNSAFE, 
                    CreateMode.EPHEMERAL);
                
                lockPaths.put(resource, createdPath);
                return true;
            } catch (Exception e) {
                return false;
            }
        }
        
        @Override
        public void unlock(String resource) {
            try {
                String lockPath = lockPaths.get(resource);
                if (lockPath != null) {
                    zooKeeper.delete(lockPath, -1);
                    lockPaths.remove(resource);
                }
            } catch (Exception e) {
                // Handle unlock error
            }
        }
        
        @Override
        public boolean isLocked(String resource) {
            try {
                String lockPath = lockPrefix + resource;
                return zooKeeper.exists(lockPath, false) != null;
            } catch (Exception e) {
                return false;
            }
        }
    }
    
    // Distributed resource manager
    public static class DistributedResourceManager {
        private final DistributedLock lock;
        private final String resourceName;
        
        public DistributedResourceManager(DistributedLock lock, String resourceName) {
            this.lock = lock;
            this.resourceName = resourceName;
        }
        
        public boolean acquireResource(long timeoutMs) {
            return lock.tryLock(resourceName, timeoutMs);
        }
        
        public void releaseResource() {
            lock.unlock(resourceName);
        }
        
        public void useResource() {
            if (acquireResource(5000)) {
                try {
                    System.out.println(Thread.currentThread().getName() + " using resource: " + resourceName);
                    Thread.sleep(2000); // Simulate resource usage
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    releaseResource();
                }
            } else {
                System.out.println(Thread.currentThread().getName() + " failed to acquire resource: " + resourceName);
            }
        }
    }
}
```

## 14.2 Consensus Algorithms

Consensus algorithms ensure that all nodes in a distributed system agree on a single value, even in the presence of failures.

### Key Concepts
- **Agreement**: All nodes agree on the same value
- **Validity**: The agreed value is valid
- **Termination**: The algorithm eventually terminates
- **Fault Tolerance**: Handles node failures

### Real-World Analogy
Think of a board meeting where all members need to agree on a decision, even if some members are absent or have different opinions.

### Java Example
```java
public class ConsensusAlgorithmsExample {
    // Simple consensus algorithm
    public static class SimpleConsensus {
        private final List<String> nodes;
        private final Map<String, String> proposals = new ConcurrentHashMap<>();
        private final Map<String, Integer> votes = new ConcurrentHashMap<>();
        private final Object lock = new Object();
        
        public SimpleConsensus(List<String> nodes) {
            this.nodes = new ArrayList<>(nodes);
        }
        
        public String propose(String nodeId, String value) {
            synchronized (lock) {
                proposals.put(nodeId, value);
                votes.put(value, votes.getOrDefault(value, 0) + 1);
                
                // Check if we have a majority
                int totalVotes = votes.values().stream().mapToInt(Integer::intValue).sum();
                for (Map.Entry<String, Integer> entry : votes.entrySet()) {
                    if (entry.getValue() > totalVotes / 2) {
                        return entry.getKey();
                    }
                }
                
                return null; // No consensus yet
            }
        }
        
        public String getConsensus() {
            synchronized (lock) {
                int totalVotes = votes.values().stream().mapToInt(Integer::intValue).sum();
                for (Map.Entry<String, Integer> entry : votes.entrySet()) {
                    if (entry.getValue() > totalVotes / 2) {
                        return entry.getKey();
                    }
                }
                return null;
            }
        }
    }
    
    // Raft algorithm simulation
    public static class RaftNode {
        public enum State { FOLLOWER, CANDIDATE, LEADER }
        
        private State state = State.FOLLOWER;
        private final String nodeId;
        private final List<String> otherNodes;
        private final AtomicInteger currentTerm = new AtomicInteger(0);
        private final AtomicInteger votedFor = new AtomicInteger(-1);
        private final AtomicInteger logIndex = new AtomicInteger(0);
        private final Map<String, String> log = new ConcurrentHashMap<>();
        
        public RaftNode(String nodeId, List<String> otherNodes) {
            this.nodeId = nodeId;
            this.otherNodes = new ArrayList<>(otherNodes);
        }
        
        public void startElection() {
            if (state == State.FOLLOWER) {
                state = State.CANDIDATE;
                currentTerm.incrementAndGet();
                votedFor.set(Integer.parseInt(nodeId));
                
                System.out.println("Node " + nodeId + " starting election for term " + currentTerm.get());
                
                // Request votes from other nodes
                int votes = 1; // Vote for self
                for (String otherNode : otherNodes) {
                    if (requestVote(otherNode)) {
                        votes++;
                    }
                }
                
                if (votes > otherNodes.size() / 2) {
                    becomeLeader();
                } else {
                    state = State.FOLLOWER;
                }
            }
        }
        
        private boolean requestVote(String otherNode) {
            // Simulate vote request
            return Math.random() > 0.5; // Random vote for simulation
        }
        
        private void becomeLeader() {
            state = State.LEADER;
            System.out.println("Node " + nodeId + " became leader for term " + currentTerm.get());
        }
        
        public void appendEntry(String entry) {
            if (state == State.LEADER) {
                logIndex.incrementAndGet();
                log.put(String.valueOf(logIndex.get()), entry);
                System.out.println("Leader " + nodeId + " appended entry: " + entry);
            }
        }
        
        public State getState() { return state; }
        public int getCurrentTerm() { return currentTerm.get(); }
    }
}
```

## 14.3 Two-Phase Commit

Two-Phase Commit (2PC) is a distributed algorithm that ensures all nodes either commit or abort a transaction.

### Key Concepts
- **Prepare Phase**: Coordinator asks all participants to prepare
- **Commit Phase**: Coordinator tells all participants to commit or abort
- **Blocking**: Can block if coordinator fails
- **Consistency**: Ensures ACID properties

### Real-World Analogy
Think of a wedding where the officiant asks both partners if they're ready to commit, and only proceeds if both say yes.

### Java Example
```java
public class TwoPhaseCommitExample {
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
    
    // Two-phase commit coordinator
    public static class TwoPhaseCommitCoordinator {
        private final List<TransactionParticipant> participants;
        
        public TwoPhaseCommitCoordinator(List<TransactionParticipant> participants) {
            this.participants = new ArrayList<>(participants);
        }
        
        public boolean executeTransaction() {
            System.out.println("Starting two-phase commit");
            
            // Phase 1: Prepare
            boolean allPrepared = true;
            for (TransactionParticipant participant : participants) {
                if (!participant.prepare()) {
                    allPrepared = false;
                    break;
                }
            }
            
            if (allPrepared) {
                // Phase 2: Commit
                System.out.println("All participants prepared, committing");
                for (TransactionParticipant participant : participants) {
                    participant.commit();
                }
                return true;
            } else {
                // Phase 2: Abort
                System.out.println("Some participants failed to prepare, aborting");
                for (TransactionParticipant participant : participants) {
                    participant.abort();
                }
                return false;
            }
        }
    }
}
```

## 14.4 Three-Phase Commit

Three-Phase Commit (3PC) is an improvement over 2PC that reduces blocking by adding a pre-commit phase.

### Key Concepts
- **Pre-commit Phase**: Additional phase to reduce blocking
- **Non-blocking**: Can handle coordinator failures
- **Complexity**: More complex than 2PC
- **Performance**: Better performance than 2PC

### Real-World Analogy
Think of a three-step approval process where you first check if everyone is available, then get preliminary approval, and finally get final approval.

### Java Example
```java
public class ThreePhaseCommitExample {
    // Three-phase commit participant
    public static class ThreePhaseCommitParticipant {
        private final String participantId;
        private final AtomicBoolean prepared = new AtomicBoolean(false);
        private final AtomicBoolean preCommitted = new AtomicBoolean(false);
        private final AtomicBoolean committed = new AtomicBoolean(false);
        
        public ThreePhaseCommitParticipant(String participantId) {
            this.participantId = participantId;
        }
        
        public boolean prepare() {
            try {
                Thread.sleep(100);
                prepared.set(true);
                System.out.println("Participant " + participantId + " prepared");
                return true;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return false;
            }
        }
        
        public void preCommit() {
            if (prepared.get()) {
                preCommitted.set(true);
                System.out.println("Participant " + participantId + " pre-committed");
            }
        }
        
        public void commit() {
            if (preCommitted.get()) {
                committed.set(true);
                System.out.println("Participant " + participantId + " committed");
            }
        }
        
        public void abort() {
            prepared.set(false);
            preCommitted.set(false);
            System.out.println("Participant " + participantId + " aborted");
        }
        
        public boolean isPrepared() { return prepared.get(); }
        public boolean isPreCommitted() { return preCommitted.get(); }
        public boolean isCommitted() { return committed.get(); }
    }
    
    // Three-phase commit coordinator
    public static class ThreePhaseCommitCoordinator {
        private final List<ThreePhaseCommitParticipant> participants;
        
        public ThreePhaseCommitCoordinator(List<ThreePhaseCommitParticipant> participants) {
            this.participants = new ArrayList<>(participants);
        }
        
        public boolean executeTransaction() {
            System.out.println("Starting three-phase commit");
            
            // Phase 1: Prepare
            boolean allPrepared = true;
            for (ThreePhaseCommitParticipant participant : participants) {
                if (!participant.prepare()) {
                    allPrepared = false;
                    break;
                }
            }
            
            if (!allPrepared) {
                System.out.println("Some participants failed to prepare, aborting");
                for (ThreePhaseCommitParticipant participant : participants) {
                    participant.abort();
                }
                return false;
            }
            
            // Phase 2: Pre-commit
            System.out.println("All participants prepared, pre-committing");
            for (ThreePhaseCommitParticipant participant : participants) {
                participant.preCommit();
            }
            
            // Phase 3: Commit
            System.out.println("All participants pre-committed, committing");
            for (ThreePhaseCommitParticipant participant : participants) {
                participant.commit();
            }
            
            return true;
        }
    }
}
```

## 14.5 Raft Algorithm

Raft is a consensus algorithm designed to be understandable and implementable, with strong consistency guarantees.

### Key Concepts
- **Leader Election**: Electing a leader to handle requests
- **Log Replication**: Replicating log entries across nodes
- **Safety**: Ensuring consistency and correctness
- **Split-brain Prevention**: Avoiding multiple leaders

### Real-World Analogy
Think of a company where employees elect a CEO who makes all decisions and ensures everyone follows the same policies.

### Java Example
```java
public class RaftAlgorithmExample {
    // Raft node implementation
    public static class RaftNode {
        public enum State { FOLLOWER, CANDIDATE, LEADER }
        
        private State state = State.FOLLOWER;
        private final String nodeId;
        private final List<String> otherNodes;
        private final AtomicInteger currentTerm = new AtomicInteger(0);
        private final AtomicInteger votedFor = new AtomicInteger(-1);
        private final AtomicInteger logIndex = new AtomicInteger(0);
        private final Map<String, String> log = new ConcurrentHashMap<>();
        private final AtomicLong lastHeartbeat = new AtomicLong(System.currentTimeMillis());
        
        public RaftNode(String nodeId, List<String> otherNodes) {
            this.nodeId = nodeId;
            this.otherNodes = new ArrayList<>(otherNodes);
        }
        
        public void startElection() {
            if (state == State.FOLLOWER) {
                state = State.CANDIDATE;
                currentTerm.incrementAndGet();
                votedFor.set(Integer.parseInt(nodeId));
                
                System.out.println("Node " + nodeId + " starting election for term " + currentTerm.get());
                
                // Request votes from other nodes
                int votes = 1; // Vote for self
                for (String otherNode : otherNodes) {
                    if (requestVote(otherNode)) {
                        votes++;
                    }
                }
                
                if (votes > otherNodes.size() / 2) {
                    becomeLeader();
                } else {
                    state = State.FOLLOWER;
                }
            }
        }
        
        private boolean requestVote(String otherNode) {
            // Simulate vote request
            return Math.random() > 0.5; // Random vote for simulation
        }
        
        private void becomeLeader() {
            state = State.LEADER;
            System.out.println("Node " + nodeId + " became leader for term " + currentTerm.get());
            startHeartbeat();
        }
        
        private void startHeartbeat() {
            new Thread(() -> {
                while (state == State.LEADER) {
                    try {
                        Thread.sleep(1000); // Send heartbeat every second
                        sendHeartbeat();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            }).start();
        }
        
        private void sendHeartbeat() {
            for (String otherNode : otherNodes) {
                // Simulate sending heartbeat
                System.out.println("Leader " + nodeId + " sending heartbeat to " + otherNode);
            }
        }
        
        public void appendEntry(String entry) {
            if (state == State.LEADER) {
                logIndex.incrementAndGet();
                log.put(String.valueOf(logIndex.get()), entry);
                System.out.println("Leader " + nodeId + " appended entry: " + entry);
            }
        }
        
        public State getState() { return state; }
        public int getCurrentTerm() { return currentTerm.get(); }
    }
}
```

## 14.6 Paxos Algorithm

Paxos is a family of protocols for solving consensus in a network of unreliable processors.

### Key Concepts
- **Proposers**: Propose values for consensus
- **Acceptors**: Accept or reject proposals
- **Learners**: Learn the chosen value
- **Majority**: Requires majority agreement

### Real-World Analogy
Think of a voting system where candidates propose policies, voters accept or reject them, and the final result is determined by majority vote.

### Java Example
```java
public class PaxosAlgorithmExample {
    // Paxos proposer
    public static class PaxosProposer {
        private final String proposerId;
        private final List<String> acceptors;
        private final AtomicInteger proposalNumber = new AtomicInteger(0);
        
        public PaxosProposer(String proposerId, List<String> acceptors) {
            this.proposerId = proposerId;
            this.acceptors = new ArrayList<>(acceptors);
        }
        
        public String propose(String value) {
            int proposalNum = proposalNumber.incrementAndGet();
            System.out.println("Proposer " + proposerId + " proposing value: " + value + " with number: " + proposalNum);
            
            // Phase 1: Prepare
            int promises = 0;
            for (String acceptor : acceptors) {
                if (prepare(acceptor, proposalNum)) {
                    promises++;
                }
            }
            
            if (promises > acceptors.size() / 2) {
                // Phase 2: Accept
                int accepts = 0;
                for (String acceptor : acceptors) {
                    if (accept(acceptor, proposalNum, value)) {
                        accepts++;
                    }
                }
                
                if (accepts > acceptors.size() / 2) {
                    System.out.println("Value " + value + " accepted by majority");
                    return value;
                }
            }
            
            return null; // No consensus
        }
        
        private boolean prepare(String acceptor, int proposalNum) {
            // Simulate prepare request
            return Math.random() > 0.3; // 70% success rate
        }
        
        private boolean accept(String acceptor, int proposalNum, String value) {
            // Simulate accept request
            return Math.random() > 0.2; // 80% success rate
        }
    }
    
    // Paxos acceptor
    public static class PaxosAcceptor {
        private final String acceptorId;
        private final AtomicInteger promisedProposal = new AtomicInteger(-1);
        private final AtomicInteger acceptedProposal = new AtomicInteger(-1);
        private final AtomicReference<String> acceptedValue = new AtomicReference<>();
        
        public PaxosAcceptor(String acceptorId) {
            this.acceptorId = acceptorId;
        }
        
        public boolean prepare(int proposalNum) {
            if (proposalNum > promisedProposal.get()) {
                promisedProposal.set(proposalNum);
                System.out.println("Acceptor " + acceptorId + " promised proposal " + proposalNum);
                return true;
            }
            return false;
        }
        
        public boolean accept(int proposalNum, String value) {
            if (proposalNum >= promisedProposal.get()) {
                acceptedProposal.set(proposalNum);
                acceptedValue.set(value);
                System.out.println("Acceptor " + acceptorId + " accepted proposal " + proposalNum + " with value " + value);
                return true;
            }
            return false;
        }
        
        public String getAcceptedValue() {
            return acceptedValue.get();
        }
    }
}
```

## 14.7 Vector Clocks

Vector clocks are a mechanism for capturing causality in distributed systems by maintaining a vector of logical timestamps.

### Key Concepts
- **Causality**: Determining if one event caused another
- **Logical Time**: Time based on event ordering
- **Vector Timestamps**: Array of timestamps for each process
- **Concurrent Events**: Events that are not causally related

### Real-World Analogy
Think of a project where each team member keeps track of when they last heard from every other team member, allowing them to determine the order of events.

### Java Example
```java
public class VectorClocksExample {
    // Vector clock implementation
    public static class VectorClock {
        private final Map<String, Integer> clock = new ConcurrentHashMap<>();
        private final String processId;
        
        public VectorClock(String processId, List<String> allProcesses) {
            this.processId = processId;
            for (String process : allProcesses) {
                clock.put(process, 0);
            }
        }
        
        public void tick() {
            clock.put(processId, clock.get(processId) + 1);
        }
        
        public void update(VectorClock other) {
            for (Map.Entry<String, Integer> entry : other.clock.entrySet()) {
                String process = entry.getKey();
                int timestamp = entry.getValue();
                clock.put(process, Math.max(clock.get(process), timestamp));
            }
        }
        
        public boolean happensBefore(VectorClock other) {
            boolean strictlyLess = false;
            for (String process : clock.keySet()) {
                int thisTime = clock.get(process);
                int otherTime = other.clock.get(process);
                
                if (thisTime > otherTime) {
                    return false;
                }
                if (thisTime < otherTime) {
                    strictlyLess = true;
                }
            }
            return strictlyLess;
        }
        
        public boolean isConcurrent(VectorClock other) {
            return !happensBefore(other) && !other.happensBefore(this);
        }
        
        @Override
        public String toString() {
            return "VectorClock{" + clock + "}";
        }
    }
    
    // Distributed event
    public static class DistributedEvent {
        private final String eventId;
        private final String processId;
        private final VectorClock timestamp;
        private final String data;
        
        public DistributedEvent(String eventId, String processId, VectorClock timestamp, String data) {
            this.eventId = eventId;
            this.processId = processId;
            this.timestamp = timestamp;
            this.data = data;
        }
        
        public String getEventId() { return eventId; }
        public String getProcessId() { return processId; }
        public VectorClock getTimestamp() { return timestamp; }
        public String getData() { return data; }
        
        @Override
        public String toString() {
            return "Event{" + eventId + ", " + processId + ", " + timestamp + ", " + data + "}";
        }
    }
    
    // Event ordering system
    public static class EventOrderingSystem {
        private final List<String> processes;
        private final Map<String, VectorClock> clocks = new ConcurrentHashMap<>();
        private final List<DistributedEvent> events = new ArrayList<>();
        
        public EventOrderingSystem(List<String> processes) {
            this.processes = new ArrayList<>(processes);
            for (String process : processes) {
                clocks.put(process, new VectorClock(process, processes));
            }
        }
        
        public DistributedEvent createEvent(String processId, String data) {
            VectorClock clock = clocks.get(processId);
            clock.tick();
            
            String eventId = processId + "-" + System.currentTimeMillis();
            DistributedEvent event = new DistributedEvent(eventId, processId, new VectorClock(clock), data);
            
            synchronized (events) {
                events.add(event);
            }
            
            return event;
        }
        
        public void synchronize(String processId, VectorClock otherClock) {
            VectorClock clock = clocks.get(processId);
            clock.update(otherClock);
        }
        
        public List<DistributedEvent> getOrderedEvents() {
            synchronized (events) {
                return new ArrayList<>(events);
            }
        }
        
        public void printEventOrdering() {
            List<DistributedEvent> orderedEvents = getOrderedEvents();
            
            System.out.println("Event Ordering Analysis:");
            for (int i = 0; i < orderedEvents.size(); i++) {
                DistributedEvent event1 = orderedEvents.get(i);
                System.out.println("Event " + i + ": " + event1);
                
                for (int j = i + 1; j < orderedEvents.size(); j++) {
                    DistributedEvent event2 = orderedEvents.get(j);
                    
                    if (event1.getTimestamp().happensBefore(event2.getTimestamp())) {
                        System.out.println("  -> happens before event " + j);
                    } else if (event1.getTimestamp().isConcurrent(event2.getTimestamp())) {
                        System.out.println("  -> concurrent with event " + j);
                    }
                }
            }
        }
    }
}
```

## 14.8 CRDTs (Conflict-free Replicated Data Types)

CRDTs are data structures that can be replicated across multiple nodes and updated independently without coordination.

### Key Concepts
- **Eventual Consistency**: All replicas eventually converge
- **No Coordination**: Updates can happen without locking
- **Commutativity**: Operations can be applied in any order
- **Idempotency**: Duplicate operations have no effect

### Real-World Analogy
Think of a shared document where multiple people can edit simultaneously, and the system automatically merges their changes without conflicts.

### Java Example
```java
public class CRDTsExample {
    // G-Counter (Grow-only Counter) CRDT
    public static class GCounter {
        private final Map<String, Integer> counters = new ConcurrentHashMap<>();
        private final String replicaId;
        
        public GCounter(String replicaId) {
            this.replicaId = replicaId;
            counters.put(replicaId, 0);
        }
        
        public void increment() {
            counters.put(replicaId, counters.get(replicaId) + 1);
        }
        
        public void increment(int delta) {
            if (delta > 0) {
                counters.put(replicaId, counters.get(replicaId) + delta);
            }
        }
        
        public int getValue() {
            return counters.values().stream().mapToInt(Integer::intValue).sum();
        }
        
        public void merge(GCounter other) {
            for (Map.Entry<String, Integer> entry : other.counters.entrySet()) {
                String replica = entry.getKey();
                int value = entry.getValue();
                counters.put(replica, Math.max(counters.getOrDefault(replica, 0), value));
            }
        }
        
        @Override
        public String toString() {
            return "GCounter{" + counters + "}";
        }
    }
    
    // PN-Counter (Positive-Negative Counter) CRDT
    public static class PNCounter {
        private final GCounter positive;
        private final GCounter negative;
        
        public PNCounter(String replicaId) {
            this.positive = new GCounter(replicaId);
            this.negative = new GCounter(replicaId);
        }
        
        public void increment() {
            positive.increment();
        }
        
        public void decrement() {
            negative.increment();
        }
        
        public int getValue() {
            return positive.getValue() - negative.getValue();
        }
        
        public void merge(PNCounter other) {
            positive.merge(other.positive);
            negative.merge(other.negative);
        }
        
        @Override
        public String toString() {
            return "PNCounter{value=" + getValue() + "}";
        }
    }
    
    // G-Set (Grow-only Set) CRDT
    public static class GSet<T> {
        private final Set<T> elements = ConcurrentHashMap.newKeySet();
        
        public void add(T element) {
            elements.add(element);
        }
        
        public boolean contains(T element) {
            return elements.contains(element);
        }
        
        public Set<T> getElements() {
            return new HashSet<>(elements);
        }
        
        public void merge(GSet<T> other) {
            elements.addAll(other.elements);
        }
        
        @Override
        public String toString() {
            return "GSet{" + elements + "}";
        }
    }
    
    // OR-Set (Observed-Remove Set) CRDT
    public static class ORSet<T> {
        private final Map<T, Set<String>> elements = new ConcurrentHashMap<>();
        private final Map<T, Set<String>> tombstones = new ConcurrentHashMap<>();
        private final String replicaId;
        
        public ORSet(String replicaId) {
            this.replicaId = replicaId;
        }
        
        public void add(T element) {
            elements.computeIfAbsent(element, k -> ConcurrentHashMap.newKeySet()).add(replicaId + ":" + System.nanoTime());
        }
        
        public void remove(T element) {
            if (elements.containsKey(element)) {
                tombstones.put(element, new HashSet<>(elements.get(element)));
                elements.remove(element);
            }
        }
        
        public boolean contains(T element) {
            return elements.containsKey(element);
        }
        
        public Set<T> getElements() {
            return new HashSet<>(elements.keySet());
        }
        
        public void merge(ORSet<T> other) {
            // Merge elements
            for (Map.Entry<T, Set<String>> entry : other.elements.entrySet()) {
                T element = entry.getKey();
                Set<String> tags = entry.getValue();
                
                if (!tombstones.containsKey(element) || !tombstones.get(element).containsAll(tags)) {
                    elements.computeIfAbsent(element, k -> ConcurrentHashMap.newKeySet()).addAll(tags);
                }
            }
            
            // Merge tombstones
            for (Map.Entry<T, Set<String>> entry : other.tombstones.entrySet()) {
                T element = entry.getKey();
                Set<String> tags = entry.getValue();
                
                tombstones.computeIfAbsent(element, k -> ConcurrentHashMap.newKeySet()).addAll(tags);
                
                // Remove elements that are in tombstones
                if (elements.containsKey(element)) {
                    elements.get(element).removeAll(tags);
                    if (elements.get(element).isEmpty()) {
                        elements.remove(element);
                    }
                }
            }
        }
        
        @Override
        public String toString() {
            return "ORSet{" + elements.keySet() + "}";
        }
    }
}
```

This comprehensive explanation covers all aspects of distributed concurrency, providing both theoretical understanding and practical Java examples to illustrate each concept.