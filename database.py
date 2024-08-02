import sqlite3

def create_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            face_data TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    print("Base de datos inicializada con éxito.")

import sqlite3

def save_user(username, password, face_data):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, face_data) VALUES (?,?,?)', 
                   (username, password, face_data))
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                   (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None
