# Section 7 – Actor Model and Message Passing

## 7.1 Actor Model Fundamentals

The Actor Model is a mathematical model of concurrent computation where actors are the fundamental units of computation. Actors communicate by sending messages to each other and can create new actors.

### Key Characteristics
- **Actors**: Independent units of computation
- **Messages**: Asynchronous communication between actors
- **Mailboxes**: Each actor has a message queue
- **No Shared State**: Actors don't share memory
- **Location Transparency**: Actors can be local or remote

### Real-World Analogy
Think of a company where each employee (actor) has their own inbox (mailbox) and can send messages to other employees. Employees work independently and only communicate through messages.

### Java Example
```java
public class ActorModelExample {
    // Simple actor interface
    public interface Actor {
        void receive(Object message);
        void start();
        void stop();
    }
    
    // Basic actor implementation
    public static class SimpleActor implements Actor {
        private final String name;
        private final BlockingQueue<Object> mailbox = new LinkedBlockingQueue<>();
        private volatile boolean running = false;
        private Thread actorThread;
        
        public SimpleActor(String name) {
            this.name = name;
        }
        
        @Override
        public void receive(Object message) {
            try {
                mailbox.put(message);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        @Override
        public void start() {
            running = true;
            actorThread = new Thread(() -> {
                while (running) {
                    try {
                        Object message = mailbox.take();
                        handleMessage(message);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
            actorThread.start();
        }
        
        @Override
        public void stop() {
            running = false;
            if (actorThread != null) {
                actorThread.interrupt();
            }
        }
        
        protected void handleMessage(Object message) {
            System.out.println(name + " received: " + message);
        }
    }
    
    // Counter actor
    public static class CounterActor extends SimpleActor {
        private int count = 0;
        
        public CounterActor(String name) {
            super(name);
        }
        
        @Override
        protected void handleMessage(Object message) {
            if (message instanceof String) {
                String cmd = (String) message;
                switch (cmd) {
                    case "increment":
                        count++;
                        System.out.println(getName() + " count: " + count);
                        break;
                    case "decrement":
                        count--;
                        System.out.println(getName() + " count: " + count);
                        break;
                    case "get":
                        System.out.println(getName() + " current count: " + count);
                        break;
                }
            }
        }
        
        public String getName() {
            return "CounterActor";
        }
    }
    
    public static void demonstrateActorModel() {
        CounterActor counter = new CounterActor("Counter1");
        counter.start();
        
        // Send messages to the actor
        counter.receive("increment");
        counter.receive("increment");
        counter.receive("get");
        counter.receive("decrement");
        counter.receive("get");
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        counter.stop();
    }
}
```

## 7.2 Message Passing Concurrency

Message passing concurrency is a paradigm where threads communicate by sending and receiving messages rather than sharing memory.

### Key Concepts
- **Asynchronous**: Messages are sent without waiting for acknowledgment
- **Synchronous**: Messages are sent and the sender waits for a response
- **Buffered**: Messages are stored in queues
- **Unbuffered**: Messages are delivered directly

### Real-World Analogy
Think of a postal system where people send letters to each other. The sender doesn't need to wait for the recipient to read the letter, and the recipient can read letters at their own pace.

### Java Example
```java
public class MessagePassingExample {
    // Message interface
    public interface Message {
        String getType();
        Object getData();
    }
    
    // Simple message implementation
    public static class SimpleMessage implements Message {
        private final String type;
        private final Object data;
        
        public SimpleMessage(String type, Object data) {
            this.type = type;
            this.data = data;
        }
        
        @Override
        public String getType() {
            return type;
        }
        
        @Override
        public Object getData() {
            return data;
        }
    }
    
    // Message passing system
    public static class MessagePassingSystem {
        private final Map<String, BlockingQueue<Message>> mailboxes = new ConcurrentHashMap<>();
        
        public void sendMessage(String recipient, Message message) {
            mailboxes.computeIfAbsent(recipient, k -> new LinkedBlockingQueue<>()).offer(message);
        }
        
        public Message receiveMessage(String recipient) throws InterruptedException {
            BlockingQueue<Message> mailbox = mailboxes.get(recipient);
            if (mailbox == null) {
                return null;
            }
            return mailbox.take();
        }
        
        public Message tryReceiveMessage(String recipient) {
            BlockingQueue<Message> mailbox = mailboxes.get(recipient);
            if (mailbox == null) {
                return null;
            }
            return mailbox.poll();
        }
    }
    
    // Producer actor
    public static class ProducerActor extends Thread {
        private final MessagePassingSystem system;
        private final String name;
        private final int messageCount;
        
        public ProducerActor(MessagePassingSystem system, String name, int messageCount) {
            this.system = system;
            this.name = name;
            this.messageCount = messageCount;
        }
        
        @Override
        public void run() {
            for (int i = 0; i < messageCount; i++) {
                Message message = new SimpleMessage("data", "Message " + i + " from " + name);
                system.sendMessage("consumer", message);
                System.out.println(name + " sent: " + message.getData());
                
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
    }
    
    // Consumer actor
    public static class ConsumerActor extends Thread {
        private final MessagePassingSystem system;
        private final String name;
        private volatile boolean running = true;
        
        public ConsumerActor(MessagePassingSystem system, String name) {
            this.system = system;
            this.name = name;
        }
        
        @Override
        public void run() {
            while (running) {
                try {
                    Message message = system.receiveMessage("consumer");
                    if (message != null) {
                        System.out.println(name + " received: " + message.getData());
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
        
        public void stop() {
            running = false;
        }
    }
    
    public static void demonstrateMessagePassing() {
        MessagePassingSystem system = new MessagePassingSystem();
        
        // Create producer and consumer actors
        ProducerActor producer1 = new ProducerActor(system, "Producer1", 5);
        ProducerActor producer2 = new ProducerActor(system, "Producer2", 5);
        ConsumerActor consumer = new ConsumerActor(system, "Consumer");
        
        // Start actors
        consumer.start();
        producer1.start();
        producer2.start();
        
        try {
            producer1.join();
            producer2.join();
            Thread.sleep(1000); // Let consumer process remaining messages
            consumer.stop();
            consumer.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 7.3 Actor Systems

Actor systems are frameworks that provide infrastructure for managing actors, their lifecycles, and communication.

### Key Components
- **Actor System**: Manages actors and their lifecycles
- **Actor References**: Handles to actors for sending messages
- **Supervision**: Manages actor failures and restarts
- **Scheduling**: Manages actor execution

### Real-World Analogy
Think of a large organization with a management system that handles hiring, firing, communication, and coordination between different departments (actors).

### Java Example
```java
public class ActorSystemExample {
    // Actor system interface
    public interface ActorSystem {
        ActorRef createActor(Class<? extends Actor> actorClass, String name);
        void sendMessage(ActorRef actorRef, Object message);
        void stopActor(ActorRef actorRef);
        void shutdown();
    }
    
    // Actor reference
    public static class ActorRef {
        private final String name;
        private final Actor actor;
        
        public ActorRef(String name, Actor actor) {
            this.name = name;
            this.actor = actor;
        }
        
        public String getName() {
            return name;
        }
        
        public Actor getActor() {
            return actor;
        }
    }
    
    // Simple actor system implementation
    public static class SimpleActorSystem implements ActorSystem {
        private final Map<String, ActorRef> actors = new ConcurrentHashMap<>();
        private final ExecutorService executor = Executors.newCachedThreadPool();
        private volatile boolean running = true;
        
        @Override
        public ActorRef createActor(Class<? extends Actor> actorClass, String name) {
            try {
                Actor actor = actorClass.getDeclaredConstructor(String.class).newInstance(name);
                ActorRef actorRef = new ActorRef(name, actor);
                actors.put(name, actorRef);
                
                // Start actor in executor
                executor.submit(() -> {
                    actor.start();
                    while (running && actors.containsKey(name)) {
                        try {
                            Thread.sleep(100);
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                            break;
                        }
                    }
                });
                
                return actorRef;
            } catch (Exception e) {
                throw new RuntimeException("Failed to create actor", e);
            }
        }
        
        @Override
        public void sendMessage(ActorRef actorRef, Object message) {
            if (actors.containsKey(actorRef.getName())) {
                actorRef.getActor().receive(message);
            }
        }
        
        @Override
        public void stopActor(ActorRef actorRef) {
            if (actors.containsKey(actorRef.getName())) {
                actorRef.getActor().stop();
                actors.remove(actorRef.getName());
            }
        }
        
        @Override
        public void shutdown() {
            running = false;
            actors.values().forEach(actorRef -> actorRef.getActor().stop());
            executor.shutdown();
        }
    }
    
    // Calculator actor
    public static class CalculatorActor extends SimpleActor {
        private double result = 0;
        
        public CalculatorActor(String name) {
            super(name);
        }
        
        @Override
        protected void handleMessage(Object message) {
            if (message instanceof String) {
                String cmd = (String) message;
                String[] parts = cmd.split(" ");
                
                if (parts.length >= 2) {
                    try {
                        double value = Double.parseDouble(parts[1]);
                        
                        switch (parts[0]) {
                            case "add":
                                result += value;
                                System.out.println(getName() + " add " + value + ", result: " + result);
                                break;
                            case "subtract":
                                result -= value;
                                System.out.println(getName() + " subtract " + value + ", result: " + result);
                                break;
                            case "multiply":
                                result *= value;
                                System.out.println(getName() + " multiply " + value + ", result: " + result);
                                break;
                            case "divide":
                                if (value != 0) {
                                    result /= value;
                                    System.out.println(getName() + " divide " + value + ", result: " + result);
                                } else {
                                    System.out.println(getName() + " error: division by zero");
                                }
                                break;
                            case "get":
                                System.out.println(getName() + " current result: " + result);
                                break;
                        }
                    } catch (NumberFormatException e) {
                        System.out.println(getName() + " error: invalid number");
                    }
                }
            }
        }
        
        public String getName() {
            return "CalculatorActor";
        }
    }
    
    public static void demonstrateActorSystem() {
        SimpleActorSystem system = new SimpleActorSystem();
        
        // Create calculator actors
        ActorRef calculator1 = system.createActor(CalculatorActor.class, "Calculator1");
        ActorRef calculator2 = system.createActor(CalculatorActor.class, "Calculator2");
        
        // Send messages to calculators
        system.sendMessage(calculator1, "add 10");
        system.sendMessage(calculator1, "multiply 2");
        system.sendMessage(calculator1, "get");
        
        system.sendMessage(calculator2, "add 5");
        system.sendMessage(calculator2, "add 3");
        system.sendMessage(calculator2, "get");
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        system.shutdown();
    }
}
```

## 7.4 Supervision and Fault Tolerance

Supervision is a key concept in actor systems where actors monitor and manage the lifecycle of other actors, handling failures and ensuring system resilience.

### Key Concepts
- **Supervisor**: Actor that monitors and manages other actors
- **Supervisee**: Actor being monitored
- **Failure Handling**: Strategies for dealing with actor failures
- **Restart Policies**: When and how to restart failed actors

### Real-World Analogy
Think of a manager who oversees a team of workers. When a worker makes a mistake or fails, the manager decides whether to give them another chance, reassign them, or replace them entirely.

### Java Example
```java
public class SupervisionExample {
    // Supervisor interface
    public interface Supervisor {
        void supervise(ActorRef actorRef);
        void handleFailure(ActorRef actorRef, Throwable error);
        void restartActor(ActorRef actorRef);
        void stopActor(ActorRef actorRef);
    }
    
    // Restart policy enum
    public enum RestartPolicy {
        ALWAYS,     // Always restart
        NEVER,      // Never restart
        ON_FAILURE  // Restart only on failure
    }
    
    // Simple supervisor implementation
    public static class SimpleSupervisor implements Supervisor {
        private final Map<ActorRef, RestartPolicy> supervisedActors = new ConcurrentHashMap<>();
        private final Map<ActorRef, Integer> restartCounts = new ConcurrentHashMap<>();
        private final int maxRestarts = 3;
        
        @Override
        public void supervise(ActorRef actorRef) {
            supervisedActors.put(actorRef, RestartPolicy.ON_FAILURE);
            restartCounts.put(actorRef, 0);
        }
        
        @Override
        public void handleFailure(ActorRef actorRef, Throwable error) {
            System.out.println("Supervisor handling failure for " + actorRef.getName() + ": " + error.getMessage());
            
            RestartPolicy policy = supervisedActors.get(actorRef);
            if (policy == RestartPolicy.ALWAYS || policy == RestartPolicy.ON_FAILURE) {
                int restarts = restartCounts.getOrDefault(actorRef, 0);
                if (restarts < maxRestarts) {
                    restartActor(actorRef);
                    restartCounts.put(actorRef, restarts + 1);
                } else {
                    System.out.println("Max restarts reached for " + actorRef.getName() + ", stopping");
                    stopActor(actorRef);
                }
            }
        }
        
        @Override
        public void restartActor(ActorRef actorRef) {
            System.out.println("Restarting actor: " + actorRef.getName());
            actorRef.getActor().stop();
            try {
                Thread.sleep(100); // Brief pause before restart
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            actorRef.getActor().start();
        }
        
        @Override
        public void stopActor(ActorRef actorRef) {
            System.out.println("Stopping actor: " + actorRef.getName());
            actorRef.getActor().stop();
            supervisedActors.remove(actorRef);
            restartCounts.remove(actorRef);
        }
    }
    
    // Faulty actor that can fail
    public static class FaultyActor extends SimpleActor {
        private final double failureRate;
        private int messageCount = 0;
        
        public FaultyActor(String name, double failureRate) {
            super(name);
            this.failureRate = failureRate;
        }
        
        @Override
        protected void handleMessage(Object message) {
            messageCount++;
            System.out.println(getName() + " processing message " + messageCount + ": " + message);
            
            // Simulate random failures
            if (Math.random() < failureRate) {
                throw new RuntimeException("Simulated failure in " + getName());
            }
            
            // Simulate work
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        public String getName() {
            return "FaultyActor";
        }
    }
    
    // Actor system with supervision
    public static class SupervisedActorSystem extends SimpleActorSystem {
        private final Supervisor supervisor;
        
        public SupervisedActorSystem(Supervisor supervisor) {
            this.supervisor = supervisor;
        }
        
        @Override
        public ActorRef createActor(Class<? extends Actor> actorClass, String name) {
            ActorRef actorRef = super.createActor(actorClass, name);
            supervisor.supervise(actorRef);
            return actorRef;
        }
        
        @Override
        public void sendMessage(ActorRef actorRef, Object message) {
            try {
                super.sendMessage(actorRef, message);
            } catch (Exception e) {
                supervisor.handleFailure(actorRef, e);
            }
        }
    }
    
    public static void demonstrateSupervision() {
        SimpleSupervisor supervisor = new SimpleSupervisor();
        SupervisedActorSystem system = new SupervisedActorSystem(supervisor);
        
        // Create faulty actors
        ActorRef faultyActor1 = system.createActor(FaultyActor.class, "FaultyActor1");
        ActorRef faultyActor2 = system.createActor(FaultyActor.class, "FaultyActor2");
        
        // Send messages that might cause failures
        for (int i = 0; i < 10; i++) {
            system.sendMessage(faultyActor1, "Message " + i);
            system.sendMessage(faultyActor2, "Message " + i);
            
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        system.shutdown();
    }
}
```

## 7.5 Actor Hierarchies

Actor hierarchies organize actors in a tree structure where parent actors supervise their children, creating a fault-tolerant system.

### Key Concepts
- **Parent-Child Relationships**: Actors can create and supervise other actors
- **Hierarchical Supervision**: Failures bubble up the hierarchy
- **Lifecycle Management**: Parents control their children's lifecycles
- **Isolation**: Failures in one branch don't affect others

### Real-World Analogy
Think of a corporate hierarchy where managers supervise their direct reports, and failures in one department don't necessarily affect other departments.

### Java Example
```java
public class ActorHierarchyExample {
    // Parent actor that can create children
    public static class ParentActor extends SimpleActor {
        private final Map<String, ActorRef> children = new ConcurrentHashMap<>();
        private final ActorSystem system;
        
        public ParentActor(String name, ActorSystem system) {
            super(name);
            this.system = system;
        }
        
        @Override
        protected void handleMessage(Object message) {
            if (message instanceof String) {
                String cmd = (String) message;
                String[] parts = cmd.split(" ");
                
                switch (parts[0]) {
                    case "createChild":
                        if (parts.length >= 2) {
                            String childName = parts[1];
                            createChild(childName);
                        }
                        break;
                    case "sendToChild":
                        if (parts.length >= 3) {
                            String childName = parts[1];
                            String childMessage = parts[2];
                            sendToChild(childName, childMessage);
                        }
                        break;
                    case "stopChild":
                        if (parts.length >= 2) {
                            String childName = parts[1];
                            stopChild(childName);
                        }
                        break;
                    case "listChildren":
                        listChildren();
                        break;
                }
            }
        }
        
        private void createChild(String childName) {
            ActorRef child = system.createActor(ChildActor.class, childName);
            children.put(childName, child);
            System.out.println(getName() + " created child: " + childName);
        }
        
        private void sendToChild(String childName, String message) {
            ActorRef child = children.get(childName);
            if (child != null) {
                system.sendMessage(child, message);
                System.out.println(getName() + " sent to " + childName + ": " + message);
            } else {
                System.out.println(getName() + " error: child " + childName + " not found");
            }
        }
        
        private void stopChild(String childName) {
            ActorRef child = children.get(childName);
            if (child != null) {
                system.stopActor(child);
                children.remove(childName);
                System.out.println(getName() + " stopped child: " + childName);
            } else {
                System.out.println(getName() + " error: child " + childName + " not found");
            }
        }
        
        private void listChildren() {
            System.out.println(getName() + " children: " + children.keySet());
        }
        
        public String getName() {
            return "ParentActor";
        }
    }
    
    // Child actor
    public static class ChildActor extends SimpleActor {
        private int messageCount = 0;
        
        public ChildActor(String name) {
            super(name);
        }
        
        @Override
        protected void handleMessage(Object message) {
            messageCount++;
            System.out.println(getName() + " received message " + messageCount + ": " + message);
            
            // Simulate work
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        public String getName() {
            return "ChildActor";
        }
    }
    
    public static void demonstrateActorHierarchy() {
        SimpleActorSystem system = new SimpleActorSystem();
        
        // Create parent actor
        ActorRef parent = system.createActor(ParentActor.class, "Parent");
        
        // Send commands to parent
        system.sendMessage(parent, "createChild Child1");
        system.sendMessage(parent, "createChild Child2");
        system.sendMessage(parent, "listChildren");
        
        system.sendMessage(parent, "sendToChild Child1 Hello from parent");
        system.sendMessage(parent, "sendToChild Child2 How are you?");
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        system.sendMessage(parent, "stopChild Child1");
        system.sendMessage(parent, "listChildren");
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        system.shutdown();
    }
}
```

## 7.6 Backpressure Handling

Backpressure is a mechanism to handle situations where a producer is generating data faster than a consumer can process it, preventing system overload.

### Key Concepts
- **Flow Control**: Managing the rate of data flow
- **Buffer Management**: Controlling buffer sizes
- **Drop Strategies**: What to do when buffers are full
- **Feedback Mechanisms**: Informing producers about consumer capacity

### Real-World Analogy
Think of a water system where a pump (producer) is filling a tank (buffer) faster than a faucet (consumer) can drain it. The system needs mechanisms to prevent overflow.

### Java Example
```java
public class BackpressureExample {
    // Message with backpressure information
    public static class BackpressureMessage {
        private final Object data;
        private final boolean canAcceptMore;
        
        public BackpressureMessage(Object data, boolean canAcceptMore) {
            this.data = data;
            this.canAcceptMore = canAcceptMore;
        }
        
        public Object getData() {
            return data;
        }
        
        public boolean canAcceptMore() {
            return canAcceptMore;
        }
    }
    
    // Producer with backpressure handling
    public static class BackpressureProducer extends SimpleActor {
        private final ActorRef consumer;
        private final int maxBufferSize;
        private final AtomicInteger bufferSize = new AtomicInteger(0);
        private volatile boolean canSend = true;
        
        public BackpressureProducer(String name, ActorRef consumer, int maxBufferSize) {
            super(name);
            this.consumer = consumer;
            this.maxBufferSize = maxBufferSize;
        }
        
        @Override
        protected void handleMessage(Object message) {
            if (message instanceof String) {
                String cmd = (String) message;
                
                if ("produce".equals(cmd)) {
                    if (canSend && bufferSize.get() < maxBufferSize) {
                        produceMessage();
                    } else {
                        System.out.println(getName() + " backpressure: cannot produce, buffer full");
                    }
                } else if (message instanceof BackpressureMessage) {
                    BackpressureMessage bpMsg = (BackpressureMessage) message;
                    canSend = bpMsg.canAcceptMore();
                    System.out.println(getName() + " backpressure update: canSend=" + canSend);
                }
            }
        }
        
        private void produceMessage() {
            String data = "Message " + System.currentTimeMillis();
            consumer.receive(data);
            bufferSize.incrementAndGet();
            System.out.println(getName() + " produced: " + data + ", buffer size: " + bufferSize.get());
        }
        
        public String getName() {
            return "BackpressureProducer";
        }
    }
    
    // Consumer with backpressure handling
    public static class BackpressureConsumer extends SimpleActor {
        private final ActorRef producer;
        private final int processingDelay;
        private final AtomicInteger processedCount = new AtomicInteger(0);
        private final int backpressureThreshold = 5;
        
        public BackpressureConsumer(String name, ActorRef producer, int processingDelay) {
            super(name);
            this.producer = producer;
            this.processingDelay = processingDelay;
        }
        
        @Override
        protected void handleMessage(Object message) {
            if (message instanceof String) {
                String data = (String) message;
                processMessage(data);
                
                // Send backpressure feedback
                int processed = processedCount.incrementAndGet();
                boolean canAcceptMore = processed % backpressureThreshold != 0;
                
                BackpressureMessage bpMsg = new BackpressureMessage("feedback", canAcceptMore);
                producer.receive(bpMsg);
            }
        }
        
        private void processMessage(String data) {
            System.out.println(getName() + " processing: " + data);
            
            try {
                Thread.sleep(processingDelay);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            System.out.println(getName() + " completed: " + data);
        }
        
        public String getName() {
            return "BackpressureConsumer";
        }
    }
    
    public static void demonstrateBackpressure() {
        SimpleActorSystem system = new SimpleActorSystem();
        
        // Create consumer first
        ActorRef consumer = system.createActor(BackpressureConsumer.class, "Consumer");
        
        // Create producer with reference to consumer
        ActorRef producer = system.createActor(BackpressureProducer.class, "Producer");
        
        // Send produce commands
        for (int i = 0; i < 20; i++) {
            system.sendMessage(producer, "produce");
            
            try {
                Thread.sleep(50);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
        
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        system.shutdown();
    }
}
```

## 7.7 Actor Communication Patterns

Actor communication patterns define common ways actors interact with each other, including request-reply, publish-subscribe, and pipeline patterns.

### Key Patterns
- **Request-Reply**: Synchronous communication with response
- **Publish-Subscribe**: One-to-many communication
- **Pipeline**: Sequential processing through multiple actors
- **Scatter-Gather**: Distributing work and collecting results

### Real-World Analogy
Think of different communication methods in an organization: direct questions (request-reply), announcements (publish-subscribe), assembly lines (pipeline), and team projects (scatter-gather).

### Java Example
```java
public class ActorCommunicationPatternsExample {
    // Request-reply pattern
    public static class RequestReplyActor extends SimpleActor {
        @Override
        protected void handleMessage(Object message) {
            if (message instanceof String) {
                String request = (String) message;
                String response = "Response to: " + request;
                System.out.println(getName() + " received: " + request);
                System.out.println(getName() + " sending: " + response);
                
                // In a real system, this would send the response back to the sender
                // For simplicity, we'll just print it
            }
        }
        
        public String getName() {
            return "RequestReplyActor";
        }
    }
    
    // Publish-subscribe pattern
    public static class PublisherActor extends SimpleActor {
        private final Set<ActorRef> subscribers = new HashSet<>();
        
        public void subscribe(ActorRef subscriber) {
            subscribers.add(subscriber);
            System.out.println("Subscriber added: " + subscriber.getName());
        }
        
        public void unsubscribe(ActorRef subscriber) {
            subscribers.remove(subscriber);
            System.out.println("Subscriber removed: " + subscriber.getName());
        }
        
        @Override
        protected void handleMessage(Object message) {
            if (message instanceof String) {
                String data = (String) message;
                System.out.println(getName() + " publishing: " + data);
                
                // Notify all subscribers
                for (ActorRef subscriber : subscribers) {
                    subscriber.getActor().receive("Published: " + data);
                }
            }
        }
        
        public String getName() {
            return "PublisherActor";
        }
    }
    
    // Subscriber actor
    public static class SubscriberActor extends SimpleActor {
        private final String name;
        
        public SubscriberActor(String name) {
            super(name);
            this.name = name;
        }
        
        @Override
        protected void handleMessage(Object message) {
            if (message instanceof String) {
                String data = (String) message;
                System.out.println(name + " received: " + data);
            }
        }
        
        public String getName() {
            return name;
        }
    }
    
    // Pipeline pattern
    public static class PipelineStage extends SimpleActor {
        private final String stageName;
        private final ActorRef nextStage;
        
        public PipelineStage(String stageName, ActorRef nextStage) {
            super(stageName);
            this.stageName = stageName;
            this.nextStage = nextStage;
        }
        
        @Override
        protected void handleMessage(Object message) {
            if (message instanceof String) {
                String data = (String) message;
                String processedData = stageName + " processed: " + data;
                System.out.println(stageName + " processing: " + data);
                
                if (nextStage != null) {
                    nextStage.getActor().receive(processedData);
                } else {
                    System.out.println("Pipeline complete: " + processedData);
                }
            }
        }
        
        public String getName() {
            return stageName;
        }
    }
    
    public static void demonstrateCommunicationPatterns() {
        SimpleActorSystem system = new SimpleActorSystem();
        
        // Request-reply pattern
        System.out.println("=== Request-Reply Pattern ===");
        ActorRef requestReplyActor = system.createActor(RequestReplyActor.class, "RequestReplyActor");
        system.sendMessage(requestReplyActor, "Hello, how are you?");
        
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Publish-subscribe pattern
        System.out.println("\n=== Publish-Subscribe Pattern ===");
        ActorRef publisher = system.createActor(PublisherActor.class, "Publisher");
        ActorRef subscriber1 = system.createActor(SubscriberActor.class, "Subscriber1");
        ActorRef subscriber2 = system.createActor(SubscriberActor.class, "Subscriber2");
        
        // Subscribe to publisher
        ((PublisherActor) publisher.getActor()).subscribe(subscriber1);
        ((PublisherActor) publisher.getActor()).subscribe(subscriber2);
        
        // Publish messages
        system.sendMessage(publisher, "Important announcement");
        system.sendMessage(publisher, "System maintenance scheduled");
        
        try {
            Thread.sleep(500);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Pipeline pattern
        System.out.println("\n=== Pipeline Pattern ===");
        ActorRef stage3 = system.createActor(PipelineStage.class, "Stage3");
        ActorRef stage2 = system.createActor(PipelineStage.class, "Stage2");
        ActorRef stage1 = system.createActor(PipelineStage.class, "Stage1");
        
        // Set up pipeline
        ((PipelineStage) stage1.getActor()).nextStage = stage2;
        ((PipelineStage) stage2.getActor()).nextStage = stage3;
        
        // Send data through pipeline
        system.sendMessage(stage1, "Raw data");
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        system.shutdown();
    }
}
```

## 7.8 Distributed Actor Systems

Distributed actor systems extend the actor model to work across multiple machines, enabling scalable and fault-tolerant distributed applications.

### Key Concepts
- **Location Transparency**: Actors can be local or remote
- **Network Communication**: Messages sent over the network
- **Failure Handling**: Network failures and node failures
- **Serialization**: Converting messages for network transmission

### Real-World Analogy
Think of a global company with offices in different countries. Employees can communicate with each other regardless of location, but communication might be slower and less reliable than local communication.

### Java Example
```java
public class DistributedActorSystemExample {
    // Message serialization interface
    public interface MessageSerializer {
        byte[] serialize(Object message);
        Object deserialize(byte[] data);
    }
    
    // Simple message serializer
    public static class SimpleMessageSerializer implements MessageSerializer {
        @Override
        public byte[] serialize(Object message) {
            if (message instanceof String) {
                return ((String) message).getBytes();
            }
            return message.toString().getBytes();
        }
        
        @Override
        public Object deserialize(byte[] data) {
            return new String(data);
        }
    }
    
    // Network message
    public static class NetworkMessage {
        private final String targetActor;
        private final Object data;
        
        public NetworkMessage(String targetActor, Object data) {
            this.targetActor = targetActor;
            this.data = data;
        }
        
        public String getTargetActor() {
            return targetActor;
        }
        
        public Object getData() {
            return data;
        }
    }
    
    // Distributed actor system
    public static class DistributedActorSystem extends SimpleActorSystem {
        private final String nodeId;
        private final MessageSerializer serializer;
        private final Map<String, String> actorLocations = new ConcurrentHashMap<>();
        
        public DistributedActorSystem(String nodeId, MessageSerializer serializer) {
            this.nodeId = nodeId;
            this.serializer = serializer;
        }
        
        public void registerActor(String actorName, String nodeId) {
            actorLocations.put(actorName, nodeId);
        }
        
        public void sendDistributedMessage(String targetActor, Object message) {
            String targetNode = actorLocations.get(targetActor);
            
            if (targetNode == null) {
                System.out.println("Actor " + targetActor + " not found");
                return;
            }
            
            if (targetNode.equals(nodeId)) {
                // Local actor
                ActorRef actorRef = actors.get(targetActor);
                if (actorRef != null) {
                    sendMessage(actorRef, message);
                }
            } else {
                // Remote actor - simulate network communication
                NetworkMessage networkMessage = new NetworkMessage(targetActor, message);
                byte[] serialized = serializer.serialize(networkMessage);
                System.out.println("Sending message to " + targetActor + " on node " + targetNode);
                
                // Simulate network delay
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                // Simulate receiving the message
                receiveDistributedMessage(serialized);
            }
        }
        
        public void receiveDistributedMessage(byte[] data) {
            NetworkMessage networkMessage = (NetworkMessage) serializer.deserialize(data);
            String targetActor = networkMessage.getTargetActor();
            Object message = networkMessage.getData();
            
            ActorRef actorRef = actors.get(targetActor);
            if (actorRef != null) {
                sendMessage(actorRef, message);
            }
        }
    }
    
    // Distributed actor
    public static class DistributedActor extends SimpleActor {
        private final String nodeId;
        
        public DistributedActor(String name, String nodeId) {
            super(name);
            this.nodeId = nodeId;
        }
        
        @Override
        protected void handleMessage(Object message) {
            if (message instanceof String) {
                String data = (String) message;
                System.out.println(getName() + " on node " + nodeId + " received: " + data);
            }
        }
        
        public String getName() {
            return "DistributedActor";
        }
    }
    
    public static void demonstrateDistributedActorSystem() {
        SimpleMessageSerializer serializer = new SimpleMessageSerializer();
        
        // Create distributed actor systems for two nodes
        DistributedActorSystem node1 = new DistributedActorSystem("node1", serializer);
        DistributedActorSystem node2 = new DistributedActorSystem("node2", serializer);
        
        // Create actors on different nodes
        ActorRef actor1 = node1.createActor(DistributedActor.class, "Actor1");
        ActorRef actor2 = node2.createActor(DistributedActor.class, "Actor2");
        
        // Register actor locations
        node1.registerActor("Actor1", "node1");
        node1.registerActor("Actor2", "node2");
        node2.registerActor("Actor1", "node1");
        node2.registerActor("Actor2", "node2");
        
        // Send messages between nodes
        node1.sendDistributedMessage("Actor2", "Hello from node1");
        node2.sendDistributedMessage("Actor1", "Hello from node2");
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        node1.shutdown();
        node2.shutdown();
    }
}
```

This comprehensive explanation covers all aspects of the Actor Model and Message Passing, providing both theoretical understanding and practical Java examples to illustrate each concept.