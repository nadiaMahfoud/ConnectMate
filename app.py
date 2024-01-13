from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(100))

  def __init__(self,email,password):
    self.email = email
    self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
  def check_password(self,password):
    return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
  db.create_all()


@app.route('/')
def hello_world():
  return render_template('home.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
  if request.method == 'POST':
    # handle request
    email = request.form['email']
    password = request.form['password']

    new_user = User(email=email,password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/login')


  return render_template('signup.html')


@app.route("/login",methods=['GET','POST'])
def login():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
        
    if user and user.check_password(password):
      session['email'] = user.email
      return redirect('/dashboard')
    else:
      return render_template('login.html',error='Invalid user')
  
  
  return render_template('login.html')

@app.route('/dashboard')
def dashboard():
  if session['email']:
    user = User.query.filter_by(email=session['email']).first()
    return render_template('dashboard.html',user=user)

  return redirect('/login')

@app.route('/logout')
def logout():
  session.pop('email',None)
  return redirect('/login')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)