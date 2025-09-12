# Section 8 – Reactive Programming

## 8.1 Reactive Streams

Reactive Streams is a specification for asynchronous stream processing with non-blocking backpressure, providing a standard for handling streams of data reactively.

### Key Characteristics
- **Asynchronous**: Non-blocking processing
- **Backpressure**: Flow control to prevent system overload
- **Composable**: Streams can be combined and transformed
- **Standardized**: Cross-platform specification

### Real-World Analogy
Think of a water treatment plant where water flows through different processing stages. The system can handle varying water pressure and can slow down or speed up processing based on demand.

### Java Example
```java
public class ReactiveStreamsExample {
    // Simple reactive stream implementation
    public static class SimpleReactiveStream<T> {
        private final List<Subscriber<T>> subscribers = new ArrayList<>();
        private final ExecutorService executor = Executors.newCachedThreadPool();
        
        public void subscribe(Subscriber<T> subscriber) {
            subscribers.add(subscriber);
            subscriber.onSubscribe(new Subscription() {
                @Override
                public void request(long n) {
                    // Handle backpressure
                }
                
                @Override
                public void cancel() {
                    subscribers.remove(subscriber);
                }
            });
        }
        
        public void publish(T item) {
            for (Subscriber<T> subscriber : subscribers) {
                executor.submit(() -> {
                    try {
                        subscriber.onNext(item);
                    } catch (Exception e) {
                        subscriber.onError(e);
                    }
                });
            }
        }
        
        public void complete() {
            for (Subscriber<T> subscriber : subscribers) {
                executor.submit(() -> subscriber.onComplete());
            }
        }
        
        public void error(Throwable error) {
            for (Subscriber<T> subscriber : subscribers) {
                executor.submit(() -> subscriber.onError(error));
            }
        }
    }
    
    // Subscriber interface
    public interface Subscriber<T> {
        void onSubscribe(Subscription subscription);
        void onNext(T item);
        void onError(Throwable error);
        void onComplete();
    }
    
    // Subscription interface
    public interface Subscription {
        void request(long n);
        void cancel();
    }
    
    // Simple subscriber implementation
    public static class SimpleSubscriber<T> implements Subscriber<T> {
        private final String name;
        private Subscription subscription;
        
        public SimpleSubscriber(String name) {
            this.name = name;
        }
        
        @Override
        public void onSubscribe(Subscription subscription) {
            this.subscription = subscription;
            System.out.println(name + " subscribed");
            subscription.request(1); // Request one item
        }
        
        @Override
        public void onNext(T item) {
            System.out.println(name + " received: " + item);
            if (subscription != null) {
                subscription.request(1); // Request next item
            }
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
    
    public static void demonstrateReactiveStreams() {
        SimpleReactiveStream<String> stream = new SimpleReactiveStream<>();
        
        // Create subscribers
        SimpleSubscriber<String> subscriber1 = new SimpleSubscriber<>("Subscriber1");
        SimpleSubscriber<String> subscriber2 = new SimpleSubscriber<>("Subscriber2");
        
        // Subscribe to stream
        stream.subscribe(subscriber1);
        stream.subscribe(subscriber2);
        
        // Publish items
        stream.publish("Item 1");
        stream.publish("Item 2");
        stream.publish("Item 3");
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        stream.complete();
    }
}
```

## 8.2 Observable Pattern

The Observable pattern is a design pattern where an object (observable) maintains a list of dependents (observers) and notifies them of state changes.

### Key Components
- **Observable**: Object being observed
- **Observer**: Object that receives notifications
- **Notification**: Information about state changes
- **Subscription**: Relationship between observable and observer

### Real-World Analogy
Think of a news channel (observable) that has subscribers (observers). When news breaks, the channel notifies all subscribers about the new information.

### Java Example
```java
public class ObservablePatternExample {
    // Observer interface
    public interface Observer<T> {
        void update(T data);
    }
    
    // Observable interface
    public interface Observable<T> {
        void addObserver(Observer<T> observer);
        void removeObserver(Observer<T> observer);
        void notifyObservers(T data);
    }
    
    // Simple observable implementation
    public static class SimpleObservable<T> implements Observable<T> {
        private final List<Observer<T>> observers = new ArrayList<>();
        
        @Override
        public void addObserver(Observer<T> observer) {
            observers.add(observer);
            System.out.println("Observer added: " + observer.getClass().getSimpleName());
        }
        
        @Override
        public void removeObserver(Observer<T> observer) {
            observers.remove(observer);
            System.out.println("Observer removed: " + observer.getClass().getSimpleName());
        }
        
        @Override
        public void notifyObservers(T data) {
            System.out.println("Notifying " + observers.size() + " observers");
            for (Observer<T> observer : observers) {
                observer.update(data);
            }
        }
    }
    
    // Weather station (observable)
    public static class WeatherStation extends SimpleObservable<WeatherData> {
        private WeatherData currentWeather;
        
        public void setWeather(WeatherData weather) {
            this.currentWeather = weather;
            notifyObservers(weather);
        }
        
        public WeatherData getCurrentWeather() {
            return currentWeather;
        }
    }
    
    // Weather data
    public static class WeatherData {
        private final double temperature;
        private final double humidity;
        private final double pressure;
        
        public WeatherData(double temperature, double humidity, double pressure) {
            this.temperature = temperature;
            this.humidity = humidity;
            this.pressure = pressure;
        }
        
        @Override
        public String toString() {
            return String.format("Weather{temperature=%.1f°C, humidity=%.1f%%, pressure=%.1f hPa}", 
                               temperature, humidity, pressure);
        }
    }
    
    // Weather display (observer)
    public static class WeatherDisplay implements Observer<WeatherData> {
        private final String name;
        
        public WeatherDisplay(String name) {
            this.name = name;
        }
        
        @Override
        public void update(WeatherData data) {
            System.out.println(name + " display updated: " + data);
        }
    }
    
    // Weather alert system (observer)
    public static class WeatherAlertSystem implements Observer<WeatherData> {
        @Override
        public void update(WeatherData data) {
            if (data.temperature > 35) {
                System.out.println("ALERT: High temperature warning!");
            }
            if (data.humidity > 80) {
                System.out.println("ALERT: High humidity warning!");
            }
            if (data.pressure < 1000) {
                System.out.println("ALERT: Low pressure warning!");
            }
        }
    }
    
    public static void demonstrateObservablePattern() {
        WeatherStation station = new WeatherStation();
        
        // Create observers
        WeatherDisplay display1 = new WeatherDisplay("Display 1");
        WeatherDisplay display2 = new WeatherDisplay("Display 2");
        WeatherAlertSystem alertSystem = new WeatherAlertSystem();
        
        // Add observers
        station.addObserver(display1);
        station.addObserver(display2);
        station.addObserver(alertSystem);
        
        // Simulate weather changes
        station.setWeather(new WeatherData(25.0, 60.0, 1013.25));
        station.setWeather(new WeatherData(30.0, 70.0, 1010.50));
        station.setWeather(new WeatherData(38.0, 85.0, 995.75));
        
        // Remove an observer
        station.removeObserver(display2);
        
        // More weather changes
        station.setWeather(new WeatherData(22.0, 50.0, 1020.00));
    }
}
```

## 8.3 Backpressure in Reactive Systems

Backpressure is a mechanism in reactive systems to handle situations where a producer generates data faster than a consumer can process it.

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
    // Backpressure-aware producer
    public static class BackpressureProducer {
        private final BlockingQueue<String> buffer;
        private final int maxBufferSize;
        private final AtomicInteger bufferSize = new AtomicInteger(0);
        private volatile boolean canProduce = true;
        
        public BackpressureProducer(int maxBufferSize) {
            this.maxBufferSize = maxBufferSize;
            this.buffer = new LinkedBlockingQueue<>();
        }
        
        public void produce(String item) {
            if (canProduce && bufferSize.get() < maxBufferSize) {
                buffer.offer(item);
                bufferSize.incrementAndGet();
                System.out.println("Produced: " + item + ", buffer size: " + bufferSize.get());
            } else {
                System.out.println("Backpressure: cannot produce " + item + ", buffer full");
            }
        }
        
        public String consume() {
            String item = buffer.poll();
            if (item != null) {
                bufferSize.decrementAndGet();
                System.out.println("Consumed: " + item + ", buffer size: " + bufferSize.get());
            }
            return item;
        }
        
        public void setCanProduce(boolean canProduce) {
            this.canProduce = canProduce;
        }
        
        public int getBufferSize() {
            return bufferSize.get();
        }
    }
    
    // Backpressure-aware consumer
    public static class BackpressureConsumer {
        private final BackpressureProducer producer;
        private final int processingDelay;
        private final AtomicInteger processedCount = new AtomicInteger(0);
        private final int backpressureThreshold = 5;
        
        public BackpressureConsumer(BackpressureProducer producer, int processingDelay) {
            this.producer = producer;
            this.processingDelay = processingDelay;
        }
        
        public void start() {
            new Thread(() -> {
                while (true) {
                    String item = producer.consume();
                    if (item != null) {
                        processItem(item);
                        
                        // Send backpressure feedback
                        int processed = processedCount.incrementAndGet();
                        boolean canAcceptMore = processed % backpressureThreshold != 0;
                        producer.setCanProduce(canAcceptMore);
                        
                        if (!canAcceptMore) {
                            System.out.println("Backpressure: telling producer to slow down");
                        }
                    } else {
                        try {
                            Thread.sleep(100);
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                            break;
                        }
                    }
                }
            }).start();
        }
        
        private void processItem(String item) {
            System.out.println("Processing: " + item);
            try {
                Thread.sleep(processingDelay);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            System.out.println("Completed: " + item);
        }
    }
    
    public static void demonstrateBackpressure() {
        BackpressureProducer producer = new BackpressureProducer(10);
        BackpressureConsumer consumer = new BackpressureConsumer(producer, 200);
        
        // Start consumer
        consumer.start();
        
        // Produce items
        for (int i = 0; i < 20; i++) {
            producer.produce("Item " + i);
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
    }
}
```

## 8.4 Error Handling in Reactive Code

Error handling in reactive programming requires special consideration because errors can occur at any point in the stream and need to be handled gracefully.

### Key Concepts
- **Error Propagation**: How errors flow through the stream
- **Error Recovery**: Strategies for recovering from errors
- **Error Isolation**: Preventing errors from affecting other parts
- **Error Logging**: Recording errors for debugging

### Real-World Analogy
Think of a production line where if one machine breaks down, the system needs to decide whether to stop the entire line, bypass the broken machine, or try to fix it automatically.

### Java Example
```java
public class ErrorHandlingExample {
    // Reactive stream with error handling
    public static class ErrorHandlingStream<T> {
        private final List<Subscriber<T>> subscribers = new ArrayList<>();
        private final ExecutorService executor = Executors.newCachedThreadPool();
        
        public void subscribe(Subscriber<T> subscriber) {
            subscribers.add(subscriber);
        }
        
        public void publish(T item) {
            for (Subscriber<T> subscriber : subscribers) {
                executor.submit(() -> {
                    try {
                        subscriber.onNext(item);
                    } catch (Exception e) {
                        System.out.println("Error in subscriber: " + e.getMessage());
                        subscriber.onError(e);
                    }
                });
            }
        }
        
        public void error(Throwable error) {
            for (Subscriber<T> subscriber : subscribers) {
                executor.submit(() -> subscriber.onError(error));
            }
        }
        
        public void complete() {
            for (Subscriber<T> subscriber : subscribers) {
                executor.submit(() -> subscriber.onComplete());
            }
        }
    }
    
    // Error-resilient subscriber
    public static class ErrorResilientSubscriber<T> implements Subscriber<T> {
        private final String name;
        private final int maxRetries;
        private final AtomicInteger retryCount = new AtomicInteger(0);
        
        public ErrorResilientSubscriber(String name, int maxRetries) {
            this.name = name;
            this.maxRetries = maxRetries;
        }
        
        @Override
        public void onSubscribe(Subscription subscription) {
            System.out.println(name + " subscribed");
        }
        
        @Override
        public void onNext(T item) {
            try {
                processItem(item);
                retryCount.set(0); // Reset retry count on success
            } catch (Exception e) {
                handleError(e, item);
            }
        }
        
        @Override
        public void onError(Throwable error) {
            System.out.println(name + " received error: " + error.getMessage());
        }
        
        @Override
        public void onComplete() {
            System.out.println(name + " completed");
        }
        
        private void processItem(T item) {
            // Simulate processing that might fail
            if (Math.random() < 0.3) { // 30% chance of failure
                throw new RuntimeException("Processing failed for: " + item);
            }
            
            System.out.println(name + " processed: " + item);
        }
        
        private void handleError(Exception e, T item) {
            int retries = retryCount.incrementAndGet();
            if (retries <= maxRetries) {
                System.out.println(name + " retrying (" + retries + "/" + maxRetries + ") for: " + item);
                try {
                    Thread.sleep(100); // Brief delay before retry
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                }
                onNext(item); // Retry
            } else {
                System.out.println(name + " max retries exceeded for: " + item);
            }
        }
    }
    
    // Circuit breaker pattern for error handling
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
        
        public boolean canExecute() {
            if (isOpen) {
                if (System.currentTimeMillis() - lastFailureTime.get() > timeout) {
                    isOpen = false;
                    failureCount.set(0);
                    System.out.println("Circuit breaker: attempting to close");
                    return true;
                }
                return false;
            }
            return true;
        }
        
        public void recordSuccess() {
            failureCount.set(0);
        }
        
        public void recordFailure() {
            int failures = failureCount.incrementAndGet();
            lastFailureTime.set(System.currentTimeMillis());
            
            if (failures >= failureThreshold) {
                isOpen = true;
                System.out.println("Circuit breaker: opened due to " + failures + " failures");
            }
        }
    }
    
    public static void demonstrateErrorHandling() {
        ErrorHandlingStream<String> stream = new ErrorHandlingStream<>();
        
        // Create error-resilient subscribers
        ErrorResilientSubscriber<String> subscriber1 = new ErrorResilientSubscriber<>("Subscriber1", 3);
        ErrorResilientSubscriber<String> subscriber2 = new ErrorResilientSubscriber<>("Subscriber2", 2);
        
        // Subscribe to stream
        stream.subscribe(subscriber1);
        stream.subscribe(subscriber2);
        
        // Publish items that might cause errors
        for (int i = 0; i < 10; i++) {
            stream.publish("Item " + i);
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
        
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 8.5 Schedulers and Threading

Schedulers in reactive programming control where and when operations are executed, managing the threading model for reactive streams.

### Key Concepts
- **Scheduler**: Controls execution context
- **Threading Models**: Different approaches to thread management
- **Context Switching**: Moving between different execution contexts
- **Resource Management**: Managing thread pools and resources

### Real-World Analogy
Think of a traffic control system that decides which vehicles (operations) can use which roads (threads) and when they can proceed.

### Java Example
```java
public class SchedulersExample {
    // Scheduler interface
    public interface Scheduler {
        void schedule(Runnable task);
        void schedule(Runnable task, long delay, TimeUnit unit);
        void shutdown();
    }
    
    // Thread pool scheduler
    public static class ThreadPoolScheduler implements Scheduler {
        private final ExecutorService executor;
        private final ScheduledExecutorService scheduledExecutor;
        
        public ThreadPoolScheduler(int poolSize) {
            this.executor = Executors.newFixedThreadPool(poolSize);
            this.scheduledExecutor = Executors.newScheduledThreadPool(poolSize);
        }
        
        @Override
        public void schedule(Runnable task) {
            executor.submit(task);
        }
        
        @Override
        public void schedule(Runnable task, long delay, TimeUnit unit) {
            scheduledExecutor.schedule(task, delay, unit);
        }
        
        @Override
        public void shutdown() {
            executor.shutdown();
            scheduledExecutor.shutdown();
        }
    }
    
    // Single thread scheduler
    public static class SingleThreadScheduler implements Scheduler {
        private final ExecutorService executor;
        private final ScheduledExecutorService scheduledExecutor;
        
        public SingleThreadScheduler() {
            this.executor = Executors.newSingleThreadExecutor();
            this.scheduledExecutor = Executors.newSingleThreadScheduledExecutor();
        }
        
        @Override
        public void schedule(Runnable task) {
            executor.submit(task);
        }
        
        @Override
        public void schedule(Runnable task, long delay, TimeUnit unit) {
            scheduledExecutor.schedule(task, delay, unit);
        }
        
        @Override
        public void shutdown() {
            executor.shutdown();
            scheduledExecutor.shutdown();
        }
    }
    
    // Reactive stream with scheduler support
    public static class ScheduledReactiveStream<T> {
        private final List<Subscriber<T>> subscribers = new ArrayList<>();
        private final Scheduler scheduler;
        
        public ScheduledReactiveStream(Scheduler scheduler) {
            this.scheduler = scheduler;
        }
        
        public void subscribe(Subscriber<T> subscriber) {
            subscribers.add(subscriber);
        }
        
        public void publish(T item) {
            for (Subscriber<T> subscriber : subscribers) {
                scheduler.schedule(() -> {
                    try {
                        subscriber.onNext(item);
                    } catch (Exception e) {
                        subscriber.onError(e);
                    }
                });
            }
        }
        
        public void publishDelayed(T item, long delay, TimeUnit unit) {
            for (Subscriber<T> subscriber : subscribers) {
                scheduler.schedule(() -> {
                    try {
                        subscriber.onNext(item);
                    } catch (Exception e) {
                        subscriber.onError(e);
                    }
                }, delay, unit);
            }
        }
        
        public void complete() {
            for (Subscriber<T> subscriber : subscribers) {
                scheduler.schedule(() -> subscriber.onComplete());
            }
        }
    }
    
    // Subscriber that logs thread information
    public static class ThreadAwareSubscriber<T> implements Subscriber<T> {
        private final String name;
        
        public ThreadAwareSubscriber(String name) {
            this.name = name;
        }
        
        @Override
        public void onSubscribe(Subscription subscription) {
            System.out.println(name + " subscribed on thread: " + Thread.currentThread().getName());
        }
        
        @Override
        public void onNext(T item) {
            System.out.println(name + " received " + item + " on thread: " + Thread.currentThread().getName());
        }
        
        @Override
        public void onError(Throwable error) {
            System.out.println(name + " error on thread: " + Thread.currentThread().getName() + " - " + error.getMessage());
        }
        
        @Override
        public void onComplete() {
            System.out.println(name + " completed on thread: " + Thread.currentThread().getName());
        }
    }
    
    public static void demonstrateSchedulers() {
        // Test with thread pool scheduler
        System.out.println("=== Thread Pool Scheduler ===");
        ThreadPoolScheduler threadPoolScheduler = new ThreadPoolScheduler(3);
        ScheduledReactiveStream<String> threadPoolStream = new ScheduledReactiveStream<>(threadPoolScheduler);
        
        ThreadAwareSubscriber<String> subscriber1 = new ThreadAwareSubscriber<>("Subscriber1");
        ThreadAwareSubscriber<String> subscriber2 = new ThreadAwareSubscriber<>("Subscriber2");
        
        threadPoolStream.subscribe(subscriber1);
        threadPoolStream.subscribe(subscriber2);
        
        threadPoolStream.publish("Item 1");
        threadPoolStream.publish("Item 2");
        threadPoolStream.publishDelayed("Delayed Item", 1, TimeUnit.SECONDS);
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        threadPoolScheduler.shutdown();
        
        // Test with single thread scheduler
        System.out.println("\n=== Single Thread Scheduler ===");
        SingleThreadScheduler singleThreadScheduler = new SingleThreadScheduler();
        ScheduledReactiveStream<String> singleThreadStream = new ScheduledReactiveStream<>(singleThreadScheduler);
        
        ThreadAwareSubscriber<String> subscriber3 = new ThreadAwareSubscriber<>("Subscriber3");
        ThreadAwareSubscriber<String> subscriber4 = new ThreadAwareSubscriber<>("Subscriber4");
        
        singleThreadStream.subscribe(subscriber3);
        singleThreadStream.subscribe(subscriber4);
        
        singleThreadStream.publish("Item 3");
        singleThreadStream.publish("Item 4");
        singleThreadStream.publishDelayed("Delayed Item 2", 1, TimeUnit.SECONDS);
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        singleThreadScheduler.shutdown();
    }
}
```

## 8.6 Hot vs Cold Observables

Hot and cold observables represent different ways of handling data streams in reactive programming.

### Key Concepts
- **Cold Observables**: Start producing data when subscribed
- **Hot Observables**: Produce data continuously, regardless of subscribers
- **Subscription Timing**: When data production begins
- **Resource Management**: How resources are managed

### Real-World Analogy
**Cold Observable**: Think of a DVD player that only starts playing when you press play
**Hot Observable**: Think of a live TV broadcast that's always on, whether you're watching or not

### Java Example
```java
public class HotColdObservablesExample {
    // Cold observable - starts producing when subscribed
    public static class ColdObservable<T> {
        private final Supplier<Stream<T>> dataSupplier;
        
        public ColdObservable(Supplier<Stream<T>> dataSupplier) {
            this.dataSupplier = dataSupplier;
        }
        
        public void subscribe(Consumer<T> subscriber) {
            System.out.println("Cold observable: starting data production");
            Stream<T> dataStream = dataSupplier.get();
            dataStream.forEach(subscriber);
            System.out.println("Cold observable: data production completed");
        }
    }
    
    // Hot observable - produces data continuously
    public static class HotObservable<T> {
        private final List<Consumer<T>> subscribers = new ArrayList<>();
        private volatile boolean running = false;
        private Thread producerThread;
        
        public void subscribe(Consumer<T> subscriber) {
            subscribers.add(subscriber);
            System.out.println("Hot observable: subscriber added, total: " + subscribers.size());
        }
        
        public void start() {
            if (!running) {
                running = true;
                producerThread = new Thread(() -> {
                    int counter = 0;
                    while (running) {
                        T data = (T) ("Hot data " + counter++);
                        notifySubscribers(data);
                        
                        try {
                            Thread.sleep(1000);
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                            break;
                        }
                    }
                });
                producerThread.start();
                System.out.println("Hot observable: started producing data");
            }
        }
        
        public void stop() {
            running = false;
            if (producerThread != null) {
                producerThread.interrupt();
            }
            System.out.println("Hot observable: stopped producing data");
        }
        
        private void notifySubscribers(T data) {
            for (Consumer<T> subscriber : subscribers) {
                try {
                    subscriber.accept(data);
                } catch (Exception e) {
                    System.out.println("Error in subscriber: " + e.getMessage());
                }
            }
        }
    }
    
    // Subject - can be both hot and cold
    public static class Subject<T> {
        private final List<Consumer<T>> subscribers = new ArrayList<>();
        private final List<T> dataHistory = new ArrayList<>();
        private volatile boolean completed = false;
        
        public void subscribe(Consumer<T> subscriber) {
            if (completed) {
                System.out.println("Subject: already completed, no new subscribers");
                return;
            }
            
            subscribers.add(subscriber);
            System.out.println("Subject: subscriber added, total: " + subscribers.size());
            
            // Replay history for new subscribers (cold behavior)
            for (T data : dataHistory) {
                subscriber.accept(data);
            }
        }
        
        public void next(T data) {
            if (completed) {
                System.out.println("Subject: already completed, ignoring data");
                return;
            }
            
            dataHistory.add(data);
            System.out.println("Subject: broadcasting data: " + data);
            
            // Notify all subscribers (hot behavior)
            for (Consumer<T> subscriber : subscribers) {
                try {
                    subscriber.accept(data);
                } catch (Exception e) {
                    System.out.println("Error in subscriber: " + e.getMessage());
                }
            }
        }
        
        public void complete() {
            completed = true;
            System.out.println("Subject: completed");
        }
    }
    
    public static void demonstrateHotColdObservables() {
        // Cold observable example
        System.out.println("=== Cold Observable ===");
        ColdObservable<String> coldObservable = new ColdObservable<>(() -> 
            Stream.of("Cold data 1", "Cold data 2", "Cold data 3"));
        
        coldObservable.subscribe(data -> System.out.println("Cold subscriber 1: " + data));
        coldObservable.subscribe(data -> System.out.println("Cold subscriber 2: " + data));
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Hot observable example
        System.out.println("\n=== Hot Observable ===");
        HotObservable<String> hotObservable = new HotObservable<>();
        
        hotObservable.subscribe(data -> System.out.println("Hot subscriber 1: " + data));
        hotObservable.start();
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        hotObservable.subscribe(data -> System.out.println("Hot subscriber 2: " + data));
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        hotObservable.stop();
        
        // Subject example
        System.out.println("\n=== Subject ===");
        Subject<String> subject = new Subject<>();
        
        subject.next("Subject data 1");
        subject.next("Subject data 2");
        
        subject.subscribe(data -> System.out.println("Subject subscriber 1: " + data));
        subject.subscribe(data -> System.out.println("Subject subscriber 2: " + data));
        
        subject.next("Subject data 3");
        subject.next("Subject data 4");
        
        subject.complete();
    }
}
```

## 8.7 Operators and Transformations

Operators in reactive programming allow you to transform, filter, and combine streams of data in various ways.

### Key Concepts
- **Map**: Transform each item in the stream
- **Filter**: Select only certain items
- **Reduce**: Combine items into a single result
- **FlatMap**: Transform and flatten streams
- **Merge**: Combine multiple streams
- **Take/Skip**: Select portions of the stream

### Real-World Analogy
Think of a factory assembly line where raw materials (data) go through various machines (operators) that cut, shape, polish, and assemble them into finished products.

### Java Example
```java
public class OperatorsExample {
    // Reactive stream with operators
    public static class ReactiveStream<T> {
        private final List<Subscriber<T>> subscribers = new ArrayList<>();
        
        public void subscribe(Subscriber<T> subscriber) {
            subscribers.add(subscriber);
        }
        
        public void publish(T item) {
            for (Subscriber<T> subscriber : subscribers) {
                subscriber.onNext(item);
            }
        }
        
        public void complete() {
            for (Subscriber<T> subscriber : subscribers) {
                subscriber.onComplete();
            }
        }
    }
    
    // Map operator
    public static class MapOperator<T, R> implements Subscriber<T> {
        private final Function<T, R> mapper;
        private final Subscriber<R> downstream;
        
        public MapOperator(Function<T, R> mapper, Subscriber<R> downstream) {
            this.mapper = mapper;
            this.downstream = downstream;
        }
        
        @Override
        public void onSubscribe(Subscription subscription) {
            downstream.onSubscribe(subscription);
        }
        
        @Override
        public void onNext(T item) {
            try {
                R mappedItem = mapper.apply(item);
                downstream.onNext(mappedItem);
            } catch (Exception e) {
                downstream.onError(e);
            }
        }
        
        @Override
        public void onError(Throwable error) {
            downstream.onError(error);
        }
        
        @Override
        public void onComplete() {
            downstream.onComplete();
        }
    }
    
    // Filter operator
    public static class FilterOperator<T> implements Subscriber<T> {
        private final Predicate<T> predicate;
        private final Subscriber<T> downstream;
        
        public FilterOperator(Predicate<T> predicate, Subscriber<T> downstream) {
            this.predicate = predicate;
            this.downstream = downstream;
        }
        
        @Override
        public void onSubscribe(Subscription subscription) {
            downstream.onSubscribe(subscription);
        }
        
        @Override
        public void onNext(T item) {
            try {
                if (predicate.test(item)) {
                    downstream.onNext(item);
                }
            } catch (Exception e) {
                downstream.onError(e);
            }
        }
        
        @Override
        public void onError(Throwable error) {
            downstream.onError(error);
        }
        
        @Override
        public void onComplete() {
            downstream.onComplete();
        }
    }
    
    // Take operator
    public static class TakeOperator<T> implements Subscriber<T> {
        private final int count;
        private final Subscriber<T> downstream;
        private int taken = 0;
        
        public TakeOperator(int count, Subscriber<T> downstream) {
            this.count = count;
            this.downstream = downstream;
        }
        
        @Override
        public void onSubscribe(Subscription subscription) {
            downstream.onSubscribe(subscription);
        }
        
        @Override
        public void onNext(T item) {
            if (taken < count) {
                downstream.onNext(item);
                taken++;
            } else {
                downstream.onComplete();
            }
        }
        
        @Override
        public void onError(Throwable error) {
            downstream.onError(error);
        }
        
        @Override
        public void onComplete() {
            downstream.onComplete();
        }
    }
    
    // Simple subscriber for testing
    public static class SimpleSubscriber<T> implements Subscriber<T> {
        private final String name;
        
        public SimpleSubscriber(String name) {
            this.name = name;
        }
        
        @Override
        public void onSubscribe(Subscription subscription) {
            System.out.println(name + " subscribed");
        }
        
        @Override
        public void onNext(T item) {
            System.out.println(name + " received: " + item);
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
    
    public static void demonstrateOperators() {
        ReactiveStream<Integer> stream = new ReactiveStream<>();
        
        // Create a pipeline with operators
        SimpleSubscriber<String> finalSubscriber = new SimpleSubscriber<>("Final");
        TakeOperator<String> takeOp = new TakeOperator<>(3, finalSubscriber);
        FilterOperator<String> filterOp = new FilterOperator<>(s -> s.length() > 5, takeOp);
        MapOperator<Integer, String> mapOp = new MapOperator<>(i -> "Number: " + i, filterOp);
        
        // Connect the pipeline
        stream.subscribe(mapOp);
        
        // Publish data
        for (int i = 1; i <= 10; i++) {
            stream.publish(i);
        }
        
        stream.complete();
    }
}
```

## 8.8 Testing Reactive Code

Testing reactive code requires special techniques to handle asynchronous operations, timing, and stream behavior.

### Key Concepts
- **Asynchronous Testing**: Handling non-blocking operations
- **Timing**: Dealing with delays and timeouts
- **Stream Testing**: Verifying stream behavior
- **Mocking**: Creating test doubles for reactive components

### Real-World Analogy
Think of testing a water treatment plant where you need to verify that water flows through different stages correctly, even though the process takes time and involves multiple components working together.

### Java Example
```java
public class TestingReactiveCodeExample {
    // Testable reactive stream
    public static class TestableReactiveStream<T> {
        private final List<Subscriber<T>> subscribers = new ArrayList<>();
        private final List<T> publishedItems = new ArrayList<>();
        private volatile boolean completed = false;
        private volatile Throwable lastError = null;
        
        public void subscribe(Subscriber<T> subscriber) {
            subscribers.add(subscriber);
        }
        
        public void publish(T item) {
            publishedItems.add(item);
            for (Subscriber<T> subscriber : subscribers) {
                subscriber.onNext(item);
            }
        }
        
        public void complete() {
            completed = true;
            for (Subscriber<T> subscriber : subscribers) {
                subscriber.onComplete();
            }
        }
        
        public void error(Throwable error) {
            lastError = error;
            for (Subscriber<T> subscriber : subscribers) {
                subscriber.onError(error);
            }
        }
        
        // Test helpers
        public List<T> getPublishedItems() {
            return new ArrayList<>(publishedItems);
        }
        
        public boolean isCompleted() {
            return completed;
        }
        
        public Throwable getLastError() {
            return lastError;
        }
        
        public int getSubscriberCount() {
            return subscribers.size();
        }
    }
    
    // Test subscriber that collects all events
    public static class TestSubscriber<T> implements Subscriber<T> {
        private final List<T> receivedItems = new ArrayList<>();
        private final List<Throwable> errors = new ArrayList<>();
        private volatile boolean completed = false;
        private Subscription subscription;
        
        @Override
        public void onSubscribe(Subscription subscription) {
            this.subscription = subscription;
        }
        
        @Override
        public void onNext(T item) {
            receivedItems.add(item);
        }
        
        @Override
        public void onError(Throwable error) {
            errors.add(error);
        }
        
        @Override
        public void onComplete() {
            completed = true;
        }
        
        // Test helpers
        public List<T> getReceivedItems() {
            return new ArrayList<>(receivedItems);
        }
        
        public List<Throwable> getErrors() {
            return new ArrayList<>(errors);
        }
        
        public boolean isCompleted() {
            return completed;
        }
        
        public boolean hasErrors() {
            return !errors.isEmpty();
        }
        
        public void request(long n) {
            if (subscription != null) {
                subscription.request(n);
            }
        }
    }
    
    // Test utilities
    public static class ReactiveTestUtils {
        public static void waitForCompletion(TestSubscriber<?> subscriber, long timeoutMs) {
            long startTime = System.currentTimeMillis();
            while (!subscriber.isCompleted() && !subscriber.hasErrors()) {
                if (System.currentTimeMillis() - startTime > timeoutMs) {
                    throw new AssertionError("Timeout waiting for completion");
                }
                try {
                    Thread.sleep(10);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
        
        public static void waitForItems(TestSubscriber<?> subscriber, int expectedCount, long timeoutMs) {
            long startTime = System.currentTimeMillis();
            while (subscriber.getReceivedItems().size() < expectedCount) {
                if (System.currentTimeMillis() - startTime > timeoutMs) {
                    throw new AssertionError("Timeout waiting for items");
                }
                try {
                    Thread.sleep(10);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
    }
    
    // Test cases
    public static void runTests() {
        System.out.println("Running reactive code tests...");
        
        // Test 1: Basic publishing and subscription
        testBasicPublishing();
        
        // Test 2: Error handling
        testErrorHandling();
        
        // Test 3: Completion
        testCompletion();
        
        // Test 4: Multiple subscribers
        testMultipleSubscribers();
        
        System.out.println("All tests completed!");
    }
    
    private static void testBasicPublishing() {
        System.out.println("\n--- Test: Basic Publishing ---");
        
        TestableReactiveStream<String> stream = new TestableReactiveStream<>();
        TestSubscriber<String> subscriber = new TestSubscriber<>();
        
        stream.subscribe(subscriber);
        
        stream.publish("Item 1");
        stream.publish("Item 2");
        stream.publish("Item 3");
        
        ReactiveTestUtils.waitForItems(subscriber, 3, 1000);
        
        List<String> receivedItems = subscriber.getReceivedItems();
        assert receivedItems.size() == 3 : "Expected 3 items, got " + receivedItems.size();
        assert receivedItems.get(0).equals("Item 1") : "First item mismatch";
        assert receivedItems.get(1).equals("Item 2") : "Second item mismatch";
        assert receivedItems.get(2).equals("Item 3") : "Third item mismatch";
        
        System.out.println("✓ Basic publishing test passed");
    }
    
    private static void testErrorHandling() {
        System.out.println("\n--- Test: Error Handling ---");
        
        TestableReactiveStream<String> stream = new TestableReactiveStream<>();
        TestSubscriber<String> subscriber = new TestSubscriber<>();
        
        stream.subscribe(subscriber);
        
        RuntimeException error = new RuntimeException("Test error");
        stream.error(error);
        
        ReactiveTestUtils.waitForCompletion(subscriber, 1000);
        
        assert subscriber.hasErrors() : "Expected errors";
        assert subscriber.getErrors().get(0) == error : "Error mismatch";
        
        System.out.println("✓ Error handling test passed");
    }
    
    private static void testCompletion() {
        System.out.println("\n--- Test: Completion ---");
        
        TestableReactiveStream<String> stream = new TestableReactiveStream<>();
        TestSubscriber<String> subscriber = new TestSubscriber<>();
        
        stream.subscribe(subscriber);
        
        stream.publish("Item 1");
        stream.complete();
        
        ReactiveTestUtils.waitForCompletion(subscriber, 1000);
        
        assert subscriber.isCompleted() : "Expected completion";
        assert subscriber.getReceivedItems().size() == 1 : "Expected 1 item";
        
        System.out.println("✓ Completion test passed");
    }
    
    private static void testMultipleSubscribers() {
        System.out.println("\n--- Test: Multiple Subscribers ---");
        
        TestableReactiveStream<String> stream = new TestableReactiveStream<>();
        TestSubscriber<String> subscriber1 = new TestSubscriber<>();
        TestSubscriber<String> subscriber2 = new TestSubscriber<>();
        
        stream.subscribe(subscriber1);
        stream.subscribe(subscriber2);
        
        stream.publish("Item 1");
        stream.publish("Item 2");
        
        ReactiveTestUtils.waitForItems(subscriber1, 2, 1000);
        ReactiveTestUtils.waitForItems(subscriber2, 2, 1000);
        
        assert subscriber1.getReceivedItems().size() == 2 : "Subscriber1 expected 2 items";
        assert subscriber2.getReceivedItems().size() == 2 : "Subscriber2 expected 2 items";
        
        System.out.println("✓ Multiple subscribers test passed");
    }
    
    public static void main(String[] args) {
        runTests();
    }
}
```

This comprehensive explanation covers all aspects of reactive programming, providing both theoretical understanding and practical Java examples to illustrate each concept.