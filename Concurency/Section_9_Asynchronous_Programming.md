# Section 9 – Asynchronous Programming

## 9.1 Callbacks and Callback Hell

Callbacks are functions that are passed as arguments to other functions and are executed when a specific event occurs or a task completes.

### Key Concepts
- **Callback**: Function passed as argument
- **Callback Hell**: Nested callbacks making code hard to read
- **Event-Driven**: Code responds to events
- **Asynchronous**: Non-blocking execution

### Real-World Analogy
Think of ordering food at a restaurant where you give your order (callback) to the waiter, and they call you back when your food is ready.

### Java Example
```java
public class CallbackExample {
    // Callback interface
    public interface Callback<T> {
        void onSuccess(T result);
        void onError(Throwable error);
    }
    
    // Asynchronous operation with callback
    public static void asyncOperation(String data, Callback<String> callback) {
        new Thread(() -> {
            try {
                // Simulate work
                Thread.sleep(1000);
                String result = "Processed: " + data;
                callback.onSuccess(result);
            } catch (Exception e) {
                callback.onError(e);
            }
        }).start();
    }
    
    // Callback hell example
    public static void demonstrateCallbackHell() {
        asyncOperation("Step 1", new Callback<String>() {
            @Override
            public void onSuccess(String result) {
                System.out.println("Step 1 completed: " + result);
                asyncOperation("Step 2", new Callback<String>() {
                    @Override
                    public void onSuccess(String result) {
                        System.out.println("Step 2 completed: " + result);
                        asyncOperation("Step 3", new Callback<String>() {
                            @Override
                            public void onSuccess(String result) {
                                System.out.println("Step 3 completed: " + result);
                            }
                            
                            @Override
                            public void onError(Throwable error) {
                                System.err.println("Step 3 error: " + error.getMessage());
                            }
                        });
                    }
                    
                    @Override
                    public void onError(Throwable error) {
                        System.err.println("Step 2 error: " + error.getMessage());
                    }
                });
            }
            
            @Override
            public void onError(Throwable error) {
                System.err.println("Step 1 error: " + error.getMessage());
            }
        });
    }
}
```

## 9.2 Promises and Futures

Promises and Futures provide a way to handle asynchronous operations more elegantly than callbacks, representing a value that will be available in the future.

### Key Concepts
- **Promise**: Represents a future value
- **Future**: Read-only view of a promise
- **Completable**: Can be completed with a value or error
- **Composable**: Can be chained and combined

### Real-World Analogy
Think of a ticket for a future event. You get the ticket now (promise), but the actual event (value) happens later.

### Java Example
```java
public class PromiseFutureExample {
    // Simple promise implementation
    public static class Promise<T> {
        private T value;
        private Throwable error;
        private boolean completed = false;
        private final List<Runnable> callbacks = new ArrayList<>();
        
        public void complete(T value) {
            synchronized (this) {
                if (completed) return;
                this.value = value;
                this.completed = true;
                notifyAll();
            }
            executeCallbacks();
        }
        
        public void completeExceptionally(Throwable error) {
            synchronized (this) {
                if (completed) return;
                this.error = error;
                this.completed = true;
                notifyAll();
            }
            executeCallbacks();
        }
        
        public T get() throws InterruptedException {
            synchronized (this) {
                while (!completed) {
                    wait();
                }
                if (error != null) {
                    throw new RuntimeException(error);
                }
                return value;
            }
        }
        
        public Promise<T> thenApply(Function<T, T> mapper) {
            Promise<T> newPromise = new Promise<>();
            callbacks.add(() -> {
                try {
                    T result = mapper.apply(value);
                    newPromise.complete(result);
                } catch (Exception e) {
                    newPromise.completeExceptionally(e);
                }
            });
            return newPromise;
        }
        
        private void executeCallbacks() {
            for (Runnable callback : callbacks) {
                callback.run();
            }
        }
    }
    
    // Asynchronous operation returning a promise
    public static Promise<String> asyncOperation(String data) {
        Promise<String> promise = new Promise<>();
        
        new Thread(() -> {
            try {
                Thread.sleep(1000);
                promise.complete("Processed: " + data);
            } catch (Exception e) {
                promise.completeExceptionally(e);
            }
        }).start();
        
        return promise;
    }
    
    public static void demonstratePromises() {
        Promise<String> promise = asyncOperation("Hello");
        
        promise.thenApply(result -> result.toUpperCase())
               .thenApply(result -> result + "!")
               .thenApply(result -> {
                   System.out.println("Final result: " + result);
                   return result;
               });
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 9.3 Async/Await Patterns

Async/await is a syntactic sugar that makes asynchronous code look and behave more like synchronous code, improving readability and maintainability.

### Key Concepts
- **Async**: Marks a function as asynchronous
- **Await**: Waits for an asynchronous operation to complete
- **Syntactic Sugar**: Makes code more readable
- **Error Handling**: Simplified error handling

### Real-World Analogy
Think of waiting in line at a coffee shop. You place your order (async) and wait (await) for it to be ready, but you can do other things while waiting.

### Java Example
```java
public class AsyncAwaitExample {
    // Simulate async/await with CompletableFuture
    public static CompletableFuture<String> asyncOperation(String data) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
                return "Processed: " + data;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException(e);
            }
        });
    }
    
    // Async function using CompletableFuture
    public static CompletableFuture<String> asyncFunction(String input) {
        return asyncOperation(input)
            .thenApply(result -> result.toUpperCase())
            .thenApply(result -> result + "!")
            .exceptionally(error -> "Error: " + error.getMessage());
    }
    
    // Chaining async operations
    public static CompletableFuture<String> chainAsyncOperations() {
        return asyncOperation("Step 1")
            .thenCompose(result1 -> {
                System.out.println("Step 1 completed: " + result1);
                return asyncOperation("Step 2");
            })
            .thenCompose(result2 -> {
                System.out.println("Step 2 completed: " + result2);
                return asyncOperation("Step 3");
            })
            .thenApply(result3 -> {
                System.out.println("Step 3 completed: " + result3);
                return "All steps completed";
            });
    }
    
    public static void demonstrateAsyncAwait() {
        // Simple async operation
        asyncFunction("Hello")
            .thenAccept(result -> System.out.println("Result: " + result))
            .join();
        
        // Chained async operations
        chainAsyncOperations()
            .thenAccept(result -> System.out.println("Final result: " + result))
            .join();
    }
}
```

## 9.4 Coroutines

Coroutines are lightweight threads that can be suspended and resumed, allowing for efficient concurrent programming without the overhead of traditional threads.

### Key Concepts
- **Suspendable**: Can be paused and resumed
- **Lightweight**: Lower overhead than threads
- **Cooperative**: Yield control voluntarily
- **Stateful**: Maintain state between suspensions

### Real-World Analogy
Think of a worker who can pause their current task to help with something urgent, then resume their original task exactly where they left off.

### Java Example
```java
public class CoroutinesExample {
    // Simple coroutine implementation
    public static class Coroutine {
        private final Runnable task;
        private volatile boolean running = false;
        private volatile boolean suspended = false;
        private Thread thread;
        
        public Coroutine(Runnable task) {
            this.task = task;
        }
        
        public void start() {
            if (!running) {
                running = true;
                thread = new Thread(() -> {
                    while (running) {
                        if (!suspended) {
                            try {
                                task.run();
                            } catch (Exception e) {
                                System.err.println("Coroutine error: " + e.getMessage());
                            }
                        }
                        try {
                            Thread.sleep(10);
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                            break;
                        }
                    }
                });
                thread.start();
            }
        }
        
        public void suspend() {
            suspended = true;
        }
        
        public void resume() {
            suspended = false;
        }
        
        public void stop() {
            running = false;
            if (thread != null) {
                thread.interrupt();
            }
        }
    }
    
    // Coroutine that yields control
    public static class YieldingCoroutine {
        private int count = 0;
        private final int maxCount;
        
        public YieldingCoroutine(int maxCount) {
            this.maxCount = maxCount;
        }
        
        public void run() {
            while (count < maxCount) {
                System.out.println("Coroutine count: " + count);
                count++;
                
                // Yield control every 3 iterations
                if (count % 3 == 0) {
                    System.out.println("Yielding control...");
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            }
        }
    }
    
    public static void demonstrateCoroutines() {
        YieldingCoroutine yieldingTask = new YieldingCoroutine(10);
        Coroutine coroutine = new Coroutine(() -> yieldingTask.run());
        
        coroutine.start();
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        coroutine.stop();
    }
}
```

## 9.5 Generators and Iterators

Generators are functions that can be paused and resumed, producing a sequence of values over time, while iterators provide a way to traverse collections.

### Key Concepts
- **Generator**: Function that yields values
- **Iterator**: Object for traversing collections
- **Lazy Evaluation**: Values produced on demand
- **Stateful**: Maintains state between calls

### Real-World Analogy
Think of a vending machine that produces items one at a time when you press a button, rather than having all items ready at once.

### Java Example
```java
public class GeneratorsIteratorsExample {
    // Simple generator interface
    public interface Generator<T> {
        T next();
        boolean hasNext();
    }
    
    // Number generator
    public static class NumberGenerator implements Generator<Integer> {
        private int current = 0;
        private final int max;
        
        public NumberGenerator(int max) {
            this.max = max;
        }
        
        @Override
        public Integer next() {
            if (hasNext()) {
                return current++;
            }
            throw new NoSuchElementException();
        }
        
        @Override
        public boolean hasNext() {
            return current < max;
        }
    }
    
    // Fibonacci generator
    public static class FibonacciGenerator implements Generator<Long> {
        private long prev = 0;
        private long curr = 1;
        private final int max;
        private int count = 0;
        
        public FibonacciGenerator(int max) {
            this.max = max;
        }
        
        @Override
        public Long next() {
            if (hasNext()) {
                long result = prev;
                long next = prev + curr;
                prev = curr;
                curr = next;
                count++;
                return result;
            }
            throw new NoSuchElementException();
        }
        
        @Override
        public boolean hasNext() {
            return count < max;
        }
    }
    
    // Custom iterator
    public static class CustomIterator<T> implements Iterator<T> {
        private final List<T> items;
        private int index = 0;
        
        public CustomIterator(List<T> items) {
            this.items = new ArrayList<>(items);
        }
        
        @Override
        public boolean hasNext() {
            return index < items.size();
        }
        
        @Override
        public T next() {
            if (hasNext()) {
                return items.get(index++);
            }
            throw new NoSuchElementException();
        }
    }
    
    public static void demonstrateGeneratorsIterators() {
        // Number generator
        System.out.println("Number Generator:");
        NumberGenerator numberGen = new NumberGenerator(5);
        while (numberGen.hasNext()) {
            System.out.println(numberGen.next());
        }
        
        // Fibonacci generator
        System.out.println("\nFibonacci Generator:");
        FibonacciGenerator fibGen = new FibonacciGenerator(10);
        while (fibGen.hasNext()) {
            System.out.println(fibGen.next());
        }
        
        // Custom iterator
        System.out.println("\nCustom Iterator:");
        List<String> items = Arrays.asList("A", "B", "C", "D", "E");
        CustomIterator<String> iterator = new CustomIterator<>(items);
        while (iterator.hasNext()) {
            System.out.println(iterator.next());
        }
    }
}
```

## 9.6 Event Loops

Event loops are the core of asynchronous programming, continuously checking for and processing events in a single thread.

### Key Concepts
- **Single Thread**: All events processed in one thread
- **Non-blocking**: Never blocks waiting for I/O
- **Event Queue**: Queue of events to process
- **Callbacks**: Functions called when events occur

### Real-World Analogy
Think of a receptionist who continuously checks for phone calls, visitors, and messages, handling each one as it comes in without getting stuck on any single task.

### Java Example
```java
public class EventLoopExample {
    // Event interface
    public interface Event {
        void execute();
    }
    
    // Simple event loop
    public static class EventLoop {
        private final Queue<Event> eventQueue = new ConcurrentLinkedQueue<>();
        private volatile boolean running = false;
        private Thread loopThread;
        
        public void start() {
            if (!running) {
                running = true;
                loopThread = new Thread(() -> {
                    while (running) {
                        Event event = eventQueue.poll();
                        if (event != null) {
                            try {
                                event.execute();
                            } catch (Exception e) {
                                System.err.println("Event execution error: " + e.getMessage());
                            }
                        } else {
                            try {
                                Thread.sleep(10);
                            } catch (InterruptedException e) {
                                Thread.currentThread().interrupt();
                                break;
                            }
                        }
                    }
                });
                loopThread.start();
            }
        }
        
        public void stop() {
            running = false;
            if (loopThread != null) {
                loopThread.interrupt();
            }
        }
        
        public void postEvent(Event event) {
            eventQueue.offer(event);
        }
    }
    
    // Timer event
    public static class TimerEvent implements Event {
        private final String message;
        private final long delay;
        
        public TimerEvent(String message, long delay) {
            this.message = message;
            this.delay = delay;
        }
        
        @Override
        public void execute() {
            try {
                Thread.sleep(delay);
                System.out.println("Timer event: " + message);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    // I/O event simulation
    public static class IOEvent implements Event {
        private final String data;
        
        public IOEvent(String data) {
            this.data = data;
        }
        
        @Override
        public void execute() {
            System.out.println("I/O event processed: " + data);
        }
    }
    
    public static void demonstrateEventLoop() {
        EventLoop eventLoop = new EventLoop();
        eventLoop.start();
        
        // Post various events
        eventLoop.postEvent(new TimerEvent("Timer 1", 1000));
        eventLoop.postEvent(new IOEvent("File read"));
        eventLoop.postEvent(new TimerEvent("Timer 2", 500));
        eventLoop.postEvent(new IOEvent("Network request"));
        
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        eventLoop.stop();
    }
}
```

## 9.7 Non-Blocking I/O

Non-blocking I/O allows operations to return immediately without waiting for data to be available, enabling efficient handling of multiple I/O operations.

### Key Concepts
- **Non-blocking**: Operations return immediately
- **Selectors**: Monitor multiple I/O channels
- **Event-driven**: Respond to I/O events
- **Scalability**: Handle many connections efficiently

### Real-World Analogy
Think of a busy restaurant where the chef doesn't wait for each order to be ready before starting the next one. Instead, they check which orders are ready and work on them as needed.

### Java Example
```java
public class NonBlockingIOExample {
    // Non-blocking I/O simulation
    public static class NonBlockingIO {
        private final Map<String, CompletableFuture<String>> pendingOperations = new ConcurrentHashMap<>();
        
        public CompletableFuture<String> readAsync(String resource) {
            CompletableFuture<String> future = new CompletableFuture<>();
            pendingOperations.put(resource, future);
            
            // Simulate async I/O
            new Thread(() -> {
                try {
                    Thread.sleep(1000 + (int)(Math.random() * 1000));
                    String result = "Data from " + resource;
                    future.complete(result);
                    pendingOperations.remove(resource);
                } catch (Exception e) {
                    future.completeExceptionally(e);
                    pendingOperations.remove(resource);
                }
            }).start();
            
            return future;
        }
        
        public void processReadyOperations() {
            List<String> readyResources = new ArrayList<>();
            
            for (Map.Entry<String, CompletableFuture<String>> entry : pendingOperations.entrySet()) {
                if (entry.getValue().isDone()) {
                    readyResources.add(entry.getKey());
                }
            }
            
            for (String resource : readyResources) {
                CompletableFuture<String> future = pendingOperations.get(resource);
                if (future != null && future.isDone()) {
                    try {
                        String result = future.get();
                        System.out.println("Processed: " + result);
                    } catch (Exception e) {
                        System.err.println("Error processing " + resource + ": " + e.getMessage());
                    }
                }
            }
        }
        
        public int getPendingCount() {
            return pendingOperations.size();
        }
    }
    
    // Selector simulation
    public static class Selector {
        private final List<CompletableFuture<String>> channels = new ArrayList<>();
        
        public void register(CompletableFuture<String> channel) {
            channels.add(channel);
        }
        
        public List<CompletableFuture<String>> select() {
            List<CompletableFuture<String>> readyChannels = new ArrayList<>();
            
            for (CompletableFuture<String> channel : channels) {
                if (channel.isDone()) {
                    readyChannels.add(channel);
                }
            }
            
            return readyChannels;
        }
    }
    
    public static void demonstrateNonBlockingIO() {
        NonBlockingIO nio = new NonBlockingIO();
        Selector selector = new Selector();
        
        // Start multiple I/O operations
        String[] resources = {"file1.txt", "file2.txt", "file3.txt", "file4.txt"};
        for (String resource : resources) {
            CompletableFuture<String> future = nio.readAsync(resource);
            selector.register(future);
        }
        
        // Process ready operations
        while (selector.select().size() < resources.length) {
            List<CompletableFuture<String>> readyChannels = selector.select();
            for (CompletableFuture<String> channel : readyChannels) {
                try {
                    String result = channel.get();
                    System.out.println("Ready: " + result);
                } catch (Exception e) {
                    System.err.println("Error: " + e.getMessage());
                }
            }
            
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
}
```

## 9.8 Asynchronous Error Handling

Asynchronous error handling requires special techniques to properly catch, propagate, and handle errors that occur in asynchronous operations.

### Key Concepts
- **Error Propagation**: How errors flow through async chains
- **Error Recovery**: Strategies for handling errors
- **Timeout Handling**: Dealing with operations that take too long
- **Circuit Breakers**: Preventing cascading failures

### Real-World Analogy
Think of a delivery service where if one package can't be delivered, the system needs to decide whether to retry, return it, or find an alternative delivery method.

### Java Example
```java
public class AsynchronousErrorHandlingExample {
    // Asynchronous operation with error handling
    public static CompletableFuture<String> asyncOperationWithError(String data, boolean shouldFail) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
                if (shouldFail) {
                    throw new RuntimeException("Simulated error for: " + data);
                }
                return "Success: " + data;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException(e);
            }
        });
    }
    
    // Error handling strategies
    public static void demonstrateErrorHandling() {
        // 1. Basic error handling
        asyncOperationWithError("test1", false)
            .thenAccept(result -> System.out.println("Success: " + result))
            .exceptionally(error -> {
                System.err.println("Error: " + error.getMessage());
                return null;
            })
            .join();
        
        // 2. Error handling with recovery
        asyncOperationWithError("test2", true)
            .handle((result, error) -> {
                if (error != null) {
                    System.err.println("Error occurred: " + error.getMessage());
                    return "Recovered from error";
                }
                return result;
            })
            .thenAccept(result -> System.out.println("Result: " + result))
            .join();
        
        // 3. Retry mechanism
        retryAsyncOperation("test3", 3)
            .thenAccept(result -> System.out.println("Final result: " + result))
            .join();
        
        // 4. Timeout handling
        timeoutAsyncOperation("test4", 2000)
            .thenAccept(result -> System.out.println("Timeout result: " + result))
            .join();
    }
    
    // Retry mechanism
    public static CompletableFuture<String> retryAsyncOperation(String data, int maxRetries) {
        return asyncOperationWithError(data, true)
            .handle((result, error) -> {
                if (error != null && maxRetries > 0) {
                    System.out.println("Retrying... " + (maxRetries - 1) + " attempts left");
                    return retryAsyncOperation(data, maxRetries - 1);
                }
                return CompletableFuture.completedFuture(result != null ? result : "Failed after retries");
            })
            .thenCompose(future -> future);
    }
    
    // Timeout handling
    public static CompletableFuture<String> timeoutAsyncOperation(String data, long timeoutMs) {
        CompletableFuture<String> operation = asyncOperationWithError(data, false);
        CompletableFuture<String> timeout = new CompletableFuture<>();
        
        // Set timeout
        new Thread(() -> {
            try {
                Thread.sleep(timeoutMs);
                timeout.complete("Operation timed out");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }).start();
        
        return CompletableFuture.anyOf(operation, timeout)
            .thenApply(result -> (String) result);
    }
    
    // Circuit breaker pattern
    public static class CircuitBreaker {
        private final int failureThreshold;
        private final long timeout;
        private final AtomicInteger failureCount = new AtomicInteger(0);
        private final AtomicLong lastFailureTime = new AtomicLong(0);
        private volatile boolean isOpen = false;
        
        public CircuitBreaker(int failureThreshold, long timeout) {
            this.failureThreshold = failureThreshold;
            this.timeout = timeout;
        }
        
        public <T> CompletableFuture<T> execute(Supplier<CompletableFuture<T>> operation) {
            if (isOpen) {
                if (System.currentTimeMillis() - lastFailureTime.get() > timeout) {
                    isOpen = false;
                    failureCount.set(0);
                    System.out.println("Circuit breaker: attempting to close");
                } else {
                    return CompletableFuture.failedFuture(new RuntimeException("Circuit breaker is open"));
                }
            }
            
            return operation.get()
                .handle((result, error) -> {
                    if (error != null) {
                        int failures = failureCount.incrementAndGet();
                        lastFailureTime.set(System.currentTimeMillis());
                        
                        if (failures >= failureThreshold) {
                            isOpen = true;
                            System.out.println("Circuit breaker: opened due to " + failures + " failures");
                        }
                        
                        throw new RuntimeException(error);
                    }
                    
                    failureCount.set(0);
                    return result;
                });
        }
    }
    
    public static void demonstrateCircuitBreaker() {
        CircuitBreaker circuitBreaker = new CircuitBreaker(3, 5000);
        
        // Simulate multiple operations
        for (int i = 0; i < 10; i++) {
            final int attempt = i;
            circuitBreaker.execute(() -> asyncOperationWithError("test" + attempt, attempt < 5))
                .thenAccept(result -> System.out.println("Attempt " + attempt + " succeeded: " + result))
                .exceptionally(error -> {
                    System.err.println("Attempt " + attempt + " failed: " + error.getMessage());
                    return null;
                });
            
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
}
```

This comprehensive explanation covers all aspects of asynchronous programming, providing both theoretical understanding and practical Java examples to illustrate each concept.