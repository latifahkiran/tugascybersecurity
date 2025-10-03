# vulnerable.py
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# contoh db sederhana
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
conn.commit()

@app.route('/user')
def get_user():
    user_id = request.args.get('id', '')
    # VULNERABLE: langsung menggabungkan input ke query -> SQL injection
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    rows = cursor.fetchall()
    return {'rows': rows}

if __name__ == '__main__':
    app.run()
