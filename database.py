import sqlite3

def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (username TEXT PRIMARY KEY,
                       password TEXT,
                       face_data BLOB)''')
    conn.commit()
    conn.close()

def save_user(username, password, face_encoding):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    if cursor.fetchone() is not None:
        print("Error: El nombre de usuario ya está en uso.")
        conn.close()
        return
    
    cursor.execute('INSERT INTO users (username, password, face_data) VALUES (?, ?, ?)',
                   (username, password, face_encoding))
    conn.commit()
    conn.close()

def get_user_data(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password, face_data FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    return row
