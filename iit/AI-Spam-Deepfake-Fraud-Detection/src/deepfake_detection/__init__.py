"""
deepfake_detection

This module contains functionalities for detecting deepfakes using Amazon Rekognition and SageMaker.
It supports both video/image analysis and training/deploying machine learning models for anomaly detection.
"""

# Import key functions and classes from submodules
from .rekognition_integration import (
    analyze_image,
    analyze_video,
    get_face_detection_results,
)
from .sagemaker_model_training import (
    train_model,
    deploy_model,
)

# Define the package's public interface
__all__ = [
    "analyze_image",
    "analyze_video",
    "get_face_detection_results",
    "train_model",
    "deploy_model",
]
