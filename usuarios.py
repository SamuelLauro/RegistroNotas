import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()  # Usando SHA-256 para hash

def inserir_usuario(username, password):
    hashed_password = hash_password(password)
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Usuarios (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Erro: O nome de usuário já existe.")

def autenticar_usuario(username, password):
    hashed_password = hash_password(password)
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE username = ? AND password = ?', (username, hashed_password))
        user = cursor.fetchone()
        return user is not None  # Retorna True se o usuário existe

def inserir_aluno(nome, idade, curso):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Alunos (nome, idade, curso) VALUES (?, ?, ?)', (nome, idade, curso))
            conn.commit()
            print("Aluno inserido com sucesso.")
        except Exception as e:
            print(f"Ocorreu um erro ao inserir aluno: {e}")

def inserir_disciplina(nome, professor):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Disciplinas (nome, professor) VALUES (?, ?)', (nome, professor))
            conn.commit()
            print("Disciplina inserida com sucesso.")
        except Exception as e:
            print(f"Ocorreu um erro ao inserir disciplina: {e}")

def registrar_nota(nome_aluno, nome_disciplina, simulado1, simulado2, avaliacao, nova_chance=0):
    # Verifica se as notas estão dentro dos limites especificados
    if not (0 <= simulado1 <= 1 and 0 <= simulado2 <= 1 and 0 <= avaliacao <= 10 and 0 <= nova_chance <= 10):
        print("Erro: As notas estão fora dos limites permitidos.")
        return

    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        
        # Obtém o ID do aluno
        cursor.execute('SELECT id_aluno FROM Alunos WHERE nome = ?', (nome_aluno,))
        aluno = cursor.fetchone()
        
        # Obtém o ID da disciplina
        cursor.execute('SELECT id_disciplina FROM Disciplinas WHERE nome = ?', (nome_disciplina,))
        disciplina = cursor.fetchone()

        if aluno and disciplina:
            id_aluno = aluno[0]
            id_disciplina = disciplina[0]
            
            try:
                cursor.execute('''
                    INSERT INTO Notas (id_aluno, id_disciplina, simulado1, simulado2, avaliacao, nova_chance)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (id_aluno, id_disciplina, simulado1, simulado2, avaliacao, nova_chance))
                conn.commit()
                print("Notas inseridas com sucesso.")
            except Exception as e:
                print(f"Ocorreu um erro ao registrar notas: {e}")
        else:
            print("Erro: Aluno ou disciplina não encontrados.")

def consultar_notas(id_aluno, disciplina=None):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        if disciplina:
            cursor.execute('''
                SELECT d.nome, n.simulado1, n.simulado2, n.avaliacao, n.nova_chance 
                FROM Notas n
                JOIN Disciplinas d ON n.id_disciplina = d.id_disciplina
                WHERE n.id_aluno = ? AND d.nome = ?
            ''', (id_aluno, disciplina))
        else:
            cursor.execute('''
                SELECT d.nome, n.simulado1, n.simulado2, n.avaliacao, n.nova_chance 
                FROM Notas n
                JOIN Disciplinas d ON n.id_disciplina = d.id_disciplina
                WHERE n.id_aluno = ?
            ''', (id_aluno,))
        notas = cursor.fetchall()
    return notas  # Retorna uma lista de tuplas com a disciplina e as notas

def obter_disciplinas():
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT nome FROM Disciplinas')
        disciplinas = cursor.fetchall()
    return [d[0] for d in disciplinas]  # Retorna apenas os nomes das disciplinas

def obter_alunos():
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id_aluno, nome FROM Alunos')
        alunos = cursor.fetchall()
    return alunos  # Retorna uma lista de tuplas com ID e nome dos alunos

def obter_cursos():
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT curso FROM Alunos')
        cursos = cursor.fetchall()
    return [c[0] for c in cursos]  # Retorna uma lista com os nomes dos cursos
