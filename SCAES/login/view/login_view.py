import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controller.auth_controller import AuthController
from view.main_view import MainView


class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de controle de aluguéis de equipamentos de som")
        self.geometry("490x400")
        self.config(bg="#5f3e34")
        self.auth_controller = AuthController()
        self.centralizar_janela()
        self.create_widgets()

    def centralizar_janela(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        title_label = tk.Label(
            self, text = "Acessar painel", font = ("Helvetica", 20, "bold"), bg = "#5f3e34", fg = "#FFFFFF"
        )
        title_label.pack(pady=15)

        tk.Label(self, text = "Nome de usuário:", fg  = "#f0f0f0", bg = "#5f3e34", font = ("Helvetica", 12, "bold")).pack(pady = (30, 1), padx = 50)
        self.entry_nomeusuario = tk.Entry(self, font = ("Helvetica", 12), width = 30)
        self.entry_nomeusuario.pack(pady=5)

        tk.Label(self, text = "Senha:", fg  = "#f0f0f0", bg = "#5f3e34", font = ("Helvetica", 12, "bold")).pack(pady = (15, 1))
        self.entry_senha = tk.Entry(self, show = "*", font = ("Helvetica", 12), width = 30)
        self.entry_senha.pack(pady=5)

        btn_login = tk.Button(
            self,
            text = "Entrar",
            command = self.login,
            bg = "#007acc",
            fg = "#ffffff",
            font = ("Helvetica", 15),
            width = 20,
            pady = 10,
        )
        btn_login.pack(pady = (30, 3))

        btn_register = tk.Button(
            self,
            text = "Registrar",
            command = self.abrir_tela_cadastro,
            bg = "#41dc8e",
            fg = "#007acc",
            font = ("Helvetica", 14),
            width = 15,
        )
        btn_register.pack(pady=10)

    def login(self):
        nomeusuario = self.entry_nomeusuario.get().strip()
        senha = self.entry_senha.get().strip()

        if not nomeusuario or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
    
        sucesso, user, msg = self.auth_controller.login(nomeusuario, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.destroy()
            MainView(user)
        else:
            messagebox.showerror("Erro", msg)

    def abrir_tela_cadastro(self):
        self.destroy()
        RegisterView()
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from view.register_view import RegisterView 
if __name__ == "__main__":
    app = LoginView()
    app.mainloop()
