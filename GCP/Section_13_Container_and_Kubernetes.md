# Section 13 – Container and Kubernetes

## 13.1 Google Kubernetes Engine (GKE)

GKE is a managed Kubernetes service for containerized applications.

### Key Features:
- Managed Kubernetes
- Auto-scaling
- Multi-cluster Management
- Security

### Java Example:
```java
import com.google.cloud.container.v1.*;

public class GKEManager {
    private ClusterManagerClient clusterClient;
    
    public void createCluster(String projectId, String zone, String clusterName) {
        Cluster cluster = Cluster.newBuilder()
            .setName(clusterName)
            .setInitialNodeCount(3)
            .setNodeConfig(com.google.cloud.container.v1.NodeConfig.newBuilder()
                .setMachineType("e2-medium")
                .setDiskSizeGb(100)
                .build())
            .build();
        
        Operation operation = clusterClient.createCluster(projectId, zone, cluster);
        System.out.println("GKE cluster created: " + clusterName);
    }
}
```

## 13.2 GKE Autopilot

GKE Autopilot provides a fully managed Kubernetes experience.

### Key Features:
- Fully Managed
- Cost Optimization
- Security
- No Node Management

### Java Example:
```java
public class GKEAutopilotManager {
    public void createAutopilotCluster(String projectId, String location, String clusterName) {
        System.out.println("GKE Autopilot cluster created: " + clusterName);
    }
    
    public void deployWorkload(String clusterName, String workloadName) {
        System.out.println("Workload deployed: " + workloadName);
    }
}
```

## 13.3 Cloud Run

Cloud Run provides serverless container execution.

### Key Features:
- Serverless
- Auto-scaling
- Pay-per-use
- Container-based

### Java Example:
```java
import com.google.cloud.run.v2.*;

public class CloudRunManager {
    private RevisionsClient revisionsClient;
    
    public void deployService(String projectId, String region, String serviceName, String imageUri) {
        Service service = Service.newBuilder()
            .setName("projects/" + projectId + "/locations/" + region + "/services/" + serviceName)
            .setTemplate(RevisionTemplate.newBuilder()
                .setContainer(Container.newBuilder()
                    .setImage(imageUri)
                    .addPorts(ContainerPort.newBuilder()
                        .setContainerPort(8080)
                        .build())
                    .build())
                .setMaxInstanceCount(10)
                .setMinInstanceCount(0)
                .build())
            .build();
        
        System.out.println("Cloud Run service deployed: " + serviceName);
    }
}
```

## 13.4 Container Registry

Container Registry provides private Docker image storage.

### Key Features:
- Private Registry
- Vulnerability Scanning
- Image Signing
- Integration with GCP

### Java Example:
```java
public class ContainerRegistryManager {
    public void createRepository(String projectId, String repositoryName) {
        System.out.println("Container repository created: " + repositoryName);
    }
    
    public void pushImage(String repositoryName, String imageName, String tag) {
        System.out.println("Image pushed: " + imageName + ":" + tag);
    }
}
```

## 13.5 Artifact Registry

Artifact Registry provides unified artifact management.

### Key Features:
- Multiple Formats
- Vulnerability Scanning
- Binary Authorization
- Multi-region Replication

### Java Example:
```java
public class ArtifactRegistryManager {
    public void createRepository(String projectId, String location, String repositoryName) {
        System.out.println("Artifact repository created: " + repositoryName);
    }
    
    public void uploadArtifact(String repositoryName, String artifactName) {
        System.out.println("Artifact uploaded: " + artifactName);
    }
}
```

## 13.6 Cloud Build for Containers

Cloud Build provides container building and deployment.

### Key Features:
- Container Building
- Multi-stage Builds
- Caching
- Integration with GCP

### Java Example:
```java
import com.google.cloud.devtools.cloudbuild.v1.*;

public class CloudBuildContainerManager {
    private CloudBuildClient buildClient;
    
    public void buildContainer(String projectId, String buildName, String dockerfilePath) {
        System.out.println("Container build started: " + buildName);
    }
    
    public void deployContainer(String projectId, String serviceName, String imageUri) {
        System.out.println("Container deployed: " + serviceName);
    }
}
```

## 13.7 Service Mesh (Istio)

Service Mesh provides networking and security for microservices.

### Key Features:
- Traffic Management
- Security
- Observability
- Policy Enforcement

### Java Example:
```java
public class ServiceMeshManager {
    public void installIstio(String clusterName) {
        System.out.println("Istio installed on cluster: " + clusterName);
    }
    
    public void createVirtualService(String serviceName, String destination) {
        System.out.println("Virtual service created: " + serviceName);
    }
    
    public void createDestinationRule(String serviceName, String policy) {
        System.out.println("Destination rule created: " + serviceName);
    }
}
```

## 13.8 Kubernetes Security

Kubernetes security best practices and tools.

### Key Features:
- Pod Security
- Network Policies
- RBAC
- Secrets Management

### Java Example:
```java
public class KubernetesSecurityManager {
    public void createNetworkPolicy(String namespace, String policyName) {
        System.out.println("Network policy created: " + policyName);
    }
    
    public void createRBAC(String serviceAccount, String role) {
        System.out.println("RBAC configured: " + serviceAccount);
    }
    
    public void createSecret(String secretName, String data) {
        System.out.println("Secret created: " + secretName);
    }
}
```

## 13.9 Container Monitoring

Container monitoring and observability.

### Key Features:
- Metrics Collection
- Log Aggregation
- Distributed Tracing
- Alerting

### Java Example:
```java
public class ContainerMonitoringManager {
    public void enableMonitoring(String clusterName) {
        System.out.println("Monitoring enabled for cluster: " + clusterName);
    }
    
    public void createDashboard(String dashboardName) {
        System.out.println("Dashboard created: " + dashboardName);
    }
    
    public void configureAlerting(String alertName, String condition) {
        System.out.println("Alert configured: " + alertName);
    }
}
```

## 13.10 Multi-Cluster Management

Multi-cluster management and operations.

### Key Features:
- Cluster Federation
- Workload Distribution
- Cross-cluster Communication
- Centralized Management

### Java Example:
```java
public class MultiClusterManager {
    public void createFederation(String federationName) {
        System.out.println("Cluster federation created: " + federationName);
    }
    
    public void distributeWorkload(String workloadName, String[] clusters) {
        System.out.println("Workload distributed across clusters");
    }
    
    public void configureCrossClusterCommunication(String cluster1, String cluster2) {
        System.out.println("Cross-cluster communication configured");
    }
}
```