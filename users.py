from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import os

def login(name, password):
    sql = "SELECT password, id FROM users WHERE name=:name"
    result = db.session.execute(sql, {"name":name})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            session["user_name"] = name
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["user_name"]

def register(name, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name, password) VALUES (:name, :password)"
        db.session.execute(sql, {"name":name, "password":hash_value})
        db.session.commit()
    except:
        return False
    
    return login(name, password)

def add_user_to_scoreboard(username):
    score = 0
    
    sql = "INSERT INTO scoreboard (username, score) VALUES (:username, :score)"
    db.session.execute(sql, {"username":username, "score":score})
    db.session.commit()

def get_scoreboard():
    sql = "SELECT username, score FROM scoreboard ORDER BY score DESC"
    return db.session.execute(sql).fetchall()

def user_id():
    return session.get("user_id", 0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
