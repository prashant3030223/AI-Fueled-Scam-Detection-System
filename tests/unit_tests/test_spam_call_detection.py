import unittest
from metadata_analysis import analyze_call_metadata
from nlp_transcript_analysis import analyze_transcript

class TestSpamCallDetection(unittest.TestCase):
    def test_analyze_call_metadata_blacklist(self):
        """
        Test if the call is flagged as spam when the caller is in the blacklist.
        """
        call_metadata = {
            "caller_id": "+1234567890",
            "receiver_id": "+1987654321",
            "call_duration": 15,
            "call_timestamp": "2025-01-20 10:15:00"
        }
        result = analyze_call_metadata(call_metadata)
        self.assertTrue(result["is_spam"])
        self.assertIn("Caller is in the blacklist.", result["reasons"])

    def test_analyze_call_metadata_short_duration(self):
        """
        Test if the call is flagged as spam when the call duration is too short.
        """
        call_metadata = {
            "caller_id": "+1112223333",
            "receiver_id": "+1987654321",
            "call_duration": 5,
            "call_timestamp": "2025-01-20 10:15:00"
        }
        result = analyze_call_metadata(call_metadata)
        self.assertTrue(result["is_spam"])
        self.assertIn("Call duration is below the threshold.", result["reasons"])

    def test_analyze_call_metadata_high_frequency(self):
        """
        Test if the call is flagged as spam when the call frequency exceeds the threshold.
        """
        call_metadata = {
            "caller_id": "+1112223333",
            "receiver_id": "+1987654321",
            "call_duration": 20,
            "call_timestamp": "2025-01-20 10:15:00"
        }
        # Simulate call logs to test frequency
        simulated_call_logs = [
            {"caller_id": "+1112223333", "timestamp": "2025-01-20 09:15:00"},
            {"caller_id": "+1112223333", "timestamp": "2025-01-20 09:45:00"},
            {"caller_id": "+1112223333", "timestamp": "2025-01-20 10:00:00"},
        ]
        # Mock the analyze_call_metadata function's access to call logs
        result = analyze_call_metadata(call_metadata)
        self.assertTrue(result["is_spam"])
        self.assertIn("Caller exceeded the allowed call frequency.", result["reasons"])

    def test_analyze_transcript_phishing_keywords(self):
        """
        Test if transcripts containing phishing keywords are flagged as spam.
        """
        transcript_text = """
        Hello, this is an urgent message regarding your account.
        Your account has been blocked due to suspicious activity.
        Please verify your details immediately to regain access.
        """
        result = analyze_transcript(transcript_text)
        self.assertTrue(result["is_spam"])
        self.assertIn("Phishing keywords detected.", result["reasons"])

    def test_analyze_transcript_negative_sentiment(self):
        """
        Test if transcripts with negative sentiment are flagged as spam.
        """
        transcript_text = """
        This is a very bad situation. You need to act immediately or you will lose your account.
        """
        result = analyze_transcript(transcript_text)
        self.assertTrue(result["is_spam"])
        self.assertIn("Negative sentiment detected.", result["reasons"])

    def test_analyze_transcript_no_spam(self):
        """
        Test if a normal transcript is not flagged as spam.
        """
        transcript_text = """
        Hello, this is a friendly reminder about your upcoming appointment.
        If you have any questions, please contact our office.
        """
        result = analyze_transcript(transcript_text)
        self.assertFalse(result["is_spam"])
        self.assertEqual(len(result["reasons"]), 0)

if __name__ == "__main__":
    unittest.main()
