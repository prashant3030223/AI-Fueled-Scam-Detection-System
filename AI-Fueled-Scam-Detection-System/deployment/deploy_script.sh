#!/bin/bash

# Exit script on error
set -e

echo "Starting Deployment of AI-Powered Fraud Detection System..."

# Variables
S3_BUCKET="your-s3-bucket-name"
GLUE_SCRIPT_PATH="scripts/transaction_etl.py"
LAMBDA_ROLE_ARN="arn:aws:iam::your-account-id:role/your-lambda-role"
SNS_TOPIC_NAME="FraudAlertsTopic"
LAMBDA_RUNTIME="python3.9"
REGION="your-region"

# 1. Create S3 Bucket
echo "Creating S3 bucket: $S3_BUCKET..."
aws s3 mb s3://$S3_BUCKET --region $REGION

# 2. Upload Glue Script
echo "Uploading Glue ETL script to S3..."
aws s3 cp $GLUE_SCRIPT_PATH s3://$S3_BUCKET/scripts/

# 3. Create SNS Topic
echo "Creating SNS Topic: $SNS_TOPIC_NAME..."
SNS_TOPIC_ARN=$(aws sns create-topic --name $SNS_TOPIC_NAME --query "TopicArn" --output text)
echo "SNS Topic ARN: $SNS_TOPIC_ARN"

# 4. Deploy Lambda Functions
deploy_lambda_function() {
    FUNCTION_NAME=$1
    HANDLER=$2
    ZIP_FILE=$3
    echo "Deploying Lambda function: $FUNCTION_NAME..."
    aws lambda create-function \
        --function-name $FUNCTION_NAME \
        --runtime $LAMBDA_RUNTIME \
        --role $LAMBDA_ROLE_ARN \
        --handler $HANDLER \
        --zip-file fileb://$ZIP_FILE \
        --timeout 60 \
        --memory-size 128
    echo "Lambda function $FUNCTION_NAME deployed successfully."
}

# Package and deploy Lambda functions
echo "Packaging Lambda functions..."
zip Spam_Call_Detection.zip Spam_Call_Detection.py
deploy_lambda_function "SpamCallDetection" "Spam_Call_Detection.lambda_handler" "Spam_Call_Detection.zip"

zip Deepfake_Detection.zip Deepfake_Detection.py
deploy_lambda_function "DeepfakeDetection" "Deepfake_Detection.lambda_handler" "Deepfake_Detection.zip"

zip Fraud_Analysis.zip Fraud_Analysis.py
deploy_lambda_function "FraudAnalysis" "Fraud_Analysis.lambda_handler" "Fraud_Analysis.zip"

# 5. Train SageMaker Model
echo "Training SageMaker model..."
python sagemaker_model_training.py

# 6. Subscribe Email to SNS
EMAIL="user@example.com"
echo "Subscribing $EMAIL to SNS topic..."
aws sns subscribe --topic-arn $SNS_TOPIC_ARN --protocol email --notification-endpoint $EMAIL
echo "Please confirm the subscription in your email."

# 7. Deploy Flask App with Amplify
echo "Deploying Flask app to AWS Amplify..."
amplify init --yes
amplify hosting add --yes
amplify publish

# 8. Cleanup Temporary Files
echo "Cleaning up temporary files..."
rm -f Spam_Call_Detection.zip Deepfake_Detection.zip Fraud_Analysis.zip

echo "Deployment completed successfully!"
