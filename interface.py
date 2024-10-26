import tkinter as tk
from tkinter import messagebox
from usuarios import (
    inserir_aluno,
    inserir_disciplina,
    registrar_nota,
    consultar_notas,
    obter_disciplinas,
    obter_alunos,
    criar_tabela_usuarios,
    autenticar_usuario,
)

class SistemaEscola:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Registro de Notas")
        self.master.geometry("600x400")
        self.login_screen()

    def login_screen(self):
        self.clear_window()

        tk.Label(self.master, text="Login", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.master, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack(pady=5)

        tk.Label(self.master, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.master, text="Login", command=self.login).pack(pady=20)
        tk.Button(self.master, text="Cadastrar Usuário", command=self.cadastrar_usuario).pack(pady=5)

    def cadastrar_usuario(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            try:
                inserir_usuario(username, password)
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Usuário já existe.")
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if autenticar_usuario(username, password):
            self.tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def tela_principal(self):
        self.clear_window()

        tk.Label(self.master, text="Menu Principal", font=("Arial", 24)).pack(pady=20)
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        aluno_menu = tk.Menu(menu)
        menu.add_cascade(label="Alunos", menu=aluno_menu)
        aluno_menu.add_command(label="Cadastrar Aluno", command=self.tela_cadastrar_aluno)

        disciplina_menu = tk.Menu(menu)
        menu.add_cascade(label="Disciplinas", menu=disciplina_menu)
        disciplina_menu.add_command(label="Cadastrar Disciplina", command=self.tela_cadastrar_disciplina)

        nota_menu = tk.Menu(menu)
        menu.add_cascade(label="Notas", menu=nota_menu)
        nota_menu.add_command(label="Cadastrar Notas", command=self.tela_cadastrar_notas)
        nota_menu.add_command(label="Consultar Notas", command=self.tela_consultar_notas)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def tela_cadastrar_aluno(self):
        self.clear_window()
        tk.Label(self.master, text="Cadastrar Aluno", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.master, text="Nome").pack(pady=5)
        self.nome_aluno_entry = tk.Entry(self.master)
        self.nome_aluno_entry.pack(pady=5)

        tk.Label(self.master, text="Idade").pack(pady=5)
        self.idade_aluno_entry = tk.Entry(self.master)
        self.idade_aluno_entry.pack(pady=5)

        tk.Label(self.master, text="Curso").pack(pady=5)
        self.curso_aluno_entry = tk.Entry(self.master)
        self.curso_aluno_entry.pack(pady=5)

        tk.Button(self.master, text="Cadastrar", command=self.cadastrar_aluno).pack(pady=20)

        tk.Button(self.master, text="Voltar", command=self.tela_principal).pack(pady=5)

    def cadastrar_aluno(self):
        nome = self.nome_aluno_entry.get()
        idade = self.idade_aluno_entry.get()
        curso = self.curso_aluno_entry.get()

        if nome and idade and curso:
            try:
                inserir_aluno(nome, idade, curso)
                messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
                self.nome_aluno_entry.delete(0, tk.END)
                self.idade_aluno_entry.delete(0, tk.END)
                self.curso_aluno_entry.delete(0, tk.END)
            except sqlite3.Error as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def tela_cadastrar_disciplina(self):
        self.clear_window()
        tk.Label(self.master, text="Cadastrar Disciplina", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.master, text="Nome da Disciplina").pack(pady=5)
        self.nome_disciplina_entry = tk.Entry(self.master)
        self.nome_disciplina_entry.pack(pady=5)

        tk.Label(self.master, text="Professor").pack(pady=5)
        self.professor_disciplina_entry = tk.Entry(self.master)
        self.professor_disciplina_entry.pack(pady=5)

        tk.Button(self.master, text="Cadastrar", command=self.cadastrar_disciplina).pack(pady=20)

        tk.Button(self.master, text="Voltar", command=self.tela_principal).pack(pady=5)

    def cadastrar_disciplina(self):
        nome = self.nome_disciplina_entry.get()
        professor = self.professor_disciplina_entry.get()

        if nome and professor:
            inserir_disciplina(nome, professor)
            messagebox.showinfo("Sucesso", "Disciplina cadastrada com sucesso!")
            self.nome_disciplina_entry.delete(0, tk.END)
            self.professor_disciplina_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def tela_cadastrar_notas(self):
        self.clear_window()
        tk.Label(self.master, text="Cadastrar Notas", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.master, text="Selecionar Aluno").pack(pady=5)
        self.aluno_var = tk.StringVar()
        self.aluno_menu = tk.OptionMenu(self.master, self.aluno_var, *self.obter_alunos())
        self.aluno_menu.pack(pady=5)

        tk.Label(self.master, text="Selecionar Disciplina").pack(pady=5)
        self.disciplina_var = tk.StringVar()
        self.disciplina_menu = tk.OptionMenu(self.master, self.disciplina_var, *obter_disciplinas())
        self.disciplina_menu.pack(pady=5)

        tk.Label(self.master, text="Simulado (1pt)").pack(pady=5)
        self.simulado_entry = tk.Entry(self.master)
        self.simulado_entry.pack(pady=5)

        tk.Label(self.master, text="Simulado2 (1pt)").pack(pady=5)
        self.simulado2_entry = tk.Entry(self.master)
        self.simulado2_entry.pack(pady=5)

        tk.Label(self.master, text="Avaliando (10pt)").pack(pady=5)
        self.avaliando_entry = tk.Entry(self.master)
        self.avaliando_entry.pack(pady=5)

        tk.Label(self.master, text="AVS (Recuperação 10pt)").pack(pady=5)
        self.avs_entry = tk.Entry(self.master)
        self.avs_entry.pack(pady=5)

        tk.Button(self.master, text="Registrar Notas", command=self.registrar_notas).pack(pady=20)
        tk.Button(self.master, text="Voltar", command=self.tela_principal).pack(pady=5)

    def registrar_notas(self):
        aluno_nome = self.aluno_var.get()
        disciplina_nome = self.disciplina_var.get()
        aluno_id = self.obter_aluno_id(aluno_nome)
        disciplina_id = self.obter_disciplina_id(disciplina_nome)

        if aluno_id and disciplina_id:
            try:
                simulado = float(self.simulado_entry.get())
                simulado2 = float(self.simulado2_entry.get())
                avaliando = float(self.avaliando_entry.get())
                avs = float(self.avs_entry.get())

                # Registrar notas no banco de dados
                registrar_nota(aluno_id, disciplina_id, simulado)
                registrar_nota(aluno_id, disciplina_id, simulado2)
                registrar_nota(aluno_id, disciplina_id, avaliando)
                registrar_nota(aluno_id, disciplina_id, avs)

                messagebox.showinfo("Sucesso", "Notas registradas com sucesso!")
                self.simulado_entry.delete(0, tk.END)
                self.simulado2_entry.delete(0, tk.END)
                self.avaliando_entry.delete(0, tk.END)
                self.avs_entry.delete(0, tk.END)

            except ValueError:
                messagebox.showwarning("Atenção", "Insira valores válidos para as notas.")
        else:
            messagebox.showwarning("Atenção", "Selecione um aluno e uma disciplina.")

    def tela_consultar_notas(self):
        self.clear_window()
        tk.Label(self.master, text="Consultar Notas", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.master, text="Selecionar Aluno").pack(pady=5)
        self.consultar_aluno_var = tk.StringVar()
        self.consultar_aluno_menu = tk.OptionMenu(self.master, self.consultar_aluno_var, *self.obter_alunos())
        self.consultar_aluno_menu.pack(pady=5)

        tk.Label(self.master, text="Selecionar Disciplina").pack(pady=5)
        self.consultar_disciplina_var = tk.StringVar()
        self.consultar_disciplina_menu = tk.OptionMenu(self.master, self.consultar_disciplina_var, *obter_disciplinas())
        self.consultar_disciplina_menu.pack(pady=5)

        tk.Button(self.master, text="Consultar Notas", command=self.exibir_notas).pack(pady=20)
        tk.Button(self.master, text="Voltar", command=self.tela_principal).pack(pady=5)

    def exibir_notas(self):
        aluno_nome = self.consultar_aluno_var.get()
        disciplina_nome = self.consultar_disciplina_var.get()

        aluno_id = self.obter_aluno_id(aluno_nome)

        if aluno_id:
            notas = consultar_notas(aluno_id, disciplina_nome)

            if notas:
                notas_str = "\n".join([str(nota[0]) for nota in notas])
                media = sum([nota[0] for nota in notas]) / len(notas)
                status = "Aprovado" if media >= 6 else "Reprovado"
                messagebox.showinfo("Notas", f"Notas: {notas_str}\nMédia: {media:.2f}\nStatus: {status}")
            else:
                messagebox.showinfo("Notas", "Nenhuma nota encontrada.")
        else:
            messagebox.showwarning("Atenção", "Selecione um aluno válido.")

    def obter_aluno_id(self, aluno_nome):
        alunos = obter_alunos()
        for aluno in alunos:
            if aluno[1] == aluno_nome:
                return aluno[0]  # Retorna o ID do aluno
        return None

    def obter_disciplina_id(self, disciplina_nome):
        disciplinas = obter_disciplinas()
        for disciplina in disciplinas:
            if disciplina[0] == disciplina_nome:
                return disciplina[0]  # Retorna o nome da disciplina
        return None

    def obter_alunos(self):
        return [aluno[1] for aluno in obter_alunos()]

if __name__ == "__main__":
    criar_tabela_usuarios()  # Cria as tabelas se não existirem
    root = tk.Tk()
    app = SistemaEscola(root)
    root.mainloop()
