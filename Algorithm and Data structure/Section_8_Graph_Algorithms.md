# Section 8 – Graph Algorithms

## 8.1 Depth-First Search (DFS)

DFS explores as far as possible along each branch before backtracking.

### Recursive DFS

```java
public class DepthFirstSearch {
    private boolean[] visited;
    private List<List<Integer>> adjList;
    
    public DepthFirstSearch(int vertices) {
        this.visited = new boolean[vertices];
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
        adjList.get(destination).add(source); // For undirected graph
    }
    
    public void dfs(int startVertex) {
        visited[startVertex] = true;
        System.out.print(startVertex + " ");
        
        for (Integer neighbor : adjList.get(startVertex)) {
            if (!visited[neighbor]) {
                dfs(neighbor);
            }
        }
    }
    
    // DFS with path tracking
    public List<Integer> dfsWithPath(int start, int target) {
        List<Integer> path = new ArrayList<>();
        boolean found = dfsWithPathUtil(start, target, path);
        return found ? path : new ArrayList<>();
    }
    
    private boolean dfsWithPathUtil(int current, int target, List<Integer> path) {
        visited[current] = true;
        path.add(current);
        
        if (current == target) {
            return true;
        }
        
        for (Integer neighbor : adjList.get(current)) {
            if (!visited[neighbor]) {
                if (dfsWithPathUtil(neighbor, target, path)) {
                    return true;
                }
            }
        }
        
        path.remove(path.size() - 1);
        return false;
    }
}
```

### Iterative DFS

```java
public class IterativeDFS {
    private boolean[] visited;
    private List<List<Integer>> adjList;
    
    public IterativeDFS(int vertices) {
        this.visited = new boolean[vertices];
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
    }
    
    public void dfs(int startVertex) {
        Stack<Integer> stack = new Stack<>();
        stack.push(startVertex);
        
        while (!stack.isEmpty()) {
            int current = stack.pop();
            
            if (!visited[current]) {
                visited[current] = true;
                System.out.print(current + " ");
                
                // Add neighbors in reverse order to maintain left-to-right traversal
                for (int i = adjList.get(current).size() - 1; i >= 0; i--) {
                    int neighbor = adjList.get(current).get(i);
                    if (!visited[neighbor]) {
                        stack.push(neighbor);
                    }
                }
            }
        }
    }
}
```

## 8.2 Breadth-First Search (BFS)

BFS explores all neighbors at the current depth before moving to the next level.

### Basic BFS

```java
public class BreadthFirstSearch {
    private boolean[] visited;
    private List<List<Integer>> adjList;
    
    public BreadthFirstSearch(int vertices) {
        this.visited = new boolean[vertices];
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
        adjList.get(destination).add(source); // For undirected graph
    }
    
    public void bfs(int startVertex) {
        Queue<Integer> queue = new LinkedList<>();
        visited[startVertex] = true;
        queue.offer(startVertex);
        
        while (!queue.isEmpty()) {
            int current = queue.poll();
            System.out.print(current + " ");
            
            for (Integer neighbor : adjList.get(current)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.offer(neighbor);
                }
            }
        }
    }
    
    // BFS with distance calculation
    public int[] shortestDistances(int startVertex) {
        int[] distances = new int[visited.length];
        Arrays.fill(distances, -1);
        
        Queue<Integer> queue = new LinkedList<>();
        visited[startVertex] = true;
        distances[startVertex] = 0;
        queue.offer(startVertex);
        
        while (!queue.isEmpty()) {
            int current = queue.poll();
            
            for (Integer neighbor : adjList.get(current)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    distances[neighbor] = distances[current] + 1;
                    queue.offer(neighbor);
                }
            }
        }
        
        return distances;
    }
}
```

## 8.3 Topological Sorting

Topological sorting is a linear ordering of vertices in a DAG such that for every directed edge (u,v), vertex u comes before vertex v.

### DFS-based Topological Sort

```java
public class TopologicalSort {
    private List<List<Integer>> adjList;
    private boolean[] visited;
    private Stack<Integer> stack;
    
    public TopologicalSort(int vertices) {
        this.adjList = new ArrayList<>();
        this.visited = new boolean[vertices];
        this.stack = new Stack<>();
        
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
    }
    
    public List<Integer> topologicalSort() {
        for (int i = 0; i < visited.length; i++) {
            if (!visited[i]) {
                dfs(i);
            }
        }
        
        List<Integer> result = new ArrayList<>();
        while (!stack.isEmpty()) {
            result.add(stack.pop());
        }
        
        return result;
    }
    
    private void dfs(int vertex) {
        visited[vertex] = true;
        
        for (Integer neighbor : adjList.get(vertex)) {
            if (!visited[neighbor]) {
                dfs(neighbor);
            }
        }
        
        stack.push(vertex);
    }
}
```

### Kahn's Algorithm (BFS-based)

```java
public class KahnsAlgorithm {
    private List<List<Integer>> adjList;
    private int[] inDegree;
    
    public KahnsAlgorithm(int vertices) {
        this.adjList = new ArrayList<>();
        this.inDegree = new int[vertices];
        
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
        inDegree[destination]++;
    }
    
    public List<Integer> topologicalSort() {
        Queue<Integer> queue = new LinkedList<>();
        List<Integer> result = new ArrayList<>();
        
        // Add all vertices with in-degree 0 to queue
        for (int i = 0; i < inDegree.length; i++) {
            if (inDegree[i] == 0) {
                queue.offer(i);
            }
        }
        
        while (!queue.isEmpty()) {
            int current = queue.poll();
            result.add(current);
            
            // Reduce in-degree of neighbors
            for (Integer neighbor : adjList.get(current)) {
                inDegree[neighbor]--;
                if (inDegree[neighbor] == 0) {
                    queue.offer(neighbor);
                }
            }
        }
        
        // Check if all vertices are processed
        if (result.size() != inDegree.length) {
            return new ArrayList<>(); // Cycle detected
        }
        
        return result;
    }
}
```

## 8.4 Shortest Path Algorithms (Dijkstra, Bellman-Ford)

### Dijkstra's Algorithm

```java
public class DijkstraAlgorithm {
    private List<List<Edge>> adjList;
    private int vertices;
    
    private class Edge {
        int destination;
        int weight;
        
        public Edge(int destination, int weight) {
            this.destination = destination;
            this.weight = weight;
        }
    }
    
    public DijkstraAlgorithm(int vertices) {
        this.vertices = vertices;
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination, int weight) {
        adjList.get(source).add(new Edge(destination, weight));
        adjList.get(destination).add(new Edge(source, weight)); // For undirected graph
    }
    
    public int[] shortestPaths(int source) {
        int[] distances = new int[vertices];
        boolean[] visited = new boolean[vertices];
        PriorityQueue<Edge> pq = new PriorityQueue<>((a, b) -> a.weight - b.weight);
        
        Arrays.fill(distances, Integer.MAX_VALUE);
        distances[source] = 0;
        pq.offer(new Edge(source, 0));
        
        while (!pq.isEmpty()) {
            Edge current = pq.poll();
            int vertex = current.destination;
            
            if (visited[vertex]) continue;
            visited[vertex] = true;
            
            for (Edge neighbor : adjList.get(vertex)) {
                int newDistance = distances[vertex] + neighbor.weight;
                if (newDistance < distances[neighbor.destination]) {
                    distances[neighbor.destination] = newDistance;
                    pq.offer(new Edge(neighbor.destination, newDistance));
                }
            }
        }
        
        return distances;
    }
    
    // Dijkstra with path reconstruction
    public List<Integer> shortestPath(int source, int destination) {
        int[] distances = new int[vertices];
        int[] previous = new int[vertices];
        boolean[] visited = new boolean[vertices];
        PriorityQueue<Edge> pq = new PriorityQueue<>((a, b) -> a.weight - b.weight);
        
        Arrays.fill(distances, Integer.MAX_VALUE);
        Arrays.fill(previous, -1);
        distances[source] = 0;
        pq.offer(new Edge(source, 0));
        
        while (!pq.isEmpty()) {
            Edge current = pq.poll();
            int vertex = current.destination;
            
            if (visited[vertex]) continue;
            visited[vertex] = true;
            
            for (Edge neighbor : adjList.get(vertex)) {
                int newDistance = distances[vertex] + neighbor.weight;
                if (newDistance < distances[neighbor.destination]) {
                    distances[neighbor.destination] = newDistance;
                    previous[neighbor.destination] = vertex;
                    pq.offer(new Edge(neighbor.destination, newDistance));
                }
            }
        }
        
        // Reconstruct path
        List<Integer> path = new ArrayList<>();
        if (distances[destination] == Integer.MAX_VALUE) {
            return path; // No path exists
        }
        
        int current = destination;
        while (current != -1) {
            path.add(current);
            current = previous[current];
        }
        Collections.reverse(path);
        
        return path;
    }
}
```

### Bellman-Ford Algorithm

```java
public class BellmanFordAlgorithm {
    private List<Edge> edges;
    private int vertices;
    
    private class Edge {
        int source;
        int destination;
        int weight;
        
        public Edge(int source, int destination, int weight) {
            this.source = source;
            this.destination = destination;
            this.weight = weight;
        }
    }
    
    public BellmanFordAlgorithm(int vertices) {
        this.vertices = vertices;
        this.edges = new ArrayList<>();
    }
    
    public void addEdge(int source, int destination, int weight) {
        edges.add(new Edge(source, destination, weight));
    }
    
    public int[] shortestPaths(int source) {
        int[] distances = new int[vertices];
        Arrays.fill(distances, Integer.MAX_VALUE);
        distances[source] = 0;
        
        // Relax edges V-1 times
        for (int i = 0; i < vertices - 1; i++) {
            for (Edge edge : edges) {
                if (distances[edge.source] != Integer.MAX_VALUE &&
                    distances[edge.source] + edge.weight < distances[edge.destination]) {
                    distances[edge.destination] = distances[edge.source] + edge.weight;
                }
            }
        }
        
        // Check for negative cycles
        for (Edge edge : edges) {
            if (distances[edge.source] != Integer.MAX_VALUE &&
                distances[edge.source] + edge.weight < distances[edge.destination]) {
                throw new RuntimeException("Negative cycle detected");
            }
        }
        
        return distances;
    }
}
```

## 8.5 All-Pairs Shortest Path (Floyd-Warshall)

```java
public class FloydWarshallAlgorithm {
    private int[][] distances;
    private int[][] next;
    private int vertices;
    
    public FloydWarshallAlgorithm(int vertices) {
        this.vertices = vertices;
        this.distances = new int[vertices][vertices];
        this.next = new int[vertices][vertices];
        
        // Initialize distances
        for (int i = 0; i < vertices; i++) {
            for (int j = 0; j < vertices; j++) {
                if (i == j) {
                    distances[i][j] = 0;
                } else {
                    distances[i][j] = Integer.MAX_VALUE;
                }
                next[i][j] = -1;
            }
        }
    }
    
    public void addEdge(int source, int destination, int weight) {
        distances[source][destination] = weight;
        next[source][destination] = destination;
    }
    
    public int[][] allPairsShortestPaths() {
        // Floyd-Warshall algorithm
        for (int k = 0; k < vertices; k++) {
            for (int i = 0; i < vertices; i++) {
                for (int j = 0; j < vertices; j++) {
                    if (distances[i][k] != Integer.MAX_VALUE &&
                        distances[k][j] != Integer.MAX_VALUE &&
                        distances[i][k] + distances[k][j] < distances[i][j]) {
                        distances[i][j] = distances[i][k] + distances[k][j];
                        next[i][j] = next[i][k];
                    }
                }
            }
        }
        
        return distances;
    }
    
    public List<Integer> getPath(int source, int destination) {
        if (distances[source][destination] == Integer.MAX_VALUE) {
            return new ArrayList<>(); // No path exists
        }
        
        List<Integer> path = new ArrayList<>();
        int current = source;
        
        while (current != destination) {
            path.add(current);
            current = next[current][destination];
        }
        path.add(destination);
        
        return path;
    }
}
```

## 8.6 Minimum Spanning Tree (Kruskal, Prim)

### Kruskal's Algorithm

```java
public class KruskalAlgorithm {
    private List<Edge> edges;
    private int vertices;
    
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
    
    public KruskalAlgorithm(int vertices) {
        this.vertices = vertices;
        this.edges = new ArrayList<>();
    }
    
    public void addEdge(int source, int destination, int weight) {
        edges.add(new Edge(source, destination, weight));
    }
    
    public List<Edge> minimumSpanningTree() {
        List<Edge> mst = new ArrayList<>();
        UnionFind uf = new UnionFind(vertices);
        
        // Sort edges by weight
        Collections.sort(edges);
        
        for (Edge edge : edges) {
            if (uf.find(edge.source) != uf.find(edge.destination)) {
                mst.add(edge);
                uf.union(edge.source, edge.destination);
                
                if (mst.size() == vertices - 1) {
                    break; // MST is complete
                }
            }
        }
        
        return mst;
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
}
```

### Prim's Algorithm

```java
public class PrimAlgorithm {
    private List<List<Edge>> adjList;
    private int vertices;
    
    private class Edge {
        int destination;
        int weight;
        
        public Edge(int destination, int weight) {
            this.destination = destination;
            this.weight = weight;
        }
    }
    
    public PrimAlgorithm(int vertices) {
        this.vertices = vertices;
        this.adjList = new ArrayList<>();
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination, int weight) {
        adjList.get(source).add(new Edge(destination, weight));
        adjList.get(destination).add(new Edge(source, weight));
    }
    
    public List<Edge> minimumSpanningTree() {
        List<Edge> mst = new ArrayList<>();
        boolean[] inMST = new boolean[vertices];
        int[] key = new int[vertices];
        int[] parent = new int[vertices];
        
        Arrays.fill(key, Integer.MAX_VALUE);
        key[0] = 0;
        parent[0] = -1;
        
        PriorityQueue<Edge> pq = new PriorityQueue<>((a, b) -> a.weight - b.weight);
        pq.offer(new Edge(0, 0));
        
        while (!pq.isEmpty()) {
            Edge current = pq.poll();
            int vertex = current.destination;
            
            if (inMST[vertex]) continue;
            inMST[vertex] = true;
            
            if (parent[vertex] != -1) {
                mst.add(new Edge(parent[vertex], vertex));
            }
            
            for (Edge neighbor : adjList.get(vertex)) {
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

## 8.7 Strongly Connected Components

### Tarjan's Algorithm

```java
public class TarjanAlgorithm {
    private List<List<Integer>> adjList;
    private int[] ids;
    private int[] low;
    private boolean[] onStack;
    private Stack<Integer> stack;
    private int id;
    private List<List<Integer>> sccs;
    
    public TarjanAlgorithm(int vertices) {
        this.adjList = new ArrayList<>();
        this.ids = new int[vertices];
        this.low = new int[vertices];
        this.onStack = new boolean[vertices];
        this.stack = new Stack<>();
        this.id = 0;
        this.sccs = new ArrayList<>();
        
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
    }
    
    public List<List<Integer>> findSCCs() {
        for (int i = 0; i < ids.length; i++) {
            if (ids[i] == 0) {
                dfs(i);
            }
        }
        return sccs;
    }
    
    private void dfs(int vertex) {
        stack.push(vertex);
        onStack[vertex] = true;
        ids[vertex] = low[vertex] = ++id;
        
        for (Integer neighbor : adjList.get(vertex)) {
            if (ids[neighbor] == 0) {
                dfs(neighbor);
            }
            if (onStack[neighbor]) {
                low[vertex] = Math.min(low[vertex], low[neighbor]);
            }
        }
        
        if (ids[vertex] == low[vertex]) {
            List<Integer> scc = new ArrayList<>();
            int w;
            do {
                w = stack.pop();
                onStack[w] = false;
                scc.add(w);
            } while (w != vertex);
            sccs.add(scc);
        }
    }
}
```

## 8.8 Network Flow Algorithms (Max Flow, Min Cut)

### Ford-Fulkerson Algorithm

```java
public class FordFulkersonAlgorithm {
    private int[][] capacity;
    private int[][] flow;
    private int vertices;
    
    public FordFulkersonAlgorithm(int vertices) {
        this.vertices = vertices;
        this.capacity = new int[vertices][vertices];
        this.flow = new int[vertices][vertices];
    }
    
    public void addEdge(int source, int destination, int weight) {
        capacity[source][destination] = weight;
    }
    
    public int maxFlow(int source, int sink) {
        int maxFlow = 0;
        
        while (true) {
            int[] parent = new int[vertices];
            Arrays.fill(parent, -1);
            
            Queue<Integer> queue = new LinkedList<>();
            queue.offer(source);
            parent[source] = source;
            
            while (!queue.isEmpty() && parent[sink] == -1) {
                int current = queue.poll();
                
                for (int neighbor = 0; neighbor < vertices; neighbor++) {
                    if (parent[neighbor] == -1 && 
                        capacity[current][neighbor] > flow[current][neighbor]) {
                        parent[neighbor] = current;
                        queue.offer(neighbor);
                    }
                }
            }
            
            if (parent[sink] == -1) break; // No augmenting path found
            
            int pathFlow = Integer.MAX_VALUE;
            int current = sink;
            while (current != source) {
                int parentVertex = parent[current];
                pathFlow = Math.min(pathFlow, capacity[parentVertex][current] - flow[parentVertex][current]);
                current = parentVertex;
            }
            
            current = sink;
            while (current != source) {
                int parentVertex = parent[current];
                flow[parentVertex][current] += pathFlow;
                flow[current][parentVertex] -= pathFlow;
                current = parentVertex;
            }
            
            maxFlow += pathFlow;
        }
        
        return maxFlow;
    }
}
```

## 8.9 Graph Coloring & Matching

### Graph Coloring

```java
public class GraphColoring {
    private List<List<Integer>> adjList;
    private int[] colors;
    private int vertices;
    
    public GraphColoring(int vertices) {
        this.vertices = vertices;
        this.adjList = new ArrayList<>();
        this.colors = new int[vertices];
        
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }
    
    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
        adjList.get(destination).add(source);
    }
    
    public boolean isColorable(int numColors) {
        Arrays.fill(colors, -1);
        return isColorableUtil(0, numColors);
    }
    
    private boolean isColorableUtil(int vertex, int numColors) {
        if (vertex == vertices) return true;
        
        for (int color = 0; color < numColors; color++) {
            if (isSafe(vertex, color)) {
                colors[vertex] = color;
                if (isColorableUtil(vertex + 1, numColors)) {
                    return true;
                }
                colors[vertex] = -1;
            }
        }
        
        return false;
    }
    
    private boolean isSafe(int vertex, int color) {
        for (Integer neighbor : adjList.get(vertex)) {
            if (colors[neighbor] == color) {
                return false;
            }
        }
        return true;
    }
    
    public int chromaticNumber() {
        for (int numColors = 1; numColors <= vertices; numColors++) {
            if (isColorable(numColors)) {
                return numColors;
            }
        }
        return -1;
    }
}
```

**Real-world Analogies:**
- **DFS:** Like exploring a maze by always taking the first available path and backtracking when stuck
- **BFS:** Like exploring a maze by checking all paths at the current level before moving deeper
- **Topological Sort:** Like arranging tasks in order of dependencies
- **Dijkstra:** Like finding the shortest route on a map with weighted roads
- **Bellman-Ford:** Like Dijkstra but can handle negative weights
- **Floyd-Warshall:** Like finding shortest paths between all pairs of cities
- **Kruskal/Prim:** Like connecting all cities with minimum cost roads
- **Graph Coloring:** Like assigning colors to regions on a map so no adjacent regions have the same color

Graph algorithms are fundamental for solving many real-world problems involving networks, relationships, and optimization.