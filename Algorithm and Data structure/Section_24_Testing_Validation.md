# Section 24 – Testing & Validation

## 24.1 Testing Strategies for Algorithms

Testing algorithms requires different strategies than testing regular software due to their mathematical nature and performance requirements.

### Unit Testing for Algorithms

```java
public class AlgorithmUnitTests {
    @Test
    public void testBinarySearch() {
        int[] arr = {1, 3, 5, 7, 9, 11, 13, 15};
        
        // Test cases
        assertEquals(0, binarySearch(arr, 1));   // First element
        assertEquals(3, binarySearch(arr, 7));   // Middle element
        assertEquals(7, binarySearch(arr, 15));  // Last element
        assertEquals(-1, binarySearch(arr, 4));  // Not found
        assertEquals(-1, binarySearch(arr, 0));  // Below range
        assertEquals(-1, binarySearch(arr, 20)); // Above range
    }
    
    @Test
    public void testQuickSort() {
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        int[] expected = {11, 12, 22, 25, 34, 64, 90};
        
        quickSort(arr);
        assertArrayEquals(expected, arr);
    }
    
    @Test
    public void testQuickSortEdgeCases() {
        // Empty array
        int[] empty = {};
        quickSort(empty);
        assertArrayEquals(new int[]{}, empty);
        
        // Single element
        int[] single = {42};
        quickSort(single);
        assertArrayEquals(new int[]{42}, single);
        
        // Already sorted
        int[] sorted = {1, 2, 3, 4, 5};
        quickSort(sorted);
        assertArrayEquals(new int[]{1, 2, 3, 4, 5}, sorted);
        
        // Reverse sorted
        int[] reverse = {5, 4, 3, 2, 1};
        quickSort(reverse);
        assertArrayEquals(new int[]{1, 2, 3, 4, 5}, reverse);
        
        // All same elements
        int[] same = {3, 3, 3, 3, 3};
        quickSort(same);
        assertArrayEquals(new int[]{3, 3, 3, 3, 3}, same);
    }
    
    @Test
    public void testHashTable() {
        HashTable<String, Integer> hashTable = new HashTable<>();
        
        // Test put and get
        hashTable.put("apple", 5);
        hashTable.put("banana", 3);
        hashTable.put("cherry", 8);
        
        assertEquals(Integer.valueOf(5), hashTable.get("apple"));
        assertEquals(Integer.valueOf(3), hashTable.get("banana"));
        assertEquals(Integer.valueOf(8), hashTable.get("cherry"));
        assertNull(hashTable.get("grape"));
        
        // Test update
        hashTable.put("apple", 10);
        assertEquals(Integer.valueOf(10), hashTable.get("apple"));
        
        // Test remove
        hashTable.remove("banana");
        assertNull(hashTable.get("banana"));
    }
    
    private int binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
    
    private void quickSort(int[] arr) {
        if (arr.length <= 1) return;
        quickSort(arr, 0, arr.length - 1);
    }
    
    private void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(arr, low, high);
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    private int partition(int[] arr, int low, int high) {
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
    
    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

### Performance Testing

```java
public class PerformanceTests {
    @Test
    public void testSortingPerformance() {
        int[] sizes = {1000, 10000, 100000};
        
        for (int size : sizes) {
            int[] data = generateRandomArray(size);
            
            // Test QuickSort
            long startTime = System.nanoTime();
            quickSort(data.clone());
            long quickSortTime = System.nanoTime() - startTime;
            
            // Test MergeSort
            startTime = System.nanoTime();
            mergeSort(data.clone());
            long mergeSortTime = System.nanoTime() - startTime;
            
            // Test BubbleSort
            startTime = System.nanoTime();
            bubbleSort(data.clone());
            long bubbleSortTime = System.nanoTime() - startTime;
            
            System.out.printf("Size: %d, QuickSort: %d ns, MergeSort: %d ns, BubbleSort: %d ns%n",
                            size, quickSortTime, mergeSortTime, bubbleSortTime);
            
            // Verify performance expectations
            assertTrue("QuickSort should be faster than BubbleSort for large arrays",
                      size < 10000 || quickSortTime < bubbleSortTime);
        }
    }
    
    @Test
    public void testMemoryUsage() {
        int size = 1000000;
        long memoryBefore = getUsedMemory();
        
        int[] data = generateRandomArray(size);
        quickSort(data);
        
        long memoryAfter = getUsedMemory();
        long memoryUsed = memoryAfter - memoryBefore;
        
        System.out.println("Memory used: " + memoryUsed + " bytes");
        
        // Verify memory usage is reasonable
        assertTrue("Memory usage should be reasonable", memoryUsed < size * 8); // 8 bytes per int
    }
    
    private int[] generateRandomArray(int size) {
        int[] arr = new int[size];
        Random random = new Random();
        for (int i = 0; i < size; i++) {
            arr[i] = random.nextInt(1000);
        }
        return arr;
    }
    
    private long getUsedMemory() {
        Runtime runtime = Runtime.getRuntime();
        return runtime.totalMemory() - runtime.freeMemory();
    }
    
    private void quickSort(int[] arr) {
        if (arr.length <= 1) return;
        quickSort(arr, 0, arr.length - 1);
    }
    
    private void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(arr, low, high);
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    private int partition(int[] arr, int low, int high) {
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
    
    private void mergeSort(int[] arr) {
        if (arr.length <= 1) return;
        int mid = arr.length / 2;
        int[] left = Arrays.copyOfRange(arr, 0, mid);
        int[] right = Arrays.copyOfRange(arr, mid, arr.length);
        mergeSort(left);
        mergeSort(right);
        merge(arr, left, right);
    }
    
    private void merge(int[] arr, int[] left, int[] right) {
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
    
    private void bubbleSort(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = 0; j < arr.length - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    swap(arr, j, j + 1);
                }
            }
        }
    }
    
    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

## 24.2 Property-Based Testing

Property-based testing generates random inputs and verifies that certain properties hold.

### Property-Based Testing Framework

```java
public class PropertyBasedTests {
    @Test
    public void testSortingProperties() {
        // Property: Sorting should produce a sorted array
        for (int i = 0; i < 1000; i++) {
            int[] arr = generateRandomArray(100);
            quickSort(arr);
            assertTrue("Array should be sorted", isSorted(arr));
        }
    }
    
    @Test
    public void testSortingStability() {
        // Property: Sorting should preserve relative order of equal elements
        for (int i = 0; i < 1000; i++) {
            Pair[] pairs = generateRandomPairs(100);
            stableSort(pairs);
            assertTrue("Array should be stably sorted", isStablySorted(pairs));
        }
    }
    
    @Test
    public void testHashTableProperties() {
        // Property: Hash table should maintain key-value relationships
        for (int i = 0; i < 1000; i++) {
            HashTable<String, Integer> hashTable = new HashTable<>();
            Map<String, Integer> reference = new HashMap<>();
            
            // Random operations
            for (int j = 0; j < 100; j++) {
                String key = generateRandomString(10);
                Integer value = new Random().nextInt(1000);
                
                if (new Random().nextBoolean()) {
                    hashTable.put(key, value);
                    reference.put(key, value);
                } else {
                    hashTable.remove(key);
                    reference.remove(key);
                }
            }
            
            // Verify properties
            for (String key : reference.keySet()) {
                assertEquals("Hash table should maintain key-value relationships",
                           reference.get(key), hashTable.get(key));
            }
        }
    }
    
    @Test
    public void testBinarySearchProperties() {
        // Property: Binary search should find existing elements
        for (int i = 0; i < 1000; i++) {
            int[] arr = generateSortedArray(100);
            int target = arr[new Random().nextInt(arr.length)];
            int index = binarySearch(arr, target);
            assertTrue("Binary search should find existing elements", index >= 0);
            assertEquals("Binary search should return correct index", target, arr[index]);
        }
    }
    
    private int[] generateRandomArray(int size) {
        int[] arr = new int[size];
        Random random = new Random();
        for (int i = 0; i < size; i++) {
            arr[i] = random.nextInt(1000);
        }
        return arr;
    }
    
    private int[] generateSortedArray(int size) {
        int[] arr = generateRandomArray(size);
        Arrays.sort(arr);
        return arr;
    }
    
    private Pair[] generateRandomPairs(int size) {
        Pair[] pairs = new Pair[size];
        Random random = new Random();
        for (int i = 0; i < size; i++) {
            pairs[i] = new Pair(random.nextInt(10), random.nextInt(1000));
        }
        return pairs;
    }
    
    private String generateRandomString(int length) {
        String chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        Random random = new Random();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < length; i++) {
            sb.append(chars.charAt(random.nextInt(chars.length())));
        }
        return sb.toString();
    }
    
    private boolean isSorted(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] < arr[i - 1]) return false;
        }
        return true;
    }
    
    private boolean isStablySorted(Pair[] pairs) {
        for (int i = 1; i < pairs.length; i++) {
            if (pairs[i].key < pairs[i - 1].key) return false;
            if (pairs[i].key == pairs[i - 1].key && pairs[i].value < pairs[i - 1].value) return false;
        }
        return true;
    }
    
    private void quickSort(int[] arr) {
        if (arr.length <= 1) return;
        quickSort(arr, 0, arr.length - 1);
    }
    
    private void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(arr, low, high);
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    private int partition(int[] arr, int low, int high) {
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
    
    private void stableSort(Pair[] pairs) {
        Arrays.sort(pairs, (a, b) -> {
            int keyCompare = Integer.compare(a.key, b.key);
            return keyCompare != 0 ? keyCompare : Integer.compare(a.value, b.value);
        });
    }
    
    private int binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
    
    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    
    private static class Pair {
        int key;
        int value;
        
        Pair(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }
}
```

## 24.3 Stress Testing

Stress testing pushes algorithms to their limits with extreme inputs.

### Stress Testing Framework

```java
public class StressTests {
    @Test
    public void testSortingStress() {
        // Test with maximum array size
        int maxSize = 1000000;
        int[] arr = generateRandomArray(maxSize);
        
        long startTime = System.nanoTime();
        quickSort(arr);
        long endTime = System.nanoTime();
        
        long executionTime = endTime - startTime;
        System.out.println("Stress test execution time: " + executionTime + " ns");
        
        // Verify correctness
        assertTrue("Array should be sorted", isSorted(arr));
        
        // Verify performance
        assertTrue("Execution time should be reasonable", executionTime < 1_000_000_000); // 1 second
    }
    
    @Test
    public void testHashTableStress() {
        HashTable<String, Integer> hashTable = new HashTable<>();
        Map<String, Integer> reference = new HashMap<>();
        
        // Insert large number of elements
        int numElements = 100000;
        for (int i = 0; i < numElements; i++) {
            String key = "key" + i;
            Integer value = i;
            hashTable.put(key, value);
            reference.put(key, value);
        }
        
        // Verify all elements are present
        for (String key : reference.keySet()) {
            assertEquals("All elements should be present", reference.get(key), hashTable.get(key));
        }
        
        // Test random access
        Random random = new Random();
        for (int i = 0; i < 10000; i++) {
            String key = "key" + random.nextInt(numElements);
            assertEquals("Random access should work", reference.get(key), hashTable.get(key));
        }
    }
    
    @Test
    public void testMemoryStress() {
        // Test memory usage with large data structures
        int size = 1000000;
        List<int[]> arrays = new ArrayList<>();
        
        try {
            for (int i = 0; i < 100; i++) {
                int[] arr = new int[size];
                Arrays.fill(arr, i);
                arrays.add(arr);
            }
            
            // Verify memory usage
            long usedMemory = getUsedMemory();
            System.out.println("Memory used: " + usedMemory + " bytes");
            
            // Clean up
            arrays.clear();
            System.gc();
            
        } catch (OutOfMemoryError e) {
            fail("Memory stress test failed: " + e.getMessage());
        }
    }
    
    @Test
    public void testConcurrencyStress() {
        // Test concurrent access to data structures
        HashTable<String, Integer> hashTable = new HashTable<>();
        int numThreads = 10;
        int operationsPerThread = 1000;
        
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        List<Future<?>> futures = new ArrayList<>();
        
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            Future<?> future = executor.submit(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    String key = "thread" + threadId + "_key" + j;
                    Integer value = threadId * operationsPerThread + j;
                    hashTable.put(key, value);
                    
                    // Verify the value
                    assertEquals("Concurrent access should work", value, hashTable.get(key));
                }
            });
            futures.add(future);
        }
        
        // Wait for all threads to complete
        for (Future<?> future : futures) {
            try {
                future.get();
            } catch (Exception e) {
                fail("Concurrency stress test failed: " + e.getMessage());
            }
        }
        
        executor.shutdown();
    }
    
    private int[] generateRandomArray(int size) {
        int[] arr = new int[size];
        Random random = new Random();
        for (int i = 0; i < size; i++) {
            arr[i] = random.nextInt(1000);
        }
        return arr;
    }
    
    private boolean isSorted(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] < arr[i - 1]) return false;
        }
        return true;
    }
    
    private long getUsedMemory() {
        Runtime runtime = Runtime.getRuntime();
        return runtime.totalMemory() - runtime.freeMemory();
    }
    
    private void quickSort(int[] arr) {
        if (arr.length <= 1) return;
        quickSort(arr, 0, arr.length - 1);
    }
    
    private void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(arr, low, high);
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    private int partition(int[] arr, int low, int high) {
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
    
    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

## 24.4 Correctness Verification

### Formal Verification Techniques

```java
public class CorrectnessVerification {
    // Invariant-based verification
    public class InvariantVerification {
        @Test
        public void testBinarySearchInvariants() {
            int[] arr = {1, 3, 5, 7, 9, 11, 13, 15};
            int target = 7;
            
            int left = 0, right = arr.length - 1;
            while (left <= right) {
                int mid = left + (right - left) / 2;
                
                // Invariant: target is in arr[left..right] if it exists
                assertTrue("Invariant: left <= right", left <= right);
                assertTrue("Invariant: mid is in range", mid >= left && mid <= right);
                
                if (arr[mid] == target) {
                    assertTrue("Target found at correct position", arr[mid] == target);
                    return;
                }
                
                if (arr[mid] < target) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
            
            // Postcondition: target not found
            assertTrue("Target not found", left > right);
        }
        
        @Test
        public void testQuickSortInvariants() {
            int[] arr = {64, 34, 25, 12, 22, 11, 90};
            quickSortWithInvariants(arr, 0, arr.length - 1);
            
            // Postcondition: array is sorted
            assertTrue("Array should be sorted", isSorted(arr));
        }
        
        private void quickSortWithInvariants(int[] arr, int low, int high) {
            if (low < high) {
                // Precondition: low < high
                assertTrue("Precondition: low < high", low < high);
                
                int pivotIndex = partitionWithInvariants(arr, low, high);
                
                // Invariant: elements before pivot are <= pivot
                for (int i = low; i < pivotIndex; i++) {
                    assertTrue("Invariant: elements before pivot <= pivot", 
                              arr[i] <= arr[pivotIndex]);
                }
                
                // Invariant: elements after pivot are >= pivot
                for (int i = pivotIndex + 1; i <= high; i++) {
                    assertTrue("Invariant: elements after pivot >= pivot", 
                              arr[i] >= arr[pivotIndex]);
                }
                
                quickSortWithInvariants(arr, low, pivotIndex - 1);
                quickSortWithInvariants(arr, pivotIndex + 1, high);
            }
        }
        
        private int partitionWithInvariants(int[] arr, int low, int high) {
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
        
        private boolean isSorted(int[] arr) {
            for (int i = 1; i < arr.length; i++) {
                if (arr[i] < arr[i - 1]) return false;
            }
            return true;
        }
        
        private void swap(int[] arr, int i, int j) {
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    
    // Loop invariant verification
    public class LoopInvariantVerification {
        @Test
        public void testInsertionSortLoopInvariants() {
            int[] arr = {64, 34, 25, 12, 22, 11, 90};
            insertionSortWithInvariants(arr);
            
            // Postcondition: array is sorted
            assertTrue("Array should be sorted", isSorted(arr));
        }
        
        private void insertionSortWithInvariants(int[] arr) {
            for (int i = 1; i < arr.length; i++) {
                int key = arr[i];
                int j = i - 1;
                
                // Loop invariant: arr[0..i-1] is sorted
                assertTrue("Loop invariant: arr[0..i-1] is sorted", 
                          isSorted(Arrays.copyOfRange(arr, 0, i)));
                
                while (j >= 0 && arr[j] > key) {
                    arr[j + 1] = arr[j];
                    j--;
                    
                    // Loop invariant: arr[j+1..i] contains elements > key
                    for (int k = j + 1; k <= i; k++) {
                        assertTrue("Loop invariant: arr[j+1..i] > key", arr[k] > key);
                    }
                }
                
                arr[j + 1] = key;
                
                // Loop invariant: arr[0..i] is sorted
                assertTrue("Loop invariant: arr[0..i] is sorted", 
                          isSorted(Arrays.copyOfRange(arr, 0, i + 1)));
            }
        }
        
        private boolean isSorted(int[] arr) {
            for (int i = 1; i < arr.length; i++) {
                if (arr[i] < arr[i - 1]) return false;
            }
            return true;
        }
    }
}
```

## 24.5 Test Data Generation

### Systematic Test Data Generation

```java
public class TestDataGeneration {
    @Test
    public void testSortingWithGeneratedData() {
        // Generate test data systematically
        List<int[]> testCases = generateSortingTestCases();
        
        for (int[] testCase : testCases) {
            int[] original = testCase.clone();
            quickSort(testCase);
            
            // Verify correctness
            assertTrue("Array should be sorted", isSorted(testCase));
            
            // Verify stability (if applicable)
            assertTrue("Array should maintain element count", 
                      original.length == testCase.length);
        }
    }
    
    @Test
    public void testSearchWithGeneratedData() {
        // Generate test data for search algorithms
        List<SearchTestCase> testCases = generateSearchTestCases();
        
        for (SearchTestCase testCase : testCases) {
            int index = binarySearch(testCase.arr, testCase.target);
            
            if (testCase.expectedIndex >= 0) {
                assertEquals("Should find existing element", testCase.expectedIndex, index);
                assertEquals("Found element should match target", testCase.target, testCase.arr[index]);
            } else {
                assertEquals("Should not find non-existing element", -1, index);
            }
        }
    }
    
    private List<int[]> generateSortingTestCases() {
        List<int[]> testCases = new ArrayList<>();
        
        // Edge cases
        testCases.add(new int[]{});                    // Empty array
        testCases.add(new int[]{42});                  // Single element
        testCases.add(new int[]{1, 2, 3, 4, 5});      // Already sorted
        testCases.add(new int[]{5, 4, 3, 2, 1});      // Reverse sorted
        testCases.add(new int[]{3, 3, 3, 3, 3});      // All same elements
        testCases.add(new int[]{1, 3, 2, 4, 5});      // Partially sorted
        
        // Random cases
        Random random = new Random();
        for (int i = 0; i < 100; i++) {
            int size = random.nextInt(100) + 1;
            int[] arr = new int[size];
            for (int j = 0; j < size; j++) {
                arr[j] = random.nextInt(1000);
            }
            testCases.add(arr);
        }
        
        // Large cases
        for (int i = 0; i < 10; i++) {
            int size = 1000 + random.nextInt(9000);
            int[] arr = new int[size];
            for (int j = 0; j < size; j++) {
                arr[j] = random.nextInt(10000);
            }
            testCases.add(arr);
        }
        
        return testCases;
    }
    
    private List<SearchTestCase> generateSearchTestCases() {
        List<SearchTestCase> testCases = new ArrayList<>();
        
        // Edge cases
        testCases.add(new SearchTestCase(new int[]{}, 5, -1));           // Empty array
        testCases.add(new SearchTestCase(new int[]{42}, 42, 0));         // Single element, found
        testCases.add(new SearchTestCase(new int[]{42}, 5, -1));         // Single element, not found
        testCases.add(new SearchTestCase(new int[]{1, 2, 3, 4, 5}, 3, 2)); // Found in middle
        testCases.add(new SearchTestCase(new int[]{1, 2, 3, 4, 5}, 1, 0)); // Found at beginning
        testCases.add(new SearchTestCase(new int[]{1, 2, 3, 4, 5}, 5, 4)); // Found at end
        testCases.add(new SearchTestCase(new int[]{1, 2, 3, 4, 5}, 6, -1)); // Not found
        
        // Random cases
        Random random = new Random();
        for (int i = 0; i < 100; i++) {
            int size = random.nextInt(100) + 1;
            int[] arr = new int[size];
            for (int j = 0; j < size; j++) {
                arr[j] = random.nextInt(1000);
            }
            Arrays.sort(arr);
            
            // Test with existing element
            int target = arr[random.nextInt(size)];
            int expectedIndex = Arrays.binarySearch(arr, target);
            testCases.add(new SearchTestCase(arr, target, expectedIndex));
            
            // Test with non-existing element
            target = random.nextInt(1000) + 1000; // Outside range
            testCases.add(new SearchTestCase(arr, target, -1));
        }
        
        return testCases;
    }
    
    private boolean isSorted(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] < arr[i - 1]) return false;
        }
        return true;
    }
    
    private int binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
    
    private void quickSort(int[] arr) {
        if (arr.length <= 1) return;
        quickSort(arr, 0, arr.length - 1);
    }
    
    private void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(arr, low, high);
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    private int partition(int[] arr, int low, int high) {
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
    
    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    
    private static class SearchTestCase {
        int[] arr;
        int target;
        int expectedIndex;
        
        SearchTestCase(int[] arr, int target, int expectedIndex) {
            this.arr = arr;
            this.target = target;
            this.expectedIndex = expectedIndex;
        }
    }
}
```

## 24.6 Regression Testing

### Regression Testing Framework

```java
public class RegressionTests {
    private Map<String, Long> baselinePerformance;
    private Map<String, Long> currentPerformance;
    
    @BeforeEach
    public void setUp() {
        baselinePerformance = new HashMap<>();
        currentPerformance = new HashMap<>();
    }
    
    @Test
    public void testPerformanceRegression() {
        // Test sorting algorithms
        testSortingPerformance("QuickSort", this::quickSort);
        testSortingPerformance("MergeSort", this::mergeSort);
        testSortingPerformance("BubbleSort", this::bubbleSort);
        
        // Test search algorithms
        testSearchPerformance("BinarySearch", this::binarySearch);
        testSearchPerformance("LinearSearch", this::linearSearch);
        
        // Verify no significant performance regression
        verifyNoRegression();
    }
    
    @Test
    public void testCorrectnessRegression() {
        // Test that algorithms still produce correct results
        int[] testData = {64, 34, 25, 12, 22, 11, 90};
        int[] expected = {11, 12, 22, 25, 34, 64, 90};
        
        // Test QuickSort
        int[] quickSortResult = testData.clone();
        quickSort(quickSortResult);
        assertArrayEquals("QuickSort regression", expected, quickSortResult);
        
        // Test MergeSort
        int[] mergeSortResult = testData.clone();
        mergeSort(mergeSortResult);
        assertArrayEquals("MergeSort regression", expected, mergeSortResult);
        
        // Test BinarySearch
        int[] sortedData = {1, 3, 5, 7, 9, 11, 13, 15};
        assertEquals("BinarySearch regression", 3, binarySearch(sortedData, 7));
        assertEquals("BinarySearch regression", -1, binarySearch(sortedData, 4));
    }
    
    private void testSortingPerformance(String algorithmName, Consumer<int[]> algorithm) {
        int[] testData = generateTestData(10000);
        
        // Measure current performance
        long startTime = System.nanoTime();
        algorithm.accept(testData);
        long endTime = System.nanoTime();
        
        long executionTime = endTime - startTime;
        currentPerformance.put(algorithmName, executionTime);
        
        // Load baseline performance (in real implementation, this would be from file)
        long baselineTime = loadBaselinePerformance(algorithmName);
        if (baselineTime > 0) {
            baselinePerformance.put(algorithmName, baselineTime);
        }
    }
    
    private void testSearchPerformance(String algorithmName, BiFunction<int[], Integer, Integer> algorithm) {
        int[] testData = generateSortedTestData(10000);
        int target = testData[5000]; // Middle element
        
        // Measure current performance
        long startTime = System.nanoTime();
        algorithm.apply(testData, target);
        long endTime = System.nanoTime();
        
        long executionTime = endTime - startTime;
        currentPerformance.put(algorithmName, executionTime);
        
        // Load baseline performance
        long baselineTime = loadBaselinePerformance(algorithmName);
        if (baselineTime > 0) {
            baselinePerformance.put(algorithmName, baselineTime);
        }
    }
    
    private void verifyNoRegression() {
        for (String algorithm : currentPerformance.keySet()) {
            long currentTime = currentPerformance.get(algorithm);
            long baselineTime = baselinePerformance.getOrDefault(algorithm, 0L);
            
            if (baselineTime > 0) {
                double regressionRatio = (double) currentTime / baselineTime;
                assertTrue("Performance regression detected for " + algorithm + 
                          ": " + regressionRatio + "x slower",
                          regressionRatio < 1.5); // Allow 50% performance degradation
            }
        }
    }
    
    private int[] generateTestData(int size) {
        int[] arr = new int[size];
        Random random = new Random();
        for (int i = 0; i < size; i++) {
            arr[i] = random.nextInt(1000);
        }
        return arr;
    }
    
    private int[] generateSortedTestData(int size) {
        int[] arr = generateTestData(size);
        Arrays.sort(arr);
        return arr;
    }
    
    private long loadBaselinePerformance(String algorithmName) {
        // In real implementation, this would load from a file or database
        // For now, return a mock value
        return 1000000; // 1ms in nanoseconds
    }
    
    private void quickSort(int[] arr) {
        if (arr.length <= 1) return;
        quickSort(arr, 0, arr.length - 1);
    }
    
    private void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(arr, low, high);
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    private int partition(int[] arr, int low, int high) {
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
    
    private void mergeSort(int[] arr) {
        if (arr.length <= 1) return;
        int mid = arr.length / 2;
        int[] left = Arrays.copyOfRange(arr, 0, mid);
        int[] right = Arrays.copyOfRange(arr, mid, arr.length);
        mergeSort(left);
        mergeSort(right);
        merge(arr, left, right);
    }
    
    private void merge(int[] arr, int[] left, int[] right) {
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
    
    private void bubbleSort(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = 0; j < arr.length - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    swap(arr, j, j + 1);
                }
            }
        }
    }
    
    private int binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
    
    private int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) return i;
        }
        return -1;
    }
    
    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

**Real-world Analogies:**
- **Unit Testing:** Like testing each component of a car engine individually
- **Property-Based Testing:** Like testing that a sorting machine always produces sorted output regardless of input
- **Stress Testing:** Like testing a bridge with maximum weight to ensure it doesn't collapse
- **Correctness Verification:** Like using mathematical proofs to verify that a formula always gives the correct answer
- **Test Data Generation:** Like creating different scenarios to test a new recipe
- **Regression Testing:** Like checking that a software update didn't break existing functionality

Testing and validation are essential for ensuring algorithm correctness and performance. These techniques help catch bugs early, verify mathematical properties, and maintain code quality over time.