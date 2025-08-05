from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)


def write_to_csv(data):
    with open('feedback.csv', mode='a', newline='') as database:
        name = data["name"]
        email = data["email"]
        feedback = data["feedback"]
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, feedback])


@app.route('/')
def feedback_form():
    return render_template('feedback.html')


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/')
