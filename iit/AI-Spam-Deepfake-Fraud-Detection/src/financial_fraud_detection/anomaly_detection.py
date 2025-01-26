import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import json

# Configuration for Isolation Forest
IF_ESTIMATORS = 100  # Number of trees in the forest
IF_CONTAMINATION = 0.05  # Proportion of anomalies in the data
IF_RANDOM_STATE = 42  # For reproducibility

def preprocess_data(data, feature_columns):
    """
    Preprocesses the data for anomaly detection by scaling the features.

    Parameters:
        data (pd.DataFrame): The input data as a pandas DataFrame.
        feature_columns (list): List of feature columns to be used for training.

    Returns:
        np.ndarray: Scaled feature array.
    """
    try:
        # Extract the required features
        features = data[feature_columns]
        
        # Standardize the features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        
        return scaled_features
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return None

def train_anomaly_detection_model(data, feature_columns):
    """
    Trains an Isolation Forest model for anomaly detection.

    Parameters:
        data (pd.DataFrame): The input data as a pandas DataFrame.
        feature_columns (list): List of feature columns to be used for training.

    Returns:
        IsolationForest: Trained Isolation Forest model.
    """
    try:
        # Preprocess the data
        scaled_features = preprocess_data(data, feature_columns)
        
        # Train the Isolation Forest model
        model = IsolationForest(
            n_estimators=IF_ESTIMATORS,
            contamination=IF_CONTAMINATION,
            random_state=IF_RANDOM_STATE
        )
        model.fit(scaled_features)
        
        print("Anomaly detection model trained successfully.")
        return model
    except Exception as e:
        print(f"Error during model training: {e}")
        return None

def detect_anomalies(model, data, feature_columns):
    """
    Detects anomalies in the input data using the trained Isolation Forest model.

    Parameters:
        model (IsolationForest): The trained anomaly detection model.
        data (pd.DataFrame): The input data to analyze.
        feature_columns (list): List of feature columns used for detection.

    Returns:
        pd.DataFrame: DataFrame with an additional column 'anomaly' indicating anomalies.
    """
    try:
        # Preprocess the data
        scaled_features = preprocess_data(data, feature_columns)
        
        # Predict anomalies (-1 for anomalies, 1 for normal points)
        predictions = model.predict(scaled_features)
        
        # Add the predictions to the DataFrame
        data["anomaly"] = np.where(predictions == -1, 1, 0)
        
        print(f"Anomalies detected: {data['anomaly'].sum()}")
        return data
    except Exception as e:
        print(f"Error during anomaly detection: {e}")
        return None

# Test the functionality
if __name__ == "__main__":
    # Sample dataset
    sample_data = {
        "transaction_id": ["T001", "T002", "T003", "T004", "T005"],
        "amount": [150.75, 3000.00, 87.20, 540.00, 1200.50],
        "merchant_score": [0.8, 0.1, 0.9, 0.5, 0.4],
        "user_activity_score": [0.7, 0.2, 0.8, 0.6, 0.3],
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(sample_data)
    
    # Feature columns for anomaly detection
    feature_cols = ["amount", "merchant_score", "user_activity_score"]
    
    # Train the model
    model = train_anomaly_detection_model(df, feature_cols)
    
    # Detect anomalies
    if model:
        result = detect_anomalies(model, df, feature_cols)
        print("Detection Results:")
        print(result)
