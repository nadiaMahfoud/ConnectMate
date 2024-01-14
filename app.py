from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'secret_key'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    location = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, first_name, last_name, phone, mobile, email, location, password):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.mobile = mobile
        self.email = email
        self.location = location
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle form submission
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        mobile = request.form['mobile']
        email = request.form['email']
        location = request.form['location']
        password = request.form['password']
        password2 = request.form['password2']

        # Validate the password
        if password != password2:
            return render_template('signup.html', error='Passwords do not match')

        # Create a new user
        new_user = User(
          first_name=first_name,
          last_name=last_name,
          phone=phone, mobile=mobile,
          email=email,
          location=location,
          password=password
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
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

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard6.html', user=user)

    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)