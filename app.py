# -- Flask Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import session

## Additional Imports
import datetime as dt
import model as model
import os
#from dotenv import load_dotenv
#load_dotenv()
#from flask_pymongo import PyMongo
MONGO_DBNAME = os.getenv("MONGO_DBNAME")
MONGO_DBUSERNAME = os.getenv("MONGO_DBUSERNAME")
MONGO_DBPASSWORD = os.getenv("MONGO_DBPASSWORD")
MONGO_DBCLUSTER = os.getenv("MONGO_DBCLUSTER","cluster0-kxrbn")

# -- Initialization section --
app = Flask(__name__)
#app.secret_key = os.urandom(24)
app.jinja_env.globals['current_time'] = dt.datetime.now()
app.config['MONGO_DBNAME'] = MONGO_DBNAME
#app.config['MONGO_URI'] = f'mongodb+srv://{MONGO_DBUSERNAME}:{MONGO_DBPASSWORD}@{MONGO_DBCLUSTER}.mongodb.net/{MONGO_DBNAME}?retryWrites=true'
#mongo = PyMongo(app)

# -- Routes --
@app.route('/')
@app.route('/index')
def index():
    data = {
    }
    return render_template('index.html', data=data)


@app.route('/games')
def games():
    data = {
    }
    return render_template('games.html', data=data)

@app.route('/add')
def add():
    data = {
    }
    return render_template('add.html', data=data)

@app.route('/about')
def about():
    data = {}
    return render_template('about.html', data=data)

@app.route('/acc')
def acc():
    data = {}
    return render_template('acc.html', data=data)

@app.route('/signup', methods=["POST", "GET"])
def signup(): 
    if request.method=="GET":
        data = {} 
        return render_template('signup.html', data=data) 
    else: 
        users=mongo.db.Users
        user={"username": request.form["username"]}
        if users.find_one(user) is None:
            user["password"] = request.form["password"]
            users.insert(user)
            session["username"] = user["username"]
            return redirect(url_for("index"))
        else: 
            return redirect(url_for("login"))

@app.route('/login', methods=["POST", "GET"])
def login(): 
    if request.method=="GET":
        data = {} 
        return render_template('login.html', data=data) 
    else: 
        users=mongo.db.Users
        user={"username": request.form["username"]}
        login_user = users.find_one(user)
        if login_user: 
            password=user["password"]
            if request.form["password"] == password:
                session["username"] = user["username"]
                return redirect(url_for("index"))
            else: 
                return redirect(url_for("login"))
        else: 
            return redirect(url_for("signup"))
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
            
app.run(debug=True, host="0.0.0.0", port=80)

