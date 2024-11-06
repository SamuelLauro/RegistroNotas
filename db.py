import sqlite3

def criar_tabelas():
    """Cria as tabelas necessárias no banco de dados."""
    with sqlite3.connect('sistema_escola.db') as conn:
        cursor = conn.cursor()
        
        # Exclui as tabelas se já existirem
        cursor.execute('DROP TABLE IF EXISTS Notas')
        cursor.execute('DROP TABLE IF EXISTS Alunos')
        cursor.execute('DROP TABLE IF EXISTS Disciplinas')
        cursor.execute('DROP TABLE IF EXISTS Usuarios')

        # Criar tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')

        # Criar tabela de alunos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Alunos (
                id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                curso TEXT NOT NULL
            )
        ''')

        # Criar tabela de disciplinas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Disciplinas (
                id_disciplina INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                professor TEXT NOT NULL
            )
        ''')

        # Criar tabela de notas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Notas (
                id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
                id_aluno INTEGER,
                id_disciplina INTEGER,
                simulado1 REAL DEFAULT 0,
                simulado2 REAL DEFAULT 0,
                avaliacao REAL DEFAULT 0,
                nova_chance REAL DEFAULT 0,
                FOREIGN KEY (id_aluno) REFERENCES Alunos(id_aluno),
                FOREIGN KEY (id_disciplina) REFERENCES Disciplinas(id_disciplina)
            )
        ''')
        conn.commit()
        print("Tabelas criadas com sucesso.")

if __name__ == "__main__":
    criar_tabelas()
