from flask import render_template, flash, redirect, jsonify, request
from flask.ext.login import login_user, logout_user, current_user, login_required, UserMixin
from app import app, login_manager
from forms import LoginForm, AddContactForm, AddUserForm
import pymongo
from pymongo import MongoClient
import datetime
import sys
from models import User
from bson.objectid import ObjectId

MONGODB_URI = 'mongodb://username:password@ds035280.mongolab.com:35280/you-db'  


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = { 'nickname': 'Miguel' }
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    cont = db.contacts
    contacts = cont.find({ "user_id": current_user.id})
    return render_template("index.html",
        title = 'Home',
        user = current_user,
        contacts = contacts)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        client = MongoClient(MONGODB_URI)
        db = client.get_default_database()
        users = db.users
        for user in users.find():
            if user['username'] == form.username.data and user['password'] == form.password.data:
                u = User.get(str(user['_id']))
                login_user(u, remember=True)
                return redirect('index')
                flash("Logged in successfully.")
                return redirect("/index")

    return render_template('login.html', 
        title = 'Sign In',
        form = form)


@app.route('/addcontact', methods = ['GET', 'POST'])
@login_required
def addcontact():
    form = AddContactForm()

    if form.validate_on_submit():
        client = MongoClient(MONGODB_URI)
        db = client.get_default_database()
        contacts = db.contacts
        newContact = {
            "name": form.name.data,
            "number": form.number.data,
            "description": form.description.data,
            "user_id": current_user.id
        }
        contacts.insert(newContact)
        return redirect('/index')
    return render_template('addcontact.html', 
        user = current_user,
        title = 'Add New Contact',
        form = form)


@app.route('/adduser', methods = ['GET', 'POST'])
def adduser():
    form = AddUserForm()

    if form.validate_on_submit():
        client = MongoClient(MONGODB_URI)
        db = client.get_default_database()
        users = db.users
        newUser = {
            "username": form.username.data,
            "password": form.password.data
        }
        users.insert(newUser)
        users = db.users
        for user in users.find():
            if user['username'] == form.username.data and user['password'] == form.password.data:
                u = User.get(str(user['_id']))
                login_user(u, remember=True)
                return redirect('index')
                flash("Logged in successfully.")
                return redirect("/index")
        return redirect('/login')
    return render_template('adduser.html',
        title = 'Add New User',
        form = form)


@app.route('/deletecontact/<contactid>')
@login_required
def deletecontact(contactid):

    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    contacts = db.contacts
    contacts.remove({"_id": ObjectId(contactid), "user_id": current_user.id})
    rContacts = contacts.find({ "user_id": current_user.id})
    return render_template("index.html",
        title = 'Home',
        user = current_user,
        contacts = rContacts)


@login_manager.user_loader
def load_user(userid):
    """
    Flask-Login user_loader callback.
    The user_loader function asks this function to get a User Object or return 
    None based on the userid.
    The userid was stored in the session environment by Flask-Login.  
    user_loader stores the returned User object in current_user during every 
    flask request. 
    """

    return User.get(str(userid))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')