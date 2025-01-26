import unittest
from unittest.mock import patch
from rekognition_integration import analyze_image, analyze_video, get_face_detection_results
from sagemaker_model_training import train_model, deploy_model


class TestDeepfakeDetection(unittest.TestCase):
    @patch("rekognition_integration.rekognition_client.detect_faces")
    def test_analyze_image_success(self, mock_detect_faces):
        """
        Test if the Rekognition analyze_image function successfully detects faces.
        """
        mock_detect_faces.return_value = {
            "FaceDetails": [{"Confidence": 99.5}, {"Confidence": 98.2}]
        }

        bucket_name = "test-bucket"
        image_key = "test-image.jpg"
        result = analyze_image(bucket_name, image_key)

        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["faces"]), 2)
        self.assertEqual(result["faces"][0]["Confidence"], 99.5)

    @patch("rekognition_integration.rekognition_client.detect_faces")
    def test_analyze_image_failure(self, mock_detect_faces):
        """
        Test if the Rekognition analyze_image function handles errors properly.
        """
        mock_detect_faces.side_effect = Exception("Rekognition error")

        bucket_name = "test-bucket"
        image_key = "test-image.jpg"
        result = analyze_image(bucket_name, image_key)

        self.assertEqual(result["status"], "error")
        self.assertIn("Rekognition error", result["message"])

    @patch("rekognition_integration.rekognition_client.start_face_detection")
    def test_analyze_video_success(self, mock_start_face_detection):
        """
        Test if the Rekognition analyze_video function starts a video analysis job.
        """
        mock_start_face_detection.return_value = {"JobId": "test-job-id"}

        bucket_name = "test-bucket"
        video_key = "test-video.mp4"
        sns_topic_arn = "arn:aws:sns:region:account-id:test-topic"
        role_arn = "arn:aws:iam::account-id:role/test-role"
        result = analyze_video(bucket_name, video_key, sns_topic_arn, role_arn)

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["job_id"], "test-job-id")

    @patch("rekognition_integration.rekognition_client.get_face_detection")
    def test_get_face_detection_results(self, mock_get_face_detection):
        """
        Test if the Rekognition get_face_detection_results function retrieves results.
        """
        mock_get_face_detection.return_value = {
            "Faces": [{"Timestamp": 1000, "Face": {"Confidence": 99.9}}]
        }

        job_id = "test-job-id"
        result = get_face_detection_results(job_id)

        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["faces"]), 1)
        self.assertEqual(result["faces"][0]["Timestamp"], 1000)

    @patch("sagemaker_model_training.Estimator.fit")
    def test_train_model(self, mock_fit):
        """
        Test if the train_model function successfully trains a model.
        """
        mock_fit.return_value = None  # Mock fit function does not return anything

        # Assuming train_model is called without arguments
        try:
            model = train_model()
            self.assertIsNotNone(model)
            print("Model training test passed.")
        except Exception as e:
            self.fail(f"train_model raised an exception: {e}")

    @patch("sagemaker_model_training.Estimator.deploy")
    def test_deploy_model(self, mock_deploy):
        """
        Test if the deploy_model function successfully deploys a model.
        """
        mock_deploy.return_value = "mock-predictor"

        # Mock deployment
        try:
            endpoint_name = "test-endpoint"
            predictor = deploy_model(None, endpoint_name)
            self.assertEqual(predictor, "mock-predictor")
            print("Model deployment test passed.")
        except Exception as e:
            self.fail(f"deploy_model raised an exception: {e}")


if __name__ == "__main__":
    unittest.main()
