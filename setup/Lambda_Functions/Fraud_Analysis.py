import boto3
import json
import pandas as pd

# Initialize AWS clients
glue_client = boto3.client('glue')
sagemaker_runtime_client = boto3.client('sagemaker-runtime')

# Configuration
SAGEMAKER_ENDPOINT_NAME = "fraud-detection-endpoint"
TRANSACTION_DATA_BUCKET = "your-s3-bucket-name"
TRANSACTION_DATA_KEY = "transactions/transaction_data.csv"
ANOMALY_THRESHOLD = 0.8  # Threshold for anomaly detection confidence

def load_transaction_data(bucket_name, file_key):
    """
    Loads transaction data from an S3 bucket using AWS Glue.
    """
    try:
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        data = pd.read_csv(response['Body'])
        print(f"Loaded transaction data from S3: {bucket_name}/{file_key}")
        return data
    except Exception as e:
        print(f"Error loading transaction data: {e}")
        return None

def prepare_data_for_analysis(dataframe):
    """
    Prepares transaction data for anomaly detection.
    Cleans, filters, and formats the data as needed.
    """
    try:
        # Example preprocessing steps
        dataframe = dataframe.dropna()  # Remove rows with missing values
        dataframe = dataframe[['transaction_id', 'amount', 'merchant', 'timestamp', 'user_id']]  # Select relevant columns
        print(f"Data prepared for analysis: {dataframe.head()}")
        return dataframe
    except Exception as e:
        print(f"Error preparing data: {e}")
        return None

def invoke_sagemaker_endpoint(payload):
    """
    Invokes the SageMaker endpoint for fraud anomaly detection.
    """
    try:
        response = sagemaker_runtime_client.invoke_endpoint(
            EndpointName=SAGEMAKER_ENDPOINT_NAME,
            ContentType="application/json",
            Body=json.dumps(payload)
        )
        result = json.loads(response['Body'].read().decode())
        print(f"SageMaker response: {result}")
        return result
    except Exception as e:
        print(f"Error invoking SageMaker endpoint: {e}")
        return None

def analyze_transactions(dataframe):
    """
    Analyzes transactions for anomalies using SageMaker.
    """
    anomalies = []
    for _, row in dataframe.iterrows():
        payload = {
            "transaction_id": row['transaction_id'],
            "amount": row['amount'],
            "merchant": row['merchant'],
            "timestamp": row['timestamp'],
            "user_id": row['user_id']
        }
        result = invoke_sagemaker_endpoint(payload)
        if result and result.get('anomaly_score', 0) > ANOMALY_THRESHOLD:
            anomalies.append({
                "transaction_id": row['transaction_id'],
                "anomaly_score": result['anomaly_score']
            })
    return anomalies

def lambda_handler(event, context):
    """
    Lambda function entry point for fraud analysis.
    """
    # Step 1: Load transaction data
    data = load_transaction_data(TRANSACTION_DATA_BUCKET, TRANSACTION_DATA_KEY)
    if data is None:
        return {"status": "error", "message": "Failed to load transaction data."}

    # Step 2: Prepare data for analysis
    prepared_data = prepare_data_for_analysis(data)
    if prepared_data is None:
        return {"status": "error", "message": "Data preparation failed."}

    # Step 3: Analyze transactions for fraud
    anomalies = analyze_transactions(prepared_data)

    # Step 4: Return analysis results
    result = {
        "status": "success",
        "anomalies": anomalies,
        "total_transactions": len(prepared_data),
        "fraudulent_transactions": len(anomalies)
    }
    print(f"Fraud Analysis Result: {json.dumps(result, indent=4)}")
    return result
