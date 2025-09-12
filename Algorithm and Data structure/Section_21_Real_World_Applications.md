# Section 21 – Real-World Applications

## 21.1 Database Query Optimization

Database query optimization is crucial for maintaining high performance in data-intensive applications.

### Query Execution Plans

```java
public class QueryOptimizer {
    
    public static class QueryPlan {
        String operation;
        double cost;
        int estimatedRows;
        List<QueryPlan> children;
        
        public QueryPlan(String operation, double cost, int estimatedRows) {
            this.operation = operation;
            this.cost = cost;
            this.estimatedRows = estimatedRows;
            this.children = new ArrayList<>();
        }
        
        public double getTotalCost() {
            double totalCost = cost;
            for (QueryPlan child : children) {
                totalCost += child.getTotalCost();
            }
            return totalCost;
        }
    }
    
    // Cost-based query optimizer
    public static QueryPlan optimizeQuery(String sql) {
        // Parse SQL and generate execution plans
        List<QueryPlan> plans = generateExecutionPlans(sql);
        
        // Select plan with minimum cost
        QueryPlan bestPlan = plans.get(0);
        for (QueryPlan plan : plans) {
            if (plan.getTotalCost() < bestPlan.getTotalCost()) {
                bestPlan = plan;
            }
        }
        
        return bestPlan;
    }
    
    private static List<QueryPlan> generateExecutionPlans(String sql) {
        List<QueryPlan> plans = new ArrayList<>();
        
        // Example: SELECT * FROM users WHERE age > 25 ORDER BY name
        // Plan 1: Index scan on age, then sort
        QueryPlan plan1 = new QueryPlan("Index Scan", 100.0, 1000);
        plan1.children.add(new QueryPlan("Sort", 50.0, 1000));
        plans.add(plan1);
        
        // Plan 2: Full table scan, then filter and sort
        QueryPlan plan2 = new QueryPlan("Full Table Scan", 200.0, 10000);
        plan2.children.add(new QueryPlan("Filter", 30.0, 1000));
        plan2.children.add(new QueryPlan("Sort", 50.0, 1000));
        plans.add(plan2);
        
        return plans;
    }
}
```

### Index Selection Algorithm

```java
public class IndexSelection {
    
    public static class Index {
        String tableName;
        String columnName;
        double selectivity;
        double maintenanceCost;
        double storageCost;
        
        public Index(String tableName, String columnName, double selectivity, 
                    double maintenanceCost, double storageCost) {
            this.tableName = tableName;
            this.columnName = columnName;
            this.selectivity = selectivity;
            this.maintenanceCost = maintenanceCost;
            this.storageCost = storageCost;
        }
        
        public double getBenefit() {
            return (1.0 - selectivity) * 1000 - maintenanceCost - storageCost;
        }
    }
    
    // Greedy algorithm for index selection
    public static List<Index> selectIndexes(List<Index> candidateIndexes, double budget) {
        List<Index> selectedIndexes = new ArrayList<>();
        double remainingBudget = budget;
        
        // Sort by benefit per cost ratio
        candidateIndexes.sort((a, b) -> 
            Double.compare(b.getBenefit() / (a.maintenanceCost + a.storageCost),
                          a.getBenefit() / (b.maintenanceCost + b.storageCost)));
        
        for (Index index : candidateIndexes) {
            double totalCost = index.maintenanceCost + index.storageCost;
            if (totalCost <= remainingBudget) {
                selectedIndexes.add(index);
                remainingBudget -= totalCost;
            }
        }
        
        return selectedIndexes;
    }
}
```

## 21.2 Search Engine Algorithms

### PageRank Algorithm

```java
public class PageRank {
    private static final double DAMPING_FACTOR = 0.85;
    private static final double CONVERGENCE_THRESHOLD = 0.0001;
    private static final int MAX_ITERATIONS = 100;
    
    public static Map<String, Double> calculatePageRank(Map<String, List<String>> graph) {
        Map<String, Double> pageRank = new HashMap<>();
        Map<String, Double> newPageRank = new HashMap<>();
        
        // Initialize PageRank values
        double initialRank = 1.0 / graph.size();
        for (String page : graph.keySet()) {
            pageRank.put(page, initialRank);
        }
        
        // Iterate until convergence
        for (int iteration = 0; iteration < MAX_ITERATIONS; iteration++) {
            double totalDiff = 0.0;
            
            for (String page : graph.keySet()) {
                double rank = 0.0;
                
                // Calculate PageRank from incoming links
                for (Map.Entry<String, List<String>> entry : graph.entrySet()) {
                    String sourcePage = entry.getKey();
                    List<String> outgoingLinks = entry.getValue();
                    
                    if (outgoingLinks.contains(page) && !outgoingLinks.isEmpty()) {
                        rank += pageRank.get(sourcePage) / outgoingLinks.size();
                    }
                }
                
                // Apply damping factor
                rank = (1.0 - DAMPING_FACTOR) / graph.size() + DAMPING_FACTOR * rank;
                newPageRank.put(page, rank);
                
                totalDiff += Math.abs(rank - pageRank.get(page));
            }
            
            // Update PageRank values
            pageRank.putAll(newPageRank);
            
            // Check for convergence
            if (totalDiff < CONVERGENCE_THRESHOLD) {
                break;
            }
        }
        
        return pageRank;
    }
}
```

### Inverted Index

```java
public class InvertedIndex {
    private Map<String, List<Document>> index;
    
    public InvertedIndex() {
        this.index = new HashMap<>();
    }
    
    public void addDocument(String docId, String content) {
        String[] words = content.toLowerCase().split("\\s+");
        
        for (String word : words) {
            // Remove punctuation
            word = word.replaceAll("[^a-zA-Z0-9]", "");
            if (word.isEmpty()) continue;
            
            index.computeIfAbsent(word, k -> new ArrayList<>())
                 .add(new Document(docId, content));
        }
    }
    
    public List<Document> search(String query) {
        String[] words = query.toLowerCase().split("\\s+");
        Set<Document> result = new HashSet<>();
        
        for (String word : words) {
            word = word.replaceAll("[^a-zA-Z0-9]", "");
            if (word.isEmpty()) continue;
            
            List<Document> docs = index.get(word);
            if (docs != null) {
                if (result.isEmpty()) {
                    result.addAll(docs);
                } else {
                    result.retainAll(docs);
                }
            }
        }
        
        return new ArrayList<>(result);
    }
    
    public static class Document {
        String id;
        String content;
        
        public Document(String id, String content) {
            this.id = id;
            this.content = content;
        }
        
        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            Document document = (Document) obj;
            return Objects.equals(id, document.id);
        }
        
        @Override
        public int hashCode() {
            return Objects.hash(id);
        }
    }
}
```

## 21.3 Recommendation Systems

### Collaborative Filtering

```java
public class CollaborativeFiltering {
    
    public static class User {
        int id;
        Map<Integer, Double> ratings; // itemId -> rating
        
        public User(int id) {
            this.id = id;
            this.ratings = new HashMap<>();
        }
    }
    
    public static class Item {
        int id;
        String name;
        
        public Item(int id, String name) {
            this.id = id;
            this.name = name;
        }
    }
    
    // User-based collaborative filtering
    public static List<Integer> recommendItems(List<User> users, int targetUserId, int numRecommendations) {
        User targetUser = users.stream()
            .filter(u -> u.id == targetUserId)
            .findFirst()
            .orElse(null);
        
        if (targetUser == null) return new ArrayList<>();
        
        // Find similar users
        List<UserSimilarity> similarities = new ArrayList<>();
        for (User user : users) {
            if (user.id != targetUserId) {
                double similarity = calculateCosineSimilarity(targetUser, user);
                similarities.add(new UserSimilarity(user, similarity));
            }
        }
        
        // Sort by similarity
        similarities.sort((a, b) -> Double.compare(b.similarity, a.similarity));
        
        // Generate recommendations
        Map<Integer, Double> itemScores = new HashMap<>();
        for (UserSimilarity sim : similarities) {
            User user = sim.user;
            for (Map.Entry<Integer, Double> entry : user.ratings.entrySet()) {
                int itemId = entry.getKey();
                double rating = entry.getValue();
                
                if (!targetUser.ratings.containsKey(itemId)) {
                    itemScores.merge(itemId, rating * sim.similarity, Double::sum);
                }
            }
        }
        
        // Sort items by score
        return itemScores.entrySet().stream()
            .sorted((a, b) -> Double.compare(b.getValue(), a.getValue()))
            .limit(numRecommendations)
            .map(Map.Entry::getKey)
            .collect(Collectors.toList());
    }
    
    private static double calculateCosineSimilarity(User user1, User user2) {
        Set<Integer> commonItems = new HashSet<>(user1.ratings.keySet());
        commonItems.retainAll(user2.ratings.keySet());
        
        if (commonItems.isEmpty()) return 0.0;
        
        double dotProduct = 0.0;
        double norm1 = 0.0;
        double norm2 = 0.0;
        
        for (int itemId : commonItems) {
            double rating1 = user1.ratings.get(itemId);
            double rating2 = user2.ratings.get(itemId);
            
            dotProduct += rating1 * rating2;
            norm1 += rating1 * rating1;
            norm2 += rating2 * rating2;
        }
        
        if (norm1 == 0.0 || norm2 == 0.0) return 0.0;
        
        return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
    }
    
    private static class UserSimilarity {
        User user;
        double similarity;
        
        public UserSimilarity(User user, double similarity) {
            this.user = user;
            this.similarity = similarity;
        }
    }
}
```

### Content-Based Filtering

```java
public class ContentBasedFiltering {
    
    public static class Item {
        int id;
        Map<String, Double> features; // feature -> weight
        
        public Item(int id, Map<String, Double> features) {
            this.id = id;
            this.features = features;
        }
    }
    
    public static class UserProfile {
        int userId;
        Map<String, Double> preferences; // feature -> weight
        
        public UserProfile(int userId, Map<String, Double> preferences) {
            this.userId = userId;
            this.preferences = preferences;
        }
    }
    
    // Build user profile from item ratings
    public static UserProfile buildUserProfile(int userId, List<Item> items, 
                                             Map<Integer, Double> ratings) {
        Map<String, Double> preferences = new HashMap<>();
        Map<String, Double> featureWeights = new HashMap<>();
        
        for (Item item : items) {
            if (ratings.containsKey(item.id)) {
                double rating = ratings.get(item.id);
                
                for (Map.Entry<String, Double> entry : item.features.entrySet()) {
                    String feature = entry.getKey();
                    double weight = entry.getValue();
                    
                    preferences.merge(feature, rating * weight, Double::sum);
                    featureWeights.merge(feature, weight, Double::sum);
                }
            }
        }
        
        // Normalize preferences
        for (String feature : preferences.keySet()) {
            double totalWeight = featureWeights.get(feature);
            if (totalWeight > 0) {
                preferences.put(feature, preferences.get(feature) / totalWeight);
            }
        }
        
        return new UserProfile(userId, preferences);
    }
    
    // Recommend items based on user profile
    public static List<Integer> recommendItems(UserProfile profile, List<Item> items, 
                                             int numRecommendations) {
        Map<Integer, Double> itemScores = new HashMap<>();
        
        for (Item item : items) {
            double score = calculateSimilarity(profile.preferences, item.features);
            itemScores.put(item.id, score);
        }
        
        return itemScores.entrySet().stream()
            .sorted((a, b) -> Double.compare(b.getValue(), a.getValue()))
            .limit(numRecommendations)
            .map(Map.Entry::getKey)
            .collect(Collectors.toList());
    }
    
    private static double calculateSimilarity(Map<String, Double> preferences, 
                                            Map<String, Double> features) {
        Set<String> commonFeatures = new HashSet<>(preferences.keySet());
        commonFeatures.retainAll(features.keySet());
        
        if (commonFeatures.isEmpty()) return 0.0;
        
        double dotProduct = 0.0;
        double norm1 = 0.0;
        double norm2 = 0.0;
        
        for (String feature : commonFeatures) {
            double pref = preferences.get(feature);
            double feat = features.get(feature);
            
            dotProduct += pref * feat;
            norm1 += pref * pref;
            norm2 += feat * feat;
        }
        
        if (norm1 == 0.0 || norm2 == 0.0) return 0.0;
        
        return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
    }
}
```

## 21.4 Machine Learning Algorithms

### K-Means Clustering

```java
public class KMeansClustering {
    
    public static class Point {
        double x, y;
        
        public Point(double x, double y) {
            this.x = x;
            this.y = y;
        }
        
        public double distanceTo(Point other) {
            double dx = this.x - other.x;
            double dy = this.y - other.y;
            return Math.sqrt(dx * dx + dy * dy);
        }
    }
    
    public static class Cluster {
        Point centroid;
        List<Point> points;
        
        public Cluster(Point centroid) {
            this.centroid = centroid;
            this.points = new ArrayList<>();
        }
        
        public void updateCentroid() {
            if (points.isEmpty()) return;
            
            double sumX = 0.0;
            double sumY = 0.0;
            
            for (Point point : points) {
                sumX += point.x;
                sumY += point.y;
            }
            
            centroid = new Point(sumX / points.size(), sumY / points.size());
        }
    }
    
    public static List<Cluster> cluster(List<Point> points, int k, int maxIterations) {
        if (points.isEmpty() || k <= 0) return new ArrayList<>();
        
        // Initialize centroids randomly
        List<Cluster> clusters = new ArrayList<>();
        Random random = new Random();
        
        for (int i = 0; i < k; i++) {
            Point randomPoint = points.get(random.nextInt(points.size()));
            clusters.add(new Cluster(new Point(randomPoint.x, randomPoint.y)));
        }
        
        // Iterate until convergence
        for (int iteration = 0; iteration < maxIterations; iteration++) {
            // Clear points from clusters
            for (Cluster cluster : clusters) {
                cluster.points.clear();
            }
            
            // Assign points to nearest centroid
            for (Point point : points) {
                Cluster nearestCluster = null;
                double minDistance = Double.MAX_VALUE;
                
                for (Cluster cluster : clusters) {
                    double distance = point.distanceTo(cluster.centroid);
                    if (distance < minDistance) {
                        minDistance = distance;
                        nearestCluster = cluster;
                    }
                }
                
                if (nearestCluster != null) {
                    nearestCluster.points.add(point);
                }
            }
            
            // Update centroids
            boolean converged = true;
            for (Cluster cluster : clusters) {
                Point oldCentroid = cluster.centroid;
                cluster.updateCentroid();
                
                if (oldCentroid.distanceTo(cluster.centroid) > 0.001) {
                    converged = false;
                }
            }
            
            if (converged) break;
        }
        
        return clusters;
    }
}
```

### Decision Tree

```java
public class DecisionTree {
    
    public static class TreeNode {
        String attribute;
        String value;
        String classification;
        List<TreeNode> children;
        
        public TreeNode(String attribute, String value) {
            this.attribute = attribute;
            this.value = value;
            this.children = new ArrayList<>();
        }
        
        public boolean isLeaf() {
            return children.isEmpty();
        }
    }
    
    public static class TrainingExample {
        Map<String, String> attributes;
        String classification;
        
        public TrainingExample(Map<String, String> attributes, String classification) {
            this.attributes = attributes;
            this.classification = classification;
        }
    }
    
    public static TreeNode buildTree(List<TrainingExample> examples, List<String> attributes) {
        if (examples.isEmpty()) return null;
        
        // Check if all examples have same classification
        String firstClassification = examples.get(0).classification;
        boolean allSame = examples.stream().allMatch(e -> e.classification.equals(firstClassification));
        
        if (allSame) {
            TreeNode leaf = new TreeNode(null, null);
            leaf.classification = firstClassification;
            return leaf;
        }
        
        // Check if no attributes left
        if (attributes.isEmpty()) {
            TreeNode leaf = new TreeNode(null, null);
            leaf.classification = getMajorityClassification(examples);
            return leaf;
        }
        
        // Find best attribute to split on
        String bestAttribute = findBestAttribute(examples, attributes);
        TreeNode root = new TreeNode(bestAttribute, null);
        
        // Get unique values for best attribute
        Set<String> values = examples.stream()
            .map(e -> e.attributes.get(bestAttribute))
            .collect(Collectors.toSet());
        
        // Create subtrees for each value
        for (String value : values) {
            List<TrainingExample> subset = examples.stream()
                .filter(e -> e.attributes.get(bestAttribute).equals(value))
                .collect(Collectors.toList());
            
            List<String> remainingAttributes = new ArrayList<>(attributes);
            remainingAttributes.remove(bestAttribute);
            
            TreeNode child = buildTree(subset, remainingAttributes);
            if (child != null) {
                child.value = value;
                root.children.add(child);
            }
        }
        
        return root;
    }
    
    private static String findBestAttribute(List<TrainingExample> examples, List<String> attributes) {
        String bestAttribute = attributes.get(0);
        double bestGain = calculateInformationGain(examples, bestAttribute);
        
        for (String attribute : attributes) {
            double gain = calculateInformationGain(examples, attribute);
            if (gain > bestGain) {
                bestGain = gain;
                bestAttribute = attribute;
            }
        }
        
        return bestAttribute;
    }
    
    private static double calculateInformationGain(List<TrainingExample> examples, String attribute) {
        double entropy = calculateEntropy(examples);
        
        // Group examples by attribute value
        Map<String, List<TrainingExample>> groups = examples.stream()
            .collect(Collectors.groupingBy(e -> e.attributes.get(attribute)));
        
        double weightedEntropy = 0.0;
        for (List<TrainingExample> group : groups.values()) {
            double weight = (double) group.size() / examples.size();
            weightedEntropy += weight * calculateEntropy(group);
        }
        
        return entropy - weightedEntropy;
    }
    
    private static double calculateEntropy(List<TrainingExample> examples) {
        Map<String, Long> classCounts = examples.stream()
            .collect(Collectors.groupingBy(e -> e.classification, Collectors.counting()));
        
        double entropy = 0.0;
        int total = examples.size();
        
        for (long count : classCounts.values()) {
            double probability = (double) count / total;
            if (probability > 0) {
                entropy -= probability * Math.log(probability) / Math.log(2);
            }
        }
        
        return entropy;
    }
    
    private static String getMajorityClassification(List<TrainingExample> examples) {
        return examples.stream()
            .collect(Collectors.groupingBy(e -> e.classification, Collectors.counting()))
            .entrySet().stream()
            .max(Map.Entry.comparingByValue())
            .map(Map.Entry::getKey)
            .orElse("unknown");
    }
}
```

## 21.5 Network Routing Algorithms

### Dijkstra's Shortest Path

```java
public class NetworkRouting {
    
    public static class Node {
        int id;
        String name;
        
        public Node(int id, String name) {
            this.id = id;
            this.name = name;
        }
    }
    
    public static class Edge {
        int from, to;
        double weight;
        
        public Edge(int from, int to, double weight) {
            this.from = from;
            this.to = to;
            this.weight = weight;
        }
    }
    
    public static class Path {
        List<Integer> nodes;
        double totalWeight;
        
        public Path(List<Integer> nodes, double totalWeight) {
            this.nodes = nodes;
            this.totalWeight = totalWeight;
        }
    }
    
    // Dijkstra's algorithm for shortest path
    public static Path findShortestPath(List<Edge> edges, int start, int end, int numNodes) {
        // Build adjacency list
        Map<Integer, List<Edge>> graph = new HashMap<>();
        for (int i = 0; i < numNodes; i++) {
            graph.put(i, new ArrayList<>());
        }
        
        for (Edge edge : edges) {
            graph.get(edge.from).add(edge);
        }
        
        // Dijkstra's algorithm
        double[] distances = new double[numNodes];
        int[] previous = new int[numNodes];
        boolean[] visited = new boolean[numNodes];
        
        Arrays.fill(distances, Double.MAX_VALUE);
        distances[start] = 0.0;
        previous[start] = -1;
        
        PriorityQueue<Integer> pq = new PriorityQueue<>(Comparator.comparingDouble(i -> distances[i]));
        pq.offer(start);
        
        while (!pq.isEmpty()) {
            int current = pq.poll();
            
            if (visited[current]) continue;
            visited[current] = true;
            
            if (current == end) break;
            
            for (Edge edge : graph.get(current)) {
                int neighbor = edge.to;
                double newDistance = distances[current] + edge.weight;
                
                if (newDistance < distances[neighbor]) {
                    distances[neighbor] = newDistance;
                    previous[neighbor] = current;
                    pq.offer(neighbor);
                }
            }
        }
        
        // Reconstruct path
        if (distances[end] == Double.MAX_VALUE) {
            return null; // No path found
        }
        
        List<Integer> path = new ArrayList<>();
        int current = end;
        while (current != -1) {
            path.add(current);
            current = previous[current];
        }
        Collections.reverse(path);
        
        return new Path(path, distances[end]);
    }
}
```

### A* Algorithm

```java
public class AStarRouting {
    
    public static class Node {
        int id;
        double x, y;
        
        public Node(int id, double x, double y) {
            this.id = id;
            this.x = x;
            this.y = y;
        }
        
        public double heuristic(Node other) {
            double dx = this.x - other.x;
            double dy = this.y - other.y;
            return Math.sqrt(dx * dx + dy * dy);
        }
    }
    
    public static class AStarNode implements Comparable<AStarNode> {
        int nodeId;
        double g; // Cost from start
        double h; // Heuristic cost to goal
        double f; // Total cost (g + h)
        int parent;
        
        public AStarNode(int nodeId, double g, double h, int parent) {
            this.nodeId = nodeId;
            this.g = g;
            this.h = h;
            this.f = g + h;
            this.parent = parent;
        }
        
        @Override
        public int compareTo(AStarNode other) {
            return Double.compare(this.f, other.f);
        }
    }
    
    public static List<Integer> findPath(List<Node> nodes, List<Edge> edges, int start, int goal) {
        Map<Integer, List<Edge>> graph = buildGraph(edges);
        Map<Integer, Node> nodeMap = nodes.stream()
            .collect(Collectors.toMap(n -> n.id, n -> n));
        
        PriorityQueue<AStarNode> openSet = new PriorityQueue<>();
        Set<Integer> closedSet = new HashSet<>();
        Map<Integer, AStarNode> openSetMap = new HashMap<>();
        
        Node startNode = nodeMap.get(start);
        Node goalNode = nodeMap.get(goal);
        
        AStarNode startAStar = new AStarNode(start, 0, startNode.heuristic(goalNode), -1);
        openSet.offer(startAStar);
        openSetMap.put(start, startAStar);
        
        while (!openSet.isEmpty()) {
            AStarNode current = openSet.poll();
            openSetMap.remove(current.nodeId);
            
            if (current.nodeId == goal) {
                return reconstructPath(current, start);
            }
            
            closedSet.add(current.nodeId);
            
            for (Edge edge : graph.get(current.nodeId)) {
                int neighbor = edge.to;
                
                if (closedSet.contains(neighbor)) continue;
                
                double tentativeG = current.g + edge.weight;
                AStarNode neighborNode = openSetMap.get(neighbor);
                
                if (neighborNode == null || tentativeG < neighborNode.g) {
                    Node neighborNodeData = nodeMap.get(neighbor);
                    double h = neighborNodeData.heuristic(goalNode);
                    
                    AStarNode newNeighbor = new AStarNode(neighbor, tentativeG, h, current.nodeId);
                    
                    if (neighborNode != null) {
                        openSet.remove(neighborNode);
                    }
                    
                    openSet.offer(newNeighbor);
                    openSetMap.put(neighbor, newNeighbor);
                }
            }
        }
        
        return null; // No path found
    }
    
    private static Map<Integer, List<Edge>> buildGraph(List<Edge> edges) {
        Map<Integer, List<Edge>> graph = new HashMap<>();
        
        for (Edge edge : edges) {
            graph.computeIfAbsent(edge.from, k -> new ArrayList<>()).add(edge);
        }
        
        return graph;
    }
    
    private static List<Integer> reconstructPath(AStarNode goal, int start) {
        List<Integer> path = new ArrayList<>();
        AStarNode current = goal;
        
        while (current != null) {
            path.add(current.nodeId);
            if (current.parent == -1) break;
            current = new AStarNode(current.parent, 0, 0, -1); // Simplified
        }
        
        Collections.reverse(path);
        return path;
    }
}
```

## 21.6 Compression Algorithms

### LZ77 Compression

```java
public class LZ77Compression {
    
    public static class LZ77Token {
        int offset;
        int length;
        char nextChar;
        
        public LZ77Token(int offset, int length, char nextChar) {
            this.offset = offset;
            this.length = length;
            this.nextChar = nextChar;
        }
    }
    
    public static List<LZ77Token> compress(String input) {
        List<LZ77Token> tokens = new ArrayList<>();
        int i = 0;
        
        while (i < input.length()) {
            int matchLength = 0;
            int matchOffset = 0;
            
            // Search for longest match in sliding window
            for (int j = Math.max(0, i - 255); j < i; j++) {
                int length = 0;
                while (i + length < input.length() && 
                       j + length < i && 
                       input.charAt(i + length) == input.charAt(j + length) && 
                       length < 258) {
                    length++;
                }
                
                if (length > matchLength) {
                    matchLength = length;
                    matchOffset = i - j;
                }
            }
            
            if (matchLength > 2) {
                tokens.add(new LZ77Token(matchOffset, matchLength, 
                    i + matchLength < input.length() ? input.charAt(i + matchLength) : '\0'));
                i += matchLength + 1;
            } else {
                tokens.add(new LZ77Token(0, 0, input.charAt(i)));
                i++;
            }
        }
        
        return tokens;
    }
    
    public static String decompress(List<LZ77Token> tokens) {
        StringBuilder output = new StringBuilder();
        
        for (LZ77Token token : tokens) {
            if (token.length > 0) {
                // Copy from previous position
                int start = output.length() - token.offset;
                for (int i = 0; i < token.length; i++) {
                    output.append(output.charAt(start + i));
                }
            }
            
            if (token.nextChar != '\0') {
                output.append(token.nextChar);
            }
        }
        
        return output.toString();
    }
}
```

### Huffman Compression

```java
public class HuffmanCompression {
    
    public static class HuffmanNode implements Comparable<HuffmanNode> {
        char character;
        int frequency;
        HuffmanNode left, right;
        
        public HuffmanNode(char character, int frequency) {
            this.character = character;
            this.frequency = frequency;
        }
        
        public HuffmanNode(int frequency, HuffmanNode left, HuffmanNode right) {
            this.frequency = frequency;
            this.left = left;
            this.right = right;
        }
        
        public boolean isLeaf() {
            return left == null && right == null;
        }
        
        @Override
        public int compareTo(HuffmanNode other) {
            return Integer.compare(this.frequency, other.frequency);
        }
    }
    
    public static Map<Character, String> buildHuffmanTree(String text) {
        // Count character frequencies
        Map<Character, Integer> frequencies = new HashMap<>();
        for (char c : text.toCharArray()) {
            frequencies.put(c, frequencies.getOrDefault(c, 0) + 1);
        }
        
        // Build priority queue
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
    
    private static void generateCodes(HuffmanNode root, String code, Map<Character, String> codes) {
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
    
    public static String encode(String text, Map<Character, String> codes) {
        StringBuilder encoded = new StringBuilder();
        for (char c : text.toCharArray()) {
            encoded.append(codes.get(c));
        }
        return encoded.toString();
    }
}
```

## 21.7 Cryptography & Security

### RSA Encryption

```java
import java.math.BigInteger;
import java.security.SecureRandom;

public class RSAEncryption {
    private BigInteger n, e, d;
    
    public RSAEncryption(int bitLength) {
        generateKeys(bitLength);
    }
    
    private void generateKeys(int bitLength) {
        SecureRandom random = new SecureRandom();
        
        // Generate two large primes
        BigInteger p = BigInteger.probablePrime(bitLength / 2, random);
        BigInteger q = BigInteger.probablePrime(bitLength / 2, random);
        
        // Calculate n and phi
        n = p.multiply(q);
        BigInteger phi = p.subtract(BigInteger.ONE).multiply(q.subtract(BigInteger.ONE));
        
        // Choose e (public exponent)
        e = BigInteger.valueOf(65537);
        while (e.gcd(phi).compareTo(BigInteger.ONE) > 0) {
            e = e.add(BigInteger.ONE);
        }
        
        // Calculate d (private exponent)
        d = e.modInverse(phi);
    }
    
    public BigInteger encrypt(BigInteger message) {
        return message.modPow(e, n);
    }
    
    public BigInteger decrypt(BigInteger ciphertext) {
        return ciphertext.modPow(d, n);
    }
    
    public BigInteger getPublicKey() {
        return e;
    }
    
    public BigInteger getModulus() {
        return n;
    }
}
```

### AES Encryption

```java
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.util.Base64;

public class AESEncryption {
    private SecretKey key;
    private Cipher cipher;
    
    public AESEncryption() throws Exception {
        KeyGenerator keyGenerator = KeyGenerator.getInstance("AES");
        keyGenerator.init(256);
        this.key = keyGenerator.generateKey();
        this.cipher = Cipher.getInstance("AES");
    }
    
    public String encrypt(String plaintext) throws Exception {
        cipher.init(Cipher.ENCRYPT_MODE, key);
        byte[] encryptedBytes = cipher.doFinal(plaintext.getBytes());
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }
    
    public String decrypt(String ciphertext) throws Exception {
        cipher.init(Cipher.DECRYPT_MODE, key);
        byte[] decodedBytes = Base64.getDecoder().decode(ciphertext);
        byte[] decryptedBytes = cipher.doFinal(decodedBytes);
        return new String(decryptedBytes);
    }
}
```

## 21.8 Game AI Algorithms

### Minimax Algorithm

```java
public class MinimaxAI {
    
    public static class GameState {
        int[][] board;
        int currentPlayer;
        
        public GameState(int[][] board, int currentPlayer) {
            this.board = board;
            this.currentPlayer = currentPlayer;
        }
        
        public boolean isTerminal() {
            return isWin(1) || isWin(2) || isDraw();
        }
        
        public int getWinner() {
            if (isWin(1)) return 1;
            if (isWin(2)) return 2;
            return 0;
        }
        
        private boolean isWin(int player) {
            // Check rows
            for (int i = 0; i < 3; i++) {
                if (board[i][0] == player && board[i][1] == player && board[i][2] == player) {
                    return true;
                }
            }
            
            // Check columns
            for (int j = 0; j < 3; j++) {
                if (board[0][j] == player && board[1][j] == player && board[2][j] == player) {
                    return true;
                }
            }
            
            // Check diagonals
            if (board[0][0] == player && board[1][1] == player && board[2][2] == player) {
                return true;
            }
            if (board[0][2] == player && board[1][1] == player && board[2][0] == player) {
                return true;
            }
            
            return false;
        }
        
        private boolean isDraw() {
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    if (board[i][j] == 0) return false;
                }
            }
            return true;
        }
    }
    
    public static int[] getBestMove(GameState state) {
        int bestScore = Integer.MIN_VALUE;
        int[] bestMove = null;
        
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (state.board[i][j] == 0) {
                    state.board[i][j] = 2; // AI player
                    int score = minimax(state, 0, false);
                    state.board[i][j] = 0; // Undo move
                    
                    if (score > bestScore) {
                        bestScore = score;
                        bestMove = new int[]{i, j};
                    }
                }
            }
        }
        
        return bestMove;
    }
    
    private static int minimax(GameState state, int depth, boolean isMaximizing) {
        if (state.isTerminal()) {
            int winner = state.getWinner();
            if (winner == 2) return 10 - depth; // AI wins
            if (winner == 1) return depth - 10; // Human wins
            return 0; // Draw
        }
        
        if (isMaximizing) {
            int bestScore = Integer.MIN_VALUE;
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    if (state.board[i][j] == 0) {
                        state.board[i][j] = 2;
                        int score = minimax(state, depth + 1, false);
                        state.board[i][j] = 0;
                        bestScore = Math.max(bestScore, score);
                    }
                }
            }
            return bestScore;
        } else {
            int bestScore = Integer.MAX_VALUE;
            for (int i = 0; i < 3; i++) {
                for (int j = 0; j < 3; j++) {
                    if (state.board[i][j] == 0) {
                        state.board[i][j] = 1;
                        int score = minimax(state, depth + 1, true);
                        state.board[i][j] = 0;
                        bestScore = Math.min(bestScore, score);
                    }
                }
            }
            return bestScore;
        }
    }
}
```

**Real-world Analogies:**
- **Database Query Optimization:** Like finding the most efficient route through a city with multiple possible paths
- **Search Engine Algorithms:** Like organizing a library with an index that helps you find books quickly
- **Recommendation Systems:** Like a friend who knows your tastes and suggests movies you might like
- **Machine Learning Algorithms:** Like teaching a computer to recognize patterns by showing it many examples
- **Network Routing:** Like GPS finding the best route considering traffic, distance, and road conditions
- **Compression Algorithms:** Like packing a suitcase efficiently to fit more items
- **Cryptography:** Like having a secret code that only you and your friend can understand
- **Game AI:** Like a chess master who can think several moves ahead to find the best strategy

Real-world applications of algorithms are everywhere in modern technology. Understanding how these algorithms work helps in building better, more efficient systems that solve practical problems in various domains.