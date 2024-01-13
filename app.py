from flask import Flask, render_template, jsonify

app = Flask(__name__)

COUNTRIES = [
  {
    'id': 1,
    'name': 'Morocco',
    'capital': 'Rabat',
  },
 {
  'id': 2,
  'name': 'USA',
  'capital': 'Washington DC',
 },
  {
    'id': 3,
    'name': 'Canada',
    'capital': 'Ottawa',
  },
  {
    'id': 4,
    'name': 'Australia',
    'capital': 'Canberra',
  },
  {
    'id': 5,
    'name': 'France',
    'capital': 'Paris',
  }
]
@app.route("/")
def hello_world():
  return render_template('home.html', countries=COUNTRIES)

@app.route("/api/login")
def login():
    return render_template('login.html')

@app.route("/api/signup")
def signup():
    return render_template('signup.html')

@app.route("/api/countries")
def list_countries():
  return jsonify(COUNTRIES)
  
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)