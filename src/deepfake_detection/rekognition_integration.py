import boto3
import json

# Initialize AWS Rekognition client
rekognition_client = boto3.client('rekognition', region_name="your-region")

def analyze_image(bucket_name, image_key):
    """
    Analyze an image for facial attributes using Amazon Rekognition.

    Parameters:
        bucket_name (str): Name of the S3 bucket containing the image.
        image_key (str): Key (path) to the image file in the S3 bucket.

    Returns:
        dict: Analysis results, including detected faces and their attributes.
    """
    try:
        response = rekognition_client.detect_faces(
            Image={"S3Object": {"Bucket": bucket_name, "Name": image_key}},
            Attributes=["ALL"]
        )
        faces = response.get("FaceDetails", [])
        print(f"Detected {len(faces)} face(s) in the image.")

        # Return detailed face attributes
        return {"status": "success", "faces": faces}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def analyze_video(bucket_name, video_key, sns_topic_arn, role_arn):
    """
    Analyze a video for face detection using Amazon Rekognition.

    Parameters:
        bucket_name (str): Name of the S3 bucket containing the video.
        video_key (str): Key (path) to the video file in the S3 bucket.
        sns_topic_arn (str): ARN of the SNS topic for job notifications.
        role_arn (str): ARN of the IAM role for Rekognition to access the S3 bucket.

    Returns:
        dict: Job ID for the face detection job.
    """
    try:
        response = rekognition_client.start_face_detection(
            Video={"S3Object": {"Bucket": bucket_name, "Name": video_key}},
            NotificationChannel={"SNSTopicArn": sns_topic_arn, "RoleArn": role_arn}
        )
        job_id = response.get("JobId")
        print(f"Face detection job started with Job ID: {job_id}")
        return {"status": "success", "job_id": job_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_face_detection_results(job_id):
    """
    Retrieve results of a face detection job.

    Parameters:
        job_id (str): ID of the Rekognition face detection job.

    Returns:
        dict: Analysis results, including detected faces.
    """
    try:
        response = rekognition_client.get_face_detection(JobId=job_id)
        faces = response.get("Faces", [])
        print(f"Retrieved results for {len(faces)} face(s) from job ID {job_id}.")
        return {"status": "success", "faces": faces}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Test the functions
if __name__ == "__main__":
    # Example usage for image analysis
    bucket_name = "your-s3-bucket-name"
    image_key = "path/to/your/image.jpg"

    image_result = analyze_image(bucket_name, image_key)
    print(json.dumps(image_result, indent=4))

    # Example usage for video analysis
    video_key = "path/to/your/video.mp4"
    sns_topic_arn = "arn:aws:sns:your-region:your-account-id:your-topic-name"
    role_arn = "arn:aws:iam::your-account-id:role/your-role-name"

    video_result = analyze_video(bucket_name, video_key, sns_topic_arn, role_arn)
    print(json.dumps(video_result, indent=4))

    # Retrieve job results (replace with a real Job ID after processing)
    # job_id = video_result.get("job_id")
    # if job_id:
    #     job_results = get_face_detection_results(job_id)
    #     print(json.dumps(job_results, indent=4))
