# Section 20 – Concurrency in Machine Learning

## 20.1 Parallel Training

Parallel training distributes machine learning model training across multiple processors or machines to reduce training time and handle large datasets.

### Key Concepts
- **Data Parallelism**: Splitting data across multiple workers
- **Model Parallelism**: Splitting model across multiple workers
- **Gradient Synchronization**: Coordinating gradient updates across workers
- **Load Balancing**: Ensuring even distribution of work

### Real-World Analogy
Think of training a team of doctors. Instead of having one doctor learn from all medical cases sequentially, you can have multiple doctors learn from different sets of cases in parallel, then share their knowledge to create a more comprehensive understanding.

### Java Example
```java
// Parallel training service
@Service
public class ParallelTrainingService {
    private final ExecutorService trainingPool;
    private final ModelRepository modelRepository;
    private final DataSplitter dataSplitter;
    
    public ParallelTrainingService(@Value("${training.threads}") int threadCount) {
        this.trainingPool = Executors.newFixedThreadPool(threadCount);
        this.modelRepository = new ModelRepository();
        this.dataSplitter = new DataSplitter();
    }
    
    public Model trainModelParallel(List<TrainingData> trainingData, ModelConfig config) {
        // Split data across workers
        List<List<TrainingData>> dataSplits = dataSplitter.splitData(trainingData, config.getWorkerCount());
        
        // Create initial model
        Model globalModel = new Model(config);
        
        // Training epochs
        for (int epoch = 0; epoch < config.getEpochs(); epoch++) {
            List<CompletableFuture<Model>> trainingFutures = new ArrayList<>();
            
            // Train on each data split in parallel
            for (int i = 0; i < dataSplits.size(); i++) {
                final int workerId = i;
                final List<TrainingData> workerData = dataSplits.get(i);
                final Model workerModel = globalModel.copy();
                
                CompletableFuture<Model> future = CompletableFuture.supplyAsync(() -> {
                    return trainWorkerModel(workerModel, workerData, config);
                }, trainingPool);
                
                trainingFutures.add(future);
            }
            
            // Wait for all workers to complete
            CompletableFuture<Void> allWorkers = CompletableFuture.allOf(
                trainingFutures.toArray(new CompletableFuture[0])
            );
            
            // Aggregate gradients from all workers
            allWorkers.thenRun(() -> {
                List<Model> workerModels = trainingFutures.stream()
                    .map(CompletableFuture::join)
                    .collect(Collectors.toList());
                
                // Average gradients across workers
                globalModel.averageGradients(workerModels);
                
                // Update global model
                globalModel.updateWeights();
            }).join();
            
            System.out.println("Epoch " + epoch + " completed");
        }
        
        return globalModel;
    }
    
    private Model trainWorkerModel(Model model, List<TrainingData> data, ModelConfig config) {
        // Train model on worker data
        for (TrainingData sample : data) {
            // Forward pass
            Prediction prediction = model.predict(sample.getFeatures());
            
            // Calculate loss
            double loss = calculateLoss(prediction, sample.getLabel());
            
            // Backward pass
            model.backward(loss);
            
            // Update weights
            model.updateWeights();
        }
        
        return model;
    }
    
    private double calculateLoss(Prediction prediction, double actual) {
        // Mean squared error
        double error = prediction.getValue() - actual;
        return error * error;
    }
}
```

## 20.2 Distributed Training

Distributed training extends parallel training across multiple machines, enabling training of very large models on massive datasets.

### Key Concepts
- **Parameter Server**: Centralized parameter storage and updates
- **All-Reduce**: Collective communication for gradient aggregation
- **Fault Tolerance**: Handling worker failures during training
- **Network Optimization**: Minimizing communication overhead

### Real-World Analogy
Think of a global research project where scientists in different countries work on the same problem. Each team works on their local data and shares their findings with a central coordinator, who combines all insights to create a comprehensive solution.

### Java Example
```java
// Distributed training coordinator
@Service
public class DistributedTrainingCoordinator {
    private final ParameterServer parameterServer;
    private final WorkerManager workerManager;
    private final CommunicationService communicationService;
    
    public Model trainDistributed(List<WorkerNode> workers, ModelConfig config) {
        // Initialize parameter server
        parameterServer.initialize(config);
        
        // Start workers
        List<CompletableFuture<Void>> workerFutures = workers.stream()
            .map(worker -> startWorker(worker, config))
            .collect(Collectors.toList());
        
        // Training loop
        for (int epoch = 0; epoch < config.getEpochs(); epoch++) {
            // Wait for all workers to complete current epoch
            CompletableFuture.allOf(workerFutures.toArray(new CompletableFuture[0])).join();
            
            // Aggregate gradients from all workers
            aggregateGradients(workers);
            
            // Update global parameters
            parameterServer.updateParameters();
            
            // Broadcast updated parameters to all workers
            broadcastParameters(workers);
            
            System.out.println("Epoch " + epoch + " completed");
        }
        
        return parameterServer.getModel();
    }
    
    private CompletableFuture<Void> startWorker(WorkerNode worker, ModelConfig config) {
        return CompletableFuture.runAsync(() -> {
            try {
                // Send initial parameters to worker
                Model initialModel = parameterServer.getModel();
                communicationService.sendModel(worker, initialModel);
                
                // Training loop
                for (int epoch = 0; epoch < config.getEpochs(); epoch++) {
                    // Train on worker data
                    Model updatedModel = worker.trainEpoch(initialModel);
                    
                    // Send gradients back to parameter server
                    Gradients gradients = calculateGradients(initialModel, updatedModel);
                    communicationService.sendGradients(worker, gradients);
                    
                    // Wait for updated parameters
                    Model newModel = communicationService.receiveModel(worker);
                    initialModel = newModel;
                }
                
            } catch (Exception e) {
                System.err.println("Worker " + worker.getId() + " failed: " + e.getMessage());
                handleWorkerFailure(worker);
            }
        });
    }
    
    private void aggregateGradients(List<WorkerNode> workers) {
        List<Gradients> allGradients = workers.stream()
            .map(worker -> communicationService.receiveGradients(worker))
            .collect(Collectors.toList());
        
        // Average gradients
        Gradients averagedGradients = averageGradients(allGradients);
        parameterServer.updateGradients(averagedGradients);
    }
    
    private void broadcastParameters(List<WorkerNode> workers) {
        Model updatedModel = parameterServer.getModel();
        workers.parallelStream().forEach(worker -> {
            communicationService.sendModel(worker, updatedModel);
        });
    }
    
    private void handleWorkerFailure(WorkerNode failedWorker) {
        // Remove failed worker from active workers
        workerManager.removeWorker(failedWorker);
        
        // Redistribute data if necessary
        if (workerManager.getActiveWorkerCount() > 0) {
            redistributeData(failedWorker);
        }
    }
}
```

## 20.3 Model Parallelism

Model parallelism splits large models across multiple devices or machines, enabling training of models that don't fit on a single device.

### Key Concepts
- **Layer Splitting**: Distributing model layers across devices
- **Pipeline Parallelism**: Processing different batches through different pipeline stages
- **Communication Overhead**: Minimizing data transfer between devices
- **Load Balancing**: Ensuring even distribution of model components

### Real-World Analogy
Think of a factory assembly line where different stations handle different parts of a product. Each station specializes in specific components, and the product moves through the line, with each station adding its specialized contribution.

### Java Example
```java
// Model parallelism implementation
@Service
public class ModelParallelismService {
    private final List<Device> devices;
    private final CommunicationService communicationService;
    
    public Model trainModelParallel(ModelConfig config) {
        // Split model across devices
        List<ModelLayer> layers = splitModelLayers(config);
        Map<Device, List<ModelLayer>> deviceLayers = assignLayersToDevices(layers);
        
        // Initialize layers on each device
        deviceLayers.forEach((device, layers) -> {
            device.initializeLayers(layers);
        });
        
        // Training loop
        for (int epoch = 0; epoch < config.getEpochs(); epoch++) {
            trainEpochParallel(deviceLayers, config);
        }
        
        // Combine layers from all devices
        return combineModelLayers(deviceLayers);
    }
    
    private void trainEpochParallel(Map<Device, List<ModelLayer>> deviceLayers, ModelConfig config) {
        List<TrainingData> batch = getNextBatch(config.getBatchSize());
        
        // Forward pass through pipeline
        Map<Device, Tensor> deviceOutputs = new HashMap<>();
        Tensor currentInput = batch.get(0).getFeatures();
        
        for (Device device : devices) {
            List<ModelLayer> layers = deviceLayers.get(device);
            
            // Process input through device layers
            Tensor output = device.forwardPass(currentInput, layers);
            deviceOutputs.put(device, output);
            
            // Send output to next device
            if (hasNextDevice(device)) {
                currentInput = output;
            }
        }
        
        // Backward pass through pipeline
        Tensor currentGradient = calculateFinalGradient(deviceOutputs, batch);
        
        for (int i = devices.size() - 1; i >= 0; i--) {
            Device device = devices.get(i);
            List<ModelLayer> layers = deviceLayers.get(device);
            
            // Backward pass through device layers
            Tensor inputGradient = device.backwardPass(currentGradient, layers);
            
            // Send gradient to previous device
            if (hasPreviousDevice(device)) {
                currentGradient = inputGradient;
            }
        }
        
        // Update weights on all devices
        deviceLayers.forEach((device, layers) -> {
            device.updateWeights(layers);
        });
    }
    
    private List<ModelLayer> splitModelLayers(ModelConfig config) {
        List<ModelLayer> layers = new ArrayList<>();
        
        // Create layers based on config
        for (int i = 0; i < config.getLayerCount(); i++) {
            ModelLayer layer = new ModelLayer(config.getLayerSize(i));
            layers.add(layer);
        }
        
        return layers;
    }
    
    private Map<Device, List<ModelLayer>> assignLayersToDevices(List<ModelLayer> layers) {
        Map<Device, List<ModelLayer>> assignment = new HashMap<>();
        int layersPerDevice = layers.size() / devices.size();
        
        for (int i = 0; i < devices.size(); i++) {
            Device device = devices.get(i);
            int startIndex = i * layersPerDevice;
            int endIndex = (i == devices.size() - 1) ? layers.size() : (i + 1) * layersPerDevice;
            
            List<ModelLayer> deviceLayers = layers.subList(startIndex, endIndex);
            assignment.put(device, deviceLayers);
        }
        
        return assignment;
    }
}
```

## 20.4 Data Parallelism

Data parallelism distributes training data across multiple workers, with each worker training on a different subset of the data.

### Key Concepts
- **Data Sharding**: Splitting dataset into non-overlapping subsets
- **Gradient Averaging**: Combining gradients from all workers
- **Synchronization**: Ensuring all workers are at the same training step
- **Data Loading**: Efficiently loading and distributing data

### Real-World Analogy
Think of a team of researchers studying a large dataset. Each researcher focuses on a different subset of the data, learns from it, and then shares their findings with the team. The team combines all findings to create a comprehensive understanding.

### Java Example
```java
// Data parallelism service
@Service
public class DataParallelismService {
    private final ExecutorService workerPool;
    private final DataLoader dataLoader;
    private final GradientAggregator gradientAggregator;
    
    public Model trainWithDataParallelism(List<TrainingData> trainingData, ModelConfig config) {
        // Split data across workers
        List<List<TrainingData>> dataShards = splitData(trainingData, config.getWorkerCount());
        
        // Initialize model
        Model globalModel = new Model(config);
        
        // Training loop
        for (int epoch = 0; epoch < config.getEpochs(); epoch++) {
            // Train on each data shard in parallel
            List<CompletableFuture<Gradients>> gradientFutures = dataShards.stream()
                .map(shard -> trainOnShard(globalModel, shard, config))
                .collect(Collectors.toList());
            
            // Wait for all workers to complete
            CompletableFuture.allOf(gradientFutures.toArray(new CompletableFuture[0])).join();
            
            // Collect gradients from all workers
            List<Gradients> allGradients = gradientFutures.stream()
                .map(CompletableFuture::join)
                .collect(Collectors.toList());
            
            // Average gradients
            Gradients averagedGradients = gradientAggregator.average(allGradients);
            
            // Update global model
            globalModel.updateWeights(averagedGradients);
            
            System.out.println("Epoch " + epoch + " completed");
        }
        
        return globalModel;
    }
    
    private CompletableFuture<Gradients> trainOnShard(Model model, List<TrainingData> shard, ModelConfig config) {
        return CompletableFuture.supplyAsync(() -> {
            // Create local copy of model
            Model localModel = model.copy();
            
            // Train on shard
            for (TrainingData sample : shard) {
                // Forward pass
                Prediction prediction = localModel.predict(sample.getFeatures());
                
                // Calculate loss
                double loss = calculateLoss(prediction, sample.getLabel());
                
                // Backward pass
                localModel.backward(loss);
            }
            
            // Calculate gradients
            return localModel.getGradients();
        }, workerPool);
    }
    
    private List<List<TrainingData>> splitData(List<TrainingData> data, int workerCount) {
        List<List<TrainingData>> shards = new ArrayList<>();
        int shardSize = data.size() / workerCount;
        
        for (int i = 0; i < workerCount; i++) {
            int startIndex = i * shardSize;
            int endIndex = (i == workerCount - 1) ? data.size() : (i + 1) * shardSize;
            
            List<TrainingData> shard = data.subList(startIndex, endIndex);
            shards.add(shard);
        }
        
        return shards;
    }
    
    private double calculateLoss(Prediction prediction, double actual) {
        double error = prediction.getValue() - actual;
        return error * error;
    }
}
```

## 20.5 Pipeline Parallelism

Pipeline parallelism processes different batches through different stages of a model pipeline, enabling efficient utilization of multiple devices.

### Key Concepts
- **Pipeline Stages**: Different parts of the model running on different devices
- **Batch Processing**: Processing multiple batches simultaneously
- **Bubble Time**: Idle time when pipeline is not fully utilized
- **Load Balancing**: Ensuring even distribution of work across stages

### Real-World Analogy
Think of a car assembly line where different stations work on different parts of the car. While one car is being painted, another car can be getting its engine installed, and a third car can be getting its interior fitted. This allows multiple cars to be in different stages of production simultaneously.

### Java Example
```java
// Pipeline parallelism service
@Service
public class PipelineParallelismService {
    private final List<PipelineStage> stages;
    private final ExecutorService stageExecutors;
    private final Queue<Batch> inputQueue;
    private final Queue<Batch> outputQueue;
    
    public Model trainWithPipelineParallelism(List<TrainingData> trainingData, ModelConfig config) {
        // Initialize pipeline stages
        initializePipelineStages(config);
        
        // Start stage executors
        startStageExecutors();
        
        // Process training data through pipeline
        List<CompletableFuture<Void>> batchFutures = new ArrayList<>();
        
        for (int i = 0; i < trainingData.size(); i += config.getBatchSize()) {
            List<TrainingData> batch = trainingData.subList(i, Math.min(i + config.getBatchSize(), trainingData.size()));
            CompletableFuture<Void> future = processBatchThroughPipeline(batch);
            batchFutures.add(future);
        }
        
        // Wait for all batches to complete
        CompletableFuture.allOf(batchFutures.toArray(new CompletableFuture[0])).join();
        
        // Combine results from all stages
        return combineStageResults();
    }
    
    private void initializePipelineStages(ModelConfig config) {
        stages.clear();
        
        for (int i = 0; i < config.getStageCount(); i++) {
            PipelineStage stage = new PipelineStage(i, config.getStageConfig(i));
            stages.add(stage);
        }
    }
    
    private void startStageExecutors() {
        for (int i = 0; i < stages.size(); i++) {
            final int stageIndex = i;
            final PipelineStage stage = stages.get(i);
            
            stageExecutors.submit(() -> {
                while (!Thread.currentThread().isInterrupted()) {
                    try {
                        // Get input from previous stage
                        Batch input = getInputForStage(stageIndex);
                        if (input != null) {
                            // Process batch through stage
                            Batch output = stage.process(input);
                            
                            // Send output to next stage
                            sendOutputToNextStage(stageIndex, output);
                        } else {
                            Thread.sleep(100); // Wait for input
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    } catch (Exception e) {
                        System.err.println("Error in stage " + stageIndex + ": " + e.getMessage());
                    }
                }
            });
        }
    }
    
    private CompletableFuture<Void> processBatchThroughPipeline(List<TrainingData> batch) {
        return CompletableFuture.runAsync(() -> {
            try {
                // Add batch to input queue
                inputQueue.offer(new Batch(batch));
                
                // Wait for batch to complete processing
                while (!isBatchComplete(batch)) {
                    Thread.sleep(100);
                }
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
    }
    
    private Batch getInputForStage(int stageIndex) {
        if (stageIndex == 0) {
            // First stage gets from input queue
            return inputQueue.poll();
        } else {
            // Other stages get from previous stage
            return stages.get(stageIndex - 1).getOutput();
        }
    }
    
    private void sendOutputToNextStage(int stageIndex, Batch output) {
        if (stageIndex < stages.size() - 1) {
            // Send to next stage
            stages.get(stageIndex + 1).setInput(output);
        } else {
            // Last stage sends to output queue
            outputQueue.offer(output);
        }
    }
}
```

## 20.6 Asynchronous SGD

Asynchronous Stochastic Gradient Descent allows workers to update parameters independently without waiting for synchronization, improving training speed.

### Key Concepts
- **Asynchronous Updates**: Workers update parameters independently
- **Stale Gradients**: Using gradients from previous iterations
- **Convergence**: Ensuring algorithm still converges despite asynchrony
- **Conflict Resolution**: Handling concurrent parameter updates

### Real-World Analogy
Think of a team of researchers working on the same problem independently. Each researcher makes their own updates to a shared solution without waiting for others to finish. While this might lead to some conflicts, it allows the team to make progress faster overall.

### Java Example
```java
// Asynchronous SGD service
@Service
public class AsynchronousSGDService {
    private final ParameterServer parameterServer;
    private final ExecutorService workerPool;
    private final ConflictResolver conflictResolver;
    
    public Model trainAsynchronously(List<TrainingData> trainingData, ModelConfig config) {
        // Initialize parameter server
        parameterServer.initialize(config);
        
        // Start asynchronous workers
        List<CompletableFuture<Void>> workerFutures = new ArrayList<>();
        
        for (int i = 0; i < config.getWorkerCount(); i++) {
            final int workerId = i;
            CompletableFuture<Void> future = CompletableFuture.runAsync(() -> {
                trainWorkerAsynchronously(workerId, trainingData, config);
            }, workerPool);
            
            workerFutures.add(future);
        }
        
        // Wait for all workers to complete
        CompletableFuture.allOf(workerFutures.toArray(new CompletableFuture[0])).join();
        
        return parameterServer.getModel();
    }
    
    private void trainWorkerAsynchronously(int workerId, List<TrainingData> trainingData, ModelConfig config) {
        // Get local copy of model
        Model localModel = parameterServer.getModel();
        
        for (int epoch = 0; epoch < config.getEpochs(); epoch++) {
            for (TrainingData sample : trainingData) {
                // Forward pass
                Prediction prediction = localModel.predict(sample.getFeatures());
                
                // Calculate loss
                double loss = calculateLoss(prediction, sample.getLabel());
                
                // Backward pass
                localModel.backward(loss);
                
                // Update local model
                localModel.updateWeights();
                
                // Asynchronously update global parameters
                updateGlobalParametersAsynchronously(localModel, workerId);
            }
        }
    }
    
    private void updateGlobalParametersAsynchronously(Model localModel, int workerId) {
        // Get current global parameters
        Model globalModel = parameterServer.getModel();
        
        // Calculate parameter differences
        ParameterDiff diff = calculateParameterDiff(globalModel, localModel);
        
        // Apply learning rate
        diff.scale(config.getLearningRate());
        
        // Update global parameters asynchronously
        parameterServer.updateParametersAsync(diff, workerId);
    }
    
    private ParameterDiff calculateParameterDiff(Model globalModel, Model localModel) {
        ParameterDiff diff = new ParameterDiff();
        
        // Calculate differences for each parameter
        for (String paramName : globalModel.getParameterNames()) {
            double globalValue = globalModel.getParameter(paramName);
            double localValue = localModel.getParameter(paramName);
            diff.setDifference(paramName, localValue - globalValue);
        }
        
        return diff;
    }
    
    // Conflict resolution
    @EventListener
    public void handleParameterConflict(ParameterConflictEvent event) {
        String paramName = event.getParamName();
        List<ParameterUpdate> updates = event.getUpdates();
        
        // Resolve conflict using configured strategy
        ParameterUpdate resolvedUpdate = conflictResolver.resolve(paramName, updates);
        
        // Apply resolved update
        parameterServer.applyUpdate(paramName, resolvedUpdate);
    }
}
```

## 20.7 Parameter Servers

Parameter servers provide centralized storage and management of model parameters in distributed training scenarios.

### Key Concepts
- **Parameter Storage**: Centralized storage of model parameters
- **Update Aggregation**: Combining updates from multiple workers
- **Consistency Models**: Ensuring parameter consistency across workers
- **Fault Tolerance**: Handling server failures

### Real-World Analogy
Think of a central library that stores all the books (parameters) that different researchers (workers) need. Researchers can check out books, make notes, and return them with updates. The library keeps track of all changes and ensures everyone has access to the latest versions.

### Java Example
```java
// Parameter server implementation
@Service
public class ParameterServer {
    private final Map<String, Double> parameters = new ConcurrentHashMap<>();
    private final Map<String, List<ParameterUpdate>> pendingUpdates = new ConcurrentHashMap<>();
    private final UpdateAggregator updateAggregator;
    private final ConsistencyManager consistencyManager;
    
    public void initialize(ModelConfig config) {
        // Initialize parameters with random values
        for (String paramName : config.getParameterNames()) {
            parameters.put(paramName, Math.random() * 0.1 - 0.05);
        }
    }
    
    public Model getModel() {
        return new Model(parameters);
    }
    
    public void updateParametersAsync(ParameterDiff diff, int workerId) {
        // Add update to pending updates
        for (String paramName : diff.getParameterNames()) {
            ParameterUpdate update = new ParameterUpdate(paramName, diff.getDifference(paramName), workerId);
            pendingUpdates.computeIfAbsent(paramName, k -> new ArrayList<>()).add(update);
        }
        
        // Process updates if threshold reached
        if (pendingUpdates.size() >= config.getUpdateThreshold()) {
            processPendingUpdates();
        }
    }
    
    private void processPendingUpdates() {
        for (Map.Entry<String, List<ParameterUpdate>> entry : pendingUpdates.entrySet()) {
            String paramName = entry.getKey();
            List<ParameterUpdate> updates = entry.getValue();
            
            // Aggregate updates
            double aggregatedUpdate = updateAggregator.aggregate(updates);
            
            // Apply update to parameter
            double currentValue = parameters.get(paramName);
            double newValue = currentValue + aggregatedUpdate;
            parameters.put(paramName, newValue);
            
            // Clear pending updates for this parameter
            updates.clear();
        }
    }
    
    public void updateParameters(Gradients gradients) {
        // Update parameters with aggregated gradients
        for (String paramName : gradients.getParameterNames()) {
            double currentValue = parameters.get(paramName);
            double gradient = gradients.getGradient(paramName);
            double newValue = currentValue - config.getLearningRate() * gradient;
            parameters.put(paramName, newValue);
        }
    }
    
    public void setParameter(String paramName, double value) {
        parameters.put(paramName, value);
    }
    
    public double getParameter(String paramName) {
        return parameters.get(paramName);
    }
    
    public Map<String, Double> getAllParameters() {
        return new HashMap<>(parameters);
    }
    
    // Consistency management
    public void ensureConsistency(List<WorkerNode> workers) {
        Model currentModel = getModel();
        
        // Send current model to all workers
        workers.parallelStream().forEach(worker -> {
            try {
                communicationService.sendModel(worker, currentModel);
            } catch (Exception e) {
                System.err.println("Failed to send model to worker " + worker.getId() + ": " + e.getMessage());
            }
        });
    }
    
    // Fault tolerance
    public void handleWorkerFailure(WorkerNode failedWorker) {
        // Remove any pending updates from failed worker
        pendingUpdates.values().forEach(updates -> {
            updates.removeIf(update -> update.getWorkerId() == failedWorker.getId());
        });
        
        // Redistribute work if necessary
        if (workers.size() > 1) {
            redistributeWork(failedWorker);
        }
    }
}
```

## 20.8 Federated Learning

Federated learning enables training machine learning models across multiple devices or organizations without sharing raw data.

### Key Concepts
- **Data Privacy**: Keeping data on local devices
- **Model Aggregation**: Combining model updates from multiple sources
- **Communication Efficiency**: Minimizing data transfer
- **Heterogeneous Data**: Handling different data distributions

### Real-World Analogy
Think of a group of hospitals that want to improve their diagnostic models. Instead of sharing patient data (which would violate privacy), each hospital trains their own model on their local data and shares only the model improvements. A central coordinator combines these improvements to create a better model that benefits everyone.

### Java Example
```java
// Federated learning service
@Service
public class FederatedLearningService {
    private final ModelAggregator modelAggregator;
    private final CommunicationService communicationService;
    private final PrivacyManager privacyManager;
    
    public Model trainFederatedModel(List<ClientNode> clients, ModelConfig config) {
        // Initialize global model
        Model globalModel = new Model(config);
        
        // Federated learning rounds
        for (int round = 0; round < config.getFederatedRounds(); round++) {
            System.out.println("Starting federated round " + round);
            
            // Select clients for this round
            List<ClientNode> selectedClients = selectClients(clients, config.getClientSelectionRatio());
            
            // Send global model to selected clients
            sendModelToClients(selectedClients, globalModel);
            
            // Wait for client updates
            List<ModelUpdate> clientUpdates = waitForClientUpdates(selectedClients, config.getClientTimeout());
            
            // Aggregate client updates
            ModelUpdate aggregatedUpdate = modelAggregator.aggregate(clientUpdates);
            
            // Update global model
            globalModel.update(aggregatedUpdate);
            
            // Evaluate global model
            double accuracy = evaluateModel(globalModel, config.getTestData());
            System.out.println("Round " + round + " accuracy: " + accuracy);
        }
        
        return globalModel;
    }
    
    private List<ClientNode> selectClients(List<ClientNode> clients, double selectionRatio) {
        int numClients = (int) (clients.size() * selectionRatio);
        Collections.shuffle(clients);
        return clients.subList(0, numClients);
    }
    
    private void sendModelToClients(List<ClientNode> clients, Model globalModel) {
        clients.parallelStream().forEach(client -> {
            try {
                // Apply differential privacy if required
                Model privateModel = privacyManager.applyDifferentialPrivacy(globalModel, client.getPrivacyLevel());
                
                // Send model to client
                communicationService.sendModel(client, privateModel);
                
            } catch (Exception e) {
                System.err.println("Failed to send model to client " + client.getId() + ": " + e.getMessage());
            }
        });
    }
    
    private List<ModelUpdate> waitForClientUpdates(List<ClientNode> clients, Duration timeout) {
        List<CompletableFuture<ModelUpdate>> updateFutures = clients.stream()
            .map(client -> CompletableFuture.supplyAsync(() -> {
                try {
                    return communicationService.receiveModelUpdate(client, timeout);
                } catch (Exception e) {
                    System.err.println("Failed to receive update from client " + client.getId() + ": " + e.getMessage());
                    return null;
                }
            }))
            .collect(Collectors.toList());
        
        // Wait for all updates or timeout
        CompletableFuture.allOf(updateFutures.toArray(new CompletableFuture[0])).join();
        
        return updateFutures.stream()
            .map(CompletableFuture::join)
            .filter(Objects::nonNull)
            .collect(Collectors.toList());
    }
    
    // Client-side federated learning
    @Service
    public class FederatedClient {
        private final Model localModel;
        private final List<TrainingData> localData;
        private final PrivacyManager privacyManager;
        
        public ModelUpdate trainLocalModel(Model globalModel, int epochs) {
            // Initialize local model with global model
            localModel.copyFrom(globalModel);
            
            // Train on local data
            for (int epoch = 0; epoch < epochs; epoch++) {
                for (TrainingData sample : localData) {
                    // Forward pass
                    Prediction prediction = localModel.predict(sample.getFeatures());
                    
                    // Calculate loss
                    double loss = calculateLoss(prediction, sample.getLabel());
                    
                    // Backward pass
                    localModel.backward(loss);
                    
                    // Update weights
                    localModel.updateWeights();
                }
            }
            
            // Calculate model update
            ModelUpdate update = calculateModelUpdate(globalModel, localModel);
            
            // Apply privacy protection
            return privacyManager.protectUpdate(update);
        }
        
        private ModelUpdate calculateModelUpdate(Model globalModel, Model localModel) {
            ModelUpdate update = new ModelUpdate();
            
            for (String paramName : globalModel.getParameterNames()) {
                double globalValue = globalModel.getParameter(paramName);
                double localValue = localModel.getParameter(paramName);
                update.setParameterUpdate(paramName, localValue - globalValue);
            }
            
            return update;
        }
    }
}
```

This comprehensive explanation covers all aspects of concurrency in machine learning, providing both theoretical understanding and practical examples to illustrate each concept.