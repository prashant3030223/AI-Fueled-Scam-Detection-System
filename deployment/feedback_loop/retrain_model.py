import boto3
import pandas as pd
from sagemaker import get_execution_role
from sagemaker.estimator import Estimator
import os

# AWS and SageMaker configuration
S3_BUCKET = "your-s3-bucket-name"
TRAINING_DATA_PATH = "training-data/new_fraud_data.csv"
OUTPUT_PATH = f"s3://{S3_BUCKET}/retrained-model-output/"
ROLE_ARN = "arn:aws:iam::your-account-id:role/SageMakerExecutionRole"
REGION = "your-region"
ENDPOINT_NAME = "fraud-detection-endpoint"

# Initialize AWS clients
sagemaker_client = boto3.client("sagemaker", region_name=REGION)
s3_client = boto3.client("s3", region_name=REGION)

def upload_training_data(local_path, s3_bucket, s3_key):
    """
    Uploads new training data to an S3 bucket.

    Parameters:
        local_path (str): Path to the local training data file.
        s3_bucket (str): Name of the S3 bucket.
        s3_key (str): Key (path) to store the file in the bucket.
    """
    try:
        s3_client.upload_file(local_path, s3_bucket, s3_key)
        print(f"Uploaded {local_path} to s3://{s3_bucket}/{s3_key}")
    except Exception as e:
        print(f"Error uploading training data: {e}")

def retrain_model():
    """
    Retrains the machine learning model using new training data.
    """
    try:
        # Define the estimator for training
        estimator = Estimator(
            image_uri="123456789012.dkr.ecr.your-region.amazonaws.com/your-custom-container",  # Replace with your image URI
            role=ROLE_ARN,
            instance_count=1,
            instance_type="ml.m5.large",
            output_path=OUTPUT_PATH
        )

        # Set hyperparameters (example for an XGBoost model)
        estimator.set_hyperparameters(
            max_depth=5,
            eta=0.2,
            gamma=4,
            min_child_weight=6,
            subsample=0.8,
            objective="binary:logistic",
            num_round=100,
        )

        # Start training
        print("Starting model retraining...")
        estimator.fit({"train": f"s3://{S3_BUCKET}/{TRAINING_DATA_PATH}"})
        print("Model retraining completed.")
        return estimator
    except Exception as e:
        print(f"Error during model retraining: {e}")
        return None

def update_endpoint(estimator, endpoint_name):
    """
    Updates the SageMaker endpoint with the newly trained model.

    Parameters:
        estimator (Estimator): Trained SageMaker model.
        endpoint_name (str): Name of the existing SageMaker endpoint.
    """
    try:
        print(f"Deploying the updated model to endpoint: {endpoint_name}...")
        estimator.deploy(
            initial_instance_count=1,
            instance_type="ml.m5.large",
            endpoint_name=endpoint_name,
            update_endpoint=True
        )
        print(f"Endpoint {endpoint_name} updated successfully.")
    except Exception as e:
        print(f"Error updating endpoint: {e}")

if __name__ == "__main__":
    # Upload new training data
    local_training_data = "./data/new_fraud_data.csv"
    upload_training_data(local_training_data, S3_BUCKET, TRAINING_DATA_PATH)

    # Retrain the model
    trained_estimator = retrain_model()

    # Update the SageMaker endpoint with the retrained model
    if trained_estimator:
        update_endpoint(trained_estimator, ENDPOINT_NAME)
