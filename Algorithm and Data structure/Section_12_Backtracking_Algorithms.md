# Section 12 – Backtracking Algorithms

## 12.1 Backtracking Principles

Backtracking is a systematic way to explore all possible solutions to a problem by building solutions incrementally and abandoning partial solutions that cannot lead to a complete solution.

### Core Concepts

Backtracking follows these key principles:

1. **Incremental Construction**: Build solutions step by step
2. **Constraint Checking**: Verify if current partial solution is valid
3. **Pruning**: Abandon paths that cannot lead to valid solutions
4. **Recursive Exploration**: Use recursion to explore all possibilities
5. **Backtracking**: Undo previous choices when they don't work

**Real-world Analogy:**
Think of solving a maze by marking your path with chalk. When you reach a dead end, you erase your marks back to the last decision point and try a different path. This is exactly how backtracking works - it explores all possible paths and "backtracks" when it hits a dead end.

### Backtracking Template

```java
public class BacktrackingTemplate {
    public void backtrack(State currentState, List<State> solution) {
        // Base case: check if current state is a complete solution
        if (isCompleteSolution(currentState)) {
            processSolution(currentState);
            return;
        }
        
        // Generate all possible next states
        List<State> nextStates = generateNextStates(currentState);
        
        // Try each possible next state
        for (State nextState : nextStates) {
            // Check if this state is valid
            if (isValidState(nextState)) {
                // Make the choice
                makeChoice(nextState);
                solution.add(nextState);
                
                // Recursively explore this path
                backtrack(nextState, solution);
                
                // Backtrack: undo the choice
                undoChoice(nextState);
                solution.remove(solution.size() - 1);
            }
        }
    }
    
    private boolean isCompleteSolution(State state) {
        // Check if current state represents a complete solution
        return state.isComplete();
    }
    
    private List<State> generateNextStates(State currentState) {
        // Generate all possible next states from current state
        return currentState.getNextStates();
    }
    
    private boolean isValidState(State state) {
        // Check if state satisfies all constraints
        return state.isValid();
    }
    
    private void makeChoice(State state) {
        // Apply the choice to the state
        state.applyChoice();
    }
    
    private void undoChoice(State state) {
        // Undo the choice from the state
        state.undoChoice();
    }
    
    private void processSolution(State state) {
        // Process a complete solution (print, count, etc.)
        System.out.println("Solution found: " + state);
    }
}
```

### When to Use Backtracking

**Characteristics of Backtracking Problems:**
- Multiple possible solutions exist
- Need to find all solutions or any valid solution
- Problem can be broken down into smaller subproblems
- Constraints can be checked incrementally
- Solutions are built incrementally

**Common Applications:**
- Puzzle solving (N-Queens, Sudoku)
- Path finding (Maze solving)
- Combinatorial problems (Permutations, Subsets)
- Constraint satisfaction problems
- Game playing algorithms

## 12.2 N-Queens Problem

The N-Queens problem is a classic backtracking problem where we place N queens on an N×N chessboard such that no two queens attack each other.

### Problem Statement

Place N queens on an N×N chessboard so that no two queens are in the same row, column, or diagonal.

### Basic N-Queens Solution

```java
public class NQueens {
    private int n;
    private int[] queens; // queens[i] = column of queen in row i
    private List<int[]> solutions;
    
    public NQueens(int n) {
        this.n = n;
        this.queens = new int[n];
        this.solutions = new ArrayList<>();
    }
    
    public List<int[]> solve() {
        solveNQueens(0);
        return solutions;
    }
    
    private void solveNQueens(int row) {
        // Base case: all queens placed
        if (row == n) {
            solutions.add(queens.clone());
            return;
        }
        
        // Try placing queen in each column of current row
        for (int col = 0; col < n; col++) {
            if (isSafe(row, col)) {
                // Place queen
                queens[row] = col;
                
                // Recursively place queens in remaining rows
                solveNQueens(row + 1);
                
                // Backtrack: remove queen (not needed as we overwrite in next iteration)
            }
        }
    }
    
    private boolean isSafe(int row, int col) {
        // Check if placing queen at (row, col) is safe
        for (int i = 0; i < row; i++) {
            // Check same column
            if (queens[i] == col) {
                return false;
            }
            
            // Check diagonals
            if (Math.abs(queens[i] - col) == Math.abs(i - row)) {
                return false;
            }
        }
        
        return true;
    }
    
    public void printSolutions() {
        for (int[] solution : solutions) {
            printBoard(solution);
            System.out.println();
        }
    }
    
    private void printBoard(int[] queens) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (queens[i] == j) {
                    System.out.print("Q ");
                } else {
                    System.out.print(". ");
                }
            }
            System.out.println();
        }
    }
}
```

### Optimized N-Queens with Bit Manipulation

```java
public class OptimizedNQueens {
    private int n;
    private int solutions;
    
    public OptimizedNQueens(int n) {
        this.n = n;
        this.solutions = 0;
    }
    
    public int countSolutions() {
        solveNQueens(0, 0, 0, 0);
        return solutions;
    }
    
    private void solveNQueens(int row, int cols, int diag1, int diag2) {
        // Base case: all queens placed
        if (row == n) {
            solutions++;
            return;
        }
        
        // Get available positions (bits set to 1 represent available columns)
        int available = ((1 << n) - 1) & (~(cols | diag1 | diag2));
        
        // Try each available position
        while (available != 0) {
            // Get rightmost set bit
            int pos = available & (-available);
            
            // Remove this position from available
            available -= pos;
            
            // Calculate column index
            int col = Integer.numberOfTrailingZeros(pos);
            
            // Recursively place queens in remaining rows
            solveNQueens(row + 1, 
                        cols | pos, 
                        (diag1 | pos) << 1, 
                        (diag2 | pos) >> 1);
        }
    }
}
```

### Performance Analysis

**Time Complexity:**
- **Worst Case:** O(N!) - exponential
- **Average Case:** Much better due to pruning
- **Space Complexity:** O(N) for recursion stack

**Optimizations:**
- Bit manipulation for faster constraint checking
- Symmetry breaking to avoid duplicate solutions
- Early termination when solution found

## 12.3 Sudoku Solver

Sudoku is a number-placement puzzle where we fill a 9×9 grid with digits so that each row, column, and 3×3 subgrid contains all digits from 1 to 9.

### Basic Sudoku Solver

```java
public class SudokuSolver {
    private static final int SIZE = 9;
    private static final int EMPTY = 0;
    
    public boolean solveSudoku(int[][] board) {
        return solveSudoku(board, 0, 0);
    }
    
    private boolean solveSudoku(int[][] board, int row, int col) {
        // Base case: if we've filled all cells
        if (row == SIZE) {
            return true;
        }
        
        // Move to next row if we've filled current row
        if (col == SIZE) {
            return solveSudoku(board, row + 1, 0);
        }
        
        // Skip if cell is already filled
        if (board[row][col] != EMPTY) {
            return solveSudoku(board, row, col + 1);
        }
        
        // Try each digit from 1 to 9
        for (int digit = 1; digit <= 9; digit++) {
            if (isValidMove(board, row, col, digit)) {
                // Make the choice
                board[row][col] = digit;
                
                // Recursively solve the rest
                if (solveSudoku(board, row, col + 1)) {
                    return true;
                }
                
                // Backtrack: undo the choice
                board[row][col] = EMPTY;
            }
        }
        
        return false;
    }
    
    private boolean isValidMove(int[][] board, int row, int col, int digit) {
        // Check row
        for (int c = 0; c < SIZE; c++) {
            if (board[row][c] == digit) {
                return false;
            }
        }
        
        // Check column
        for (int r = 0; r < SIZE; r++) {
            if (board[r][col] == digit) {
                return false;
            }
        }
        
        // Check 3x3 subgrid
        int startRow = (row / 3) * 3;
        int startCol = (col / 3) * 3;
        
        for (int r = startRow; r < startRow + 3; r++) {
            for (int c = startCol; c < startCol + 3; c++) {
                if (board[r][c] == digit) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    public void printBoard(int[][] board) {
        for (int i = 0; i < SIZE; i++) {
            if (i % 3 == 0 && i != 0) {
                System.out.println("-----------");
            }
            for (int j = 0; j < SIZE; j++) {
                if (j % 3 == 0 && j != 0) {
                    System.out.print("|");
                }
                System.out.print(board[i][j] == EMPTY ? "." : board[i][j]);
            }
            System.out.println();
        }
    }
}
```

### Optimized Sudoku Solver

```java
public class OptimizedSudokuSolver {
    private static final int SIZE = 9;
    private static final int EMPTY = 0;
    
    public boolean solveSudoku(int[][] board) {
        // Find the cell with minimum possibilities
        int[] cell = findBestCell(board);
        if (cell[0] == -1) {
            return true; // All cells filled
        }
        
        int row = cell[0];
        int col = cell[1];
        
        // Try each possible digit for this cell
        for (int digit = 1; digit <= 9; digit++) {
            if (isValidMove(board, row, col, digit)) {
                board[row][col] = digit;
                
                if (solveSudoku(board)) {
                    return true;
                }
                
                board[row][col] = EMPTY;
            }
        }
        
        return false;
    }
    
    private int[] findBestCell(int[][] board) {
        int minPossibilities = 10;
        int[] bestCell = {-1, -1};
        
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                if (board[i][j] == EMPTY) {
                    int possibilities = countPossibilities(board, i, j);
                    if (possibilities < minPossibilities) {
                        minPossibilities = possibilities;
                        bestCell[0] = i;
                        bestCell[1] = j;
                    }
                }
            }
        }
        
        return bestCell;
    }
    
    private int countPossibilities(int[][] board, int row, int col) {
        int count = 0;
        for (int digit = 1; digit <= 9; digit++) {
            if (isValidMove(board, row, col, digit)) {
                count++;
            }
        }
        return count;
    }
    
    private boolean isValidMove(int[][] board, int row, int col, int digit) {
        // Check row
        for (int c = 0; c < SIZE; c++) {
            if (board[row][c] == digit) {
                return false;
            }
        }
        
        // Check column
        for (int r = 0; r < SIZE; r++) {
            if (board[r][col] == digit) {
                return false;
            }
        }
        
        // Check 3x3 subgrid
        int startRow = (row / 3) * 3;
        int startCol = (col / 3) * 3;
        
        for (int r = startRow; r < startRow + 3; r++) {
            for (int c = startCol; c < startCol + 3; c++) {
                if (board[r][c] == digit) {
                    return false;
                }
            }
        }
        
        return true;
    }
}
```

## 12.4 Graph Coloring

Graph coloring is the problem of assigning colors to vertices of a graph such that no two adjacent vertices have the same color.

### Problem Statement

Given a graph G and a number of colors k, determine if the graph can be colored with at most k colors such that no two adjacent vertices have the same color.

### Basic Graph Coloring

```java
public class GraphColoring {
    private int[][] graph;
    private int[] colors;
    private int numVertices;
    private int numColors;
    
    public GraphColoring(int[][] graph, int numColors) {
        this.graph = graph;
        this.numVertices = graph.length;
        this.numColors = numColors;
        this.colors = new int[numVertices];
    }
    
    public boolean colorGraph() {
        return colorGraph(0);
    }
    
    private boolean colorGraph(int vertex) {
        // Base case: all vertices colored
        if (vertex == numVertices) {
            return true;
        }
        
        // Try each color for current vertex
        for (int color = 1; color <= numColors; color++) {
            if (isValidColor(vertex, color)) {
                // Assign color
                colors[vertex] = color;
                
                // Recursively color remaining vertices
                if (colorGraph(vertex + 1)) {
                    return true;
                }
                
                // Backtrack: remove color
                colors[vertex] = 0;
            }
        }
        
        return false;
    }
    
    private boolean isValidColor(int vertex, int color) {
        // Check if color is valid for this vertex
        for (int i = 0; i < numVertices; i++) {
            if (graph[vertex][i] == 1 && colors[i] == color) {
                return false; // Adjacent vertex has same color
            }
        }
        return true;
    }
    
    public void printColoring() {
        for (int i = 0; i < numVertices; i++) {
            System.out.println("Vertex " + i + " -> Color " + colors[i]);
        }
    }
}
```

### M-Coloring Problem (Find All Solutions)

```java
public class MColoringAllSolutions {
    private int[][] graph;
    private int[] colors;
    private int numVertices;
    private int numColors;
    private List<int[]> solutions;
    
    public MColoringAllSolutions(int[][] graph, int numColors) {
        this.graph = graph;
        this.numVertices = graph.length;
        this.numColors = numColors;
        this.colors = new int[numVertices];
        this.solutions = new ArrayList<>();
    }
    
    public List<int[]> findAllColorings() {
        colorGraph(0);
        return solutions;
    }
    
    private void colorGraph(int vertex) {
        // Base case: all vertices colored
        if (vertex == numVertices) {
            solutions.add(colors.clone());
            return;
        }
        
        // Try each color for current vertex
        for (int color = 1; color <= numColors; color++) {
            if (isValidColor(vertex, color)) {
                // Assign color
                colors[vertex] = color;
                
                // Recursively color remaining vertices
                colorGraph(vertex + 1);
                
                // Backtrack: remove color
                colors[vertex] = 0;
            }
        }
    }
    
    private boolean isValidColor(int vertex, int color) {
        for (int i = 0; i < numVertices; i++) {
            if (graph[vertex][i] == 1 && colors[i] == color) {
                return false;
            }
        }
        return true;
    }
}
```

## 12.5 Hamiltonian Path/Cycle

A Hamiltonian path visits each vertex exactly once, while a Hamiltonian cycle is a Hamiltonian path that starts and ends at the same vertex.

### Hamiltonian Path

```java
public class HamiltonianPath {
    private int[][] graph;
    private int numVertices;
    private boolean[] visited;
    private int[] path;
    
    public HamiltonianPath(int[][] graph) {
        this.graph = graph;
        this.numVertices = graph.length;
        this.visited = new boolean[numVertices];
        this.path = new int[numVertices];
    }
    
    public boolean hasHamiltonianPath() {
        // Try starting from each vertex
        for (int start = 0; start < numVertices; start++) {
            Arrays.fill(visited, false);
            path[0] = start;
            visited[start] = true;
            
            if (findHamiltonianPath(1)) {
                return true;
            }
        }
        return false;
    }
    
    private boolean findHamiltonianPath(int pathLength) {
        // Base case: all vertices visited
        if (pathLength == numVertices) {
            return true;
        }
        
        // Try each unvisited vertex
        for (int v = 0; v < numVertices; v++) {
            if (!visited[v] && graph[path[pathLength - 1]][v] == 1) {
                // Add vertex to path
                path[pathLength] = v;
                visited[v] = true;
                
                // Recursively find remaining path
                if (findHamiltonianPath(pathLength + 1)) {
                    return true;
                }
                
                // Backtrack: remove vertex from path
                visited[v] = false;
            }
        }
        
        return false;
    }
    
    public void printPath() {
        if (hasHamiltonianPath()) {
            System.out.print("Hamiltonian Path: ");
            for (int i = 0; i < numVertices; i++) {
                System.out.print(path[i] + " ");
            }
            System.out.println();
        } else {
            System.out.println("No Hamiltonian Path exists");
        }
    }
}
```

### Hamiltonian Cycle

```java
public class HamiltonianCycle {
    private int[][] graph;
    private int numVertices;
    private boolean[] visited;
    private int[] path;
    
    public HamiltonianCycle(int[][] graph) {
        this.graph = graph;
        this.numVertices = graph.length;
        this.visited = new boolean[numVertices];
        this.path = new int[numVertices];
    }
    
    public boolean hasHamiltonianCycle() {
        // Start from vertex 0
        path[0] = 0;
        visited[0] = true;
        
        return findHamiltonianCycle(1);
    }
    
    private boolean findHamiltonianCycle(int pathLength) {
        // Base case: all vertices visited
        if (pathLength == numVertices) {
            // Check if last vertex connects to first vertex
            return graph[path[pathLength - 1]][path[0]] == 1;
        }
        
        // Try each unvisited vertex
        for (int v = 1; v < numVertices; v++) {
            if (!visited[v] && graph[path[pathLength - 1]][v] == 1) {
                // Add vertex to path
                path[pathLength] = v;
                visited[v] = true;
                
                // Recursively find remaining path
                if (findHamiltonianCycle(pathLength + 1)) {
                    return true;
                }
                
                // Backtrack: remove vertex from path
                visited[v] = false;
            }
        }
        
        return false;
    }
    
    public void printCycle() {
        if (hasHamiltonianCycle()) {
            System.out.print("Hamiltonian Cycle: ");
            for (int i = 0; i < numVertices; i++) {
                System.out.print(path[i] + " ");
            }
            System.out.println(path[0]); // Complete the cycle
        } else {
            System.out.println("No Hamiltonian Cycle exists");
        }
    }
}
```

## 12.6 Subset Generation

Generate all possible subsets of a given set.

### Recursive Subset Generation

```java
public class SubsetGeneration {
    public List<List<Integer>> generateSubsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        generateSubsets(nums, 0, new ArrayList<>(), result);
        return result;
    }
    
    private void generateSubsets(int[] nums, int index, List<Integer> current, List<List<Integer>> result) {
        // Base case: processed all elements
        if (index == nums.length) {
            result.add(new ArrayList<>(current));
            return;
        }
        
        // Include current element
        current.add(nums[index]);
        generateSubsets(nums, index + 1, current, result);
        
        // Exclude current element (backtrack)
        current.remove(current.size() - 1);
        generateSubsets(nums, index + 1, current, result);
    }
    
    public void printSubsets(int[] nums) {
        List<List<Integer>> subsets = generateSubsets(nums);
        for (List<Integer> subset : subsets) {
            System.out.println(subset);
        }
    }
}
```

### Bit Manipulation Approach

```java
public class SubsetGenerationBitwise {
    public List<List<Integer>> generateSubsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        int n = nums.length;
        int totalSubsets = 1 << n; // 2^n
        
        for (int i = 0; i < totalSubsets; i++) {
            List<Integer> subset = new ArrayList<>();
            for (int j = 0; j < n; j++) {
                if ((i & (1 << j)) != 0) {
                    subset.add(nums[j]);
                }
            }
            result.add(subset);
        }
        
        return result;
    }
}
```

## 12.7 Permutation Generation

Generate all possible permutations of a given set.

### Recursive Permutation Generation

```java
public class PermutationGeneration {
    public List<List<Integer>> generatePermutations(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        generatePermutations(nums, 0, result);
        return result;
    }
    
    private void generatePermutations(int[] nums, int index, List<List<Integer>> result) {
        // Base case: all elements placed
        if (index == nums.length) {
            List<Integer> permutation = new ArrayList<>();
            for (int num : nums) {
                permutation.add(num);
            }
            result.add(permutation);
            return;
        }
        
        // Try each element at current position
        for (int i = index; i < nums.length; i++) {
            // Swap elements
            swap(nums, index, i);
            
            // Recursively generate permutations for remaining positions
            generatePermutations(nums, index + 1, result);
            
            // Backtrack: restore original order
            swap(nums, index, i);
        }
    }
    
    private void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
    
    public void printPermutations(int[] nums) {
        List<List<Integer>> permutations = generatePermutations(nums);
        for (List<Integer> permutation : permutations) {
            System.out.println(permutation);
        }
    }
}
```

### Lexicographic Permutation Generation

```java
public class LexicographicPermutations {
    public List<List<Integer>> generatePermutations(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        Arrays.sort(nums); // Start with sorted array
        
        do {
            List<Integer> permutation = new ArrayList<>();
            for (int num : nums) {
                permutation.add(num);
            }
            result.add(permutation);
        } while (nextPermutation(nums));
        
        return result;
    }
    
    private boolean nextPermutation(int[] nums) {
        int i = nums.length - 2;
        
        // Find largest index i such that nums[i] < nums[i + 1]
        while (i >= 0 && nums[i] >= nums[i + 1]) {
            i--;
        }
        
        if (i < 0) {
            return false; // No more permutations
        }
        
        // Find largest index j such that nums[i] < nums[j]
        int j = nums.length - 1;
        while (nums[j] <= nums[i]) {
            j--;
        }
        
        // Swap nums[i] and nums[j]
        swap(nums, i, j);
        
        // Reverse suffix starting at nums[i + 1]
        reverse(nums, i + 1, nums.length - 1);
        
        return true;
    }
    
    private void swap(int[] nums, int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }
    
    private void reverse(int[] nums, int start, int end) {
        while (start < end) {
            swap(nums, start, end);
            start++;
            end--;
        }
    }
}
```

## 12.8 Constraint Satisfaction Problems

Constraint Satisfaction Problems (CSP) involve finding values for variables that satisfy a set of constraints.

### Generic CSP Solver

```java
public class CSPSolver {
    private Map<String, List<Object>> variables;
    private List<Constraint> constraints;
    private Map<String, Object> assignment;
    
    public CSPSolver(Map<String, List<Object>> variables, List<Constraint> constraints) {
        this.variables = variables;
        this.constraints = constraints;
        this.assignment = new HashMap<>();
    }
    
    public Map<String, Object> solve() {
        if (backtrack()) {
            return assignment;
        }
        return null; // No solution found
    }
    
    private boolean backtrack() {
        // Check if assignment is complete
        if (assignment.size() == variables.size()) {
            return true;
        }
        
        // Select unassigned variable
        String variable = selectUnassignedVariable();
        
        // Try each value in variable's domain
        for (Object value : variables.get(variable)) {
            // Check if value is consistent with constraints
            if (isConsistent(variable, value)) {
                // Make assignment
                assignment.put(variable, value);
                
                // Recursively solve remaining variables
                if (backtrack()) {
                    return true;
                }
                
                // Backtrack: remove assignment
                assignment.remove(variable);
            }
        }
        
        return false;
    }
    
    private String selectUnassignedVariable() {
        // Select first unassigned variable (can be optimized with MRV heuristic)
        for (String variable : variables.keySet()) {
            if (!assignment.containsKey(variable)) {
                return variable;
            }
        }
        return null;
    }
    
    private boolean isConsistent(String variable, Object value) {
        // Check all constraints involving this variable
        for (Constraint constraint : constraints) {
            if (constraint.involves(variable) && !constraint.isSatisfied(assignment, variable, value)) {
                return false;
            }
        }
        return true;
    }
}

// Constraint interface
interface Constraint {
    boolean involves(String variable);
    boolean isSatisfied(Map<String, Object> assignment, String variable, Object value);
}

// Example: AllDifferent constraint
class AllDifferentConstraint implements Constraint {
    private List<String> variables;
    
    public AllDifferentConstraint(List<String> variables) {
        this.variables = variables;
    }
    
    @Override
    public boolean involves(String variable) {
        return variables.contains(variable);
    }
    
    @Override
    public boolean isSatisfied(Map<String, Object> assignment, String variable, Object value) {
        // Check if any other variable in this constraint has the same value
        for (String otherVar : variables) {
            if (!otherVar.equals(variable) && assignment.containsKey(otherVar)) {
                if (assignment.get(otherVar).equals(value)) {
                    return false;
                }
            }
        }
        return true;
    }
}
```

### Map Coloring CSP Example

```java
public class MapColoringCSP {
    public static void main(String[] args) {
        // Variables: regions to color
        Map<String, List<Object>> variables = new HashMap<>();
        variables.put("WA", Arrays.asList("Red", "Green", "Blue"));
        variables.put("NT", Arrays.asList("Red", "Green", "Blue"));
        variables.put("SA", Arrays.asList("Red", "Green", "Blue"));
        variables.put("Q", Arrays.asList("Red", "Green", "Blue"));
        variables.put("NSW", Arrays.asList("Red", "Green", "Blue"));
        variables.put("V", Arrays.asList("Red", "Green", "Blue"));
        variables.put("T", Arrays.asList("Red", "Green", "Blue"));
        
        // Constraints: adjacent regions must have different colors
        List<Constraint> constraints = new ArrayList<>();
        constraints.add(new AllDifferentConstraint(Arrays.asList("WA", "NT")));
        constraints.add(new AllDifferentConstraint(Arrays.asList("WA", "SA")));
        constraints.add(new AllDifferentConstraint(Arrays.asList("NT", "SA")));
        constraints.add(new AllDifferentConstraint(Arrays.asList("NT", "Q")));
        constraints.add(new AllDifferentConstraint(Arrays.asList("SA", "Q")));
        constraints.add(new AllDifferentConstraint(Arrays.asList("SA", "NSW")));
        constraints.add(new AllDifferentConstraint(Arrays.asList("SA", "V")));
        constraints.add(new AllDifferentConstraint(Arrays.asList("Q", "NSW")));
        constraints.add(new AllDifferentConstraint(Arrays.asList("NSW", "V")));
        
        // Solve CSP
        CSPSolver solver = new CSPSolver(variables, constraints);
        Map<String, Object> solution = solver.solve();
        
        if (solution != null) {
            System.out.println("Map coloring solution:");
            for (Map.Entry<String, Object> entry : solution.entrySet()) {
                System.out.println(entry.getKey() + " -> " + entry.getValue());
            }
        } else {
            System.out.println("No solution found");
        }
    }
}
```

**Real-world Analogies:**
- **Backtracking:** Like solving a maze by trying different paths and going back when you hit a dead end
- **N-Queens:** Like placing queens on a chessboard so they don't attack each other
- **Sudoku:** Like filling a number puzzle by trying different numbers and erasing when they don't work
- **Graph Coloring:** Like coloring a map so adjacent countries have different colors
- **Hamiltonian Path:** Like visiting every city exactly once on a road trip
- **Subset Generation:** Like choosing different combinations of items from a menu
- **Permutation Generation:** Like arranging people in different orders for a photo
- **Constraint Satisfaction:** Like solving a puzzle where each piece must fit certain rules

Backtracking is a powerful technique for solving problems that require exploring all possible solutions. The key is to efficiently prune invalid paths and systematically explore the solution space.