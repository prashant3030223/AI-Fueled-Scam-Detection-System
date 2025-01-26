import boto3
import sagemaker
from sagemaker import get_execution_role
from sagemaker.estimator import Estimator
import os

# Configuration
BUCKET_NAME = "your-s3-bucket-name"
TRAINING_DATA_PATH = "training-data/fraud_detection.csv"  # Path in the S3 bucket
OUTPUT_PATH = f"s3://{BUCKET_NAME}/model-output/"
ROLE_ARN = "arn:aws:iam::your-account-id:role/service-role/AmazonSageMaker-ExecutionRole"
IMAGE_URI = "123456789012.dkr.ecr.your-region.amazonaws.com/your-custom-container"  # Replace with your container URI

# Initialize SageMaker session and role
sagemaker_session = sagemaker.Session()
role = ROLE_ARN  # Replace with your SageMaker execution role ARN

def upload_data(local_path, bucket_name, s3_path):
    """
    Uploads local data to an S3 bucket.
    """
    s3 = boto3.client('s3')
    s3.upload_file(local_path, bucket_name, s3_path)
    print(f"Uploaded {local_path} to s3://{bucket_name}/{s3_path}")


def train_model():
    """
    Train a machine learning model using Amazon SageMaker.
    """
    try:
        # Create the Estimator for training
        estimator = Estimator(
            image_uri=IMAGE_URI,
            role=role,
            instance_count=1,
            instance_type="ml.m5.large",
            output_path=OUTPUT_PATH,
            sagemaker_session=sagemaker_session,
        )

        # Set hyperparameters (example: for an XGBoost model)
        estimator.set_hyperparameters(
            max_depth=5,
            eta=0.2,
            gamma=4,
            min_child_weight=6,
            subsample=0.8,
            objective="binary:logistic",
            num_round=100,
        )

        # Start the training job
        print("Starting training job...")
        estimator.fit({"train": f"s3://{BUCKET_NAME}/{TRAINING_DATA_PATH}"})
        print("Training job completed.")

        return estimator
    except Exception as e:
        print(f"Error during training: {e}")
        return None


def deploy_model(estimator, endpoint_name):
    """
    Deploys the trained model to a SageMaker endpoint for real-time inference.
    """
    try:
        print(f"Deploying model to endpoint: {endpoint_name}...")
        predictor = estimator.deploy(
            initial_instance_count=1,
            instance_type="ml.m5.large",
            endpoint_name=endpoint_name,
        )
        print(f"Model deployed at endpoint: {endpoint_name}")
        return predictor
    except Exception as e:
        print(f"Error during deployment: {e}")
        return None


def main():
    # Ensure your local data is uploaded to S3
    local_data_path = "./data/fraud_detection.csv"
    upload_data(local_data_path, BUCKET_NAME, TRAINING_DATA_PATH)

    # Train the model
    estimator = train_model()
    if not estimator:
        print("Model training failed.")
        return

    # Deploy the model
    endpoint_name = "fraud-detection-endpoint"
    predictor = deploy_model(estimator, endpoint_name)
    if not predictor:
        print("Model deployment failed.")
        return

    print(f"Model training and deployment completed successfully. Endpoint: {endpoint_name}")


if __name__ == "__main__":
    main()
