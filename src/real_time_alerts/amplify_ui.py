from flask import Flask, request, jsonify
import boto3

# Initialize Flask app
app = Flask(__name__)

# AWS SNS Configuration
SNS_TOPIC_ARN = "arn:aws:sns:your-region:your-account-id:fraud-alerts-topic"
sns_client = boto3.client("sns", region_name="your-region")

# Amplify UI Route: Home Page
@app.route("/")
def home():
    return """
    <h1>Fraud Detection System</h1>
    <p>Welcome to the Fraud Detection System UI.</p>
    <p><a href="/report-fraud">Report Suspicious Activity</a></p>
    """

# Amplify UI Route: Report Suspicious Activity
@app.route("/report-fraud", methods=["GET", "POST"])
def report_fraud():
    if request.method == "POST":
        # Extract data from the form
        user_id = request.form.get("user_id")
        transaction_id = request.form.get("transaction_id")
        details = request.form.get("details")

        # Validate inputs
        if not user_id or not transaction_id or not details:
            return jsonify({"status": "error", "message": "All fields are required!"}), 400

        # Send the report as an alert using SNS
        try:
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="Suspicious Activity Reported",
                Message=f"User ID: {user_id}\nTransaction ID: {transaction_id}\nDetails: {details}",
            )
            return jsonify({"status": "success", "message": "Fraud report submitted successfully!"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    # Render the form for GET requests
    return """
    <h2>Report Suspicious Activity</h2>
    <form method="POST">
        <label for="user_id">User ID:</label><br>
        <input type="text" id="user_id" name="user_id" required><br><br>
        <label for="transaction_id">Transaction ID:</label><br>
        <input type="text" id="transaction_id" name="transaction_id" required><br><br>
        <label for="details">Details:</label><br>
        <textarea id="details" name="details" rows="4" required></textarea><br><br>
        <input type="submit" value="Submit Report">
    </form>
    """

# Amplify UI Route: View Real-Time Alerts
@app.route("/view-alerts", methods=["GET"])
def view_alerts():
    # Simulated alerts (replace with actual alert fetching from a database or API)
    alerts = [
        {"user_id": "U001", "transaction_id": "T001", "details": "Large transaction flagged."},
        {"user_id": "U002", "transaction_id": "T002", "details": "Login from an unknown device."},
    ]
    alerts_html = "<h2>Real-Time Alerts</h2><ul>"
    for alert in alerts:
        alerts_html += f"<li>User ID: {alert['user_id']}, Transaction ID: {alert['transaction_id']}, Details: {alert['details']}</li>"
    alerts_html += "</ul>"
    return alerts_html

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
