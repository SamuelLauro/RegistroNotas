import sqlite3

def criar_tabela_usuarios():
    conn = sqlite3.connect('sistema_escola.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def cadastrar_usuario(username, password):
    conn = sqlite3.connect('sistema_escola.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Usuarios (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def autenticar_usuario(username, password):
    conn = sqlite3.connect('sistema_escola.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuarios WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None  # Retorna True se o usuário foi encontrado
