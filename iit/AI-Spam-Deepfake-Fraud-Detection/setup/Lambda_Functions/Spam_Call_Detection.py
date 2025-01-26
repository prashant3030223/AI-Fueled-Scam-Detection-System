import boto3
import json

# Initialize AWS clients
transcribe_client = boto3.client('transcribe')
comprehend_client = boto3.client('comprehend')

# Configuration
BUCKET_NAME = "your-s3-bucket-name"
PHISHING_KEYWORDS = ["account blocked", "verify your details", "urgent payment", "prize money"]

def transcribe_call(audio_file_uri, job_name):
    """
    Transcribes call audio using AWS Transcribe.
    """
    try:
        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': audio_file_uri},
            MediaFormat='mp3',
            LanguageCode='en-US',
            OutputBucketName=BUCKET_NAME
        )
        print(f"Transcription job started: {job_name}")
        return response
    except Exception as e:
        print(f"Error in transcription job: {e}")
        return None

def fetch_transcription_result(job_name):
    """
    Fetches the transcription result from AWS Transcribe.
    """
    try:
        result = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        if result['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            transcription_url = result['TranscriptionJob']['Transcript']['TranscriptFileUri']
            print(f"Transcription completed. Download results from: {transcription_url}")
            return transcription_url
        else:
            print(f"Transcription job {job_name} not yet completed.")
            return None
    except Exception as e:
        print(f"Error fetching transcription result: {e}")
        return None

def analyze_transcript(transcript_text):
    """
    Analyzes the transcript for spam using NLP and phishing keyword detection.
    """
    try:
        # Detect sentiment using AWS Comprehend
        sentiment_response = comprehend_client.detect_sentiment(
            Text=transcript_text,
            LanguageCode='en'
        )
        sentiment = sentiment_response['Sentiment']

        # Check for phishing keywords
        detected_phrases = [keyword for keyword in PHISHING_KEYWORDS if keyword in transcript_text.lower()]
        is_spam = len(detected_phrases) > 0

        print(f"Sentiment Analysis: {sentiment}")
        print(f"Detected Keywords: {detected_phrases}")
        return is_spam, sentiment, detected_phrases
    except Exception as e:
        print(f"Error analyzing transcript: {e}")
        return False, None, []

def lambda_handler(event, context):
    """
    Lambda function entry point.
    """
    # Parse input
    audio_file_uri = event.get('audio_file_uri')
    job_name = event.get('job_name', 'SpamCallDetectionJob')

    # Step 1: Transcribe the audio file
    transcribe_response = transcribe_call(audio_file_uri, job_name)
    if not transcribe_response:
        return {"status": "error", "message": "Transcription job failed."}

    # Wait for transcription to complete (this can be optimized using an S3 event trigger)
    # Placeholder for polling logic or event-based response
    transcription_url = fetch_transcription_result(job_name)
    if not transcription_url:
        return {"status": "error", "message": "Transcription not yet available."}

    # Step 2: Fetch and process the transcript
    # Simulate transcript content (Replace this with actual S3 fetch logic)
    transcript_text = "Simulated transcript with phishing keywords like urgent payment."

    # Step 3: Analyze the transcript
    is_spam, sentiment, keywords = analyze_transcript(transcript_text)

    # Step 4: Return results
    result = {
        "audio_file_uri": audio_file_uri,
        "is_spam": is_spam,
        "sentiment": sentiment,
        "keywords_detected": keywords
    }
    print(f"Result: {json.dumps(result, indent=4)}")
    return result
