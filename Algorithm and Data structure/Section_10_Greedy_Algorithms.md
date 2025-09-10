# Section 10 – Greedy Algorithms

## 10.1 Greedy Algorithm Design

Greedy algorithms make locally optimal choices at each step, hoping to find a global optimum.

### Greedy Algorithm Template

```java
public class GreedyAlgorithmTemplate {
    public void greedyAlgorithm(Problem problem) {
        // 1. Sort items by some criteria
        List<Item> items = problem.getItems();
        items.sort(Comparator.comparing(Item::getValue));
        
        // 2. Process items in order
        List<Item> solution = new ArrayList<>();
        for (Item item : items) {
            if (isFeasible(item, solution)) {
                solution.add(item);
            }
        }
        
        // 3. Return solution
        problem.setSolution(solution);
    }
    
    private boolean isFeasible(Item item, List<Item> currentSolution) {
        // Check if adding this item maintains feasibility
        return true; // Implementation depends on problem
    }
}
```

### Greedy Algorithm Properties

```java
public class GreedyProperties {
    // 1. Greedy Choice Property
    // A global optimum can be reached by making locally optimal choices
    public boolean hasGreedyChoiceProperty(Problem problem) {
        // Check if local optimal choice leads to global optimum
        return true; // Implementation depends on problem
    }
    
    // 2. Optimal Substructure
    // The problem can be broken down into subproblems
    public boolean hasOptimalSubstructure(Problem problem) {
        // Check if optimal solution contains optimal solutions to subproblems
        return true; // Implementation depends on problem
    }
    
    // 3. Proof of Correctness
    public boolean proveCorrectness(Problem problem) {
        // Mathematical proof that greedy algorithm produces optimal solution
        return true; // Implementation depends on problem
    }
}
```

## 10.2 Activity Selection Problem

The activity selection problem is a classic greedy algorithm problem.

### Basic Activity Selection

```java
public class ActivitySelection {
    private class Activity {
        int start;
        int end;
        String name;
        
        public Activity(int start, int end, String name) {
            this.start = start;
            this.end = end;
            this.name = name;
        }
    }
    
    public List<Activity> selectActivities(List<Activity> activities) {
        // Sort activities by end time
        activities.sort(Comparator.comparing(a -> a.end));
        
        List<Activity> selected = new ArrayList<>();
        selected.add(activities.get(0));
        
        int lastEndTime = activities.get(0).end;
        
        for (int i = 1; i < activities.size(); i++) {
            Activity current = activities.get(i);
            if (current.start >= lastEndTime) {
                selected.add(current);
                lastEndTime = current.end;
            }
        }
        
        return selected;
    }
    
    // Recursive approach
    public List<Activity> selectActivitiesRecursive(List<Activity> activities) {
        activities.sort(Comparator.comparing(a -> a.end));
        List<Activity> selected = new ArrayList<>();
        selectActivitiesRecursive(activities, 0, selected);
        return selected;
    }
    
    private void selectActivitiesRecursive(List<Activity> activities, int index, List<Activity> selected) {
        if (index >= activities.size()) return;
        
        Activity current = activities.get(index);
        
        if (selected.isEmpty() || current.start >= selected.get(selected.size() - 1).end) {
            selected.add(current);
        }
        
        selectActivitiesRecursive(activities, index + 1, selected);
    }
}
```

### Weighted Activity Selection

```java
public class WeightedActivitySelection {
    private class WeightedActivity {
        int start;
        int end;
        int weight;
        String name;
        
        public WeightedActivity(int start, int end, int weight, String name) {
            this.start = start;
            this.end = end;
            this.weight = weight;
            this.name = name;
        }
    }
    
    public int maxWeight(List<WeightedActivity> activities) {
        // Sort by end time
        activities.sort(Comparator.comparing(a -> a.end));
        
        int n = activities.size();
        int[] dp = new int[n];
        dp[0] = activities.get(0).weight;
        
        for (int i = 1; i < n; i++) {
            int currentWeight = activities.get(i).weight;
            int maxWeight = currentWeight;
            
            // Find last compatible activity
            for (int j = i - 1; j >= 0; j--) {
                if (activities.get(j).end <= activities.get(i).start) {
                    maxWeight = Math.max(maxWeight, dp[j] + currentWeight);
                    break;
                }
            }
            
            dp[i] = Math.max(dp[i - 1], maxWeight);
        }
        
        return dp[n - 1];
    }
}
```

## 10.3 Huffman Coding

Huffman coding is a lossless data compression algorithm.

### Huffman Tree Node

```java
public class HuffmanNode implements Comparable<HuffmanNode> {
    char character;
    int frequency;
    HuffmanNode left;
    HuffmanNode right;
    
    public HuffmanNode(char character, int frequency) {
        this.character = character;
        this.frequency = frequency;
        this.left = null;
        this.right = null;
    }
    
    public HuffmanNode(int frequency, HuffmanNode left, HuffmanNode right) {
        this.character = '\0';
        this.frequency = frequency;
        this.left = left;
        this.right = right;
    }
    
    public boolean isLeaf() {
        return left == null && right == null;
    }
    
    @Override
    public int compareTo(HuffmanNode other) {
        return this.frequency - other.frequency;
    }
}
```

### Huffman Coding Implementation

```java
public class HuffmanCoding {
    public Map<Character, String> buildHuffmanTree(String text) {
        // Count character frequencies
        Map<Character, Integer> frequencies = new HashMap<>();
        for (char c : text.toCharArray()) {
            frequencies.put(c, frequencies.getOrDefault(c, 0) + 1);
        }
        
        // Create priority queue
        PriorityQueue<HuffmanNode> pq = new PriorityQueue<>();
        for (Map.Entry<Character, Integer> entry : frequencies.entrySet()) {
            pq.offer(new HuffmanNode(entry.getKey(), entry.getValue()));
        }
        
        // Build Huffman tree
        while (pq.size() > 1) {
            HuffmanNode left = pq.poll();
            HuffmanNode right = pq.poll();
            
            HuffmanNode merged = new HuffmanNode(
                left.frequency + right.frequency, left, right
            );
            pq.offer(merged);
        }
        
        // Generate codes
        Map<Character, String> codes = new HashMap<>();
        if (pq.size() == 1) {
            generateCodes(pq.poll(), "", codes);
        }
        
        return codes;
    }
    
    private void generateCodes(HuffmanNode root, String code, Map<Character, String> codes) {
        if (root.isLeaf()) {
            codes.put(root.character, code.isEmpty() ? "0" : code);
        } else {
            if (root.left != null) {
                generateCodes(root.left, code + "0", codes);
            }
            if (root.right != null) {
                generateCodes(root.right, code + "1", codes);
            }
        }
    }
    
    public String encode(String text, Map<Character, String> codes) {
        StringBuilder encoded = new StringBuilder();
        for (char c : text.toCharArray()) {
            encoded.append(codes.get(c));
        }
        return encoded.toString();
    }
    
    public String decode(String encoded, HuffmanNode root) {
        StringBuilder decoded = new StringBuilder();
        HuffmanNode current = root;
        
        for (char bit : encoded.toCharArray()) {
            if (bit == '0') {
                current = current.left;
            } else {
                current = current.right;
            }
            
            if (current.isLeaf()) {
                decoded.append(current.character);
                current = root;
            }
        }
        
        return decoded.toString();
    }
}
```

## 10.4 Minimum Spanning Tree (Greedy Approach)

### Kruskal's Algorithm

```java
public class KruskalMST {
    private class Edge implements Comparable<Edge> {
        int source;
        int destination;
        int weight;
        
        public Edge(int source, int destination, int weight) {
            this.source = source;
            this.destination = destination;
            this.weight = weight;
        }
        
        @Override
        public int compareTo(Edge other) {
            return Integer.compare(this.weight, other.weight);
        }
    }
    
    private class UnionFind {
        private int[] parent;
        private int[] rank;
        
        public UnionFind(int n) {
            parent = new int[n];
            rank = new int[n];
            for (int i = 0; i < n; i++) {
                parent[i] = i;
            }
        }
        
        public int find(int x) {
            if (parent[x] != x) {
                parent[x] = find(parent[x]);
            }
            return parent[x];
        }
        
        public void union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);
            
            if (rootX != rootY) {
                if (rank[rootX] < rank[rootY]) {
                    parent[rootX] = rootY;
                } else if (rank[rootX] > rank[rootY]) {
                    parent[rootY] = rootX;
                } else {
                    parent[rootY] = rootX;
                    rank[rootX]++;
                }
            }
        }
    }
    
    public List<Edge> findMST(List<Edge> edges, int vertices) {
        // Sort edges by weight
        edges.sort(Edge::compareTo);
        
        UnionFind uf = new UnionFind(vertices);
        List<Edge> mst = new ArrayList<>();
        
        for (Edge edge : edges) {
            if (uf.find(edge.source) != uf.find(edge.destination)) {
                mst.add(edge);
                uf.union(edge.source, edge.destination);
                
                if (mst.size() == vertices - 1) {
                    break;
                }
            }
        }
        
        return mst;
    }
}
```

### Prim's Algorithm

```java
public class PrimMST {
    private class Edge {
        int destination;
        int weight;
        
        public Edge(int destination, int weight) {
            this.destination = destination;
            this.weight = weight;
        }
    }
    
    public List<Edge> findMST(List<List<Edge>> graph, int startVertex) {
        int vertices = graph.size();
        boolean[] inMST = new boolean[vertices];
        int[] key = new int[vertices];
        int[] parent = new int[vertices];
        
        Arrays.fill(key, Integer.MAX_VALUE);
        key[startVertex] = 0;
        parent[startVertex] = -1;
        
        PriorityQueue<Edge> pq = new PriorityQueue<>((a, b) -> a.weight - b.weight);
        pq.offer(new Edge(startVertex, 0));
        
        List<Edge> mst = new ArrayList<>();
        
        while (!pq.isEmpty()) {
            Edge current = pq.poll();
            int vertex = current.destination;
            
            if (inMST[vertex]) continue;
            inMST[vertex] = true;
            
            if (parent[vertex] != -1) {
                mst.add(new Edge(vertex, key[vertex]));
            }
            
            for (Edge neighbor : graph.get(vertex)) {
                if (!inMST[neighbor.destination] && neighbor.weight < key[neighbor.destination]) {
                    key[neighbor.destination] = neighbor.weight;
                    parent[neighbor.destination] = vertex;
                    pq.offer(new Edge(neighbor.destination, neighbor.weight));
                }
            }
        }
        
        return mst;
    }
}
```

## 10.5 Job Scheduling Problems

### Interval Scheduling

```java
public class IntervalScheduling {
    private class Job {
        int start;
        int end;
        int profit;
        String name;
        
        public Job(int start, int end, int profit, String name) {
            this.start = start;
            this.end = end;
            this.profit = profit;
            this.name = name;
        }
    }
    
    public List<Job> scheduleJobs(List<Job> jobs) {
        // Sort by end time
        jobs.sort(Comparator.comparing(j -> j.end));
        
        List<Job> scheduled = new ArrayList<>();
        scheduled.add(jobs.get(0));
        
        int lastEndTime = jobs.get(0).end;
        
        for (int i = 1; i < jobs.size(); i++) {
            Job current = jobs.get(i);
            if (current.start >= lastEndTime) {
                scheduled.add(current);
                lastEndTime = current.end;
            }
        }
        
        return scheduled;
    }
}
```

### Weighted Job Scheduling

```java
public class WeightedJobScheduling {
    private class Job {
        int start;
        int end;
        int profit;
        
        public Job(int start, int end, int profit) {
            this.start = start;
            this.end = end;
            this.profit = profit;
        }
    }
    
    public int maxProfit(List<Job> jobs) {
        // Sort by end time
        jobs.sort(Comparator.comparing(j -> j.end));
        
        int n = jobs.size();
        int[] dp = new int[n];
        dp[0] = jobs.get(0).profit;
        
        for (int i = 1; i < n; i++) {
            int currentProfit = jobs.get(i).profit;
            int maxProfit = currentProfit;
            
            // Find last compatible job
            for (int j = i - 1; j >= 0; j--) {
                if (jobs.get(j).end <= jobs.get(i).start) {
                    maxProfit = Math.max(maxProfit, dp[j] + currentProfit);
                    break;
                }
            }
            
            dp[i] = Math.max(dp[i - 1], maxProfit);
        }
        
        return dp[n - 1];
    }
}
```

## 10.6 Fractional Knapsack

```java
public class FractionalKnapsack {
    private class Item {
        int weight;
        int value;
        double ratio;
        
        public Item(int weight, int value) {
            this.weight = weight;
            this.value = value;
            this.ratio = (double) value / weight;
        }
    }
    
    public double maxValue(List<Item> items, int capacity) {
        // Sort by value-to-weight ratio in descending order
        items.sort((a, b) -> Double.compare(b.ratio, a.ratio));
        
        double totalValue = 0;
        int remainingCapacity = capacity;
        
        for (Item item : items) {
            if (remainingCapacity >= item.weight) {
                // Take the entire item
                totalValue += item.value;
                remainingCapacity -= item.weight;
            } else {
                // Take a fraction of the item
                totalValue += item.ratio * remainingCapacity;
                break;
            }
        }
        
        return totalValue;
    }
    
    public List<Item> maxValueWithItems(List<Item> items, int capacity) {
        items.sort((a, b) -> Double.compare(b.ratio, a.ratio));
        
        List<Item> selectedItems = new ArrayList<>();
        int remainingCapacity = capacity;
        
        for (Item item : items) {
            if (remainingCapacity >= item.weight) {
                selectedItems.add(item);
                remainingCapacity -= item.weight;
            } else if (remainingCapacity > 0) {
                // Take a fraction of the item
                Item fractionalItem = new Item(remainingCapacity, 
                    (int) (item.ratio * remainingCapacity));
                selectedItems.add(fractionalItem);
                break;
            }
        }
        
        return selectedItems;
    }
}
```

## 10.7 Greedy vs Dynamic Programming

### Comparison Framework

```java
public class GreedyVsDP {
    public void compareApproaches(Problem problem) {
        System.out.println("=== Greedy Approach ===");
        long startTime = System.currentTimeMillis();
        Solution greedySolution = solveGreedy(problem);
        long greedyTime = System.currentTimeMillis() - startTime;
        
        System.out.println("=== Dynamic Programming Approach ===");
        startTime = System.currentTimeMillis();
        Solution dpSolution = solveDP(problem);
        long dpTime = System.currentTimeMillis() - startTime;
        
        System.out.println("Greedy Solution: " + greedySolution.getValue());
        System.out.println("DP Solution: " + dpSolution.getValue());
        System.out.println("Greedy Time: " + greedyTime + "ms");
        System.out.println("DP Time: " + dpTime + "ms");
    }
    
    private Solution solveGreedy(Problem problem) {
        // Greedy algorithm implementation
        return new Solution();
    }
    
    private Solution solveDP(Problem problem) {
        // Dynamic programming implementation
        return new Solution();
    }
}

class Solution {
    private int value;
    
    public int getValue() { return value; }
    public void setValue(int value) { this.value = value; }
}
```

### When to Use Greedy vs DP

```java
public class AlgorithmSelection {
    public AlgorithmType selectAlgorithm(Problem problem) {
        if (hasGreedyChoiceProperty(problem) && hasOptimalSubstructure(problem)) {
            return AlgorithmType.GREEDY;
        } else if (hasOverlappingSubproblems(problem) && hasOptimalSubstructure(problem)) {
            return AlgorithmType.DYNAMIC_PROGRAMMING;
        } else {
            return AlgorithmType.BRUTE_FORCE;
        }
    }
    
    private boolean hasGreedyChoiceProperty(Problem problem) {
        // Check if greedy choice property holds
        return true; // Implementation depends on problem
    }
    
    private boolean hasOptimalSubstructure(Problem problem) {
        // Check if optimal substructure property holds
        return true; // Implementation depends on problem
    }
    
    private boolean hasOverlappingSubproblems(Problem problem) {
        // Check if subproblems overlap
        return true; // Implementation depends on problem
    }
}

enum AlgorithmType {
    GREEDY, DYNAMIC_PROGRAMMING, BRUTE_FORCE
}
```

## 10.8 Proof Techniques for Greedy Algorithms

### Exchange Argument

```java
public class ExchangeArgument {
    public boolean proveGreedyCorrectness(Problem problem) {
        // 1. Assume there's an optimal solution that differs from greedy
        Solution optimal = problem.getOptimalSolution();
        Solution greedy = problem.getGreedySolution();
        
        // 2. Show that we can exchange elements to make optimal more like greedy
        if (canExchange(optimal, greedy)) {
            // 3. This contradicts optimality, so greedy must be optimal
            return true;
        }
        
        return false;
    }
    
    private boolean canExchange(Solution optimal, Solution greedy) {
        // Implementation of exchange argument
        return true; // Implementation depends on problem
    }
}
```

### Stays Ahead Argument

```java
public class StaysAheadArgument {
    public boolean proveGreedyStaysAhead(Problem problem) {
        // 1. Show that greedy solution is always at least as good as any other
        Solution greedy = problem.getGreedySolution();
        
        // 2. Prove that greedy maintains this property at each step
        for (int i = 0; i < greedy.getSteps().size(); i++) {
            if (!greedyStaysAhead(greedy, i)) {
                return false;
            }
        }
        
        return true;
    }
    
    private boolean greedyStaysAhead(Solution greedy, int step) {
        // Check if greedy is ahead at this step
        return true; // Implementation depends on problem
    }
}
```

**Real-world Analogies:**
- **Greedy Algorithms:** Like always choosing the best available option at each step
- **Activity Selection:** Like scheduling meetings to maximize the number of meetings
- **Huffman Coding:** Like creating a custom alphabet where frequent letters have shorter codes
- **Minimum Spanning Tree:** Like connecting all cities with minimum cost roads
- **Job Scheduling:** Like assigning tasks to maximize profit or minimize completion time
- **Fractional Knapsack:** Like packing a suitcase with the most valuable items
- **Greedy vs DP:** Like choosing between a quick decision (greedy) and a thorough analysis (DP)
- **Proof Techniques:** Like proving that your strategy is the best possible

Greedy algorithms are powerful tools for solving optimization problems where local optimal choices lead to global optimal solutions. They are often simpler and more efficient than dynamic programming approaches when applicable.