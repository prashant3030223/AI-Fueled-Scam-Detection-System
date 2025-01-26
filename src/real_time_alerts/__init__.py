"""
real_time_alerts

This module provides functionalities for real-time fraud alerts, including:
- Sending alerts via Amazon SNS.
- A user interface for reporting suspicious activities and viewing alerts using Flask.
"""

# Import key functions from sns_alerts
from .sns_alerts import (
    create_sns_topic,
    subscribe_to_topic,
    send_alert,
)

# Import the Flask app from amplify_ui
from .amplify_ui import app as amplify_ui_app

# Define the public API for the package
__all__ = [
    "create_sns_topic",
    "subscribe_to_topic",
    "send_alert",
    "amplify_ui_app",
]
