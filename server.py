import os
import logging

from datetime import datetime
from dotenv import load_dotenv

from flask import Flask, request

from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

load_dotenv()
db = None
log = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=["get"])
def index():
   return {}, 200

@app.route("/register", methods=["post"])
def register():
   return {"data": "ok"}, 200


if __name__ == "__main__":
   mongo = MongoClient(
      os.environ["MONGO_HOST"],
      int(os.environ["MONGO_PORT"])
   )

   db = mongo.users

   app.run(host="0.0.0.0", port=5000, debug=True)
