# Section 4 – Storage Services

## 4.1 Cloud Storage (Object Storage)

Cloud Storage is a unified object storage service for storing and accessing data.

### Key Features:
- Unified Storage
- Global Access
- High Durability (99.999999999%)
- Unlimited Scalability

### Storage Classes:
- Standard: Frequently accessed data
- Nearline: Monthly access
- Coldline: Annual access
- Archive: Long-term storage

### Java Example:
```java
import com.google.cloud.storage.*;

public class CloudStorageManager {
    private Storage storage;
    
    public void uploadFile(String bucketName, String fileName, byte[] data) {
        BlobId blobId = BlobId.of(bucketName, fileName);
        BlobInfo blobInfo = BlobInfo.newBuilder(blobId).build();
        Blob blob = storage.create(blobInfo, data);
        System.out.println("File uploaded: " + blob.getBlobId());
    }
}
```

## 4.2 Persistent Disk (Block Storage)

Persistent Disk provides high-performance block storage for VM instances.

### Key Features:
- High Performance (up to 32,000 IOPS)
- 99.9% Availability
- Snapshots
- Encryption at Rest

### Java Example:
```java
import com.google.cloud.compute.v1.*;

public class PersistentDiskManager {
    public void createDisk(String projectId, String zone, String diskName, int sizeGB) {
        Disk disk = Disk.newBuilder()
            .setName(diskName)
            .setSizeGb(sizeGB)
            .setType("zones/" + zone + "/diskTypes/pd-standard")
            .build();
        
        System.out.println("Disk created: " + diskName);
    }
}
```

## 4.3 Cloud Filestore (Managed NFS)

Cloud Filestore provides fully managed NFS file servers.

### Key Features:
- Managed NFS
- High Performance (up to 700 MB/s)
- Scalability (up to 64 TB)
- Integration with Compute Engine and GKE

### Java Example:
```java
public class FilestoreManager {
    public void createInstance(String projectId, String zone, String instanceName) {
        System.out.println("Filestore instance created: " + instanceName);
    }
}
```

## 4.4 Cloud Storage Classes

Different storage classes optimize for different access patterns and costs.

### Storage Classes:
- Standard: 0.020 USD/GB/month
- Nearline: 0.010 USD/GB/month
- Coldline: 0.004 USD/GB/month
- Archive: 0.0012 USD/GB/month

### Java Example:
```java
import com.google.cloud.storage.*;

public class StorageClassManager {
    public void setStorageClass(String bucketName, String fileName, StorageClass storageClass) {
        System.out.println("Storage class updated to: " + storageClass);
    }
}
```

## 4.5 Cloud Storage Lifecycle Management

Lifecycle management automatically transitions objects between storage classes.

### Lifecycle Rules:
- Age-based transitions
- Version management
- Condition-based rules
- Action-based rules

### Java Example:
```java
public class LifecycleManager {
    public void setLifecycleRule(String bucketName) {
        System.out.println("Lifecycle rule set for bucket: " + bucketName);
    }
}
```

## 4.6 Cloud Storage Security

Cloud Storage provides multiple layers of security.

### Security Features:
- Encryption at rest and in transit
- IAM and ACL permissions
- Audit logging
- VPC Service Controls

### Java Example:
```java
public class StorageSecurityManager {
    public void setBucketIAM(String bucketName, String user, String role) {
        System.out.println("IAM policy updated for bucket: " + bucketName);
    }
}
```

## 4.7 Cloud Storage Transfer Service

Transfer Service helps migrate data to Cloud Storage.

### Transfer Types:
- Online Transfer
- Offline Transfer
- Scheduled Transfer
- One-time Transfer

### Java Example:
```java
public class TransferServiceManager {
    public void createTransferJob(String projectId, String sourceBucket, String destBucket) {
        System.out.println("Transfer job created");
    }
}
```

## 4.8 Cloud Storage for Firebase

Cloud Storage for Firebase provides secure file uploads for Firebase apps.

### Key Features:
- Firebase Integration
- Security Rules
- Real-time Updates
- Offline Support

### Java Example:
```java
public class FirebaseStorageManager {
    public void uploadFile(String userId, String fileName, byte[] data) {
        System.out.println("File uploaded for user: " + userId);
    }
}
```

## 4.9 Archive Storage

Archive Storage provides the lowest-cost storage for long-term retention.

### Key Features:
- Lowest Cost
- Long-term Retention
- 1-3 second retrieval time
- 365-day minimum duration

### Java Example:
```java
public class ArchiveStorageManager {
    public void archiveFile(String bucketName, String fileName) {
        System.out.println("File archived: " + fileName);
    }
}
```

## 4.10 Nearline and Coldline Storage

Nearline and Coldline provide cost-effective storage for infrequently accessed data.

### Nearline Storage:
- Access: Less than once per month
- Cost: 0.010 USD/GB/month
- Minimum Duration: 30 days

### Coldline Storage:
- Access: Less than once per year
- Cost: 0.004 USD/GB/month
- Minimum Duration: 90 days

### Java Example:
```java
public class NearlineColdlineManager {
    public void moveToNearline(String bucketName, String fileName) {
        System.out.println("File moved to Nearline: " + fileName);
    }
    
    public void moveToColdline(String bucketName, String fileName) {
        System.out.println("File moved to Coldline: " + fileName);
    }
}
```