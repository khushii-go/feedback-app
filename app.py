from flask import Flask, render_template, request, redirect
import csv
import logging

app = Flask(__name__)

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


@app.route('/')
def index():
    return render_template('feedback.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        feedback = request.form['feedback']

        with open('feedback.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, feedback])
            logging.info(f"Feedback submitted by: {name}, {email}")

        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
