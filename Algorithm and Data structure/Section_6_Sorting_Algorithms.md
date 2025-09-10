# Section 6 – Sorting Algorithms

## 6.1 Comparison-Based Sorting

Comparison-based sorting algorithms compare elements to determine their relative order.

### Sorting Interface

```java
public interface SortingAlgorithm {
    void sort(int[] arr);
    String getName();
    int getTimeComplexity();
    int getSpaceComplexity();
}
```

### Common Comparison-Based Sorts

```java
public class ComparisonSorts {
    // Bubble Sort - O(n²) time, O(1) space
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    swap(arr, j, j + 1);
                    swapped = true;
                }
            }
            if (!swapped) break; // Optimization
        }
    }
    
    // Selection Sort - O(n²) time, O(1) space
    public static void selectionSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {
            int minIndex = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }
            if (minIndex != i) {
                swap(arr, i, minIndex);
            }
        }
    }
    
    // Insertion Sort - O(n²) time, O(1) space
    public static void insertionSort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int key = arr[i];
            int j = i - 1;
            
            while (j >= 0 && arr[j] > key) {
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

## 6.2 Bubble Sort & Selection Sort

### Bubble Sort

```java
public class BubbleSort {
    public static void sort(int[] arr) {
        int n = arr.length;
        boolean swapped;
        
        for (int i = 0; i < n - 1; i++) {
            swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    swap(arr, j, j + 1);
                    swapped = true;
                }
            }
            if (!swapped) break; // Early termination
        }
    }
    
    // Optimized version with last swap position
    public static void optimizedBubbleSort(int[] arr) {
        int n = arr.length;
        int lastSwap = n - 1;
        
        while (lastSwap > 0) {
            int currentSwap = 0;
            for (int j = 0; j < lastSwap; j++) {
                if (arr[j] > arr[j + 1]) {
                    swap(arr, j, j + 1);
                    currentSwap = j;
                }
            }
            lastSwap = currentSwap;
        }
    }
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

### Selection Sort

```java
public class SelectionSort {
    public static void sort(int[] arr) {
        int n = arr.length;
        
        for (int i = 0; i < n - 1; i++) {
            int minIndex = i;
            
            // Find minimum element in remaining array
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }
            
            // Swap if minimum is not at current position
            if (minIndex != i) {
                swap(arr, i, minIndex);
            }
        }
    }
    
    // Stable selection sort
    public static void stableSelectionSort(int[] arr) {
        int n = arr.length;
        
        for (int i = 0; i < n - 1; i++) {
            int minIndex = i;
            
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }
            
            // Shift elements to maintain stability
            int minValue = arr[minIndex];
            for (int k = minIndex; k > i; k--) {
                arr[k] = arr[k - 1];
            }
            arr[i] = minValue;
        }
    }
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

## 6.3 Insertion Sort & Shell Sort

### Insertion Sort

```java
public class InsertionSort {
    public static void sort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int key = arr[i];
            int j = i - 1;
            
            // Move elements greater than key one position ahead
            while (j >= 0 && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
        }
    }
    
    // Binary insertion sort
    public static void binaryInsertionSort(int[] arr) {
        for (int i = 1; i < arr.length; i++) {
            int key = arr[i];
            int pos = binarySearch(arr, key, 0, i - 1);
            
            // Shift elements to make space
            for (int j = i; j > pos; j--) {
                arr[j] = arr[j - 1];
            }
            arr[pos] = key;
        }
    }
    
    private static int binarySearch(int[] arr, int key, int left, int right) {
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] <= key) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return left;
    }
}
```

### Shell Sort

```java
public class ShellSort {
    public static void sort(int[] arr) {
        int n = arr.length;
        
        // Start with large gap, reduce it
        for (int gap = n / 2; gap > 0; gap /= 2) {
            // Do insertion sort for this gap
            for (int i = gap; i < n; i++) {
                int temp = arr[i];
                int j;
                
                for (j = i; j >= gap && arr[j - gap] > temp; j -= gap) {
                    arr[j] = arr[j - gap];
                }
                arr[j] = temp;
            }
        }
    }
    
    // Shell sort with different gap sequences
    public static void sortWithGaps(int[] arr) {
        int n = arr.length;
        int[] gaps = {701, 301, 132, 57, 23, 10, 4, 1}; // Ciura sequence
        
        for (int gap : gaps) {
            if (gap < n) {
                for (int i = gap; i < n; i++) {
                    int temp = arr[i];
                    int j;
                    
                    for (j = i; j >= gap && arr[j - gap] > temp; j -= gap) {
                        arr[j] = arr[j - gap];
                    }
                    arr[j] = temp;
                }
            }
        }
    }
}
```

## 6.4 Merge Sort & Divide-and-Conquer

### Merge Sort

```java
public class MergeSort {
    public static void sort(int[] arr) {
        if (arr.length <= 1) return;
        
        int[] temp = new int[arr.length];
        mergeSort(arr, temp, 0, arr.length - 1);
    }
    
    private static void mergeSort(int[] arr, int[] temp, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            
            // Sort left half
            mergeSort(arr, temp, left, mid);
            
            // Sort right half
            mergeSort(arr, temp, mid + 1, right);
            
            // Merge the sorted halves
            merge(arr, temp, left, mid, right);
        }
    }
    
    private static void merge(int[] arr, int[] temp, int left, int mid, int right) {
        // Copy data to temp arrays
        for (int i = left; i <= right; i++) {
            temp[i] = arr[i];
        }
        
        int i = left;    // Initial index of first subarray
        int j = mid + 1; // Initial index of second subarray
        int k = left;    // Initial index of merged subarray
        
        // Merge the temp arrays back into arr[left..right]
        while (i <= mid && j <= right) {
            if (temp[i] <= temp[j]) {
                arr[k] = temp[i];
                i++;
            } else {
                arr[k] = temp[j];
                j++;
            }
            k++;
        }
        
        // Copy remaining elements of left subarray
        while (i <= mid) {
            arr[k] = temp[i];
            i++;
            k++;
        }
        
        // Copy remaining elements of right subarray
        while (j <= right) {
            arr[k] = temp[j];
            j++;
            k++;
        }
    }
    
    // Iterative merge sort
    public static void iterativeMergeSort(int[] arr) {
        int n = arr.length;
        int[] temp = new int[n];
        
        for (int size = 1; size < n; size *= 2) {
            for (int left = 0; left < n; left += 2 * size) {
                int mid = Math.min(left + size - 1, n - 1);
                int right = Math.min(left + 2 * size - 1, n - 1);
                merge(arr, temp, left, mid, right);
            }
        }
    }
}
```

## 6.5 Quick Sort & Partitioning

### Quick Sort

```java
public class QuickSort {
    public static void sort(int[] arr) {
        if (arr.length <= 1) return;
        quickSort(arr, 0, arr.length - 1);
    }
    
    private static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            // Partition the array
            int pivotIndex = partition(arr, low, high);
            
            // Recursively sort elements before and after partition
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    private static int partition(int[] arr, int low, int high) {
        // Choose rightmost element as pivot
        int pivot = arr[high];
        int i = low - 1; // Index of smaller element
        
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        
        swap(arr, i + 1, high);
        return i + 1;
    }
    
    // Randomized quick sort
    public static void randomizedQuickSort(int[] arr) {
        if (arr.length <= 1) return;
        randomizedQuickSort(arr, 0, arr.length - 1);
    }
    
    private static void randomizedQuickSort(int[] arr, int low, int high) {
        if (low < high) {
            // Randomly select pivot
            int randomIndex = low + (int) (Math.random() * (high - low + 1));
            swap(arr, randomIndex, high);
            
            int pivotIndex = partition(arr, low, high);
            randomizedQuickSort(arr, low, pivotIndex - 1);
            randomizedQuickSort(arr, pivotIndex + 1, high);
        }
    }
    
    // Three-way partitioning (Dutch National Flag)
    public static void threeWayQuickSort(int[] arr) {
        threeWayQuickSort(arr, 0, arr.length - 1);
    }
    
    private static void threeWayQuickSort(int[] arr, int low, int high) {
        if (low >= high) return;
        
        int lt = low, gt = high;
        int pivot = arr[low];
        int i = low;
        
        while (i <= gt) {
            if (arr[i] < pivot) {
                swap(arr, lt++, i++);
            } else if (arr[i] > pivot) {
                swap(arr, i, gt--);
            } else {
                i++;
            }
        }
        
        threeWayQuickSort(arr, low, lt - 1);
        threeWayQuickSort(arr, gt + 1, high);
    }
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

## 6.6 Heap Sort & Priority Queue Sorting

### Heap Sort

```java
public class HeapSort {
    public static void sort(int[] arr) {
        int n = arr.length;
        
        // Build max heap
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }
        
        // Extract elements from heap one by one
        for (int i = n - 1; i > 0; i--) {
            // Move current root to end
            swap(arr, 0, i);
            
            // Call heapify on reduced heap
            heapify(arr, i, 0);
        }
    }
    
    private static void heapify(int[] arr, int n, int i) {
        int largest = i; // Initialize largest as root
        int left = 2 * i + 1; // Left child
        int right = 2 * i + 2; // Right child
        
        // If left child is larger than root
        if (left < n && arr[left] > arr[largest]) {
            largest = left;
        }
        
        // If right child is larger than largest so far
        if (right < n && arr[right] > arr[largest]) {
            largest = right;
        }
        
        // If largest is not root
        if (largest != i) {
            swap(arr, i, largest);
            
            // Recursively heapify the affected sub-tree
            heapify(arr, n, largest);
        }
    }
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

## 6.7 Non-Comparison Sorting (Counting, Radix, Bucket)

### Counting Sort

```java
public class CountingSort {
    public static void sort(int[] arr) {
        int n = arr.length;
        if (n == 0) return;
        
        // Find the maximum element
        int max = arr[0];
        for (int i = 1; i < n; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        
        // Create count array
        int[] count = new int[max + 1];
        
        // Store count of each element
        for (int i = 0; i < n; i++) {
            count[arr[i]]++;
        }
        
        // Modify count array to store actual position
        for (int i = 1; i <= max; i++) {
            count[i] += count[i - 1];
        }
        
        // Build output array
        int[] output = new int[n];
        for (int i = n - 1; i >= 0; i--) {
            output[count[arr[i]] - 1] = arr[i];
            count[arr[i]]--;
        }
        
        // Copy output array to original array
        System.arraycopy(output, 0, arr, 0, n);
    }
}
```

### Radix Sort

```java
public class RadixSort {
    public static void sort(int[] arr) {
        int n = arr.length;
        if (n == 0) return;
        
        // Find maximum number to know number of digits
        int max = arr[0];
        for (int i = 1; i < n; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        
        // Do counting sort for every digit
        for (int exp = 1; max / exp > 0; exp *= 10) {
            countingSortByDigit(arr, n, exp);
        }
    }
    
    private static void countingSortByDigit(int[] arr, int n, int exp) {
        int[] output = new int[n];
        int[] count = new int[10];
        
        // Store count of occurrences
        for (int i = 0; i < n; i++) {
            count[(arr[i] / exp) % 10]++;
        }
        
        // Change count[i] so that count[i] contains actual position
        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }
        
        // Build output array
        for (int i = n - 1; i >= 0; i--) {
            output[count[(arr[i] / exp) % 10] - 1] = arr[i];
            count[(arr[i] / exp) % 10]--;
        }
        
        // Copy output array to original array
        System.arraycopy(output, 0, arr, 0, n);
    }
}
```

### Bucket Sort

```java
public class BucketSort {
    public static void sort(double[] arr) {
        int n = arr.length;
        if (n == 0) return;
        
        // Create buckets
        List<Double>[] buckets = new List[n];
        for (int i = 0; i < n; i++) {
            buckets[i] = new ArrayList<>();
        }
        
        // Put array elements in different buckets
        for (int i = 0; i < n; i++) {
            int bucketIndex = (int) (n * arr[i]);
            buckets[bucketIndex].add(arr[i]);
        }
        
        // Sort individual buckets
        for (int i = 0; i < n; i++) {
            Collections.sort(buckets[i]);
        }
        
        // Concatenate all buckets into arr[]
        int index = 0;
        for (int i = 0; i < n; i++) {
            for (double item : buckets[i]) {
                arr[index++] = item;
            }
        }
    }
}
```

## 6.8 Hybrid Sorting Algorithms

### Timsort (Used in Python and Java)

```java
public class TimSort {
    private static final int MIN_MERGE = 32;
    
    public static void sort(int[] arr) {
        int n = arr.length;
        if (n < 2) return;
        
        // Sort individual subarrays of size MIN_MERGE
        for (int i = 0; i < n; i += MIN_MERGE) {
            insertionSort(arr, i, Math.min(i + MIN_MERGE - 1, n - 1));
        }
        
        // Merge subarrays
        for (int size = MIN_MERGE; size < n; size *= 2) {
            for (int left = 0; left < n; left += 2 * size) {
                int mid = left + size - 1;
                int right = Math.min(left + 2 * size - 1, n - 1);
                
                if (mid < right) {
                    merge(arr, left, mid, right);
                }
            }
        }
    }
    
    private static void insertionSort(int[] arr, int left, int right) {
        for (int i = left + 1; i <= right; i++) {
            int key = arr[i];
            int j = i - 1;
            
            while (j >= left && arr[j] > key) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key;
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

## 6.9 External Sorting & Large Data Sets

### External Merge Sort

```java
public class ExternalMergeSort {
    private static final int CHUNK_SIZE = 1000; // Size of each chunk
    
    public static void sort(String inputFile, String outputFile) {
        try {
            // Phase 1: Sort chunks and write to temporary files
            List<String> tempFiles = sortChunks(inputFile);
            
            // Phase 2: Merge sorted chunks
            mergeFiles(tempFiles, outputFile);
            
            // Clean up temporary files
            for (String tempFile : tempFiles) {
                new File(tempFile).delete();
            }
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    private static List<String> sortChunks(String inputFile) throws IOException {
        List<String> tempFiles = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new FileReader(inputFile));
        List<Integer> chunk = new ArrayList<>();
        int chunkCount = 0;
        
        String line;
        while ((line = reader.readLine()) != null) {
            chunk.add(Integer.parseInt(line));
            
            if (chunk.size() >= CHUNK_SIZE) {
                Collections.sort(chunk);
                String tempFile = "temp_" + chunkCount + ".txt";
                writeChunk(chunk, tempFile);
                tempFiles.add(tempFile);
                chunk.clear();
                chunkCount++;
            }
        }
        
        // Handle remaining elements
        if (!chunk.isEmpty()) {
            Collections.sort(chunk);
            String tempFile = "temp_" + chunkCount + ".txt";
            writeChunk(chunk, tempFile);
            tempFiles.add(tempFile);
        }
        
        reader.close();
        return tempFiles;
    }
    
    private static void writeChunk(List<Integer> chunk, String filename) throws IOException {
        BufferedWriter writer = new BufferedWriter(new FileWriter(filename));
        for (Integer value : chunk) {
            writer.write(value.toString());
            writer.newLine();
        }
        writer.close();
    }
    
    private static void mergeFiles(List<String> tempFiles, String outputFile) throws IOException {
        PriorityQueue<FileEntry> minHeap = new PriorityQueue<>();
        List<BufferedReader> readers = new ArrayList<>();
        
        // Initialize heap with first element from each file
        for (String tempFile : tempFiles) {
            BufferedReader reader = new BufferedReader(new FileReader(tempFile));
            readers.add(reader);
            String line = reader.readLine();
            if (line != null) {
                minHeap.offer(new FileEntry(Integer.parseInt(line), readers.size() - 1));
            }
        }
        
        BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile));
        
        while (!minHeap.isEmpty()) {
            FileEntry min = minHeap.poll();
            writer.write(min.value.toString());
            writer.newLine();
            
            String nextLine = readers.get(min.fileIndex).readLine();
            if (nextLine != null) {
                minHeap.offer(new FileEntry(Integer.parseInt(nextLine), min.fileIndex));
            }
        }
        
        // Close all readers and writer
        for (BufferedReader reader : readers) {
            reader.close();
        }
        writer.close();
    }
    
    private static class FileEntry implements Comparable<FileEntry> {
        Integer value;
        int fileIndex;
        
        public FileEntry(Integer value, int fileIndex) {
            this.value = value;
            this.fileIndex = fileIndex;
        }
        
        @Override
        public int compareTo(FileEntry other) {
            return this.value.compareTo(other.value);
        }
    }
}
```

**Real-world Analogies:**
- **Bubble Sort:** Like bubbles rising to the surface in water
- **Selection Sort:** Like finding the shortest person in a line and moving them to the front
- **Insertion Sort:** Like sorting playing cards in your hand
- **Merge Sort:** Like dividing a deck of cards in half, sorting each half, then merging them
- **Quick Sort:** Like organizing books on a shelf by picking a book and putting smaller books to the left and larger to the right
- **Heap Sort:** Like building a pyramid and then removing the top element repeatedly
- **Counting Sort:** Like counting how many of each type of item you have
- **Radix Sort:** Like sorting by the last digit, then second-to-last, etc.

Sorting algorithms are fundamental to computer science and understanding their trade-offs is crucial for choosing the right algorithm for specific use cases.