"""
__init__.py

This package contains modules for detecting spam calls, analyzing VKYC deepfakes, and identifying financial fraud.
"""

# Import key functions or classes from submodules
from .metadata_analysis import analyze_call_metadata
from .nlp_transcript_analysis import analyze_transcript
from .real_time_alerts import send_alert
from .fraud_analysis import analyze_transactions
from .deepfake_detection import analyze_video_pattern, analyze_voice_pattern

# Define the package's public interface
__all__ = [
    "analyze_call_metadata",
    "analyze_transcript",
    "send_alert",
    "analyze_transactions",
    "analyze_video_pattern",
    "analyze_voice_pattern",
]
