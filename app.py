"""Blogly application."""

from flask import Flask, render_template,redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import text
from models import db, connect_db,User
import os

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']='abcd'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

app.config["TESTING"] = 'False'
if "TESTING" in os.environ.keys():
    print("Testing Enabled")
    app.config["TESTING"] = os.environ["TESTING"]
    
if app.config["TESTING"] == 'True':
    print("Setting DB as Test")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
else:
    print("Setting DB As Prod")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'

print(app.config['SQLALCHEMY_DATABASE_URI'])
debug= DebugToolbarExtension(app)

    # DB Initialization code
connect_db(app)
#db.create_all()

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/users')
def users_list():
    users = User.query.all()
    return render_template('list.html',users=users)

@app.route('/users/new')
def new_user_form():
    return render_template('form.html')

@app.route('/users/new',methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name =  request.form["last_name"]
    image_url = request.form["image_url"]
    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html',user=user)

@app.route('/users/<int:user_id>/edit',methods=["POST"])
def edit_user(user_id):
    user= User.query.get_or_404(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    user.first_name= first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>/delete',methods=["POST"])
def delete_user(user_id):
    user=User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
