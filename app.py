import os
from flask import Flask, render_template, request, redirect, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

CSV_FILE = 'feedback.csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        feedback = request.form.get('feedback')

        if name and email and feedback:
            file_exists = os.path.isfile(CSV_FILE)
            with open(CSV_FILE, 'a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(['Name', 'Email', 'Feedback'])
                writer.writerow([name, email, feedback])

            flash("Thank you for your feedback!", "success")
            return redirect('/')

    return render_template('feedback.html')

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False') == 'True'
    port = 6060
    print(f" * Running on http://localhost:{port}/")
    app.run(debug=debug_mode, port=port)
