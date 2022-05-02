from crypt import methods
from distutils.log import debug
from enum import unique
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session, Response
#from pymysql import cursors,connect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin_1:Hi6ky7sC!@movies.cxxu1vwhuriz.us-east-1.rds.amazonaws.com/sys"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)



class movies_watched(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)

    def __init__(self, movie_id):
        self.movie_id = movie_id
    def __repr__(self):
        return f"movie_id : {self.movie_id}"
class movies_watching(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)

    def __init__(self, movie_id):
        self.movie_id = movie_id
    def __repr__(self):
        return f"movie_id : {self.movie_id}"
class MoviesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'movie_id')
        
movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many = True)

@app.route('/')
def index():
    return "idk"

@app.route("/get", methods= ['GET'])
def get_movie():
    movies = movies_watched.query.all()
    results =movies_schema.dump(movies)
    return jsonify(results)


@app.route("/insert_movie", methods = ["GET","POST"])
def insert_movies():
    if request.method == "POST":
        id = request.form.get("movie_id")
        movie = movies_watched(movie_id = id)
        try:    
            db.session.add(movie)
            db.session.commit()
            return movie_schema.jsonify(movie)
        except:
            return "an error occurred"
    else:
        return("error?")

@app.route("/watchinglist", methods = ["GET","POST"])
def insert_watchinglist():
    if request.method =="POST":
        id = request.form.get("movie_id")
        movie = movies_watching(movie_id = id)
        try:    
            db.session.add(movie)
            db.session.commit()
            movie_schema.dump(movie)
            return "done"
        except:
            return "an error occurred"
    else:
        return("error?")
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique =True)
    email = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(32), unique=True)

    def __init__(self, username, email, password):
        self.username=username
        self.email=email
        self.password=password
    def __repr__(self) -> str:
        return f"username: {self.username}, email: {self.email}, password:{self.password}"
class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username')
        
user_schema = UsersSchema()
users_schema = UsersSchema(many = True)

@app.route("/newuser", methods = ["GET","POST"])
def addUser():
    if request.method=="POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        users = user(username=username, email=email, password=password)
        try:
            db.session.add(users)
            db.session.commit()
            return 'done'
        except:
            return "error here?"
    else:
        return "error in else statement"
@app.route("/getUsers", methods= ['GET'])
def get_users():
    users = user.query.all()
    results =users_schema.dump(users)
    return jsonify(results)
'''
@app.route('/delete/<int:id>')
def erase(id):
    # deletes the data on the basis of unique id and
    # directs to home page
    data = movies_watched.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')
'''


#TRY USING MOVIE_SCHEMA TO SEE IF IT ADDS

if __name__ == "__main__":
    app.debug= True
    app.run()
