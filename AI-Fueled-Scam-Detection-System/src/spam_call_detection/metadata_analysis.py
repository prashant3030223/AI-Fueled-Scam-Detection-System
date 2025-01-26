import json
import datetime

# Thresholds for spam detection
CALL_FREQUENCY_THRESHOLD = 5  # Maximum number of calls allowed per hour from the same number
CALL_DURATION_THRESHOLD = 10  # Minimum call duration in seconds to avoid short spam calls
BLACKLISTED_NUMBERS = ["+1234567890", "+0987654321"]  # Predefined list of spam numbers

def analyze_call_metadata(call_metadata):
    """
    Analyzes call metadata to identify potential spam calls.
    
    Parameters:
        call_metadata (dict): Dictionary containing metadata of the call.
            Example:
            {
                "caller_id": "+1234567890",
                "receiver_id": "+1987654321",
                "call_duration": 8,
                "call_timestamp": "2025-01-20 10:15:00"
            }
    
    Returns:
        dict: Analysis results indicating if the call is spam and reasons.
    """
    try:
        # Extract metadata
        caller_id = call_metadata.get("caller_id")
        call_duration = call_metadata.get("call_duration", 0)
        call_timestamp = call_metadata.get("call_timestamp")

        # Parse the call timestamp
        call_time = datetime.datetime.strptime(call_timestamp, "%Y-%m-%d %H:%M:%S")

        # Initialize results
        is_spam = False
        reasons = []

        # Rule 1: Check if the caller is in the blacklist
        if caller_id in BLACKLISTED_NUMBERS:
            is_spam = True
            reasons.append("Caller is in the blacklist.")

        # Rule 2: Check call duration
        if call_duration < CALL_DURATION_THRESHOLD:
            is_spam = True
            reasons.append("Call duration is below the threshold.")

        # Rule 3: Check call frequency
        # Simulated call logs for frequency analysis
        simulated_call_logs = [
            {"caller_id": "+1234567890", "timestamp": "2025-01-20 09:15:00"},
            {"caller_id": "+1234567890", "timestamp": "2025-01-20 09:45:00"},
            {"caller_id": "+1234567890", "timestamp": "2025-01-20 10:00:00"},
        ]

        call_count = sum(
            1
            for log in simulated_call_logs
            if log["caller_id"] == caller_id
            and datetime.datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S") > call_time - datetime.timedelta(hours=1)
        )

        if call_count >= CALL_FREQUENCY_THRESHOLD:
            is_spam = True
            reasons.append("Caller exceeded the allowed call frequency.")

        # Return analysis results
        return {
            "caller_id": caller_id,
            "is_spam": is_spam,
            "reasons": reasons,
        }

    except Exception as e:
        return {"error": f"An error occurred during analysis: {e}"}

# Test the function
if __name__ == "__main__":
    sample_metadata = {
        "caller_id": "+1234567890",
        "receiver_id": "+1987654321",
        "call_duration": 8,
        "call_timestamp": "2025-01-20 10:15:00",
    }

    result = analyze_call_metadata(sample_metadata)
    print(json.dumps(result, indent=4))
