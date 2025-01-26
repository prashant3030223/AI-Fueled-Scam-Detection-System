"""
feedback_loop

This module manages the feedback loop for the fraud detection system. It includes:
- Collecting user feedback to improve the system.
- Retraining machine learning models based on updated data.
"""

# Import key functions from user_feedback_collector
from .user_feedback_collector import (
    collect_feedback,
    get_feedback_summary,
)

# Import key functions from retrain_model
from .retrain_model import (
    upload_training_data,
    retrain_model,
    update_endpoint,
)

# Define the public API for the package
__all__ = [
    "collect_feedback",
    "get_feedback_summary",
    "upload_training_data",
    "retrain_model",
    "update_endpoint",
]
