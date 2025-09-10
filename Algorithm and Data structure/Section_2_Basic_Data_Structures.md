# Section 2 – Basic Data Structures

## 2.1 Arrays & Dynamic Arrays

Arrays are the most fundamental data structure in computer science, providing contiguous memory storage for elements of the same type.

### Static Arrays

Static arrays have a fixed size determined at compile time.

**Characteristics:**
- Fixed size
- Contiguous memory allocation
- Random access in O(1) time
- Cache-friendly due to spatial locality

**Example:**
```java
public class StaticArrayExample {
    public static void main(String[] args) {
        // Declaration and initialization
        int[] numbers = new int[5]; // Array of 5 integers
        String[] names = {"Alice", "Bob", "Charlie"}; // Array with initial values
        
        // Accessing elements
        numbers[0] = 10;
        numbers[1] = 20;
        System.out.println("First element: " + numbers[0]);
        
        // Iterating through array
        for (int i = 0; i < numbers.length; i++) {
            System.out.println("Element " + i + ": " + numbers[i]);
        }
        
        // Enhanced for loop
        for (String name : names) {
            System.out.println("Name: " + name);
        }
    }
}
```

**Real-world Analogy:**
Think of a static array like a row of lockers in a school hallway. Each locker has a number (index), and you can directly go to any locker without checking others first. However, you can't add more lockers to the row once it's built.

### Dynamic Arrays (ArrayList in Java)

Dynamic arrays can grow and shrink as needed, providing the flexibility of dynamic sizing with array-like performance.

**Characteristics:**
- Dynamic size
- Amortized O(1) insertion at end
- O(n) insertion/deletion in middle
- O(1) random access
- Automatic resizing when capacity exceeded

**Example:**
```java
import java.util.ArrayList;
import java.util.List;

public class DynamicArrayExample {
    public static void main(String[] args) {
        // Creating dynamic array
        List<Integer> dynamicArray = new ArrayList<>();
        
        // Adding elements
        dynamicArray.add(10);
        dynamicArray.add(20);
        dynamicArray.add(30);
        
        System.out.println("Size: " + dynamicArray.size());
        System.out.println("Elements: " + dynamicArray);
        
        // Accessing elements
        System.out.println("Element at index 1: " + dynamicArray.get(1));
        
        // Inserting at specific position
        dynamicArray.add(1, 15); // Insert 15 at index 1
        System.out.println("After insertion: " + dynamicArray);
        
        // Removing elements
        dynamicArray.remove(2); // Remove element at index 2
        System.out.println("After removal: " + dynamicArray);
        
        // Updating elements
        dynamicArray.set(0, 100);
        System.out.println("After update: " + dynamicArray);
    }
}
```

**Internal Implementation:**
```java
public class MyDynamicArray<T> {
    private T[] array;
    private int size;
    private int capacity;
    
    @SuppressWarnings("unchecked")
    public MyDynamicArray() {
        this.capacity = 10;
        this.size = 0;
        this.array = (T[]) new Object[capacity];
    }
    
    public void add(T element) {
        if (size >= capacity) {
            resize();
        }
        array[size] = element;
        size++;
    }
    
    public void add(int index, T element) {
        if (index < 0 || index > size) {
            throw new IndexOutOfBoundsException();
        }
        
        if (size >= capacity) {
            resize();
        }
        
        // Shift elements to the right
        for (int i = size; i > index; i--) {
            array[i] = array[i - 1];
        }
        
        array[index] = element;
        size++;
    }
    
    public T get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        return array[index];
    }
    
    public T remove(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        
        T removed = array[index];
        
        // Shift elements to the left
        for (int i = index; i < size - 1; i++) {
            array[i] = array[i + 1];
        }
        
        size--;
        return removed;
    }
    
    @SuppressWarnings("unchecked")
    private void resize() {
        capacity *= 2;
        T[] newArray = (T[]) new Object[capacity];
        System.arraycopy(array, 0, newArray, 0, size);
        array = newArray;
    }
    
    public int size() {
        return size;
    }
    
    public boolean isEmpty() {
        return size == 0;
    }
}
```

**Performance Analysis:**
- **Access:** O(1) - Direct index access
- **Search:** O(n) - Linear search required
- **Insertion at end:** O(1) amortized - May need to resize
- **Insertion at beginning/middle:** O(n) - Need to shift elements
- **Deletion:** O(n) - Need to shift elements
- **Space:** O(n) - Linear space complexity

## 2.2 Linked Lists (Singly, Doubly, Circular)

Linked lists are linear data structures where elements are stored in nodes, and each node contains data and a reference to the next node.

### Singly Linked List

Each node points to the next node in the sequence.

**Node Structure:**
```java
public class ListNode {
    int val;
    ListNode next;
    
    public ListNode(int val) {
        this.val = val;
        this.next = null;
    }
}
```

**Implementation:**
```java
public class SinglyLinkedList {
    private ListNode head;
    private int size;
    
    public SinglyLinkedList() {
        this.head = null;
        this.size = 0;
    }
    
    // Add element at the beginning
    public void addFirst(int val) {
        ListNode newNode = new ListNode(val);
        newNode.next = head;
        head = newNode;
        size++;
    }
    
    // Add element at the end
    public void addLast(int val) {
        ListNode newNode = new ListNode(val);
        
        if (head == null) {
            head = newNode;
        } else {
            ListNode current = head;
            while (current.next != null) {
                current = current.next;
            }
            current.next = newNode;
        }
        size++;
    }
    
    // Add element at specific index
    public void add(int index, int val) {
        if (index < 0 || index > size) {
            throw new IndexOutOfBoundsException();
        }
        
        if (index == 0) {
            addFirst(val);
            return;
        }
        
        ListNode newNode = new ListNode(val);
        ListNode current = head;
        
        for (int i = 0; i < index - 1; i++) {
            current = current.next;
        }
        
        newNode.next = current.next;
        current.next = newNode;
        size++;
    }
    
    // Remove element at specific index
    public int remove(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        
        if (index == 0) {
            int val = head.val;
            head = head.next;
            size--;
            return val;
        }
        
        ListNode current = head;
        for (int i = 0; i < index - 1; i++) {
            current = current.next;
        }
        
        int val = current.next.val;
        current.next = current.next.next;
        size--;
        return val;
    }
    
    // Get element at specific index
    public int get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        
        ListNode current = head;
        for (int i = 0; i < index; i++) {
            current = current.next;
        }
        return current.val;
    }
    
    // Check if list is empty
    public boolean isEmpty() {
        return size == 0;
    }
    
    // Get size
    public int size() {
        return size;
    }
    
    // Display the list
    public void display() {
        ListNode current = head;
        while (current != null) {
            System.out.print(current.val + " -> ");
            current = current.next;
        }
        System.out.println("null");
    }
}
```

### Doubly Linked List

Each node has references to both the next and previous nodes.

**Node Structure:**
```java
public class DoublyListNode {
    int val;
    DoublyListNode next;
    DoublyListNode prev;
    
    public DoublyListNode(int val) {
        this.val = val;
        this.next = null;
        this.prev = null;
    }
}
```

**Implementation:**
```java
public class DoublyLinkedList {
    private DoublyListNode head;
    private DoublyListNode tail;
    private int size;
    
    public DoublyLinkedList() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }
    
    // Add element at the beginning
    public void addFirst(int val) {
        DoublyListNode newNode = new DoublyListNode(val);
        
        if (head == null) {
            head = tail = newNode;
        } else {
            newNode.next = head;
            head.prev = newNode;
            head = newNode;
        }
        size++;
    }
    
    // Add element at the end
    public void addLast(int val) {
        DoublyListNode newNode = new DoublyListNode(val);
        
        if (tail == null) {
            head = tail = newNode;
        } else {
            tail.next = newNode;
            newNode.prev = tail;
            tail = newNode;
        }
        size++;
    }
    
    // Remove element from the beginning
    public int removeFirst() {
        if (head == null) {
            throw new NoSuchElementException();
        }
        
        int val = head.val;
        if (head == tail) {
            head = tail = null;
        } else {
            head = head.next;
            head.prev = null;
        }
        size--;
        return val;
    }
    
    // Remove element from the end
    public int removeLast() {
        if (tail == null) {
            throw new NoSuchElementException();
        }
        
        int val = tail.val;
        if (head == tail) {
            head = tail = null;
        } else {
            tail = tail.prev;
            tail.next = null;
        }
        size--;
        return val;
    }
    
    // Display forward
    public void displayForward() {
        DoublyListNode current = head;
        while (current != null) {
            System.out.print(current.val + " <-> ");
            current = current.next;
        }
        System.out.println("null");
    }
    
    // Display backward
    public void displayBackward() {
        DoublyListNode current = tail;
        while (current != null) {
            System.out.print(current.val + " <-> ");
            current = current.prev;
        }
        System.out.println("null");
    }
}
```

### Circular Linked List

The last node points back to the first node, creating a circular structure.

**Implementation:**
```java
public class CircularLinkedList {
    private ListNode head;
    private int size;
    
    public CircularLinkedList() {
        this.head = null;
        this.size = 0;
    }
    
    // Add element at the beginning
    public void addFirst(int val) {
        ListNode newNode = new ListNode(val);
        
        if (head == null) {
            head = newNode;
            head.next = head; // Point to itself
        } else {
            newNode.next = head;
            
            // Find the last node and update its next pointer
            ListNode current = head;
            while (current.next != head) {
                current = current.next;
            }
            current.next = newNode;
            head = newNode;
        }
        size++;
    }
    
    // Add element at the end
    public void addLast(int val) {
        ListNode newNode = new ListNode(val);
        
        if (head == null) {
            head = newNode;
            head.next = head;
        } else {
            ListNode current = head;
            while (current.next != head) {
                current = current.next;
            }
            current.next = newNode;
            newNode.next = head;
        }
        size++;
    }
    
    // Display the circular list
    public void display() {
        if (head == null) {
            System.out.println("Empty list");
            return;
        }
        
        ListNode current = head;
        do {
            System.out.print(current.val + " -> ");
            current = current.next;
        } while (current != head);
        System.out.println("(back to head)");
    }
}
```

**Real-world Analogy:**
- **Singly Linked List:** Like a treasure hunt where each clue leads to the next location
- **Doubly Linked List:** Like a two-way street where you can go forward or backward
- **Circular Linked List:** Like a roundabout where you can keep going in circles

## 2.3 Stacks & Queues

Stacks and queues are linear data structures that follow specific ordering principles.

### Stack (LIFO - Last In, First Out)

A stack follows the Last In, First Out principle, like a stack of plates.

**Operations:**
- `push()` - Add element to top
- `pop()` - Remove element from top
- `peek()` - View top element without removing
- `isEmpty()` - Check if stack is empty

**Implementation:**
```java
public class Stack<T> {
    private T[] array;
    private int top;
    private int capacity;
    
    @SuppressWarnings("unchecked")
    public Stack(int capacity) {
        this.capacity = capacity;
        this.array = (T[]) new Object[capacity];
        this.top = -1;
    }
    
    public void push(T element) {
        if (isFull()) {
            throw new StackOverflowError("Stack is full");
        }
        array[++top] = element;
    }
    
    public T pop() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return array[top--];
    }
    
    public T peek() {
        if (isEmpty()) {
            throw new EmptyStackException();
        }
        return array[top];
    }
    
    public boolean isEmpty() {
        return top == -1;
    }
    
    public boolean isFull() {
        return top == capacity - 1;
    }
    
    public int size() {
        return top + 1;
    }
}
```

**Applications:**
```java
public class StackApplications {
    // 1. Balanced Parentheses Checker
    public static boolean isBalanced(String expression) {
        Stack<Character> stack = new Stack<>(expression.length());
        
        for (char c : expression.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') {
                stack.push(c);
            } else if (c == ')' || c == ']' || c == '}') {
                if (stack.isEmpty()) return false;
                
                char top = stack.pop();
                if ((c == ')' && top != '(') ||
                    (c == ']' && top != '[') ||
                    (c == '}' && top != '{')) {
                    return false;
                }
            }
        }
        
        return stack.isEmpty();
    }
    
    // 2. Expression Evaluation (Postfix)
    public static int evaluatePostfix(String expression) {
        Stack<Integer> stack = new Stack<>(expression.length());
        
        for (char c : expression.toCharArray()) {
            if (Character.isDigit(c)) {
                stack.push(c - '0');
            } else {
                int b = stack.pop();
                int a = stack.pop();
                
                switch (c) {
                    case '+': stack.push(a + b); break;
                    case '-': stack.push(a - b); break;
                    case '*': stack.push(a * b); break;
                    case '/': stack.push(a / b); break;
                }
            }
        }
        
        return stack.pop();
    }
    
    // 3. Undo/Redo Functionality
    public static class TextEditor {
        private Stack<String> undoStack;
        private Stack<String> redoStack;
        private String currentText;
        
        public TextEditor() {
            this.undoStack = new Stack<>(100);
            this.redoStack = new Stack<>(100);
            this.currentText = "";
        }
        
        public void type(String text) {
            undoStack.push(currentText);
            currentText += text;
            redoStack.clear(); // Clear redo when new action is performed
        }
        
        public void undo() {
            if (!undoStack.isEmpty()) {
                redoStack.push(currentText);
                currentText = undoStack.pop();
            }
        }
        
        public void redo() {
            if (!redoStack.isEmpty()) {
                undoStack.push(currentText);
                currentText = redoStack.pop();
            }
        }
        
        public String getText() {
            return currentText;
        }
    }
}
```

### Queue (FIFO - First In, First Out)

A queue follows the First In, First Out principle, like a line of people waiting.

**Operations:**
- `enqueue()` - Add element to rear
- `dequeue()` - Remove element from front
- `front()` - View front element without removing
- `isEmpty()` - Check if queue is empty

**Implementation:**
```java
public class Queue<T> {
    private T[] array;
    private int front;
    private int rear;
    private int size;
    private int capacity;
    
    @SuppressWarnings("unchecked")
    public Queue(int capacity) {
        this.capacity = capacity;
        this.array = (T[]) new Object[capacity];
        this.front = 0;
        this.rear = -1;
        this.size = 0;
    }
    
    public void enqueue(T element) {
        if (isFull()) {
            throw new IllegalStateException("Queue is full");
        }
        
        rear = (rear + 1) % capacity;
        array[rear] = element;
        size++;
    }
    
    public T dequeue() {
        if (isEmpty()) {
            throw new NoSuchElementException("Queue is empty");
        }
        
        T element = array[front];
        front = (front + 1) % capacity;
        size--;
        return element;
    }
    
    public T front() {
        if (isEmpty()) {
            throw new NoSuchElementException("Queue is empty");
        }
        return array[front];
    }
    
    public boolean isEmpty() {
        return size == 0;
    }
    
    public boolean isFull() {
        return size == capacity;
    }
    
    public int size() {
        return size;
    }
}
```

**Applications:**
```java
public class QueueApplications {
    // 1. Breadth-First Search (BFS)
    public static void bfs(int[][] graph, int start) {
        boolean[] visited = new boolean[graph.length];
        Queue<Integer> queue = new Queue<>(graph.length);
        
        visited[start] = true;
        queue.enqueue(start);
        
        while (!queue.isEmpty()) {
            int vertex = queue.dequeue();
            System.out.print(vertex + " ");
            
            for (int i = 0; i < graph[vertex].length; i++) {
                if (graph[vertex][i] == 1 && !visited[i]) {
                    visited[i] = true;
                    queue.enqueue(i);
                }
            }
        }
    }
    
    // 2. Task Scheduling
    public static class TaskScheduler {
        private Queue<String> taskQueue;
        
        public TaskScheduler() {
            this.taskQueue = new Queue<>(100);
        }
        
        public void addTask(String task) {
            taskQueue.enqueue(task);
            System.out.println("Task added: " + task);
        }
        
        public String processNextTask() {
            if (taskQueue.isEmpty()) {
                return "No tasks to process";
            }
            
            String task = taskQueue.dequeue();
            System.out.println("Processing task: " + task);
            return task;
        }
        
        public boolean hasTasks() {
            return !taskQueue.isEmpty();
        }
    }
    
    // 3. Print Spooler
    public static class PrintSpooler {
        private Queue<String> printQueue;
        
        public PrintSpooler() {
            this.printQueue = new Queue<>(50);
        }
        
        public void addPrintJob(String document) {
            printQueue.enqueue(document);
            System.out.println("Print job queued: " + document);
        }
        
        public void processPrintJobs() {
            while (!printQueue.isEmpty()) {
                String document = printQueue.dequeue();
                System.out.println("Printing: " + document);
                // Simulate printing time
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }
    }
}
```

## 2.4 Hash Tables & Hash Maps

Hash tables provide fast access to data using key-value pairs through hashing.

### Hash Table Implementation

**Basic Hash Table:**
```java
public class HashTable<K, V> {
    private static final int DEFAULT_CAPACITY = 16;
    private static final double LOAD_FACTOR = 0.75;
    
    private Entry<K, V>[] table;
    private int size;
    private int capacity;
    
    @SuppressWarnings("unchecked")
    public HashTable() {
        this.capacity = DEFAULT_CAPACITY;
        this.table = new Entry[capacity];
        this.size = 0;
    }
    
    private static class Entry<K, V> {
        K key;
        V value;
        Entry<K, V> next;
        
        public Entry(K key, V value) {
            this.key = key;
            this.value = value;
            this.next = null;
        }
    }
    
    private int hash(K key) {
        return Math.abs(key.hashCode()) % capacity;
    }
    
    public void put(K key, V value) {
        if (size >= capacity * LOAD_FACTOR) {
            resize();
        }
        
        int index = hash(key);
        Entry<K, V> entry = new Entry<>(key, value);
        
        if (table[index] == null) {
            table[index] = entry;
        } else {
            // Handle collision with chaining
            Entry<K, V> current = table[index];
            while (current.next != null) {
                if (current.key.equals(key)) {
                    current.value = value;
                    return;
                }
                current = current.next;
            }
            
            if (current.key.equals(key)) {
                current.value = value;
            } else {
                current.next = entry;
            }
        }
        size++;
    }
    
    public V get(K key) {
        int index = hash(key);
        Entry<K, V> current = table[index];
        
        while (current != null) {
            if (current.key.equals(key)) {
                return current.value;
            }
            current = current.next;
        }
        
        return null;
    }
    
    public V remove(K key) {
        int index = hash(key);
        Entry<K, V> current = table[index];
        Entry<K, V> prev = null;
        
        while (current != null) {
            if (current.key.equals(key)) {
                if (prev == null) {
                    table[index] = current.next;
                } else {
                    prev.next = current.next;
                }
                size--;
                return current.value;
            }
            prev = current;
            current = current.next;
        }
        
        return null;
    }
    
    @SuppressWarnings("unchecked")
    private void resize() {
        Entry<K, V>[] oldTable = table;
        capacity *= 2;
        table = new Entry[capacity];
        size = 0;
        
        for (Entry<K, V> entry : oldTable) {
            while (entry != null) {
                put(entry.key, entry.value);
                entry = entry.next;
            }
        }
    }
    
    public boolean containsKey(K key) {
        return get(key) != null;
    }
    
    public int size() {
        return size;
    }
    
    public boolean isEmpty() {
        return size == 0;
    }
}
```

**Applications:**
```java
public class HashTableApplications {
    // 1. Word Frequency Counter
    public static Map<String, Integer> countWordFrequency(String text) {
        Map<String, Integer> frequency = new HashMap<>();
        String[] words = text.toLowerCase().split("\\W+");
        
        for (String word : words) {
            frequency.put(word, frequency.getOrDefault(word, 0) + 1);
        }
        
        return frequency;
    }
    
    // 2. Two Sum Problem
    public static int[] twoSum(int[] nums, int target) {
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
    
    // 3. LRU Cache Implementation
    public static class LRUCache {
        private Map<Integer, Node> cache;
        private Node head;
        private Node tail;
        private int capacity;
        
        private class Node {
            int key;
            int value;
            Node prev;
            Node next;
            
            public Node(int key, int value) {
                this.key = key;
                this.value = value;
            }
        }
        
        public LRUCache(int capacity) {
            this.capacity = capacity;
            this.cache = new HashMap<>();
            this.head = new Node(0, 0);
            this.tail = new Node(0, 0);
            head.next = tail;
            tail.prev = head;
        }
        
        public int get(int key) {
            Node node = cache.get(key);
            if (node != null) {
                moveToHead(node);
                return node.value;
            }
            return -1;
        }
        
        public void put(int key, int value) {
            Node node = cache.get(key);
            
            if (node != null) {
                node.value = value;
                moveToHead(node);
            } else {
                Node newNode = new Node(key, value);
                
                if (cache.size() >= capacity) {
                    Node tail = removeTail();
                    cache.remove(tail.key);
                }
                
                cache.put(key, newNode);
                addToHead(newNode);
            }
        }
        
        private void addToHead(Node node) {
            node.prev = head;
            node.next = head.next;
            head.next.prev = node;
            head.next = node;
        }
        
        private void removeNode(Node node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
        }
        
        private void moveToHead(Node node) {
            removeNode(node);
            addToHead(node);
        }
        
        private Node removeTail() {
            Node lastNode = tail.prev;
            removeNode(lastNode);
            return lastNode;
        }
    }
}
```

## 2.5 Sets & Multisets

Sets store unique elements, while multisets allow duplicate elements.

### Set Implementation

**Hash Set:**
```java
public class HashSet<T> {
    private HashTable<T, Boolean> table;
    
    public HashSet() {
        this.table = new HashTable<>();
    }
    
    public void add(T element) {
        table.put(element, true);
    }
    
    public boolean contains(T element) {
        return table.containsKey(element);
    }
    
    public boolean remove(T element) {
        return table.remove(element) != null;
    }
    
    public int size() {
        return table.size();
    }
    
    public boolean isEmpty() {
        return table.isEmpty();
    }
    
    // Union of two sets
    public HashSet<T> union(HashSet<T> other) {
        HashSet<T> result = new HashSet<>();
        
        // Add all elements from this set
        for (T element : this.toArray()) {
            result.add(element);
        }
        
        // Add all elements from other set
        for (T element : other.toArray()) {
            result.add(element);
        }
        
        return result;
    }
    
    // Intersection of two sets
    public HashSet<T> intersection(HashSet<T> other) {
        HashSet<T> result = new HashSet<>();
        
        for (T element : this.toArray()) {
            if (other.contains(element)) {
                result.add(element);
            }
        }
        
        return result;
    }
    
    private T[] toArray() {
        // Implementation to convert set to array
        // This is a simplified version
        return (T[]) new Object[0];
    }
}
```

**Tree Set (Sorted Set):**
```java
public class TreeSet<T extends Comparable<T>> {
    private TreeNode root;
    private int size;
    
    private class TreeNode {
        T value;
        TreeNode left;
        TreeNode right;
        
        public TreeNode(T value) {
            this.value = value;
            this.left = null;
            this.right = null;
        }
    }
    
    public void add(T element) {
        root = addRecursive(root, element);
    }
    
    private TreeNode addRecursive(TreeNode node, T element) {
        if (node == null) {
            size++;
            return new TreeNode(element);
        }
        
        int comparison = element.compareTo(node.value);
        if (comparison < 0) {
            node.left = addRecursive(node.left, element);
        } else if (comparison > 0) {
            node.right = addRecursive(node.right, element);
        }
        
        return node;
    }
    
    public boolean contains(T element) {
        return containsRecursive(root, element);
    }
    
    private boolean containsRecursive(TreeNode node, T element) {
        if (node == null) {
            return false;
        }
        
        int comparison = element.compareTo(node.value);
        if (comparison == 0) {
            return true;
        } else if (comparison < 0) {
            return containsRecursive(node.left, element);
        } else {
            return containsRecursive(node.right, element);
        }
    }
    
    public int size() {
        return size;
    }
}
```

### Multiset Implementation

```java
public class Multiset<T> {
    private Map<T, Integer> counts;
    
    public Multiset() {
        this.counts = new HashMap<>();
    }
    
    public void add(T element) {
        counts.put(element, counts.getOrDefault(element, 0) + 1);
    }
    
    public void add(T element, int count) {
        counts.put(element, counts.getOrDefault(element, 0) + count);
    }
    
    public int count(T element) {
        return counts.getOrDefault(element, 0);
    }
    
    public boolean remove(T element) {
        int currentCount = counts.getOrDefault(element, 0);
        if (currentCount > 0) {
            if (currentCount == 1) {
                counts.remove(element);
            } else {
                counts.put(element, currentCount - 1);
            }
            return true;
        }
        return false;
    }
    
    public boolean remove(T element, int count) {
        int currentCount = counts.getOrDefault(element, 0);
        if (currentCount >= count) {
            if (currentCount == count) {
                counts.remove(element);
            } else {
                counts.put(element, currentCount - count);
            }
            return true;
        }
        return false;
    }
    
    public Set<T> elementSet() {
        return counts.keySet();
    }
    
    public int size() {
        return counts.values().stream().mapToInt(Integer::intValue).sum();
    }
    
    public boolean isEmpty() {
        return counts.isEmpty();
    }
}
```

## 2.6 Strings & String Manipulation

Strings are sequences of characters that require special handling due to their immutable nature in Java.

### String Operations

**Basic String Operations:**
```java
public class StringOperations {
    // 1. String Reversal
    public static String reverse(String str) {
        char[] chars = str.toCharArray();
        int left = 0;
        int right = chars.length - 1;
        
        while (left < right) {
            char temp = chars[left];
            chars[left] = chars[right];
            chars[right] = temp;
            left++;
            right--;
        }
        
        return new String(chars);
    }
    
    // 2. Palindrome Check
    public static boolean isPalindrome(String str) {
        str = str.toLowerCase().replaceAll("[^a-z0-9]", "");
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
    
    // 3. Anagram Check
    public static boolean areAnagrams(String str1, String str2) {
        if (str1.length() != str2.length()) {
            return false;
        }
        
        int[] count = new int[26];
        
        for (int i = 0; i < str1.length(); i++) {
            count[str1.charAt(i) - 'a']++;
            count[str2.charAt(i) - 'a']--;
        }
        
        for (int c : count) {
            if (c != 0) {
                return false;
            }
        }
        
        return true;
    }
    
    // 4. Longest Common Subsequence
    public static int longestCommonSubsequence(String text1, String text2) {
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
    
    // 5. String Compression
    public static String compress(String str) {
        if (str == null || str.isEmpty()) {
            return str;
        }
        
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
        
        compressed.append(str.charAt(str.length() - 1));
        if (count > 1) {
            compressed.append(count);
        }
        
        return compressed.length() < str.length() ? compressed.toString() : str;
    }
}
```

### Pattern Matching

**KMP Algorithm:**
```java
public class PatternMatching {
    // KMP Algorithm for pattern matching
    public static int kmpSearch(String text, String pattern) {
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
    
    // Rabin-Karp Algorithm
    public static int rabinKarpSearch(String text, String pattern) {
        int n = text.length();
        int m = pattern.length();
        
        if (m > n) return -1;
        
        int patternHash = pattern.hashCode();
        
        for (int i = 0; i <= n - m; i++) {
            String substring = text.substring(i, i + m);
            if (substring.hashCode() == patternHash && substring.equals(pattern)) {
                return i;
            }
        }
        
        return -1;
    }
}
```

## 2.7 Basic Data Structure Operations

Common operations that can be performed on various data structures.

### Traversal Operations

**Array Traversal:**
```java
public class TraversalOperations {
    // 1. Linear Search
    public static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                return i;
            }
        }
        return -1;
    }
    
    // 2. Binary Search (for sorted arrays)
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
    
    // 3. Find Maximum Element
    public static int findMax(int[] arr) {
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
    
    // 4. Find Minimum Element
    public static int findMin(int[] arr) {
        if (arr.length == 0) {
            throw new IllegalArgumentException("Array is empty");
        }
        
        int min = arr[0];
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] < min) {
                min = arr[i];
            }
        }
        return min;
    }
}
```

### Sorting Operations

**Basic Sorting Algorithms:**
```java
public class SortingOperations {
    // 1. Bubble Sort
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
            if (!swapped) break; // Optimization: array is sorted
        }
    }
    
    // 2. Selection Sort
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
    
    // 3. Insertion Sort
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
    
    // 4. Merge Sort
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
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

### Utility Operations

**Common Utility Functions:**
```java
public class UtilityOperations {
    // 1. Array Copy
    public static int[] copyArray(int[] arr) {
        int[] copy = new int[arr.length];
        System.arraycopy(arr, 0, copy, 0, arr.length);
        return copy;
    }
    
    // 2. Array Reverse
    public static void reverseArray(int[] arr) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left < right) {
            swap(arr, left, right);
            left++;
            right--;
        }
    }
    
    // 3. Array Rotation
    public static void rotateArray(int[] arr, int k) {
        int n = arr.length;
        k = k % n; // Handle k > n
        
        reverseArray(arr, 0, n - 1);
        reverseArray(arr, 0, k - 1);
        reverseArray(arr, k, n - 1);
    }
    
    private static void reverseArray(int[] arr, int start, int end) {
        while (start < end) {
            swap(arr, start, end);
            start++;
            end--;
        }
    }
    
    // 4. Find Duplicates
    public static List<Integer> findDuplicates(int[] arr) {
        Set<Integer> seen = new HashSet<>();
        Set<Integer> duplicates = new HashSet<>();
        
        for (int num : arr) {
            if (seen.contains(num)) {
                duplicates.add(num);
            } else {
                seen.add(num);
            }
        }
        
        return new ArrayList<>(duplicates);
    }
    
    // 5. Remove Duplicates
    public static int[] removeDuplicates(int[] arr) {
        Set<Integer> unique = new HashSet<>();
        for (int num : arr) {
            unique.add(num);
        }
        
        return unique.stream().mapToInt(Integer::intValue).toArray();
    }
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

Understanding basic data structures provides the foundation for solving more complex problems. Each data structure has its strengths and weaknesses, and choosing the right one for a specific problem is crucial for optimal performance. The key is to understand the time and space complexity of operations and match them to your problem requirements.