from flask import Flask, render_template, request


app = Flask(__name__)
@app.route('/')
def feedback_form():
    return render_template('feedback.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    
    # Simple Gmail validation (backend)
    if not email.endswith('@gmail.com'):
        return "Only Gmail addresses are allowed!", 400
    
    return render_template('thank.html', name=name, email=email)

if __name__ == '__main__':
    app.run(debug=True)
