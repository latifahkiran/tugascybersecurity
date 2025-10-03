# vulnerable.py
import sqlite3
from flask import Flask, request
import os
import pickle

app = Flask(__name__)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
conn.commit()

# ALERT 1: SQL Injection
@app.route('/user')
def get_user():
    user_id = request.args.get('id', '')
    query = "SELECT * FROM users WHERE id = " + user_id  # ❌ raw query -> SQL injection
    cursor.execute(query)
    rows = cursor.fetchall()
    return {'rows': rows}

# ALERT 2: Command Injection / Uncontrolled command line
@app.route('/ping')
def ping():
    ip = request.args.get('ip', '')
    os.system("ping -c 1 " + ip)  # ❌ executes shell command built from user input
    return {"status": "done"}

# ALERT 3: Eval / Remote Code Execution pattern
@app.route('/calc')
def calc():
    expr = request.args.get('expr', '')
    # ❌ using eval on user-controlled input -> CodeQL should flag this as RCE risk
    result = eval(expr)
    return {"result": result}

# (optional) Hardcoded secret - may appear under Secret scanning instead
SECRET_KEY = "12345supersecret"

@app.route('/')
def home():
    return "Cyber Security Demo App"
