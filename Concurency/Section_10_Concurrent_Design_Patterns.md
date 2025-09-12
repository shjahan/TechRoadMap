# Section 10 – Concurrent Design Patterns

## 10.1 Producer-Consumer Pattern

The Producer-Consumer pattern involves one or more threads producing data and one or more threads consuming that data, typically using a shared buffer.

### Key Concepts
- **Producer**: Threads that create data
- **Consumer**: Threads that process data
- **Buffer**: Shared data structure between producers and consumers
- **Synchronization**: Coordinating access to the shared buffer

### Real-World Analogy
Think of a restaurant kitchen where chefs (producers) prepare dishes and place them on a counter, while waiters (consumers) take dishes from the counter to serve customers.

### Java Example
```java
public class ProducerConsumerExample {
    // Shared buffer
    public static class Buffer<T> {
        private final Queue<T> queue = new LinkedBlockingQueue<>();
        private final int maxSize;
        
        public Buffer(int maxSize) {
            this.maxSize = maxSize;
        }
        
        public synchronized void put(T item) throws InterruptedException {
            while (queue.size() >= maxSize) {
                wait();
            }
            queue.offer(item);
            notifyAll();
        }
        
        public synchronized T take() throws InterruptedException {
            while (queue.isEmpty()) {
                wait();
            }
            T item = queue.poll();
            notifyAll();
            return item;
        }
    }
    
    // Producer
    public static class Producer extends Thread {
        private final Buffer<String> buffer;
        private final String name;
        private final int itemCount;
        
        public Producer(Buffer<String> buffer, String name, int itemCount) {
            this.buffer = buffer;
            this.name = name;
            this.itemCount = itemCount;
        }
        
        @Override
        public void run() {
            for (int i = 0; i < itemCount; i++) {
                try {
                    String item = name + "-Item-" + i;
                    buffer.put(item);
                    System.out.println(name + " produced: " + item);
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
    }
    
    // Consumer
    public static class Consumer extends Thread {
        private final Buffer<String> buffer;
        private final String name;
        
        public Consumer(Buffer<String> buffer, String name) {
            this.buffer = buffer;
            this.name = name;
        }
        
        @Override
        public void run() {
            while (true) {
                try {
                    String item = buffer.take();
                    System.out.println(name + " consumed: " + item);
                    Thread.sleep(150);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
    }
    
    public static void demonstrateProducerConsumer() {
        Buffer<String> buffer = new Buffer<>(5);
        
        // Create producers and consumers
        Producer producer1 = new Producer(buffer, "Producer1", 10);
        Producer producer2 = new Producer(buffer, "Producer2", 10);
        Consumer consumer1 = new Consumer(buffer, "Consumer1");
        Consumer consumer2 = new Consumer(buffer, "Consumer2");
        
        // Start all threads
        producer1.start();
        producer2.start();
        consumer1.start();
        consumer2.start();
        
        try {
            producer1.join();
            producer2.join();
            Thread.sleep(2000);
            consumer1.interrupt();
            consumer2.interrupt();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 10.2 Reader-Writer Pattern

The Reader-Writer pattern allows multiple readers to access shared data simultaneously, while writers have exclusive access.

### Key Concepts
- **Readers**: Threads that only read data
- **Writers**: Threads that modify data
- **Read Lock**: Shared lock for readers
- **Write Lock**: Exclusive lock for writers

### Real-World Analogy
Think of a library where multiple people can read books simultaneously, but only one person can write in the library's log book at a time.

### Java Example
```java
public class ReaderWriterExample {
    // Reader-Writer lock
    public static class ReaderWriterLock {
        private int readers = 0;
        private int writers = 0;
        private int writeRequests = 0;
        
        public synchronized void readLock() throws InterruptedException {
            while (writers > 0 || writeRequests > 0) {
                wait();
            }
            readers++;
        }
        
        public synchronized void readUnlock() {
            readers--;
            notifyAll();
        }
        
        public synchronized void writeLock() throws InterruptedException {
            writeRequests++;
            while (readers > 0 || writers > 0) {
                wait();
            }
            writeRequests--;
            writers++;
        }
        
        public synchronized void writeUnlock() {
            writers--;
            notifyAll();
        }
    }
    
    // Shared data
    public static class SharedData {
        private final ReaderWriterLock lock = new ReaderWriterLock();
        private String data = "Initial data";
        private int version = 0;
        
        public String read() throws InterruptedException {
            lock.readLock();
            try {
                Thread.sleep(100); // Simulate reading
                return data + " (version " + version + ")";
            } finally {
                lock.readUnlock();
            }
        }
        
        public void write(String newData) throws InterruptedException {
            lock.writeLock();
            try {
                Thread.sleep(200); // Simulate writing
                this.data = newData;
                this.version++;
            } finally {
                lock.writeUnlock();
            }
        }
    }
    
    // Reader thread
    public static class Reader extends Thread {
        private final SharedData sharedData;
        private final String name;
        
        public Reader(SharedData sharedData, String name) {
            this.sharedData = sharedData;
            this.name = name;
        }
        
        @Override
        public void run() {
            for (int i = 0; i < 5; i++) {
                try {
                    String data = sharedData.read();
                    System.out.println(name + " read: " + data);
                    Thread.sleep(300);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
    }
    
    // Writer thread
    public static class Writer extends Thread {
        private final SharedData sharedData;
        private final String name;
        
        public Writer(SharedData sharedData, String name) {
            this.sharedData = sharedData;
            this.name = name;
        }
        
        @Override
        public void run() {
            for (int i = 0; i < 3; i++) {
                try {
                    String newData = name + "-Data-" + i;
                    sharedData.write(newData);
                    System.out.println(name + " wrote: " + newData);
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
    }
    
    public static void demonstrateReaderWriter() {
        SharedData sharedData = new SharedData();
        
        // Create readers and writers
        Reader reader1 = new Reader(sharedData, "Reader1");
        Reader reader2 = new Reader(sharedData, "Reader2");
        Reader reader3 = new Reader(sharedData, "Reader3");
        Writer writer1 = new Writer(sharedData, "Writer1");
        Writer writer2 = new Writer(sharedData, "Writer2");
        
        // Start all threads
        reader1.start();
        reader2.start();
        reader3.start();
        writer1.start();
        writer2.start();
        
        try {
            reader1.join();
            reader2.join();
            reader3.join();
            writer1.join();
            writer2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 10.3 Master-Worker Pattern

The Master-Worker pattern involves a master thread that distributes work to multiple worker threads and collects their results.

### Key Concepts
- **Master**: Distributes work and collects results
- **Worker**: Processes assigned work
- **Work Queue**: Shared queue of work items
- **Result Collection**: Gathering results from workers

### Real-World Analogy
Think of a construction site where a foreman (master) assigns tasks to different workers and collects their completed work.

### Java Example
```java
public class MasterWorkerExample {
    // Work item
    public static class WorkItem {
        private final int id;
        private final int data;
        
        public WorkItem(int id, int data) {
            this.id = id;
            this.data = data;
        }
        
        public int getId() { return id; }
        public int getData() { return data; }
    }
    
    // Result
    public static class Result {
        private final int workId;
        private final int result;
        
        public Result(int workId, int result) {
            this.workId = workId;
            this.result = result;
        }
        
        public int getWorkId() { return workId; }
        public int getResult() { return result; }
    }
    
    // Master
    public static class Master {
        private final Queue<WorkItem> workQueue = new ConcurrentLinkedQueue<>();
        private final Queue<Result> resultQueue = new ConcurrentLinkedQueue<>();
        private final List<Worker> workers = new ArrayList<>();
        private final int workerCount;
        
        public Master(int workerCount) {
            this.workerCount = workerCount;
        }
        
        public void start() {
            // Create and start workers
            for (int i = 0; i < workerCount; i++) {
                Worker worker = new Worker(workQueue, resultQueue, "Worker" + i);
                workers.add(worker);
                worker.start();
            }
        }
        
        public void submitWork(WorkItem work) {
            workQueue.offer(work);
        }
        
        public Result getResult() {
            return resultQueue.poll();
        }
        
        public void shutdown() {
            for (Worker worker : workers) {
                worker.interrupt();
            }
        }
        
        public boolean hasWork() {
            return !workQueue.isEmpty();
        }
        
        public boolean hasResults() {
            return !resultQueue.isEmpty();
        }
    }
    
    // Worker
    public static class Worker extends Thread {
        private final Queue<WorkItem> workQueue;
        private final Queue<Result> resultQueue;
        private final String name;
        
        public Worker(Queue<WorkItem> workQueue, Queue<Result> resultQueue, String name) {
            this.workQueue = workQueue;
            this.resultQueue = resultQueue;
            this.name = name;
        }
        
        @Override
        public void run() {
            while (!Thread.currentThread().isInterrupted()) {
                WorkItem work = workQueue.poll();
                if (work != null) {
                    // Process work
                    int result = processWork(work);
                    resultQueue.offer(new Result(work.getId(), result));
                    System.out.println(name + " completed work " + work.getId() + " with result " + result);
                } else {
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            }
        }
        
        private int processWork(WorkItem work) {
            // Simulate work processing
            try {
                Thread.sleep(1000 + (int)(Math.random() * 1000));
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return work.getData() * work.getData(); // Square the data
        }
    }
    
    public static void demonstrateMasterWorker() {
        Master master = new Master(3);
        master.start();
        
        // Submit work
        for (int i = 0; i < 10; i++) {
            master.submitWork(new WorkItem(i, i + 1));
        }
        
        // Collect results
        int completedWork = 0;
        while (completedWork < 10) {
            Result result = master.getResult();
            if (result != null) {
                System.out.println("Master received result: Work " + result.getWorkId() + " = " + result.getResult());
                completedWork++;
            } else {
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
        
        master.shutdown();
    }
}
```

## 10.4 Pipeline Pattern

The Pipeline pattern processes data through a series of stages, where each stage performs a specific transformation on the data.

### Key Concepts
- **Stages**: Sequential processing steps
- **Data Flow**: Data passes through stages in order
- **Parallel Processing**: Each stage can process different data simultaneously
- **Buffering**: Data buffering between stages

### Real-World Analogy
Think of an assembly line where a product moves through different stations, each performing a specific operation like cutting, drilling, and painting.

### Java Example
```java
public class PipelineExample {
    // Pipeline stage interface
    public interface PipelineStage<T, R> {
        R process(T input);
    }
    
    // Pipeline
    public static class Pipeline<T> {
        private final List<PipelineStage<?, ?>> stages = new ArrayList<>();
        private final Queue<Object> inputQueue = new ConcurrentLinkedQueue<>();
        private final Queue<Object> outputQueue = new ConcurrentLinkedQueue<>();
        private final List<Thread> stageThreads = new ArrayList<>();
        private volatile boolean running = false;
        
        public <R> Pipeline<T> addStage(PipelineStage<T, R> stage) {
            stages.add(stage);
            return this;
        }
        
        public void start() {
            running = true;
            
            // Create threads for each stage
            for (int i = 0; i < stages.size(); i++) {
                final int stageIndex = i;
                final PipelineStage<?, ?> stage = stages.get(stageIndex);
                
                Thread stageThread = new Thread(() -> {
                    Queue<Object> inputQueue = this.inputQueue;
                    Queue<Object> outputQueue = this.outputQueue;
                    
                    if (stageIndex > 0) {
                        // Use previous stage's output as input
                        inputQueue = new ConcurrentLinkedQueue<>();
                    }
                    
                    while (running) {
                        Object input = inputQueue.poll();
                        if (input != null) {
                            try {
                                Object result = stage.process(input);
                                outputQueue.offer(result);
                                System.out.println("Stage " + stageIndex + " processed: " + input + " -> " + result);
                            } catch (Exception e) {
                                System.err.println("Error in stage " + stageIndex + ": " + e.getMessage());
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
                
                stageThreads.add(stageThread);
                stageThread.start();
            }
        }
        
        public void submit(T input) {
            inputQueue.offer(input);
        }
        
        public Object getResult() {
            return outputQueue.poll();
        }
        
        public void shutdown() {
            running = false;
            for (Thread thread : stageThreads) {
                thread.interrupt();
            }
        }
    }
    
    // Example stages
    public static class StringToIntStage implements PipelineStage<String, Integer> {
        @Override
        public Integer process(String input) {
            try {
                Thread.sleep(100); // Simulate processing
                return Integer.parseInt(input);
            } catch (NumberFormatException e) {
                return 0;
            }
        }
    }
    
    public static class SquareStage implements PipelineStage<Integer, Integer> {
        @Override
        public Integer process(Integer input) {
            try {
                Thread.sleep(100); // Simulate processing
                return input * input;
            } catch (Exception e) {
                return 0;
            }
        }
    }
    
    public static class FormatStage implements PipelineStage<Integer, String> {
        @Override
        public String process(Integer input) {
            try {
                Thread.sleep(100); // Simulate processing
                return "Result: " + input;
            } catch (Exception e) {
                return "Error: " + e.getMessage();
            }
        }
    }
    
    public static void demonstratePipeline() {
        Pipeline<String> pipeline = new Pipeline<>();
        pipeline.addStage(new StringToIntStage())
               .addStage(new SquareStage())
               .addStage(new FormatStage());
        
        pipeline.start();
        
        // Submit work
        pipeline.submit("5");
        pipeline.submit("10");
        pipeline.submit("15");
        
        // Collect results
        int resultCount = 0;
        while (resultCount < 3) {
            Object result = pipeline.getResult();
            if (result != null) {
                System.out.println("Final result: " + result);
                resultCount++;
            } else {
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
        
        pipeline.shutdown();
    }
}
```

## 10.5 Scatter-Gather Pattern

The Scatter-Gather pattern distributes work to multiple workers and then collects and combines their results.

### Key Concepts
- **Scatter**: Distribute work to multiple workers
- **Gather**: Collect results from all workers
- **Combination**: Merge results into final output
- **Synchronization**: Wait for all workers to complete

### Real-World Analogy
Think of a research project where a team leader assigns different research tasks to team members and then combines all their findings into a final report.

### Java Example
```java
public class ScatterGatherExample {
    // Work item
    public static class WorkItem {
        private final int id;
        private final String data;
        
        public WorkItem(int id, String data) {
            this.id = id;
            this.data = data;
        }
        
        public int getId() { return id; }
        public String getData() { return data; }
    }
    
    // Result
    public static class Result {
        private final int workId;
        private final String processedData;
        
        public Result(int workId, String processedData) {
            this.workId = workId;
            this.processedData = processedData;
        }
        
        public int getWorkId() { return workId; }
        public String getProcessedData() { return processedData; }
    }
    
    // Scatter-Gather coordinator
    public static class ScatterGatherCoordinator {
        private final int workerCount;
        private final ExecutorService executor;
        
        public ScatterGatherCoordinator(int workerCount) {
            this.workerCount = workerCount;
            this.executor = Executors.newFixedThreadPool(workerCount);
        }
        
        public List<Result> process(List<WorkItem> workItems) {
            // Scatter work to workers
            List<Future<Result>> futures = new ArrayList<>();
            
            for (WorkItem workItem : workItems) {
                Future<Result> future = executor.submit(() -> processWork(workItem));
                futures.add(future);
            }
            
            // Gather results
            List<Result> results = new ArrayList<>();
            for (Future<Result> future : futures) {
                try {
                    Result result = future.get();
                    results.add(result);
                } catch (InterruptedException | ExecutionException e) {
                    System.err.println("Error processing work: " + e.getMessage());
                }
            }
            
            return results;
        }
        
        private Result processWork(WorkItem workItem) {
            try {
                Thread.sleep(1000 + (int)(Math.random() * 1000));
                String processedData = "Processed: " + workItem.getData().toUpperCase();
                return new Result(workItem.getId(), processedData);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return new Result(workItem.getId(), "Interrupted");
            }
        }
        
        public void shutdown() {
            executor.shutdown();
        }
    }
    
    public static void demonstrateScatterGather() {
        ScatterGatherCoordinator coordinator = new ScatterGatherCoordinator(4);
        
        // Create work items
        List<WorkItem> workItems = new ArrayList<>();
        for (int i = 0; i < 8; i++) {
            workItems.add(new WorkItem(i, "Task " + i));
        }
        
        System.out.println("Starting scatter-gather processing...");
        long startTime = System.currentTimeMillis();
        
        // Process work items
        List<Result> results = coordinator.process(workItems);
        
        long endTime = System.currentTimeMillis();
        System.out.println("Processing completed in " + (endTime - startTime) + "ms");
        
        // Display results
        for (Result result : results) {
            System.out.println("Work " + result.getWorkId() + ": " + result.getProcessedData());
        }
        
        coordinator.shutdown();
    }
}
```

## 10.6 Map-Reduce Pattern

The Map-Reduce pattern processes large datasets by mapping data to key-value pairs and then reducing them to a final result.

### Key Concepts
- **Map**: Transform data into key-value pairs
- **Reduce**: Combine values for each key
- **Partitioning**: Distribute data across workers
- **Shuffling**: Group values by key

### Real-World Analogy
Think of counting votes in an election where you first count votes by district (map) and then sum up the totals for each candidate (reduce).

### Java Example
```java
public class MapReduceExample {
    // Key-value pair
    public static class KeyValue<K, V> {
        private final K key;
        private final V value;
        
        public KeyValue(K key, V value) {
            this.key = key;
            this.value = value;
        }
        
        public K getKey() { return key; }
        public V getValue() { return value; }
    }
    
    // Map-Reduce framework
    public static class MapReduceFramework<K, V, R> {
        private final int workerCount;
        private final ExecutorService executor;
        
        public MapReduceFramework(int workerCount) {
            this.workerCount = workerCount;
            this.executor = Executors.newFixedThreadPool(workerCount);
        }
        
        public Map<K, R> process(List<String> data, 
                                Function<String, List<KeyValue<K, V>>> mapper,
                                Function<List<V>, R> reducer) {
            // Map phase
            List<Future<List<KeyValue<K, V>>>> mapFutures = new ArrayList<>();
            
            for (String item : data) {
                Future<List<KeyValue<K, V>>> future = executor.submit(() -> mapper.apply(item));
                mapFutures.add(future);
            }
            
            // Collect map results
            List<KeyValue<K, V>> mapResults = new ArrayList<>();
            for (Future<List<KeyValue<K, V>>> future : mapFutures) {
                try {
                    mapResults.addAll(future.get());
                } catch (InterruptedException | ExecutionException e) {
                    System.err.println("Error in map phase: " + e.getMessage());
                }
            }
            
            // Group by key
            Map<K, List<V>> groupedData = new HashMap<>();
            for (KeyValue<K, V> kv : mapResults) {
                groupedData.computeIfAbsent(kv.getKey(), k -> new ArrayList<>()).add(kv.getValue());
            }
            
            // Reduce phase
            Map<K, R> results = new HashMap<>();
            for (Map.Entry<K, List<V>> entry : groupedData.entrySet()) {
                K key = entry.getKey();
                List<V> values = entry.getValue();
                R result = reducer.apply(values);
                results.put(key, result);
            }
            
            return results;
        }
        
        public void shutdown() {
            executor.shutdown();
        }
    }
    
    // Word count example
    public static class WordCountMapper implements Function<String, List<KeyValue<String, Integer>>> {
        @Override
        public List<KeyValue<String, Integer>> apply(String text) {
            List<KeyValue<String, Integer>> results = new ArrayList<>();
            String[] words = text.toLowerCase().split("\\W+");
            
            for (String word : words) {
                if (!word.isEmpty()) {
                    results.add(new KeyValue<>(word, 1));
                }
            }
            
            return results;
        }
    }
    
    public static class WordCountReducer implements Function<List<Integer>, Integer> {
        @Override
        public Integer apply(List<Integer> values) {
            return values.stream().mapToInt(Integer::intValue).sum();
        }
    }
    
    public static void demonstrateMapReduce() {
        MapReduceFramework<String, Integer, Integer> framework = new MapReduceFramework<>(4);
        
        // Sample data
        List<String> texts = Arrays.asList(
            "Hello world hello",
            "World hello world",
            "Hello java world",
            "Java world hello"
        );
        
        System.out.println("Processing texts with Map-Reduce...");
        
        // Process data
        Map<String, Integer> wordCounts = framework.process(
            texts,
            new WordCountMapper(),
            new WordCountReducer()
        );
        
        // Display results
        System.out.println("Word counts:");
        for (Map.Entry<String, Integer> entry : wordCounts.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue());
        }
        
        framework.shutdown();
    }
}
```

## 10.7 Fork-Join Pattern

The Fork-Join pattern recursively breaks down work into smaller tasks and then combines their results.

### Key Concepts
- **Fork**: Split work into smaller tasks
- **Join**: Combine results from subtasks
- **Recursive**: Tasks can create subtasks
- **Work Stealing**: Idle threads can steal work from busy threads

### Real-World Analogy
Think of a project manager who breaks down a large project into smaller tasks, assigns them to team members, and then combines their results into the final deliverable.

### Java Example
```java
public class ForkJoinExample {
    // Fork-Join task
    public static class SumTask extends RecursiveTask<Long> {
        private final int[] array;
        private final int start;
        private final int end;
        private final int threshold;
        
        public SumTask(int[] array, int start, int end, int threshold) {
            this.array = array;
            this.start = start;
            this.end = end;
            this.threshold = threshold;
        }
        
        @Override
        protected Long compute() {
            if (end - start <= threshold) {
                // Base case: compute sum directly
                long sum = 0;
                for (int i = start; i < end; i++) {
                    sum += array[i];
                }
                return sum;
            } else {
                // Fork: split into subtasks
                int mid = (start + end) / 2;
                SumTask leftTask = new SumTask(array, start, mid, threshold);
                SumTask rightTask = new SumTask(array, mid, end, threshold);
                
                // Fork both tasks
                leftTask.fork();
                rightTask.fork();
                
                // Join: combine results
                return leftTask.join() + rightTask.join();
            }
        }
    }
    
    // Merge sort using Fork-Join
    public static class MergeSortTask extends RecursiveTask<int[]> {
        private final int[] array;
        private final int start;
        private final int end;
        private final int threshold;
        
        public MergeSortTask(int[] array, int start, int end, int threshold) {
            this.array = array;
            this.start = start;
            this.end = end;
            this.threshold = threshold;
        }
        
        @Override
        protected int[] compute() {
            if (end - start <= threshold) {
                // Base case: sort directly
                int[] result = Arrays.copyOfRange(array, start, end);
                Arrays.sort(result);
                return result;
            } else {
                // Fork: split into subtasks
                int mid = (start + end) / 2;
                MergeSortTask leftTask = new MergeSortTask(array, start, mid, threshold);
                MergeSortTask rightTask = new MergeSortTask(array, mid, end, threshold);
                
                // Fork both tasks
                leftTask.fork();
                rightTask.fork();
                
                // Join: merge results
                int[] leftResult = leftTask.join();
                int[] rightResult = rightTask.join();
                return merge(leftResult, rightResult);
            }
        }
        
        private int[] merge(int[] left, int[] right) {
            int[] result = new int[left.length + right.length];
            int i = 0, j = 0, k = 0;
            
            while (i < left.length && j < right.length) {
                if (left[i] <= right[j]) {
                    result[k++] = left[i++];
                } else {
                    result[k++] = right[j++];
                }
            }
            
            while (i < left.length) {
                result[k++] = left[i++];
            }
            
            while (j < right.length) {
                result[k++] = right[j++];
            }
            
            return result;
        }
    }
    
    public static void demonstrateForkJoin() {
        // Sum example
        System.out.println("=== Fork-Join Sum Example ===");
        int[] numbers = new int[1000000];
        for (int i = 0; i < numbers.length; i++) {
            numbers[i] = i + 1;
        }
        
        ForkJoinPool pool = new ForkJoinPool();
        SumTask sumTask = new SumTask(numbers, 0, numbers.length, 10000);
        
        long startTime = System.currentTimeMillis();
        Long sum = pool.invoke(sumTask);
        long endTime = System.currentTimeMillis();
        
        System.out.println("Sum: " + sum);
        System.out.println("Time: " + (endTime - startTime) + "ms");
        
        // Merge sort example
        System.out.println("\n=== Fork-Join Merge Sort Example ===");
        int[] unsorted = new int[100000];
        for (int i = 0; i < unsorted.length; i++) {
            unsorted[i] = (int)(Math.random() * 1000);
        }
        
        MergeSortTask sortTask = new MergeSortTask(unsorted, 0, unsorted.length, 1000);
        
        startTime = System.currentTimeMillis();
        int[] sorted = pool.invoke(sortTask);
        endTime = System.currentTimeMillis();
        
        System.out.println("Sort completed in " + (endTime - startTime) + "ms");
        System.out.println("First 10 elements: " + Arrays.toString(Arrays.copyOfRange(sorted, 0, 10)));
        
        pool.shutdown();
    }
}
```

## 10.8 Work-Stealing Pattern

The Work-Stealing pattern allows idle threads to steal work from busy threads, improving load balancing and resource utilization.

### Key Concepts
- **Work Stealing**: Idle threads take work from busy threads
- **Load Balancing**: Distribute work evenly across threads
- **Deque**: Double-ended queue for work items
- **Efficiency**: Better utilization of available threads

### Real-World Analogy
Think of a busy restaurant where idle waiters help other waiters who are overwhelmed with orders, ensuring all customers are served efficiently.

### Java Example
```java
public class WorkStealingExample {
    // Work item
    public static class WorkItem {
        private final int id;
        private final int workTime;
        
        public WorkItem(int id, int workTime) {
            this.id = id;
            this.workTime = workTime;
        }
        
        public int getId() { return id; }
        public int getWorkTime() { return workTime; }
    }
    
    // Work-stealing thread pool
    public static class WorkStealingThreadPool {
        private final int threadCount;
        private final List<Deque<WorkItem>> workQueues;
        private final List<Thread> threads;
        private volatile boolean running = false;
        
        public WorkStealingThreadPool(int threadCount) {
            this.threadCount = threadCount;
            this.workQueues = new ArrayList<>();
            this.threads = new ArrayList<>();
            
            for (int i = 0; i < threadCount; i++) {
                workQueues.add(new ConcurrentLinkedDeque<>());
            }
        }
        
        public void start() {
            running = true;
            
            for (int i = 0; i < threadCount; i++) {
                final int threadId = i;
                Thread thread = new Thread(() -> {
                    while (running) {
                        WorkItem work = getWork(threadId);
                        if (work != null) {
                            processWork(threadId, work);
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
                threads.add(thread);
                thread.start();
            }
        }
        
        private WorkItem getWork(int threadId) {
            // Try to get work from own queue first
            Deque<WorkItem> ownQueue = workQueues.get(threadId);
            WorkItem work = ownQueue.pollLast();
            if (work != null) {
                return work;
            }
            
            // Steal work from other queues
            for (int i = 0; i < threadCount; i++) {
                if (i != threadId) {
                    Deque<WorkItem> otherQueue = workQueues.get(i);
                    work = otherQueue.pollFirst();
                    if (work != null) {
                        System.out.println("Thread " + threadId + " stole work " + work.getId() + " from thread " + i);
                        return work;
                    }
                }
            }
            
            return null;
        }
        
        private void processWork(int threadId, WorkItem work) {
            try {
                Thread.sleep(work.getWorkTime());
                System.out.println("Thread " + threadId + " completed work " + work.getId());
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        public void submitWork(WorkItem work) {
            // Submit work to a random queue
            int randomThread = (int)(Math.random() * threadCount);
            workQueues.get(randomThread).offerLast(work);
        }
        
        public void shutdown() {
            running = false;
            for (Thread thread : threads) {
                thread.interrupt();
            }
        }
    }
    
    public static void demonstrateWorkStealing() {
        WorkStealingThreadPool pool = new WorkStealingThreadPool(4);
        pool.start();
        
        // Submit work with varying work times
        for (int i = 0; i < 20; i++) {
            int workTime = 100 + (int)(Math.random() * 500);
            pool.submitWork(new WorkItem(i, workTime));
        }
        
        try {
            Thread.sleep(10000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        pool.shutdown();
    }
}
```

This comprehensive explanation covers all concurrent design patterns, providing both theoretical understanding and practical Java examples to illustrate each concept.