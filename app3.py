import os
from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder to store uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# App configs
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# DB Model
class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    filetype = db.Column(db.String(50))

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded = request.files['file']
        if uploaded:
            filename = secure_filename(uploaded.filename)
            filetype = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded.save(filepath)

            # Save in DB
            file_entry = UploadedFile(filename=filename, filetype=filetype)
            db.session.add(file_entry)
            db.session.commit()

            return redirect(url_for('upload_file'))

    files = UploadedFile.query.all()
    return render_template('upload.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Init DB
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
