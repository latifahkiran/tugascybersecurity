import sqlite3
from flask import Flask, request

app = Flask(__name__)

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
conn.commit()

# ALERT 1: SQL Injection
@app.route('/user')
def get_user():
    user_id = request.args.get('id', '')
    query = "SELECT * FROM users WHERE id = " + user_id  # ❌ raw query
    cursor.execute(query)
    rows = cursor.fetchall()
    return {'rows': rows}

# ALERT 2: Command Injection (os.system dengan input user)
import os
@app.route('/ping')
def ping():
    ip = request.args.get('ip', '')
    # ❌ langsung eksekusi perintah shell dari input user
    os.system("ping -c 1 " + ip)
    return {"status": "done"}

# ALERT 3: Hardcoded secret
SECRET_KEY = "12345supersecret"   # ❌ key hardcoded, CodeQL/secret-scanning bisa detect

@app.route('/')
def home():
    return "Cyber Security Demo App"
