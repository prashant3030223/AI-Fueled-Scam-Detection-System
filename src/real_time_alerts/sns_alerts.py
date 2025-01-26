import boto3
import json

# Initialize the SNS client
sns_client = boto3.client("sns", region_name="your-region")

def create_sns_topic(topic_name):
    """
    Creates an Amazon SNS topic.
    
    Parameters:
        topic_name (str): Name of the SNS topic to create.
    
    Returns:
        dict: Details of the created topic, including the TopicArn.
    """
    try:
        response = sns_client.create_topic(Name=topic_name)
        topic_arn = response.get("TopicArn")
        print(f"SNS topic '{topic_name}' created successfully. ARN: {topic_arn}")
        return {"status": "success", "topic_arn": topic_arn}
    except Exception as e:
        print(f"Error creating SNS topic: {e}")
        return {"status": "error", "message": str(e)}

def subscribe_to_topic(topic_arn, protocol, endpoint):
    """
    Subscribes an email or phone number to the specified SNS topic.
    
    Parameters:
        topic_arn (str): ARN of the SNS topic.
        protocol (str): Protocol for the subscription ("email" or "sms").
        endpoint (str): Endpoint to receive notifications (email address or phone number).
    
    Returns:
        dict: Details of the subscription request.
    """
    try:
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol=protocol,
            Endpoint=endpoint,
        )
        subscription_arn = response.get("SubscriptionArn")
        print(f"Subscription successful. Subscription ARN: {subscription_arn}")
        return {"status": "success", "subscription_arn": subscription_arn}
    except Exception as e:
        print(f"Error subscribing to SNS topic: {e}")
        return {"status": "error", "message": str(e)}

def send_alert(topic_arn, subject, message):
    """
    Publishes a message to the specified SNS topic.

    Parameters:
        topic_arn (str): ARN of the SNS topic.
        subject (str): Subject of the alert (for email notifications).
        message (str): The message to send.

    Returns:
        dict: Details of the publish action, including MessageId.
    """
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message,
        )
        message_id = response.get("MessageId")
        print(f"Alert sent successfully. Message ID: {message_id}")
        return {"status": "success", "message_id": message_id}
    except Exception as e:
        print(f"Error sending alert: {e}")
        return {"status": "error", "message": str(e)}

# Example usage
if __name__ == "__main__":
    # Replace with your configuration
    sns_topic_name = "FraudAlertsTopic"
    sns_email = "user@example.com"
    sns_sms = "+1234567890"

    # Create SNS topic
    topic_response = create_sns_topic(sns_topic_name)
    topic_arn = topic_response.get("topic_arn") if topic_response["status"] == "success" else None

    # Subscribe email and SMS (optional)
    if topic_arn:
        subscribe_to_topic(topic_arn, "email", sns_email)
        subscribe_to_topic(topic_arn, "sms", sns_sms)

    # Send an alert
    if topic_arn:
        alert_response = send_alert(
            topic_arn=topic_arn,
            subject="Urgent Fraud Alert",
            message="Suspicious activity detected in your account. Please review your transactions immediately."
        )
        print(json.dumps(alert_response, indent=4))
