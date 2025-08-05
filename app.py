from flask import Flask, render_template, request, redirect, flash, url_for
import csv
import os

app = Flask(__name__)
# Secret key for flashing messages (change for production)
app.secret_key = "dev_secret_change_this"

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
            print("Error writing to CSV:", e)
            flash("There was a problem saving your feedback. Please try again.", "error")
            return redirect(url_for("feedback"))

        # Flash success message
        flash("Thank you for your feedback!", "success")
        return redirect(url_for("feedback"))

    # For GET request
    return render_template("feedback.html")

if __name__ == "__main__":
    # Runs on port 5001 to avoid macOS Control Center conflict
    app.run(host="0.0.0.0", port=5001, debug=True)
