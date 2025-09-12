# Section 17 – Big Data and Analytics

## 17.1 Big Data Characteristics (Volume, Velocity, Variety)

Big Data refers to extremely large datasets that traditional data processing applications cannot handle efficiently. The three main characteristics are Volume, Velocity, and Variety, often called the "3 Vs."

### Key Characteristics:
- **Volume**: Massive amounts of data (terabytes, petabytes, exabytes)
- **Velocity**: High speed of data generation and processing
- **Variety**: Different types of data (structured, semi-structured, unstructured)
- **Veracity**: Data quality and reliability
- **Value**: Extracting meaningful insights from data

### Real-World Analogy:
Big Data is like a massive library with:
- **Volume** = Millions of books (data size)
- **Velocity** = New books arriving every second (data speed)
- **Variety** = Books, magazines, videos, audio (data types)
- **Veracity** = Accuracy of information (data quality)
- **Value** = Knowledge gained from reading (insights)

### Java Example - Big Data Processing:
```java
import java.util.*;
import java.util.stream.Collectors;

public class BigDataProcessor {
    private List<DataRecord> dataStore = new ArrayList<>();
    
    // Data record structure
    public static class DataRecord {
        private String id;
        private String type;
        private long timestamp;
        private Map<String, Object> data;
        
        public DataRecord(String id, String type, long timestamp, Map<String, Object> data) {
            this.id = id;
            this.type = type;
            this.timestamp = timestamp;
            this.data = data;
        }
        
        // Getters
        public String getId() { return id; }
        public String getType() { return type; }
        public long getTimestamp() { return timestamp; }
        public Map<String, Object> getData() { return data; }
    }
    
    // Process high-volume data
    public void processHighVolumeData(List<DataRecord> records) {
        System.out.println("Processing " + records.size() + " records");
        
        // Batch processing for volume
        int batchSize = 1000;
        for (int i = 0; i < records.size(); i += batchSize) {
            List<DataRecord> batch = records.subList(i, 
                Math.min(i + batchSize, records.size()));
            processBatch(batch);
        }
    }
    
    // Process high-velocity data
    public void processHighVelocityData(DataRecord record) {
        // Real-time processing
        long currentTime = System.currentTimeMillis();
        if (currentTime - record.getTimestamp() < 1000) { // Within 1 second
            processRealTime(record);
        }
    }
    
    // Process variety of data types
    public void processVarietyData(DataRecord record) {
        switch (record.getType()) {
            case "JSON":
                processJSONData(record);
                break;
            case "XML":
                processXMLData(record);
                break;
            case "CSV":
                processCSVData(record);
                break;
            case "BINARY":
                processBinaryData(record);
                break;
            default:
                processUnknownData(record);
        }
    }
    
    private void processBatch(List<DataRecord> batch) {
        // Process batch of records
        System.out.println("Processing batch of " + batch.size() + " records");
    }
    
    private void processRealTime(DataRecord record) {
        System.out.println("Real-time processing: " + record.getId());
    }
    
    private void processJSONData(DataRecord record) {
        System.out.println("Processing JSON data: " + record.getId());
    }
    
    private void processXMLData(DataRecord record) {
        System.out.println("Processing XML data: " + record.getId());
    }
    
    private void processCSVData(DataRecord record) {
        System.out.println("Processing CSV data: " + record.getId());
    }
    
    private void processBinaryData(DataRecord record) {
        System.out.println("Processing binary data: " + record.getId());
    }
    
    private void processUnknownData(DataRecord record) {
        System.out.println("Processing unknown data type: " + record.getId());
    }
}
```

## 17.2 Hadoop Ecosystem

Hadoop is an open-source framework for distributed storage and processing of large datasets across clusters of computers.

### Core Components:
- **HDFS**: Hadoop Distributed File System
- **MapReduce**: Programming model for processing large datasets
- **YARN**: Yet Another Resource Negotiator
- **HBase**: NoSQL database
- **Hive**: Data warehouse software
- **Pig**: High-level platform for data analysis
- **Sqoop**: Tool for transferring data between Hadoop and relational databases

### Real-World Analogy:
Hadoop is like a massive warehouse system:
- **HDFS** = Warehouse storage (distributed shelves)
- **MapReduce** = Workers processing items (distributed processing)
- **YARN** = Warehouse manager (resource management)
- **HBase** = Quick access storage (fast retrieval)
- **Hive** = Warehouse catalog (data organization)
- **Pig** = Automated processing (batch operations)
- **Sqoop** = Delivery trucks (data transfer)

### Java Example - Hadoop MapReduce:
```java
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCountMapReduce {
    
    // Mapper class
    public static class TokenizerMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();
        
        @Override
        public void map(LongWritable key, Text value, Context context) 
                throws IOException, InterruptedException {
            String line = value.toString();
            String[] words = line.split("\\s+");
            
            for (String w : words) {
                word.set(w.toLowerCase());
                context.write(word, one);
            }
        }
    }
    
    // Reducer class
    public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();
        
        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context) 
                throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }
    
    // Main method
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        
        job.setJarByClass(WordCountMapReduce.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

## 17.3 Apache Spark

Apache Spark is a unified analytics engine for large-scale data processing, providing high-level APIs in Java, Scala, Python, and R.

### Key Features:
- **In-Memory Processing**: Faster than Hadoop MapReduce
- **Unified Platform**: Batch and streaming processing
- **Machine Learning**: Built-in MLlib library
- **Graph Processing**: GraphX for graph analytics
- **SQL Processing**: Spark SQL for structured data
- **Real-time Processing**: Spark Streaming

### Real-World Analogy:
Apache Spark is like a high-speed train system:
- **In-Memory Processing** = Express trains (fast)
- **Unified Platform** = All train types on same tracks
- **Machine Learning** = AI-powered routing
- **Graph Processing** = Network analysis
- **SQL Processing** = Scheduled services
- **Real-time Processing** = Live updates

### Java Example - Spark Processing:
```java
import org.apache.spark.sql.*;
import org.apache.spark.sql.types.*;
import org.apache.spark.sql.functions.*;

public class SparkDataProcessing {
    private SparkSession spark;
    
    public SparkDataProcessing() {
        spark = SparkSession.builder()
            .appName("BigDataProcessing")
            .master("local[*]")
            .getOrCreate();
    }
    
    // Process large dataset with Spark
    public void processLargeDataset(String inputPath, String outputPath) {
        // Read data
        Dataset<Row> df = spark.read()
            .option("header", "true")
            .option("inferSchema", "true")
            .csv(inputPath);
        
        // Transform data
        Dataset<Row> processed = df
            .filter(col("age").gt(18))
            .groupBy("department")
            .agg(
                count("*").alias("employee_count"),
                avg("salary").alias("avg_salary"),
                max("salary").alias("max_salary")
            )
            .orderBy(desc("avg_salary"));
        
        // Write results
        processed.write()
            .mode(SaveMode.Overwrite)
            .option("header", "true")
            .csv(outputPath);
        
        System.out.println("Data processing completed");
    }
    
    // Real-time streaming processing
    public void processStreamingData() {
        Dataset<Row> streamingDF = spark
            .readStream()
            .format("kafka")
            .option("kafka.bootstrap.servers", "localhost:9092")
            .option("subscribe", "bigdata-topic")
            .load();
        
        Dataset<Row> processedStream = streamingDF
            .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
            .filter(col("value").isNotNull());
        
        processedStream.writeStream()
            .outputMode("append")
            .format("console")
            .start()
            .awaitTermination();
    }
    
    // Machine learning with Spark
    public void performMachineLearning() {
        // Load data
        Dataset<Row> data = spark.read()
            .format("libsvm")
            .load("data/sample_libsvm_data.txt");
        
        // Split data
        Dataset<Row>[] splits = data.randomSplit(new double[]{0.7, 0.3});
        Dataset<Row> trainingData = splits[0];
        Dataset<Row> testData = splits[1];
        
        // Train model (simplified example)
        System.out.println("Training machine learning model...");
        System.out.println("Training data size: " + trainingData.count());
        System.out.println("Test data size: " + testData.count());
    }
}
```

## 17.4 Data Lakes

Data lakes are centralized repositories that store raw data in its native format, including structured, semi-structured, and unstructured data.

### Key Features:
- **Raw Data Storage**: Store data in original format
- **Schema-on-Read**: Apply schema when reading data
- **Scalability**: Handle massive amounts of data
- **Flexibility**: Support various data types
- **Cost-Effective**: Lower storage costs
- **Analytics Ready**: Enable various analytics

### Real-World Analogy:
Data lakes are like natural lakes:
- **Raw Data Storage** = Natural water (unprocessed)
- **Schema-on-Read** = Different ways to use water
- **Scalability** = Lakes can be very large
- **Flexibility** = Various uses (drinking, irrigation, recreation)
- **Cost-Effective** = Natural storage
- **Analytics Ready** = Water analysis capabilities

### Java Example - Data Lake Operations:
```java
import java.util.*;
import java.io.*;

public class DataLakeManager {
    private Map<String, List<DataObject>> dataLake = new HashMap<>();
    
    // Data object structure
    public static class DataObject {
        private String id;
        private String type;
        private byte[] data;
        private Map<String, String> metadata;
        private long timestamp;
        
        public DataObject(String id, String type, byte[] data, Map<String, String> metadata) {
            this.id = id;
            this.type = type;
            this.data = data;
            this.metadata = metadata;
            this.timestamp = System.currentTimeMillis();
        }
        
        // Getters
        public String getId() { return id; }
        public String getType() { return type; }
        public byte[] getData() { return data; }
        public Map<String, String> getMetadata() { return metadata; }
        public long getTimestamp() { return timestamp; }
    }
    
    // Store raw data
    public void storeRawData(String dataType, DataObject dataObject) {
        dataLake.computeIfAbsent(dataType, k -> new ArrayList<>()).add(dataObject);
        System.out.println("Stored raw data: " + dataObject.getId() + " of type: " + dataType);
    }
    
    // Query data with schema-on-read
    public List<DataObject> queryData(String dataType, Map<String, String> filters) {
        List<DataObject> results = new ArrayList<>();
        List<DataObject> dataObjects = dataLake.get(dataType);
        
        if (dataObjects != null) {
            for (DataObject obj : dataObjects) {
                if (matchesFilters(obj, filters)) {
                    results.add(obj);
                }
            }
        }
        
        return results;
    }
    
    // Apply schema when reading
    public void applySchemaOnRead(String dataType, String schema) {
        List<DataObject> dataObjects = dataLake.get(dataType);
        
        if (dataObjects != null) {
            System.out.println("Applying schema '" + schema + "' to " + dataObjects.size() + " objects");
            
            for (DataObject obj : dataObjects) {
                processWithSchema(obj, schema);
            }
        }
    }
    
    // Data lake analytics
    public void performAnalytics(String dataType) {
        List<DataObject> dataObjects = dataLake.get(dataType);
        
        if (dataObjects != null) {
            System.out.println("Performing analytics on " + dataObjects.size() + " objects");
            
            // Calculate statistics
            long totalSize = dataObjects.stream()
                .mapToLong(obj -> obj.getData().length)
                .sum();
            
            double avgSize = dataObjects.stream()
                .mapToLong(obj -> obj.getData().length)
                .average()
                .orElse(0.0);
            
            System.out.println("Total size: " + totalSize + " bytes");
            System.out.println("Average size: " + avgSize + " bytes");
        }
    }
    
    private boolean matchesFilters(DataObject obj, Map<String, String> filters) {
        for (Map.Entry<String, String> filter : filters.entrySet()) {
            String key = filter.getKey();
            String value = filter.getValue();
            
            if (obj.getMetadata().containsKey(key)) {
                if (!obj.getMetadata().get(key).equals(value)) {
                    return false;
                }
            } else {
                return false;
            }
        }
        return true;
    }
    
    private void processWithSchema(DataObject obj, String schema) {
        System.out.println("Processing " + obj.getId() + " with schema: " + schema);
    }
}
```

## 17.5 Stream Processing

Stream processing involves real-time processing of continuous data streams, enabling immediate analysis and response to data as it arrives.

### Key Features:
- **Real-time Processing**: Process data as it arrives
- **Low Latency**: Minimal delay between data arrival and processing
- **Scalability**: Handle high-volume streams
- **Fault Tolerance**: Continue processing despite failures
- **Event Time**: Process data based on event timestamps
- **Windowing**: Group events into time windows

### Real-World Analogy:
Stream processing is like a live news broadcast:
- **Real-time Processing** = Live reporting
- **Low Latency** = Immediate updates
- **Scalability** = Multiple news channels
- **Fault Tolerance** = Backup systems
- **Event Time** = When events actually happened
- **Windowing** = News segments (hourly, daily)

### Java Example - Stream Processing:
```java
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.*;

public class StreamProcessor {
    private BlockingQueue<DataEvent> eventQueue = new LinkedBlockingQueue<>();
    private List<StreamProcessor> processors = new ArrayList<>();
    private volatile boolean running = false;
    
    // Data event structure
    public static class DataEvent {
        private String id;
        private String type;
        private Map<String, Object> data;
        private long timestamp;
        
        public DataEvent(String id, String type, Map<String, Object> data) {
            this.id = id;
            this.type = type;
            this.data = data;
            this.timestamp = System.currentTimeMillis();
        }
        
        // Getters
        public String getId() { return id; }
        public String getType() { return type; }
        public Map<String, Object> getData() { return data; }
        public long getTimestamp() { return timestamp; }
    }
    
    // Start stream processing
    public void startProcessing() {
        running = true;
        
        // Start multiple processing threads
        for (int i = 0; i < 4; i++) {
            Thread processor = new Thread(this::processEvents);
            processor.start();
        }
        
        System.out.println("Stream processing started");
    }
    
    // Stop stream processing
    public void stopProcessing() {
        running = false;
        System.out.println("Stream processing stopped");
    }
    
    // Add event to stream
    public void addEvent(DataEvent event) {
        try {
            eventQueue.put(event);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Process events from queue
    private void processEvents() {
        while (running) {
            try {
                DataEvent event = eventQueue.take();
                processEvent(event);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    // Process individual event
    private void processEvent(DataEvent event) {
        System.out.println("Processing event: " + event.getId() + 
                         " of type: " + event.getType() + 
                         " at: " + new Date(event.getTimestamp()));
        
        // Apply different processing based on event type
        switch (event.getType()) {
            case "SENSOR_DATA":
                processSensorData(event);
                break;
            case "USER_ACTION":
                processUserAction(event);
                break;
            case "SYSTEM_LOG":
                processSystemLog(event);
                break;
            default:
                processGenericEvent(event);
        }
    }
    
    // Process sensor data
    private void processSensorData(DataEvent event) {
        Map<String, Object> data = event.getData();
        Double value = (Double) data.get("value");
        
        if (value != null && value > 100.0) {
            System.out.println("High sensor reading detected: " + value);
            // Trigger alert
        }
    }
    
    // Process user action
    private void processUserAction(DataEvent event) {
        Map<String, Object> data = event.getData();
        String action = (String) data.get("action");
        
        System.out.println("User performed action: " + action);
        // Update user analytics
    }
    
    // Process system log
    private void processSystemLog(DataEvent event) {
        Map<String, Object> data = event.getData();
        String level = (String) data.get("level");
        
        if ("ERROR".equals(level)) {
            System.out.println("Error detected in system log: " + event.getId());
            // Trigger error handling
        }
    }
    
    // Process generic event
    private void processGenericEvent(DataEvent event) {
        System.out.println("Processing generic event: " + event.getId());
    }
    
    // Window-based processing
    public void processWindowedData(List<DataEvent> events, long windowSizeMs) {
        long currentTime = System.currentTimeMillis();
        long windowStart = currentTime - windowSizeMs;
        
        List<DataEvent> windowEvents = events.stream()
            .filter(event -> event.getTimestamp() >= windowStart)
            .collect(Collectors.toList());
        
        System.out.println("Processing " + windowEvents.size() + " events in window");
        
        // Calculate window statistics
        double avgValue = windowEvents.stream()
            .mapToDouble(event -> {
                Object value = event.getData().get("value");
                return value instanceof Number ? ((Number) value).doubleValue() : 0.0;
            })
            .average()
            .orElse(0.0);
        
        System.out.println("Average value in window: " + avgValue);
    }
}
```

## 17.6 Machine Learning with Databases

Machine learning with databases involves integrating ML algorithms with database systems to enable intelligent data processing and predictive analytics.

### Key Features:
- **Data Preparation**: Clean and prepare data for ML
- **Feature Engineering**: Create meaningful features
- **Model Training**: Train ML models on database data
- **Model Deployment**: Deploy models for real-time prediction
- **Model Management**: Version and manage ML models
- **Performance Monitoring**: Monitor model performance

### Real-World Analogy:
Machine learning with databases is like having a smart librarian:
- **Data Preparation** = Organizing books
- **Feature Engineering** = Creating book categories
- **Model Training** = Learning from book patterns
- **Model Deployment** = Making recommendations
- **Model Management** = Updating recommendations
- **Performance Monitoring** = Tracking recommendation accuracy

### Java Example - ML with Databases:
```java
import java.util.*;
import java.sql.*;

public class MachineLearningWithDatabase {
    private Connection connection;
    
    public MachineLearningWithDatabase(Connection connection) {
        this.connection = connection;
    }
    
    // Prepare data for ML training
    public List<MLDataPoint> prepareTrainingData(String query) throws SQLException {
        List<MLDataPoint> trainingData = new ArrayList<>();
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(query)) {
            
            while (rs.next()) {
                MLDataPoint dataPoint = new MLDataPoint();
                dataPoint.setId(rs.getInt("id"));
                dataPoint.setFeatures(extractFeatures(rs));
                dataPoint.setLabel(rs.getDouble("label"));
                trainingData.add(dataPoint);
            }
        }
        
        System.out.println("Prepared " + trainingData.size() + " training data points");
        return trainingData;
    }
    
    // Extract features from database row
    private Map<String, Double> extractFeatures(ResultSet rs) throws SQLException {
        Map<String, Double> features = new HashMap<>();
        
        // Extract numerical features
        features.put("age", rs.getDouble("age"));
        features.put("income", rs.getDouble("income"));
        features.put("credit_score", rs.getDouble("credit_score"));
        
        // Extract categorical features (encoded)
        features.put("gender_male", rs.getString("gender").equals("M") ? 1.0 : 0.0);
        features.put("education_college", rs.getString("education").equals("college") ? 1.0 : 0.0);
        
        return features;
    }
    
    // Train ML model
    public MLModel trainModel(List<MLDataPoint> trainingData) {
        System.out.println("Training ML model with " + trainingData.size() + " data points");
        
        // Simple linear regression model (simplified)
        MLModel model = new MLModel();
        model.train(trainingData);
        
        System.out.println("Model training completed");
        return model;
    }
    
    // Make predictions using trained model
    public List<Prediction> makePredictions(MLModel model, String query) throws SQLException {
        List<Prediction> predictions = new ArrayList<>();
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(query)) {
            
            while (rs.next()) {
                Map<String, Double> features = extractFeatures(rs);
                double prediction = model.predict(features);
                
                Prediction pred = new Prediction();
                pred.setId(rs.getInt("id"));
                pred.setPrediction(prediction);
                pred.setConfidence(calculateConfidence(features));
                predictions.add(pred);
            }
        }
        
        return predictions;
    }
    
    // Store predictions back to database
    public void storePredictions(List<Prediction> predictions) throws SQLException {
        String sql = "INSERT INTO predictions (id, prediction, confidence, created_at) VALUES (?, ?, ?, ?)";
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            for (Prediction pred : predictions) {
                stmt.setInt(1, pred.getId());
                stmt.setDouble(2, pred.getPrediction());
                stmt.setDouble(3, pred.getConfidence());
                stmt.setTimestamp(4, new Timestamp(System.currentTimeMillis()));
                stmt.addBatch();
            }
            
            stmt.executeBatch();
            System.out.println("Stored " + predictions.size() + " predictions");
        }
    }
    
    // Monitor model performance
    public void monitorModelPerformance(String modelId) throws SQLException {
        String sql = """
            SELECT 
                AVG(ABS(actual - prediction)) as mae,
                AVG(POWER(actual - prediction, 2)) as mse,
                COUNT(*) as prediction_count
            FROM model_evaluations 
            WHERE model_id = ? AND created_at >= DATE_SUB(NOW(), INTERVAL 1 DAY)
            """;
        
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, modelId);
            
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    double mae = rs.getDouble("mae");
                    double mse = rs.getDouble("mse");
                    int count = rs.getInt("prediction_count");
                    
                    System.out.println("Model Performance Metrics:");
                    System.out.println("Mean Absolute Error: " + mae);
                    System.out.println("Mean Squared Error: " + mse);
                    System.out.println("Prediction Count: " + count);
                }
            }
        }
    }
    
    private double calculateConfidence(Map<String, Double> features) {
        // Simple confidence calculation based on feature completeness
        long nonZeroFeatures = features.values().stream()
            .mapToLong(v -> v != 0.0 ? 1 : 0)
            .sum();
        
        return (double) nonZeroFeatures / features.size();
    }
    
    // ML Data Point class
    public static class MLDataPoint {
        private int id;
        private Map<String, Double> features;
        private double label;
        
        // Getters and setters
        public int getId() { return id; }
        public void setId(int id) { this.id = id; }
        public Map<String, Double> getFeatures() { return features; }
        public void setFeatures(Map<String, Double> features) { this.features = features; }
        public double getLabel() { return label; }
        public void setLabel(double label) { this.label = label; }
    }
    
    // ML Model class
    public static class MLModel {
        private Map<String, Double> weights = new HashMap<>();
        
        public void train(List<MLDataPoint> trainingData) {
            // Simplified training (in practice, use proper ML libraries)
            System.out.println("Training model with " + trainingData.size() + " samples");
        }
        
        public double predict(Map<String, Double> features) {
            // Simplified prediction (in practice, use proper ML libraries)
            return Math.random() * 100; // Placeholder
        }
    }
    
    // Prediction class
    public static class Prediction {
        private int id;
        private double prediction;
        private double confidence;
        
        // Getters and setters
        public int getId() { return id; }
        public void setId(int id) { this.id = id; }
        public double getPrediction() { return prediction; }
        public void setPrediction(double prediction) { this.prediction = prediction; }
        public double getConfidence() { return confidence; }
        public void setConfidence(double confidence) { this.confidence = confidence; }
    }
}
```

## 17.7 Real-time Analytics

Real-time analytics involves analyzing data as it arrives to provide immediate insights and enable quick decision-making.

### Key Features:
- **Stream Processing**: Process data streams in real-time
- **Low Latency**: Minimal delay between data arrival and analysis
- **Continuous Analysis**: Ongoing analysis of incoming data
- **Alert Generation**: Immediate notifications for important events
- **Dashboard Updates**: Real-time visualization of data
- **Decision Support**: Enable quick decision-making

### Real-World Analogy:
Real-time analytics is like a live sports broadcast:
- **Stream Processing** = Live commentary
- **Low Latency** = Immediate updates
- **Continuous Analysis** = Ongoing game analysis
- **Alert Generation** = Breaking news alerts
- **Dashboard Updates** = Live score updates
- **Decision Support** = Instant replays

### Java Example - Real-time Analytics:
```java
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

public class RealTimeAnalytics {
    private Map<String, Double> metrics = new ConcurrentHashMap<>();
    private List<Alert> alerts = new ArrayList<>();
    private BlockingQueue<DataPoint> dataStream = new LinkedBlockingQueue<>();
    private volatile boolean running = false;
    
    // Data point structure
    public static class DataPoint {
        private String metric;
        private double value;
        private long timestamp;
        private Map<String, String> tags;
        
        public DataPoint(String metric, double value, Map<String, String> tags) {
            this.metric = metric;
            this.value = value;
            this.timestamp = System.currentTimeMillis();
            this.tags = tags;
        }
        
        // Getters
        public String getMetric() { return metric; }
        public double getValue() { return value; }
        public long getTimestamp() { return timestamp; }
        public Map<String, String> getTags() { return tags; }
    }
    
    // Alert structure
    public static class Alert {
        private String id;
        private String message;
        private String severity;
        private long timestamp;
        
        public Alert(String id, String message, String severity) {
            this.id = id;
            this.message = message;
            this.severity = severity;
            this.timestamp = System.currentTimeMillis();
        }
        
        // Getters
        public String getId() { return id; }
        public String getMessage() { return message; }
        public String getSeverity() { return severity; }
        public long getTimestamp() { return timestamp; }
    }
    
    // Start real-time analytics
    public void startAnalytics() {
        running = true;
        
        // Start processing thread
        Thread processor = new Thread(this::processDataStream);
        processor.start();
        
        // Start alert checking thread
        Thread alertChecker = new Thread(this::checkAlerts);
        alertChecker.start();
        
        System.out.println("Real-time analytics started");
    }
    
    // Stop real-time analytics
    public void stopAnalytics() {
        running = false;
        System.out.println("Real-time analytics stopped");
    }
    
    // Add data point to stream
    public void addDataPoint(DataPoint dataPoint) {
        try {
            dataStream.put(dataPoint);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Process data stream
    private void processDataStream() {
        while (running) {
            try {
                DataPoint dataPoint = dataStream.take();
                processDataPoint(dataPoint);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    // Process individual data point
    private void processDataPoint(DataPoint dataPoint) {
        String metric = dataPoint.getMetric();
        double value = dataPoint.getValue();
        
        // Update metrics
        metrics.put(metric, value);
        
        // Calculate moving average
        double movingAvg = calculateMovingAverage(metric, value);
        
        // Check for anomalies
        if (isAnomaly(metric, value, movingAvg)) {
            generateAlert(metric, value, movingAvg);
        }
        
        // Update dashboard
        updateDashboard(metric, value, movingAvg);
        
        System.out.println("Processed: " + metric + " = " + value + 
                         " (MA: " + movingAvg + ")");
    }
    
    // Calculate moving average
    private double calculateMovingAverage(String metric, double value) {
        // Simplified moving average calculation
        Double currentValue = metrics.get(metric);
        if (currentValue == null) {
            return value;
        }
        
        // Simple exponential moving average
        double alpha = 0.1; // Smoothing factor
        return alpha * value + (1 - alpha) * currentValue;
    }
    
    // Check for anomalies
    private boolean isAnomaly(String metric, double value, double movingAvg) {
        double threshold = 2.0; // 2 standard deviations
        double difference = Math.abs(value - movingAvg);
        double thresholdValue = movingAvg * threshold;
        
        return difference > thresholdValue;
    }
    
    // Generate alert
    private void generateAlert(String metric, double value, double movingAvg) {
        String alertId = UUID.randomUUID().toString();
        String message = String.format("Anomaly detected in %s: value=%.2f, expected=%.2f", 
                                     metric, value, movingAvg);
        String severity = "HIGH";
        
        Alert alert = new Alert(alertId, message, severity);
        alerts.add(alert);
        
        System.out.println("ALERT: " + message);
    }
    
    // Update dashboard
    private void updateDashboard(String metric, double value, double movingAvg) {
        // In real implementation, this would update a web dashboard
        System.out.println("Dashboard updated: " + metric + " = " + value);
    }
    
    // Check alerts
    private void checkAlerts() {
        while (running) {
            try {
                Thread.sleep(1000); // Check every second
                
                // Process recent alerts
                long currentTime = System.currentTimeMillis();
                List<Alert> recentAlerts = alerts.stream()
                    .filter(alert -> currentTime - alert.getTimestamp() < 60000) // Last minute
                    .collect(Collectors.toList());
                
                if (!recentAlerts.isEmpty()) {
                    System.out.println("Recent alerts: " + recentAlerts.size());
                }
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    // Get current metrics
    public Map<String, Double> getCurrentMetrics() {
        return new HashMap<>(metrics);
    }
    
    // Get recent alerts
    public List<Alert> getRecentAlerts(long timeWindowMs) {
        long currentTime = System.currentTimeMillis();
        return alerts.stream()
            .filter(alert -> currentTime - alert.getTimestamp() < timeWindowMs)
            .collect(Collectors.toList());
    }
    
    // Generate analytics report
    public void generateAnalyticsReport() {
        System.out.println("=== Real-time Analytics Report ===");
        System.out.println("Current Metrics:");
        metrics.forEach((metric, value) -> 
            System.out.println("  " + metric + ": " + value));
        
        System.out.println("\nRecent Alerts:");
        List<Alert> recentAlerts = getRecentAlerts(300000); // Last 5 minutes
        recentAlerts.forEach(alert -> 
            System.out.println("  " + alert.getSeverity() + ": " + alert.getMessage()));
        
        System.out.println("=================================");
    }
}
```

## 17.8 Data Science and Databases

Data science with databases involves using database systems to support data science workflows, including data exploration, feature engineering, and model deployment.

### Key Features:
- **Data Exploration**: Explore and understand data
- **Feature Engineering**: Create meaningful features
- **Data Visualization**: Visualize data patterns
- **Statistical Analysis**: Perform statistical tests
- **Model Deployment**: Deploy ML models
- **Data Pipeline**: End-to-end data processing

### Real-World Analogy:
Data science with databases is like having a research laboratory:
- **Data Exploration** = Examining samples
- **Feature Engineering** = Creating test procedures
- **Data Visualization** = Creating charts and graphs
- **Statistical Analysis** = Running experiments
- **Model Deployment** = Implementing solutions
- **Data Pipeline** = Complete research process

### Java Example - Data Science with Databases:
```java
import java.util.*;
import java.sql.*;
import java.util.stream.Collectors;

public class DataScienceWithDatabase {
    private Connection connection;
    
    public DataScienceWithDatabase(Connection connection) {
        this.connection = connection;
    }
    
    // Explore data
    public void exploreData(String tableName) throws SQLException {
        System.out.println("Exploring data in table: " + tableName);
        
        // Get basic statistics
        String sql = String.format("""
            SELECT 
                COUNT(*) as total_rows,
                COUNT(DISTINCT %s) as unique_values
            FROM %s
            """, getPrimaryKeyColumn(tableName), tableName);
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                System.out.println("Total rows: " + rs.getInt("total_rows"));
                System.out.println("Unique values: " + rs.getInt("unique_values"));
            }
        }
        
        // Get column statistics
        getColumnStatistics(tableName);
    }
    
    // Get column statistics
    private void getColumnStatistics(String tableName) throws SQLException {
        String sql = String.format("""
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE,
                COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '%s'
            """, tableName);
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("\nColumn Statistics:");
            while (rs.next()) {
                System.out.println("  " + rs.getString("COLUMN_NAME") + 
                                 " (" + rs.getString("DATA_TYPE") + ")" +
                                 " - Nullable: " + rs.getString("IS_NULLABLE"));
            }
        }
    }
    
    // Feature engineering
    public void performFeatureEngineering(String tableName) throws SQLException {
        System.out.println("Performing feature engineering on table: " + tableName);
        
        // Create derived features
        String sql = String.format("""
            SELECT 
                *,
                CASE 
                    WHEN age < 30 THEN 'young'
                    WHEN age < 50 THEN 'middle'
                    ELSE 'senior'
                END as age_group,
                income / NULLIF(age, 0) as income_per_age,
                SQRT(income) as sqrt_income
            FROM %s
            """, tableName);
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            int count = 0;
            while (rs.next()) {
                count++;
                // Process each row for feature engineering
                if (count % 1000 == 0) {
                    System.out.println("Processed " + count + " rows");
                }
            }
            
            System.out.println("Feature engineering completed for " + count + " rows");
        }
    }
    
    // Data visualization (simplified)
    public void visualizeData(String tableName, String columnName) throws SQLException {
        System.out.println("Creating visualization for column: " + columnName);
        
        // Get data distribution
        String sql = String.format("""
            SELECT 
                %s,
                COUNT(*) as frequency
            FROM %s
            GROUP BY %s
            ORDER BY frequency DESC
            LIMIT 10
            """, columnName, tableName, columnName);
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            System.out.println("\nTop 10 values in " + columnName + ":");
            while (rs.next()) {
                System.out.println("  " + rs.getString(columnName) + 
                                 ": " + rs.getInt("frequency"));
            }
        }
    }
    
    // Statistical analysis
    public void performStatisticalAnalysis(String tableName, String columnName) throws SQLException {
        System.out.println("Performing statistical analysis on column: " + columnName);
        
        String sql = String.format("""
            SELECT 
                COUNT(*) as count,
                AVG(%s) as mean,
                MIN(%s) as min,
                MAX(%s) as max,
                STDDEV(%s) as stddev,
                VARIANCE(%s) as variance
            FROM %s
            WHERE %s IS NOT NULL
            """, columnName, columnName, columnName, columnName, columnName, tableName, columnName);
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                System.out.println("\nStatistical Summary:");
                System.out.println("  Count: " + rs.getInt("count"));
                System.out.println("  Mean: " + rs.getDouble("mean"));
                System.out.println("  Min: " + rs.getDouble("min"));
                System.out.println("  Max: " + rs.getDouble("max"));
                System.out.println("  Std Dev: " + rs.getDouble("stddev"));
                System.out.println("  Variance: " + rs.getDouble("variance"));
            }
        }
    }
    
    // Deploy model
    public void deployModel(String modelName, String modelVersion) throws SQLException {
        System.out.println("Deploying model: " + modelName + " version: " + modelVersion);
        
        // Create model deployment table
        String sql = """
            CREATE TABLE IF NOT EXISTS model_deployments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                model_name VARCHAR(255),
                model_version VARCHAR(50),
                deployment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'ACTIVE'
            )
            """;
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        // Insert deployment record
        sql = "INSERT INTO model_deployments (model_name, model_version) VALUES (?, ?)";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, modelName);
            stmt.setString(2, modelVersion);
            stmt.executeUpdate();
        }
        
        System.out.println("Model deployed successfully");
    }
    
    // Create data pipeline
    public void createDataPipeline(String sourceTable, String targetTable) throws SQLException {
        System.out.println("Creating data pipeline from " + sourceTable + " to " + targetTable);
        
        // Create target table
        String sql = String.format("""
            CREATE TABLE IF NOT EXISTS %s AS
            SELECT 
                *,
                CURRENT_TIMESTAMP as processed_at
            FROM %s
            WHERE 1=0
            """, targetTable, sourceTable);
        
        try (Statement stmt = connection.createStatement()) {
            stmt.execute(sql);
        }
        
        // Copy data
        sql = String.format("""
            INSERT INTO %s
            SELECT 
                *,
                CURRENT_TIMESTAMP as processed_at
            FROM %s
            """, targetTable, sourceTable);
        
        try (Statement stmt = connection.createStatement()) {
            int rowsAffected = stmt.executeUpdate(sql);
            System.out.println("Data pipeline created: " + rowsAffected + " rows processed");
        }
    }
    
    // Get primary key column
    private String getPrimaryKeyColumn(String tableName) throws SQLException {
        String sql = String.format("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_NAME = '%s' AND CONSTRAINT_NAME = 'PRIMARY'
            LIMIT 1
            """, tableName);
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            if (rs.next()) {
                return rs.getString("COLUMN_NAME");
            }
        }
        
        return "id"; // Default fallback
    }
}
```