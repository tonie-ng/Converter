"""Module  providingFunction printing python version."""

import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

#config
server.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
server.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
server.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
server.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
server.config['MYSQLPORT'] = os.environ.get('MYSQL_PORT')

@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    
    #check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT email, password FROM users WHERE email =%s", (auth.username))

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.password != password or auth.username != email:
            return "Invalid Credentials", 401
        else:
            return create_jwt(auth.username, os.environ.get('JWT_SECRET_KEY'), True)
    else:
        return "Invalid Credentials", 401

def create_jwt(username, secret, authz): 
    return jwt.encode(
        {
           'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        "iat": datetime.datetime.utcnow(),
        "nbf": datetime.datetime.utcnow(),
        "admin": authz 
        },
        secret,
        algorithm='HS256'
        )

if __name__ == "__main__":
    print("Starting server...")

    
