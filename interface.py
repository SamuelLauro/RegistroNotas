import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from operacoes import (
    inserir_aluno,
    inserir_disciplina,
    inserir_nota,
    consultar_notas,
    obter_disciplinas,
    autenticar_usuario,
    inserir_usuario,
    obter_alunos,
)

# Definições de estilo
BACKGROUND_COLOR = "#eaeaea"
BUTTON_COLOR = "#4CAF50"
BUTTON_HOVER_COLOR = "#45a049"
TEXT_COLOR = "#333333"
LABEL_FONT = ("Arial", 16)
BUTTON_FONT = ("Arial", 14)


class SistemaEscola:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Registro de Notas")
        self.master.geometry("600x400")
        self.master.config(bg=BACKGROUND_COLOR)

        self.username_entry = None
        self.password_entry = None
        self.nome_entry = None
        self.curso_combobox = None
        self.nome_aluno_combobox = None
        self.disciplinas_combobox = None
        self.simulado1_entry = None
        self.simulado2_entry = None
        self.avaliacao_entry = None
        self.nova_chance_entry = None
        self.alunos = []
        self.disciplinas = []

        self.login_screen()

    def create_button(self, text, command):
        button = tk.Button(self.master, text=text, command=command,
                           bg=BUTTON_COLOR, fg="white", font=BUTTON_FONT, relief="raised", borderwidth=2)
        button.pack(pady=10, padx=20, fill='x')
        button.bind("<Enter>", lambda e: button.config(bg=BUTTON_HOVER_COLOR))
        button.bind("<Leave>", lambda e: button.config(bg=BUTTON_COLOR))

    def create_label(self, text, size):
        label = tk.Label(self.master, text=text, font=("Arial", size), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        label.pack(pady=5)

    def create_entry(self, label_text, show=None):
        tk.Label(self.master, text=label_text, bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=5)
        entry = tk.Entry(self.master, show=show, font=("Arial", 12), bd=2, relief="sunken")
        entry.pack(pady=5, padx=20, fill='x')
        return entry

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_window()
        self.create_label("Login", 24)
        self.username_entry = self.create_entry("Username")
        self.password_entry = self.create_entry("Password", show="*")
        self.create_button("Login", self.login)
        self.create_button("Cadastrar Usuário", self.cadastrar_usuario)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if autenticar_usuario(username, password):
            self.tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def cadastrar_usuario(self):
        self.clear_window()
        self.create_label("Cadastrar Usuário", 24)
        self.username_entry = self.create_entry("Username")
        self.password_entry = self.create_entry("Password", show="*")
        self.create_button("Cadastrar", self.registrar_usuario)
        self.create_button("Voltar", self.login_screen)

    def registrar_usuario(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            try:
                inserir_usuario(username, password)
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.login_screen()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Usuário já existe.")
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def tela_principal(self):
        self.clear_window()
        self.create_label("Menu Principal", 24)
        self.create_button("Cadastrar Aluno", self.cadastrar_aluno)
        self.create_button("Cadastrar Disciplina", self.cadastrar_disciplina)
        self.create_button("Registrar Nota", self.registrar_nota)
        self.create_button("Consultar Notas", self.consultar_notas)
        self.create_button("Sair", self.master.quit)

    def cadastrar_aluno(self):
        self.clear_window()
        self.create_label("Cadastrar Aluno", 24)
        self.nome_entry = self.create_entry("Nome")

        # Obter a lista de disciplinas para seleção
        self.disciplinas = obter_disciplinas()  # Lista de tuplas (id, nome)
        self.disciplinas_nomes = [disciplina[1] for disciplina in self.disciplinas]  # Extrai apenas os nomes

        # Combobox para seleção da disciplina
        tk.Label(self.master, text="Curso", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=5)
        self.curso_combobox = ttk.Combobox(self.master, values=self.disciplinas_nomes)
        self.curso_combobox.set("Selecione o Curso")
        self.curso_combobox.pack(pady=5)

        self.create_button("Cadastrar", self.registrar_aluno)
        self.create_button("Voltar", self.tela_principal)

    def registrar_aluno(self):
        nome = self.nome_entry.get()
        curso = self.curso_combobox.get()

        if nome and curso:
            # Encontrar o ID da disciplina selecionada
            id_disciplina = next((disciplina[0] for disciplina in self.disciplinas if disciplina[1] == curso), None)

            if id_disciplina:
                inserir_aluno(nome, id_disciplina)
                messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
                
                if messagebox.askyesno("Cadastrar outro?", "Deseja cadastrar outro aluno?"):
                    self.cadastrar_aluno()
                else:
                    self.tela_principal()
            else:
                messagebox.showwarning("Erro", "Disciplina selecionada não encontrada.")
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente.")

### Função para inserir notas de um aluno
    def cadastrar_disciplina(self):
        self.clear_window()
        self.create_label("Cadastrar Disciplina", 24)
        self.nome_disciplina_entry = self.create_entry("Nome da Disciplina")
        self.professor_entry = self.create_entry("Nome do Professor")
        self.create_button("Cadastrar", self.registrar_disciplina)
        self.create_button("Voltar", self.tela_principal)

### Função para inserir uma nova disciplina no banco de dados
    def registrar_disciplina(self):
        nome_disciplina = self.nome_disciplina_entry.get()
        nome_professor = self.professor_entry.get()

        if nome_disciplina and nome_professor:
            inserir_disciplina(nome_disciplina, nome_professor)
            messagebox.showinfo("Sucesso", "Disciplina cadastrada com sucesso!")
            
            if messagebox.askyesno("Cadastrar outra?", "Deseja cadastrar outra disciplina?"):
                self.cadastrar_disciplina()
            else:
                self.tela_principal()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente.")

    def registrar_nota(self):
        self.clear_window()
        self.create_label("Registrar Nota", 24)

        # Obter alunos e disciplinas com IDs e nomes
        self.alunos = obter_alunos()  # Lista de tuplas (id, nome)
        self.disciplinas = obter_disciplinas()  # Lista de tuplas (id, nome)

        # Extrair apenas os nomes para exibir nas Combobox
        self.alunos_nomes = [aluno[1] for aluno in self.alunos]
        self.disciplinas_nomes = [disciplina[1] for disciplina in self.disciplinas]

        # Combobox para seleção do aluno
        tk.Label(self.master, text="Nome do Aluno", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=5)
        self.nome_aluno_combobox = ttk.Combobox(self.master, values=self.alunos_nomes)
        self.nome_aluno_combobox.set("Selecione o Aluno")
        self.nome_aluno_combobox.pack(pady=5)

        # Combobox para seleção da disciplina
        tk.Label(self.master, text="Nome da Disciplina", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=5)
        self.disciplinas_combobox = ttk.Combobox(self.master, values=self.disciplinas_nomes)
        self.disciplinas_combobox.set("Selecione a Disciplina")
        self.disciplinas_combobox.pack(pady=5)

        # Campos para as notas
        self.simulado1_entry = self.create_entry("Simulado 1 (0 a 1)")
        self.simulado2_entry = self.create_entry("Simulado 2 (0 a 1)")
        self.avaliacao_entry = self.create_entry("Avaliação (0 a 10)")
        self.nova_chance_entry = self.create_entry("Nova Chance (0 a 10)")

        self.create_button("Registrar", self.salvar_nota)
        self.create_button("Voltar", self.tela_principal)

    def salvar_nota(self):
        nome_aluno = self.nome_aluno_combobox.get()
        nome_disciplina = self.disciplinas_combobox.get()

        # Encontrar o ID do aluno e da disciplina com base no nome selecionado
        id_aluno = next((aluno[0] for aluno in self.alunos if aluno[1] == nome_aluno), None)
        id_disciplina = next((disciplina[0] for disciplina in self.disciplinas if disciplina[1] == nome_disciplina), None)

        if id_aluno and id_disciplina:
            try:
                simulado1 = float(self.simulado1_entry.get())
                simulado2 = float(self.simulado2_entry.get())
                avaliacao = float(self.avaliacao_entry.get())
                nova_chance = float(self.nova_chance_entry.get()) if self.nova_chance_entry.get() else 0

                inserir_nota(nome_aluno, nome_disciplina, simulado1, simulado2, avaliacao, nova_chance)
                messagebox.showinfo("Sucesso", "Notas registradas com sucesso!")
                self.tela_principal()
            except ValueError:
                messagebox.showwarning("Erro", "Verifique se todas as notas são números válidos.")
        else:
            messagebox.showwarning("Erro", "Aluno ou disciplina não encontrados.")

    def consultar_notas(self):
        self.clear_window()
        self.create_label("Consultar Notas", 24)

        # Configurar Combobox para seleção de aluno
        self.alunos = obter_alunos()
        self.alunos_nomes = [aluno[1] for aluno in self.alunos]

        tk.Label(self.master, text="Nome do Aluno", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=5)
        self.nome_aluno_combobox = ttk.Combobox(self.master, values=self.alunos_nomes)
        self.nome_aluno_combobox.set("Selecione o Aluno")
        self.nome_aluno_combobox.pack(pady=5)

        # Configurar Combobox para seleção de disciplina
        self.disciplinas = obter_disciplinas()
        self.disciplinas_nomes = [disciplina[1] for disciplina in self.disciplinas]

        tk.Label(self.master, text="Nome da Disciplina", bg=BACKGROUND_COLOR, fg=TEXT_COLOR).pack(pady=5)
        self.nome_disciplina_combobox = ttk.Combobox(self.master, values=self.disciplinas_nomes)
        self.nome_disciplina_combobox.set("Selecione a Disciplina")
        self.nome_disciplina_combobox.pack(pady=5)

        self.create_button("Consultar", self.mostrar_notas)
        self.create_button("Voltar", self.tela_principal)
        
    def mostrar_notas(self):
        nome_aluno = self.nome_aluno_combobox.get()
        nome_disciplina = self.nome_disciplina_combobox.get()

        id_aluno = next((aluno[0] for aluno in self.alunos if aluno[1] == nome_aluno), None)
        id_disciplina = next((disciplina[0] for disciplina in self.disciplinas if disciplina[1] == nome_disciplina), None)

        if id_aluno and id_disciplina:
            notas = consultar_notas(id_aluno)
            if notas:
                media_total = 0
                notas_texto = ""
                for disciplina, simulado1, simulado2, avaliacao, nova_chance in notas:
                    # Substituir a avaliação pela nova chance se a nova chance for maior que a avaliação
                    if nova_chance > avaliacao:
                        avaliacao = nova_chance

                    # Calcular a média
                    media = (simulado1 + simulado2 + avaliacao)

                    # Determinar status
                    status = "Aprovado" if media >= 6 else "Reprovado"

                    notas_texto += f"{disciplina}: Simulado 1: {simulado1}, Simulado 2: {simulado2}, Avaliação: {avaliacao}, Nova Chance: {nova_chance} - Média: {media:.2f} ({status})\n"
                    media_total += media

                media_total /= len(notas)
                notas_texto += f"\nMédia Geral: {media_total:.2f} - {'Aprovado' if media_total >= 6 else 'Reprovado'}"
                messagebox.showinfo("Notas", notas_texto)
            else:
                messagebox.showinfo("Notas", "Nenhuma nota encontrada para este aluno.")
        else:
            messagebox.showwarning("Erro", "Aluno ou disciplina não encontrados.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEscola(root)
    root.mainloop()
