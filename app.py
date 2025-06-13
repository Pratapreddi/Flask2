from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    feedback = db.Column(db.Text)

# Route to handle form and display
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        feedback_text = request.form['feedback']

        if not email.endswith('@gmail.com'):
            return "Only Gmail addresses are allowed!", 400

        new_feedback = Feedback(name=name, email=email, feedback=feedback_text)
        db.session.add(new_feedback)
        db.session.commit()

    all_feedback = Feedback.query.all()
    return render_template('form.html', feedbacks=all_feedback)

# Initialize the database
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
