from flask import render_template, flash, redirect
from flask.ext.login import login_user, logout_user, current_user, login_required, UserMixin
from app import app
from forms import LoginForm
import pymongo
from pymongo import MongoClient
import datetime
import sys

MONGODB_URI = 'mongodb://username:password@ds035280.mongolab.com:35280/you-db' 

class User(UserMixin):
    """
    User Class for flask-Login
    """
    def __init__(self, userid, username, password):
        self.id = userid
        self.username = username
        self.password = password

    @staticmethod
    def get(userid):
        """
        Static method to search the database and see if userid exists.  If it 
        does exist then return a User Object.  If not then return None as 
        required by Flask-Login. 
        """
        
        client = MongoClient(MONGODB_URI)
        db = client.get_default_database()
        users = db.users
        for user in users.find():
            if str(user["_id"]) == userid:
                return User(str(user['_id']), user["username"], user["password"])
        return None