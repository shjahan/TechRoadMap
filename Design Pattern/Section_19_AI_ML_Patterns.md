# Section 19 - AI/ML Patterns

## 19.1 Machine Learning Pipeline Patterns

Machine Learning pipeline patterns provide structured approaches to building, training, and deploying ML models in production environments.

### When to Use:
- When you need to process large datasets for ML training
- When you want to automate the ML workflow
- When you need to ensure reproducibility in ML experiments

### Real-World Analogy:
Think of an assembly line in a factory where raw materials go through various stages of processing to become finished products. In ML, raw data goes through cleaning, feature engineering, training, and validation stages to become a trained model.

### Basic Implementation:
```python
# ML Pipeline using scikit-learn
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class MLPipeline:
    def __init__(self):
        self.pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(n_estimators=100))
        ])
    
    def train(self, X, y):
        """Train the ML pipeline"""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        # Fit the pipeline
        self.pipeline.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        return {
            'accuracy': accuracy,
            'model': self.pipeline
        }
    
    def predict(self, X):
        """Make predictions using the trained pipeline"""
        return self.pipeline.predict(X)

# Usage
pipeline = MLPipeline()
results = pipeline.train(X_train, y_train)
predictions = pipeline.predict(X_test)
```

## 19.2 Model Training Patterns

Model training patterns provide structured approaches to training machine learning models with proper validation and monitoring.

### When to Use:
- When you need to train ML models systematically
- When you want to implement proper validation strategies
- When you need to monitor training progress

### Real-World Analogy:
Think of training a sports team. You need to practice regularly, track performance metrics, adjust strategies based on results, and ensure the team is ready for competition. Similarly, ML model training involves iterative improvement with performance monitoring.

### Basic Implementation:
```python
# Model training with validation
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam

class ModelTrainer:
    def __init__(self, model, validation_split=0.2):
        self.model = model
        self.validation_split = validation_split
        self.history = None
    
    def train(self, X, y, epochs=100, batch_size=32):
        """Train the model with validation"""
        # Split data for validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=self.validation_split, random_state=42
        )
        
        # Compile model
        self.model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Define callbacks
        callbacks = [
            EarlyStopping(patience=10, restore_best_weights=True),
            ModelCheckpoint('best_model.h5', save_best_only=True)
        ]
        
        # Train model
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        return self.history
    
    def evaluate(self, X_test, y_test):
        """Evaluate the trained model"""
        return self.model.evaluate(X_test, y_test, verbose=0)

# Usage
trainer = ModelTrainer(model)
history = trainer.train(X_train, y_train)
test_loss, test_accuracy = trainer.evaluate(X_test, y_test)
```

## 19.3 Model Serving Patterns

Model serving patterns provide approaches to deploy and serve ML models in production environments.

### When to Use:
- When you need to deploy ML models to production
- When you want to serve predictions via APIs
- When you need to handle model versioning and updates

### Real-World Analogy:
Think of a restaurant kitchen that needs to serve dishes quickly and consistently. The kitchen has standardized recipes (models), efficient processes (serving patterns), and can handle multiple orders (requests) simultaneously.

### Basic Implementation:
```python
# Model serving with Flask
from flask import Flask, request, jsonify
import joblib
import numpy as np

class ModelServer:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)
        self.app = Flask(__name__)
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/predict', methods=['POST'])
        def predict():
            try:
                data = request.get_json()
                features = np.array(data['features']).reshape(1, -1)
                prediction = self.model.predict(features)[0]
                probability = self.model.predict_proba(features)[0]
                
                return jsonify({
                    'prediction': int(prediction),
                    'probability': probability.tolist(),
                    'status': 'success'
                })
            except Exception as e:
                return jsonify({
                    'error': str(e),
                    'status': 'error'
                }), 400
        
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({'status': 'healthy'})
    
    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port, debug=False)

# Usage
server = ModelServer('trained_model.pkl')
server.run()
```

## 19.4 Feature Engineering Patterns

Feature engineering patterns provide systematic approaches to creating and selecting features for ML models.

### When to Use:
- When you need to transform raw data into ML-ready features
- When you want to improve model performance through better features
- When you need to handle different data types and scales

### Real-World Analogy:
Think of a chef preparing ingredients for a dish. Raw ingredients need to be cleaned, cut, seasoned, and combined in specific ways to create the best possible dish. Similarly, raw data needs to be processed and transformed into meaningful features.

### Basic Implementation:
```python
# Feature engineering pipeline
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.compose import ColumnTransformer

class FeatureEngineer:
    def __init__(self):
        self.preprocessor = None
        self.feature_selector = None
        self.is_fitted = False
    
    def fit_transform(self, X, y=None):
        """Fit and transform features"""
        # Separate numerical and categorical columns
        numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = X.select_dtypes(include=['object']).columns
        
        # Create preprocessing pipeline
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numerical_cols),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
            ]
        )
        
        # Fit and transform
        X_transformed = self.preprocessor.fit_transform(X)
        
        # Feature selection if target is provided
        if y is not None:
            self.feature_selector = SelectKBest(score_func=f_classif, k=10)
            X_transformed = self.feature_selector.fit_transform(X_transformed, y)
        
        self.is_fitted = True
        return X_transformed
    
    def transform(self, X):
        """Transform new data using fitted preprocessor"""
        if not self.is_fitted:
            raise ValueError("FeatureEngineer must be fitted before transform")
        
        X_transformed = self.preprocessor.transform(X)
        
        if self.feature_selector is not None:
            X_transformed = self.feature_selector.transform(X_transformed)
        
        return X_transformed

# Usage
engineer = FeatureEngineer()
X_processed = engineer.fit_transform(X_train, y_train)
X_test_processed = engineer.transform(X_test)
```

## 19.5 Data Pipeline Patterns

Data pipeline patterns provide structured approaches to processing and moving data through ML systems.

### When to Use:
- When you need to process large volumes of data
- When you want to automate data processing workflows
- When you need to ensure data quality and consistency

### Real-World Analogy:
Think of a water treatment plant that processes water through multiple stages - filtration, chemical treatment, testing, and distribution. Each stage has specific requirements and the water flows through the system systematically.

### Basic Implementation:
```python
# Data pipeline using Apache Airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

def extract_data():
    """Extract data from source"""
    # Extract data from database, API, or file
    data = pd.read_csv('raw_data.csv')
    return data

def transform_data(**context):
    """Transform data"""
    # Get data from previous task
    data = context['task_instance'].xcom_pull(task_ids='extract_data')
    
    # Apply transformations
    data['new_feature'] = data['feature1'] * data['feature2']
    data = data.dropna()
    
    return data

def load_data(**context):
    """Load data to destination"""
    # Get transformed data
    data = context['task_instance'].xcom_pull(task_ids='transform_data')
    
    # Save to destination
    data.to_csv('processed_data.csv', index=False)

# Define DAG
dag = DAG(
    'ml_data_pipeline',
    default_args={
        'owner': 'ml_team',
        'depends_on_past': False,
        'start_date': datetime(2023, 1, 1),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5)
    },
    description='ML Data Processing Pipeline',
    schedule_interval=timedelta(days=1)
)

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag
)

# Set task dependencies
extract_task >> transform_task >> load_task
```

## 19.6 A/B Testing Patterns

A/B testing patterns provide systematic approaches to testing ML models and features in production.

### When to Use:
- When you need to compare different ML models
- When you want to test new features safely
- When you need to measure the impact of changes

### Real-World Analogy:
Think of a restaurant testing a new menu item. They might serve the new item to half of their customers and the old item to the other half, then compare customer satisfaction and sales to decide whether to keep the new item.

### Basic Implementation:
```python
# A/B testing framework
import random
import numpy as np
from scipy import stats

class ABTestFramework:
    def __init__(self, control_model, treatment_model, traffic_split=0.5):
        self.control_model = control_model
        self.treatment_model = treatment_model
        self.traffic_split = traffic_split
        self.results = {'control': [], 'treatment': []}
    
    def assign_traffic(self, user_id):
        """Assign user to control or treatment group"""
        hash_value = hash(str(user_id)) % 100
        return 'treatment' if hash_value < (self.traffic_split * 100) else 'control'
    
    def get_prediction(self, user_id, features):
        """Get prediction based on assigned group"""
        group = self.assign_traffic(user_id)
        
        if group == 'control':
            prediction = self.control_model.predict(features)
        else:
            prediction = self.treatment_model.predict(features)
        
        # Store result for analysis
        self.results[group].append({
            'user_id': user_id,
            'prediction': prediction,
            'features': features
        })
        
        return prediction, group
    
    def analyze_results(self):
        """Analyze A/B test results"""
        control_predictions = [r['prediction'] for r in self.results['control']]
        treatment_predictions = [r['prediction'] for r in self.results['treatment']]
        
        # Statistical test
        t_stat, p_value = stats.ttest_ind(control_predictions, treatment_predictions)
        
        return {
            'control_mean': np.mean(control_predictions),
            'treatment_mean': np.mean(treatment_predictions),
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }

# Usage
ab_test = ABTestFramework(control_model, treatment_model)
prediction, group = ab_test.get_prediction(user_id, features)
results = ab_test.analyze_results()
```

## 19.7 Model Versioning Patterns

Model versioning patterns provide approaches to manage different versions of ML models in production.

### When to Use:
- When you need to track model versions
- When you want to rollback to previous models
- When you need to compare model performance across versions

### Real-World Analogy:
Think of a software version control system like Git, but for ML models. You can track changes, compare versions, and rollback to previous versions if needed.

### Basic Implementation:
```python
# Model versioning system
import mlflow
import mlflow.sklearn
from datetime import datetime
import os

class ModelVersioning:
    def __init__(self, experiment_name):
        self.experiment_name = experiment_name
        mlflow.set_experiment(experiment_name)
    
    def log_model(self, model, metrics, parameters, model_name):
        """Log model with versioning"""
        with mlflow.start_run():
            # Log parameters
            for key, value in parameters.items():
                mlflow.log_param(key, value)
            
            # Log metrics
            for key, value in metrics.items():
                mlflow.log_metric(key, value)
            
            # Log model
            mlflow.sklearn.log_model(
                model, 
                "model",
                registered_model_name=model_name
            )
    
    def get_model_version(self, model_name, version=None):
        """Get specific model version"""
        if version:
            model_uri = f"models:/{model_name}/{version}"
        else:
            model_uri = f"models:/{model_name}/latest"
        
        return mlflow.sklearn.load_model(model_uri)
    
    def compare_models(self, model_name, versions):
        """Compare different model versions"""
        comparison = {}
        
        for version in versions:
            model = self.get_model_version(model_name, version)
            # Get model metrics
            metrics = self.get_model_metrics(model_name, version)
            comparison[version] = metrics
        
        return comparison
    
    def promote_model(self, model_name, version, stage):
        """Promote model to different stage"""
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )

# Usage
versioning = ModelVersioning("my_experiment")
versioning.log_model(
    model=my_model,
    metrics={'accuracy': 0.95, 'precision': 0.93},
    parameters={'n_estimators': 100, 'max_depth': 10},
    model_name="random_forest"
)
```

## 19.8 Model Monitoring Patterns

Model monitoring patterns provide approaches to monitor ML models in production for performance degradation and data drift.

### When to Use:
- When you need to monitor model performance in production
- When you want to detect data drift
- When you need to ensure model reliability

### Real-World Analogy:
Think of a car's dashboard that monitors various metrics like speed, fuel level, engine temperature, and alerts you when something needs attention. Similarly, model monitoring tracks model performance and alerts when issues arise.

### Basic Implementation:
```python
# Model monitoring system
import numpy as np
from scipy import stats
import pandas as pd
from datetime import datetime, timedelta

class ModelMonitor:
    def __init__(self, baseline_data, baseline_predictions):
        self.baseline_data = baseline_data
        self.baseline_predictions = baseline_predictions
        self.baseline_stats = self._calculate_baseline_stats()
    
    def _calculate_baseline_stats(self):
        """Calculate baseline statistics"""
        return {
            'mean': np.mean(self.baseline_predictions),
            'std': np.std(self.baseline_predictions),
            'feature_means': self.baseline_data.mean().to_dict(),
            'feature_stds': self.baseline_data.std().to_dict()
        }
    
    def detect_data_drift(self, new_data, threshold=0.05):
        """Detect data drift using statistical tests"""
        drift_detected = {}
        
        for feature in new_data.columns:
            if feature in self.baseline_stats['feature_means']:
                # Kolmogorov-Smirnov test
                ks_stat, ks_pvalue = stats.ks_2samp(
                    self.baseline_data[feature],
                    new_data[feature]
                )
                
                drift_detected[feature] = {
                    'ks_statistic': ks_stat,
                    'ks_pvalue': ks_pvalue,
                    'drift_detected': ks_pvalue < threshold
                }
        
        return drift_detected
    
    def detect_performance_drift(self, new_predictions, threshold=0.05):
        """Detect performance drift"""
        # Calculate performance metrics
        new_mean = np.mean(new_predictions)
        new_std = np.std(new_predictions)
        
        # Compare with baseline
        mean_diff = abs(new_mean - self.baseline_stats['mean'])
        std_diff = abs(new_std - self.baseline_stats['std'])
        
        performance_drift = {
            'mean_difference': mean_diff,
            'std_difference': std_diff,
            'drift_detected': mean_diff > threshold or std_diff > threshold
        }
        
        return performance_drift
    
    def generate_alert(self, drift_results):
        """Generate alert if drift is detected"""
        alerts = []
        
        for feature, drift_info in drift_results.items():
            if drift_info['drift_detected']:
                alerts.append(f"Data drift detected in feature: {feature}")
        
        return alerts

# Usage
monitor = ModelMonitor(baseline_data, baseline_predictions)
drift_results = monitor.detect_data_drift(new_data)
performance_drift = monitor.detect_performance_drift(new_predictions)
alerts = monitor.generate_alert(drift_results)
```

## 19.9 MLOps Patterns

MLOps patterns provide approaches to operationalizing machine learning models with proper CI/CD, monitoring, and deployment practices.

### When to Use:
- When you need to operationalize ML models
- When you want to implement ML CI/CD
- When you need to manage ML model lifecycle

### Real-World Analogy:
Think of a manufacturing plant that produces products consistently and efficiently. MLOps is like the operational processes that ensure ML models are produced, tested, deployed, and maintained systematically.

### Basic Implementation:
```python
# MLOps pipeline using MLflow and Docker
import mlflow
import mlflow.sklearn
from docker import DockerClient
import subprocess

class MLOpsPipeline:
    def __init__(self, model_name, model_version):
        self.model_name = model_name
        self.model_version = model_version
        self.docker_client = DockerClient()
    
    def train_model(self, X, y, parameters):
        """Train model and log to MLflow"""
        with mlflow.start_run():
            # Train model
            model = self._train_model(X, y, parameters)
            
            # Log parameters and metrics
            mlflow.log_params(parameters)
            mlflow.log_metrics(self._evaluate_model(model, X, y))
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            return model
    
    def deploy_model(self, model_uri, environment="production"):
        """Deploy model using Docker"""
        # Create Dockerfile
        dockerfile_content = f"""
        FROM python:3.8-slim
        WORKDIR /app
        COPY requirements.txt .
        RUN pip install -r requirements.txt
        COPY app.py .
        CMD ["python", "app.py"]
        """
        
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content)
        
        # Build Docker image
        image = self.docker_client.images.build(
            path=".",
            tag=f"{self.model_name}:{self.model_version}"
        )
        
        # Run container
        container = self.docker_client.containers.run(
            image[0],
            ports={5000: 5000},
            environment={"MODEL_URI": model_uri},
            detach=True
        )
        
        return container
    
    def monitor_model(self, model_name, model_version):
        """Monitor deployed model"""
        # Get model metrics
        client = mlflow.tracking.MlflowClient()
        model_versions = client.get_latest_versions(model_name)
        
        # Check model health
        health_status = self._check_model_health(model_name, model_version)
        
        return {
            'model_versions': model_versions,
            'health_status': health_status
        }
    
    def _train_model(self, X, y, parameters):
        """Train model with given parameters"""
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(**parameters)
        model.fit(X, y)
        return model
    
    def _evaluate_model(self, model, X, y):
        """Evaluate model and return metrics"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score
        y_pred = model.predict(X)
        return {
            'accuracy': accuracy_score(y, y_pred),
            'precision': precision_score(y, y_pred, average='weighted'),
            'recall': recall_score(y, y_pred, average='weighted')
        }
    
    def _check_model_health(self, model_name, model_version):
        """Check if model is healthy"""
        try:
            # Try to load model
            model = mlflow.sklearn.load_model(f"models:/{model_name}/{model_version}")
            return "healthy"
        except Exception as e:
            return f"unhealthy: {str(e)}"

# Usage
mlops = MLOpsPipeline("my_model", "1.0")
model = mlops.train_model(X_train, y_train, {'n_estimators': 100})
container = mlops.deploy_model("models:/my_model/1.0")
status = mlops.monitor_model("my_model", "1.0")
```

## 19.10 AI Ethics Patterns

AI ethics patterns provide approaches to ensure AI systems are fair, transparent, and accountable.

### When to Use:
- When you need to ensure AI fairness
- When you want to implement AI transparency
- When you need to address AI bias and accountability

### Real-World Analogy:
Think of a court system that ensures justice is served fairly and transparently. AI ethics patterns are like the principles and processes that ensure AI systems make fair and accountable decisions.

### Basic Implementation:
```python
# AI ethics framework
import pandas as pd
from sklearn.metrics import confusion_matrix
import numpy as np

class AIEthicsFramework:
    def __init__(self, model, sensitive_features):
        self.model = model
        self.sensitive_features = sensitive_features
    
    def check_fairness(self, X, y, protected_attribute):
        """Check for fairness across protected groups"""
        fairness_metrics = {}
        
        # Get predictions
        y_pred = self.model.predict(X)
        
        # Calculate metrics for each group
        for group_value in X[protected_attribute].unique():
            group_mask = X[protected_attribute] == group_value
            group_y = y[group_mask]
            group_pred = y_pred[group_mask]
            
            # Calculate confusion matrix
            tn, fp, fn, tp = confusion_matrix(group_y, group_pred).ravel()
            
            # Calculate fairness metrics
            tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
            fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            
            fairness_metrics[group_value] = {
                'tpr': tpr,
                'fpr': fpr,
                'precision': precision
            }
        
        return fairness_metrics
    
    def detect_bias(self, X, y, protected_attribute):
        """Detect bias in the model"""
        fairness_metrics = self.check_fairness(X, y, protected_attribute)
        
        # Check for significant differences
        tprs = [metrics['tpr'] for metrics in fairness_metrics.values()]
        fprs = [metrics['fpr'] for metrics in fairness_metrics.values()]
        
        tpr_bias = max(tprs) - min(tprs) > 0.1
        fpr_bias = max(fprs) - min(fprs) > 0.1
        
        return {
            'tpr_bias': tpr_bias,
            'fpr_bias': fpr_bias,
            'bias_detected': tpr_bias or fpr_bias
        }
    
    def explain_prediction(self, X, feature_names):
        """Provide explanation for model predictions"""
        # Get feature importance
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
        else:
            # Use permutation importance
            importances = self._calculate_permutation_importance(X)
        
        # Create explanation
        explanation = {
            'feature_importances': dict(zip(feature_names, importances)),
            'top_features': sorted(zip(feature_names, importances), 
                                 key=lambda x: x[1], reverse=True)[:5]
        }
        
        return explanation
    
    def audit_model(self, X, y, protected_attribute):
        """Comprehensive model audit"""
        audit_results = {
            'fairness': self.check_fairness(X, y, protected_attribute),
            'bias': self.detect_bias(X, y, protected_attribute),
            'performance': self._calculate_performance_metrics(y, self.model.predict(X))
        }
        
        return audit_results
    
    def _calculate_permutation_importance(self, X):
        """Calculate permutation importance"""
        from sklearn.inspection import permutation_importance
        # This would need actual implementation
        return np.random.random(X.shape[1])
    
    def _calculate_performance_metrics(self, y_true, y_pred):
        """Calculate performance metrics"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted')
        }

# Usage
ethics_framework = AIEthicsFramework(model, ['gender', 'race'])
fairness_results = ethics_framework.check_fairness(X_test, y_test, 'gender')
bias_results = ethics_framework.detect_bias(X_test, y_test, 'gender')
audit_results = ethics_framework.audit_model(X_test, y_test, 'gender')
```

This comprehensive coverage of AI/ML patterns provides the foundation for building robust, ethical, and production-ready machine learning systems. Each pattern addresses specific challenges in the ML lifecycle and offers different approaches to creating reliable AI solutions.