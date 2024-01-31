
from flask import Blueprint, redirect, render_template, request, session

from models.user import User, db

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    # Handle form submission
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone = request.form['phone']
    email = request.form['email']
    location = request.form['location']
    password = request.form['password']
    password2 = request.form['password2']

    # Validate the password
    if password != password2:
      return render_template('signup.html', error='Passwords do not match')

    # Create a new user
    new_user = User(first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    email=email,
                    location=location,
                    password=password)
    print(new_user)
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect('/login')

  return render_template('signup.html')


@auth_controller.route('/login', methods=['GET', 'POST'])
def login():
  print("login ", request.form)
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
      session['email'] = user.email
      return redirect('/dashboard')
    else:
      return render_template('login.html', error='Invalid user')

  return render_template('login.html')


@auth_controller.route('/dashboard', methods=['GET'])
def dashboard():
  if 'email' in session:
    user = User.query.filter_by(email=session['email']).first()

    return render_template('dashboard.html', user=user)

  return redirect('/login')

@auth_controller.route('/logout', methods=['DELETE'])
def logout():
  session.pop('email', None)
  return redirect('/login')
