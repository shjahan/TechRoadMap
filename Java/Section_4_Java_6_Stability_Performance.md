# Section 4 - Java 6 - Stability & Performance

## 4.1 Scripting Engine Support

Java 6 با معرفی Scripting Engine Support امکان اجرای زبان‌های اسکریپت‌نویسی مختلف را در داخل برنامه‌های Java فراهم کرد.

### مفاهیم کلیدی:

**1. Scripting API:**
- `javax.script` package                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
- Multiple scripting languages support
- Dynamic script execution

**2. Supported Languages:**
- JavaScript (Rhino engine)
- Python (Jython)
- Ruby (JRuby)
- Groovy

### مثال عملی:

```java
import javax.script.*;
import java.io.FileReader;

public class ScriptingEngineExample {
    public static void main(String[] args) {
        System.out.println("=== Scripting Engine Support ===");
        
        // 1. Basic JavaScript execution
        demonstrateJavaScript();
        
        // 2. Script with variables
        demonstrateScriptVariables();
        
        // 3. Script file execution
        demonstrateScriptFile();
        
        // 4. Error handling
        demonstrateErrorHandling();
    }
    
    public static void demonstrateJavaScript() {
        try {
            ScriptEngineManager manager = new ScriptEngineManager();
            ScriptEngine engine = manager.getEngineByName("javascript");
            
            if (engine == null) {
                System.out.println("JavaScript engine not available");
                return;
            }
            
            // Execute simple JavaScript
            engine.eval("print('Hello from JavaScript!')");
            
            // Execute JavaScript with calculations
            Object result = engine.eval("2 + 3 * 4");
            System.out.println("JavaScript calculation result: " + result);
            
            // Execute JavaScript function
            engine.eval("function factorial(n) { return n <= 1 ? 1 : n * factorial(n-1); }");
            Object factorialResult = engine.eval("factorial(5)");
            System.out.println("Factorial of 5: " + factorialResult);
            
        } catch (ScriptException e) {
            System.err.println("Script execution error: " + e.getMessage());
        }
    }
    
    public static void demonstrateScriptVariables() {
        try {
            ScriptEngineManager manager = new ScriptEngineManager();
            ScriptEngine engine = manager.getEngineByName("javascript");
            
            if (engine == null) {
                System.out.println("JavaScript engine not available");
                return;
            }
            
            // Set variables in script context
            ScriptContext context = engine.getContext();
            context.setAttribute("name", "احمد محمدی", ScriptContext.ENGINE_SCOPE);
            context.setAttribute("age", 25, ScriptContext.ENGINE_SCOPE);
            
            // Execute script that uses variables
            engine.eval("print('Name: ' + name + ', Age: ' + age)");
            
            // Get variables from script
            engine.eval("var message = 'Hello ' + name;");
            Object message = engine.get("message");
            System.out.println("Message from script: " + message);
            
        } catch (ScriptException e) {
            System.err.println("Script execution error: " + e.getMessage());
        }
    }
    
    public static void demonstrateScriptFile() {
        try {
            ScriptEngineManager manager = new ScriptEngineManager();
            ScriptEngine engine = manager.getEngineByName("javascript");
            
            if (engine == null) {
                System.out.println("JavaScript engine not available");
                return;
            }
            
            // Create a simple JavaScript file
            String scriptContent = """
                function calculateArea(radius) {
                    return Math.PI * radius * radius;
                }
                
                function calculateCircumference(radius) {
                    return 2 * Math.PI * radius;
                }
                
                var radius = 5;
                print('Radius: ' + radius);
                print('Area: ' + calculateArea(radius));
                print('Circumference: ' + calculateCircumference(radius));
                """;
            
            // Execute script from string
            engine.eval(scriptContent);
            
        } catch (ScriptException e) {
            System.err.println("Script execution error: " + e.getMessage());
        }
    }
    
    public static void demonstrateErrorHandling() {
        try {
            ScriptEngineManager manager = new ScriptEngineManager();
            ScriptEngine engine = manager.getEngineByName("javascript");
            
            if (engine == null) {
                System.out.println("JavaScript engine not available");
                return;
            }
            
            // Execute script with error
            try {
                engine.eval("undefinedFunction();");
            } catch (ScriptException e) {
                System.out.println("Caught script error: " + e.getMessage());
                System.out.println("Line number: " + e.getLineNumber());
                System.out.println("Column number: " + e.getColumnNumber());
            }
            
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
```

### آنالوژی دنیای واقعی:
Scripting Engine Support مانند داشتن مترجم در یک کنفرانس بین‌المللی است. شما می‌توانید با افراد مختلف که زبان‌های مختلف صحبت می‌کنند ارتباط برقرار کنید، و مترجم (scripting engine) پیام‌ها را ترجمه می‌کند.

## 4.2 JDBC 4.0 Improvements

JDBC 4.0 بهبودهای قابل توجهی در زمینه اتصال به پایگاه داده و مدیریت منابع ارائه داد.

### ویژگی‌های کلیدی:

**1. Auto-loading Driver:**
- Automatic driver discovery
- No need for Class.forName()
- Service provider mechanism

**2. Enhanced Exception Handling:**
- SQLException chaining
- Better error information
- Categorized exceptions

**3. New Data Types:**
- SQLXML support
- RowId support
- NCHAR, NVARCHAR, NCLOB

### مثال عملی:

```java
import java.sql.*;
import java.util.Properties;

public class JDBC4Example {
    private static final String URL = "jdbc:h2:mem:testdb";
    private static final String USER = "sa";
    private static final String PASSWORD = "";
    
    public static void main(String[] args) {
        System.out.println("=== JDBC 4.0 Improvements ===");
        
        try {
            // 1. Auto-loading driver (JDBC 4.0 feature)
            demonstrateAutoLoadingDriver();
            
            // 2. Enhanced exception handling
            demonstrateEnhancedExceptionHandling();
            
            // 3. New data types
            demonstrateNewDataTypes();
            
            // 4. Connection management
            demonstrateConnectionManagement();
            
        } catch (SQLException e) {
            System.err.println("Database error: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    public static void demonstrateAutoLoadingDriver() throws SQLException {
        System.out.println("\n=== Auto-loading Driver ===");
        
        // JDBC 4.0: No need for Class.forName()
        // Driver is automatically loaded
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD)) {
            System.out.println("Connection established successfully");
            
            // Get database metadata
            DatabaseMetaData metaData = conn.getMetaData();
            System.out.println("Database: " + metaData.getDatabaseProductName());
            System.out.println("Version: " + metaData.getDatabaseProductVersion());
            System.out.println("Driver: " + metaData.getDriverName());
            System.out.println("Driver Version: " + metaData.getDriverVersion());
            
        } catch (SQLException e) {
            System.err.println("Connection failed: " + e.getMessage());
            throw e;
        }
    }
    
    public static void demonstrateEnhancedExceptionHandling() throws SQLException {
        System.out.println("\n=== Enhanced Exception Handling ===");
        
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD)) {
            // Create test table
            try (Statement stmt = conn.createStatement()) {
                stmt.execute("CREATE TABLE test_table (id INT PRIMARY KEY, name VARCHAR(50))");
                System.out.println("Table created successfully");
            }
            
            // Insert data
            try (PreparedStatement pstmt = conn.prepareStatement(
                    "INSERT INTO test_table (id, name) VALUES (?, ?)")) {
                pstmt.setInt(1, 1);
                pstmt.setString(2, "احمد");
                pstmt.executeUpdate();
                System.out.println("Data inserted successfully");
            }
            
            // Query data
            try (PreparedStatement pstmt = conn.prepareStatement(
                    "SELECT * FROM test_table WHERE id = ?")) {
                pstmt.setInt(1, 1);
                try (ResultSet rs = pstmt.executeQuery()) {
                    while (rs.next()) {
                        System.out.println("ID: " + rs.getInt("id"));
                        System.out.println("Name: " + rs.getString("name"));
                    }
                }
            }
            
        } catch (SQLException e) {
            // Enhanced exception information
            System.err.println("SQL State: " + e.getSQLState());
            System.err.println("Error Code: " + e.getErrorCode());
            System.err.println("Message: " + e.getMessage());
            
            // Exception chaining
            Throwable cause = e.getCause();
            if (cause != null) {
                System.err.println("Cause: " + cause.getMessage());
            }
            
            throw e;
        }
    }
    
    public static void demonstrateNewDataTypes() throws SQLException {
        System.out.println("\n=== New Data Types ===");
        
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD)) {
            // Create table with new data types
            try (Statement stmt = conn.createStatement()) {
                stmt.execute("""
                    CREATE TABLE new_types_table (
                        id INT PRIMARY KEY,
                        xml_data XML,
                        row_id ROWID
                    )
                    """);
                System.out.println("Table with new data types created");
            }
            
            // Insert data with new types
            try (PreparedStatement pstmt = conn.prepareStatement(
                    "INSERT INTO new_types_table (id, xml_data) VALUES (?, ?)")) {
                pstmt.setInt(1, 1);
                pstmt.setString(2, "<person><name>احمد</name><age>25</age></person>");
                pstmt.executeUpdate();
                System.out.println("Data with new types inserted");
            }
            
        } catch (SQLException e) {
            System.err.println("New data types error: " + e.getMessage());
        }
    }
    
    public static void demonstrateConnectionManagement() throws SQLException {
        System.out.println("\n=== Connection Management ===");
        
        // JDBC 4.0: Better connection management
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD)) {
            // Check if connection is valid
            if (conn.isValid(5)) {
                System.out.println("Connection is valid");
            } else {
                System.out.println("Connection is not valid");
            }
            
            // Get connection properties
            Properties props = conn.getClientInfo();
            System.out.println("Connection properties: " + props);
            
            // Set client info
            conn.setClientInfo("ApplicationName", "JDBC4Example");
            conn.setClientInfo("ClientUser", "احمد محمدی");
            
            // Get updated client info
            props = conn.getClientInfo();
            System.out.println("Updated connection properties: " + props);
            
        } catch (SQLClientInfoException e) {
            System.err.println("Client info error: " + e.getMessage());
        }
    }
}
```

### آنالوژی دنیای واقعی:
JDBC 4.0 مانند بهبود سیستم تلفن است. قبلاً باید شماره تلفن را دستی شماره‌گیری می‌کردید (Class.forName)، اما حالا فقط شماره را می‌گیرید و سیستم خودکار اتصال برقرار می‌کند. همچنین خطاها بهتر گزارش می‌شوند و می‌توانید اطلاعات بیشتری از مشکل دریافت کنید.

## 4.3 Java Compiler API

Java Compiler API امکان کامپایل کردن کد Java در runtime را فراهم می‌کند.

### مفاهیم کلیدی:

**1. Compiler Interface:**
- `javax.tools.JavaCompiler`
- `javax.tools.ToolProvider`
- Compilation units

**2. Features:**
- Runtime compilation
- Dynamic code generation
- Error reporting

### مثال عملی:

```java
import javax.tools.*;
import java.io.*;
import java.util.*;

public class JavaCompilerAPIExample {
    public static void main(String[] args) {
        System.out.println("=== Java Compiler API ===");
        
        // 1. Basic compilation
        demonstrateBasicCompilation();
        
        // 2. Compilation with errors
        demonstrateCompilationErrors();
        
        // 3. Dynamic class generation
        demonstrateDynamicClassGeneration();
        
        // 4. Compilation with custom options
        demonstrateCustomCompilation();
    }
    
    public static void demonstrateBasicCompilation() {
        System.out.println("\n=== Basic Compilation ===");
        
        // Get system Java compiler
        JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
        if (compiler == null) {
            System.out.println("No Java compiler available");
            return;
        }
        
        // Create compilation task
        String sourceCode = """
            public class HelloWorld {
                public static void main(String[] args) {
                    System.out.println("Hello from compiled code!");
                }
            }
            """;
        
        // Compile the code
        JavaFileObject fileObject = new StringJavaFileObject("HelloWorld", sourceCode);
        Iterable<? extends JavaFileObject> compilationUnits = Arrays.asList(fileObject);
        
        JavaCompiler.CompilationTask task = compiler.getTask(
            null, null, null, null, null, compilationUnits);
        
        boolean success = task.call();
        System.out.println("Compilation " + (success ? "successful" : "failed"));
    }
    
    public static void demonstrateCompilationErrors() {
        System.out.println("\n=== Compilation with Errors ===");
        
        JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
        if (compiler == null) {
            System.out.println("No Java compiler available");
            return;
        }
        
        // Create compilation task with error
        String sourceCodeWithError = """
            public class ErrorClass {
                public static void main(String[] args) {
                    System.out.println("This will cause an error: " + undefinedVariable);
                }
            }
            """;
        
        // Custom diagnostic listener
        DiagnosticCollector<JavaFileObject> diagnostics = new DiagnosticCollector<>();
        
        JavaFileObject fileObject = new StringJavaFileObject("ErrorClass", sourceCodeWithError);
        Iterable<? extends JavaFileObject> compilationUnits = Arrays.asList(fileObject);
        
        JavaCompiler.CompilationTask task = compiler.getTask(
            null, null, diagnostics, null, null, compilationUnits);
        
        boolean success = task.call();
        System.out.println("Compilation " + (success ? "successful" : "failed"));
        
        // Print diagnostics
        for (Diagnostic<? extends JavaFileObject> diagnostic : diagnostics.getDiagnostics()) {
            System.out.println("Error: " + diagnostic.getMessage(null));
            System.out.println("Line: " + diagnostic.getLineNumber());
            System.out.println("Column: " + diagnostic.getColumnNumber());
        }
    }
    
    public static void demonstrateDynamicClassGeneration() {
        System.out.println("\n=== Dynamic Class Generation ===");
        
        JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
        if (compiler == null) {
            System.out.println("No Java compiler available");
            return;
        }
        
        // Generate dynamic class
        String className = "DynamicCalculator";
        String sourceCode = """
            public class """ + className + """ {
                public int add(int a, int b) {
                    return a + b;
                }
                
                public int multiply(int a, int b) {
                    return a * b;
                }
                
                public static void main(String[] args) {
                    """ + className + """ calc = new """ + className + """();
                    System.out.println("Addition: " + calc.add(5, 3));
                    System.out.println("Multiplication: " + calc.multiply(5, 3));
                }
            }
            """;
        
        // Compile dynamic class
        JavaFileObject fileObject = new StringJavaFileObject(className, sourceCode);
        Iterable<? extends JavaFileObject> compilationUnits = Arrays.asList(fileObject);
        
        JavaCompiler.CompilationTask task = compiler.getTask(
            null, null, null, null, null, compilationUnits);
        
        boolean success = task.call();
        System.out.println("Dynamic class compilation " + (success ? "successful" : "failed"));
    }
    
    public static void demonstrateCustomCompilation() {
        System.out.println("\n=== Custom Compilation Options ===");
        
        JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
        if (compiler == null) {
            System.out.println("No Java compiler available");
            return;
        }
        
        // Custom compilation options
        List<String> options = Arrays.asList("-verbose", "-deprecation");
        
        String sourceCode = """
            public class CustomOptions {
                @Deprecated
                public void oldMethod() {
                    System.out.println("This method is deprecated");
                }
                
                public static void main(String[] args) {
                    CustomOptions obj = new CustomOptions();
                    obj.oldMethod();
                }
            }
            """;
        
        // Compile with custom options
        JavaFileObject fileObject = new StringJavaFileObject("CustomOptions", sourceCode);
        Iterable<? extends JavaFileObject> compilationUnits = Arrays.asList(fileObject);
        
        JavaCompiler.CompilationTask task = compiler.getTask(
            null, null, null, options, null, compilationUnits);
        
        boolean success = task.call();
        System.out.println("Custom compilation " + (success ? "successful" : "failed"));
    }
    
    // Helper class for in-memory Java file objects
    static class StringJavaFileObject extends SimpleJavaFileObject {
        private final String code;
        
        protected StringJavaFileObject(String className, String code) {
            super(URI.create("string:///" + className.replace('.', '/') + Kind.SOURCE.extension), Kind.SOURCE);
            this.code = code;
        }
        
        @Override
        public CharSequence getCharContent(boolean ignoreEncodingErrors) {
            return code;
        }
    }
}
```

### آنالوژی دنیای واقعی:
Java Compiler API مانند داشتن یک کارخانه کوچک در خانه است. شما می‌توانید مواد اولیه (کد Java) را بدهید و کارخانه آن را به محصول نهایی (کلاس کامپایل شده) تبدیل کند. این کارخانه می‌تواند خطاها را تشخیص دهد و گزارش دهد.

## 4.4 Pluggable Annotation Processing

Pluggable Annotation Processing امکان پردازش annotations در compile time را فراهم می‌کند.

### مفاهیم کلیدی:

**1. Annotation Processor:**
- `javax.annotation.processing.Processor`
- `javax.annotation.processing.AbstractProcessor`
- Compile-time processing

**2. Features:**
- Code generation
- Validation
- Documentation generation

### مثال عملی:

```java
import javax.annotation.processing.*;
import javax.lang.model.SourceVersion;
import javax.lang.model.element.*;
import javax.lang.model.type.TypeMirror;
import javax.tools.Diagnostic;
import java.util.*;

// Custom annotation
@Retention(RetentionPolicy.SOURCE)
@Target(ElementType.TYPE)
@interface GenerateBuilder {
    String value() default "";
}

// Annotation processor
@SupportedAnnotationTypes("GenerateBuilder")
@SupportedSourceVersion(SourceVersion.RELEASE_6)
public class BuilderAnnotationProcessor extends AbstractProcessor {
    
    @Override
    public boolean process(Set<? extends TypeElement> annotations, RoundEnvironment roundEnv) {
        System.out.println("=== Pluggable Annotation Processing ===");
        
        for (TypeElement annotation : annotations) {
            Set<? extends Element> elements = roundEnv.getElementsAnnotatedWith(annotation);
            
            for (Element element : elements) {
                if (element.getKind() == ElementKind.CLASS) {
                    processClass((TypeElement) element);
                }
            }
        }
        
        return true;
    }
    
    private void processClass(TypeElement classElement) {
        String className = classElement.getSimpleName().toString();
        String packageName = processingEnv.getElementUtils().getPackageOf(classElement).getQualifiedName().toString();
        
        System.out.println("Processing class: " + className);
        System.out.println("Package: " + packageName);
        
        // Generate builder class
        generateBuilderClass(classElement, packageName, className);
        
        // Validate class
        validateClass(classElement);
    }
    
    private void generateBuilderClass(TypeElement classElement, String packageName, String className) {
        StringBuilder builderCode = new StringBuilder();
        
        // Package declaration
        if (!packageName.isEmpty()) {
            builderCode.append("package ").append(packageName).append(";\n\n");
        }
        
        // Builder class
        builderCode.append("public class ").append(className).append("Builder {\n");
        
        // Fields
        for (Element member : classElement.getEnclosedElements()) {
            if (member.getKind() == ElementKind.FIELD) {
                VariableElement field = (VariableElement) member;
                String fieldName = field.getSimpleName().toString();
                String fieldType = field.asType().toString();
                
                builderCode.append("    private ").append(fieldType).append(" ").append(fieldName).append(";\n");
            }
        }
        
        // Setter methods
        for (Element member : classElement.getEnclosedElements()) {
            if (member.getKind() == ElementKind.FIELD) {
                VariableElement field = (VariableElement) member;
                String fieldName = field.getSimpleName().toString();
                String fieldType = field.asType().toString();
                String methodName = "set" + Character.toUpperCase(fieldName.charAt(0)) + fieldName.substring(1);
                
                builderCode.append("\n    public ").append(className).append("Builder ").append(methodName).append("(").append(fieldType).append(" ").append(fieldName).append(") {\n");
                builderCode.append("        this.").append(fieldName).append(" = ").append(fieldName).append(";\n");
                builderCode.append("        return this;\n");
                builderCode.append("    }\n");
            }
        }
        
        // Build method
        builderCode.append("\n    public ").append(className).append(" build() {\n");
        builderCode.append("        return new ").append(className).append("(");
        
        // Constructor parameters
        List<String> fieldNames = new ArrayList<>();
        for (Element member : classElement.getEnclosedElements()) {
            if (member.getKind() == ElementKind.FIELD) {
                VariableElement field = (VariableElement) member;
                fieldNames.add(field.getSimpleName().toString());
            }
        }
        
        builderCode.append(String.join(", ", fieldNames));
        builderCode.append(");\n");
        builderCode.append("    }\n");
        builderCode.append("}\n");
        
        System.out.println("Generated builder class:");
        System.out.println(builderCode.toString());
    }
    
    private void validateClass(TypeElement classElement) {
        System.out.println("\n=== Class Validation ===");
        
        // Check if class has constructor
        boolean hasConstructor = false;
        for (Element member : classElement.getEnclosedElements()) {
            if (member.getKind() == ElementKind.CONSTRUCTOR) {
                hasConstructor = true;
                break;
            }
        }
        
        if (!hasConstructor) {
            processingEnv.getMessager().printMessage(
                Diagnostic.Kind.WARNING,
                "Class " + classElement.getSimpleName() + " should have a constructor",
                classElement
            );
        }
        
        // Check field accessibility
        for (Element member : classElement.getEnclosedElements()) {
            if (member.getKind() == ElementKind.FIELD) {
                VariableElement field = (VariableElement) member;
                Set<Modifier> modifiers = field.getModifiers();
                
                if (modifiers.contains(Modifier.PRIVATE)) {
                    processingEnv.getMessager().printMessage(
                        Diagnostic.Kind.INFO,
                        "Field " + field.getSimpleName() + " is private",
                        field
                    );
                }
            }
        }
    }
}

// Example class using the annotation
@GenerateBuilder
class Person {
    private String name;
    private int age;
    private String email;
    
    public Person(String name, int age, String email) {
        this.name = name;
        this.age = age;
        this.email = email;
    }
    
    // Getters and setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
```

### آنالوژی دنیای واقعی:
Pluggable Annotation Processing مانند داشتن یک سیستم بازرسی خودکار در کارخانه است. قبل از اینکه محصول نهایی (کلاس کامپایل شده) آماده شود، سیستم بازرسی (annotation processor) آن را بررسی می‌کند، اعتبارسنجی می‌کند و در صورت نیاز، قطعات اضافی (کد تولید شده) را اضافه می‌کند.

## 4.5 JVM Performance Improvements

Java 6 بهبودهای قابل توجهی در عملکرد JVM ارائه داد.

### ویژگی‌های کلیدی:

**1. Garbage Collection:**
- Parallel GC improvements
- Better memory management
- Reduced pause times

**2. JIT Compilation:**
- Enhanced HotSpot optimizations
- Better code generation
- Improved startup time

**3. Memory Management:**
- Better heap management
- Reduced memory footprint
- Improved allocation

### مثال عملی:

```java
import java.util.*;
import java.lang.management.*;

public class JVMPerformanceExample {
    public static void main(String[] args) {
        System.out.println("=== JVM Performance Improvements ===");
        
        // 1. Memory management
        demonstrateMemoryManagement();
        
        // 2. Garbage collection
        demonstrateGarbageCollection();
        
        // 3. JIT compilation
        demonstrateJITCompilation();
        
        // 4. Performance monitoring
        demonstratePerformanceMonitoring();
    }
    
    public static void demonstrateMemoryManagement() {
        System.out.println("\n=== Memory Management ===");
        
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        MemoryUsage heapUsage = memoryBean.getHeapMemoryUsage();
        
        System.out.println("Heap Memory Usage:");
        System.out.println("  Initial: " + formatBytes(heapUsage.getInit()));
        System.out.println("  Used: " + formatBytes(heapUsage.getUsed()));
        System.out.println("  Committed: " + formatBytes(heapUsage.getCommitted()));
        System.out.println("  Max: " + formatBytes(heapUsage.getMax()));
        
        // Create objects to test memory management
        List<String> list = new ArrayList<>();
        for (int i = 0; i < 100000; i++) {
            list.add("String " + i);
        }
        
        System.out.println("Created 100,000 strings");
        
        // Clear list to make objects eligible for GC
        list.clear();
        list = null;
        
        // Force garbage collection
        System.gc();
        
        // Check memory after GC
        heapUsage = memoryBean.getHeapMemoryUsage();
        System.out.println("Memory after GC: " + formatBytes(heapUsage.getUsed()));
    }
    
    public static void demonstrateGarbageCollection() {
        System.out.println("\n=== Garbage Collection ===");
        
        List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
        
        System.out.println("Garbage Collectors:");
        for (GarbageCollectorMXBean gcBean : gcBeans) {
            System.out.println("  Name: " + gcBean.getName());
            System.out.println("  Collections: " + gcBean.getCollectionCount());
            System.out.println("  Time: " + gcBean.getCollectionTime() + " ms");
        }
        
        // Create objects to trigger GC
        for (int i = 0; i < 10; i++) {
            List<String> tempList = new ArrayList<>();
            for (int j = 0; j < 10000; j++) {
                tempList.add("Temp string " + j);
            }
            // tempList goes out of scope, eligible for GC
        }
        
        // Force GC
        System.gc();
        
        System.out.println("After forced GC:");
        for (GarbageCollectorMXBean gcBean : gcBeans) {
            System.out.println("  " + gcBean.getName() + " collections: " + gcBean.getCollectionCount());
        }
    }
    
    public static void demonstrateJITCompilation() {
        System.out.println("\n=== JIT Compilation ===");
        
        CompilationMXBean compilationBean = ManagementFactory.getCompilationMXBean();
        
        if (compilationBean.isCompilationTimeSupported()) {
            System.out.println("JIT Compiler: " + compilationBean.getName());
            System.out.println("Compilation time: " + compilationBean.getTotalCompilationTime() + " ms");
        }
        
        // Method that will be JIT compiled
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < 1000000; i++) {
            performCalculation(i);
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Calculation time: " + (endTime - startTime) + " ms");
        
        // Second run (should be faster due to JIT)
        startTime = System.currentTimeMillis();
        
        for (int i = 0; i < 1000000; i++) {
            performCalculation(i);
        }
        
        endTime = System.currentTimeMillis();
        System.out.println("Second run time: " + (endTime - startTime) + " ms");
    }
    
    public static void demonstratePerformanceMonitoring() {
        System.out.println("\n=== Performance Monitoring ===");
        
        RuntimeMXBean runtimeBean = ManagementFactory.getRuntimeMXBean();
        
        System.out.println("Runtime Information:");
        System.out.println("  JVM Name: " + runtimeBean.getVmName());
        System.out.println("  JVM Version: " + runtimeBean.getVmVersion());
        System.out.println("  JVM Vendor: " + runtimeBean.getVmVendor());
        System.out.println("  Uptime: " + runtimeBean.getUptime() + " ms");
        System.out.println("  Available Processors: " + runtimeBean.getAvailableProcessors());
        
        // Thread information
        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        
        System.out.println("\nThread Information:");
        System.out.println("  Thread Count: " + threadBean.getThreadCount());
        System.out.println("  Peak Thread Count: " + threadBean.getPeakThreadCount());
        System.out.println("  Total Started Threads: " + threadBean.getTotalStartedThreadCount());
        
        // Class loading information
        ClassLoadingMXBean classBean = ManagementFactory.getClassLoadingMXBean();
        
        System.out.println("\nClass Loading Information:");
        System.out.println("  Loaded Classes: " + classBean.getLoadedClassCount());
        System.out.println("  Total Loaded Classes: " + classBean.getTotalLoadedClassCount());
        System.out.println("  Unloaded Classes: " + classBean.getUnloadedClassCount());
    }
    
    private static int performCalculation(int value) {
        // Simple calculation that can be optimized by JIT
        return value * value + value * 2 + 1;
    }
    
    private static String formatBytes(long bytes) {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return String.format("%.2f KB", bytes / 1024.0);
        if (bytes < 1024 * 1024 * 1024) return String.format("%.2f MB", bytes / (1024.0 * 1024.0));
        return String.format("%.2f GB", bytes / (1024.0 * 1024.0 * 1024.0));
    }
}
```

### آنالوژی دنیای واقعی:
JVM Performance Improvements مانند بهبود موتور خودرو است. موتور جدیدتر (Java 6) همان سوخت (کد Java) را مصرف می‌کند اما با کارایی بیشتر، مصرف کمتر و آلودگی کمتر. همچنین سیستم تعمیر و نگهداری (Garbage Collection) بهتر کار می‌کند.

## 4.6 Web Services Support

Java 6 پشتیبانی بهتری از Web Services ارائه داد.

### ویژگی‌های کلیدی:

**1. JAX-WS:**
- Java API for XML Web Services
- SOAP web services
- WSDL support

**2. JAXB:**
- Java Architecture for XML Binding
- XML to Java mapping
- Schema generation

**3. JAXP:**
- Java API for XML Processing
- DOM, SAX, StAX support
- XSLT processing

### مثال عملی:

```java
import javax.xml.bind.*;
import javax.xml.bind.annotation.*;
import javax.xml.parsers.*;
import javax.xml.transform.*;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.*;

// JAXB annotated class
@XmlRootElement
@XmlAccessorType(XmlAccessType.FIELD)
class Person {
    @XmlElement
    private String name;
    
    @XmlElement
    private int age;
    
    @XmlElement
    private String email;
    
    public Person() {}
    
    public Person(String name, int age, String email) {
        this.name = name;
        this.age = age;
        this.email = email;
    }
    
    // Getters and setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + ", email='" + email + "'}";
    }
}

public class WebServicesSupportExample {
    public static void main(String[] args) {
        System.out.println("=== Web Services Support ===");
        
        // 1. JAXB XML Binding
        demonstrateJAXB();
        
        // 2. XML Processing
        demonstrateXMLProcessing();
        
        // 3. XSLT Transformation
        demonstrateXSLT();
    }
    
    public static void demonstrateJAXB() {
        System.out.println("\n=== JAXB XML Binding ===");
        
        try {
            // Create JAXB context
            JAXBContext context = JAXBContext.newInstance(Person.class);
            
            // Create person object
            Person person = new Person("احمد محمدی", 25, "ahmad@example.com");
            
            // Marshal to XML
            Marshaller marshaller = context.createMarshaller();
            marshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);
            
            StringWriter writer = new StringWriter();
            marshaller.marshal(person, writer);
            
            System.out.println("Marshalled XML:");
            System.out.println(writer.toString());
            
            // Unmarshal from XML
            StringReader reader = new StringReader(writer.toString());
            Unmarshaller unmarshaller = context.createUnmarshaller();
            Person unmarshalledPerson = (Person) unmarshaller.unmarshal(reader);
            
            System.out.println("\nUnmarshalled Person: " + unmarshalledPerson);
            
        } catch (JAXBException e) {
            System.err.println("JAXB error: " + e.getMessage());
        }
    }
    
    public static void demonstrateXMLProcessing() {
        System.out.println("\n=== XML Processing ===");
        
        try {
            // Create XML document
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document document = builder.newDocument();
            
            // Create root element
            Element root = document.createElement("employees");
            document.appendChild(root);
            
            // Create employee elements
            String[] names = {"احمد", "فاطمه", "علی"};
            int[] ages = {25, 30, 28};
            
            for (int i = 0; i < names.length; i++) {
                Element employee = document.createElement("employee");
                employee.setAttribute("id", String.valueOf(i + 1));
                
                Element name = document.createElement("name");
                name.setTextContent(names[i]);
                employee.appendChild(name);
                
                Element age = document.createElement("age");
                age.setTextContent(String.valueOf(ages[i]));
                employee.appendChild(age);
                
                root.appendChild(employee);
            }
            
            // Transform to string
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            
            StringWriter writer = new StringWriter();
            transformer.transform(new DOMSource(document), new StreamResult(writer));
            
            System.out.println("Generated XML:");
            System.out.println(writer.toString());
            
        } catch (Exception e) {
            System.err.println("XML processing error: " + e.getMessage());
        }
    }
    
    public static void demonstrateXSLT() {
        System.out.println("\n=== XSLT Transformation ===");
        
        try {
            // Create XML document
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document document = builder.newDocument();
            
            // Create simple XML
            Element root = document.createElement("data");
            document.appendChild(root);
            
            Element item1 = document.createElement("item");
            item1.setTextContent("آیتم 1");
            root.appendChild(item1);
            
            Element item2 = document.createElement("item");
            item2.setTextContent("آیتم 2");
            root.appendChild(item2);
            
            // Create XSLT stylesheet
            String xslt = """
                <?xml version="1.0" encoding="UTF-8"?>
                <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                    <xsl:template match="/">
                        <html>
                            <body>
                                <h2>Transformed Data</h2>
                                <ul>
                                    <xsl:for-each select="data/item">
                                        <li><xsl:value-of select="."/></li>
                                    </xsl:for-each>
                                </ul>
                            </body>
                        </html>
                    </xsl:template>
                </xsl:stylesheet>
                """;
            
            // Apply XSLT transformation
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer(
                new StreamSource(new StringReader(xslt)));
            
            StringWriter writer = new StringWriter();
            transformer.transform(new DOMSource(document), new StreamResult(writer));
            
            System.out.println("XSLT Transformation Result:");
            System.out.println(writer.toString());
            
        } catch (Exception e) {
            System.err.println("XSLT error: " + e.getMessage());
        }
    }
}
```

### آنالوژی دنیای واقعی:
Web Services Support مانند داشتن یک سیستم پست پیشرفته است. JAXB مانند داشتن ماشین ترجمه است که نامه‌ها را از زبان XML به زبان Java ترجمه می‌کند. XML Processing مانند داشتن ماشین‌های مختلف برای خواندن، نوشتن و پردازش نامه‌ها است. XSLT مانند داشتن قالب‌های مختلف برای فرمت‌بندی نامه‌ها است.