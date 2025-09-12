# Section 3 – Compute Services

## 3.1 Compute Engine (VMs)

Compute Engine provides scalable virtual machines running in Google's data centers.

### Key Features:
- Custom Machine Types
- Preemptible Instances
- Live Migration
- Sustained Use Discounts

### Java Example:
```java
import com.google.cloud.compute.v1.*;

public class ComputeEngineManager {
    public void createVM(String projectId, String zone, String instanceName) {
        Instance instance = Instance.newBuilder()
            .setName(instanceName)
            .setMachineType("zones/" + zone + "/machineTypes/n1-standard-1")
            .build();
        
        System.out.println("VM created: " + instanceName);
    }
}
```

## 3.2 Google Kubernetes Engine (GKE)

GKE is a managed Kubernetes service for containerized applications.

### Key Features:
- Managed Kubernetes
- Auto-scaling
- Multi-cluster Management
- Security

### Java Example:
```java
import com.google.cloud.container.v1.ClusterManagerClient;

public class GKEManager {
    public void createCluster(String projectId, String zone, String clusterName) {
        System.out.println("GKE cluster created: " + clusterName);
    }
}
```

## 3.3 Cloud Run (Serverless Containers)

Cloud Run is a fully managed serverless platform for containers.

### Key Features:
- Serverless
- Auto-scaling
- Pay-per-use
- Container-based

### Java Example:
```java
public class CloudRunManager {
    public void deployService(String serviceName, String imageUri) {
        System.out.println("Cloud Run service deployed: " + serviceName);
    }
}
```

## 3.4 App Engine (Serverless Applications)

App Engine is a fully managed serverless platform for web applications.

### Key Features:
- Serverless
- Auto-scaling
- Multiple Languages
- Built-in Services

### Java Example:
```java
import com.google.appengine.api.datastore.*;

public class AppEngineExample {
    public void createUserProfile(String userId, String name) {
        Entity userProfile = new Entity("UserProfile", userId);
        userProfile.setProperty("name", name);
        System.out.println("User profile created: " + name);
    }
}
```

## 3.5 Cloud Functions (Serverless Functions)

Cloud Functions is a serverless execution environment.

### Key Features:
- Event-driven
- Pay-per-execution
- Multiple Languages
- Automatic Scaling

### Java Example:
```java
import com.google.cloud.functions.HttpFunction;

public class CloudFunctionExample implements HttpFunction {
    @Override
    public void service(HttpRequest request, HttpResponse response) throws Exception {
        response.getWriter().write("Hello from Cloud Function!");
    }
}
```

## 3.6 Preemptible VMs

Preemptible VMs are short-lived, low-cost instances.

### Key Features:
- Cost Savings (up to 80%)
- Short Lifespan (24 hours max)
- Interruptible
- Batch Workloads

### Java Example:
```java
public class PreemptibleVMManager {
    public void createPreemptibleVM(String instanceName) {
        System.out.println("Preemptible VM created: " + instanceName);
    }
}
```

## 3.7 Spot VMs

Spot VMs have dynamic pricing based on supply and demand.

### Key Features:
- Dynamic Pricing
- Cost Savings (up to 91%)
- Flexible Duration
- Regional Availability

### Java Example:
```java
public class SpotVMManager {
    public void createSpotVM(String instanceName) {
        System.out.println("Spot VM created: " + instanceName);
    }
}
```

## 3.8 VM Instance Types

GCP offers various VM instance types for different workloads.

### Instance Families:
- E2: Cost-optimized
- N1: First-generation
- N2: Second-generation
- C2: Compute-optimized
- M1: Memory-optimized

### Java Example:
```java
public class InstanceTypeSelector {
    public String selectInstanceType(String workloadType) {
        switch (workloadType) {
            case "GENERAL_PURPOSE": return "e2-standard-2";
            case "COMPUTE_INTENSIVE": return "c2-standard-4";
            case "MEMORY_INTENSIVE": return "m1-standard-4";
            default: return "e2-standard-2";
        }
    }
}
```

## 3.9 Custom Machine Types

Custom machine types allow specific CPU and memory configurations.

### Key Features:
- Flexible Configuration
- Cost Optimization
- Performance Tuning
- Regional Availability

### Java Example:
```java
public class CustomMachineTypeManager {
    public void createCustomMachineType(String name, int cpuCores, int memoryMB) {
        System.out.println("Custom machine type created: " + name);
    }
}
```

## 3.10 Compute Engine Images

Images are templates used to create VM instances.

### Image Types:
- Public Images
- Custom Images
- Family Images
- Specific Images

### Java Example:
```java
public class ImageManager {
    public void listImages(String projectId) {
        System.out.println("Listing images for project: " + projectId);
    }
    
    public void createCustomImage(String imageName, String sourceDisk) {
        System.out.println("Custom image created: " + imageName);
    }
}
```