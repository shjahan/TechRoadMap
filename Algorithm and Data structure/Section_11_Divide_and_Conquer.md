# Section 11 – Divide and Conquer

## 11.1 Divide and Conquer Strategy

Divide and Conquer is a fundamental algorithmic paradigm that breaks down a problem into smaller, more manageable subproblems, solves them recursively, and then combines their solutions to solve the original problem.

### Core Principles

The Divide and Conquer strategy follows three main steps:

1. **Divide**: Break the problem into smaller, similar subproblems
2. **Conquer**: Solve the subproblems recursively
3. **Combine**: Merge the solutions of subproblems to solve the original problem

**Real-world Analogy:**
Think of organizing a large library. Instead of trying to organize all books at once, you:
- **Divide**: Split books by category (fiction, non-fiction, science, etc.)
- **Conquer**: Organize each category separately (alphabetically within each category)
- **Combine**: Put all organized categories together to form a complete organized library

### Basic Template

```java
public class DivideAndConquer {
    public Result divideAndConquer(Problem problem) {
        // Base case: problem is small enough to solve directly
        if (isBaseCase(problem)) {
            return solveDirectly(problem);
        }
        
        // Divide: break problem into smaller subproblems
        Problem[] subproblems = divide(problem);
        
        // Conquer: solve subproblems recursively
        Result[] subResults = new Result[subproblems.length];
        for (int i = 0; i < subproblems.length; i++) {
            subResults[i] = divideAndConquer(subproblems[i]);
        }
        
        // Combine: merge solutions
        return combine(subResults);
    }
    
    private boolean isBaseCase(Problem problem) {
        // Define when problem is small enough
        return problem.size() <= 1;
    }
    
    private Problem[] divide(Problem problem) {
        // Split problem into smaller parts
        return problem.split();
    }
    
    private Result solveDirectly(Problem problem) {
        // Solve small problems directly
        return new Result(problem.solve());
    }
    
    private Result combine(Result[] subResults) {
        // Merge subproblem solutions
        return Result.merge(subResults);
    }
}
```

### When to Use Divide and Conquer

**Advantages:**
- Often leads to efficient algorithms
- Natural for recursive problems
- Can be parallelized easily
- Reduces problem complexity

**Disadvantages:**
- Overhead of recursion
- May not be optimal for small problems
- Memory usage due to recursion stack

**Best Use Cases:**
- Problems that can be naturally divided
- When subproblems are independent
- When combining solutions is straightforward

## 11.2 Merge Sort Implementation

Merge Sort is a classic example of the Divide and Conquer paradigm, providing O(n log n) time complexity.

### Basic Merge Sort

```java
public class MergeSort {
    public static void mergeSort(int[] arr) {
        if (arr.length <= 1) {
            return; // Base case: array is already sorted
        }
        
        // Divide: split array into two halves
        int mid = arr.length / 2;
        int[] left = Arrays.copyOfRange(arr, 0, mid);
        int[] right = Arrays.copyOfRange(arr, mid, arr.length);
        
        // Conquer: recursively sort both halves
        mergeSort(left);
        mergeSort(right);
        
        // Combine: merge the sorted halves
        merge(arr, left, right);
    }
    
    private static void merge(int[] arr, int[] left, int[] right) {
        int i = 0, j = 0, k = 0;
        
        // Merge elements from both arrays in sorted order
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                arr[k++] = left[i++];
            } else {
                arr[k++] = right[j++];
            }
        }
        
        // Copy remaining elements from left array
        while (i < left.length) {
            arr[k++] = left[i++];
        }
        
        // Copy remaining elements from right array
        while (j < right.length) {
            arr[k++] = right[j++];
        }
    }
}
```

### In-Place Merge Sort (Space Optimized)

```java
public class InPlaceMergeSort {
    public static void mergeSort(int[] arr) {
        mergeSort(arr, 0, arr.length - 1);
    }
    
    private static void mergeSort(int[] arr, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            
            // Divide: sort left and right halves
            mergeSort(arr, left, mid);
            mergeSort(arr, mid + 1, right);
            
            // Combine: merge the sorted halves
            merge(arr, left, mid, right);
        }
    }
    
    private static void merge(int[] arr, int left, int mid, int right) {
        int[] temp = new int[right - left + 1];
        int i = left, j = mid + 1, k = 0;
        
        // Merge elements in sorted order
        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) {
                temp[k++] = arr[i++];
            } else {
                temp[k++] = arr[j++];
            }
        }
        
        // Copy remaining elements
        while (i <= mid) temp[k++] = arr[i++];
        while (j <= right) temp[k++] = arr[j++];
        
        // Copy back to original array
        for (i = 0; i < temp.length; i++) {
            arr[left + i] = temp[i];
        }
    }
}
```

### Performance Analysis

**Time Complexity:**
- **Best Case:** O(n log n)
- **Average Case:** O(n log n)
- **Worst Case:** O(n log n)

**Space Complexity:** O(n) for auxiliary array

**Stability:** Stable (maintains relative order of equal elements)

## 11.3 Quick Sort Implementation

Quick Sort is another Divide and Conquer algorithm that uses partitioning instead of merging.

### Basic Quick Sort

```java
public class QuickSort {
    public static void quickSort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }
    
    private static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            // Divide: partition array around pivot
            int pivotIndex = partition(arr, low, high);
            
            // Conquer: recursively sort elements before and after partition
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    private static int partition(int[] arr, int low, int high) {
        // Choose rightmost element as pivot
        int pivot = arr[high];
        int i = low - 1; // Index of smaller element
        
        for (int j = low; j < high; j++) {
            // If current element is smaller than or equal to pivot
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        
        // Place pivot in correct position
        swap(arr, i + 1, high);
        return i + 1;
    }
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

### Optimized Quick Sort

```java
public class OptimizedQuickSort {
    private static final int INSERTION_SORT_THRESHOLD = 10;
    
    public static void quickSort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }
    
    private static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            // Use insertion sort for small arrays
            if (high - low + 1 < INSERTION_SORT_THRESHOLD) {
                insertionSort(arr, low, high);
                return;
            }
            
            // Choose pivot using median-of-three
            int pivotIndex = choosePivot(arr, low, high);
            swap(arr, pivotIndex, high);
            
            int partitionIndex = partition(arr, low, high);
            
            quickSort(arr, low, partitionIndex - 1);
            quickSort(arr, partitionIndex + 1, high);
        }
    }
    
    private static int choosePivot(int[] arr, int low, int high) {
        int mid = low + (high - low) / 2;
        
        // Return median of first, middle, and last elements
        if (arr[low] <= arr[mid] && arr[mid] <= arr[high]) return mid;
        if (arr[mid] <= arr[low] && arr[low] <= arr[high]) return low;
        return high;
    }
    
    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        
        swap(arr, i + 1, high);
        return i + 1;
    }
    
    private static void insertionSort(int[] arr, int low, int high) {
        for (int i = low + 1; i <= high; i++) {
            int key = arr[i];
            int j = i - 1;
            
            while (j >= low && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

### Performance Analysis

**Time Complexity:**
- **Best Case:** O(n log n) - when pivot divides array evenly
- **Average Case:** O(n log n)
- **Worst Case:** O(n²) - when pivot is always smallest or largest element

**Space Complexity:** O(log n) for recursion stack

**Stability:** Not stable

## 11.4 Binary Search Variations

Binary search is a classic Divide and Conquer algorithm for searching in sorted arrays.

### Standard Binary Search

```java
public class BinarySearch {
    public static int binarySearch(int[] arr, int target) {
        return binarySearch(arr, target, 0, arr.length - 1);
    }
    
    private static int binarySearch(int[] arr, int target, int left, int right) {
        if (left > right) {
            return -1; // Element not found
        }
        
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) {
            return mid; // Found target
        } else if (arr[mid] > target) {
            // Search left half
            return binarySearch(arr, target, left, mid - 1);
        } else {
            // Search right half
            return binarySearch(arr, target, mid + 1, right);
        }
    }
}
```

### First Occurrence Binary Search

```java
public class FirstOccurrenceBinarySearch {
    public static int findFirstOccurrence(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                result = mid;
                right = mid - 1; // Continue searching in left half
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
}
```

### Last Occurrence Binary Search

```java
public class LastOccurrenceBinarySearch {
    public static int findLastOccurrence(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                result = mid;
                left = mid + 1; // Continue searching in right half
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
}
```

### Count Occurrences

```java
public class CountOccurrences {
    public static int countOccurrences(int[] arr, int target) {
        int first = findFirstOccurrence(arr, target);
        if (first == -1) {
            return 0; // Target not found
        }
        
        int last = findLastOccurrence(arr, target);
        return last - first + 1;
    }
    
    private static int findFirstOccurrence(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                result = mid;
                right = mid - 1;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
    
    private static int findLastOccurrence(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                result = mid;
                left = mid + 1;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
}
```

## 11.5 Closest Pair of Points

The closest pair of points problem finds the two points in a set that are closest to each other.

### Brute Force Approach

```java
public class ClosestPairBruteForce {
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
    
    public static double findClosestPair(Point[] points) {
        double minDistance = Double.MAX_VALUE;
        
        for (int i = 0; i < points.length; i++) {
            for (int j = i + 1; j < points.length; j++) {
                double distance = points[i].distanceTo(points[j]);
                minDistance = Math.min(minDistance, distance);
            }
        }
        
        return minDistance;
    }
}
```

### Divide and Conquer Approach

```java
public class ClosestPairDivideConquer {
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
    
    public static double findClosestPair(Point[] points) {
        // Sort points by x-coordinate
        Arrays.sort(points, (a, b) -> Double.compare(a.x, b.x));
        return closestPairRecursive(points, 0, points.length - 1);
    }
    
    private static double closestPairRecursive(Point[] points, int left, int right) {
        // Base case: if there are 2 or 3 points, use brute force
        if (right - left + 1 <= 3) {
            return bruteForceClosest(points, left, right);
        }
        
        // Divide: find middle point
        int mid = left + (right - left) / 2;
        Point midPoint = points[mid];
        
        // Conquer: find closest pair in left and right halves
        double leftMin = closestPairRecursive(points, left, mid);
        double rightMin = closestPairRecursive(points, mid + 1, right);
        
        // Find minimum of two halves
        double minDistance = Math.min(leftMin, rightMin);
        
        // Combine: check for closer pairs across the dividing line
        return Math.min(minDistance, closestAcrossLine(points, left, right, mid, minDistance));
    }
    
    private static double bruteForceClosest(Point[] points, int left, int right) {
        double minDistance = Double.MAX_VALUE;
        
        for (int i = left; i <= right; i++) {
            for (int j = i + 1; j <= right; j++) {
                minDistance = Math.min(minDistance, points[i].distanceTo(points[j]));
            }
        }
        
        return minDistance;
    }
    
    private static double closestAcrossLine(Point[] points, int left, int right, int mid, double minDistance) {
        // Create array of points close to the dividing line
        List<Point> strip = new ArrayList<>();
        
        for (int i = left; i <= right; i++) {
            if (Math.abs(points[i].x - points[mid].x) < minDistance) {
                strip.add(points[i]);
            }
        }
        
        // Sort strip by y-coordinate
        strip.sort((a, b) -> Double.compare(a.y, b.y));
        
        // Find closest points in strip
        double minStripDistance = minDistance;
        for (int i = 0; i < strip.size(); i++) {
            for (int j = i + 1; j < strip.size() && (strip.get(j).y - strip.get(i).y) < minDistance; j++) {
                minStripDistance = Math.min(minStripDistance, strip.get(i).distanceTo(strip.get(j)));
            }
        }
        
        return minStripDistance;
    }
}
```

## 11.6 Strassen's Matrix Multiplication

Strassen's algorithm reduces the time complexity of matrix multiplication from O(n³) to O(n^log₂7) ≈ O(n^2.81).

### Standard Matrix Multiplication

```java
public class StandardMatrixMultiplication {
    public static int[][] multiply(int[][] A, int[][] B) {
        int n = A.length;
        int[][] C = new int[n][n];
        
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        
        return C;
    }
}
```

### Strassen's Algorithm

```java
public class StrassenMatrixMultiplication {
    public static int[][] multiply(int[][] A, int[][] B) {
        int n = A.length;
        
        // Base case: if matrix is small, use standard multiplication
        if (n <= 2) {
            return standardMultiply(A, B);
        }
        
        // Ensure matrix size is power of 2
        int newSize = nextPowerOfTwo(n);
        int[][] paddedA = padMatrix(A, newSize);
        int[][] paddedB = padMatrix(B, newSize);
        
        int[][] result = strassenMultiply(paddedA, paddedB);
        
        // Extract original size result
        return extractMatrix(result, 0, 0, n, n);
    }
    
    private static int[][] strassenMultiply(int[][] A, int[][] B) {
        int n = A.length;
        
        if (n <= 2) {
            return standardMultiply(A, B);
        }
        
        int half = n / 2;
        
        // Divide matrices into quarters
        int[][] A11 = extractMatrix(A, 0, 0, half, half);
        int[][] A12 = extractMatrix(A, 0, half, half, half);
        int[][] A21 = extractMatrix(A, half, 0, half, half);
        int[][] A22 = extractMatrix(A, half, half, half, half);
        
        int[][] B11 = extractMatrix(B, 0, 0, half, half);
        int[][] B12 = extractMatrix(B, 0, half, half, half);
        int[][] B21 = extractMatrix(B, half, 0, half, half);
        int[][] B22 = extractMatrix(B, half, half, half, half);
        
        // Calculate Strassen's formulas
        int[][] P1 = strassenMultiply(add(A11, A22), add(B11, B22));
        int[][] P2 = strassenMultiply(add(A21, A22), B11);
        int[][] P3 = strassenMultiply(A11, subtract(B12, B22));
        int[][] P4 = strassenMultiply(A22, subtract(B21, B11));
        int[][] P5 = strassenMultiply(add(A11, A12), B22);
        int[][] P6 = strassenMultiply(subtract(A21, A11), add(B11, B12));
        int[][] P7 = strassenMultiply(subtract(A12, A22), add(B21, B22));
        
        // Calculate result quarters
        int[][] C11 = add(subtract(add(P1, P4), P5), P7);
        int[][] C12 = add(P3, P5);
        int[][] C21 = add(P2, P4);
        int[][] C22 = add(subtract(add(P1, P3), P2), P6);
        
        // Combine quarters into result matrix
        return combineMatrices(C11, C12, C21, C22);
    }
    
    private static int[][] standardMultiply(int[][] A, int[][] B) {
        int n = A.length;
        int[][] C = new int[n][n];
        
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        
        return C;
    }
    
    private static int nextPowerOfTwo(int n) {
        int power = 1;
        while (power < n) {
            power *= 2;
        }
        return power;
    }
    
    private static int[][] padMatrix(int[][] matrix, int newSize) {
        int[][] padded = new int[newSize][newSize];
        for (int i = 0; i < matrix.length; i++) {
            System.arraycopy(matrix[i], 0, padded[i], 0, matrix[i].length);
        }
        return padded;
    }
    
    private static int[][] extractMatrix(int[][] matrix, int startRow, int startCol, int rows, int cols) {
        int[][] result = new int[rows][cols];
        for (int i = 0; i < rows; i++) {
            System.arraycopy(matrix[startRow + i], startCol, result[i], 0, cols);
        }
        return result;
    }
    
    private static int[][] add(int[][] A, int[][] B) {
        int n = A.length;
        int[][] C = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                C[i][j] = A[i][j] + B[i][j];
            }
        }
        return C;
    }
    
    private static int[][] subtract(int[][] A, int[][] B) {
        int n = A.length;
        int[][] C = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                C[i][j] = A[i][j] - B[i][j];
            }
        }
        return C;
    }
    
    private static int[][] combineMatrices(int[][] C11, int[][] C12, int[][] C21, int[][] C22) {
        int n = C11.length * 2;
        int[][] C = new int[n][n];
        int half = C11.length;
        
        // Copy quarters into result matrix
        for (int i = 0; i < half; i++) {
            System.arraycopy(C11[i], 0, C[i], 0, half);
            System.arraycopy(C12[i], 0, C[i], half, half);
            System.arraycopy(C21[i], 0, C[half + i], 0, half);
            System.arraycopy(C22[i], 0, C[half + i], half, half);
        }
        
        return C;
    }
}
```

## 11.7 Master Theorem & Recurrence Relations

The Master Theorem provides a way to solve recurrence relations that arise in Divide and Conquer algorithms.

### Master Theorem

For a recurrence relation of the form:
T(n) = aT(n/b) + f(n)

Where:
- a ≥ 1, b > 1
- f(n) is asymptotically positive

The solution depends on comparing f(n) with n^(log_b(a)):

```java
public class MasterTheorem {
    public static String solveRecurrence(int a, int b, String f_n) {
        double log_b_a = Math.log(a) / Math.log(b);
        
        if (f_n.equals("n^k") && k < log_b_a) {
            return "T(n) = Θ(n^" + log_b_a + ")";
        } else if (f_n.equals("n^k") && k == log_b_a) {
            return "T(n) = Θ(n^" + k + " * log n)";
        } else if (f_n.equals("n^k") && k > log_b_a) {
            return "T(n) = Θ(n^" + k + ")";
        }
        
        return "Master theorem doesn't apply";
    }
    
    // Examples of common recurrences
    public static void demonstrateMasterTheorem() {
        // Merge Sort: T(n) = 2T(n/2) + O(n)
        // a=2, b=2, f(n)=n
        // log_2(2) = 1, f(n) = n^1
        // Since 1 = 1, T(n) = Θ(n log n)
        
        // Binary Search: T(n) = T(n/2) + O(1)
        // a=1, b=2, f(n)=1
        // log_2(1) = 0, f(n) = n^0
        // Since 0 = 0, T(n) = Θ(log n)
        
        // Strassen's: T(n) = 7T(n/2) + O(n^2)
        // a=7, b=2, f(n)=n^2
        // log_2(7) ≈ 2.81, f(n) = n^2
        // Since 2 < 2.81, T(n) = Θ(n^2.81)
    }
}
```

### Solving Recurrence Relations

```java
public class RecurrenceSolver {
    // Example: T(n) = 2T(n/2) + n
    public static int solveMergeSort(int n) {
        if (n <= 1) {
            return 0; // Base case
        }
        
        int leftCost = solveMergeSort(n / 2);
        int rightCost = solveMergeSort(n / 2);
        int mergeCost = n; // O(n) merge operation
        
        return leftCost + rightCost + mergeCost;
    }
    
    // Example: T(n) = T(n/2) + 1
    public static int solveBinarySearch(int n) {
        if (n <= 1) {
            return 1; // Base case
        }
        
        int searchCost = solveBinarySearch(n / 2);
        int comparisonCost = 1; // O(1) comparison
        
        return searchCost + comparisonCost;
    }
    
    // Example: T(n) = 7T(n/2) + n^2
    public static int solveStrassen(int n) {
        if (n <= 2) {
            return n * n * n; // Base case: standard multiplication
        }
        
        int recursiveCost = 7 * solveStrassen(n / 2);
        int combineCost = n * n; // O(n^2) for matrix addition/subtraction
        
        return recursiveCost + combineCost;
    }
}
```

## 11.8 Parallel Divide and Conquer

Divide and Conquer algorithms can be easily parallelized since subproblems are independent.

### Parallel Merge Sort

```java
import java.util.concurrent.*;

public class ParallelMergeSort {
    private static final int THRESHOLD = 1000; // Switch to sequential for small arrays
    
    public static void parallelMergeSort(int[] arr) {
        ForkJoinPool pool = new ForkJoinPool();
        pool.invoke(new MergeSortTask(arr, 0, arr.length - 1));
        pool.shutdown();
    }
    
    private static class MergeSortTask extends RecursiveAction {
        private int[] arr;
        private int left, right;
        
        public MergeSortTask(int[] arr, int left, int right) {
            this.arr = arr;
            this.left = left;
            this.right = right;
        }
        
        @Override
        protected void compute() {
            if (right - left < THRESHOLD) {
                // Sequential sort for small arrays
                sequentialMergeSort(arr, left, right);
            } else {
                int mid = left + (right - left) / 2;
                
                // Create tasks for left and right halves
                MergeSortTask leftTask = new MergeSortTask(arr, left, mid);
                MergeSortTask rightTask = new MergeSortTask(arr, mid + 1, right);
                
                // Fork both tasks (execute in parallel)
                leftTask.fork();
                rightTask.fork();
                
                // Wait for both tasks to complete
                leftTask.join();
                rightTask.join();
                
                // Merge the sorted halves
                merge(arr, left, mid, right);
            }
        }
    }
    
    private static void sequentialMergeSort(int[] arr, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            sequentialMergeSort(arr, left, mid);
            sequentialMergeSort(arr, mid + 1, right);
            merge(arr, left, mid, right);
        }
    }
    
    private static void merge(int[] arr, int left, int mid, int right) {
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
}
```

### Parallel Quick Sort

```java
public class ParallelQuickSort {
    private static final int THRESHOLD = 1000;
    
    public static void parallelQuickSort(int[] arr) {
        ForkJoinPool pool = new ForkJoinPool();
        pool.invoke(new QuickSortTask(arr, 0, arr.length - 1));
        pool.shutdown();
    }
    
    private static class QuickSortTask extends RecursiveAction {
        private int[] arr;
        private int left, right;
        
        public QuickSortTask(int[] arr, int left, int right) {
            this.arr = arr;
            this.left = left;
            this.right = right;
        }
        
        @Override
        protected void compute() {
            if (right - left < THRESHOLD) {
                // Sequential sort for small arrays
                sequentialQuickSort(arr, left, right);
            } else {
                int pivotIndex = partition(arr, left, right);
                
                // Create tasks for left and right partitions
                QuickSortTask leftTask = new QuickSortTask(arr, left, pivotIndex - 1);
                QuickSortTask rightTask = new QuickSortTask(arr, pivotIndex + 1, right);
                
                // Execute tasks in parallel
                leftTask.fork();
                rightTask.fork();
                
                leftTask.join();
                rightTask.join();
            }
        }
    }
    
    private static void sequentialQuickSort(int[] arr, int left, int right) {
        if (left < right) {
            int pivotIndex = partition(arr, left, right);
            sequentialQuickSort(arr, left, pivotIndex - 1);
            sequentialQuickSort(arr, pivotIndex + 1, right);
        }
    }
    
    private static int partition(int[] arr, int left, int right) {
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
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

**Real-world Analogies:**
- **Divide and Conquer:** Like organizing a large event by dividing it into smaller committees
- **Merge Sort:** Like sorting a deck of cards by dividing into two piles, sorting each, then merging
- **Quick Sort:** Like organizing a library by picking a book as reference and placing others on left/right
- **Binary Search:** Like finding a word in a dictionary by always checking the middle
- **Closest Pair:** Like finding the two closest cities on a map by dividing the map into regions
- **Strassen's Algorithm:** Like multiplying large numbers using a clever mathematical trick
- **Master Theorem:** Like a formula to predict how long a recursive process will take
- **Parallel Processing:** Like having multiple people work on different parts of the same project simultaneously

Divide and Conquer is a powerful paradigm that often leads to efficient algorithms. The key is recognizing when a problem can be naturally divided into independent subproblems and how to efficiently combine their solutions.