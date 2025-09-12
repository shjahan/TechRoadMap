# Section 14 – String Algorithms

## 14.1 String Matching Algorithms

String matching algorithms are fundamental tools for finding patterns within text. They are essential for search engines, text editors, bioinformatics, and many other applications.

### Basic Concepts

String matching involves finding all occurrences of a pattern P in a text T. The pattern is typically much shorter than the text, and we want to find all positions where the pattern appears.

**Real-world Analogy:**
Think of searching for a specific word in a book. You scan through each page, looking for the exact sequence of letters that matches your target word. String matching algorithms automate this process efficiently.

### Naive String Matching

The simplest approach is to check every possible position in the text.

```java
public class NaiveStringMatching {
    public static List<Integer> findPattern(String text, String pattern) {
        List<Integer> positions = new ArrayList<>();
        int n = text.length();
        int m = pattern.length();
        
        // Check every possible starting position
        for (int i = 0; i <= n - m; i++) {
            int j;
            // Check if pattern matches at position i
            for (j = 0; j < m; j++) {
                if (text.charAt(i + j) != pattern.charAt(j)) {
                    break;
                }
            }
            // If we matched all characters
            if (j == m) {
                positions.add(i);
            }
        }
        
        return positions;
    }
    
    // Time Complexity: O((n-m+1) * m) in worst case
    // Space Complexity: O(1)
}
```

### Optimized Naive Approach

We can optimize by skipping characters we know won't match.

```java
public class OptimizedNaiveMatching {
    public static List<Integer> findPattern(String text, String pattern) {
        List<Integer> positions = new ArrayList<>();
        int n = text.length();
        int m = pattern.length();
        
        for (int i = 0; i <= n - m; i++) {
            int j = 0;
            while (j < m && text.charAt(i + j) == pattern.charAt(j)) {
                j++;
            }
            if (j == m) {
                positions.add(i);
            }
        }
        
        return positions;
    }
}
```

## 14.2 Pattern Matching (KMP, Rabin-Karp)

### Knuth-Morris-Pratt (KMP) Algorithm

KMP algorithm uses information from previous matches to avoid unnecessary comparisons.

```java
public class KMPAlgorithm {
    public static List<Integer> findPattern(String text, String pattern) {
        List<Integer> positions = new ArrayList<>();
        int n = text.length();
        int m = pattern.length();
        
        // Build failure function (LPS array)
        int[] lps = buildLPS(pattern);
        
        int i = 0; // index for text
        int j = 0; // index for pattern
        
        while (i < n) {
            if (pattern.charAt(j) == text.charAt(i)) {
                i++;
                j++;
            }
            
            if (j == m) {
                positions.add(i - j);
                j = lps[j - 1]; // Find next match
            } else if (i < n && pattern.charAt(j) != text.charAt(i)) {
                if (j != 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }
        
        return positions;
    }
    
    private static int[] buildLPS(String pattern) {
        int m = pattern.length();
        int[] lps = new int[m];
        int len = 0; // length of previous longest prefix suffix
        int i = 1;
        
        lps[0] = 0; // lps[0] is always 0
        
        while (i < m) {
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
    
    // Time Complexity: O(n + m)
    // Space Complexity: O(m)
}
```

### Rabin-Karp Algorithm

Uses hashing to quickly compare patterns.

```java
public class RabinKarpAlgorithm {
    private static final int PRIME = 101;
    
    public static List<Integer> findPattern(String text, String pattern) {
        List<Integer> positions = new ArrayList<>();
        int n = text.length();
        int m = pattern.length();
        
        if (m > n) return positions;
        
        // Calculate hash of pattern and first window of text
        long patternHash = calculateHash(pattern, m);
        long textHash = calculateHash(text.substring(0, m), m);
        
        // Check if first window matches
        if (patternHash == textHash && checkMatch(text, pattern, 0)) {
            positions.add(0);
        }
        
        // Calculate hash for remaining windows
        long h = 1;
        for (int i = 0; i < m - 1; i++) {
            h = (h * 256) % PRIME;
        }
        
        for (int i = 1; i <= n - m; i++) {
            // Remove leading digit, add trailing digit
            textHash = (256 * (textHash - text.charAt(i - 1) * h) + text.charAt(i + m - 1)) % PRIME;
            
            // Make sure hash is positive
            if (textHash < 0) {
                textHash += PRIME;
            }
            
            // Check if current window matches
            if (patternHash == textHash && checkMatch(text, pattern, i)) {
                positions.add(i);
            }
        }
        
        return positions;
    }
    
    private static long calculateHash(String str, int length) {
        long hash = 0;
        for (int i = 0; i < length; i++) {
            hash = (256 * hash + str.charAt(i)) % PRIME;
        }
        return hash;
    }
    
    private static boolean checkMatch(String text, String pattern, int start) {
        for (int i = 0; i < pattern.length(); i++) {
            if (text.charAt(start + i) != pattern.charAt(i)) {
                return false;
            }
        }
        return true;
    }
    
    // Time Complexity: O(n + m) average case, O(n * m) worst case
    // Space Complexity: O(1)
}
```

## 14.3 Suffix Arrays & Suffix Trees

### Suffix Array

A suffix array is a sorted array of all suffixes of a string.

```java
public class SuffixArray {
    private String text;
    private int[] suffixArray;
    private int[] lcp; // Longest Common Prefix array
    
    public SuffixArray(String text) {
        this.text = text;
        buildSuffixArray();
        buildLCP();
    }
    
    private void buildSuffixArray() {
        int n = text.length();
        suffixArray = new int[n];
        
        // Initialize with indices
        for (int i = 0; i < n; i++) {
            suffixArray[i] = i;
        }
        
        // Sort suffixes
        Arrays.sort(suffixArray, (a, b) -> {
            String suffixA = text.substring(a);
            String suffixB = text.substring(b);
            return suffixA.compareTo(suffixB);
        });
    }
    
    private void buildLCP() {
        int n = text.length();
        lcp = new int[n];
        
        for (int i = 1; i < n; i++) {
            lcp[i] = longestCommonPrefix(suffixArray[i - 1], suffixArray[i]);
        }
    }
    
    private int longestCommonPrefix(int i, int j) {
        int count = 0;
        while (i < text.length() && j < text.length() && text.charAt(i) == text.charAt(j)) {
            i++;
            j++;
            count++;
        }
        return count;
    }
    
    // Search for pattern in suffix array
    public List<Integer> search(String pattern) {
        List<Integer> positions = new ArrayList<>();
        int left = 0, right = suffixArray.length - 1;
        
        // Binary search for pattern
        while (left <= right) {
            int mid = (left + right) / 2;
            String suffix = text.substring(suffixArray[mid]);
            
            if (suffix.startsWith(pattern)) {
                // Found a match, find all occurrences
                int start = mid;
                while (start > 0 && text.substring(suffixArray[start - 1]).startsWith(pattern)) {
                    start--;
                }
                
                int end = mid;
                while (end < suffixArray.length - 1 && text.substring(suffixArray[end + 1]).startsWith(pattern)) {
                    end++;
                }
                
                for (int i = start; i <= end; i++) {
                    positions.add(suffixArray[i]);
                }
                break;
            } else if (suffix.compareTo(pattern) < 0) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return positions;
    }
    
    // Time Complexity: O(n log n) construction, O(m log n) search
    // Space Complexity: O(n)
}
```

### Suffix Tree

A compressed trie containing all suffixes of a string.

```java
public class SuffixTree {
    private static class Node {
        Map<Character, Node> children = new HashMap<>();
        int start, end;
        Node suffixLink;
        
        public Node(int start, int end) {
            this.start = start;
            this.end = end;
        }
    }
    
    private String text;
    private Node root;
    private int activeNode, activeEdge, activeLength;
    private int remaining;
    private Node lastNewNode;
    
    public SuffixTree(String text) {
        this.text = text + "$"; // Add sentinel
        buildSuffixTree();
    }
    
    private void buildSuffixTree() {
        root = new Node(-1, -1);
        activeNode = 0;
        activeEdge = -1;
        activeLength = 0;
        remaining = 0;
        
        for (int i = 0; i < text.length(); i++) {
            extendSuffixTree(i);
        }
    }
    
    private void extendSuffixTree(int pos) {
        remaining++;
        lastNewNode = null;
        
        while (remaining > 0) {
            if (activeLength == 0) {
                activeEdge = pos;
            }
            
            if (!getActiveNode().children.containsKey(text.charAt(activeEdge))) {
                // Rule 2: Create new leaf
                getActiveNode().children.put(text.charAt(activeEdge), new Node(pos, text.length() - 1));
                
                if (lastNewNode != null) {
                    lastNewNode.suffixLink = getActiveNode();
                    lastNewNode = null;
                }
            } else {
                Node next = getActiveNode().children.get(text.charAt(activeEdge));
                int edgeLength = next.end - next.start + 1;
                
                if (activeLength >= edgeLength) {
                    activeEdge += edgeLength;
                    activeLength -= edgeLength;
                    activeNode = next.start;
                    continue;
                }
                
                if (text.charAt(next.start + activeLength) == text.charAt(pos)) {
                    if (lastNewNode != null && activeNode != 0) {
                        lastNewNode.suffixLink = getActiveNode();
                        lastNewNode = null;
                    }
                    activeLength++;
                    break;
                }
                
                // Rule 3: Split edge
                Node split = new Node(next.start, next.start + activeLength - 1);
                getActiveNode().children.put(text.charAt(activeEdge), split);
                
                next.start += activeLength;
                split.children.put(text.charAt(next.start), next);
                split.children.put(text.charAt(pos), new Node(pos, text.length() - 1));
                
                if (lastNewNode != null) {
                    lastNewNode.suffixLink = split;
                }
                
                lastNewNode = split;
            }
            
            remaining--;
            
            if (activeNode == 0 && activeLength > 0) {
                activeLength--;
                activeEdge = pos - remaining + 1;
            } else if (activeNode != 0) {
                activeNode = getActiveNode().suffixLink.start;
            }
        }
    }
    
    private Node getActiveNode() {
        return root;
    }
    
    // Search for pattern in suffix tree
    public boolean search(String pattern) {
        Node current = root;
        int i = 0;
        
        while (i < pattern.length()) {
            if (!current.children.containsKey(pattern.charAt(i))) {
                return false;
            }
            
            Node next = current.children.get(pattern.charAt(i));
            int j = next.start;
            
            while (j <= next.end && i < pattern.length()) {
                if (text.charAt(j) != pattern.charAt(i)) {
                    return false;
                }
                j++;
                i++;
            }
            
            if (j > next.end) {
                current = next;
            }
        }
        
        return true;
    }
    
    // Time Complexity: O(n) construction, O(m) search
    // Space Complexity: O(n)
}
```

## 14.4 Longest Common Subsequence

The Longest Common Subsequence (LCS) problem finds the longest sequence that appears in both strings.

```java
public class LongestCommonSubsequence {
    public static String findLCS(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        
        // Create DP table
        int[][] dp = new int[m + 1][n + 1];
        
        // Fill DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        // Reconstruct LCS
        StringBuilder lcs = new StringBuilder();
        int i = m, j = n;
        
        while (i > 0 && j > 0) {
            if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                lcs.insert(0, str1.charAt(i - 1));
                i--;
                j--;
            } else if (dp[i - 1][j] > dp[i][j - 1]) {
                i--;
            } else {
                j--;
            }
        }
        
        return lcs.toString();
    }
    
    public static int findLCSLength(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        
        // Space-optimized version
        int[] prev = new int[n + 1];
        int[] curr = new int[n + 1];
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    curr[j] = prev[j - 1] + 1;
                } else {
                    curr[j] = Math.max(prev[j], curr[j - 1]);
                }
            }
            
            // Swap arrays
            int[] temp = prev;
            prev = curr;
            curr = temp;
        }
        
        return prev[n];
    }
    
    // Time Complexity: O(m * n)
    // Space Complexity: O(m * n) for full DP, O(min(m, n)) for optimized
}
```

## 14.5 Edit Distance (Levenshtein)

Edit distance measures the minimum number of operations needed to transform one string into another.

```java
public class EditDistance {
    public static int levenshteinDistance(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        
        // Create DP table
        int[][] dp = new int[m + 1][n + 1];
        
        // Initialize base cases
        for (int i = 0; i <= m; i++) {
            dp[i][0] = i;
        }
        for (int j = 0; j <= n; j++) {
            dp[0][j] = j;
        }
        
        // Fill DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(
                        Math.min(dp[i - 1][j],    // deletion
                                dp[i][j - 1]),    // insertion
                        dp[i - 1][j - 1]         // substitution
                    );
                }
            }
        }
        
        return dp[m][n];
    }
    
    // Space-optimized version
    public static int levenshteinDistanceOptimized(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        
        // Use shorter string for optimization
        if (m < n) {
            return levenshteinDistanceOptimized(str2, str1);
        }
        
        int[] prev = new int[n + 1];
        int[] curr = new int[n + 1];
        
        // Initialize first row
        for (int j = 0; j <= n; j++) {
            prev[j] = j;
        }
        
        for (int i = 1; i <= m; i++) {
            curr[0] = i;
            
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    curr[j] = prev[j - 1];
                } else {
                    curr[j] = 1 + Math.min(
                        Math.min(prev[j], curr[j - 1]),
                        prev[j - 1]
                    );
                }
            }
            
            // Swap arrays
            int[] temp = prev;
            prev = curr;
            curr = temp;
        }
        
        return prev[n];
    }
    
    // Time Complexity: O(m * n)
    // Space Complexity: O(m * n) for full DP, O(min(m, n)) for optimized
}
```

## 14.6 Palindrome Detection

Detecting palindromes and finding palindromic substrings.

```java
public class PalindromeDetection {
    // Check if entire string is palindrome
    public static boolean isPalindrome(String str) {
        int left = 0;
        int right = str.length() - 1;
        
        while (left < right) {
            if (str.charAt(left) != str.charAt(right)) {
                return false;
            }
            left++;
            right--;
        }
        
        return true;
    }
    
    // Find longest palindromic substring using expand around centers
    public static String longestPalindrome(String str) {
        if (str == null || str.length() < 1) return "";
        
        int start = 0, end = 0;
        
        for (int i = 0; i < str.length(); i++) {
            // Check for odd length palindromes
            int len1 = expandAroundCenter(str, i, i);
            // Check for even length palindromes
            int len2 = expandAroundCenter(str, i, i + 1);
            
            int len = Math.max(len1, len2);
            
            if (len > end - start) {
                start = i - (len - 1) / 2;
                end = i + len / 2;
            }
        }
        
        return str.substring(start, end + 1);
    }
    
    private static int expandAroundCenter(String str, int left, int right) {
        while (left >= 0 && right < str.length() && str.charAt(left) == str.charAt(right)) {
            left--;
            right++;
        }
        return right - left - 1;
    }
    
    // Count all palindromic substrings
    public static int countPalindromes(String str) {
        int count = 0;
        
        for (int i = 0; i < str.length(); i++) {
            // Count odd length palindromes
            count += expandAroundCenter(str, i, i);
            // Count even length palindromes
            count += expandAroundCenter(str, i, i + 1);
        }
        
        return count;
    }
    
    // Time Complexity: O(n^2) for longest palindrome
    // Space Complexity: O(1)
}
```

## 14.7 String Compression

Compressing strings to reduce storage space.

```java
public class StringCompression {
    // Run-length encoding
    public static String compressRLE(String str) {
        if (str == null || str.length() == 0) return str;
        
        StringBuilder compressed = new StringBuilder();
        int count = 1;
        
        for (int i = 1; i < str.length(); i++) {
            if (str.charAt(i) == str.charAt(i - 1)) {
                count++;
            } else {
                compressed.append(str.charAt(i - 1));
                if (count > 1) {
                    compressed.append(count);
                }
                count = 1;
            }
        }
        
        // Add last character
        compressed.append(str.charAt(str.length() - 1));
        if (count > 1) {
            compressed.append(count);
        }
        
        return compressed.length() < str.length() ? compressed.toString() : str;
    }
    
    // LZW compression (simplified)
    public static List<Integer> compressLZW(String str) {
        Map<String, Integer> dictionary = new HashMap<>();
        List<Integer> result = new ArrayList<>();
        
        // Initialize dictionary with single characters
        for (int i = 0; i < 256; i++) {
            dictionary.put(String.valueOf((char) i), i);
        }
        
        String current = "";
        int dictSize = 256;
        
        for (char c : str.toCharArray()) {
            String combined = current + c;
            
            if (dictionary.containsKey(combined)) {
                current = combined;
            } else {
                result.add(dictionary.get(current));
                dictionary.put(combined, dictSize++);
                current = String.valueOf(c);
            }
        }
        
        if (!current.isEmpty()) {
            result.add(dictionary.get(current));
        }
        
        return result;
    }
    
    // Huffman coding (simplified)
    public static String compressHuffman(String str) {
        // Count character frequencies
        Map<Character, Integer> frequencies = new HashMap<>();
        for (char c : str.toCharArray()) {
            frequencies.put(c, frequencies.getOrDefault(c, 0) + 1);
        }
        
        // Build Huffman tree and generate codes
        // This is a simplified version - full implementation would include tree building
        StringBuilder compressed = new StringBuilder();
        
        for (char c : str.toCharArray()) {
            // In real implementation, this would use actual Huffman codes
            compressed.append(c);
        }
        
        return compressed.toString();
    }
}
```

## 14.8 Regular Expression Matching

Implementing regular expression matching algorithms.

```java
public class RegularExpressionMatching {
    // Simple regex matching with '.' and '*'
    public static boolean isMatch(String text, String pattern) {
        int m = text.length();
        int n = pattern.length();
        
        boolean[][] dp = new boolean[m + 1][n + 1];
        dp[0][0] = true;
        
        // Handle patterns like a*, a*b*, a*b*c*
        for (int j = 1; j <= n; j++) {
            if (pattern.charAt(j - 1) == '*') {
                dp[0][j] = dp[0][j - 2];
            }
        }
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (pattern.charAt(j - 1) == text.charAt(i - 1) || pattern.charAt(j - 1) == '.') {
                    dp[i][j] = dp[i - 1][j - 1];
                } else if (pattern.charAt(j - 1) == '*') {
                    dp[i][j] = dp[i][j - 2]; // Zero occurrences
                    
                    if (pattern.charAt(j - 2) == text.charAt(i - 1) || pattern.charAt(j - 2) == '.') {
                        dp[i][j] = dp[i][j] || dp[i - 1][j]; // One or more occurrences
                    }
                }
            }
        }
        
        return dp[m][n];
    }
    
    // Wildcard matching with '?' and '*'
    public static boolean isMatchWildcard(String text, String pattern) {
        int m = text.length();
        int n = pattern.length();
        
        boolean[][] dp = new boolean[m + 1][n + 1];
        dp[0][0] = true;
        
        // Handle patterns starting with '*'
        for (int j = 1; j <= n; j++) {
            if (pattern.charAt(j - 1) == '*') {
                dp[0][j] = dp[0][j - 1];
            }
        }
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (pattern.charAt(j - 1) == '?' || pattern.charAt(j - 1) == text.charAt(i - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else if (pattern.charAt(j - 1) == '*') {
                    dp[i][j] = dp[i][j - 1] || dp[i - 1][j];
                }
            }
        }
        
        return dp[m][n];
    }
    
    // Time Complexity: O(m * n)
    // Space Complexity: O(m * n)
}
```

**Real-world Analogies:**
- **String Matching:** Like finding a specific word in a dictionary by scanning through pages
- **KMP Algorithm:** Like a smart reader who remembers where they've seen similar patterns before
- **Rabin-Karp:** Like using a quick fingerprint to identify if two things might be the same
- **Suffix Arrays:** Like creating an index of all possible starting points in a book
- **Suffix Trees:** Like organizing a library where each book is connected to related books
- **LCS:** Like finding the longest common sequence of moves in two different chess games
- **Edit Distance:** Like measuring how many changes you need to make one word into another
- **Palindrome Detection:** Like checking if a word reads the same forwards and backwards
- **String Compression:** Like packing a suitcase efficiently to save space
- **Regular Expressions:** Like creating a flexible search pattern that can match many variations

String algorithms are fundamental to computer science and have applications in search engines, text processing, bioinformatics, and many other domains. Understanding these algorithms helps in building efficient text processing systems and solving complex pattern matching problems.