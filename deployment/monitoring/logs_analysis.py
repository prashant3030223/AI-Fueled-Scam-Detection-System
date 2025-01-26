import boto3
import json
from datetime import datetime, timedelta

# Initialize the CloudWatch Logs client
logs_client = boto3.client("logs", region_name="your-region")

# Configuration
LOG_GROUP_NAMES = [
    "/aws/lambda/SpamCallDetection",
    "/aws/lambda/DeepfakeDetection",
    "/aws/lambda/FraudAnalysis",
]
START_TIME = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
END_TIME = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
FILTER_PATTERN = "?ERROR ?WARN ?Exception"

def get_log_events(log_group_name, start_time, end_time, filter_pattern=None):
    """
    Fetches log events from a specific log group.

    Parameters:
        log_group_name (str): The name of the log group to query.
        start_time (str): The start time for the query (ISO 8601 format).
        end_time (str): The end time for the query (ISO 8601 format).
        filter_pattern (str): Optional filter pattern for querying specific logs.

    Returns:
        list: List of log events.
    """
    try:
        start_timestamp = int(datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)
        end_timestamp = int(datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)

        response = logs_client.filter_log_events(
            logGroupName=log_group_name,
            startTime=start_timestamp,
            endTime=end_timestamp,
            filterPattern=filter_pattern or "",
        )

        events = response.get("events", [])
        print(f"Fetched {len(events)} log events from {log_group_name}.")
        return events
    except Exception as e:
        print(f"Error fetching logs for {log_group_name}: {e}")
        return []

def analyze_logs():
    """
    Analyzes logs across multiple log groups and extracts key insights.
    """
    all_logs = []

    for log_group in LOG_GROUP_NAMES:
        print(f"Fetching logs from: {log_group}")
        logs = get_log_events(
            log_group_name=log_group,
            start_time=START_TIME,
            end_time=END_TIME,
            filter_pattern=FILTER_PATTERN,
        )
        all_logs.extend(logs)

    print(f"Total log events fetched: {len(all_logs)}")
    
    # Analyze log data
    error_count = sum(1 for log in all_logs if "ERROR" in log["message"])
    warning_count = sum(1 for log in all_logs if "WARN" in log["message"])
    exception_count = sum(1 for log in all_logs if "Exception" in log["message"])

    # Print summary
    print("\n--- Logs Analysis Summary ---")
    print(f"Total Errors: {error_count}")
    print(f"Total Warnings: {warning_count}")
    print(f"Total Exceptions: {exception_count}")

    # Save detailed logs to a file
    with open("logs_analysis_summary.json", "w") as file:
        json.dump(all_logs, file, indent=4)
    print("Detailed logs saved to logs_analysis_summary.json.")

if __name__ == "__main__":
    analyze_logs()
