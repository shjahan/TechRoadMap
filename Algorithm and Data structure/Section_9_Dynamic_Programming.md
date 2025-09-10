# Section 9 – Dynamic Programming

## 9.1 Dynamic Programming Principles

Dynamic Programming (DP) is a method for solving complex problems by breaking them down into simpler subproblems and storing the results to avoid redundant calculations.

### Core Principles

```java
public class DynamicProgrammingPrinciples {
    // 1. Optimal Substructure
    // The optimal solution contains optimal solutions to subproblems
    public int fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    
    // 2. Overlapping Subproblems
    // The same subproblems are solved multiple times
    public int fibonacciMemoized(int n) {
        int[] memo = new int[n + 1];
        Arrays.fill(memo, -1);
        return fibonacciMemoized(n, memo);
    }
    
    private int fibonacciMemoized(int n, int[] memo) {
        if (n <= 1) return n;
        if (memo[n] != -1) return memo[n];
        
        memo[n] = fibonacciMemoized(n - 1, memo) + fibonacciMemoized(n - 2, memo);
        return memo[n];
    }
    
    // 3. State Definition
    // Clearly define what each state represents
    public int longestCommonSubsequence(String text1, String text2) {
        int m = text1.length();
        int n = text2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        // dp[i][j] = LCS of text1[0...i-1] and text2[0...j-1]
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        return dp[m][n];
    }
}
```

## 9.2 Memoization vs Tabulation

### Memoization (Top-Down)

```java
public class Memoization {
    private Map<String, Integer> memo = new HashMap<>();
    
    // Memoized Fibonacci
    public int fibonacci(int n) {
        if (n <= 1) return n;
        
        String key = String.valueOf(n);
        if (memo.containsKey(key)) {
            return memo.get(key);
        }
        
        int result = fibonacci(n - 1) + fibonacci(n - 2);
        memo.put(key, result);
        return result;
    }
    
    // Memoized Longest Increasing Subsequence
    public int longestIncreasingSubsequence(int[] nums) {
        return lisHelper(nums, 0, Integer.MIN_VALUE);
    }
    
    private int lisHelper(int[] nums, int index, int prev) {
        if (index == nums.length) return 0;
        
        String key = index + "," + prev;
        if (memo.containsKey(key)) {
            return memo.get(key);
        }
        
        int take = 0;
        if (nums[index] > prev) {
            take = 1 + lisHelper(nums, index + 1, nums[index]);
        }
        
        int skip = lisHelper(nums, index + 1, prev);
        
        int result = Math.max(take, skip);
        memo.put(key, result);
        return result;
    }
}
```

### Tabulation (Bottom-Up)

```java
public class Tabulation {
    // Tabulated Fibonacci
    public int fibonacci(int n) {
        if (n <= 1) return n;
        
        int[] dp = new int[n + 1];
        dp[0] = 0;
        dp[1] = 1;
        
        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        
        return dp[n];
    }
    
    // Tabulated Longest Increasing Subsequence
    public int longestIncreasingSubsequence(int[] nums) {
        int n = nums.length;
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
        }
        
        return Arrays.stream(dp).max().orElse(0);
    }
}
```

## 9.3 Optimal Substructure & Overlapping Subproblems

### Optimal Substructure Example

```java
public class OptimalSubstructure {
    // Minimum Path Sum
    public int minPathSum(int[][] grid) {
        int m = grid.length;
        int n = grid[0].length;
        int[][] dp = new int[m][n];
        
        // Base case
        dp[0][0] = grid[0][0];
        
        // Fill first row
        for (int j = 1; j < n; j++) {
            dp[0][j] = dp[0][j - 1] + grid[0][j];
        }
        
        // Fill first column
        for (int i = 1; i < m; i++) {
            dp[i][0] = dp[i - 1][0] + grid[i][0];
        }
        
        // Fill remaining cells
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                dp[i][j] = Math.min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j];
            }
        }
        
        return dp[m - 1][n - 1];
    }
    
    // Coin Change
    public int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        
        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (coin <= i) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        
        return dp[amount] > amount ? -1 : dp[amount];
    }
}
```

## 9.4 Classic DP Problems (Fibonacci, LCS, LIS)

### Fibonacci Sequence

```java
public class FibonacciDP {
    // Recursive (inefficient)
    public int fibonacciRecursive(int n) {
        if (n <= 1) return n;
        return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
    }
    
    // Memoized
    public int fibonacciMemoized(int n) {
        int[] memo = new int[n + 1];
        Arrays.fill(memo, -1);
        return fibonacciMemoized(n, memo);
    }
    
    private int fibonacciMemoized(int n, int[] memo) {
        if (n <= 1) return n;
        if (memo[n] != -1) return memo[n];
        
        memo[n] = fibonacciMemoized(n - 1, memo) + fibonacciMemoized(n - 2, memo);
        return memo[n];
    }
    
    // Tabulated
    public int fibonacciTabulated(int n) {
        if (n <= 1) return n;
        
        int[] dp = new int[n + 1];
        dp[0] = 0;
        dp[1] = 1;
        
        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        
        return dp[n];
    }
    
    // Space optimized
    public int fibonacciOptimized(int n) {
        if (n <= 1) return n;
        
        int prev2 = 0;
        int prev1 = 1;
        
        for (int i = 2; i <= n; i++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }
}
```

### Longest Common Subsequence (LCS)

```java
public class LongestCommonSubsequence {
    // Basic LCS
    public int lcs(String text1, String text2) {
        int m = text1.length();
        int n = text2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        return dp[m][n];
    }
    
    // LCS with path reconstruction
    public String lcsWithPath(String text1, String text2) {
        int m = text1.length();
        int n = text2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        // Fill DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        // Reconstruct path
        StringBuilder result = new StringBuilder();
        int i = m, j = n;
        
        while (i > 0 && j > 0) {
            if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                result.append(text1.charAt(i - 1));
                i--;
                j--;
            } else if (dp[i - 1][j] > dp[i][j - 1]) {
                i--;
            } else {
                j--;
            }
        }
        
        return result.reverse().toString();
    }
}
```

### Longest Increasing Subsequence (LIS)

```java
public class LongestIncreasingSubsequence {
    // O(n²) solution
    public int lis(int[] nums) {
        int n = nums.length;
        int[] dp = new int[n];
        Arrays.fill(dp, 1);
        
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
        }
        
        return Arrays.stream(dp).max().orElse(0);
    }
    
    // O(n log n) solution with binary search
    public int lisOptimized(int[] nums) {
        List<Integer> tails = new ArrayList<>();
        
        for (int num : nums) {
            int pos = binarySearch(tails, num);
            if (pos == tails.size()) {
                tails.add(num);
            } else {
                tails.set(pos, num);
            }
        }
        
        return tails.size();
    }
    
    private int binarySearch(List<Integer> tails, int target) {
        int left = 0, right = tails.size();
        
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (tails.get(mid) < target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        
        return left;
    }
}
```

## 9.5 Knapsack Problems (0/1, Fractional, Multiple)

### 0/1 Knapsack

```java
public class ZeroOneKnapsack {
    public int knapsack(int[] weights, int[] values, int capacity) {
        int n = weights.length;
        int[][] dp = new int[n + 1][capacity + 1];
        
        for (int i = 1; i <= n; i++) {
            for (int w = 1; w <= capacity; w++) {
                if (weights[i - 1] <= w) {
                    dp[i][w] = Math.max(
                        values[i - 1] + dp[i - 1][w - weights[i - 1]],
                        dp[i - 1][w]
                    );
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }
        
        return dp[n][capacity];
    }
    
    // Space optimized version
    public int knapsackOptimized(int[] weights, int[] values, int capacity) {
        int[] dp = new int[capacity + 1];
        
        for (int i = 0; i < weights.length; i++) {
            for (int w = capacity; w >= weights[i]; w--) {
                dp[w] = Math.max(dp[w], dp[w - weights[i]] + values[i]);
            }
        }
        
        return dp[capacity];
    }
}
```

### Fractional Knapsack

```java
public class FractionalKnapsack {
    private class Item {
        int weight;
        int value;
        double ratio;
        
        public Item(int weight, int value) {
            this.weight = weight;
            this.value = value;
            this.ratio = (double) value / weight;
        }
    }
    
    public double fractionalKnapsack(int[] weights, int[] values, int capacity) {
        List<Item> items = new ArrayList<>();
        
        for (int i = 0; i < weights.length; i++) {
            items.add(new Item(weights[i], values[i]));
        }
        
        // Sort by value-to-weight ratio in descending order
        items.sort((a, b) -> Double.compare(b.ratio, a.ratio));
        
        double totalValue = 0;
        int remainingCapacity = capacity;
        
        for (Item item : items) {
            if (remainingCapacity >= item.weight) {
                // Take the entire item
                totalValue += item.value;
                remainingCapacity -= item.weight;
            } else {
                // Take a fraction of the item
                totalValue += item.ratio * remainingCapacity;
                break;
            }
        }
        
        return totalValue;
    }
}
```

## 9.6 Matrix Chain Multiplication

```java
public class MatrixChainMultiplication {
    public int matrixChainOrder(int[] dimensions) {
        int n = dimensions.length - 1;
        int[][] dp = new int[n][n];
        
        // Fill diagonal with 0s (cost of multiplying single matrix)
        for (int i = 0; i < n; i++) {
            dp[i][i] = 0;
        }
        
        // Fill the table
        for (int length = 2; length <= n; length++) {
            for (int i = 0; i < n - length + 1; i++) {
                int j = i + length - 1;
                dp[i][j] = Integer.MAX_VALUE;
                
                for (int k = i; k < j; k++) {
                    int cost = dp[i][k] + dp[k + 1][j] + 
                              dimensions[i] * dimensions[k + 1] * dimensions[j + 1];
                    
                    if (cost < dp[i][j]) {
                        dp[i][j] = cost;
                    }
                }
            }
        }
        
        return dp[0][n - 1];
    }
    
    // With parenthesization
    public String matrixChainOrderWithParentheses(int[] dimensions) {
        int n = dimensions.length - 1;
        int[][] dp = new int[n][n];
        int[][] split = new int[n][n];
        
        // Fill diagonal with 0s
        for (int i = 0; i < n; i++) {
            dp[i][i] = 0;
        }
        
        // Fill the table
        for (int length = 2; length <= n; length++) {
            for (int i = 0; i < n - length + 1; i++) {
                int j = i + length - 1;
                dp[i][j] = Integer.MAX_VALUE;
                
                for (int k = i; k < j; k++) {
                    int cost = dp[i][k] + dp[k + 1][j] + 
                              dimensions[i] * dimensions[k + 1] * dimensions[j + 1];
                    
                    if (cost < dp[i][j]) {
                        dp[i][j] = cost;
                        split[i][j] = k;
                    }
                }
            }
        }
        
        return printParentheses(split, 0, n - 1);
    }
    
    private String printParentheses(int[][] split, int i, int j) {
        if (i == j) {
            return "A" + i;
        }
        
        return "(" + printParentheses(split, i, split[i][j]) + 
               printParentheses(split, split[i][j] + 1, j) + ")";
    }
}
```

## 9.7 Edit Distance & String Alignment

### Levenshtein Distance

```java
public class EditDistance {
    public int levenshteinDistance(String word1, String word2) {
        int m = word1.length();
        int n = word2.length();
        int[][] dp = new int[m + 1][n + 1];
        
        // Initialize base cases
        for (int i = 0; i <= m; i++) {
            dp[i][0] = i;
        }
        for (int j = 0; j <= n; j++) {
            dp[0][j] = j;
        }
        
        // Fill the DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(
                        Math.min(dp[i - 1][j], dp[i][j - 1]),
                        dp[i - 1][j - 1]
                    );
                }
            }
        }
        
        return dp[m][n];
    }
    
    // Space optimized version
    public int levenshteinDistanceOptimized(String word1, String word2) {
        int m = word1.length();
        int n = word2.length();
        
        if (m < n) {
            return levenshteinDistanceOptimized(word2, word1);
        }
        
        int[] prev = new int[n + 1];
        int[] curr = new int[n + 1];
        
        for (int j = 0; j <= n; j++) {
            prev[j] = j;
        }
        
        for (int i = 1; i <= m; i++) {
            curr[0] = i;
            for (int j = 1; j <= n; j++) {
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    curr[j] = prev[j - 1];
                } else {
                    curr[j] = 1 + Math.min(
                        Math.min(prev[j], curr[j - 1]),
                        prev[j - 1]
                    );
                }
            }
            prev = curr.clone();
        }
        
        return prev[n];
    }
}
```

## 9.8 Advanced DP Patterns & Techniques

### State Machine DP

```java
public class StateMachineDP {
    // Buy and Sell Stock with Cooldown
    public int maxProfit(int[] prices) {
        int n = prices.length;
        if (n <= 1) return 0;
        
        int[] hold = new int[n];
        int[] sold = new int[n];
        int[] rest = new int[n];
        
        hold[0] = -prices[0];
        sold[0] = 0;
        rest[0] = 0;
        
        for (int i = 1; i < n; i++) {
            hold[i] = Math.max(hold[i - 1], rest[i - 1] - prices[i]);
            sold[i] = hold[i - 1] + prices[i];
            rest[i] = Math.max(rest[i - 1], sold[i - 1]);
        }
        
        return Math.max(sold[n - 1], rest[n - 1]);
    }
}
```

### Digit DP

```java
public class DigitDP {
    // Count numbers with digit sum equal to target
    public int countNumbersWithDigitSum(String num, int target) {
        int n = num.length();
        int[][][] dp = new int[n][target + 1][2];
        
        for (int i = 0; i < n; i++) {
            for (int j = 0; j <= target; j++) {
                for (int k = 0; k < 2; k++) {
                    dp[i][j][k] = -1;
                }
            }
        }
        
        return countNumbers(num, 0, target, 0, dp);
    }
    
    private int countNumbers(String num, int pos, int target, int tight, int[][][] dp) {
        if (pos == num.length()) {
            return target == 0 ? 1 : 0;
        }
        
        if (dp[pos][target][tight] != -1) {
            return dp[pos][target][tight];
        }
        
        int limit = tight == 1 ? num.charAt(pos) - '0' : 9;
        int count = 0;
        
        for (int digit = 0; digit <= limit; digit++) {
            if (target >= digit) {
                int newTight = (tight == 1 && digit == limit) ? 1 : 0;
                count += countNumbers(num, pos + 1, target - digit, newTight, dp);
            }
        }
        
        return dp[pos][target][tight] = count;
    }
}
```

**Real-world Analogies:**
- **Dynamic Programming:** Like solving a complex puzzle by breaking it into smaller pieces and remembering solutions
- **Memoization:** Like keeping a notebook of solved problems to avoid re-solving them
- **Tabulation:** Like building a solution from the ground up, step by step
- **Optimal Substructure:** Like finding the best route by combining the best sub-routes
- **Overlapping Subproblems:** Like solving the same math problem multiple times in different contexts
- **Knapsack Problem:** Like packing a suitcase with the most valuable items within weight limit
- **Edit Distance:** Like measuring how many changes needed to transform one word into another
- **Matrix Chain Multiplication:** Like finding the most efficient way to multiply a chain of matrices

Dynamic Programming is a powerful technique for solving optimization problems by breaking them down into simpler subproblems and storing solutions to avoid redundant calculations.