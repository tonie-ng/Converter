import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo


server = Flask(__name__)
server.config['MONGO_URI'] = os.environ['MONGO_URI']

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)