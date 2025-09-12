# Section 16 - Concurrency Models

## 16.1 Actor Model

The Actor Model is a mathematical model of concurrent computation where actors are the fundamental units of computation. Each actor can send messages to other actors, create new actors, and change its behavior in response to messages.

### Key Concepts:

**1. Actors:**
- Independent units of computation
- Have their own state
- Communicate only through messages

**2. Messages:**
- Asynchronous communication
- Immutable data
- No shared state

**3. Mailboxes:**
- Message queues for each actor
- FIFO ordering
- Buffering mechanism

### Java Example - Actor Model:

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class ActorModelExample {
    // Message interface
    interface Message {}
    
    // Greeting message
    static class GreetingMessage implements Message {
        private final String name;
        
        public GreetingMessage(String name) {
            this.name = name;
        }
        
        public String getName() {
            return name;
        }
    }
    
    // Response message
    static class ResponseMessage implements Message {
        private final String response;
        
        public ResponseMessage(String response) {
            this.response = response;
        }
        
        public String getResponse() {
            return response;
        }
    }
    
    // Actor class
    static class Actor {
        private final BlockingQueue<Message> mailbox = new LinkedBlockingQueue<>();
        private final AtomicBoolean running = new AtomicBoolean(true);
        private final String name;
        
        public Actor(String name) {
            this.name = name;
        }
        
        public void start() {
            Thread actorThread = new Thread(() -> {
                while (running.get()) {
                    try {
                        Message message = mailbox.take();
                        handleMessage(message);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
            actorThread.start();
        }
        
        public void send(Message message) {
            mailbox.offer(message);
        }
        
        public void stop() {
            running.set(false);
        }
        
        private void handleMessage(Message message) {
            if (message instanceof GreetingMessage) {
                GreetingMessage greeting = (GreetingMessage) message;
                System.out.println("Actor " + name + " received greeting from " + greeting.getName());
                
                // Send response back
                ResponseMessage response = new ResponseMessage("Hello " + greeting.getName() + "!");
                System.out.println("Actor " + name + " sending response: " + response.getResponse());
            }
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        // Create actors
        Actor actor1 = new Actor("Actor1");
        Actor actor2 = new Actor("Actor2");
        
        // Start actors
        actor1.start();
        actor2.start();
        
        // Send messages
        actor1.send(new GreetingMessage("Alice"));
        actor2.send(new GreetingMessage("Bob"));
        
        // Wait a bit
        Thread.sleep(1000);
        
        // Stop actors
        actor1.stop();
        actor2.stop();
    }
}
```

## 16.2 Communicating Sequential Processes (CSP)

CSP is a formal language for describing patterns of interaction in concurrent systems. It emphasizes communication between processes rather than shared memory.

### Key Concepts:

**1. Processes:**
- Sequential programs
- No shared variables
- Communicate through channels

**2. Channels:**
- Communication mechanism
- Synchronous or asynchronous
- Type-safe communication

**3. Operations:**
- Input (!)
- Output (?)
- Choice (|)
- Parallel (||)

### Java Example - CSP:

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class CSPExample {
    // Channel interface
    interface Channel<T> {
        void send(T value) throws InterruptedException;
        T receive() throws InterruptedException;
    }
    
    // Blocking channel implementation
    static class BlockingChannel<T> implements Channel<T> {
        private final BlockingQueue<T> queue = new LinkedBlockingQueue<>();
        
        @Override
        public void send(T value) throws InterruptedException {
            queue.put(value);
        }
        
        @Override
        public T receive() throws InterruptedException {
            return queue.take();
        }
    }
    
    // Process 1: Producer
    static class Producer {
        private final Channel<Integer> channel;
        private final AtomicBoolean running = new AtomicBoolean(true);
        
        public Producer(Channel<Integer> channel) {
            this.channel = channel;
        }
        
        public void start() {
            Thread producerThread = new Thread(() -> {
                try {
                    for (int i = 1; i <= 10; i++) {
                        channel.send(i);
                        System.out.println("Producer sent: " + i);
                        Thread.sleep(100);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            producerThread.start();
        }
        
        public void stop() {
            running.set(false);
        }
    }
    
    // Process 2: Consumer
    static class Consumer {
        private final Channel<Integer> channel;
        private final AtomicBoolean running = new AtomicBoolean(true);
        
        public Consumer(Channel<Integer> channel) {
            this.channel = channel;
        }
        
        public void start() {
            Thread consumerThread = new Thread(() -> {
                try {
                    while (running.get()) {
                        Integer value = channel.receive();
                        System.out.println("Consumer received: " + value);
                        Thread.sleep(150);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            consumerThread.start();
        }
        
        public void stop() {
            running.set(false);
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        // Create channel
        Channel<Integer> channel = new BlockingChannel<>();
        
        // Create processes
        Producer producer = new Producer(channel);
        Consumer consumer = new Consumer(channel);
        
        // Start processes
        producer.start();
        consumer.start();
        
        // Wait for completion
        Thread.sleep(2000);
        
        // Stop processes
        producer.stop();
        consumer.stop();
    }
}
```

## 16.3 Dataflow Programming

Dataflow programming is a programming paradigm where the program is modeled as a directed graph of data flowing between operations. It's particularly useful for parallel and concurrent programming.

### Key Concepts:

**1. Dataflow Graph:**
- Nodes represent operations
- Edges represent data flow
- Implicit parallelism

**2. Tokens:**
- Data units flowing through the graph
- Carry values between operations
- Enable parallel execution

**3. Firing Rules:**
- When to execute operations
- Based on data availability
- Automatic scheduling

### Java Example - Dataflow Programming:

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Function;

public class DataflowExample {
    // Dataflow node
    static class DataflowNode<T, R> {
        private final Function<T, R> operation;
        private final BlockingQueue<T> inputQueue = new LinkedBlockingQueue<>();
        private final BlockingQueue<R> outputQueue = new LinkedBlockingQueue<>();
        private final AtomicBoolean running = new AtomicBoolean(true);
        
        public DataflowNode(Function<T, R> operation) {
            this.operation = operation;
        }
        
        public void start() {
            Thread nodeThread = new Thread(() -> {
                while (running.get()) {
                    try {
                        T input = inputQueue.take();
                        R output = operation.apply(input);
                        outputQueue.put(output);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
            nodeThread.start();
        }
        
        public void sendInput(T input) throws InterruptedException {
            inputQueue.put(input);
        }
        
        public R getOutput() throws InterruptedException {
            return outputQueue.take();
        }
        
        public void stop() {
            running.set(false);
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        // Create dataflow nodes
        DataflowNode<Integer, Integer> multiplyNode = new DataflowNode<>(x -> x * 2);
        DataflowNode<Integer, Integer> addNode = new DataflowNode<>(x -> x + 1);
        DataflowNode<Integer, String> toStringNode = new DataflowNode<>(x -> "Result: " + x);
        
        // Start nodes
        multiplyNode.start();
        addNode.start();
        toStringNode.start();
        
        // Send data through the pipeline
        for (int i = 1; i <= 5; i++) {
            multiplyNode.sendInput(i);
            Integer multiplied = multiplyNode.getOutput();
            
            addNode.sendInput(multiplied);
            Integer added = addNode.getOutput();
            
            toStringNode.sendInput(added);
            String result = toStringNode.getOutput();
            
            System.out.println("Input: " + i + " -> " + result);
        }
        
        // Stop nodes
        multiplyNode.stop();
        addNode.stop();
        toStringNode.stop();
    }
}
```

## 16.4 Reactive Programming

Reactive programming is a programming paradigm that deals with asynchronous data streams and the propagation of change. It's particularly useful for handling events and asynchronous operations.

### Key Concepts:

**1. Observables:**
- Data streams
- Can emit values over time
- Can complete or error

**2. Observers:**
- Subscribe to observables
- React to emitted values
- Handle completion and errors

**3. Operators:**
- Transform data streams
- Filter, map, reduce
- Combine multiple streams

### Java Example - Reactive Programming:

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;

public class ReactiveExample {
    // Observable interface
    interface Observable<T> {
        void subscribe(Observer<T> observer);
        void unsubscribe(Observer<T> observer);
    }
    
    // Observer interface
    interface Observer<T> {
        void onNext(T value);
        void onError(Throwable error);
        void onComplete();
    }
    
    // Simple observable implementation
    static class SimpleObservable<T> implements Observable<T> {
        private final BlockingQueue<T> values = new LinkedBlockingQueue<>();
        private final AtomicBoolean running = new AtomicBoolean(true);
        private final AtomicBoolean completed = new AtomicBoolean(false);
        
        public void start() {
            Thread observableThread = new Thread(() -> {
                while (running.get() && !completed.get()) {
                    try {
                        T value = values.take();
                        // Notify observers
                        notifyObservers(value);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
            observableThread.start();
        }
        
        public void emit(T value) throws InterruptedException {
            if (!completed.get()) {
                values.put(value);
            }
        }
        
        public void complete() {
            completed.set(true);
        }
        
        public void stop() {
            running.set(false);
        }
        
        private void notifyObservers(T value) {
            // In a real implementation, this would notify all subscribed observers
            System.out.println("Emitted: " + value);
        }
    }
    
    // Observer implementation
    static class SimpleObserver<T> implements Observer<T> {
        private final String name;
        
        public SimpleObserver(String name) {
            this.name = name;
        }
        
        @Override
        public void onNext(T value) {
            System.out.println(name + " received: " + value);
        }
        
        @Override
        public void onError(Throwable error) {
            System.out.println(name + " error: " + error.getMessage());
        }
        
        @Override
        public void onComplete() {
            System.out.println(name + " completed");
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        // Create observable
        SimpleObservable<Integer> observable = new SimpleObservable<>();
        
        // Start observable
        observable.start();
        
        // Emit values
        for (int i = 1; i <= 5; i++) {
            observable.emit(i);
            Thread.sleep(100);
        }
        
        // Complete observable
        observable.complete();
        
        // Stop observable
        observable.stop();
    }
}
```

## 16.5 Event-Driven Programming

Event-driven programming is a programming paradigm where the flow of the program is determined by events such as user actions, sensor outputs, or messages from other programs.

### Key Concepts:

**1. Events:**
- Occurrences that trigger actions
- Can be user input, system events, or custom events
- Asynchronous in nature

**2. Event Handlers:**
- Functions that respond to events
- Register for specific events
- Execute when events occur

**3. Event Loop:**
- Continuously checks for events
- Dispatches events to handlers
- Manages event queue

### Java Example - Event-Driven Programming:

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.function.Consumer;

public class EventDrivenExample {
    // Event interface
    interface Event {}
    
    // Button click event
    static class ButtonClickEvent implements Event {
        private final String buttonId;
        
        public ButtonClickEvent(String buttonId) {
            this.buttonId = buttonId;
        }
        
        public String getButtonId() {
            return buttonId;
        }
    }
    
    // Key press event
    static class KeyPressEvent implements Event {
        private final char key;
        
        public KeyPressEvent(char key) {
            this.key = key;
        }
        
        public char getKey() {
            return key;
        }
    }
    
    // Event handler interface
    interface EventHandler<T extends Event> {
        void handle(T event);
    }
    
    // Event dispatcher
    static class EventDispatcher {
        private final BlockingQueue<Event> eventQueue = new LinkedBlockingQueue<>();
        private final AtomicBoolean running = new AtomicBoolean(true);
        
        public void start() {
            Thread dispatcherThread = new Thread(() -> {
                while (running.get()) {
                    try {
                        Event event = eventQueue.take();
                        dispatchEvent(event);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
            dispatcherThread.start();
        }
        
        public void postEvent(Event event) throws InterruptedException {
            eventQueue.put(event);
        }
        
        public void stop() {
            running.set(false);
        }
        
        private void dispatchEvent(Event event) {
            if (event instanceof ButtonClickEvent) {
                ButtonClickEvent buttonEvent = (ButtonClickEvent) event;
                System.out.println("Button clicked: " + buttonEvent.getButtonId());
            } else if (event instanceof KeyPressEvent) {
                KeyPressEvent keyEvent = (KeyPressEvent) event;
                System.out.println("Key pressed: " + keyEvent.getKey());
            }
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        // Create event dispatcher
        EventDispatcher dispatcher = new EventDispatcher();
        
        // Start dispatcher
        dispatcher.start();
        
        // Post events
        dispatcher.postEvent(new ButtonClickEvent("submit"));
        dispatcher.postEvent(new KeyPressEvent('a'));
        dispatcher.postEvent(new ButtonClickEvent("cancel"));
        dispatcher.postEvent(new KeyPressEvent('b'));
        
        // Wait a bit
        Thread.sleep(1000);
        
        // Stop dispatcher
        dispatcher.stop();
    }
}
```

## 16.6 Message Passing

Message passing is a communication paradigm where processes communicate by sending and receiving messages. It's a fundamental concept in distributed systems and concurrent programming.

### Key Concepts:

**1. Messages:**
- Data packets sent between processes
- Can contain any type of data
- Asynchronous or synchronous

**2. Channels:**
- Communication pathways
- Can be unidirectional or bidirectional
- Can be buffered or unbuffered

**3. Processes:**
- Independent units of execution
- Communicate only through messages
- No shared memory

### Java Example - Message Passing:

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class MessagePassingExample {
    // Message interface
    interface Message {}
    
    // Text message
    static class TextMessage implements Message {
        private final String content;
        private final String sender;
        
        public TextMessage(String content, String sender) {
            this.content = content;
            this.sender = sender;
        }
        
        public String getContent() {
            return content;
        }
        
        public String getSender() {
            return sender;
        }
    }
    
    // Process class
    static class Process {
        private final String name;
        private final BlockingQueue<Message> inbox = new LinkedBlockingQueue<>();
        private final AtomicBoolean running = new AtomicBoolean(true);
        
        public Process(String name) {
            this.name = name;
        }
        
        public void start() {
            Thread processThread = new Thread(() -> {
                while (running.get()) {
                    try {
                        Message message = inbox.take();
                        handleMessage(message);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
            processThread.start();
        }
        
        public void sendMessage(Process recipient, Message message) throws InterruptedException {
            recipient.inbox.put(message);
        }
        
        public void stop() {
            running.set(false);
        }
        
        private void handleMessage(Message message) {
            if (message instanceof TextMessage) {
                TextMessage textMessage = (TextMessage) message;
                System.out.println(name + " received from " + textMessage.getSender() + 
                                 ": " + textMessage.getContent());
            }
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        // Create processes
        Process process1 = new Process("Process1");
        Process process2 = new Process("Process2");
        
        // Start processes
        process1.start();
        process2.start();
        
        // Send messages
        process1.sendMessage(process2, new TextMessage("Hello from Process1", "Process1"));
        process2.sendMessage(process1, new TextMessage("Hello from Process2", "Process2"));
        
        // Wait a bit
        Thread.sleep(1000);
        
        // Stop processes
        process1.stop();
        process2.stop();
    }
}
```

## 16.7 Shared Memory Model

The shared memory model is a programming paradigm where multiple processes or threads share a common memory space. It's the most common model in multithreaded programming.

### Key Concepts:

**1. Shared Variables:**
- Variables accessible by multiple threads
- Require synchronization
- Can cause race conditions

**2. Synchronization:**
- Mechanisms to control access
- Locks, semaphores, barriers
- Prevent race conditions

**3. Memory Consistency:**
- Ordering of memory operations
- Visibility of changes
- Cache coherence

### Java Example - Shared Memory Model:

```java
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

public class SharedMemoryExample {
    private int sharedCounter = 0;
    private final AtomicInteger atomicCounter = new AtomicInteger(0);
    private final ReentrantLock lock = new ReentrantLock();
    
    public void demonstrateSharedMemory() throws InterruptedException {
        // Test unsynchronized access
        testUnsynchronizedAccess();
        
        // Test synchronized access
        testSynchronizedAccess();
        
        // Test atomic access
        testAtomicAccess();
    }
    
    private void testUnsynchronizedAccess() throws InterruptedException {
        System.out.println("=== Unsynchronized Access ===");
        
        sharedCounter = 0;
        Thread[] threads = new Thread[4];
        
        for (int i = 0; i < 4; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    sharedCounter++; // Race condition!
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Expected: 4000, Actual: " + sharedCounter);
    }
    
    private void testSynchronizedAccess() throws InterruptedException {
        System.out.println("\n=== Synchronized Access ===");
        
        sharedCounter = 0;
        Thread[] threads = new Thread[4];
        
        for (int i = 0; i < 4; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    lock.lock();
                    try {
                        sharedCounter++;
                    } finally {
                        lock.unlock();
                    }
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Expected: 4000, Actual: " + sharedCounter);
    }
    
    private void testAtomicAccess() throws InterruptedException {
        System.out.println("\n=== Atomic Access ===");
        
        atomicCounter.set(0);
        Thread[] threads = new Thread[4];
        
        for (int i = 0; i < 4; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    atomicCounter.incrementAndGet();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Expected: 4000, Actual: " + atomicCounter.get());
    }
    
    public static void main(String[] args) throws InterruptedException {
        SharedMemoryExample example = new SharedMemoryExample();
        example.demonstrateSharedMemory();
    }
}
```

## 16.8 Functional Programming

Functional programming is a programming paradigm that treats computation as the evaluation of mathematical functions. It emphasizes immutability and avoids side effects, making it naturally suitable for concurrent programming.

### Key Concepts:

**1. Immutability:**
- Data cannot be changed after creation
- No side effects
- Thread-safe by default

**2. Pure Functions:**
- Same input always produces same output
- No side effects
- Easy to test and reason about

**3. Higher-Order Functions:**
- Functions that take other functions as parameters
- Functions that return other functions
- Enable composition and abstraction

### Java Example - Functional Programming:

```java
import java.util.Arrays;
import java.util.List;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;

public class FunctionalProgrammingExample {
    public void demonstrateFunctionalProgramming() {
        // Immutable data
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        
        // Pure functions
        Function<Integer, Integer> square = x -> x * x;
        Function<Integer, Integer> doubleValue = x -> x * 2;
        Predicate<Integer> isEven = x -> x % 2 == 0;
        
        // Function composition
        Function<Integer, Integer> squareThenDouble = square.andThen(doubleValue);
        
        // Higher-order functions
        List<Integer> result = numbers.stream()
                .filter(isEven)
                .map(squareThenDouble)
                .collect(Collectors.toList());
        
        System.out.println("Original: " + numbers);
        System.out.println("Filtered (even), squared, then doubled: " + result);
        
        // Parallel processing
        List<Integer> parallelResult = numbers.parallelStream()
                .filter(isEven)
                .map(square)
                .collect(Collectors.toList());
        
        System.out.println("Parallel processing result: " + parallelResult);
    }
    
    // Pure function example
    public static int add(int a, int b) {
        return a + b;
    }
    
    // Higher-order function example
    public static <T> List<T> filter(List<T> list, Predicate<T> predicate) {
        return list.stream()
                .filter(predicate)
                .collect(Collectors.toList());
    }
    
    // Function composition example
    public static <T, U, V> Function<T, V> compose(Function<T, U> f, Function<U, V> g) {
        return x -> g.apply(f.apply(x));
    }
    
    public static void main(String[] args) {
        FunctionalProgrammingExample example = new FunctionalProgrammingExample();
        example.demonstrateFunctionalProgramming();
    }
}
```

## 16.9 Concurrent Programming Patterns

Concurrent programming patterns are common solutions to recurring problems in concurrent programming. They provide proven approaches to handle concurrency challenges.

### Key Patterns:

**1. Producer-Consumer:**
- Separate production and consumption
- Use queues for buffering
- Handle backpressure

**2. Reader-Writer:**
- Multiple readers, single writer
- Optimize for read-heavy workloads
- Use read-write locks

**3. Master-Worker:**
- Master distributes work
- Workers process tasks
- Collect results

### Java Example - Concurrent Programming Patterns:

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class ConcurrentPatternsExample {
    // Producer-Consumer Pattern
    static class ProducerConsumerPattern {
        private final BlockingQueue<Integer> queue = new LinkedBlockingQueue<>(10);
        private final AtomicBoolean running = new AtomicBoolean(true);
        
        public void demonstrateProducerConsumer() throws InterruptedException {
            // Producer
            Thread producer = new Thread(() -> {
                try {
                    for (int i = 1; i <= 20; i++) {
                        queue.put(i);
                        System.out.println("Produced: " + i);
                        Thread.sleep(100);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            // Consumer
            Thread consumer = new Thread(() -> {
                try {
                    while (running.get()) {
                        Integer value = queue.take();
                        System.out.println("Consumed: " + value);
                        Thread.sleep(150);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            producer.start();
            consumer.start();
            
            producer.join();
            running.set(false);
            consumer.join();
        }
    }
    
    // Reader-Writer Pattern
    static class ReaderWriterPattern {
        private final ReadWriteLock lock = new ReentrantReadWriteLock();
        private int sharedData = 0;
        
        public void demonstrateReaderWriter() throws InterruptedException {
            // Writer
            Thread writer = new Thread(() -> {
                for (int i = 1; i <= 5; i++) {
                    lock.writeLock().lock();
                    try {
                        sharedData = i;
                        System.out.println("Writer wrote: " + i);
                        Thread.sleep(200);
                    } finally {
                        lock.writeLock().unlock();
                    }
                }
            });
            
            // Readers
            Thread[] readers = new Thread[3];
            for (int i = 0; i < 3; i++) {
                final int readerId = i;
                readers[i] = new Thread(() -> {
                    for (int j = 0; j < 5; j++) {
                        lock.readLock().lock();
                        try {
                            System.out.println("Reader " + readerId + " read: " + sharedData);
                            Thread.sleep(100);
                        } finally {
                            lock.readLock().unlock();
                        }
                    }
                });
            }
            
            writer.start();
            for (Thread reader : readers) {
                reader.start();
            }
            
            writer.join();
            for (Thread reader : readers) {
                reader.join();
            }
        }
    }
    
    // Master-Worker Pattern
    static class MasterWorkerPattern {
        private final BlockingQueue<Integer> taskQueue = new LinkedBlockingQueue<>();
        private final BlockingQueue<Integer> resultQueue = new LinkedBlockingQueue<>();
        private final AtomicBoolean running = new AtomicBoolean(true);
        
        public void demonstrateMasterWorker() throws InterruptedException {
            // Master
            Thread master = new Thread(() -> {
                try {
                    for (int i = 1; i <= 10; i++) {
                        taskQueue.put(i);
                        System.out.println("Master assigned task: " + i);
                        Thread.sleep(100);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            // Workers
            Thread[] workers = new Thread[3];
            for (int i = 0; i < 3; i++) {
                final int workerId = i;
                workers[i] = new Thread(() -> {
                    try {
                        while (running.get()) {
                            Integer task = taskQueue.take();
                            int result = task * 2; // Simulate work
                            resultQueue.put(result);
                            System.out.println("Worker " + workerId + " completed task " + task + 
                                             " with result " + result);
                            Thread.sleep(150);
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
            }
            
            // Result collector
            Thread collector = new Thread(() -> {
                try {
                    for (int i = 0; i < 10; i++) {
                        Integer result = resultQueue.take();
                        System.out.println("Collected result: " + result);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            master.start();
            for (Thread worker : workers) {
                worker.start();
            }
            collector.start();
            
            master.join();
            running.set(false);
            for (Thread worker : workers) {
                worker.join();
            }
            collector.join();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ConcurrentPatternsExample example = new ConcurrentPatternsExample();
        
        System.out.println("=== Producer-Consumer Pattern ===");
        example.new ProducerConsumerPattern().demonstrateProducerConsumer();
        
        System.out.println("\n=== Reader-Writer Pattern ===");
        example.new ReaderWriterPattern().demonstrateReaderWriter();
        
        System.out.println("\n=== Master-Worker Pattern ===");
        example.new MasterWorkerPattern().demonstrateMasterWorker();
    }
}
```

## 16.10 Concurrency Model Selection

Choosing the right concurrency model depends on the specific requirements of your application. Each model has its strengths and weaknesses.

### Selection Criteria:

**1. Performance Requirements:**
- Throughput needs
- Latency requirements
- Resource constraints

**2. Complexity:**
- Development complexity
- Maintenance overhead
- Debugging difficulty

**3. Scalability:**
- Horizontal scaling
- Vertical scaling
- Load distribution

### Java Example - Concurrency Model Selection:

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.CompletableFuture;

public class ConcurrencyModelSelectionExample {
    public void demonstrateModelSelection() throws Exception {
        // For CPU-intensive tasks - use thread pools
        demonstrateThreadPoolModel();
        
        // For I/O-intensive tasks - use async/await
        demonstrateAsyncModel();
        
        // For simple tasks - use basic threading
        demonstrateBasicThreadingModel();
    }
    
    private void demonstrateThreadPoolModel() throws Exception {
        System.out.println("=== Thread Pool Model (CPU-intensive) ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        long startTime = System.currentTimeMillis();
        
        Future<Integer>[] futures = new Future[10];
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            futures[i] = executor.submit(() -> {
                // CPU-intensive work
                long sum = 0;
                for (int j = 0; j < 1000000; j++) {
                    sum += j;
                }
                return taskId;
            });
        }
        
        for (Future<Integer> future : futures) {
            future.get();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Thread pool completed in " + (endTime - startTime) + "ms");
        
        executor.shutdown();
    }
    
    private void demonstrateAsyncModel() throws Exception {
        System.out.println("\n=== Async Model (I/O-intensive) ===");
        
        long startTime = System.currentTimeMillis();
        
        CompletableFuture<String>[] futures = new CompletableFuture[5];
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            futures[i] = CompletableFuture.supplyAsync(() -> {
                // Simulate I/O work
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                return "Task " + taskId + " completed";
            });
        }
        
        CompletableFuture.allOf(futures).join();
        
        long endTime = System.currentTimeMillis();
        System.out.println("Async model completed in " + (endTime - startTime) + "ms");
    }
    
    private void demonstrateBasicThreadingModel() throws InterruptedException {
        System.out.println("\n=== Basic Threading Model (Simple tasks) ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            threads[i] = new Thread(() -> {
                // Simple work
                System.out.println("Task " + taskId + " completed");
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Basic threading completed in " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws Exception {
        ConcurrencyModelSelectionExample example = new ConcurrencyModelSelectionExample();
        example.demonstrateModelSelection();
    }
}
```

### Real-World Analogy:
Think of concurrency models like different ways to organize a team:

- **Actor Model**: Like having independent workers who only communicate through messages
- **CSP**: Like having workers who pass work through specific channels
- **Dataflow Programming**: Like having an assembly line where work flows through different stations
- **Reactive Programming**: Like having a system that reacts to events as they happen
- **Event-Driven Programming**: Like having a system that responds to specific triggers
- **Message Passing**: Like having workers who communicate by sending notes to each other
- **Shared Memory Model**: Like having workers who share a common workspace
- **Functional Programming**: Like having workers who only work with immutable data
- **Concurrent Programming Patterns**: Like having proven ways to organize teams for specific tasks

The key is to choose the right model for your specific needs and constraints!