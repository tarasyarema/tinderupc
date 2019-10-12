import os
import logging

from random import choices

from datetime import datetime
from dotenv import load_dotenv

from flask import Flask, request, session, redirect, render_template

from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

from elo import update_elo

load_dotenv()
log = logging.getLogger(__name__)

client = MongoClient(
    os.environ["MONGO_HOST"],
    int(os.environ["MONGO_PORT"]))
db = client['tinder']
app = Flask(__name__, template_folder="templates")


@app.route("/error", methods=["GET", "POST"])
def error():
    return render_template("404.html")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        if "logged_in" not in session.keys():
            return redirect('/register')

        if session["logged_in"] is False:
            return redirect('/register')

        users = db.users.find()
        user1, user2 = choices(users, k=2)
        return render_template("index.html",
                               user1=dumps(user1),
                               user2=dumps(user2))
    
    if request.method == 'POST':
        relations = session["session_id"]["relations"]
        
        update_elo(request.data.user1.id,
                   request.data.user2.id, relations, win)
        
        redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]

        except Exception as e:
            log.error(e)
            return redirect("/error")

        user = {
            "email": email,
            "password": password,
            "meta": {},
            "realtions": {}
        }

        try:
            _user = db.users.insert_one(user)

        except Exception as e:
            log.error(e)
            return redirect("/404.html")

        session["logged_in"] = True
        session["user"] = _user
        
        return redirect("/")

    else:
        return redirect("/error")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    elif request.method == "POST":
        try:
            email = request.form["email"]
            password = request.form["password"]

        except Exception as e:
            log.error(e)
            return redirect("/error")

        target = db.users.find_one({"email": email})

        if target is None:
            return redirect("/error")

        if target["password"] == password:
            session["logged_in"] = True
            session["user"] = target

        else:
            return redirect("/error")

        return redirect("/")

    else:
        return redirect("/error")


if __name__ == "__main__":
    app.secret_key = os.environ["SECRET"]
    app.run(host="0.0.0.0", port=5000, debug=True)
