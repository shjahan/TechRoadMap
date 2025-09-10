# Section 1 – Fundamentals of Computer Science

## 1.1 Computational Thinking

Computational thinking is the process of breaking down complex problems into smaller, manageable parts that can be solved using computational methods. It's a fundamental skill that forms the foundation of computer science and programming.

### Core Components of Computational Thinking

#### 1. Decomposition
Breaking down complex problems into smaller, more manageable subproblems.

**Example:**
Problem: Calculate the average score of students in a class.
- Step 1: Decompose → separate input, processing, and output
- Step 2: Recognize patterns → summing numbers is always the same
- Step 3: Abstract → generalize formula for any number of students
- Step 4: Algorithm → `sum(scores) / len(scores)`

```java
public class StudentGradeCalculator {
    public static double calculateAverage(int[] scores) {
        // Decomposition: Break into steps
        // 1. Sum all scores
        int sum = 0;
        for (int score : scores) {
            sum += score;
        }
        
        // 2. Count number of scores
        int count = scores.length;
        
        // 3. Calculate average
        return (double) sum / count;
    }
    
    public static void main(String[] args) {
        int[] scores = {85, 92, 78, 96, 88};
        double average = calculateAverage(scores);
        System.out.println("Average score: " + average);
    }
}
```

#### 2. Pattern Recognition
Identifying similarities and patterns in problems to apply known solutions.

**Real-world Analogy:**
Like recognizing that cooking different dishes follows similar patterns (preparation → cooking → seasoning → serving), computational problems often follow similar patterns.

```java
// Pattern: Finding maximum element in different data structures
public class PatternRecognition {
    // Pattern 1: Find max in array
    public static int findMaxInArray(int[] arr) {
        int max = arr[0];
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        return max;
    }
    
    // Pattern 2: Find max in list
    public static int findMaxInList(List<Integer> list) {
        int max = list.get(0);
        for (int i = 1; i < list.size(); i++) {
            if (list.get(i) > max) {
                max = list.get(i);
            }
        }
        return max;
    }
    
    // Pattern 3: Find max in tree (recursive pattern)
    public static int findMaxInTree(TreeNode root) {
        if (root == null) return Integer.MIN_VALUE;
        
        int max = root.val;
        int leftMax = findMaxInTree(root.left);
        int rightMax = findMaxInTree(root.right);
        
        return Math.max(max, Math.max(leftMax, rightMax));
    }
}
```

#### 3. Abstraction
Focusing on the essential features while ignoring irrelevant details.

**Example:**
Abstracting a "Student" concept:

```java
// Abstraction: Focus on essential properties
public class Student {
    private String name;
    private int studentId;
    private double gpa;
    
    // Essential operations
    public Student(String name, int studentId) {
        this.name = name;
        this.studentId = studentId;
        this.gpa = 0.0;
    }
    
    public void updateGPA(double newGpa) {
        this.gpa = newGpa;
    }
    
    public boolean isHonorStudent() {
        return gpa >= 3.5;
    }
    
    // Ignore irrelevant details like hair color, height, etc.
}
```

#### 4. Algorithm Design
Creating step-by-step procedures to solve problems.

**Example:**
Designing an algorithm to find the shortest path:

```java
public class ShortestPathAlgorithm {
    // Algorithm: Dijkstra's shortest path
    public static int[] dijkstra(int[][] graph, int source) {
        int n = graph.length;
        int[] distances = new int[n];
        boolean[] visited = new boolean[n];
        
        // Step 1: Initialize distances
        Arrays.fill(distances, Integer.MAX_VALUE);
        distances[source] = 0;
        
        // Step 2: Find shortest path for all vertices
        for (int count = 0; count < n - 1; count++) {
            // Step 3: Pick minimum distance vertex
            int u = minDistance(distances, visited);
            visited[u] = true;
            
            // Step 4: Update distances of adjacent vertices
            for (int v = 0; v < n; v++) {
                if (!visited[v] && graph[u][v] != 0 && 
                    distances[u] != Integer.MAX_VALUE &&
                    distances[u] + graph[u][v] < distances[v]) {
                    distances[v] = distances[u] + graph[u][v];
                }
            }
        }
        
        return distances;
    }
    
    private static int minDistance(int[] distances, boolean[] visited) {
        int min = Integer.MAX_VALUE;
        int minIndex = -1;
        
        for (int v = 0; v < distances.length; v++) {
            if (!visited[v] && distances[v] <= min) {
                min = distances[v];
                minIndex = v;
            }
        }
        
        return minIndex;
    }
}
```

## 1.2 Problem-Solving Methodology

A systematic approach to solving computational problems that ensures thorough analysis and effective solutions.

### The Problem-Solving Process

#### 1. Problem Understanding
- Read the problem carefully
- Identify inputs and outputs
- Understand constraints and requirements
- Ask clarifying questions

**Example:**
Problem: "Find the two numbers in an array that sum to a target value."

```java
public class ProblemUnderstanding {
    // Step 1: Understand the problem
    // Input: Array of integers, target sum
    // Output: Indices of two numbers that sum to target
    // Constraints: Exactly one solution exists, can't use same element twice
    
    public static int[] twoSum(int[] nums, int target) {
        // Step 2: Think of approach
        // Brute force: Check all pairs O(n²)
        // Optimized: Use hash map O(n)
        
        Map<Integer, Integer> map = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            map.put(nums[i], i);
        }
        
        return new int[]{-1, -1}; // No solution found
    }
}
```

#### 2. Solution Design
- Choose appropriate data structures
- Design algorithm steps
- Consider edge cases
- Plan for optimization

**Example:**
Designing a solution for the "Two Sum" problem:

```java
public class SolutionDesign {
    // Approach 1: Brute Force O(n²)
    public static int[] twoSumBruteForce(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) {
                    return new int[]{i, j};
                }
            }
        }
        return new int[]{-1, -1};
    }
    
    // Approach 2: Hash Map O(n)
    public static int[] twoSumOptimized(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            map.put(nums[i], i);
        }
        
        return new int[]{-1, -1};
    }
}
```

#### 3. Implementation
- Write clean, readable code
- Handle edge cases
- Add comments for clarity
- Test with examples

```java
public class Implementation {
    public static int[] twoSum(int[] nums, int target) {
        // Edge case: Empty array
        if (nums == null || nums.length < 2) {
            return new int[]{-1, -1};
        }
        
        Map<Integer, Integer> map = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            
            // Check if complement exists in map
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            
            // Store current number and its index
            map.put(nums[i], i);
        }
        
        // No solution found
        return new int[]{-1, -1};
    }
    
    // Test the implementation
    public static void main(String[] args) {
        int[] nums = {2, 7, 11, 15};
        int target = 9;
        int[] result = twoSum(nums, target);
        System.out.println("Indices: " + Arrays.toString(result));
    }
}
```

#### 4. Testing and Validation
- Test with various inputs
- Verify edge cases
- Check performance
- Validate correctness

```java
public class TestingValidation {
    public static void testTwoSum() {
        // Test case 1: Normal case
        int[] nums1 = {2, 7, 11, 15};
        int target1 = 9;
        int[] result1 = twoSum(nums1, target1);
        assert Arrays.equals(result1, new int[]{0, 1}) : "Test case 1 failed";
        
        // Test case 2: Edge case - no solution
        int[] nums2 = {2, 7, 11, 15};
        int target2 = 10;
        int[] result2 = twoSum(nums2, target2);
        assert Arrays.equals(result2, new int[]{-1, -1}) : "Test case 2 failed";
        
        // Test case 3: Edge case - empty array
        int[] nums3 = {};
        int target3 = 0;
        int[] result3 = twoSum(nums3, target3);
        assert Arrays.equals(result3, new int[]{-1, -1}) : "Test case 3 failed";
        
        System.out.println("All tests passed!");
    }
}
```

## 1.3 Algorithm Design Principles

Fundamental principles that guide the creation of efficient and correct algorithms.

### Key Design Principles

#### 1. Correctness
The algorithm must produce the correct output for all valid inputs.

**Example:**
Correct implementation of binary search:

```java
public class CorrectnessExample {
    public static int binarySearch(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2; // Avoid overflow
            
            if (arr[mid] == target) {
                return mid; // Found target
            } else if (arr[mid] < target) {
                left = mid + 1; // Search right half
            } else {
                right = mid - 1; // Search left half
            }
        }
        
        return -1; // Target not found
    }
    
    // Verification: Test with various inputs
    public static void verifyCorrectness() {
        int[] arr = {1, 3, 5, 7, 9, 11, 13, 15};
        
        // Test cases
        assert binarySearch(arr, 7) == 3 : "Should find 7 at index 3";
        assert binarySearch(arr, 1) == 0 : "Should find 1 at index 0";
        assert binarySearch(arr, 15) == 7 : "Should find 15 at index 7";
        assert binarySearch(arr, 4) == -1 : "Should not find 4";
        assert binarySearch(arr, 0) == -1 : "Should not find 0";
        assert binarySearch(arr, 20) == -1 : "Should not find 20";
        
        System.out.println("All correctness tests passed!");
    }
}
```

#### 2. Efficiency
The algorithm should use resources (time and space) efficiently.

**Example:**
Comparing different approaches for finding duplicates:

```java
public class EfficiencyExample {
    // Approach 1: Brute Force O(n²)
    public static boolean hasDuplicateBruteForce(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            for (int j = i + 1; j < arr.length; j++) {
                if (arr[i] == arr[j]) {
                    return true;
                }
            }
        }
        return false;
    }
    
    // Approach 2: Sorting O(n log n)
    public static boolean hasDuplicateSorting(int[] arr) {
        Arrays.sort(arr);
        for (int i = 0; i < arr.length - 1; i++) {
            if (arr[i] == arr[i + 1]) {
                return true;
            }
        }
        return false;
    }
    
    // Approach 3: Hash Set O(n)
    public static boolean hasDuplicateHashSet(int[] arr) {
        Set<Integer> seen = new HashSet<>();
        for (int num : arr) {
            if (seen.contains(num)) {
                return true;
            }
            seen.add(num);
        }
        return false;
    }
}
```

#### 3. Simplicity
The algorithm should be easy to understand and implement.

**Example:**
Simple vs complex approaches to finding the maximum:

```java
public class SimplicityExample {
    // Simple approach - easy to understand
    public static int findMaxSimple(int[] arr) {
        if (arr.length == 0) {
            throw new IllegalArgumentException("Array is empty");
        }
        
        int max = arr[0];
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        return max;
    }
    
    // Complex approach - harder to understand
    public static int findMaxComplex(int[] arr) {
        if (arr.length == 0) {
            throw new IllegalArgumentException("Array is empty");
        }
        
        return Arrays.stream(arr)
                .reduce(Integer.MIN_VALUE, Math::max);
    }
}
```

#### 4. Robustness
The algorithm should handle edge cases and unexpected inputs gracefully.

**Example:**
Robust implementation of array reversal:

```java
public class RobustnessExample {
    public static void reverseArray(int[] arr) {
        // Handle edge cases
        if (arr == null || arr.length <= 1) {
            return; // Nothing to reverse
        }
        
        int left = 0;
        int right = arr.length - 1;
        
        while (left < right) {
            // Swap elements
            int temp = arr[left];
            arr[left] = arr[right];
            arr[right] = temp;
            
            left++;
            right--;
        }
    }
    
    // Test robustness
    public static void testRobustness() {
        // Test case 1: Normal array
        int[] arr1 = {1, 2, 3, 4, 5};
        reverseArray(arr1);
        System.out.println("Reversed: " + Arrays.toString(arr1));
        
        // Test case 2: Empty array
        int[] arr2 = {};
        reverseArray(arr2);
        System.out.println("Empty array handled: " + Arrays.toString(arr2));
        
        // Test case 3: Single element
        int[] arr3 = {42};
        reverseArray(arr3);
        System.out.println("Single element: " + Arrays.toString(arr3));
        
        // Test case 4: Null array
        int[] arr4 = null;
        reverseArray(arr4);
        System.out.println("Null array handled safely");
    }
}
```

## 1.4 Time & Space Complexity Analysis

Understanding how algorithms perform as input size grows is crucial for choosing the right solution.

### Time Complexity

Time complexity describes how the running time of an algorithm increases with input size.

#### Common Time Complexities

**O(1) - Constant Time:**
```java
public class ConstantTime {
    // Accessing array element by index
    public static int getFirstElement(int[] arr) {
        return arr[0]; // Always takes same time
    }
    
    // Hash map lookup (average case)
    public static String getValue(Map<String, String> map, String key) {
        return map.get(key); // O(1) average case
    }
}
```

**O(log n) - Logarithmic Time:**
```java
public class LogarithmicTime {
    // Binary search
    public static int binarySearch(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }
}
```

**O(n) - Linear Time:**
```java
public class LinearTime {
    // Linear search
    public static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
    
    // Finding maximum
    public static int findMax(int[] arr) {
        int max = arr[0];
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        return max;
    }
}
```

**O(n log n) - Linearithmic Time:**
```java
public class LinearithmicTime {
    // Merge sort
    public static void mergeSort(int[] arr) {
        if (arr.length <= 1) return;
        
        int mid = arr.length / 2;
        int[] left = Arrays.copyOfRange(arr, 0, mid);
        int[] right = Arrays.copyOfRange(arr, mid, arr.length);
        
        mergeSort(left);
        mergeSort(right);
        merge(arr, left, right);
    }
    
    private static void merge(int[] arr, int[] left, int[] right) {
        int i = 0, j = 0, k = 0;
        
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                arr[k++] = left[i++];
            } else {
                arr[k++] = right[j++];
            }
        }
        
        while (i < left.length) arr[k++] = left[i++];
        while (j < right.length) arr[k++] = right[j++];
    }
}
```

**O(n²) - Quadratic Time:**
```java
public class QuadraticTime {
    // Bubble sort
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // Swap
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
    
    // Finding all pairs
    public static void printAllPairs(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            for (int j = i + 1; j < arr.length; j++) {
                System.out.println("(" + arr[i] + ", " + arr[j] + ")");
            }
        }
    }
}
```

### Space Complexity

Space complexity describes how much memory an algorithm uses relative to input size.

**O(1) - Constant Space:**
```java
public class ConstantSpace {
    // In-place array reversal
    public static void reverseArray(int[] arr) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left < right) {
            int temp = arr[left];
            arr[left] = arr[right];
            arr[right] = temp;
            left++;
            right--;
        }
    }
}
```

**O(n) - Linear Space:**
```java
public class LinearSpace {
    // Creating a copy of array
    public static int[] copyArray(int[] arr) {
        int[] copy = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            copy[i] = arr[i];
        }
        return copy;
    }
    
    // Merge sort (recursive calls use O(n) space)
    public static void mergeSort(int[] arr) {
        if (arr.length <= 1) return;
        
        int mid = arr.length / 2;
        int[] left = Arrays.copyOfRange(arr, 0, mid);
        int[] right = Arrays.copyOfRange(arr, mid, arr.length);
        
        mergeSort(left);
        mergeSort(right);
        merge(arr, left, right);
    }
}
```

## 1.5 Big O, Big Theta, and Big Omega Notations

Mathematical notations used to describe algorithm performance in different scenarios.

### Big O Notation (Upper Bound)

Big O describes the worst-case performance of an algorithm.

**Definition:** f(n) = O(g(n)) if there exist positive constants c and n₀ such that f(n) ≤ c·g(n) for all n ≥ n₀

**Example:**
```java
public class BigONotation {
    // O(n) - Linear search worst case
    public static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1; // Worst case: target not found
    }
    
    // O(n²) - Bubble sort worst case
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    swap(arr, j, j + 1);
                }
            }
        }
    }
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

### Big Omega Notation (Lower Bound)

Big Omega describes the best-case performance of an algorithm.

**Definition:** f(n) = Ω(g(n)) if there exist positive constants c and n₀ such that f(n) ≥ c·g(n) for all n ≥ n₀

**Example:**
```java
public class BigOmegaNotation {
    // Ω(1) - Linear search best case (first element)
    public static int linearSearchBestCase(int[] arr, int target) {
        if (arr[0] == target) {
            return 0; // Best case: found immediately
        }
        // ... rest of search
        return -1;
    }
    
    // Ω(n log n) - Comparison-based sorting best case
    public static void mergeSortBestCase(int[] arr) {
        // Even in best case, we need to compare all elements
        // Lower bound for comparison-based sorting is Ω(n log n)
        mergeSort(arr);
    }
}
```

### Big Theta Notation (Tight Bound)

Big Theta describes both upper and lower bounds, giving a tight characterization.

**Definition:** f(n) = Θ(g(n)) if f(n) = O(g(n)) and f(n) = Ω(g(n))

**Example:**
```java
public class BigThetaNotation {
    // Θ(n) - Linear search (both best and worst case are O(n))
    public static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
    
    // Θ(n log n) - Merge sort (always takes n log n time)
    public static void mergeSort(int[] arr) {
        if (arr.length <= 1) return;
        
        int mid = arr.length / 2;
        int[] left = Arrays.copyOfRange(arr, 0, mid);
        int[] right = Arrays.copyOfRange(arr, mid, arr.length);
        
        mergeSort(left);  // T(n/2)
        mergeSort(right); // T(n/2)
        merge(arr, left, right); // O(n)
        // T(n) = 2T(n/2) + O(n) = Θ(n log n)
    }
}
```

## 1.6 Asymptotic Analysis

Asymptotic analysis focuses on the behavior of algorithms as input size approaches infinity.

### Key Concepts

#### 1. Dominant Terms
Focus on the term that grows fastest as n increases.

**Example:**
```java
public class DominantTerms {
    // Function: f(n) = 3n² + 2n + 1
    // As n → ∞, n² dominates, so f(n) = O(n²)
    
    public static void exampleFunction(int n) {
        // O(n²) - dominant term
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                System.out.println("Operation: " + (i * j));
            }
        }
        
        // O(n) - less significant
        for (int i = 0; i < n; i++) {
            System.out.println("Linear operation: " + i);
        }
        
        // O(1) - constant, negligible
        System.out.println("Constant operation");
    }
}
```

#### 2. Asymptotic Growth Rates
Comparing different growth rates:

```java
public class GrowthRates {
    // O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)
    
    // O(1) - Constant
    public static int constantTime(int n) {
        return n * 2; // Always same time
    }
    
    // O(log n) - Logarithmic
    public static int logarithmicTime(int n) {
        int result = 0;
        while (n > 1) {
            n /= 2;
            result++;
        }
        return result;
    }
    
    // O(n) - Linear
    public static int linearTime(int n) {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            sum += i;
        }
        return sum;
    }
    
    // O(n log n) - Linearithmic
    public static void linearithmicTime(int n) {
        for (int i = 0; i < n; i++) {
            int j = n;
            while (j > 1) {
                j /= 2;
                System.out.println("Operation");
            }
        }
    }
    
    // O(n²) - Quadratic
    public static void quadraticTime(int n) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                System.out.println("Operation");
            }
        }
    }
}
```

#### 3. Asymptotic Equivalence
Functions that grow at the same rate:

```java
public class AsymptoticEquivalence {
    // These functions are asymptotically equivalent:
    // f(n) = 2n + 3
    // g(n) = n
    // Both are O(n)
    
    public static int function1(int n) {
        return 2 * n + 3; // O(n)
    }
    
    public static int function2(int n) {
        return n; // O(n)
    }
    
    // Both functions grow linearly with n
    // As n → ∞, 2n + 3 ≈ 2n ≈ n (ignoring constants)
}
```

## 1.7 Algorithm Correctness & Verification

Ensuring algorithms produce correct results for all valid inputs.

### Verification Methods

#### 1. Loop Invariants
Properties that remain true throughout loop execution.

**Example:**
```java
public class LoopInvariants {
    // Binary search with loop invariant
    public static int binarySearch(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        // Loop invariant: target is in arr[left..right] if it exists
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid; // Found target
            } else if (arr[mid] < target) {
                left = mid + 1; // Target in right half
            } else {
                right = mid - 1; // Target in left half
            }
        }
        
        return -1; // Target not found
    }
    
    // Loop invariant for array reversal
    public static void reverseArray(int[] arr) {
        int left = 0;
        int right = arr.length - 1;
        
        // Loop invariant: arr[0..left-1] and arr[right+1..n-1] are reversed
        while (left < right) {
            swap(arr, left, right);
            left++;
            right--;
        }
    }
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

#### 2. Mathematical Induction
Proving correctness using mathematical induction.

**Example:**
```java
public class MathematicalInduction {
    // Proving correctness of recursive factorial
    public static int factorial(int n) {
        // Base case: n = 0, factorial(0) = 1 ✓
        if (n == 0) {
            return 1;
        }
        
        // Inductive step: assume factorial(n-1) is correct
        // Then factorial(n) = n * factorial(n-1) is correct ✓
        return n * factorial(n - 1);
    }
    
    // Proving correctness of recursive sum
    public static int sum(int[] arr, int index) {
        // Base case: index >= arr.length, return 0 ✓
        if (index >= arr.length) {
            return 0;
        }
        
        // Inductive step: assume sum(arr, index+1) is correct
        // Then sum(arr, index) = arr[index] + sum(arr, index+1) is correct ✓
        return arr[index] + sum(arr, index + 1);
    }
}
```

#### 3. Testing and Validation
Comprehensive testing to verify correctness.

**Example:**
```java
public class TestingValidation {
    public static void testBinarySearch() {
        int[] arr = {1, 3, 5, 7, 9, 11, 13, 15};
        
        // Test case 1: Target exists
        assert binarySearch(arr, 7) == 3 : "Should find 7 at index 3";
        
        // Test case 2: Target doesn't exist
        assert binarySearch(arr, 4) == -1 : "Should not find 4";
        
        // Test case 3: Target at beginning
        assert binarySearch(arr, 1) == 0 : "Should find 1 at index 0";
        
        // Test case 4: Target at end
        assert binarySearch(arr, 15) == 7 : "Should find 15 at index 7";
        
        // Test case 5: Empty array
        int[] empty = {};
        assert binarySearch(empty, 5) == -1 : "Should handle empty array";
        
        System.out.println("All binary search tests passed!");
    }
    
    public static void testFactorial() {
        // Test cases for factorial
        assert factorial(0) == 1 : "factorial(0) should be 1";
        assert factorial(1) == 1 : "factorial(1) should be 1";
        assert factorial(5) == 120 : "factorial(5) should be 120";
        assert factorial(10) == 3628800 : "factorial(10) should be 3628800";
        
        System.out.println("All factorial tests passed!");
    }
}
```

#### 4. Formal Verification
Using formal methods to prove correctness.

**Example:**
```java
public class FormalVerification {
    // Precondition: arr is sorted in ascending order
    // Postcondition: returns index of target if found, -1 otherwise
    public static int binarySearch(int[] arr, int target) {
        // Precondition check
        if (arr == null) {
            throw new IllegalArgumentException("Array cannot be null");
        }
        
        int left = 0;
        int right = arr.length - 1;
        
        // Loop invariant: if target exists, it's in arr[left..right]
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid; // Postcondition satisfied
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1; // Postcondition satisfied: target not found
    }
}
```

Understanding the fundamentals of computer science provides the foundation for mastering algorithms and data structures. These concepts form the building blocks that enable us to think computationally, solve problems systematically, and create efficient, correct algorithms.