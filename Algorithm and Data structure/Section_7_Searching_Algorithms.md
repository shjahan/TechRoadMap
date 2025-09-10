# Section 7 – Searching Algorithms

## 7.1 Linear Search & Sequential Search

Linear search is the simplest searching algorithm that checks each element sequentially until the target is found.

### Basic Linear Search

```java
public class LinearSearch {
    public static int search(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i; // Return index of found element
            }
        }
        return -1; // Element not found
    }
    
    // Recursive linear search
    public static int searchRecursive(int[] arr, int target, int index) {
        if (index >= arr.length) {
            return -1; // Element not found
        }
        
        if (arr[index] == target) {
            return index;
        }
        
        return searchRecursive(arr, target, index + 1);
    }
    
    // Linear search with sentinel
    public static int searchWithSentinel(int[] arr, int target) {
        int n = arr.length;
        int last = arr[n - 1];
        arr[n - 1] = target; // Set sentinel
        
        int i = 0;
        while (arr[i] != target) {
            i++;
        }
        
        arr[n - 1] = last; // Restore original value
        
        if (i < n - 1 || arr[n - 1] == target) {
            return i;
        }
        return -1;
    }
}
```

**Time Complexity:** O(n)  
**Space Complexity:** O(1)  
**Best Case:** O(1) - Element found at first position  
**Worst Case:** O(n) - Element not found or at last position

## 7.2 Binary Search & Variations

Binary search is an efficient algorithm for searching in sorted arrays using divide-and-conquer approach.

### Basic Binary Search

```java
public class BinarySearch {
    public static int search(int[] arr, int target) {
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
    
    // Recursive binary search
    public static int searchRecursive(int[] arr, int target) {
        return searchRecursive(arr, target, 0, arr.length - 1);
    }
    
    private static int searchRecursive(int[] arr, int target, int left, int right) {
        if (left > right) {
            return -1; // Target not found
        }
        
        int mid = left + (right - left) / 2;
        
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            return searchRecursive(arr, target, mid + 1, right);
        } else {
            return searchRecursive(arr, target, left, mid - 1);
        }
    }
}
```

### Binary Search Variations

```java
public class BinarySearchVariations {
    // Find first occurrence of target
    public static int findFirst(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                result = mid;
                right = mid - 1; // Continue searching left
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
    
    // Find last occurrence of target
    public static int findLast(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                result = mid;
                left = mid + 1; // Continue searching right
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
    
    // Find insertion position (where target should be inserted)
    public static int findInsertionPosition(int[] arr, int target) {
        int left = 0;
        int right = arr.length;
        
        while (left < right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        
        return left;
    }
    
    // Find floor (largest element <= target)
    public static int findFloor(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] <= target) {
                result = mid;
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
    
    // Find ceiling (smallest element >= target)
    public static int findCeiling(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        int result = -1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] >= target) {
                result = mid;
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }
        
        return result;
    }
}
```

**Time Complexity:** O(log n)  
**Space Complexity:** O(1) for iterative, O(log n) for recursive  
**Best Case:** O(1) - Target found at middle  
**Worst Case:** O(log n) - Target not found

## 7.3 Interpolation Search

Interpolation search is an improvement over binary search for uniformly distributed data.

```java
public class InterpolationSearch {
    public static int search(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right && target >= arr[left] && target <= arr[right]) {
            // Calculate position using interpolation formula
            int pos = left + ((target - arr[left]) * (right - left)) / (arr[right] - arr[left]);
            
            if (arr[pos] == target) {
                return pos;
            } else if (arr[pos] < target) {
                left = pos + 1;
            } else {
                right = pos - 1;
            }
        }
        
        return -1; // Target not found
    }
    
    // Recursive interpolation search
    public static int searchRecursive(int[] arr, int target) {
        return searchRecursive(arr, target, 0, arr.length - 1);
    }
    
    private static int searchRecursive(int[] arr, int target, int left, int right) {
        if (left > right || target < arr[left] || target > arr[right]) {
            return -1;
        }
        
        int pos = left + ((target - arr[left]) * (right - left)) / (arr[right] - arr[left]);
        
        if (arr[pos] == target) {
            return pos;
        } else if (arr[pos] < target) {
            return searchRecursive(arr, target, pos + 1, right);
        } else {
            return searchRecursive(arr, target, left, pos - 1);
        }
    }
}
```

**Time Complexity:** O(log log n) for uniformly distributed data, O(n) for worst case  
**Space Complexity:** O(1) for iterative, O(log log n) for recursive

## 7.4 Exponential Search

Exponential search is useful for unbounded arrays or when the target is near the beginning.

```java
public class ExponentialSearch {
    public static int search(int[] arr, int target) {
        int n = arr.length;
        
        // If target is at first position
        if (arr[0] == target) {
            return 0;
        }
        
        // Find range for binary search
        int i = 1;
        while (i < n && arr[i] <= target) {
            i *= 2; // Double the index
        }
        
        // Binary search in the found range
        return binarySearch(arr, target, i / 2, Math.min(i, n - 1));
    }
    
    private static int binarySearch(int[] arr, int target, int left, int right) {
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

**Time Complexity:** O(log n)  
**Space Complexity:** O(1)

## 7.5 Jump Search

Jump search is a searching algorithm for sorted arrays that jumps ahead by fixed steps.

```java
public class JumpSearch {
    public static int search(int[] arr, int target) {
        int n = arr.length;
        int step = (int) Math.sqrt(n);
        int prev = 0;
        
        // Find the block where target might be
        while (arr[Math.min(step, n) - 1] < target) {
            prev = step;
            step += (int) Math.sqrt(n);
            if (prev >= n) {
                return -1; // Target not found
            }
        }
        
        // Linear search in the found block
        while (arr[prev] < target) {
            prev++;
            if (prev == Math.min(step, n)) {
                return -1; // Target not found
            }
        }
        
        if (arr[prev] == target) {
            return prev;
        }
        
        return -1; // Target not found
    }
    
    // Optimized jump search with dynamic step size
    public static int searchOptimized(int[] arr, int target) {
        int n = arr.length;
        int step = (int) Math.sqrt(n);
        int prev = 0;
        
        while (step < n && arr[step] < target) {
            prev = step;
            step += (int) Math.sqrt(n);
        }
        
        // Linear search in the found block
        for (int i = prev; i < Math.min(step, n); i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        
        return -1;
    }
}
```

**Time Complexity:** O(√n)  
**Space Complexity:** O(1)

## 7.6 Ternary Search

Ternary search is a divide-and-conquer algorithm that divides the search space into three parts.

```java
public class TernarySearch {
    public static int search(int[] arr, int target) {
        return search(arr, target, 0, arr.length - 1);
    }
    
    private static int search(int[] arr, int target, int left, int right) {
        if (left > right) {
            return -1; // Target not found
        }
        
        int mid1 = left + (right - left) / 3;
        int mid2 = right - (right - left) / 3;
        
        if (arr[mid1] == target) {
            return mid1;
        }
        
        if (arr[mid2] == target) {
            return mid2;
        }
        
        if (target < arr[mid1]) {
            return search(arr, target, left, mid1 - 1);
        } else if (target > arr[mid2]) {
            return search(arr, target, mid2 + 1, right);
        } else {
            return search(arr, target, mid1 + 1, mid2 - 1);
        }
    }
    
    // Iterative ternary search
    public static int searchIterative(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right) {
            int mid1 = left + (right - left) / 3;
            int mid2 = right - (right - left) / 3;
            
            if (arr[mid1] == target) {
                return mid1;
            }
            
            if (arr[mid2] == target) {
                return mid2;
            }
            
            if (target < arr[mid1]) {
                right = mid1 - 1;
            } else if (target > arr[mid2]) {
                left = mid2 + 1;
            } else {
                left = mid1 + 1;
                right = mid2 - 1;
            }
        }
        
        return -1;
    }
}
```

**Time Complexity:** O(log₃ n)  
**Space Complexity:** O(log₃ n) for recursive, O(1) for iterative

## 7.7 String Searching (KMP, Boyer-Moore, Rabin-Karp)

### Knuth-Morris-Pratt (KMP) Algorithm

```java
public class KMPSearch {
    public static int search(String text, String pattern) {
        if (pattern.isEmpty()) return 0;
        
        int[] lps = computeLPS(pattern);
        int i = 0; // index for text
        int j = 0; // index for pattern
        
        while (i < text.length()) {
            if (text.charAt(i) == pattern.charAt(j)) {
                i++;
                j++;
            }
            
            if (j == pattern.length()) {
                return i - j; // pattern found
            } else if (i < text.length() && text.charAt(i) != pattern.charAt(j)) {
                if (j != 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }
        
        return -1; // pattern not found
    }
    
    private static int[] computeLPS(String pattern) {
        int[] lps = new int[pattern.length()];
        int len = 0;
        int i = 1;
        
        while (i < pattern.length()) {
            if (pattern.charAt(i) == pattern.charAt(len)) {
                len++;
                lps[i] = len;
                i++;
            } else {
                if (len != 0) {
                    len = lps[len - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        
        return lps;
    }
}
```

### Boyer-Moore Algorithm

```java
public class BoyerMooreSearch {
    public static int search(String text, String pattern) {
        if (pattern.isEmpty()) return 0;
        
        int[] badChar = buildBadCharTable(pattern);
        int[] goodSuffix = buildGoodSuffixTable(pattern);
        
        int textIndex = 0;
        while (textIndex <= text.length() - pattern.length()) {
            int patternIndex = pattern.length() - 1;
            
            while (patternIndex >= 0 && 
                   text.charAt(textIndex + patternIndex) == pattern.charAt(patternIndex)) {
                patternIndex--;
            }
            
            if (patternIndex < 0) {
                return textIndex; // pattern found
            }
            
            int badCharShift = badChar[text.charAt(textIndex + patternIndex)];
            int goodSuffixShift = goodSuffix[patternIndex];
            
            textIndex += Math.max(1, Math.max(badCharShift, goodSuffixShift));
        }
        
        return -1; // pattern not found
    }
    
    private static int[] buildBadCharTable(String pattern) {
        int[] table = new int[256];
        Arrays.fill(table, -1);
        
        for (int i = 0; i < pattern.length(); i++) {
            table[pattern.charAt(i)] = i;
        }
        
        return table;
    }
    
    private static int[] buildGoodSuffixTable(String pattern) {
        int[] table = new int[pattern.length()];
        int[] suffix = new int[pattern.length()];
        
        // Compute suffix array
        suffix[pattern.length() - 1] = pattern.length();
        int j = pattern.length() - 1;
        
        for (int i = pattern.length() - 2; i >= 0; i--) {
            if (i > j && suffix[i + pattern.length() - 1 - j] < i - j) {
                suffix[i] = suffix[i + pattern.length() - 1 - j];
            } else {
                if (i < j) j = i;
                int k = i;
                while (j >= 0 && pattern.charAt(j) == pattern.charAt(j + pattern.length() - 1 - k)) {
                    j--;
                }
                suffix[i] = k - j;
            }
        }
        
        // Compute good suffix table
        Arrays.fill(table, pattern.length());
        for (int i = pattern.length() - 1; i >= 0; i--) {
            if (suffix[i] == i + 1) {
                for (int j = 0; j < pattern.length() - 1 - i; j++) {
                    if (table[j] == pattern.length()) {
                        table[j] = pattern.length() - 1 - i;
                    }
                }
            }
        }
        
        for (int i = 0; i < pattern.length() - 1; i++) {
            table[pattern.length() - 1 - suffix[i]] = pattern.length() - 1 - i;
        }
        
        return table;
    }
}
```

### Rabin-Karp Algorithm

```java
public class RabinKarpSearch {
    private static final int PRIME = 101;
    
    public static int search(String text, String pattern) {
        if (pattern.isEmpty()) return 0;
        
        int patternHash = calculateHash(pattern);
        int textHash = calculateHash(text.substring(0, pattern.length()));
        
        for (int i = 0; i <= text.length() - pattern.length(); i++) {
            if (patternHash == textHash && 
                text.substring(i, i + pattern.length()).equals(pattern)) {
                return i; // pattern found
            }
            
            if (i < text.length() - pattern.length()) {
                textHash = recalculateHash(text, textHash, i, pattern.length());
            }
        }
        
        return -1; // pattern not found
    }
    
    private static int calculateHash(String str) {
        int hash = 0;
        for (int i = 0; i < str.length(); i++) {
            hash += str.charAt(i) * Math.pow(PRIME, i);
        }
        return hash;
    }
    
    private static int recalculateHash(String text, int oldHash, int oldIndex, int patternLength) {
        int newHash = oldHash - text.charAt(oldIndex);
        newHash /= PRIME;
        newHash += text.charAt(oldIndex + patternLength) * Math.pow(PRIME, patternLength - 1);
        return newHash;
    }
}
```

## 7.8 Fuzzy Search & Approximate Matching

### Levenshtein Distance

```java
public class FuzzySearch {
    public static int levenshteinDistance(String s1, String s2) {
        int[][] dp = new int[s1.length() + 1][s2.length() + 1];
        
        // Initialize base cases
        for (int i = 0; i <= s1.length(); i++) {
            dp[i][0] = i;
        }
        for (int j = 0; j <= s2.length(); j++) {
            dp[0][j] = j;
        }
        
        // Fill the DP table
        for (int i = 1; i <= s1.length(); i++) {
            for (int j = 1; j <= s2.length(); j++) {
                if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(Math.min(dp[i - 1][j], dp[i][j - 1]), dp[i - 1][j - 1]);
                }
            }
        }
        
        return dp[s1.length()][s2.length()];
    }
    
    // Find best match with threshold
    public static String findBestMatch(String query, String[] candidates, int threshold) {
        String bestMatch = null;
        int minDistance = Integer.MAX_VALUE;
        
        for (String candidate : candidates) {
            int distance = levenshteinDistance(query, candidate);
            if (distance <= threshold && distance < minDistance) {
                minDistance = distance;
                bestMatch = candidate;
            }
        }
        
        return bestMatch;
    }
    
    // Fuzzy search with similarity score
    public static List<String> fuzzySearch(String query, String[] candidates, double threshold) {
        List<String> results = new ArrayList<>();
        
        for (String candidate : candidates) {
            double similarity = calculateSimilarity(query, candidate);
            if (similarity >= threshold) {
                results.add(candidate);
            }
        }
        
        // Sort by similarity score
        results.sort((a, b) -> Double.compare(
            calculateSimilarity(query, b), 
            calculateSimilarity(query, a)
        ));
        
        return results;
    }
    
    private static double calculateSimilarity(String s1, String s2) {
        int distance = levenshteinDistance(s1, s2);
        int maxLength = Math.max(s1.length(), s2.length());
        return 1.0 - (double) distance / maxLength;
    }
}
```

**Real-world Analogies:**
- **Linear Search:** Like looking through a phone book page by page
- **Binary Search:** Like guessing a number between 1-100 by always guessing the middle
- **Interpolation Search:** Like estimating where to look in a dictionary based on the first letter
- **Exponential Search:** Like doubling your search range until you find the right area
- **Jump Search:** Like jumping ahead by fixed steps and then searching backwards
- **String Searching:** Like finding a specific word in a book using different strategies

Searching algorithms are fundamental to computer science and understanding their trade-offs helps in choosing the right algorithm for specific use cases.