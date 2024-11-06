import sqlite3
import hashlib

### Função para criar a tabela de usuários no banco de dados
def criar_tabela_usuarios():
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()  # Usando SHA-256 para hash

def cadastrar_usuario(username, password):
    hashed_password = hash_password(password)
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Usuarios (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

### Função para autenticar um usuário
def autenticar_usuario(username, password):
    hashed_password = hash_password(password)
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE username = ? AND password = ?', (username, hashed_password))
        user = cursor.fetchone()
        return user is not None  # Retorna True se o usuário foi encontrado