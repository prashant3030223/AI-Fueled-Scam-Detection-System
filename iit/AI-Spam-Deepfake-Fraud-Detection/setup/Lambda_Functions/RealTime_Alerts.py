import boto3
import json

# Initialize the SNS client
sns_client = boto3.client('sns')

# Configuration
SNS_TOPIC_ARN = "arn:aws:sns:your-region:your-account-id:fraud-alerts-topic"

def send_alert(message, subject, phone_number=None, email=None):
    """
    Sends a real-time alert using Amazon SNS.
    If both phone_number and email are provided, sends to both.
    """
    try:
        if phone_number:
            sns_client.publish(
                PhoneNumber=phone_number,
                Message=message
            )
            print(f"SMS alert sent to {phone_number}")

        if email:
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=subject,
                Message=message
            )
            print(f"Email alert sent to topic: {SNS_TOPIC_ARN}")

        return {"status": "success", "message": "Alert sent successfully."}
    except Exception as e:
        print(f"Error sending alert: {e}")
        return {"status": "error", "message": str(e)}

def format_alert(transaction_id, anomaly_score, user_id):
    """
    Formats the alert message with transaction details.
    """
    message = (
        f"Suspicious activity detected!\n\n"
        f"Transaction ID: {transaction_id}\n"
        f"Anomaly Score: {anomaly_score}\n"
        f"User ID: {user_id}\n\n"
        f"Please review this transaction immediately."
    )
    return message

def lambda_handler(event, context):
    """
    AWS Lambda function entry point.
    """
    try:
        # Parse input
        transaction_id = event['transaction_id']
        anomaly_score = event['anomaly_score']
        user_id = event['user_id']
        email = event.get('email')  # User's email for notifications
        phone_number = event.get('phone_number')  # User's phone number for SMS

        # Step 1: Format the alert message
        message = format_alert(transaction_id, anomaly_score, user_id)
        subject = "Urgent: Fraudulent Transaction Alert"

        # Step 2: Send the alert
        response = send_alert(message, subject, phone_number, email)

        # Step 3: Log the response and return
        print(f"Alert response: {json.dumps(response)}")
        return response
    except KeyError as e:
        print(f"Missing required parameter: {e}")
        return {"status": "error", "message": f"Missing parameter: {e}"}
    except Exception as e:
        print(f"Error in Lambda handler: {e}")
        return {"status": "error", "message": str(e)}
