import sqlite3
import hashlib

### Função para gerar o hash da senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest() 

### Função para inserir um novo usuário no banco de dados
def inserir_usuario(username, password):
    hashed_password = hash_password(password)  ### Aplica a função de hash na senha
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Usuarios (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()  ### Confirma a inserção do usuário
        except sqlite3.IntegrityError:
            print("Erro: O nome de usuário já existe.")  ### Trata o erro de nome de usuário duplicado

### Função para autenticar um usuário
def autenticar_usuario(username, password):
    hashed_password = hash_password(password)  ### Aplica a função de hash na senha informada
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE username = ? AND password = ?', (username, hashed_password))
        user = cursor.fetchone()
        return user is not None  ### Retorna True se o usuário existe

### Função para inserir um novo aluno no banco de dados
def inserir_aluno(nome, idade, curso):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Alunos (nome, idade, curso) VALUES (?, ?, ?)', (nome, idade, curso))
            conn.commit()  ### Confirma a inserção do aluno
            print("Aluno inserido com sucesso.")
        except Exception as e:
            print(f"Ocorreu um erro ao inserir aluno: {e}")  ### Exibe mensagem de erro

### Função para inserir uma nova disciplina no banco de dados
def inserir_disciplina(nome, professor):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Disciplinas (nome, professor) VALUES (?, ?)', (nome, professor))
            conn.commit()  ### Confirma a inserção da disciplina
            print("Disciplina inserida com sucesso.")
        except Exception as e:
            print(f"Ocorreu um erro ao inserir disciplina: {e}")  ### Exibe mensagem de erro

### Função para registrar notas de um aluno em uma disciplina
def registrar_nota(nome_aluno, nome_disciplina, simulado1, simulado2, avaliacao, nova_chance=0):
    ### Verifica se as notas estão dentro dos limites especificados
    if not (0 <= simulado1 <= 1 and 0 <= simulado2 <= 1 and 0 <= avaliacao <= 10 and 0 <= nova_chance <= 10):
        print("Erro: As notas estão fora dos limites permitidos.")
        return  ### Interrompe a função se as notas estiverem fora dos limites

    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        
        ### Obtém o ID do aluno
        cursor.execute('SELECT id_aluno FROM Alunos WHERE nome = ?', (nome_aluno,))
        aluno = cursor.fetchone()
        
        ### Obtém o ID da disciplina
        cursor.execute('SELECT id_disciplina FROM Disciplinas WHERE nome = ?', (nome_disciplina,))
        disciplina = cursor.fetchone()

        ### Verifica se o aluno e a disciplina existem
        if aluno and disciplina:
            id_aluno = aluno[0]
            id_disciplina = disciplina[0]
            
            try:
                cursor.execute('''
                    INSERT INTO Notas (id_aluno, id_disciplina, simulado1, simulado2, avaliacao, nova_chance)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (id_aluno, id_disciplina, simulado1, simulado2, avaliacao, nova_chance))
                conn.commit()  ### Confirma a inserção das notas
                print("Notas inseridas com sucesso.")
            except Exception as e:
                print(f"Ocorreu um erro ao registrar notas: {e}")  ### Exibe mensagem de erro
        else:
            print("Erro: Aluno ou disciplina não encontrados.")  ### Mensagem de erro se aluno ou disciplina não forem encontrados

### Função para consultar as notas de um aluno
def consultar_notas(id_aluno, disciplina=None):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        if disciplina:
            cursor.execute('''  ### Consulta específica por disciplina
                SELECT d.nome, n.simulado1, n.simulado2, n.avaliacao, n.nova_chance 
                FROM Notas n
                JOIN Disciplinas d ON n.id_disciplina = d.id_disciplina
                WHERE n.id_aluno = ? AND d.nome = ?
            ''', (id_aluno, disciplina))
        else:
            cursor.execute('''  ### Consulta por todas as disciplinas
                SELECT d.nome, n.simulado1, n.simulado2, n.avaliacao, n.nova_chance 
                FROM Notas n
                JOIN Disciplinas d ON n.id_disciplina = d.id_disciplina
                WHERE n.id_aluno = ?
            ''', (id_aluno,))
        notas = cursor.fetchall()
    return notas  ### Retorna uma lista de tuplas com a disciplina e as notas

### Função para obter todas as disciplinas
def obter_disciplinas():
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT nome FROM Disciplinas')
        disciplinas = cursor.fetchall()
    return [d[0] for d in disciplinas]  ### Retorna apenas os nomes das disciplinas

### Função para obter todos os alunos
def obter_alunos():
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id_aluno, nome FROM Alunos')
        alunos = cursor.fetchall()
    return alunos  ### Retorna uma lista de tuplas com ID e nome dos alunos

### Função para obter todos os cursos
def obter_cursos():
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT curso FROM Alunos')
        cursos = cursor.fetchall()
    return [c[0] for c in cursos]  ### Retorna uma lista com os nomes dos cursos
