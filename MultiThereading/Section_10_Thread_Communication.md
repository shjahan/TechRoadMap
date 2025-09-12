# Section 10 - Thread Communication

## 10.1 Thread Communication Methods

Thread communication is the mechanism by which threads exchange data and coordinate their activities. There are several methods for threads to communicate, each with its own advantages and use cases.

### Key Communication Methods:

**1. Shared Memory:**
- Threads access shared variables
- Requires synchronization
- Fast but error-prone

**2. Message Passing:**
- Threads send messages to each other
- Explicit communication
- Safer but more overhead

**3. Event-Driven:**
- Threads respond to events
- Decoupled communication
- Reactive programming

### Java Example - Thread Communication Methods:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ThreadCommunicationMethods {
    private final AtomicInteger sharedCounter = new AtomicInteger(0);
    private final BlockingQueue<String> messageQueue = new LinkedBlockingQueue<>();
    private final Object eventLock = new Object();
    private boolean eventOccurred = false;
    
    public void demonstrateCommunicationMethods() throws InterruptedException {
        // Method 1: Shared Memory
        demonstrateSharedMemory();
        
        // Method 2: Message Passing
        demonstrateMessagePassing();
        
        // Method 3: Event-Driven
        demonstrateEventDriven();
    }
    
    private void demonstrateSharedMemory() throws InterruptedException {
        System.out.println("=== Shared Memory Communication ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Writer thread
        executor.submit(() -> {
            for (int i = 0; i < 10; i++) {
                sharedCounter.incrementAndGet();
                System.out.println("Writer: Counter = " + sharedCounter.get());
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Reader threads
        for (int i = 0; i < 2; i++) {
            final int readerId = i;
            executor.submit(() -> {
                for (int j = 0; j < 5; j++) {
                    System.out.println("Reader " + readerId + ": Counter = " + sharedCounter.get());
                    try {
                        Thread.sleep(150);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    private void demonstrateMessagePassing() throws InterruptedException {
        System.out.println("\n=== Message Passing Communication ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Sender thread
        executor.submit(() -> {
            for (int i = 0; i < 10; i++) {
                try {
                    messageQueue.put("Message " + i);
                    System.out.println("Sent: Message " + i);
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Receiver threads
        for (int i = 0; i < 2; i++) {
            final int receiverId = i;
            executor.submit(() -> {
                for (int j = 0; j < 5; j++) {
                    try {
                        String message = messageQueue.take();
                        System.out.println("Receiver " + receiverId + " received: " + message);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    private void demonstrateEventDriven() throws InterruptedException {
        System.out.println("\n=== Event-Driven Communication ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Event generator
        executor.submit(() -> {
            for (int i = 0; i < 5; i++) {
                try {
                    Thread.sleep(1000);
                    synchronized (eventLock) {
                        eventOccurred = true;
                        eventLock.notifyAll();
                    }
                    System.out.println("Event " + i + " generated");
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Event handlers
        for (int i = 0; i < 2; i++) {
            final int handlerId = i;
            executor.submit(() -> {
                for (int j = 0; j < 5; j++) {
                    synchronized (eventLock) {
                        while (!eventOccurred) {
                            try {
                                eventLock.wait();
                            } catch (InterruptedException e) {
                                Thread.currentThread().interrupt();
                                return;
                            }
                        }
                        eventOccurred = false;
                    }
                    System.out.println("Handler " + handlerId + " processed event");
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadCommunicationMethods example = new ThreadCommunicationMethods();
        example.demonstrateCommunicationMethods();
    }
}
```

### Real-World Analogy:
Think of thread communication like different ways people communicate:
- **Shared Memory**: Like a shared whiteboard where everyone can read and write
- **Message Passing**: Like sending emails or text messages
- **Event-Driven**: Like a notification system that alerts people when something happens

## 10.2 Shared Memory Communication

Shared memory communication allows threads to access the same memory locations. It's fast but requires careful synchronization to avoid race conditions.

### Key Concepts:

**1. Memory Sharing:**
- Threads access same variables
- No data copying
- Direct memory access

**2. Synchronization:**
- Prevent race conditions
- Ensure data consistency
- Coordinate access

**3. Visibility:**
- Changes visible to other threads
- Memory barriers
- Cache coherence

### Java Example - Shared Memory Communication:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

public class SharedMemoryCommunication {
    private final AtomicInteger atomicCounter = new AtomicInteger(0);
    private int regularCounter = 0;
    private final ReentrantLock lock = new ReentrantLock();
    
    public void demonstrateSharedMemory() throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        // Atomic operations
        demonstrateAtomicOperations(executor);
        
        // Synchronized access
        demonstrateSynchronizedAccess(executor);
        
        // Lock-based access
        demonstrateLockBasedAccess(executor);
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    private void demonstrateAtomicOperations(ExecutorService executor) throws InterruptedException {
        System.out.println("=== Atomic Operations ===");
        
        for (int i = 0; i < 4; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    atomicCounter.incrementAndGet();
                }
            });
        }
        
        Thread.sleep(2000);
        System.out.println("Atomic counter: " + atomicCounter.get());
    }
    
    private void demonstrateSynchronizedAccess(ExecutorService executor) throws InterruptedException {
        System.out.println("\n=== Synchronized Access ===");
        
        for (int i = 0; i < 4; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    synchronized (this) {
                        regularCounter++;
                    }
                }
            });
        }
        
        Thread.sleep(2000);
        System.out.println("Synchronized counter: " + regularCounter);
    }
    
    private void demonstrateLockBasedAccess(ExecutorService executor) throws InterruptedException {
        System.out.println("\n=== Lock-Based Access ===");
        
        int lockCounter = 0;
        
        for (int i = 0; i < 4; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    lock.lock();
                    try {
                        regularCounter++;
                    } finally {
                        lock.unlock();
                    }
                }
            });
        }
        
        Thread.sleep(2000);
        System.out.println("Lock-based counter: " + regularCounter);
    }
    
    public static void main(String[] args) throws InterruptedException {
        SharedMemoryCommunication example = new SharedMemoryCommunication();
        example.demonstrateSharedMemory();
    }
}
```

## 10.3 Message Passing

Message passing allows threads to communicate by sending and receiving messages. It provides better isolation and safety compared to shared memory.

### Key Concepts:

**1. Message Queues:**
- Thread-safe message storage
- FIFO ordering
- Blocking operations

**2. Asynchronous Communication:**
- Non-blocking message sending
- Callback-based processing
- Event-driven architecture

**3. Synchronous Communication:**
- Blocking message exchange
- Request-response pattern
- Rendezvous communication

### Java Example - Message Passing:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class MessagePassingExample {
    private final BlockingQueue<Message> messageQueue = new LinkedBlockingQueue<>();
    private final AtomicInteger messageId = new AtomicInteger(0);
    
    public void demonstrateMessagePassing() throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        // Asynchronous message passing
        demonstrateAsynchronousMessaging(executor);
        
        // Synchronous message passing
        demonstrateSynchronousMessaging(executor);
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
    }
    
    private void demonstrateAsynchronousMessaging(ExecutorService executor) throws InterruptedException {
        System.out.println("=== Asynchronous Message Passing ===");
        
        // Message sender
        executor.submit(() -> {
            for (int i = 0; i < 10; i++) {
                Message message = new Message(messageId.incrementAndGet(), "Async message " + i);
                try {
                    messageQueue.put(message);
                    System.out.println("Sent: " + message);
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Message receiver
        executor.submit(() -> {
            for (int i = 0; i < 10; i++) {
                try {
                    Message message = messageQueue.take();
                    System.out.println("Received: " + message);
                    Thread.sleep(150);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
    }
    
    private void demonstrateSynchronousMessaging(ExecutorService executor) throws InterruptedException {
        System.out.println("\n=== Synchronous Message Passing ===");
        
        // Request-response pattern
        for (int i = 0; i < 5; i++) {
            final int requestId = i;
            executor.submit(() -> {
                try {
                    // Send request
                    Message request = new Message(requestId, "Request " + requestId);
                    messageQueue.put(request);
                    System.out.println("Sent request: " + request);
                    
                    // Wait for response
                    Message response = messageQueue.take();
                    System.out.println("Received response: " + response);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Response handler
        executor.submit(() -> {
            for (int i = 0; i < 5; i++) {
                try {
                    Message request = messageQueue.take();
                    Thread.sleep(200); // Process request
                    Message response = new Message(request.getId(), "Response to " + request.getContent());
                    messageQueue.put(response);
                    System.out.println("Sent response: " + response);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
    }
    
    private static class Message {
        private final int id;
        private final String content;
        
        public Message(int id, String content) {
            this.id = id;
            this.content = content;
        }
        
        public int getId() { return id; }
        public String getContent() { return content; }
        
        @Override
        public String toString() {
            return "Message{id=" + id + ", content='" + content + "'}";
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        MessagePassingExample example = new MessagePassingExample();
        example.demonstrateMessagePassing();
    }
}
```

## 10.4 Event-Driven Communication

Event-driven communication allows threads to communicate through events. Threads can subscribe to events and react when they occur.

### Key Concepts:

**1. Event System:**
- Central event dispatcher
- Event subscription
- Event publishing

**2. Observer Pattern:**
- Event listeners
- Decoupled communication
- Reactive programming

**3. Event Types:**
- Custom event types
- Event filtering
- Event prioritization

### Java Example - Event-Driven Communication:

```java
import java.util.concurrent.*;
import java.util.*;
import java.util.function.Consumer;

public class EventDrivenCommunication {
    private final Map<String, List<Consumer<Event>>> eventListeners = new ConcurrentHashMap<>();
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    
    public void demonstrateEventDriven() throws InterruptedException {
        // Register event listeners
        registerEventListeners();
        
        // Publish events
        publishEvents();
        
        Thread.sleep(5000);
        executor.shutdown();
    }
    
    private void registerEventListeners() {
        // User events
        subscribe("user.login", event -> 
            System.out.println("User logged in: " + event.getData()));
        subscribe("user.logout", event -> 
            System.out.println("User logged out: " + event.getData()));
        
        // System events
        subscribe("system.startup", event -> 
            System.out.println("System started: " + event.getData()));
        subscribe("system.shutdown", event -> 
            System.out.println("System shutting down: " + event.getData()));
        
        // Error events
        subscribe("error", event -> 
            System.err.println("Error occurred: " + event.getData()));
    }
    
    private void publishEvents() {
        // Publish user events
        executor.submit(() -> {
            try {
                Thread.sleep(1000);
                publish("user.login", "john.doe");
                Thread.sleep(1000);
                publish("user.logout", "john.doe");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Publish system events
        executor.submit(() -> {
            try {
                Thread.sleep(500);
                publish("system.startup", "Application started");
                Thread.sleep(2000);
                publish("system.shutdown", "Application shutting down");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Publish error events
        executor.submit(() -> {
            try {
                Thread.sleep(1500);
                publish("error", "Database connection failed");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
    }
    
    public void subscribe(String eventType, Consumer<Event> listener) {
        eventListeners.computeIfAbsent(eventType, k -> new ArrayList<>()).add(listener);
    }
    
    public void publish(String eventType, Object data) {
        Event event = new Event(eventType, data);
        List<Consumer<Event>> listeners = eventListeners.get(eventType);
        if (listeners != null) {
            listeners.forEach(listener -> 
                executor.submit(() -> listener.accept(event)));
        }
    }
    
    private static class Event {
        private final String type;
        private final Object data;
        private final long timestamp;
        
        public Event(String type, Object data) {
            this.type = type;
            this.data = data;
            this.timestamp = System.currentTimeMillis();
        }
        
        public String getType() { return type; }
        public Object getData() { return data; }
        public long getTimestamp() { return timestamp; }
    }
    
    public static void main(String[] args) throws InterruptedException {
        EventDrivenCommunication example = new EventDrivenCommunication();
        example.demonstrateEventDriven();
    }
}
```

## 10.5 Observer Pattern

The observer pattern allows objects to notify multiple observers about state changes. It's a fundamental pattern for event-driven communication.

### Key Concepts:

**1. Subject:**
- Maintains list of observers
- Notifies observers of changes
- Manages observer lifecycle

**2. Observer:**
- Receives notifications
- Implements update method
- Can subscribe/unsubscribe

**3. Notification:**
- Push notifications
- Pull notifications
- Event data

### Java Example - Observer Pattern:

```java
import java.util.concurrent.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ObserverPatternExample {
    private final AtomicInteger observerId = new AtomicInteger(0);
    
    public void demonstrateObserverPattern() throws InterruptedException {
        // Create subject
        NewsAgency newsAgency = new NewsAgency();
        
        // Create observers
        NewsChannel channel1 = new NewsChannel("Channel 1");
        NewsChannel channel2 = new NewsChannel("Channel 2");
        NewsChannel channel3 = new NewsChannel("Channel 3");
        
        // Subscribe observers
        newsAgency.subscribe(channel1);
        newsAgency.subscribe(channel2);
        newsAgency.subscribe(channel3);
        
        // Publish news
        ExecutorService executor = Executors.newFixedThreadPool(2);
        executor.submit(() -> {
            try {
                for (int i = 0; i < 5; i++) {
                    newsAgency.publishNews("Breaking news " + i);
                    Thread.sleep(1000);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Unsubscribe one observer
        executor.submit(() -> {
            try {
                Thread.sleep(2000);
                newsAgency.unsubscribe(channel2);
                System.out.println("Channel 2 unsubscribed");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        Thread.sleep(6000);
        executor.shutdown();
    }
    
    private static class NewsAgency {
        private final List<NewsChannel> channels = new ArrayList<>();
        private final ExecutorService executor = Executors.newFixedThreadPool(4);
        
        public synchronized void subscribe(NewsChannel channel) {
            channels.add(channel);
            System.out.println("Channel subscribed: " + channel.getName());
        }
        
        public synchronized void unsubscribe(NewsChannel channel) {
            channels.remove(channel);
            System.out.println("Channel unsubscribed: " + channel.getName());
        }
        
        public void publishNews(String news) {
            System.out.println("Publishing news: " + news);
            List<NewsChannel> currentChannels = new ArrayList<>(channels);
            currentChannels.forEach(channel -> 
                executor.submit(() -> channel.update(news)));
        }
    }
    
    private static class NewsChannel {
        private final String name;
        private final List<String> news = new ArrayList<>();
        
        public NewsChannel(String name) {
            this.name = name;
        }
        
        public String getName() { return name; }
        
        public void update(String newsItem) {
            news.add(newsItem);
            System.out.println(name + " received: " + newsItem);
        }
        
        public List<String> getNews() { return new ArrayList<>(news); }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ObserverPatternExample example = new ObserverPatternExample();
        example.demonstrateObserverPattern();
    }
}
```

## 10.6 Command Pattern

The command pattern encapsulates requests as objects, allowing them to be queued, logged, and executed. It's useful for implementing undo/redo functionality and queuing operations.

### Key Concepts:

**1. Command Interface:**
- Execute method
- Undo method
- Command data

**2. Invoker:**
- Executes commands
- Manages command queue
- Handles command history

**3. Receiver:**
- Performs actual work
- Command target
- Business logic

### Java Example - Command Pattern:

```java
import java.util.concurrent.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

public class CommandPatternExample {
    private final AtomicInteger commandId = new AtomicInteger(0);
    
    public void demonstrateCommandPattern() throws InterruptedException {
        // Create receiver
        TextEditor editor = new TextEditor();
        
        // Create invoker
        CommandInvoker invoker = new CommandInvoker();
        
        // Create and execute commands
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        executor.submit(() -> {
            try {
                // Type text
                invoker.execute(new TypeCommand(editor, "Hello "));
                Thread.sleep(100);
                invoker.execute(new TypeCommand(editor, "World!"));
                Thread.sleep(100);
                
                // Delete text
                invoker.execute(new DeleteCommand(editor, 6));
                Thread.sleep(100);
                
                // Undo last command
                invoker.undo();
                Thread.sleep(100);
                
                // Redo command
                invoker.redo();
                Thread.sleep(100);
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        Thread.sleep(2000);
        executor.shutdown();
    }
    
    private static class TextEditor {
        private StringBuilder content = new StringBuilder();
        
        public void type(String text) {
            content.append(text);
            System.out.println("Typed: " + text + " (Content: " + content + ")");
        }
        
        public void delete(int length) {
            if (content.length() >= length) {
                content.setLength(content.length() - length);
                System.out.println("Deleted " + length + " characters (Content: " + content + ")");
            }
        }
        
        public String getContent() { return content.toString(); }
    }
    
    private static class CommandInvoker {
        private final List<Command> history = new ArrayList<>();
        private int currentIndex = -1;
        
        public void execute(Command command) {
            command.execute();
            history.add(command);
            currentIndex++;
        }
        
        public void undo() {
            if (currentIndex >= 0) {
                Command command = history.get(currentIndex);
                command.undo();
                currentIndex--;
            }
        }
        
        public void redo() {
            if (currentIndex < history.size() - 1) {
                currentIndex++;
                Command command = history.get(currentIndex);
                command.execute();
            }
        }
    }
    
    private static abstract class Command {
        protected final TextEditor editor;
        
        public Command(TextEditor editor) {
            this.editor = editor;
        }
        
        public abstract void execute();
        public abstract void undo();
    }
    
    private static class TypeCommand extends Command {
        private final String text;
        
        public TypeCommand(TextEditor editor, String text) {
            super(editor);
            this.text = text;
        }
        
        @Override
        public void execute() {
            editor.type(text);
        }
        
        @Override
        public void undo() {
            editor.delete(text.length());
        }
    }
    
    private static class DeleteCommand extends Command {
        private final int length;
        
        public DeleteCommand(TextEditor editor, int length) {
            super(editor);
            this.length = length;
        }
        
        @Override
        public void execute() {
            editor.delete(length);
        }
        
        @Override
        public void undo() {
            // Cannot undo delete without knowing what was deleted
            System.out.println("Cannot undo delete command");
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        CommandPatternExample example = new CommandPatternExample();
        example.demonstrateCommandPattern();
    }
}
```

## 10.7 Mediator Pattern

The mediator pattern defines how objects interact with each other through a central mediator. It reduces coupling between objects and makes the system easier to maintain.

### Key Concepts:

**1. Mediator:**
- Central communication hub
- Manages object interactions
- Decouples objects

**2. Colleagues:**
- Objects that communicate
- Don't know about each other
- Only know about mediator

**3. Communication:**
- Through mediator
- Event-based
- Decoupled

### Java Example - Mediator Pattern:

```java
import java.util.concurrent.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

public class MediatorPatternExample {
    private final AtomicInteger messageId = new AtomicInteger(0);
    
    public void demonstrateMediatorPattern() throws InterruptedException {
        // Create mediator
        ChatMediator chatMediator = new ChatMediator();
        
        // Create users
        User user1 = new User("Alice", chatMediator);
        User user2 = new User("Bob", chatMediator);
        User user3 = new User("Charlie", chatMediator);
        
        // Register users with mediator
        chatMediator.addUser(user1);
        chatMediator.addUser(user2);
        chatMediator.addUser(user3);
        
        // Simulate chat
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        executor.submit(() -> {
            try {
                user1.sendMessage("Hello everyone!");
                Thread.sleep(1000);
                user1.sendMessage("How are you?");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        executor.submit(() -> {
            try {
                Thread.sleep(500);
                user2.sendMessage("Hi Alice!");
                Thread.sleep(1000);
                user2.sendMessage("I'm doing well, thanks!");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        executor.submit(() -> {
            try {
                Thread.sleep(1000);
                user3.sendMessage("Hello Alice and Bob!");
                Thread.sleep(1000);
                user3.sendMessage("Nice to meet you!");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        Thread.sleep(5000);
        executor.shutdown();
    }
    
    private static class ChatMediator {
        private final List<User> users = new ArrayList<>();
        private final ExecutorService executor = Executors.newFixedThreadPool(4);
        
        public synchronized void addUser(User user) {
            users.add(user);
            System.out.println("User " + user.getName() + " joined the chat");
        }
        
        public void sendMessage(String message, User sender) {
            System.out.println("Mediator received message from " + sender.getName() + ": " + message);
            
            // Send message to all other users
            users.stream()
                .filter(user -> user != sender)
                .forEach(user -> 
                    executor.submit(() -> user.receiveMessage(message, sender.getName())));
        }
    }
    
    private static class User {
        private final String name;
        private final ChatMediator mediator;
        
        public User(String name, ChatMediator mediator) {
            this.name = name;
            this.mediator = mediator;
        }
        
        public String getName() { return name; }
        
        public void sendMessage(String message) {
            mediator.sendMessage(message, this);
        }
        
        public void receiveMessage(String message, String senderName) {
            System.out.println(name + " received from " + senderName + ": " + message);
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        MediatorPatternExample example = new MediatorPatternExample();
        example.demonstrateMediatorPattern();
    }
}
```

## 10.8 Thread Communication Patterns

There are several common patterns for thread communication, each suited for different scenarios and requirements.

### Common Patterns:

**1. Producer-Consumer:**
- One thread produces data
- Another thread consumes data
- Shared buffer for communication

**2. Master-Worker:**
- Master distributes work
- Workers process tasks
- Results collected by master

**3. Pipeline:**
- Data flows through stages
- Each stage processes data
- Sequential processing

### Java Example - Thread Communication Patterns:

```java
import java.util.concurrent.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ThreadCommunicationPatterns {
    private final AtomicInteger taskId = new AtomicInteger(0);
    
    public void demonstratePatterns() throws InterruptedException {
        // Pattern 1: Producer-Consumer
        demonstrateProducerConsumer();
        
        // Pattern 2: Master-Worker
        demonstrateMasterWorker();
        
        // Pattern 3: Pipeline
        demonstratePipeline();
    }
    
    private void demonstrateProducerConsumer() throws InterruptedException {
        System.out.println("=== Producer-Consumer Pattern ===");
        
        BlockingQueue<String> queue = new LinkedBlockingQueue<>(5);
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Producer
        executor.submit(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    String item = "Item-" + i;
                    queue.put(item);
                    System.out.println("Produced: " + item);
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Consumer
        executor.submit(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    String item = queue.take();
                    System.out.println("Consumed: " + item);
                    Thread.sleep(150);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        Thread.sleep(3000);
        executor.shutdown();
    }
    
    private void demonstrateMasterWorker() throws InterruptedException {
        System.out.println("\n=== Master-Worker Pattern ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        List<CompletableFuture<String>> futures = new ArrayList<>();
        
        // Master distributes work
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
                try {
                    Thread.sleep(1000 + taskId * 200);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                return "Result from task " + taskId;
            }, executor);
            futures.add(future);
        }
        
        // Master collects results
        CompletableFuture<Void> allTasks = CompletableFuture.allOf(
            futures.toArray(new CompletableFuture[0])
        );
        
        allTasks.thenRun(() -> {
            System.out.println("All tasks completed");
            futures.forEach(future -> {
                try {
                    System.out.println("Result: " + future.get());
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
        });
        
        allTasks.get();
        executor.shutdown();
    }
    
    private void demonstratePipeline() throws InterruptedException {
        System.out.println("\n=== Pipeline Pattern ===");
        
        BlockingQueue<String> stage1Queue = new LinkedBlockingQueue<>();
        BlockingQueue<String> stage2Queue = new LinkedBlockingQueue<>();
        BlockingQueue<String> stage3Queue = new LinkedBlockingQueue<>();
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        // Stage 1: Input processing
        executor.submit(() -> {
            try {
                for (int i = 0; i < 5; i++) {
                    String item = "Input-" + i;
                    stage1Queue.put(item);
                    System.out.println("Stage 1: " + item);
                    Thread.sleep(200);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Stage 2: Processing
        executor.submit(() -> {
            try {
                for (int i = 0; i < 5; i++) {
                    String item = stage1Queue.take();
                    String processed = item + "-Processed";
                    stage2Queue.put(processed);
                    System.out.println("Stage 2: " + processed);
                    Thread.sleep(300);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Stage 3: Output
        executor.submit(() -> {
            try {
                for (int i = 0; i < 5; i++) {
                    String item = stage2Queue.take();
                    String output = item + "-Output";
                    stage3Queue.put(output);
                    System.out.println("Stage 3: " + output);
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        Thread.sleep(5000);
        executor.shutdown();
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadCommunicationPatterns example = new ThreadCommunicationPatterns();
        example.demonstratePatterns();
    }
}
```

## 10.9 Thread Communication Best Practices

Following best practices ensures efficient, maintainable, and robust thread communication.

### Best Practices:

**1. Choose Appropriate Method:**
- Shared memory for performance
- Message passing for safety
- Events for decoupling

**2. Handle Errors:**
- Exception handling
- Timeout handling
- Graceful degradation

**3. Monitor Performance:**
- Measure communication overhead
- Optimize bottlenecks
- Scale appropriately

### Java Example - Best Practices:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class ThreadCommunicationBestPractices {
    private final AtomicInteger messageCount = new AtomicInteger(0);
    private final AtomicLong totalLatency = new AtomicLong(0);
    private final BlockingQueue<Message> messageQueue = new LinkedBlockingQueue<>();
    
    public void demonstrateBestPractices() throws InterruptedException {
        // Practice 1: Proper error handling
        demonstrateErrorHandling();
        
        // Practice 2: Performance monitoring
        demonstratePerformanceMonitoring();
        
        // Practice 3: Resource management
        demonstrateResourceManagement();
    }
    
    private void demonstrateErrorHandling() throws InterruptedException {
        System.out.println("=== Error Handling ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Message sender with error handling
        executor.submit(() -> {
            for (int i = 0; i < 10; i++) {
                try {
                    Message message = new Message(i, "Message " + i);
                    if (!messageQueue.offer(message, 1, TimeUnit.SECONDS)) {
                        System.err.println("Failed to send message " + i + " - queue full");
                    } else {
                        System.out.println("Sent: " + message);
                    }
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        
        // Message receiver with error handling
        executor.submit(() -> {
            for (int i = 0; i < 10; i++) {
                try {
                    Message message = messageQueue.poll(2, TimeUnit.SECONDS);
                    if (message != null) {
                        System.out.println("Received: " + message);
                    } else {
                        System.err.println("Timeout waiting for message " + i);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        
        Thread.sleep(3000);
        executor.shutdown();
    }
    
    private void demonstratePerformanceMonitoring() throws InterruptedException {
        System.out.println("\n=== Performance Monitoring ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        // Monitor message throughput
        executor.submit(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                try {
                    Thread.sleep(1000);
                    int count = messageCount.get();
                    long latency = totalLatency.get();
                    System.out.println("Messages/sec: " + count + ", Avg latency: " + 
                                     (count > 0 ? latency / count : 0) + "ms");
                    messageCount.set(0);
                    totalLatency.set(0);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        
        // Generate messages
        for (int i = 0; i < 3; i++) {
            final int senderId = i;
            executor.submit(() -> {
                while (!Thread.currentThread().isInterrupted()) {
                    try {
                        long startTime = System.currentTimeMillis();
                        Message message = new Message(senderId, "Performance test");
                        messageQueue.put(message);
                        long latency = System.currentTimeMillis() - startTime;
                        totalLatency.addAndGet(latency);
                        messageCount.incrementAndGet();
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
        }
        
        Thread.sleep(5000);
        executor.shutdown();
    }
    
    private void demonstrateResourceManagement() throws InterruptedException {
        System.out.println("\n=== Resource Management ===");
        
        try (ExecutorService executor = Executors.newFixedThreadPool(2)) {
            // Use try-with-resources for automatic cleanup
            executor.submit(() -> {
                System.out.println("Task running in managed executor");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            executor.awaitTermination(2, TimeUnit.SECONDS);
        } // Executor automatically closed
    }
    
    private static class Message {
        private final int id;
        private final String content;
        private final long timestamp;
        
        public Message(int id, String content) {
            this.id = id;
            this.content = content;
            this.timestamp = System.currentTimeMillis();
        }
        
        public int getId() { return id; }
        public String getContent() { return content; }
        public long getTimestamp() { return timestamp; }
        
        @Override
        public String toString() {
            return "Message{id=" + id + ", content='" + content + "'}";
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadCommunicationBestPractices example = new ThreadCommunicationBestPractices();
        example.demonstrateBestPractices();
    }
}
```

## 10.10 Thread Communication Testing

Testing thread communication requires special techniques to handle the non-deterministic nature of concurrent systems.

### Testing Strategies:

**1. Unit Testing:**
- Test individual components
- Mock dependencies
- Isolate behavior

**2. Integration Testing:**
- Test communication between threads
- Verify message passing
- Check synchronization

**3. Stress Testing:**
- High load testing
- Race condition detection
- Performance validation

### Java Example - Thread Communication Testing:

```java
import java.util.concurrent.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicBoolean;

public class ThreadCommunicationTesting {
    private final AtomicInteger testResults = new AtomicInteger(0);
    private final AtomicBoolean testPassed = new AtomicBoolean(true);
    
    public void demonstrateTesting() throws InterruptedException {
        // Test 1: Basic communication
        testBasicCommunication();
        
        // Test 2: Race condition testing
        testRaceConditions();
        
        // Test 3: Stress testing
        testStressConditions();
        
        // Test 4: Timeout testing
        testTimeoutConditions();
    }
    
    private void testBasicCommunication() throws InterruptedException {
        System.out.println("=== Basic Communication Test ===");
        
        BlockingQueue<String> queue = new LinkedBlockingQueue<>();
        ExecutorService executor = Executors.newFixedThreadPool(2);
        
        // Producer
        executor.submit(() -> {
            try {
                for (int i = 0; i < 5; i++) {
                    queue.put("Test message " + i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Consumer
        executor.submit(() -> {
            try {
                for (int i = 0; i < 5; i++) {
                    String message = queue.take();
                    System.out.println("Received: " + message);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
        
        System.out.println("Basic communication test completed");
    }
    
    private void testRaceConditions() throws InterruptedException {
        System.out.println("\n=== Race Condition Test ===");
        
        AtomicInteger counter = new AtomicInteger(0);
        ExecutorService executor = Executors.newFixedThreadPool(10);
        
        // Multiple threads incrementing counter
        for (int i = 0; i < 100; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 100; j++) {
                    counter.incrementAndGet();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
        
        int expected = 100 * 100;
        int actual = counter.get();
        
        if (actual == expected) {
            System.out.println("Race condition test PASSED: " + actual);
        } else {
            System.out.println("Race condition test FAILED: expected " + expected + ", got " + actual);
            testPassed.set(false);
        }
    }
    
    private void testStressConditions() throws InterruptedException {
        System.out.println("\n=== Stress Test ===");
        
        BlockingQueue<String> queue = new LinkedBlockingQueue<>(1000);
        ExecutorService executor = Executors.newFixedThreadPool(20);
        
        // High load producers
        for (int i = 0; i < 10; i++) {
            final int producerId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < 1000; j++) {
                        queue.put("Producer-" + producerId + "-Message-" + j);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // High load consumers
        for (int i = 0; i < 10; i++) {
            final int consumerId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < 1000; j++) {
                        String message = queue.take();
                        if (j % 100 == 0) {
                            System.out.println("Consumer " + consumerId + " processed: " + message);
                        }
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(30, TimeUnit.SECONDS);
        
        System.out.println("Stress test completed. Queue size: " + queue.size());
    }
    
    private void testTimeoutConditions() throws InterruptedException {
        System.out.println("\n=== Timeout Test ===");
        
        BlockingQueue<String> queue = new LinkedBlockingQueue<>();
        ExecutorService executor = Executors.newFixedThreadPool(2);
        
        // Consumer with timeout
        executor.submit(() -> {
            try {
                String message = queue.poll(2, TimeUnit.SECONDS);
                if (message != null) {
                    System.out.println("Received: " + message);
                } else {
                    System.out.println("Timeout occurred - no message received");
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Delayed producer
        executor.submit(() -> {
            try {
                Thread.sleep(3000); // Longer than timeout
                queue.put("Delayed message");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
        
        System.out.println("Timeout test completed");
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadCommunicationTesting example = new ThreadCommunicationTesting();
        example.demonstrateTesting();
    }
}
```

### Real-World Analogy:
Think of thread communication testing like testing a telephone system:
- **Basic Communication**: Like testing if two people can have a normal conversation
- **Race Conditions**: Like testing what happens when multiple people try to call the same number
- **Stress Testing**: Like testing the system during peak hours with many simultaneous calls
- **Timeout Testing**: Like testing what happens when someone doesn't answer the phone

The key is to test all the edge cases and failure scenarios to ensure your communication system is robust!