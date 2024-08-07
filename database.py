import sqlite3

def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Crear la tabla de usuarios
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (username TEXT PRIMARY KEY,
                       password TEXT,
                       face_data TEXT)''')
    
    # Crear la tabla de archivos relacionados con los usuarios
    cursor.execute('''CREATE TABLE IF NOT EXISTS files
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT,
                       file_path TEXT,
                       FOREIGN KEY (username) REFERENCES users (username))''')
    conn.commit()

    conn.close()

def save_user(username, password, face_encoding):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    if cursor.fetchone() is not None:
        print("Error: El nombre de usuario ya esta en uso")
        conn.close()
        return
    
    cursor.execute('INSERT INTO users (username, password, face_data) VALUES (?, ?, ?)',
                   (username, password, face_encoding))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password, face_data FROM users WHERE username = ?', (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT face_data, username FROM users')
    user_data = cursor.fetchall()
    conn.close()
    return user_data

def save_file_to_db(file_path, username):
    # Crear la conexión y el cursor
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Insertar la ruta del archivo en la base de datos
    cursor.execute('''INSERT INTO user_files (username, file_path)
                        VALUES (?, ?)''', (username, file_path))

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

def load_user_files(username):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT file_path FROM files WHERE username = ?', (username,))
        files = cursor.fetchall()
        conn.close()
        return files
    except Exception as e:
        print(e)
