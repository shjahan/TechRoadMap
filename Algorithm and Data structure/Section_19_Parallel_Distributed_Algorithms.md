# Section 19 – Parallel & Distributed Algorithms

## 19.1 Parallel Algorithm Design

Parallel algorithms are designed to solve problems using multiple processors simultaneously, reducing execution time and improving performance.

### Key Concepts

**Parallelism:** The ability to execute multiple operations simultaneously
**Speedup:** The ratio of sequential execution time to parallel execution time
**Efficiency:** The ratio of speedup to the number of processors
**Load Balancing:** Distributing work evenly across processors
**Synchronization:** Coordinating access to shared resources

**Real-world Analogy:**
Think of parallel algorithms like having multiple chefs working in a kitchen. Instead of one chef doing everything sequentially, you can have one chef chopping vegetables while another is cooking pasta and a third is preparing the sauce. This way, the meal gets ready much faster than if one person did everything step by step.

### Basic Parallel Algorithm Template

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ParallelAlgorithm {
    private ExecutorService executor;
    private int numThreads;
    
    public ParallelAlgorithm(int numThreads) {
        this.numThreads = numThreads;
        this.executor = Executors.newFixedThreadPool(numThreads);
    }
    
    // Parallel sum using divide and conquer
    public int parallelSum(int[] arr) throws InterruptedException {
        if (arr.length == 0) return 0;
        if (arr.length == 1) return arr[0];
        
        int chunkSize = arr.length / numThreads;
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < numThreads; i++) {
            int start = i * chunkSize;
            int end = (i == numThreads - 1) ? arr.length : (i + 1) * chunkSize;
            
            Future<Integer> future = executor.submit(() -> {
                int sum = 0;
                for (int j = start; j < end; j++) {
                    sum += arr[j];
                }
                return sum;
            });
            
            futures.add(future);
        }
        
        int totalSum = 0;
        for (Future<Integer> future : futures) {
            totalSum += future.get();
        }
        
        return totalSum;
    }
    
    // Parallel maximum finding
    public int parallelMax(int[] arr) throws InterruptedException {
        if (arr.length == 0) throw new IllegalArgumentException("Array is empty");
        
        int chunkSize = arr.length / numThreads;
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < numThreads; i++) {
            int start = i * chunkSize;
            int end = (i == numThreads - 1) ? arr.length : (i + 1) * chunkSize;
            
            Future<Integer> future = executor.submit(() -> {
                int max = Integer.MIN_VALUE;
                for (int j = start; j < end; j++) {
                    max = Math.max(max, arr[j]);
                }
                return max;
            });
            
            futures.add(future);
        }
        
        int globalMax = Integer.MIN_VALUE;
        for (Future<Integer> future : futures) {
            globalMax = Math.max(globalMax, future.get());
        }
        
        return globalMax;
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}
```

## 19.2 MapReduce Paradigm

MapReduce is a programming model for processing large datasets in parallel.

### Basic MapReduce Implementation

```java
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

public class MapReduce<T, K, V> {
    private ExecutorService executor;
    private int numWorkers;
    
    public MapReduce(int numWorkers) {
        this.numWorkers = numWorkers;
        this.executor = Executors.newFixedThreadPool(numWorkers);
    }
    
    // Map function interface
    @FunctionalInterface
    public interface MapFunction<T, K, V> {
        List<Map.Entry<K, V>> map(T input);
    }
    
    // Reduce function interface
    @FunctionalInterface
    public interface ReduceFunction<K, V> {
        V reduce(K key, List<V> values);
    }
    
    // Execute MapReduce job
    public Map<K, V> execute(List<T> input, 
                            MapFunction<T, K, V> mapFunction,
                            ReduceFunction<K, V> reduceFunction) throws InterruptedException {
        
        // Map phase
        List<Future<List<Map.Entry<K, V>>>> mapFutures = new ArrayList<>();
        
        for (T item : input) {
            Future<List<Map.Entry<K, V>>> future = executor.submit(() -> mapFunction.map(item));
            mapFutures.add(future);
        }
        
        // Collect all key-value pairs
        Map<K, List<V>> groupedData = new HashMap<>();
        
        for (Future<List<Map.Entry<K, V>>> future : mapFutures) {
            List<Map.Entry<K, V>> entries = future.get();
            for (Map.Entry<K, V> entry : entries) {
                groupedData.computeIfAbsent(entry.getKey(), k -> new ArrayList<>())
                          .add(entry.getValue());
            }
        }
        
        // Reduce phase
        List<Future<Map.Entry<K, V>>> reduceFutures = new ArrayList<>();
        
        for (Map.Entry<K, List<V>> entry : groupedData.entrySet()) {
            K key = entry.getKey();
            List<V> values = entry.getValue();
            
            Future<Map.Entry<K, V>> future = executor.submit(() -> {
                V result = reduceFunction.reduce(key, values);
                return new AbstractMap.SimpleEntry<>(key, result);
            });
            
            reduceFutures.add(future);
        }
        
        // Collect results
        Map<K, V> result = new HashMap<>();
        for (Future<Map.Entry<K, V>> future : reduceFutures) {
            Map.Entry<K, V> entry = future.get();
            result.put(entry.getKey(), entry.getValue());
        }
        
        return result;
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}
```

### Word Count Example

```java
public class WordCountMapReduce {
    public static void main(String[] args) throws InterruptedException {
        MapReduce<String, String, Integer> mapReduce = new MapReduce<>(4);
        
        List<String> documents = Arrays.asList(
            "hello world hello",
            "world hello world",
            "hello hello world"
        );
        
        // Map function: split document into words and emit (word, 1)
        MapReduce.MapFunction<String, String, Integer> mapFunction = document -> {
            List<Map.Entry<String, Integer>> result = new ArrayList<>();
            String[] words = document.split("\\s+");
            for (String word : words) {
                result.add(new AbstractMap.SimpleEntry<>(word, 1));
            }
            return result;
        };
        
        // Reduce function: sum up counts for each word
        MapReduce.ReduceFunction<String, Integer> reduceFunction = (word, counts) -> {
            return counts.stream().mapToInt(Integer::intValue).sum();
        };
        
        Map<String, Integer> wordCounts = mapReduce.execute(documents, mapFunction, reduceFunction);
        
        System.out.println("Word counts:");
        wordCounts.forEach((word, count) -> 
            System.out.println(word + ": " + count));
        
        mapReduce.shutdown();
    }
}
```

## 19.3 Parallel Sorting

### Parallel Merge Sort

```java
public class ParallelMergeSort {
    private ExecutorService executor;
    private int numThreads;
    
    public ParallelMergeSort(int numThreads) {
        this.numThreads = numThreads;
        this.executor = Executors.newFixedThreadPool(numThreads);
    }
    
    public void parallelMergeSort(int[] arr) throws InterruptedException {
        parallelMergeSort(arr, 0, arr.length - 1, 0);
    }
    
    private void parallelMergeSort(int[] arr, int left, int right, int depth) throws InterruptedException {
        if (left >= right) return;
        
        int mid = left + (right - left) / 2;
        
        // Use parallel processing for deeper levels
        if (depth < Math.log(numThreads) / Math.log(2)) {
            Future<?> leftFuture = executor.submit(() -> {
                try {
                    parallelMergeSort(arr, left, mid, depth + 1);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            Future<?> rightFuture = executor.submit(() -> {
                try {
                    parallelMergeSort(arr, mid + 1, right, depth + 1);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            leftFuture.get();
            rightFuture.get();
        } else {
            // Use sequential processing for deeper levels
            parallelMergeSort(arr, left, mid, depth + 1);
            parallelMergeSort(arr, mid + 1, right, depth + 1);
        }
        
        merge(arr, left, mid, right);
    }
    
    private void merge(int[] arr, int left, int mid, int right) {
        int[] temp = new int[right - left + 1];
        int i = left, j = mid + 1, k = 0;
        
        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) {
                temp[k++] = arr[i++];
            } else {
                temp[k++] = arr[j++];
            }
        }
        
        while (i <= mid) temp[k++] = arr[i++];
        while (j <= right) temp[k++] = arr[j++];
        
        System.arraycopy(temp, 0, arr, left, temp.length);
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}
```

### Parallel Quick Sort

```java
public class ParallelQuickSort {
    private ExecutorService executor;
    private int numThreads;
    
    public ParallelQuickSort(int numThreads) {
        this.numThreads = numThreads;
        this.executor = Executors.newFixedThreadPool(numThreads);
    }
    
    public void parallelQuickSort(int[] arr) throws InterruptedException {
        parallelQuickSort(arr, 0, arr.length - 1, 0);
    }
    
    private void parallelQuickSort(int[] arr, int left, int right, int depth) throws InterruptedException {
        if (left >= right) return;
        
        int pivotIndex = partition(arr, left, right);
        
        // Use parallel processing for deeper levels
        if (depth < Math.log(numThreads) / Math.log(2)) {
            Future<?> leftFuture = executor.submit(() -> {
                try {
                    parallelQuickSort(arr, left, pivotIndex - 1, depth + 1);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            Future<?> rightFuture = executor.submit(() -> {
                try {
                    parallelQuickSort(arr, pivotIndex + 1, right, depth + 1);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            leftFuture.get();
            rightFuture.get();
        } else {
            // Use sequential processing for deeper levels
            parallelQuickSort(arr, left, pivotIndex - 1, depth + 1);
            parallelQuickSort(arr, pivotIndex + 1, right, depth + 1);
        }
    }
    
    private int partition(int[] arr, int left, int right) {
        int pivot = arr[right];
        int i = left - 1;
        
        for (int j = left; j < right; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        
        swap(arr, i + 1, right);
        return i + 1;
    }
    
    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}
```

## 19.4 Parallel Graph Algorithms

### Parallel Breadth-First Search

```java
public class ParallelBFS {
    private ExecutorService executor;
    private int numThreads;
    
    public ParallelBFS(int numThreads) {
        this.numThreads = numThreads;
        this.executor = Executors.newFixedThreadPool(numThreads);
    }
    
    public int[] parallelBFS(List<List<Integer>> graph, int start) throws InterruptedException {
        int n = graph.size();
        int[] distances = new int[n];
        Arrays.fill(distances, -1);
        distances[start] = 0;
        
        Queue<Integer> currentLevel = new ConcurrentLinkedQueue<>();
        currentLevel.offer(start);
        
        int level = 0;
        
        while (!currentLevel.isEmpty()) {
            level++;
            Queue<Integer> nextLevel = new ConcurrentLinkedQueue<>();
            
            // Process current level in parallel
            List<Future<Void>> futures = new ArrayList<>();
            
            for (int i = 0; i < numThreads; i++) {
                Future<Void> future = executor.submit(() -> {
                    while (true) {
                        Integer node = currentLevel.poll();
                        if (node == null) break;
                        
                        for (int neighbor : graph.get(node)) {
                            if (distances[neighbor] == -1) {
                                distances[neighbor] = level;
                                nextLevel.offer(neighbor);
                            }
                        }
                    }
                    return null;
                });
                futures.add(future);
            }
            
            // Wait for all threads to complete
            for (Future<Void> future : futures) {
                future.get();
            }
            
            currentLevel = nextLevel;
        }
        
        return distances;
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}
```

### Parallel Dijkstra's Algorithm

```java
public class ParallelDijkstra {
    private ExecutorService executor;
    private int numThreads;
    
    public ParallelDijkstra(int numThreads) {
        this.numThreads = numThreads;
        this.executor = Executors.newFixedThreadPool(numThreads);
    }
    
    public int[] parallelDijkstra(List<List<Edge>> graph, int start) throws InterruptedException {
        int n = graph.size();
        int[] distances = new int[n];
        boolean[] visited = new boolean[n];
        Arrays.fill(distances, Integer.MAX_VALUE);
        distances[start] = 0;
        
        PriorityQueue<Edge> pq = new PriorityQueue<>();
        pq.offer(new Edge(start, 0));
        
        while (!pq.isEmpty()) {
            Edge current = pq.poll();
            int u = current.to;
            
            if (visited[u]) continue;
            visited[u] = true;
            
            // Process neighbors in parallel
            List<Future<Void>> futures = new ArrayList<>();
            
            for (int i = 0; i < numThreads; i++) {
                Future<Void> future = executor.submit(() -> {
                    for (Edge edge : graph.get(u)) {
                        int v = edge.to;
                        int weight = edge.weight;
                        
                        if (!visited[v] && distances[u] + weight < distances[v]) {
                            distances[v] = distances[u] + weight;
                            pq.offer(new Edge(v, distances[v]));
                        }
                    }
                    return null;
                });
                futures.add(future);
            }
            
            // Wait for all threads to complete
            for (Future<Void> future : futures) {
                future.get();
            }
        }
        
        return distances;
    }
    
    public static class Edge implements Comparable<Edge> {
        int to, weight;
        
        public Edge(int to, int weight) {
            this.to = to;
            this.weight = weight;
        }
        
        @Override
        public int compareTo(Edge other) {
            return Integer.compare(this.weight, other.weight);
        }
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}
```

## 19.5 Distributed Consensus

### Raft Algorithm (Simplified)

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
    }
    
    // Request vote RPC
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
    
    // Append entries RPC
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
        
        return success;
    }
    
    private boolean isUpToDate(int lastLogIndex, int lastLogTerm) {
        if (log.isEmpty()) return true;
        
        LogEntry lastEntry = log.get(log.size() - 1);
        return lastLogTerm > lastEntry.term || 
               (lastLogTerm == lastEntry.term && lastLogIndex >= log.size() - 1);
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

### PBFT (Practical Byzantine Fault Tolerance)

```java
public class PBFTNode {
    private int nodeId;
    private int totalNodes;
    private int f; // Maximum number of faulty nodes
    private int viewNumber;
    private int sequenceNumber;
    private Map<String, Request> pendingRequests;
    private Map<String, List<PrePrepare>> prePrepareMessages;
    private Map<String, List<Prepare>> prepareMessages;
    private Map<String, List<Commit>> commitMessages;
    
    public PBFTNode(int nodeId, int totalNodes) {
        this.nodeId = nodeId;
        this.totalNodes = totalNodes;
        this.f = (totalNodes - 1) / 3;
        this.viewNumber = 0;
        this.sequenceNumber = 0;
        this.pendingRequests = new HashMap<>();
        this.prePrepareMessages = new HashMap<>();
        this.prepareMessages = new HashMap<>();
        this.commitMessages = new HashMap<>();
    }
    
    // Pre-prepare phase
    public void prePrepare(Request request) {
        if (isPrimary()) {
            sequenceNumber++;
            String requestId = generateRequestId(request);
            pendingRequests.put(requestId, request);
            
            PrePrepare prePrepare = new PrePrepare(viewNumber, sequenceNumber, requestId, request);
            broadcast(prePrepare);
        }
    }
    
    // Prepare phase
    public void prepare(PrePrepare prePrepare) {
        if (validatePrePrepare(prePrepare)) {
            String requestId = prePrepare.requestId;
            prePrepareMessages.computeIfAbsent(requestId, k -> new ArrayList<>()).add(prePrepare);
            
            if (prePrepareMessages.get(requestId).size() >= 2 * f + 1) {
                Prepare prepare = new Prepare(viewNumber, sequenceNumber, requestId, nodeId);
                broadcast(prepare);
            }
        }
    }
    
    // Commit phase
    public void commit(Prepare prepare) {
        if (validatePrepare(prepare)) {
            String requestId = prepare.requestId;
            prepareMessages.computeIfAbsent(requestId, k -> new ArrayList<>()).add(prepare);
            
            if (prepareMessages.get(requestId).size() >= 2 * f + 1) {
                Commit commit = new Commit(viewNumber, sequenceNumber, requestId, nodeId);
                broadcast(commit);
            }
        }
    }
    
    // Execute committed request
    public void execute(Commit commit) {
        if (validateCommit(commit)) {
            String requestId = commit.requestId;
            commitMessages.computeIfAbsent(requestId, k -> new ArrayList<>()).add(commit);
            
            if (commitMessages.get(requestId).size() >= 2 * f + 1) {
                Request request = pendingRequests.get(requestId);
                if (request != null) {
                    executeRequest(request);
                    pendingRequests.remove(requestId);
                }
            }
        }
    }
    
    private boolean isPrimary() {
        return nodeId == (viewNumber % totalNodes);
    }
    
    private boolean validatePrePrepare(PrePrepare prePrepare) {
        return prePrepare.viewNumber == viewNumber &&
               prePrepare.sequenceNumber > sequenceNumber &&
               isValidRequest(prePrepare.request);
    }
    
    private boolean validatePrepare(Prepare prepare) {
        return prepare.viewNumber == viewNumber &&
               prepare.sequenceNumber == sequenceNumber;
    }
    
    private boolean validateCommit(Commit commit) {
        return commit.viewNumber == viewNumber &&
               commit.sequenceNumber == sequenceNumber;
    }
    
    private void broadcast(Object message) {
        // Implementation would send message to all nodes
        System.out.println("Node " + nodeId + " broadcasting: " + message);
    }
    
    private String generateRequestId(Request request) {
        return request.clientId + "_" + request.timestamp;
    }
    
    private boolean isValidRequest(Request request) {
        // Validate request format and content
        return request != null && request.clientId != null;
    }
    
    private void executeRequest(Request request) {
        System.out.println("Node " + nodeId + " executing request: " + request);
    }
    
    public static class Request {
        String clientId;
        long timestamp;
        String operation;
        
        public Request(String clientId, long timestamp, String operation) {
            this.clientId = clientId;
            this.timestamp = timestamp;
            this.operation = operation;
        }
    }
    
    public static class PrePrepare {
        int viewNumber;
        int sequenceNumber;
        String requestId;
        Request request;
        
        public PrePrepare(int viewNumber, int sequenceNumber, String requestId, Request request) {
            this.viewNumber = viewNumber;
            this.sequenceNumber = sequenceNumber;
            this.requestId = requestId;
            this.request = request;
        }
    }
    
    public static class Prepare {
        int viewNumber;
        int sequenceNumber;
        String requestId;
        int nodeId;
        
        public Prepare(int viewNumber, int sequenceNumber, String requestId, int nodeId) {
            this.viewNumber = viewNumber;
            this.sequenceNumber = sequenceNumber;
            this.requestId = requestId;
            this.nodeId = nodeId;
        }
    }
    
    public static class Commit {
        int viewNumber;
        int sequenceNumber;
        String requestId;
        int nodeId;
        
        public Commit(int viewNumber, int sequenceNumber, String requestId, int nodeId) {
            this.viewNumber = viewNumber;
            this.sequenceNumber = sequenceNumber;
            this.requestId = requestId;
            this.nodeId = nodeId;
        }
    }
}
```

## 19.6 Load Balancing Algorithms

### Round Robin Load Balancer

```java
public class RoundRobinLoadBalancer {
    private List<String> servers;
    private AtomicInteger currentIndex;
    
    public RoundRobinLoadBalancer(List<String> servers) {
        this.servers = new ArrayList<>(servers);
        this.currentIndex = new AtomicInteger(0);
    }
    
    public String getNextServer() {
        int index = currentIndex.getAndIncrement() % servers.size();
        return servers.get(index);
    }
    
    public void addServer(String server) {
        servers.add(server);
    }
    
    public void removeServer(String server) {
        servers.remove(server);
    }
}
```

### Weighted Round Robin Load Balancer

```java
public class WeightedRoundRobinLoadBalancer {
    private List<Server> servers;
    private AtomicInteger currentWeight;
    private AtomicInteger currentIndex;
    
    public WeightedRoundRobinLoadBalancer(List<Server> servers) {
        this.servers = new ArrayList<>(servers);
        this.currentWeight = new AtomicInteger(0);
        this.currentIndex = new AtomicInteger(-1);
    }
    
    public String getNextServer() {
        while (true) {
            int index = currentIndex.getAndIncrement() % servers.size();
            if (index == 0) {
                currentWeight.addAndGet(-getTotalWeight());
                if (currentWeight.get() <= 0) {
                    currentWeight.set(getTotalWeight());
                }
            }
            
            Server server = servers.get(index);
            if (server.weight >= currentWeight.get()) {
                return server.name;
            }
        }
    }
    
    private int getTotalWeight() {
        return servers.stream().mapToInt(s -> s.weight).sum();
    }
    
    public static class Server {
        String name;
        int weight;
        
        public Server(String name, int weight) {
            this.name = name;
            this.weight = weight;
        }
    }
}
```

### Least Connections Load Balancer

```java
public class LeastConnectionsLoadBalancer {
    private List<Server> servers;
    private Map<String, AtomicInteger> connectionCounts;
    
    public LeastConnectionsLoadBalancer(List<Server> servers) {
        this.servers = new ArrayList<>(servers);
        this.connectionCounts = new HashMap<>();
        
        for (Server server : servers) {
            connectionCounts.put(server.name, new AtomicInteger(0));
        }
    }
    
    public String getNextServer() {
        Server selectedServer = null;
        int minConnections = Integer.MAX_VALUE;
        
        for (Server server : servers) {
            int connections = connectionCounts.get(server.name).get();
            if (connections < minConnections) {
                minConnections = connections;
                selectedServer = server;
            }
        }
        
        if (selectedServer != null) {
            connectionCounts.get(selectedServer.name).incrementAndGet();
        }
        
        return selectedServer != null ? selectedServer.name : null;
    }
    
    public void releaseConnection(String serverName) {
        connectionCounts.get(serverName).decrementAndGet();
    }
    
    public static class Server {
        String name;
        int weight;
        
        public Server(String name, int weight) {
            this.name = name;
            this.weight = weight;
        }
    }
}
```

## 19.7 Fault Tolerance

### Circuit Breaker Pattern

```java
public class CircuitBreaker {
    private enum State {
        CLOSED, OPEN, HALF_OPEN
    }
    
    private State state;
    private int failureCount;
    private int failureThreshold;
    private long timeout;
    private long lastFailureTime;
    private long retryTimeout;
    
    public CircuitBreaker(int failureThreshold, long timeout, long retryTimeout) {
        this.state = State.CLOSED;
        this.failureCount = 0;
        this.failureThreshold = failureThreshold;
        this.timeout = timeout;
        this.retryTimeout = retryTimeout;
    }
    
    public <T> T execute(Supplier<T> operation) throws Exception {
        if (state == State.OPEN) {
            if (System.currentTimeMillis() - lastFailureTime > retryTimeout) {
                state = State.HALF_OPEN;
            } else {
                throw new RuntimeException("Circuit breaker is OPEN");
            }
        }
        
        try {
            T result = operation.get();
            onSuccess();
            return result;
        } catch (Exception e) {
            onFailure();
            throw e;
        }
    }
    
    private void onSuccess() {
        failureCount = 0;
        state = State.CLOSED;
    }
    
    private void onFailure() {
        failureCount++;
        lastFailureTime = System.currentTimeMillis();
        
        if (failureCount >= failureThreshold) {
            state = State.OPEN;
        }
    }
    
    public State getState() {
        return state;
    }
}
```

### Retry Mechanism

```java
public class RetryMechanism {
    private int maxRetries;
    private long delay;
    private double backoffMultiplier;
    
    public RetryMechanism(int maxRetries, long delay, double backoffMultiplier) {
        this.maxRetries = maxRetries;
        this.delay = delay;
        this.backoffMultiplier = backoffMultiplier;
    }
    
    public <T> T execute(Supplier<T> operation) throws Exception {
        Exception lastException = null;
        long currentDelay = delay;
        
        for (int attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                return operation.get();
            } catch (Exception e) {
                lastException = e;
                
                if (attempt < maxRetries) {
                    Thread.sleep(currentDelay);
                    currentDelay = (long) (currentDelay * backoffMultiplier);
                }
            }
        }
        
        throw new RuntimeException("Operation failed after " + maxRetries + " retries", lastException);
    }
}
```

## 19.8 Consistency Models

### Eventual Consistency

```java
public class EventualConsistency {
    private Map<String, Object> data;
    private List<Operation> operations;
    private ExecutorService executor;
    
    public EventualConsistency() {
        this.data = new ConcurrentHashMap<>();
        this.operations = new ArrayList<>();
        this.executor = Executors.newFixedThreadPool(4);
    }
    
    public void write(String key, Object value) {
        Operation operation = new Operation(OperationType.WRITE, key, value, System.currentTimeMillis());
        operations.add(operation);
        
        // Apply operation locally
        data.put(key, value);
        
        // Replicate to other nodes asynchronously
        executor.submit(() -> replicateOperation(operation));
    }
    
    public Object read(String key) {
        return data.get(key);
    }
    
    private void replicateOperation(Operation operation) {
        // Simulate replication to other nodes
        try {
            Thread.sleep(100); // Simulate network delay
            System.out.println("Replicated operation: " + operation);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public void applyOperation(Operation operation) {
        if (operation.type == OperationType.WRITE) {
            data.put(operation.key, operation.value);
        }
    }
    
    public static class Operation {
        OperationType type;
        String key;
        Object value;
        long timestamp;
        
        public Operation(OperationType type, String key, Object value, long timestamp) {
            this.type = type;
            this.key = key;
            this.value = value;
            this.timestamp = timestamp;
        }
    }
    
    public enum OperationType {
        WRITE, READ
    }
}
```

### Strong Consistency

```java
public class StrongConsistency {
    private Map<String, Object> data;
    private List<Operation> operations;
    private int quorumSize;
    
    public StrongConsistency(int quorumSize) {
        this.data = new ConcurrentHashMap<>();
        this.operations = new ArrayList<>();
        this.quorumSize = quorumSize;
    }
    
    public void write(String key, Object value) throws InterruptedException {
        Operation operation = new Operation(OperationType.WRITE, key, value, System.currentTimeMillis());
        
        // Wait for quorum acknowledgment
        int acknowledgments = 0;
        while (acknowledgments < quorumSize) {
            // Simulate waiting for acknowledgments
            Thread.sleep(10);
            acknowledgments++;
        }
        
        // Apply operation only after quorum acknowledgment
        data.put(key, value);
        operations.add(operation);
    }
    
    public Object read(String key) throws InterruptedException {
        // Wait for quorum acknowledgment for read
        int acknowledgments = 0;
        while (acknowledgments < quorumSize) {
            Thread.sleep(10);
            acknowledgments++;
        }
        
        return data.get(key);
    }
    
    public static class Operation {
        OperationType type;
        String key;
        Object value;
        long timestamp;
        
        public Operation(OperationType type, String key, Object value, long timestamp) {
            this.type = type;
            this.key = key;
            this.value = value;
            this.timestamp = timestamp;
        }
    }
    
    public enum OperationType {
        WRITE, READ
    }
}
```

**Real-world Analogies:**
- **Parallel Algorithms:** Like having multiple chefs working in a kitchen simultaneously
- **MapReduce:** Like dividing a large task among many workers and then combining their results
- **Parallel Sorting:** Like having multiple people sort different parts of a deck of cards simultaneously
- **Distributed Consensus:** Like a group of people agreeing on a decision through voting
- **Load Balancing:** Like a traffic controller directing cars to different lanes to avoid congestion
- **Fault Tolerance:** Like having backup systems that kick in when the main system fails
- **Consistency Models:** Like different levels of synchronization in a team project

Parallel and distributed algorithms are essential for building scalable, high-performance systems that can handle large amounts of data and provide reliable services even when individual components fail.