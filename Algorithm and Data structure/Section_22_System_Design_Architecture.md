# Section 22 – System Design & Architecture

## 22.1 Scalable System Design

Scalable system design focuses on building systems that can handle increasing loads while maintaining performance and reliability.

### Load Balancing Strategies

```java
public class LoadBalancer {
    private List<Server> servers;
    private LoadBalancingStrategy strategy;
    
    public LoadBalancer(List<Server> servers, LoadBalancingStrategy strategy) {
        this.servers = servers;
        this.strategy = strategy;
    }
    
    public Server getServer() {
        return strategy.selectServer(servers);
    }
    
    public interface LoadBalancingStrategy {
        Server selectServer(List<Server> servers);
    }
    
    // Round Robin Strategy
    public static class RoundRobinStrategy implements LoadBalancingStrategy {
        private AtomicInteger currentIndex = new AtomicInteger(0);
        
        @Override
        public Server selectServer(List<Server> servers) {
            int index = currentIndex.getAndIncrement() % servers.size();
            return servers.get(index);
        }
    }
    
    // Least Connections Strategy
    public static class LeastConnectionsStrategy implements LoadBalancingStrategy {
        @Override
        public Server selectServer(List<Server> servers) {
            return servers.stream()
                .min(Comparator.comparing(Server::getActiveConnections))
                .orElse(servers.get(0));
        }
    }
    
    // Weighted Round Robin Strategy
    public static class WeightedRoundRobinStrategy implements LoadBalancingStrategy {
        private AtomicInteger currentWeight = new AtomicInteger(0);
        private AtomicInteger currentIndex = new AtomicInteger(-1);
        
        @Override
        public Server selectServer(List<Server> servers) {
            while (true) {
                int index = currentIndex.incrementAndGet() % servers.size();
                if (index == 0) {
                    currentWeight.addAndGet(-getTotalWeight(servers));
                    if (currentWeight.get() <= 0) {
                        currentWeight.set(getTotalWeight(servers));
                    }
                }
                
                Server server = servers.get(index);
                if (server.getWeight() >= currentWeight.get()) {
                    return server;
                }
            }
        }
        
        private int getTotalWeight(List<Server> servers) {
            return servers.stream().mapToInt(Server::getWeight).sum();
        }
    }
    
    public static class Server {
        private String id;
        private String host;
        private int port;
        private int weight;
        private AtomicInteger activeConnections = new AtomicInteger(0);
        private boolean healthy = true;
        
        public Server(String id, String host, int port, int weight) {
            this.id = id;
            this.host = host;
            this.port = port;
            this.weight = weight;
        }
        
        public void incrementConnections() {
            activeConnections.incrementAndGet();
        }
        
        public void decrementConnections() {
            activeConnections.decrementAndGet();
        }
        
        public int getActiveConnections() {
            return activeConnections.get();
        }
        
        public int getWeight() {
            return weight;
        }
        
        public boolean isHealthy() {
            return healthy;
        }
        
        public void setHealthy(boolean healthy) {
            this.healthy = healthy;
        }
        
        public String getUrl() {
            return "http://" + host + ":" + port;
        }
    }
}
```

### Caching Strategies

```java
public class CacheManager {
    private Map<String, CacheEntry> cache;
    private int maxSize;
    private EvictionPolicy evictionPolicy;
    
    public CacheManager(int maxSize, EvictionPolicy evictionPolicy) {
        this.cache = new ConcurrentHashMap<>();
        this.maxSize = maxSize;
        this.evictionPolicy = evictionPolicy;
    }
    
    public void put(String key, Object value, long ttl) {
        if (cache.size() >= maxSize) {
            evict();
        }
        
        CacheEntry entry = new CacheEntry(value, System.currentTimeMillis() + ttl);
        cache.put(key, entry);
    }
    
    public Object get(String key) {
        CacheEntry entry = cache.get(key);
        if (entry == null) {
            return null;
        }
        
        if (entry.isExpired()) {
            cache.remove(key);
            return null;
        }
        
        entry.updateAccessTime();
        return entry.getValue();
    }
    
    private void evict() {
        String keyToEvict = evictionPolicy.selectKeyToEvict(cache);
        if (keyToEvict != null) {
            cache.remove(keyToEvict);
        }
    }
    
    public interface EvictionPolicy {
        String selectKeyToEvict(Map<String, CacheEntry> cache);
    }
    
    // Least Recently Used (LRU) Eviction
    public static class LRUEvictionPolicy implements EvictionPolicy {
        @Override
        public String selectKeyToEvict(Map<String, CacheEntry> cache) {
            return cache.entrySet().stream()
                .min(Comparator.comparing(entry -> entry.getValue().getLastAccessTime()))
                .map(Map.Entry::getKey)
                .orElse(null);
        }
    }
    
    // Least Frequently Used (LFU) Eviction
    public static class LFUEvictionPolicy implements EvictionPolicy {
        @Override
        public String selectKeyToEvict(Map<String, CacheEntry> cache) {
            return cache.entrySet().stream()
                .min(Comparator.comparing(entry -> entry.getValue().getAccessCount()))
                .map(Map.Entry::getKey)
                .orElse(null);
        }
    }
    
    private static class CacheEntry {
        private Object value;
        private long expirationTime;
        private long lastAccessTime;
        private int accessCount;
        
        public CacheEntry(Object value, long expirationTime) {
            this.value = value;
            this.expirationTime = expirationTime;
            this.lastAccessTime = System.currentTimeMillis();
            this.accessCount = 1;
        }
        
        public Object getValue() {
            return value;
        }
        
        public boolean isExpired() {
            return System.currentTimeMillis() > expirationTime;
        }
        
        public void updateAccessTime() {
            this.lastAccessTime = System.currentTimeMillis();
            this.accessCount++;
        }
        
        public long getLastAccessTime() {
            return lastAccessTime;
        }
        
        public int getAccessCount() {
            return accessCount;
        }
    }
}
```

## 22.2 Distributed System Algorithms

### Consistent Hashing

```java
public class ConsistentHash {
    private SortedMap<Long, String> circle;
    private int numberOfReplicas;
    private HashFunction hashFunction;
    
    public ConsistentHash(int numberOfReplicas, Collection<String> nodes) {
        this.numberOfReplicas = numberOfReplicas;
        this.circle = new TreeMap<>();
        this.hashFunction = new MD5Hash();
        
        for (String node : nodes) {
            add(node);
        }
    }
    
    public void add(String node) {
        for (int i = 0; i < numberOfReplicas; i++) {
            String virtualNode = node + ":" + i;
            long hash = hashFunction.hash(virtualNode);
            circle.put(hash, node);
        }
    }
    
    public void remove(String node) {
        for (int i = 0; i < numberOfReplicas; i++) {
            String virtualNode = node + ":" + i;
            long hash = hashFunction.hash(virtualNode);
            circle.remove(hash);
        }
    }
    
    public String get(String key) {
        if (circle.isEmpty()) {
            return null;
        }
        
        long hash = hashFunction.hash(key);
        SortedMap<Long, String> tailMap = circle.tailMap(hash);
        
        if (tailMap.isEmpty()) {
            return circle.get(circle.firstKey());
        }
        
        return tailMap.get(tailMap.firstKey());
    }
    
    public interface HashFunction {
        long hash(String input);
    }
    
    public static class MD5Hash implements HashFunction {
        @Override
        public long hash(String input) {
            try {
                MessageDigest md = MessageDigest.getInstance("MD5");
                byte[] digest = md.digest(input.getBytes());
                return ((long) (digest[0] & 0xFF) << 24) |
                       ((long) (digest[1] & 0xFF) << 16) |
                       ((long) (digest[2] & 0xFF) << 8) |
                       (long) (digest[3] & 0xFF);
            } catch (NoSuchAlgorithmException e) {
                throw new RuntimeException(e);
            }
        }
    }
}
```

### Distributed Lock

```java
public class DistributedLock {
    private String lockKey;
    private String lockValue;
    private long expirationTime;
    private RedisClient redisClient;
    
    public DistributedLock(String lockKey, RedisClient redisClient) {
        this.lockKey = lockKey;
        this.lockValue = UUID.randomUUID().toString();
        this.redisClient = redisClient;
    }
    
    public boolean tryLock(long timeoutMs) {
        long startTime = System.currentTimeMillis();
        expirationTime = System.currentTimeMillis() + timeoutMs;
        
        while (System.currentTimeMillis() - startTime < timeoutMs) {
            if (acquireLock()) {
                return true;
            }
            
            try {
                Thread.sleep(10); // Wait before retry
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return false;
            }
        }
        
        return false;
    }
    
    private boolean acquireLock() {
        // Use Redis SET with NX and EX options for atomic lock acquisition
        String script = "if redis.call('get', KEYS[1]) == false then " +
                       "return redis.call('set', KEYS[1], ARGV[1], 'EX', ARGV[2]) " +
                       "else return false end";
        
        return redisClient.eval(script, Arrays.asList(lockKey), 
                               Arrays.asList(lockValue, String.valueOf(expirationTime / 1000)));
    }
    
    public void unlock() {
        // Use Lua script to ensure atomic unlock
        String script = "if redis.call('get', KEYS[1]) == ARGV[1] then " +
                       "return redis.call('del', KEYS[1]) " +
                       "else return 0 end";
        
        redisClient.eval(script, Arrays.asList(lockKey), Arrays.asList(lockValue));
    }
    
    public boolean isLocked() {
        String value = redisClient.get(lockKey);
        return lockValue.equals(value);
    }
}
```

## 22.3 Consensus Algorithms

### Raft Algorithm Implementation

```java
public class RaftNode {
    public enum State {
        FOLLOWER, CANDIDATE, LEADER
    }
    
    private int nodeId;
    private State state;
    private int currentTerm;
    private int votedFor;
    private int commitIndex;
    private int lastApplied;
    private List<LogEntry> log;
    private Map<Integer, Integer> nextIndex;
    private Map<Integer, Integer> matchIndex;
    private long lastHeartbeat;
    private Random random;
    
    public RaftNode(int nodeId) {
        this.nodeId = nodeId;
        this.state = State.FOLLOWER;
        this.currentTerm = 0;
        this.votedFor = -1;
        this.commitIndex = 0;
        this.lastApplied = 0;
        this.log = new ArrayList<>();
        this.nextIndex = new HashMap<>();
        this.matchIndex = new HashMap<>();
        this.lastHeartbeat = System.currentTimeMillis();
        this.random = new Random();
    }
    
    public void startElection() {
        state = State.CANDIDATE;
        currentTerm++;
        votedFor = nodeId;
        
        // Request votes from other nodes
        int votes = 1; // Vote for self
        for (int otherNodeId : getOtherNodeIds()) {
            if (requestVote(otherNodeId, currentTerm, log.size() - 1, 
                           getLastLogTerm())) {
                votes++;
            }
        }
        
        if (votes > getMajority()) {
            becomeLeader();
        }
    }
    
    public boolean requestVote(int candidateId, int term, int lastLogIndex, int lastLogTerm) {
        if (term > currentTerm) {
            currentTerm = term;
            state = State.FOLLOWER;
            votedFor = -1;
        }
        
        boolean voteGranted = false;
        
        if (term == currentTerm && 
            (votedFor == -1 || votedFor == candidateId) &&
            isUpToDate(lastLogIndex, lastLogTerm)) {
            votedFor = candidateId;
            voteGranted = true;
        }
        
        return voteGranted;
    }
    
    public boolean appendEntries(int leaderId, int term, int prevLogIndex, 
                               int prevLogTerm, List<LogEntry> entries, int leaderCommit) {
        if (term > currentTerm) {
            currentTerm = term;
            state = State.FOLLOWER;
            votedFor = -1;
        }
        
        boolean success = false;
        
        if (term == currentTerm) {
            if (state == State.CANDIDATE) {
                state = State.FOLLOWER;
            }
            
            if (prevLogIndex == -1 || 
                (prevLogIndex < log.size() && log.get(prevLogIndex).term == prevLogTerm)) {
                success = true;
                
                // Append new entries
                for (int i = 0; i < entries.size(); i++) {
                    int logIndex = prevLogIndex + 1 + i;
                    if (logIndex < log.size()) {
                        if (log.get(logIndex).term != entries.get(i).term) {
                            // Truncate log
                            log = new ArrayList<>(log.subList(0, logIndex));
                        }
                    }
                    if (logIndex >= log.size()) {
                        log.add(entries.get(i));
                    }
                }
                
                // Update commit index
                if (leaderCommit > commitIndex) {
                    commitIndex = Math.min(leaderCommit, log.size() - 1);
                }
            }
        }
        
        lastHeartbeat = System.currentTimeMillis();
        return success;
    }
    
    private void becomeLeader() {
        state = State.LEADER;
        
        // Initialize nextIndex and matchIndex
        for (int otherNodeId : getOtherNodeIds()) {
            nextIndex.put(otherNodeId, log.size());
            matchIndex.put(otherNodeId, 0);
        }
        
        // Start sending heartbeats
        startHeartbeat();
    }
    
    private void startHeartbeat() {
        // Send heartbeats to all followers
        for (int otherNodeId : getOtherNodeIds()) {
            sendHeartbeat(otherNodeId);
        }
    }
    
    private void sendHeartbeat(int followerId) {
        int prevLogIndex = nextIndex.get(followerId) - 1;
        int prevLogTerm = prevLogIndex >= 0 ? log.get(prevLogIndex).term : 0;
        
        List<LogEntry> entries = new ArrayList<>();
        if (nextIndex.get(followerId) < log.size()) {
            entries = log.subList(nextIndex.get(followerId), log.size());
        }
        
        appendEntries(followerId, currentTerm, prevLogIndex, prevLogTerm, 
                     entries, commitIndex);
    }
    
    private boolean isUpToDate(int lastLogIndex, int lastLogTerm) {
        if (log.isEmpty()) return true;
        
        LogEntry lastEntry = log.get(log.size() - 1);
        return lastLogTerm > lastEntry.term || 
               (lastLogTerm == lastEntry.term && lastLogIndex >= log.size() - 1);
    }
    
    private int getLastLogTerm() {
        if (log.isEmpty()) return 0;
        return log.get(log.size() - 1).term;
    }
    
    private int getMajority() {
        return (getOtherNodeIds().size() + 1) / 2 + 1;
    }
    
    private List<Integer> getOtherNodeIds() {
        // Return list of other node IDs
        return Arrays.asList(1, 2, 3, 4); // Example
    }
    
    public static class LogEntry {
        int term;
        String command;
        
        public LogEntry(int term, String command) {
            this.term = term;
            this.command = command;
        }
    }
}
```

## 22.4 Load Balancing Strategies

### Advanced Load Balancing

```java
public class AdvancedLoadBalancer {
    private List<Server> servers;
    private LoadBalancingStrategy strategy;
    private HealthChecker healthChecker;
    private CircuitBreaker circuitBreaker;
    
    public AdvancedLoadBalancer(List<Server> servers, LoadBalancingStrategy strategy) {
        this.servers = servers;
        this.strategy = strategy;
        this.healthChecker = new HealthChecker();
        this.circuitBreaker = new CircuitBreaker();
    }
    
    public Server getServer() {
        List<Server> healthyServers = servers.stream()
            .filter(Server::isHealthy)
            .collect(Collectors.toList());
        
        if (healthyServers.isEmpty()) {
            throw new RuntimeException("No healthy servers available");
        }
        
        Server selectedServer = strategy.selectServer(healthyServers);
        
        // Check circuit breaker
        if (circuitBreaker.isOpen(selectedServer)) {
            throw new RuntimeException("Server circuit breaker is open");
        }
        
        return selectedServer;
    }
    
    public void handleRequest(Server server, Runnable request) {
        try {
            request.run();
            circuitBreaker.recordSuccess(server);
        } catch (Exception e) {
            circuitBreaker.recordFailure(server);
            throw e;
        }
    }
    
    public static class HealthChecker {
        private Map<Server, Long> lastHealthCheck = new ConcurrentHashMap<>();
        private long healthCheckInterval = 30000; // 30 seconds
        
        public boolean isHealthy(Server server) {
            long now = System.currentTimeMillis();
            Long lastCheck = lastHealthCheck.get(server);
            
            if (lastCheck == null || now - lastCheck > healthCheckInterval) {
                boolean healthy = performHealthCheck(server);
                lastHealthCheck.put(server, now);
                server.setHealthy(healthy);
                return healthy;
            }
            
            return server.isHealthy();
        }
        
        private boolean performHealthCheck(Server server) {
            try {
                // Perform actual health check (e.g., HTTP request)
                // This is a simplified version
                return true;
            } catch (Exception e) {
                return false;
            }
        }
    }
    
    public static class CircuitBreaker {
        private Map<Server, CircuitState> states = new ConcurrentHashMap<>();
        private int failureThreshold = 5;
        private long timeout = 60000; // 1 minute
        
        public boolean isOpen(Server server) {
            CircuitState state = states.get(server);
            if (state == null) {
                state = new CircuitState();
                states.put(server, state);
            }
            
            if (state.state == CircuitState.State.OPEN) {
                if (System.currentTimeMillis() - state.lastFailureTime > timeout) {
                    state.state = CircuitState.State.HALF_OPEN;
                    return false;
                }
                return true;
            }
            
            return false;
        }
        
        public void recordSuccess(Server server) {
            CircuitState state = states.get(server);
            if (state != null) {
                state.failureCount = 0;
                state.state = CircuitState.State.CLOSED;
            }
        }
        
        public void recordFailure(Server server) {
            CircuitState state = states.get(server);
            if (state == null) {
                state = new CircuitState();
                states.put(server, state);
            }
            
            state.failureCount++;
            state.lastFailureTime = System.currentTimeMillis();
            
            if (state.failureCount >= failureThreshold) {
                state.state = CircuitState.State.OPEN;
            }
        }
        
        private static class CircuitState {
            enum State { CLOSED, OPEN, HALF_OPEN }
            
            State state = State.CLOSED;
            int failureCount = 0;
            long lastFailureTime = 0;
        }
    }
}
```

## 22.5 Caching Strategies & Algorithms

### Multi-Level Cache

```java
public class MultiLevelCache {
    private CacheManager l1Cache; // Fast, small cache
    private CacheManager l2Cache; // Slower, larger cache
    private CacheManager l3Cache; // Slowest, largest cache
    
    public MultiLevelCache(int l1Size, int l2Size, int l3Size) {
        this.l1Cache = new CacheManager(l1Size, new LRUEvictionPolicy());
        this.l2Cache = new CacheManager(l2Size, new LRUEvictionPolicy());
        this.l3Cache = new CacheManager(l3Size, new LRUEvictionPolicy());
    }
    
    public Object get(String key) {
        // Check L1 cache first
        Object value = l1Cache.get(key);
        if (value != null) {
            return value;
        }
        
        // Check L2 cache
        value = l2Cache.get(key);
        if (value != null) {
            // Promote to L1
            l1Cache.put(key, value, 300000); // 5 minutes TTL
            return value;
        }
        
        // Check L3 cache
        value = l3Cache.get(key);
        if (value != null) {
            // Promote to L2 and L1
            l2Cache.put(key, value, 600000); // 10 minutes TTL
            l1Cache.put(key, value, 300000); // 5 minutes TTL
            return value;
        }
        
        return null;
    }
    
    public void put(String key, Object value, long ttl) {
        // Store in all levels
        l1Cache.put(key, value, ttl);
        l2Cache.put(key, value, ttl * 2);
        l3Cache.put(key, value, ttl * 4);
    }
    
    public void evict(String key) {
        l1Cache.evict(key);
        l2Cache.evict(key);
        l3Cache.evict(key);
    }
}
```

### Cache-Aside Pattern

```java
public class CacheAsidePattern {
    private CacheManager cache;
    private DataSource dataSource;
    
    public CacheAsidePattern(CacheManager cache, DataSource dataSource) {
        this.cache = cache;
        this.dataSource = dataSource;
    }
    
    public Object get(String key) {
        // Try to get from cache first
        Object value = cache.get(key);
        if (value != null) {
            return value;
        }
        
        // If not in cache, get from data source
        value = dataSource.get(key);
        if (value != null) {
            // Store in cache for future requests
            cache.put(key, value, 300000); // 5 minutes TTL
        }
        
        return value;
    }
    
    public void put(String key, Object value) {
        // Update data source first
        dataSource.put(key, value);
        
        // Update cache
        cache.put(key, value, 300000);
    }
    
    public void delete(String key) {
        // Delete from data source first
        dataSource.delete(key);
        
        // Remove from cache
        cache.evict(key);
    }
    
    public interface DataSource {
        Object get(String key);
        void put(String key, Object value);
        void delete(String key);
    }
}
```

## 22.6 Data Partitioning & Sharding

### Horizontal Sharding

```java
public class HorizontalSharding {
    private List<Shard> shards;
    private ShardingStrategy strategy;
    
    public HorizontalSharding(List<Shard> shards, ShardingStrategy strategy) {
        this.shards = shards;
        this.strategy = strategy;
    }
    
    public void insert(String key, Object value) {
        Shard shard = strategy.selectShard(key, shards);
        shard.insert(key, value);
    }
    
    public Object get(String key) {
        Shard shard = strategy.selectShard(key, shards);
        return shard.get(key);
    }
    
    public void update(String key, Object value) {
        Shard shard = strategy.selectShard(key, shards);
        shard.update(key, value);
    }
    
    public void delete(String key) {
        Shard shard = strategy.selectShard(key, shards);
        shard.delete(key);
    }
    
    public interface ShardingStrategy {
        Shard selectShard(String key, List<Shard> shards);
    }
    
    // Hash-based sharding
    public static class HashShardingStrategy implements ShardingStrategy {
        @Override
        public Shard selectShard(String key, List<Shard> shards) {
            int hash = key.hashCode();
            int index = Math.abs(hash) % shards.size();
            return shards.get(index);
        }
    }
    
    // Range-based sharding
    public static class RangeShardingStrategy implements ShardingStrategy {
        @Override
        public Shard selectShard(String key, List<Shard> shards) {
            for (Shard shard : shards) {
                if (shard.isInRange(key)) {
                    return shard;
                }
            }
            return shards.get(0); // Default to first shard
        }
    }
    
    public static class Shard {
        private String id;
        private String startKey;
        private String endKey;
        private Map<String, Object> data;
        
        public Shard(String id, String startKey, String endKey) {
            this.id = id;
            this.startKey = startKey;
            this.endKey = endKey;
            this.data = new ConcurrentHashMap<>();
        }
        
        public boolean isInRange(String key) {
            return key.compareTo(startKey) >= 0 && key.compareTo(endKey) < 0;
        }
        
        public void insert(String key, Object value) {
            data.put(key, value);
        }
        
        public Object get(String key) {
            return data.get(key);
        }
        
        public void update(String key, Object value) {
            data.put(key, value);
        }
        
        public void delete(String key) {
            data.remove(key);
        }
    }
}
```

## 22.7 Event Sourcing & CQRS

### Event Store

```java
public class EventStore {
    private List<Event> events;
    private Map<String, List<Event>> streamEvents;
    
    public EventStore() {
        this.events = new ArrayList<>();
        this.streamEvents = new HashMap<>();
    }
    
    public void appendEvent(String streamId, Event event) {
        event.setStreamId(streamId);
        event.setVersion(events.size());
        event.setTimestamp(System.currentTimeMillis());
        
        events.add(event);
        streamEvents.computeIfAbsent(streamId, k -> new ArrayList<>()).add(event);
    }
    
    public List<Event> getEvents(String streamId) {
        return streamEvents.getOrDefault(streamId, new ArrayList<>());
    }
    
    public List<Event> getEvents(String streamId, int fromVersion) {
        return streamEvents.getOrDefault(streamId, new ArrayList<>())
            .stream()
            .filter(event -> event.getVersion() >= fromVersion)
            .collect(Collectors.toList());
    }
    
    public static class Event {
        private String streamId;
        private String eventType;
        private Object data;
        private int version;
        private long timestamp;
        
        public Event(String eventType, Object data) {
            this.eventType = eventType;
            this.data = data;
        }
        
        // Getters and setters
        public String getStreamId() { return streamId; }
        public void setStreamId(String streamId) { this.streamId = streamId; }
        
        public String getEventType() { return eventType; }
        public void setEventType(String eventType) { this.eventType = eventType; }
        
        public Object getData() { return data; }
        public void setData(Object data) { this.data = data; }
        
        public int getVersion() { return version; }
        public void setVersion(int version) { this.version = version; }
        
        public long getTimestamp() { return timestamp; }
        public void setTimestamp(long timestamp) { this.timestamp = timestamp; }
    }
}
```

### CQRS Implementation

```java
public class CQRSHandler {
    private EventStore eventStore;
    private Map<String, AggregateRoot> aggregates;
    private Map<String, ReadModel> readModels;
    
    public CQRSHandler(EventStore eventStore) {
        this.eventStore = eventStore;
        this.aggregates = new HashMap<>();
        this.readModels = new HashMap<>();
    }
    
    public void handleCommand(Command command) {
        String aggregateId = command.getAggregateId();
        AggregateRoot aggregate = getAggregate(aggregateId);
        
        List<Event> events = aggregate.handleCommand(command);
        
        for (Event event : events) {
            eventStore.appendEvent(aggregateId, event);
            updateReadModels(event);
        }
    }
    
    public Object handleQuery(Query query) {
        String readModelId = query.getReadModelId();
        ReadModel readModel = readModels.get(readModelId);
        
        if (readModel == null) {
            readModel = createReadModel(readModelId);
            readModels.put(readModelId, readModel);
        }
        
        return readModel.handleQuery(query);
    }
    
    private AggregateRoot getAggregate(String aggregateId) {
        AggregateRoot aggregate = aggregates.get(aggregateId);
        if (aggregate == null) {
            aggregate = new AggregateRoot(aggregateId);
            aggregates.put(aggregateId, aggregate);
        }
        return aggregate;
    }
    
    private void updateReadModels(Event event) {
        for (ReadModel readModel : readModels.values()) {
            readModel.handleEvent(event);
        }
    }
    
    private ReadModel createReadModel(String readModelId) {
        // Create read model based on ID
        return new ReadModel(readModelId);
    }
    
    public static class Command {
        private String aggregateId;
        private String commandType;
        private Object data;
        
        public Command(String aggregateId, String commandType, Object data) {
            this.aggregateId = aggregateId;
            this.commandType = commandType;
            this.data = data;
        }
        
        // Getters
        public String getAggregateId() { return aggregateId; }
        public String getCommandType() { return commandType; }
        public Object getData() { return data; }
    }
    
    public static class Query {
        private String readModelId;
        private String queryType;
        private Object parameters;
        
        public Query(String readModelId, String queryType, Object parameters) {
            this.readModelId = readModelId;
            this.queryType = queryType;
            this.parameters = parameters;
        }
        
        // Getters
        public String getReadModelId() { return readModelId; }
        public String getQueryType() { return queryType; }
        public Object getParameters() { return parameters; }
    }
}
```

## 22.8 Microservices Communication

### Service Discovery

```java
public class ServiceDiscovery {
    private Map<String, List<ServiceInstance>> services;
    private HealthChecker healthChecker;
    
    public ServiceDiscovery() {
        this.services = new ConcurrentHashMap<>();
        this.healthChecker = new HealthChecker();
    }
    
    public void register(ServiceInstance instance) {
        services.computeIfAbsent(instance.getServiceName(), k -> new ArrayList<>())
                .add(instance);
    }
    
    public void deregister(ServiceInstance instance) {
        List<ServiceInstance> instances = services.get(instance.getServiceName());
        if (instances != null) {
            instances.remove(instance);
        }
    }
    
    public ServiceInstance getInstance(String serviceName) {
        List<ServiceInstance> instances = services.get(serviceName);
        if (instances == null || instances.isEmpty()) {
            throw new RuntimeException("No instances available for service: " + serviceName);
        }
        
        // Filter healthy instances
        List<ServiceInstance> healthyInstances = instances.stream()
            .filter(instance -> healthChecker.isHealthy(instance))
            .collect(Collectors.toList());
        
        if (healthyInstances.isEmpty()) {
            throw new RuntimeException("No healthy instances available for service: " + serviceName);
        }
        
        // Use round-robin selection
        return healthyInstances.get(new Random().nextInt(healthyInstances.size()));
    }
    
    public List<ServiceInstance> getAllInstances(String serviceName) {
        return services.getOrDefault(serviceName, new ArrayList<>());
    }
    
    public static class ServiceInstance {
        private String serviceName;
        private String host;
        private int port;
        private Map<String, String> metadata;
        
        public ServiceInstance(String serviceName, String host, int port) {
            this.serviceName = serviceName;
            this.host = host;
            this.port = port;
            this.metadata = new HashMap<>();
        }
        
        public String getUrl() {
            return "http://" + host + ":" + port;
        }
        
        // Getters and setters
        public String getServiceName() { return serviceName; }
        public String getHost() { return host; }
        public int getPort() { return port; }
        public Map<String, String> getMetadata() { return metadata; }
    }
}
```

### API Gateway

```java
public class APIGateway {
    private ServiceDiscovery serviceDiscovery;
    private LoadBalancer loadBalancer;
    private RateLimiter rateLimiter;
    private AuthenticationService authService;
    
    public APIGateway(ServiceDiscovery serviceDiscovery, LoadBalancer loadBalancer,
                     RateLimiter rateLimiter, AuthenticationService authService) {
        this.serviceDiscovery = serviceDiscovery;
        this.loadBalancer = loadBalancer;
        this.rateLimiter = rateLimiter;
        this.authService = authService;
    }
    
    public Response handleRequest(Request request) {
        // Rate limiting
        if (!rateLimiter.isAllowed(request.getClientId())) {
            return new Response(429, "Rate limit exceeded");
        }
        
        // Authentication
        if (!authService.isAuthenticated(request.getToken())) {
            return new Response(401, "Unauthorized");
        }
        
        // Route to appropriate service
        String serviceName = routeToService(request.getPath());
        ServiceInstance instance = serviceDiscovery.getInstance(serviceName);
        
        // Forward request
        return forwardRequest(instance, request);
    }
    
    private String routeToService(String path) {
        if (path.startsWith("/users")) {
            return "user-service";
        } else if (path.startsWith("/orders")) {
            return "order-service";
        } else if (path.startsWith("/products")) {
            return "product-service";
        }
        throw new RuntimeException("No service found for path: " + path);
    }
    
    private Response forwardRequest(ServiceInstance instance, Request request) {
        // Forward HTTP request to service instance
        // This is a simplified version
        try {
            // Make HTTP request to service
            return new Response(200, "Success");
        } catch (Exception e) {
            return new Response(500, "Internal server error");
        }
    }
    
    public static class Request {
        private String path;
        private String method;
        private String token;
        private String clientId;
        private Object body;
        
        // Getters and setters
        public String getPath() { return path; }
        public String getMethod() { return method; }
        public String getToken() { return token; }
        public String getClientId() { return clientId; }
        public Object getBody() { return body; }
    }
    
    public static class Response {
        private int statusCode;
        private String message;
        private Object body;
        
        public Response(int statusCode, String message) {
            this.statusCode = statusCode;
            this.message = message;
        }
        
        // Getters and setters
        public int getStatusCode() { return statusCode; }
        public String getMessage() { return message; }
        public Object getBody() { return body; }
    }
}
```

**Real-world Analogies:**
- **Scalable System Design:** Like designing a restaurant that can handle more customers by adding more tables and staff
- **Load Balancing:** Like a traffic controller directing cars to different lanes to avoid congestion
- **Caching Strategies:** Like having different levels of storage (desk drawer, filing cabinet, warehouse) for different access patterns
- **Data Partitioning:** Like dividing a large library into different sections (fiction, non-fiction, reference)
- **Event Sourcing:** Like keeping a detailed log of all changes to a document
- **CQRS:** Like having separate systems for writing (cash register) and reading (display screen) in a store
- **Microservices Communication:** Like different departments in a company working together through clear interfaces
- **Consensus Algorithms:** Like a group of people agreeing on a decision through voting

System design and architecture are crucial for building scalable, maintainable, and reliable systems. Understanding these patterns and algorithms helps in designing systems that can handle growth and complexity while maintaining performance and reliability.