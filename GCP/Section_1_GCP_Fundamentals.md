# Section 1 – GCP Fundamentals

## 1.1 What is Google Cloud Platform

Google Cloud Platform (GCP) is a comprehensive suite of cloud computing services offered by Google. It provides infrastructure, platform, and software services that run on Google's hardware infrastructure, allowing organizations to build, deploy, and scale applications in the cloud.

### Key Concepts:
- **Cloud Computing**: On-demand delivery of IT resources over the internet
- **Infrastructure as a Service (IaaS)**: Virtual machines, storage, and networking
- **Platform as a Service (PaaS)**: Development and deployment environments
- **Software as a Service (SaaS)**: Ready-to-use applications

### Real-World Analogy:
Think of GCP like a massive digital city where you can rent:
- **Apartments** (Virtual Machines) for your applications to live
- **Storage Units** (Cloud Storage) for your data
- **Utilities** (Database services) for power and water
- **Transportation** (Networking) to move data around

### Java Example - Basic GCP Client Setup:
```java
import com.google.cloud.storage.Storage;
import com.google.cloud.storage.StorageOptions;

public class GCPBasicExample {
    public static void main(String[] args) {
        // Initialize GCP Storage client
        Storage storage = StorageOptions.getDefaultInstance().getService();
        
        // List all buckets in your project
        storage.list().iterateAll().forEach(bucket -> {
            System.out.println("Bucket: " + bucket.getName());
        });
    }
}
```

## 1.2 GCP History and Evolution

Google Cloud Platform evolved from Google's internal infrastructure that powers services like Google Search, Gmail, and YouTube. The platform was officially launched in 2008 with App Engine, but the modern GCP ecosystem began taking shape around 2011-2012.

### Timeline:
- **2008**: App Engine launched (PaaS for web applications)
- **2011**: Google Cloud Storage and BigQuery introduced
- **2012**: Compute Engine launched (IaaS)
- **2014**: Kubernetes open-sourced by Google
- **2016**: Google Kubernetes Engine (GKE) launched
- **2018**: Anthos introduced for hybrid cloud
- **2020**: Cloud Run for serverless containers
- **2022**: Vertex AI for machine learning

### Evolution Phases:
1. **Early Phase (2008-2012)**: Focus on web applications and data analytics
2. **Infrastructure Phase (2012-2016)**: Full IaaS capabilities and containerization
3. **AI/ML Phase (2016-2020)**: Machine learning and artificial intelligence services
4. **Hybrid/Multi-cloud Phase (2020-present)**: Enterprise-grade hybrid solutions

### Java Example - Evolution of GCP APIs:
```java
// Early GCP (2012) - Basic REST API calls
public class EarlyGCPExample {
    public void createInstance() {
        // Manual REST API calls
        String url = "https://www.googleapis.com/compute/v1/projects/PROJECT/zones/ZONE/instances";
        // Complex JSON payload construction...
    }
}

// Modern GCP (2022) - Client Libraries
public class ModernGCPExample {
    public void createInstance() {
        Compute compute = ComputeOptions.getDefaultInstance().getService();
        InstanceInfo instance = InstanceInfo.of(
            ZoneId.of("us-central1-a"),
            InstanceId.of("my-instance"),
            MachineTypeId.of("n1-standard-1")
        );
        compute.create(instance);
    }
}
```

## 1.3 GCP vs AWS vs Azure

The three major cloud providers each have their strengths and target different use cases. Understanding these differences is crucial for making informed decisions.

### Comparison Matrix:

| Feature | GCP | AWS | Azure |
|---------|-----|-----|-------|
| **Strengths** | AI/ML, Data Analytics, Kubernetes | Market Leader, Broad Services | Enterprise Integration, Microsoft Ecosystem |
| **Pricing Model** | Per-second billing | Per-hour billing | Per-minute billing |
| **Global Reach** | 35+ regions | 25+ regions | 60+ regions |
| **AI/ML Services** | Vertex AI, AutoML | SageMaker, Rekognition | Azure ML, Cognitive Services |
| **Container Services** | GKE (Kubernetes) | EKS, ECS | AKS, Container Instances |

### Real-World Analogy:
- **AWS**: Like a massive shopping mall with everything you need
- **Azure**: Like a corporate office building with Microsoft integration
- **GCP**: Like a high-tech research facility with cutting-edge tools

### Java Example - Multi-Cloud Strategy:
```java
public class CloudProviderStrategy {
    public void chooseProvider(String workloadType) {
        switch (workloadType) {
            case "AI_ML":
                // GCP excels in AI/ML with Vertex AI
                useGCPVertexAI();
                break;
            case "ENTERPRISE":
                // Azure for Microsoft-centric organizations
                useAzureServices();
                break;
            case "GENERAL_PURPOSE":
                // AWS for broad service coverage
                useAWSServices();
                break;
        }
    }
    
    private void useGCPVertexAI() {
        // GCP's strength in AI/ML
        System.out.println("Using GCP Vertex AI for machine learning workloads");
    }
}
```

## 1.4 GCP Global Infrastructure

GCP operates a global network of data centers organized into regions and zones, providing high availability, low latency, and data sovereignty options.

### Infrastructure Components:
- **Regions**: Geographic locations containing multiple zones
- **Zones**: Independent data centers within a region
- **Edge Locations**: Points of presence for CDN and caching
- **Submarine Cables**: Google's private fiber network

### Global Network:
- **35+ regions** worldwide
- **106+ zones** across regions
- **140+ edge locations** for CDN
- **Private fiber network** connecting data centers

### Java Example - Multi-Region Deployment:
```java
public class GlobalInfrastructureExample {
    private static final String[] REGIONS = {
        "us-central1",    // Iowa, USA
        "europe-west1",   // Belgium
        "asia-southeast1" // Singapore
    };
    
    public void deployGlobally(String application) {
        for (String region : REGIONS) {
            deployToRegion(application, region);
        }
    }
    
    private void deployToRegion(String app, String region) {
        System.out.println("Deploying " + app + " to " + region);
        // Deploy application to specific region
    }
}
```

## 1.5 GCP Regions and Zones

Understanding regions and zones is fundamental to designing resilient and performant applications on GCP.

### Key Concepts:
- **Region**: A geographic location containing multiple zones
- **Zone**: A single data center within a region
- **Multi-Zone**: Deploying across multiple zones in the same region
- **Multi-Region**: Deploying across multiple regions

### Best Practices:
- Deploy across multiple zones for high availability
- Use multi-region for disaster recovery
- Consider data residency requirements
- Optimize for latency and cost

### Java Example - Zone-Aware Application:
```java
public class ZoneAwareApplication {
    private String currentZone;
    private String region;
    
    public ZoneAwareApplication() {
        this.currentZone = getCurrentZone();
        this.region = extractRegion(currentZone);
    }
    
    private String getCurrentZone() {
        // Get current zone from metadata server
        return System.getenv("GCE_ZONE");
    }
    
    private String extractRegion(String zone) {
        // Extract region from zone (e.g., us-central1-a -> us-central1)
        return zone.substring(0, zone.lastIndexOf('-'));
    }
    
    public boolean isInSameRegion(String otherZone) {
        String otherRegion = extractRegion(otherZone);
        return this.region.equals(otherRegion);
    }
}
```

## 1.6 GCP Console and CLI

GCP provides multiple interfaces for managing cloud resources, each suited for different use cases.

### GCP Console:
- Web-based graphical interface
- User-friendly for beginners
- Visual resource management
- Real-time monitoring and logging

### Cloud CLI (gcloud):
- Command-line interface for automation
- Scriptable and programmable
- Advanced configuration options
- CI/CD integration

### Java Example - CLI Integration:
```java
public class GCPCLIIntegration {
    public void createInstanceViaCLI() {
        try {
            ProcessBuilder pb = new ProcessBuilder(
                "gcloud", "compute", "instances", "create", "my-instance",
                "--zone=us-central1-a",
                "--machine-type=n1-standard-1",
                "--image-family=debian-11",
                "--image-project=debian-cloud"
            );
            
            Process process = pb.start();
            int exitCode = process.waitFor();
            
            if (exitCode == 0) {
                System.out.println("Instance created successfully");
            } else {
                System.err.println("Failed to create instance");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## 1.7 GCP Billing and Pricing

GCP uses a pay-as-you-go pricing model with various discounts and optimization options.

### Pricing Models:
- **On-demand**: Pay for what you use
- **Committed Use**: 1-3 year commitments for discounts
- **Preemptible VMs**: Up to 80% discount for interruptible workloads
- **Sustained Use**: Automatic discounts for long-running instances

### Cost Optimization Strategies:
- Right-size your resources
- Use preemptible instances for batch jobs
- Implement auto-scaling
- Regular cost monitoring and alerts

### Java Example - Cost Monitoring:
```java
public class CostMonitoring {
    private BillingClient billingClient;
    
    public void monitorCosts() {
        // Get current month's costs
        List<BillingAccount> accounts = billingClient.listBillingAccounts();
        
        for (BillingAccount account : accounts) {
            double monthlyCost = getMonthlyCost(account);
            if (monthlyCost > 1000) { // Alert if over $1000
                sendCostAlert(account, monthlyCost);
            }
        }
    }
    
    private void sendCostAlert(BillingAccount account, double cost) {
        System.out.println("Cost alert: $" + cost + " for account " + account.getName());
    }
}
```

## 1.8 GCP Free Tier and Credits

GCP offers generous free tier services and credits to help users get started and experiment with cloud services.

### Free Tier Services:
- **Compute Engine**: 1 f1-micro instance per month
- **Cloud Storage**: 5GB standard storage
- **Cloud Functions**: 2 million invocations per month
- **BigQuery**: 1TB queries per month
- **Cloud SQL**: 1 f1-micro instance per month

### Credit Programs:
- **$300 free credits** for new users
- **Always Free** services with usage limits
- **Student credits** for educational institutions
- **Startup credits** for qualifying companies

### Java Example - Free Tier Monitoring:
```java
public class FreeTierMonitoring {
    public void checkFreeTierUsage() {
        // Monitor Compute Engine usage
        int instances = getComputeEngineInstances();
        if (instances > 1) {
            System.out.println("Warning: Using " + instances + " instances, free tier allows 1");
        }
        
        // Monitor Cloud Storage usage
        long storageGB = getCloudStorageUsage();
        if (storageGB > 5) {
            System.out.println("Warning: Using " + storageGB + "GB, free tier allows 5GB");
        }
    }
    
    private int getComputeEngineInstances() {
        // Query GCP API for instance count
        return 1; // Placeholder
    }
    
    private long getCloudStorageUsage() {
        // Query GCP API for storage usage
        return 3; // Placeholder
    }
}
```