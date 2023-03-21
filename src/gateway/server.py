import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth_svc import access
from auth import validate


server = Flask(__name__)
server.config['MONGO_URI'] = os.environ['MONGO_URI']

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route('/login', methods=['POST'])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else: 
        return err
    
@server.route('/upload', methods=['POST'])
def upload():
    access, err = validate.token(request)