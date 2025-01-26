import json
from datetime import datetime

# File-based storage for simplicity (can be replaced with a database)
FEEDBACK_FILE = "user_feedback.json"

def collect_feedback(user_id, feedback_text, rating):
    """
    Collects user feedback and stores it in a file.

    Parameters:
        user_id (str): The ID of the user providing feedback.
        feedback_text (str): The feedback text provided by the user.
        rating (int): The user's rating of the system (1 to 5).

    Returns:
        dict: Confirmation message with feedback details.
    """
    try:
        # Validate input
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        if not feedback_text.strip():
            raise ValueError("Feedback text cannot be empty.")

        # Create feedback entry
        feedback_entry = {
            "user_id": user_id,
            "feedback_text": feedback_text.strip(),
            "rating": rating,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Load existing feedback
        try:
            with open(FEEDBACK_FILE, "r") as file:
                feedback_data = json.load(file)
        except FileNotFoundError:
            feedback_data = []

        # Append new feedback
        feedback_data.append(feedback_entry)

        # Save updated feedback
        with open(FEEDBACK_FILE, "w") as file:
            json.dump(feedback_data, file, indent=4)

        print("Feedback collected successfully!")
        return {
            "status": "success",
            "feedback": feedback_entry
        }

    except Exception as e:
        print(f"Error collecting feedback: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

def get_feedback_summary():
    """
    Provides a summary of collected feedback, including average rating.

    Returns:
        dict: Summary of feedback statistics.
    """
    try:
        # Load feedback data
        with open(FEEDBACK_FILE, "r") as file:
            feedback_data = json.load(file)

        # Calculate summary statistics
        total_feedback = len(feedback_data)
        average_rating = (
            sum(entry["rating"] for entry in feedback_data) / total_feedback
            if total_feedback > 0
            else 0
        )

        return {
            "total_feedback": total_feedback,
            "average_rating": round(average_rating, 2),
            "feedback_count_per_rating": {
                rating: sum(1 for entry in feedback_data if entry["rating"] == rating)
                for rating in range(1, 6)
            },
        }

    except FileNotFoundError:
        return {
            "total_feedback": 0,
            "average_rating": 0,
            "feedback_count_per_rating": {rating: 0 for rating in range(1, 6)},
        }
    except Exception as e:
        print(f"Error generating feedback summary: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

# Test the module
if __name__ == "__main__":
    # Collect feedback
    user_id = "U001"
    feedback_text = "The fraud detection system is very effective and easy to use."
    rating = 5
    collect_feedback(user_id, feedback_text, rating)

    # Get feedback summary
    summary = get_feedback_summary()
    print("\n--- Feedback Summary ---")
    print(json.dumps(summary, indent=4))
