# Section 2 - Java 1.0 - 1.4 (Classic Java Era)

## 2.1 Java 1.0 - The Beginning (1996)

Java 1.0 اولین نسخه رسمی جاوا بود که در سال 1996 منتشر شد. این نسخه پایه‌های زبان جاوا را بنا نهاد.

### ویژگی‌های کلیدی Java 1.0:

**1. Core Language Features:**
- Object-Oriented Programming
- Platform Independence (Write Once, Run Anywhere)
- Automatic Memory Management
- Strong Type System

**2. Basic APIs:**
- java.lang package (Object, String, Thread)
- java.io package (File I/O)
- java.util package (Basic collections)
- java.awt package (Abstract Window Toolkit)

**3. Security Model:**
- Sandbox security model
- Bytecode verification
- Class loader security

### مثال عملی Java 1.0 Style:

```java
// Java 1.0 style programming
import java.awt.*;
import java.awt.event.*;

public class ClassicJavaApp extends Frame {
    private Button button;
    private Label label;
    private int clickCount = 0;
    
    public ClassicJavaApp() {
        // Set up the frame
        setTitle("Java 1.0 Classic App");
        setSize(300, 200);
        setLayout(new FlowLayout());
        
        // Create components
        label = new Label("کلیک کنید: 0");
        button = new Button("کلیک");
        
        // Add event listener (Java 1.0 style)
        button.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                clickCount++;
                label.setText("کلیک کنید: " + clickCount);
            }
        });
        
        // Add components to frame
        add(label);
        add(button);
        
        // Handle window closing
        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                System.exit(0);
            }
        });
    }
    
    public static void main(String[] args) {
        ClassicJavaApp app = new ClassicJavaApp();
        app.setVisible(true);
    }
}
```

### محدودیت‌های Java 1.0:

**1. Collection Framework:**
- فقط Vector و Hashtable موجود بود
- هیچ interface مشترکی وجود نداشت
- Performance ضعیف

**2. I/O Operations:**
- فقط byte streams
- Character streams در Java 1.1 اضافه شد

**3. Exception Handling:**
- محدودیت‌های exception handling
- No try-with-resources

### آنالوژی دنیای واقعی:
Java 1.0 مانند اولین خودروی تولید شده است - عملکرد اصلی را دارد اما امکانات رفاهی کمی دارد. مانند خودروی مدل T فورد که پایه‌های صنعت خودروسازی را بنا نهاد.

## 2.2 Java 1.1 - Inner Classes & Reflection (1997)

Java 1.1 در سال 1997 منتشر شد و ویژگی‌های مهمی را به زبان جاوا اضافه کرد.

### ویژگی‌های جدید Java 1.1:

**1. Inner Classes:**
- Member classes
- Local classes
- Anonymous classes
- Static nested classes

**2. Reflection API:**
- java.lang.reflect package
- Runtime class inspection
- Dynamic method invocation

**3. Character Streams:**
- Reader/Writer classes
- Better text handling

**4. JDBC (Java Database Connectivity):**
- Database connectivity
- SQL operations

### مثال عملی Inner Classes:

```java
public class InnerClassesExample {
    private String outerField = "فیلد خارجی";
    private static String staticOuterField = "فیلد استاتیک خارجی";
    
    // 1. Member Inner Class
    class MemberInnerClass {
        private String innerField = "فیلد داخلی";
        
        public void display() {
            System.out.println("Member Inner Class:");
            System.out.println("Outer field: " + outerField);
            System.out.println("Inner field: " + innerField);
        }
    }
    
    // 2. Static Nested Class
    static class StaticNestedClass {
        private String nestedField = "فیلد تودرتو";
        
        public void display() {
            System.out.println("Static Nested Class:");
            System.out.println("Static outer field: " + staticOuterField);
            System.out.println("Nested field: " + nestedField);
        }
    }
    
    public void demonstrateInnerClasses() {
        // 3. Local Class
        class LocalClass {
            private String localField = "فیلد محلی";
            
            public void display() {
                System.out.println("Local Class:");
                System.out.println("Outer field: " + outerField);
                System.out.println("Local field: " + localField);
            }
        }
        
        // 4. Anonymous Class
        Runnable anonymousRunnable = new Runnable() {
            private String anonymousField = "فیلد ناشناس";
            
            @Override
            public void run() {
                System.out.println("Anonymous Class:");
                System.out.println("Outer field: " + outerField);
                System.out.println("Anonymous field: " + anonymousField);
            }
        };
        
        // Use all classes
        MemberInnerClass memberInner = new MemberInnerClass();
        memberInner.display();
        
        StaticNestedClass staticNested = new StaticNestedClass();
        staticNested.display();
        
        LocalClass local = new LocalClass();
        local.display();
        
        anonymousRunnable.run();
    }
    
    public static void main(String[] args) {
        InnerClassesExample example = new InnerClassesExample();
        example.demonstrateInnerClasses();
    }
}
```

### مثال عملی Reflection API:

```java
import java.lang.reflect.*;

public class ReflectionExample {
    private String name;
    private int age;
    
    public ReflectionExample(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public void displayInfo() {
        System.out.println("نام: " + name + ", سن: " + age);
    }
    
    private void privateMethod() {
        System.out.println("این یک متد خصوصی است");
    }
    
    public static void main(String[] args) {
        try {
            // 1. Get Class object
            Class<?> clazz = ReflectionExample.class;
            System.out.println("نام کلاس: " + clazz.getName());
            
            // 2. Get constructors
            System.out.println("\n=== Constructors ===");
            Constructor<?>[] constructors = clazz.getConstructors();
            for (Constructor<?> constructor : constructors) {
                System.out.println("Constructor: " + constructor);
            }
            
            // 3. Get fields
            System.out.println("\n=== Fields ===");
            Field[] fields = clazz.getDeclaredFields();
            for (Field field : fields) {
                System.out.println("Field: " + field.getName() + " - " + field.getType());
            }
            
            // 4. Get methods
            System.out.println("\n=== Methods ===");
            Method[] methods = clazz.getDeclaredMethods();
            for (Method method : methods) {
                System.out.println("Method: " + method.getName() + " - " + method.getReturnType());
            }
            
            // 5. Create instance using reflection
            System.out.println("\n=== Creating Instance ===");
            Constructor<?> constructor = clazz.getConstructor(String.class, int.class);
            Object instance = constructor.newInstance("احمد", 25);
            
            // 6. Invoke method
            Method displayMethod = clazz.getMethod("displayInfo");
            displayMethod.invoke(instance);
            
            // 7. Access private field
            System.out.println("\n=== Accessing Private Field ===");
            Field nameField = clazz.getDeclaredField("name");
            nameField.setAccessible(true);
            String nameValue = (String) nameField.get(instance);
            System.out.println("نام از طریق reflection: " + nameValue);
            
            // 8. Invoke private method
            System.out.println("\n=== Invoking Private Method ===");
            Method privateMethod = clazz.getDeclaredMethod("privateMethod");
            privateMethod.setAccessible(true);
            privateMethod.invoke(instance);
            
        } catch (Exception e) {
            System.err.println("خطا در reflection: " + e.getMessage());
        }
    }
}
```

### مثال عملی Character Streams:

```java
import java.io.*;

public class CharacterStreamsExample {
    public static void main(String[] args) {
        // 1. File Reading with Character Streams
        System.out.println("=== Character Streams ===");
        
        // Write text file
        writeTextFile("sample.txt", "سلام دنیا!\nاین یک فایل متنی است.");
        
        // Read text file
        readTextFile("sample.txt");
        
        // 2. BufferedReader example
        System.out.println("\n=== BufferedReader ===");
        readWithBufferedReader("sample.txt");
        
        // 3. StringReader example
        System.out.println("\n=== StringReader ===");
        readFromString("این یک رشته نمونه است");
    }
    
    public static void writeTextFile(String filename, String content) {
        try (FileWriter writer = new FileWriter(filename)) {
            writer.write(content);
            System.out.println("فایل متنی نوشته شد: " + filename);
        } catch (IOException e) {
            System.err.println("خطا در نوشتن فایل: " + e.getMessage());
        }
    }
    
    public static void readTextFile(String filename) {
        try (FileReader reader = new FileReader(filename)) {
            int character;
            System.out.println("محتوای فایل:");
            while ((character = reader.read()) != -1) {
                System.out.print((char) character);
            }
            System.out.println();
        } catch (IOException e) {
            System.err.println("خطا در خواندن فایل: " + e.getMessage());
        }
    }
    
    public static void readWithBufferedReader(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            System.out.println("خواندن خط به خط:");
            while ((line = reader.readLine()) != null) {
                System.out.println("خط: " + line);
            }
        } catch (IOException e) {
            System.err.println("خطا در خواندن بافر: " + e.getMessage());
        }
    }
    
    public static void readFromString(String content) {
        try (StringReader reader = new StringReader(content)) {
            int character;
            System.out.println("خواندن از رشته:");
            while ((character = reader.read()) != -1) {
                System.out.print((char) character);
            }
            System.out.println();
        } catch (IOException e) {
            System.err.println("خطا در خواندن رشته: " + e.getMessage());
        }
    }
}
```

### آنالوژی دنیای واقعی:
Java 1.1 مانند اضافه کردن آینه‌های جانبی و سیستم صوتی به خودرو است - عملکرد اصلی همان است اما امکانات بیشتری برای راحتی و کارایی اضافه شده است.

## 2.3 Java 1.2 - Collections Framework (1998)

Java 1.2 در سال 1998 منتشر شد و Collections Framework را معرفی کرد که یکی از مهم‌ترین پیشرفت‌های جاوا محسوب می‌شود.

### ویژگی‌های کلیدی Java 1.2:

**1. Collections Framework:**
- List, Set, Map interfaces
- ArrayList, LinkedList, HashSet, TreeSet, HashMap, TreeMap
- Iterator pattern
- Collections utility class

**2. Swing GUI Framework:**
- JFC (Java Foundation Classes)
- Lightweight components
- Pluggable Look and Feel

**3. Java 2D API:**
- Advanced graphics
- Image processing
- Font rendering

### مثال عملی Collections Framework:

```java
import java.util.*;

public class CollectionsFrameworkExample {
    public static void main(String[] args) {
        // 1. List Examples
        System.out.println("=== List Examples ===");
        demonstrateLists();
        
        // 2. Set Examples
        System.out.println("\n=== Set Examples ===");
        demonstrateSets();
        
        // 3. Map Examples
        System.out.println("\n=== Map Examples ===");
        demonstrateMaps();
        
        // 4. Iterator Examples
        System.out.println("\n=== Iterator Examples ===");
        demonstrateIterators();
        
        // 5. Collections Utility
        System.out.println("\n=== Collections Utility ===");
        demonstrateCollectionsUtility();
    }
    
    public static void demonstrateLists() {
        // ArrayList
        List<String> arrayList = new ArrayList<>();
        arrayList.add("اولین");
        arrayList.add("دومین");
        arrayList.add("سومین");
        arrayList.add("دومین"); // Duplicate allowed
        
        System.out.println("ArrayList: " + arrayList);
        System.out.println("اندازه: " + arrayList.size());
        System.out.println("عنصر در ایندکس 1: " + arrayList.get(1));
        
        // LinkedList
        List<Integer> linkedList = new LinkedList<>();
        linkedList.add(10);
        linkedList.add(20);
        linkedList.add(30);
        
        System.out.println("LinkedList: " + linkedList);
        
        // Vector (legacy, synchronized)
        Vector<String> vector = new Vector<>();
        vector.add("عنصر 1");
        vector.add("عنصر 2");
        System.out.println("Vector: " + vector);
    }
    
    public static void demonstrateSets() {
        // HashSet
        Set<String> hashSet = new HashSet<>();
        hashSet.add("قرمز");
        hashSet.add("سبز");
        hashSet.add("آبی");
        hashSet.add("قرمز"); // Duplicate ignored
        
        System.out.println("HashSet: " + hashSet);
        System.out.println("حاوی 'سبز': " + hashSet.contains("سبز"));
        
        // TreeSet (sorted)
        Set<Integer> treeSet = new TreeSet<>();
        treeSet.add(50);
        treeSet.add(10);
        treeSet.add(30);
        treeSet.add(20);
        System.out.println("TreeSet (مرتب): " + treeSet);
        
        // LinkedHashSet (maintains insertion order)
        Set<String> linkedHashSet = new LinkedHashSet<>();
        linkedHashSet.add("اولین");
        linkedHashSet.add("دومین");
        linkedHashSet.add("سومین");
        System.out.println("LinkedHashSet: " + linkedHashSet);
    }
    
    public static void demonstrateMaps() {
        // HashMap
        Map<String, Integer> studentGrades = new HashMap<>();
        studentGrades.put("احمد", 18);
        studentGrades.put("فاطمه", 19);
        studentGrades.put("علی", 17);
        studentGrades.put("زهرا", 20);
        
        System.out.println("نمرات دانشجویان: " + studentGrades);
        System.out.println("نمره احمد: " + studentGrades.get("احمد"));
        
        // TreeMap (sorted by key)
        Map<String, Integer> sortedGrades = new TreeMap<>(studentGrades);
        System.out.println("نمرات مرتب: " + sortedGrades);
        
        // Hashtable (legacy, synchronized)
        Hashtable<String, String> hashtable = new Hashtable<>();
        hashtable.put("کلید1", "مقدار1");
        hashtable.put("کلید2", "مقدار2");
        System.out.println("Hashtable: " + hashtable);
    }
    
    public static void demonstrateIterators() {
        List<String> list = Arrays.asList("آ", "ب", "پ", "ت", "ث");
        
        // Iterator
        System.out.println("با Iterator:");
        Iterator<String> iterator = list.iterator();
        while (iterator.hasNext()) {
            System.out.println(iterator.next());
        }
        
        // ListIterator (bidirectional)
        System.out.println("\nبا ListIterator (معکوس):");
        ListIterator<String> listIterator = list.listIterator(list.size());
        while (listIterator.hasPrevious()) {
            System.out.println(listIterator.previous());
        }
    }
    
    public static void demonstrateCollectionsUtility() {
        List<Integer> numbers = new ArrayList<>(Arrays.asList(5, 2, 8, 1, 9, 3));
        
        System.out.println("لیست اصلی: " + numbers);
        
        // Sort
        Collections.sort(numbers);
        System.out.println("مرتب شده: " + numbers);
        
        // Reverse
        Collections.reverse(numbers);
        System.out.println("معکوس: " + numbers);
        
        // Shuffle
        Collections.shuffle(numbers);
        System.out.println("تصادفی: " + numbers);
        
        // Binary search (list must be sorted)
        Collections.sort(numbers);
        int index = Collections.binarySearch(numbers, 5);
        System.out.println("ایندکس 5: " + index);
        
        // Min and Max
        System.out.println("حداقل: " + Collections.min(numbers));
        System.out.println("حداکثر: " + Collections.max(numbers));
        
        // Frequency
        numbers.add(5);
        numbers.add(5);
        System.out.println("تکرار 5: " + Collections.frequency(numbers, 5));
    }
}
```

### مثال عملی Swing GUI:

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class SwingExample extends JFrame {
    private JLabel label;
    private JButton button;
    private JTextField textField;
    private JList<String> list;
    private DefaultListModel<String> listModel;
    
    public SwingExample() {
        initializeComponents();
        setupLayout();
        addEventListeners();
    }
    
    private void initializeComponents() {
        setTitle("Java 1.2 Swing Example");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(400, 300);
        
        // Create components
        label = new JLabel("برنامه Swing");
        button = new JButton("کلیک کنید");
        textField = new JTextField(20);
        
        // Create list
        listModel = new DefaultListModel<>();
        listModel.addElement("آیتم 1");
        listModel.addElement("آیتم 2");
        listModel.addElement("آیتم 3");
        list = new JList<>(listModel);
        list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
    }
    
    private void setupLayout() {
        setLayout(new BorderLayout());
        
        // North panel
        JPanel northPanel = new JPanel(new FlowLayout());
        northPanel.add(label);
        northPanel.add(textField);
        northPanel.add(button);
        
        // Center panel
        JScrollPane scrollPane = new JScrollPane(list);
        
        // Add to frame
        add(northPanel, BorderLayout.NORTH);
        add(scrollPane, BorderLayout.CENTER);
    }
    
    private void addEventListeners() {
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String text = textField.getText();
                if (!text.isEmpty()) {
                    listModel.addElement(text);
                    textField.setText("");
                }
            }
        });
        
        list.addListSelectionListener(new ListSelectionListener() {
            @Override
            public void valueChanged(ListSelectionEvent e) {
                if (!e.getValueIsAdjusting()) {
                    String selected = list.getSelectedValue();
                    if (selected != null) {
                        label.setText("انتخاب شده: " + selected);
                    }
                }
            }
        });
    }
    
    public static void main(String[] args) {
        // Set Look and Feel
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeel());
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        // Create and show frame
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new SwingExample().setVisible(true);
            }
        });
    }
}
```

### آنالوژی دنیای واقعی:
Java 1.2 مانند اضافه کردن سیستم ناوبری و کروز کنترل به خودرو است - امکانات پیشرفته‌ای که تجربه رانندگی را به طور قابل توجهی بهبود می‌بخشد.

## 2.4 Java 1.3 - HotSpot JVM (2000)

Java 1.3 در سال 2000 منتشر شد و HotSpot JVM را معرفی کرد که عملکرد جاوا را به طور قابل توجهی بهبود بخشید.

### ویژگی‌های کلیدی Java 1.3:

**1. HotSpot JVM:**
- Just-In-Time (JIT) compilation
- Adaptive optimization
- Better garbage collection
- Improved performance

**2. Java Sound API:**
- Audio playback and recording
- MIDI support
- Sound effects

**3. Java Naming and Directory Interface (JNDI):**
- Directory services
- Naming services
- LDAP support

**4. RMI Improvements:**
- Better remote method invocation
- Improved serialization

### مثال عملی HotSpot JVM Performance:

```java
public class HotSpotPerformanceExample {
    private static final int ITERATIONS = 1000000;
    
    public static void main(String[] args) {
        System.out.println("=== HotSpot JVM Performance Test ===");
        
        // 1. Method Call Optimization
        System.out.println("Testing method call optimization...");
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < ITERATIONS; i++) {
            performCalculation(i);
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Method calls completed in: " + (endTime - startTime) + " ms");
        
        // 2. Loop Optimization
        System.out.println("\nTesting loop optimization...");
        startTime = System.currentTimeMillis();
        
        int sum = 0;
        for (int i = 0; i < ITERATIONS; i++) {
            sum += i;
        }
        
        endTime = System.currentTimeMillis();
        System.out.println("Loop completed in: " + (endTime - startTime) + " ms");
        System.out.println("Sum: " + sum);
        
        // 3. String Concatenation Optimization
        System.out.println("\nTesting string concatenation...");
        startTime = System.currentTimeMillis();
        
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 10000; i++) {
            sb.append("item").append(i).append(" ");
        }
        String result = sb.toString();
        
        endTime = System.currentTimeMillis();
        System.out.println("String concatenation completed in: " + (endTime - startTime) + " ms");
        System.out.println("Result length: " + result.length());
        
        // 4. Array Access Optimization
        System.out.println("\nTesting array access...");
        int[] array = new int[100000];
        startTime = System.currentTimeMillis();
        
        for (int i = 0; i < array.length; i++) {
            array[i] = i * 2;
        }
        
        endTime = System.currentTimeMillis();
        System.out.println("Array access completed in: " + (endTime - startTime) + " ms");
    }
    
    private static int performCalculation(int value) {
        // Simple calculation that can be optimized by HotSpot
        return value * value + value * 2 + 1;
    }
}
```

### مثال عملی Java Sound API:

```java
import javax.sound.sampled.*;
import java.io.*;

public class JavaSoundExample {
    public static void main(String[] args) {
        System.out.println("=== Java Sound API Example ===");
        
        // 1. List available audio formats
        listAudioFormats();
        
        // 2. Play a simple tone
        playTone(440, 1000); // 440 Hz for 1 second
        
        // 3. Record audio (if microphone is available)
        // recordAudio();
    }
    
    public static void listAudioFormats() {
        System.out.println("Available audio formats:");
        
        AudioFormat[] formats = {
            new AudioFormat(44100, 16, 2, true, false), // CD quality
            new AudioFormat(22050, 16, 1, true, false), // Mono
            new AudioFormat(8000, 8, 1, true, false)    // Telephone quality
        };
        
        for (AudioFormat format : formats) {
            System.out.println("Sample Rate: " + format.getSampleRate() + 
                             ", Channels: " + format.getChannels() + 
                             ", Sample Size: " + format.getSampleSizeInBits());
        }
    }
    
    public static void playTone(int frequency, int duration) {
        try {
            AudioFormat format = new AudioFormat(44100, 16, 1, true, false);
            DataLine.Info info = new DataLine.Info(SourceDataLine.class, format);
            
            if (!AudioSystem.isLineSupported(info)) {
                System.out.println("Audio line not supported");
                return;
            }
            
            SourceDataLine line = (SourceDataLine) AudioSystem.getLine(info);
            line.open(format);
            line.start();
            
            // Generate sine wave
            byte[] buffer = new byte[1024];
            int samples = (int) (format.getSampleRate() * duration / 1000.0);
            
            for (int i = 0; i < samples; i += buffer.length) {
                int length = Math.min(buffer.length, samples - i);
                
                for (int j = 0; j < length; j++) {
                    double angle = 2.0 * Math.PI * frequency * (i + j) / format.getSampleRate();
                    short sample = (short) (Short.MAX_VALUE * Math.sin(angle));
                    buffer[j * 2] = (byte) (sample & 0xFF);
                    buffer[j * 2 + 1] = (byte) ((sample >> 8) & 0xFF);
                }
                
                line.write(buffer, 0, length * 2);
            }
            
            line.drain();
            line.close();
            
        } catch (Exception e) {
            System.err.println("Error playing tone: " + e.getMessage());
        }
    }
}
```

### مثال عملی JNDI:

```java
import javax.naming.*;
import java.util.Hashtable;

public class JNDIExample {
    public static void main(String[] args) {
        System.out.println("=== JNDI Example ===");
        
        // 1. Basic JNDI operations
        demonstrateBasicJNDI();
        
        // 2. Context operations
        demonstrateContextOperations();
    }
    
    public static void demonstrateBasicJNDI() {
        try {
            // Create initial context
            Hashtable<String, String> env = new Hashtable<>();
            env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.fscontext.RefFSContextFactory");
            env.put(Context.PROVIDER_URL, "file:///tmp");
            
            Context ctx = new InitialContext(env);
            
            // Bind an object
            String name = "testObject";
            String value = "Hello JNDI";
            ctx.bind(name, value);
            
            // Lookup the object
            String retrieved = (String) ctx.lookup(name);
            System.out.println("Retrieved value: " + retrieved);
            
            // List context
            NamingEnumeration<NameClassPair> list = ctx.list("");
            System.out.println("Context contents:");
            while (list.hasMore()) {
                NameClassPair pair = list.next();
                System.out.println("Name: " + pair.getName() + ", Class: " + pair.getClassName());
            }
            
            // Unbind
            ctx.unbind(name);
            System.out.println("Object unbound successfully");
            
            ctx.close();
            
        } catch (Exception e) {
            System.err.println("JNDI error: " + e.getMessage());
        }
    }
    
    public static void demonstrateContextOperations() {
        try {
            // Create context
            Context ctx = new InitialContext();
            
            // Create subcontext
            Context subCtx = ctx.createSubcontext("testSubcontext");
            System.out.println("Subcontext created");
            
            // Bind in subcontext
            subCtx.bind("subObject", "Subcontext object");
            System.out.println("Object bound in subcontext");
            
            // Lookup in subcontext
            String value = (String) subCtx.lookup("subObject");
            System.out.println("Retrieved from subcontext: " + value);
            
            // Close contexts
            subCtx.close();
            ctx.close();
            
        } catch (Exception e) {
            System.err.println("Context operation error: " + e.getMessage());
        }
    }
}
```

### آنالوژی دنیای واقعی:
Java 1.3 مانند اضافه کردن موتور V8 به خودرو است - همان بدنه و امکانات قبلی اما با قدرت و کارایی بسیار بیشتر.

## 2.5 Java 1.4 - Assertions & Regular Expressions (2002)

Java 1.4 در سال 2002 منتشر شد و ویژگی‌های مهمی مانند Assertions و Regular Expressions را معرفی کرد.

### ویژگی‌های کلیدی Java 1.4:

**1. Assertions:**
- Runtime assertions
- Debugging support
- Performance testing

**2. Regular Expressions:**
- java.util.regex package
- Pattern and Matcher classes
- String regex methods

**3. NIO (New I/O):**
- Non-blocking I/O
- Memory-mapped files
- File locking

**4. Logging API:**
- java.util.logging package
- Configurable logging
- Multiple log levels

### مثال عملی Assertions:

```java
public class AssertionsExample {
    private int balance;
    
    public AssertionsExample(int initialBalance) {
        // Assertion for constructor
        assert initialBalance >= 0 : "موجودی اولیه نمی‌تواند منفی باشد";
        this.balance = initialBalance;
    }
    
    public void deposit(int amount) {
        // Assertion for method parameter
        assert amount > 0 : "مبلغ واریز باید مثبت باشد";
        
        int oldBalance = balance;
        balance += amount;
        
        // Assertion for method result
        assert balance == oldBalance + amount : "محاسبه موجودی نادرست است";
        assert balance >= 0 : "موجودی نمی‌تواند منفی باشد";
    }
    
    public void withdraw(int amount) {
        // Assertion for method parameter
        assert amount > 0 : "مبلغ برداشت باید مثبت باشد";
        assert amount <= balance : "مبلغ برداشت بیشتر از موجودی است";
        
        int oldBalance = balance;
        balance -= amount;
        
        // Assertion for method result
        assert balance == oldBalance - amount : "محاسبه موجودی نادرست است";
        assert balance >= 0 : "موجودی نمی‌تواند منفی باشد";
    }
    
    public int getBalance() {
        return balance;
    }
    
    // Method to demonstrate assertion usage
    public void demonstrateAssertions() {
        System.out.println("=== Assertions Demo ===");
        
        // Enable assertions programmatically
        ClassLoader.getSystemClassLoader().setDefaultAssertionStatus(true);
        
        try {
            // Valid operations
            deposit(100);
            System.out.println("واریز 100: موجودی = " + getBalance());
            
            withdraw(50);
            System.out.println("برداشت 50: موجودی = " + getBalance());
            
            // This will trigger assertion error
            withdraw(100); // More than balance
            
        } catch (AssertionError e) {
            System.out.println("Assertion error: " + e.getMessage());
        }
    }
    
    public static void main(String[] args) {
        // Enable assertions with -ea flag
        AssertionsExample account = new AssertionsExample(100);
        account.demonstrateAssertions();
    }
}
```

### مثال عملی Regular Expressions:

```java
import java.util.regex.*;
import java.util.*;

public class RegularExpressionsExample {
    public static void main(String[] args) {
        System.out.println("=== Regular Expressions Examples ===");
        
        // 1. Basic pattern matching
        demonstrateBasicPatterns();
        
        // 2. Email validation
        demonstrateEmailValidation();
        
        // 3. Phone number validation
        demonstratePhoneValidation();
        
        // 4. Text processing
        demonstrateTextProcessing();
        
        // 5. Group capturing
        demonstrateGroupCapturing();
    }
    
    public static void demonstrateBasicPatterns() {
        System.out.println("\n=== Basic Pattern Matching ===");
        
        String text = "Java 1.4 introduced regular expressions in 2002";
        
        // Simple pattern
        Pattern pattern = Pattern.compile("Java");
        Matcher matcher = pattern.matcher(text);
        
        System.out.println("Text: " + text);
        System.out.println("Pattern: Java");
        System.out.println("Found: " + matcher.find());
        
        // Case insensitive
        pattern = Pattern.compile("java", Pattern.CASE_INSENSITIVE);
        matcher = pattern.matcher(text);
        System.out.println("Case insensitive 'java': " + matcher.find());
        
        // Word boundaries
        pattern = Pattern.compile("\\bJava\\b");
        matcher = pattern.matcher(text);
        System.out.println("Word 'Java': " + matcher.find());
    }
    
    public static void demonstrateEmailValidation() {
        System.out.println("\n=== Email Validation ===");
        
        String emailPattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$";
        Pattern pattern = Pattern.compile(emailPattern);
        
        String[] emails = {
            "user@example.com",
            "test.email@domain.co.uk",
            "invalid.email",
            "user@",
            "@domain.com"
        };
        
        for (String email : emails) {
            Matcher matcher = pattern.matcher(email);
            System.out.println(email + " -> " + (matcher.matches() ? "Valid" : "Invalid"));
        }
    }
    
    public static void demonstratePhoneValidation() {
        System.out.println("\n=== Phone Number Validation ===");
        
        // Iranian phone number pattern
        String phonePattern = "^(\\+98|0)?9\\d{9}$";
        Pattern pattern = Pattern.compile(phonePattern);
        
        String[] phones = {
            "09123456789",
            "00989123456789",
            "+989123456789",
            "9123456789",
            "08123456789", // Invalid
            "1234567890"   // Invalid
        };
        
        for (String phone : phones) {
            Matcher matcher = pattern.matcher(phone);
            System.out.println(phone + " -> " + (matcher.matches() ? "Valid" : "Invalid"));
        }
    }
    
    public static void demonstrateTextProcessing() {
        System.out.println("\n=== Text Processing ===");
        
        String text = "Java 1.4 was released in 2002. It introduced many new features.";
        
        // Find all numbers
        Pattern numberPattern = Pattern.compile("\\d+");
        Matcher matcher = numberPattern.matcher(text);
        
        System.out.println("Text: " + text);
        System.out.println("Numbers found:");
        while (matcher.find()) {
            System.out.println("  " + matcher.group());
        }
        
        // Replace numbers with [NUMBER]
        String replaced = text.replaceAll("\\d+", "[NUMBER]");
        System.out.println("After replacement: " + replaced);
        
        // Split by non-word characters
        String[] words = text.split("\\W+");
        System.out.println("Words: " + Arrays.toString(words));
    }
    
    public static void demonstrateGroupCapturing() {
        System.out.println("\n=== Group Capturing ===");
        
        String text = "احمد محمدی 25 ساله از تهران";
        
        // Pattern with groups
        String pattern = "(\\w+)\\s+(\\w+)\\s+(\\d+)\\s+ساله\\s+از\\s+(\\w+)";
        Pattern compiledPattern = Pattern.compile(pattern);
        Matcher matcher = compiledPattern.matcher(text);
        
        System.out.println("Text: " + text);
        System.out.println("Pattern: " + pattern);
        
        if (matcher.find()) {
            System.out.println("نام: " + matcher.group(1));
            System.out.println("نام خانوادگی: " + matcher.group(2));
            System.out.println("سن: " + matcher.group(3));
            System.out.println("شهر: " + matcher.group(4));
        } else {
            System.out.println("Pattern not found");
        }
    }
}
```

### مثال عملی NIO:

```java
import java.nio.*;
import java.nio.channels.*;
import java.nio.file.*;
import java.io.*;

public class NIOExample {
    public static void main(String[] args) {
        System.out.println("=== NIO Examples ===");
        
        // 1. Buffer operations
        demonstrateBuffers();
        
        // 2. File operations
        demonstrateFileOperations();
        
        // 3. Channel operations
        demonstrateChannels();
    }
    
    public static void demonstrateBuffers() {
        System.out.println("\n=== Buffer Operations ===");
        
        // Create buffer
        ByteBuffer buffer = ByteBuffer.allocate(1024);
        
        System.out.println("Buffer created:");
        System.out.println("Capacity: " + buffer.capacity());
        System.out.println("Position: " + buffer.position());
        System.out.println("Limit: " + buffer.limit());
        
        // Write data
        String data = "Hello NIO World!";
        buffer.put(data.getBytes());
        
        System.out.println("\nAfter writing data:");
        System.out.println("Position: " + buffer.position());
        System.out.println("Limit: " + buffer.limit());
        
        // Flip for reading
        buffer.flip();
        
        System.out.println("\nAfter flip:");
        System.out.println("Position: " + buffer.position());
        System.out.println("Limit: " + buffer.limit());
        
        // Read data
        byte[] readData = new byte[buffer.remaining()];
        buffer.get(readData);
        System.out.println("Read data: " + new String(readData));
        
        // Clear buffer
        buffer.clear();
        System.out.println("\nAfter clear:");
        System.out.println("Position: " + buffer.position());
        System.out.println("Limit: " + buffer.limit());
    }
    
    public static void demonstrateFileOperations() {
        System.out.println("\n=== File Operations ===");
        
        try {
            // Create test file
            Path file = Paths.get("nio_test.txt");
            Files.write(file, "This is a NIO test file".getBytes());
            
            // Read file using NIO
            byte[] content = Files.readAllBytes(file);
            System.out.println("File content: " + new String(content));
            
            // Copy file
            Path copyFile = Paths.get("nio_test_copy.txt");
            Files.copy(file, copyFile, StandardCopyOption.REPLACE_EXISTING);
            System.out.println("File copied successfully");
            
            // Delete files
            Files.delete(file);
            Files.delete(copyFile);
            System.out.println("Files deleted successfully");
            
        } catch (IOException e) {
            System.err.println("File operation error: " + e.getMessage());
        }
    }
    
    public static void demonstrateChannels() {
        System.out.println("\n=== Channel Operations ===");
        
        try {
            // Create test file
            Path file = Paths.get("channel_test.txt");
            String content = "This is a channel test file\nLine 2\nLine 3";
            Files.write(file, content.getBytes());
            
            // Read using FileChannel
            try (FileChannel channel = FileChannel.open(file, StandardOpenOption.READ)) {
                ByteBuffer buffer = ByteBuffer.allocate(1024);
                int bytesRead = channel.read(buffer);
                
                buffer.flip();
                byte[] data = new byte[buffer.remaining()];
                buffer.get(data);
                
                System.out.println("Read from channel: " + new String(data));
            }
            
            // Write using FileChannel
            try (FileChannel channel = FileChannel.open(file, StandardOpenOption.WRITE)) {
                String newContent = "New content written via channel";
                ByteBuffer buffer = ByteBuffer.wrap(newContent.getBytes());
                channel.write(buffer);
                System.out.println("Content written via channel");
            }
            
            // Clean up
            Files.delete(file);
            
        } catch (IOException e) {
            System.err.println("Channel operation error: " + e.getMessage());
        }
    }
}
```

### آنالوژی دنیای واقعی:
Java 1.4 مانند اضافه کردن سیستم ترمز ABS و کیسه هوا به خودرو است - ویژگی‌های ایمنی و امنیتی که تجربه رانندگی را بهبود می‌بخشد و از مشکلات احتمالی جلوگیری می‌کند.