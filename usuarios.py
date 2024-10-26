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

def inserir_usuario(username, password):
    conn = sqlite3.connect('sistema_escola.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Usuarios (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def autenticar_usuario(username, password):
    conn = sqlite3.connect('sistema_escola.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuarios WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None  # Retorna True se o usuário existe

def inserir_aluno(nome, idade, curso):
    conn = sqlite3.connect('sistema_escola.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Alunos (nome, idade, curso) VALUES (?, ?, ?)', (nome, idade, curso))
    conn.commit()
    conn.close()

def inserir_disciplina(nome, professor):
    conn = sqlite3.connect('sistema_escola.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Disciplinas (nome, professor) VALUES (?, ?)', (nome, professor))
    conn.commit()
    conn.close()

def registrar_nota(id_aluno, id_disciplina, nota):
    conn = sqlite3.connect('sistema_escola.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Notas (id_aluno, id_disciplina, nota) VALUES (?, ?, ?)', (id_aluno, id_disciplina, nota))
    conn.commit()
    conn.close()

def consultar_notas(id_aluno, disciplina):
    conn = sqlite3.connect('sistema_escola.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT n.nota FROM Notas n
        JOIN Disciplinas d ON n.id_disciplina = d.id_disciplina
        WHERE n.id_aluno = ? AND d.nome = ?
    ''', (id_aluno, disciplina))
    notas = cursor.fetchall()
    conn.close()
    return notas

def obter_disciplinas():
    conn = sqlite3.connect('sistema_escola.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM Disciplinas')
    disciplinas = cursor.fetchall()
    conn.close()
    return [d[0] for d in disciplinas]

def obter_alunos():
    conn = sqlite3.connect('sistema_escola.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id_aluno, nome FROM Alunos')
    alunos = cursor.fetchall()
    conn.close()
    return alunos
