import unittest
from unittest.mock import patch
from anomaly_detection import train_anomaly_detection_model, detect_anomalies
from metadata_analysis import analyze_call_metadata
from rekognition_integration import analyze_image, analyze_video
from nlp_transcript_analysis import analyze_transcript


class TestFraudDetectionSystem(unittest.TestCase):
    ### Anomaly Detection Tests ###
    @patch("anomaly_detection.IsolationForest.fit")
    def test_train_anomaly_detection_model(self, mock_fit):
        """
        Test if the anomaly detection model is trained successfully.
        """
        mock_fit.return_value = None  # Mock the fit method of IsolationForest
        sample_data = {
            "transaction_id": [1, 2, 3],
            "amount": [100, 200, 300],
            "risk_score": [0.2, 0.8, 0.5],
        }
        feature_columns = ["amount", "risk_score"]

        try:
            model = train_anomaly_detection_model(sample_data, feature_columns)
            self.assertIsNotNone(model)
            print("Anomaly detection model training test passed.")
        except Exception as e:
            self.fail(f"train_anomaly_detection_model raised an exception: {e}")

    @patch("anomaly_detection.IsolationForest.predict")
    def test_detect_anomalies(self, mock_predict):
        """
        Test if the anomalies are detected correctly.
        """
        mock_predict.return_value = [1, -1, 1]  # Simulate anomaly detection
        sample_data = {
            "transaction_id": [1, 2, 3],
            "amount": [100, 200, 300],
            "risk_score": [0.2, 0.8, 0.5],
        }
        feature_columns = ["amount", "risk_score"]

        try:
            anomalies = detect_anomalies(None, sample_data, feature_columns)
            self.assertEqual(sum(anomalies["anomaly"]), 1)  # One anomaly (-1)
            print("Anomaly detection test passed.")
        except Exception as e:
            self.fail(f"detect_anomalies raised an exception: {e}")

    ### Spam Call Detection Tests ###
    def test_analyze_call_metadata_spam(self):
        """
        Test if spam calls are flagged based on metadata.
        """
        call_metadata = {
            "caller_id": "+1234567890",
            "receiver_id": "+1987654321",
            "call_duration": 5,  # Short call duration
            "call_timestamp": "2025-01-22 10:15:00",
        }
        result = analyze_call_metadata(call_metadata)
        self.assertTrue(result["is_spam"])
        self.assertIn("Call duration is below the threshold.", result["reasons"])

    def test_analyze_transcript_spam(self):
        """
        Test if phishing keywords are detected in call transcripts.
        """
        transcript_text = (
            "This is an urgent message regarding your account. "
            "Please verify your details immediately to regain access."
        )
        result = analyze_transcript(transcript_text)
        self.assertTrue(result["is_spam"])
        self.assertIn("Phishing keywords detected.", result["reasons"])

    ### Deepfake Detection Tests ###
    @patch("rekognition_integration.rekognition_client.detect_faces")
    def test_analyze_image_deepfake(self, mock_detect_faces):
        """
        Test if the Rekognition analyze_image function detects faces correctly.
        """
        mock_detect_faces.return_value = {
            "FaceDetails": [{"Confidence": 99.5}, {"Confidence": 98.2}]
        }
        bucket_name = "test-bucket"
        image_key = "test-image.jpg"

        result = analyze_image(bucket_name, image_key)
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["faces"]), 2)

    @patch("rekognition_integration.rekognition_client.start_face_detection")
    def test_analyze_video_deepfake(self, mock_start_face_detection):
        """
        Test if the Rekognition analyze_video function starts a job successfully.
        """
        mock_start_face_detection.return_value = {"JobId": "test-job-id"}
        bucket_name = "test-bucket"
        video_key = "test-video.mp4"
        sns_topic_arn = "arn:aws:sns:region:account-id:test-topic"
        role_arn = "arn:aws:iam::account-id:role/test-role"

        result = analyze_video(bucket_name, video_key, sns_topic_arn, role_arn)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["job_id"], "test-job-id")


if __name__ == "__main__":
    unittest.main()
