import unittest
from unittest.mock import patch
from sns_alerts import create_sns_topic, subscribe_to_topic, send_alert
from amplify_ui import app


class TestRealTimeAlerts(unittest.TestCase):
    ### SNS Alerts Tests ###
    @patch("sns_alerts.sns_client.create_topic")
    def test_create_sns_topic(self, mock_create_topic):
        """
        Test if an SNS topic is created successfully.
        """
        mock_create_topic.return_value = {"TopicArn": "arn:aws:sns:region:account-id:TestTopic"}
        result = create_sns_topic("TestTopic")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["topic_arn"], "arn:aws:sns:region:account-id:TestTopic")

    @patch("sns_alerts.sns_client.subscribe")
    def test_subscribe_to_topic(self, mock_subscribe):
        """
        Test if a subscription to an SNS topic is successful.
        """
        mock_subscribe.return_value = {"SubscriptionArn": "arn:aws:sns:region:account-id:TestSubscription"}
        topic_arn = "arn:aws:sns:region:account-id:TestTopic"
        protocol = "email"
        endpoint = "test@example.com"
        result = subscribe_to_topic(topic_arn, protocol, endpoint)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["subscription_arn"], "arn:aws:sns:region:account-id:TestSubscription")

    @patch("sns_alerts.sns_client.publish")
    def test_send_alert(self, mock_publish):
        """
        Test if an alert is sent successfully via SNS.
        """
        mock_publish.return_value = {"MessageId": "12345"}
        topic_arn = "arn:aws:sns:region:account-id:TestTopic"
        subject = "Test Alert"
        message = "This is a test alert message."
        result = send_alert(topic_arn, subject, message)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["message_id"], "12345")

    ### Flask UI Tests ###
    def setUp(self):
        """
        Set up the Flask test client.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        """
        Test if the home page loads successfully.
        """
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Fraud Detection System", response.data)

    def test_report_fraud_get(self):
        """
        Test if the Report Fraud page loads successfully (GET request).
        """
        response = self.app.get("/report-fraud")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Report Suspicious Activity", response.data)

    @patch("sns_alerts.sns_client.publish")
    def test_report_fraud_post(self, mock_publish):
        """
        Test if the Report Fraud form submits successfully (POST request).
        """
        mock_publish.return_value = {"MessageId": "12345"}
        response = self.app.post("/report-fraud", data={
            "user_id": "U001",
            "transaction_id": "T001",
            "details": "Suspicious activity detected."
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Fraud report submitted successfully!", response.data)

    def test_view_alerts(self):
        """
        Test if the View Alerts page loads successfully.
        """
        response = self.app.get("/view-alerts")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Real-Time Alerts", response.data)


if __name__ == "__main__":
    unittest.main()
