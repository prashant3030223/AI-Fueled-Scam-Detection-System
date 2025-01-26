"""
monitoring

This module provides tools for monitoring the AI-powered fraud detection system, including:
- CloudWatch dashboards for real-time monitoring of system metrics.
- Log analysis tools for identifying errors, warnings, and exceptions.
"""

# Import key functions from logs_analysis
from .logs_analysis import analyze_logs, get_log_events

# Define the public API for the package
__all__ = [
    "analyze_logs",
    "get_log_events",
]
