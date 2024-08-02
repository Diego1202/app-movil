import sqlite3

import sqlite3

def create_db():

    conn = sqlite3.connect('database.db')
    
    # Crear un cursor
    c = conn.cursor()
    
    # Crear la tabla de usuarios
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    fingerprint TEXT
                 )''')
    
    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()


def save_user(username, password, face_data):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, face_data) VALUES (?,?,?)',(username, password, face_data))
    conn.commit()
    conn.close()
def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

print("Base de datos inicializada con éxito.")