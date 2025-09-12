# Section 12 – Application Integration

## 12.1 Cloud Pub/Sub

Cloud Pub/Sub provides reliable messaging for event-driven systems.

### Key Features:
- Reliable Messaging
- At-least-once Delivery
- Ordering
- Dead Letter Topics

### Java Example:
```java
import com.google.cloud.pubsub.v1.*;

public class PubSubManager {
    private TopicAdminClient topicClient;
    private SubscriptionAdminClient subscriptionClient;
    
    public void createTopic(String projectId, String topicName) {
        TopicName topic = TopicName.of(projectId, topicName);
        Topic topicObj = Topic.newBuilder().setName(topic.toString()).build();
        
        topicClient.createTopic(topicObj);
        System.out.println("Topic created: " + topicName);
    }
    
    public void createSubscription(String projectId, String topicName, String subscriptionName) {
        TopicName topic = TopicName.of(projectId, topicName);
        SubscriptionName subscription = SubscriptionName.of(projectId, subscriptionName);
        
        Subscription subscriptionObj = Subscription.newBuilder()
            .setName(subscription.toString())
            .setTopic(topic.toString())
            .build();
        
        subscriptionClient.createSubscription(subscriptionObj);
        System.out.println("Subscription created: " + subscriptionName);
    }
}
```

## 12.2 Cloud Tasks

Cloud Tasks provides reliable task execution and management.

### Key Features:
- Reliable Task Execution
- Rate Limiting
- Retry Logic
- Dead Letter Queues

### Java Example:
```java
import com.google.cloud.tasks.v2.*;

public class CloudTasksManager {
    private CloudTasksClient tasksClient;
    
    public void createQueue(String projectId, String location, String queueName) {
        Queue queue = Queue.newBuilder()
            .setName("projects/" + projectId + "/locations/" + location + "/queues/" + queueName)
            .build();
        
        tasksClient.createQueue(LocationName.of(projectId, location), queue);
        System.out.println("Queue created: " + queueName);
    }
    
    public void createTask(String queueName, String taskName, String payload) {
        Task task = Task.newBuilder()
            .setName(taskName)
            .setHttpRequest(HttpRequest.newBuilder()
                .setUrl("https://example.com/process")
                .setHttpMethod(HttpMethod.POST)
                .setBody(ByteString.copyFromUtf8(payload))
                .build())
            .build();
        
        tasksClient.createTask(QueueName.of(queueName), task);
        System.out.println("Task created: " + taskName);
    }
}
```

## 12.3 Cloud Scheduler

Cloud Scheduler provides cron-based job scheduling.

### Key Features:
- Cron-based Scheduling
- HTTP Targets
- Pub/Sub Targets
- App Engine Targets

### Java Example:
```java
import com.google.cloud.scheduler.v1.*;

public class CloudSchedulerManager {
    private CloudSchedulerClient schedulerClient;
    
    public void createJob(String projectId, String location, String jobName, String schedule) {
        Job job = Job.newBuilder()
            .setName("projects/" + projectId + "/locations/" + location + "/jobs/" + jobName)
            .setSchedule(schedule)
            .setTimeZone("UTC")
            .setHttpTarget(HttpTarget.newBuilder()
                .setUri("https://example.com/execute")
                .setHttpMethod(HttpMethod.POST)
                .build())
            .build();
        
        schedulerClient.createJob(LocationName.of(projectId, location), job);
        System.out.println("Job created: " + jobName);
    }
}
```

## 12.4 Cloud Workflows

Cloud Workflows provides serverless workflow orchestration.

### Key Features:
- Serverless Workflows
- YAML-based Definition
- Error Handling
- Retry Logic

### Java Example:
```java
public class CloudWorkflowsManager {
    public void createWorkflow(String projectId, String location, String workflowName) {
        System.out.println("Workflow created: " + workflowName);
    }
    
    public void executeWorkflow(String workflowName, String input) {
        System.out.println("Workflow executed: " + workflowName);
    }
}
```

## 12.5 Eventarc

Eventarc provides event routing and delivery.

### Key Features:
- Event Routing
- Multiple Sources
- Multiple Destinations
- Filtering

### Java Example:
```java
public class EventarcManager {
    public void createTrigger(String projectId, String location, String triggerName) {
        System.out.println("Eventarc trigger created: " + triggerName);
    }
    
    public void configureEventFilter(String triggerName, String filter) {
        System.out.println("Event filter configured: " + filter);
    }
}
```

## 12.6 Cloud Functions

Cloud Functions provides serverless event-driven functions.

### Key Features:
- Event-driven Execution
- Pay-per-use
- Multiple Languages
- Automatic Scaling

### Java Example:
```java
import com.google.cloud.functions.HttpFunction;
import com.google.cloud.functions.HttpRequest;
import com.google.cloud.functions.HttpResponse;

public class CloudFunctionExample implements HttpFunction {
    @Override
    public void service(HttpRequest request, HttpResponse response) throws Exception {
        response.getWriter().write("Hello from Cloud Function!");
    }
}
```

## 12.7 API Management

API Management provides tools for managing APIs.

### Key Features:
- API Gateway
- Authentication
- Rate Limiting
- Monitoring

### Java Example:
```java
public class APIManagementManager {
    public void createAPI(String projectId, String apiName) {
        System.out.println("API created: " + apiName);
    }
    
    public void configureAuthentication(String apiName, String authType) {
        System.out.println("Authentication configured: " + authType);
    }
}
```

## 12.8 Service Mesh

Service Mesh provides networking and security for microservices.

### Key Features:
- Traffic Management
- Security
- Observability
- Policy Enforcement

### Java Example:
```java
public class ServiceMeshManager {
    public void configureIstio(String projectId, String clusterName) {
        System.out.println("Istio configured for cluster: " + clusterName);
    }
    
    public void createVirtualService(String serviceName, String destination) {
        System.out.println("Virtual service created: " + serviceName);
    }
}
```

## 12.9 Event-Driven Architecture

Event-driven architecture patterns and best practices.

### Key Features:
- Loose Coupling
- Scalability
- Resilience
- Real-time Processing

### Java Example:
```java
public class EventDrivenArchitecture {
    public void publishEvent(String eventType, String payload) {
        System.out.println("Event published: " + eventType);
    }
    
    public void subscribeToEvent(String eventType, String handler) {
        System.out.println("Subscribed to event: " + eventType);
    }
}
```

## 12.10 Microservices Integration

Microservices integration patterns and tools.

### Key Features:
- Service Discovery
- Load Balancing
- Circuit Breakers
- Distributed Tracing

### Java Example:
```java
public class MicroservicesIntegration {
    public void registerService(String serviceName, String endpoint) {
        System.out.println("Service registered: " + serviceName);
    }
    
    public void discoverService(String serviceName) {
        System.out.println("Service discovered: " + serviceName);
    }
}
```