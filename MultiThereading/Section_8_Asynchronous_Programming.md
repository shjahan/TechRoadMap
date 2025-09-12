# Section 8 - Asynchronous Programming

## 8.1 Asynchronous Programming Concepts

Asynchronous programming allows tasks to run independently without blocking the main thread. It's essential for building responsive applications that can handle multiple operations concurrently.

### Key Concepts:

**1. Non-Blocking Execution:**
- Tasks don't block the calling thread
- Main thread remains responsive
- Better resource utilization

**2. Callback-Based:**
- Functions called when operations complete
- Event-driven programming model
- Handles results and errors

**3. Future/Promise Pattern:**
- Represent values that will be available later
- Can be checked for completion
- Support chaining and composition

### Java Example - Basic Asynchronous Programming:

```java
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class AsynchronousProgrammingExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    
    public void demonstrateAsyncConcepts() throws Exception {
        // Method 1: CompletableFuture
        demonstrateCompletableFuture();
        
        // Method 2: Callback-based
        demonstrateCallbacks();
        
        // Method 3: Chaining operations
        demonstrateChaining();
        
        executor.shutdown();
    }
    
    private void demonstrateCompletableFuture() throws Exception {
        System.out.println("=== CompletableFuture ===");
        
        CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "Hello from async task";
        }, executor);
        
        // Non-blocking: do other work
        System.out.println("Doing other work...");
        
        // Get result when ready
        String result = future.get();
        System.out.println("Result: " + result);
    }
    
    private void demonstrateCallbacks() {
        System.out.println("\n=== Callbacks ===");
        
        CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "Callback result";
        }, executor)
        .thenAccept(result -> System.out.println("Callback received: " + result))
        .exceptionally(throwable -> {
            System.out.println("Error: " + throwable.getMessage());
            return null;
        });
    }
    
    private void demonstrateChaining() throws Exception {
        System.out.println("\n=== Chaining ===");
        
        CompletableFuture<String> future = CompletableFuture
            .supplyAsync(() -> "Hello", executor)
            .thenApply(s -> s + " World")
            .thenApply(s -> s + "!")
            .thenCompose(s -> CompletableFuture.supplyAsync(() -> s + " Async", executor));
        
        System.out.println("Chained result: " + future.get());
    }
    
    public static void main(String[] args) throws Exception {
        AsynchronousProgrammingExample example = new AsynchronousProgrammingExample();
        example.demonstrateAsyncConcepts();
    }
}
```

## 8.2 Callbacks

Callbacks are functions that are passed as arguments to other functions and are executed when a specific event occurs or an operation completes.

### Key Concepts:

**1. Event-Driven:**
- Functions called in response to events
- Decouples event source from handler
- Asynchronous execution model

**2. Error Handling:**
- Separate callbacks for success and error
- Proper exception propagation
- Graceful error recovery

**3. Composition:**
- Multiple callbacks can be chained
- Complex workflows from simple callbacks
- Reusable callback patterns

### Java Example - Callback Implementation:

```java
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class CallbackExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    
    public void demonstrateCallbacks() {
        // Success callback
        performAsyncOperation("Success Task")
            .thenAccept(this::onSuccess)
            .exceptionally(this::onError);
        
        // Error callback
        performAsyncOperation("Error Task")
            .thenAccept(this::onSuccess)
            .exceptionally(this::onError);
        
        // Chained callbacks
        performAsyncOperation("Chained Task")
            .thenApply(this::processResult)
            .thenAccept(this::onSuccess)
            .exceptionally(this::onError);
    }
    
    private CompletableFuture<String> performAsyncOperation(String taskName) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
                if (taskName.contains("Error")) {
                    throw new RuntimeException("Simulated error");
                }
                return "Result from " + taskName;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException(e);
            }
        }, executor);
    }
    
    private void onSuccess(String result) {
        System.out.println("Success callback: " + result);
    }
    
    private Void onError(Throwable throwable) {
        System.out.println("Error callback: " + throwable.getMessage());
        return null;
    }
    
    private String processResult(String result) {
        return result + " (processed)";
    }
    
    public static void main(String[] args) throws InterruptedException {
        CallbackExample example = new CallbackExample();
        example.demonstrateCallbacks();
        
        Thread.sleep(3000);
    }
}
```

## 8.3 Promises and Futures

Promises and Futures represent values that will be available in the future. They provide a way to work with asynchronous operations in a more structured manner.

### Key Concepts:

**1. Future Interface:**
- Represents a result of an asynchronous computation
- Can be checked for completion
- Supports cancellation

**2. CompletableFuture:**
- Enhanced Future with completion callbacks
- Supports chaining and composition
- Better error handling

**3. Promise Pattern:**
- Producer-consumer pattern for async values
- Can be resolved or rejected
- Supports multiple listeners

### Java Example - Promises and Futures:

```java
import java.util.concurrent.*;
import java.util.function.Supplier;

public class PromiseFutureExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    
    public void demonstratePromisesAndFutures() throws Exception {
        // Basic Future
        demonstrateBasicFuture();
        
        // CompletableFuture
        demonstrateCompletableFuture();
        
        // Promise-like behavior
        demonstratePromise();
    }
    
    private void demonstrateBasicFuture() throws Exception {
        System.out.println("=== Basic Future ===");
        
        Future<String> future = executor.submit(() -> {
            Thread.sleep(1000);
            return "Future result";
        });
        
        // Check if completed
        while (!future.isDone()) {
            System.out.println("Waiting for future to complete...");
            Thread.sleep(100);
        }
        
        System.out.println("Future result: " + future.get());
    }
    
    private void demonstrateCompletableFuture() throws Exception {
        System.out.println("\n=== CompletableFuture ===");
        
        CompletableFuture<String> future = CompletableFuture
            .supplyAsync(() -> {
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                return "CompletableFuture result";
            }, executor);
        
        // Non-blocking completion
        future.thenAccept(result -> 
            System.out.println("CompletableFuture result: " + result));
        
        // Wait for completion
        future.get();
    }
    
    private void demonstratePromise() throws Exception {
        System.out.println("\n=== Promise-like Behavior ===");
        
        CompletableFuture<String> promise = new CompletableFuture<>();
        
        // Simulate async operation
        executor.submit(() -> {
            try {
                Thread.sleep(1000);
                promise.complete("Promise resolved");
            } catch (InterruptedException e) {
                promise.completeExceptionally(e);
            }
        });
        
        // Multiple listeners
        promise.thenAccept(result -> 
            System.out.println("Listener 1: " + result));
        promise.thenAccept(result -> 
            System.out.println("Listener 2: " + result));
        
        // Wait for resolution
        promise.get();
    }
    
    public static void main(String[] args) throws Exception {
        PromiseFutureExample example = new PromiseFutureExample();
        example.demonstratePromisesAndFutures();
    }
}
```

## 8.4 Async/Await Patterns

Async/await patterns provide a more synchronous-looking syntax for asynchronous operations. While Java doesn't have native async/await, we can simulate it using CompletableFuture.

### Key Concepts:

**1. Async Functions:**
- Functions that return CompletableFuture
- Can be awaited for results
- Handle exceptions properly

**2. Await Pattern:**
- Wait for async operations to complete
- Blocking until result is available
- Exception propagation

**3. Sequential vs Parallel:**
- Sequential: await each operation
- Parallel: start all operations, then await

### Java Example - Async/Await Simulation:

```java
import java.util.concurrent.*;
import java.util.List;
import java.util.ArrayList;

public class AsyncAwaitExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    
    public void demonstrateAsyncAwait() throws Exception {
        // Sequential async/await
        demonstrateSequential();
        
        // Parallel async/await
        demonstrateParallel();
        
        // Error handling
        demonstrateErrorHandling();
    }
    
    private void demonstrateSequential() throws Exception {
        System.out.println("=== Sequential Async/Await ===");
        
        String result1 = await(asyncOperation("Task 1", 1000));
        String result2 = await(asyncOperation("Task 2", 1000));
        String result3 = await(asyncOperation("Task 3", 1000));
        
        System.out.println("Sequential results: " + result1 + ", " + result2 + ", " + result3);
    }
    
    private void demonstrateParallel() throws Exception {
        System.out.println("\n=== Parallel Async/Await ===");
        
        CompletableFuture<String> future1 = asyncOperation("Parallel Task 1", 1000);
        CompletableFuture<String> future2 = asyncOperation("Parallel Task 2", 1000);
        CompletableFuture<String> future3 = asyncOperation("Parallel Task 3", 1000);
        
        String result1 = await(future1);
        String result2 = await(future2);
        String result3 = await(future3);
        
        System.out.println("Parallel results: " + result1 + ", " + result2 + ", " + result3);
    }
    
    private void demonstrateErrorHandling() throws Exception {
        System.out.println("\n=== Error Handling ===");
        
        try {
            String result = await(asyncOperationWithError("Error Task"));
            System.out.println("Result: " + result);
        } catch (Exception e) {
            System.out.println("Caught error: " + e.getMessage());
        }
    }
    
    private CompletableFuture<String> asyncOperation(String taskName, int delay) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(delay);
                return "Result from " + taskName;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException(e);
            }
        }, executor);
    }
    
    private CompletableFuture<String> asyncOperationWithError(String taskName) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
                throw new RuntimeException("Simulated error in " + taskName);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException(e);
            }
        }, executor);
    }
    
    private <T> T await(CompletableFuture<T> future) throws Exception {
        return future.get();
    }
    
    public static void main(String[] args) throws Exception {
        AsyncAwaitExample example = new AsyncAwaitExample();
        example.demonstrateAsyncAwait();
    }
}
```

## 8.5 CompletableFuture

CompletableFuture is Java's implementation of the Future interface with additional capabilities for asynchronous programming. It provides methods for composing, transforming, and handling asynchronous operations.

### Key Features:

**1. Composition:**
- thenApply(): Transform result
- thenCompose(): Chain async operations
- thenCombine(): Combine multiple futures

**2. Error Handling:**
- exceptionally(): Handle exceptions
- handle(): Handle both success and error
- whenComplete(): Execute regardless of outcome

**3. Coordination:**
- allOf(): Wait for all futures
- anyOf(): Wait for any future
- join(): Block until complete

### Java Example - CompletableFuture Advanced Usage:

```java
import java.util.concurrent.*;
import java.util.function.Function;
import java.util.function.Supplier;

public class CompletableFutureExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    
    public void demonstrateCompletableFuture() throws Exception {
        // Basic operations
        demonstrateBasicOperations();
        
        // Composition
        demonstrateComposition();
        
        // Error handling
        demonstrateErrorHandling();
        
        // Coordination
        demonstrateCoordination();
    }
    
    private void demonstrateBasicOperations() throws Exception {
        System.out.println("=== Basic Operations ===");
        
        // Supply async
        CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "Hello";
        }, executor);
        
        // Transform result
        CompletableFuture<String> transformed = future.thenApply(s -> s + " World");
        
        System.out.println("Result: " + transformed.get());
    }
    
    private void demonstrateComposition() throws Exception {
        System.out.println("\n=== Composition ===");
        
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Hello", executor);
        CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "World", executor);
        
        // Combine results
        CompletableFuture<String> combined = future1.thenCombine(future2, (s1, s2) -> s1 + " " + s2);
        
        // Chain operations
        CompletableFuture<String> chained = combined.thenCompose(s -> 
            CompletableFuture.supplyAsync(() -> s + "!", executor));
        
        System.out.println("Combined result: " + chained.get());
    }
    
    private void demonstrateErrorHandling() throws Exception {
        System.out.println("\n=== Error Handling ===");
        
        CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
            throw new RuntimeException("Simulated error");
        }, executor);
        
        // Handle exception
        CompletableFuture<String> handled = future.handle((result, throwable) -> {
            if (throwable != null) {
                return "Error handled: " + throwable.getMessage();
            }
            return result;
        });
        
        System.out.println("Error handling result: " + handled.get());
    }
    
    private void demonstrateCoordination() throws Exception {
        System.out.println("\n=== Coordination ===");
        
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "Task 1", executor);
        CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "Task 2", executor);
        CompletableFuture<String> future3 = CompletableFuture.supplyAsync(() -> "Task 3", executor);
        
        // Wait for all
        CompletableFuture<Void> allOf = CompletableFuture.allOf(future1, future2, future3);
        allOf.thenRun(() -> System.out.println("All tasks completed"));
        
        // Wait for any
        CompletableFuture<Object> anyOf = CompletableFuture.anyOf(future1, future2, future3);
        System.out.println("First completed: " + anyOf.get());
        
        allOf.get();
    }
    
    public static void main(String[] args) throws Exception {
        CompletableFutureExample example = new CompletableFutureExample();
        example.demonstrateCompletableFuture();
    }
}
```

## 8.6 Reactive Programming

Reactive programming is a programming paradigm that deals with asynchronous data streams and the propagation of change. It's particularly useful for handling real-time data and event-driven systems.

### Key Concepts:

**1. Streams:**
- Continuous flow of data
- Can be transformed and filtered
- Support backpressure

**2. Observers:**
- Subscribe to streams
- React to data changes
- Handle errors and completion

**3. Operators:**
- Transform, filter, and combine streams
- Functional programming approach
- Composable operations

### Java Example - Reactive Programming with CompletableFuture:

```java
import java.util.concurrent.*;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Stream;

public class ReactiveProgrammingExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    
    public void demonstrateReactiveProgramming() throws Exception {
        // Create data stream
        demonstrateDataStream();
        
        // Transform operations
        demonstrateTransformations();
        
        // Error handling
        demonstrateErrorHandling();
    }
    
    private void demonstrateDataStream() throws Exception {
        System.out.println("=== Data Stream ===");
        
        // Create stream of async operations
        Stream<CompletableFuture<String>> stream = Stream.of(
            createAsyncTask("Task 1", 1000),
            createAsyncTask("Task 2", 1500),
            createAsyncTask("Task 3", 800)
        );
        
        // Process stream
        CompletableFuture<Void> allTasks = CompletableFuture.allOf(
            stream.toArray(CompletableFuture[]::new)
        );
        
        allTasks.thenRun(() -> System.out.println("All tasks completed"));
        allTasks.get();
    }
    
    private void demonstrateTransformations() throws Exception {
        System.out.println("\n=== Transformations ===");
        
        CompletableFuture<String> future = createAsyncTask("Transform", 1000);
        
        // Transform result
        CompletableFuture<String> transformed = future
            .thenApply(String::toUpperCase)
            .thenApply(s -> s + " TRANSFORMED")
            .thenApply(s -> "[" + s + "]");
        
        System.out.println("Transformed result: " + transformed.get());
    }
    
    private void demonstrateErrorHandling() throws Exception {
        System.out.println("\n=== Error Handling ===");
        
        CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
            throw new RuntimeException("Stream error");
        }, executor);
        
        // Handle error and provide fallback
        CompletableFuture<String> handled = future
            .handle((result, throwable) -> {
                if (throwable != null) {
                    return "Fallback value";
                }
                return result;
            });
        
        System.out.println("Error handling result: " + handled.get());
    }
    
    private CompletableFuture<String> createAsyncTask(String name, int delay) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(delay);
                return "Result from " + name;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException(e);
            }
        }, executor);
    }
    
    public static void main(String[] args) throws Exception {
        ReactiveProgrammingExample example = new ReactiveProgrammingExample();
        example.demonstrateReactiveProgramming();
    }
}
```

## 8.7 Event Loops

Event loops are a programming construct that continuously listens for events and executes callbacks when events occur. They're fundamental to asynchronous programming.

### Key Concepts:

**1. Event Loop:**
- Continuous loop checking for events
- Executes callbacks when events occur
- Non-blocking I/O operations

**2. Event Queue:**
- Queue of events waiting to be processed
- FIFO processing order
- Priority-based processing

**3. Callback Execution:**
- Functions executed when events occur
- Asynchronous execution
- Error handling

### Java Example - Simple Event Loop:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Consumer;

public class EventLoopExample {
    private final BlockingQueue<Event> eventQueue = new LinkedBlockingQueue<>();
    private final AtomicBoolean running = new AtomicBoolean(false);
    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    
    public void startEventLoop() {
        running.set(true);
        executor.submit(this::runEventLoop);
    }
    
    public void stopEventLoop() {
        running.set(false);
        executor.shutdown();
    }
    
    private void runEventLoop() {
        while (running.get()) {
            try {
                Event event = eventQueue.take();
                processEvent(event);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    private void processEvent(Event event) {
        try {
            event.getCallback().accept(event.getData());
        } catch (Exception e) {
            System.err.println("Error processing event: " + e.getMessage());
        }
    }
    
    public void emitEvent(String type, Object data, Consumer<Object> callback) {
        Event event = new Event(type, data, callback);
        eventQueue.offer(event);
    }
    
    private static class Event {
        private final String type;
        private final Object data;
        private final Consumer<Object> callback;
        
        public Event(String type, Object data, Consumer<Object> callback) {
            this.type = type;
            this.data = data;
            this.callback = callback;
        }
        
        public String getType() { return type; }
        public Object getData() { return data; }
        public Consumer<Object> getCallback() { return callback; }
    }
    
    public static void main(String[] args) throws InterruptedException {
        EventLoopExample eventLoop = new EventLoopExample();
        eventLoop.startEventLoop();
        
        // Emit events
        eventLoop.emitEvent("user", "John", data -> 
            System.out.println("User event: " + data));
        eventLoop.emitEvent("message", "Hello", data -> 
            System.out.println("Message event: " + data));
        eventLoop.emitEvent("error", "Something went wrong", data -> 
            System.err.println("Error event: " + data));
        
        Thread.sleep(2000);
        eventLoop.stopEventLoop();
    }
}
```

## 8.8 Non-Blocking I/O

Non-blocking I/O allows operations to return immediately without waiting for data to be available. This enables better resource utilization and responsiveness.

### Key Concepts:

**1. Non-Blocking Operations:**
- Return immediately
- Don't block the calling thread
- Use callbacks for completion

**2. I/O Multiplexing:**
- Monitor multiple I/O operations
- Single thread handles multiple connections
- Event-driven I/O

**3. Asynchronous I/O:**
- Operations complete asynchronously
- Callbacks handle results
- Better scalability

### Java Example - Non-Blocking I/O Simulation:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class NonBlockingIOExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    private final AtomicInteger requestCounter = new AtomicInteger(0);
    
    public void demonstrateNonBlockingIO() throws InterruptedException {
        // Simulate multiple concurrent I/O operations
        for (int i = 0; i < 10; i++) {
            performNonBlockingIO("Request " + i);
        }
        
        Thread.sleep(5000);
        executor.shutdown();
    }
    
    private void performNonBlockingIO(String requestId) {
        // Non-blocking: return immediately
        CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
            // Simulate I/O operation
            try {
                Thread.sleep(1000 + (int)(Math.random() * 2000));
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "Response for " + requestId;
        }, executor);
        
        // Handle result asynchronously
        future.thenAccept(response -> {
            int count = requestCounter.incrementAndGet();
            System.out.println("Received response: " + response + " (Count: " + count + ")");
        });
        
        System.out.println("Submitted " + requestId + " (non-blocking)");
    }
    
    public static void main(String[] args) throws InterruptedException {
        NonBlockingIOExample example = new NonBlockingIOExample();
        example.demonstrateNonBlockingIO();
    }
}
```

## 8.9 Asynchronous Error Handling

Proper error handling in asynchronous programming is crucial for building robust applications. Errors can occur at any point in the async chain.

### Key Concepts:

**1. Exception Propagation:**
- Exceptions in async operations
- Proper error handling
- Graceful degradation

**2. Error Recovery:**
- Retry mechanisms
- Fallback strategies
- Circuit breakers

**3. Error Monitoring:**
- Logging errors
- Metrics collection
- Alerting

### Java Example - Asynchronous Error Handling:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class AsynchronousErrorHandlingExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    private final AtomicInteger retryCount = new AtomicInteger(0);
    
    public void demonstrateErrorHandling() throws Exception {
        // Basic error handling
        demonstrateBasicErrorHandling();
        
        // Retry mechanism
        demonstrateRetryMechanism();
        
        // Fallback strategy
        demonstrateFallbackStrategy();
    }
    
    private void demonstrateBasicErrorHandling() throws Exception {
        System.out.println("=== Basic Error Handling ===");
        
        CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
            throw new RuntimeException("Simulated error");
        }, executor);
        
        future.handle((result, throwable) -> {
            if (throwable != null) {
                System.out.println("Error handled: " + throwable.getMessage());
                return "Error recovery result";
            }
            return result;
        }).thenAccept(result -> System.out.println("Final result: " + result));
        
        future.get();
    }
    
    private void demonstrateRetryMechanism() throws Exception {
        System.out.println("\n=== Retry Mechanism ===");
        
        CompletableFuture<String> future = retryOperation("Retry Task", 3);
        System.out.println("Retry result: " + future.get());
    }
    
    private CompletableFuture<String> retryOperation(String taskName, int maxRetries) {
        return CompletableFuture.supplyAsync(() -> {
            int attempts = retryCount.incrementAndGet();
            if (attempts <= maxRetries) {
                throw new RuntimeException("Attempt " + attempts + " failed");
            }
            return "Success after " + attempts + " attempts";
        }, executor)
        .handle((result, throwable) -> {
            if (throwable != null && retryCount.get() < maxRetries) {
                System.out.println("Retrying... (attempt " + retryCount.get() + ")");
                return retryOperation(taskName, maxRetries);
            }
            return CompletableFuture.completedFuture(result);
        })
        .thenCompose(Function.identity());
    }
    
    private void demonstrateFallbackStrategy() throws Exception {
        System.out.println("\n=== Fallback Strategy ===");
        
        CompletableFuture<String> future = CompletableFuture
            .supplyAsync(() -> {
                throw new RuntimeException("Primary operation failed");
            }, executor)
            .handle((result, throwable) -> {
                if (throwable != null) {
                    System.out.println("Primary failed, using fallback");
                    return "Fallback result";
                }
                return result;
            });
        
        System.out.println("Fallback result: " + future.get());
    }
    
    public static void main(String[] args) throws Exception {
        AsynchronousErrorHandlingExample example = new AsynchronousErrorHandlingExample();
        example.demonstrateErrorHandling();
    }
}
```

## 8.10 Asynchronous Best Practices

Following best practices ensures efficient, maintainable, and robust asynchronous code.

### Best Practices:

**1. Resource Management:**
- Properly close resources
- Use try-with-resources
- Avoid resource leaks

**2. Error Handling:**
- Handle all exceptions
- Provide meaningful error messages
- Implement retry mechanisms

**3. Performance:**
- Use appropriate thread pools
- Avoid blocking operations
- Monitor resource usage

### Java Example - Best Practices:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class AsynchronousBestPracticesExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    private final AtomicInteger taskCount = new AtomicInteger(0);
    
    public void demonstrateBestPractices() throws Exception {
        // Resource management
        demonstrateResourceManagement();
        
        // Error handling
        demonstrateErrorHandling();
        
        // Performance optimization
        demonstratePerformanceOptimization();
    }
    
    private void demonstrateResourceManagement() throws Exception {
        System.out.println("=== Resource Management ===");
        
        try (ExecutorService resourceExecutor = Executors.newFixedThreadPool(2)) {
            CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
                return "Resource managed task";
            }, resourceExecutor);
            
            System.out.println("Result: " + future.get());
        } // Executor automatically closed
    }
    
    private void demonstrateErrorHandling() throws Exception {
        System.out.println("\n=== Error Handling ===");
        
        CompletableFuture<String> future = CompletableFuture
            .supplyAsync(() -> {
                if (Math.random() > 0.5) {
                    throw new RuntimeException("Random error");
                }
                return "Success";
            }, executor)
            .exceptionally(throwable -> {
                System.out.println("Error handled: " + throwable.getMessage());
                return "Error recovery";
            });
        
        System.out.println("Result: " + future.get());
    }
    
    private void demonstratePerformanceOptimization() throws Exception {
        System.out.println("\n=== Performance Optimization ===");
        
        // Batch operations
        List<CompletableFuture<String>> futures = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            futures.add(CompletableFuture.supplyAsync(() -> {
                return "Task " + taskCount.incrementAndGet();
            }, executor));
        }
        
        // Wait for all to complete
        CompletableFuture<Void> allFutures = CompletableFuture.allOf(
            futures.toArray(new CompletableFuture[0])
        );
        
        allFutures.thenRun(() -> 
            System.out.println("All " + futures.size() + " tasks completed"));
        
        allFutures.get();
    }
    
    public static void main(String[] args) throws Exception {
        AsynchronousBestPracticesExample example = new AsynchronousBestPracticesExample();
        example.demonstrateBestPractices();
    }
}
```

### Real-World Analogy:
Think of asynchronous programming like a restaurant kitchen:
- **Callbacks**: Like order tickets that get called when food is ready
- **Promises/Futures**: Like order numbers that you can check on
- **Event Loops**: Like the kitchen manager who coordinates all the cooking
- **Non-blocking I/O**: Like taking multiple orders without waiting for each one to finish
- **Error Handling**: Like having backup plans when something goes wrong

The key is to keep the "kitchen" (your application) running smoothly even when individual "dishes" (tasks) take different amounts of time to complete!