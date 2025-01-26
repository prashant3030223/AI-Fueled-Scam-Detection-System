import pytest
import json
from your_project import (
    analyze_call_metadata,
    analyze_transcript,
    analyze_image,
    analyze_video,
    detect_anomalies,
    send_alert,
    start_glue_job,
)

# Test data for different components
sample_call_metadata = {
    "caller_id": "+1234567890",
    "receiver_id": "+1987654321",
    "call_duration": 15,
    "call_timestamp": "2025-01-20 10:15:00",
}

sample_transcript = """
Hello, this is an urgent message regarding your account.
Your account has been blocked due to suspicious activity.
Please verify your details immediately to regain access.
"""

sample_image_data = {
    "bucket_name": "your-bucket-name",
    "image_key": "path/to/your/image.jpg",
}

sample_video_data = {
    "bucket_name": "your-bucket-name",
    "video_key": "path/to/your/video.mp4",
    "sns_topic_arn": "arn:aws:sns:your-region:your-account-id:fraud-alerts-topic",
    "role_arn": "arn:aws:iam::your-account-id:role/your-role-name",
}

sample_transaction_data = {
    "transaction_id": ["T001", "T002", "T003", "T004", "T005"],
    "user_id": ["U001", "U002", "U001", "U003", "U004"],
    "amount": [150.75, 3000.00, 87.20, 540.00, 1200.50],
    "merchant": ["Amazon", "Tesla", "Netflix", "Walmart", "Google"],
    "timestamp": [
        "2025-01-20 10:00:00",
        "2025-01-20 10:15:00",
        "2025-01-20 12:00:00",
        "2025-01-20 12:30:00",
        "2025-01-20 04:45:00",
    ],
    "status": ["Completed", "Completed", "Completed", "Failed", "Pending"],
}

# Test call metadata analysis (spam detection)
def test_analyze_call_metadata():
    result = analyze_call_metadata(sample_call_metadata)
    assert result["is_spam"] == False, "Call should not be flagged as spam"

# Test transcript analysis for phishing keyword detection
def test_analyze_transcript():
    result = analyze_transcript(sample_transcript)
    assert result["is_spam"] == True, "Transcript should contain phishing keywords"

# Test image analysis for facial recognition using Rekognition
def test_analyze_image():
    result = analyze_image(sample_image_data["bucket_name"], sample_image_data["image_key"])
    assert "faces" in result, "Face detection should be present in the result"

# Test video analysis for face detection using Rekognition
def test_analyze_video():
    result = analyze_video(sample_video_data["bucket_name"], sample_video_data["video_key"], sample_video_data["sns_topic_arn"], sample_video_data["role_arn"])
    assert "job_id" in result, "Video analysis should return a job ID"

# Test anomaly detection in financial transaction data
def test_detect_anomalies():
    from sklearn.ensemble import IsolationForest

    # Simulate training model and detecting anomalies
    model = IsolationForest()
    model.fit(sample_transaction_data["amount"].reshape(-1, 1))
    anomalies = detect_anomalies(model, sample_transaction_data, ["amount"])
    assert anomalies["anomaly"].sum() > 0, "There should be some anomalies detected in the transactions"

# Test sending an alert using SNS
def test_send_alert():
    alert_response = send_alert("arn:aws:sns:your-region:your-account-id:fraud-alerts-topic", "Test Alert", "Suspicious activity detected in account U001")
    assert alert_response["status"] == "success", "Alert should be sent successfully"

# Test Glue job start
def test_start_glue_job():
    job_response = start_glue_job("fraud-detection-job")
    assert "job_run_id" in job_response, "Glue job should start successfully and return a JobRunId"

# Run all tests
if __name__ == "__main__":
    pytest.main()
