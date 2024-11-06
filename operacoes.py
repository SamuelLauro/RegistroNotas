import sqlite3

### Função para inserir um novo aluno no banco de dados
def inserir_aluno(nome, curso):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Alunos (nome, curso) 
                VALUES (?, ?)
            ''', (nome, curso))
            conn.commit()  ### Confirma a inserção
            print("Aluno inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Erro: O aluno já existe.")

### Função para inserir uma nova disciplina no banco de dados
def inserir_disciplina(nome, professor):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Disciplinas (nome, professor) 
                VALUES (?, ?)
            ''', (nome, professor))
            conn.commit()  ### Confirma a inserção
            print("Disciplina inserida com sucesso.")
        except sqlite3.IntegrityError:
            print("Erro: A disciplina já existe.")

### Função para registrar notas de um aluno em uma disciplina
def inserir_nota(nome_aluno, nome_disciplina, simulado1, simulado2, avaliacao, nova_chance=0):
    ### Verifica se as notas estão dentro dos limites especificados
    if not (0 <= simulado1 <= 1 and 0 <= simulado2 <= 1 and 0 <= avaliacao <= 10 and 0 <= nova_chance <= 10):
        return "Erro: As notas estão fora dos limites permitidos."

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
                return "Notas inseridas com sucesso."
            except Exception as e:
                return f"Ocorreu um erro ao registrar notas: {e}"
        else:
            return "Erro: Aluno ou disciplina não encontrados."

### Função para calcular a média das notas de um aluno em uma disciplina
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

        ### Verifica se as notas foram encontradas
        if notas is None:
            return "Erro: Notas não encontradas para o aluno e disciplina especificados."

        simulado1, simulado2, avaliacao, nova_chance = notas
        media = (simulado1 + simulado2 + avaliacao) / 3  ### Calcula a média das notas

        ### Considera a nova chance se a média for menor que 6
        if media < 6:
            media = max(media, nova_chance)

        status = "Aprovado" if media >= 6 else "Reprovado"  ### Determina o status
        return {"media": media, "status": status}

### Função para exibir o status do aluno
def exibir_status_aluno(nome_aluno, nome_disciplina):
    resultado = calcular_media(nome_aluno, nome_disciplina)
    if isinstance(resultado, dict):
        print(f"Média: {resultado['media']}, Status: {resultado['status']}")
    else:
        print(resultado)  ### Exibe mensagem de erro se houver

### Função para obter todos os alunos
def obter_alunos():
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_aluno, nome FROM Alunos")
        return cursor.fetchall()  ### Retorna a lista de alunos

### Função para obter todas as disciplinas
def obter_disciplinas():
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id_disciplina, nome FROM Disciplinas")
        return cursor.fetchall()  ### Retorna a lista de disciplinas

### Função para autenticar usuário
def autenticar_usuario(username, password):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE username = ? AND password = ?", (username, password))
        return cursor.fetchone() is not None  ### Retorna True se o usuário existir

### Função para inserir um novo usuário
def inserir_usuario(username, password):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Usuarios (username, password) 
                VALUES (?, ?)
            ''', (username, password))
            conn.commit()  ### Confirma a inserção do usuário
            print("Usuário inserido com sucesso.")
        except sqlite3.IntegrityError:
            print("Erro: O usuário já existe.")

### Função para consultar as notas de um aluno
def consultar_notas(id_aluno):
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT d.nome, n.simulado1, n.simulado2, n.avaliacao, n.nova_chance
            FROM Notas n
            JOIN Disciplinas d ON n.id_disciplina = d.id_disciplina
            WHERE n.id_aluno = ?
        ''', (id_aluno,))
        return cursor.fetchall()  ### Retorna as notas do aluno
