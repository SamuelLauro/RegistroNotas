from tkinter import Tk
from interface import SistemaEscola
from db import criar_tabelas  # importar do db.py

if __name__ == "__main__":
    criar_tabelas()  # Cria as tabelas se elas ainda não existirem
    root = Tk()
    app = SistemaEscola(root)  # Inicializa o sistema escolar com a interface gráfica
    root.mainloop()  # Executa o loop principal do tkinter para a interface
