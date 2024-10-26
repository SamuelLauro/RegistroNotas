import sqlite3

def criar_tabelas():
    conn = sqlite3.connect('sistema_escola.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Alunos (
        id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        curso TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Disciplinas (
        id_disciplina INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        professor TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Notas (
        id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
        id_aluno INTEGER,
        id_disciplina INTEGER,
        nota REAL NOT NULL,
        FOREIGN KEY (id_aluno) REFERENCES Alunos(id_aluno),
        FOREIGN KEY (id_disciplina) REFERENCES Disciplinas(id_disciplina)
    )
    ''')

    conn.commit()
    conn.close()
