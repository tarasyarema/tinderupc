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
    header = request.headers.get("Authorization")
    
    if header:
        token = header.split(" ")[1]
    else:
        return error("No authorization", 401)

    _user_id = jwt.decode(token, SECRET, algorithms=['HS256'])

    users = list(db.users.find({"_id": {"$ne": ObjectId(_user_id["id"])}}))
    data = choices(list(users), k=2)
    data = [{"id": str(u["_id"]), "data": u["meta"]} for u in data]

    return dumps({"data": data})


@app.route("/vote", methods=["POST"])
def vote():
    try:
        content = request.get_json()
        id_a = content["id_a"]
        id_b = content["id_b"]
        win = content["win"]

    except Exception as e:
        log.error(e)
        return error("Wrong data", 400)

    header = request.headers.get("Authorization")
    
    if header:
        token = header.split(" ")[1]
    else:
        return error("No authorization", 401)

    _user_id = jwt.decode(token, SECRET, algorithms=['HS256'])
    _user = db.users.find_one({"_id": ObjectId(_user_id["id"])})  
    
    if _user is None:
        return error("User not found", 404)

    _updated = db.users.update_one(
        {"_id": _user["_id"]},
        update_elo(id_a, id_b, _user["relations"], win))

    log.info(_updated)

    return {"message": "user relations updated"}, 200


@app.route("/ranking", methods=["GET"])
def ranking():
    header = request.headers.get("Authorization")
    
    if header:
        token = header.split(" ")[1]
    else:
        return error("No authorization", 401)

    _user_id = jwt.decode(token, SECRET, algorithms=['HS256'])
    _user = db.users.find_one({"_id": ObjectId(_user_id["id"])})  

    if _user is None:
        return error("User not found", 404)

    _relations_list = [
        {"id": k, "elo": v["elo"]} 
        for k, v in _user["relations"].items()
        ]

    _relations = sorted(_relations_list, 
                        key=lambda x: x["elo"], 
                        reverse=True)

    for r in _relations:
        _tmp = db.users.find_one({"_id": ObjectId(r["id"])})
        if _tmp is None:
            r["user_data"] = {}
        else:
            r["user_data"] = {
                "email": _tmp["email"],
                "meta": _tmp["meta"]
            }

    return dumps({"data": _relations[:5]}), 200


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


@app.route("/login", methods=["POST"])
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
