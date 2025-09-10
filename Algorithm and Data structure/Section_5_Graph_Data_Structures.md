# Section 5 – Graph Data Structures

## 5.1 Graph Representation (Adjacency Matrix, List)

Graphs can be represented using different data structures, each with its own advantages.

### Adjacency Matrix

```java
public class GraphMatrix {
    private int[][] adjMatrix;
    private int vertices;
    
    public GraphMatrix(int vertices) {
        this.vertices = vertices;
        this.adjMatrix = new int[vertices][vertices];
    }
    
    public void addEdge(int source, int destination) {
        adjMatrix[source][destination] = 1;
        // For undirected graph
        adjMatrix[destination][source] = 1;
    }
    
    public void addWeightedEdge(int source, int destination, int weight) {
        adjMatrix[source][destination] = weight;
        // For undirected graph
        adjMatrix[destination][source] = weight;
    }
    
    public boolean hasEdge(int source, int destination) {
        return adjMatrix[source][destination] != 0;
    }
    
    public int getWeight(int source, int destination) {
        return adjMatrix[source][destination];
    }
    
    public void printGraph() {
        for (int i = 0; i < vertices; i++) {
            for (int j = 0; j < vertices; j++) {
                System.out.print(adjMatrix[i][j] + " ");
            }
            System.out.println();
        }
    }
}
```

### Adjacency List

```java
import java.util.*;

public class GraphList {
    private int vertices;
    private List<List<Integer>> adjList;
    
    public GraphList(int vertices) {
        this.vertices = vertices;
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
        // For undirected graph
        adjList.get(destination).add(source);
    }
    
    public void removeEdge(int source, int destination) {
        adjList.get(source).remove(Integer.valueOf(destination));
        adjList.get(destination).remove(Integer.valueOf(source));
    }
    
    public boolean hasEdge(int source, int destination) {
        return adjList.get(source).contains(destination);
    }
    
    public List<Integer> getNeighbors(int vertex) {
        return adjList.get(vertex);
    }
    
    public void printGraph() {
        for (int i = 0; i < vertices; i++) {
            System.out.print("Vertex " + i + ": ");
            for (Integer neighbor : adjList.get(i)) {
                System.out.print(neighbor + " ");
            }
            System.out.println();
        }
    }
}
```

### Weighted Graph Representation

```java
public class WeightedGraph {
    private int vertices;
    private List<List<Edge>> adjList;
    
    private class Edge {
        int destination;
        int weight;
        
        public Edge(int destination, int weight) {
            this.destination = destination;
            this.weight = weight;
        }
    }
    
    public WeightedGraph(int vertices) {
        this.vertices = vertices;
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination, int weight) {
        adjList.get(source).add(new Edge(destination, weight));
        // For undirected graph
        adjList.get(destination).add(new Edge(source, weight));
    }
    
    public List<Edge> getNeighbors(int vertex) {
        return adjList.get(vertex);
    }
}
```

## 5.2 Directed & Undirected Graphs

### Directed Graph

```java
public class DirectedGraph {
    private int vertices;
    private List<List<Integer>> adjList;
    
    public DirectedGraph(int vertices) {
        this.vertices = vertices;
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
        // No reverse edge for directed graph
    }
    
    public boolean isCyclic() {
        boolean[] visited = new boolean[vertices];
        boolean[] recStack = new boolean[vertices];
        
        for (int i = 0; i < vertices; i++) {
            if (!visited[i] && isCyclicUtil(i, visited, recStack)) {
                return true;
            }
        }
        return false;
    }
    
    private boolean isCyclicUtil(int vertex, boolean[] visited, boolean[] recStack) {
        visited[vertex] = true;
        recStack[vertex] = true;
        
        for (Integer neighbor : adjList.get(vertex)) {
            if (!visited[neighbor] && isCyclicUtil(neighbor, visited, recStack)) {
                return true;
            } else if (recStack[neighbor]) {
                return true;
            }
        }
        
        recStack[vertex] = false;
        return false;
    }
}
```

### Undirected Graph

```java
public class UndirectedGraph {
    private int vertices;
    private List<List<Integer>> adjList;
    
    public UndirectedGraph(int vertices) {
        this.vertices = vertices;
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
        adjList.get(destination).add(source);
    }
    
    public boolean isCyclic() {
        boolean[] visited = new boolean[vertices];
        
        for (int i = 0; i < vertices; i++) {
            if (!visited[i] && isCyclicUtil(i, visited, -1)) {
                return true;
            }
        }
        return false;
    }
    
    private boolean isCyclicUtil(int vertex, boolean[] visited, int parent) {
        visited[vertex] = true;
        
        for (Integer neighbor : adjList.get(vertex)) {
            if (!visited[neighbor]) {
                if (isCyclicUtil(neighbor, visited, vertex)) {
                    return true;
                }
            } else if (neighbor != parent) {
                return true;
            }
        }
        return false;
    }
}
```

## 5.3 Weighted & Unweighted Graphs

### Unweighted Graph Operations

```java
public class UnweightedGraph {
    private int vertices;
    private List<List<Integer>> adjList;
    
    public UnweightedGraph(int vertices) {
        this.vertices = vertices;
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
    }
    
    public int shortestPath(int source, int destination) {
        boolean[] visited = new boolean[vertices];
        int[] distance = new int[vertices];
        Queue<Integer> queue = new LinkedList<>();
        
        queue.offer(source);
        visited[source] = true;
        distance[source] = 0;
        
        while (!queue.isEmpty()) {
            int current = queue.poll();
            
            if (current == destination) {
                return distance[current];
            }
            
            for (Integer neighbor : adjList.get(current)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    distance[neighbor] = distance[current] + 1;
                    queue.offer(neighbor);
                }
            }
        }
        
        return -1; // No path found
    }
}
```

### Weighted Graph Operations

```java
public class WeightedGraph {
    private int vertices;
    private List<List<Edge>> adjList;
    
    private class Edge {
        int destination;
        int weight;
        
        public Edge(int destination, int weight) {
            this.destination = destination;
            this.weight = weight;
        }
    }
    
    public WeightedGraph(int vertices) {
        this.vertices = vertices;
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination, int weight) {
        adjList.get(source).add(new Edge(destination, weight));
    }
    
    public int[] dijkstra(int source) {
        int[] distance = new int[vertices];
        boolean[] visited = new boolean[vertices];
        PriorityQueue<Edge> pq = new PriorityQueue<>((a, b) -> a.weight - b.weight);
        
        Arrays.fill(distance, Integer.MAX_VALUE);
        distance[source] = 0;
        pq.offer(new Edge(source, 0));
        
        while (!pq.isEmpty()) {
            Edge current = pq.poll();
            int vertex = current.destination;
            
            if (visited[vertex]) continue;
            visited[vertex] = true;
            
            for (Edge neighbor : adjList.get(vertex)) {
                int newDistance = distance[vertex] + neighbor.weight;
                if (newDistance < distance[neighbor.destination]) {
                    distance[neighbor.destination] = newDistance;
                    pq.offer(new Edge(neighbor.destination, newDistance));
                }
            }
        }
        
        return distance;
    }
}
```

## 5.4 Graph Properties & Characteristics

### Graph Properties

```java
public class GraphProperties {
    private int vertices;
    private List<List<Integer>> adjList;
    
    public GraphProperties(int vertices) {
        this.vertices = vertices;
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
        adjList.get(destination).add(source);
    }
    
    // Check if graph is connected
    public boolean isConnected() {
        boolean[] visited = new boolean[vertices];
        dfs(0, visited);
        
        for (boolean v : visited) {
            if (!v) return false;
        }
        return true;
    }
    
    private void dfs(int vertex, boolean[] visited) {
        visited[vertex] = true;
        for (Integer neighbor : adjList.get(vertex)) {
            if (!visited[neighbor]) {
                dfs(neighbor, visited);
            }
        }
    }
    
    // Get degree of a vertex
    public int getDegree(int vertex) {
        return adjList.get(vertex).size();
    }
    
    // Check if graph is complete
    public boolean isComplete() {
        int expectedEdges = vertices * (vertices - 1) / 2;
        int actualEdges = 0;
        
        for (int i = 0; i < vertices; i++) {
            actualEdges += adjList.get(i).size();
        }
        
        return actualEdges == expectedEdges;
    }
    
    // Check if graph is bipartite
    public boolean isBipartite() {
        int[] color = new int[vertices];
        Arrays.fill(color, -1);
        
        for (int i = 0; i < vertices; i++) {
            if (color[i] == -1) {
                if (!isBipartiteUtil(i, color)) {
                    return false;
                }
            }
        }
        return true;
    }
    
    private boolean isBipartiteUtil(int vertex, int[] color) {
        Queue<Integer> queue = new LinkedList<>();
        queue.offer(vertex);
        color[vertex] = 0;
        
        while (!queue.isEmpty()) {
            int current = queue.poll();
            
            for (Integer neighbor : adjList.get(current)) {
                if (color[neighbor] == -1) {
                    color[neighbor] = 1 - color[current];
                    queue.offer(neighbor);
                } else if (color[neighbor] == color[current]) {
                    return false;
                }
            }
        }
        return true;
    }
}
```

## 5.5 Special Graph Types (DAG, Bipartite, etc.)

### Directed Acyclic Graph (DAG)

```java
public class DAG {
    private int vertices;
    private List<List<Integer>> adjList;
    
    public DAG(int vertices) {
        this.vertices = vertices;
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
    }
    
    // Topological sort using DFS
    public List<Integer> topologicalSort() {
        boolean[] visited = new boolean[vertices];
        Stack<Integer> stack = new Stack<>();
        
        for (int i = 0; i < vertices; i++) {
            if (!visited[i]) {
                topologicalSortUtil(i, visited, stack);
            }
        }
        
        List<Integer> result = new ArrayList<>();
        while (!stack.isEmpty()) {
            result.add(stack.pop());
        }
        return result;
    }
    
    private void topologicalSortUtil(int vertex, boolean[] visited, Stack<Integer> stack) {
        visited[vertex] = true;
        
        for (Integer neighbor : adjList.get(vertex)) {
            if (!visited[neighbor]) {
                topologicalSortUtil(neighbor, visited, stack);
            }
        }
        
        stack.push(vertex);
    }
    
    // Check if graph is DAG
    public boolean isDAG() {
        boolean[] visited = new boolean[vertices];
        boolean[] recStack = new boolean[vertices];
        
        for (int i = 0; i < vertices; i++) {
            if (!visited[i] && hasCycle(i, visited, recStack)) {
                return false;
            }
        }
        return true;
    }
    
    private boolean hasCycle(int vertex, boolean[] visited, boolean[] recStack) {
        visited[vertex] = true;
        recStack[vertex] = true;
        
        for (Integer neighbor : adjList.get(vertex)) {
            if (!visited[neighbor] && hasCycle(neighbor, visited, recStack)) {
                return true;
            } else if (recStack[neighbor]) {
                return true;
            }
        }
        
        recStack[vertex] = false;
        return false;
    }
}
```

### Bipartite Graph

```java
public class BipartiteGraph {
    private int vertices;
    private List<List<Integer>> adjList;
    
    public BipartiteGraph(int vertices) {
        this.vertices = vertices;
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
        adjList.get(destination).add(source);
    }
    
    public boolean isBipartite() {
        int[] color = new int[vertices];
        Arrays.fill(color, -1);
        
        for (int i = 0; i < vertices; i++) {
            if (color[i] == -1) {
                if (!isBipartiteUtil(i, color)) {
                    return false;
                }
            }
        }
        return true;
    }
    
    private boolean isBipartiteUtil(int vertex, int[] color) {
        Queue<Integer> queue = new LinkedList<>();
        queue.offer(vertex);
        color[vertex] = 0;
        
        while (!queue.isEmpty()) {
            int current = queue.poll();
            
            for (Integer neighbor : adjList.get(current)) {
                if (color[neighbor] == -1) {
                    color[neighbor] = 1 - color[current];
                    queue.offer(neighbor);
                } else if (color[neighbor] == color[current]) {
                    return false;
                }
            }
        }
        return true;
    }
    
    // Get bipartition
    public List<List<Integer>> getBipartition() {
        int[] color = new int[vertices];
        Arrays.fill(color, -1);
        
        for (int i = 0; i < vertices; i++) {
            if (color[i] == -1) {
                if (!isBipartiteUtil(i, color)) {
                    return null; // Not bipartite
                }
            }
        }
        
        List<Integer> setA = new ArrayList<>();
        List<Integer> setB = new ArrayList<>();
        
        for (int i = 0; i < vertices; i++) {
            if (color[i] == 0) {
                setA.add(i);
            } else {
                setB.add(i);
            }
        }
        
        List<List<Integer>> result = new ArrayList<>();
        result.add(setA);
        result.add(setB);
        return result;
    }
}
```

## 5.6 Graph Storage & Memory Optimization

### Memory-Efficient Graph Representation

```java
public class CompactGraph {
    private int[] edges;
    private int[] offsets;
    private int vertexCount;
    private int edgeCount;
    
    public CompactGraph(int vertexCount, int edgeCount) {
        this.vertexCount = vertexCount;
        this.edgeCount = edgeCount;
        this.edges = new int[edgeCount * 2]; // For undirected graph
        this.offsets = new int[vertexCount + 1];
    }
    
    public void addEdge(int source, int destination) {
        edges[offsets[source]++] = destination;
        edges[offsets[destination]++] = source;
    }
    
    public List<Integer> getNeighbors(int vertex) {
        List<Integer> neighbors = new ArrayList<>();
        int start = offsets[vertex];
        int end = offsets[vertex + 1];
        
        for (int i = start; i < end; i++) {
            neighbors.add(edges[i]);
        }
        
        return neighbors;
    }
    
    // Memory usage in bytes
    public long getMemoryUsage() {
        return (edges.length * 4L) + (offsets.length * 4L);
    }
}
```

### Graph Compression

```java
public class GraphCompression {
    private int[] compressedEdges;
    private int[] vertexOffsets;
    private int vertexCount;
    
    public GraphCompression(List<List<Integer>> adjList) {
        this.vertexCount = adjList.size();
        this.vertexOffsets = new int[vertexCount + 1];
        
        // Calculate total edges
        int totalEdges = 0;
        for (List<Integer> neighbors : adjList) {
            totalEdges += neighbors.size();
        }
        
        this.compressedEdges = new int[totalEdges];
        
        // Build compressed representation
        int edgeIndex = 0;
        for (int i = 0; i < vertexCount; i++) {
            vertexOffsets[i] = edgeIndex;
            for (Integer neighbor : adjList.get(i)) {
                compressedEdges[edgeIndex++] = neighbor;
            }
        }
        vertexOffsets[vertexCount] = edgeIndex;
    }
    
    public List<Integer> getNeighbors(int vertex) {
        List<Integer> neighbors = new ArrayList<>();
        int start = vertexOffsets[vertex];
        int end = vertexOffsets[vertex + 1];
        
        for (int i = start; i < end; i++) {
            neighbors.add(compressedEdges[i]);
        }
        
        return neighbors;
    }
    
    // Compression ratio
    public double getCompressionRatio() {
        int originalSize = vertexCount * vertexCount * 4; // Adjacency matrix
        int compressedSize = compressedEdges.length * 4 + vertexOffsets.length * 4;
        return (double) compressedSize / originalSize;
    }
}
```

**Real-world Analogies:**
- **Adjacency Matrix:** Like a city map where each intersection shows which roads connect to it
- **Adjacency List:** Like a phone book where each person lists their direct contacts
- **Directed Graph:** Like a one-way street system where you can only go in one direction
- **Weighted Graph:** Like a road map with distances marked on each road
- **DAG:** Like a project dependency chart where tasks must be completed in order
- **Bipartite Graph:** Like a dating app where users are divided into two groups and can only match with the other group

Graph data structures are fundamental for modeling relationships and solving complex problems in computer science, from social networks to transportation systems.