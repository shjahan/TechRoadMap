# Section 4 – Tree Data Structures

## 4.1 Binary Trees

Binary trees are hierarchical data structures where each node has at most two children.

### Binary Tree Node

```java
public class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    
    public TreeNode(int val) {
        this.val = val;
        this.left = null;
        this.right = null;
    }
}
```

### Basic Binary Tree Operations

```java
public class BinaryTree {
    private TreeNode root;
    
    public BinaryTree() {
        this.root = null;
    }
    
    // Insert a node
    public void insert(int val) {
        root = insertRecursive(root, val);
    }
    
    private TreeNode insertRecursive(TreeNode node, int val) {
        if (node == null) {
            return new TreeNode(val);
        }
        
        if (val < node.val) {
            node.left = insertRecursive(node.left, val);
        } else if (val > node.val) {
            node.right = insertRecursive(node.right, val);
        }
        
        return node;
    }
    
    // Search for a value
    public boolean search(int val) {
        return searchRecursive(root, val);
    }
    
    private boolean searchRecursive(TreeNode node, int val) {
        if (node == null) return false;
        if (node.val == val) return true;
        
        return searchRecursive(node.left, val) || searchRecursive(node.right, val);
    }
    
    // Get height of tree
    public int height() {
        return heightRecursive(root);
    }
    
    private int heightRecursive(TreeNode node) {
        if (node == null) return -1;
        
        int leftHeight = heightRecursive(node.left);
        int rightHeight = heightRecursive(node.right);
        
        return Math.max(leftHeight, rightHeight) + 1;
    }
    
    // Count nodes
    public int countNodes() {
        return countNodesRecursive(root);
    }
    
    private int countNodesRecursive(TreeNode node) {
        if (node == null) return 0;
        return 1 + countNodesRecursive(node.left) + countNodesRecursive(node.right);
    }
}
```

## 4.2 Binary Search Trees (BST)

BSTs maintain the property that left child < parent < right child.

### BST Implementation

```java
public class BinarySearchTree {
    private TreeNode root;
    
    public BinarySearchTree() {
        this.root = null;
    }
    
    // Insert maintaining BST property
    public void insert(int val) {
        root = insertRecursive(root, val);
    }
    
    private TreeNode insertRecursive(TreeNode node, int val) {
        if (node == null) {
            return new TreeNode(val);
        }
        
        if (val < node.val) {
            node.left = insertRecursive(node.left, val);
        } else if (val > node.val) {
            node.right = insertRecursive(node.right, val);
        }
        
        return node;
    }
    
    // Search in BST
    public boolean search(int val) {
        return searchRecursive(root, val);
    }
    
    private boolean searchRecursive(TreeNode node, int val) {
        if (node == null) return false;
        if (node.val == val) return true;
        
        if (val < node.val) {
            return searchRecursive(node.left, val);
        } else {
            return searchRecursive(node.right, val);
        }
    }
    
    // Delete node
    public void delete(int val) {
        root = deleteRecursive(root, val);
    }
    
    private TreeNode deleteRecursive(TreeNode node, int val) {
        if (node == null) return null;
        
        if (val < node.val) {
            node.left = deleteRecursive(node.left, val);
        } else if (val > node.val) {
            node.right = deleteRecursive(node.right, val);
        } else {
            // Node to delete found
            if (node.left == null) return node.right;
            if (node.right == null) return node.left;
            
            // Node with two children
            TreeNode minNode = findMin(node.right);
            node.val = minNode.val;
            node.right = deleteRecursive(node.right, minNode.val);
        }
        
        return node;
    }
    
    private TreeNode findMin(TreeNode node) {
        while (node.left != null) {
            node = node.left;
        }
        return node;
    }
}
```

## 4.3 Balanced Trees (AVL, Red-Black)

Balanced trees maintain height balance to ensure O(log n) operations.

### AVL Tree Implementation

```java
public class AVLTree {
    private TreeNode root;
    
    private class TreeNode {
        int val;
        int height;
        TreeNode left;
        TreeNode right;
        
        public TreeNode(int val) {
            this.val = val;
            this.height = 1;
            this.left = null;
            this.right = null;
        }
    }
    
    private int height(TreeNode node) {
        return node == null ? 0 : node.height;
    }
    
    private int getBalance(TreeNode node) {
        return node == null ? 0 : height(node.left) - height(node.right);
    }
    
    private TreeNode rightRotate(TreeNode y) {
        TreeNode x = y.left;
        TreeNode T2 = x.right;
        
        x.right = y;
        y.left = T2;
        
        y.height = Math.max(height(y.left), height(y.right)) + 1;
        x.height = Math.max(height(x.left), height(x.right)) + 1;
        
        return x;
    }
    
    private TreeNode leftRotate(TreeNode x) {
        TreeNode y = x.right;
        TreeNode T2 = y.left;
        
        y.left = x;
        x.right = T2;
        
        x.height = Math.max(height(x.left), height(x.right)) + 1;
        y.height = Math.max(height(y.left), height(y.right)) + 1;
        
        return y;
    }
    
    public void insert(int val) {
        root = insertRecursive(root, val);
    }
    
    private TreeNode insertRecursive(TreeNode node, int val) {
        if (node == null) return new TreeNode(val);
        
        if (val < node.val) {
            node.left = insertRecursive(node.left, val);
        } else if (val > node.val) {
            node.right = insertRecursive(node.right, val);
        } else {
            return node; // Duplicate values not allowed
        }
        
        node.height = 1 + Math.max(height(node.left), height(node.right));
        
        int balance = getBalance(node);
        
        // Left Left Case
        if (balance > 1 && val < node.left.val) {
            return rightRotate(node);
        }
        
        // Right Right Case
        if (balance < -1 && val > node.right.val) {
            return leftRotate(node);
        }
        
        // Left Right Case
        if (balance > 1 && val > node.left.val) {
            node.left = leftRotate(node.left);
            return rightRotate(node);
        }
        
        // Right Left Case
        if (balance < -1 && val < node.right.val) {
            node.right = rightRotate(node.right);
            return leftRotate(node);
        }
        
        return node;
    }
}
```

## 4.4 B-Trees & B+ Trees

B-trees are balanced trees designed for disk storage systems.

### B-Tree Node

```java
public class BTreeNode {
    int[] keys;
    BTreeNode[] children;
    int numKeys;
    boolean isLeaf;
    
    public BTreeNode(int degree, boolean isLeaf) {
        this.keys = new int[2 * degree - 1];
        this.children = new BTreeNode[2 * degree];
        this.numKeys = 0;
        this.isLeaf = isLeaf;
    }
}
```

### B-Tree Implementation

```java
public class BTree {
    private BTreeNode root;
    private int degree;
    
    public BTree(int degree) {
        this.degree = degree;
        this.root = null;
    }
    
    public void insert(int key) {
        if (root == null) {
            root = new BTreeNode(degree, true);
            root.keys[0] = key;
            root.numKeys = 1;
        } else {
            if (root.numKeys == 2 * degree - 1) {
                BTreeNode newRoot = new BTreeNode(degree, false);
                newRoot.children[0] = root;
                splitChild(newRoot, 0);
                root = newRoot;
            }
            insertNonFull(root, key);
        }
    }
    
    private void insertNonFull(BTreeNode node, int key) {
        int i = node.numKeys - 1;
        
        if (node.isLeaf) {
            while (i >= 0 && node.keys[i] > key) {
                node.keys[i + 1] = node.keys[i];
                i--;
            }
            node.keys[i + 1] = key;
            node.numKeys++;
        } else {
            while (i >= 0 && node.keys[i] > key) {
                i--;
            }
            i++;
            
            if (node.children[i].numKeys == 2 * degree - 1) {
                splitChild(node, i);
                if (node.keys[i] < key) {
                    i++;
                }
            }
            insertNonFull(node.children[i], key);
        }
    }
    
    private void splitChild(BTreeNode parent, int index) {
        BTreeNode child = parent.children[index];
        BTreeNode newChild = new BTreeNode(degree, child.isLeaf);
        newChild.numKeys = degree - 1;
        
        for (int j = 0; j < degree - 1; j++) {
            newChild.keys[j] = child.keys[j + degree];
        }
        
        if (!child.isLeaf) {
            for (int j = 0; j < degree; j++) {
                newChild.children[j] = child.children[j + degree];
            }
        }
        
        child.numKeys = degree - 1;
        
        for (int j = parent.numKeys; j >= index + 1; j--) {
            parent.children[j + 1] = parent.children[j];
        }
        
        parent.children[index + 1] = newChild;
        
        for (int j = parent.numKeys - 1; j >= index; j--) {
            parent.keys[j + 1] = parent.keys[j];
        }
        
        parent.keys[index] = child.keys[degree - 1];
        parent.numKeys++;
    }
}
```

## 4.5 Tries (Prefix Trees)

Tries are tree structures optimized for string operations and prefix matching.

### Trie Implementation

```java
public class Trie {
    private TrieNode root;
    
    private class TrieNode {
        TrieNode[] children;
        boolean isEndOfWord;
        
        public TrieNode() {
            this.children = new TrieNode[26]; // For lowercase English letters
            this.isEndOfWord = false;
        }
    }
    
    public Trie() {
        this.root = new TrieNode();
    }
    
    public void insert(String word) {
        TrieNode current = root;
        
        for (char c : word.toCharArray()) {
            int index = c - 'a';
            if (current.children[index] == null) {
                current.children[index] = new TrieNode();
            }
            current = current.children[index];
        }
        
        current.isEndOfWord = true;
    }
    
    public boolean search(String word) {
        TrieNode current = root;
        
        for (char c : word.toCharArray()) {
            int index = c - 'a';
            if (current.children[index] == null) {
                return false;
            }
            current = current.children[index];
        }
        
        return current.isEndOfWord;
    }
    
    public boolean startsWith(String prefix) {
        TrieNode current = root;
        
        for (char c : prefix.toCharArray()) {
            int index = c - 'a';
            if (current.children[index] == null) {
                return false;
            }
            current = current.children[index];
        }
        
        return true;
    }
}
```

## 4.6 Segment Trees

Segment trees enable efficient range queries and updates.

### Segment Tree Implementation

```java
public class SegmentTree {
    private int[] tree;
    private int n;
    
    public SegmentTree(int[] arr) {
        this.n = arr.length;
        this.tree = new int[4 * n];
        build(arr, 0, 0, n - 1);
    }
    
    private void build(int[] arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
        } else {
            int mid = (start + end) / 2;
            build(arr, 2 * node + 1, start, mid);
            build(arr, 2 * node + 2, mid + 1, end);
            tree[node] = tree[2 * node + 1] + tree[2 * node + 2];
        }
    }
    
    public void update(int index, int value) {
        update(0, 0, n - 1, index, value);
    }
    
    private void update(int node, int start, int end, int index, int value) {
        if (start == end) {
            tree[node] = value;
        } else {
            int mid = (start + end) / 2;
            if (index <= mid) {
                update(2 * node + 1, start, mid, index, value);
            } else {
                update(2 * node + 2, mid + 1, end, index, value);
            }
            tree[node] = tree[2 * node + 1] + tree[2 * node + 2];
        }
    }
    
    public int query(int left, int right) {
        return query(0, 0, n - 1, left, right);
    }
    
    private int query(int node, int start, int end, int left, int right) {
        if (right < start || left > end) {
            return 0;
        }
        if (left <= start && end <= right) {
            return tree[node];
        }
        
        int mid = (start + end) / 2;
        int leftSum = query(2 * node + 1, start, mid, left, right);
        int rightSum = query(2 * node + 2, mid + 1, end, left, right);
        return leftSum + rightSum;
    }
}
```

## 4.7 Fenwick Trees (Binary Indexed Trees)

Fenwick trees provide efficient prefix sum operations.

### Fenwick Tree Implementation

```java
public class FenwickTree {
    private int[] tree;
    private int n;
    
    public FenwickTree(int size) {
        this.n = size;
        this.tree = new int[n + 1];
    }
    
    public void update(int index, int delta) {
        index++;
        while (index <= n) {
            tree[index] += delta;
            index += index & -index;
        }
    }
    
    public int query(int index) {
        index++;
        int sum = 0;
        while (index > 0) {
            sum += tree[index];
            index -= index & -index;
        }
        return sum;
    }
    
    public int rangeQuery(int left, int right) {
        return query(right) - query(left - 1);
    }
}
```

## 4.8 Tree Traversal Algorithms

Different ways to visit all nodes in a tree.

### Tree Traversal Implementation

```java
public class TreeTraversal {
    // Preorder: Root -> Left -> Right
    public static void preorder(TreeNode root) {
        if (root == null) return;
        
        System.out.print(root.val + " ");
        preorder(root.left);
        preorder(root.right);
    }
    
    // Inorder: Left -> Root -> Right
    public static void inorder(TreeNode root) {
        if (root == null) return;
        
        inorder(root.left);
        System.out.print(root.val + " ");
        inorder(root.right);
    }
    
    // Postorder: Left -> Right -> Root
    public static void postorder(TreeNode root) {
        if (root == null) return;
        
        postorder(root.left);
        postorder(root.right);
        System.out.print(root.val + " ");
    }
    
    // Level order (BFS)
    public static void levelOrder(TreeNode root) {
        if (root == null) return;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();
            System.out.print(node.val + " ");
            
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
    }
    
    // Iterative preorder
    public static void preorderIterative(TreeNode root) {
        if (root == null) return;
        
        Stack<TreeNode> stack = new Stack<>();
        stack.push(root);
        
        while (!stack.isEmpty()) {
            TreeNode node = stack.pop();
            System.out.print(node.val + " ");
            
            if (node.right != null) stack.push(node.right);
            if (node.left != null) stack.push(node.left);
        }
    }
}
```

**Real-world Analogies:**
- **Binary Tree:** Like a family tree where each person has at most two children
- **BST:** Like a phone book where names are organized alphabetically
- **AVL Tree:** Like a balanced scale that automatically adjusts to stay level
- **Trie:** Like a dictionary where words are organized by their prefixes
- **Segment Tree:** Like a filing cabinet where you can quickly find documents in a range

Tree data structures are fundamental to computer science and provide efficient solutions for many problems involving hierarchical data, searching, and range queries.