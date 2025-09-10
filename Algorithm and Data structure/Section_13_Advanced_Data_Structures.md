# Section 13 – Advanced Data Structures

## 13.1 Disjoint Set Union (Union-Find)

Disjoint Set Union (DSU) or Union-Find is a data structure that efficiently handles disjoint sets and supports two main operations: finding which set an element belongs to and merging two sets.

### Basic Union-Find Implementation

```java
public class UnionFind {
    private int[] parent;
    private int[] rank;
    private int count; // Number of disjoint sets
    
    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        count = n;
        
        // Initialize each element as its own parent
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            rank[i] = 0;
        }
    }
    
    // Find root of element x with path compression
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // Path compression
        }
        return parent[x];
    }
    
    // Union two sets by rank
    public void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX == rootY) {
            return; // Already in same set
        }
        
        // Union by rank: attach smaller tree to larger tree
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else if (rank[rootX] > rank[rootY]) {
            parent[rootY] = rootX;
        } else {
            parent[rootY] = rootX;
            rank[rootX]++;
        }
        
        count--; // Decrease number of disjoint sets
    }
    
    // Check if two elements are in same set
    public boolean connected(int x, int y) {
        return find(x) == find(y);
    }
    
    // Get number of disjoint sets
    public int getCount() {
        return count;
    }
}
```

### Applications of Union-Find

**1. Kruskal's Minimum Spanning Tree Algorithm**

```java
public class KruskalMST {
    private static class Edge implements Comparable<Edge> {
        int src, dest, weight;
        
        public Edge(int src, int dest, int weight) {
            this.src = src;
            this.dest = dest;
            this.weight = weight;
        }
        
        @Override
        public int compareTo(Edge other) {
            return Integer.compare(this.weight, other.weight);
        }
    }
    
    public static List<Edge> findMST(List<Edge> edges, int vertices) {
        // Sort edges by weight
        Collections.sort(edges);
        
        UnionFind uf = new UnionFind(vertices);
        List<Edge> mst = new ArrayList<>();
        
        for (Edge edge : edges) {
            if (!uf.connected(edge.src, edge.dest)) {
                mst.add(edge);
                uf.union(edge.src, edge.dest);
                
                if (mst.size() == vertices - 1) {
                    break; // MST complete
                }
            }
        }
        
        return mst;
    }
}
```

**2. Detecting Cycles in Undirected Graph**

```java
public class CycleDetection {
    public static boolean hasCycle(List<Edge> edges, int vertices) {
        UnionFind uf = new UnionFind(vertices);
        
        for (Edge edge : edges) {
            if (uf.connected(edge.src, edge.dest)) {
                return true; // Cycle detected
            }
            uf.union(edge.src, edge.dest);
        }
        
        return false;
    }
}
```

**3. Number of Connected Components**

```java
public class ConnectedComponents {
    public static int countComponents(int[][] edges, int n) {
        UnionFind uf = new UnionFind(n);
        
        for (int[] edge : edges) {
            uf.union(edge[0], edge[1]);
        }
        
        return uf.getCount();
    }
}
```

## 13.2 Sparse Tables

Sparse Tables provide efficient range minimum/maximum queries on static arrays with O(1) query time after O(n log n) preprocessing.

### Range Minimum Query (RMQ)

```java
public class SparseTable {
    private int[][] table;
    private int[] log;
    private int n;
    
    public SparseTable(int[] arr) {
        this.n = arr.length;
        this.log = new int[n + 1];
        this.table = new int[n][log2(n) + 1];
        
        // Precompute log values
        for (int i = 2; i <= n; i++) {
            log[i] = log[i / 2] + 1;
        }
        
        // Build sparse table
        buildTable(arr);
    }
    
    private void buildTable(int[] arr) {
        // Initialize table with single elements
        for (int i = 0; i < n; i++) {
            table[i][0] = arr[i];
        }
        
        // Build table for powers of 2
        for (int j = 1; j <= log2(n); j++) {
            for (int i = 0; i + (1 << j) <= n; i++) {
                table[i][j] = Math.min(table[i][j - 1], table[i + (1 << (j - 1))][j - 1]);
            }
        }
    }
    
    // Range minimum query in O(1)
    public int query(int left, int right) {
        int length = right - left + 1;
        int k = log[length];
        return Math.min(table[left][k], table[right - (1 << k) + 1][k]);
    }
    
    private int log2(int n) {
        return (int) (Math.log(n) / Math.log(2));
    }
}
```

### Range Maximum Query

```java
public class SparseTableMax {
    private int[][] table;
    private int[] log;
    private int n;
    
    public SparseTableMax(int[] arr) {
        this.n = arr.length;
        this.log = new int[n + 1];
        this.table = new int[n][log2(n) + 1];
        
        // Precompute log values
        for (int i = 2; i <= n; i++) {
            log[i] = log[i / 2] + 1;
        }
        
        buildTable(arr);
    }
    
    private void buildTable(int[] arr) {
        for (int i = 0; i < n; i++) {
            table[i][0] = arr[i];
        }
        
        for (int j = 1; j <= log2(n); j++) {
            for (int i = 0; i + (1 << j) <= n; i++) {
                table[i][j] = Math.max(table[i][j - 1], table[i + (1 << (j - 1))][j - 1]);
            }
        }
    }
    
    public int query(int left, int right) {
        int length = right - left + 1;
        int k = log[length];
        return Math.max(table[left][k], table[right - (1 << k) + 1][k]);
    }
    
    private int log2(int n) {
        return (int) (Math.log(n) / Math.log(2));
    }
}
```

## 13.3 Heavy-Light Decomposition

Heavy-Light Decomposition (HLD) is a technique for decomposing trees into chains to enable efficient path queries.

### HLD Implementation

```java
public class HeavyLightDecomposition {
    private List<List<Integer>> tree;
    private int[] parent, depth, heavy, head, pos;
    private int[] values;
    private int n, curPos;
    
    public HeavyLightDecomposition(List<List<Integer>> tree, int[] values) {
        this.tree = tree;
        this.values = values;
        this.n = tree.size();
        this.parent = new int[n];
        this.depth = new int[n];
        this.heavy = new int[n];
        this.head = new int[n];
        this.pos = new int[n];
        this.curPos = 0;
        
        Arrays.fill(heavy, -1);
        Arrays.fill(head, -1);
        
        dfs(0, -1);
        decompose(0, 0);
    }
    
    private int dfs(int v, int p) {
        parent[v] = p;
        depth[v] = (p == -1) ? 0 : depth[p] + 1;
        
        int size = 1;
        int maxChildSize = 0;
        
        for (int u : tree.get(v)) {
            if (u != p) {
                int childSize = dfs(u, v);
                size += childSize;
                
                if (childSize > maxChildSize) {
                    maxChildSize = childSize;
                    heavy[v] = u;
                }
            }
        }
        
        return size;
    }
    
    private void decompose(int v, int h) {
        head[v] = h;
        pos[v] = curPos++;
        
        if (heavy[v] != -1) {
            decompose(heavy[v], h);
        }
        
        for (int u : tree.get(v)) {
            if (u != parent[v] && u != heavy[v]) {
                decompose(u, u);
            }
        }
    }
    
    // Query maximum value on path from u to v
    public int queryPath(int u, int v) {
        int res = Integer.MIN_VALUE;
        
        while (head[u] != head[v]) {
            if (depth[head[u]] > depth[head[v]]) {
                int temp = u;
                u = v;
                v = temp;
            }
            
            res = Math.max(res, queryRange(pos[head[v]], pos[v]));
            v = parent[head[v]];
        }
        
        if (depth[u] > depth[v]) {
            int temp = u;
            u = v;
            v = temp;
        }
        
        res = Math.max(res, queryRange(pos[u], pos[v]));
        return res;
    }
    
    private int queryRange(int l, int r) {
        // This would typically use a segment tree or other range query structure
        // For simplicity, we'll use a linear scan here
        int max = Integer.MIN_VALUE;
        for (int i = l; i <= r; i++) {
            max = Math.max(max, values[i]);
        }
        return max;
    }
}
```

## 13.4 Persistent Data Structures

Persistent data structures maintain multiple versions of themselves, allowing access to historical states.

### Persistent Array

```java
public class PersistentArray<T> {
    private static class Node<T> {
        T value;
        Node<T> left, right;
        int version;
        
        public Node(T value, int version) {
            this.value = value;
            this.version = version;
            this.left = null;
            this.right = null;
        }
    }
    
    private Node<T>[] roots;
    private int currentVersion;
    private int size;
    
    @SuppressWarnings("unchecked")
    public PersistentArray(T[] initialArray) {
        this.size = initialArray.length;
        this.roots = new Node[1000]; // Pre-allocate space for versions
        this.currentVersion = 0;
        
        roots[0] = buildTree(initialArray, 0, size - 1, 0);
    }
    
    private Node<T> buildTree(T[] arr, int start, int end, int version) {
        if (start == end) {
            return new Node<>(arr[start], version);
        }
        
        int mid = start + (end - start) / 2;
        Node<T> node = new Node<>(null, version);
        node.left = buildTree(arr, start, mid, version);
        node.right = buildTree(arr, mid + 1, end, version);
        
        return node;
    }
    
    public T get(int index, int version) {
        return get(roots[version], 0, size - 1, index);
    }
    
    private T get(Node<T> node, int start, int end, int index) {
        if (start == end) {
            return node.value;
        }
        
        int mid = start + (end - start) / 2;
        if (index <= mid) {
            return get(node.left, start, mid, index);
        } else {
            return get(node.right, mid + 1, end, index);
        }
    }
    
    public int update(int index, T value) {
        currentVersion++;
        roots[currentVersion] = update(roots[currentVersion - 1], 0, size - 1, index, value, currentVersion);
        return currentVersion;
    }
    
    private Node<T> update(Node<T> node, int start, int end, int index, T value, int version) {
        if (start == end) {
            return new Node<>(value, version);
        }
        
        int mid = start + (end - start) / 2;
        Node<T> newNode = new Node<>(node.value, version);
        
        if (index <= mid) {
            newNode.left = update(node.left, start, mid, index, value, version);
            newNode.right = node.right;
        } else {
            newNode.left = node.left;
            newNode.right = update(node.right, mid + 1, end, index, value, version);
        }
        
        return newNode;
    }
}
```

### Persistent Stack

```java
public class PersistentStack<T> {
    private static class Node<T> {
        T value;
        Node<T> next;
        int version;
        
        public Node(T value, Node<T> next, int version) {
            this.value = value;
            this.next = next;
            this.version = version;
        }
    }
    
    private Node<T>[] versions;
    private int currentVersion;
    
    @SuppressWarnings("unchecked")
    public PersistentStack() {
        this.versions = new Node[1000];
        this.currentVersion = 0;
        versions[0] = null; // Empty stack
    }
    
    public PersistentStack<T> push(T value) {
        currentVersion++;
        versions[currentVersion] = new Node<>(value, versions[currentVersion - 1], currentVersion);
        return this;
    }
    
    public T top(int version) {
        if (versions[version] == null) {
            throw new IllegalStateException("Stack is empty");
        }
        return versions[version].value;
    }
    
    public PersistentStack<T> pop(int version) {
        if (versions[version] == null) {
            throw new IllegalStateException("Stack is empty");
        }
        
        currentVersion++;
        versions[currentVersion] = versions[version].next;
        return this;
    }
    
    public boolean isEmpty(int version) {
        return versions[version] == null;
    }
}
```

## 13.5 Skip Lists

Skip Lists are probabilistic data structures that provide O(log n) search, insertion, and deletion with high probability.

### Skip List Implementation

```java
import java.util.Random;

public class SkipList<T extends Comparable<T>> {
    private static final int MAX_LEVEL = 16;
    private static final double PROBABILITY = 0.5;
    
    private static class Node<T> {
        T value;
        Node<T>[] forward;
        int level;
        
        @SuppressWarnings("unchecked")
        public Node(T value, int level) {
            this.value = value;
            this.level = level;
            this.forward = new Node[level + 1];
        }
    }
    
    private Node<T> header;
    private int level;
    private Random random;
    
    public SkipList() {
        this.header = new Node<>(null, MAX_LEVEL);
        this.level = 0;
        this.random = new Random();
    }
    
    public boolean search(T value) {
        Node<T> current = header;
        
        for (int i = level; i >= 0; i--) {
            while (current.forward[i] != null && 
                   current.forward[i].value.compareTo(value) < 0) {
                current = current.forward[i];
            }
        }
        
        current = current.forward[0];
        return current != null && current.value.equals(value);
    }
    
    public void insert(T value) {
        Node<T>[] update = new Node[MAX_LEVEL + 1];
        Node<T> current = header;
        
        // Find insertion point
        for (int i = level; i >= 0; i--) {
            while (current.forward[i] != null && 
                   current.forward[i].value.compareTo(value) < 0) {
                current = current.forward[i];
            }
            update[i] = current;
        }
        
        current = current.forward[0];
        
        // If value already exists, don't insert
        if (current == null || !current.value.equals(value)) {
            int newLevel = randomLevel();
            
            // If new level is higher than current level, update header
            if (newLevel > level) {
                for (int i = level + 1; i <= newLevel; i++) {
                    update[i] = header;
                }
                level = newLevel;
            }
            
            // Create new node
            Node<T> newNode = new Node<>(value, newLevel);
            
            // Update forward pointers
            for (int i = 0; i <= newLevel; i++) {
                newNode.forward[i] = update[i].forward[i];
                update[i].forward[i] = newNode;
            }
        }
    }
    
    public void delete(T value) {
        Node<T>[] update = new Node[MAX_LEVEL + 1];
        Node<T> current = header;
        
        // Find node to delete
        for (int i = level; i >= 0; i--) {
            while (current.forward[i] != null && 
                   current.forward[i].value.compareTo(value) < 0) {
                current = current.forward[i];
            }
            update[i] = current;
        }
        
        current = current.forward[0];
        
        // If value exists, delete it
        if (current != null && current.value.equals(value)) {
            for (int i = 0; i <= level; i++) {
                if (update[i].forward[i] != current) {
                    break;
                }
                update[i].forward[i] = current.forward[i];
            }
            
            // Decrease level if necessary
            while (level > 0 && header.forward[level] == null) {
                level--;
            }
        }
    }
    
    private int randomLevel() {
        int level = 0;
        while (random.nextDouble() < PROBABILITY && level < MAX_LEVEL) {
            level++;
        }
        return level;
    }
    
    public void print() {
        for (int i = level; i >= 0; i--) {
            System.out.print("Level " + i + ": ");
            Node<T> current = header.forward[i];
            while (current != null) {
                System.out.print(current.value + " ");
                current = current.forward[i];
            }
            System.out.println();
        }
    }
}
```

## 13.6 Bloom Filters

Bloom Filters are space-efficient probabilistic data structures that test whether an element is a member of a set.

### Basic Bloom Filter

```java
import java.util.BitSet;
import java.util.Random;

public class BloomFilter {
    private BitSet bitSet;
    private int size;
    private int hashFunctions;
    private Random random;
    
    public BloomFilter(int expectedElements, double falsePositiveRate) {
        this.size = calculateSize(expectedElements, falsePositiveRate);
        this.hashFunctions = calculateHashFunctions(expectedElements, size);
        this.bitSet = new BitSet(size);
        this.random = new Random();
    }
    
    private int calculateSize(int n, double p) {
        return (int) (-n * Math.log(p) / (Math.log(2) * Math.log(2)));
    }
    
    private int calculateHashFunctions(int n, int m) {
        return (int) (m * Math.log(2) / n);
    }
    
    public void add(String element) {
        for (int i = 0; i < hashFunctions; i++) {
            int hash = hash(element, i);
            bitSet.set(Math.abs(hash % size));
        }
    }
    
    public boolean contains(String element) {
        for (int i = 0; i < hashFunctions; i++) {
            int hash = hash(element, i);
            if (!bitSet.get(Math.abs(hash % size))) {
                return false;
            }
        }
        return true;
    }
    
    private int hash(String element, int seed) {
        random.setSeed(seed);
        return element.hashCode() ^ random.nextInt();
    }
    
    public double getFalsePositiveRate() {
        return Math.pow(1 - Math.exp(-hashFunctions * (double) bitSet.cardinality() / size), hashFunctions);
    }
}
```

### Counting Bloom Filter

```java
public class CountingBloomFilter {
    private int[] counters;
    private int size;
    private int hashFunctions;
    private Random random;
    
    public CountingBloomFilter(int expectedElements, double falsePositiveRate) {
        this.size = calculateSize(expectedElements, falsePositiveRate);
        this.hashFunctions = calculateHashFunctions(expectedElements, size);
        this.counters = new int[size];
        this.random = new Random();
    }
    
    private int calculateSize(int n, double p) {
        return (int) (-n * Math.log(p) / (Math.log(2) * Math.log(2)));
    }
    
    private int calculateHashFunctions(int n, int m) {
        return (int) (m * Math.log(2) / n);
    }
    
    public void add(String element) {
        for (int i = 0; i < hashFunctions; i++) {
            int hash = hash(element, i);
            counters[Math.abs(hash % size)]++;
        }
    }
    
    public boolean contains(String element) {
        for (int i = 0; i < hashFunctions; i++) {
            int hash = hash(element, i);
            if (counters[Math.abs(hash % size)] == 0) {
                return false;
            }
        }
        return true;
    }
    
    public void remove(String element) {
        if (contains(element)) {
            for (int i = 0; i < hashFunctions; i++) {
                int hash = hash(element, i);
                counters[Math.abs(hash % size)]--;
            }
        }
    }
    
    private int hash(String element, int seed) {
        random.setSeed(seed);
        return element.hashCode() ^ random.nextInt();
    }
}
```

## 13.7 Count-Min Sketch

Count-Min Sketch is a probabilistic data structure for frequency estimation.

### Count-Min Sketch Implementation

```java
import java.util.Random;

public class CountMinSketch {
    private int[][] sketch;
    private int width;
    private int depth;
    private Random[] hashFunctions;
    
    public CountMinSketch(double epsilon, double delta) {
        this.width = (int) Math.ceil(Math.E / epsilon);
        this.depth = (int) Math.ceil(Math.log(1 / delta));
        this.sketch = new int[depth][width];
        this.hashFunctions = new Random[depth];
        
        for (int i = 0; i < depth; i++) {
            hashFunctions[i] = new Random(i);
        }
    }
    
    public void add(String element) {
        for (int i = 0; i < depth; i++) {
            int hash = hash(element, i);
            sketch[i][Math.abs(hash % width)]++;
        }
    }
    
    public int estimateCount(String element) {
        int minCount = Integer.MAX_VALUE;
        
        for (int i = 0; i < depth; i++) {
            int hash = hash(element, i);
            int count = sketch[i][Math.abs(hash % width)];
            minCount = Math.min(minCount, count);
        }
        
        return minCount;
    }
    
    private int hash(String element, int seed) {
        hashFunctions[seed].setSeed(seed);
        return element.hashCode() ^ hashFunctions[seed].nextInt();
    }
}
```

## 13.8 Probabilistic Data Structures

### HyperLogLog for Cardinality Estimation

```java
public class HyperLogLog {
    private int[] registers;
    private int m; // Number of registers (must be power of 2)
    private int b; // Number of bits to determine register
    private double alpha;
    
    public HyperLogLog(int b) {
        this.b = b;
        this.m = 1 << b; // 2^b
        this.registers = new int[m];
        this.alpha = getAlpha(m);
    }
    
    private double getAlpha(int m) {
        switch (m) {
            case 16: return 0.673;
            case 32: return 0.697;
            case 64: return 0.709;
            default: return 0.7213 / (1 + 1.079 / m);
        }
    }
    
    public void add(String element) {
        int hash = element.hashCode();
        int j = hash >>> (32 - b); // First b bits
        int w = hash << b >>> b; // Remaining bits
        int rho = Integer.numberOfLeadingZeros(w) + 1;
        
        registers[j] = Math.max(registers[j], rho);
    }
    
    public long estimateCardinality() {
        double sum = 0;
        int zeroRegisters = 0;
        
        for (int i = 0; i < m; i++) {
            if (registers[i] == 0) {
                zeroRegisters++;
            }
            sum += Math.pow(2, -registers[i]);
        }
        
        double estimate = alpha * m * m / sum;
        
        // Small range correction
        if (estimate <= 2.5 * m && zeroRegisters > 0) {
            estimate = m * Math.log((double) m / zeroRegisters);
        }
        
        return Math.round(estimate);
    }
}
```

### MinHash for Similarity Estimation

```java
import java.util.*;

public class MinHash {
    private int numHashFunctions;
    private Random random;
    
    public MinHash(int numHashFunctions) {
        this.numHashFunctions = numHashFunctions;
        this.random = new Random();
    }
    
    public int[] getMinHashes(Set<String> set) {
        int[] minHashes = new int[numHashFunctions];
        Arrays.fill(minHashes, Integer.MAX_VALUE);
        
        for (String element : set) {
            for (int i = 0; i < numHashFunctions; i++) {
                int hash = hash(element, i);
                minHashes[i] = Math.min(minHashes[i], hash);
            }
        }
        
        return minHashes;
    }
    
    public double estimateJaccardSimilarity(Set<String> set1, Set<String> set2) {
        int[] minHashes1 = getMinHashes(set1);
        int[] minHashes2 = getMinHashes(set2);
        
        int matches = 0;
        for (int i = 0; i < numHashFunctions; i++) {
            if (minHashes1[i] == minHashes2[i]) {
                matches++;
            }
        }
        
        return (double) matches / numHashFunctions;
    }
    
    private int hash(String element, int seed) {
        random.setSeed(seed);
        return element.hashCode() ^ random.nextInt();
    }
}
```

**Real-world Analogies:**
- **Union-Find:** Like organizing people into groups and quickly checking if two people are in the same group
- **Sparse Tables:** Like having a pre-computed lookup table for quick range queries
- **Heavy-Light Decomposition:** Like breaking a complex tree into simpler chains for easier processing
- **Persistent Data Structures:** Like keeping snapshots of a document at different points in time
- **Skip Lists:** Like having express lanes in a highway system for faster navigation
- **Bloom Filters:** Like a quick "maybe" filter before doing expensive database lookups
- **Count-Min Sketch:** Like keeping rough counts of items without storing each one individually
- **Probabilistic Data Structures:** Like using sampling and estimation instead of exact counting for efficiency

Advanced data structures provide powerful tools for solving complex problems efficiently. They often trade some accuracy or space for significant performance improvements, making them invaluable in large-scale systems and real-time applications.