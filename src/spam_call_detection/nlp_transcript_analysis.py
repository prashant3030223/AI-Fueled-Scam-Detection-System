import boto3
import json

# Initialize AWS Comprehend client
comprehend_client = boto3.client("comprehend", region_name="your-region")

# Predefined phishing keywords
PHISHING_KEYWORDS = [
    "urgent payment",
    "verify your details",
    "account blocked",
    "prize money",
    "lottery",
    "sensitive information",
    "click the link",
    "immediate action required"
]

def analyze_transcript(transcript_text):
    """
    Analyzes a transcript for spam indicators using NLP.
    
    Parameters:
        transcript_text (str): The transcript text from a call.
    
    Returns:
        dict: Results of the analysis, including spam status, detected keywords, and sentiment.
    """
    try:
        # Initialize results
        is_spam = False
        reasons = []

        # Step 1: Keyword Matching
        detected_keywords = [
            keyword for keyword in PHISHING_KEYWORDS if keyword in transcript_text.lower()
        ]
        if detected_keywords:
            is_spam = True
            reasons.append("Phishing keywords detected.")
        
        # Step 2: Sentiment Analysis with AWS Comprehend
        sentiment_response = comprehend_client.detect_sentiment(
            Text=transcript_text, LanguageCode="en"
        )
        sentiment = sentiment_response.get("Sentiment")
        
        if sentiment == "NEGATIVE":
            is_spam = True
            reasons.append("Negative sentiment detected.")
        
        # Step 3: Return analysis results
        return {
            "is_spam": is_spam,
            "reasons": reasons,
            "detected_keywords": detected_keywords,
            "sentiment": sentiment,
        }

    except Exception as e:
        return {"error": f"An error occurred during analysis: {e}"}

# Test the function
if __name__ == "__main__":
    # Sample transcript text
    sample_transcript = """
    Hello, this is an urgent message regarding your account.
    Your account has been blocked due to suspicious activity.
    Please verify your details immediately to regain access.
    """

    # Analyze the sample transcript
    result = analyze_transcript(sample_transcript)
    print(json.dumps(result, indent=4))
