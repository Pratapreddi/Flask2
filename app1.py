from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# This class represents your table
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    message = db.Column(db.String(200))

# ✅ All DB operations must be inside the app context
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the table if not exists

        # Adding a feedback row
        new_feedback = Feedback(name="Pratap", message="Great session!")
        db.session.add(new_feedback)
        db.session.commit()

    print("Feedback added successfully!")
