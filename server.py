import os
import logging

from datetime import datetime
from dotenv import load_dotenv

from flask import Flask, request, session, redirect, render_template

from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

from utils import update_elo 

load_dotenv()
log = logging.getLogger(__name__)

# PyMongo config
client = MongoClient('localhost', 27017)
db = client['tinder-upc']

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == 'GET':
        if not session["logged_in"]:
            return redirect('/login')
        user1 = db.users.aggregate([{$sample: {size:1}}])
        user2 = db.users.aggregate([{$sample: {size:1}}])
        while user1 == user2:
            user2 = db.users.aggregate([{$sample: {size:1}}])

        return render_template("index.html",
                                        user1=user1,
                                        user2=user2)
    if request.method == 'POST':
        relations = dict()
        update_elo(request.data.user1.id, request.data.user2.id,relations, win) 
        redirect('/')

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
         return {"message": "Bad form"}, 400

      print(email, password)
      
      return {"message": "user registered and logged in"}, 200
   
   else:
      return {"message": "wtf"}, 400

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
         return {"message": "Bad from"}, 400

      target = db.find_one({"email": email})

      if target is None:
         return {"message": "user not found"}, 404

      if target["password"] == password:
         session["logged_in"] = True

      else:
         return {"message": "wrong credentials"}, 400

      return {"message": "user logged in"}, 200
   
   else:
      return {"message": "wtf"}, 400

if __name__ == "__main__":
   mongo = MongoClient(
      os.environ["MONGO_HOST"],
      int(os.environ["MONGO_PORT"])
   )

   db = mongo.users

   app.run(host="0.0.0.0", port=5000, debug=True)
