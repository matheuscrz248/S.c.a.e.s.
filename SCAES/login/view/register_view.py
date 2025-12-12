import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controller.auth_controller import AuthController


class RegisterView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de controle de aluguéis de equipamentos de som")
        self.geometry("490x450")
        self.config(bg="#22222c")
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
            self, text="Cadastro de Novo Usuário", font=("Helvetica", 20, "bold"), bg="#22222c", fg="#FFFFFF",
        )
        title_label.pack(pady=15)

        tk.Label(self, text="Apelido:", bg="#22222c", fg="#FFFFFF", font=("Helvetica", 12, "bold")).pack(pady=(15, 1))
        self.entry_nome = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.entry_nome.pack(pady=5)

        tk.Label(self, text="Nome de usuário:", bg="#22222c", fg="#FFFFFF", font=("Helvetica", 12, "bold")).pack(
            pady=(15, 1), padx=50)
        self.entry_nomeusuario = tk.Entry(self, font=("Helvetica", 12), width=30)
        self.entry_nomeusuario.pack(pady=5)

        tk.Label(self, text="Senha:", bg="#22222c", fg="#FFFFFF", font=("Helvetica", 12, "bold")).pack(pady=(15, 1),
                                                                                                       padx=50)
        self.entry_senha = tk.Entry(self, show="*", font=("Helvetica", 12), width=30)
        self.entry_senha.pack(pady=5)

        btn_register = tk.Button(
            self,
            text="Criar conta",
            command=self.registrar,
            bg="#513063",
            fg="#ffffff",
            font=("Helvetica", 14),
            width=15,
        )
        btn_register.pack(pady=(35, 10))

        btn_back = tk.Button(
            self,
            text="Voltar",
            command=self.voltar_tela_login,
            bg="#392344",
            fg="#ffffff",
            font=("Helvetica", 13),
            width=5,
        )
        btn_back.pack()

    def registrar(self):
        nome = self.entry_nome.get().strip()
        nomeusuario = self.entry_nomeusuario.get().strip()
        senha = self.entry_senha.get().strip()

        if not nomeusuario or not senha or not nome:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        sucesso, msg = self.auth_controller.register(nome, nomeusuario, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.destroy()
            LoginView()
        else:
            messagebox.showerror("Erro", msg)

    def voltar_tela_login(self):
        self.destroy()
        LoginView()


from view.login_view import LoginView
