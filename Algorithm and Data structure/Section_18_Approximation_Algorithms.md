# Section 18 – Approximation Algorithms

## 18.1 Approximation Algorithm Concepts

Approximation algorithms provide near-optimal solutions to NP-hard problems in polynomial time. They trade optimality for efficiency, offering solutions that are guaranteed to be within a certain factor of the optimal solution.

### Key Concepts

**Approximation Ratio:** The ratio between the cost of the approximate solution and the optimal solution
**PTAS (Polynomial Time Approximation Scheme):** Algorithms that can achieve any desired approximation ratio
**FPTAS (Fully Polynomial Time Approximation Scheme):** PTAS with running time polynomial in both input size and 1/ε
**Greedy Approximation:** Using greedy strategies to build approximate solutions

**Real-world Analogy:**
Think of approximation algorithms like using a GPS that gives you a "good enough" route instead of the absolute shortest path. It might not be perfect, but it gets you there quickly and the route is usually close to optimal. Sometimes the perfect solution takes too long to find, so we settle for something that's 90% as good but can be found in seconds.

### Basic Approximation Framework

```java
public abstract class ApproximationAlgorithm {
    protected String problemName;
    protected double approximationRatio;
    
    public ApproximationAlgorithm(String problemName, double approximationRatio) {
        this.problemName = problemName;
        this.approximationRatio = approximationRatio;
    }
    
    // Abstract method to solve the problem
    public abstract Object solve(Object input);
    
    // Verify if solution is valid
    public abstract boolean isValid(Object input, Object solution);
    
    // Calculate cost of solution
    public abstract double calculateCost(Object solution);
    
    // Get approximation ratio
    public double getApproximationRatio() {
        return approximationRatio;
    }
    
    // Analyze performance
    public void analyzePerformance(Object input, Object solution) {
        double cost = calculateCost(solution);
        System.out.println("Problem: " + problemName);
        System.out.println("Solution cost: " + cost);
        System.out.println("Approximation ratio: " + approximationRatio);
        System.out.println("Valid solution: " + isValid(input, solution));
    }
}
```

## 18.2 Traveling Salesman Problem (TSP)

The TSP is one of the most famous NP-hard problems. We'll implement several approximation algorithms.

### Nearest Neighbor Heuristic

```java
public class TSPNearestNeighbor extends ApproximationAlgorithm {
    public TSPNearestNeighbor() {
        super("Traveling Salesman Problem", 2.0); // 2-approximation
    }
    
    @Override
    public Object solve(Object input) {
        if (!(input instanceof double[][])) {
            throw new IllegalArgumentException("Input must be a distance matrix");
        }
        
        double[][] distances = (double[][]) input;
        int n = distances.length;
        
        if (n <= 1) return new int[0];
        
        boolean[] visited = new boolean[n];
        int[] tour = new int[n];
        tour[0] = 0;
        visited[0] = true;
        
        for (int i = 1; i < n; i++) {
            int last = tour[i - 1];
            int nearest = -1;
            double minDistance = Double.MAX_VALUE;
            
            for (int j = 0; j < n; j++) {
                if (!visited[j] && distances[last][j] < minDistance) {
                    minDistance = distances[last][j];
                    nearest = j;
                }
            }
            
            tour[i] = nearest;
            visited[nearest] = true;
        }
        
        return tour;
    }
    
    @Override
    public boolean isValid(Object input, Object solution) {
        if (!(solution instanceof int[])) return false;
        
        int[] tour = (int[]) solution;
        int n = tour.length;
        boolean[] visited = new boolean[n];
        
        for (int city : tour) {
            if (city < 0 || city >= n || visited[city]) return false;
            visited[city] = true;
        }
        
        return true;
    }
    
    @Override
    public double calculateCost(Object solution) {
        if (!(solution instanceof int[])) return Double.MAX_VALUE;
        
        int[] tour = (int[]) solution;
        double[][] distances = new double[tour.length][tour.length]; // Assume input available
        
        double cost = 0;
        for (int i = 0; i < tour.length; i++) {
            int from = tour[i];
            int to = tour[(i + 1) % tour.length];
            cost += distances[from][to];
        }
        
        return cost;
    }
}
```

### Minimum Spanning Tree Approximation

```java
public class TSPMSTApproximation extends ApproximationAlgorithm {
    public TSPMSTApproximation() {
        super("TSP MST Approximation", 2.0); // 2-approximation
    }
    
    @Override
    public Object solve(Object input) {
        if (!(input instanceof double[][])) {
            throw new IllegalArgumentException("Input must be a distance matrix");
        }
        
        double[][] distances = (double[][]) input;
        int n = distances.length;
        
        if (n <= 1) return new int[0];
        
        // Find MST using Prim's algorithm
        List<Edge> mst = findMST(distances);
        
        // Create adjacency list from MST
        List<List<Integer>> graph = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            graph.add(new ArrayList<>());
        }
        
        for (Edge edge : mst) {
            graph.get(edge.from).add(edge.to);
            graph.get(edge.to).add(edge.from);
        }
        
        // Perform DFS to get Eulerian tour
        List<Integer> eulerTour = new ArrayList<>();
        boolean[] visited = new boolean[n];
        dfs(0, graph, visited, eulerTour);
        
        // Convert Eulerian tour to TSP tour (remove duplicates)
        List<Integer> tspTour = new ArrayList<>();
        boolean[] inTour = new boolean[n];
        
        for (int city : eulerTour) {
            if (!inTour[city]) {
                tspTour.add(city);
                inTour[city] = true;
            }
        }
        
        return tspTour.stream().mapToInt(i -> i).toArray();
    }
    
    private List<Edge> findMST(double[][] distances) {
        int n = distances.length;
        List<Edge> edges = new ArrayList<>();
        
        // Create all edges
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                edges.add(new Edge(i, j, distances[i][j]));
            }
        }
        
        // Sort edges by weight
        edges.sort(Comparator.comparingDouble(e -> e.weight));
        
        // Kruskal's algorithm
        UnionFind uf = new UnionFind(n);
        List<Edge> mst = new ArrayList<>();
        
        for (Edge edge : edges) {
            if (uf.find(edge.from) != uf.find(edge.to)) {
                mst.add(edge);
                uf.union(edge.from, edge.to);
                
                if (mst.size() == n - 1) break;
            }
        }
        
        return mst;
    }
    
    private void dfs(int node, List<List<Integer>> graph, boolean[] visited, List<Integer> tour) {
        visited[node] = true;
        tour.add(node);
        
        for (int neighbor : graph.get(node)) {
            if (!visited[neighbor]) {
                dfs(neighbor, graph, visited, tour);
                tour.add(node); // Return to parent
            }
        }
    }
    
    private static class Edge {
        int from, to;
        double weight;
        
        public Edge(int from, int to, double weight) {
            this.from = from;
            this.to = to;
            this.weight = weight;
        }
    }
    
    private static class UnionFind {
        private int[] parent;
        
        public UnionFind(int n) {
            parent = new int[n];
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
            parent[find(x)] = find(y);
        }
    }
    
    @Override
    public boolean isValid(Object input, Object solution) {
        if (!(solution instanceof int[])) return false;
        
        int[] tour = (int[]) solution;
        int n = tour.length;
        boolean[] visited = new boolean[n];
        
        for (int city : tour) {
            if (city < 0 || city >= n || visited[city]) return false;
            visited[city] = true;
        }
        
        return true;
    }
    
    @Override
    public double calculateCost(Object solution) {
        // Implementation similar to TSPNearestNeighbor
        return 0; // Placeholder
    }
}
```

## 18.3 Set Cover Problem

The Set Cover problem is another classic NP-hard problem with important applications.

### Greedy Set Cover

```java
public class GreedySetCover extends ApproximationAlgorithm {
    public GreedySetCover() {
        super("Set Cover Problem", Math.log(4)); // O(log n) approximation
    }
    
    @Override
    public Object solve(Object input) {
        if (!(input instanceof SetCoverInput)) {
            throw new IllegalArgumentException("Input must be SetCoverInput");
        }
        
        SetCoverInput inputData = (SetCoverInput) input;
        Set<Integer> universe = inputData.universe;
        List<Set<Integer>> sets = inputData.sets;
        
        Set<Integer> uncovered = new HashSet<>(universe);
        List<Integer> selectedSets = new ArrayList<>();
        
        while (!uncovered.isEmpty()) {
            int bestSet = -1;
            double bestRatio = Double.MAX_VALUE;
            
            for (int i = 0; i < sets.size(); i++) {
                if (selectedSets.contains(i)) continue;
                
                Set<Integer> set = sets.get(i);
                Set<Integer> intersection = new HashSet<>(set);
                intersection.retainAll(uncovered);
                
                if (!intersection.isEmpty()) {
                    double ratio = (double) set.size() / intersection.size();
                    if (ratio < bestRatio) {
                        bestRatio = ratio;
                        bestSet = i;
                    }
                }
            }
            
            if (bestSet == -1) break;
            
            selectedSets.add(bestSet);
            uncovered.removeAll(sets.get(bestSet));
        }
        
        return selectedSets;
    }
    
    @Override
    public boolean isValid(Object input, Object solution) {
        if (!(input instanceof SetCoverInput) || !(solution instanceof List)) {
            return false;
        }
        
        SetCoverInput inputData = (SetCoverInput) input;
        List<Integer> selectedSets = (List<Integer>) solution;
        
        Set<Integer> covered = new HashSet<>();
        for (int setIndex : selectedSets) {
            if (setIndex < 0 || setIndex >= inputData.sets.size()) {
                return false;
            }
            covered.addAll(inputData.sets.get(setIndex));
        }
        
        return covered.containsAll(inputData.universe);
    }
    
    @Override
    public double calculateCost(Object solution) {
        if (!(solution instanceof List)) return Double.MAX_VALUE;
        
        List<Integer> selectedSets = (List<Integer>) solution;
        return selectedSets.size();
    }
    
    public static class SetCoverInput {
        Set<Integer> universe;
        List<Set<Integer>> sets;
        
        public SetCoverInput(Set<Integer> universe, List<Set<Integer>> sets) {
            this.universe = universe;
            this.sets = sets;
        }
    }
}
```

## 18.4 Vertex Cover Problem

The Vertex Cover problem asks for the minimum set of vertices that covers all edges.

### Greedy Vertex Cover

```java
public class GreedyVertexCover extends ApproximationAlgorithm {
    public GreedyVertexCover() {
        super("Vertex Cover Problem", 2.0); // 2-approximation
    }
    
    @Override
    public Object solve(Object input) {
        if (!(input instanceof List)) {
            throw new IllegalArgumentException("Input must be a list of edges");
        }
        
        List<Edge> edges = (List<Edge>) input;
        Set<Integer> vertexCover = new HashSet<>();
        List<Edge> remainingEdges = new ArrayList<>(edges);
        
        while (!remainingEdges.isEmpty()) {
            // Pick an arbitrary edge
            Edge edge = remainingEdges.get(0);
            
            // Add both endpoints to cover
            vertexCover.add(edge.from);
            vertexCover.add(edge.to);
            
            // Remove all edges incident to these vertices
            remainingEdges.removeIf(e -> 
                e.from == edge.from || e.from == edge.to ||
                e.to == edge.from || e.to == edge.to);
        }
        
        return new ArrayList<>(vertexCover);
    }
    
    // Improved greedy: pick vertex with highest degree
    public Object solveImproved(Object input) {
        if (!(input instanceof List)) {
            throw new IllegalArgumentException("Input must be a list of edges");
        }
        
        List<Edge> edges = (List<Edge>) input;
        Map<Integer, Integer> degree = new HashMap<>();
        Map<Integer, Set<Edge>> incidentEdges = new HashMap<>();
        
        // Calculate degrees and incident edges
        for (Edge edge : edges) {
            degree.put(edge.from, degree.getOrDefault(edge.from, 0) + 1);
            degree.put(edge.to, degree.getOrDefault(edge.to, 0) + 1);
            
            incidentEdges.computeIfAbsent(edge.from, k -> new HashSet<>()).add(edge);
            incidentEdges.computeIfAbsent(edge.to, k -> new HashSet<>()).add(edge);
        }
        
        Set<Integer> vertexCover = new HashSet<>();
        Set<Edge> remainingEdges = new HashSet<>(edges);
        
        while (!remainingEdges.isEmpty()) {
            // Find vertex with maximum degree among remaining edges
            int maxDegree = 0;
            int selectedVertex = -1;
            
            for (Map.Entry<Integer, Integer> entry : degree.entrySet()) {
                if (entry.getValue() > maxDegree) {
                    maxDegree = entry.getValue();
                    selectedVertex = entry.getKey();
                }
            }
            
            if (selectedVertex == -1) break;
            
            vertexCover.add(selectedVertex);
            
            // Remove all edges incident to selected vertex
            Set<Edge> toRemove = new HashSet<>();
            for (Edge edge : remainingEdges) {
                if (edge.from == selectedVertex || edge.to == selectedVertex) {
                    toRemove.add(edge);
                    degree.put(edge.from, degree.get(edge.from) - 1);
                    degree.put(edge.to, degree.get(edge.to) - 1);
                }
            }
            
            remainingEdges.removeAll(toRemove);
        }
        
        return new ArrayList<>(vertexCover);
    }
    
    @Override
    public boolean isValid(Object input, Object solution) {
        if (!(input instanceof List) || !(solution instanceof List)) {
            return false;
        }
        
        List<Edge> edges = (List<Edge>) input;
        List<Integer> vertexCover = (List<Integer>) solution;
        
        for (Edge edge : edges) {
            if (!vertexCover.contains(edge.from) && !vertexCover.contains(edge.to)) {
                return false;
            }
        }
        
        return true;
    }
    
    @Override
    public double calculateCost(Object solution) {
        if (!(solution instanceof List)) return Double.MAX_VALUE;
        
        List<Integer> vertexCover = (List<Integer>) solution;
        return vertexCover.size();
    }
    
    public static class Edge {
        int from, to;
        
        public Edge(int from, int to) {
            this.from = from;
            this.to = to;
        }
    }
}
```

## 18.5 Bin Packing

The Bin Packing problem asks for the minimum number of bins needed to pack items of given sizes.

### First Fit Decreasing

```java
public class FirstFitDecreasing extends ApproximationAlgorithm {
    public FirstFitDecreasing() {
        super("Bin Packing Problem", 11.0/9.0); // 11/9-approximation
    }
    
    @Override
    public Object solve(Object input) {
        if (!(input instanceof BinPackingInput)) {
            throw new IllegalArgumentException("Input must be BinPackingInput");
        }
        
        BinPackingInput inputData = (BinPackingInput) input;
        List<Double> items = new ArrayList<>(inputData.items);
        double binCapacity = inputData.binCapacity;
        
        // Sort items in decreasing order
        items.sort(Collections.reverseOrder());
        
        List<Bin> bins = new ArrayList<>();
        
        for (double item : items) {
            boolean placed = false;
            
            // Try to place in existing bins
            for (Bin bin : bins) {
                if (bin.canFit(item)) {
                    bin.addItem(item);
                    placed = true;
                    break;
                }
            }
            
            // If couldn't place, create new bin
            if (!placed) {
                Bin newBin = new Bin(binCapacity);
                newBin.addItem(item);
                bins.add(newBin);
            }
        }
        
        return bins;
    }
    
    // Best Fit Decreasing
    public Object solveBestFit(Object input) {
        if (!(input instanceof BinPackingInput)) {
            throw new IllegalArgumentException("Input must be BinPackingInput");
        }
        
        BinPackingInput inputData = (BinPackingInput) input;
        List<Double> items = new ArrayList<>(inputData.items);
        double binCapacity = inputData.binCapacity;
        
        // Sort items in decreasing order
        items.sort(Collections.reverseOrder());
        
        List<Bin> bins = new ArrayList<>();
        
        for (double item : items) {
            Bin bestBin = null;
            double bestFit = Double.MAX_VALUE;
            
            // Find bin with smallest remaining capacity that can fit the item
            for (Bin bin : bins) {
                if (bin.canFit(item)) {
                    double remaining = bin.getRemainingCapacity();
                    if (remaining < bestFit) {
                        bestFit = remaining;
                        bestBin = bin;
                    }
                }
            }
            
            if (bestBin != null) {
                bestBin.addItem(item);
            } else {
                Bin newBin = new Bin(binCapacity);
                newBin.addItem(item);
                bins.add(newBin);
            }
        }
        
        return bins;
    }
    
    @Override
    public boolean isValid(Object input, Object solution) {
        if (!(input instanceof BinPackingInput) || !(solution instanceof List)) {
            return false;
        }
        
        BinPackingInput inputData = (BinPackingInput) input;
        List<Bin> bins = (List<Bin>) solution;
        
        // Check that all items are placed
        Set<Double> placedItems = new HashSet<>();
        for (Bin bin : bins) {
            placedItems.addAll(bin.getItems());
        }
        
        if (!placedItems.containsAll(inputData.items)) {
            return false;
        }
        
        // Check that no bin exceeds capacity
        for (Bin bin : bins) {
            if (bin.getTotalWeight() > inputData.binCapacity + 1e-9) {
                return false;
            }
        }
        
        return true;
    }
    
    @Override
    public double calculateCost(Object solution) {
        if (!(solution instanceof List)) return Double.MAX_VALUE;
        
        List<Bin> bins = (List<Bin>) solution;
        return bins.size();
    }
    
    public static class BinPackingInput {
        List<Double> items;
        double binCapacity;
        
        public BinPackingInput(List<Double> items, double binCapacity) {
            this.items = items;
            this.binCapacity = binCapacity;
        }
    }
    
    public static class Bin {
        private double capacity;
        private List<Double> items;
        
        public Bin(double capacity) {
            this.capacity = capacity;
            this.items = new ArrayList<>();
        }
        
        public boolean canFit(double item) {
            return getTotalWeight() + item <= capacity;
        }
        
        public void addItem(double item) {
            if (canFit(item)) {
                items.add(item);
            } else {
                throw new IllegalArgumentException("Item too large for bin");
            }
        }
        
        public double getTotalWeight() {
            return items.stream().mapToDouble(Double::doubleValue).sum();
        }
        
        public double getRemainingCapacity() {
            return capacity - getTotalWeight();
        }
        
        public List<Double> getItems() {
            return new ArrayList<>(items);
        }
    }
}
```

## 18.6 Load Balancing

The Load Balancing problem distributes jobs across machines to minimize maximum load.

### Greedy Load Balancing

```java
public class GreedyLoadBalancing extends ApproximationAlgorithm {
    public GreedyLoadBalancing() {
        super("Load Balancing Problem", 2.0); // 2-approximation
    }
    
    @Override
    public Object solve(Object input) {
        if (!(input instanceof LoadBalancingInput)) {
            throw new IllegalArgumentException("Input must be LoadBalancingInput");
        }
        
        LoadBalancingInput inputData = (LoadBalancingInput) input;
        List<Double> jobs = inputData.jobs;
        int numMachines = inputData.numMachines;
        
        double[] machineLoads = new double[numMachines];
        List<List<Integer>> assignments = new ArrayList<>();
        
        for (int i = 0; i < numMachines; i++) {
            assignments.add(new ArrayList<>());
        }
        
        // Assign each job to the machine with minimum current load
        for (int i = 0; i < jobs.size(); i++) {
            double jobWeight = jobs.get(i);
            int minLoadMachine = 0;
            
            for (int j = 1; j < numMachines; j++) {
                if (machineLoads[j] < machineLoads[minLoadMachine]) {
                    minLoadMachine = j;
                }
            }
            
            machineLoads[minLoadMachine] += jobWeight;
            assignments.get(minLoadMachine).add(i);
        }
        
        return new LoadBalancingSolution(assignments, machineLoads);
    }
    
    // LPT (Longest Processing Time) algorithm
    public Object solveLPT(Object input) {
        if (!(input instanceof LoadBalancingInput)) {
            throw new IllegalArgumentException("Input must be LoadBalancingInput");
        }
        
        LoadBalancingInput inputData = (LoadBalancingInput) input;
        List<Double> jobs = new ArrayList<>(inputData.jobs);
        int numMachines = inputData.numMachines;
        
        // Sort jobs in decreasing order of processing time
        jobs.sort(Collections.reverseOrder());
        
        double[] machineLoads = new double[numMachines];
        List<List<Integer>> assignments = new ArrayList<>();
        
        for (int i = 0; i < numMachines; i++) {
            assignments.add(new ArrayList<>());
        }
        
        // Assign each job to the machine with minimum current load
        for (int i = 0; i < jobs.size(); i++) {
            double jobWeight = jobs.get(i);
            int minLoadMachine = 0;
            
            for (int j = 1; j < numMachines; j++) {
                if (machineLoads[j] < machineLoads[minLoadMachine]) {
                    minLoadMachine = j;
                }
            }
            
            machineLoads[minLoadMachine] += jobWeight;
            assignments.get(minLoadMachine).add(i);
        }
        
        return new LoadBalancingSolution(assignments, machineLoads);
    }
    
    @Override
    public boolean isValid(Object input, Object solution) {
        if (!(input instanceof LoadBalancingInput) || !(solution instanceof LoadBalancingSolution)) {
            return false;
        }
        
        LoadBalancingInput inputData = (LoadBalancingInput) input;
        LoadBalancingSolution sol = (LoadBalancingSolution) solution;
        
        // Check that all jobs are assigned
        Set<Integer> assignedJobs = new HashSet<>();
        for (List<Integer> machineJobs : sol.assignments) {
            assignedJobs.addAll(machineJobs);
        }
        
        if (assignedJobs.size() != inputData.jobs.size()) {
            return false;
        }
        
        // Check that no job is assigned to multiple machines
        for (int i = 0; i < inputData.jobs.size(); i++) {
            int count = 0;
            for (List<Integer> machineJobs : sol.assignments) {
                if (machineJobs.contains(i)) count++;
            }
            if (count != 1) return false;
        }
        
        return true;
    }
    
    @Override
    public double calculateCost(Object solution) {
        if (!(solution instanceof LoadBalancingSolution)) return Double.MAX_VALUE;
        
        LoadBalancingSolution sol = (LoadBalancingSolution) solution;
        return Arrays.stream(sol.machineLoads).max().orElse(0.0);
    }
    
    public static class LoadBalancingInput {
        List<Double> jobs;
        int numMachines;
        
        public LoadBalancingInput(List<Double> jobs, int numMachines) {
            this.jobs = jobs;
            this.numMachines = numMachines;
        }
    }
    
    public static class LoadBalancingSolution {
        List<List<Integer>> assignments;
        double[] machineLoads;
        
        public LoadBalancingSolution(List<List<Integer>> assignments, double[] machineLoads) {
            this.assignments = assignments;
            this.machineLoads = machineLoads;
        }
    }
}
```

## 18.7 Approximation Ratios & Analysis

### Analyzing Approximation Quality

```java
public class ApproximationAnalysis {
    // Calculate approximation ratio
    public static double calculateApproximationRatio(double approximateCost, double optimalCost) {
        if (optimalCost == 0) return Double.POSITIVE_INFINITY;
        return approximateCost / optimalCost;
    }
    
    // Analyze performance over multiple instances
    public static void analyzePerformance(List<ApproximationAlgorithm> algorithms, 
                                        List<Object> testInstances) {
        for (ApproximationAlgorithm algorithm : algorithms) {
            System.out.println("Algorithm: " + algorithm.getClass().getSimpleName());
            
            double totalCost = 0;
            double maxRatio = 0;
            double minRatio = Double.MAX_VALUE;
            
            for (Object instance : testInstances) {
                Object solution = algorithm.solve(instance);
                double cost = algorithm.calculateCost(solution);
                totalCost += cost;
                
                // Assuming we have optimal costs (in practice, this would be calculated)
                double optimalCost = cost * 0.8; // Placeholder
                double ratio = calculateApproximationRatio(cost, optimalCost);
                
                maxRatio = Math.max(maxRatio, ratio);
                minRatio = Math.min(minRatio, ratio);
            }
            
            double avgCost = totalCost / testInstances.size();
            System.out.println("Average cost: " + avgCost);
            System.out.println("Max approximation ratio: " + maxRatio);
            System.out.println("Min approximation ratio: " + minRatio);
            System.out.println();
        }
    }
    
    // Compare algorithms
    public static void compareAlgorithms(List<ApproximationAlgorithm> algorithms, 
                                       Object testInstance) {
        System.out.println("Comparing algorithms on single instance:");
        
        for (ApproximationAlgorithm algorithm : algorithms) {
            long startTime = System.currentTimeMillis();
            Object solution = algorithm.solve(testInstance);
            long endTime = System.currentTimeMillis();
            
            double cost = algorithm.calculateCost(solution);
            boolean valid = algorithm.isValid(testInstance, solution);
            
            System.out.println(algorithm.getClass().getSimpleName() + ":");
            System.out.println("  Cost: " + cost);
            System.out.println("  Valid: " + valid);
            System.out.println("  Time: " + (endTime - startTime) + "ms");
            System.out.println();
        }
    }
}
```

## 18.8 Online Algorithms

Online algorithms make decisions without knowing future input.

### Online Load Balancing

```java
public class OnlineLoadBalancing {
    private double[] machineLoads;
    private List<List<Integer>> assignments;
    
    public OnlineLoadBalancing(int numMachines) {
        this.machineLoads = new double[numMachines];
        this.assignments = new ArrayList<>();
        
        for (int i = 0; i < numMachines; i++) {
            assignments.add(new ArrayList<>());
        }
    }
    
    // Greedy online algorithm
    public void assignJob(double jobWeight) {
        int minLoadMachine = 0;
        
        for (int i = 1; i < machineLoads.length; i++) {
            if (machineLoads[i] < machineLoads[minLoadMachine]) {
                minLoadMachine = i;
            }
        }
        
        machineLoads[minLoadMachine] += jobWeight;
        assignments.get(minLoadMachine).add(assignments.get(minLoadMachine).size());
    }
    
    // Competitive ratio analysis
    public double getCompetitiveRatio() {
        double maxLoad = Arrays.stream(machineLoads).max().orElse(0.0);
        double totalLoad = Arrays.stream(machineLoads).sum();
        double avgLoad = totalLoad / machineLoads.length;
        
        // For greedy algorithm, competitive ratio is 2 - 1/m
        return maxLoad / avgLoad;
    }
    
    public double getMaxLoad() {
        return Arrays.stream(machineLoads).max().orElse(0.0);
    }
    
    public double getTotalLoad() {
        return Arrays.stream(machineLoads).sum();
    }
}
```

### Online Bin Packing

```java
public class OnlineBinPacking {
    private List<Bin> bins;
    private double binCapacity;
    
    public OnlineBinPacking(double binCapacity) {
        this.bins = new ArrayList<>();
        this.binCapacity = binCapacity;
    }
    
    // First Fit online algorithm
    public void addItem(double itemSize) {
        boolean placed = false;
        
        for (Bin bin : bins) {
            if (bin.canFit(itemSize)) {
                bin.addItem(itemSize);
                placed = true;
                break;
            }
        }
        
        if (!placed) {
            Bin newBin = new Bin(binCapacity);
            newBin.addItem(itemSize);
            bins.add(newBin);
        }
    }
    
    // Best Fit online algorithm
    public void addItemBestFit(double itemSize) {
        Bin bestBin = null;
        double bestFit = Double.MAX_VALUE;
        
        for (Bin bin : bins) {
            if (bin.canFit(itemSize)) {
                double remaining = bin.getRemainingCapacity();
                if (remaining < bestFit) {
                    bestFit = remaining;
                    bestBin = bin;
                }
            }
        }
        
        if (bestBin != null) {
            bestBin.addItem(itemSize);
        } else {
            Bin newBin = new Bin(binCapacity);
            newBin.addItem(itemSize);
            bins.add(newBin);
        }
    }
    
    public int getNumBins() {
        return bins.size();
    }
    
    public double getWaste() {
        double totalWaste = 0;
        for (Bin bin : bins) {
            totalWaste += bin.getRemainingCapacity();
        }
        return totalWaste;
    }
    
    // Competitive ratio for First Fit is 1.7
    public double getCompetitiveRatio() {
        return 1.7; // Theoretical bound
    }
}
```

**Real-world Analogies:**
- **Approximation Algorithms:** Like using a GPS that gives you a "good enough" route instead of the perfect one
- **TSP Approximation:** Like planning a delivery route that's close to optimal but can be calculated quickly
- **Set Cover:** Like choosing the minimum number of radio stations to cover all cities
- **Vertex Cover:** Like placing security guards at the minimum number of intersections to monitor all roads
- **Bin Packing:** Like efficiently packing items into shipping containers
- **Load Balancing:** Like distributing work among team members to minimize the maximum workload
- **Approximation Ratios:** Like measuring how close your solution is to the perfect answer
- **Online Algorithms:** Like making decisions in real-time without knowing what's coming next

Approximation algorithms are essential for solving NP-hard problems in practice. They provide practical solutions that are guaranteed to be within a certain factor of optimal, making them invaluable for real-world applications where perfect solutions are computationally infeasible.