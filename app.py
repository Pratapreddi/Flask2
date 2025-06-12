from flask import Flask, render_template, request

app = Flask(__name__)

# Route to display form
@app.route('/')
def feedback_form():
    return render_template('student_form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_feedback():
    # Get data from form
    name = request.form.get('name')
    email = request.form.get('email')
    feedback = request.form.get('feedback')

    # Check if any field is empty
    if not name or not email or not feedback:
        return "Please fill in all fields!", 400

    # Save feedback to a text file
    with open('feedback.txt', 'a') as file:
        file.write(f"Name: {name}\nEmail: {email}\nFeedback: {feedback}\n---\n")

    # Render thank you page
    return render_template('thank_you.html', name=name)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
