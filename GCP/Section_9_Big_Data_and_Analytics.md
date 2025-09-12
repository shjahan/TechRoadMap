# Section 9 – Big Data and Analytics

## 9.1 BigQuery (Data Warehouse)

BigQuery is a fully managed data warehouse for analytics.

### Key Features:
- Serverless Data Warehouse
- SQL Queries
- Real-time Analytics
- Machine Learning Integration

### Java Example:
```java
import com.google.cloud.bigquery.*;

public class BigQueryManager {
    private BigQuery bigquery;
    
    public void createDataset(String projectId, String datasetId) {
        DatasetInfo datasetInfo = DatasetInfo.newBuilder(datasetId)
            .setLocation("US")
            .build();
        
        Dataset dataset = bigquery.create(datasetInfo);
        System.out.println("Dataset created: " + dataset.getDatasetId());
    }
    
    public void createTable(String datasetId, String tableId, Schema schema) {
        TableId tableIdObj = TableId.of(datasetId, tableId);
        TableDefinition tableDefinition = StandardTableDefinition.of(schema);
        TableInfo tableInfo = TableInfo.newBuilder(tableIdObj, tableDefinition).build();
        
        Table table = bigquery.create(tableInfo);
        System.out.println("Table created: " + table.getTableId());
    }
}
```

## 9.2 Cloud Dataflow (Stream and Batch Processing)

Cloud Dataflow is a fully managed service for stream and batch processing.

### Key Features:
- Apache Beam
- Auto-scaling
- Serverless
- Real-time Processing

### Java Example:
```java
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.transforms.Count;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.values.TypeDescriptors;

public class DataflowManager {
    public void createBatchPipeline(String inputPath, String outputPath) {
        Pipeline pipeline = Pipeline.create();
        
        pipeline.apply("ReadLines", TextIO.read().from(inputPath))
                .apply("CountWords", Count.perElement())
                .apply("FormatOutput", MapElements.into(TypeDescriptors.strings())
                    .via(wordCount -> wordCount.getKey() + ": " + wordCount.getValue()))
                .apply("WriteResults", TextIO.write().to(outputPath));
        
        System.out.println("Batch pipeline created");
    }
}
```

## 9.3 Cloud Dataproc (Managed Spark and Hadoop)

Cloud Dataproc provides managed Spark and Hadoop clusters.

### Key Features:
- Managed Clusters
- Auto-scaling
- Preemptible Instances
- Integration with GCP Services

### Java Example:
```java
import com.google.cloud.dataproc.v1.*;

public class DataprocManager {
    private ClusterControllerClient clusterClient;
    
    public void createCluster(String projectId, String region, String clusterName) {
        Cluster cluster = Cluster.newBuilder()
            .setClusterName(clusterName)
            .setConfig(ClusterConfig.newBuilder()
                .setGceClusterConfig(GceClusterConfig.newBuilder()
                    .setZoneUri(region + "-a")
                    .build())
                .setMasterConfig(InstanceGroupConfig.newBuilder()
                    .setNumInstances(1)
                    .setMachineTypeUri("n1-standard-1")
                    .build())
                .setWorkerConfig(InstanceGroupConfig.newBuilder()
                    .setNumInstances(2)
                    .setMachineTypeUri("n1-standard-1")
                    .build())
                .build())
            .build();
        
        System.out.println("Dataproc cluster created: " + clusterName);
    }
}
```

## 9.4 Cloud Data Fusion (Data Integration)

Cloud Data Fusion provides visual data integration and ETL.

### Key Features:
- Visual ETL
- Pre-built Connectors
- Data Pipeline Management
- Real-time Processing

### Java Example:
```java
public class DataFusionManager {
    public void createPipeline(String projectId, String pipelineName) {
        System.out.println("Data Fusion pipeline created: " + pipelineName);
    }
    
    public void runPipeline(String pipelineName) {
        System.out.println("Pipeline started: " + pipelineName);
    }
}
```

## 9.5 Cloud Composer (Managed Apache Airflow)

Cloud Composer provides managed Apache Airflow for workflow orchestration.

### Key Features:
- Managed Airflow
- Python DAGs
- Workflow Orchestration
- Monitoring and Logging

### Java Example:
```java
public class ComposerManager {
    public void createEnvironment(String projectId, String environmentName) {
        System.out.println("Composer environment created: " + environmentName);
    }
    
    public void deployDAG(String environmentName, String dagName) {
        System.out.println("DAG deployed: " + dagName);
    }
}
```

## 9.6 Cloud Pub/Sub (Messaging Service)

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

## 9.7 Cloud Data Loss Prevention

Cloud DLP helps discover, classify, and protect sensitive data.

### Key Features:
- Data Discovery
- Classification
- Masking
- De-identification

### Java Example:
```java
import com.google.cloud.dlp.v2.*;

public class DLPManager {
    private DlpServiceClient dlpClient;
    
    public void inspectData(String projectId, String text) {
        System.out.println("Data inspection completed for: " + text);
    }
    
    public void deidentifyData(String projectId, String text) {
        System.out.println("Data de-identified: " + text);
    }
}
```

## 9.8 Cloud Data Catalog

Cloud Data Catalog provides metadata management and discovery.

### Key Features:
- Metadata Discovery
- Data Lineage
- Search and Discovery
- Integration with BigQuery

### Java Example:
```java
public class DataCatalogManager {
    public void createEntryGroup(String projectId, String location, String entryGroupId) {
        System.out.println("Entry group created: " + entryGroupId);
    }
    
    public void createEntry(String entryGroupName, String entryId) {
        System.out.println("Entry created: " + entryId);
    }
}
```

## 9.9 Cloud Dataprep

Cloud Dataprep provides visual data preparation and cleaning.

### Key Features:
- Visual Data Prep
- Data Profiling
- Data Cleaning
- Export to BigQuery

### Java Example:
```java
public class DataprepManager {
    public void createDataset(String projectId, String datasetName) {
        System.out.println("Dataprep dataset created: " + datasetName);
    }
    
    public void createRecipe(String datasetName, String recipeName) {
        System.out.println("Recipe created: " + recipeName);
    }
}
```

## 9.10 Data Studio

Data Studio provides interactive dashboards and reports.

### Key Features:
- Interactive Dashboards
- Real-time Data
- Collaboration
- Custom Visualizations

### Java Example:
```java
public class DataStudioManager {
    public void createReport(String reportName) {
        System.out.println("Data Studio report created: " + reportName);
    }
    
    public void addDataSource(String reportName, String dataSourceName) {
        System.out.println("Data source added: " + dataSourceName);
    }
}
```