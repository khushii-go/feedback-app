from flask import Flask, render_template, request, redirect, flash, url_for
import csv
import os
import logging

app = Flask(__name__)
app.secret_key = "dev_secret_change_this"

# Configure logging to console (Render shows this in the "Logs" tab)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CSV_FILE = "feedback.csv"

# Create CSV file with header if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Email", "Feedback"])

@app.route("/", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        feedback_text = request.form.get("feedback", "").strip()

        # Log the feedback to console (will be visible in Render logs)
        logging.info(f"Feedback submitted: Name={name}, Email={email}, Feedback={feedback_text}")

        # Validate form fields
        if not name or not email or not feedback_text:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("feedback"))

        # Save feedback to CSV
        try:
            with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([name, email, feedback_text])
        except Exception as e:
            logging.error(f"Error writing to CSV: {e}")
            flash("There was a problem saving your feedback. Please try again.", "error")
            return redirect(url_for("feedback"))

        # Flash success message
        flash("Thank you for your feedback!", "success")
        return redirect(url_for("feedback"))

    return render_template("feedback.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)

