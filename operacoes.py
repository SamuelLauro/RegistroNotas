import sqlite3

def inserir_aluno(nome, curso):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Alunos (nome, curso) 
                VALUES (?, ?)
            ''', (nome, curso))
            conn.commit()
            print("Aluno inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Erro: O aluno já existe.")

def inserir_disciplina(nome, professor):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Disciplinas (nome, professor) 
                VALUES (?, ?)
            ''', (nome, professor))
            conn.commit()
            print("Disciplina inserida com sucesso.")
        except sqlite3.IntegrityError:
            print("Erro: A disciplina já existe.")

def inserir_nota(nome_aluno, nome_disciplina, simulado1, simulado2, avaliacao, nova_chance=0):
    if not (0 <= simulado1 <= 1 and 0 <= simulado2 <= 1 and 0 <= avaliacao <= 10 and 0 <= nova_chance <= 10):
        return "Erro: As notas estão fora dos limites permitidos."

    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT id_aluno FROM Alunos WHERE nome = ?', (nome_aluno,))
        aluno = cursor.fetchone()
        
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
                return "Notas inseridas com sucesso."
            except Exception as e:
                return f"Ocorreu um erro ao registrar notas: {e}"
        else:
            return "Erro: Aluno ou disciplina não encontrados."

def calcular_media(nome_aluno, nome_disciplina):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT simulado1, simulado2, avaliacao, nova_chance
            FROM Notas n
            JOIN Alunos a ON n.id_aluno = a.id_aluno
            JOIN Disciplinas d ON n.id_disciplina = d.id_disciplina
            WHERE a.nome = ? AND d.nome = ?
        ''', (nome_aluno, nome_disciplina))
        notas = cursor.fetchone()

        if notas is None:
            return "Erro: Notas não encontradas para o aluno e disciplina especificados."

        simulado1, simulado2, avaliacao, nova_chance = notas
        media = (simulado1 + simulado2 + avaliacao) / 3

        if media < 6:
            media = max(media, nova_chance)

        status = "Aprovado" if media >= 6 else "Reprovado"
        return {"media": media, "status": status}

def exibir_status_aluno(nome_aluno, nome_disciplina):
    resultado = calcular_media(nome_aluno, nome_disciplina)
    if isinstance(resultado, dict):
        print(f"Média: {resultado['media']}, Status: {resultado['status']}")
    else:
        print(resultado)

def obter_alunos():
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_aluno, nome FROM Alunos")
        return cursor.fetchall()

def obter_disciplinas():
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_disciplina, nome FROM Disciplinas")
        return cursor.fetchall()

def autenticar_usuario(username, password):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE username = ? AND password = ?", (username, password))
        return cursor.fetchone() is not None

def inserir_usuario(username, password):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Usuarios (username, password) 
                VALUES (?, ?)
            ''', (username, password))
            conn.commit()
            print("Usuário inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Erro: O usuário já existe.")

def consultar_notas(id_aluno):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.nome, n.simulado1, n.simulado2, n.avaliacao, n.nova_chance
            FROM Notas n
            JOIN Disciplinas d ON n.id_disciplina = d.id_disciplina
            WHERE n.id_aluno = ?
        ''', (id_aluno,))
        return cursor.fetchall()
