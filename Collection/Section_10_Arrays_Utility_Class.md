# Section 10 – Arrays Utility Class

## 10.1 Arrays Utility Concepts

The Arrays utility class provides static methods for operating on arrays, offering a wide range of operations including sorting, searching, filling, copying, and transformation. Understanding these utility methods is essential for efficient array manipulation.

### What is the Arrays Utility Class?

The Arrays class is a utility class that contains static methods for:
- **Sorting**: Ordering elements in arrays
- **Searching**: Finding elements in sorted arrays
- **Filling**: Setting all elements to a specific value
- **Copying**: Creating copies of arrays
- **Comparison**: Comparing arrays for equality
- **Transformation**: Converting arrays to collections
- **String Representation**: Converting arrays to strings

### Key Characteristics of Arrays Utility

#### 1. Static Methods
- All methods are static
- No need to create instances
- Easy to use and access

#### 2. Generic Support
- Type-safe operations
- Works with any array type
- Compile-time type checking

#### 3. Performance Optimized
- Efficient implementations
- Optimized for different array types
- Minimal overhead

### Common Arrays Utility Categories

| Category | Methods | Purpose |
|----------|---------|---------|
| Sorting | sort() | Order elements |
| Searching | binarySearch() | Find elements |
| Filling | fill() | Set all elements |
| Copying | copyOf(), copyOfRange() | Create copies |
| Comparison | equals(), deepEquals() | Compare arrays |
| Transformation | asList(), toString() | Convert arrays |
| Streams | stream() | Create streams |

### Real-World Analogy: Array Toolkit

Think of the Arrays utility class as a comprehensive toolkit for arrays:

- **Sorting methods**: Like a sorting machine that organizes items in order
- **Searching methods**: Like a metal detector that finds specific items quickly
- **Filling methods**: Like a paint roller that covers all surfaces with the same color
- **Copying methods**: Like a photocopier that creates exact duplicates
- **Comparison methods**: Like a scale that checks if two items weigh the same
- **Transformation methods**: Like a converter that changes one format to another

## 10.2 Sorting Methods

Sorting methods provide various ways to order elements in arrays, from simple natural ordering to complex custom comparators.

### Core Sorting Methods

```java
public class Arrays {
    // Basic sorting
    public static void sort(byte[] a)
    public static void sort(short[] a)
    public static void sort(int[] a)
    public static void sort(long[] a)
    public static void sort(float[] a)
    public static void sort(double[] a)
    public static void sort(char[] a)
    public static void sort(Object[] a)
    public static <T> void sort(T[] a, Comparator<? super T> c)
    
    // Range sorting
    public static void sort(byte[] a, int fromIndex, int toIndex)
    public static void sort(short[] a, int fromIndex, int toIndex)
    public static void sort(int[] a, int fromIndex, int toIndex)
    public static void sort(long[] a, int fromIndex, int toIndex)
    public static void sort(float[] a, int fromIndex, int toIndex)
    public static void sort(double[] a, int fromIndex, int toIndex)
    public static void sort(char[] a, int fromIndex, int toIndex)
    public static void sort(Object[] a, int fromIndex, int toIndex)
    public static <T> void sort(T[] a, int fromIndex, int toIndex, Comparator<? super T> c)
}
```

### Understanding Sorting Operations

#### 1. Primitive Array Sorting
```java
// Integer array sorting
int[] numbers = {5, 2, 8, 1, 9, 3};
Arrays.sort(numbers);
System.out.println("Sorted: " + Arrays.toString(numbers)); // [1, 2, 3, 5, 8, 9]

// String array sorting
String[] names = {"Charlie", "Alice", "Bob", "David"};
Arrays.sort(names);
System.out.println("Sorted: " + Arrays.toString(names)); // [Alice, Bob, Charlie, David]

// Double array sorting
double[] prices = {19.99, 12.50, 25.00, 8.75};
Arrays.sort(prices);
System.out.println("Sorted: " + Arrays.toString(prices)); // [8.75, 12.5, 19.99, 25.0]
```

#### 2. Range Sorting
```java
int[] numbers = {5, 2, 8, 1, 9, 3, 7, 4};

// Sort only elements from index 2 to 5 (inclusive)
Arrays.sort(numbers, 2, 6);
System.out.println("Range sorted: " + Arrays.toString(numbers)); // [5, 2, 1, 3, 8, 9, 7, 4]

// Sort entire array
Arrays.sort(numbers);
System.out.println("Fully sorted: " + Arrays.toString(numbers)); // [1, 2, 3, 4, 5, 7, 8, 9]
```

#### 3. Custom Comparator Sorting
```java
// Custom object array
Person[] people = {
    new Person("Alice", 25),
    new Person("Bob", 30),
    new Person("Charlie", 35)
};

// Sort by age
Arrays.sort(people, (p1, p2) -> Integer.compare(p1.getAge(), p2.getAge()));
System.out.println("Sorted by age: " + Arrays.toString(people));

// Sort by name
Arrays.sort(people, (p1, p2) -> p1.getName().compareTo(p2.getName()));
System.out.println("Sorted by name: " + Arrays.toString(people));

// Sort by age in descending order
Arrays.sort(people, (p1, p2) -> Integer.compare(p2.getAge(), p1.getAge()));
System.out.println("Sorted by age (desc): " + Arrays.toString(people));
```

### Real-World Example: Student Grade Management
```java
public class StudentGradeManager {
    private Student[] students;
    private int size;
    
    public StudentGradeManager(int capacity) {
        this.students = new Student[capacity];
        this.size = 0;
    }
    
    public void addStudent(Student student) {
        if (size < students.length) {
            students[size++] = student;
        }
    }
    
    public void sortByGrade() {
        Arrays.sort(students, 0, size, (s1, s2) -> 
            Double.compare(s2.getGrade(), s1.getGrade())); // Descending order
    }
    
    public void sortByName() {
        Arrays.sort(students, 0, size, (s1, s2) -> 
            s1.getName().compareTo(s2.getName()));
    }
    
    public void sortByGradeThenName() {
        Arrays.sort(students, 0, size, (s1, s2) -> {
            int gradeCompare = Double.compare(s2.getGrade(), s1.getGrade());
            if (gradeCompare != 0) {
                return gradeCompare;
            }
            return s1.getName().compareTo(s2.getName());
        });
    }
    
    public Student[] getTopStudents(int count) {
        Student[] topStudents = new Student[Math.min(count, size)];
        System.arraycopy(students, 0, topStudents, 0, topStudents.length);
        return topStudents;
    }
    
    public void printStudents() {
        for (int i = 0; i < size; i++) {
            System.out.println(students[i].getName() + ": " + students[i].getGrade());
        }
    }
    
    public static class Student {
        private String name;
        private double grade;
        
        public Student(String name, double grade) {
            this.name = name;
            this.grade = grade;
        }
        
        public String getName() { return name; }
        public double getGrade() { return grade; }
        
        @Override
        public String toString() {
            return "Student{name='" + name + "', grade=" + grade + "}";
        }
    }
}
```

## 10.3 Searching Methods

Searching methods provide efficient ways to find elements in arrays, particularly in sorted arrays.

### Core Searching Methods

```java
public class Arrays {
    // Binary search for primitive arrays
    public static int binarySearch(byte[] a, byte key)
    public static int binarySearch(short[] a, short key)
    public static int binarySearch(int[] a, int key)
    public static int binarySearch(long[] a, long key)
    public static int binarySearch(float[] a, float key)
    public static int binarySearch(double[] a, double key)
    public static int binarySearch(char[] a, char key)
    
    // Binary search for object arrays
    public static int binarySearch(Object[] a, Object key)
    public static <T> int binarySearch(T[] a, T key, Comparator<? super T> c)
    
    // Range binary search
    public static int binarySearch(byte[] a, int fromIndex, int toIndex, byte key)
    public static int binarySearch(short[] a, int fromIndex, int toIndex, short key)
    public static int binarySearch(int[] a, int fromIndex, int toIndex, int key)
    public static int binarySearch(long[] a, int fromIndex, int toIndex, long key)
    public static int binarySearch(float[] a, int fromIndex, int toIndex, float key)
    public static int binarySearch(double[] a, int fromIndex, int toIndex, double key)
    public static int binarySearch(char[] a, int fromIndex, int toIndex, char key)
    public static int binarySearch(Object[] a, int fromIndex, int toIndex, Object key)
    public static <T> int binarySearch(T[] a, int fromIndex, int toIndex, T key, Comparator<? super T> c)
}
```

### Understanding Searching Operations

#### 1. Basic Binary Search
```java
int[] numbers = {1, 3, 5, 7, 9, 11, 13, 15};

// Search for existing element
int index = Arrays.binarySearch(numbers, 7);
System.out.println("7 found at index: " + index); // 3

// Search for non-existent element
int notFound = Arrays.binarySearch(numbers, 6);
System.out.println("6 not found, insertion point: " + (-notFound - 1)); // 3

// Search for element at beginning
int first = Arrays.binarySearch(numbers, 1);
System.out.println("1 found at index: " + first); // 0

// Search for element at end
int last = Arrays.binarySearch(numbers, 15);
System.out.println("15 found at index: " + last); // 7
```

#### 2. Range Binary Search
```java
int[] numbers = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};

// Search in range from index 2 to 7 (inclusive)
int index = Arrays.binarySearch(numbers, 2, 8, 9);
System.out.println("9 found at index: " + index); // 4

// Search for element not in range
int notFound = Arrays.binarySearch(numbers, 2, 8, 1);
System.out.println("1 not found in range, insertion point: " + (-notFound - 1)); // 2
```

#### 3. Custom Comparator Search
```java
Person[] people = {
    new Person("Alice", 25),
    new Person("Bob", 30),
    new Person("Charlie", 35)
};

// Sort by age first
Arrays.sort(people, (p1, p2) -> Integer.compare(p1.getAge(), p2.getAge()));

// Search by age
Person searchKey = new Person("", 30);
int index = Arrays.binarySearch(people, searchKey, 
    (p1, p2) -> Integer.compare(p1.getAge(), p2.getAge()));
System.out.println("Person with age 30 found at index: " + index);
```

### Real-World Example: Library Management
```java
public class LibraryManager {
    private Book[] books;
    private int size;
    
    public LibraryManager(int capacity) {
        this.books = new Book[capacity];
        this.size = 0;
    }
    
    public void addBook(Book book) {
        if (size < books.length) {
            books[size++] = book;
        }
    }
    
    public Book findBookByTitle(String title) {
        // Sort by title first
        Arrays.sort(books, 0, size, (b1, b2) -> b1.getTitle().compareTo(b2.getTitle()));
        
        // Create search key
        Book searchKey = new Book(title, "", 0);
        
        // Binary search
        int index = Arrays.binarySearch(books, 0, size, searchKey, 
            (b1, b2) -> b1.getTitle().compareTo(b2.getTitle()));
        
        return index >= 0 ? books[index] : null;
    }
    
    public Book findBookByAuthor(String author) {
        // Sort by author first
        Arrays.sort(books, 0, size, (b1, b2) -> b1.getAuthor().compareTo(b2.getAuthor()));
        
        // Create search key
        Book searchKey = new Book("", author, 0);
        
        // Binary search
        int index = Arrays.binarySearch(books, 0, size, searchKey, 
            (b1, b2) -> b1.getAuthor().compareTo(b2.getAuthor()));
        
        return index >= 0 ? books[index] : null;
    }
    
    public Book findMostExpensiveBook() {
        if (size == 0) return null;
        
        Book maxBook = books[0];
        for (int i = 1; i < size; i++) {
            if (books[i].getPrice() > maxBook.getPrice()) {
                maxBook = books[i];
            }
        }
        return maxBook;
    }
    
    public Book findCheapestBook() {
        if (size == 0) return null;
        
        Book minBook = books[0];
        for (int i = 1; i < size; i++) {
            if (books[i].getPrice() < minBook.getPrice()) {
                minBook = books[i];
            }
        }
        return minBook;
    }
    
    public void sortBooksByTitle() {
        Arrays.sort(books, 0, size, (b1, b2) -> b1.getTitle().compareTo(b2.getTitle()));
    }
    
    public void sortBooksByPrice() {
        Arrays.sort(books, 0, size, (b1, b2) -> Double.compare(b1.getPrice(), b2.getPrice()));
    }
    
    public static class Book {
        private String title;
        private String author;
        private double price;
        
        public Book(String title, String author, double price) {
            this.title = title;
            this.author = author;
            this.price = price;
        }
        
        public String getTitle() { return title; }
        public String getAuthor() { return author; }
        public double getPrice() { return price; }
        
        @Override
        public String toString() {
            return "Book{title='" + title + "', author='" + author + "', price=" + price + "}";
        }
    }
}
```

## 10.4 Filling Methods

Filling methods provide ways to set all elements in an array to a specific value.

### Core Filling Methods

```java
public class Arrays {
    // Fill entire array
    public static void fill(byte[] a, byte val)
    public static void fill(short[] a, short val)
    public static void fill(int[] a, int val)
    public static void fill(long[] a, long val)
    public static void fill(float[] a, float val)
    public static void fill(double[] a, double val)
    public static void fill(char[] a, char val)
    public static void fill(boolean[] a, boolean val)
    public static void fill(Object[] a, Object val)
    
    // Fill range
    public static void fill(byte[] a, int fromIndex, int toIndex, byte val)
    public static void fill(short[] a, int fromIndex, int toIndex, short val)
    public static void fill(int[] a, int fromIndex, int toIndex, int val)
    public static void fill(long[] a, int fromIndex, int toIndex, long val)
    public static void fill(float[] a, int fromIndex, int toIndex, float val)
    public static void fill(double[] a, int fromIndex, int toIndex, double val)
    public static void fill(char[] a, int fromIndex, int toIndex, char val)
    public static void fill(boolean[] a, int fromIndex, int toIndex, boolean val)
    public static void fill(Object[] a, int fromIndex, int toIndex, Object val)
}
```

### Understanding Filling Operations

#### 1. Fill Entire Array
```java
// Fill integer array
int[] numbers = new int[5];
Arrays.fill(numbers, 42);
System.out.println("Filled: " + Arrays.toString(numbers)); // [42, 42, 42, 42, 42]

// Fill string array
String[] names = new String[3];
Arrays.fill(names, "Unknown");
System.out.println("Filled: " + Arrays.toString(names)); // [Unknown, Unknown, Unknown]

// Fill boolean array
boolean[] flags = new boolean[4];
Arrays.fill(flags, true);
System.out.println("Filled: " + Arrays.toString(flags)); // [true, true, true, true]
```

#### 2. Fill Range
```java
int[] numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Fill range from index 2 to 6 (exclusive)
Arrays.fill(numbers, 2, 6, 0);
System.out.println("Range filled: " + Arrays.toString(numbers)); // [1, 2, 0, 0, 0, 0, 7, 8, 9, 10]

// Fill range from index 0 to 3 (exclusive)
Arrays.fill(numbers, 0, 3, -1);
System.out.println("Range filled: " + Arrays.toString(numbers)); // [-1, -1, -1, 0, 0, 0, 7, 8, 9, 10]
```

#### 3. Fill with Different Values
```java
// Fill with different values for different ranges
int[] numbers = new int[10];

// Fill first half with 1
Arrays.fill(numbers, 0, 5, 1);

// Fill second half with 2
Arrays.fill(numbers, 5, 10, 2);

System.out.println("Filled: " + Arrays.toString(numbers)); // [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
```

### Real-World Example: Game Board Initialization
```java
public class GameBoard {
    private char[][] board;
    private int rows;
    private int cols;
    
    public GameBoard(int rows, int cols) {
        this.rows = rows;
        this.cols = cols;
        this.board = new char[rows][cols];
        initializeBoard();
    }
    
    private void initializeBoard() {
        // Fill entire board with empty spaces
        for (int i = 0; i < rows; i++) {
            Arrays.fill(board[i], ' ');
        }
    }
    
    public void clearBoard() {
        // Clear entire board
        for (int i = 0; i < rows; i++) {
            Arrays.fill(board[i], ' ');
        }
    }
    
    public void clearRow(int row) {
        if (row >= 0 && row < rows) {
            Arrays.fill(board[row], ' ');
        }
    }
    
    public void clearColumn(int col) {
        if (col >= 0 && col < cols) {
            for (int i = 0; i < rows; i++) {
                board[i][col] = ' ';
            }
        }
    }
    
    public void setCell(int row, int col, char value) {
        if (row >= 0 && row < rows && col >= 0 && col < cols) {
            board[row][col] = value;
        }
    }
    
    public char getCell(int row, int col) {
        if (row >= 0 && row < rows && col >= 0 && col < cols) {
            return board[row][col];
        }
        return ' ';
    }
    
    public void printBoard() {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                System.out.print("|" + board[i][j]);
            }
            System.out.println("|");
        }
    }
}
```

## 10.5 Copying Methods

Copying methods provide ways to create copies of arrays, including partial copies and range copies.

### Core Copying Methods

```java
public class Arrays {
    // Copy entire array
    public static byte[] copyOf(byte[] original, int newLength)
    public static short[] copyOf(short[] original, int newLength)
    public static int[] copyOf(int[] original, int newLength)
    public static long[] copyOf(long[] original, int newLength)
    public static float[] copyOf(float[] original, int newLength)
    public static double[] copyOf(double[] original, int newLength)
    public static char[] copyOf(char[] original, int newLength)
    public static boolean[] copyOf(boolean[] original, int newLength)
    public static <T> T[] copyOf(T[] original, int newLength)
    public static <T,U> T[] copyOf(U[] original, int newLength, Class<? extends T[]> newType)
    
    // Copy range
    public static byte[] copyOfRange(byte[] original, int from, int to)
    public static short[] copyOfRange(short[] original, int from, int to)
    public static int[] copyOfRange(int[] original, int from, int to)
    public static long[] copyOfRange(long[] original, int from, int to)
    public static float[] copyOfRange(float[] original, int from, int to)
    public static double[] copyOfRange(double[] original, int from, int to)
    public static char[] copyOfRange(char[] original, int from, int to)
    public static boolean[] copyOfRange(boolean[] original, int from, int to)
    public static <T> T[] copyOfRange(T[] original, int from, int to)
    public static <T,U> T[] copyOfRange(U[] original, int from, int to, Class<? extends T[]> newType)
}
```

### Understanding Copying Operations

#### 1. Copy Entire Array
```java
int[] original = {1, 2, 3, 4, 5};

// Copy with same length
int[] copy1 = Arrays.copyOf(original, original.length);
System.out.println("Same length: " + Arrays.toString(copy1)); // [1, 2, 3, 4, 5]

// Copy with larger length (padded with zeros)
int[] copy2 = Arrays.copyOf(original, 8);
System.out.println("Larger length: " + Arrays.toString(copy2)); // [1, 2, 3, 4, 5, 0, 0, 0]

// Copy with smaller length (truncated)
int[] copy3 = Arrays.copyOf(original, 3);
System.out.println("Smaller length: " + Arrays.toString(copy3)); // [1, 2, 3]
```

#### 2. Copy Range
```java
int[] original = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Copy range from index 2 to 7 (exclusive)
int[] range1 = Arrays.copyOfRange(original, 2, 7);
System.out.println("Range 2-7: " + Arrays.toString(range1)); // [3, 4, 5, 6, 7]

// Copy range from index 0 to 5 (exclusive)
int[] range2 = Arrays.copyOfRange(original, 0, 5);
System.out.println("Range 0-5: " + Arrays.toString(range2)); // [1, 2, 3, 4, 5]

// Copy range from index 5 to 10 (exclusive)
int[] range3 = Arrays.copyOfRange(original, 5, 10);
System.out.println("Range 5-10: " + Arrays.toString(range3)); // [6, 7, 8, 9, 10]
```

#### 3. Copy with Type Conversion
```java
String[] original = {"1", "2", "3", "4", "5"};

// Copy with type conversion
Integer[] converted = Arrays.copyOf(original, original.length, Integer[].class);
System.out.println("Converted: " + Arrays.toString(converted)); // [1, 2, 3, 4, 5]
```

### Real-World Example: Data Buffer Management
```java
public class DataBuffer {
    private byte[] buffer;
    private int size;
    private int capacity;
    
    public DataBuffer(int initialCapacity) {
        this.capacity = initialCapacity;
        this.buffer = new byte[capacity];
        this.size = 0;
    }
    
    public void addData(byte[] data) {
        if (size + data.length > capacity) {
            // Expand buffer
            expandBuffer(size + data.length);
        }
        
        // Copy data to buffer
        System.arraycopy(data, 0, buffer, size, data.length);
        size += data.length;
    }
    
    public byte[] getData() {
        // Return copy of actual data
        return Arrays.copyOf(buffer, size);
    }
    
    public byte[] getData(int from, int to) {
        if (from < 0 || to > size || from >= to) {
            throw new IllegalArgumentException("Invalid range");
        }
        return Arrays.copyOfRange(buffer, from, to);
    }
    
    public void clear() {
        size = 0;
    }
    
    public void trim() {
        if (size < capacity) {
            // Trim buffer to actual size
            buffer = Arrays.copyOf(buffer, size);
            capacity = size;
        }
    }
    
    private void expandBuffer(int newCapacity) {
        // Double the capacity or use new capacity
        int newSize = Math.max(capacity * 2, newCapacity);
        buffer = Arrays.copyOf(buffer, newSize);
        capacity = newSize;
    }
    
    public int getSize() {
        return size;
    }
    
    public int getCapacity() {
        return capacity;
    }
    
    public boolean isEmpty() {
        return size == 0;
    }
}
```

## 10.6 Arrays Utility Best Practices

Following best practices ensures efficient and maintainable code when working with Arrays utility methods.

### 1. Choose the Right Method

#### Use sort() When:
- Need to order elements
- Performance is important
- Working with large arrays

```java
// Good: Use sort() for ordering
int[] numbers = {5, 2, 8, 1, 9};
Arrays.sort(numbers);
```

#### Use binarySearch() When:
- Array is already sorted
- Need efficient searching
- Working with large arrays

```java
// Good: Use binarySearch() for sorted arrays
Arrays.sort(numbers);
int index = Arrays.binarySearch(numbers, 5);
```

#### Use fill() When:
- Need to initialize array
- Set all elements to same value
- Clear array data

```java
// Good: Use fill() for initialization
int[] numbers = new int[10];
Arrays.fill(numbers, 0);
```

#### Use copyOf() When:
- Need to create array copy
- Resize array
- Preserve original array

```java
// Good: Use copyOf() for copying
int[] copy = Arrays.copyOf(original, newLength);
```

### 2. Handle Exceptions Properly

```java
// Good: Handle exceptions
try {
    int[] numbers = {1, 2, 3};
    int[] copy = Arrays.copyOfRange(numbers, 1, 5); // May throw exception
} catch (ArrayIndexOutOfBoundsException e) {
    System.out.println("Invalid range");
}
```

### 3. Use Appropriate Array Types

```java
// Good: Use appropriate array types
int[] numbers = new int[10]; // For integers
String[] names = new String[10]; // For strings
boolean[] flags = new boolean[10]; // For booleans

// Bad: Using Object array for primitives
Object[] numbers = new Object[10]; // Inefficient for primitives
```

### 4. Consider Performance Implications

```java
// Good: Sort once, search multiple times
Arrays.sort(numbers);
int index1 = Arrays.binarySearch(numbers, 5);
int index2 = Arrays.binarySearch(numbers, 7);

// Bad: Sort every time before searching
Arrays.sort(numbers);
int index1 = Arrays.binarySearch(numbers, 5);
Arrays.sort(numbers); // Unnecessary
int index2 = Arrays.binarySearch(numbers, 7);
```

## 10.7 Arrays Utility Testing

Comprehensive testing ensures Arrays utility methods work correctly and meet performance requirements.

### 1. Unit Testing

```java
@Test
public void testSortOperations() {
    int[] numbers = {5, 2, 8, 1, 9};
    
    // Test sort
    Arrays.sort(numbers);
    assertArrayEquals(new int[]{1, 2, 5, 8, 9}, numbers);
    
    // Test reverse
    Arrays.sort(numbers);
    for (int i = 0; i < numbers.length / 2; i++) {
        int temp = numbers[i];
        numbers[i] = numbers[numbers.length - 1 - i];
        numbers[numbers.length - 1 - i] = temp;
    }
    assertArrayEquals(new int[]{9, 8, 5, 2, 1}, numbers);
}
```

### 2. Performance Testing

```java
@Test
public void testSortPerformance() {
    int[] numbers = new int[100000];
    for (int i = 0; i < numbers.length; i++) {
        numbers[i] = (int) (Math.random() * 1000);
    }
    
    // Test sort performance
    long startTime = System.currentTimeMillis();
    Arrays.sort(numbers);
    long sortTime = System.currentTimeMillis() - startTime;
    
    // Test binary search performance
    startTime = System.currentTimeMillis();
    int index = Arrays.binarySearch(numbers, numbers[50000]);
    long searchTime = System.currentTimeMillis() - startTime;
    
    System.out.println("Sort time: " + sortTime + "ms");
    System.out.println("Search time: " + searchTime + "ms");
    
    assertTrue(sortTime < 1000); // Should complete within 1 second
    assertTrue(searchTime < 10);  // Should complete within 10ms
}
```

### 3. Edge Case Testing

```java
@Test
public void testEdgeCases() {
    // Test empty array
    int[] empty = {};
    Arrays.sort(empty);
    assertArrayEquals(new int[]{}, empty);
    
    // Test single element
    int[] single = {5};
    Arrays.sort(single);
    assertArrayEquals(new int[]{5}, single);
    
    // Test already sorted array
    int[] sorted = {1, 2, 3, 4, 5};
    Arrays.sort(sorted);
    assertArrayEquals(new int[]{1, 2, 3, 4, 5}, sorted);
}
```

## 10.8 Arrays Utility Performance

Understanding performance characteristics helps in choosing the right utility method and optimizing code.

### Performance Comparison

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| sort() | O(n log n) | O(1) |
| binarySearch() | O(log n) | O(1) |
| fill() | O(n) | O(1) |
| copyOf() | O(n) | O(n) |
| copyOfRange() | O(n) | O(n) |

### Memory Usage

```java
// sort() memory usage
Arrays.sort(array);
// Memory: O(1) additional space for in-place sorting

// binarySearch() memory usage
Arrays.binarySearch(array, key);
// Memory: O(1) additional space

// copyOf() memory usage
Arrays.copyOf(array, newLength);
// Memory: O(n) for new array

// fill() memory usage
Arrays.fill(array, value);
// Memory: O(1) additional space
```

### Performance Optimization Tips

#### 1. Use Appropriate Sorting Algorithm
```java
// Good: Use sort() for general purpose
Arrays.sort(array);

// Good: Use specialized sorting for specific cases
Arrays.sort(array, Collections.reverseOrder());
```

#### 2. Sort Once, Search Multiple Times
```java
// Good: Sort once, search multiple times
Arrays.sort(array);
int index1 = Arrays.binarySearch(array, key1);
int index2 = Arrays.binarySearch(array, key2);

// Bad: Sort every time before searching
Arrays.sort(array);
int index1 = Arrays.binarySearch(array, key1);
Arrays.sort(array); // Unnecessary
int index2 = Arrays.binarySearch(array, key2);
```

#### 3. Use Appropriate Array Types
```java
// Good: Use primitive arrays for primitives
int[] numbers = new int[1000];
Arrays.sort(numbers);

// Bad: Use Object arrays for primitives
Integer[] numbers = new Integer[1000];
Arrays.sort(numbers); // Slower due to boxing/unboxing
```

## 10.9 Arrays Utility Troubleshooting

Common issues and solutions when working with Arrays utility methods.

### 1. ArrayIndexOutOfBoundsException

```java
// Problem: Invalid range in copyOfRange
int[] array = {1, 2, 3, 4, 5};
int[] copy = Arrays.copyOfRange(array, 2, 10); // ArrayIndexOutOfBoundsException

// Solution: Check bounds before copying
if (from >= 0 && to <= array.length && from <= to) {
    int[] copy = Arrays.copyOfRange(array, from, to);
}
```

### 2. ClassCastException

```java
// Problem: Incompatible types in sorting
Object[] mixedArray = {1, "string", 3.14};
Arrays.sort(mixedArray); // ClassCastException

// Solution: Use appropriate types or comparators
String[] stringArray = {"c", "a", "b"};
Arrays.sort(stringArray); // OK
```

### 3. Performance Issues

```java
// Problem: Sorting large arrays frequently
int[] largeArray = new int[1000000];
for (int i = 0; i < 1000; i++) {
    Arrays.sort(largeArray); // O(n log n) each time
    // ... do something
}

// Solution: Sort once or use appropriate data structure
Arrays.sort(largeArray); // Sort once
// Or use TreeSet for automatically sorted data
TreeSet<Integer> sortedSet = new TreeSet<>();
```

### 4. Memory Issues

```java
// Problem: Creating too many copies
int[] original = new int[1000000];
for (int i = 0; i < 1000; i++) {
    int[] copy = Arrays.copyOf(original, original.length); // O(n) memory each time
    // ... do something
}

// Solution: Reuse arrays or use appropriate data structures
int[] copy = new int[original.length];
System.arraycopy(original, 0, copy, 0, original.length);
```

## 10.10 Arrays Utility Security

Security considerations when working with Arrays utility methods.

### 1. Input Validation

```java
public class SecureArraysManager {
    private int[] data;
    private int size;
    
    public SecureArraysManager(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("Capacity must be positive");
        }
        this.data = new int[capacity];
        this.size = 0;
    }
    
    public void addData(int[] newData) {
        if (newData == null) {
            throw new IllegalArgumentException("Data cannot be null");
        }
        
        if (size + newData.length > data.length) {
            throw new IllegalStateException("Not enough capacity");
        }
        
        System.arraycopy(newData, 0, data, size, newData.length);
        size += newData.length;
    }
    
    public int[] getSortedData() {
        int[] sortedData = Arrays.copyOf(data, size);
        Arrays.sort(sortedData);
        return sortedData;
    }
    
    public int[] searchData(int key) {
        int[] sortedData = Arrays.copyOf(data, size);
        Arrays.sort(sortedData);
        
        int index = Arrays.binarySearch(sortedData, key);
        if (index >= 0) {
            return new int[]{index};
        }
        return new int[0];
    }
}
```

### 2. Access Control

```java
public class SecureArraysWrapper {
    private int[] data;
    private Set<String> allowedUsers = new HashSet<>();
    
    public int[] getSortedData(String user) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        int[] sortedData = Arrays.copyOf(data, data.length);
        Arrays.sort(sortedData);
        return sortedData;
    }
    
    public void addData(String user, int[] newData) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        if (newData != null) {
            System.arraycopy(newData, 0, data, 0, Math.min(newData.length, data.length));
        }
    }
}
```

### 3. Data Encryption

```java
public class EncryptedArraysManager {
    private int[] encryptedData;
    private String encryptionKey = "secret-key";
    
    public void addEncryptedData(int[] data) {
        int[] encrypted = new int[data.length];
        for (int i = 0; i < data.length; i++) {
            encrypted[i] = encrypt(data[i], encryptionKey);
        }
        this.encryptedData = encrypted;
    }
    
    public int[] getSortedDecryptedData() {
        int[] decrypted = new int[encryptedData.length];
        for (int i = 0; i < encryptedData.length; i++) {
            decrypted[i] = decrypt(encryptedData[i], encryptionKey);
        }
        
        Arrays.sort(decrypted);
        return decrypted;
    }
    
    private int encrypt(int data, String key) {
        // Implementation of encryption
        return data; // Placeholder
    }
    
    private int decrypt(int encrypted, String key) {
        // Implementation of decryption
        return encrypted; // Placeholder
    }
}
```

Understanding the Arrays utility class is crucial for efficient array manipulation. These utility methods provide powerful tools for sorting, searching, filling, copying, and transformation, making array operations more efficient and maintainable.