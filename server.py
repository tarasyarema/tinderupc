import os
import logging
import jwt

from random import choices

from datetime import datetime
from dotenv import load_dotenv

from flask import Flask, request, session, redirect

from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

from elo import update_elo

load_dotenv()
log = logging.getLogger(__name__)

SECRET = os.environ["SECRET"]
CLIENT = MongoClient(
    os.environ["MONGO_HOST"],
    int(os.environ["MONGO_PORT"]))
db = CLIENT["tinder"]

app = Flask(__name__)


def error(message="Bad request", code=400):
    return {"message": message}, code


@app.route("/", methods=["GET"])
def index():
    return {"message": "GTFO"}


@app.route("/register", methods=["POST"])
def register():
    try:
        if request.is_json:
            content = request.get_json()
        else:
            content = request.form
        
        email = content["email"]
        password = content["password"]
        lang = content["lang"]
        description = content["description"]

    except Exception as e:
        log.error(e)
        return error("Bad form data")

    _target = db.users.find_one({"email": email})
    
    if _target is not None:
        return error(message="User already exists", code=400)

    user = {
        "email": email,
        "password": password,
        "meta": {
            "lang": lang,
            "description": description
        },
        "relations": {}
    }

    try:
        _user = db.users.insert_one(user)

    except Exception as e:
        log.error(e)
        return error(message="Could not create user")

    _jwt = jwt.encode({"id": str(_user.inserted_id)}, SECRET, algorithm='HS256').decode()
    return {"token": _jwt}, 200


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.is_json:
            content = request.get_json()
        else:
            content = request.form
        
        email = content["email"]
        password = content["password"]

    except Exception as e:
        log.error(e)
        return error("Bad form data")

    _target = db.users.find_one({"email": email})
    
    if _target is None:
        return error(message="User not found", code=404)

    if _target["password"] != password:
        return error(message="Wrong credentials")

    _jwt = jwt.encode({"id": str(_target["_id"])}, SECRET, algorithm='HS256').decode()
    return {"token": _jwt}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
