from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt

from controllers.auth_controller import auth_controller
from controllers.trip_controller import trip_controller
from models.db import db 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

submitted_messages = []

db.init_app(app)

bcrypt = Bcrypt(app)

with app.app_context():
  db.create_all()


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/index')
def home_page():
  return render_template('index.html')


@app.route('/continue_reading-eu')
def cr_eu():
  return render_template('continue_reading-eu.html')


@app.route('/continue_reading-as')
def cr_as():
  return render_template('continue_reading-as.html')


@app.route('/continue_reading-am')
def cr_am():
  return render_template('continue_reading-am.html')

@app.route('/contact_submit', methods=['POST'])
def contact_submit():
    # Access form data using request.form['field_name']
    name = request.form['contact_name']
    email = request.form['contact_email']
    subject = request.form['contact_subject']
    message = request.form['contact_message']

    # Example: Print form data to console
    print('Name:', name)
    print('Email:', email)
    print('Subject:', subject)
    print('Message:', message)

    # Store the submitted message (for demonstration purposes)
    submitted_messages.append({
        'name': name,
        'email': email,
        'subject': subject,
        'message': message
    })

    # You can add more logic here, such as sending emails, storing data in a database, etc.

    # Redirect to a success page or return a JSON response
    return redirect(url_for('success'))

@app.route('/success')
def success():
    # Render a success page or provide a success message
    return render_template('success.html', messages=submitted_messages)


app.register_blueprint(trip_controller)
app.register_blueprint(auth_controller)



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5001, debug=True)
