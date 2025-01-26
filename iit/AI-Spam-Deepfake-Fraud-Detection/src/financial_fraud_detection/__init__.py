"""
financial_fraud_detection

This module provides tools for detecting financial fraud, including anomaly detection using machine learning
and data processing with AWS Glue.
"""

# Import key functions from submodules
from .anomaly_detection import (
    preprocess_data,
    train_anomaly_detection_model,
    detect_anomalies,
)
from .glue_integration import (
    create_glue_job,
    start_glue_job,
    get_glue_job_status,
)

# Define the public API for the package
__all__ = [
    "preprocess_data",
    "train_anomaly_detection_model",
    "detect_anomalies",
    "create_glue_job",
    "start_glue_job",
    "get_glue_job_status",
]
