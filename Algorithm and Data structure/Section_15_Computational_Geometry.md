# Section 15 – Computational Geometry

## 15.1 Basic Geometric Concepts

Computational geometry deals with algorithms for solving geometric problems. It combines mathematics and computer science to solve problems involving points, lines, polygons, and other geometric objects.

### Fundamental Concepts

**Points:** Represented by coordinates (x, y) in 2D or (x, y, z) in 3D
**Lines:** Defined by two points or by a point and direction
**Polygons:** Closed shapes formed by connected line segments
**Vectors:** Directed line segments with magnitude and direction

**Real-world Analogy:**
Think of computational geometry like being a digital architect. You need to design buildings, plan city layouts, or create video game worlds - all of which involve working with shapes, distances, and spatial relationships.

### Point and Vector Operations

```java
public class Point2D {
    public double x, y;
    
    public Point2D(double x, double y) {
        this.x = x;
        this.y = y;
    }
    
    // Calculate distance between two points
    public double distanceTo(Point2D other) {
        double dx = this.x - other.x;
        double dy = this.y - other.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
    
    // Calculate squared distance (faster, avoids sqrt)
    public double distanceSquaredTo(Point2D other) {
        double dx = this.x - other.x;
        double dy = this.y - other.y;
        return dx * dx + dy * dy;
    }
    
    // Vector addition
    public Point2D add(Point2D other) {
        return new Point2D(this.x + other.x, this.y + other.y);
    }
    
    // Vector subtraction
    public Point2D subtract(Point2D other) {
        return new Point2D(this.x - other.x, this.y - other.y);
    }
    
    // Scalar multiplication
    public Point2D multiply(double scalar) {
        return new Point2D(this.x * scalar, this.y * scalar);
    }
    
    // Dot product
    public double dot(Point2D other) {
        return this.x * other.x + this.y * other.y;
    }
    
    // Cross product (2D cross product returns scalar)
    public double cross(Point2D other) {
        return this.x * other.y - this.y * other.x;
    }
    
    // Calculate angle between vectors
    public double angleTo(Point2D other) {
        double dot = this.dot(other);
        double mag1 = Math.sqrt(this.x * this.x + this.y * this.y);
        double mag2 = Math.sqrt(other.x * other.x + other.y * other.y);
        return Math.acos(dot / (mag1 * mag2));
    }
}
```

### Line and Segment Operations

```java
public class Line2D {
    public Point2D p1, p2;
    
    public Line2D(Point2D p1, Point2D p2) {
        this.p1 = p1;
        this.p2 = p2;
    }
    
    // Check if point is on line
    public boolean containsPoint(Point2D point) {
        double cross = (point.x - p1.x) * (p2.y - p1.y) - (point.y - p1.y) * (p2.x - p1.x);
        return Math.abs(cross) < 1e-9; // Use epsilon for floating point comparison
    }
    
    // Check if point is on line segment
    public boolean containsPointOnSegment(Point2D point) {
        if (!containsPoint(point)) return false;
        
        // Check if point is within segment bounds
        double minX = Math.min(p1.x, p2.x);
        double maxX = Math.max(p1.x, p2.x);
        double minY = Math.min(p1.y, p2.y);
        double maxY = Math.max(p1.y, p2.y);
        
        return point.x >= minX && point.x <= maxX && point.y >= minY && point.y <= maxY;
    }
    
    // Calculate distance from point to line
    public double distanceToPoint(Point2D point) {
        Point2D lineVec = p2.subtract(p1);
        Point2D pointVec = point.subtract(p1);
        
        double cross = lineVec.cross(pointVec);
        double lineLength = Math.sqrt(lineVec.x * lineVec.x + lineVec.y * lineVec.y);
        
        return Math.abs(cross) / lineLength;
    }
    
    // Check if two lines intersect
    public boolean intersects(Line2D other) {
        Point2D p1 = this.p1, p2 = this.p2;
        Point2D p3 = other.p1, p4 = other.p2;
        
        double denom = (p1.x - p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x - p4.x);
        
        if (Math.abs(denom) < 1e-9) {
            // Lines are parallel
            return false;
        }
        
        double t = ((p1.x - p3.x) * (p3.y - p4.y) - (p1.y - p3.y) * (p3.x - p4.x)) / denom;
        double u = -((p1.x - p2.x) * (p1.y - p3.y) - (p1.y - p2.y) * (p1.x - p3.x)) / denom;
        
        return t >= 0 && t <= 1 && u >= 0 && u <= 1;
    }
}
```

## 15.2 Convex Hull Algorithms

The convex hull of a set of points is the smallest convex polygon that contains all the points.

### Graham Scan Algorithm

```java
public class ConvexHull {
    public static List<Point2D> grahamScan(List<Point2D> points) {
        if (points.size() < 3) return new ArrayList<>(points);
        
        // Find bottom-most point (and leftmost in case of tie)
        Point2D pivot = points.get(0);
        for (Point2D point : points) {
            if (point.y < pivot.y || (point.y == pivot.y && point.x < pivot.x)) {
                pivot = point;
            }
        }
        
        // Sort points by polar angle with respect to pivot
        final Point2D finalPivot = pivot;
        points.sort((a, b) -> {
            double angleA = Math.atan2(a.y - finalPivot.y, a.x - finalPivot.x);
            double angleB = Math.atan2(b.y - finalPivot.y, b.x - finalPivot.x);
            
            if (Math.abs(angleA - angleB) < 1e-9) {
                // If angles are equal, sort by distance
                double distA = finalPivot.distanceSquaredTo(a);
                double distB = finalPivot.distanceSquaredTo(b);
                return Double.compare(distA, distB);
            }
            
            return Double.compare(angleA, angleB);
        });
        
        // Build convex hull using stack
        Stack<Point2D> hull = new Stack<>();
        hull.push(points.get(0));
        hull.push(points.get(1));
        
        for (int i = 2; i < points.size(); i++) {
            Point2D current = points.get(i);
            
            // Remove points that create clockwise turn
            while (hull.size() > 1 && 
                   orientation(hull.get(hull.size() - 2), hull.peek(), current) <= 0) {
                hull.pop();
            }
            
            hull.push(current);
        }
        
        return new ArrayList<>(hull);
    }
    
    // Calculate orientation of three points
    private static int orientation(Point2D p, Point2D q, Point2D r) {
        double val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y);
        
        if (Math.abs(val) < 1e-9) return 0;  // Collinear
        return (val > 0) ? 1 : 2;  // Clockwise or Counterclockwise
    }
    
    // Time Complexity: O(n log n)
    // Space Complexity: O(n)
}
```

### Jarvis March (Gift Wrapping) Algorithm

```java
public class JarvisMarch {
    public static List<Point2D> convexHull(List<Point2D> points) {
        if (points.size() < 3) return new ArrayList<>(points);
        
        List<Point2D> hull = new ArrayList<>();
        
        // Find leftmost point
        int leftmost = 0;
        for (int i = 1; i < points.size(); i++) {
            if (points.get(i).x < points.get(leftmost).x) {
                leftmost = i;
            }
        }
        
        int p = leftmost, q;
        do {
            hull.add(points.get(p));
            q = (p + 1) % points.size();
            
            for (int i = 0; i < points.size(); i++) {
                if (orientation(points.get(p), points.get(i), points.get(q)) == 2) {
                    q = i;
                }
            }
            
            p = q;
        } while (p != leftmost);
        
        return hull;
    }
    
    private static int orientation(Point2D p, Point2D q, Point2D r) {
        double val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y);
        
        if (Math.abs(val) < 1e-9) return 0;
        return (val > 0) ? 1 : 2;
    }
    
    // Time Complexity: O(n * h) where h is number of hull points
    // Space Complexity: O(h)
}
```

## 15.3 Line Intersection

Finding intersections between lines and line segments.

### Line-Line Intersection

```java
public class LineIntersection {
    public static Point2D lineIntersection(Line2D line1, Line2D line2) {
        Point2D p1 = line1.p1, p2 = line1.p2;
        Point2D p3 = line2.p1, p4 = line2.p2;
        
        double denom = (p1.x - p2.x) * (p3.y - p4.y) - (p1.y - p2.y) * (p3.x - p4.x);
        
        if (Math.abs(denom) < 1e-9) {
            return null; // Lines are parallel
        }
        
        double t = ((p1.x - p3.x) * (p3.y - p4.y) - (p1.y - p3.y) * (p3.x - p4.x)) / denom;
        
        double x = p1.x + t * (p2.x - p1.x);
        double y = p1.y + t * (p2.y - p1.y);
        
        return new Point2D(x, y);
    }
    
    // Check if two line segments intersect
    public static boolean segmentsIntersect(Line2D seg1, Line2D seg2) {
        Point2D p1 = seg1.p1, p2 = seg1.p2;
        Point2D p3 = seg2.p1, p4 = seg2.p2;
        
        // Check if any endpoint is on the other segment
        if (seg1.containsPointOnSegment(p3) || seg1.containsPointOnSegment(p4) ||
            seg2.containsPointOnSegment(p1) || seg2.containsPointOnSegment(p2)) {
            return true;
        }
        
        // Check if segments cross each other
        int o1 = orientation(p1, p2, p3);
        int o2 = orientation(p1, p2, p4);
        int o3 = orientation(p3, p4, p1);
        int o4 = orientation(p3, p4, p2);
        
        return o1 != o2 && o3 != o4;
    }
    
    private static int orientation(Point2D p, Point2D q, Point2D r) {
        double val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y);
        
        if (Math.abs(val) < 1e-9) return 0;
        return (val > 0) ? 1 : 2;
    }
}
```

### Ray Casting Algorithm

```java
public class RayCasting {
    // Check if point is inside polygon using ray casting
    public static boolean pointInPolygon(Point2D point, List<Point2D> polygon) {
        int n = polygon.size();
        boolean inside = false;
        
        for (int i = 0, j = n - 1; i < n; j = i++) {
            Point2D pi = polygon.get(i);
            Point2D pj = polygon.get(j);
            
            if (((pi.y > point.y) != (pj.y > point.y)) &&
                (point.x < (pj.x - pi.x) * (point.y - pi.y) / (pj.y - pi.y) + pi.x)) {
                inside = !inside;
            }
        }
        
        return inside;
    }
    
    // Count intersections with horizontal ray
    public static int countRayIntersections(Point2D point, List<Point2D> polygon) {
        int count = 0;
        int n = polygon.size();
        
        for (int i = 0; i < n; i++) {
            Point2D p1 = polygon.get(i);
            Point2D p2 = polygon.get((i + 1) % n);
            
            if (rayIntersectsSegment(point, p1, p2)) {
                count++;
            }
        }
        
        return count;
    }
    
    private static boolean rayIntersectsSegment(Point2D point, Point2D p1, Point2D p2) {
        if (p1.y > p2.y) {
            Point2D temp = p1;
            p1 = p2;
            p2 = temp;
        }
        
        if (point.y < p1.y || point.y >= p2.y) return false;
        if (p1.y == p2.y) return false;
        
        double x = p1.x + (point.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y);
        return point.x < x;
    }
}
```

## 15.4 Closest Pair of Points

Finding the two closest points in a set of points.

### Divide and Conquer Approach

```java
public class ClosestPair {
    public static double closestPairDistance(List<Point2D> points) {
        if (points.size() < 2) return Double.MAX_VALUE;
        
        // Sort points by x-coordinate
        List<Point2D> sortedPoints = new ArrayList<>(points);
        sortedPoints.sort((a, b) -> Double.compare(a.x, b.x));
        
        return closestPairRecursive(sortedPoints, 0, sortedPoints.size() - 1);
    }
    
    private static double closestPairRecursive(List<Point2D> points, int left, int right) {
        if (right - left + 1 <= 3) {
            return bruteForceClosest(points, left, right);
        }
        
        int mid = (left + right) / 2;
        Point2D midPoint = points.get(mid);
        
        // Find closest pair in left and right halves
        double leftMin = closestPairRecursive(points, left, mid);
        double rightMin = closestPairRecursive(points, mid + 1, right);
        
        double minDistance = Math.min(leftMin, rightMin);
        
        // Find closest pair across the dividing line
        return Math.min(minDistance, closestAcrossLine(points, left, right, mid, minDistance));
    }
    
    private static double bruteForceClosest(List<Point2D> points, int left, int right) {
        double minDistance = Double.MAX_VALUE;
        
        for (int i = left; i <= right; i++) {
            for (int j = i + 1; j <= right; j++) {
                double distance = points.get(i).distanceTo(points.get(j));
                minDistance = Math.min(minDistance, distance);
            }
        }
        
        return minDistance;
    }
    
    private static double closestAcrossLine(List<Point2D> points, int left, int right, int mid, double minDistance) {
        Point2D midPoint = points.get(mid);
        
        // Create strip of points close to dividing line
        List<Point2D> strip = new ArrayList<>();
        for (int i = left; i <= right; i++) {
            if (Math.abs(points.get(i).x - midPoint.x) < minDistance) {
                strip.add(points.get(i));
            }
        }
        
        // Sort strip by y-coordinate
        strip.sort((a, b) -> Double.compare(a.y, b.y));
        
        // Find closest points in strip
        double minStripDistance = minDistance;
        for (int i = 0; i < strip.size(); i++) {
            for (int j = i + 1; j < strip.size() && (strip.get(j).y - strip.get(i).y) < minDistance; j++) {
                double distance = strip.get(i).distanceTo(strip.get(j));
                minStripDistance = Math.min(minStripDistance, distance);
            }
        }
        
        return minStripDistance;
    }
    
    // Time Complexity: O(n log n)
    // Space Complexity: O(n)
}
```

## 15.5 Polygon Triangulation

Breaking a polygon into triangles.

### Ear Clipping Algorithm

```java
public class PolygonTriangulation {
    public static List<Triangle> triangulatePolygon(List<Point2D> polygon) {
        List<Triangle> triangles = new ArrayList<>();
        List<Point2D> vertices = new ArrayList<>(polygon);
        
        while (vertices.size() > 3) {
            boolean earFound = false;
            
            for (int i = 0; i < vertices.size(); i++) {
                if (isEar(vertices, i)) {
                    // Create triangle from ear
                    Point2D prev = vertices.get((i - 1 + vertices.size()) % vertices.size());
                    Point2D current = vertices.get(i);
                    Point2D next = vertices.get((i + 1) % vertices.size());
                    
                    triangles.add(new Triangle(prev, current, next));
                    
                    // Remove ear vertex
                    vertices.remove(i);
                    earFound = true;
                    break;
                }
            }
            
            if (!earFound) {
                throw new IllegalArgumentException("Polygon cannot be triangulated");
            }
        }
        
        // Add final triangle
        if (vertices.size() == 3) {
            triangles.add(new Triangle(vertices.get(0), vertices.get(1), vertices.get(2)));
        }
        
        return triangles;
    }
    
    private static boolean isEar(List<Point2D> vertices, int index) {
        int n = vertices.size();
        Point2D prev = vertices.get((index - 1 + n) % n);
        Point2D current = vertices.get(index);
        Point2D next = vertices.get((index + 1) % n);
        
        // Check if angle is convex
        if (orientation(prev, current, next) != 2) {
            return false;
        }
        
        // Check if any other vertex is inside the triangle
        for (int i = 0; i < n; i++) {
            if (i == index || i == (index - 1 + n) % n || i == (index + 1) % n) {
                continue;
            }
            
            Point2D vertex = vertices.get(i);
            if (pointInTriangle(vertex, prev, current, next)) {
                return false;
            }
        }
        
        return true;
    }
    
    private static boolean pointInTriangle(Point2D point, Point2D a, Point2D b, Point2D c) {
        double denom = (b.y - c.y) * (a.x - c.x) + (c.x - b.x) * (a.y - c.y);
        double alpha = ((b.y - c.y) * (point.x - c.x) + (c.x - b.x) * (point.y - c.y)) / denom;
        double beta = ((c.y - a.y) * (point.x - c.x) + (a.x - c.x) * (point.y - c.y)) / denom;
        double gamma = 1 - alpha - beta;
        
        return alpha >= 0 && beta >= 0 && gamma >= 0;
    }
    
    private static int orientation(Point2D p, Point2D q, Point2D r) {
        double val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y);
        
        if (Math.abs(val) < 1e-9) return 0;
        return (val > 0) ? 1 : 2;
    }
    
    public static class Triangle {
        public Point2D a, b, c;
        
        public Triangle(Point2D a, Point2D b, Point2D c) {
            this.a = a;
            this.b = b;
            this.c = c;
        }
        
        public double area() {
            return Math.abs((a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)) / 2.0);
        }
    }
}
```

## 15.6 Voronoi Diagrams

A Voronoi diagram partitions the plane into regions based on distance to a set of points.

### Fortune's Algorithm (Simplified)

```java
public class VoronoiDiagram {
    public static class VoronoiCell {
        public Point2D site;
        public List<Point2D> vertices;
        
        public VoronoiCell(Point2D site) {
            this.site = site;
            this.vertices = new ArrayList<>();
        }
    }
    
    public static List<VoronoiCell> computeVoronoi(List<Point2D> sites) {
        List<VoronoiCell> cells = new ArrayList<>();
        
        for (Point2D site : sites) {
            cells.add(new VoronoiCell(site));
        }
        
        // Simplified implementation - in practice, use Fortune's algorithm
        for (VoronoiCell cell : cells) {
            computeCellVertices(cell, sites);
        }
        
        return cells;
    }
    
    private static void computeCellVertices(VoronoiCell cell, List<Point2D> allSites) {
        List<Point2D> vertices = new ArrayList<>();
        
        for (Point2D other : allSites) {
            if (other.equals(cell.site)) continue;
            
            // Find perpendicular bisector
            Point2D midpoint = new Point2D(
                (cell.site.x + other.x) / 2,
                (cell.site.y + other.y) / 2
            );
            
            // Calculate direction vector
            Point2D direction = new Point2D(
                -(other.y - cell.site.y),
                other.x - cell.site.x
            );
            
            // Normalize direction
            double length = Math.sqrt(direction.x * direction.x + direction.y * direction.y);
            if (length > 0) {
                direction.x /= length;
                direction.y /= length;
            }
            
            // Add vertices along the bisector
            for (double t = -100; t <= 100; t += 10) {
                Point2D vertex = new Point2D(
                    midpoint.x + t * direction.x,
                    midpoint.y + t * direction.y
                );
                vertices.add(vertex);
            }
        }
        
        cell.vertices = vertices;
    }
}
```

## 15.7 Delaunay Triangulation

A Delaunay triangulation maximizes the minimum angle of all triangles.

### Bowyer-Watson Algorithm

```java
public class DelaunayTriangulation {
    public static class Triangle {
        public Point2D a, b, c;
        public Point2D circumcenter;
        public double circumradius;
        
        public Triangle(Point2D a, Point2D b, Point2D c) {
            this.a = a;
            this.b = b;
            this.c = c;
            computeCircumcircle();
        }
        
        private void computeCircumcircle() {
            double ax = a.x, ay = a.y;
            double bx = b.x, by = b.y;
            double cx = c.x, cy = c.y;
            
            double d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by));
            
            if (Math.abs(d) < 1e-9) {
                // Degenerate triangle
                circumcenter = new Point2D(0, 0);
                circumradius = Double.MAX_VALUE;
                return;
            }
            
            double ux = ((ax * ax + ay * ay) * (by - cy) + 
                        (bx * bx + by * by) * (cy - ay) + 
                        (cx * cx + cy * cy) * (ay - by)) / d;
            
            double uy = ((ax * ax + ay * ay) * (cx - bx) + 
                        (bx * bx + by * by) * (ax - cx) + 
                        (cx * cx + cy * cy) * (bx - ax)) / d;
            
            circumcenter = new Point2D(ux, uy);
            circumradius = circumcenter.distanceTo(a);
        }
        
        public boolean containsPoint(Point2D point) {
            return circumcenter.distanceTo(point) <= circumradius + 1e-9;
        }
    }
    
    public static List<Triangle> triangulate(List<Point2D> points) {
        if (points.size() < 3) return new ArrayList<>();
        
        // Create super triangle that contains all points
        double minX = points.stream().mapToDouble(p -> p.x).min().orElse(0) - 1;
        double maxX = points.stream().mapToDouble(p -> p.x).max().orElse(0) + 1;
        double minY = points.stream().mapToDouble(p -> p.y).min().orElse(0) - 1;
        double maxY = points.stream().mapToDouble(p -> p.y).max().orElse(0) + 1;
        
        double width = maxX - minX;
        double height = maxY - minY;
        double size = Math.max(width, height) * 2;
        
        Point2D p1 = new Point2D(minX + width / 2, minY + height / 2 + size);
        Point2D p2 = new Point2D(minX + width / 2 - size, minY + height / 2 - size);
        Point2D p3 = new Point2D(minX + width / 2 + size, minY + height / 2 - size);
        
        List<Triangle> triangles = new ArrayList<>();
        triangles.add(new Triangle(p1, p2, p3));
        
        // Add each point
        for (Point2D point : points) {
            List<Triangle> badTriangles = new ArrayList<>();
            
            // Find all triangles whose circumcircle contains the point
            for (Triangle triangle : triangles) {
                if (triangle.containsPoint(point)) {
                    badTriangles.add(triangle);
                }
            }
            
            // Find the boundary of the polygonal hole
            List<Edge> polygon = new ArrayList<>();
            for (Triangle triangle : badTriangles) {
                Edge[] edges = {
                    new Edge(triangle.a, triangle.b),
                    new Edge(triangle.b, triangle.c),
                    new Edge(triangle.c, triangle.a)
                };
                
                for (Edge edge : edges) {
                    boolean shared = false;
                    for (Triangle other : badTriangles) {
                        if (other == triangle) continue;
                        if (other.hasEdge(edge)) {
                            shared = true;
                            break;
                        }
                    }
                    if (!shared) {
                        polygon.add(edge);
                    }
                }
            }
            
            // Remove bad triangles
            triangles.removeAll(badTriangles);
            
            // Create new triangles from the polygon
            for (Edge edge : polygon) {
                triangles.add(new Triangle(edge.p1, edge.p2, point));
            }
        }
        
        // Remove triangles that contain super triangle vertices
        triangles.removeIf(triangle -> 
            triangle.a == p1 || triangle.a == p2 || triangle.a == p3 ||
            triangle.b == p1 || triangle.b == p2 || triangle.b == p3 ||
            triangle.c == p1 || triangle.c == p2 || triangle.c == p3);
        
        return triangles;
    }
    
    private static class Edge {
        public Point2D p1, p2;
        
        public Edge(Point2D p1, Point2D p2) {
            this.p1 = p1;
            this.p2 = p2;
        }
        
        @Override
        public boolean equals(Object obj) {
            if (!(obj instanceof Edge)) return false;
            Edge other = (Edge) obj;
            return (p1.equals(other.p1) && p2.equals(other.p2)) ||
                   (p1.equals(other.p2) && p2.equals(other.p1));
        }
        
        @Override
        public int hashCode() {
            return p1.hashCode() + p2.hashCode();
        }
    }
}
```

## 15.8 Range Queries & Spatial Data Structures

### KD-Tree for 2D Range Queries

```java
public class KDTree {
    private static class Node {
        Point2D point;
        Node left, right;
        boolean isVertical;
        
        public Node(Point2D point, boolean isVertical) {
            this.point = point;
            this.isVertical = isVertical;
        }
    }
    
    private Node root;
    
    public KDTree(List<Point2D> points) {
        root = buildTree(points, true);
    }
    
    private Node buildTree(List<Point2D> points, boolean isVertical) {
        if (points.isEmpty()) return null;
        
        // Sort points by x or y coordinate
        if (isVertical) {
            points.sort((a, b) -> Double.compare(a.x, b.x));
        } else {
            points.sort((a, b) -> Double.compare(a.y, b.y));
        }
        
        int median = points.size() / 2;
        Node node = new Node(points.get(median), isVertical);
        
        // Recursively build left and right subtrees
        node.left = buildTree(new ArrayList<>(points.subList(0, median)), !isVertical);
        node.right = buildTree(new ArrayList<>(points.subList(median + 1, points.size())), !isVertical);
        
        return node;
    }
    
    public List<Point2D> rangeQuery(double xMin, double yMin, double xMax, double yMax) {
        List<Point2D> result = new ArrayList<>();
        rangeQuery(root, xMin, yMin, xMax, yMax, result);
        return result;
    }
    
    private void rangeQuery(Node node, double xMin, double yMin, double xMax, double yMax, List<Point2D> result) {
        if (node == null) return;
        
        Point2D point = node.point;
        
        // Check if point is in range
        if (point.x >= xMin && point.x <= xMax && point.y >= yMin && point.y <= yMax) {
            result.add(point);
        }
        
        // Recursively search subtrees
        if (node.isVertical) {
            if (xMin <= point.x) {
                rangeQuery(node.left, xMin, yMin, xMax, yMax, result);
            }
            if (xMax >= point.x) {
                rangeQuery(node.right, xMin, yMin, xMax, yMax, result);
            }
        } else {
            if (yMin <= point.y) {
                rangeQuery(node.left, xMin, yMin, xMax, yMax, result);
            }
            if (yMax >= point.y) {
                rangeQuery(node.right, xMin, yMin, xMax, yMax, result);
            }
        }
    }
    
    // Time Complexity: O(log n) average case, O(n) worst case
    // Space Complexity: O(n)
}
```

### Quadtree for Spatial Partitioning

```java
public class Quadtree {
    private static class Rectangle {
        double x, y, width, height;
        
        public Rectangle(double x, double y, double width, double height) {
            this.x = x;
            this.y = y;
            this.width = width;
            this.height = height;
        }
        
        public boolean contains(Point2D point) {
            return point.x >= x && point.x <= x + width &&
                   point.y >= y && point.y <= y + height;
        }
        
        public boolean intersects(Rectangle other) {
            return !(x + width < other.x || other.x + other.width < x ||
                    y + height < other.y || other.y + other.height < y);
        }
    }
    
    private static class QuadNode {
        Rectangle bounds;
        List<Point2D> points;
        QuadNode[] children;
        boolean isLeaf;
        
        public QuadNode(Rectangle bounds) {
            this.bounds = bounds;
            this.points = new ArrayList<>();
            this.children = new QuadNode[4];
            this.isLeaf = true;
        }
        
        public void subdivide() {
            double halfWidth = bounds.width / 2;
            double halfHeight = bounds.height / 2;
            
            children[0] = new QuadNode(new Rectangle(bounds.x, bounds.y + halfHeight, halfWidth, halfHeight));
            children[1] = new QuadNode(new Rectangle(bounds.x + halfWidth, bounds.y + halfHeight, halfWidth, halfHeight));
            children[2] = new QuadNode(new Rectangle(bounds.x, bounds.y, halfWidth, halfHeight));
            children[3] = new QuadNode(new Rectangle(bounds.x + halfWidth, bounds.y, halfWidth, halfHeight));
            
            isLeaf = false;
        }
    }
    
    private QuadNode root;
    private int maxPointsPerNode;
    
    public Quadtree(Rectangle bounds, int maxPointsPerNode) {
        this.root = new QuadNode(bounds);
        this.maxPointsPerNode = maxPointsPerNode;
    }
    
    public void insert(Point2D point) {
        insert(root, point);
    }
    
    private void insert(QuadNode node, Point2D point) {
        if (!node.bounds.contains(point)) return;
        
        if (node.isLeaf) {
            node.points.add(point);
            
            if (node.points.size() > maxPointsPerNode) {
                node.subdivide();
                
                // Redistribute points to children
                for (Point2D p : node.points) {
                    for (QuadNode child : node.children) {
                        if (child.bounds.contains(p)) {
                            insert(child, p);
                            break;
                        }
                    }
                }
                
                node.points.clear();
            }
        } else {
            // Insert into appropriate child
            for (QuadNode child : node.children) {
                if (child.bounds.contains(point)) {
                    insert(child, point);
                    break;
                }
            }
        }
    }
    
    public List<Point2D> query(Rectangle range) {
        List<Point2D> result = new ArrayList<>();
        query(root, range, result);
        return result;
    }
    
    private void query(QuadNode node, Rectangle range, List<Point2D> result) {
        if (node == null || !node.bounds.intersects(range)) return;
        
        if (node.isLeaf) {
            for (Point2D point : node.points) {
                if (range.contains(point)) {
                    result.add(point);
                }
            }
        } else {
            for (QuadNode child : node.children) {
                query(child, range, result);
            }
        }
    }
}
```

**Real-world Analogies:**
- **Computational Geometry:** Like being a digital architect designing buildings and cities
- **Convex Hull:** Like finding the smallest rubber band that can wrap around all the nails on a board
- **Line Intersection:** Like finding where two roads cross on a map
- **Closest Pair:** Like finding the two closest cities on a map
- **Polygon Triangulation:** Like cutting a pizza into triangular slices
- **Voronoi Diagrams:** Like dividing a city into districts where each district contains the closest fire station
- **Delaunay Triangulation:** Like creating the most "balanced" triangular mesh for a surface
- **Range Queries:** Like finding all restaurants within a certain distance of your location
- **Spatial Data Structures:** Like organizing a library where books are arranged by location rather than alphabetically

Computational geometry algorithms are essential for computer graphics, geographic information systems, robotics, and many other applications that deal with spatial data and geometric relationships.