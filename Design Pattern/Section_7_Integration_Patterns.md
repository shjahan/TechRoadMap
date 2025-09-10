# Section 7 - Integration Patterns

## 7.1 Messaging Patterns

Messaging patterns are fundamental to building distributed systems where different components need to communicate asynchronously. These patterns help decouple systems and enable reliable communication between services.

### What are Messaging Patterns?

Messaging patterns provide structured approaches for communication between different parts of a system. They handle the complexity of sending, receiving, and processing messages in distributed environments.

### Real-World Analogy:
Think of a postal system - you write a letter (message), put it in an envelope with an address (routing), and drop it in a mailbox (message queue). The postal service (message broker) ensures it gets delivered to the right recipient, even if they're not home when it arrives.

### Key Concepts:
- **Message**: A unit of communication containing data and metadata
- **Message Broker**: A system that routes messages between senders and receivers
- **Queue**: A buffer that holds messages until they can be processed
- **Topic**: A channel for broadcasting messages to multiple subscribers

### Basic Implementation:
```java
// Message interface
public interface Message {
    String getId();
    String getType();
    Object getPayload();
    Map<String, String> getHeaders();
    long getTimestamp();
}

// Concrete message implementation
public class OrderMessage implements Message {
    private String id;
    private String type;
    private Order payload;
    private Map<String, String> headers;
    private long timestamp;
    
    public OrderMessage(Order order) {
        this.id = UUID.randomUUID().toString();
        this.type = "ORDER_CREATED";
        this.payload = order;
        this.headers = new HashMap<>();
        this.timestamp = System.currentTimeMillis();
    }
    
    // Getters and setters
    public String getId() { return id; }
    public String getType() { return type; }
    public Object getPayload() { return payload; }
    public Map<String, String> getHeaders() { return headers; }
    public long getTimestamp() { return timestamp; }
}

// Message broker interface
public interface MessageBroker {
    void send(String destination, Message message);
    void subscribe(String destination, MessageHandler handler);
    void unsubscribe(String destination, MessageHandler handler);
}

// Message handler interface
public interface MessageHandler {
    void handle(Message message);
}

// Simple message broker implementation
public class SimpleMessageBroker implements MessageBroker {
    private Map<String, List<MessageHandler>> subscribers = new HashMap<>();
    private Map<String, Queue<Message>> queues = new HashMap<>();
    
    public void send(String destination, Message message) {
        Queue<Message> queue = queues.computeIfAbsent(destination, k -> new LinkedList<>());
        queue.offer(message);
        
        // Notify subscribers
        List<MessageHandler> handlers = subscribers.get(destination);
        if (handlers != null) {
            for (MessageHandler handler : handlers) {
                handler.handle(message);
            }
        }
    }
    
    public void subscribe(String destination, MessageHandler handler) {
        subscribers.computeIfAbsent(destination, k -> new ArrayList<>()).add(handler);
    }
    
    public void unsubscribe(String destination, MessageHandler handler) {
        List<MessageHandler> handlers = subscribers.get(destination);
        if (handlers != null) {
            handlers.remove(handler);
        }
    }
}
```

### Advanced Messaging Features:
```java
// Message with priority
public class PriorityMessage implements Message {
    private Message message;
    private int priority;
    
    public PriorityMessage(Message message, int priority) {
        this.message = message;
        this.priority = priority;
    }
    
    public int getPriority() { return priority; }
    // Delegate other methods to wrapped message
}

// Message broker with priority support
public class PriorityMessageBroker implements MessageBroker {
    private Map<String, PriorityQueue<PriorityMessage>> priorityQueues = new HashMap<>();
    
    public void send(String destination, Message message) {
        send(destination, message, 0);
    }
    
    public void send(String destination, Message message, int priority) {
        PriorityQueue<PriorityMessage> queue = priorityQueues.computeIfAbsent(
            destination, k -> new PriorityQueue<>(Comparator.comparingInt(PriorityMessage::getPriority).reversed())
        );
        queue.offer(new PriorityMessage(message, priority));
    }
}
```

## 7.2 Publish-Subscribe Pattern

The Publish-Subscribe pattern enables one-to-many communication where publishers send messages to topics, and subscribers receive messages from topics they're interested in.

### When to Use:
- When you need to broadcast information to multiple consumers
- When consumers have different interests
- When you want to decouple publishers from subscribers

### Real-World Analogy:
Think of a newspaper subscription system. The newspaper (publisher) publishes articles (messages) to different sections (topics). Subscribers (consumers) can subscribe to specific sections they're interested in, and they'll receive all articles published to those sections.

### Basic Implementation:
```java
// Publisher interface
public interface Publisher {
    void publish(String topic, Message message);
}

// Subscriber interface
public interface Subscriber {
    void onMessage(String topic, Message message);
}

// Topic-based publish-subscribe system
public class TopicBasedPubSub implements Publisher {
    private Map<String, List<Subscriber>> topicSubscribers = new HashMap<>();
    
    public void subscribe(String topic, Subscriber subscriber) {
        topicSubscribers.computeIfAbsent(topic, k -> new ArrayList<>()).add(subscriber);
    }
    
    public void unsubscribe(String topic, Subscriber subscriber) {
        List<Subscriber> subscribers = topicSubscribers.get(topic);
        if (subscribers != null) {
            subscribers.remove(subscriber);
        }
    }
    
    public void publish(String topic, Message message) {
        List<Subscriber> subscribers = topicSubscribers.get(topic);
        if (subscribers != null) {
            for (Subscriber subscriber : subscribers) {
                try {
                    subscriber.onMessage(topic, message);
                } catch (Exception e) {
                    // Handle subscriber errors
                    System.err.println("Error notifying subscriber: " + e.getMessage());
                }
            }
        }
    }
}

// Example usage
public class NewsPublisher implements Publisher {
    private TopicBasedPubSub pubSub;
    
    public NewsPublisher(TopicBasedPubSub pubSub) {
        this.pubSub = pubSub;
    }
    
    public void publishNews(String category, String headline, String content) {
        NewsMessage message = new NewsMessage(headline, content);
        pubSub.publish(category, message);
    }
}

public class NewsSubscriber implements Subscriber {
    private String name;
    private Set<String> subscribedTopics;
    
    public NewsSubscriber(String name) {
        this.name = name;
        this.subscribedTopics = new HashSet<>();
    }
    
    public void subscribeTo(String topic) {
        subscribedTopics.add(topic);
    }
    
    public void onMessage(String topic, Message message) {
        if (subscribedTopics.contains(topic)) {
            System.out.println(name + " received " + topic + " news: " + message.getPayload());
        }
    }
}
```

### Advanced Publish-Subscribe Features:
```java
// Wildcard subscription support
public class WildcardPubSub extends TopicBasedPubSub {
    public void subscribeWithWildcard(String pattern, Subscriber subscriber) {
        // Support patterns like "sports.*" or "news.*.politics"
        // Implementation would use pattern matching
    }
}

// Message filtering
public class FilteredSubscriber implements Subscriber {
    private Subscriber delegate;
    private Predicate<Message> filter;
    
    public FilteredSubscriber(Subscriber delegate, Predicate<Message> filter) {
        this.delegate = delegate;
        this.filter = filter;
    }
    
    public void onMessage(String topic, Message message) {
        if (filter.test(message)) {
            delegate.onMessage(topic, message);
        }
    }
}
```

## 7.3 Message Queue Pattern

The Message Queue pattern provides asynchronous communication using queues to store messages until they can be processed by consumers.

### When to Use:
- When you need reliable message delivery
- When processing can be asynchronous
- When you need to handle varying loads

### Real-World Analogy:
Think of a restaurant kitchen. Orders (messages) are placed on a ticket rail (queue) and chefs (consumers) process them one by one. If a chef is busy, orders wait in the queue until they can be processed.

### Basic Implementation:
```java
// Message queue interface
public interface MessageQueue<T> {
    void enqueue(T message);
    T dequeue() throws InterruptedException;
    boolean isEmpty();
    int size();
}

// Simple message queue implementation
public class SimpleMessageQueue<T> implements MessageQueue<T> {
    private Queue<T> queue = new LinkedList<>();
    private final Object lock = new Object();
    
    public void enqueue(T message) {
        synchronized (lock) {
            queue.offer(message);
            lock.notifyAll();
        }
    }
    
    public T dequeue() throws InterruptedException {
        synchronized (lock) {
            while (queue.isEmpty()) {
                lock.wait();
            }
            return queue.poll();
        }
    }
    
    public boolean isEmpty() {
        synchronized (lock) {
            return queue.isEmpty();
        }
    }
    
    public int size() {
        synchronized (lock) {
            return queue.size();
        }
    }
}

// Message processor
public class MessageProcessor<T> {
    private MessageQueue<T> queue;
    private MessageHandler<T> handler;
    private boolean running = false;
    private Thread processorThread;
    
    public MessageProcessor(MessageQueue<T> queue, MessageHandler<T> handler) {
        this.queue = queue;
        this.handler = handler;
    }
    
    public void start() {
        running = true;
        processorThread = new Thread(this::processMessages);
        processorThread.start();
    }
    
    public void stop() {
        running = false;
        if (processorThread != null) {
            processorThread.interrupt();
        }
    }
    
    private void processMessages() {
        while (running) {
            try {
                T message = queue.dequeue();
                handler.handle(message);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            } catch (Exception e) {
                System.err.println("Error processing message: " + e.getMessage());
            }
        }
    }
}

// Message handler interface
public interface MessageHandler<T> {
    void handle(T message);
}
```

### Advanced Queue Features:
```java
// Priority message queue
public class PriorityMessageQueue<T> implements MessageQueue<T> {
    private PriorityQueue<PriorityMessage<T>> queue = new PriorityQueue<>();
    private final Object lock = new Object();
    
    public void enqueue(T message) {
        enqueue(message, 0);
    }
    
    public void enqueue(T message, int priority) {
        synchronized (lock) {
            queue.offer(new PriorityMessage<>(message, priority));
            lock.notifyAll();
        }
    }
    
    public T dequeue() throws InterruptedException {
        synchronized (lock) {
            while (queue.isEmpty()) {
                lock.wait();
            }
            return queue.poll().getMessage();
        }
    }
    
    // Other methods...
}

// Bounded message queue
public class BoundedMessageQueue<T> implements MessageQueue<T> {
    private Queue<T> queue;
    private int maxSize;
    private final Object lock = new Object();
    
    public BoundedMessageQueue(int maxSize) {
        this.maxSize = maxSize;
        this.queue = new LinkedList<>();
    }
    
    public void enqueue(T message) throws InterruptedException {
        synchronized (lock) {
            while (queue.size() >= maxSize) {
                lock.wait();
            }
            queue.offer(message);
            lock.notifyAll();
        }
    }
    
    public T dequeue() throws InterruptedException {
        synchronized (lock) {
            while (queue.isEmpty()) {
                lock.wait();
            }
            T message = queue.poll();
            lock.notifyAll(); // Notify waiting enqueuers
            return message;
        }
    }
    
    // Other methods...
}
```

## 7.4 Request-Reply Pattern

The Request-Reply pattern enables synchronous communication where a client sends a request and waits for a response from the server.

### When to Use:
- When you need immediate response
- When the operation must complete before continuing
- When you need to handle errors synchronously

### Real-World Analogy:
Think of asking a question in a meeting. You raise your hand (send request), wait for the speaker to acknowledge you, ask your question, and wait for an answer (reply) before continuing.

### Basic Implementation:
```java
// Request interface
public interface Request {
    String getId();
    String getType();
    Object getPayload();
}

// Reply interface
public interface Reply {
    String getRequestId();
    boolean isSuccess();
    Object getResult();
    String getErrorMessage();
}

// Request-reply client
public class RequestReplyClient {
    private MessageBroker messageBroker;
    private Map<String, CompletableFuture<Reply>> pendingRequests = new HashMap<>();
    
    public RequestReplyClient(MessageBroker messageBroker) {
        this.messageBroker = messageBroker;
        // Subscribe to replies
        messageBroker.subscribe("replies", this::handleReply);
    }
    
    public CompletableFuture<Reply> sendRequest(String serverQueue, Request request) {
        CompletableFuture<Reply> future = new CompletableFuture<>();
        pendingRequests.put(request.getId(), future);
        
        // Send request
        messageBroker.send(serverQueue, request);
        
        // Set timeout
        CompletableFuture.delayedExecutor(30, TimeUnit.SECONDS)
            .execute(() -> {
                if (pendingRequests.remove(request.getId()) != null) {
                    future.completeExceptionally(new TimeoutException("Request timeout"));
                }
            });
        
        return future;
    }
    
    private void handleReply(Message message) {
        if (message.getPayload() instanceof Reply) {
            Reply reply = (Reply) message.getPayload();
            CompletableFuture<Reply> future = pendingRequests.remove(reply.getRequestId());
            if (future != null) {
                future.complete(reply);
            }
        }
    }
}

// Request-reply server
public class RequestReplyServer {
    private MessageBroker messageBroker;
    private String requestQueue;
    private RequestHandler requestHandler;
    
    public RequestReplyServer(MessageBroker messageBroker, String requestQueue, RequestHandler requestHandler) {
        this.messageBroker = messageBroker;
        this.requestQueue = requestQueue;
        this.requestHandler = requestHandler;
        
        // Subscribe to requests
        messageBroker.subscribe(requestQueue, this::handleRequest);
    }
    
    private void handleRequest(Message message) {
        if (message.getPayload() instanceof Request) {
            Request request = (Request) message.getPayload();
            
            try {
                // Process request
                Object result = requestHandler.handle(request);
                
                // Send reply
                Reply reply = new SuccessReply(request.getId(), result);
                messageBroker.send("replies", reply);
                
            } catch (Exception e) {
                // Send error reply
                Reply reply = new ErrorReply(request.getId(), e.getMessage());
                messageBroker.send("replies", reply);
            }
        }
    }
}

// Request handler interface
public interface RequestHandler {
    Object handle(Request request) throws Exception;
}
```

## 7.5 Message Router Pattern

The Message Router pattern routes messages to different destinations based on message content, headers, or routing rules.

### When to Use:
- When you need to route messages based on content
- When you have multiple processing paths
- When you need to implement business rules for routing

### Real-World Analogy:
Think of a postal sorting facility. Letters arrive at a central location and are sorted into different bins based on their destination address, ensuring each letter reaches the correct regional office.

### Basic Implementation:
```java
// Message router interface
public interface MessageRouter {
    void route(Message message);
    void addRoute(RoutingRule rule);
    void removeRoute(RoutingRule rule);
}

// Routing rule interface
public interface RoutingRule {
    boolean matches(Message message);
    String getDestination();
    int getPriority();
}

// Content-based routing rule
public class ContentBasedRoutingRule implements RoutingRule {
    private String messageType;
    private String destination;
    private int priority;
    
    public ContentBasedRoutingRule(String messageType, String destination, int priority) {
        this.messageType = messageType;
        this.destination = destination;
        this.priority = priority;
    }
    
    public boolean matches(Message message) {
        return messageType.equals(message.getType());
    }
    
    public String getDestination() { return destination; }
    public int getPriority() { return priority; }
}

// Header-based routing rule
public class HeaderBasedRoutingRule implements RoutingRule {
    private String headerName;
    private String headerValue;
    private String destination;
    private int priority;
    
    public HeaderBasedRoutingRule(String headerName, String headerValue, String destination, int priority) {
        this.headerName = headerName;
        this.headerValue = headerValue;
        this.destination = destination;
        this.priority = priority;
    }
    
    public boolean matches(Message message) {
        String value = message.getHeaders().get(headerName);
        return headerValue.equals(value);
    }
    
    public String getDestination() { return destination; }
    public int getPriority() { return priority; }
}

// Simple message router implementation
public class SimpleMessageRouter implements MessageRouter {
    private List<RoutingRule> rules = new ArrayList<>();
    private MessageBroker messageBroker;
    
    public SimpleMessageRouter(MessageBroker messageBroker) {
        this.messageBroker = messageBroker;
    }
    
    public void route(Message message) {
        // Sort rules by priority (higher priority first)
        List<RoutingRule> sortedRules = rules.stream()
            .sorted(Comparator.comparingInt(RoutingRule::getPriority).reversed())
            .collect(Collectors.toList());
        
        // Find first matching rule
        for (RoutingRule rule : sortedRules) {
            if (rule.matches(message)) {
                messageBroker.send(rule.getDestination(), message);
                return;
            }
        }
        
        // No rule matched, send to default destination
        messageBroker.send("default", message);
    }
    
    public void addRoute(RoutingRule rule) {
        rules.add(rule);
    }
    
    public void removeRoute(RoutingRule rule) {
        rules.remove(rule);
    }
}
```

## 7.6 Message Translator Pattern

The Message Translator pattern transforms messages from one format to another, enabling communication between systems that use different message formats.

### When to Use:
- When integrating systems with different message formats
- When you need to transform data structures
- When you need to normalize message formats

### Real-World Analogy:
Think of a translator at the United Nations. They listen to a speaker in one language and translate the message into another language so that everyone can understand, regardless of their native language.

### Basic Implementation:
```java
// Message translator interface
public interface MessageTranslator {
    Message translate(Message sourceMessage, String targetFormat);
    boolean canTranslate(String sourceFormat, String targetFormat);
}

// JSON to XML translator
public class JsonToXmlTranslator implements MessageTranslator {
    public Message translate(Message sourceMessage, String targetFormat) {
        if (!"JSON".equals(sourceMessage.getType()) || !"XML".equals(targetFormat)) {
            throw new IllegalArgumentException("Cannot translate from " + sourceMessage.getType() + " to " + targetFormat);
        }
        
        try {
            // Parse JSON
            ObjectMapper mapper = new ObjectMapper();
            JsonNode jsonNode = mapper.readTree(sourceMessage.getPayload().toString());
            
            // Convert to XML
            String xml = convertJsonToXml(jsonNode);
            
            // Create new message
            return new TranslatedMessage(sourceMessage, xml, "XML");
            
        } catch (Exception e) {
            throw new RuntimeException("Translation failed", e);
        }
    }
    
    public boolean canTranslate(String sourceFormat, String targetFormat) {
        return "JSON".equals(sourceFormat) && "XML".equals(targetFormat);
    }
    
    private String convertJsonToXml(JsonNode jsonNode) {
        // Implementation to convert JSON to XML
        // This is a simplified example
        StringBuilder xml = new StringBuilder();
        xml.append("<root>");
        convertNode(jsonNode, xml);
        xml.append("</root>");
        return xml.toString();
    }
    
    private void convertNode(JsonNode node, StringBuilder xml) {
        if (node.isObject()) {
            node.fields().forEachRemaining(entry -> {
                xml.append("<").append(entry.getKey()).append(">");
                convertNode(entry.getValue(), xml);
                xml.append("</").append(entry.getKey()).append(">");
            });
        } else if (node.isArray()) {
            node.forEach(item -> {
                xml.append("<item>");
                convertNode(item, xml);
                xml.append("</item>");
            });
        } else {
            xml.append(node.asText());
        }
    }
}

// Message format converter
public class MessageFormatConverter {
    private List<MessageTranslator> translators = new ArrayList<>();
    
    public void addTranslator(MessageTranslator translator) {
        translators.add(translator);
    }
    
    public Message convert(Message sourceMessage, String targetFormat) {
        for (MessageTranslator translator : translators) {
            if (translator.canTranslate(sourceMessage.getType(), targetFormat)) {
                return translator.translate(sourceMessage, targetFormat);
            }
        }
        throw new UnsupportedOperationException("No translator found for " + sourceMessage.getType() + " to " + targetFormat);
    }
}
```

## 7.7 Message Filter Pattern

The Message Filter pattern selectively processes messages based on filtering criteria, allowing only relevant messages to pass through.

### When to Use:
- When you need to process only specific messages
- When you want to reduce processing load
- When you need to implement business rules for message selection

### Real-World Analogy:
Think of a spam filter in your email. It examines each incoming email and only allows legitimate messages to reach your inbox, filtering out spam based on various criteria.

### Basic Implementation:
```java
// Message filter interface
public interface MessageFilter {
    boolean shouldProcess(Message message);
    String getFilterName();
}

// Content-based filter
public class ContentBasedFilter implements MessageFilter {
    private String requiredContent;
    private String filterName;
    
    public ContentBasedFilter(String requiredContent, String filterName) {
        this.requiredContent = requiredContent;
        this.filterName = filterName;
    }
    
    public boolean shouldProcess(Message message) {
        String content = message.getPayload().toString().toLowerCase();
        return content.contains(requiredContent.toLowerCase());
    }
    
    public String getFilterName() { return filterName; }
}

// Header-based filter
public class HeaderBasedFilter implements MessageFilter {
    private String headerName;
    private String headerValue;
    private String filterName;
    
    public HeaderBasedFilter(String headerName, String headerValue, String filterName) {
        this.headerName = headerName;
        this.headerValue = headerValue;
        this.filterName = filterName;
    }
    
    public boolean shouldProcess(Message message) {
        String value = message.getHeaders().get(headerName);
        return headerValue.equals(value);
    }
    
    public String getFilterName() { return filterName; }
}

// Composite filter
public class CompositeFilter implements MessageFilter {
    private List<MessageFilter> filters;
    private FilterMode mode;
    private String filterName;
    
    public enum FilterMode {
        AND, // All filters must pass
        OR   // Any filter can pass
    }
    
    public CompositeFilter(List<MessageFilter> filters, FilterMode mode, String filterName) {
        this.filters = filters;
        this.mode = mode;
        this.filterName = filterName;
    }
    
    public boolean shouldProcess(Message message) {
        if (mode == FilterMode.AND) {
            return filters.stream().allMatch(filter -> filter.shouldProcess(message));
        } else {
            return filters.stream().anyMatch(filter -> filter.shouldProcess(message));
        }
    }
    
    public String getFilterName() { return filterName; }
}

// Filtered message processor
public class FilteredMessageProcessor {
    private List<MessageFilter> filters;
    private MessageHandler messageHandler;
    
    public FilteredMessageProcessor(List<MessageFilter> filters, MessageHandler messageHandler) {
        this.filters = filters;
        this.messageHandler = messageHandler;
    }
    
    public void process(Message message) {
        boolean shouldProcess = true;
        
        for (MessageFilter filter : filters) {
            if (!filter.shouldProcess(message)) {
                shouldProcess = false;
                System.out.println("Message filtered out by: " + filter.getFilterName());
                break;
            }
        }
        
        if (shouldProcess) {
            messageHandler.handle(message);
        }
    }
}
```

## 7.8 Splitter Pattern

The Splitter pattern breaks down a single message into multiple smaller messages, each containing a part of the original message.

### When to Use:
- When you need to process large messages in parallel
- When different parts of a message need different processing
- When you want to improve system throughput

### Real-World Analogy:
Think of a mail sorting facility that receives a large package containing multiple letters. The facility opens the package and sorts each letter individually, sending them to their respective destinations.

### Basic Implementation:
```java
// Message splitter interface
public interface MessageSplitter {
    List<Message> split(Message message);
    boolean canSplit(Message message);
}

// List-based splitter
public class ListSplitter implements MessageSplitter {
    private String listProperty;
    
    public ListSplitter(String listProperty) {
        this.listProperty = listProperty;
    }
    
    public List<Message> split(Message message) {
        if (!canSplit(message)) {
            throw new IllegalArgumentException("Cannot split message of type: " + message.getType());
        }
        
        List<Message> splitMessages = new ArrayList<>();
        
        try {
            // Parse the message payload to extract the list
            ObjectMapper mapper = new ObjectMapper();
            JsonNode rootNode = mapper.readTree(message.getPayload().toString());
            JsonNode listNode = rootNode.get(listProperty);
            
            if (listNode.isArray()) {
                for (JsonNode item : listNode) {
                    // Create a new message for each item
                    Message splitMessage = createSplitMessage(message, item);
                    splitMessages.add(splitMessage);
                }
            }
            
        } catch (Exception e) {
            throw new RuntimeException("Failed to split message", e);
        }
        
        return splitMessages;
    }
    
    public boolean canSplit(Message message) {
        return "LIST_MESSAGE".equals(message.getType());
    }
    
    private Message createSplitMessage(Message originalMessage, JsonNode item) {
        Map<String, String> headers = new HashMap<>(originalMessage.getHeaders());
        headers.put("SPLIT_INDEX", String.valueOf(splitMessages.size()));
        headers.put("ORIGINAL_MESSAGE_ID", originalMessage.getId());
        
        return new SplitMessage(
            UUID.randomUUID().toString(),
            "ITEM_MESSAGE",
            item.toString(),
            headers,
            System.currentTimeMillis()
        );
    }
}

// Batch splitter
public class BatchSplitter implements MessageSplitter {
    private int batchSize;
    
    public BatchSplitter(int batchSize) {
        this.batchSize = batchSize;
    }
    
    public List<Message> split(Message message) {
        if (!canSplit(message)) {
            throw new IllegalArgumentException("Cannot split message of type: " + message.getType());
        }
        
        List<Message> splitMessages = new ArrayList<>();
        
        try {
            ObjectMapper mapper = new ObjectMapper();
            JsonNode rootNode = mapper.readTree(message.getPayload().toString());
            JsonNode itemsNode = rootNode.get("items");
            
            if (itemsNode.isArray()) {
                List<JsonNode> items = new ArrayList<>();
                itemsNode.forEach(items::add);
                
                // Split into batches
                for (int i = 0; i < items.size(); i += batchSize) {
                    int endIndex = Math.min(i + batchSize, items.size());
                    List<JsonNode> batch = items.subList(i, endIndex);
                    
                    Message batchMessage = createBatchMessage(message, batch, i / batchSize);
                    splitMessages.add(batchMessage);
                }
            }
            
        } catch (Exception e) {
            throw new RuntimeException("Failed to split message", e);
        }
        
        return splitMessages;
    }
    
    public boolean canSplit(Message message) {
        return "BATCH_MESSAGE".equals(message.getType());
    }
    
    private Message createBatchMessage(Message originalMessage, List<JsonNode> batch, int batchIndex) {
        Map<String, String> headers = new HashMap<>(originalMessage.getHeaders());
        headers.put("BATCH_INDEX", String.valueOf(batchIndex));
        headers.put("BATCH_SIZE", String.valueOf(batch.size()));
        headers.put("ORIGINAL_MESSAGE_ID", originalMessage.getId());
        
        // Create batch payload
        ObjectNode batchPayload = new ObjectMapper().createObjectNode();
        ArrayNode itemsArray = batchPayload.putArray("items");
        batch.forEach(itemsArray::add);
        
        return new SplitMessage(
            UUID.randomUUID().toString(),
            "BATCH_MESSAGE",
            batchPayload.toString(),
            headers,
            System.currentTimeMillis()
        );
    }
}
```

## 7.9 Aggregator Pattern

The Aggregator pattern combines multiple related messages into a single message, often used after processing split messages.

### When to Use:
- When you need to combine results from multiple processing steps
- When you want to reduce the number of messages in the system
- When you need to create summary reports

### Real-World Analogy:
Think of a financial report that combines data from multiple departments. Each department provides their individual reports, and the aggregator combines them into a comprehensive company-wide report.

### Basic Implementation:
```java
// Message aggregator interface
public interface MessageAggregator {
    void addMessage(Message message);
    boolean isComplete();
    Message aggregate();
    void reset();
}

// Count-based aggregator
public class CountBasedAggregator implements MessageAggregator {
    private int expectedCount;
    private List<Message> messages = new ArrayList<>();
    private String correlationId;
    
    public CountBasedAggregator(int expectedCount, String correlationId) {
        this.expectedCount = expectedCount;
        this.correlationId = correlationId;
    }
    
    public void addMessage(Message message) {
        if (correlationId.equals(message.getHeaders().get("CORRELATION_ID"))) {
            messages.add(message);
        }
    }
    
    public boolean isComplete() {
        return messages.size() >= expectedCount;
    }
    
    public Message aggregate() {
        if (!isComplete()) {
            throw new IllegalStateException("Not enough messages to aggregate");
        }
        
        // Create aggregated payload
        ObjectMapper mapper = new ObjectMapper();
        ObjectNode aggregatedPayload = mapper.createObjectNode();
        ArrayNode itemsArray = aggregatedPayload.putArray("items");
        
        for (Message message : messages) {
            try {
                JsonNode messagePayload = mapper.readTree(message.getPayload().toString());
                itemsArray.add(messagePayload);
            } catch (Exception e) {
                System.err.println("Error processing message: " + e.getMessage());
            }
        }
        
        // Create aggregated message
        Map<String, String> headers = new HashMap<>();
        headers.put("CORRELATION_ID", correlationId);
        headers.put("AGGREGATED_COUNT", String.valueOf(messages.size()));
        
        return new AggregatedMessage(
            UUID.randomUUID().toString(),
            "AGGREGATED_MESSAGE",
            aggregatedPayload.toString(),
            headers,
            System.currentTimeMillis()
        );
    }
    
    public void reset() {
        messages.clear();
    }
}

// Time-based aggregator
public class TimeBasedAggregator implements MessageAggregator {
    private long timeoutMillis;
    private long startTime;
    private List<Message> messages = new ArrayList<>();
    private String correlationId;
    
    public TimeBasedAggregator(long timeoutMillis, String correlationId) {
        this.timeoutMillis = timeoutMillis;
        this.correlationId = correlationId;
        this.startTime = System.currentTimeMillis();
    }
    
    public void addMessage(Message message) {
        if (correlationId.equals(message.getHeaders().get("CORRELATION_ID"))) {
            messages.add(message);
        }
    }
    
    public boolean isComplete() {
        return System.currentTimeMillis() - startTime >= timeoutMillis;
    }
    
    public Message aggregate() {
        if (messages.isEmpty()) {
            throw new IllegalStateException("No messages to aggregate");
        }
        
        // Create aggregated payload
        ObjectMapper mapper = new ObjectMapper();
        ObjectNode aggregatedPayload = mapper.createObjectNode();
        ArrayNode itemsArray = aggregatedPayload.putArray("items");
        
        for (Message message : messages) {
            try {
                JsonNode messagePayload = mapper.readTree(message.getPayload().toString());
                itemsArray.add(messagePayload);
            } catch (Exception e) {
                System.err.println("Error processing message: " + e.getMessage());
            }
        }
        
        // Create aggregated message
        Map<String, String> headers = new HashMap<>();
        headers.put("CORRELATION_ID", correlationId);
        headers.put("AGGREGATED_COUNT", String.valueOf(messages.size()));
        headers.put("AGGREGATION_TIME", String.valueOf(System.currentTimeMillis() - startTime));
        
        return new AggregatedMessage(
            UUID.randomUUID().toString(),
            "AGGREGATED_MESSAGE",
            aggregatedPayload.toString(),
            headers,
            System.currentTimeMillis()
        );
    }
    
    public void reset() {
        messages.clear();
        startTime = System.currentTimeMillis();
    }
}
```

## 7.10 Content-Based Router Pattern

The Content-Based Router pattern routes messages to different destinations based on the content of the message, enabling sophisticated routing logic.

### When to Use:
- When you need complex routing based on message content
- When you want to implement business rules for message routing
- When you need to route messages to different processing pipelines

### Real-World Analogy:
Think of a smart postal system that reads the content of letters and routes them to different departments based on what's written inside. A letter about billing goes to the finance department, while a letter about technical support goes to the IT department.

### Basic Implementation:
```java
// Content-based router
public class ContentBasedRouter implements MessageRouter {
    private List<ContentRoutingRule> rules = new ArrayList<>();
    private MessageBroker messageBroker;
    
    public ContentBasedRouter(MessageBroker messageBroker) {
        this.messageBroker = messageBroker;
    }
    
    public void route(Message message) {
        for (ContentRoutingRule rule : rules) {
            if (rule.matches(message)) {
                messageBroker.send(rule.getDestination(), message);
                return;
            }
        }
        
        // No rule matched, send to default destination
        messageBroker.send("default", message);
    }
    
    public void addRule(ContentRoutingRule rule) {
        rules.add(rule);
    }
    
    public void removeRule(ContentRoutingRule rule) {
        rules.remove(rule);
    }
}

// Content routing rule interface
public interface ContentRoutingRule {
    boolean matches(Message message);
    String getDestination();
    int getPriority();
}

// XPath-based routing rule
public class XPathRoutingRule implements ContentRoutingRule {
    private String xpathExpression;
    private String expectedValue;
    private String destination;
    private int priority;
    
    public XPathRoutingRule(String xpathExpression, String expectedValue, String destination, int priority) {
        this.xpathExpression = xpathExpression;
        this.expectedValue = expectedValue;
        this.destination = destination;
        this.priority = priority;
    }
    
    public boolean matches(Message message) {
        try {
            // Parse XML content
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            DocumentBuilder builder = factory.newDocumentBuilder();
            Document doc = builder.parse(new ByteArrayInputStream(message.getPayload().toString().getBytes()));
            
            // Evaluate XPath expression
            XPathFactory xpathFactory = XPathFactory.newInstance();
            XPath xpath = xpathFactory.newXPath();
            String result = xpath.evaluate(xpathExpression, doc);
            
            return expectedValue.equals(result);
            
        } catch (Exception e) {
            System.err.println("Error evaluating XPath: " + e.getMessage());
            return false;
        }
    }
    
    public String getDestination() { return destination; }
    public int getPriority() { return priority; }
}

// JSON-based routing rule
public class JsonRoutingRule implements ContentRoutingRule {
    private String jsonPath;
    private String expectedValue;
    private String destination;
    private int priority;
    
    public JsonRoutingRule(String jsonPath, String expectedValue, String destination, int priority) {
        this.jsonPath = jsonPath;
        this.expectedValue = expectedValue;
        this.destination = destination;
        this.priority = priority;
    }
    
    public boolean matches(Message message) {
        try {
            ObjectMapper mapper = new ObjectMapper();
            JsonNode rootNode = mapper.readTree(message.getPayload().toString());
            
            // Evaluate JSON path
            String result = evaluateJsonPath(rootNode, jsonPath);
            
            return expectedValue.equals(result);
            
        } catch (Exception e) {
            System.err.println("Error evaluating JSON path: " + e.getMessage());
            return false;
        }
    }
    
    private String evaluateJsonPath(JsonNode node, String path) {
        String[] parts = path.split("\\.");
        JsonNode current = node;
        
        for (String part : parts) {
            if (current.isArray() && part.matches("\\d+")) {
                int index = Integer.parseInt(part);
                current = current.get(index);
            } else {
                current = current.get(part);
            }
            
            if (current == null) {
                return null;
            }
        }
        
        return current.asText();
    }
    
    public String getDestination() { return destination; }
    public int getPriority() { return priority; }
}

// Regex-based routing rule
public class RegexRoutingRule implements ContentRoutingRule {
    private Pattern pattern;
    private String destination;
    private int priority;
    
    public RegexRoutingRule(String regex, String destination, int priority) {
        this.pattern = Pattern.compile(regex);
        this.destination = destination;
        this.priority = priority;
    }
    
    public boolean matches(Message message) {
        String content = message.getPayload().toString();
        return pattern.matcher(content).find();
    }
    
    public String getDestination() { return destination; }
    public int getPriority() { return priority; }
}
```

This comprehensive coverage of integration patterns provides the foundation for building robust, scalable distributed systems. Each pattern addresses specific integration challenges and offers different trade-offs in terms of complexity, performance, and reliability.